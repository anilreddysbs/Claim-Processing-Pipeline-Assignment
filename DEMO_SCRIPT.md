# Demo Script for PDF Claim Processing Service

## Introduction
"Hello, this is a demonstration of the PDF Claim Processing Service built with FastAPI and LangGraph. This service uses a multi-agent system to classify and extract data from medical claim documents."

## Workflow Overview
"This is a PDF Claim Processing System. It uses AI agents to:
1.  **Segregate** pages by type.
2.  **Extract** specific data (Identity, Discharge, Bill).
3.  **Aggregate** results into a structured format.
4.  **Generate** a downloadable PDF report."

## Demonstration
1.  **Show Code**: Briefly show `app/graph.py` to demonstrate the LangGraph structure.
2.  **Run Service**: 
    ```bash
    uvicorn app.main:app --reload
    ```
3.  **Open Frontend**: Navigate to `http://127.0.0.1:8000` in your browser.
4.  **Process Claim**:
    - Enter `CLAIM-123`.
    - Upload `final.pdf` (drag and drop).
    - Click **Process Claim**.
5.  **Show Results**: Explain the extracted data displayed on the UI.
6.  **Download PDF**: Click the **Download Report (PDF)** button and show the generated PDF.
5.  **Mention Groq Speed**: "We switched to Groq for ultra-fast inference, avoiding the rate limits we faced with other providers."

## Conclusion
"This architecture ensures that each agent focuses only on its relevant context, improving accuracy and reducing token usage compared to passing the entire document to a single prompt."
