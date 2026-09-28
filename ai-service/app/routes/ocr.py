"""
MediKiosk AI Service
OCR API Routes

Purpose:
    Provide REST API endpoints for medical document OCR.

Supported:
    - JPG
    - JPEG
    - PNG
    - BMP
    - TIFF
    - PDF

Important:
    OCR is used for document digitization and information extraction.
    Extracted medical information must be reviewed by a healthcare
    professional.
"""

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ocr_service import (
    check_ocr_dependencies,
    create_ocr_summary,
    get_supported_file_information,
    process_document,
)


router = APIRouter(
    prefix="/ocr",
    tags=["OCR"],
)


# ============================================================
# OCR HEALTH CHECK
# ============================================================

@router.get("/health")
def ocr_health():
    """
    Check OCR engine and dependency status.
    """

    result = check_ocr_dependencies()

    return {
        "service": "OCR Service",
        "status": (
            "healthy"
            if result.get("tesseract_available")
            and result.get("pymupdf_available")
            else "degraded"
        ),
        "dependencies": result,
    }


# ============================================================
# SUPPORTED FILE INFORMATION
# ============================================================

@router.get("/supported-files")
def supported_files():
    """
    Return supported document formats and OCR capabilities.
    """

    return get_supported_file_information()


# ============================================================
# UPLOAD AND PROCESS DOCUMENT
# ============================================================

@router.post("/process")
async def process_ocr_document(
    file: UploadFile = File(...),
    language: str = "eng",
):
    """
    Upload a medical document and perform OCR.

    Supported:
        JPG
        JPEG
        PNG
        BMP
        TIFF
        PDF
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    try:
        file_bytes = await file.read()

        result = process_document(
            file_bytes=file_bytes,
            filename=file.filename,
            language=language,
        )

        return {
            "success": True,
            "message": "Document processed successfully.",
            "data": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(exc)}",
        ) from exc


# ============================================================
# OCR SUMMARY
# ============================================================

@router.post("/summary")
async def process_ocr_summary(
    file: UploadFile = File(...),
    language: str = "eng",
):
    """
    Upload a document and return a simplified OCR summary.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    try:
        file_bytes = await file.read()

        result = process_document(
            file_bytes=file_bytes,
            filename=file.filename,
            language=language,
        )

        summary = create_ocr_summary(result)

        return {
            "success": True,
            "message": "OCR summary generated successfully.",
            "data": summary,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OCR summary failed: {str(exc)}",
        ) from exc


# ============================================================
# OCR DISCLAIMER
# ============================================================

@router.get("/disclaimer")
def ocr_disclaimer():
    """
    Return OCR safety information.
    """

    return {
        "message": (
            "OCR and medical entity extraction are assistive "
            "document-digitization features. Extracted information "
            "should be reviewed and confirmed by a qualified "
            "healthcare professional."
        ),
        "diagnosis": False,
        "autonomous_medical_decision": False,
    }