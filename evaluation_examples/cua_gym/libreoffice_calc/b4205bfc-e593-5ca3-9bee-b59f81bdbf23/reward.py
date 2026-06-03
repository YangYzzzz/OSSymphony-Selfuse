"""
Reward Script: Process employee onboarding Excel file and generate onboarding packet PDFs
Task ID: osworld_multi_apps_excel_pdf_form_011
Domain: libreoffice_calc (multi_apps: xlsx + PDF generation)

Scoring Rubric:
  Component 1: Desktop/onboarding/ folder exists                          (0.20 pts)
  Component 2: All 10 employee PDFs present in folder                     (0.30 pts)
  Component 3: Personal details (name, ID, dept, role) correct in PDFs    (0.30 pts)
  Component 4: IT access level correctly marked with checkmark (√)        (0.10 pts)
  Component 5: Equipment assigned correctly marked with checkmark (√)     (0.10 pts)
  Total: 1.0
"""

import os
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_excel_pdf_form_011'

# Employee data from new_hires.xlsx (ground truth from task context)
EMPLOYEES = [
    {'name': 'Sarah Chen',       'id': 'EMP-2025-001', 'dept': 'Engineering',     'role': 'Software Engineer',           'start': '2025-03-03', 'manager': 'David Kim',       'it_level': 'Standard', 'equipment': 'Laptop'},
    {'name': 'Marcus Johnson',   'id': 'EMP-2025-002', 'dept': 'Marketing',       'role': 'Digital Marketing Manager',   'start': '2025-03-03', 'manager': 'Emily Watson',     'it_level': 'Standard', 'equipment': 'Both'},
    {'name': 'Priya Patel',      'id': 'EMP-2025-003', 'dept': 'Finance',         'role': 'Financial Analyst',           'start': '2025-03-10', 'manager': 'Robert Hughes',    'it_level': 'Elevated', 'equipment': 'Desktop'},
    {'name': "James O'Brien",    'id': 'EMP-2025-004', 'dept': 'Engineering',     'role': 'DevOps Engineer',             'start': '2025-03-10', 'manager': 'David Kim',       'it_level': 'Admin',    'equipment': 'Laptop'},
    {'name': 'Anika Müller',     'id': 'EMP-2025-005', 'dept': 'Human Resources', 'role': 'HR Business Partner',         'start': '2025-03-17', 'manager': 'Sandra Torres',   'it_level': 'Standard', 'equipment': 'Desktop'},
    {'name': 'Chen Wei',         'id': 'EMP-2025-006', 'dept': 'Security',        'role': 'Information Security Analyst','start': '2025-03-17', 'manager': 'Laura Fernandez', 'it_level': 'Admin',    'equipment': 'Both'},
    {'name': 'Fatima Al-Rashid', 'id': 'EMP-2025-007', 'dept': 'Product',         'role': 'Product Manager',             'start': '2025-03-24', 'manager': 'Michael Chang',   'it_level': 'Elevated', 'equipment': 'Laptop'},
    {'name': 'Diego Ramirez',    'id': 'EMP-2025-008', 'dept': 'Engineering',     'role': 'Backend Developer',           'start': '2025-03-24', 'manager': 'David Kim',       'it_level': 'Standard', 'equipment': 'Laptop'},
    {'name': 'Yuki Tanaka',      'id': 'EMP-2025-009', 'dept': 'Data Science',    'role': 'Machine Learning Engineer',   'start': '2025-03-31', 'manager': 'Laura Fernandez', 'it_level': 'Elevated', 'equipment': 'Both'},
    {'name': 'Olivia Bennett',   'id': 'EMP-2025-010', 'dept': 'Legal',           'role': 'Corporate Counsel',           'start': '2025-03-31', 'manager': 'Richard Nolan',   'it_level': 'Standard', 'equipment': 'Desktop'},
]

ONBOARDING_DIR = os.path.join(WORKDIR, 'Desktop', 'onboarding')

# IT access levels and equipment options for checkmark detection
IT_LEVELS = ['Standard', 'Elevated', 'Admin']
EQUIPMENT_TYPES = ['Laptop', 'Desktop', 'Both']


def get_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext with layout preservation."""
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', pdf_path, '-'],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout
    except Exception as e:
        print(f"ERROR: Could not extract text from {pdf_path}: {e}")
        return None


def normalize_name_for_filename(name):
    """
    Normalize employee name for PDF filename (handle unicode chars).
    Uses 'ue' for ü, 'oe' for ö, 'ae' for ä (German convention).
    """
    replacements = {
        'ü': 'ue', 'ö': 'oe', 'ä': 'ae', 'ß': 'ss',
        'Ü': 'Ue', 'Ö': 'Oe', 'Ä': 'Ae',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u',
        'ñ': 'n', 'ç': 'c',
    }
    result = name
    for orig, repl in replacements.items():
        result = result.replace(orig, repl)
    return result


def normalize_name_ascii_simple(name):
    """
    Simple ASCII fallback: replace each accented char with single ASCII equivalent.
    """
    replacements = {
        'ü': 'u', 'ö': 'o', 'ä': 'a', 'ß': 'ss',
        'Ü': 'U', 'Ö': 'O', 'Ä': 'A',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u',
        'ñ': 'n', 'ç': 'c',
    }
    result = name
    for orig, repl in replacements.items():
        result = result.replace(orig, repl)
    return result


def find_pdf_for_employee(emp_name):
    """
    Try to find a PDF file for an employee, handling unicode filename variants.
    Returns the path if found, else None.
    """
    # Try exact name first
    exact_path = os.path.join(ONBOARDING_DIR, f"{emp_name}.pdf")
    if os.path.exists(exact_path):
        return exact_path
    # Try normalized (ASCII) name
    norm_name = normalize_name_for_filename(emp_name)
    norm_path = os.path.join(ONBOARDING_DIR, f"{norm_name}.pdf")
    if os.path.exists(norm_path):
        return norm_path
    # Try further variant: 'ü' -> 'ue', 'ö' -> 'oe', 'ä' -> 'ae'
    replacements2 = {'ü': 'ue', 'ö': 'oe', 'ä': 'ae', 'Ü': 'Ue', 'Ö': 'Oe', 'Ä': 'Ae'}
    variant = emp_name
    for orig, repl in replacements2.items():
        variant = variant.replace(orig, repl)
    variant_path = os.path.join(ONBOARDING_DIR, f"{variant}.pdf")
    if os.path.exists(variant_path):
        return variant_path
    return None


def detect_checked_it_level(pdf_text):
    """
    Detect which IT access level has the checkmark (√) in the PDF text with layout.
    Returns 'Standard', 'Elevated', 'Admin', or None.
    """
    lines = pdf_text.split('\n')
    in_it_section = False
    in_equip_section = False
    for line in lines:
        if 'IT ACCESS LEVEL' in line:
            in_it_section = True
            in_equip_section = False
            continue
        if 'EQUIPMENT ASSIGNED' in line:
            in_it_section = False
            in_equip_section = True
            continue
        if 'BADGE PHOTO' in line:
            in_it_section = False
            in_equip_section = False
            continue
        if in_it_section and '√' in line:
            for level in IT_LEVELS:
                if level in line:
                    return level
    return None


def detect_checked_equipment(pdf_text):
    """
    Detect which equipment type has the checkmark (√) in the PDF text with layout.
    Returns 'Laptop', 'Desktop', 'Both', or None.
    """
    lines = pdf_text.split('\n')
    in_equip_section = False
    for line in lines:
        if 'EQUIPMENT ASSIGNED' in line:
            in_equip_section = True
            continue
        if 'BADGE PHOTO' in line:
            in_equip_section = False
            continue
        if in_equip_section and '√' in line:
            for equip in EQUIPMENT_TYPES:
                if equip in line:
                    return equip
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Desktop/onboarding/ folder exists (0.20 points)
    # This is a task-introduced change: initial env has no onboarding/ folder
    try:
        if os.path.isdir(ONBOARDING_DIR):
            print(f"PASS: Component 1 — Desktop/onboarding/ folder exists (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Desktop/onboarding/ folder not found at {ONBOARDING_DIR}")
            # Cannot verify further components without the folder
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All 10 employee PDFs present in folder (0.30 points)
    # Each PDF found = 0.03 points, up to 0.30 total
    try:
        found_pdfs = []
        missing_pdfs = []
        for emp in EMPLOYEES:
            pdf_path = find_pdf_for_employee(emp['name'])
            if pdf_path:
                found_pdfs.append((emp['name'], pdf_path))
            else:
                missing_pdfs.append(emp['name'])

        pdf_score = (len(found_pdfs) / len(EMPLOYEES)) * 0.30
        if pdf_score > 0:
            total_score += pdf_score

        if missing_pdfs:
            print(f"PARTIAL: Component 2 — {len(found_pdfs)}/{len(EMPLOYEES)} PDFs found ({pdf_score:.2f} pts)")
            print(f"  Missing: {missing_pdfs}")
        else:
            print(f"PASS: Component 2 — All {len(EMPLOYEES)} employee PDFs found (0.30 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        found_pdfs = []

    if not found_pdfs:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Personal details correct (name, ID, dept, role) in PDFs (0.30 points)
    # Check the PDFs that were found; each correct PDF = 0.03 points
    try:
        details_correct_count = 0
        details_total = len(found_pdfs)

        for emp_name, pdf_path in found_pdfs:
            # Find the employee record
            emp = next((e for e in EMPLOYEES if e['name'] == emp_name), None)
            if emp is None:
                continue

            pdf_text = get_pdf_text(pdf_path)
            if pdf_text is None:
                print(f"  FAIL: Could not read {pdf_path}")
                continue

            # Check key personal details in the PDF text
            # For EmployeeName: accept original, 'ue'-normalized, or simple ASCII
            name_variants = [
                emp['name'],
                normalize_name_for_filename(emp['name']),
                normalize_name_ascii_simple(emp['name']),
            ]
            name_found = any(variant in pdf_text for variant in name_variants)
            checks = {
                'EmployeeName': name_found,
                'EmployeeID': emp['id'] in pdf_text,
                'Department': emp['dept'] in pdf_text,
                'Role': emp['role'] in pdf_text,
            }
            passed = all(checks.values())
            if passed:
                details_correct_count += 1
            else:
                failed_checks = [k for k, v in checks.items() if not v]
                print(f"  FAIL: {emp_name} — Personal details missing: {failed_checks}")

        details_score = (details_correct_count / details_total) * 0.30 if details_total > 0 else 0.0
        total_score += details_score

        if details_correct_count == details_total:
            print(f"PASS: Component 3 — Personal details correct in all {details_total} PDFs (0.30 pts)")
        else:
            print(f"PARTIAL: Component 3 — {details_correct_count}/{details_total} PDFs have correct personal details ({details_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: IT access level correctly marked with √ (0.10 points)
    # Each correct PDF = 0.01 points, up to 0.10 total
    try:
        it_correct_count = 0
        it_total = len(found_pdfs)

        for emp_name, pdf_path in found_pdfs:
            emp = next((e for e in EMPLOYEES if e['name'] == emp_name), None)
            if emp is None:
                continue

            pdf_text = get_pdf_text(pdf_path)
            if pdf_text is None:
                continue

            detected_level = detect_checked_it_level(pdf_text)
            expected_level = emp['it_level']
            if detected_level == expected_level:
                it_correct_count += 1
            else:
                print(f"  FAIL: {emp_name} — IT level: expected '{expected_level}', detected '{detected_level}'")

        it_score = (it_correct_count / it_total) * 0.10 if it_total > 0 else 0.0
        total_score += it_score

        if it_correct_count == it_total:
            print(f"PASS: Component 4 — IT access level correct in all {it_total} PDFs (0.10 pts)")
        else:
            print(f"PARTIAL: Component 4 — {it_correct_count}/{it_total} PDFs have correct IT level ({it_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Equipment assigned correctly marked with √ (0.10 points)
    # Each correct PDF = 0.01 points, up to 0.10 total
    try:
        equip_correct_count = 0
        equip_total = len(found_pdfs)

        for emp_name, pdf_path in found_pdfs:
            emp = next((e for e in EMPLOYEES if e['name'] == emp_name), None)
            if emp is None:
                continue

            pdf_text = get_pdf_text(pdf_path)
            if pdf_text is None:
                continue

            detected_equip = detect_checked_equipment(pdf_text)
            expected_equip = emp['equipment']
            if detected_equip == expected_equip:
                equip_correct_count += 1
            else:
                print(f"  FAIL: {emp_name} — Equipment: expected '{expected_equip}', detected '{detected_equip}'")

        equip_score = (equip_correct_count / equip_total) * 0.10 if equip_total > 0 else 0.0
        total_score += equip_score

        if equip_correct_count == equip_total:
            print(f"PASS: Component 5 — Equipment assigned correct in all {equip_total} PDFs (0.10 pts)")
        else:
            print(f"PARTIAL: Component 5 — {equip_correct_count}/{equip_total} PDFs have correct equipment ({equip_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
