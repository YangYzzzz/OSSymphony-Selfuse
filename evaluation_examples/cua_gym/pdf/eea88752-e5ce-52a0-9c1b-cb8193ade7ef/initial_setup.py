"""
Initial Setup: Create four separate medical record PDFs for merging task
Task ID: pdf_legal_091
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_091'
MEDICAL_DIR = f'{WORKDIR}/legal/medical'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def add_medical_page(doc, page_num, title, content_lines, header_info):
    """Add a single page of medical record content."""
    page = doc.new_page(width=612, height=792)  # Letter size

    # Header
    page.insert_text(pymupdf.Point(72, 50), header_info["facility"],
                     fontsize=14, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 68), header_info["address"],
                     fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 80), header_info["phone"],
                     fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    # Horizontal line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 90), pymupdf.Point(540, 90))
    shape.finish(color=(0, 0, 0.5), width=1.5)
    shape.commit()

    # Patient info block
    page.insert_text(pymupdf.Point(72, 110), "Patient: Margaret R. Sullivan",
                     fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 124), "DOB: 03/14/1962  |  MRN: 2847193  |  SSN: XXX-XX-4582",
                     fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 138), f"Case No: CV-2025-03841  |  Attorneys: Whitfield & Associates",
                     fontsize=9, fontname="helv", color=(0, 0, 0))

    # Section title
    page.insert_text(pymupdf.Point(72, 168), title,
                     fontsize=12, fontname="hebo", color=(0, 0, 0))

    # Content lines
    y = 190
    for line in content_lines:
        if y > 740:
            break
        if line.startswith("##"):
            page.insert_text(pymupdf.Point(72, y), line[2:].strip(),
                             fontsize=10, fontname="hebo", color=(0, 0, 0))
        else:
            page.insert_text(pymupdf.Point(72, y), line,
                             fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 14

    # Footer
    page.insert_text(pymupdf.Point(72, 760), "CONFIDENTIAL - ATTORNEY WORK PRODUCT",
                     fontsize=7, fontname="heit", color=(0.5, 0, 0))
    page.insert_text(pymupdf.Point(450, 760), f"Page {page_num}",
                     fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


def create_hospital_records():
    """Create 45-page hospital records PDF."""
    doc = pymupdf.open()
    header = {
        "facility": "Riverside General Hospital",
        "address": "1200 Medical Center Drive, Portland, OR 97205",
        "phone": "Tel: (503) 555-7200  |  Fax: (503) 555-7201"
    }

    sections = [
        ("Emergency Department Visit - 08/15/2024", [
            "##Chief Complaint",
            "Patient presented to ED via ambulance following a motor vehicle collision",
            "at the intersection of NW 23rd Ave and Burnside St at approximately 14:32.",
            "Patient was the restrained driver of a sedan struck on the driver's side",
            "by a pickup truck running a red light.",
            "",
            "##Triage Assessment",
            "GCS: 14 (E3V5M6)  |  BP: 158/94  |  HR: 112  |  RR: 22  |  SpO2: 96%",
            "Temp: 98.4F  |  Pain: 8/10",
            "",
            "##History of Present Illness",
            "62-year-old female involved in T-bone MVC. Patient reports she was",
            "proceeding through a green light when struck on the driver's side.",
            "She reports immediate onset of left-sided chest pain, left hip pain,",
            "and headache. No loss of consciousness per EMS. Patient denies",
            "neck pain but reports tingling in left upper extremity.",
            "",
            "##Past Medical History",
            "Hypertension (controlled with lisinopril 20mg daily)",
            "Type 2 Diabetes Mellitus (metformin 1000mg BID, A1c 6.8%)",
            "Osteoarthritis bilateral knees",
            "Hypothyroidism (levothyroxine 75mcg daily)",
            "Appendectomy (1998), Right knee arthroscopy (2019)",
        ]),
        ("Emergency Department - Physical Examination", [
            "##General",
            "Alert, oriented x3, appears in moderate distress, cervical collar in place.",
            "",
            "##HEENT",
            "3cm laceration to left temporal region, actively bleeding.",
            "Pupils equal, round, reactive to light. TMs clear bilaterally.",
            "No Battle's sign. No raccoon eyes. No rhinorrhea or otorrhea.",
            "",
            "##Neck",
            "Cervical collar in place. No midline tenderness to palpation.",
            "No step-off deformity. Trachea midline.",
            "",
            "##Chest/Cardiovascular",
            "Tachycardic, regular rhythm. No murmurs. Left-sided chest wall",
            "tenderness over ribs 5-8 laterally. Decreased breath sounds at",
            "left base. No crepitus. Skin abrasion left lateral chest wall.",
            "",
            "##Abdomen",
            "Soft, non-distended. Mild tenderness LUQ. No rebound or guarding.",
            "Bowel sounds present in all four quadrants.",
            "",
            "##Extremities",
            "Left hip: significant tenderness to palpation over greater trochanter.",
            "Limited ROM due to pain. Distal pulses 2+ bilaterally.",
            "Left wrist: swelling and tenderness over distal radius.",
            "Sensation intact but diminished in left median nerve distribution.",
        ]),
        ("Emergency Department - Diagnostic Studies", [
            "##Laboratory Results (drawn 15:04)",
            "CBC: WBC 11.2, Hgb 12.8, Hct 38.4, Plt 234",
            "BMP: Na 138, K 4.1, Cl 102, CO2 24, BUN 18, Cr 0.9, Glu 142",
            "Troponin I: <0.01 (normal)",
            "Lipase: 45 (normal range 10-140)",
            "Lactate: 2.1 mmol/L",
            "PT/INR: 12.8/1.0  |  PTT: 28.4",
            "Urinalysis: trace blood, otherwise unremarkable",
            "Blood alcohol: <10 mg/dL (negative)",
            "Urine drug screen: negative",
            "",
            "##Imaging Studies",
            "CT Head without contrast: No acute intracranial hemorrhage.",
            "Small left temporal scalp hematoma. No skull fracture.",
            "",
            "CT Cervical Spine: No acute fracture or malalignment.",
            "Mild degenerative changes C5-C6, C6-C7.",
            "",
            "CT Chest/Abdomen/Pelvis with contrast:",
            "- Left rib fractures #6, #7, #8 laterally",
            "- Small left hemothorax (estimated 200mL)",
            "- No pneumothorax",
            "- Grade I splenic laceration with small perisplenic hematoma",
            "- No free intraperitoneal air",
            "- Left acetabular fracture (anterior column)",
            "",
            "Left wrist X-ray: Distal radius fracture, minimally displaced.",
            "No ulnar styloid fracture. Radiocarpal alignment maintained.",
        ]),
    ]

    # Generate 45 pages with varied content
    page_num = 1
    for section_title, content in sections:
        add_medical_page(doc, page_num, section_title, content, header)
        page_num += 1

    # Additional pages for surgical consult, nursing notes, etc.
    additional_sections = [
        "Orthopedic Surgery Consultation - 08/15/2024",
        "Trauma Surgery Consultation - 08/15/2024",
        "Admission Orders - 08/15/2024",
        "Nursing Assessment - 08/15/2024 16:00",
        "Nursing Notes - 08/15/2024 18:00",
        "Nursing Notes - 08/15/2024 22:00",
        "Nursing Notes - 08/16/2024 02:00",
        "Nursing Notes - 08/16/2024 06:00",
        "Physician Progress Note - 08/16/2024",
        "Physical Therapy Evaluation - 08/16/2024",
        "Occupational Therapy Evaluation - 08/16/2024",
        "Nursing Notes - 08/16/2024 14:00",
        "Nursing Notes - 08/16/2024 22:00",
        "Physician Progress Note - 08/17/2024",
        "Physical Therapy Session Note - 08/17/2024",
        "Social Work Consultation - 08/17/2024",
        "Pain Management Consultation - 08/17/2024",
        "Nursing Notes - 08/17/2024 14:00",
        "Physician Progress Note - 08/18/2024",
        "Physical Therapy Session Note - 08/18/2024",
        "Nursing Notes - 08/18/2024 14:00",
        "Physician Progress Note - 08/19/2024",
        "Discharge Planning Note - 08/19/2024",
        "Physical Therapy Session Note - 08/19/2024",
        "Nursing Notes - 08/19/2024 14:00",
        "Physician Progress Note - 08/20/2024",
        "Physical Therapy Discharge Summary - 08/20/2024",
        "Discharge Summary - 08/20/2024",
        "Discharge Instructions - 08/20/2024",
        "Medication Reconciliation - 08/20/2024",
        "Operative Report - Left Wrist ORIF - 08/16/2024",
        "Anesthesia Record - 08/16/2024",
        "Post-Anesthesia Care Unit Note - 08/16/2024",
        "Radiology Report - Post-Op Left Wrist - 08/16/2024",
        "Radiology Report - Follow-up Chest - 08/18/2024",
        "Laboratory Results Summary - Hospital Stay",
        "Blood Bank Records - 08/15/2024",
        "Pharmacy Medication Administration Record",
        "Vital Signs Flowsheet Summary",
        "Intake/Output Summary",
        "Fall Risk Assessment - Daily",
        "DVT Prophylaxis Documentation",
    ]

    med_content_templates = [
        [
            "Assessment and evaluation performed as documented.",
            "Patient continues to show expected progress given mechanism of injury.",
            "Vital signs within acceptable parameters. Pain managed with current regimen.",
            "Patient cooperative with care plan and therapy sessions.",
            "Will continue to monitor for complications including infection,",
            "compartment syndrome, and thromboembolic events.",
            "Discussed plan of care with patient and family.",
            "Questions answered to their satisfaction.",
        ],
        [
            "Reviewed imaging studies and laboratory results.",
            "Fracture alignment remains satisfactory on follow-up imaging.",
            "Hemothorax resolving on serial chest X-rays.",
            "Splenic laceration stable - serial abdominal exams unremarkable.",
            "Patient tolerating oral medications. Diet advanced as tolerated.",
            "Ambulating with assistance of physical therapy team.",
            "Weight-bearing status: left lower extremity toe-touch only.",
            "Left upper extremity immobilized in short arm cast.",
        ],
        [
            "Nursing assessment completed per protocol.",
            "Pain level: 5/10 at rest, 7/10 with movement.",
            "IV fluids: D5 1/2 NS at 75 mL/hr via left antecubital 20G PIV.",
            "Medications administered as ordered - see MAR.",
            "Fall precautions in place. Bed alarm activated.",
            "Patient resting comfortably. Call light within reach.",
            "Respiratory: Incentive spirometry q1h while awake, achieving 1250 mL.",
            "Wound care: surgical site clean, dry, intact. No signs of infection.",
        ],
    ]

    for i, section in enumerate(additional_sections):
        content = med_content_templates[i % len(med_content_templates)]
        add_medical_page(doc, page_num, section, content, header)
        page_num += 1

    output = f'{MEDICAL_DIR}/hospital_records.pdf'
    doc.save(output)
    doc.close()
    print(f'Created: {output} ({page_num - 1} pages)')
    return page_num - 1


def create_primary_care():
    """Create 20-page primary care records PDF."""
    doc = pymupdf.open()
    header = {
        "facility": "Cascade Family Medicine",
        "address": "845 SE Hawthorne Blvd, Suite 200, Portland, OR 97214",
        "phone": "Tel: (503) 555-3100  |  Fax: (503) 555-3101"
    }

    sections = [
        "Annual Physical Examination - 02/12/2024",
        "Office Visit - Hypertension Follow-up - 04/18/2024",
        "Office Visit - Diabetes Management - 06/20/2024",
        "Telephone Encounter - Medication Refill - 07/05/2024",
        "Annual Physical Examination - 02/15/2023",
        "Office Visit - Upper Respiratory Infection - 03/22/2023",
        "Office Visit - Knee Pain Evaluation - 05/10/2023",
        "Office Visit - Hypertension Follow-up - 08/14/2023",
        "Office Visit - Diabetes Follow-up - 10/25/2023",
        "Referral Letter - Orthopedic Surgery - 05/15/2023",
        "Annual Physical Examination - 02/10/2022",
        "Office Visit - New Onset Diabetes - 04/20/2022",
        "Office Visit - Diabetes Education Follow-up - 06/15/2022",
        "Office Visit - Thyroid Follow-up - 09/12/2022",
        "Immunization Record - Updated 06/20/2024",
        "Medication List - Current as of 07/05/2024",
        "Problem List Summary",
        "Allergies and Adverse Reactions",
        "Family History Summary",
        "Preventive Care Screening Log",
    ]

    pcp_content = [
        "Patient seen for scheduled visit. History reviewed and updated.",
        "Medications reconciled. Compliance with current regimen discussed.",
        "Vitals: BP 132/82, HR 76, Wt 168 lbs, BMI 28.4",
        "Physical examination performed - see detailed findings below.",
        "Lab results reviewed and discussed with patient.",
        "Plan of care updated. Follow-up appointment scheduled.",
        "Patient educated on lifestyle modifications including diet and exercise.",
        "Referrals placed as indicated. Documentation forwarded.",
    ]

    for i, section in enumerate(sections):
        add_medical_page(doc, i + 1, section, pcp_content, header)

    output = f'{MEDICAL_DIR}/primary_care.pdf'
    doc.save(output)
    doc.close()
    print(f'Created: {output} (20 pages)')


def create_specialist_reports():
    """Create 15-page specialist reports PDF."""
    doc = pymupdf.open()
    header = {
        "facility": "Oregon Orthopedic & Sports Medicine",
        "address": "2200 NW Lovejoy St, Suite 400, Portland, OR 97210",
        "phone": "Tel: (503) 555-4500  |  Fax: (503) 555-4501"
    }

    sections = [
        "Initial Orthopedic Consultation - 08/22/2024",
        "Post-Operative Follow-up - Left Wrist - 08/30/2024",
        "Post-Operative Follow-up - Left Wrist - 09/13/2024",
        "Hip Fracture Follow-up - 09/13/2024",
        "Post-Operative Follow-up - Left Wrist - 10/11/2024",
        "Hip Fracture Follow-up - 10/11/2024",
        "Functional Capacity Evaluation Request - 10/11/2024",
        "Post-Operative Follow-up - Left Wrist - 11/08/2024",
        "Hip Fracture Follow-up - 11/08/2024",
        "Physical Therapy Prescription - 11/08/2024",
        "Post-Operative Follow-up - Left Wrist - 12/06/2024",
        "Hip Fracture Follow-up - 12/06/2024",
        "Independent Medical Examination Summary - 12/20/2024",
        "Permanent Impairment Rating - 01/15/2025",
        "Supplemental Report - Response to IME - 01/28/2025",
    ]

    ortho_content = [
        "Patient evaluated in orthopedic clinic per referral.",
        "Reviewed outside imaging and hospital operative reports.",
        "Left wrist: healing distal radius fracture s/p ORIF with volar plate.",
        "Left hip: acetabular fracture managed non-operatively.",
        "Range of motion measurements documented - see attached forms.",
        "Grip strength testing performed bilaterally.",
        "Current functional limitations discussed at length.",
        "Work restrictions outlined. Return to modified duty recommended.",
    ]

    for i, section in enumerate(sections):
        add_medical_page(doc, i + 1, section, ortho_content, header)

    output = f'{MEDICAL_DIR}/specialist_reports.pdf'
    doc.save(output)
    doc.close()
    print(f'Created: {output} (15 pages)')


def create_imaging_results():
    """Create 10-page imaging results PDF."""
    doc = pymupdf.open()
    header = {
        "facility": "Pacific Northwest Radiology Associates",
        "address": "1200 Medical Center Drive, Portland, OR 97205 (at Riverside General)",
        "phone": "Tel: (503) 555-7250  |  Fax: (503) 555-7251"
    }

    sections = [
        "CT Head w/o Contrast - 08/15/2024",
        "CT Cervical Spine w/o Contrast - 08/15/2024",
        "CT Chest/Abdomen/Pelvis w/ Contrast - 08/15/2024",
        "X-Ray Left Wrist 3-View - 08/15/2024",
        "X-Ray Left Wrist Post-Op - 08/16/2024",
        "X-Ray Chest PA/Lateral - 08/18/2024",
        "X-Ray Left Wrist Follow-up - 09/13/2024",
        "CT Left Hip w/o Contrast - 09/13/2024",
        "MRI Left Wrist w/ and w/o Contrast - 11/08/2024",
        "X-Ray Left Hip AP/Lateral - 12/06/2024",
    ]

    imaging_content = [
        "CLINICAL INDICATION: Motor vehicle collision, multiple trauma.",
        "",
        "TECHNIQUE: Standard imaging protocol performed as indicated.",
        "Comparison: Prior studies where available.",
        "",
        "FINDINGS:",
        "Detailed findings as documented in formal radiology report.",
        "Measurements and observations recorded per standard protocol.",
        "Relevant positive and negative findings noted.",
        "",
        "IMPRESSION:",
        "1. See detailed findings above.",
        "2. Clinical correlation recommended.",
        "3. Follow-up imaging as clinically indicated.",
        "",
        "Electronically signed by:",
        "Robert T. Nakamura, MD, FACR",
        "Board Certified Diagnostic Radiologist",
        "Pacific Northwest Radiology Associates",
    ]

    for i, section in enumerate(sections):
        add_medical_page(doc, i + 1, section, imaging_content, header)

    output = f'{MEDICAL_DIR}/imaging_results.pdf'
    doc.save(output)
    doc.close()
    print(f'Created: {output} (10 pages)')


def create_initial():
    os.makedirs(MEDICAL_DIR, exist_ok=True)

    hosp_pages = create_hospital_records()
    create_primary_care()
    create_specialist_reports()
    create_imaging_results()

    print(f'\nAll initial files created in {MEDICAL_DIR}')
    print(f'Hospital: 45 pages, Primary Care: 20 pages, Specialist: 15 pages, Imaging: 10 pages')
    print(f'Total: 90 pages')

    # Open file manager to show the medical directory
    launch_gui(f'nautilus "{MEDICAL_DIR}"', delay_sec=2.0)
    # Open one PDF to show the content
    launch_gui(f'evince "{MEDICAL_DIR}/hospital_records.pdf"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus and Evince with DISPLAY=:0')


create_initial()
