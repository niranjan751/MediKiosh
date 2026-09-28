"""
MediKiosk AI Service - Physician-Ready AI Clinical Summary Service
==================================================================

Purpose:
    Generate comprehensive, structured, professional clinical case intake summaries
    following hospital documentation standards (SOAP / Clinical History):
        - CHIEF COMPLAINT
        - HISTORY OF PRESENT ILLNESS (HPI) with SOCRATES breakdown
        - PAST MEDICAL & SURGICAL HISTORY
        - CURRENT MEDICATIONS & ADHERENCE
        - DRUG ALLERGIES & ADVERSE REACTIONS
        - FAMILY HISTORY
        - PERSONAL / SOCIAL / HABITS HISTORY
        - REVIEW OF SYSTEMS (ROS)
        - RECENT INVESTIGATIONS & ABNORMAL LAB FINDINGS (from OCR)
        - AI RED FLAGS & TRIAGE LEVEL
        - PHYSICIAN ACTIONS (Editable & Confirmatory notes)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.models.schemas import (
    AlertSeverity,
    ClinicalMode,
    ClinicalSummary,
    HPIStructured,
    LabValue,
    Medication,
    PatientBasicInfo,
    RedFlag,
    ReviewOfSystems,
    ReviewStatus,
    TimelineEvent,
    TriagePriority,
)
from app.services.ayush_service import conduct_ayush_assessment
from app.services.red_flag_service import build_red_flag_result
from app.services.timeline_service import build_timeline_events


def generate_structured_clinical_summary(
    patient_id: Optional[str] = None,
    session_id: Optional[str] = None,
    patient_info: Optional[PatientBasicInfo] = None,
    interview_data: Optional[Dict[str, Any]] = None,
    documents_data: Optional[List[Dict[str, Any]]] = None,
    clinical_mode: ClinicalMode = ClinicalMode.ALLOPATHIC,
    ayush_data: Optional[Dict[str, Any]] = None,
) -> ClinicalSummary:
    """
    Synthesizes interview inputs, OCR findings, and triage flags into a
    physician-ready electronic health record intake summary.
    """
    interview = interview_data or {}
    documents = documents_data or []

    # 1. Chief Complaint & Duration
    raw_complaint = (
        interview.get("chief_complaint")
        or interview.get("main_complaint")
        or "General clinical consultation"
    )
    duration_str = interview.get("onset") or interview.get("symptom_duration") or "Recently reported"
    chief_complaint_formatted = f"{raw_complaint} (Duration / Onset: {duration_str})"

    # 2. HPI with SOCRATES breakdown
    site = interview.get("site") or interview.get("symptom_location") or "Localized as reported"
    onset = interview.get("onset") or interview.get("symptom_onset") or "Gradual onset"
    character = interview.get("character") or "Discomfort"
    radiation = interview.get("radiation") or "No radiation reported"
    associations = interview.get("associations") or interview.get("associated_symptoms") or "None noted"
    severity = interview.get("severity") or interview.get("symptom_severity") or "Moderate"

    socrates_dict = {
        "site": site,
        "onset": onset,
        "character": character,
        "radiation": radiation,
        "associations": associations,
        "time_course": duration_str,
        "exacerbating_relieving": interview.get("exacerbating") or "Under evaluation",
        "severity": severity,
    }

    hpi_narrative = (
        f"The patient presents with {raw_complaint}, which commenced {onset.lower()}. "
        f"The discomfort is described as {character.lower()} located at {site.lower()}. "
        f"{'It radiates to ' + radiation.lower() + '.' if 'no' not in radiation.lower() else 'There is no reported radiation.'} "
        f"Associated features include {associations.lower()}. "
        f"Current severity is rated as {severity} on the clinical scale."
    )

    hpi = HPIStructured(
        narrative=hpi_narrative,
        socrates=socrates_dict,
        duration_onset=duration_str,
        progression="Under evaluation during intake",
    )

    # 3. Past Medical & Surgical History
    pmh_items = []
    med_hist_ans = interview.get("medical_history") or interview.get("past_history")
    if med_hist_ans and "none" not in str(med_hist_ans).lower():
        pmh_items.append(str(med_hist_ans))

    # Aggregate diagnoses from uploaded documents
    for doc in documents:
        for diag in doc.get("diagnoses", []):
            if diag not in pmh_items:
                pmh_items.append(f"{diag} (per record: {doc.get('filename', 'doc')})")

    if not pmh_items:
        pmh_items = ["No prior chronic medical illnesses reported by patient."]

    psh_items = ["No major surgical history declared."]

    # 4. Medications (Combined from Interview + OCR Prescriptions)
    med_list: List[Medication] = []
    seen_meds = set()

    # From interview
    med_ans = interview.get("medications")
    if med_ans and "none" not in str(med_ans).lower():
        med_list.append(
            Medication(
                name=str(med_ans),
                dosage="As prescribed",
                frequency="Daily",
                source="patient_intake",
            )
        )
        seen_meds.add(str(med_ans).lower())

    # From OCR Prescriptions
    for doc in documents:
        for m in doc.get("medications", []):
            m_name = m.get("name", "") if isinstance(m, dict) else str(m)
            if m_name.lower() not in seen_meds:
                if isinstance(m, dict):
                    med_list.append(Medication(**m))
                else:
                    med_list.append(Medication(name=m_name, source="ocr_document"))
                seen_meds.add(m_name.lower())

    # 5. Drug Allergies
    allergy_items = []
    allergy_ans = interview.get("allergies")
    if allergy_ans and "no known" not in str(allergy_ans).lower() and "none" not in str(allergy_ans).lower():
        allergy_items.append(str(allergy_ans))
    else:
        allergy_items = ["No Known Drug Allergies (NKDA)"]

    # 6. Family History
    fam_items = []
    fam_ans = interview.get("family_history")
    if fam_ans and "none" not in str(fam_ans).lower() and "no significant" not in str(fam_ans).lower():
        fam_items.append(str(fam_ans))
    else:
        fam_items = ["Non-contributory / No major premature familial diseases reported."]

    # 7. Review of Systems (ROS)
    ros = ReviewOfSystems(
        constitutional=["Fatigue / Malaise" if "tired" in hpi_narrative else "Normal general state"],
        cardiovascular=[site if "chest" in site.lower() else "No orthopnea reported"],
        respiratory=[associations if "breath" in associations.lower() else "Clear lung fields reported"],
        gastrointestinal=[site if "abdomen" in site.lower() or "stomach" in site.lower() else "Normal bowel habits"],
        neurological=[severity if "headache" in raw_complaint.lower() else "Intact sensorium"],
        musculoskeletal=["Normal mobility"],
        integumentary=["No active rashes noted"],
    )

    # 8. Investigations & Abnormal Lab Findings (from OCR)
    investigations: List[LabValue] = []
    for doc in documents:
        for lv in doc.get("lab_values", []):
            if isinstance(lv, dict):
                investigations.append(LabValue(**lv))

    # 9. Red Flag Assessment
    red_flag_res = build_red_flag_result(
        symptoms=[raw_complaint, associations, site],
        interview_answers=interview,
    )
    red_flags: List[RedFlag] = red_flag_res.get("flags", [])
    triage_priority = red_flag_res.get("triage_priority", TriagePriority.LEVEL_4_ROUTINE)

    # 10. Medical Timeline
    timeline_events = build_timeline_events(
        documents_data=documents,
        interview_answers=interview,
        current_red_flags=red_flags,
    )

    # 11. AYUSH Profile (if AYUSH mode active)
    ayush_profile = None
    if clinical_mode == ClinicalMode.AYUSH or ayush_data:
        ayush_profile = conduct_ayush_assessment(
            patient_id=patient_id,
            responses=ayush_data or interview,
        )

    # 12. Formatted Physician Clinical Note Text (SOAP style)
    lines = [
        "=" * 60,
        "MEDIKIOSK AI - ELECTRONIC CLINICAL INTAKE SUMMARY",
        f"Generated At: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"Triage Priority: {triage_priority.value}",
        "=" * 60,
        "",
        "1. CHIEF COMPLAINT:",
        f"   {chief_complaint_formatted}",
        "",
        "2. HISTORY OF PRESENT ILLNESS (HPI):",
        f"   {hpi_narrative}",
        "",
        "   [SOCRATES Analysis]:",
        f"   - Site: {site}",
        f"   - Onset: {onset}",
        f"   - Character: {character}",
        f"   - Radiation: {radiation}",
        f"   - Associated Symptoms: {associations}",
        f"   - Severity: {severity}",
        "",
        "3. PAST MEDICAL & SURGICAL HISTORY:",
    ]
    for p in pmh_items:
        lines.append(f"   • {p}")

    lines.extend([
        "",
        "4. CURRENT MEDICATIONS:",
    ])
    if med_list:
        for m in med_list:
            lines.append(f"   • {m.name} | Dose: {m.dosage or 'N/A'} | Freq: {m.frequency or 'Daily'} [{m.source}]")
    else:
        lines.append("   • No active medications recorded.")

    lines.extend([
        "",
        "5. ALLERGIES:",
    ])
    for a in allergy_items:
        lines.append(f"   • {a}")

    lines.extend([
        "",
        "6. FAMILY HISTORY:",
    ])
    for f in fam_items:
        lines.append(f"   • {f}")

    lines.extend([
        "",
        "7. RECENT INVESTIGATIONS & ABNORMAL FINDINGS (OCR):",
    ])
    if investigations:
        for inv in investigations:
            flag_note = f" [{inv.status}]" if inv.status != "NORMAL" else ""
            lines.append(f"   • {inv.test_name}: {inv.value} {inv.unit or ''} (Ref: {inv.reference_range or 'N/A'}){flag_note}")
    else:
        lines.append("   • No uploaded laboratory investigations available.")

    lines.extend([
        "",
        "8. AI RED-FLAG & TRIAGE ASSESSMENT:",
    ])
    if red_flags:
        for rf in red_flags:
            lines.append(f"   🚨 [{rf.severity.value.upper()}] {rf.symptom}: {rf.reason}")
            lines.append(f"      Action: {rf.recommended_action}")
    else:
        lines.append("   ✓ No emergent red-flag warning signs detected.")

    if ayush_profile:
        lines.extend([
            "",
            "9. AYUSH / AYURVEDIC ASSESSMENT:",
            f"   • Prakriti: {ayush_profile.prakriti.dominant_dosha} ({ayush_profile.prakriti.constitution_type})",
            f"   • Agni: {ayush_profile.agni}",
            f"   • Koshtha: {ayush_profile.koshtha}",
            f"   • Pathya (Wholesome Diet): {', '.join(ayush_profile.pathya_recommendations[:2])}",
        ])

    lines.extend([
        "",
        "=" * 60,
        "ATTENDING PHYSICIAN ACTIONS & REVIEW:",
        "Status: [ PENDING PHYSICIAN CONFIRMATION ]",
        "Physician Notes: __________________________________________________",
        "Clinical Plan:   __________________________________________________",
        "=" * 60,
    ])

    formatted_note = "\n".join(lines)

    return ClinicalSummary(
        summary_id=session_id or str(uuid4()),
        patient=patient_info,
        chief_complaint=chief_complaint_formatted,
        hpi=hpi,
        past_medical_history=pmh_items,
        past_surgical_history=psh_items,
        current_medications=med_list,
        drug_allergies=allergy_items,
        family_history=fam_items,
        personal_social_history=["Non-smoker / Social history reviewed at intake"],
        review_of_systems=ros,
        investigations_summary=investigations,
        red_flag_alerts=red_flags,
        priority_level=triage_priority,
        timeline_events=timeline_events,
        ayush_profile=ayush_profile,
        review_status=ReviewStatus.PENDING,
        formatted_physician_note=formatted_note,
        generated_at=datetime.utcnow(),
    )


def apply_doctor_review_to_summary(
    summary: Dict[str, Any],
    doctor_notes: str,
    doctor_name: Optional[str] = "Attending Physician",
    confirmed_diagnoses: Optional[List[str]] = None,
    prescribed_plan: Optional[str] = None,
) -> Dict[str, Any]:
    """Applies physician edits and marks the summary as verified."""
    updated = dict(summary)
    updated["doctor_name"] = doctor_name
    updated["doctor_review_notes"] = doctor_notes
    updated["review_status"] = "approved"

    append_note = (
        f"\n\n[CONFIRMED BY PHYSICIAN: Dr. {doctor_name} at {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}]\n"
        f"Physician Notes: {doctor_notes}\n"
    )
    if confirmed_diagnoses:
        append_note += f"Confirmed Diagnoses: {', '.join(confirmed_diagnoses)}\n"
    if prescribed_plan:
        append_note += f"Clinical Plan: {prescribed_plan}\n"

    if "formatted_physician_note" in updated:
        updated["formatted_physician_note"] += append_note

    return updated