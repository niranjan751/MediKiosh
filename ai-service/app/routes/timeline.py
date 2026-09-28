"""
MediKiosk AI Service - Medical Timeline API Route
=================================================
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.models.schemas import MedicalTimelineResponse
from app.services.timeline_service import build_timeline_events


router = APIRouter(
    prefix="/timeline",
    tags=["Medical Timeline"],
)


class TimelineGenerationRequest(BaseModel):
    patient_id: Optional[str] = None
    documents_data: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    interview_answers: Optional[Dict[str, Any]] = Field(default_factory=dict)
    patient_records: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    current_red_flags: Optional[List[Any]] = Field(default_factory=list)


@router.post("/generate", response_model=MedicalTimelineResponse)
def generate_patient_timeline(request: TimelineGenerationRequest):
    """
    Generates a structured, chronological medical timeline from uploaded documents,
    interview answers, and patient clinical records.
    """
    events = build_timeline_events(
        documents_data=request.documents_data,
        interview_answers=request.interview_answers,
        patient_records=request.patient_records,
        current_red_flags=request.current_red_flags,
    )

    years = sorted(list(set(e.year for e in events if e.year)), reverse=True)

    return MedicalTimelineResponse(
        success=True,
        patient_id=request.patient_id,
        total_events=len(events),
        events=events,
        years_covered=years,
    )


@router.get("/{patient_id}", response_model=MedicalTimelineResponse)
def get_timeline_by_patient(patient_id: str):
    """Fetches default/active medical timeline for a patient."""
    events = build_timeline_events()
    years = sorted(list(set(e.year for e in events if e.year)), reverse=True)
    return MedicalTimelineResponse(
        success=True,
        patient_id=patient_id,
        total_events=len(events),
        events=events,
        years_covered=years,
    )
