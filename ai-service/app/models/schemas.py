from typing import Any, Dict, List, Optional, Union
from enum import Enum
from datetime import datetime
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field


# ============================================================
# LANGUAGE
# ============================================================

class LanguageCode(str, Enum):
    ENGLISH = "en"
    TAMIL = "ta"
    HINDI = "hi"
    TELUGU = "te"
    KANNADA = "kn"
    MALAYALAM = "ml"


# ============================================================
# GENDER & CLINICAL ENUMS
# ============================================================

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class InterviewStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SeverityLevel(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TriagePriority(str, Enum):
    LEVEL_1_RESUSCITATION = "Level 1 - Immediate Resuscitation"
    LEVEL_2_EMERGENT = "Level 2 - Emergent (Within 15 mins)"
    LEVEL_3_URGENT = "Level 3 - Urgent (Within 60 mins)"
    LEVEL_4_ROUTINE = "Level 4 - Routine / Non-Urgent"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    EDITED = "edited"
    APPROVED = "approved"


class DocumentType(str, Enum):
    LAB_REPORT = "lab_report"
    PRESCRIPTION = "prescription"
    DISCHARGE_SUMMARY = "discharge_summary"
    SCAN_REPORT = "scan_report"
    MEDICAL_CERTIFICATE = "medical_certificate"
    OP_RECORD = "op_record"
    OTHER = "other"
    UNKNOWN = "unknown"


class FileType(str, Enum):
    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    BMP = "bmp"
    TIFF = "tiff"


class ClinicalMode(str, Enum):
    ALLOPATHIC = "allopathic"
    AYUSH = "ayush"


# ============================================================
# PATIENT INFORMATION
# ============================================================

class PatientBasicInfo(BaseModel):
    patient_id: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)
    gender: Optional[Gender] = None
    abha_id: Optional[str] = None
    language: LanguageCode = LanguageCode.ENGLISH
    phone: Optional[str] = None


# ============================================================
# ADAPTIVE INTERVIEW SCHEMAS (SOCRATES)
# ============================================================

class QuestionOption(BaseModel):
    label: str
    value: str
    icon: Optional[str] = None
    hint: Optional[str] = None


class InterviewStartRequest(BaseModel):
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    language: LanguageCode = LanguageCode.ENGLISH
    age: Optional[int] = Field(default=None, ge=0, le=150)
    gender: Optional[Gender] = None
    clinical_mode: ClinicalMode = ClinicalMode.ALLOPATHIC
    chief_complaint_initial: Optional[str] = None
    consent_given: bool = False


class InterviewQuestion(BaseModel):
    question_id: str
    key: str
    question: str
    language: LanguageCode
    question_number: int
    total_questions: int
    required: bool = True
    category: Optional[str] = None
    help_text: Optional[str] = None
    input_type: str = "text"  # "choice", "multiselect", "scale", "text", "voice"
    options: List[QuestionOption] = Field(default_factory=list)
    socrates_dimension: Optional[str] = None  # site, onset, character, radiation, associations, time, exacerbating, severity
    allow_custom_text: bool = True


class InterviewStartResponse(BaseModel):
    success: bool = True
    session_id: str
    patient_id: Optional[str] = None
    language: LanguageCode
    status: InterviewStatus
    question_number: int
    total_questions: int
    question: Optional[str] = None
    question_key: Optional[str] = None
    category: Optional[str] = None
    input_type: str = "text"
    options: List[QuestionOption] = Field(default_factory=list)
    completed: bool = False


class InterviewAnswerRequest(BaseModel):
    session_id: str
    answer: str = Field(min_length=1, max_length=5000)
    question_id: Optional[str] = None
    language: Optional[LanguageCode] = None
    input_mode: Optional[str] = "text"  # "text", "voice", "option_click"


# ============================================================
# RED FLAG SCHEMAS
# ============================================================

class RedFlag(BaseModel):
    flag_id: str
    category: str
    symptom: str
    severity: AlertSeverity
    triage_priority: TriagePriority = TriagePriority.LEVEL_2_EMERGENT
    reason: str
    evidence: Optional[str] = None
    recommended_action: str
    requires_staff_attention: bool = True
    alert_triage_staff: bool = True
    created_at: Optional[datetime] = None


class RedFlagRequest(BaseModel):
    symptoms: List[str] = Field(default_factory=list)
    clinical_text: Optional[str] = None
    interview_answers: Dict[str, str] = Field(default_factory=dict)
    language: LanguageCode = LanguageCode.ENGLISH


