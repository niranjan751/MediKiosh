"""
MediKiosk AI Service
Multilingual Translation Service

Supported languages:
    English
    Tamil
    Hindi
    Telugu
    Kannada
    Malayalam

Purpose:
    Provide a structured translation layer for the MediKiosk
    multilingual clinical interview and healthcare interface.

Important:
    This prototype uses a local medical phrase dictionary and
    fallback behavior. It does not claim to provide professional
    medical translation.

    Medical content should be reviewed by a qualified healthcare
    professional when accuracy is clinically important.
"""

from typing import Any, Dict, List, Optional, Tuple

DEFAULT_LANGUAGE = "en"

LANGUAGE_INFORMATION: Dict[str, Dict[str, str]] = {
    "en": {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "speech_code": "en-US",
        "ocr_code": "eng",
    },
    "ta": {
        "code": "ta",
        "name": "Tamil",
        "native_name": "தமிழ்",
        "speech_code": "ta-IN",
        "ocr_code": "tam",
    },
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "native_name": "हिन्दी",
        "speech_code": "hi-IN",
        "ocr_code": "hin",
    },
    "te": {
        "code": "te",
        "name": "Telugu",
        "native_name": "తెలుగు",
        "speech_code": "te-IN",
        "ocr_code": "tel",
    },
    "kn": {
        "code": "kn",
        "name": "Kannada",
        "native_name": "ಕನ್ನಡ",
        "speech_code": "kn-IN",
        "ocr_code": "kan",
    },
    "ml": {
        "code": "ml",
        "name": "Malayalam",
        "native_name": "മലയാളം",
        "speech_code": "ml-IN",
        "ocr_code": "mal",
    },
}
SUPPORTED_LANGUAGES = list(LANGUAGE_INFORMATION)


def normalize_language_code(language_code: str) -> str:
    """Normalize supported language codes and locale tags."""

    normalized = str(language_code).strip().lower().replace("_", "-")
    code = normalized.split("-", maxsplit=1)[0]

    if code not in LANGUAGE_INFORMATION:
        raise ValueError(f"Unsupported language: {language_code}")

    return code


def is_supported_language(language_code: str) -> bool:
    """Return whether a language code is supported."""

    try:
        normalize_language_code(language_code)
    except ValueError:
        return False
    return True


def get_language(language_code: str) -> Dict[str, str]:
    """Return metadata for a supported language."""

    return LANGUAGE_INFORMATION[normalize_language_code(language_code)]


def get_language_name(language_code: str) -> str:
    """Return the English name of a supported language."""

    return get_language(language_code)["name"]


def get_native_language_name(language_code: str) -> str:
    """Return the native name of a supported language."""

    return get_language(language_code)["native_name"]


# ============================================================
# CONSTANTS
# ============================================================

SERVICE_NAME = "MediKiosk Multilingual Translation Service"

TRANSLATION_DISCLAIMER = (
    "Translation is AI-assisted and intended to support "
    "multilingual communication. Clinically important information "
    "should be reviewed by a qualified healthcare professional."
)


# ============================================================
# MEDICAL PHRASE DICTIONARY
# ============================================================

MEDICAL_TRANSLATIONS: Dict[str, Dict[str, str]] = {

    # --------------------------------------------------------
    # General
    # --------------------------------------------------------

    "hello": {
        "en": "Hello",
        "ta": "வணக்கம்",
        "hi": "नमस्ते",
        "te": "నమస్కారం",
        "kn": "ನಮಸ್ಕಾರ",
        "ml": "നമസ്കാരം",
    },

    "thank_you": {
        "en": "Thank you",
        "ta": "நன்றி",
        "hi": "धन्यवाद",
        "te": "ధన్యవాదాలు",
        "kn": "ಧನ್ಯವಾದಗಳು",
        "ml": "നന്ദി",
    },

    "please": {
        "en": "Please",
        "ta": "தயவுசெய்து",
        "hi": "कृपया",
        "te": "దయచేసి",
        "kn": "ದಯವಿಟ್ಟು",
        "ml": "ദയവായി",
    },

    "yes": {
        "en": "Yes",
        "ta": "ஆம்",
        "hi": "हाँ",
        "te": "అవును",
        "kn": "ಹೌದು",
        "ml": "അതെ",
    },

    "no": {
        "en": "No",
        "ta": "இல்லை",
        "hi": "नहीं",
        "te": "కాదు",
        "kn": "ಇಲ್ಲ",
        "ml": "ഇല്ല",
    },

    # --------------------------------------------------------
    # Clinical Interview
    # --------------------------------------------------------

    "how_are_you_feeling": {
        "en": "How are you feeling today?",
        "ta": "இன்று நீங்கள் எப்படி உணர்கிறீர்கள்?",
        "hi": "आज आप कैसा महसूस कर रहे हैं?",
        "te": "ఈరోజు మీరు ఎలా అనుభవిస్తున్నారు?",
        "kn": "ಇಂದು ನೀವು ಹೇಗೆ ಅನುಭವಿಸುತ್ತಿದ್ದೀರಿ?",
        "ml": "ഇന്ന് നിങ്ങൾക്ക് എങ്ങനെ അനുഭവപ്പെടുന്നു?",
    },

    "what_is_main_problem": {
        "en": "What is your main health problem?",
        "ta": "உங்கள் முக்கிய உடல்நலப் பிரச்சனை என்ன?",
        "hi": "आपकी मुख्य स्वास्थ्य समस्या क्या है?",
        "te": "మీ ప్రధాన ఆరోగ్య సమస్య ఏమిటి?",
        "kn": "ನಿಮ್ಮ ಮುಖ್ಯ ಆರೋಗ್ಯ ಸಮಸ್ಯೆ ಏನು?",
        "ml": "നിങ്ങളുടെ പ്രധാന ആരോഗ്യ പ്രശ്നം എന്താണ്?",
    },

    "when_did_it_start": {
        "en": "When did the problem start?",
        "ta": "இந்த பிரச்சனை எப்போது தொடங்கியது?",
        "hi": "यह समस्या कब शुरू हुई?",
        "te": "ఈ సమస్య ఎప్పుడు ప్రారంభమైంది?",
        "kn": "ಈ ಸಮಸ್ಯೆ ಯಾವಾಗ ಪ್ರಾರಂಭವಾಯಿತು?",
        "ml": "ഈ പ്രശ്നം എപ്പോൾ ആരംഭിച്ചു?",
    },

    "where_is_pain": {
        "en": "Where is the pain located?",
        "ta": "வலி எங்கு உள்ளது?",
        "hi": "दर्द कहाँ है?",
        "te": "నొప్పి ఎక్కడ ఉంది?",
        "kn": "ನೋವು ಎಲ್ಲಿದೆ?",
        "ml": "വേദന എവിടെയാണ്?",
    },

    "how_severe_is_pain": {
        "en": "How severe is the pain?",
        "ta": "வலி எவ்வளவு தீவிரமாக உள்ளது?",
        "hi": "दर्द कितना गंभीर है?",
        "te": "నొప్పి ఎంత తీవ్రంగా ఉంది?",
        "kn": "ನೋವು ಎಷ್ಟು ತೀವ್ರವಾಗಿದೆ?",
        "ml": "വേദന എത്രത്തോളം തീവ്രമാണ്?",
    },

    "does_pain_spread": {
        "en": "Does the pain spread to another part of the body?",
        "ta": "வலி உடலின் வேறு பகுதிக்கு பரவுகிறதா?",
        "hi": "क्या दर्द शरीर के किसी अन्य हिस्से में फैलता है?",
        "te": "నొప్పి శరీరంలోని ఇతర భాగాలకు వ్యాపిస్తుందా?",
        "kn": "ನೋವು ದೇಹದ ಬೇರೆ ಭಾಗಕ್ಕೆ ಹರಡುತ್ತದೆಯೇ?",
        "ml": "വേദന ശരീരത്തിന്റെ മറ്റൊരു ഭാഗത്തേക്ക് പടരുന്നുണ്ടോ?",
    },

    "other_symptoms": {
        "en": "Are you experiencing any other symptoms?",
        "ta": "வேறு ஏதேனும் அறிகுறிகள் உள்ளனவா?",
        "hi": "क्या आपको कोई अन्य लक्षण हैं?",
        "te": "మీకు ఇతర లక్షణాలు ఉన్నాయా?",
        "kn": "ನಿಮಗೆ ಬೇರೆ ಯಾವುದೇ ಲಕ್ಷಣಗಳಿವೆಯೇ?",
        "ml": "നിങ്ങൾക്ക് മറ്റ് ലക്ഷണങ്ങളുണ്ടോ?",
    },

    "medical_history_question": {
        "en": "Do you have any previous medical conditions?",
        "ta": "உங்களுக்கு முன்பு ஏதேனும் உடல்நலப் பிரச்சனைகள் இருந்ததா?",
        "hi": "क्या आपको पहले से कोई चिकित्सीय समस्या है?",
        "te": "మీకు ఇంతకుముందు ఏవైనా వైద్య సమస్యలు ఉన్నాయా?",
        "kn": "ನಿಮಗೆ ಹಿಂದೆ ಯಾವುದೇ ವೈದ್ಯಕೀಯ ಸಮಸ್ಯೆಗಳಿದ್ದವೆಯೇ?",
        "ml": "നിങ്ങൾക്ക് മുമ്പ് എന്തെങ്കിലും ആരോഗ്യ പ്രശ്നങ്ങളുണ്ടായിരുന്നോ?",
    },

    "medications_question": {
        "en": "Are you currently taking any medicines?",
        "ta": "நீங்கள் தற்போது ஏதேனும் மருந்துகள் எடுத்துக்கொள்கிறீர்களா?",
        "hi": "क्या आप वर्तमान में कोई दवा ले रहे हैं?",
        "te": "మీరు ప్రస్తుతం ఏవైనా మందులు తీసుకుంటున్నారా?",
        "kn": "ನೀವು ಪ್ರಸ್ತುತ ಯಾವುದೇ ಔಷಧಿಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದ್ದೀರಾ?",
        "ml": "നിങ്ങൾ ഇപ്പോൾ എന്തെങ്കിലും മരുന്നുകൾ കഴിക്കുന്നുണ്ടോ?",
    },

    "allergies_question": {
        "en": "Do you have any known allergies?",
        "ta": "உங்களுக்கு ஏதேனும் அறியப்பட்ட ஒவ்வாமைகள் உள்ளனவா?",
        "hi": "क्या आपको किसी प्रकार की एलर्जी है?",
        "te": "మీకు ఏవైనా తెలిసిన అలెర్జీలు ఉన్నాయా?",
        "kn": "ನಿಮಗೆ ಯಾವುದೇ ತಿಳಿದಿರುವ ಅಲರ್ಜಿಗಳಿವೆಯೇ?",
        "ml": "നിങ്ങൾക്ക് അറിയാവുന്ന എന്തെങ്കിലും അലർജികളുണ്ടോ?",
    },

    "family_history_question": {
        "en": "Is there any important medical history in your family?",
        "ta": "உங்கள் குடும்பத்தில் முக்கியமான மருத்துவ வரலாறு ஏதேனும் உள்ளதா?",
        "hi": "क्या आपके परिवार में कोई महत्वपूर्ण चिकित्सीय इतिहास है?",
        "te": "మీ కుటుంబంలో ముఖ్యమైన వైద్య చరిత్ర ఏదైనా ఉందా?",
        "kn": "ನಿಮ್ಮ ಕುಟುಂಬದಲ್ಲಿ ಯಾವುದೇ ಪ್ರಮುಖ ವೈದ್ಯಕೀಯ ಇತಿಹಾಸವಿದೆಯೇ?",
        "ml": "നിങ്ങളുടെ കുടുംബത്തിൽ പ്രധാനപ്പെട്ട ആരോഗ്യ ചരിത്രമുണ്ടോ?",
    },

    # --------------------------------------------------------
    # Symptoms
    # --------------------------------------------------------

    "fever": {
        "en": "Fever",
        "ta": "காய்ச்சல்",
        "hi": "बुखार",
        "te": "జ్వరం",
        "kn": "ಜ್ವರ",
        "ml": "പനി",
    },

    "cough": {
        "en": "Cough",
        "ta": "இருமல்",
        "hi": "खांसी",
        "te": "దగ్గు",
        "kn": "ಕೆಮ್ಮು",
        "ml": "ചുമ",
    },

    "cold": {
        "en": "Cold",
        "ta": "சளி",
        "hi": "जुकाम",
        "te": "జలుబు",
        "kn": "ಶೀತ",
        "ml": "ജലദോഷം",
    },

    "headache": {
        "en": "Headache",
        "ta": "தலைவலி",
        "hi": "सिरदर्द",
        "te": "తలనొప్పి",
        "kn": "ತಲೆನೋವು",
        "ml": "തലവേദന",
    },

    "chest_pain": {
        "en": "Chest pain",
        "ta": "மார்பு வலி",
        "hi": "सीने में दर्द",
        "te": "ఛాతీ నొప్పి",
        "kn": "ಎದೆ ನೋವು",
        "ml": "നെഞ്ചുവേദന",
    },

    "abdominal_pain": {
        "en": "Abdominal pain",
        "ta": "வயிற்று வலி",
        "hi": "पेट में दर्द",
        "te": "కడుపు నొప్పి",
        "kn": "ಹೊಟ್ಟೆ ನೋವು",
        "ml": "വയറുവേദന",
    },

    "back_pain": {
        "en": "Back pain",
        "ta": "முதுகு வலி",
        "hi": "कमर दर्द",
        "te": "వెన్నునొప్పి",
        "kn": "ಬೆನ್ನು ನೋವು",
        "ml": "നടുവേദന",
    },

    "joint_pain": {
        "en": "Joint pain",
        "ta": "மூட்டு வலி",
        "hi": "जोड़ों का दर्द",
        "te": "కీళ్ల నొప్పి",
        "kn": "ಕೀಲು ನೋವು",
        "ml": "സന്ധിവേദന",
    },

    "dizziness": {
        "en": "Dizziness",
        "ta": "தலைச்சுற்றல்",
        "hi": "चक्कर आना",
        "te": "తల తిరగడం",
        "kn": "ತಲೆತಿರುಗುವಿಕೆ",
        "ml": "തലകറക്കം",
    },

    "nausea": {
        "en": "Nausea",
        "ta": "குமட்டல்",
        "hi": "मतली",
        "te": "వికారం",
        "kn": "ವಾಕರಿಕೆ",
        "ml": "ഓക്കാനം",
    },

    "vomiting": {
        "en": "Vomiting",
        "ta": "வாந்தி",
        "hi": "उल्टी",
        "te": "వాంతులు",
        "kn": "ವಾಂತಿ",
        "ml": "ഛർദ്ദി",
    },

    "breathing_difficulty": {
        "en": "Difficulty breathing",
        "ta": "சுவாசிப்பதில் சிரமம்",
        "hi": "सांस लेने में कठिनाई",
        "te": "శ్వాస తీసుకోవడంలో ఇబ్బంది",
        "kn": "ಉಸಿರಾಟದ ತೊಂದರೆ",
        "ml": "ശ്വസിക്കാൻ ബുദ്ധിമുട്ട്",
    },

    "fatigue": {
        "en": "Fatigue",
        "ta": "சோர்வு",
        "hi": "थकान",
        "te": "అలసట",
        "kn": "ಆಯಾಸ",
        "ml": "ക്ഷീണം",
    },

    "weakness": {
        "en": "Weakness",
        "ta": "பலவீனம்",
        "hi": "कमजोरी",
        "te": "బలహీనత",
        "kn": "ದೌರ್ಬಲ್ಯ",
        "ml": "ബലഹീനത",
    },

    # --------------------------------------------------------
    # Medical History
    # --------------------------------------------------------

    "diabetes": {
        "en": "Diabetes",
        "ta": "நீரிழிவு நோய்",
        "hi": "मधुमेह",
        "te": "మధుమేహం",
        "kn": "ಮಧುಮೇಹ",
        "ml": "പ്രമേഹം",
    },

    "hypertension": {
        "en": "Hypertension",
        "ta": "உயர் இரத்த அழுத்தம்",
        "hi": "उच्च रक्तचाप",
        "te": "అధిక రక్తపోటు",
        "kn": "ಅಧಿಕ ರಕ್ತದೊತ್ತಡ",
        "ml": "ഉയർന്ന രക്തസമ്മർദ്ദം",
    },

    "asthma": {
        "en": "Asthma",
        "ta": "ஆஸ்துமா",
        "hi": "अस्थमा",
        "te": "ఆస్తమా",
        "kn": "ಆಸ್ತಮಾ",
        "ml": "ആസ്ത്മ",
    },

    "anemia": {
        "en": "Anemia",
        "ta": "இரத்த சோகை",
        "hi": "एनीमिया",
        "te": "రక్తహీనత",
        "kn": "ರಕ್ತಹೀನತೆ",
        "ml": "വിളർച്ച",
    },

    # --------------------------------------------------------
    # Common Medicines
    # --------------------------------------------------------

    "paracetamol": {
        "en": "Paracetamol",
        "ta": "பாராசிட்டமால்",
        "hi": "पैरासिटामोल",
        "te": "పారాసిటమాల్",
        "kn": "ಪ್ಯಾರಾಸಿಟಮಾಲ್",
        "ml": "പാരസെറ്റമോൾ",
    },

    "ibuprofen": {
        "en": "Ibuprofen",
        "ta": "இபுபுரோஃபன்",
        "hi": "इबुप्रोफेन",
        "te": "ఇబుప్రోఫెన్",
        "kn": "ಐಬುಪ್ರೊಫೆನ್",
        "ml": "ഐബുപ്രോഫെൻ",
    },

    "amoxicillin": {
        "en": "Amoxicillin",
        "ta": "அமோக்ஸிசிலின்",
        "hi": "एमोक्सिसिलिन",
        "te": "అమోక్సిసిలిన్",
        "kn": "ಅಮೋಕ್ಸಿಸಿಲಿನ್",
        "ml": "അമോക്സിസിലിൻ",
    },

    "metformin": {
        "en": "Metformin",
        "ta": "மெட்ஃபார்மின்",
        "hi": "मेटफॉर्मिन",
        "te": "మెట్‌ఫార్మిన్",
        "kn": "ಮೆಟ್ಫಾರ್ಮಿನ್",
        "ml": "മെറ്റ്ഫോർമിൻ",
    },

    # --------------------------------------------------------
    # Alerts
    # --------------------------------------------------------

    "red_flag_detected": {
        "en": "A red-flag symptom was detected. Please seek clinical attention.",
        "ta": "அவசர எச்சரிக்கை அறிகுறி கண்டறியப்பட்டுள்ளது. தயவுசெய்து மருத்துவ கவனிப்பைப் பெறுங்கள்.",
        "hi": "एक गंभीर चेतावनी लक्षण पाया गया है। कृपया चिकित्सकीय सहायता लें।",
        "te": "తీవ్రమైన హెచ్చరిక లక్షణం గుర్తించబడింది. దయచేసి వైద్య సహాయం పొందండి.",
        "kn": "ಗಂಭೀರ ಎಚ್ಚರಿಕೆಯ ಲಕ್ಷಣ ಪತ್ತೆಯಾಗಿದೆ. ದಯವಿಟ್ಟು ವೈದ್ಯಕೀಯ ಸಹಾಯ ಪಡೆಯಿರಿ.",
        "ml": "ഗുരുതരമായ മുന്നറിയിപ്പ് ലക്ഷണം കണ്ടെത്തി. ദയവായി വൈദ്യസഹായം തേടുക.",
    },

    "doctor_review_required": {
        "en": "Doctor review is required.",
        "ta": "மருத்துவர் பரிசோதனை அவசியம்.",
        "hi": "डॉक्टर की समीक्षा आवश्यक है।",
        "te": "వైద్యుల సమీక్ష అవసరం.",
        "kn": "ವೈದ್ಯರ ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ.",
        "ml": "ഡോക്ടറുടെ പരിശോധന ആവശ്യമാണ്.",
    },

    "assessment_complete": {
        "en": "Your health assessment is complete.",
        "ta": "உங்கள் உடல்நல மதிப்பீடு முடிந்தது.",
        "hi": "आपका स्वास्थ्य मूल्यांकन पूरा हो गया है।",
        "te": "మీ ఆరోగ్య అంచనా పూర్తయింది.",
        "kn": "ನಿಮ್ಮ ಆರೋಗ್ಯ ಮೌಲ್ಯಮಾಪನ ಪೂರ್ಣಗೊಂಡಿದೆ.",
        "ml": "നിങ്ങളുടെ ആരോഗ്യ വിലയിരുത്തൽ പൂർത്തിയായി.",
    },
}


# ============================================================
# BASIC VALIDATION
# ============================================================

def validate_language(
    language_code: str,
) -> str:
    """
    Validate and normalize a language code.
    """

    if not language_code:
        return DEFAULT_LANGUAGE

    normalized = normalize_language_code(
        language_code
    )

    return normalized


def validate_language_pair(
    source_language: str,
    target_language: str,
) -> Tuple[str, str]:
    """
    Validate a source and target language pair.
    """

    source = validate_language(
        source_language
    )

    target = validate_language(
        target_language
    )

    return source, target


# ============================================================
# TRANSLATION KEY FUNCTIONS
# ============================================================

def get_translation_keys() -> List[str]:
    """
    Return all available translation keys.
    """

    return list(
        MEDICAL_TRANSLATIONS.keys()
    )


def has_translation_key(
    key: str,
) -> bool:
    """
    Check whether a translation key exists.
    """

    return (
        key in MEDICAL_TRANSLATIONS
    )


# ============================================================
# TRANSLATE BY KEY
# ============================================================

def translate_key(
    key: str,
    target_language: str = DEFAULT_LANGUAGE,
) -> str:
    """
    Translate a predefined medical phrase key.
    """

    target = validate_language(
        target_language
    )

    translation = MEDICAL_TRANSLATIONS.get(
        key
    )

    if not translation:
        return key

    return translation.get(
        target,
        translation.get(
            DEFAULT_LANGUAGE,
            key,
        ),
    )


# ============================================================
# TRANSLATE TEXT
# ============================================================

def translate_text(
    text: str,
    source_language: str = DEFAULT_LANGUAGE,
    target_language: str = DEFAULT_LANGUAGE,
) -> Dict[str, Any]:
    """
    Translate supported predefined phrases.

    For unsupported free-form text, the original text is
    returned with a fallback status.

    This keeps the prototype deterministic without falsely
    claiming that a full external translation model is active.
    """

    source, target = validate_language_pair(
        source_language,
        target_language,
    )

    original_text = (
        str(text).strip()
        if text is not None
        else ""
    )

    if not original_text:
        return {
            "success": False,
            "source_language": source,
            "target_language": target,
            "source_text": "",
            "translated_text": "",
            "translation_method": "none",
            "message": "Text is required.",
        }

    if source == target:
        return {
            "success": True,
            "source_language": source,
            "target_language": target,
            "source_text": original_text,
            "translated_text": original_text,
            "translation_method": "same_language",
            "message": "Source and target languages are the same.",
        }

    normalized_input = (
        original_text.lower().strip()
    )

    # --------------------------------------------------------
    # Direct key matching
    # --------------------------------------------------------

    for key, translations in MEDICAL_TRANSLATIONS.items():

        source_text = translations.get(
            source,
            "",
        ).lower().strip()

        if (
            source_text
            and normalized_input == source_text
        ):

            translated = translations.get(
                target,
                original_text,
            )

            return {
                "success": True,
                "source_language": source,
                "target_language": target,
                "source_text": original_text,
                "translated_text": translated,
                "translation_method": "medical_dictionary",
                "translation_key": key,
                "message": "Translation completed.",
            }

    # --------------------------------------------------------
    # Key-name matching
    # --------------------------------------------------------

    normalized_key = (
        normalized_input
        .replace(" ", "_")
        .replace("-", "_")
    )

    if normalized_key in MEDICAL_TRANSLATIONS:

        translated = translate_key(
            normalized_key,
            target,
        )

        return {
            "success": True,
            "source_language": source,
            "target_language": target,
            "source_text": original_text,
            "translated_text": translated,
            "translation_method": "medical_dictionary",
            "translation_key": normalized_key,
            "message": "Translation completed.",
        }

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    return {
        "success": True,
        "source_language": source,
        "target_language": target,
        "source_text": original_text,
        "translated_text": original_text,
        "translation_method": "fallback",
        "translation_key": None,
        "message": (
            "No local translation entry was found. "
            "Original text returned."
        ),
    }


