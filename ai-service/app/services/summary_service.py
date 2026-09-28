"""
MediKiosk AI Service
Clinical Summary Service

Purpose:
    Generate a structured clinical summary from:
    - Patient information
    - Clinical interview answers
    - Symptoms
    - Medical history
    - Medications
    - Allergies
    - Family history
    - Red-flag detection
    - OCR medical document information

Important:
    This service organizes information for clinical review.
    It does not diagnose the patient.
"""


from typing import Any, Dict, List, Optional


# ============================================================
# CONSTANTS
# ============================================================

SUMMARY_DISCLAIMER = (
    "This summary is AI-assisted and intended for clinical "
    "information organization only. It is not a diagnosis "
    "or autonomous medical decision. A qualified healthcare "
    "professional must review and confirm the information."
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value: Any) -> str:
    """
    Convert a value into clean text.
    """

    if value is None:
        return ""

    return str(value).strip()


def clean_list(items: Any) -> List[str]:
    """
    Convert a value into a clean list of strings.
    """

    if items is None:
        return []

    if isinstance(items, str):
        return [items.strip()] if items.strip() else []

    if not isinstance(items, list):
        return []

    result = []

    for item in items:
        text = clean_text(item)

        if text:
            result.append(text)

    return result


# ============================================================
# PATIENT INFORMATION
# ============================================================

