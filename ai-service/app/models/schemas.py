from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

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
# GENDER
# ============================================================

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


# ============================================================
# INTERVIEW STATUS
# ============================================================

class InterviewStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ============================================================
# SEVERITY
# ============================================================

class SeverityLevel(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    UNKNOWN = "unknown"


# ============================================================
# ALERT SEVERITY
# ============================================================

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================
# PROCESSING STATUS
# ============================================================

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================
# REVIEW STATUS
# ============================================================

class ReviewStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    EDITED = "edited"
    APPROVED = "approved"


# ============================================================
# DOCUMENT TYPE
# ============================================================

class DocumentType(str, Enum):
    LAB_REPORT = "lab_report"
    PRESCRIPTION = "prescription"
    DISCHARGE_SUMMARY = "discharge_summary"
    SCAN_REPORT = "scan_report"
    MEDICAL_CERTIFICATE = "medical_certificate"
    OP_RECORD = "op_record"
    OTHER = "other"
    UNKNOWN = "unknown"


# ============================================================
# FILE TYPE
# ============================================================

class FileType(str, Enum):
    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"


# ============================================================
# PATIENT INFORMATION
# ============================================================

class PatientBasicInfo(BaseModel):
    patient_id: Optional[str] = None

    name: Optional[str] = None

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150
    )

    gender: Optional[Gender] = None

    language: LanguageCode = LanguageCode.ENGLISH


# ============================================================
# INTERVIEW START
# ============================================================

class InterviewStartRequest(BaseModel):
    patient_id: Optional[str] = None

    patient_name: Optional[str] = None

    language: LanguageCode = LanguageCode.ENGLISH

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150
    )

    gender: Optional[Gender] = None

    consent_given: bool = False


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

    completed: bool = False


# ============================================================
# INTERVIEW QUESTION
# ============================================================

class InterviewQuestion(BaseModel):
    question_id: str

    key: str

    question: str

    language: LanguageCode

    question_number: int

    required: bool = True

    category: Optional[str] = None

    help_text: Optional[str] = None


# ============================================================
# INTERVIEW ANSWER
# ============================================================

class InterviewAnswerRequest(BaseModel):
    session_id: str

    answer: str = Field(
        min_length=1,
        max_length=5000
    )

    question_id: Optional[str] = None

    language: Optional[LanguageCode] = None


class InterviewAnswerResponse(BaseModel):
    success: bool = True

    session_id: str

    question_number: int

    total_questions: int

    answer_saved: bool

    completed: bool

    next_question: Optional[str] = None

    next_question_key: Optional[str] = None

    collected_data: Dict[str, str] = Field(
        default_factory=dict
    )


# ============================================================
# INTERVIEW SESSION
# ============================================================

class InterviewSession(BaseModel):
    session_id: str

    patient_id: Optional[str] = None

    patient_name: Optional[str] = None

    language: LanguageCode

    status: InterviewStatus

    current_question: int = 0

    total_questions: int

    answers: Dict[str, str] = Field(
        default_factory=dict
    )

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None


# ============================================================
# INTERVIEW SUMMARY
# ============================================================

class InterviewSummary(BaseModel):
    session_id: str

    patient_id: Optional[str] = None

    language: LanguageCode

    status: InterviewStatus

    answers: Dict[str, str] = Field(
        default_factory=dict
    )

    completed: bool

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None


# ============================================================
# SYMPTOM
# ============================================================

class Symptom(BaseModel):
    name: str

    description: Optional[str] = None

    duration: Optional[str] = None

    onset: Optional[str] = None

    location: Optional[str] = None

    severity: SeverityLevel = SeverityLevel.UNKNOWN

    frequency: Optional[str] = None

    triggers: List[str] = Field(
        default_factory=list
    )

    relieving_factors: List[str] = Field(
        default_factory=list
    )

    associated_symptoms: List[str] = Field(
        default_factory=list
    )


# ============================================================
# MEDICAL CONDITION
# ============================================================

class MedicalCondition(BaseModel):
    name: str

    diagnosed_date: Optional[str] = None

    status: Optional[str] = None

    notes: Optional[str] = None


# ============================================================
# MEDICAL HISTORY
# ============================================================