# ============================================================
# TRANSLATE INTERVIEW QUESTION
# ============================================================

def translate_interview_question(
    question_key: str,
    target_language: str,
) -> Dict[str, Any]:
    """
    Translate a clinical interview question.
    """

    target = validate_language(
        target_language
    )

    if not has_translation_key(
        question_key
    ):

        return {
            "success": False,
            "question_key": question_key,
            "target_language": target,
            "question": question_key,
            "message": "Question translation key not found.",
        }

    translated = translate_key(
        question_key,
        target,
    )

    return {
        "success": True,
        "question_key": question_key,
        "target_language": target,
        "question": translated,
    }


# ============================================================
# TRANSLATE SYMPTOM
# ============================================================

def translate_symptom(
    symptom_key: str,
    target_language: str,
) -> Dict[str, Any]:
    """
    Translate a symptom.
    """

    target = validate_language(
        target_language
    )

    if not has_translation_key(
        symptom_key
    ):

        return {
            "success": False,
            "symptom_key": symptom_key,
            "target_language": target,
            "symptom": symptom_key,
            "message": "Symptom translation key not found.",
        }

    return {
        "success": True,
        "symptom_key": symptom_key,
        "target_language": target,
        "symptom": translate_key(
            symptom_key,
            target,
        ),
    }


# ============================================================
# TRANSLATE MEDICAL ENTITY
# ============================================================

def translate_medical_entity(
    entity: Dict[str, Any],
    target_language: str,
) -> Dict[str, Any]:
    """
    Translate a medical entity when it exists in
    the local dictionary.
    """

    target = validate_language(
        target_language
    )

    entity_text = str(
        entity.get("text", "")
    ).strip()

    entity_type = str(
        entity.get("type", "")
    ).strip()

    result = dict(entity)

    if not entity_text:
        result["translated_text"] = ""
        result["translation_method"] = "none"
        return result

    translated = translate_text(
        text=entity_text,
        source_language=DEFAULT_LANGUAGE,
        target_language=target,
    )

    result["translated_text"] = translated[
        "translated_text"
    ]

    result["translation_method"] = translated[
        "translation_method"
    ]

    result["entity_type"] = entity_type

    return result


# ============================================================
# TRANSLATE ENTITY LIST
# ============================================================

def translate_medical_entities(
    entities: List[Dict[str, Any]],
    target_language: str,
) -> List[Dict[str, Any]]:
    """
    Translate a list of medical entities.
    """

    translated_entities = []

    for entity in entities:

        if not isinstance(entity, dict):
            continue

        translated_entities.append(
            translate_medical_entity(
                entity,
                target_language,
            )
        )

    return translated_entities


# ============================================================
# TRANSLATE SUMMARY
# ============================================================

def translate_summary(
    summary: Dict[str, Any],
    target_language: str,
) -> Dict[str, Any]:
    """
    Translate important predefined fields in a clinical
    summary while preserving the original structure.
    """

    target = validate_language(
        target_language
    )

    result = dict(summary)

    result["target_language"] = target
    result["target_language_name"] = get_language_name(
        target
    )

    result["translation_disclaimer"] = (
        TRANSLATION_DISCLAIMER
    )

    clinical_summary = summary.get(
        "clinical_summary",
        {},
    )

    if not isinstance(
        clinical_summary,
        dict,
    ):
        clinical_summary = {}

    translated_clinical = dict(
        clinical_summary
    )

    # --------------------------------------------------------
    # Chief complaint
    # --------------------------------------------------------

    complaint = clinical_summary.get(
        "chief_complaint"
    )

    if complaint:

        translated_clinical[
            "chief_complaint_original"
        ] = complaint

        translated_clinical[
            "chief_complaint_translated"
        ] = translate_text(
            str(complaint),
            DEFAULT_LANGUAGE,
            target,
        )["translated_text"]

    # --------------------------------------------------------
    # Symptoms
    # --------------------------------------------------------

    symptoms = clinical_summary.get(
        "symptoms",
        [],
    )

    if isinstance(symptoms, list):

        translated_symptoms = []

        for symptom in symptoms:

            if not isinstance(
                symptom,
                dict,
            ):
                continue

            translated_symptom = dict(
                symptom
            )

            name = symptom.get(
                "name",
                "",
            )

            if name:

                translation_result = translate_text(
                    str(name),
                    DEFAULT_LANGUAGE,
                    target,
                )

                translated_symptom[
                    "translated_name"
                ] = translation_result[
                    "translated_text"
                ]

            translated_symptoms.append(
                translated_symptom
            )

        translated_clinical[
            "symptoms"
        ] = translated_symptoms

    # --------------------------------------------------------
    # Medical history
    # --------------------------------------------------------

    history = clinical_summary.get(
        "medical_history",
        [],
    )

    if isinstance(history, list):

        translated_history = []

        for item in history:

            translation_result = translate_text(
                str(item),
                DEFAULT_LANGUAGE,
                target,
            )

            translated_history.append(
                translation_result[
                    "translated_text"
                ]
            )

        translated_clinical[
            "medical_history_translated"
        ] = translated_history

    # --------------------------------------------------------
    # Allergies
    # --------------------------------------------------------

    allergies = clinical_summary.get(
        "allergies",
        [],
    )

    if isinstance(allergies, list):

        translated_allergies = []

        for allergy in allergies:

            translation_result = translate_text(
                str(allergy),
                DEFAULT_LANGUAGE,
                target,
            )

            translated_allergies.append(
                translation_result[
                    "translated_text"
                ]
            )

        translated_clinical[
            "allergies_translated"
        ] = translated_allergies

    result[
        "clinical_summary"
    ] = translated_clinical

    return result


