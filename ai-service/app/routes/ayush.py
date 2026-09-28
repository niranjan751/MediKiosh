"""
MediKiosk AI Service - AYUSH / Ayurveda API Routes
==================================================
"""

from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.models.schemas import (
    AyushAssessmentRequest,
    AyushAssessmentResponse,
)
from app.services.ayush_service import (
    PRAKRITI_QUESTIONS,
    conduct_ayush_assessment,
)


router = APIRouter(
    prefix="/ayush",
    tags=["AYUSH / Ayurveda"],
)


@router.get("/questions")
def get_ayush_questions():
    """Returns the validated Prakriti and Dashavidha Pariksha questionnaire."""
    return {
        "success": True,
        "total_questions": len(PRAKRITI_QUESTIONS),
        "questions": PRAKRITI_QUESTIONS,
    }


@router.post("/assess", response_model=AyushAssessmentResponse)
def perform_ayush_assessment(request: AyushAssessmentRequest):
    """
    Computes Prakriti (Tridosha) scores, Vikriti imbalance, Agni,
    Koshtha, Dashavidha Pariksha, and personalized Pathya-Apathya guidance.
    """
    assessment = conduct_ayush_assessment(
        patient_id=request.patient_id,
        responses=request.responses,
        language=request.language,
    )

    summary_text = (
        f"Ayurvedic Clinical Profile: Prakriti is {assessment.prakriti.dominant_dosha} "
        f"({assessment.prakriti.constitution_type}) with {assessment.agni}. "
        f"Koshtha identified as {assessment.koshtha}."
    )

    return AyushAssessmentResponse(
        success=True,
        patient_id=request.patient_id,
        assessment=assessment,
        summary=summary_text,
    )
