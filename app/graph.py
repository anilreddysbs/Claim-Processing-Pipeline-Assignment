from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from .models import FinalResponse, ExtractedData, IdentityInfo, DischargeSummaryResult, ItemizedBillResult, SegregationResult
from .agents import SegregatorAgent, IdentityExtractionAgent, DischargeSummaryExtractionAgent, ItemizedBillExtractionAgent
from .utils import extract_text_from_pdf, get_pages_for_type
import operator

# Reducer function for ExtractedData
def reduce_extracted_data(left: ExtractedData | None, right: ExtractedData | None) -> ExtractedData:
    if left is None:
        left = ExtractedData()
    if right is None:
        return left
    
    # Create a new object to avoid mutation issues if any
    new_data = ExtractedData(
        identity=left.identity if left.identity else None,
        bill_data=left.bill_data if left.bill_data else None,
        discharge_summary=left.discharge_summary if left.discharge_summary else None,
        other_documents=left.other_documents if left.other_documents else None
    )
    
    if right.identity:
        new_data.identity = right.identity
    if right.bill_data:
        new_data.bill_data = right.bill_data
    if right.discharge_summary:
        new_data.discharge_summary = right.discharge_summary
    if right.other_documents:
        if new_data.other_documents:
            new_data.other_documents.extend(right.other_documents)
        else:
            new_data.other_documents = right.other_documents
            
    return new_data

# Define the state of the graph
class GraphState(TypedDict):
    pdf_bytes: bytes
    claim_id: str
    pages_text: Dict[int, str]
    classification_result: SegregationResult
    extracted_data: Annotated[ExtractedData, reduce_extracted_data]
    logs: Annotated[List[str], operator.add]

# Initialize Agents
segregator = SegregatorAgent()
id_agent = IdentityExtractionAgent()
discharge_agent = DischargeSummaryExtractionAgent()
bill_agent = ItemizedBillExtractionAgent()

from .retry_utils import run_with_retry

# Node Functions
def classify_document(state: GraphState):
    print("---SEGREGATOR AGENT---")
    pages_text = extract_text_from_pdf(state['pdf_bytes'])
    result = run_with_retry(segregator.classify, pages_text)
    print(f"Classification Result: {result}")
    return {
        "pages_text": pages_text,
        "classification_result": result,
        # Initialize extracted_data with empty object if not present, but better to let reducer handle None
        "logs": ["Segregator Agent finished classification."]
    }

def extract_identity(state: GraphState):
    print("---IDENTITY AGENT---")
    classifications = state['classification_result'].classifications
    
    target_pages = get_pages_for_type([c.dict() for c in classifications], "identity_document")
    target_pages += get_pages_for_type([c.dict() for c in classifications], "claim_form")
    target_pages = sorted(list(set(target_pages))) # Unique pages

    if not target_pages:
        return {} # No update

    text_to_process = "\n".join([state['pages_text'][p] for p in target_pages])
    extracted_info = run_with_retry(id_agent.extract, text_to_process)
    
    # Return partial update
    return {
        "extracted_data": ExtractedData(identity=extracted_info),
        "logs": [f"Identity Agent processed pages {target_pages}."]
    }

def extract_discharge_summary(state: GraphState):
    print("---DISCHARGE SUMMARY AGENT---")
    classifications = state['classification_result'].classifications
    target_pages = get_pages_for_type([c.dict() for c in classifications], "discharge_summary")

    if not target_pages:
        return {}

    text_to_process = "\n".join([state['pages_text'][p] for p in target_pages])
    extracted_info = run_with_retry(discharge_agent.extract, text_to_process)

    return {
        "extracted_data": ExtractedData(discharge_summary=extracted_info),
        "logs": [f"Discharge Summary Agent processed pages {target_pages}."]
    }

def extract_itemized_bill(state: GraphState):
    print("---ITEMIZED BILL AGENT---")
    classifications = state['classification_result'].classifications
    target_pages = get_pages_for_type([c.dict() for c in classifications], "itemized_bill")

    if not target_pages:
        return {}

    text_to_process = "\n".join([state['pages_text'][p] for p in target_pages])
    extracted_info = run_with_retry(bill_agent.extract, text_to_process)

    return {
        "extracted_data": ExtractedData(bill_data=extracted_info),
        "logs": [f"Itemized Bill Agent processed pages {target_pages}."]
    }

def aggregator(state: GraphState):
    print("---AGGREGATOR AGENT---")
    return {
        "logs": ["Aggregator finished."]
    }

# Build the Graph
workflow = StateGraph(GraphState)

# Add Nodes
workflow.add_node("segregator", classify_document)
workflow.add_node("id_agent", extract_identity)
workflow.add_node("discharge_agent", extract_discharge_summary)
workflow.add_node("bill_agent", extract_itemized_bill)
workflow.add_node("aggregator", aggregator)

# Define Edges
workflow.set_entry_point("segregator")

workflow.add_edge("segregator", "id_agent")
workflow.add_edge("segregator", "discharge_agent")
workflow.add_edge("segregator", "bill_agent")

workflow.add_edge("id_agent", "aggregator")
workflow.add_edge("discharge_agent", "aggregator")
workflow.add_edge("bill_agent", "aggregator")

workflow.add_edge("aggregator", END)

# Compile
app_graph = workflow.compile()
