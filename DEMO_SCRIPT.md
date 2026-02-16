# PDF Claim Processing Service - Demo Script

## Introduction
"Hello, this is a demonstration of the PDF Claim Processing Service built with FastAPI and LangGraph. This service uses a multi-agent system to classify and extract data from medical claim documents."

## Workflow Overview
"This is a PDF Claim Processing System. It uses AI agents to:
1.  **Segregate** pages by type.
2.  **Extract** specific data (Identity, Discharge, Bill).
3.  **Aggregate** results into a structured format.
4.  **Generate** a downloadable PDF report."

## 2. Architecture & LangGraph Workflow
**Visual**: Open VS Code and show `app/graph.py`. Highlight the `workflow` definition.
**Script**:
"Let's dive into the architecture. I used **LangGraph** to orchestrate this as a stateful graph.

The workflow follows a clear path:
1.  **Start**: The **Segregator** classifies every page.
2.  **Fan-Out**: Based on those classifications, the graph branches out. We trigger the Identity, Discharge, and Bill agents simultaneously.
3.  **Fan-In (Aggregation)**: As each agent finishes, it updates a shared **GraphState**. I implemented a custom 'reducer' function to ensure these concurrent updates are merged correctly without overwriting each other.
4.  **End**: Finally, an **Aggregator** node compiles the JSON response."

## 3. The Segregator Agent
**Visual**: Switch to `app/agents.py` and scroll to `SegregatorAgent`.
**Script**:
"Efficiency is key. Instead of sending the whole PDF to every agent, the **Segregator Agent** acts as the intelligent router.

It analyzes the text content of each page using **Groq's Llama-3.3-70b**. We don't just keyword match; the model understands the *context* of the page to classify it as a 'Discharge Summary', 'Itemized Bill', or 'Identity Document'. 

 This allows us to:
1.  Filter out irrelevant pages (like cover sheets or instructions).
2.  Route specific pages only to the agents that need them, saving on processing time and cost."

## 4. Extraction Agents
**Visual**: Scroll down to `IdentityExtractionAgent` or `ItemizedBillExtractionAgent` in `app/agents.py`.
**Script**:
"Once the pages are segregated, our specialized **Extraction Agents** kick in. These are designed to be experts in their specific domains:

-   **Identity Agent**: Focuses solely on patient demographics and policy details.
-   **Discharge Summary Agent**: Extracts clinical data like diagnosis and admission dates.
-   **Itemized Bill Agent**: This is the most complex one. It parses table structures to extract line items and costs.

Critically, these agents run in **PARALLEL**. Thanks to LangGraph, we don't wait for one to finish before starting the next. This parallel execution significantly reduces the total processing time for large documents."

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
7.  **Mention Groq Speed**: "We switched to Groq for ultra-fast inference, avoiding the rate limits we faced with other providers."

## Conclusion
"This architecture allows for scalable, intelligent document processing with minimal manual intervention. Thank you."
