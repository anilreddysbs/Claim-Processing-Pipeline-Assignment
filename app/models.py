from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PageClassification(BaseModel):
    page_number: int
    document_type: str = Field(..., description="Type of document this page belongs to. Options: claim_form, cheque_or_bank_details, identity_document, itemized_bill, discharge_summary, prescription, investigation_report, cash_receipt, other")
    confidence: float

class SegregationResult(BaseModel):
    classifications: List[PageClassification]

class IdentityInfo(BaseModel):
    patient_name: Optional[str] = None
    dob: Optional[str] = None
    policy_number: Optional[str] = None
    id_number: Optional[str] = None
    raw_text: Optional[str] = None

class LineItem(BaseModel):
    description: str
    amount: float

class ItemizedBillResult(BaseModel):
    items: List[LineItem] = []
    total_amount: float = 0.0
    raw_text: Optional[str] = None

class DischargeSummaryResult(BaseModel):
    diagnosis: Optional[str] = None
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None
    physician_name: Optional[str] = None
    raw_text: Optional[str] = None

class ExtractedData(BaseModel):
    identity: Optional[IdentityInfo] = None
    bill_data: Optional[ItemizedBillResult] = None
    discharge_summary: Optional[DischargeSummaryResult] = None
    other_documents: Optional[List[str]] = None

class FinalResponse(BaseModel):
    claim_id: str
    extracted_data: ExtractedData
    agent_logs: Optional[List[str]] = None
