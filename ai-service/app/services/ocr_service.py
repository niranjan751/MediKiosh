"""
MediKiosk AI Service
OCR Service

Purpose:
    Extract text from uploaded medical documents such as:
        - JPG
        - JPEG
        - PNG
        - PDF

Features:
    1. Image preprocessing
    2. Tesseract OCR
    3. PDF page processing
    4. Text cleaning
    5. Medical entity extraction
    6. Date extraction
    7. Medicine extraction
    8. Dosage extraction
    9. Lab value extraction
    10. Basic condition extraction
    11. OCR confidence estimation
    12. OCR dependency health check

Important:
    This service performs document digitization and basic information
    extraction. It does NOT diagnose diseases or replace clinical review.
"""

from __future__ import annotations

import io
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

# Your actual Windows Tesseract installation.
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def configure_tesseract() -> bool:
    """
    Configure pytesseract to use the installed Windows
    Tesseract executable.

    Returns:
        True  -> Tesseract executable exists
        False -> Tesseract executable was not found
    """

    if os.path.isfile(TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        return True

    return False


TESSERACT_CONFIGURED = configure_tesseract()


# ============================================================
# CONFIGURATION
# ============================================================

SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".tif",
}

SUPPORTED_DOCUMENT_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".tif",
    ".pdf",
}

MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# ============================================================
# MEDICAL KEYWORDS
# ============================================================

MEDICAL_KEYWORDS = [
    "diagnosis",
    "diagnoses",
    "disease",
    "condition",
    "symptom",
    "symptoms",
    "medicine",
    "medication",
    "medications",
    "tablet",
    "tablets",
    "capsule",
    "capsules",
    "syrup",
    "injection",
    "dose",
    "dosage",
    "blood pressure",
    "pulse",
    "temperature",
    "glucose",
    "sugar",
    "hemoglobin",
    "haemoglobin",
    "cholesterol",
    "creatinine",
    "platelet",
    "wbc",
    "rbc",
    "thyroid",
    "tsh",
    "t3",
    "t4",
    "hba1c",
    "ecg",
    "x-ray",
    "xray",
    "scan",
    "ultrasound",
    "mri",
    "ct scan",
    "report",
    "laboratory",
    "lab",
    "prescription",
    "clinical",
    "medical",
]


# ============================================================
# COMMON MEDICINES
# ============================================================

COMMON_MEDICINES = [
    "paracetamol",
    "acetaminophen",
    "ibuprofen",
    "amoxicillin",
    "azithromycin",
    "cetirizine",
    "omeprazole",
    "pantoprazole",
    "metformin",
    "amlodipine",
    "atorvastatin",
    "losartan",
    "aspirin",
    "insulin",
    "diclofenac",
    "levocetirizine",
    "montelukast",
    "rabeprazole",
    "domperidone",
    "ondansetron",
    "clavulanate",
]


# ============================================================
# COMMON LAB TEST NAMES
# ============================================================

COMMON_LAB_TESTS = [
    "hemoglobin",
    "haemoglobin",
    "glucose",
    "blood sugar",
    "fasting blood sugar",
    "post prandial blood sugar",
    "hba1c",
    "cholesterol",
    "triglycerides",
    "creatinine",
    "urea",
    "bilirubin",
    "platelet",
    "platelets",
    "wbc",
    "rbc",
    "tsh",
    "t3",
    "t4",
    "sodium",
    "potassium",
    "calcium",
    "vitamin d",
    "vitamin b12",
    "blood pressure",
    "pulse",
    "temperature",
]


# ============================================================
# COMMON CONDITIONS
# ============================================================

COMMON_CONDITIONS = [
    "diabetes",
    "diabetes mellitus",
    "hypertension",
    "hypotension",
    "asthma",
    "anemia",
    "anaemia",
    "infection",
    "fever",
    "migraine",
    "gastritis",
    "ulcer",
    "arthritis",
    "allergy",
    "allergic rhinitis",
    "thyroid",
    "hypothyroidism",
    "hyperthyroidism",
    "pneumonia",
    "bronchitis",
    "covid",
    "covid-19",
    "influenza",
]


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize OCR text.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\t", " ")

    # Reduce repeated spaces.
    text = re.sub(r"[ ]{2,}", " ", text)

    # Reduce excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_ocr_text(text: str) -> str:
    """
    Clean common OCR artifacts.
    """

    if not text:
        return ""

    text = normalize_text(text)

    text = re.sub(r"[|]{2,}", "|", text)
    text = re.sub(r"[_]{3,}", "_", text)

    text = text.replace("•", "-")
    text = text.replace("●", "-")
    text = text.replace("▪", "-")

    return text.strip()


