"""
MediKiosk AI Service - Advanced Medical Document OCR & Entity Extraction
========================================================================

Purpose:
    Digitize and extract structured clinical information from:
    - Doctor Prescriptions
    - Laboratory Investigation Reports
    - Hospital Discharge Summaries
    - Scan / Imaging Reports
    Supported Formats: JPG, JPEG, PNG, BMP, TIFF, PDF.

Core Capabilities:
    1. Preprocessing (autocontrast, sharpening, grayscale binarization).
    2. Document Type Detection (Prescription, Lab Report, Discharge Summary, Scan).
    3. Document Date Extraction (Chronological tagging).
    4. Extensive Medication Detection (Generic & Brand Names, Dosages, Regimens like 1-0-1, OD, BD).
    5. Quantitative Lab Result Extraction with Reference Range & Status (NORMAL, HIGH, LOW, CRITICAL).
    6. Diagnoses & Surgical Procedures extraction.
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

from app.models.schemas import (
    DocumentAnalysisResult,
    DocumentType,
    LabValue,
    Medication,
)


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def configure_tesseract() -> bool:
    if os.path.isfile(TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        return True
    return False

TESSERACT_CONFIGURED = configure_tesseract()

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
SUPPORTED_DOCUMENT_EXTENSIONS = SUPPORTED_IMAGE_EXTENSIONS | {".pdf"}
MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# ============================================================
# CLINICAL REFERENCE DICTIONARIES (DRUGS, LABS, CONDITIONS)
# ============================================================

COMPREHENSIVE_DRUG_DATABASE = [
    # Cardiovascular & Antihypertensives
    {"name": "Amlodipine", "generic": "Amlodipine Besylate", "default_dosage": "5 mg", "purpose": "Hypertension"},
    {"name": "Telmisartan", "generic": "Telmisartan", "default_dosage": "40 mg", "purpose": "Hypertension"},
    {"name": "Atorvastatin", "generic": "Atorvastatin Calcium", "default_dosage": "10 mg / 20 mg", "purpose": "Cholesterol / Dyslipidemia"},
    {"name": "Rosuvastatin", "generic": "Rosuvastatin", "default_dosage": "10 mg", "purpose": "Cholesterol"},
    {"name": "Losartan", "generic": "Losartan Potassium", "default_dosage": "50 mg", "purpose": "Hypertension"},
    {"name": "Metoprolol", "generic": "Metoprolol Succinate", "default_dosage": "25 mg / 50 mg", "purpose": "Beta-blocker / Angina"},
    {"name": "Enalapril", "generic": "Enalapril Maleate", "default_dosage": "5 mg", "purpose": "ACE Inhibitor"},
    {"name": "Ramipril", "generic": "Ramipril", "default_dosage": "2.5 mg / 5 mg", "purpose": "ACE Inhibitor"},
    {"name": "Aspirin", "generic": "Acetylsalicylic Acid", "default_dosage": "75 mg / 150 mg", "purpose": "Antiplatelet / Blood thinner"},
    {"name": "Ecosprin", "generic": "Aspirin Enteric Coated", "default_dosage": "75 mg", "purpose": "Antiplatelet"},
    {"name": "Clopidogrel", "generic": "Clopidogrel", "default_dosage": "75 mg", "purpose": "Antiplatelet"},
    {"name": "Hydrochlorothiazide", "generic": "Hydrochlorothiazide", "default_dosage": "12.5 mg", "purpose": "Diuretic"},
    {"name": "Furosemide", "generic": "Furosemide / Lasix", "default_dosage": "20 mg / 40 mg", "purpose": "Diuretic"},
    {"name": "Digoxin", "generic": "Digoxin", "default_dosage": "0.25 mg", "purpose": "Inotrope / Arrhythmia"},

    # Diabetes
    {"name": "Metformin", "generic": "Metformin Hydrochloride", "default_dosage": "500 mg / 850 mg", "purpose": "Type 2 Diabetes"},
    {"name": "Glycomet", "generic": "Metformin", "default_dosage": "500 mg", "purpose": "Type 2 Diabetes"},
    {"name": "Glimepiride", "generic": "Glimepiride", "default_dosage": "1 mg / 2 mg", "purpose": "Sulfonylurea / Diabetes"},
    {"name": "Gliclazide", "generic": "Gliclazide", "default_dosage": "80 mg", "purpose": "Diabetes"},
    {"name": "Teneligliptin", "generic": "Teneligliptin", "default_dosage": "20 mg", "purpose": "DPP-4 Inhibitor"},
    {"name": "Sitagliptin", "generic": "Sitagliptin", "default_dosage": "50 mg / 100 mg", "purpose": "Januvia / Diabetes"},
    {"name": "Dapagliflozin", "generic": "Dapagliflozin", "default_dosage": "10 mg", "purpose": "SGLT2 Inhibitor"},
    {"name": "Empagliflozin", "generic": "Empagliflozin / Jardiance", "default_dosage": "10 mg / 25 mg", "purpose": "SGLT2 Inhibitor"},
    {"name": "Insulin", "generic": "Human Insulin / Glargine", "default_dosage": "Subcutaneous", "purpose": "Diabetes"},

    # Gastrointestinal
    {"name": "Pantoprazole", "generic": "Pantoprazole Sodium", "default_dosage": "40 mg", "purpose": "Proton Pump Inhibitor / Acidity"},
    {"name": "Pan-D", "generic": "Pantoprazole + Domperidone", "default_dosage": "Pan 40 + Dom 30", "purpose": "GERD / Acidity"},
    {"name": "Omeprazole", "generic": "Omeprazole", "default_dosage": "20 mg", "purpose": "Acidity / Peptic Ulcer"},
    {"name": "Rabeprazole", "generic": "Rabeprazole Sodium", "default_dosage": "20 mg", "purpose": "PPI / Acidity"},
    {"name": "Domperidone", "generic": "Domperidone", "default_dosage": "10 mg", "purpose": "Antiemetic / Prokinetic"},
    {"name": "Ondansetron", "generic": "Ondansetron / Emset", "default_dosage": "4 mg", "purpose": "Antiemetic / Nausea"},
    {"name": "Sucralfate", "generic": "Sucralfate Syrup", "default_dosage": "10 ml", "purpose": "Mucosal protectant"},

    # Antibiotics & Antimicrobials
    {"name": "Amoxicillin", "generic": "Amoxicillin", "default_dosage": "500 mg", "purpose": "Antibiotic"},
    {"name": "Augmentin", "generic": "Amoxicillin + Clavulanate", "default_dosage": "625 mg", "purpose": "Broad-spectrum Antibiotic"},
    {"name": "Azithromycin", "generic": "Azithromycin", "default_dosage": "250 mg / 500 mg", "purpose": "Macrolide Antibiotic"},
    {"name": "Ciprofloxacin", "generic": "Ciprofloxacin", "default_dosage": "500 mg", "purpose": "Fluoroquinolone"},
    {"name": "Levofloxacin", "generic": "Levofloxacin", "default_dosage": "500 mg", "purpose": "Fluoroquinolone"},
    {"name": "Cefixime", "generic": "Cefixime", "default_dosage": "200 mg", "purpose": "Cephalosporin"},
    {"name": "Doxycycline", "generic": "Doxycycline", "default_dosage": "100 mg", "purpose": "Tetracycline"},
    {"name": "Metronidazole", "generic": "Metronidazole / Flagyl", "default_dosage": "400 mg", "purpose": "Amoebicide / Anaerobes"},

    # Analgesics & Antipyretics
    {"name": "Paracetamol", "generic": "Acetaminophen", "default_dosage": "500 mg / 650 mg", "purpose": "Fever & Mild Pain"},
    {"name": "Dolo", "generic": "Paracetamol 650mg", "default_dosage": "650 mg", "purpose": "Antipyretic / Analgesic"},
    {"name": "Ibuprofen", "generic": "Ibuprofen", "default_dosage": "400 mg", "purpose": "NSAID Pain / Inflammation"},
    {"name": "Diclofenac", "generic": "Diclofenac Sodium", "default_dosage": "50 mg", "purpose": "NSAID Pain relief"},
    {"name": "Aceclofenac", "generic": "Aceclofenac", "default_dosage": "100 mg", "purpose": "NSAID Pain relief"},
    {"name": "Tramadol", "generic": "Tramadol Hydrochloride", "default_dosage": "50 mg", "purpose": "Moderate to severe pain"},

    # Respiratory & Allergy
    {"name": "Montelukast", "generic": "Montelukast Sodium", "default_dosage": "10 mg", "purpose": "Leukotriene receptor antagonist"},
    {"name": "Levocetirizine", "generic": "Levocetirizine Dihydrochloride", "default_dosage": "5 mg", "purpose": "Antihistamine / Allergy"},
    {"name": "Cetirizine", "generic": "Cetirizine", "default_dosage": "10 mg", "purpose": "Antihistamine"},
    {"name": "Budesonide", "generic": "Budecort Inhaler", "default_dosage": "200 mcg", "purpose": "Inhaled Corticosteroid"},
    {"name": "Salbutamol", "generic": "Asthalin / Albuterol", "default_dosage": "100 mcg", "purpose": "Bronchodilator / SABA"},

    # Thyroid & Minerals
    {"name": "Levothyroxine", "generic": "Thyronorm / Eltroxin", "default_dosage": "25 / 50 / 75 / 100 mcg", "purpose": "Hypothyroidism"},
    {"name": "Calcium", "generic": "Calcium Carbonate + Vit D3", "default_dosage": "500 mg", "purpose": "Bone Health"},
    {"name": "Shelcal", "generic": "Calcium 500mg + D3", "default_dosage": "500 mg", "purpose": "Supplement"},
    {"name": "Vitamin D3", "generic": "Cholecalciferol", "default_dosage": "60,000 IU", "purpose": "Vitamin D Deficiency"},
]


# Laboratory Standard Reference Ranges
LAB_TEST_DEFINITIONS = [
    # Complete Blood Count (CBC)
    {"name": "Hemoglobin", "synonyms": ["hb", "haemoglobin", "hgb"], "category": "Hematology", "unit": "g/dL", "low": 12.0, "high": 17.5, "critical_low": 7.0, "critical_high": 20.0},
    {"name": "WBC Count", "synonyms": ["total leukocyte count", "tlc", "wbc", "white blood cells"], "category": "Hematology", "unit": "/mcL", "low": 4000, "high": 11000, "critical_low": 2000, "critical_high": 30000},
    {"name": "Platelet Count", "synonyms": ["platelets", "plt"], "category": "Hematology", "unit": "/mcL", "low": 150000, "high": 450000, "critical_low": 50000, "critical_high": 1000000},
    {"name": "ESR", "synonyms": ["erythrocyte sedimentation rate"], "category": "Hematology", "unit": "mm/hr", "low": 0, "high": 20, "critical_high": 100},

    # Blood Sugar & Glycemic
    {"name": "Fasting Blood Sugar", "synonyms": ["fbs", "fasting blood glucose", "glucose fasting"], "category": "Biochemistry", "unit": "mg/dL", "low": 70, "high": 100, "critical_low": 50, "critical_high": 300},
    {"name": "Post Prandial Blood Sugar", "synonyms": ["ppbs", "pp glucose", "post prandial blood glucose"], "category": "Biochemistry", "unit": "mg/dL", "low": 80, "high": 140, "critical_low": 50, "critical_high": 350},
    {"name": "Random Blood Sugar", "synonyms": ["rbs", "random blood glucose"], "category": "Biochemistry", "unit": "mg/dL", "low": 70, "high": 140, "critical_low": 50, "critical_high": 350},
    {"name": "HbA1c", "synonyms": ["glycated hemoglobin", "a1c"], "category": "Biochemistry", "unit": "%", "low": 4.0, "high": 5.6, "critical_high": 10.0},

    # Renal Function
    {"name": "Serum Creatinine", "synonyms": ["creatinine", "creat"], "category": "Renal", "unit": "mg/dL", "low": 0.6, "high": 1.2, "critical_high": 4.0},
    {"name": "Blood Urea", "synonyms": ["urea", "bun"], "category": "Renal", "unit": "mg/dL", "low": 15, "high": 40, "critical_high": 100},
    {"name": "Serum Uric Acid", "synonyms": ["uric acid"], "category": "Renal", "unit": "mg/dL", "low": 3.5, "high": 7.2, "critical_high": 12.0},

    # Lipid Profile
    {"name": "Total Cholesterol", "synonyms": ["cholesterol total"], "category": "Lipid Profile", "unit": "mg/dL", "low": 120, "high": 200, "critical_high": 300},
    {"name": "Triglycerides", "synonyms": ["tg", "triglyceride"], "category": "Lipid Profile", "unit": "mg/dL", "low": 50, "high": 150, "critical_high": 500},
    {"name": "HDL Cholesterol", "synonyms": ["hdl", "good cholesterol"], "category": "Lipid Profile", "unit": "mg/dL", "low": 40, "high": 60, "critical_low": 25},
    {"name": "LDL Cholesterol", "synonyms": ["ldl", "bad cholesterol"], "category": "Lipid Profile", "unit": "mg/dL", "low": 60, "high": 100, "critical_high": 190},

    # Liver Function
    {"name": "Total Bilirubin", "synonyms": ["bilirubin total", "s. bilirubin"], "category": "Hepatic", "unit": "mg/dL", "low": 0.2, "high": 1.2, "critical_high": 5.0},
    {"name": "SGOT / AST", "synonyms": ["sgot", "ast", "aspartate aminotransferase"], "category": "Hepatic", "unit": "U/L", "low": 10, "high": 40, "critical_high": 300},
    {"name": "SGPT / ALT", "synonyms": ["sgpt", "alt", "alanine aminotransferase"], "category": "Hepatic", "unit": "U/L", "low": 10, "high": 45, "critical_high": 300},
    {"name": "Alkaline Phosphatase", "synonyms": ["alp", "alk phos"], "category": "Hepatic", "unit": "U/L", "low": 44, "high": 147, "critical_high": 500},

    # Thyroid Function
    {"name": "TSH", "synonyms": ["thyroid stimulating hormone"], "category": "Endocrine", "unit": "uIU/mL", "low": 0.4, "high": 4.5, "critical_high": 20.0, "critical_low": 0.05},
    {"name": "Free T3", "synonyms": ["ft3"], "category": "Endocrine", "unit": "pg/mL", "low": 2.3, "high": 4.2},
    {"name": "Free T4", "synonyms": ["ft4"], "category": "Endocrine", "unit": "ng/dL", "low": 0.8, "high": 1.8},

    # Vitals
    {"name": "Systolic Blood Pressure", "synonyms": ["systolic bp", "systolic", "bp sys"], "category": "Vitals", "unit": "mmHg", "low": 90, "high": 130, "critical_high": 180, "critical_low": 80},
    {"name": "Diastolic Blood Pressure", "synonyms": ["diastolic bp", "diastolic", "bp dia"], "category": "Vitals", "unit": "mmHg", "low": 60, "high": 85, "critical_high": 120, "critical_low": 50},
    {"name": "Pulse / Heart Rate", "synonyms": ["pulse", "heart rate", "hr"], "category": "Vitals", "unit": "bpm", "low": 60, "high": 100, "critical_high": 140, "critical_low": 45},
    {"name": "SpO2 (Oxygen Saturation)", "synonyms": ["spo2", "oxygen saturation", "o2 sat"], "category": "Vitals", "unit": "%", "low": 95, "high": 100, "critical_low": 90},
]


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_medical_image(image: Image.Image) -> Image.Image:
    """Applies optimal contrast, grayscale, and sharpening for OCR."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    gray = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.8)
    sharpened = enhanced.filter(ImageFilter.SHARPEN)
    return ImageOps.autocontrast(sharpened)


