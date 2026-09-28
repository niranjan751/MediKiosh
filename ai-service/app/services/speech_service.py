"""
MediKiosk AI Service - Multilingual Speech-to-Text & Voice Processing
=====================================================================

Purpose:
    Provide voice intake and speech-to-text transcription for MediKiosk
    supporting English, Tamil, Hindi, Telugu, Kannada, Malayalam.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional
from app.models.schemas import LanguageCode


# Common multilingual voice command mappings
VOICE_PHRASE_MAPPINGS = {
    LanguageCode.TAMIL: {
        "நெஞ்சு வலி": "chest pain",
        "மார்பு வலி": "chest pain",
        "மூச்சுத்திணறல்": "difficulty breathing",
        "வயிற்று வலி": "abdominal pain",
        "காய்ச்சல்": "fever",
        "தலைவலி": "headache",
        "இருமல்": "cough",
        "ஆம்": "yes",
        "இல்லை": "no",
    },
    LanguageCode.HINDI: {
        "सीने में दर्द": "chest pain",
        "सांस फूलना": "difficulty breathing",
        "पेट दर्द": "abdominal pain",
        "बुखार": "fever",
        "सिरदर्द": "headache",
        "खांसी": "cough",
        "हाँ": "yes",
        "नहीं": "no",
    },
    LanguageCode.TELUGU: {
        "ఛాతీ నొప్పి": "chest pain",
        "శ్వాస ఆడకపోవడం": "difficulty breathing",
        "కడుపు నొప్పి": "abdominal pain",
        "జ్వరం": "fever",
        "తలనొప్పి": "headache",
    },
    LanguageCode.KANNADA: {
        "ಎದೆ ನೋவு": "chest pain",
        "ಉಸಿರಾಟ ಕಷ್ಟ": "difficulty breathing",
        "ಹೊಟ್ಟೆ ನೋವು": "abdominal pain",
        "ಜ್ವರ": "fever",
    },
    LanguageCode.MALAYALAM: {
        "നെഞ്ചുവേദന": "chest pain",
        "ശ്വാസംമുട്ടൽ": "difficulty breathing",
        "വയറുവേദന": "abdominal pain",
        "പനി": "fever",
    },
}


def process_voice_transcript(
    transcript: str,
    language: LanguageCode = LanguageCode.ENGLISH,
) -> Dict[str, Any]:
    """
    Cleans spoken text, identifies keywords, and normalizes spoken input.
    """
    cleaned = transcript.strip()
    norm = cleaned.lower()

    # Normalize spoken numbers
    number_words = {
        "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "ஒன்று": "1", "இரண்டு": "2", "மூன்று": "3", "நான்கு": "4", "ஐந்து": "5",
        "ஒரு": "1", "ரெண்டு": "2", "பத்து": "10",
        "एक": "1", "दो": "2", "तीन": "3", "चार": "4", "पांच": "5", "दस": "10",
    }
    for word, digit in number_words.items():
        if word in norm:
            norm = norm.replace(word, digit)

    normalized_concept = None
    lang_map = VOICE_PHRASE_MAPPINGS.get(language, {})
    for phrase, concept in lang_map.items():
        if phrase in cleaned or phrase in norm:
            normalized_concept = concept
            break

    return {
        "original_transcript": cleaned,
        "normalized_text": norm,
        "detected_clinical_concept": normalized_concept,
        "language": language,
        "confidence": 0.94,
    }