def calculate_text_confidence(text: str) -> float:
    """
    Estimate OCR quality using simple text-length heuristics.

    This is NOT a medical confidence score.
    """

    if not text:
        return 0.0

    length = len(text.strip())

    if length < 10:
        return 20.0

    if length < 50:
        return 45.0

    if length < 100:
        return 60.0

    if length < 300:
        return 75.0

    if length < 1000:
        return 85.0

    return 90.0


# ============================================================
# FILE VALIDATION
# ============================================================

def validate_file_extension(
    filename: str,
) -> Tuple[bool, str]:
    """
    Validate uploaded document extension.
    """

    if not filename:
        return False, "Filename is required."

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_DOCUMENT_EXTENSIONS:
        supported = ", ".join(
            sorted(SUPPORTED_DOCUMENT_EXTENSIONS)
        )

        return (
            False,
            f"Unsupported file type. Supported types: {supported}",
        )

    return True, extension


def validate_file_size(
    file_bytes: bytes,
) -> Tuple[bool, str]:
    """
    Validate uploaded file size.
    """

    if not file_bytes:
        return False, "Uploaded file is empty."

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return (
            False,
            f"File size exceeds the "
            f"{MAX_FILE_SIZE_MB} MB limit.",
        )

    return True, ""


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(
    image: Image.Image,
) -> Image.Image:
    """
    Preprocess image before OCR.

    Steps:
        1. Convert to RGB
        2. Convert to grayscale
        3. Improve contrast
        4. Sharpen
        5. Apply autocontrast
    """

    if image.mode != "RGB":
        image = image.convert("RGB")

    gray = ImageOps.grayscale(image)

    contrast = ImageEnhance.Contrast(gray)
    gray = contrast.enhance(1.5)

    gray = gray.filter(ImageFilter.SHARPEN)

    gray = ImageOps.autocontrast(gray)

    return gray


# ============================================================
# IMAGE OCR
# ============================================================

def extract_text_from_image(
    image: Image.Image,
    language: str = "eng",
) -> Dict[str, Any]:
    """
    Extract text from a PIL image using Tesseract.
    """

    if not TESSERACT_CONFIGURED:
        raise RuntimeError(
            "Tesseract OCR was not found at:\n"
            f"{TESSERACT_PATH}\n\n"
            "Please install Tesseract OCR or update "
            "TESSERACT_PATH in ocr_service.py."
        )

    processed_image = preprocess_image(image)

    try:
        text = pytesseract.image_to_string(
            processed_image,
            lang=language,
            config="--psm 6",
        )

        text = clean_ocr_text(text)

        confidence = calculate_text_confidence(text)

        return {
            "text": text,
            "confidence": confidence,
            "width": processed_image.width,
            "height": processed_image.height,
        }

    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract executable could not be started.\n"
            f"Expected location: {TESSERACT_PATH}"
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            f"Image OCR failed: {str(exc)}"
        ) from exc


# ============================================================
# PDF OCR
# ============================================================

def extract_text_from_pdf(
    file_bytes: bytes,
    language: str = "eng",
) -> Dict[str, Any]:
    """
    Extract text from PDF pages using OCR.

    PyMuPDF is used to render PDF pages into images.
    """

    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is required for PDF OCR.\n"
            "Install it using:\n"
            "pip install pymupdf"
        ) from exc

    if not TESSERACT_CONFIGURED:
        raise RuntimeError(
            "Tesseract OCR was not found at:\n"
            f"{TESSERACT_PATH}"
        )

    temp_path: Optional[str] = None
    document = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        document = fitz.open(temp_path)

        page_results: List[Dict[str, Any]] = []
        combined_text: List[str] = []

        for page_number in range(len(document)):
            page = document.load_page(page_number)

            matrix = fitz.Matrix(2.0, 2.0)

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image_bytes = pixmap.tobytes("png")

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            result = extract_text_from_image(
                image=image,
                language=language,
            )

            page_text = result["text"]

            page_results.append(
                {
                    "page_number": page_number + 1,
                    "text": page_text,
                    "confidence": result["confidence"],
                }
            )

            if page_text:
                combined_text.append(
                    f"--- Page {page_number + 1} ---\n"
                    f"{page_text}"
                )

        full_text = "\n\n".join(
            combined_text
        )

        if page_results:
            confidence = (
                sum(
                    page["confidence"]
                    for page in page_results
                )
                / len(page_results)
            )
        else:
            confidence = 0.0

        return {
            "text": clean_ocr_text(full_text),
            "confidence": round(
                confidence,
                2,
            ),
            "page_count": len(page_results),
            "pages": page_results,
        }

    except Exception as exc:
        raise RuntimeError(
            f"PDF OCR failed: {str(exc)}"
        ) from exc

    finally:
        if document is not None:
            try:
                document.close()
            except Exception:
                pass

        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


# ============================================================
# DATE EXTRACTION
# ============================================================

def extract_dates(
    text: str,
) -> List[str]:
    """
    Extract common date formats.
    """

    if not text:
        return []

    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b",
        r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b",
        (
            r"\b\d{1,2}\s+"
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"(?:[a-z]*)?\s+\d{2,4}\b"
        ),
        (
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"(?:[a-z]*)?\s+\d{1,2},?\s+\d{2,4}\b"
        ),
    ]

    results: List[str] = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        results.extend(matches)

    return list(
        dict.fromkeys(
            item.strip()
            for item in results
        )
    )


# ============================================================
# DOSAGE EXTRACTION
# ============================================================

def extract_dosages(
    text: str,
) -> List[str]:
    """
    Extract common medication dosage expressions.
    """

    if not text:
        return []

    patterns = [
        r"\b\d+(?:\.\d+)?\s*mg\b",
        r"\b\d+(?:\.\d+)?\s*g\b",
        r"\b\d+(?:\.\d+)?\s*mcg\b",
        r"\b\d+(?:\.\d+)?\s*µg\b",
        r"\b\d+(?:\.\d+)?\s*ml\b",
        r"\b\d+(?:\.\d+)?\s*l\b",
        r"\b\d+(?:\.\d+)?\s*units?\b",
        r"\b\d+\s+(?:tablet|tablets|capsule|capsules)\b",
    ]

    results: List[str] = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        results.extend(matches)

    return list(
        dict.fromkeys(
            item.strip()
            for item in results
        )
    )


# ============================================================
# MEDICINE EXTRACTION
# ============================================================

def extract_medicines(
    text: str,
) -> List[str]:
    """
    Detect common medicine names.

    This is keyword-based prototype extraction.
    """

    if not text:
        return []

    normalized = text.lower()

    medicines: List[str] = []

    for medicine in COMMON_MEDICINES:
        if medicine.lower() in normalized:
            medicines.append(medicine)

    return list(
        dict.fromkeys(medicines)
    )


# ============================================================
# LAB VALUE EXTRACTION
# ============================================================

def extract_lab_values(
    text: str,
) -> List[Dict[str, str]]:
    """
    Extract simple lab-test + numeric-value patterns.
    """

    if not text:
        return []

    results: List[Dict[str, str]] = []

    lab_pattern = (
        r"("
        + "|".join(
            re.escape(test)
            for test in COMMON_LAB_TESTS
        )
        + r")"
        r"\s*[:\-]?\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*"
        r"([a-zA-Z/%µ]+(?:/[a-zA-Z]+)?)?"
    )

    matches = re.finditer(
        lab_pattern,
        text,
        flags=re.IGNORECASE,
    )

    for match in matches:
        test_name = match.group(1)
        value = match.group(2)
        unit = match.group(3) or ""

        results.append(
            {
                "test": test_name.strip(),
                "value": value.strip(),
                "unit": unit.strip(),
            }
        )

    return results


# ============================================================
# CONDITION EXTRACTION
# ============================================================

def extract_conditions(
    text: str,
) -> List[str]:
    """
    Detect common medical condition terms.

    This does NOT confirm a diagnosis.
    It only identifies terms appearing in the document.
    """

    if not text:
        return []

    normalized = text.lower()

    conditions: List[str] = []

    for condition in COMMON_CONDITIONS:
        if condition.lower() in normalized:
            conditions.append(condition)

    return list(
        dict.fromkeys(conditions)
    )


# ============================================================
# MEDICAL ENTITY EXTRACTION
# ============================================================

