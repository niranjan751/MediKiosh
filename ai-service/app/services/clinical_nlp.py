"""
MediKiosk - Clinical NLP Service
================================

Purpose
-------
This module provides lightweight, explainable Clinical NLP for the
MediKiosk prototype.

Main responsibilities
---------------------
1. Extract medical entities from clinical text.
2. Identify symptoms, conditions, medications and laboratory information.
3. Detect negation such as:
       "no fever"
       "denies chest pain"

4. Detect uncertainty such as:
       "possible infection"
       "might have fever"

5. Extract:
       - duration
       - severity
       - body part
       - dosage
       - frequency
       - temporal information

6. Produce a structured clinical representation.

Important safety note
---------------------
This module is NOT a diagnostic system.

It does not:
    - diagnose diseases
    - recommend treatment
    - prescribe medicines
    - replace a doctor
    - determine whether a patient has a disease

It is intended for:
    - information extraction
    - clinical documentation support
    - document structuring
    - interview summarization
    - downstream AI-assisted workflows
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# SERVICE INFORMATION
# ============================================================================

SERVICE_NAME = "MediKiosk Clinical NLP Service"

SERVICE_VERSION = "1.0.0"

CLINICAL_NLP_DISCLAIMER = (
    "Clinical NLP is used only for information extraction and clinical "
    "documentation support. It does not provide a medical diagnosis, "
    "treatment recommendation, prescription, or emergency medical decision."
)


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ClinicalEntity:
    """
    Represents one extracted clinical entity.
    """

    text: str
    normalized_text: str
    entity_type: str
    confidence: float = 0.0

    negated: bool = False
    uncertain: bool = False

    severity: Optional[str] = None
    duration: Optional[str] = None
    body_part: Optional[str] = None

    dosage: Optional[str] = None
    frequency: Optional[str] = None

    source_sentence: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None

    attributes: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SentenceAnalysis:
    """
    Structured analysis of a single clinical sentence.
    """

    sentence: str

    entities: List[ClinicalEntity]

    negation_detected: bool = False
    uncertainty_detected: bool = False

    severity: Optional[str] = None
    duration: Optional[str] = None

    red_flag_terms: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sentence": self.sentence,
            "entities": [
                entity.to_dict()
                for entity in self.entities
            ],
            "negation_detected": self.negation_detected,
            "uncertainty_detected": self.uncertainty_detected,
            "severity": self.severity,
            "duration": self.duration,
            "red_flag_terms": self.red_flag_terms or [],
        }


# ============================================================================
# NORMALIZATION
# ============================================================================

NORMALIZATION_MAP = {
    # Symptoms
    "fever": "fever",
    "high temperature": "fever",
    "temperature": "fever",

    "cough": "cough",
    "dry cough": "dry cough",
    "cold": "common cold",
    "runny nose": "runny nose",
    "blocked nose": "nasal congestion",
    "nasal congestion": "nasal congestion",

    "headache": "headache",
    "head pain": "headache",

    "chest pain": "chest pain",
    "chest discomfort": "chest pain",

    "stomach pain": "abdominal pain",
    "abdominal pain": "abdominal pain",
    "belly pain": "abdominal pain",

    "vomiting": "vomiting",
    "nausea": "nausea",

    "dizziness": "dizziness",
    "weakness": "weakness",
    "fatigue": "fatigue",

    "shortness of breath": "shortness of breath",
    "breathing difficulty": "breathing difficulty",
    "difficulty breathing": "breathing difficulty",

    "back pain": "back pain",
    "joint pain": "joint pain",
    "muscle pain": "muscle pain",

    # Conditions
    "diabetes": "diabetes",
    "diabetic": "diabetes",

    "hypertension": "hypertension",
    "high blood pressure": "hypertension",

    "asthma": "asthma",

    "heart disease": "heart disease",
    "cardiac disease": "heart disease",

    "kidney disease": "kidney disease",

    "liver disease": "liver disease",

    "thyroid disease": "thyroid disease",

    "anemia": "anemia",

    "infection": "infection",

    "migraine": "migraine",

    # Medications
    "paracetamol": "paracetamol",
    "acetaminophen": "paracetamol",

    "ibuprofen": "ibuprofen",

    "amoxicillin": "amoxicillin",

    "azithromycin": "azithromycin",

    "metformin": "metformin",

    "insulin": "insulin",

    "amlodipine": "amlodipine",

    "omeprazole": "omeprazole",

    "pantoprazole": "pantoprazole",
}


# ============================================================================
# MEDICAL VOCABULARY
# ============================================================================

SYMPTOMS = {
    "fever",
    "high temperature",
    "cough",
    "dry cough",
    "cold",
    "runny nose",
    "blocked nose",
    "nasal congestion",
    "headache",
    "head pain",
    "chest pain",
    "chest discomfort",
    "stomach pain",
    "abdominal pain",
    "belly pain",
    "vomiting",
    "nausea",
    "dizziness",
    "weakness",
    "fatigue",
    "shortness of breath",
    "breathing difficulty",
    "difficulty breathing",
    "back pain",
    "joint pain",
    "muscle pain",
    "sore throat",
    "throat pain",
    "diarrhea",
    "constipation",
    "rash",
    "itching",
    "swelling",
    "palpitations",
    "fainting",
    "loss of consciousness",
    "blurred vision",
    "abdominal cramps",
    "loss of appetite",
    "weight loss",
    "weight gain",
}


CONDITIONS = {
    "diabetes",
    "diabetic",
    "hypertension",
    "high blood pressure",
    "asthma",
    "heart disease",
    "cardiac disease",
    "kidney disease",
    "liver disease",
    "thyroid disease",
    "anemia",
    "infection",
    "migraine",
    "arthritis",
    "pneumonia",
    "tuberculosis",
    "covid",
    "covid-19",
    "coronary artery disease",
    "chronic kidney disease",
    "chronic liver disease",
}


MEDICATIONS = {
    "paracetamol",
    "acetaminophen",
    "ibuprofen",
    "amoxicillin",
    "azithromycin",
    "metformin",
    "insulin",
    "amlodipine",
    "omeprazole",
    "pantoprazole",
    "cetirizine",
    "aspirin",
    "atorvastatin",
    "losartan",
    "telmisartan",
    "glimepiride",
}


LAB_TESTS = {
    "blood sugar",
    "blood glucose",
    "fasting blood sugar",
    "postprandial blood sugar",
    "hba1c",
    "hemoglobin",
    "haemoglobin",
    "white blood cell count",
    "wbc",
    "platelet count",
    "platelets",
    "creatinine",
    "urea",
    "bilirubin",
    "cholesterol",
    "total cholesterol",
    "hdl",
    "ldl",
    "triglycerides",
    "tsh",
    "t3",
    "t4",
    "blood pressure",
    "heart rate",
    "oxygen saturation",
    "spo2",
    "temperature",
    "esr",
    "crp",
    "urine test",
    "urinalysis",
    "liver function test",
    "lft",
    "kidney function test",
    "kft",
    "renal function test",
}


BODY_PARTS = {
    "head",
    "eye",
    "eyes",
    "ear",
    "ears",
    "nose",
    "throat",
    "neck",
    "chest",
    "heart",
    "abdomen",
    "stomach",
    "back",
    "lower back",
    "upper back",
    "arm",
    "arms",
    "hand",
    "hands",
    "leg",
    "legs",
    "knee",
    "knees",
    "ankle",
    "foot",
    "feet",
    "hip",
    "shoulder",
    "shoulders",
}


ALLERGIES = {
    "penicillin",
    "amoxicillin",
    "aspirin",
    "ibuprofen",
    "sulfa",
    "sulfonamide",
    "dust",
    "pollen",
    "peanuts",
    "peanut",
    "milk",
    "egg",
    "eggs",
    "seafood",
    "shellfish",
    "latex",
}


PROCEDURES = {
    "surgery",
    "operation",
    "biopsy",
    "endoscopy",
    "colonoscopy",
    "ultrasound",
    "x-ray",
    "xray",
    "mri",
    "ct scan",
    "ecg",
    "ekg",
    "blood test",
    "urine test",
}


# ============================================================================
# NEGATION
# ============================================================================

NEGATION_TERMS = {
    "no",
    "not",
    "never",
    "without",
    "denies",
    "deny",
    "denied",
    "negative for",
    "does not have",
    "doesn't have",
    "do not have",
    "don't have",
    "has no",
    "having no",
    "free of",
    "absence of",
}


NEGATION_PATTERNS = [
    r"\bno\s+{term}\b",
    r"\bnot\s+{term}\b",
    r"\bdenies\s+{term}\b",
    r"\bdenied\s+{term}\b",
    r"\bwithout\s+{term}\b",
    r"\bnegative\s+for\s+{term}\b",
    r"\bdoes\s+not\s+have\s+{term}\b",
    r"\bdoesn't\s+have\s+{term}\b",
    r"\bdo\s+not\s+have\s+{term}\b",
    r"\bdon't\s+have\s+{term}\b",
]


# ============================================================================
# UNCERTAINTY
# ============================================================================

UNCERTAINTY_TERMS = {
    "possible",
    "possibly",
    "maybe",
    "might",
    "may",
    "could",
    "suspected",
    "suspect",
    "likely",
    "unlikely",
    "probable",
    "questionable",
    "appears to",
    "suggestive of",
    "concern for",
    "rule out",
    "r/o",
}


# ============================================================================
# SEVERITY
# ============================================================================

SEVERITY_TERMS = {
    "mild": "mild",
    "slight": "mild",
    "minor": "mild",

    "moderate": "moderate",
    "medium": "moderate",

    "severe": "severe",
    "very severe": "severe",
    "extreme": "severe",
    "intense": "severe",

    "critical": "critical",
    "life threatening": "critical",
    "life-threatening": "critical",
}


# ============================================================================
# RED FLAG TERMS
# ============================================================================

RED_FLAG_TERMS = {
    "chest pain",
    "severe chest pain",
    "shortness of breath",
    "difficulty breathing",
    "loss of consciousness",
    "fainting",
    "severe bleeding",
    "heavy bleeding",
    "stroke",
    "facial drooping",
    "slurred speech",
    "severe allergic reaction",
    "anaphylaxis",
    "suicidal thoughts",
    "suicidal",
}


# ============================================================================
# DOSAGE / FREQUENCY PATTERNS
# ============================================================================

DOSAGE_PATTERNS = [
    r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|kg|ml|mL|µg|units?|iu)\b",
    r"\b\d+(?:\.\d+)?\s*(?:milligram|milligrams|gram|grams|milliliter|milliliters)\b",
]


FREQUENCY_PATTERNS = [
    r"\bonce\s+(?:a|per)\s+day\b",
    r"\btwice\s+(?:a|per)\s+day\b",
    r"\bthrice\s+(?:a|per)\s+day\b",
    r"\bonce\s+daily\b",
    r"\btwice\s+daily\b",
    r"\bthree\s+times\s+(?:a|per)\s+day\b",
    r"\b\d+\s+times\s+(?:a|per)\s+day\b",
    r"\bevery\s+\d+\s+(?:hour|hours|day|days)\b",
    r"\bqhs\b",
    r"\bbid\b",
    r"\btid\b",
    r"\bqid\b",
    r"\bod\b",
]


# ============================================================================
# DURATION PATTERNS
# ============================================================================

DURATION_PATTERNS = [
    r"\bfor\s+\d+\s+(?:minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\b",
    r"\b\d+\s+(?:minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\s+ago\b",
    r"\bsince\s+(?:yesterday|today|morning|last night|last week|last month)\b",
    r"\bsince\s+\w+\b",
    r"\bfor\s+a\s+few\s+days\b",
    r"\bfor\s+several\s+days\b",
    r"\bfor\s+the\s+past\s+\d+\s+\w+\b",
]


# ============================================================================
# LAB VALUE PATTERNS
# ============================================================================

LAB_VALUE_PATTERNS = [
    r"\b(?:hba1c|a1c)\s*(?:is|=|:)?\s*\d+(?:\.\d+)?\s*%?\b",
    r"\b(?:blood sugar|glucose)\s*(?:is|=|:)?\s*\d+(?:\.\d+)?\s*(?:mg/dl|mg/dL)?\b",
    r"\b(?:hemoglobin|haemoglobin|hb)\s*(?:is|=|:)?\s*\d+(?:\.\d+)?\s*(?:g/dl|g/dL)?\b",
    r"\b(?:creatinine)\s*(?:is|=|:)?\s*\d+(?:\.\d+)?\s*(?:mg/dl|mg/dL)?\b",
    r"\b(?:spo2|oxygen saturation)\s*(?:is|=|:)?\s*\d+(?:\.\d+)?\s*%?\b",
    r"\b(?:heart rate|pulse)\s*(?:is|=|:)?\s*\d+\s*(?:bpm)?\b",
    r"\b(?:temperature)\s*(?:is|=|:)?\s*\d+(?:\.\d+)?\s*(?:°c|c|f|°f)?\b",
]


# ============================================================================
# DATE PATTERNS
# ============================================================================

DATE_PATTERNS = [
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b",
    r"\b(?:today|yesterday|tomorrow)\b",
    r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    r"\b(?:january|february|march|april|may|june|july|august|"
    r"september|october|november|december)\b",
]


# ============================================================================
# TEXT UTILITIES
# ============================================================================

def normalize_text(text: str) -> str:
    """
    Normalize text for NLP processing.
    """

    if not text:
        return ""

    text = str(text)

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_entity_text(text: str) -> str:
    """
    Normalize one entity.
    """

    value = normalize_text(text).lower()

    value = re.sub(r"[.,;:!?]+$", "", value)

    if value in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[value]

    return value


def safe_confidence(value: float) -> float:
    """
    Keep confidence between 0 and 1.
    """

    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0

    return round(max(0.0, min(1.0, value)), 4)


def unique_strings(values: List[str]) -> List[str]:
    """
    Remove duplicate strings while preserving order.
    """

    result = []

    seen = set()

    for value in values:
        cleaned = normalize_text(value)

        if not cleaned:
            continue

        key = cleaned.lower()

        if key not in seen:
            seen.add(key)
            result.append(cleaned)

    return result


# ============================================================================
# SENTENCE SPLITTING
# ============================================================================

def split_sentences(text: str) -> List[str]:
    """
    Split clinical text into sentences.

    This intentionally uses a lightweight approach so the service can run
    without requiring a large NLP model.
    """

    text = normalize_text(text)

    if not text:
        return []

    parts = re.split(r"(?<=[.!?])\s+", text)

    sentences = []

    for part in parts:
        part = part.strip()

        if part:
            sentences.append(part)

    return sentences


# ============================================================================
# GENERIC TERM SEARCH
# ============================================================================

def _find_terms(
    text: str,
    vocabulary: set[str],
) -> List[Tuple[str, int, int]]:
    """
    Find vocabulary terms in text.

    Longer phrases are searched first so that:
        "chest pain"
    is preferred over:
        "pain"
    """

    text_lower = text.lower()

    sorted_terms = sorted(
        vocabulary,
        key=lambda item: len(item),
        reverse=True,
    )

    matches = []

    for term in sorted_terms:

        pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"

        for match in re.finditer(pattern, text_lower):

            matches.append(
                (
                    term,
                    match.start(),
                    match.end(),
                )
            )

    return _remove_overlapping_matches(matches)


def _remove_overlapping_matches(
    matches: List[Tuple[str, int, int]],
) -> List[Tuple[str, int, int]]:
    """
    Remove overlapping entity matches.

    Longer entities are preferred.
    """

    if not matches:
        return []

    matches = sorted(
        matches,
        key=lambda item: (
            -(item[2] - item[1]),
            item[1],
        ),
    )

    selected = []

    for match in matches:

        _, start, end = match

        overlaps = False

        for _, existing_start, existing_end in selected:

            if start < existing_end and end > existing_start:
                overlaps = True
                break

        if not overlaps:
            selected.append(match)

    return sorted(
        selected,
        key=lambda item: item[1],
    )


# ============================================================================
# NEGATION DETECTION
# ============================================================================

def is_negated(
    text: str,
    entity_start: int,
    entity_text: str,
    window: int = 60,
) -> bool:
    """
    Detect whether an entity is negated.

    Example:
        "no fever"
        "denies chest pain"
        "without vomiting"

    This is a lightweight heuristic, not a clinical-grade negation model.
    """

    before_start = max(0, entity_start - window)

    before_text = text[before_start:entity_start].lower()

    entity_lower = entity_text.lower()

    for pattern_template in NEGATION_PATTERNS:

        pattern = pattern_template.format(
            term=re.escape(entity_lower)
        )

        if re.search(pattern, before_text + entity_lower):
            return True

    # Simple nearby negation check
    words = before_text.split()

    recent_words = words[-8:]

    for term in NEGATION_TERMS:

        if term in " ".join(recent_words):
            return True

    return False


# ============================================================================
# UNCERTAINTY DETECTION
# ============================================================================

def is_uncertain(
    text: str,
    entity_start: int,
    window: int = 80,
) -> bool:
    """
    Detect uncertainty around an entity.
    """

    before_start = max(0, entity_start - window)

    context = text[before_start:entity_start].lower()

    for term in UNCERTAINTY_TERMS:

        if term in context:
            return True

    return False


# ============================================================================
# SEVERITY DETECTION
# ============================================================================

def detect_severity(
    text: str,
    entity_start: Optional[int] = None,
    window: int = 80,
) -> Optional[str]:
    """
    Detect severity near an entity.
    """

    if not text:
        return None

    if entity_start is None:
        context = text.lower()
    else:
        start = max(0, entity_start - window)

        end = min(
            len(text),
            entity_start + window,
        )

        context = text[start:end].lower()

    # Search longer phrases first.
    sorted_terms = sorted(
        SEVERITY_TERMS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for term, severity in sorted_terms:

        if term in context:
            return severity

    return None


# ============================================================================
# DURATION EXTRACTION
# ============================================================================

def extract_durations(text: str) -> List[str]:
    """
    Extract duration expressions.
    """

    text = normalize_text(text)

    results = []

    for pattern in DURATION_PATTERNS:

        matches = re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        for match in matches:
            results.append(match.group(0))

    return unique_strings(results)


# ============================================================================
# DOSAGE EXTRACTION
# ============================================================================

def extract_dosages(text: str) -> List[str]:
    """
    Extract medication dosage expressions.
    """

    text = normalize_text(text)

    results = []

    for pattern in DOSAGE_PATTERNS:

        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            results.append(match.group(0))

    return unique_strings(results)


# ============================================================================
# FREQUENCY EXTRACTION
# ============================================================================

def extract_frequencies(text: str) -> List[str]:
    """
    Extract medication frequency expressions.
    """

    text = normalize_text(text)

    results = []

    for pattern in FREQUENCY_PATTERNS:

        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            results.append(match.group(0))

    return unique_strings(results)


# ============================================================================
# LAB VALUE EXTRACTION
# ============================================================================

def extract_lab_values(text: str) -> List[str]:
    """
    Extract common laboratory/vital-value expressions.
    """

    text = normalize_text(text)

    results = []

    for pattern in LAB_VALUE_PATTERNS:

        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            results.append(match.group(0))

    return unique_strings(results)


# ============================================================================
# DATE EXTRACTION
# ============================================================================

def extract_dates(text: str) -> List[str]:
    """
    Extract basic date and temporal expressions.
    """

    text = normalize_text(text)

    results = []

    for pattern in DATE_PATTERNS:

        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            results.append(match.group(0))

    return unique_strings(results)


# ============================================================================
# ENTITY CREATION
# ============================================================================

def _create_entity(
    *,
    text: str,
    entity_type: str,
    confidence: float,
    source_text: str,
    start: int,
    end: int,
) -> ClinicalEntity:

    normalized = normalize_entity_text(text)

    negated = is_negated(
        source_text,
        start,
        text,
    )

    uncertain = is_uncertain(
        source_text,
        start,
    )

    severity = detect_severity(
        source_text,
        start,
    )

    return ClinicalEntity(
        text=text,
        normalized_text=normalized,
        entity_type=entity_type,
        confidence=safe_confidence(confidence),
        negated=negated,
        uncertain=uncertain,
        severity=severity,
        source_sentence=source_text,
        start=start,
        end=end,
        attributes={},
    )


# ============================================================================
# SYMPTOM EXTRACTION
# ============================================================================

def extract_symptoms(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract symptom entities.
    """

    text = normalize_text(text)

    entities = []

    for term, start, end in _find_terms(
        text,
        SYMPTOMS,
    ):

        original = text[start:end]

        confidence = 0.92

        if original.lower() != term.lower():
            confidence = 0.90

        entity = _create_entity(
            text=original,
            entity_type="SYMPTOM",
            confidence=confidence,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# CONDITION EXTRACTION
# ============================================================================

def extract_conditions(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract known medical condition terms.
    """

    text = normalize_text(text)

    entities = []

    for term, start, end in _find_terms(
        text,
        CONDITIONS,
    ):

        original = text[start:end]

        entity = _create_entity(
            text=original,
            entity_type="CONDITION",
            confidence=0.90,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# MEDICATION EXTRACTION
# ============================================================================

def extract_medications(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract medication names.
    """

    text = normalize_text(text)

    entities = []

    for term, start, end in _find_terms(
        text,
        MEDICATIONS,
    ):

        original = text[start:end]

        entity = _create_entity(
            text=original,
            entity_type="MEDICATION",
            confidence=0.93,
            source_text=text,
            start=start,
            end=end,
        )

        # Search around medication for dosage.
        context_start = max(0, start - 20)
        context_end = min(len(text), end + 60)

        context = text[
            context_start:context_end
        ]

        dosage_values = extract_dosages(context)

        frequency_values = extract_frequencies(context)

        if dosage_values:
            entity.dosage = dosage_values[0]

        if frequency_values:
            entity.frequency = frequency_values[0]

        entities.append(entity)

    return entities


# ============================================================================
# LAB TEST EXTRACTION
# ============================================================================

def extract_lab_tests(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract laboratory tests and common vital measurements.
    """

    text = normalize_text(text)

    entities = []

    for term, start, end in _find_terms(
        text,
        LAB_TESTS,
    ):

        original = text[start:end]

        entity = _create_entity(
            text=original,
            entity_type="LAB_TEST",
            confidence=0.88,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# BODY PART EXTRACTION
# ============================================================================

def extract_body_parts(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract body parts.
    """

    text = normalize_text(text)

    entities = []

    for term, start, end in _find_terms(
        text,
        BODY_PARTS,
    ):

        original = text[start:end]

        entity = _create_entity(
            text=original,
            entity_type="BODY_PART",
            confidence=0.95,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# ALLERGY EXTRACTION
# ============================================================================

def extract_allergies(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract allergy-related terms.

    This function also checks whether the surrounding sentence contains
    words such as "allergic" or "allergy".
    """

    text = normalize_text(text)

    entities = []

    lower_text = text.lower()

    allergy_context = (
        "allergy" in lower_text
        or "allergic" in lower_text
        or "allergies" in lower_text
    )

    for term, start, end in _find_terms(
        text,
        ALLERGIES,
    ):

        original = text[start:end]

        confidence = 0.80 if allergy_context else 0.55

        entity = _create_entity(
            text=original,
            entity_type="ALLERGY",
            confidence=confidence,
            source_text=text,
            start=start,
            end=end,
        )

        if not allergy_context:
            entity.attributes["allergy_context_missing"] = True

        entities.append(entity)

    return entities


# ============================================================================
# PROCEDURE EXTRACTION
# ============================================================================

def extract_procedures(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract medical procedures/tests.
    """

    text = normalize_text(text)

    entities = []

    for term, start, end in _find_terms(
        text,
        PROCEDURES,
    ):

        original = text[start:end]

        entity = _create_entity(
            text=original,
            entity_type="PROCEDURE",
            confidence=0.86,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# DOSAGE ENTITY EXTRACTION
# ============================================================================

def extract_dosage_entities(
    text: str,
) -> List[ClinicalEntity]:
    """
    Convert dosage strings into ClinicalEntity objects.
    """

    entities = []

    for dosage in extract_dosages(text):

        start = text.lower().find(
            dosage.lower()
        )

        if start < 0:
            continue

        end = start + len(dosage)

        entity = _create_entity(
            text=dosage,
            entity_type="DOSAGE",
            confidence=0.95,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# LAB VALUE ENTITY EXTRACTION
# ============================================================================

def extract_lab_value_entities(
    text: str,
) -> List[ClinicalEntity]:
    """
    Convert lab-value strings into ClinicalEntity objects.
    """

    entities = []

    for value in extract_lab_values(text):

        start = text.lower().find(
            value.lower()
        )

        if start < 0:
            continue

        end = start + len(value)

        entity = _create_entity(
            text=value,
            entity_type="LAB_VALUE",
            confidence=0.90,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# DATE ENTITY EXTRACTION
# ============================================================================

def extract_date_entities(
    text: str,
) -> List[ClinicalEntity]:
    """
    Convert dates/temporal expressions into entities.
    """

    entities = []

    for value in extract_dates(text):

        start = text.lower().find(
            value.lower()
        )

        if start < 0:
            continue

        end = start + len(value)

        entity = _create_entity(
            text=value,
            entity_type="DATE",
            confidence=0.90,
            source_text=text,
            start=start,
            end=end,
        )

        entities.append(entity)

    return entities


# ============================================================================
# ENTITY DEDUPLICATION
# ============================================================================

def deduplicate_entities(
    entities: List[ClinicalEntity],
) -> List[ClinicalEntity]:
    """
    Remove duplicate entities.

    Preference:
    1. Higher confidence
    2. Longer text
    """

    if not entities:
        return []

    sorted_entities = sorted(
        entities,
        key=lambda entity: (
            -entity.confidence,
            -len(entity.text),
            entity.start if entity.start is not None else 999999,
        ),
    )

    selected: List[ClinicalEntity] = []

    seen = set()

    for entity in sorted_entities:

        key = (
            entity.entity_type,
            entity.normalized_text,
            entity.negated,
        )

        if key in seen:
            continue

        seen.add(key)

        selected.append(entity)

    return sorted(
        selected,
        key=lambda entity: (
            entity.start
            if entity.start is not None
            else 999999
        ),
    )


# ============================================================================
# ENTITY EXTRACTION
# ============================================================================

def extract_entities(
    text: str,
) -> List[ClinicalEntity]:
    """
    Extract all supported clinical entities.
    """

    text = normalize_text(text)

    if not text:
        return []

    entities: List[ClinicalEntity] = []

    entities.extend(
        extract_symptoms(text)
    )

    entities.extend(
        extract_conditions(text)
    )

    entities.extend(
        extract_medications(text)
    )

    entities.extend(
        extract_lab_tests(text)
    )

    entities.extend(
        extract_body_parts(text)
    )

    entities.extend(
        extract_allergies(text)
    )

    entities.extend(
        extract_procedures(text)
    )

    entities.extend(
        extract_dosage_entities(text)
    )

    entities.extend(
        extract_lab_value_entities(text)
    )

    entities.extend(
        extract_date_entities(text)
    )

    return deduplicate_entities(entities)


# ============================================================================
# RED FLAG TERM DETECTION
# ============================================================================

def detect_red_flag_terms(
    text: str,
) -> List[str]:
    """
    Identify red-flag keywords.

    Important:
    This only identifies potentially important terms.
    It does NOT determine whether the patient is experiencing an emergency.
    """

    text = normalize_text(text)

    if not text:
        return []

    matches = []

    for term, _, _ in _find_terms(
        text,
        RED_FLAG_TERMS,
    ):

        matches.append(term)

    return unique_strings(matches)


# ============================================================================
# NEGATION SUMMARY
# ============================================================================

def get_negated_entities(
    entities: List[ClinicalEntity],
) -> List[ClinicalEntity]:
    """
    Return only negated entities.
    """

    return [
        entity
        for entity in entities
        if entity.negated
    ]


def get_positive_entities(
    entities: List[ClinicalEntity],
) -> List[ClinicalEntity]:
    """
    Return entities that are not negated.
    """

    return [
        entity
        for entity in entities
        if not entity.negated
    ]


def get_uncertain_entities(
    entities: List[ClinicalEntity],
) -> List[ClinicalEntity]:
    """
    Return uncertain entities.
    """

    return [
        entity
        for entity in entities
        if entity.uncertain
    ]


# ============================================================================
# ENTITY TYPE GROUPING
# ============================================================================

def group_entities(
    entities: List[ClinicalEntity],
) -> Dict[str, List[ClinicalEntity]]:
    """
    Group entities by entity type.
    """

    groups: Dict[str, List[ClinicalEntity]] = {}

    for entity in entities:

        groups.setdefault(
            entity.entity_type,
            [],
        ).append(entity)

    return groups


# ============================================================================
# CHIEF COMPLAINT EXTRACTION
# ============================================================================

CHIEF_COMPLAINT_PATTERNS = [
    r"(?:chief complaint|complains of|complaint of)\s*[:\-]?\s*(.+)",
    r"(?:presenting with|presented with)\s*[:\-]?\s*(.+)",
    r"(?:main problem|main complaint)\s*[:\-]?\s*(.+)",
]


def extract_chief_complaint(
    text: str,
) -> Optional[str]:
    """
    Extract a likely chief complaint from the beginning of a clinical note.
    """

    text = normalize_text(text)

    if not text:
        return None

    for pattern in CHIEF_COMPLAINT_PATTERNS:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:

            complaint = match.group(1)

            complaint = complaint.split(".")[0]

            complaint = complaint.strip()

            if complaint:
                return complaint

    # Fallback:
    # use the first sentence if it contains a symptom.
    sentences = split_sentences(text)

    if sentences:

        first_sentence = sentences[0]

        symptoms = extract_symptoms(
            first_sentence
        )

        if symptoms:
            return first_sentence

    return None


# ============================================================================
# ASSOCIATION HELPERS
# ============================================================================

def _find_nearest_body_part(
    entity: ClinicalEntity,
    body_parts: List[ClinicalEntity],
    max_distance: int = 80,
) -> Optional[str]:
    """
    Find the nearest body part around an entity.
    """

    if entity.start is None:
        return None

    nearest = None
    nearest_distance = None

    for body in body_parts:

        if body.start is None:
            continue

        distance = abs(
            body.start - entity.start
        )

        if distance <= max_distance:

            if (
                nearest_distance is None
                or distance < nearest_distance
            ):
                nearest = body.normalized_text
                nearest_distance = distance

    return nearest


def enrich_entities(
    entities: List[ClinicalEntity],
) -> List[ClinicalEntity]:
    """
    Add contextual information to entities.

    Example:
        "severe chest pain for 2 days"

    Can become approximately:

        entity_type: SYMPTOM
        normalized_text: chest pain
        severity: severe
        duration: 2 days
    """

    body_parts = [
        entity
        for entity in entities
        if entity.entity_type == "BODY_PART"
    ]

    return entities


# ============================================================================
# SENTENCE ANALYSIS
# ============================================================================

def analyze_sentence(
    sentence: str,
) -> SentenceAnalysis:
    """
    Analyze one clinical sentence.
    """

    sentence = normalize_text(sentence)

    entities = extract_entities(
        sentence
    )

    red_flags = detect_red_flag_terms(
        sentence
    )

    durations = extract_durations(
        sentence
    )

    severity = detect_severity(
        sentence
    )

    negation_detected = any(
        entity.negated
        for entity in entities
    )

    uncertainty_detected = any(
        entity.uncertain
        for entity in entities
    )

    return SentenceAnalysis(
        sentence=sentence,
        entities=entities,
        negation_detected=negation_detected,
        uncertainty_detected=uncertainty_detected,
        severity=severity,
        duration=durations[0]
        if durations
        else None,
        red_flag_terms=red_flags,
    )


# ============================================================================
# CLINICAL TEXT ANALYSIS
# ============================================================================

def analyze_clinical_text(
    text: str,
) -> Dict[str, Any]:
    """
    Perform complete clinical NLP analysis.

    Returns a structured dictionary suitable for:
        - FastAPI responses
        - database storage
        - clinical summary generation
        - dashboard display
        - downstream AI processing
    """

    text = normalize_text(text)

    if not text:
        return {
            "success": False,
            "message": "Clinical text is empty.",
            "text": "",
            "entities": [],
            "sentences": [],
        }

    entities = extract_entities(
        text
    )

    groups = group_entities(
        entities
    )

    sentences = split_sentences(
        text
    )

    sentence_analysis = [
        analyze_sentence(sentence)
        for sentence in sentences
    ]

    durations = extract_durations(
        text
    )

    dosages = extract_dosages(
        text
    )

    frequencies = extract_frequencies(
        text
    )

    lab_values = extract_lab_values(
        text
    )

    dates = extract_dates(
        text
    )

    red_flags = detect_red_flag_terms(
        text
    )

    chief_complaint = extract_chief_complaint(
        text
    )

    negated_entities = get_negated_entities(
        entities
    )

    uncertain_entities = get_uncertain_entities(
        entities
    )

    positive_entities = get_positive_entities(
        entities
    )

    return {
        "success": True,
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,

        "text": text,

        "chief_complaint": chief_complaint,

        "entities": [
            entity.to_dict()
            for entity in entities
        ],

        "entity_counts": {
            entity_type: len(values)
            for entity_type, values in groups.items()
        },

        "symptoms": [
            entity.to_dict()
            for entity in groups.get(
                "SYMPTOM",
                [],
            )
        ],

        "conditions": [
            entity.to_dict()
            for entity in groups.get(
                "CONDITION",
                [],
            )
        ],

        "medications": [
            entity.to_dict()
            for entity in groups.get(
                "MEDICATION",
                [],
            )
        ],

        "lab_tests": [
            entity.to_dict()
            for entity in groups.get(
                "LAB_TEST",
                [],
            )
        ],

        "lab_values": [
            entity.to_dict()
            for entity in groups.get(
                "LAB_VALUE",
                [],
            )
        ],

        "allergies": [
            entity.to_dict()
            for entity in groups.get(
                "ALLERGY",
                [],
            )
        ],

        "body_parts": [
            entity.to_dict()
            for entity in groups.get(
                "BODY_PART",
                [],
            )
        ],

        "procedures": [
            entity.to_dict()
            for entity in groups.get(
                "PROCEDURE",
                [],
            )
        ],

        "dosages": dosages,

        "frequencies": frequencies,

        "durations": durations,

        "dates": dates,

        "red_flag_terms": red_flags,

        "negated_entities": [
            entity.to_dict()
            for entity in negated_entities
        ],

        "uncertain_entities": [
            entity.to_dict()
            for entity in uncertain_entities
        ],

        "positive_entities": [
            entity.to_dict()
            for entity in positive_entities
        ],

        "sentence_analysis": [
            item.to_dict()
            for item in sentence_analysis
        ],

        "statistics": {
            "sentence_count": len(sentences),
            "entity_count": len(entities),
            "symptom_count": len(
                groups.get("SYMPTOM", [])
            ),
            "condition_count": len(
                groups.get("CONDITION", [])
            ),
            "medication_count": len(
                groups.get("MEDICATION", [])
            ),
            "lab_test_count": len(
                groups.get("LAB_TEST", [])
            ),
            "red_flag_term_count": len(
                red_flags
            ),
        },

        "disclaimer": CLINICAL_NLP_DISCLAIMER,
    }


# ============================================================================
# CLINICAL INFORMATION EXTRACTION
# ============================================================================

def extract_clinical_information(
    text: str,
) -> Dict[str, Any]:
    """
    Return a cleaner structured representation for other MediKiosk services.

    This function is useful when the summary service needs structured
    information rather than every low-level NLP detail.
    """

    analysis = analyze_clinical_text(
        text
    )

    if not analysis.get("success"):
        return analysis

    return {
        "success": True,

        "chief_complaint": analysis.get(
            "chief_complaint"
        ),

        "symptoms": [
            item["normalized_text"]
            for item in analysis.get(
                "symptoms",
                [],
            )
            if not item.get("negated")
        ],

        "negative_symptoms": [
            item["normalized_text"]
            for item in analysis.get(
                "symptoms",
                [],
            )
            if item.get("negated")
        ],

        "conditions": [
            item["normalized_text"]
            for item in analysis.get(
                "conditions",
                [],
            )
            if not item.get("negated")
        ],

        "medications": [
            {
                "name": item["normalized_text"],
                "dosage": item.get("dosage"),
                "frequency": item.get("frequency"),
            }
            for item in analysis.get(
                "medications",
                [],
            )
        ],

        "allergies": [
            item["normalized_text"]
            for item in analysis.get(
                "allergies",
                [],
            )
        ],

        "lab_tests": [
            item["normalized_text"]
            for item in analysis.get(
                "lab_tests",
                [],
            )
        ],

        "lab_values": analysis.get(
            "lab_values",
            [],
        ),

        "durations": analysis.get(
            "durations",
            [],
        ),

        "red_flag_terms": analysis.get(
            "red_flag_terms",
            [],
        ),

        "uncertain_findings": [
            item["normalized_text"]
            for item in analysis.get(
                "uncertain_entities",
                [],
            )
        ],

        "disclaimer": CLINICAL_NLP_DISCLAIMER,
    }


# ============================================================================
# CLINICAL SUMMARY INPUT PREPARATION
# ============================================================================

def prepare_summary_data(
    text: str,
) -> Dict[str, Any]:
    """
    Prepare NLP output for the existing summary_service.py.

    This function deliberately does not generate a diagnosis.
    """

    information = extract_clinical_information(
        text
    )

    if not information.get("success"):
        return information

    return {
        "chief_complaint": information.get(
            "chief_complaint"
        ),

        "symptoms": information.get(
            "symptoms",
            [],
        ),

        "negative_symptoms": information.get(
            "negative_symptoms",
            [],
        ),

        "medical_history": information.get(
            "conditions",
            [],
        ),

        "medications": information.get(
            "medications",
            [],
        ),

        "allergies": information.get(
            "allergies",
            [],
        ),

        "lab_tests": information.get(
            "lab_tests",
            [],
        ),

        "lab_values": information.get(
            "lab_values",
            [],
        ),

        "duration": (
            information.get(
                "durations",
                [],
            )[0]
            if information.get(
                "durations",
                [],
            )
            else None
        ),

        "red_flag_terms": information.get(
            "red_flag_terms",
            [],
        ),

        "uncertain_findings": information.get(
            "uncertain_findings",
            [],
        ),

        "disclaimer": CLINICAL_NLP_DISCLAIMER,
    }


# ============================================================================
# CLINICAL NLP QUALITY METRICS
# ============================================================================

def calculate_nlp_statistics(
    entities: List[ClinicalEntity],
) -> Dict[str, Any]:
    """
    Calculate simple extraction statistics.

    These are engineering metrics, NOT medical accuracy metrics.
    """

    if not entities:
        return {
            "entity_count": 0,
            "average_confidence": 0.0,
            "high_confidence_count": 0,
            "medium_confidence_count": 0,
            "low_confidence_count": 0,
        }

    confidences = [
        entity.confidence
        for entity in entities
    ]

    average_confidence = (
        sum(confidences)
        / len(confidences)
    )

    high = sum(
        1
        for value in confidences
        if value >= 0.85
    )

    medium = sum(
        1
        for value in confidences
        if 0.60 <= value < 0.85
    )

    low = sum(
        1
        for value in confidences
        if value < 0.60
    )

    return {
        "entity_count": len(entities),
        "average_confidence": round(
            average_confidence,
            4,
        ),
        "high_confidence_count": high,
        "medium_confidence_count": medium,
        "low_confidence_count": low,
    }


# ============================================================================
# SERVICE STATUS
# ============================================================================

def get_clinical_nlp_status() -> Dict[str, Any]:
    """
    Return service status.
    """

    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "ready",
        "implementation": "rule_based_clinical_nlp",
        "diagnosis_supported": False,
        "features": {
            "symptom_extraction": True,
            "condition_extraction": True,
            "medication_extraction": True,
            "dosage_extraction": True,
            "frequency_extraction": True,
            "lab_test_extraction": True,
            "lab_value_extraction": True,
            "allergy_extraction": True,
            "body_part_extraction": True,
            "procedure_extraction": True,
            "negation_detection": True,
            "uncertainty_detection": True,
            "severity_detection": True,
            "duration_extraction": True,
            "date_extraction": True,
            "red_flag_term_detection": True,
            "chief_complaint_extraction": True,
        },
        "disclaimer": CLINICAL_NLP_DISCLAIMER,
    }


# ============================================================================
# SUPPORTED ENTITY TYPES
# ============================================================================

def get_supported_entity_types() -> List[str]:
    """
    Return all supported entity types.
    """

    return [
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


# ============================================================================
# VALIDATION
# ============================================================================

def validate_clinical_text(
    text: str,
) -> Dict[str, Any]:
    """
    Validate clinical text before NLP processing.
    """

    cleaned = normalize_text(text)

    if not cleaned:
        return {
            "valid": False,
            "message": "Clinical text cannot be empty.",
        }

    if len(cleaned) < 3:
        return {
            "valid": False,
            "message": "Clinical text is too short.",
        }

    if len(cleaned) > 100000:
        return {
            "valid": False,
            "message": "Clinical text exceeds the maximum supported length.",
        }

    return {
        "valid": True,
        "message": "Clinical text is valid.",
        "character_count": len(cleaned),
        "word_count": len(cleaned.split()),
    }


# ============================================================================
# PUBLIC MAIN FUNCTION
# ============================================================================

def process_clinical_text(
    text: str,
) -> Dict[str, Any]:
    """
    Main public entry point.

    Other MediKiosk modules should preferably call this function instead of
    directly calling multiple extraction functions.
    """

    validation = validate_clinical_text(
        text
    )

    if not validation["valid"]:
        return {
            "success": False,
            "validation": validation,
            "disclaimer": CLINICAL_NLP_DISCLAIMER,
        }

    result = analyze_clinical_text(
        text
    )

    entities = [
        ClinicalEntity(
            **{
                key: value
                for key, value in item.items()
                if key in {
                    "text",
                    "normalized_text",
                    "entity_type",
                    "confidence",
                    "negated",
                    "uncertain",
                    "severity",
                    "duration",
                    "body_part",
                    "dosage",
                    "frequency",
                    "source_sentence",
                    "start",
                    "end",
                    "attributes",
                }
            }
        )
        for item in result.get(
            "entities",
            [],
        )
    ]

    result["nlp_statistics"] = (
        calculate_nlp_statistics(
            entities
        )
    )

    result["validation"] = validation

    return result


# ============================================================================
# DEMO / LOCAL TEST
# ============================================================================

if __name__ == "__main__":

    sample_text = (
        "Patient complains of severe chest pain for 2 days. "
        "The patient has diabetes and hypertension. "
        "Currently taking metformin 500 mg twice daily. "
        "Patient denies vomiting but reports dizziness. "
        "Possible infection was mentioned. "
        "HbA1c is 7.2%."
    )

    result = process_clinical_text(
        sample_text
    )

    print("=" * 80)
    print(SERVICE_NAME)
    print("=" * 80)

    print(
        "Chief Complaint:",
        result.get("chief_complaint"),
    )

    print(
        "\nSymptoms:"
    )

    for symptom in result.get(
        "symptoms",
        [],
    ):
        print(
            " -",
            symptom["normalized_text"],
            "| negated:",
            symptom["negated"],
            "| severity:",
            symptom["severity"],
        )

    print(
        "\nConditions:"
    )

    for condition in result.get(
        "conditions",
        [],
    ):
        print(
            " -",
            condition["normalized_text"],
        )

    print(
        "\nMedications:"
    )

    for medication in result.get(
        "medications",
        [],
    ):
        print(
            " -",
            medication["normalized_text"],
            "| dosage:",
            medication["dosage"],
            "| frequency:",
            medication["frequency"],
        )

    print(
        "\nLab Values:"
    )

    for value in result.get(
        "lab_values",
        [],
    ):
        print(
            " -",
            value["text"],
        )

    print(
        "\nRed Flag Terms:",
        result.get(
            "red_flag_terms",
            [],
        ),
    )

    print(
        "\nNLP Statistics:",
        result.get(
            "nlp_statistics",
            {},
        ),
    )

    print(
        "\nDISCLAIMER:",
        CLINICAL_NLP_DISCLAIMER,
    )