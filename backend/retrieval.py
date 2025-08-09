# retrieval.py

import pandas as pd
import faiss
import numpy as np
from typing import List
from utils import format_units
from llm_engine import ask_llm
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Global variables to hold vectors and data
VECTOR_STORE = None
TEXT_CHUNKS = []
DATA_ROWS = []

# 1. Convert a row to a descriptive string
def row_to_text(row: pd.Series) -> str:
    return ", ".join([f"{col}: {row[col]}" for col in row.index])

# 2. Embed a list of texts
def embed_texts(texts: List[str]) -> List[List[float]]:
    return model.encode(texts).tolist()

# 3. Create the vector store from the uploaded DataFrame
async def index_dataframe(df: pd.DataFrame):
    global VECTOR_STORE, TEXT_CHUNKS, DATA_ROWS

    TEXT_CHUNKS = [row_to_text(row) for _, row in df.iterrows()]
    DATA_ROWS = df.to_dict(orient="records")

    embeddings = embed_texts(TEXT_CHUNKS)
    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))

    VECTOR_STORE = index

# 4. Retrieve top-k similar rows for a query
def retrieve_similar_chunks(query: str, k=3) -> List[str]:
    global VECTOR_STORE, TEXT_CHUNKS

    if VECTOR_STORE is None:
        return ["No data indexed."]

    query_vector = embed_texts([query])[0]
    query_vector = np.array([query_vector]).astype('float32')

    distances, indices = VECTOR_STORE.search(query_vector, k)

    return [TEXT_CHUNKS[i] for i in indices[0]]

# 5. Query LLM with retrieved context
async def query_llm_with_context(question: str, df: pd.DataFrame) -> str:
    # Index the data first
    await index_dataframe(df)
    relevant_chunks = retrieve_similar_chunks(question)

    prompt = f"""
You are a technical assistant working with tabular ship hydrostatic data.

Here is some relevant data from the table:
{chr(10).join(relevant_chunks)}

Now, answer the question in detail using only the data above:
Question: {question}
"""

    response = ask_llm(prompt)
    return format_units(response)

async def extract_chart_details(question: str, df: pd.DataFrame):
    
    columns = ", ".join(df.columns)
    prompt = (
        f"You are an AI assistant. Given the following table columns: {columns}\n"
        f"Extract the chart type (bar, line, scatter), x column, and y column from this question.\n"
        f"Reply with JSON only, no explanation or extra text. "
        f"If you cannot extract, reply exactly: {{\"chart_type\": null, \"x_col\": null, \"y_col\": null}}\n\n"
        f"Question: {question}"
    )
    import json
    response = ask_llm(prompt)
    try:
        details = json.loads(response)
        return details.get("chart_type"), details.get("x_col"), details.get("y_col")
    except Exception:
        return None, None, None
