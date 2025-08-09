from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from ingestion import load_and_parse_file
from retrieval import query_llm_with_context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store current parsed dataframe in memory (for now)
CURRENT_DATAFRAME = None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global CURRENT_DATAFRAME
    CURRENT_DATAFRAME = await load_and_parse_file(file)
    return {"message": "File uploaded and parsed successfully."}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    if CURRENT_DATAFRAME is None:
        return {"error": "No file uploaded yet."}

    answer = await query_llm_with_context(question, CURRENT_DATAFRAME)
    return {"answer": answer}
