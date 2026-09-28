"""
MediKiosk AI Service - ABDM / HL7 FHIR R4 Interoperability Service
==================================================================

Purpose:
    Transform MediKiosk AI clinical intake summaries, OCR extractions,
    and patient assessments into standard HL7 FHIR R4 JSON Bundles
    ready for ABDM (Ayushman Bharat Digital Mission) and EHR integration.

Standards Compliance:
    - HL7 FHIR Release 4 (R4)
    - NRCES (National Resource Centre for EHR Standards) India Profiles
    - ABDM Health Information Provider (HIP) Data Formats
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.models.schemas import ClinicalSummary


def generate_fhir_bundle(
    summary: ClinicalSummary,
    abha_id: Optional[str] = "91-XXXX-XXXX-XXXX",
) -> Dict[str, Any]:
    """
    Generates a valid HL7 FHIR R4 Document Bundle from a MediKiosk ClinicalSummary.
    """
    bundle_id = str(uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    patient_id = summary.patient.patient_id if summary.patient else str(uuid4())[:8]
    patient_name = summary.patient.name if summary.patient else "Patient"

    entries = []

    # 1. Composition Resource (Document Header)
    comp_id = f"comp-{uuid4()}"
    entries.append({
        "fullUrl": f"urn:uuid:{comp_id}",
        "resource": {
            "resourceType": "Composition",
            "id": comp_id,
            "status": "final",
            "type": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "34117-2",
                    "display": "History and Physical Examination Document"
                }],
                "text": "MediKiosk Clinical Intake Summary"
            },
            "subject": {
                "reference": f"urn:uuid:pat-{patient_id}",
                "display": patient_name
            },
            "date": timestamp,
            "author": [{
                "display": "MediKiosk AI Clinical Intake Kiosk"
            }],
            "title": "Clinical History and Triage Intake Report",
            "section": [
                {
                    "title": "Chief Complaint & History of Present Illness",
                    "code": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": "10154-3",
                            "display": "Chief Complaint & HPI"
                        }]
                    },
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><strong>Chief Complaint:</strong> {summary.chief_complaint}</p><p>{summary.hpi.narrative}</p></div>"
                    }
                },
                {
                    "title": "Medications",
                    "code": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": "10160-0",
                            "display": "History of Medication Use"
                        }]
                    },
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>{', '.join(m.name for m in summary.current_medications) if summary.current_medications else 'None'}</p></div>"
                    }
                }
            ]
        }
    })

    # 2. Patient Resource
    pat_id = f"pat-{patient_id}"
    entries.append({
        "fullUrl": f"urn:uuid:{pat_id}",
        "resource": {
            "resourceType": "Patient",
            "id": pat_id,
            "identifier": [
                {
                    "system": "https://healthid.ndhm.gov.in",
                    "value": summary.patient.abha_id if summary.patient and summary.patient.abha_id else abha_id,
                    "type": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR",
                            "display": "Medical Record Number / ABHA"
                        }]
                    }
                }
            ],
            "name": [{
                "text": patient_name,
                "family": patient_name.split()[-1] if len(patient_name.split()) > 1 else patient_name
            }],
            "gender": summary.patient.gender.value if summary.patient and summary.patient.gender else "unknown",
        }
    })

    # 3. Condition Resources (Chief Complaint & Diagnoses)
    cond_id = f"cond-{uuid4()}"
    entries.append({
        "fullUrl": f"urn:uuid:{cond_id}",
        "resource": {
            "resourceType": "Condition",
            "id": cond_id,
            "clinicalStatus": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active"
                }]
            },
            "code": {
                "text": summary.chief_complaint
            },
            "subject": {
                "reference": f"urn:uuid:{pat_id}"
            },
            "recordedDate": timestamp,
        }
    })

    # 4. MedicationStatement Resources
    for med in summary.current_medications:
        med_id = f"med-{uuid4()}"
        entries.append({
            "fullUrl": f"urn:uuid:{med_id}",
            "resource": {
                "resourceType": "MedicationStatement",
                "id": med_id,
                "status": "active",
                "medicationCodeableConcept": {
                    "text": f"{med.name} {med.dosage or ''}".strip()
                },
                "subject": {
                    "reference": f"urn:uuid:{pat_id}"
                },
                "dosage": [{
                    "text": f"{med.frequency or 'Daily'} {med.timing or ''}".strip()
                }]
            }
        })

    # 5. Observation Resources (Laboratory and Vital Findings)
    for lab in summary.investigations_summary:
        obs_id = f"obs-{uuid4()}"
        entries.append({
            "fullUrl": f"urn:uuid:{obs_id}",
            "resource": {
                "resourceType": "Observation",
                "id": obs_id,
                "status": "final",
                "code": {
                    "text": lab.test_name
                },
                "subject": {
                    "reference": f"urn:uuid:{pat_id}"
                },
                "valueString": f"{lab.value} {lab.unit or ''}".strip(),
                "interpretation": [{
                    "text": lab.status
                }],
                "referenceRange": [{
                    "text": lab.reference_range or "Standard biological interval"
                }]
            }
        })

    # 6. AllergyIntolerance Resource
    for allergy in summary.drug_allergies:
        allergy_id = f"all-{uuid4()}"
        is_nkda = "no known" in allergy.lower() or "nkda" in allergy.lower()
        entries.append({
            "fullUrl": f"urn:uuid:{allergy_id}",
            "resource": {
                "resourceType": "AllergyIntolerance",
                "id": allergy_id,
                "clinicalStatus": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                        "code": "active"
                    }]
                },
                "code": {
                    "text": "No Known Drug Allergies" if is_nkda else allergy
                },
                "subject": {
                    "reference": f"urn:uuid:{pat_id}"
                }
            }
        })

    return {
        "resourceType": "Bundle",
        "id": bundle_id,
        "type": "document",
        "timestamp": timestamp,
        "total": len(entries),
        "entry": entries,
        "meta": {
            "profile": [
                "https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"
            ]
        }
    }
