# PDF Claim Processing Service

## Overview
This is a FastAPI service designed to process PDF claims using a LangGraph-orchestrated multi-agent system. It segregates PDF pages into various document types and extracts information using specialized agents.

## Features
- **Segregator Agent**: Classifies pages into document types (Claim Form, Discharge Summary, Itemized Bill, etc.).
- **Extraction Agents**:
  - `ID Agent`: Extracts patient identity and policy details.
  - `Discharge Summary Agent`: Extracts diagnosis and admission details.
  - `Itemized Bill Agent`: Extracts line items and calculates totals.
- **Aggregator**: Combines extracted data into a structured JSON response.

## Setup
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables (create `.env`):
    ```
    GROQ_API_KEY=gsk_...
    ```

## Usage
Run the server:
```bash
uvicorn app.main:app --reload
```

## API Endpoint
`POST /api/process`
- **claim_id**: String
- **file**: PDF File

## Demo
See `DEMO_SCRIPT.md` for a walkthrough.