def build_patient_information(
    patient: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build structured patient information.
    """

    patient = patient or {}

    return {
        "patient_id": clean_text(
            patient.get("patient_id")
        ),
        "name": clean_text(
            patient.get("name")
        ),
        "age": patient.get("age"),
        "gender": clean_text(
            patient.get("gender")
        ),
        "language": clean_text(
            patient.get("language")
        ),
    }


# ============================================================
# CHIEF COMPLAINT
# ============================================================

def extract_chief_complaint(
    interview_data: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Extract the main complaint from interview data.
    """

    interview_data = interview_data or {}

    fields = [
        "chief_complaint",
        "main_complaint",
        "complaint",
        "presenting_complaint",
    ]

    for field in fields:

        value = clean_text(
            interview_data.get(field)
        )

        if value:
            return value

    return "Not provided"


# ============================================================
# SYMPTOMS
# ============================================================

def extract_symptoms(
    interview_data: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Extract structured symptoms.
    """

    interview_data = interview_data or {}

    symptoms = interview_data.get(
        "symptoms",
        []
    )

    if not isinstance(symptoms, list):
        symptoms = [symptoms]

    result = []

    for symptom in symptoms:

        if isinstance(symptom, dict):

            name = clean_text(
                symptom.get("name")
                or symptom.get("symptom")
            )

            if not name:
                continue

            result.append(
                {
                    "name": name,
                    "severity": clean_text(
                        symptom.get("severity")
                    ),
                    "duration": clean_text(
                        symptom.get("duration")
                    ),
                    "location": clean_text(
                        symptom.get("location")
                    ),
                    "onset": clean_text(
                        symptom.get("onset")
                    ),
                }
            )

        else:

            name = clean_text(symptom)

            if name:
                result.append(
                    {
                        "name": name,
                        "severity": "",
                        "duration": "",
                        "location": "",
                        "onset": "",
                    }
                )

    return result


# ============================================================
# MEDICAL HISTORY
# ============================================================

def extract_medical_history(
    interview_data: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """
    Extract previous medical history.
    """

    interview_data = interview_data or {}

    history = interview_data.get(
        "medical_history",
        interview_data.get("history", [])
    )

    return clean_list(history)


# ============================================================
# MEDICATIONS
# ============================================================

def extract_medications(
    interview_data: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Extract current medications.
    """

    interview_data = interview_data or {}

    medications = interview_data.get(
        "medications",
        []
    )

    if not isinstance(medications, list):
        medications = [medications]

    result = []

    for medication in medications:

        if isinstance(medication, dict):

            name = clean_text(
                medication.get("name")
                or medication.get("medicine")
            )

            if not name:
                continue

            result.append(
                {
                    "name": name,
                    "dose": clean_text(
                        medication.get("dose")
                    ),
                    "frequency": clean_text(
                        medication.get("frequency")
                    ),
                    "duration": clean_text(
                        medication.get("duration")
                    ),
                }
            )

        else:

            name = clean_text(medication)

            if name:
                result.append(
                    {
                        "name": name,
                        "dose": "",
                        "frequency": "",
                        "duration": "",
                    }
                )

    return result


# ============================================================
# ALLERGIES
# ============================================================

def extract_allergies(
    interview_data: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """
    Extract patient allergies.
    """

    interview_data = interview_data or {}

    allergies = interview_data.get(
        "allergies",
        []
    )

    return clean_list(allergies)


# ============================================================
# FAMILY HISTORY
# ============================================================

def extract_family_history(
    interview_data: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """
    Extract family medical history.
    """

    interview_data = interview_data or {}

    family_history = interview_data.get(
        "family_history",
        []
    )

    return clean_list(family_history)


# ============================================================
# RED FLAG INFORMATION
# ============================================================

def extract_red_flags(
    red_flag_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Extract information from the red-flag detection service.
    """

    red_flag_data = red_flag_data or {}

    flags = red_flag_data.get(
        "red_flags",
        red_flag_data.get("flags", [])
    )

    if not isinstance(flags, list):
        flags = []

    cleaned_flags = []

    for flag in flags:

        if isinstance(flag, dict):

            name = clean_text(
                flag.get("name")
                or flag.get("title")
                or flag.get("flag")
            )

            severity = clean_text(
                flag.get("severity")
            )

            message = clean_text(
                flag.get("message")
                or flag.get("description")
            )

            if name:
                cleaned_flags.append(
                    {
                        "name": name,
                        "severity": severity,
                        "message": message,
                    }
                )

        else:

            name = clean_text(flag)

            if name:
                cleaned_flags.append(
                    {
                        "name": name,
                        "severity": "",
                        "message": "",
                    }
                )

    return {
        "detected": bool(cleaned_flags),
        "count": len(cleaned_flags),
        "flags": cleaned_flags,
        "requires_clinical_review": bool(
            cleaned_flags
        ),
    }


# ============================================================
# DOCUMENT INFORMATION
# ============================================================

def extract_document_information(
    document_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Extract useful information from OCR processing.
    """

    document_data = document_data or {}

    entities = document_data.get(
        "medical_entities",
        document_data.get("entities", [])
    )

    if not isinstance(entities, list):
        entities = []

    cleaned_entities = []

    for entity in entities:

        if isinstance(entity, dict):

            text = clean_text(
                entity.get("text")
                or entity.get("value")
            )

            entity_type = clean_text(
                entity.get("type")
                or entity.get("entity_type")
            )

            if text:
                cleaned_entities.append(
                    {
                        "text": text,
                        "type": entity_type,
                        "confidence": entity.get(
                            "confidence"
                        ),
                    }
                )

    return {
        "document_type": clean_text(
            document_data.get("document_type")
        ),
        "filename": clean_text(
            document_data.get("filename")
        ),
        "processing_status": clean_text(
            document_data.get("processing_status")
        ),
        "ocr_text_preview": clean_text(
            document_data.get("text_preview")
            or document_data.get("ocr_text_preview")
        ),
        "medical_entities": cleaned_entities,
    }


# ============================================================
# GENERATE CLINICAL SUMMARY
# ============================================================

def generate_clinical_summary(
    patient: Optional[Dict[str, Any]] = None,
    interview_data: Optional[Dict[str, Any]] = None,
    red_flag_data: Optional[Dict[str, Any]] = None,
    document_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate a structured AI-assisted clinical summary.
    """

    patient_information = build_patient_information(
        patient
    )

    interview_data = interview_data or {}

    chief_complaint = extract_chief_complaint(
        interview_data
    )

    symptoms = extract_symptoms(
        interview_data
    )

    medical_history = extract_medical_history(
        interview_data
    )

    medications = extract_medications(
        interview_data
    )

    allergies = extract_allergies(
        interview_data
    )

    family_history = extract_family_history(
        interview_data
    )

    red_flags = extract_red_flags(
        red_flag_data
    )

    document_information = extract_document_information(
        document_data
    )

    summary = {
        "patient": patient_information,

        "clinical_summary": {
            "chief_complaint": chief_complaint,
            "symptoms": symptoms,
            "medical_history": medical_history,
            "current_medications": medications,
            "allergies": allergies,
            "family_history": family_history,
        },

        "red_flag_assessment": red_flags,

        "document_information": document_information,

        "clinical_review": {
            "requires_doctor_review": True,
            "doctor_review_status": "pending",
        },

        "ai_metadata": {
            "generated_by": (
                "MediKiosk AI Clinical Summary Service"
            ),
            "ai_assisted": True,
            "diagnosis_generated": False,
            "autonomous_decision": False,
        },

        "disclaimer": SUMMARY_DISCLAIMER,
    }

    return summary


# ============================================================
# SHORT SUMMARY
# ============================================================

def create_short_summary(
    summary: Dict[str, Any],
) -> str:
    """
    Create a short readable summary.
    """

    clinical = summary.get(
        "clinical_summary",
        {}
    )

    parts = []

    # --------------------------------------------------------
    # Chief complaint
    # --------------------------------------------------------

    complaint = clean_text(
        clinical.get("chief_complaint")
    )

    if complaint and complaint != "Not provided":
        parts.append(
            f"Chief complaint: {complaint}."
        )

    # --------------------------------------------------------
    # Symptoms
    # --------------------------------------------------------

    symptoms = clinical.get(
        "symptoms",
        []
    )

    symptom_names = []

    for symptom in symptoms:

        if isinstance(symptom, dict):

            name = clean_text(
                symptom.get("name")
            )

            if name:
                symptom_names.append(name)

    if symptom_names:
        parts.append(
            "Reported symptoms: "
            + ", ".join(symptom_names)
            + "."
        )

    # --------------------------------------------------------
    # Medical history
    # --------------------------------------------------------

    history = clinical.get(
        "medical_history",
        []
    )

    if history:
        parts.append(
            "Medical history: "
            + ", ".join(history)
            + "."
        )

    # --------------------------------------------------------
    # Medications
    # --------------------------------------------------------

    medications = clinical.get(
        "current_medications",
        []
    )

    medication_names = []

    for medication in medications:

        if isinstance(medication, dict):

            name = clean_text(
                medication.get("name")
            )

            if name:
                medication_names.append(name)

    if medication_names:
        parts.append(
            "Current medications: "
            + ", ".join(medication_names)
            + "."
        )

    # --------------------------------------------------------
    # Allergies
    # --------------------------------------------------------

    allergies = clinical.get(
        "allergies",
        []
    )

    if allergies:
        parts.append(
            "Allergies: "
            + ", ".join(allergies)
            + "."
        )

    # --------------------------------------------------------
    # Red flags
    # --------------------------------------------------------

    red_flags = summary.get(
        "red_flag_assessment",
        {}
    )

    if red_flags.get("detected"):
        parts.append(
            "Red-flag findings detected and "
            "require clinical review."
        )

    # --------------------------------------------------------
    # Empty result
    # --------------------------------------------------------

    if not parts:
        return (
            "No sufficient clinical information is "
            "available to generate a summary."
        )

    return " ".join(parts)


# ============================================================
# DOCTOR REVIEW
# ============================================================

def apply_doctor_review(
    summary: Dict[str, Any],
    doctor_notes: str,
    doctor_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add doctor review information to the AI summary.
    """

    updated_summary = dict(summary)

    updated_summary["clinical_review"] = {
        "requires_doctor_review": False,
        "doctor_review_status": "reviewed",
        "doctor_name": clean_text(
            doctor_name
        ),
        "doctor_notes": clean_text(
            doctor_notes
        ),
    }

    return updated_summary


# ============================================================
# SERVICE HEALTH
# ============================================================

def get_summary_service_status() -> Dict[str, Any]:
    """
    Return clinical summary service status.
    """

    return {
        "service": "Clinical Summary Service",
        "status": "online",
        "ai_assisted": True,
        "diagnosis": False,
        "autonomous_medical_decision": False,
        "doctor_review_required": True,
    }