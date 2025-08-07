import pandas as pd
from fastapi import UploadFile
import io

async def load_and_parse_file(file: UploadFile):
    filename = file.filename.lower()

    contents = await file.read()  # Read the file contents
    df = None

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        elif filename.endswith(".json"):
            df = pd.read_json(io.BytesIO(contents))
        else:
            raise ValueError("Unsupported file type.")

        # Clean column names: remove spaces, lowercase
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        return df

    except Exception as e:
        print("Error while parsing file:", e)
        raise e
