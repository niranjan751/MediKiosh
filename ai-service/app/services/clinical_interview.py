from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from app.models.schemas import (
    InterviewSession,
    InterviewStatus,
    LanguageCode,
)


# ============================================================
# CLINICAL INTERVIEW QUESTIONS
# ============================================================

INTERVIEW_QUESTIONS = {
    LanguageCode.ENGLISH: [
        {
            "key": "chief_complaint",
            "question": "What is your main health concern today?",
            "category": "chief_complaint",
            "required": True,
        },
        {
            "key": "symptom_duration",
            "question": "How long have you had this problem?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_onset",
            "question": "When did the symptoms first start?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_location",
            "question": "Where exactly do you feel the symptom?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_severity",
            "question": "How severe is the symptom on a scale from 1 to 10?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "associated_symptoms",
            "question": "Do you have any other symptoms along with this problem?",
            "category": "associated_symptoms",
            "required": True,
        },
        {
            "key": "medical_history",
            "question": "Do you have any existing medical conditions?",
            "category": "medical_history",
            "required": True,
        },
        {
            "key": "medications",
            "question": "Are you currently taking any medicines?",
            "category": "medications",
            "required": True,
        },
        {
            "key": "allergies",
            "question": "Do you have any known allergies?",
            "category": "allergies",
            "required": True,
        },
        {
            "key": "family_history",
            "question": "Is there any important medical history in your family?",
            "category": "family_history",
            "required": True,
        },
    ],

    LanguageCode.TAMIL: [
        {
            "key": "chief_complaint",
            "question": "இன்று உங்களுக்கு முக்கியமான உடல்நலப் பிரச்சனை என்ன?",
            "category": "chief_complaint",
            "required": True,
        },
        {
            "key": "symptom_duration",
            "question": "இந்த பிரச்சனை உங்களுக்கு எவ்வளவு காலமாக உள்ளது?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_onset",
            "question": "இந்த அறிகுறிகள் முதலில் எப்போது தொடங்கின?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_location",
            "question": "இந்த அறிகுறி உங்கள் உடலில் எந்த இடத்தில் உள்ளது?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_severity",
            "question": "1 முதல் 10 வரை இந்த அறிகுறியின் தீவிரம் எவ்வளவு?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "associated_symptoms",
            "question": "இந்த பிரச்சனையுடன் வேறு ஏதேனும் அறிகுறிகள் உள்ளதா?",
            "category": "associated_symptoms",
            "required": True,
        },
        {
            "key": "medical_history",
            "question": "உங்களுக்கு ஏதேனும் முன்பிருந்த உடல்நலப் பிரச்சனைகள் உள்ளதா?",
            "category": "medical_history",
            "required": True,
        },
        {
            "key": "medications",
            "question": "தற்போது நீங்கள் ஏதேனும் மருந்துகள் எடுத்துக்கொள்கிறீர்களா?",
            "category": "medications",
            "required": True,
        },
        {
            "key": "allergies",
            "question": "உங்களுக்கு ஏதேனும் ஒவ்வாமை உள்ளதா?",
            "category": "allergies",
            "required": True,
        },
        {
            "key": "family_history",
            "question": "உங்கள் குடும்பத்தில் முக்கியமான உடல்நல வரலாறு ஏதேனும் உள்ளதா?",
            "category": "family_history",
            "required": True,
        },
    ],

    LanguageCode.HINDI: [
        {
            "key": "chief_complaint",
            "question": "आज आपकी मुख्य स्वास्थ्य समस्या क्या है?",
            "category": "chief_complaint",
            "required": True,
        },
        {
            "key": "symptom_duration",
            "question": "यह समस्या आपको कितने समय से है?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_onset",
            "question": "लक्षण पहली बार कब शुरू हुए?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_location",
            "question": "आपको यह लक्षण शरीर के किस स्थान पर महसूस होता है?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_severity",
            "question": "1 से 10 के पैमाने पर यह लक्षण कितना गंभीर है?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "associated_symptoms",
            "question": "क्या इस समस्या के साथ कोई अन्य लक्षण भी हैं?",
            "category": "associated_symptoms",
            "required": True,
        },
        {
            "key": "medical_history",
            "question": "क्या आपको पहले से कोई स्वास्थ्य समस्या है?",
            "category": "medical_history",
            "required": True,
        },
        {
            "key": "medications",
            "question": "क्या आप वर्तमान में कोई दवा ले रहे हैं?",
            "category": "medications",
            "required": True,
        },
        {
            "key": "allergies",
            "question": "क्या आपको किसी चीज़ से एलर्जी है?",
            "category": "allergies",
            "required": True,
        },
        {
            "key": "family_history",
            "question": "क्या आपके परिवार में कोई महत्वपूर्ण स्वास्थ्य इतिहास है?",
            "category": "family_history",
            "required": True,
        },
    ],

    LanguageCode.TELUGU: [
        {
            "key": "chief_complaint",
            "question": "ఈ రోజు మీ ప్రధాన ఆరోగ్య సమస్య ఏమిటి?",
            "category": "chief_complaint",
            "required": True,
        },
        {
            "key": "symptom_duration",
            "question": "ఈ సమస్య మీకు ఎంతకాలంగా ఉంది?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_onset",
            "question": "లక్షణాలు మొదట ఎప్పుడు ప్రారంభమయ్యాయి?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_location",
            "question": "ఈ లక్షణం మీ శరీరంలో ఏ భాగంలో ఉంది?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_severity",
            "question": "1 నుండి 10 వరకు ఈ లక్షణం తీవ్రత ఎంత?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "associated_symptoms",
            "question": "ఈ సమస్యతో పాటు మరే ఇతర లక్షణాలు ఉన్నాయా?",
            "category": "associated_symptoms",
            "required": True,
        },
        {
            "key": "medical_history",
            "question": "మీకు ఇప్పటికే ఏవైనా ఆరోగ్య సమస్యలు ఉన్నాయా?",
            "category": "medical_history",
            "required": True,
        },
        {
            "key": "medications",
            "question": "మీరు ప్రస్తుతం ఏదైనా మందులు తీసుకుంటున్నారా?",
            "category": "medications",
            "required": True,
        },
        {
            "key": "allergies",
            "question": "మీకు ఏవైనా అలెర్జీలు ఉన్నాయా?",
            "category": "allergies",
            "required": True,
        },
        {
            "key": "family_history",
            "question": "మీ కుటుంబంలో ముఖ్యమైన ఆరోగ్య చరిత్ర ఏదైనా ఉందా?",
            "category": "family_history",
            "required": True,
        },
    ],

    LanguageCode.KANNADA: [
        {
            "key": "chief_complaint",
            "question": "ಇಂದು ನಿಮ್ಮ ಮುಖ್ಯ ಆರೋಗ್ಯ ಸಮಸ್ಯೆ ಏನು?",
            "category": "chief_complaint",
            "required": True,
        },
        {
            "key": "symptom_duration",
            "question": "ಈ ಸಮಸ್ಯೆ ನಿಮಗೆ ಎಷ್ಟು ಸಮಯದಿಂದ ಇದೆ?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_onset",
            "question": "ಲಕ್ಷಣಗಳು ಮೊದಲ ಬಾರಿಗೆ ಯಾವಾಗ ಪ್ರಾರಂಭವಾದವು?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_location",
            "question": "ಈ ಲಕ್ಷಣವನ್ನು ನಿಮ್ಮ ದೇಹದ ಯಾವ ಭಾಗದಲ್ಲಿ ಅನುಭವಿಸುತ್ತೀರಿ?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_severity",
            "question": "1 ರಿಂದ 10 ರವರೆಗೆ ಈ ಲಕ್ಷಣದ ತೀವ್ರತೆ ಎಷ್ಟು?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "associated_symptoms",
            "question": "ಈ ಸಮಸ್ಯೆಯೊಂದಿಗೆ ಬೇರೆ ಯಾವುದೇ ಲಕ್ಷಣಗಳಿವೆಯೇ?",
            "category": "associated_symptoms",
            "required": True,
        },
        {
            "key": "medical_history",
            "question": "ನಿಮಗೆ ಈಗಾಗಲೇ ಯಾವುದೇ ಆರೋಗ್ಯ ಸಮಸ್ಯೆಗಳಿವೆಯೇ?",
            "category": "medical_history",
            "required": True,
        },
        {
            "key": "medications",
            "question": "ನೀವು ಪ್ರಸ್ತುತ ಯಾವುದೇ ಔಷಧಿಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದ್ದೀರಾ?",
            "category": "medications",
            "required": True,
        },
        {
            "key": "allergies",
            "question": "ನಿಮಗೆ ಯಾವುದೇ ಅಲರ್ಜಿ ಇದೆಯೇ?",
            "category": "allergies",
            "required": True,
        },
        {
            "key": "family_history",
            "question": "ನಿಮ್ಮ ಕುಟುಂಬದಲ್ಲಿ ಯಾವುದೇ ಪ್ರಮುಖ ಆರೋಗ್ಯ ಇತಿಹಾಸವಿದೆಯೇ?",
            "category": "family_history",
            "required": True,
        },
    ],

    LanguageCode.MALAYALAM: [
        {
            "key": "chief_complaint",
            "question": "ഇന്ന് നിങ്ങളുടെ പ്രധാന ആരോഗ്യ പ്രശ്നം എന്താണ്?",
            "category": "chief_complaint",
            "required": True,
        },
        {
            "key": "symptom_duration",
            "question": "ഈ പ്രശ്നം നിങ്ങൾക്ക് എത്ര കാലമായി ഉണ്ട്?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_onset",
            "question": "ലക്ഷണങ്ങൾ ആദ്യമായി ആരംഭിച്ചത് എപ്പോഴാണ്?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_location",
            "question": "ഈ ലക്ഷണം നിങ്ങളുടെ ശരീരത്തിലെ ഏത് ഭാഗത്താണ് അനുഭവപ്പെടുന്നത്?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "symptom_severity",
            "question": "1 മുതൽ 10 വരെ ഈ ലക്ഷണത്തിന്റെ തീവ്രത എത്രയാണ്?",
            "category": "symptom",
            "required": True,
        },
        {
            "key": "associated_symptoms",
            "question": "ഈ പ്രശ്നത്തോടൊപ്പം മറ്റ് ലക്ഷണങ്ങളുണ്ടോ?",
            "category": "associated_symptoms",
            "required": True,
        },
        {
            "key": "medical_history",
            "question": "നിങ്ങൾക്ക് നേരത്തെ എന്തെങ്കിലും ആരോഗ്യ പ്രശ്നങ്ങളുണ്ടോ?",
            "category": "medical_history",
            "required": True,
        },
        {
            "key": "medications",
            "question": "നിങ്ങൾ ഇപ്പോൾ എന്തെങ്കിലും മരുന്നുകൾ കഴിക്കുന്നുണ്ടോ?",
            "category": "medications",
            "required": True,
        },
        {
            "key": "allergies",
            "question": "നിങ്ങൾക്ക് എന്തെങ്കിലും അലർജിയുണ്ടോ?",
            "category": "allergies",
            "required": True,
        },
        {
            "key": "family_history",
            "question": "നിങ്ങളുടെ കുടുംബത്തിൽ പ്രധാനപ്പെട്ട ആരോഗ്യ ചരിത്രമുണ്ടോ?",
            "category": "family_history",
            "required": True,
        },
    ],
}


# ============================================================
# IN-MEMORY INTERVIEW STORAGE
# ============================================================
# This is suitable for the first prototype.
# Later, sessions can be stored in MySQL/MongoDB.

_interview_sessions: Dict[str, InterviewSession] = {}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_questions(language: LanguageCode):
    """
    Return interview questions for the selected language.
    """

    return INTERVIEW_QUESTIONS.get(
        language,
        INTERVIEW_QUESTIONS[LanguageCode.ENGLISH]
    )


def get_total_questions(language: LanguageCode) -> int:
    """
    Return the number of questions for a language.
    """

    return len(get_questions(language))


def get_question(
    language: LanguageCode,
    question_index: int
) -> Optional[dict]:
    """
    Get one question using zero-based index.
    """

    questions = get_questions(language)

    if question_index < 0:
        return None

    if question_index >= len(questions):
        return None

    return questions[question_index]


# ============================================================
# START INTERVIEW
# ============================================================

def start_interview(
    patient_id: Optional[str],
    patient_name: Optional[str],
    language: LanguageCode,
) -> InterviewSession:
    """
    Create a new clinical interview session.
    """

    session_id = str(uuid4())

    total_questions = get_total_questions(language)

    session = InterviewSession(
        session_id=session_id,
        patient_id=patient_id,
        patient_name=patient_name,
        language=language,
        status=InterviewStatus.IN_PROGRESS,
        current_question=0,
        total_questions=total_questions,
        answers={},
        started_at=datetime.utcnow(),
    )

    _interview_sessions[session_id] = session

    return session


