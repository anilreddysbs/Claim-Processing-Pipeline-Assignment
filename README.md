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

1.  **Run the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
2.  **Open the Application**:
    Navigate to `http://127.0.0.1:8000` in your web browser.

3.  **Process a Claim**:
    - Enter a Claim ID.
    - Upload a PDF file.
    - Click **Process Claim**.
    - View extracted data and download the PDF report.

## API Endpoint
`POST /api/process`
- **claim_id**: String
- **file**: PDF File

## Deployment (Render)

This application includes a `Dockerfile` for easy deployment on Render or any Docker-compatible platform.

1.  **Push to GitHub**: Ensure this repository is pushed to your GitHub account.
2.  **Create New Web Service** on Render.
3.  **Connect Repository**: Select this repository.
4.  **Runtime**: Select **Docker**.
5.  **Environment Variables**: add `GROQ_API_KEY` with your API key.
6.  **Deploy**: Render will build the Docker image and start the service.

## Demo
See `DEMO_SCRIPT.md` (local only) for a walkthrough.
