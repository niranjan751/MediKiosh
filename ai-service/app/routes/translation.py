"""
MediKiosk AI Service
Translation API Routes

Provides multilingual translation endpoints for:
- General text
- Clinical interview questions
- Symptoms
- Medical summaries
- Language information
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.utils.language import (
    get_all_language_information,
    get_language_information,
    get_translation_disclaimer,
    get_translation_service_status,
    translate_interview_question,
    translate_medical_entity,
    translate_summary,
    translate_symptom,
    translate_text,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/translation",
    tags=["Translation"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class TranslationRequest(BaseModel):
    """General text translation request."""

    text: str = Field(
        ...,
        min_length=1,
        description="Text to translate",
    )

    source_language: str = Field(
        default="en",
        description="Source language code",
    )

    target_language: str = Field(
        default="ta",
        description="Target language code",
    )


class QuestionTranslationRequest(BaseModel):
    """Clinical interview question translation request."""

    question_key: str = Field(
        ...,
        min_length=1,
        description="Clinical question translation key",
    )

    target_language: str = Field(
        default="ta",
        description="Target language code",
    )


class SymptomTranslationRequest(BaseModel):
    """Medical symptom translation request."""

    symptom_key: str = Field(
        ...,
        min_length=1,
        description="Medical symptom translation key",
    )

    target_language: str = Field(
        default="ta",
        description="Target language code",
    )


class EntityTranslationRequest(BaseModel):
    """Medical entity translation request."""

    entity: Dict[str, Any] = Field(
        ...,
        description="Medical entity object",
    )

    target_language: str = Field(
        default="ta",
        description="Target language code",
    )


class SummaryTranslationRequest(BaseModel):
    """Clinical summary translation request."""

    summary: Dict[str, Any] = Field(
        ...,
        description="Clinical summary object",
    )

    target_language: str = Field(
        default="ta",
        description="Target language code",
    )


# ============================================================
# HEALTH
# ============================================================

@router.get("/health")
def translation_health():
    """
    Check translation service status.
    """

    return get_translation_service_status()


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

@router.get("/languages")
def supported_languages():
    """
    Return all supported languages.
    """

    return {
        "success": True,
        "count": len(
            get_all_language_information()
        ),
        "languages": get_all_language_information(),
    }


# ============================================================
# SINGLE LANGUAGE INFORMATION
# ============================================================

@router.get("/languages/{language_code}")
def language_information(
    language_code: str,
):
    """
    Return information about one language.
    """

    try:

        return {
            "success": True,
            "data": get_language_information(
                language_code
            ),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


# ============================================================
# GENERAL TEXT TRANSLATION
# ============================================================

@router.post("/text")
def translate_general_text(
    request: TranslationRequest,
):
    """
    Translate general text.
    """

    try:

        result = translate_text(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
        )

        return result

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Translation failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# INTERVIEW QUESTION TRANSLATION
# ============================================================

@router.post("/question")
def translate_question(
    request: QuestionTranslationRequest,
):
    """
    Translate a clinical interview question.
    """

    try:

        result = translate_interview_question(
            question_key=request.question_key,
            target_language=request.target_language,
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=404,
                detail=result.get(
                    "message",
                    "Question translation not found.",
                ),
            )

        return result

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Question translation failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# SYMPTOM TRANSLATION
# ============================================================

@router.post("/symptom")
def translate_symptom_route(
    request: SymptomTranslationRequest,
):
    """
    Translate a medical symptom.
    """

    try:

        result = translate_symptom(
            symptom_key=request.symptom_key,
            target_language=request.target_language,
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=404,
                detail=result.get(
                    "message",
                    "Symptom translation not found.",
                ),
            )

        return result

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Symptom translation failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# MEDICAL ENTITY TRANSLATION
# ============================================================

@router.post("/entity")
def translate_entity_route(
    request: EntityTranslationRequest,
):
    """
    Translate a medical entity.
    """

    try:

        result = translate_medical_entity(
            entity=request.entity,
            target_language=request.target_language,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Medical entity translation failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# CLINICAL SUMMARY TRANSLATION
# ============================================================

@router.post("/summary")
def translate_summary_route(
    request: SummaryTranslationRequest,
):
    """
    Translate important fields in a clinical summary.
    """

    try:

        result = translate_summary(
            summary=request.summary,
            target_language=request.target_language,
        )

        return {
            "success": True,
            "message": (
                "Clinical summary translated successfully."
            ),
            "data": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Summary translation failed: {str(exc)}"
            ),
        ) from exc


# ============================================================
# DISCLAIMER
# ============================================================

@router.get("/disclaimer")
def translation_disclaimer():
    """
    Return translation disclaimer.
    """

    return {
        "message": get_translation_disclaimer(),
        "medical_translation": True,
        "diagnosis": False,
        "autonomous_medical_decision": False,
        "doctor_review_recommended": True,
    }