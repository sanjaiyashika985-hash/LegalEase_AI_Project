"""Request and response models for LegalEase."""
from typing import Literal

from pydantic import BaseModel, Field


DocumentType = Literal[
    "Non-Disclosure Agreement (NDA)",
    "Employment Agreement",
    "Residential Lease Agreement",
    "Freelance Services Agreement",
]


class DocumentRequest(BaseModel):
    document_type: DocumentType
    parties: str = Field(min_length=2, max_length=2000)
    effective_date: str = Field(min_length=1, max_length=100)
    jurisdiction: str = Field(default="India", min_length=2, max_length=100)
    terms: list[str] = Field(min_length=1, max_length=30)


class DocumentResponse(BaseModel):
    document_text: str
    generator: str
