"""
Reward Script: Fill PDF intake forms from Excel patient data
Task ID: osworld_multi_apps_excel_pdf_form_003
Domain: multi_apps (libreoffice_calc + PDF)
Scoring:
  Component 1: All 5 patient PDF files exist on Desktop (0.3 pts)
  Component 2: Each PDF contains correct patient name and DOB (0.3 pts)
  Component 3: Each PDF contains correct Insurance ID, Condition, Doctor, Appointment (0.4 pts)
"""

import os
import subprocess

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_excel_pdf_form_003'

# Ground truth data from patient_intake.xlsx
PATIENTS = [
    {
        'name': 'Maria Garcia',
        'dob': '1985-03-22',
        'insurance_id': 'INS-447821',
        'condition': 'Hypertension',
        'doctor': 'Dr. James Patel',
        'appt_date': '2025-06-10',
    },
    {
        'name': 'David Chen',
        'dob': '1972-11-08',
        'insurance_id': 'INS-339056',
        'condition': 'Type 2 Diabetes',
        'doctor': 'Dr. Emily Torres',
        'appt_date': '2025-06-11',
    },
    {
        'name': 'Sophia Williams',
        'dob': '1990-07-14',
        'insurance_id': 'INS-552134',
        'condition': 'Asthma',
        'doctor': 'Dr. Robert Kim',
        'appt_date': '2025-06-12',
    },
    {
        'name': 'Liam Johnson',
        'dob': '1965-01-30',
        'insurance_id': 'INS-661789',
        'condition': 'Chronic Back Pain',
        'doctor': 'Dr. James Patel',
        'appt_date': '2025-06-13',
    },
    {
        'name': 'Aisha Mohammed',
        'dob': '1998-09-05',
        'insurance_id': 'INS-774302',
        'condition': 'Anxiety Disorder',
        'doctor': 'Dr. Sarah Nguyen',
        'appt_date': '2025-06-16',
    },
]


def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext. Returns empty string on failure."""
    try:
        result = subprocess.run(
            ['pdftotext', pdf_path, '-'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout
        return ''
    except Exception as e:
        print(f"  ERROR extracting text from {pdf_path}: {e}")
        return ''


def verify_task():
    """
    Verify that all 5 patient PDF intake forms have been created on the Desktop
    with correct patient data filled in from patient_intake.xlsx.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: All 5 patient PDF files exist on Desktop (0.3 points)
    # These files should NOT exist in initial_env (only template exists there)
    # They MUST exist in golden_env
    try:
        missing_files = []
        existing_files = []
        for patient in PATIENTS:
            pdf_path = os.path.join(DESKTOP, f"{patient['name']}.pdf")
            if os.path.isfile(pdf_path):
                existing_files.append(patient['name'])
            else:
                missing_files.append(patient['name'])

        if len(existing_files) == 5:
            print(f"PASS: Component 1 — All 5 patient PDFs exist on Desktop (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Only {len(existing_files)}/5 PDFs found. "
                  f"Missing: {missing_files}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each PDF contains correct patient name and DOB (0.3 points)
    # Each patient PDF must contain the patient's name and date of birth from the spreadsheet
    # These fields are fundamental identifiers — verifies basic form completion
    try:
        name_dob_pass = 0
        name_dob_fail = []
        for patient in PATIENTS:
            pdf_path = os.path.join(DESKTOP, f"{patient['name']}.pdf")
            if not os.path.isfile(pdf_path):
                name_dob_fail.append(f"{patient['name']} (file missing)")
                continue
            text = extract_pdf_text(pdf_path)
            has_name = patient['name'] in text
            has_dob = patient['dob'] in text
            if has_name and has_dob:
                name_dob_pass += 1
            else:
                issues = []
                if not has_name:
                    issues.append(f"name '{patient['name']}' not found")
                if not has_dob:
                    issues.append(f"DOB '{patient['dob']}' not found")
                name_dob_fail.append(f"{patient['name']}: {', '.join(issues)}")

        if name_dob_pass == 5:
            print(f"PASS: Component 2 — All 5 PDFs contain correct patient name and DOB (0.3 pts)")
            total_score += 0.3
        elif name_dob_pass >= 3:
            partial = round(0.3 * name_dob_pass / 5, 2)
            print(f"PARTIAL: Component 2 — {name_dob_pass}/5 PDFs have correct name+DOB. "
                  f"Partial credit: {partial}. Issues: {name_dob_fail}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {name_dob_pass}/5 PDFs have correct name+DOB. "
                  f"Issues: {name_dob_fail}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each PDF contains correct Insurance ID, Condition, Doctor, Appointment (0.4 points)
    # Verifies that all remaining fields from the spreadsheet were accurately transferred
    try:
        full_data_pass = 0
        full_data_fail = []
        for patient in PATIENTS:
            pdf_path = os.path.join(DESKTOP, f"{patient['name']}.pdf")
            if not os.path.isfile(pdf_path):
                full_data_fail.append(f"{patient['name']} (file missing)")
                continue
            text = extract_pdf_text(pdf_path)
            has_insurance = patient['insurance_id'] in text
            has_condition = patient['condition'] in text
            has_doctor = patient['doctor'] in text
            has_appt = patient['appt_date'] in text
            if has_insurance and has_condition and has_doctor and has_appt:
                full_data_pass += 1
            else:
                issues = []
                if not has_insurance:
                    issues.append(f"insurance '{patient['insurance_id']}' not found")
                if not has_condition:
                    issues.append(f"condition '{patient['condition']}' not found")
                if not has_doctor:
                    issues.append(f"doctor '{patient['doctor']}' not found")
                if not has_appt:
                    issues.append(f"appt '{patient['appt_date']}' not found")
                full_data_fail.append(f"{patient['name']}: {', '.join(issues)}")

        if full_data_pass == 5:
            print(f"PASS: Component 3 — All 5 PDFs contain all correct data fields (0.4 pts)")
            total_score += 0.4
        elif full_data_pass >= 3:
            partial = round(0.4 * full_data_pass / 5, 2)
            print(f"PARTIAL: Component 3 — {full_data_pass}/5 PDFs have all data fields. "
                  f"Partial credit: {partial}. Issues: {full_data_fail}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {full_data_pass}/5 PDFs have all data fields. "
                  f"Issues: {full_data_fail}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
