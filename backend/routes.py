from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str


class DocumentResponse(BaseModel):
    document_type: str
    generated_text: str


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        generated_text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

        return DocumentResponse(
            document_type=request.document_type,
            generated_text=generated_text
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )