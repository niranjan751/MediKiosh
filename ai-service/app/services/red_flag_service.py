from typing import Dict, List

from app.models.schemas import (
    AlertSeverity,
    LanguageCode,
    RedFlag,
)


# ============================================================
# RED FLAG KEYWORDS
# ============================================================

RED_FLAG_RULES = {
    "chest_pain": {
        "keywords": [
            "chest pain",
            "chest pressure",
            "chest tightness",
            "chest discomfort",
        ],
        "category": "cardiac",
        "severity": AlertSeverity.HIGH,
        "symptom": "Chest pain or chest discomfort",
        "reason": (
            "The patient reported chest pain or chest discomfort."
        ),
        "recommended_action": (
            "Alert clinical staff for prompt assessment."
        ),
    },

    "breathing_difficulty": {
        "keywords": [
            "difficulty breathing",
            "shortness of breath",
            "breathlessness",
            "cannot breathe",
            "can't breathe",
            "breathing problem",
        ],
        "category": "respiratory",
        "severity": AlertSeverity.HIGH,
        "symptom": "Breathing difficulty",
        "reason": (
            "The patient reported difficulty breathing "
            "or significant shortness of breath."
        ),
        "recommended_action": (
            "Alert clinical staff for prompt assessment."
        ),
    },

    "loss_of_consciousness": {
        "keywords": [
            "unconscious",
            "passed out",
            "fainted",
            "fainting",
            "lost consciousness",
        ],
        "category": "neurological",
        "severity": AlertSeverity.CRITICAL,
        "symptom": "Loss of consciousness",
        "reason": (
            "The patient reported fainting or loss of consciousness."
        ),
        "recommended_action": (
            "Alert clinical staff immediately."
        ),
    },

    "severe_bleeding": {
        "keywords": [
            "heavy bleeding",
            "severe bleeding",
            "blood loss",
            "bleeding heavily",
        ],
        "category": "bleeding",
        "severity": AlertSeverity.CRITICAL,
        "symptom": "Severe bleeding",
        "reason": (
            "The patient reported potentially significant bleeding."
        ),
        "recommended_action": (
            "Alert clinical staff immediately."
        ),
    },

    "severe_abdominal_pain": {
        "keywords": [
            "severe abdominal pain",
            "severe stomach pain",
            "extreme stomach pain",
            "extreme abdominal pain",
        ],
        "category": "abdominal",
        "severity": AlertSeverity.HIGH,
        "symptom": "Severe abdominal pain",
        "reason": (
            "The patient reported severe abdominal or stomach pain."
        ),
        "recommended_action": (
            "Alert clinical staff for prompt assessment."
        ),
    },

    "stroke_warning": {
        "keywords": [
            "face drooping",
            "facial drooping",
            "slurred speech",
            "speech difficulty",
            "sudden weakness",
            "sudden numbness",
            "one sided weakness",
            "one-sided weakness",
        ],
        "category": "neurological",
        "severity": AlertSeverity.CRITICAL,
        "symptom": "Possible acute neurological warning sign",
        "reason": (
            "The patient reported a sudden neurological warning sign."
        ),
        "recommended_action": (
            "Alert clinical staff immediately."
        ),
    },

    "severe_allergic_reaction": {
        "keywords": [
            "swelling of face",
            "face swelling",
            "throat swelling",
            "difficulty swallowing",
            "severe allergic reaction",
            "anaphylaxis",
        ],
        "category": "allergic_reaction",
        "severity": AlertSeverity.CRITICAL,
        "symptom": "Possible severe allergic reaction",
        "reason": (
            "The patient reported symptoms that may require "
            "urgent clinical assessment."
        ),
        "recommended_action": (
            "Alert clinical staff immediately."
        ),
    },

    "severe_vomiting": {
        "keywords": [
            "vomiting blood",
            "blood in vomit",
            "continuous vomiting",
            "severe vomiting",
        ],
        "category": "gastrointestinal",
        "severity": AlertSeverity.HIGH,
        "symptom": "Severe or concerning vomiting",
        "reason": (
            "The patient reported severe vomiting or blood in vomit."
        ),
        "recommended_action": (
            "Alert clinical staff for prompt assessment."
        ),
    },

    "suicidal_thoughts": {
        "keywords": [
            "suicidal thoughts",
            "want to die",
            "kill myself",
            "harm myself",
            "self harm",
            "self-harm",
        ],
        "category": "mental_health",
        "severity": AlertSeverity.CRITICAL,
        "symptom": "Self-harm or suicidal thoughts",
        "reason": (
            "The patient reported content indicating "
            "possible immediate mental-health risk."
        ),
        "recommended_action": (
            "Alert appropriate clinical staff immediately "
            "for safety assessment."
        ),
    },
}


