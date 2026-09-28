"""
MediKiosk AI Service - Adaptive Clinical Interview API Routes
=============================================================
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewStatus,
    QuestionOption,
)
from app.services.clinical_interview import (
    get_collected_data,
    get_current_question,
    get_progress,
    get_session,
    save_answer,
    start_interview,
)


router = APIRouter(
    prefix="/interview",
    tags=["Clinical Interview"],
)


@router.post(
    "/start",
    response_model=InterviewStartResponse,
)
def start_clinical_interview(
    request: InterviewStartRequest,
):
    """
    Start an adaptive clinical interview session.
    Requires patient consent.
    """
    if not request.consent_given:
        raise HTTPException(
            status_code=400,
            detail="Patient consent is mandatory before starting the medical assessment.",
        )

    session = start_interview(
        patient_id=request.patient_id,
        patient_name=request.patient_name,
        language=request.language,
        clinical_mode=request.clinical_mode,
        chief_complaint_initial=request.chief_complaint_initial,
    )

    question_data = get_current_question(session.session_id)

    raw_options = question_data.get("options", []) if question_data else []
    formatted_options = [
        opt if isinstance(opt, QuestionOption) else QuestionOption(**opt)
        for opt in raw_options
    ]

    return InterviewStartResponse(
        success=True,
        session_id=session.session_id,
        patient_id=session.patient_id,
        language=session.language,
        status=session.status,
        question_number=session.current_question + 1,
        total_questions=session.total_questions,
        question=question_data["question"] if question_data else None,
        question_key=question_data["key"] if question_data else None,
        category=question_data.get("category") if question_data else None,
        input_type=question_data.get("input_type", "choice") if question_data else "text",
        options=formatted_options,
        completed=(session.status == InterviewStatus.COMPLETED),
    )


@router.get(
    "/{session_id}/question",
)
def get_interview_question(session_id: str):
    """Fetch the active question for an interview session."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    question_data = get_current_question(session_id)
    if not question_data:
        return {
            "success": True,
            "session_id": session_id,
            "completed": True,
            "question": None,
        }

    return {
        "success": True,
        "session_id": session_id,
        "question_number": session.current_question + 1,
        "total_questions": session.total_questions,
        "question": question_data["question"],
        "question_key": question_data["key"],
        "category": question_data.get("category"),
        "input_type": question_data.get("input_type", "choice"),
        "options": question_data.get("options", []),
        "socrates_dimension": question_data.get("socrates_dimension"),
        "completed": False,
    }


@router.post(
    "/answer",
    response_model=InterviewAnswerResponse,
)
def submit_interview_answer(
    request: InterviewAnswerRequest,
):
    """Submits patient answer and returns next adaptive question with quick-select options."""
    session = get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    if session.status == InterviewStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="This clinical interview is already completed.",
        )

    updated_session = save_answer(
        session_id=request.session_id,
        answer=request.answer,
        question_id=request.question_id,
    )

    if not updated_session:
        raise HTTPException(status_code=500, detail="Failed to save answer.")

    next_q = get_current_question(request.session_id)
    is_completed = (updated_session.status == InterviewStatus.COMPLETED)

    raw_options = next_q.get("options", []) if next_q else []
    formatted_options = [
        opt if isinstance(opt, QuestionOption) else QuestionOption(**opt)
        for opt in raw_options
    ]

    return InterviewAnswerResponse(
        success=True,
        session_id=updated_session.session_id,
        question_number=min(updated_session.current_question + 1, updated_session.total_questions),
        total_questions=updated_session.total_questions,
        answer_saved=True,
        completed=is_completed,
        next_question=next_q["question"] if next_q else None,
        next_question_key=next_q["key"] if next_q else None,
        category=next_q.get("category") if next_q else None,
        input_type=next_q.get("input_type", "choice") if next_q else "text",
        options=formatted_options,
        collected_data=get_collected_data(request.session_id) or {},
        red_flags_detected=updated_session.red_flags,
        priority_alert=(len(updated_session.red_flags) > 0),
    )


@router.get(
    "/{session_id}/progress",
)
def interview_progress(session_id: str):
    """Retrieve current progress percentage and triage status."""
    progress = get_progress(session_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Interview session not found.")
    return {"success": True, **progress}


@router.get(
    "/{session_id}/answers",
)
def interview_answers(session_id: str):
    """Retrieve full transcript of collected answers and red flags."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")
    return {
        "success": True,
        "session_id": session_id,
        "status": session.status,
        "answers": get_collected_data(session_id) or {},
        "red_flags": session.red_flags,
        "detected_category": session.detected_complaint_category,
    }