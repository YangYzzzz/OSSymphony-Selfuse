"""
Reward Script: Create individualized annual review PDFs for all employees in Excel performance data file.
Task ID: osworld_multi_apps_excel_pdf_form_012
Domain: libreoffice_calc (multi-app: Excel + PDF generation)
Scoring:
  Component 1: reviews/ directory structure with correct department subdirs (0.20 pts)
  Component 2: All 12 employee PDFs exist in correct department folders (0.30 pts)
  Component 3: PDF content correctness — employee info, ratings, overall score (0.30 pts)
  Component 4: Manager recommendation correctly marked in PDFs (0.20 pts)
  Total: 1.0
"""

import os
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_excel_pdf_form_012'
REVIEWS_DIR = '/home/user/Desktop/reviews'

# Employee data from annual_reviews.xlsx (ground truth)
# Format: (EmployeeID, Name, Department, TechSkills, Communication, Leadership, Teamwork, OverallScore, Recommendation)
EMPLOYEES = [
    ('EMP001', 'Sarah Chen',      'Engineering', 5, 4, 4, 5, 4.5,  'Promote'),
    ('EMP002', 'Marcus Johnson',  'Engineering', 4, 5, 3, 4, 4.0,  'Retain'),
    ('EMP003', 'Priya Patel',     'Marketing',   3, 5, 4, 5, 4.25, 'Retain'),
    ('EMP004', 'Derek Williams',  'Marketing',   2, 3, 2, 3, 2.5,  'PIP'),
    ('EMP005', 'Aisha Okonkwo',   'HR',          4, 5, 5, 5, 4.75, 'Promote'),
    ('EMP006', 'James Kowalski',  'Engineering', 5, 3, 4, 4, 4.0,  'Retain'),
    ('EMP007', 'Lisa Nguyen',     'Finance',     4, 4, 3, 4, 3.75, 'Retain'),
    ('EMP008', 'Roberto Martinez','Finance',     3, 3, 2, 3, 2.75, 'PIP'),
    ('EMP009', 'Fatima Al-Hassan','HR',          5, 5, 5, 5, 5.0,  'Promote'),
    ('EMP010', 'Tyler Brooks',    'Marketing',   4, 4, 4, 4, 4.0,  'Retain'),
    ('EMP011', 'Hannah Kimura',   'Engineering', 5, 4, 5, 5, 4.75, 'Promote'),
    ('EMP012', 'David Osei',      'Finance',     4, 5, 4, 4, 4.25, 'Retain'),
]

# Expected department subfolders
EXPECTED_DEPARTMENTS = {'Engineering', 'Finance', 'HR', 'Marketing'}

# Build lookup: EmployeeID -> full record
EMP_MAP = {emp[0]: emp for emp in EMPLOYEES}

# Build lookup: department -> set of employee IDs
DEPT_EMP_MAP = {}
for emp in EMPLOYEES:
    dept = emp[2]
    if dept not in DEPT_EMP_MAP:
        DEPT_EMP_MAP[dept] = set()
    DEPT_EMP_MAP[dept].add(emp[0])


