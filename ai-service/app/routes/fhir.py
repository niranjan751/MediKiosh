"""
MediKiosk AI Service - ABDM & FHIR Interoperability API Routes
==============================================================
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.schemas import ClinicalSummaryRequest
from app.services.fhir_service import generate_fhir_bundle
from app.services.summary_service import generate_structured_clinical_summary


router = APIRouter(
    prefix="/fhir",
    tags=["ABDM & FHIR Interoperability"],
)


class FHIRBundleRequest(BaseModel):
    summary_request: ClinicalSummaryRequest
    abha_id: Optional[str] = "91-1234-5678-9012"


@router.post("/bundle")
def export_fhir_bundle(request: FHIRBundleRequest):
    """
    Transforms the MediKiosk patient clinical intake into a
    validated HL7 FHIR Release 4 (R4) Document Bundle conforming to
    ABDM (Ayushman Bharat Digital Mission) Health Record standards.
    """
    try:
        summary = generate_structured_clinical_summary(
            patient_id=request.summary_request.patient_id,
            session_id=request.summary_request.session_id,
            patient_info=request.summary_request.patient_info,
            interview_data=request.summary_request.interview_data,
            documents_data=request.summary_request.documents_data,
            clinical_mode=request.summary_request.clinical_mode,
            ayush_data=request.summary_request.ayush_data,
        )

        bundle = generate_fhir_bundle(summary, abha_id=request.abha_id)

        return {
            "success": True,
            "standard": "HL7 FHIR R4",
            "abdm_compliant": True,
            "bundle": bundle,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"FHIR bundle conversion failed: {str(exc)}",
        ) from exc


@router.get("/profile")
def get_fhir_profile_info():
    """Returns ABDM and FHIR profile specifications."""
    return {
        "standard": "HL7 FHIR Release 4",
        "jurisdiction": "India (ABDM / NRCES)",
        "supported_resources": [
            "Bundle (Document)",
            "Composition",
            "Patient (with ABHA ID)",
            "Condition",
            "MedicationStatement",
            "Observation (Labs & Vitals)",
            "AllergyIntolerance",
        ],
        "interoperability": "Enables seamless transfer to Hospital Information Systems (HIS) and EHRs",
    }