class RedFlagResponse(BaseModel):
    success: bool = True
    red_flag_detected: bool
    overall_severity: AlertSeverity = AlertSeverity.LOW
    triage_priority: TriagePriority = TriagePriority.LEVEL_4_ROUTINE
    flags: List[RedFlag] = Field(default_factory=list)
    staff_alert_required: bool = False
    immediate_hospital_triage: bool = False
    emergency_instructions: Optional[str] = None
    disclaimer: str = (
        "Red-flag detection is an AI clinical alerting tool for hospital triage staff. "
        "It identifies potential life-threatening or emergent warning signs. "
        "It does not replace clinical judgment or provide an autonomous diagnosis."
    )


class InterviewAnswerResponse(BaseModel):
    success: bool = True
    session_id: str
    question_number: int
    total_questions: int
    answer_saved: bool
    completed: bool
    next_question: Optional[str] = None
    next_question_key: Optional[str] = None
    category: Optional[str] = None
    input_type: str = "text"
    options: List[QuestionOption] = Field(default_factory=list)
    collected_data: Dict[str, str] = Field(default_factory=dict)
    red_flags_detected: List[RedFlag] = Field(default_factory=list)
    priority_alert: bool = False


class InterviewSession(BaseModel):
    session_id: str
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    language: LanguageCode
    clinical_mode: ClinicalMode = ClinicalMode.ALLOPATHIC
    status: InterviewStatus
    current_question: int = 0
    total_questions: int = 10
    answers: Dict[str, str] = Field(default_factory=dict)
    detected_complaint_category: Optional[str] = None
    adaptive_queue: List[Dict[str, Any]] = Field(default_factory=list)
    socrates_data: Dict[str, Any] = Field(default_factory=dict)
    red_flags: List[RedFlag] = Field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class InterviewSummary(BaseModel):
    session_id: str
    patient_id: Optional[str] = None
    language: LanguageCode
    status: InterviewStatus
    answers: Dict[str, str] = Field(default_factory=dict)
    socrates_breakdown: Dict[str, Any] = Field(default_factory=dict)
    red_flags: List[RedFlag] = Field(default_factory=list)
    completed: bool
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# ============================================================
# MEDICAL ENTITIES, MEDICATIONS & LABS
# ============================================================

class Symptom(BaseModel):
    name: str
    description: Optional[str] = None
    duration: Optional[str] = None
    onset: Optional[str] = None
    location: Optional[str] = None
    character: Optional[str] = None
    radiation: Optional[str] = None
    severity: SeverityLevel = SeverityLevel.UNKNOWN
    frequency: Optional[str] = None
    triggers: List[str] = Field(default_factory=list)
    relieving_factors: List[str] = Field(default_factory=list)
    associated_symptoms: List[str] = Field(default_factory=list)


class MedicalCondition(BaseModel):
    name: str
    diagnosed_date: Optional[str] = None
    status: Optional[str] = None  # active, resolved, chronic
    notes: Optional[str] = None
    icd10_code: Optional[str] = None


class MedicalHistory(BaseModel):
    conditions: List[MedicalCondition] = Field(default_factory=list)
    previous_surgeries: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    family_history: List[str] = Field(default_factory=list)
    lifestyle_notes: List[str] = Field(default_factory=list)
    personal_habits: Dict[str, str] = Field(default_factory=dict)


class Medication(BaseModel):
    name: str
    generic_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = "oral"
    timing: Optional[str] = None  # after food, before food
    duration: Optional[str] = None
    purpose: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_active: bool = True
    source: Optional[str] = "interview"  # "interview", "ocr_prescription", "records"


class LabValue(BaseModel):
    test_name: str
    category: Optional[str] = None  # Hematology, Biochemistry, Lipid, Thyroid, Vitals
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = "NORMAL"  # "NORMAL", "HIGH", "LOW", "CRITICAL HIGH", "CRITICAL LOW"
    date: Optional[str] = None
    confidence: float = Field(default=0.9, ge=0, le=1)
    clinical_note: Optional[str] = None


class MedicalEntity(BaseModel):
    entity_type: str
    value: str
    normalized_value: Optional[str] = None
    confidence: float = Field(default=0.9, ge=0, le=1)
    source_text: Optional[str] = None
    page_number: Optional[int] = None
    category: Optional[str] = None


# ============================================================
# OCR & DOCUMENT SCHEMAS
# ============================================================

class OCRTextBlock(BaseModel):
    text: str
    page_number: Optional[int] = None
    confidence: Optional[float] = Field(default=None, ge=0, le=100)