# ============================================================
# LANGUAGE-SPECIFIC KEYWORDS
# ============================================================
# These are simple prototype keywords.
# A future NLP model can replace this rule-based layer.

MULTILINGUAL_KEYWORDS = {
    LanguageCode.TAMIL: {
        "chest_pain": [
            "நெஞ்சு வலி",
            "மார்பு வலி",
        ],
        "breathing_difficulty": [
            "மூச்சுத்திணறல்",
            "மூச்சு விடுவதில் சிரமம்",
        ],
        "fainting": [
            "மயக்கம்",
            "நினைவிழப்பு",
        ],
    },

    LanguageCode.HINDI: {
        "chest_pain": [
            "सीने में दर्द",
            "छाती में दर्द",
        ],
        "breathing_difficulty": [
            "सांस लेने में कठिनाई",
            "सांस फूलना",
        ],
        "fainting": [
            "बेहोशी",
            "बेहोश",
        ],
    },

    LanguageCode.TELUGU: {
        "chest_pain": [
            "ఛాతీ నొప్పి",
            "గుండె నొప్పి",
        ],
        "breathing_difficulty": [
            "శ్వాస తీసుకోవడంలో ఇబ్బంది",
            "ఊపిరి తీసుకోవడంలో ఇబ్బంది",
        ],
    },

    LanguageCode.KANNADA: {
        "chest_pain": [
            "ಎದೆ ನೋವು",
            "ಎದೆಯಲ್ಲಿ ನೋವು",
        ],
        "breathing_difficulty": [
            "ಉಸಿರಾಟದ ತೊಂದರೆ",
            "ಉಸಿರಾಟ ಕಷ್ಟ",
        ],
    },

    LanguageCode.MALAYALAM: {
        "chest_pain": [
            "നെഞ്ചുവേദന",
            "നെഞ്ചിൽ വേദന",
        ],
        "breathing_difficulty": [
            "ശ്വാസംമുട്ടൽ",
            "ശ്വസിക്കാൻ ബുദ്ധിമുട്ട്",
        ],
    },
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize clinical text for keyword matching.
    """

    if not text:
        return ""

    return " ".join(
        text.lower().strip().split()
    )


# ============================================================
# COLLECT TEXT
# ============================================================

def collect_clinical_text(
    symptoms: List[str],
    clinical_text: str,
    interview_answers: Dict[str, str],
) -> str:
    """
    Combine all available patient text into one searchable string.
    """

    parts = []

    if clinical_text:
        parts.append(clinical_text)

    if symptoms:
        parts.extend(symptoms)

    if interview_answers:
        parts.extend(
            str(value)
            for value in interview_answers.values()
            if value
        )

    return normalize_text(
        " ".join(parts)
    )


# ============================================================
# CHECK ENGLISH RED FLAGS
# ============================================================

def check_english_rules(
    text: str,
) -> List[RedFlag]:
    """
    Check English clinical text against red-flag rules.
    """

    flags = []

    for flag_id, rule in RED_FLAG_RULES.items():

        matched_keyword = None

        for keyword in rule["keywords"]:
            if normalize_text(keyword) in text:
                matched_keyword = keyword
                break

        if matched_keyword:

            flags.append(
                RedFlag(
                    flag_id=flag_id,
                    category=rule["category"],
                    symptom=rule["symptom"],
                    severity=rule["severity"],
                    reason=rule["reason"],
                    evidence=matched_keyword,
                    recommended_action=(
                        rule["recommended_action"]
                    ),
                    requires_staff_attention=True,
                )
            )

    return flags


# ============================================================
# CHECK MULTILINGUAL RULES
# ============================================================

def check_multilingual_rules(
    text: str,
    language: LanguageCode,
) -> List[RedFlag]:
    """
    Check supported multilingual keywords.
    """

    flags = []

    language_rules = MULTILINGUAL_KEYWORDS.get(
        language,
        {}
    )

    for rule_key, keywords in language_rules.items():

        matched_keyword = None

        for keyword in keywords:
            if keyword in text:
                matched_keyword = keyword
                break

        if not matched_keyword:
            continue

        base_rule = RED_FLAG_RULES.get(
            rule_key
        )

        if base_rule is None:

            if rule_key == "fainting":
                flags.append(
                    RedFlag(
                        flag_id="loss_of_consciousness",
                        category="neurological",
                        symptom="Possible loss of consciousness",
                        severity=AlertSeverity.CRITICAL,
                        reason=(
                            "The patient reported a symptom "
                            "that may indicate loss of consciousness."
                        ),
                        evidence=matched_keyword,
                        recommended_action=(
                            "Alert clinical staff immediately."
                        ),
                        requires_staff_attention=True,
                    )
                )

            continue

        flags.append(
            RedFlag(
                flag_id=rule_key,
                category=base_rule["category"],
                symptom=base_rule["symptom"],
                severity=base_rule["severity"],
                reason=base_rule["reason"],
                evidence=matched_keyword,
                recommended_action=(
                    base_rule["recommended_action"]
                ),
                requires_staff_attention=True,
            )
        )

    return flags


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicate_flags(
    flags: List[RedFlag],
) -> List[RedFlag]:
    """
    Remove duplicate alerts with the same flag ID.
    """

    unique_flags = {}
    
    for flag in flags:
        unique_flags[flag.flag_id] = flag

    return list(
        unique_flags.values()
    )


# ============================================================
# GET OVERALL SEVERITY
# ============================================================

def get_overall_severity(
    flags: List[RedFlag],
) -> AlertSeverity:
    """
    Determine the highest alert severity.
    """

    if not flags:
        return AlertSeverity.LOW

    severity_order = {
        AlertSeverity.LOW: 1,
        AlertSeverity.MEDIUM: 2,
        AlertSeverity.HIGH: 3,
        AlertSeverity.CRITICAL: 4,
    }

    highest = AlertSeverity.LOW

    for flag in flags:

        if (
            severity_order[flag.severity]
            > severity_order[highest]
        ):
            highest = flag.severity

    return highest


# ============================================================
# MAIN RED FLAG DETECTION
# ============================================================

def detect_red_flags(
    symptoms: List[str],
    clinical_text: str = "",
    interview_answers: Dict[str, str] = None,
    language: LanguageCode = LanguageCode.ENGLISH,
) -> List[RedFlag]:
    """
    Detect potential red flags from patient information.

    This is an alerting mechanism, not a diagnostic system.
    """

    if interview_answers is None:
        interview_answers = {}

    combined_text = collect_clinical_text(
        symptoms=symptoms,
        clinical_text=clinical_text,
        interview_answers=interview_answers,
    )

    flags = []

    # English keyword rules
    flags.extend(
        check_english_rules(
            combined_text
        )
    )

    # Multilingual keyword rules
    if language != LanguageCode.ENGLISH:

        flags.extend(
            check_multilingual_rules(
                combined_text,
                language,
            )
        )

    return remove_duplicate_flags(
        flags
    )


# ============================================================
# BUILD RED FLAG RESULT
# ============================================================

def build_red_flag_result(
    symptoms: List[str],
    clinical_text: str = "",
    interview_answers: Dict[str, str] = None,
    language: LanguageCode = LanguageCode.ENGLISH,
) -> dict:
    """
    Build a complete red-flag detection response.
    """

    flags = detect_red_flags(
        symptoms=symptoms,
        clinical_text=clinical_text,
        interview_answers=interview_answers,
        language=language,
    )

    overall_severity = get_overall_severity(
        flags
    )

    staff_alert_required = any(
        flag.requires_staff_attention
        for flag in flags
    )

    return {
        "red_flag_detected": len(flags) > 0,
        "overall_severity": overall_severity,
        "flags": flags,
        "staff_alert_required": staff_alert_required,
        "disclaimer": (
            "Red-flag detection is an alerting and "
            "clinical support feature. It is not a diagnosis."
        ),
    }