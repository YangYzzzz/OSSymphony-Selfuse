"""
Reward Script: Fill scholarship application PDFs from Excel data
Task ID: osworld_multi_apps_excel_pdf_form_007
Domain: libreoffice_calc (multi-app: Excel + PDF)

Task: Read scholarship applicant data from Excel, create individual PDF forms
per applicant (named 'ApplicantName.pdf'), with correct data filled in and
checkmarks for financial need level and essay submission status.

Scoring Rubric:
  Component 1: All 5 applicant PDF files exist (0.30 pts, 0.06 per file)
               [PDFs don't exist in initial_env — task-introduced change]
  Component 2: Correct applicant info (name, ID, GPA, scholarship type) in each PDF (0.40 pts, 0.08 per file)
  Component 3: Correct checkmarks (financial need level + essay Y/N) in each PDF (0.30 pts, 0.06 per file)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_excel_pdf_form_007'

# Expected applicant data from scholarship_candidates.xlsx (task context ground truth)
EXPECTED_APPLICANTS = [
    {
        'name': 'Emily Hartwell',
        'student_id': 'S2024-0041',
        'gpa': '3.87',
        'scholarship_type': 'Merit-Based Excellence',
        'financial_need': 'High',
        'essay_submitted': 'Y',
    },
    {
        'name': 'Daniel Okonkwo',
        'student_id': 'S2024-0089',
        'gpa': '3.45',
        'scholarship_type': 'Community Leadership',
        'financial_need': 'Medium',
        'essay_submitted': 'Y',
    },
    {
        'name': 'Priya Nambiar',
        'student_id': 'S2024-0133',
        'gpa': '3.92',
        'scholarship_type': 'STEM Achievement',
        'financial_need': 'Low',
        'essay_submitted': 'Y',
    },
    {
        'name': 'Carlos Vega',
        'student_id': 'S2024-0178',
        'gpa': '3.20',
        'scholarship_type': 'First-Generation Scholar',
        'financial_need': 'High',
        'essay_submitted': 'N',
    },
    {
        'name': 'Sophia Lindqvist',
        'student_id': 'S2024-0215',
        'gpa': '3.68',
        'scholarship_type': 'Global Studies Award',
        'financial_need': 'Medium',
        'essay_submitted': 'Y',
    },
]

CHECKMARK_CHAR = '\u221a'  # √


def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF file using pdftotext via os.popen.
    Returns the text as a string, or None if extraction fails.
    """
    try:
        import shlex
        cmd = f'pdftotext -layout {shlex.quote(pdf_path)} -'
        text = os.popen(cmd).read()
        if not text:
            return None
        return text
    except Exception as e:
        print(f"ERROR: Could not extract text from {pdf_path}: {e}")
        return None


def score_pdf_existence(applicant):
    """
    Check if the output PDF for this applicant was created.
    Task change: PDFs do NOT exist in initial_env — their creation IS the task.
    Returns (score: float, text_or_none: str|None)
    """
    pdf_path = os.path.join(WORKDIR, f"{applicant['name']}.pdf")
    pdf_path_exists = os.path.exists(pdf_path)
    if pdf_path_exists:
        text = extract_pdf_text(pdf_path)
        return 1.0, text
    else:
        return 0.0, None


def score_pdf_info(text, applicant):
    """
    Verify that the PDF contains correct applicant info.
    Checks: name, student ID, GPA, scholarship type.
    Returns 1.0 if all 4 fields present, 0.0 otherwise.
    """
    name_ok = applicant['name'] in text
    id_ok = applicant['student_id'] in text
    # GPA may appear as '3.87' or '3.20' (with or without trailing zero)
    gpa_ok = (applicant['gpa'] in text
              or applicant['gpa'].rstrip('0').rstrip('.') in text)
    scholarship_ok = applicant['scholarship_type'] in text

    if name_ok and id_ok and gpa_ok and scholarship_ok:
        return 1.0
    else:
        return 0.0