class DocumentAnalysisResult(BaseModel):
    document_id: Optional[str] = None
    filename: str
    file_type: str
    document_type: DocumentType
    document_date: Optional[str] = None
    doctor_name: Optional[str] = None
    hospital_clinic: Optional[str] = None
    patient_name: Optional[str] = None
    extracted_text: str = ""
    confidence: float = 0.0
    pages: int = 1
    diagnoses: List[str] = Field(default_factory=list)
    medications: List[Medication] = Field(default_factory=list)
    lab_values: List[LabValue] = Field(default_factory=list)
    procedures: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    critical_findings: List[str] = Field(default_factory=list)
    text_preview: str = ""
    processed_at: Optional[datetime] = None


class OCRResponse(BaseModel):
    success: bool = True
    document_id: Optional[str] = None
    status: ProcessingStatus = ProcessingStatus.COMPLETED
    extracted_text: str = ""
    pages: int = 1
    confidence: Optional[float] = 0.0
    document_analysis: Optional[DocumentAnalysisResult] = None
    text_blocks: List[OCRTextBlock] = Field(default_factory=list)


# ============================================================
# MEDICAL TIMELINE SCHEMAS
# ============================================================

class TimelineEvent(BaseModel):
    event_id: str
    date: Optional[str] = None
    year: Optional[str] = None
    title: str
    event_type: str  # "consultation", "lab_report", "prescription", "hospital_admission", "procedure", "assessment"
    description: Optional[str] = None
    severity: Optional[str] = "routine"  # "routine", "alert", "critical"
    source: Optional[str] = None
    highlights: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    diagnoses: List[str] = Field(default_factory=list)
    abnormal_labs: List[str] = Field(default_factory=list)


class MedicalTimelineResponse(BaseModel):
    success: bool = True
    patient_id: Optional[str] = None
    total_events: int = 0
    events: List[TimelineEvent] = Field(default_factory=list)
    years_covered: List[str] = Field(default_factory=list)


# ============================================================
# AYUSH / AYURVEDA ASSESSMENT SCHEMAS
# ============================================================

class PrakritiScores(BaseModel):
    vata: float = 0.0
    pitta: float = 0.0
    kapha: float = 0.0
    dominant_dosha: str = "Vata-Pitta"
    secondary_dosha: Optional[str] = None
    constitution_type: str = "Dwandvaja (Dual Dosha)"


class VikritiScores(BaseModel):
    vata_aggravation: float = 0.0
    pitta_aggravation: float = 0.0
    kapha_aggravation: float = 0.0
    current_imbalance: str = "Vata-Pitta"
    severity: str = "Moderate"


class DashavidhaParikshaData(BaseModel):
    dushyam: Optional[str] = None      # Dhatus / Malas involved
    desham: Optional[str] = None       # Habitat / Bhoomi desha
    balam: Optional[str] = None        # Physical strength (Pravara, Madhyama, Avara)
    kalam: Optional[str] = None        # Ritu / Seasonal and chronological timing
    analam: Optional[str] = None       # Agni (Digestive fire strength)
    prakriti: Optional[str] = None     # Basic constitution
    vayas: Optional[str] = None        # Age stage (Balya, Madhyama, Vardhakya)
    satvam: Optional[str] = None       # Mental fortitude (Pravara, Madhyama, Avara)
    satmyam: Optional[str] = None      # Adaptability / Dietetic habituation
    aharam: Optional[str] = None       # Digestive and metabolic capacity


class AyushAssessment(BaseModel):
    prakriti: PrakritiScores = Field(default_factory=PrakritiScores)
    vikriti: VikritiScores = Field(default_factory=VikritiScores)
    agni: str = "Sama Agni (Balanced)"          # Sama, Vishama (Vata), Tikshna (Pitta), Manda (Kapha)
    koshtha: str = "Madhyama Koshtha (Medium)"  # Mridu (Soft/Pitta), Krura (Hard/Vata), Madhyama (Kapha)
    ahara_habits: Dict[str, Any] = Field(default_factory=dict)
    vihara_lifestyle: Dict[str, Any] = Field(default_factory=dict)
    dashavidha_pariksha: DashavidhaParikshaData = Field(default_factory=DashavidhaParikshaData)
    pathya_recommendations: List[str] = Field(default_factory=list)  # Wholesome food & habits
    apathya_warnings: List[str] = Field(default_factory=list)        # Avoid foods & habits
    herbal_support_guidance: List[str] = Field(default_factory=list)


class AyushAssessmentRequest(BaseModel):
    patient_id: Optional[str] = None
    responses: Dict[str, Any] = Field(default_factory=dict)
    language: LanguageCode = LanguageCode.ENGLISH