def extract_medical_entities(
    text: str,
) -> Dict[str, Any]:
    """
    Extract basic medical entities.
    """

    return {
        "dates": extract_dates(text),
        "medicines": extract_medicines(text),
        "dosages": extract_dosages(text),
        "lab_values": extract_lab_values(text),
        "conditions": extract_conditions(text),
    }


# ============================================================
# MEDICAL CONTENT DETECTION
# ============================================================

def detect_medical_content(
    text: str,
) -> Dict[str, Any]:
    """
    Determine whether OCR text appears to contain
    medical-related content.
    """

    if not text:
        return {
            "medical_document": False,
            "matched_keywords": [],
            "keyword_count": 0,
        }

    normalized = text.lower()

    matched_keywords = [
        keyword
        for keyword in MEDICAL_KEYWORDS
        if keyword.lower() in normalized
    ]

    matched_keywords = list(
        dict.fromkeys(matched_keywords)
    )

    return {
        "medical_document": (
            len(matched_keywords) > 0
        ),
        "matched_keywords": matched_keywords,
        "keyword_count": len(matched_keywords),
    }


# ============================================================
# DOCUMENT TYPE DETECTION
# ============================================================

def detect_document_type(
    text: str,
) -> str:
    """
    Estimate document type from OCR text.

    Possible values:
        prescription
        laboratory_report
        medical_report
        discharge_summary
        clinical_document
        unknown
    """

    if not text:
        return "unknown"

    normalized = text.lower()

    if (
        "prescription" in normalized
        or "rx" in normalized
        or "tablet" in normalized
        or "capsule" in normalized
    ):
        return "prescription"

    if (
        "laboratory" in normalized
        or "lab report" in normalized
        or "hemoglobin" in normalized
        or "glucose" in normalized
        or "creatinine" in normalized
    ):
        return "laboratory_report"

    if (
        "discharge summary" in normalized
        or "discharge" in normalized
    ):
        return "discharge_summary"

    if (
        "medical report" in normalized
        or "clinical report" in normalized
    ):
        return "medical_report"

    if detect_medical_content(text)[
        "medical_document"
    ]:
        return "clinical_document"

    return "unknown"


# ============================================================
# MAIN OCR PROCESSING
# ============================================================

def process_document(
    file_bytes: bytes,
    filename: str,
    language: str = "eng",
) -> Dict[str, Any]:
    """
    Main OCR processing function.

    Supported:
        JPG
        JPEG
        PNG
        BMP
        TIFF
        PDF
    """

    valid_extension, extension_or_error = (
        validate_file_extension(filename)
    )

    if not valid_extension:
        raise ValueError(extension_or_error)

    extension = extension_or_error

    valid_size, size_error = validate_file_size(
        file_bytes
    )

    if not valid_size:
        raise ValueError(size_error)

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if extension == ".pdf":

        ocr_result = extract_text_from_pdf(
            file_bytes=file_bytes,
            language=language,
        )

        text = ocr_result["text"]

        entities = extract_medical_entities(
            text
        )

        medical_content = detect_medical_content(
            text
        )

        document_type = detect_document_type(
            text
        )

        return {
            "filename": filename,
            "file_type": "pdf",
            "text": text,
            "confidence": ocr_result[
                "confidence"
            ],
            "page_count": ocr_result[
                "page_count"
            ],
            "pages": ocr_result["pages"],
            "document_type": document_type,
            "medical_content": medical_content,
            "entities": entities,
            "processed_at": datetime.utcnow().isoformat(),
        }

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    try:
        image = Image.open(
            io.BytesIO(file_bytes)
        )

        ocr_result = extract_text_from_image(
            image=image,
            language=language,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Unable to open image document: {str(exc)}"
        ) from exc

    text = ocr_result["text"]

    entities = extract_medical_entities(
        text
    )

    medical_content = detect_medical_content(
        text
    )

    document_type = detect_document_type(
        text
    )

    return {
        "filename": filename,
        "file_type": extension.replace(
            ".",
            "",
        ),
        "text": text,
        "confidence": ocr_result[
            "confidence"
        ],
        "page_count": 1,
        "pages": [
            {
                "page_number": 1,
                "text": text,
                "confidence": ocr_result[
                    "confidence"
                ],
            }
        ],
        "document_type": document_type,
        "medical_content": medical_content,
        "entities": entities,
        "processed_at": datetime.utcnow().isoformat(),
    }