def score_pdf_checkmarks(text, applicant):
    """
    Verify that checkmarks are placed correctly in the PDF.
    Checks:
      (a) checkmark on the correct financial need level line
      (b) no checkmark on any wrong financial need level line
      (c) essay Y/N checkmark is correct
    Returns 1.0 if all 3 conditions met, 0.0 otherwise.
    """
    lines = text.split('\n')
    expected_need = applicant['financial_need']
    essay_value = applicant['essay_submitted']

    # (a) Checkmark on the correct financial need level line
    correct_need_checked = any(
        CHECKMARK_CHAR in line and expected_need in line
        for line in lines
    )

    # (b) No checkmark on any wrong financial need level
    other_needs = [n for n in ['High', 'Medium', 'Low'] if n != expected_need]
    wrong_need_checked = any(
        CHECKMARK_CHAR in line and other_need in line
        for line in lines
        for other_need in other_needs
    )

    # (c) Essay checkmark matches Y/N
    if essay_value == 'Y':
        essay_ok = any(CHECKMARK_CHAR in line and 'Yes' in line for line in lines)
    else:
        essay_ok = any(CHECKMARK_CHAR in line and 'No' in line for line in lines)

    if correct_need_checked and not wrong_need_checked and essay_ok:
        return 1.0
    else:
        return 0.0


def verify_task():
    """
    Verify that individual scholarship application PDFs were created for each applicant.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    n = len(EXPECTED_APPLICANTS)  # 5

    comp1_weight = 0.30 / n   # 0.06 per file
    comp2_weight = 0.40 / n   # 0.08 per file
    comp3_weight = 0.30 / n   # 0.06 per file

    comp1_total = 0.0
    comp2_total = 0.0
    comp3_total = 0.0

    # -------------------------------------------------------------------------
    # Components 1+2+3: Evaluated per applicant (all 3 components use PDF content)
    # -------------------------------------------------------------------------
    for applicant in EXPECTED_APPLICANTS:
        name = applicant['name']
        pdf_path = os.path.join(WORKDIR, f"{name}.pdf")

        # --- Component 1: PDF file exists (task-introduced — no PDFs in initial state) ---
        try:
            exists_score, pdf_text = score_pdf_existence(applicant)
            if exists_score > 0:
                comp1_total += comp1_weight
                print(f"PASS: Component 1 — '{name}.pdf' created (+{comp1_weight:.2f} pts)")
            else:
                print(f"FAIL: Component 1 — '{name}.pdf' NOT found at {pdf_path}")
        except Exception as e:
            print(f"ERROR: Component 1 ({name}) — {e}")
            pdf_text = None

        # --- Component 2: Correct applicant info in PDF ---
        try:
            if pdf_text:
                info_score = score_pdf_info(pdf_text, applicant)
                if info_score > 0:
                    comp2_total += comp2_weight
                    print(f"PASS: Component 2 — Info correct in '{name}.pdf' (+{comp2_weight:.2f} pts)")
                else:
                    # Show what was found vs expected
                    name_ok = applicant['name'] in pdf_text
                    id_ok = applicant['student_id'] in pdf_text
                    gpa_ok = applicant['gpa'] in pdf_text
                    sch_ok = applicant['scholarship_type'] in pdf_text
                    print(f"FAIL: Component 2 — Info missing in '{name}.pdf' "
                          f"[name={name_ok}, id={id_ok}, gpa={gpa_ok}, scholarship={sch_ok}]")
            else:
                print(f"SKIP: Component 2 — PDF not available for '{name}'")
        except Exception as e:
            print(f"ERROR: Component 2 ({name}) — {e}")

        # --- Component 3: Correct checkmarks in PDF ---
        try:
            if pdf_text:
                chk_score = score_pdf_checkmarks(pdf_text, applicant)
                if chk_score > 0:
                    comp3_total += comp3_weight
                    print(f"PASS: Component 3 — Checkmarks correct in '{name}.pdf' (+{comp3_weight:.2f} pts) "
                          f"[need={applicant['financial_need']}, essay={applicant['essay_submitted']}]")
                else:
                    print(f"FAIL: Component 3 — Checkmarks incorrect in '{name}.pdf' "
                          f"[expected need={applicant['financial_need']}, essay={applicant['essay_submitted']}]")
            else:
                print(f"SKIP: Component 3 — PDF not available for '{name}'")
        except Exception as e:
            print(f"ERROR: Component 3 ({name}) — {e}")

    total_score = comp1_total + comp2_total + comp3_total

    print(f"\nComponent 1 subtotal: {comp1_total:.2f}/0.30")
    print(f"Component 2 subtotal: {comp2_total:.2f}/0.40")
    print(f"Component 3 subtotal: {comp3_total:.2f}/0.30")
    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
