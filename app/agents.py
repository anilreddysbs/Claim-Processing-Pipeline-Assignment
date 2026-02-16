from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from .models import SegregationResult, PageClassification, IdentityInfo, DischargeSummaryResult, ItemizedBillResult
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# Try identifying .env in current or parent directory
env_path = Path(__file__).resolve().parent.parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize LLM with Groq
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Using llama-3.3-70b-versatile for good performance/cost balance
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, groq_api_key=api_key)

class SegregatorAgent:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=SegregationResult)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert medical document classifier. Analyze the provided text from each page and classify it into one of the following categories: claim_form, cheque_or_bank_details, identity_document, itemized_bill, discharge_summary, prescription, investigation_report, cash_receipt, other. Return the result as a JSON object with a list of classifications, where each classification has 'page_number' and 'document_type'."),
            ("user", "Here is the text content of the pages:\n{pages_text}\n\n{format_instructions}")
        ])
        self.chain = self.prompt | llm | self.parser

    def classify(self, pages_text: Dict[int, str]) -> SegregationResult:
        # Prepare text for prompt
        formatted_text = ""
        for page_num, text in pages_text.items():
            formatted_text += f"Page {page_num}:\n{text[:2000]}...\n\n" 
        
        return self.chain.invoke({
            "pages_text": formatted_text,
            "format_instructions": self.parser.get_format_instructions()
        })

class IdentityExtractionAgent:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=IdentityInfo)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at extracting identity information from medical documents. Extract patient name, DOB, policy number, and ID number."),
            ("user", "Here is the text from the identity documents:\n{text}\n\n{format_instructions}")
        ])
        self.chain = self.prompt | llm | self.parser

    def extract(self, text: str) -> IdentityInfo:
        return self.chain.invoke({
            "text": text,
            "format_instructions": self.parser.get_format_instructions()
        })

class DischargeSummaryExtractionAgent:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=DischargeSummaryResult)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at extracting information from discharge summaries. Extract diagnosis, admission date, discharge date, and physician name."),
            ("user", "Here is the text from the discharge summary:\n{text}\n\n{format_instructions}")
        ])
        self.chain = self.prompt | llm | self.parser

    def extract(self, text: str) -> DischargeSummaryResult:
        return self.chain.invoke({
            "text": text,
            "format_instructions": self.parser.get_format_instructions()
        })

class ItemizedBillExtractionAgent:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=ItemizedBillResult)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at extracting itemized bills from medical documents. Extract a list of items with their descriptions and amounts, and the total amount."),
            ("user", "Here is the text from the itemized bill:\n{text}\n\n{format_instructions}")
        ])
        self.chain = self.prompt | llm | self.parser

    def extract(self, text: str) -> ItemizedBillResult:
        return self.chain.invoke({
            "text": text,
            "format_instructions": self.parser.get_format_instructions()
        })
