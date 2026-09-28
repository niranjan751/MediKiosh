"""
MediKiosk AI Service
Medical Utility Functions

Purpose:
    Common utilities used by the AI services for handling
    medical text, entities, medications, symptoms and
    clinical information.

Important:
    These utilities organize extracted information.
    They do not provide medical diagnosis.
"""


from typing import Any, Dict, List


# ============================================================
# MEDICAL ENTITY TYPES
# ============================================================

MEDICAL_ENTITY_TYPES = [
    "SYMPTOM",
    "CONDITION",
    "MEDICATION",
    "DOSAGE",
    "LAB_TEST",
    "LAB_VALUE",
    "DATE",
    "ALLERGY",
    "BODY_PART",
    "PROCEDURE",
]


# ============================================================
# COMMON MEDICAL TERMS
# ============================================================

COMMON_SYMPTOMS = [
    "fever",
    "cough",
    "cold",
    "headache",
    "chest pain",
    "abdominal pain",
    "stomach pain",
    "vomiting",
    "nausea",
    "dizziness",
    "fatigue",
    "weakness",
    "breathing difficulty",
    "shortness of breath",
    "back pain",
    "joint pain",
    "body pain",
    "sore throat",
    "diarrhea",
]


COMMON_CONDITIONS = [
    "diabetes",
    "hypertension",
    "asthma",
    "anemia",
    "arthritis",
    "thyroid",
    "heart disease",
    "kidney disease",
    "liver disease",
    "migraine",
]


COMMON_MEDICATIONS = [
    "paracetamol",
    "acetaminophen",
    "ibuprofen",
    "amoxicillin",
    "azithromycin",
    "metformin",
    "insulin",
    "amlodipine",
    "omeprazole",
    "cetirizine",
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_medical_text(
    text: str,
) -> str:
    """
    Normalize medical text for processing.
    """

    if not text:
        return ""

    text = str(text)

    # Remove unnecessary whitespace
    text = " ".join(
        text.split()
    )

    return text.strip()


# ============================================================
# LOWERCASE TEXT
# ============================================================

def normalize_for_matching(
    text: str,
) -> str:
    """
    Normalize text for keyword matching.
    """

    return normalize_medical_text(
        text
    ).lower()


# ============================================================
# FIND KEYWORDS
# ============================================================

def find_medical_keywords(
    text: str,
    keywords: List[str],
) -> List[str]:
    """
    Find medical keywords present in text.
    """

    normalized_text = normalize_for_matching(
        text
    )

    found = []

    for keyword in keywords:

        normalized_keyword = normalize_for_matching(
            keyword
        )

        if (
            normalized_keyword
            and normalized_keyword in normalized_text
        ):
            found.append(keyword)

    return found


# ============================================================
# FIND SYMPTOMS
# ============================================================

def find_symptoms(
    text: str,
) -> List[str]:
    """
    Find common symptoms in medical text.
    """

    return find_medical_keywords(
        text,
        COMMON_SYMPTOMS,
    )


# ============================================================
# FIND CONDITIONS
# ============================================================

def find_conditions(
    text: str,
) -> List[str]:
    """
    Find common medical conditions.
    """

    return find_medical_keywords(
        text,
        COMMON_CONDITIONS,
    )


# ============================================================
# FIND MEDICATIONS
# ============================================================

def find_medications(
    text: str,
) -> List[str]:
    """
    Find common medications.
    """

    return find_medical_keywords(
        text,
        COMMON_MEDICATIONS,
    )


# ============================================================
# CREATE MEDICAL ENTITY
# ============================================================

def create_medical_entity(
    text: str,
    entity_type: str,
    confidence: float = 0.0,
) -> Dict[str, Any]:
    """
    Create a standardized medical entity.
    """

    return {
        "text": normalize_medical_text(text),
        "type": entity_type.upper(),
        "confidence": round(
            max(0.0, min(confidence, 1.0)),
            4,
        ),
    }


# ============================================================
# EXTRACT BASIC ENTITIES
# ============================================================

def extract_basic_medical_entities(
    text: str,
) -> List[Dict[str, Any]]:
    """
    Extract basic medical entities using
    keyword matching.

    This is a lightweight prototype utility.
    """

    entities = []

    symptoms = find_symptoms(text)

    for symptom in symptoms:
        entities.append(
            create_medical_entity(
                symptom,
                "SYMPTOM",
                0.90,
            )
        )

    conditions = find_conditions(text)

    for condition in conditions:
        entities.append(
            create_medical_entity(
                condition,
                "CONDITION",
                0.90,
            )
        )

    medications = find_medications(text)

    for medication in medications:
        entities.append(
            create_medical_entity(
                medication,
                "MEDICATION",
                0.90,
            )
        )

    return entities


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicate_entities(
    entities: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Remove duplicate medical entities.
    """

    unique_entities = []
    seen = set()

    for entity in entities:

        text = normalize_for_matching(
            entity.get("text", "")
        )

        entity_type = normalize_for_matching(
            entity.get("type", "")
        )

        key = (
            entity_type,
            text,
        )

        if key in seen:
            continue

        seen.add(key)

        unique_entities.append(entity)

    return unique_entities


# ============================================================
# VALIDATE ENTITY
# ============================================================

def is_valid_medical_entity(
    entity: Dict[str, Any],
) -> bool:
    """
    Validate a medical entity.
    """

    if not isinstance(entity, dict):
        return False

    text = normalize_medical_text(
        entity.get("text", "")
    )

    entity_type = normalize_medical_text(
        entity.get("type", "")
    ).upper()

    if not text:
        return False

    if entity_type not in MEDICAL_ENTITY_TYPES:
        return False

    return True


# ============================================================
# FILTER VALID ENTITIES
# ============================================================

def filter_valid_entities(
    entities: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Keep only valid medical entities.
    """

    return [
        entity
        for entity in entities
        if is_valid_medical_entity(entity)
    ]


# ============================================================
# CREATE MEDICAL TEXT SUMMARY
# ============================================================

def create_medical_text_summary(
    text: str,
) -> Dict[str, Any]:
    """
    Create a basic structured summary from medical text.
    """

    normalized_text = normalize_medical_text(
        text
    )

    symptoms = find_symptoms(
        normalized_text
    )

    conditions = find_conditions(
        normalized_text
    )

    medications = find_medications(
        normalized_text
    )

    entities = extract_basic_medical_entities(
        normalized_text
    )

    entities = remove_duplicate_entities(
        entities
    )

    return {
        "text_length": len(normalized_text),
        "symptoms": symptoms,
        "conditions": conditions,
        "medications": medications,
        "medical_entities": entities,
        "entity_count": len(entities),
    }


# ============================================================
# SERVICE INFORMATION
# ============================================================

def get_medical_utils_status() -> Dict[str, Any]:
    """
    Return medical utility service information.
    """

    return {
        "service": "Medical Utilities",
        "status": "online",
        "entity_types": MEDICAL_ENTITY_TYPES,
        "keyword_based_extraction": True,
        "diagnosis": False,
    }