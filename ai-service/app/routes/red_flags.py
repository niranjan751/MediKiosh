from fastapi import APIRouter, HTTPException
from typing import Dict, List

from app.models.schemas import (
    LanguageCode,
    RedFlag,
    RedFlagRequest,
    RedFlagResponse,
    AlertSeverity,
)

from app.services.red_flag_service import (
    build_red_flag_result,
    detect_red_flags,
    get_overall_severity,
)


# ============================================================
# ROUTER CONFIGURATION
# ============================================================

router = APIRouter(
    prefix="/red-flags",
    tags=["Red Flag Detection"],
)


# ============================================================
# SERVICE INFORMATION
# ============================================================

@router.get("/")
def red_flag_service_info():
    """
    Return information about the red-flag detection service.
    """

    return {
        "success": True,
        "service": "MediKiosk Red Flag Detection",
        "status": "online",
        "purpose": (
            "Detect potential clinical warning signs "
            "and alert appropriate healthcare staff."
        ),
        "mode": "clinical_support",
        "diagnosis": False,
        "supported_languages": [
            "en",
            "ta",
            "hi",
            "te",
            "kn",
            "ml",
        ],
        "endpoints": [
            "POST /red-flags/detect",
            "POST /red-flags/check-symptoms",
            "GET /red-flags/health",
        ],
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def red_flag_health():
    """
    Check whether the red-flag detection service is healthy.
    """

    return {
        "success": True,
        "service": "Red Flag Detection",
        "status": "healthy",
    }


# ============================================================
# MAIN RED FLAG DETECTION
# ============================================================

@router.post(
    "/detect",
    response_model=RedFlagResponse,
)
def detect_patient_red_flags(
    request: RedFlagRequest,
):
    """
    Detect potential clinical red flags.

    This endpoint analyzes:
    - Symptoms
    - Clinical text
    - Interview answers
    - Selected language

    It does NOT provide a medical diagnosis.
    """

    # --------------------------------------------------------
    # Basic validation
    # --------------------------------------------------------

    if not request.symptoms and not request.clinical_text:
        if not request.interview_answers:

            return RedFlagResponse(
                success=True,
                red_flag_detected=False,
                overall_severity=AlertSeverity.LOW,
                flags=[],
                staff_alert_required=False,
                disclaimer=(
                    "No clinical information was provided. "
                    "Red-flag detection is an alerting and "
                    "clinical support feature. It is not a diagnosis."
                ),
            )

    # --------------------------------------------------------
    # Run detection
    # --------------------------------------------------------

    try:

        result = build_red_flag_result(
            symptoms=request.symptoms,
            clinical_text=request.clinical_text or "",
            interview_answers=request.interview_answers,
            language=request.language,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Red-flag detection failed: {str(error)}",
        )

    # --------------------------------------------------------
    # Return structured response
    # --------------------------------------------------------

    return RedFlagResponse(
        success=True,
        red_flag_detected=result["red_flag_detected"],
        overall_severity=result["overall_severity"],
        triage_priority=result["triage_priority"],
        flags=result["flags"],
        staff_alert_required=result["staff_alert_required"],
        immediate_hospital_triage=result.get("immediate_hospital_triage", False),
        emergency_instructions=result.get("emergency_instructions"),
        disclaimer=result["disclaimer"],
    )


# ============================================================
# SYMPTOM-ONLY CHECK
# ============================================================

@router.post(
    "/check-symptoms",
)
def check_symptoms(
    symptoms: List[str],
    language: LanguageCode = LanguageCode.ENGLISH,
):
    """
    Quickly check a list of symptoms for potential red flags.
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    cleaned_symptoms = [
        symptom.strip()
        for symptom in symptoms
        if symptom and symptom.strip()
    ]

    if not cleaned_symptoms:

        return {
            "success": True,
            "red_flag_detected": False,
            "overall_severity": AlertSeverity.LOW,
            "flags": [],
            "staff_alert_required": False,
        }

    # --------------------------------------------------------
    # Run detection
    # --------------------------------------------------------

    try:

        flags = detect_red_flags(
            symptoms=cleaned_symptoms,
            clinical_text="",
            interview_answers={},
            language=language,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Symptom analysis failed: {str(error)}",
        )

    # --------------------------------------------------------
    # Calculate severity
    # --------------------------------------------------------

    overall_severity = get_overall_severity(
        flags
    )

    staff_alert_required = any(
        flag.requires_staff_attention
        for flag in flags
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "success": True,
        "red_flag_detected": len(flags) > 0,
        "overall_severity": overall_severity,
        "flag_count": len(flags),
        "flags": flags,
        "staff_alert_required": staff_alert_required,
        "language": language,
        "disclaimer": (
            "This result is intended for clinical support "
            "and alerting only. It is not a diagnosis."
        ),
    }


# ============================================================
# INTERVIEW ANSWER CHECK
# ============================================================

@router.post(
    "/check-interview",
)
def check_interview_answers(
    interview_answers: Dict[str, str],
    language: LanguageCode = LanguageCode.ENGLISH,
):
    """
    Analyze answers collected from the clinical interview.
    """

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not interview_answers:

        return {
            "success": True,
            "red_flag_detected": False,
            "overall_severity": AlertSeverity.LOW,
            "flags": [],
            "staff_alert_required": False,
            "message": "No interview answers were provided.",
        }

    # --------------------------------------------------------
    # Run detection
    # --------------------------------------------------------

    try:

        flags = detect_red_flags(
            symptoms=[],
            clinical_text="",
            interview_answers=interview_answers,
            language=language,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Interview red-flag detection failed: "
                f"{str(error)}"
            ),
        )

    # --------------------------------------------------------
    # Severity
    # --------------------------------------------------------

    overall_severity = get_overall_severity(
        flags
    )

    staff_alert_required = any(
        flag.requires_staff_attention
        for flag in flags
    )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {
        "success": True,
        "red_flag_detected": len(flags) > 0,
        "overall_severity": overall_severity,
        "flag_count": len(flags),
        "flags": flags,
        "staff_alert_required": staff_alert_required,
        "language": language,
        "disclaimer": (
            "Red-flag detection is an alerting and "
            "clinical support feature. It is not a diagnosis."
        ),
    }


# ============================================================
# CLINICAL TEXT CHECK
# ============================================================

@router.post(
    "/check-text",
)
def check_clinical_text(
    clinical_text: str,
    language: LanguageCode = LanguageCode.ENGLISH,
):
    """
    Analyze free-form clinical text.
    """

    # --------------------------------------------------------
    # Validate text
    # --------------------------------------------------------

    if not clinical_text or not clinical_text.strip():

        return {
            "success": True,
            "red_flag_detected": False,
            "overall_severity": AlertSeverity.LOW,
            "flags": [],
            "staff_alert_required": False,
            "message": "No clinical text was provided.",
        }

    # --------------------------------------------------------
    # Detect
    # --------------------------------------------------------

    try:

        flags = detect_red_flags(
            symptoms=[],
            clinical_text=clinical_text,
            interview_answers={},
            language=language,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Clinical text analysis failed: "
                f"{str(error)}"
            ),
        )

    # --------------------------------------------------------
    # Severity
    # --------------------------------------------------------

    overall_severity = get_overall_severity(
        flags
    )

    staff_alert_required = any(
        flag.requires_staff_attention
        for flag in flags
    )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {
        "success": True,
        "red_flag_detected": len(flags) > 0,
        "overall_severity": overall_severity,
        "flag_count": len(flags),
        "flags": flags,
        "staff_alert_required": staff_alert_required,
        "language": language,
        "disclaimer": (
            "Clinical text analysis provides "
            "supportive alerts only and does not "
            "constitute a medical diagnosis."
        ),
    }


# ============================================================
# GET ALERT SUMMARY
# ============================================================

@router.post(
    "/summary",
)
def red_flag_summary(
    request: RedFlagRequest,
):
    """
    Return a compact summary suitable for
    the doctor/admin dashboard.
    """

    # --------------------------------------------------------
    # Detect flags
    # --------------------------------------------------------

    try:

        flags = detect_red_flags(
            symptoms=request.symptoms,
            clinical_text=request.clinical_text or "",
            interview_answers=request.interview_answers,
            language=request.language,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Unable to create red-flag summary: "
                f"{str(error)}"
            ),
        )

    # --------------------------------------------------------
    # Severity
    # --------------------------------------------------------

    overall_severity = get_overall_severity(
        flags
    )

    critical_count = sum(
        1
        for flag in flags
        if flag.severity == AlertSeverity.CRITICAL
    )

    high_count = sum(
        1
        for flag in flags
        if flag.severity == AlertSeverity.HIGH
    )

    medium_count = sum(
        1
        for flag in flags
        if flag.severity == AlertSeverity.MEDIUM
    )

    low_count = sum(
        1
        for flag in flags
        if flag.severity == AlertSeverity.LOW
    )

    # --------------------------------------------------------
    # Staff alert
    # --------------------------------------------------------

    staff_alert_required = any(
        flag.requires_staff_attention
        for flag in flags
    )

    # --------------------------------------------------------
    # Return dashboard-friendly data
    # --------------------------------------------------------

    return {
        "success": True,
        "red_flag_detected": len(flags) > 0,
        "overall_severity": overall_severity,

        "total_flags": len(flags),

        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,

        "staff_alert_required": staff_alert_required,

        "alerts": [
            {
                "flag_id": flag.flag_id,
                "category": flag.category,
                "symptom": flag.symptom,
                "severity": flag.severity,
                "reason": flag.reason,
                "evidence": flag.evidence,
                "recommended_action": (
                    flag.recommended_action
                ),
                "requires_staff_attention": (
                    flag.requires_staff_attention
                ),
            }
            for flag in flags
        ],

        "language": request.language,

        "disclaimer": (
            "This summary is intended to support "
            "clinical staff review. It is not a diagnosis."
        ),
    }


# ============================================================
# SEVERITY LEVELS
# ============================================================

@router.get(
    "/severity-levels",
)
def get_severity_levels():
    """
    Return available red-flag severity levels.
    """

    return {
        "success": True,
        "severity_levels": [
            {
                "level": "low",
                "description": (
                    "No major red flag detected "
                    "by the current rules."
                ),
            },
            {
                "level": "medium",
                "description": (
                    "Potential concern that may "
                    "require clinical review."
                ),
            },
            {
                "level": "high",
                "description": (
                    "Potential warning sign requiring "
                    "prompt staff attention."
                ),
            },
            {
                "level": "critical",
                "description": (
                    "Potential serious warning sign "
                    "requiring immediate staff attention."
                ),
            },
        ],
    }


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

@router.get(
    "/languages",
)
def get_supported_languages():
    """
    Return languages supported by the red-flag endpoint.
    """

    return {
        "success": True,
        "languages": [
            {
                "code": "en",
                "name": "English",
            },
            {
                "code": "ta",
                "name": "Tamil",
            },
            {
                "code": "hi",
                "name": "Hindi",
            },
            {
                "code": "te",
                "name": "Telugu",
            },
            {
                "code": "kn",
                "name": "Kannada",
            },
            {
                "code": "ml",
                "name": "Malayalam",
            },
        ],
    }


# ============================================================
# DISCLAIMER
# ============================================================

@router.get(
    "/disclaimer",
)
def red_flag_disclaimer():
    """
    Return the clinical safety disclaimer.
    """

    return {
        "success": True,
        "disclaimer": (
            "MediKiosk red-flag detection is an "
            "AI-assisted clinical support feature. "
            "It identifies potential warning signs "
            "from provided information and alerts "
            "appropriate staff. It does not diagnose "
            "medical conditions and should not replace "
            "professional clinical assessment."
        ),
    }