def extract_pdf_text(pdf_path):
    """Extract text from a PDF file using pdftotext CLI tool."""
    try:
        result = subprocess.run(
            ['pdftotext', pdf_path, '-'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"  ERROR extracting PDF text from {pdf_path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: reviews/ directory structure with correct department subdirs (0.20 pts)
    # The task requires PDFs organized into Desktop/reviews/DepartmentName/ subfolders
    try:
        if not os.path.isdir(REVIEWS_DIR):
            print(f"FAIL: Component 1 — reviews/ directory does not exist at {REVIEWS_DIR}")
        else:
            existing_subdirs = set(
                d for d in os.listdir(REVIEWS_DIR)
                if os.path.isdir(os.path.join(REVIEWS_DIR, d))
            )
            missing_depts = EXPECTED_DEPARTMENTS - existing_subdirs
            extra_depts = existing_subdirs - EXPECTED_DEPARTMENTS

            if missing_depts:
                print(f"FAIL: Component 1 — Missing department subdirs: {sorted(missing_depts)}")
            else:
                print(f"PASS: Component 1 — reviews/ directory exists with all 4 department subdirs: "
                      f"{sorted(existing_subdirs)} (0.20 pts)")
                if extra_depts:
                    print(f"  NOTE: Extra unexpected subdirs found: {sorted(extra_depts)}")
                total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 12 employee PDFs exist in correct department folders (0.30 pts)
    # Each PDF must be named EmployeeID.pdf and placed in the correct department subfolder
    try:
        missing_pdfs = []
        misplaced_pdfs = []
        found_count = 0

        for emp_id, name, dept, *_ in EMPLOYEES:
            expected_path = os.path.join(REVIEWS_DIR, dept, f'{emp_id}.pdf')
            if os.path.exists(expected_path):
                found_count += 1
            else:
                missing_pdfs.append(f"{dept}/{emp_id}.pdf")
                # Check if it's in the wrong department
                for other_dept in EXPECTED_DEPARTMENTS:
                    if other_dept != dept:
                        wrong_path = os.path.join(REVIEWS_DIR, other_dept, f'{emp_id}.pdf')
                        if os.path.exists(wrong_path):
                            misplaced_pdfs.append(f"{emp_id}.pdf found in {other_dept}/ instead of {dept}/")

        if found_count == 12:
            print(f"PASS: Component 2 — All 12 employee PDFs exist in correct department folders (0.30 pts)")
            total_score += 0.30
        elif found_count >= 8:
            # Partial credit: at least 8 PDFs in right place
            partial = 0.15
            print(f"PARTIAL: Component 2 — {found_count}/12 PDFs found in correct locations ({partial} pts)")
            print(f"  Missing: {missing_pdfs}")
            if misplaced_pdfs:
                print(f"  Misplaced: {misplaced_pdfs}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {found_count}/12 PDFs found in correct department folders")
            print(f"  Missing: {missing_pdfs}")
            if misplaced_pdfs:
                print(f"  Misplaced: {misplaced_pdfs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF content correctness — employee info, ratings, overall score (0.30 pts)
    # Spot-check a sample of PDFs for correct employee ID, name, ratings with [√] marks, and overall score
    # We check EMP001 (Promote, Engineering), EMP004 (PIP, Marketing), EMP009 (Promote, HR)
    try:
        sample_checks = [
            ('EMP001', 'Engineering', 4.5,  [5, 4, 4, 5]),  # Technical=5, Comm=4, Lead=4, Team=5
            ('EMP004', 'Marketing',   2.5,  [2, 3, 2, 3]),  # Technical=2, Comm=3, Lead=2, Team=3
            ('EMP009', 'HR',          5.0,  [5, 5, 5, 5]),  # Technical=5, Comm=5, Lead=5, Team=5
        ]

        content_passed = 0
        content_total = len(sample_checks)

        for emp_id, dept, expected_score, expected_ratings in sample_checks:
            pdf_path = os.path.join(REVIEWS_DIR, dept, f'{emp_id}.pdf')
            if not os.path.exists(pdf_path):
                print(f"  SKIP: Component 3 check for {emp_id} — PDF not found at {pdf_path}")
                continue

            text = extract_pdf_text(pdf_path)
            if text is None:
                print(f"  ERROR: Component 3 — Could not extract text from {emp_id}.pdf")
                continue

            # Check employee ID appears
            id_ok = emp_id in text
            # Check overall score appears (formatted as X.XX or X.X)
            score_str_1 = f"{expected_score:.2f}"  # e.g., "4.50"
            score_str_2 = f"{expected_score}"       # e.g., "4.5"
            score_ok = score_str_1 in text or score_str_2 in text

            # Check each rating appears with [√] mark at correct value
            # The PDF format is: "[ ] 1 [ ] 2 [√] 3 [ ] 4 [ ] 5" etc.
            # We look for "[√] N" where N is the expected rating
            ratings_ok = True
            for rating in expected_ratings:
                # The check mark should appear before the correct rating number
                mark_pattern = f"[{chr(0x221a)}] {rating}"  # √ = U+221A
                alt_pattern = f"[√] {rating}"
                if mark_pattern not in text and alt_pattern not in text:
                    ratings_ok = False
                    print(f"  FAIL: Component 3 — {emp_id}: expected [√] {rating} not found in PDF")
                    break

            if id_ok and score_ok and ratings_ok:
                content_passed += 1
                print(f"  PASS: Component 3 check — {emp_id}: ID={id_ok}, score={score_ok} ({expected_score}), ratings={ratings_ok}")
            else:
                reasons = []
                if not id_ok:
                    reasons.append(f"EmployeeID {emp_id} not found")
                if not score_ok:
                    reasons.append(f"Overall score {expected_score} not found")
                if not ratings_ok:
                    reasons.append("Rating marks incorrect")
                print(f"  FAIL: Component 3 check — {emp_id}: {', '.join(reasons)}")

        if content_passed == content_total:
            print(f"PASS: Component 3 — All {content_total} sample PDFs have correct content (0.30 pts)")
            total_score += 0.30
        elif content_passed >= 2:
            partial = 0.15
            print(f"PARTIAL: Component 3 — {content_passed}/{content_total} sample PDFs correct ({partial} pts)")
            total_score += partial
        elif content_passed == 1:
            partial = 0.10
            print(f"PARTIAL: Component 3 — {content_passed}/{content_total} sample PDFs correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — {content_passed}/{content_total} sample PDFs have correct content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Manager recommendation correctly marked in PDFs (0.20 pts)
    # Verify PDFs for Promote, Retain, and PIP cases have correct recommendation checked
    try:
        rec_checks = [
            ('EMP001', 'Engineering', 'Promote'),  # [√] Promote
            ('EMP004', 'Marketing',   'PIP'),       # [√] PIP
            ('EMP007', 'Finance',     'Retain'),    # [√] Retain
        ]

        rec_passed = 0
        rec_total = len(rec_checks)

        for emp_id, dept, expected_rec in rec_checks:
            pdf_path = os.path.join(REVIEWS_DIR, dept, f'{emp_id}.pdf')
            if not os.path.exists(pdf_path):
                print(f"  SKIP: Component 4 check for {emp_id} — PDF not found")
                continue

            text = extract_pdf_text(pdf_path)
            if text is None:
                print(f"  ERROR: Component 4 — Could not extract text from {emp_id}.pdf")
                continue

            # Check that the correct recommendation has [√] before it
            # and that incorrect recommendations do NOT have [√]
            wrong_recs = [r for r in ['Promote', 'Retain', 'PIP'] if r != expected_rec]

            # Check correct recommendation is marked
            rec_mark_found = False
            for mark in [f"[{chr(0x221a)}] {expected_rec}", f"[√] {expected_rec}"]:
                if mark in text:
                    rec_mark_found = True
                    break

            if rec_mark_found:
                rec_passed += 1
                print(f"  PASS: Component 4 check — {emp_id}: [{chr(0x221a)}] {expected_rec} found correctly")
            else:
                print(f"  FAIL: Component 4 check — {emp_id}: Expected [√] {expected_rec} but not found in PDF")
                print(f"    PDF excerpt: {repr(text[text.find('Recommendation'):text.find('Recommendation')+200] if 'Recommendation' in text else 'section not found')}")

        if rec_passed == rec_total:
            print(f"PASS: Component 4 — All {rec_total} sample PDFs have correct manager recommendation (0.20 pts)")
            total_score += 0.20
        elif rec_passed >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 4 — {rec_passed}/{rec_total} recommendation checks passed ({partial} pts)")
            total_score += partial
        elif rec_passed == 1:
            partial = 0.07
            print(f"PARTIAL: Component 4 — {rec_passed}/{rec_total} recommendation checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — {rec_passed}/{rec_total} recommendation checks passed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
