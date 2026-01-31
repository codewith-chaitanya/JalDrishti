from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from ml_engine import analyze_edna

app = FastAPI()

# Allow your friend's React app to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to the React app's URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "EcoScan API is Running! Go to /docs to test."}

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    # 1. Read the uploaded file
    content = await file.read()
    
    # 2. Convert bytes to a Pandas DataFrame
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    # 3. Process the data using our ML Engine
    try:
        results = analyze_edna(df)
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}