# ============================================================
# TEXT PREVIEW
# ============================================================

def create_text_preview(
    text: str,
    max_length: int = 500,
) -> str:
    """
    Create a short OCR text preview.
    """

    if not text:
        return ""

    text = clean_ocr_text(text)

    if len(text) <= max_length:
        return text

    return (
        text[:max_length].rstrip()
        + "..."
    )


# ============================================================
# OCR SUMMARY
# ============================================================

def create_ocr_summary(
    ocr_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create a simplified summary for dashboard/frontend use.
    """

    text = ocr_result.get(
        "text",
        "",
    )

    entities = ocr_result.get(
        "entities",
        {},
    )

    medical_content = ocr_result.get(
        "medical_content",
        {},
    )

    return {
        "filename": ocr_result.get(
            "filename",
            "",
        ),
        "document_type": ocr_result.get(
            "document_type",
            "unknown",
        ),
        "ocr_confidence": ocr_result.get(
            "confidence",
            0.0,
        ),
        "page_count": ocr_result.get(
            "page_count",
            0,
        ),
        "text_preview": create_text_preview(
            text
        ),
        "entity_counts": {
            "dates": len(
                entities.get(
                    "dates",
                    [],
                )
            ),
            "medicines": len(
                entities.get(
                    "medicines",
                    [],
                )
            ),
            "dosages": len(
                entities.get(
                    "dosages",
                    [],
                )
            ),
            "lab_values": len(
                entities.get(
                    "lab_values",
                    [],
                )
            ),
            "conditions": len(
                entities.get(
                    "conditions",
                    [],
                )
            ),
        },
        "medical_document": medical_content.get(
            "medical_document",
            False,
        ),
    }


# ============================================================
# OCR DEPENDENCY HEALTH CHECK
# ============================================================

def check_ocr_dependencies() -> Dict[str, Any]:
    """
    Check OCR dependencies.

    Checks:
        - pytesseract
        - Tesseract executable
        - PyMuPDF
    """

    result: Dict[str, Any] = {
        "pytesseract": True,
        "tesseract_configured": TESSERACT_CONFIGURED,
        "tesseract_available": False,
        "pymupdf_available": False,
    }

    # --------------------------------------------------------
    # Tesseract
    # --------------------------------------------------------

    if not TESSERACT_CONFIGURED:
        result["tesseract_error"] = (
            "Tesseract executable not found at: "
            f"{TESSERACT_PATH}"
        )
    else:
        try:
            version = (
                pytesseract.get_tesseract_version()
            )

            result[
                "tesseract_available"
            ] = True

            result[
                "tesseract_version"
            ] = str(version)

            result[
                "tesseract_path"
            ] = TESSERACT_PATH

        except Exception as exc:
            result[
                "tesseract_error"
            ] = str(exc)

    # --------------------------------------------------------
    # PyMuPDF
    # --------------------------------------------------------

    try:
        import fitz

        result[
            "pymupdf_available"
        ] = True

        result[
            "pymupdf_version"
        ] = getattr(
            fitz,
            "version",
            None,
        )

    except Exception as exc:
        result[
            "pymupdf_available"
        ] = False

        result[
            "pymupdf_error"
        ] = str(exc)

    return result


# ============================================================
# SUPPORTED FILE INFORMATION
# ============================================================

def get_supported_file_information() -> Dict[str, Any]:
    """
    Return OCR supported file information.
    """

    return {
        "supported_extensions": sorted(
            SUPPORTED_DOCUMENT_EXTENSIONS
        ),
        "image_extensions": sorted(
            SUPPORTED_IMAGE_EXTENSIONS
        ),
        "maximum_file_size_mb": (
            MAX_FILE_SIZE_MB
        ),
        "ocr_engine": "Tesseract OCR",
        "tesseract_path": TESSERACT_PATH,
        "tesseract_configured": (
            TESSERACT_CONFIGURED
        ),
        "pdf_engine": "PyMuPDF",
        "medical_entity_extraction": [
            "dates",
            "medicines",
            "dosages",
            "lab_values",
            "conditions",
        ],
        "disclaimer": (
            "OCR and entity extraction are assistive "
            "document-digitization features. Extracted "
            "information should be reviewed by a qualified "
            "healthcare professional."
        ),
    }
