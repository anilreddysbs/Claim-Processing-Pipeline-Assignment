# Demo Script for PDF Claim Processing Service

## Introduction
"Hello, this is a demonstration of the PDF Claim Processing Service built with FastAPI and LangGraph. This service uses a multi-agent system to classify and extract data from medical claim documents."

## Workflow Overview
"The system follows this workflow:
1.  **Segregator Agent**: Takes the PDF, analyzes each page using Groq (Llama-3.3-70b), and classifies them into types like Claim Form, Discharge Summary, or Itemized Bill.
2.  **Extraction Agents**: specific agents (ID, Discharge, Bill) pick up the relevant pages based on the classification.
3.  **Aggregator**: Combines everything into a final JSON response."

## Demonstration
1.  **Show Code**: Briefly show `app/graph.py` to demonstrate the LangGraph structure.
2.  **Run Service**: 
    ```bash
    uvicorn app.main:app --reload
    ```
3.  **Make Request**: Use Swagger UI (`http://127.0.0.1:8000/docs`) or Curl.
    - Upload `final.pdf`.
    - Set `claim_id` to "CLAIM-123".
    - Execute.
4.  **Show Response**: Explain the JSON output, showing how different sections (Identity, Bill, Discharge) are populated from different pages.
5.  **Mention Groq Speed**: "We switched to Groq for ultra-fast inference, avoiding the rate limits we faced with other providers."

## Conclusion
"This architecture ensures that each agent focuses only on its relevant context, improving accuracy and reducing token usage compared to passing the entire document to a single prompt."
