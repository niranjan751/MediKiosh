"""
MediKiosk AI Service
Clinical Summary API Routes

Purpose:
    Provide REST API endpoints for generating and reviewing
    AI-assisted clinical summaries.

Important:
    Clinical summaries are assistive only.
    They are not diagnoses or autonomous medical decisions.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.summary_service import (
    apply_doctor_review,
    create_short_summary,
    generate_clinical_summary,
    get_summary_service_status,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/summary",
    tags=["Clinical Summary"],
)


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class ClinicalSummaryRequest(BaseModel):
    """
    Request model for generating a clinical summary.
    """

    patient: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Patient information",
    )

    interview_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Clinical interview information",
    )

    red_flag_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Red-flag detection results",
    )

    document_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="OCR/document information",
    )


class DoctorReviewRequest(BaseModel):
    """
    Request model for doctor review.
    """

    summary: Dict[str, Any] = Field(
        ...,
        description="AI-generated clinical summary",
    )

    doctor_notes: str = Field(
        ...,
        min_length=1,
        description="Doctor's review notes",
    )

    doctor_name: Optional[str] = Field(
        default=None,
        description="Doctor name",
    )


# ============================================================
# HEALTH
# ============================================================

@router.get("/health")
def summary_health():
    """
    Check clinical summary service status.
    """

    return get_summary_service_status()


# ============================================================
# GENERATE SUMMARY
# ============================================================

@router.post("/generate")
def generate_summary(
    request: ClinicalSummaryRequest,
):
    """
    Generate an AI-assisted clinical summary.
    """

    try:

        summary = generate_clinical_summary(
            patient=request.patient,
            interview_data=request.interview_data,
            red_flag_data=request.red_flag_data,
            document_data=request.document_data,
        )

        return {
            "success": True,
            "message": (
                "Clinical summary generated successfully."
            ),
            "data": summary,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Clinical summary generation failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# SHORT SUMMARY
# ============================================================

@router.post("/short")
def generate_short_summary(
    request: ClinicalSummaryRequest,
):
    """
    Generate a short readable clinical summary.
    """

    try:

        summary = generate_clinical_summary(
            patient=request.patient,
            interview_data=request.interview_data,
            red_flag_data=request.red_flag_data,
            document_data=request.document_data,
        )

        short_summary = create_short_summary(
            summary
        )

        return {
            "success": True,
            "message": (
                "Short clinical summary generated successfully."
            ),
            "summary": short_summary,
            "data": summary,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Short summary generation failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# DOCTOR REVIEW
# ============================================================

@router.post("/review")
def review_summary(
    request: DoctorReviewRequest,
):
    """
    Apply doctor review to an AI-generated summary.
    """

    try:

        reviewed_summary = apply_doctor_review(
            summary=request.summary,
            doctor_notes=request.doctor_notes,
            doctor_name=request.doctor_name,
        )

        return {
            "success": True,
            "message": (
                "Clinical summary reviewed successfully."
            ),
            "data": reviewed_summary,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Doctor review failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# DISCLAIMER
# ============================================================

@router.get("/disclaimer")
def summary_disclaimer():
    """
    Return clinical summary disclaimer.
    """

    return {
        "message": (
            "AI-generated clinical summaries are intended "
            "for information organization and clinical "
            "review only."
        ),
        "diagnosis": False,
        "autonomous_medical_decision": False,
        "doctor_review_required": True,
    }