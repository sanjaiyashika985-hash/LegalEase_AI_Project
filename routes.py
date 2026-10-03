"""API routes."""
from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import generate_document
from schemas import DocumentRequest, DocumentResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/generate", response_model=DocumentResponse)
def generate(request: DocumentRequest):
    try:
        text, generator = generate_document(
            document_type=request.document_type,
            parties=request.parties,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            terms=request.terms,
        )
        return DocumentResponse(document_text=text, generator=generator)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