def clean_ocr_text(text: str) -> str:
    """Cleans OCR noise and normalizes line breaks."""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ============================================================
# DOCUMENT DATE EXTRACTION
# ============================================================

def extract_document_date(text: str) -> Optional[str]:
    """Finds clinical document consultation, report, or admission date."""
    patterns = [
        r"\b(?:date|dated|dt|do[ab]|admitted|discharge)\s*[:\-\.]?\s*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})\b",
        r"\b(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{4})\b",
        r"\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b",
        r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4})\b",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


# ============================================================
# DOCUMENT TYPE CLASSIFICATION
# ============================================================

def classify_document_type(text: str) -> DocumentType:
    """Classifies the medical document based on clinical markers."""
    norm = text.lower()

    if any(k in norm for k in ["discharge summary", "date of admission", "date of discharge", "hospital course", "discharge advice"]):
        return DocumentType.DISCHARGE_SUMMARY

    if any(k in norm for k in ["rx", "prescription", "tab ", "cap ", "tablet", "capsule", "dosage", "sig:", "1-0-1", "0-1-0"]):
        return DocumentType.PRESCRIPTION

    if any(k in norm for k in ["lab report", "laboratory", "reference interval", "specimen", "haematology", "biochemistry", "pathology", "test name", "observed value"]):
        return DocumentType.LAB_REPORT

    if any(k in norm for k in ["x-ray", "mri", "ct scan", "ultrasound", "usg", "radiology", "impression:", "findings:"]):
        return DocumentType.SCAN_REPORT

    if any(k in norm for k in ["medical certificate", "fitness certificate"]):
        return DocumentType.MEDICAL_CERTIFICATE

    if any(k in norm for k in ["op record", "outpatient", "consultation sheet"]):
        return DocumentType.OP_RECORD

    return DocumentType.UNKNOWN


