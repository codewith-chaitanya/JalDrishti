from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import logging
from ml_engine import analyze_edna

# Setup basic logging to track errors without leaking them to the user
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 1. FIXED: Restrict origins to specific URLs (update with your actual React URL)
allowed_origins = [
    "http://localhost:3000", 
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"], # Only allow necessary methods
    allow_headers=["*"],
)

# 2. CONSTANTS for security
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB Limit

@app.get("/")
def home():
    return {"message": "EcoScan API is Secure and Running!"}

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    # 3. BUG FIX: Check file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type. Please upload a CSV."
        )

    # 4. BUG FIX: Prevent Memory Exhaustion (DoS)
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 5MB."
        )

    try:
        # 5. BUG FIX: Robust Decoding
        try:
            decoded_content = content.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback for common Excel-style CSVs
            decoded_content = content.decode('latin-1')

        df = pd.read_csv(io.StringIO(decoded_content))

        # Check if DataFrame is empty
        if df.empty:
            return {"status": "error", "message": "The uploaded CSV is empty."}

        # 6. Process data
        results = analyze_edna(df)
        return {"status": "success", "results": results}

    except Exception as e:
        # 7. FIXED: Log the real error for you, but send a generic message to the user
        logger.error(f"Analysis Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during data analysis."
        )
    finally:
        await file.close()