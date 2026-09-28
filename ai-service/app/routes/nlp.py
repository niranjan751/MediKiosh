"""
MediKiosk AI Service - Clinical NLP API Routes
==============================================
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.clinical_nlp import (
    analyze_clinical_text,
    extract_clinical_information,
    extract_entities,
    get_clinical_nlp_status,
    is_negated,
    prepare_summary_data,
)


router = APIRouter(
    prefix="/nlp",
    tags=["Clinical NLP"],
)


class NLPTextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Clinical narrative or patient response text")


class NegationCheckRequest(BaseModel):
    text: str = Field(..., min_length=1)
    entity_text: str = Field(..., min_length=1)


@router.get("/status")
def nlp_status():
    """Returns the capabilities and status of the Clinical NLP service."""
    return get_clinical_nlp_status()


@router.post("/analyze")
def analyze_text_endpoint(request: NLPTextRequest):
    """
    Performs full clinical NLP processing:
    - Sentence segmentation
    - Medical named entity recognition (NER)
    - NegEx negation detection (e.g. 'denies chest pain', 'no fever')
    - Uncertainty and hedging detection
    - Severity and temporal duration extraction
    - Entity grouping by type
    """
    try:
        return analyze_clinical_text(request.text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Clinical NLP analysis failed: {str(exc)}",
        ) from exc


@router.post("/entities")
def extract_entities_endpoint(request: NLPTextRequest):
    """Extracts deduplicated clinical entities from input text."""
    try:
        entities = extract_entities(request.text)
        return {
            "success": True,
            "total_entities": len(entities),
            "entities": [e.to_dict() for e in entities],
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Entity extraction failed: {str(exc)}",
        ) from exc


@router.post("/negation-check")
def check_negation_endpoint(request: NegationCheckRequest):
    """Verifies whether a specific clinical term is affirmed or negated in context."""
    pos = request.text.lower().find(request.entity_text.lower())
    start_idx = pos if pos >= 0 else 0
    negated = is_negated(request.text, start_idx, request.entity_text)
    return {
        "success": True,
        "text": request.text,
        "entity": request.entity_text,
        "is_negated": negated,
        "interpretation": "Negative / Denied finding" if negated else "Positive / Affirmed finding",
    }


@router.post("/summary-input")
def prepare_summary_input_endpoint(request: NLPTextRequest):
    """Structures free-text clinical intake into structured summary parameters."""
    return prepare_summary_data(request.text)