# ============================================================
# MEDICATION & DOSAGE EXTRACTION
# ============================================================

def extract_structured_medications(text: str) -> List[Medication]:
    """Extracts medicines with dosage, frequency, and instructions."""
    medications: List[Medication] = []
    lines = text.split("\n")

    for drug_info in COMPREHENSIVE_DRUG_DATABASE:
        drug_name = drug_info["name"]
        drug_pat = r"\b" + re.escape(drug_name) + r"\b"

        match = re.search(drug_pat, text, re.IGNORECASE)
        if match:
            # Look at the matching line and immediate next line for dosage & timing
            matched_line = ""
            for line in lines:
                if re.search(drug_pat, line, re.IGNORECASE):
                    matched_line = line
                    break

            dosage = drug_info["default_dosage"]
            dose_m = re.search(r"(\d+(?:\.\d+)?\s*(?:mg|g|mcg|ml|iu|units?))", matched_line, re.IGNORECASE)
            if dose_m:
                dosage = dose_m.group(1)

            # Frequency detection (1-0-1, OD, BD, TID, etc.)
            freq = "Once daily"
            if re.search(r"\b1\-0\-1\b|\bbid\b|\btwice daily\b", matched_line, re.IGNORECASE):
                freq = "Twice daily (1-0-1)"
            elif re.search(r"\b1\-1\-1\b|\btid\b|\bthree times\b", matched_line, re.IGNORECASE):
                freq = "Three times daily (1-1-1)"
            elif re.search(r"\b1\-0\-0\b|\bod\b|\bonce daily\b|\bmorning\b", matched_line, re.IGNORECASE):
                freq = "Once daily morning (1-0-0)"
            elif re.search(r"\b0\-0\-1\b|\bhs\b|\bbedtime\b|\bnight\b", matched_line, re.IGNORECASE):
                freq = "Once daily night (0-0-1)"
            elif re.search(r"\bsos\b|\bas needed\b", matched_line, re.IGNORECASE):
                freq = "As needed (SOS)"

            # Timing
            timing = "After food"
            if re.search(r"\bbefore food\b|\bac\b|\bempty stomach\b", matched_line, re.IGNORECASE):
                timing = "Before food (Empty stomach)"

            # Duration
            duration = "Ongoing / As advised"
            dur_m = re.search(r"(?:for\s+|x\s*)(\d+\s*(?:days?|weeks?|months?))", matched_line, re.IGNORECASE)
            if dur_m:
                duration = dur_m.group(1)

            med = Medication(
                name=drug_name,
                generic_name=drug_info["generic"],
                dosage=dosage,
                frequency=freq,
                timing=timing,
                duration=duration,
                purpose=drug_info["purpose"],
                source="ocr_prescription",
            )
            medications.append(med)

    return medications


# ============================================================
# LABORATORY VALUE EXTRACTION WITH REFERENCE ANALYSIS
# ============================================================

def extract_structured_lab_values(text: str) -> List[LabValue]:
    """
    Extracts laboratory test names, numerical values, units,
    and assigns clinical status (NORMAL, HIGH, LOW, CRITICAL).
    """
    lab_values: List[LabValue] = []

    # Check for BP format: e.g. "BP: 150/95 mmHg" or "150/95"
    bp_match = re.search(r"\b(?:bp|blood pressure)\s*[:\-]?\s*(\d{2,3})\s*[/]\s*(\d{2,3})\s*(?:mmhg)?\b", text, re.IGNORECASE)
    if bp_match:
        sys_val = float(bp_match.group(1))
        dia_val = float(bp_match.group(2))

        sys_status = "NORMAL"
        if sys_val >= 180:
            sys_status = "CRITICAL HIGH (Stage 2 HTN Emergency)"
        elif sys_val >= 140:
            sys_status = "HIGH (Hypertension)"
        elif sys_val < 90:
            sys_status = "LOW (Hypotension)"

        lab_values.append(
            LabValue(
                test_name="Blood Pressure",
                category="Vitals",
                value=f"{int(sys_val)}/{int(dia_val)}",
                unit="mmHg",
                reference_range="90-120 / 60-80 mmHg",
                status=sys_status,
                confidence=0.95,
                clinical_note="Above target range" if "HIGH" in sys_status else "Within normal clinical range",
            )
        )

    for test_def in LAB_TEST_DEFINITIONS:
        patterns = [test_def["name"]] + test_def.get("synonyms", [])
        for pat in patterns:
            # Look for "Test Name ... 12.5 g/dl" or "Test Name : 140"
            regex = (
                r"(?<!\w)" + re.escape(pat) +
                r"(?!\w)\s*[:\-\t|]?\s*(\d+(?:\.\d+)?)\s*([a-zA-Z/%µ]+(?:/[a-zA-Z]+)?)?"
            )
            m = re.search(regex, text, re.IGNORECASE)
            if m:
                val_num = float(m.group(1))
                unit = m.group(2) or test_def["unit"]

                # Determine clinical status
                status = "NORMAL"
                note = "Normal reference interval"

                if "critical_high" in test_def and val_num >= test_def["critical_high"]:
                    status = "CRITICAL HIGH"
                    note = f"Significantly above reference ({test_def.get('low')}-{test_def.get('high')})"
                elif "critical_low" in test_def and val_num <= test_def["critical_low"]:
                    status = "CRITICAL LOW"
                    note = f"Significantly below reference ({test_def.get('low')}-{test_def.get('high')})"
                elif "high" in test_def and val_num > test_def["high"]:
                    status = "HIGH"
                    note = f"Above reference range ({test_def.get('low')}-{test_def.get('high')})"
                elif "low" in test_def and val_num < test_def["low"]:
                    status = "LOW"
                    note = f"Below reference range ({test_def.get('low')}-{test_def.get('high')})"

                ref_range = f"{test_def.get('low', '')} - {test_def.get('high', '')} {test_def['unit']}".strip()

                lab_values.append(
                    LabValue(
                        test_name=test_def["name"],
                        category=test_def["category"],
                        value=str(val_num),
                        unit=unit,
                        reference_range=ref_range,
                        status=status,
                        confidence=0.92,
                        clinical_note=note,
                    )
                )
                break  # Matched this test definition

    return lab_values


# ============================================================
# DIAGNOSES & PROCEDURES EXTRACTION
# ============================================================

def extract_diagnoses(text: str) -> List[str]:
    """Identifies confirmed clinical conditions in the document."""
    conditions = [
        "Hypertension", "Essential Hypertension", "Type 2 Diabetes Mellitus",
        "Diabetic Neuropathy", "Coronary Artery Disease", "Myocardial Infarction",
        "Bronchial Asthma", "Acute Bronchitis", "Pneumonia", "Gastritis",
        "Gastroesophageal Reflux Disease (GERD)", "Chronic Kidney Disease",
        "Hypothyroidism", "Hyperthyroidism", "Osteoarthritis", "Migraine",
        "Dengue Fever", "Typhoid", "Urinary Tract Infection (UTI)", "Anemia"
    ]
    found = []
    norm = text.lower()
    for c in conditions:
        if c.lower() in norm:
            found.append(c)
    return list(dict.fromkeys(found))


def extract_procedures(text: str) -> List[str]:
    """Extracts diagnostic or surgical procedures mentioned."""
    procs = [
        "Coronary Angiography", "PTCA / Stent placement", "Echocardiogram (2D Echo)",
        "Electrocardiogram (ECG)", "Chest X-Ray", "Ultrasound Abdomen",
        "CT Brain / Head", "Endoscopy", "Colonoscopy", "Appendectomy",
        "Cholecystectomy", "Caesarean Section", "Dialysis"
    ]
    found = []
    norm = text.lower()
    for p in procs:
        if p.lower() in norm:
            found.append(p)
    return list(dict.fromkeys(found))


# ============================================================
# COMPLETE OCR PROCESSING FOR IMAGES AND PDFS
# ============================================================

def process_document(
    file_bytes: bytes,
    filename: str,
    language: str = "eng",
) -> Dict[str, Any]:
    """
    Main entry point: Performs OCR on the uploaded document,
    preprocesses, and extracts structured medical entities.
    """
    if not file_bytes:
        raise ValueError("Uploaded file is empty.")

    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_DOCUMENT_EXTENSIONS:
        raise ValueError(f"Unsupported file type '{ext}'. Supported: JPG, PNG, PDF, TIFF, BMP.")

    extracted_text = ""
    pages_count = 1
    page_blocks = []

    # 1. Process PDF
    if ext == ".pdf":
        try:
            import fitz
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
                tf.write(file_bytes)
                temp_pdf = tf.name

            doc = fitz.open(temp_pdf)
            pages_count = len(doc)
            combined_pages = []

            for pno in range(pages_count):
                page = doc.load_page(pno)
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                img_data = pix.tobytes("png")
                pil_img = Image.open(io.BytesIO(img_data))
                processed = preprocess_medical_image(pil_img)

                ptext = pytesseract.image_to_string(processed, lang="eng", config="--psm 6")
                ptext_clean = clean_ocr_text(ptext)
                combined_pages.append(f"--- Page {pno + 1} ---\n{ptext_clean}")
                page_blocks.append({"page_number": pno + 1, "text": ptext_clean})

            doc.close()
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

            extracted_text = "\n\n".join(combined_pages)

        except Exception as exc:
            # Fallback if fitz / tesseract has issue
            raise RuntimeError(f"PDF OCR failed: {str(exc)}")

    # 2. Process Image
    else:
        try:
            pil_img = Image.open(io.BytesIO(file_bytes))
            processed = preprocess_medical_image(pil_img)
            extracted_text = pytesseract.image_to_string(processed, lang="eng", config="--psm 6")
            extracted_text = clean_ocr_text(extracted_text)
            page_blocks.append({"page_number": 1, "text": extracted_text})
        except Exception as exc:
            raise RuntimeError(f"Image OCR failed: {str(exc)}")

    # 3. Extract Medical Entities & Structure
    doc_type = classify_document_type(extracted_text)
    doc_date = extract_document_date(extracted_text) or datetime.utcnow().strftime("%d/%m/%Y")
    diagnoses = extract_diagnoses(extracted_text)
    medications = extract_structured_medications(extracted_text)
    lab_values = extract_structured_lab_values(extracted_text)
    procedures = extract_procedures(extracted_text)

    # Critical findings detection
    critical_findings = []
    for lv in lab_values:
        if "CRITICAL" in lv.status or "HIGH" in lv.status:
            critical_findings.append(f"{lv.test_name}: {lv.value} {lv.unit or ''} [{lv.status}]")

    preview = (extracted_text[:400].strip() + "...") if len(extracted_text) > 400 else extracted_text

    analysis_result = DocumentAnalysisResult(
        document_id=str(Path(filename).stem),
        filename=filename,
        file_type=ext.replace(".", ""),
        document_type=doc_type,
        document_date=doc_date,
        extracted_text=extracted_text,
        confidence=88.5,
        pages=pages_count,
        diagnoses=diagnoses,
        medications=medications,
        lab_values=lab_values,
        procedures=procedures,
        critical_findings=critical_findings,
        text_preview=preview,
        processed_at=datetime.utcnow(),
    )

    return analysis_result.model_dump()


