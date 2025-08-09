from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from ingestion import load_and_parse_file
from retrieval import query_llm_with_context, extract_chart_details
from chart_generator import generate_chart
import base64

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
    
    chart_type, x_col, y_col = await extract_chart_details(question, CURRENT_DATAFRAME)
    if chart_type and x_col and y_col:
        try:
            buf, description = generate_chart(CURRENT_DATAFRAME, chart_type, x_col, y_col)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            return {
                "type": "chart",
                "chart": img_base64,
                "description": description,
                "chart_type": chart_type,
                "x_col": x_col,
                "y_col": y_col
            }
        except Exception as e:
            return {"error": f"Chart generation failed: {e}"}


    answer = await query_llm_with_context(question, CURRENT_DATAFRAME)
    return {"type": "text","answer": answer}
