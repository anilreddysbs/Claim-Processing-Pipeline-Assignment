from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from .models import FinalResponse, ExtractedData
from .graph import app_graph
import uuid
import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path

# Try identifying .env in current or parent directory
env_path = Path(__file__).resolve().parent.parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="PDF Claim Processing Service")

@app.post("/api/process", response_model=FinalResponse)
async def process_claim(claim_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    try:
        # Read the file
        pdf_bytes = await file.read()
        
        # Initialize Graph State
        initial_state = {
            "pdf_bytes": pdf_bytes,
            "claim_id": claim_id,
            "pages_text": {},
            "classification_result": None,
            "extracted_data": None,
            "logs": []
        }

        # Run Graph
        final_state = app_graph.invoke(initial_state)
        
        extracted_data = final_state.get('extracted_data')
        logs = final_state.get('logs')

        return FinalResponse(
            claim_id=claim_id,
            extracted_data=extracted_data,
            agent_logs=logs
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