class AyushAssessmentResponse(BaseModel):
    success: bool = True
    patient_id: Optional[str] = None
    assessment: AyushAssessment
    summary: str
    clinical_note: str = (
        "AYUSH mode assessment utilizes classical Dashavidha Pariksha and Tridosha scoring. "
        "It supports Ayurvedic consultation and does not substitute for an in-person Vaidya/physician examination."
    )


# ============================================================
# CLINICAL SUMMARY SCHEMAS (PHYSICIAN-READY)
# ============================================================

class HPIStructured(BaseModel):
    narrative: str
    socrates: Dict[str, Any] = Field(default_factory=dict)
    duration_onset: Optional[str] = None
    progression: Optional[str] = None


class ReviewOfSystems(BaseModel):
    constitutional: List[str] = Field(default_factory=list)
    cardiovascular: List[str] = Field(default_factory=list)
    respiratory: List[str] = Field(default_factory=list)
    gastrointestinal: List[str] = Field(default_factory=list)
    neurological: List[str] = Field(default_factory=list)
    musculoskeletal: List[str] = Field(default_factory=list)
    integumentary: List[str] = Field(default_factory=list)


class ClinicalSummary(BaseModel):
    summary_id: Optional[str] = None
    patient: Optional[PatientBasicInfo] = None
    chief_complaint: str
    hpi: HPIStructured
    past_medical_history: List[str] = Field(default_factory=list)
    past_surgical_history: List[str] = Field(default_factory=list)
    current_medications: List[Medication] = Field(default_factory=list)
    drug_allergies: List[str] = Field(default_factory=list)
    family_history: List[str] = Field(default_factory=list)
    personal_social_history: List[str] = Field(default_factory=list)
    review_of_systems: ReviewOfSystems = Field(default_factory=ReviewOfSystems)
    investigations_summary: List[LabValue] = Field(default_factory=list)
    red_flag_alerts: List[RedFlag] = Field(default_factory=list)
    priority_level: TriagePriority = TriagePriority.LEVEL_4_ROUTINE
    timeline_events: List[TimelineEvent] = Field(default_factory=list)
    ayush_profile: Optional[AyushAssessment] = None
    doctor_review_notes: Optional[str] = None
    doctor_name: Optional[str] = None
    review_status: ReviewStatus = ReviewStatus.PENDING
    formatted_physician_note: str = ""
    generated_at: Optional[datetime] = None


class ClinicalSummaryRequest(BaseModel):
    patient_id: Optional[str] = None
    session_id: Optional[str] = None
    patient_info: Optional[PatientBasicInfo] = None
    interview_data: Optional[Dict[str, Any]] = None
    symptoms: List[Symptom] = Field(default_factory=list)
    medical_history: Optional[MedicalHistory] = None
    medications: List[Medication] = Field(default_factory=list)
    lab_values: List[LabValue] = Field(default_factory=list)
    medical_entities: List[MedicalEntity] = Field(default_factory=list)
    red_flags: List[RedFlag] = Field(default_factory=list)
    documents_data: Optional[List[Dict[str, Any]]] = None
    clinical_mode: ClinicalMode = ClinicalMode.ALLOPATHIC
    ayush_data: Optional[Dict[str, Any]] = None
    language: LanguageCode = LanguageCode.ENGLISH


class ClinicalSummaryResponse(BaseModel):
    success: bool = True
    patient_id: Optional[str] = None
    session_id: Optional[str] = None
    status: ProcessingStatus = ProcessingStatus.COMPLETED
    summary: ClinicalSummary
    review_status: ReviewStatus = ReviewStatus.PENDING
    disclaimer: str = (
        "This physician-ready clinical summary is generated by MediKiosk AI for clinical history structuring. "
        "It is designed to be reviewed, edited, confirmed, or rejected by the consulting physician. "
        "It does not constitute an autonomous diagnosis."
    )


# ============================================================
# DOCTOR REVIEW SCHEMAS
# ============================================================

class DoctorReviewRequest(BaseModel):
    summary_id: str
    doctor_id: str
    doctor_name: Optional[str] = "Attending Physician"
    status: ReviewStatus = ReviewStatus.APPROVED
    comments: Optional[str] = None
    edited_summary: Optional[str] = None
    confirmed_diagnoses: List[str] = Field(default_factory=list)
    prescribed_plan: Optional[str] = None


class DoctorReviewResponse(BaseModel):
    success: bool = True
    summary_id: str
    doctor_id: str
    doctor_name: Optional[str] = None
    review_status: ReviewStatus
    comments: Optional[str] = None
    reviewed_at: Optional[datetime] = None