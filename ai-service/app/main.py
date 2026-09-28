# pyrefly: ignore [missing-import]
from fastapi import FastAPI

from app.routes.interview import router as interview_router
from app.routes.red_flags import router as red_flag_router
from app.routes.ocr import router as ocr_router
from app.routes.summary import router as summary_router


# ============================================================
# MEDIKIOSK AI SERVICE
# ============================================================

app = FastAPI(
    title="MediKiosk AI Service",
    description=(
        "AI services for clinical history, "
        "red-flag detection, medical document processing, "
        "OCR, clinical NLP and AI-assisted summaries."
    ),
    version="1.0.0",
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(interview_router)
app.include_router(red_flag_router)
app.include_router(ocr_router)
app.include_router(summary_router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "MediKiosk AI Service is running",
        "status": "online",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "service": "MediKiosk AI Service",
        "status": "healthy",
        "services": {
            "clinical_interview": "online",
            "red_flag_detection": "online",
            "ocr": "online",
            "clinical_nlp": "planned",
            "clinical_summary": "planned",
        },
    }