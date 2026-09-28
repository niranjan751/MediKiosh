"""
MediKiosk AI Service - Clinical Summary API Routes
==================================================
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ClinicalSummaryRequest,
    ClinicalSummaryResponse,
    DoctorReviewRequest,
    DoctorReviewResponse,
    ProcessingStatus,
    ReviewStatus,
)
from app.services.summary_service import (
    apply_doctor_review_to_summary,
    generate_structured_clinical_summary,
)


router = APIRouter(
    prefix="/summary",
    tags=["Clinical Summary"],
)


@router.post("/generate", response_model=ClinicalSummaryResponse)
def generate_clinical_summary_endpoint(request: ClinicalSummaryRequest):
    """
    Generates a comprehensive, physician-ready AI clinical summary
    incorporating patient interview (SOCRATES), OCR document findings,
    abnormal lab results, and red-flag triage badges.
    """
    try:
        summary = generate_structured_clinical_summary(
            patient_id=request.patient_id,
            session_id=request.session_id,
            patient_info=request.patient_info,
            interview_data=request.interview_data,
            documents_data=request.documents_data,
            clinical_mode=request.clinical_mode,
            ayush_data=request.ayush_data,
        )

        return ClinicalSummaryResponse(
            success=True,
            patient_id=request.patient_id,
            session_id=request.session_id,
            status=ProcessingStatus.COMPLETED,
            summary=summary,
            review_status=ReviewStatus.PENDING,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate clinical summary: {str(exc)}",
        ) from exc


@router.post("/review")
def review_summary_endpoint(request: DoctorReviewRequest):
    """
    Enables attending doctor to edit, append clinical notes,
    confirm diagnoses, and approve the clinical intake summary.
    """
    try:
        updated = apply_doctor_review_to_summary(
            summary=request.model_dump(),
            doctor_notes=request.comments or "Reviewed and approved by physician.",
            doctor_name=request.doctor_name,
            confirmed_diagnoses=request.confirmed_diagnoses,
            prescribed_plan=request.prescribed_plan,
        )

        return {
            "success": True,
            "message": "Clinical summary reviewed and approved successfully.",
            "data": updated,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Doctor review failed: {str(exc)}",
        ) from exc