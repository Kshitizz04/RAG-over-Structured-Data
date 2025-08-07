# retrieval.py

import os
import pandas as pd
import faiss
import numpy as np
from openai import OpenAI
from typing import List
from utils import format_units
from llm_engine import ask_llm

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Global variables to hold vectors and data
VECTOR_STORE = None
TEXT_CHUNKS = []
DATA_ROWS = []

# 1. Convert a row to a descriptive string
def row_to_text(row: pd.Series) -> str:
    return ", ".join([f"{col}: {row[col]}" for col in row.index])

# 2. Embed a list of texts
def embed_texts(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [e.embedding for e in response.data]

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
