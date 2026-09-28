"""
MediKiosk AI Service - Adaptive Clinical Interview (SOCRATES Engine)
===================================================================

Purpose:
    Conduct an adaptive, conversational, multilingual clinical history interview
    using the clinically recognized SOCRATES framework:
        S - Site (Anatomical location)
        O - Onset (When and how it started - sudden vs gradual)
        C - Character (Nature of the symptom - sharp, dull, burning, aching)
        R - Radiation (Does it travel to left arm, jaw, back, etc.)
        A - Associations (Associated symptoms - sweating, nausea, breathlessness)
        T - Time / Duration (Continuous, intermittent, worsening)
        E - Exacerbating / Relieving factors (Exertion, rest, food, breathing)
        S - Severity (1-10 pain/discomfort scale)

Followed by Comprehensive Clinical History:
    - Past Medical & Surgical History
    - Current Medications
    - Drug Allergies
    - Family History
    - Social / Habits History
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from app.models.schemas import (
    ClinicalMode,
    InterviewSession,
    InterviewStatus,
    LanguageCode,
    QuestionOption,
    RedFlag,
)
from app.services.red_flag_service import detect_red_flags


# ============================================================
# COMPLAINT CATEGORY DETECTION
# ============================================================

COMPLAINT_PATTERNS = {
    "chest_pain": [
        "chest pain", "chest", "heart", "angina", "tightness", "pressure",
        "மார்பு வலி", "நெஞ்சு வலி", "நெஞ்சு", "सीने में दर्द", "छाती में दर्द",
        "గుండె నొప్పి", "ఛాతీ నొప్పి", "ಎದೆ ನೋವು", "നെഞ്ചുവേദന"
    ],
    "breathing_difficulty": [
        "breath", "breathing", "shortness of breath", "asthma", "gasping", "wheezing",
        "மூச்சுத்திணறல்", "மூச்சு", "सांस फूलना", "सांस", "శ్వాస", "ಉಸಿರಾಟ", "ശ്വാസംമുട്ടൽ"
    ],
    "abdominal_pain": [
        "stomach", "abdomen", "abdominal", "belly", "cramp", "gastric", "ulcer",
        "வயிற்று வலி", "வயிறு", "पेट में दर्द", "पेट", "కడుపు నొప్పి", "ಹೊಟ್ಟೆ ನೋವು", "വയറുവേദന"
    ],
    "headache": [
        "headache", "head pain", "migraine", "throbbing head",
        "தலைவலி", "தலை", "सिरदर्द", "सिर में दर्द", "తలనొప్పి", "ತಲೆನೋವು", "തലവേദന"
    ],
    "fever": [
        "fever", "temperature", "chills", "shivering", "hot body",
        "காய்ச்சல்", "நடுக்கம்", "बुखार", "ताप", "జ్వరం", "ಜ್ವರ", "പനി"
    ],
    "cough": [
        "cough", "cold", "sore throat", "phlegm", "runny nose",
        "இருமல்", "சளி", "தொண்டை வலி", "खांसी", "जुकाम", "దగ్గు", "ಕೆಮ್ಮು", "ചുമ"
    ],
}


def classify_chief_complaint(text: str) -> str:
    """Classifies chief complaint into a clinical category for adaptive branching."""
    if not text:
        return "general"
    normalized = text.lower().strip()
    for category, keywords in COMPLAINT_PATTERNS.items():
        for kw in keywords:
            if kw in normalized:
                return category
    return "general"


# ============================================================
# MULTILINGUAL QUESTION REPOSITORY (SOCRATES & HISTORY)
# ============================================================

def build_options(options_dict: Dict[str, List[Dict[str, str]]], language: LanguageCode) -> List[QuestionOption]:
    lang_key = language.value if hasattr(language, "value") else str(language)
    raw_list = options_dict.get(lang_key, options_dict.get("en", []))
    return [QuestionOption(**opt) for opt in raw_list]


# Initial Chief Complaint Questions
INITIAL_COMPLAINT_QUESTIONS = {
    "en": "Hello! What health concern or problem are you experiencing today?",
    "ta": "வணக்கம்! இன்று உங்களுக்கு என்ன உடல்நலப் பிரச்சனை அல்லது அசௌகரியம் உள்ளது?",
    "hi": "नमस्ते! आज आपको क्या स्वास्थ्य समस्या या परेशानी हो रही है?",
    "te": "నమస్కారం! ఈ రోజు మీ ప్రధాన ఆరోగ్య సమస్య లేదా ఇబ్బంది ఏమిటి?",
    "kn": "ನಮಸ್ಕಾರ! ಇಂದು ನಿಮ್ಮ ಮುಖ್ಯ ಆರೋಗ್ಯ ಸಮಸ್ಯೆ ಅಥವಾ ತೊಂದರೆ ಏನು?",
    "ml": "നമസ്കാരം! ഇന്ന് നിങ്ങൾക്ക് എന്തെങ്കിലും ആരോഗ്യ പ്രശ്നമോ ബുദ്ധിമുട്ടോ ഉണ്ടോ?",
}

INITIAL_COMPLAINT_OPTIONS = {
    "en": [
        {"label": "Chest Pain / Discomfort", "value": "chest pain", "icon": "heart"},
        {"label": "Difficulty Breathing", "value": "difficulty breathing", "icon": "wind"},
        {"label": "Stomach / Abdominal Pain", "value": "abdominal pain", "icon": "activity"},
        {"label": "Fever & Chills", "value": "fever", "icon": "thermometer"},
        {"label": "Severe Headache", "value": "headache", "icon": "zap"},
        {"label": "Cough & Cold", "value": "cough and cold", "icon": "cloud"},
        {"label": "General Consultation", "value": "general checkup", "icon": "user"},
    ],
    "ta": [
        {"label": "மார்பு வலி / அழுத்தம்", "value": "chest pain", "icon": "heart"},
        {"label": "மூச்சு விடுவதில் சிரமம்", "value": "difficulty breathing", "icon": "wind"},
        {"label": "வயிற்று வலி", "value": "abdominal pain", "icon": "activity"},
        {"label": "காய்ச்சல் / நடுக்கம்", "value": "fever", "icon": "thermometer"},
        {"label": "தலைவலி", "value": "headache", "icon": "zap"},
        {"label": "இருமல் மற்றும் சளி", "value": "cough and cold", "icon": "cloud"},
        {"label": "பொது உடல் பரிசோதனை", "value": "general checkup", "icon": "user"},
    ],
    "hi": [
        {"label": "सीने में दर्द / बेचैनी", "value": "chest pain", "icon": "heart"},
        {"label": "सांस लेने में कठिनाई", "value": "difficulty breathing", "icon": "wind"},
        {"label": "पेट में दर्द", "value": "abdominal pain", "icon": "activity"},
        {"label": "बुखार और ठंड लगना", "value": "fever", "icon": "thermometer"},
        {"label": "तेज सिरदर्द", "value": "headache", "icon": "zap"},
        {"label": "खांसी और जुकाम", "value": "cough and cold", "icon": "cloud"},
        {"label": "सामान्य जांच", "value": "general checkup", "icon": "user"},
    ],
    "te": [
        {"label": "ఛాతీ నొప్పి / అసౌకర్యం", "value": "chest pain", "icon": "heart"},
        {"label": "శ్వాస తీసుకోవడంలో ఇబ్బంది", "value": "difficulty breathing", "icon": "wind"},
        {"label": "కడుపు నొప్పి", "value": "abdominal pain", "icon": "activity"},
        {"label": "జ్వరం మరియు చలి", "value": "fever", "icon": "thermometer"},
        {"label": "తీవ్రమైన తలనొప్పి", "value": "headache", "icon": "zap"},
        {"label": "దగ్గు మరియు జలుబు", "value": "cough and cold", "icon": "cloud"},
    ],
    "kn": [
        {"label": "ಎದೆ ನೋವು / ಅಸ್ವಸ್ಥತೆ", "value": "chest pain", "icon": "heart"},
        {"label": "ಉಸಿರಾಟದ ತೊಂದರೆ", "value": "difficulty breathing", "icon": "wind"},
        {"label": "ಹೊಟ್ಟೆ ನೋವು", "value": "abdominal pain", "icon": "activity"},
        {"label": "ಜ್ವರ", "value": "fever", "icon": "thermometer"},
        {"label": "ತಲೆನೋವು", "value": "headache", "icon": "zap"},
    ],
    "ml": [
        {"label": "നെഞ്ചുവേദന / അസ്വസ്ഥത", "value": "chest pain", "icon": "heart"},
        {"label": "ശ്വാസമെടുക്കാൻ ബുദ്ധിമുട്ട്", "value": "difficulty breathing", "icon": "wind"},
        {"label": "വയറുവേദന", "value": "abdominal pain", "icon": "activity"},
        {"label": "പനി", "value": "fever", "icon": "thermometer"},
        {"label": "തലവേദന", "value": "headache", "icon": "zap"},
    ],
}


# ============================================================
# ADAPTIVE QUESTION QUEUES GENERATOR
# ============================================================

def get_adaptive_question_definition(
    step_key: str,
    complaint_category: str,
    language: LanguageCode,
) -> Dict[str, Any]:
    """Generates localized adaptive question and options based on SOCRATES step."""
    lang = language.value if hasattr(language, "value") else str(language)

    # 1. Onset / Time
    if step_key == "onset":
        q_text = {
            "en": "When did this symptom start?",
            "ta": "இந்த அறிகுறி எப்போது தொடங்கியது?",
            "hi": "यह लक्षण कब शुरू हुआ?",
            "te": "ఈ లక్షణం ఎప్పుడు ప్రారంభమైంది?",
            "kn": "ಈ ಲಕ್ಷಣ ಯಾವಾಗ ಪ್ರಾರಂಭವಾಯಿತು?",
            "ml": "ഈ ലക്ഷണം എപ്പോൾ ആരംഭിച്ചു?",
        }.get(lang, "When did this symptom start?")

        opts = {
            "en": [
                {"label": "Suddenly today (< 12 hours ago)", "value": "suddenly today (< 12 hours ago)"},
                {"label": "Yesterday", "value": "yesterday"},
                {"label": "Few days ago (2-4 days)", "value": "few days ago (2-4 days)"},
                {"label": "More than 1-2 weeks ago", "value": "more than 1-2 weeks ago"},
                {"label": "Longstanding / Chronic (Months)", "value": "chronic (months)"},
            ],
            "ta": [
                {"label": "இன்று திடீரென (12 மணி நேரத்திற்குள்)", "value": "suddenly today"},
                {"label": "நேற்று முதல்", "value": "yesterday"},
                {"label": "சில நாட்களாக (2-4 நாட்கள்)", "value": "few days ago"},
                {"label": "1-2 வாரங்களுக்கும் மேலாக", "value": "more than a week"},
            ],
            "hi": [
                {"label": "आज अचानक (12 घंटे के भीतर)", "value": "suddenly today"},
                {"label": "कल से", "value": "yesterday"},
                {"label": "कुछ दिनों से (2-4 दिन)", "value": "few days ago"},
                {"label": "एक सप्ताह से अधिक समय से", "value": "more than a week"},
            ],
        }
        return {
            "key": "onset",
            "category": "socrates_onset",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
            "socrates_dimension": "onset",
        }

    # 2. Site / Location
    elif step_key == "site":
        if complaint_category == "chest_pain":
            q_text = {
                "en": "Where exactly is the chest discomfort located?",
                "ta": "மார்பில் எந்த இடத்தில் வலி உள்ளது?",
                "hi": "सीने में दर्द ठीक किस जगह पर है?",
                "te": "ఛాతీలో నొప్పి ఎక్కడ ఉంది?",
                "kn": "ಎದೆಯಲ್ಲಿ ನೋವು ಎಲ್ಲಿದೆ?",
                "ml": "നെഞ്ചിൽ എവിടെയാണ് വേദന?",
            }.get(lang, "Where exactly is the chest discomfort located?")
            opts = {
                "en": [
                    {"label": "Center of Chest (Behind Breastbone)", "value": "center of chest / retrosternal"},
                    {"label": "Left Side of Chest", "value": "left side of chest"},
                    {"label": "Right Side of Chest", "value": "right side of chest"},
                    {"label": "Entire Chest / Diffuse", "value": "entire chest / diffuse"},
                ],
                "ta": [
                    {"label": "மார்பின் நடுப்பகுதி", "value": "center of chest"},
                    {"label": "இடது மார்பு", "value": "left side of chest"},
                    {"label": "வலது மார்பு", "value": "right side of chest"},
                ],
                "hi": [
                    {"label": "सीने के बीच में", "value": "center of chest"},
                    {"label": "बाईं तरफ", "value": "left side of chest"},
                    {"label": "दाईं तरफ", "value": "right side of chest"},
                ],
            }
        elif complaint_category == "abdominal_pain":
            q_text = {
                "en": "Where in your abdomen / stomach is the pain?",
                "ta": "வயிற்றில் எந்த இடத்தில் வலி அதிகமாக உள்ளது?",
                "hi": "पेट में दर्द किस हिस्से में है?",
            }.get(lang, "Where in your abdomen is the pain?")
            opts = {
                "en": [
                    {"label": "Upper Abdomen / Epigastric", "value": "upper abdomen / epigastric"},
                    {"label": "Right Lower Abdomen", "value": "right lower abdomen (appendix area)"},
                    {"label": "Left Lower Abdomen", "value": "left lower abdomen"},
                    {"label": "All Over Stomach (Diffuse)", "value": "diffuse all over abdomen"},
                ],
                "ta": [
                    {"label": "மேல் வயிறு (நெஞ்செரிச்சல் பகுதி)", "value": "upper abdomen"},
                    {"label": "வலது கீழ் வயிறு", "value": "right lower abdomen"},
                    {"label": "முழு வயிறு", "value": "all over abdomen"},
                ],
                "hi": [
                    {"label": "पेट के ऊपरी हिस्से में", "value": "upper abdomen"},
                    {"label": "दाहिनी तरफ नीचे", "value": "right lower abdomen"},
                    {"label": "पूरे पेट में", "value": "all over abdomen"},
                ],
            }
        else:
            q_text = {
                "en": "Where exactly in your body do you feel this symptom?",
                "ta": "உங்கள் உடலில் எந்த இடத்தில் இந்த உணர்வு உள்ளது?",
                "hi": "शरीर के किस हिस्से में यह समस्या महसूस हो रही है?",
            }.get(lang, "Where exactly in your body do you feel this symptom?")
            opts = {
                "en": [
                    {"label": "Head / Neck", "value": "head and neck"},
                    {"label": "Throat / Upper Airway", "value": "throat and upper airway"},
                    {"label": "Generalized / Whole Body", "value": "generalized whole body"},
                ]
            }
        return {
            "key": "site",
            "category": "socrates_site",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
            "socrates_dimension": "site",
        }

    # 3. Radiation
    elif step_key == "radiation":
        q_text = {
            "en": "Does the discomfort spread or radiate anywhere else?",
            "ta": "இந்த வலி உடலின் வேறு பகுதிக்கு பரவுகிறதா?",
            "hi": "क्या यह दर्द शरीर के किसी अन्य हिस्से में फैलता है?",
            "te": "ఈ నొప్పి ఇతర భాగాలకు వ్యాపిస్తుందా?",
            "kn": "ಈ ನೋವು ಬೇರೆ ಭಾಗಕ್ಕೆ ಹರಡುತ್ತದೆಯೇ?",
            "ml": "ഈ വേദന മറ്റ് ഭാഗങ്ങളിലേക്ക് പടരുന്നുണ്ടോ?",
        }.get(lang, "Does the discomfort spread or radiate anywhere else?")
        opts = {
            "en": [
                {"label": "Spreads to Left Arm & Shoulder", "value": "radiates to left arm and shoulder"},
                {"label": "Spreads to Jaw, Teeth, or Neck", "value": "radiates to jaw and neck"},
                {"label": "Spreads to Upper Back / Between Shoulder Blades", "value": "radiates to back"},
                {"label": "Spreads to Stomach / Abdomen", "value": "radiates to abdomen"},
                {"label": "No, it stays in one spot", "value": "no radiation, localized"},
            ],
            "ta": [
                {"label": "இடது கை மற்றும் தோள்பட்டைக்கு பரவுகிறது", "value": "radiates to left arm"},
                {"label": "தாடை மற்றும் கழுத்துக்கு பரவுகிறது", "value": "radiates to jaw and neck"},
                {"label": "முதுகுக்கு பரவுகிறது", "value": "radiates to back"},
                {"label": "இல்லை, ஓரிடத்தில் மட்டுமே உள்ளது", "value": "no radiation"},
            ],
            "hi": [
                {"label": "बाएं हाथ और कंधे में फैलता है", "value": "radiates to left arm"},
                {"label": "जबड़े और गर्दन में फैलता है", "value": "radiates to jaw"},
                {"label": "पीठ में फैलता है", "value": "radiates to back"},
                {"label": "नहीं, एक ही जगह पर है", "value": "no radiation"},
            ],
        }
        return {
            "key": "radiation",
            "category": "socrates_radiation",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
            "socrates_dimension": "radiation",
        }

    # 4. Character / Nature
    elif step_key == "character":
        q_text = {
            "en": "How would you describe the character of the symptom / pain?",
            "ta": "இந்த வலியின் தன்மை எப்படிப்பட்டது?",
            "hi": "दर्द किस तरह का महसूस होता है?",
        }.get(lang, "How would you describe the character of the pain?")
        opts = {
            "en": [
                {"label": "Heavy Pressure / Squeezing / Crushing", "value": "heavy pressure / squeezing"},
                {"label": "Sharp / Stabbing (worse with breath)", "value": "sharp / stabbing"},
                {"label": "Burning / Acidity sensation", "value": "burning sensation"},
                {"label": "Dull Ache / Heaviness", "value": "dull ache"},
                {"label": "Throbbing / Pulsating", "value": "throbbing / pulsating"},
            ],
            "ta": [
                {"label": "அழுத்தும் வலி / பிழிவது போன்ற உணர்வு", "value": "heavy pressure / squeezing"},
                {"label": "குத்துவது போன்ற கூர்மையான வலி", "value": "sharp stabbing"},
                {"label": "எரிச்சல் போன்ற வலி", "value": "burning sensation"},
                {"label": "மந்தமான வலி", "value": "dull ache"},
            ],
            "hi": [
                {"label": "दबाव या जकड़न जैसा भारी दर्द", "value": "heavy pressure / squeezing"},
                {"label": "तेज चुभने वाला दर्द", "value": "sharp stabbing"},
                {"label": "जलन जैसा दर्द", "value": "burning sensation"},
                {"label": "हल्का धीमा दर्द", "value": "dull ache"},
            ],
        }
        return {
            "key": "character",
            "category": "socrates_character",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
            "socrates_dimension": "character",
        }

    # 5. Associated Symptoms
    elif step_key == "associations":
        q_text = {
            "en": "Do you have any of these associated symptoms right now?",
            "ta": "இவற்றுடன் வேறு ஏதேனும் அறிகுறிகள் உள்ளதா?",
            "hi": "क्या साथ में इनमें से कोई अन्य लक्षण भी हैं?",
        }.get(lang, "Do you have any of these associated symptoms right now?")
        opts = {
            "en": [
                {"label": "Profuse Sweating / Cold Clammy Skin", "value": "profuse cold sweating"},
                {"label": "Shortness of Breath / Breathlessness", "value": "shortness of breath"},
                {"label": "Nausea or Vomiting", "value": "nausea and vomiting"},
                {"label": "Dizziness / Feeling Faint", "value": "dizziness / pre-syncope"},
                {"label": "Palpitations / Fast Heartbeat", "value": "palpitations"},
                {"label": "None of the above", "value": "none"},
            ],
            "ta": [
                {"label": "குளிர்ந்த வியர்வை கொட்டுதல்", "value": "cold sweating"},
                {"label": "மூச்சுத்திணறல்", "value": "shortness of breath"},
                {"label": "குமட்டல் அல்லது வாந்தி", "value": "nausea or vomiting"},
                {"label": "மயக்கம் வருவது போன்ற உணர்வு", "value": "dizziness"},
                {"label": "மேற்கண்ட எதுவுமில்லை", "value": "none"},
            ],
            "hi": [
                {"label": "ठंडा पसीना आना", "value": "cold sweating"},
                {"label": "सांस फूलना", "value": "shortness of breath"},
                {"label": "उल्टी या मतली", "value": "nausea or vomiting"},
                {"label": "चक्कर आना", "value": "dizziness"},
                {"label": "इनमें से कोई नहीं", "value": "none"},
            ],
        }
        return {
            "key": "associations",
            "category": "socrates_associations",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
            "socrates_dimension": "associations",
        }

    # 6. Severity (Scale 1 to 10)
    elif step_key == "severity":
        q_text = {
            "en": "On a scale from 1 to 10, how severe is your discomfort right now?",
            "ta": "1 முதல் 10 வரை இந்த அறிகுறியின் தீவிரம் எவ்வளவு?",
            "hi": "1 से 10 के पैमाने पर यह तकलीफ कितनी गंभीर है?",
            "te": "1 నుండి 10 వరకు తీవ్రత ఎంత?",
            "kn": "1 ರಿಂದ 10 ರವರೆಗೆ ತೀವ್ರತೆ ಎಷ್ಟು?",
            "ml": "1 മുതൽ 10 വരെ തീവ്രത എത്രയാണ്?",
        }.get(lang, "On a scale from 1 to 10, how severe is your discomfort?")
        opts = {
            "en": [
                {"label": "1 - 3 (Mild - Easily Tolerated)", "value": "mild (scale 1-3)"},
                {"label": "4 - 6 (Moderate - Interferes with work)", "value": "moderate (scale 4-6)"},
                {"label": "7 - 8 (Severe - Cannot do normal activities)", "value": "severe (scale 7-8)"},
                {"label": "9 - 10 (Very Severe / Unbearable Emergency)", "value": "critical (scale 9-10)"},
            ],
            "ta": [
                {"label": "1 - 3 (லேசானது)", "value": "mild (1-3)"},
                {"label": "4 - 6 (மிதமானது)", "value": "moderate (4-6)"},
                {"label": "7 - 8 (கடுமையானது)", "value": "severe (7-8)"},
                {"label": "9 - 10 (தாங்க முடியாத மிகத் தீவிர வலி)", "value": "critical (9-10)"},
            ],
            "hi": [
                {"label": "1 - 3 (हल्का दर्द)", "value": "mild (1-3)"},
                {"label": "4 - 6 (मध्यम दर्द)", "value": "moderate (4-6)"},
                {"label": "7 - 8 (गंभीर दर्द)", "value": "severe (7-8)"},
                {"label": "9 - 10 (अत्यधिक असहनीय दर्द)", "value": "critical (9-10)"},
            ],
        }
        return {
            "key": "severity",
            "category": "socrates_severity",
            "question": q_text,
            "input_type": "scale",
            "options": build_options(opts, language),
            "socrates_dimension": "severity",
        }

    # 7. Past Medical History
    elif step_key == "medical_history":
        q_text = {
            "en": "Do you have any existing diagnosed medical conditions?",
            "ta": "உங்களுக்கு ஏற்கனவே ஏதேனும் உடல்நல பாதிப்புகள் உள்ளதா?",
            "hi": "क्या आपको पहले से कोई बीमारी या स्वास्थ्य समस्या है?",
            "te": "మీకు ఇప్పటికే ఏవైనా ఆరోగ్య సమస్యలు ఉన్నాయా?",
            "kn": "ನಿಮಗೆ ಈಗಾಗಲೇ ಯಾವುದೇ ಆರೋಗ್ಯ ಸಮಸ್ಯೆಗಳಿವೆಯೇ?",
            "ml": "നിങ്ങൾക്ക് നേരത്തെ എന്തെങ്കിലും ആരോഗ്യ പ്രശ്നങ്ങളുണ്ടോ?",
        }.get(lang, "Do you have any existing diagnosed medical conditions?")
        opts = {
            "en": [
                {"label": "High Blood Pressure (Hypertension)", "value": "hypertension"},
                {"label": "Diabetes Mellitus", "value": "diabetes"},
                {"label": "Heart Disease / Prior Stent or Bypass", "value": "heart disease / CAD"},
                {"label": "Asthma / COPD", "value": "asthma / COPD"},
                {"label": "Thyroid Disorder", "value": "thyroid disorder"},
                {"label": "Kidney Disease", "value": "kidney disease"},
                {"label": "None / No Known Chronic Illness", "value": "none"},
            ],
            "ta": [
                {"label": "உயர் இரத்த அழுத்தம் (BP)", "value": "hypertension"},
                {"label": "சர்க்கரை நோய் (Diabetes)", "value": "diabetes"},
                {"label": "இதய நோய் / மாரடைப்பு வரலாறு", "value": "heart disease"},
                {"label": "ஆஸ்துமா", "value": "asthma"},
                {"label": "எந்த நோயும் இல்லை", "value": "none"},
            ],
            "hi": [
                {"label": "उच्च रक्तचाप (High BP)", "value": "hypertension"},
                {"label": "मधुमेह (Diabetes)", "value": "diabetes"},
                {"label": "हृदय रोग (Heart Disease)", "value": "heart disease"},
                {"label": "अस्थमा", "value": "asthma"},
                {"label": "कोई पुरानी बीमारी नहीं", "value": "none"},
            ],
        }
        return {
            "key": "medical_history",
            "category": "past_medical_history",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
        }

    # 8. Medications
    elif step_key == "medications":
        q_text = {
            "en": "Are you currently taking any prescription medicines regularly?",
            "ta": "தற்போது நீங்கள் தினமும் ஏதேனும் மருந்துகள் அல்லது மாத்திரைகள் சாப்பிடுகிறீர்களா?",
            "hi": "क्या आप वर्तमान में नियमित रूप से कोई दवा ले रहे हैं?",
            "te": "మీరు ప్రస్తుతం క్రమం తప్పకుండా ఏవైనా మందులు వాడుతున్నారా?",
            "kn": "ನೀವು ಪ್ರಸ್ತುತ ನಿಯಮಿತವಾಗಿ ಯಾವುದೇ ಔಷಧಿಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದ್ದೀರಾ?",
            "ml": "നിങ്ങൾ ഇപ്പോൾ സ്ഥിരമായി എന്തെങ്കിലും മരുന്നുകൾ കഴിക്കുന്നുണ്ടോ?",
        }.get(lang, "Are you currently taking any prescription medicines regularly?")
        opts = {
            "en": [
                {"label": "Blood Pressure Medicine (Amlodipine/Telmisartan, etc.)", "value": "BP medication"},
                {"label": "Diabetes Medicine (Metformin/Insulin, etc.)", "value": "Diabetes medication"},
                {"label": "Blood Thinners / Aspirin / Clopidogrel", "value": "Blood thinners / Aspirin"},
                {"label": "Cholesterol / Statin Medicine", "value": "Cholesterol medication"},
                {"label": "Inhalers for Asthma", "value": "Inhalers"},
                {"label": "No regular medicines", "value": "none"},
            ],
            "ta": [
                {"label": "பிபி மாத்திரை (BP tablets)", "value": "BP medication"},
                {"label": "சர்க்கரை மாத்திரை / இன்சுலின்", "value": "Diabetes medication"},
                {"label": "ரத்தத்தை நீர்க்க வைக்கும் மாத்திரை (Aspirin)", "value": "Blood thinners"},
                {"label": "எந்த மருந்தும் எடுப்பதில்லை", "value": "none"},
            ],
            "hi": [
                {"label": "बीपी की दवा", "value": "BP medication"},
                {"label": "शुगर / डायबिटीज की दवा या इंसुलिन", "value": "Diabetes medication"},
                {"label": "खून पतला करने वाली दवा (Aspirin)", "value": "Blood thinners"},
                {"label": "कोई नियमित दवा नहीं", "value": "none"},
            ],
        }
        return {
            "key": "medications",
            "category": "medication_history",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
        }

    # 9. Allergies
    elif step_key == "allergies":
        q_text = {
            "en": "Do you have any known allergies to medicines, foods, or substances?",
            "ta": "உங்களுக்கு மருந்துகள், உணவுகள் அல்லது பிறவற்றிற்கு ஏதேனும் ஒவ்வாமை (Allergy) உள்ளதா?",
            "hi": "क्या आपको किसी दवा, भोजन या अन्य चीज से एलर्जी है?",
            "te": "మీకు మందులు లేదా ఆహారంతో ఏవైనా అలెర్జీలు ఉన్నాయా?",
            "kn": "ನಿಮಗೆ ಯಾವುದೇ ಔಷಧಿ ಅಥವಾ ಆಹಾರ ಅಲರ್ಜಿ ಇದೆಯೇ?",
            "ml": "നിങ്ങൾക്ക് ഏതെങ്കിലും മരുന്നുകളോടോ ഭക്ഷണമോടോ അലർജിയുണ്ടോ?",
        }.get(lang, "Do you have any known allergies to medicines or foods?")
        opts = {
            "en": [
                {"label": "Penicillin / Amoxicillin Allergy", "value": "Penicillin allergy"},
                {"label": "Sulfa Drug Allergy", "value": "Sulfa drug allergy"},
                {"label": "Aspirin / NSAID Painkiller Allergy", "value": "Aspirin / NSAID allergy"},
                {"label": "Food Allergies (Peanuts, Seafood, Milk, Egg)", "value": "Food allergy"},
                {"label": "No Known Drug or Food Allergies (NKDA)", "value": "No known allergies"},
            ],
            "ta": [
                {"label": "பென்சிலின் அலர்ஜி (Penicillin)", "value": "Penicillin allergy"},
                {"label": "வலி நிவாரணி மாத்திரை அலர்ஜி", "value": "Painkiller allergy"},
                {"label": "உணவு அலர்ஜி", "value": "Food allergy"},
                {"label": "எந்த அலர்ஜியும் இல்லை (NKDA)", "value": "No known allergies"},
            ],
            "hi": [
                {"label": "पेनिसिलिन से एलर्जी", "value": "Penicillin allergy"},
                {"label": "दर्द निवारक दवाओं से एलर्जी", "value": "Painkiller allergy"},
                {"label": "खाने की चीजों से एलर्जी", "value": "Food allergy"},
                {"label": "कोई एलर्जी नहीं है", "value": "No known allergies"},
            ],
        }
        return {
            "key": "allergies",
            "category": "allergy_history",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
        }

    # 10. Family History
    else:
        q_text = {
            "en": "Is there any family history of heart attack, stroke, diabetes, or cancer?",
            "ta": "உங்கள் குடும்பத்தில் யாருக்கேனும் மாரடைப்பு, பக்கவாதம் அல்லது சர்க்கரை நோய் வரலாறு உள்ளதா?",
            "hi": "क्या आपके परिवार में किसी को दिल का दौरा, स्ट्रोक, कैंसर या मधुमेह का इतिहास है?",
            "te": "మీ కుటుంబంలో గుండె జబ్బులు లేదా మధుమేహం చరిత్ర ఉందా?",
            "kn": "ನಿಮ್ಮ ಕುಟುಂಬದಲ್ಲಿ ಹೃದ್ರೋಗ ಅಥವಾ ಮಧುಮೇಹದ ಇತಿಹಾಸವಿದೆಯೇ?",
            "ml": "കുടുംബത്തിൽ ആർക്കെങ്കിലും ഹൃദ്രോഗമോ പക്ഷാഘാതമോ ഉണ്ടോ?",
        }.get(lang, "Is there any significant family medical history?")
        opts = {
            "en": [
                {"label": "Early Heart Attack in Parents / Siblings", "value": "Family history of early coronary disease"},
                {"label": "Diabetes in Parents / Siblings", "value": "Family history of diabetes"},
                {"label": "High Blood Pressure in Family", "value": "Family history of hypertension"},
                {"label": "Stroke History in Family", "value": "Family history of stroke"},
                {"label": "No significant family illness", "value": "No significant family history"},
            ],
            "ta": [
                {"label": "பெற்றோருக்கு இளம் வயதில் மாரடைப்பு", "value": "Family history of early heart disease"},
                {"label": "குடும்பத்தில் சர்க்கரை நோய் உள்ளது", "value": "Family history of diabetes"},
                {"label": "உயர் இரத்த அழுத்தம் உள்ளது", "value": "Family history of hypertension"},
                {"label": "முக்கியமான குடும்ப நோய் எதுவும் இல்லை", "value": "No significant family history"},
            ],
            "hi": [
                {"label": "माता-पिता में हृदय रोग का इतिहास", "value": "Family history of heart disease"},
                {"label": "परिवार में डायबिटीज का इतिहास", "value": "Family history of diabetes"},
                {"label": "परिवार में हाई बीपी का इतिहास", "value": "Family history of hypertension"},
                {"label": "कोई विशेष पारिवारिक इतिहास नहीं", "value": "No significant family history"},
            ],
        }
        return {
            "key": "family_history",
            "category": "family_history",
            "question": q_text,
            "input_type": "choice",
            "options": build_options(opts, language),
        }


# ============================================================
# SESSION MANAGEMENT (IN-MEMORY WITH STRUCTURED STATE)
# ============================================================

_interview_sessions: Dict[str, InterviewSession] = {}


def start_interview(
    patient_id: Optional[str],
    patient_name: Optional[str],
    language: LanguageCode = LanguageCode.ENGLISH,
    clinical_mode: ClinicalMode = ClinicalMode.ALLOPATHIC,
    chief_complaint_initial: Optional[str] = None,
) -> InterviewSession:
    """Initializes a new clinical interview session with adaptive scheduling."""
    session_id = str(uuid4())
    lang_key = language.value if hasattr(language, "value") else str(language)

    # Initial question is always Chief Complaint
    initial_q_text = INITIAL_COMPLAINT_QUESTIONS.get(lang_key, INITIAL_COMPLAINT_QUESTIONS["en"])
    initial_options = build_options(INITIAL_COMPLAINT_OPTIONS, language)

    # Default sequence keys
    sequence = [
        "chief_complaint",
        "onset",
        "site",
        "character",
        "radiation",
        "associations",
        "severity",
        "medical_history",
        "medications",
        "allergies",
        "family_history",
    ]

    session = InterviewSession(
        session_id=session_id,
        patient_id=patient_id,
        patient_name=patient_name,
        language=language,
        clinical_mode=clinical_mode,
        status=InterviewStatus.IN_PROGRESS,
        current_question=0,
        total_questions=len(sequence),
        answers={},
        detected_complaint_category=None,
        adaptive_queue=[{"key": k} for k in sequence],
        socrates_data={},
        red_flags=[],
        started_at=datetime.utcnow(),
    )

    if chief_complaint_initial:
        category = classify_chief_complaint(chief_complaint_initial)
        session.detected_complaint_category = category
        session.answers["chief_complaint"] = chief_complaint_initial

    _interview_sessions[session_id] = session
    return session


def get_session(session_id: str) -> Optional[InterviewSession]:
    return _interview_sessions.get(session_id)


def get_current_question(session_id: str) -> Optional[Dict[str, Any]]:
    session = get_session(session_id)
    if not session or session.status == InterviewStatus.COMPLETED:
        return None

    if session.current_question >= len(session.adaptive_queue):
        return None

    step_info = session.adaptive_queue[session.current_question]
    step_key = step_info["key"]

    if step_key == "chief_complaint":
        lang_key = session.language.value if hasattr(session.language, "value") else str(session.language)
        return {
            "key": "chief_complaint",
            "category": "chief_complaint",
            "question": INITIAL_COMPLAINT_QUESTIONS.get(lang_key, INITIAL_COMPLAINT_QUESTIONS["en"]),
            "input_type": "choice",
            "options": build_options(INITIAL_COMPLAINT_OPTIONS, session.language),
        }

    category = session.detected_complaint_category or "general"
    return get_adaptive_question_definition(step_key, category, session.language)


def save_answer(
    session_id: str,
    answer: str,
    question_id: Optional[str] = None,
) -> Optional[InterviewSession]:
    session = get_session(session_id)
    if not session or session.status != InterviewStatus.IN_PROGRESS:
        return session

    current_q = get_current_question(session_id)
    if not current_q:
        return session

    key = question_id or current_q["key"]
    clean_ans = answer.strip()
    session.answers[key] = clean_ans

    # If chief complaint was answered, dynamically adapt category and tail queue
    if key == "chief_complaint":
        category = classify_chief_complaint(clean_ans)
        session.detected_complaint_category = category

    # Check for red flags immediately with this newly added answer
    new_flags = detect_red_flags(
        symptoms=[clean_ans],
        interview_answers=session.answers,
        language=session.language,
    )
    if new_flags:
        session.red_flags = new_flags

    session.current_question += 1
    if session.current_question >= len(session.adaptive_queue):
        session.status = InterviewStatus.COMPLETED
        session.completed_at = datetime.utcnow()

    _interview_sessions[session_id] = session
    return session


def get_progress(session_id: str) -> Optional[Dict[str, Any]]:
    session = get_session(session_id)
    if not session:
        return None
    completed_q = len(session.answers)
    total_q = len(session.adaptive_queue)
    pct = (completed_q / total_q) * 100 if total_q > 0 else 0
    return {
        "session_id": session.session_id,
        "status": session.status,
        "completed_questions": completed_q,
        "total_questions": total_q,
        "current_question": min(session.current_question + 1, total_q),
        "progress_percentage": round(pct, 1),
        "red_flags_present": len(session.red_flags) > 0,
        "detected_category": session.detected_complaint_category,
    }


def get_collected_data(session_id: str) -> Optional[Dict[str, str]]:
    session = get_session(session_id)
    return session.answers.copy() if session else None