class MedicalHistory(BaseModel):
    conditions: List[MedicalCondition] = Field(
        default_factory=list
    )

    previous_surgeries: List[str] = Field(
        default_factory=list
    )

    allergies: List[str] = Field(
        default_factory=list
    )

    family_history: List[str] = Field(
        default_factory=list
    )

    lifestyle_notes: List[str] = Field(
        default_factory=list
    )


# ============================================================
# MEDICATION
# ============================================================

class Medication(BaseModel):
    name: str

    dosage: Optional[str] = None

    frequency: Optional[str] = None

    route: Optional[str] = None

    duration: Optional[str] = None

    purpose: Optional[str] = None

    start_date: Optional[str] = None

    end_date: Optional[str] = None


# ============================================================
# LAB VALUE
# ============================================================

class LabValue(BaseModel):
    test_name: str

    value: str

    unit: Optional[str] = None

    reference_range: Optional[str] = None

    status: Optional[str] = None

    date: Optional[str] = None

    confidence: float = Field(
        default=0.0,
        ge=0,
        le=1
    )


# ============================================================
# MEDICAL ENTITY
# ============================================================

class MedicalEntity(BaseModel):
    entity_type: str

    value: str

    normalized_value: Optional[str] = None

    confidence: float = Field(
        default=0.0,
        ge=0,
        le=1
    )

    source_text: Optional[str] = None

    page_number: Optional[int] = None


# ============================================================
# RED FLAG
# ============================================================

class RedFlag(BaseModel):
    flag_id: str

    category: str

    symptom: str

    severity: AlertSeverity

    reason: str

    evidence: Optional[str] = None

    recommended_action: str

    requires_staff_attention: bool = True


class RedFlagRequest(BaseModel):
    symptoms: List[str] = Field(
        default_factory=list
    )

    clinical_text: Optional[str] = None

    interview_answers: Dict[str, str] = Field(
        default_factory=dict
    )

    language: LanguageCode = LanguageCode.ENGLISH


class RedFlagResponse(BaseModel):
    success: bool = True

    red_flag_detected: bool

    overall_severity: AlertSeverity = AlertSeverity.LOW

    flags: List[RedFlag] = Field(
        default_factory=list
    )

    staff_alert_required: bool = False

    disclaimer: str = (
        "Red-flag detection is an alerting and "
        "clinical support feature. It is not a diagnosis."
    )


# ============================================================
# CLINICAL SUMMARY REQUEST
# ============================================================

class ClinicalSummaryRequest(BaseModel):
    patient_id: Optional[str] = None

    session_id: Optional[str] = None

    patient_info: Optional[PatientBasicInfo] = None

    symptoms: List[Symptom] = Field(
        default_factory=list
    )

    medical_history: Optional[MedicalHistory] = None

    medications: List[Medication] = Field(
        default_factory=list
    )

    lab_values: List[LabValue] = Field(
        default_factory=list
    )

    medical_entities: List[MedicalEntity] = Field(
        default_factory=list
    )

    red_flags: List[RedFlag] = Field(
        default_factory=list
    )

    language: LanguageCode = LanguageCode.ENGLISH


# ============================================================
# CLINICAL SUMMARY
# ============================================================

class ClinicalSummary(BaseModel):
    chief_complaint: Optional[str] = None

    symptoms: List[Symptom] = Field(
        default_factory=list
    )

    medical_history: Optional[MedicalHistory] = None

    medications: List[Medication] = Field(
        default_factory=list
    )

    lab_values: List[LabValue] = Field(
        default_factory=list
    )

    important_findings: List[str] = Field(
        default_factory=list
    )

    red_flag_alerts: List[RedFlag] = Field(
        default_factory=list
    )

    timeline_events: List[str] = Field(
        default_factory=list
    )

    summary_text: str = ""

    generated_at: Optional[datetime] = None


class ClinicalSummaryResponse(BaseModel):
    success: bool = True

    patient_id: Optional[str] = None

    session_id: Optional[str] = None

    status: ProcessingStatus

    summary: ClinicalSummary

    review_status: ReviewStatus = ReviewStatus.PENDING

    disclaimer: str = (
        "This summary is AI-assisted and should be "
        "reviewed by a qualified healthcare professional."
    )


# ============================================================
# MEDICAL DOCUMENT
# ============================================================

class MedicalDocument(BaseModel):
    document_id: str

    patient_id: Optional[str] = None

    file_name: str

    file_type: FileType

    document_type: DocumentType = DocumentType.UNKNOWN

    status: ProcessingStatus = ProcessingStatus.PENDING

    uploaded_at: Optional[datetime] = None