# ============================================================
# GET SESSION
# ============================================================

def get_session(session_id: str) -> Optional[InterviewSession]:
    """
    Get an existing interview session.
    """

    return _interview_sessions.get(session_id)


# ============================================================
# GET CURRENT QUESTION
# ============================================================

def get_current_question(
    session_id: str
) -> Optional[dict]:
    """
    Return the current question for a session.
    """

    session = get_session(session_id)

    if session is None:
        return None

    return get_question(
        session.language,
        session.current_question
    )


# ============================================================
# SAVE ANSWER
# ============================================================

def save_answer(
    session_id: str,
    answer: str,
    question_id: Optional[str] = None,
) -> Optional[InterviewSession]:
    """
    Save the patient's answer and move to the next question.
    """

    session = get_session(session_id)

    if session is None:
        return None

    if session.status != InterviewStatus.IN_PROGRESS:
        return session

    current_question = get_current_question(session_id)

    if current_question is None:
        return session

    question_key = current_question["key"]

    if question_id:
        question_key = question_id

    session.answers[question_key] = answer.strip()

    session.current_question += 1

    if session.current_question >= session.total_questions:
        session.status = InterviewStatus.COMPLETED
        session.completed_at = datetime.utcnow()

    _interview_sessions[session_id] = session

    return session