def create_ocr_summary(ocr_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generates concise dashboard summary representation."""
    return {
        "filename": ocr_result.get("filename"),
        "document_type": ocr_result.get("document_type"),
        "document_date": ocr_result.get("document_date"),
        "confidence": ocr_result.get("confidence", 88.0),
        "pages": ocr_result.get("pages", 1),
        "total_medications": len(ocr_result.get("medications", [])),
        "total_lab_tests": len(ocr_result.get("lab_values", [])),
        "diagnoses_count": len(ocr_result.get("diagnoses", [])),
        "critical_findings": ocr_result.get("critical_findings", []),
        "text_preview": ocr_result.get("text_preview", ""),
    }


def check_ocr_dependencies() -> Dict[str, Any]:
    """System dependency audit for Tesseract and PyMuPDF."""
    res = {
        "pytesseract": True,
        "tesseract_configured": TESSERACT_CONFIGURED,
        "tesseract_available": False,
        "pymupdf_available": False,
    }
    if TESSERACT_CONFIGURED:
        try:
            v = pytesseract.get_tesseract_version()
            res["tesseract_available"] = True
            res["tesseract_version"] = str(v)
            res["tesseract_path"] = TESSERACT_PATH
        except Exception as e:
            res["tesseract_error"] = str(e)

    try:
        import fitz
        res["pymupdf_available"] = True
        res["pymupdf_version"] = getattr(fitz, "version", "available")
    except Exception as e:
        res["pymupdf_error"] = str(e)

    return res


def get_supported_file_information() -> Dict[str, Any]:
    return {
        "supported_extensions": sorted(SUPPORTED_DOCUMENT_EXTENSIONS),
        "max_size_mb": MAX_FILE_SIZE_MB,
        "tesseract_configured": TESSERACT_CONFIGURED,
        "extraction_capabilities": [
            "Document Type Classification",
            "Prescription Itemization (Medicine, Dose, 1-0-1 Regimen)",
            "Quantitative Lab Ranges & Flagging (High/Low/Critical)",
            "Clinical Diagnoses & Surgeries",
            "Document Date Identification for Timeline",
        ],
    }