# ============================================================
# LANGUAGE INFORMATION
# ============================================================

def get_language_information(
    language_code: str,
) -> Dict[str, Any]:
    """
    Return complete information about a language.
    """

    code = validate_language(
        language_code
    )

    language = get_language(
        code
    )

    return {
        "code": language["code"],
        "name": language["name"],
        "native_name": language["native_name"],
        "speech_code": language["speech_code"],
        "ocr_code": language["ocr_code"],
        "supported": is_supported_language(
            code
        ),
    }


# ============================================================
# ALL LANGUAGE INFORMATION
# ============================================================

def get_all_language_information() -> List[Dict[str, Any]]:
    """
    Return information about all supported languages.
    """

    languages = []

    for code in SUPPORTED_LANGUAGES:

        languages.append(
            get_language_information(
                code
            )
        )

    return languages


# ============================================================
# TRANSLATION STATUS
# ============================================================

def get_translation_service_status() -> Dict[str, Any]:
    """
    Return translation service status.
    """

    return {
        "service": SERVICE_NAME,
        "status": "online",
        "default_language": DEFAULT_LANGUAGE,
        "supported_languages": (
            get_all_language_information()
        ),
        "translation_dictionary_entries": len(
            MEDICAL_TRANSLATIONS
        ),
        "medical_translation": True,
        "external_translation_model": False,
        "fallback_enabled": True,
        "diagnosis": False,
        "autonomous_medical_decision": False,
        "disclaimer": TRANSLATION_DISCLAIMER,
    }


# ============================================================
# DISCLAIMER
# ============================================================

def get_translation_disclaimer() -> str:
    """
    Return translation disclaimer.
    """

    return TRANSLATION_DISCLAIMER