# ============================================================
# GET NEXT QUESTION
# ============================================================

def get_next_question(
    session_id: str
) -> Optional[dict]:
    """
    Return the next question after the current question.
    """

    session = get_session(session_id)

    if session is None:
        return None

    if session.status == InterviewStatus.COMPLETED:
        return None

    return get_current_question(session_id)


# ============================================================
# COMPLETE INTERVIEW
# ============================================================

def complete_interview(
    session_id: str
) -> Optional[InterviewSession]:
    """
    Manually complete an interview.
    """

    session = get_session(session_id)

    if session is None:
        return None

    session.status = InterviewStatus.COMPLETED
    session.completed_at = datetime.utcnow()

    _interview_sessions[session_id] = session

    return session


# ============================================================
# CANCEL INTERVIEW
# ============================================================

def cancel_interview(
    session_id: str
) -> Optional[InterviewSession]:
    """
    Cancel an active interview.
    """

    session = get_session(session_id)

    if session is None:
        return None

    session.status = InterviewStatus.CANCELLED

    _interview_sessions[session_id] = session

    return session


# ============================================================
# GET INTERVIEW PROGRESS
# ============================================================

def get_progress(
    session_id: str
) -> Optional[dict]:
    """
    Return interview progress information.
    """

    session = get_session(session_id)

    if session is None:
        return None

    completed_questions = len(session.answers)

    if session.total_questions > 0:
        progress_percentage = (
            completed_questions / session.total_questions
        ) * 100
    else:
        progress_percentage = 0

    return {
        "session_id": session.session_id,
        "status": session.status,
        "completed_questions": completed_questions,
        "total_questions": session.total_questions,
        "current_question": session.current_question + 1,
        "progress_percentage": round(progress_percentage, 2),
    }


# ============================================================
# GET COLLECTED DATA
# ============================================================

def get_collected_data(
    session_id: str
) -> Optional[Dict[str, str]]:
    """
    Return all answers collected during the interview.
    """

    session = get_session(session_id)

    if session is None:
        return None

    return session.answers.copy()