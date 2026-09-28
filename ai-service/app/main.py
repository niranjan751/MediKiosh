from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.interview import router as interview_router
from app.routes.red_flags import router as red_flag_router
from app.routes.ocr import router as ocr_router
from app.routes.summary import router as summary_router
from app.routes.timeline import router as timeline_router
from app.routes.ayush import router as ayush_router
from app.routes.translation import router as translation_router
from app.routes.voice import router as voice_router
from app.routes.nlp import router as nlp_router
from app.routes.fhir import router as fhir_router


# ============================================================
# MEDIKIOSK AI SERVICE
# ============================================================

app = FastAPI(
    title="MediKiosk AI Service",
    description=(
        "Comprehensive clinical AI microservice for the MediKiosk healthcare platform: "
        "Adaptive SOCRATES Clinical Interview, Emergency Red-Flag & Hospital Triage Alerts, "
        "Medical Document OCR (Prescriptions, Labs, Discharge Summaries), Clinical NLP (NegEx, NER), "
        "Medical Timeline Generator, Physician-Ready SOAP Summaries, Classical AYUSH/Ayurveda Mode, "
        "ABDM / HL7 FHIR R4 Bundle Interoperability, and Multilingual Translation & Voice Processing."
    ),
    version="2.1.0",
)

# Enable CORS for frontend & backend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTES REGISTRATION
# ============================================================

app.include_router(interview_router)
app.include_router(red_flag_router)
app.include_router(ocr_router)
app.include_router(summary_router)
app.include_router(timeline_router)
app.include_router(ayush_router)
app.include_router(translation_router)
app.include_router(voice_router)
app.include_router(nlp_router)
app.include_router(fhir_router)


# ============================================================
# ROOT & SYSTEM HEALTH
# ============================================================

@app.get("/")
def root():
    return {
        "message": "MediKiosk AI Clinical Service is running",
        "status": "online",
        "version": "2.1.0",
        "modules": [
            "Adaptive SOCRATES Clinical Interview (en, ta, hi, te, kn, ml)",
            "Emergency Red-Flag & Triage Alert Engine (Level 1 to Level 4)",
            "Deep Medical OCR (Prescriptions, Quantitative Lab Reports, Discharge)",
            "Clinical NLP with NegEx Negation Detection and Entity Categorization",
            "Automated Chronological Medical Timeline",
            "Physician-Ready SOAP Clinical Intake Summary",
            "Classical AYUSH / Ayurveda Mode (Tridosha & Dashavidha Pariksha)",
            "HL7 FHIR R4 / ABDM Electronic Health Record Interoperability",
            "Multilingual Translation & Voice Processing",
        ],
    }


@app.get("/health")
def health_check():
    return {
        "service": "MediKiosk AI Service",
        "status": "healthy",
        "version": "2.1.0",
        "services": {
            "adaptive_interview": "online",
            "red_flag_triage": "online",
            "ocr_engine": "online",
            "clinical_nlp": "online",
            "clinical_summary": "online",
            "medical_timeline": "online",
            "ayush_mode": "online",
            "translation": "online",
            "voice_intake": "online",
            "fhir_abdm": "online",
        },
    }