# ============================================================
# OCR
# ============================================================

class OCRTextBlock(BaseModel):
    text: str

    page_number: Optional[int] = None

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1
    )


class OCRResponse(BaseModel):
    success: bool = True

    document_id: Optional[str] = None

    status: ProcessingStatus

    extracted_text: str = ""

    pages: int = 0

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1
    )

    text_blocks: List[OCRTextBlock] = Field(
        default_factory=list
    )


# ============================================================
# MEDICAL TIMELINE
# ============================================================

class TimelineEvent(BaseModel):
    event_id: str

    date: Optional[str] = None

    title: str

    description: Optional[str] = None

    event_type: str

    source: Optional[str] = None


class MedicalTimelineResponse(BaseModel):
    success: bool = True

    patient_id: Optional[str] = None

    events: List[TimelineEvent] = Field(
        default_factory=list
    )


# ============================================================
# DOCTOR REVIEW
# ============================================================

class DoctorReviewRequest(BaseModel):
    summary_id: str

    doctor_id: str

    status: ReviewStatus

    comments: Optional[str] = None

    edited_summary: Optional[str] = None


class DoctorReviewResponse(BaseModel):
    success: bool = True

    summary_id: str

    doctor_id: str

    review_status: ReviewStatus

    comments: Optional[str] = None

    reviewed_at: Optional[datetime] = None


# ============================================================
# TRANSLATION
# ============================================================

class TranslationRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=10000
    )

    source_language: LanguageCode

    target_language: LanguageCode


class TranslationResponse(BaseModel):
    success: bool = True

    source_language: LanguageCode

    target_language: LanguageCode

    original_text: str

    translated_text: str


# ============================================================
# SPEECH TO TEXT
# ============================================================

class SpeechToTextRequest(BaseModel):
    language: LanguageCode = LanguageCode.ENGLISH

    session_id: Optional[str] = None


class SpeechToTextResponse(BaseModel):
    success: bool = True

    text: str

    language: LanguageCode

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1
    )


# ============================================================
# AYUSH ASSESSMENT
# ============================================================

class AyushAssessment(BaseModel):
    prakriti: Optional[str] = None

    vikriti: Optional[str] = None

    agni: Optional[str] = None

    koshtha: Optional[str] = None

    ahara: Optional[str] = None

    vihara: Optional[str] = None

    dashavidha_pariksha: Dict[str, str] = Field(
        default_factory=dict
    )


class AyushAssessmentRequest(BaseModel):
    patient_id: Optional[str] = None

    responses: Dict[str, str] = Field(
        default_factory=dict
    )

    language: LanguageCode = LanguageCode.ENGLISH


class AyushAssessmentResponse(BaseModel):
    success: bool = True

    patient_id: Optional[str] = None

    assessment: AyushAssessment


# ============================================================
# AI CONFIDENCE
# ============================================================

class AIConfidence(BaseModel):
    overall: float = Field(
        default=0.0,
        ge=0,
        le=1
    )

    explanation: Optional[str] = None


class AIResultMetadata(BaseModel):
    model_name: Optional[str] = None

    model_version: Optional[str] = None

    confidence: Optional[AIConfidence] = None

    processing_time_ms: Optional[float] = None

    generated_at: Optional[datetime] = None


# ============================================================
# FINAL AI CLINICAL REPORT
# ============================================================

class AIClinicalReport(BaseModel):
    patient_id: Optional[str] = None

    session_id: Optional[str] = None

    patient: Optional[PatientBasicInfo] = None

    interview: Optional[InterviewSummary] = None

    symptoms: List[Symptom] = Field(
        default_factory=list
    )

    medical_history: Optional[MedicalHistory] = None

    medications: List[Medication] = Field(
        default_factory=list
    )

    lab_values: List[LabValue] = Field(
        default_factory=list
    )

    medical_entities: List[MedicalEntity] = Field(
        default_factory=list
    )

    red_flags: List[RedFlag] = Field(
        default_factory=list
    )

    timeline: List[TimelineEvent] = Field(
        default_factory=list
    )

    clinical_summary: Optional[ClinicalSummary] = None

    ayush_assessment: Optional[AyushAssessment] = None

    metadata: Optional[AIResultMetadata] = None

    generated_at: Optional[datetime] = None

    review_status: ReviewStatus = ReviewStatus.PENDING