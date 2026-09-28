"""
MediKiosk AI Service - Clinical Red-Flag Detection & Emergency Triage
====================================================================

Purpose:
    Provide an explainable, highly accurate clinical red-flag detection engine
    designed for hospital intake kiosks and patient triage.

Core Principles:
    1. Early identification of emergency / life-threatening conditions (ACS, Stroke, Sepsis, Anaphylaxis).
    2. Combination symptom analysis (e.g. Chest pain + Left arm radiation + Sweating).
    3. Multilingual recognition across English, Tamil, Hindi, Telugu, Kannada, Malayalam.
    4. Categorization by standard hospital triage levels (Level 1 Resuscitation to Level 4 Routine).
    5. Non-diagnostic: Formatted strictly as clinical alerts for hospital triage staff.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from app.models.schemas import (
    AlertSeverity,
    LanguageCode,
    RedFlag,
    TriagePriority,
)


# ============================================================
# MULTILINGUAL CLINICAL VOCABULARY & RED-FLAG PATTERNS
# ============================================================

RED_FLAG_DEFINITIONS: List[Dict[str, Any]] = [
    # --------------------------------------------------------
    # 1. ACUTE CORONARY SYNDROME (ACS) / MYOCARDIAL INFARCTION
    # --------------------------------------------------------
    {
        "flag_id": "acute_coronary_syndrome",
        "category": "Cardiovascular Emergency",
        "symptom": "Possible Acute Coronary Syndrome / Heart Attack",
        "severity": AlertSeverity.CRITICAL,
        "triage_priority": TriagePriority.LEVEL_1_RESUSCITATION,
        "primary_keywords": [
            "chest pain", "chest pressure", "chest tightness", "crushing chest pain",
            "heavy chest", "chest squeezing", "chest discomfort", "cardiac pain",
            "heart pain", "retrosternal pain", "substernal pain", "angina"
        ],
        "amplifying_keywords": [
            "left arm", "left shoulder", "jaw", "neck", "back", "radiation", "sweating",
            "cold sweat", "diaphoresis", "shortness of breath", "breathless", "dizziness",
            "nausea", "vomiting", "palpitations"
        ],
        "tamil": [
            "நெஞ்சு வலி", "மார்பு வலி", "மார்பில் அழுத்தம்", "மார்பு எரிச்சல்",
            "இடது கை வலி", "தாடை வலி", "வியர்த்தல்", "மூச்சுத்திணறல்"
        ],
        "hindi": [
            "सीने में दर्द", "छाती में दर्द", "सीने में दबाव", "सीने में जकड़न",
            "बाएं हाथ में दर्द", "जबड़े में दर्द", "पसीना आना", "सांस फूलना"
        ],
        "telugu": [
            "ఛాతీ నొప్పి", "గుండె నొప్పి", "ఛాతీలో ఒత్తిడి", "ఎడమ చేయి నొప్పి", "శ్వాస ఆడకపోవడం"
        ],
        "kannada": [
            "ಎದೆ ನೋವು", "ಎದೆಯಲ್ಲಿ ನೋವು", "ಎದೆಯ ಭಾರ", "ಎಡಗೈ ನೋವು", "ಉಸಿರಾಟ ಕಷ್ಟ"
        ],
        "malayalam": [
            "നെഞ്ചുവേദന", "നെഞ്ചിൽ ഭാരം", "ഇടതുകൈ വേദന", "ശ്വാസംമുട്ടൽ", "വിയർപ്പ്"
        ],
        "reason": "Chest discomfort accompanied by characteristic radiation (left arm/jaw) or autonomic symptoms suggests possible acute myocardial ischemia.",
        "recommended_action": "IMMEDIATE TRIAGE: Direct to Resuscitation/Cardiac ER. Obtain immediate 12-lead ECG, establish IV access, and notify ER physician.",
    },

    # --------------------------------------------------------
    # 2. ACUTE STROKE / NEUROLOGICAL DEFICIT (FAST)
    # --------------------------------------------------------
    {
        "flag_id": "acute_stroke_fast",
        "category": "Neurological Emergency",
        "symptom": "Acute Stroke Warning Signs (FAST)",
        "severity": AlertSeverity.CRITICAL,
        "triage_priority": TriagePriority.LEVEL_1_RESUSCITATION,
        "primary_keywords": [
            "stroke", "facial drooping", "face drooping", "face droop", "slurred speech",
            "speech difficulty", "cannot speak", "unable to speak", "arm weakness",
            "one sided weakness", "one-sided weakness", "hemiparesis", "sudden numbness",
            "sudden paralysis", "paralysis of leg", "loss of balance", "sudden vision loss",
            "diplopia", "double vision"
        ],
        "amplifying_keywords": ["sudden", "morning", "abrupt", "hours ago", "minutes ago"],
        "tamil": [
            "பக்கவாதம்", "முகம் ஒருபுறம் சாய்வது", "பேச முடியாமை", "குளறும் பேச்சு",
            "ஒரு கை பலவீனம்", "ஒரு பக்கம் உணர்வின்மை", "திடீர் மயக்கம்"
        ],
        "hindi": [
            "लकवा", "फालिज", "मुंह टेढ़ा होना", "बोलने में दिक्कत", "आवाज लड़खड़ाना",
            "एक तरफ कमजोरी", "हाथ पैर में सुन्नपन", "स्ट्रोक"
        ],
        "telugu": [
            "పక్షవాతం", "ముఖం వంకర పోవడం", "మాట తడబడటం", "ఒక వైపు బలహీనత"
        ],
        "kannada": [
            "ಪಾರ್ಶ್ವವಾಯು", "ಮುಖ ವಕ್ರವಾಗುವುದು", "ಮಾತು ತೊದಲುವುದು", "ಒಂದು ಬದಿಯ ದೌರ್ಬಲ್ಯ"
        ],
        "malayalam": [
            "പക്ഷാഘാതം", "മുഖം കോടിപ്പോവുക", "സംസാരത്തിന് തടസ്സം", "ഒരു ഭാഗം തളരുക"
        ],
        "reason": "Sudden onset focal neurological signs (facial asymmetry, motor weakness, speech impediment) suggest acute cerebrovascular event within thrombolysis window.",
        "recommended_action": "CODE STROKE ALERT: Record exact last known normal time. Expedite urgent non-contrast head CT scan and neuro-triage evaluation.",
    },

    # --------------------------------------------------------
    # 3. SEVERE RESPIRATORY DISTRESS / HYPOXEMIA
    # --------------------------------------------------------
    {
        "flag_id": "severe_respiratory_distress",
        "category": "Respiratory Emergency",
        "symptom": "Severe Respiratory Distress / Impending Respiratory Failure",
        "severity": AlertSeverity.CRITICAL,
        "triage_priority": TriagePriority.LEVEL_1_RESUSCITATION,
        "primary_keywords": [
            "cannot breathe", "can't breathe", "suffocating", "severe shortness of breath",
            "gasping for air", "gasping", "stridor", "bluish lips", "cyanosis",
            "unable to speak sentences", "inability to speak full sentence", "severe asthma attack",
            "acute breathlessness", "severe wheezing"
        ],
        "amplifying_keywords": ["choking", "blue", "chest tight", "spO2 below 90", "low oxygen"],
        "tamil": [
            "மூச்சு விடவே முடியவில்லை", "மூச்சுத்திணறல் மிகக் கடுமையானது",
            "நீல நிற உதடுகள்", "ஆஸ்துமா முற்றிவிட்டது"
        ],
        "hindi": [
            "सांस बिल्कुल नहीं आ रही", "सांस फूल रही है", "दम घुट रहा है",
            "गंभीर सांस की तकलीफ", "होंठ नीले पड़ना"
        ],
        "telugu": [
            "శ్వాస అస్సలు ఆడడం లేదు", "తీవ్రమైన ఊపిరితిత్తుల సమస్య", "పెదవులు నీలంగా మారడం"
        ],
        "kannada": [
            "ಉಸಿರಾಟ ಸಂಪೂರ್ಣ ಕಷ್ಟ", "ಉಸಿರುಗಟ್ಟುವಿಕೆ", "ತುಟಿಗಳು ನೀಲಿ ಬಣ್ಣಕ್ಕೆ ತಿರುಗುವುದು"
        ],
        "malayalam": [
            "ശ്വാസം കിട്ടുന്നില്ല", "ശ്വാസംമുട്ടി മരിക്കാൻ തോന്നുന്നു", "ചുണ്ടുകൾ നീലനിറമാകുന്നു"
        ],
        "reason": "Severe acute respiratory distress with signs of respiratory muscle fatigue or hypoxemia threatens immediate airway and ventilation.",
        "recommended_action": "AIRWAY PRIORITY: Administer supplemental high-flow oxygen, attach pulse oximeter, prepare airway equipment, and alert ER resus team.",
    },

    # --------------------------------------------------------
    # 4. ANAPHYLAXIS & ACUTE AIRWAY SWELLING
    # --------------------------------------------------------
    {
        "flag_id": "anaphylaxis",
        "category": "Immunological / Airway Emergency",
        "symptom": "Anaphylaxis / Severe Systemic Allergic Reaction",
        "severity": AlertSeverity.CRITICAL,
        "triage_priority": TriagePriority.LEVEL_1_RESUSCITATION,
        "primary_keywords": [
            "anaphylaxis", "severe allergic reaction", "throat swelling", "swelling of tongue",
            "tongue swelling", "throat closing", "difficulty swallowing and breathing",
            "lip swelling", "hives all over with breathing problem", "bee sting reaction",
            "medicine reaction with breathlessness"
        ],
        "amplifying_keywords": ["peanuts", "injection", "antibiotic", "hives", "rash", "hypotension"],
        "tamil": [
            "தொண்டை அடைப்பு", "நாக்கு வீக்கம்", "கடுமையான ஒவ்வாமை",
            "உதடு வீக்கம்", "மருந்து அலர்ஜி"
        ],
        "hindi": [
            "गले में सूजन", "जीभ में सूजन", "गंभीर एलर्जी", "सांस रुकना", "दवा से रिएक्शन"
        ],
        "telugu": [
            "గొంతు వాపు", "నాలుక వాపు", "తీవ్రమైన అలెర్జీ"
        ],
        "kannada": [
            "ಗಂಟಲು ಊತ", "ನಾಲಿಗೆ ಊತ", "ತೀವ್ರ ಅಲರ್ಜಿ"
        ],
        "malayalam": [
            "തൊണ്ട വീക്കം", "നാക്ക് വീക്കം", "ഗുരുതരമായ അലർജി"
        ],
        "reason": "Rapid onset multi-system allergic reaction with upper airway compromise or hemodynamic instability constitutes acute anaphylaxis.",
        "recommended_action": "ANAPHYLAXIS ALERT: Prepare intramuscular Epinephrine (1:1000) 0.5mg immediately, maintain airway, administer IV fluids.",
    },

    # --------------------------------------------------------
    # 5. SYNCOPE & LOSS OF CONSCIOUSNESS
    # --------------------------------------------------------
    {
        "flag_id": "loss_of_consciousness",
        "category": "Neurological / Hemodynamic Emergency",
        "symptom": "Syncope / Loss of Consciousness",
        "severity": AlertSeverity.CRITICAL,
        "triage_priority": TriagePriority.LEVEL_2_EMERGENT,
        "primary_keywords": [
            "loss of consciousness", "lost consciousness", "unconscious", "passed out",
            "fainted", "blackout", "black out", "collapsed", "sudden collapse",
            "unresponsive", "coma"
        ],
        "amplifying_keywords": ["seizure", "jerking", "head injury", "chest pain before fainting"],
        "tamil": ["மயக்கம்", "நினைவிழப்பு", "சுயநினைவின்றி விழுந்தார்", "மயங்கி விழுந்தார்"],
        "hindi": ["बेहोशी", "बेहोश हो गया", "चक्कर खाकर गिरना", "अचेत"],
        "telugu": ["స్పృహ కోల్పోవడం", "సృహ తప్పడం", "కళ్లు తిరిగి పడిపోవడం"],
        "kannada": ["ಪ್ರಜ್ಞೆ ತಪ್ಪುವುದು", "ಮೂರ್ಛೆ", "ಬಿದ್ದುಹೋಗುವುದು"],
        "malayalam": ["ബോധക്ഷയം", "ബോധം മറഞ്ഞു", "തളർന്നു വീണു"],
        "reason": "Transient or persistent loss of consciousness may reflect acute cardiac dysrhythmia, cerebrovascular compromise, or intracranial pathology.",
        "recommended_action": "EMERGENCY TRIAGE: Assess GCS, check blood glucose immediately, continuous ECG monitoring, immobilize cervical spine if trauma occurred.",
    },

    # --------------------------------------------------------
    # 6. SEVERE HEMORRHAGE / GASTROINTESTINAL BLEEDING
    # --------------------------------------------------------
    {
        "flag_id": "severe_hemorrhage",
        "category": "Vascular / GI Emergency",
        "symptom": "Acute Severe Bleeding / Hemorrhage",
        "severity": AlertSeverity.CRITICAL,
        "triage_priority": TriagePriority.LEVEL_2_EMERGENT,
        "primary_keywords": [
            "severe bleeding", "heavy bleeding", "bleeding heavily", "blood loss",
            "vomiting blood", "hematemesis", "blood in vomit", "coughing blood", "hemoptysis",
            "black tarry stool", "melena", "rectal bleeding heavy", "uncontrolled bleeding"
        ],
        "amplifying_keywords": ["pale", "dizzy", "fainting", "low BP", "hypotension"],
        "tamil": [
            "ரத்த வாந்தி", "ரத்தம் கொட்டுதல்", "அதிக ரத்தப்போக்கு", "இருமும்போது ரத்தம்",
            "கருப்பு மலம்"
        ],
        "hindi": [
            "खून की उल्टी", "भारी रक्तस्राव", "खांसी में खून आना", "बहुत खून बहना",
            "काला मल"
        ],
        "telugu": [
            "రక్తం వాంతులు", "తీవ్రమైన రక్తస్రావం", "దగ్గులో రక్తం"
        ],
        "kannada": [
            "ರಕ್ತ ವಾಂತಿ", "ಹೆಚ್ಚಿನ ರಕ್ತಸ್ರಾವ", "ಕೆಮ್ಮಿನಲ್ಲಿ ರಕ್ತ"
        ],
        "malayalam": [
            "രക്തം ഛർദ്ദിക്കുക", "അമിത രക്തസ്രാവം", "ചുമയ്ക്കുമ്പോൾ രക്തം"
        ],
        "reason": "Significant active blood loss or signs of upper/lower GI bleeding may lead to hypovolemic shock without rapid volume resuscitation.",
        "recommended_action": "HEMORRHAGE TRIAGE: Large-bore IV access x 2, send type and crossmatch blood, fluid resuscitation, initiate direct pressure / GI consult.",
    },

    # --------------------------------------------------------
    # 7. ACUTE ABDOMEN / PERITONEAL SIGNS
    # --------------------------------------------------------
    {
        "flag_id": "acute_abdomen",
        "category": "Surgical Emergency",
        "symptom": "Acute Abdomen / Possible Peritonitis or Perforation",
        "severity": AlertSeverity.HIGH,
        "triage_priority": TriagePriority.LEVEL_2_EMERGENT,
        "primary_keywords": [
            "severe abdominal pain", "severe stomach pain", "rigid abdomen", "board like abdomen",
            "extreme stomach pain", "rebound tenderness", "sudden excruciating abdominal pain",
            "abdominal guarding", "appendicitis signs", "perforation"
        ],
        "amplifying_keywords": ["vomiting", "fever", "fainting", "unable to touch abdomen"],
        "tamil": ["கடுமையான வயிற்று வலி", "தாங்க முடியாத வயிற்று வலி", "வயிறு கல் போல உள்ளது"],
        "hindi": ["पेट में असहनीय दर्द", "कड़ा पेट", "गंभीर पेट दर्द"],
        "telugu": ["తీవ్రమైన కడుపు నొప్పి", "కడుపు బిగుతుగా ఉండటం"],
        "kannada": ["ಅಸಹನೀಯ ಹೊಟ್ಟೆ ನೋವು", "ಹೊಟ್ಟೆ ಗಟ್ಟಿಯಾಗುವುದು"],
        "malayalam": ["സഹിക്കാൻ പറ്റാത്ത വയറുവേദന", "വയർ കല്ലുപോലെയാകുന്നു"],
        "reason": "Severe generalized or focal abdominal rigidity and rebound pain suggests visceral perforation, acute appendicitis, or peritonitis requiring surgical triage.",
        "recommended_action": "SURGICAL TRIAGE: Keep patient NPO (nil per os), obtain vitals, insert IV line, order abdominal imaging and urgent surgical consultation.",
    },

    # --------------------------------------------------------
    # 8. SEVERE SEPSIS & SYSTEMIC INFECTION
    # --------------------------------------------------------
    {
        "flag_id": "sepsis_warning",
        "category": "Infectious Emergency",
        "symptom": "Possible Sepsis / Severe Systemic Infection",
        "severity": AlertSeverity.HIGH,
        "triage_priority": TriagePriority.LEVEL_2_EMERGENT,
        "primary_keywords": [
            "high fever with confusion", "severe chills and shaking", "rigors with fever",
            "fever and drowsiness", "fever and altered consciousness", "hypothermia with infection",
            "sepsis", "septic shock"
        ],
        "amplifying_keywords": ["rapid breathing", "fast pulse", "very low BP", "mottled skin"],
        "tamil": ["கடுமையான நடுக்கத்துடன் காய்ச்சல்", "காய்ச்சலுடன் மயக்கம்", "அதிவிரைவு மூச்சு"],
        "hindi": ["कंपकंपी के साथ तेज बुखार", "बुखार में बेहोशी", "तेज बुखार और भ्रम"],
        "telugu": ["తీవ్రమైన వణుకుతో కూడిన జ్వరం", "జ్వరంతో మగత"],
        "kannada": ["ನಡುಕದೊಂದಿಗೆ ತೀವ್ರ ಜ್ವರ", "ಜ್ವರದೊಂದಿಗೆ ಅರೆಪ್ರಜ್ಞೆ"],
        "malayalam": ["വിറയലോടെയുള്ള കടുത്ത പനി", "പനിയോടൊപ്പം തളർച്ച"],
        "reason": "High fever accompanied by altered mental status, severe shivering, or hemodynamic disturbance indicates possible systemic sepsis.",
        "recommended_action": "SEPSIS PROTOCOL: Measure serum lactate, draw blood cultures before antibiotics, begin broad-spectrum antibiotics and IV crystalloid.",
    },

    # --------------------------------------------------------
    # 9. HYPERTENSIVE CRISIS / SEVERE HYPERTENSION
    # --------------------------------------------------------
    {
        "flag_id": "hypertensive_crisis",
        "category": "Cardiovascular Emergency",
        "symptom": "Suspected Hypertensive Crisis / Urgency",
        "severity": AlertSeverity.HIGH,
        "triage_priority": TriagePriority.LEVEL_2_EMERGENT,
        "primary_keywords": [
            "bp 200", "bp 190", "bp 180", "blood pressure 200", "blood pressure 190",
            "blood pressure 180", "hypertensive crisis", "severe high bp with headache",
            "extremely high blood pressure"
        ],
        "amplifying_keywords": ["severe headache", "blurred vision", "chest pain", "nosebleed", "confusion"],
        "tamil": ["மிக உயர் இரத்த அழுத்தம்", "தலைவலியுடன் கூடிய பிபி"],
        "hindi": ["अत्यधिक उच्च रक्तचाप", "हाई बीपी के साथ तेज सिरदर्द"],
        "telugu": ["అత్యధిక రక్తపోటు"],
        "kannada": ["ಅತಿಯಾದ ರಕ್ತದೊತ್ತಡ"],
        "malayalam": ["അമിത രക്തസമ്മർദ്ദം"],
        "reason": "Markedly elevated blood pressure associated with acute target organ symptoms (headache, vision loss, chest discomfort) indicates hypertensive emergency.",
        "recommended_action": "TRIAGE ASSESSMENT: Repeat BP in both arms, examine fundus, check renal function, and consult physician for gradual BP lowering.",
    },

    # --------------------------------------------------------
    # 10. MENTAL HEALTH & SUICIDAL CRISIS
    # --------------------------------------------------------
    {
        "flag_id": "suicidal_ideation",
        "category": "Psychiatric Emergency",
        "symptom": "Acute Self-Harm / Suicidal Risk",
        "severity": AlertSeverity.CRITICAL,
        "triage_priority": TriagePriority.LEVEL_1_RESUSCITATION,
        "primary_keywords": [
            "suicidal thoughts", "suicide", "want to die", "kill myself", "harm myself",
            "self harm", "self-harm", "end my life", "cannot live anymore"
        ],
        "amplifying_keywords": ["pills", "plan", "poison", "rope"],
        "tamil": ["தற்கொலை எண்ணம்", "சாக வேண்டும் என்று தோன்றுகிறது", "உயிரை மாய்த்துக் கொள்ளுதல்"],
        "hindi": ["आत्महत्या के विचार", "मरने का मन करना", "खुद को नुकसान पहुंचाना"],
        "telugu": ["ఆత్మహత్య ఆలోచనలు", "చనిపోవాలని అనిపించడం"],
        "kannada": ["ಆತ್ಮಹತ್ಯೆಯ ಆಲೋಚನೆಗಳು", "ಸಾಯಬೇಕೆನಿಸುವುದು"],
        "malayalam": ["ആത്മഹത്യാ ചിന്തകൾ", "ജീവനൊടുക്കാൻ തോന്നുന്നു"],
        "reason": "Expressed thoughts of intentional self-harm or active suicidal intent represents an acute safety emergency.",
        "recommended_action": "SAFETY INTERVENTION: Ensure continuous 1-to-1 supervision in a secure environment. Promptly mobilize psychiatric emergency team.",
    },
]


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def normalize_text_for_matching(text: str) -> str:
    """Normalize input text for reliable substring and keyword matching."""
    if not text:
        return ""
    cleaned = str(text).lower()
    cleaned = re.sub(r"[,;:\.!\?\-\(\)\/]", " ", cleaned)
    return " ".join(cleaned.split())


def extract_searchable_text(
    symptoms: List[str],
    clinical_text: str = "",
    interview_answers: Optional[Dict[str, Any]] = None,
) -> str:
    """Aggregate all patient text fields into a single unified search string."""
    tokens = []
    if clinical_text:
        tokens.append(str(clinical_text))
    if symptoms:
        for s in symptoms:
            if isinstance(s, dict):
                tokens.append(str(s.get("name", "")))
                tokens.append(str(s.get("location", "")))
                tokens.append(str(s.get("description", "")))
            else:
                tokens.append(str(s))
    if interview_answers:
        for key, value in interview_answers.items():
            if value:
                tokens.append(f"{key}: {value}")
    return normalize_text_for_matching(" ".join(tokens))


# ============================================================
# CORE RED-FLAG DETECTION ALGORITHM
# ============================================================

def detect_red_flags(
    symptoms: List[str],
    clinical_text: str = "",
    interview_answers: Optional[Dict[str, Any]] = None,
    language: LanguageCode = LanguageCode.ENGLISH,
) -> List[RedFlag]:
    """
    Analyzes patient inputs against multi-tier clinical red-flag rules.
    Identifies single triggers and synergistic multi-symptom clusters.
    """
    search_text = extract_searchable_text(symptoms, clinical_text, interview_answers)
    if not search_text:
        return []

    detected_flags: List[RedFlag] = []
    triggered_ids: Set[str] = set()

    for defn in RED_FLAG_DEFINITIONS:
        flag_id = defn["flag_id"]
        matched_primary: Optional[str] = None
        matched_amplifying: List[str] = []

        # 1. Check English primary keywords
        for kw in defn.get("primary_keywords", []):
            if kw in search_text:
                matched_primary = kw
                break

        # 2. Check multilingual keywords if primary was not found
        if not matched_primary:
            lang_key = language.value if hasattr(language, "value") else str(language)
            lang_keywords = defn.get(lang_key, [])
            for kw in lang_keywords:
                if kw in search_text:
                    matched_primary = kw
                    break

            # Also cross-check all language keywords as patients often use mixed native terms
            if not matched_primary:
                for lang_name in ["tamil", "hindi", "telugu", "kannada", "malayalam"]:
                    for kw in defn.get(lang_name, []):
                        if kw in search_text:
                            matched_primary = kw
                            break
                    if matched_primary:
                        break

        # If a primary keyword matched, check for amplifying/combination terms
        if matched_primary:
            for amp_kw in defn.get("amplifying_keywords", []):
                if amp_kw in search_text and amp_kw != matched_primary:
                    matched_amplifying.append(amp_kw)

            evidence_str = f"Detected: '{matched_primary}'"
            if matched_amplifying:
                evidence_str += f" + Associated: {', '.join(set(matched_amplifying[:3]))}"

            # Escalate severity if amplifying terms exist (e.g. chest pain + arm radiation)
            severity = defn["severity"]
            triage_priority = defn["triage_priority"]

            if flag_id == "acute_coronary_syndrome" and matched_amplifying:
                severity = AlertSeverity.CRITICAL
                triage_priority = TriagePriority.LEVEL_1_RESUSCITATION

            red_flag = RedFlag(
                flag_id=flag_id,
                category=defn["category"],
                symptom=defn["symptom"],
                severity=severity,
                triage_priority=triage_priority,
                reason=defn["reason"],
                evidence=evidence_str,
                recommended_action=defn["recommended_action"],
                requires_staff_attention=True,
                alert_triage_staff=True,
                created_at=datetime.utcnow(),
            )
            detected_flags.append(red_flag)
            triggered_ids.add(flag_id)

    # --------------------------------------------------------
    # SYNERGISTIC DUAL-SYMPTOM COMBO DETECTION
    # --------------------------------------------------------
    # Check for "Chest Pain" + "Breathing Difficulty" combo (classic high-mortality presentation)
    has_chest = any(k in search_text for k in ["chest pain", "chest tightness", "மார்பு வலி", "सीने में दर्द"])
    has_breath = any(k in search_text for k in ["breath", "breathing", "மூச்சுத்திணறல்", "सांस", "dyspnea", "shortness of breath"])

    if has_chest and has_breath and "acute_coronary_syndrome" not in triggered_ids:
        detected_flags.append(
            RedFlag(
                flag_id="cardiorespiratory_emergency",
                category="Cardiovascular / Respiratory Emergency",
                symptom="Concurrent Chest Pain & Dyspnea",
                severity=AlertSeverity.CRITICAL,
                triage_priority=TriagePriority.LEVEL_1_RESUSCITATION,
                reason="Co-occurrence of acute chest pain and shortness of breath represents a high-risk presentation for ACS, Pulmonary Embolism, or Tension Pneumothorax.",
                evidence="Concurrently reported chest pain and respiratory difficulty.",
                recommended_action="PRIORITY TRIAGE: Transfer immediately to emergency bay for simultaneous oxygenation, ECG, and physician evaluation.",
                requires_staff_attention=True,
                alert_triage_staff=True,
                created_at=datetime.utcnow(),
            )
        )

    return detected_flags


def get_overall_severity(flags: List[RedFlag]) -> AlertSeverity:
    """Calculates the composite highest severity from detected flags."""
    if not flags:
        return AlertSeverity.LOW
    order = {
        AlertSeverity.LOW: 1,
        AlertSeverity.MEDIUM: 2,
        AlertSeverity.HIGH: 3,
        AlertSeverity.CRITICAL: 4,
    }
    return max(flags, key=lambda f: order.get(f.severity, 1)).severity


def get_overall_triage_priority(flags: List[RedFlag]) -> TriagePriority:
    """Calculates the highest hospital triage priority level."""
    if not flags:
        return TriagePriority.LEVEL_4_ROUTINE
    for f in flags:
        if f.triage_priority == TriagePriority.LEVEL_1_RESUSCITATION:
            return TriagePriority.LEVEL_1_RESUSCITATION
    for f in flags:
        if f.triage_priority == TriagePriority.LEVEL_2_EMERGENT:
            return TriagePriority.LEVEL_2_EMERGENT
    for f in flags:
        if f.triage_priority == TriagePriority.LEVEL_3_URGENT:
            return TriagePriority.LEVEL_3_URGENT
    return TriagePriority.LEVEL_4_ROUTINE


def build_red_flag_result(
    symptoms: List[str],
    clinical_text: str = "",
    interview_answers: Optional[Dict[str, Any]] = None,
    language: LanguageCode = LanguageCode.ENGLISH,
) -> Dict[str, Any]:
    """Builds a complete, dashboard-ready response structure."""
    flags = detect_red_flags(symptoms, clinical_text, interview_answers, language)
    overall_severity = get_overall_severity(flags)
    triage_priority = get_overall_triage_priority(flags)
    staff_alert_required = any(f.requires_staff_attention for f in flags)
    immediate_hospital_triage = any(f.severity == AlertSeverity.CRITICAL for f in flags)

    instructions = None
    if immediate_hospital_triage:
        instructions = "URGENT HOSPITAL TRIAGE: High-risk symptoms detected. Please immediately notify triage nurse and physician."

    return {
        "red_flag_detected": len(flags) > 0,
        "overall_severity": overall_severity,
        "triage_priority": triage_priority,
        "flags": flags,
        "staff_alert_required": staff_alert_required,
        "immediate_hospital_triage": immediate_hospital_triage,
        "emergency_instructions": instructions,
        "disclaimer": (
            "MediKiosk Red-Flag Detection is an assistive alerting tool for hospital triage staff. "
            "It does NOT diagnose patients. All clinical care decisions remain the responsibility of healthcare providers."
        ),
    }