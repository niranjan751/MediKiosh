from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewStatus,
)

from app.services.clinical_interview import (
    start_interview,
    get_session,
    get_current_question,
    save_answer,
    get_progress,
    get_collected_data,
)


router = APIRouter(
    prefix="/interview",
    tags=["Clinical Interview"]
)


# ============================================================
# START INTERVIEW
# ============================================================

@router.post(
    "/start",
    response_model=InterviewStartResponse
)
def start_clinical_interview(
    request: InterviewStartRequest
):
    """
    Start a new clinical interview session.
    """

    if not request.consent_given:
        raise HTTPException(
            status_code=400,
            detail="Patient consent is required before starting the interview."
        )

    session = start_interview(
        patient_id=request.patient_id,
        patient_name=request.patient_name,
        language=request.language,
    )

    question = get_current_question(
        session.session_id
    )

    return InterviewStartResponse(
        success=True,
        session_id=session.session_id,
        patient_id=session.patient_id,
        language=session.language,
        status=session.status,
        question_number=session.current_question + 1,
        total_questions=session.total_questions,
        question=(
            question["question"]
            if question
            else None
        ),
        question_key=(
            question["key"]
            if question
            else None
        ),
        completed=(
            session.status == InterviewStatus.COMPLETED
        ),
    )


# ============================================================
# GET CURRENT QUESTION
# ============================================================

@router.get(
    "/{session_id}/question"
)
def get_interview_question(
    session_id: str
):
    """
    Get the current question for an interview session.
    """

    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    question = get_current_question(
        session_id
    )

    if question is None:
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
        "question": question["question"],
        "question_key": question["key"],
        "category": question["category"],
        "required": question["required"],
        "completed": False,
    }


# ============================================================
# SUBMIT ANSWER
# ============================================================

@router.post(
    "/answer",
    response_model=InterviewAnswerResponse
)
def submit_interview_answer(
    request: InterviewAnswerRequest
):
    """
    Save the patient's answer and return the next question.
    """

    session = get_session(
        request.session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    if session.status == InterviewStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="This interview has already been completed."
        )

    if session.status == InterviewStatus.CANCELLED:
        raise HTTPException(
            status_code=400,
            detail="This interview has been cancelled."
        )

    updated_session = save_answer(
        session_id=request.session_id,
        answer=request.answer,
        question_id=request.question_id,
    )

    if updated_session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    next_question = get_current_question(
        request.session_id
    )

    completed = (
        updated_session.status
        == InterviewStatus.COMPLETED
    )

    return InterviewAnswerResponse(
        success=True,
        session_id=updated_session.session_id,
        question_number=(
            min(
                updated_session.current_question + 1,
                updated_session.total_questions
            )
        ),
        total_questions=updated_session.total_questions,
        answer_saved=True,
        completed=completed,
        next_question=(
            next_question["question"]
            if next_question
            else None
        ),
        next_question_key=(
            next_question["key"]
            if next_question
            else None
        ),
        collected_data=get_collected_data(
            request.session_id
        ) or {},
    )


# ============================================================
# INTERVIEW PROGRESS
# ============================================================

@router.get(
    "/{session_id}/progress"
)
def interview_progress(
    session_id: str
):
    """
    Get interview completion progress.
    """

    progress = get_progress(
        session_id
    )

    if progress is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    return {
        "success": True,
        **progress,
    }


# ============================================================
# GET COLLECTED ANSWERS
# ============================================================

@router.get(
    "/{session_id}/answers"
)
def interview_answers(
    session_id: str
):
    """
    Get answers collected during the interview.
    """

    session = get_session(
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    return {
        "success": True,
        "session_id": session_id,
        "status": session.status,
        "answers": get_collected_data(
            session_id
        ) or {},
    }