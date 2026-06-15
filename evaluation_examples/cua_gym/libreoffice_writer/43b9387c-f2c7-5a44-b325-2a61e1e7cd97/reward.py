"""
Reward Script: Batch process 3 ODP presentation files and create ODT notes documents
Task ID: osworld_multi_apps_doc_pres_to_writer_011
Domain: libreoffice_writer
Scoring:
  Component 1: All 3 output .odt files exist in notes_output/                      (0.30 pts)
  Component 2: report_q1_notes.odt has 5 Heading 2 paragraphs with correct titles  (0.25 pts)
  Component 3: training_hr_notes.odt has 4 Heading 2 paragraphs with correct titles(0.20 pts)
  Component 4: product_demo_notes.odt has 6 Heading 2 paragraphs with correct titles(0.25 pts)
  Total: 1.0
"""

import os

# python-docx reads .odt files saved in DOCX format
from docx import Document

DESKTOP = '/home/user/Desktop'
NOTES_OUTPUT = os.path.join(DESKTOP, 'notes_output')
TASK_ID = 'osworld_multi_apps_doc_pres_to_writer_011'

# Ground truth slide titles extracted from .odp source files (matches task context)
EXPECTED_HEADINGS = {
    'report_q1_notes.odt': [
        'Q1 Financial Performance Report',
        'Revenue Summary',
        'Cost Analysis',
        'Product Line Performance',
        'Q2 Outlook and Goals',
    ],
    'training_hr_notes.odt': [
        'HR Onboarding Training Program',
        'Company Policies and Code of Conduct',
        'Benefits and Compensation Overview',
        'Tools and Systems Access',
    ],
    'product_demo_notes.odt': [
        'DataSync Pro \u2014 Product Demonstration',
        'Problem Statement',
        'Solution Architecture',
        'Live Demo: Dashboard Overview',
        'Performance Benchmarks',
        'Pricing and Next Steps',
    ],
}

# Scoring weights per output file
FILE_SCORES = {
    'report_q1_notes.odt': 0.25,
    'training_hr_notes.odt': 0.20,
    'product_demo_notes.odt': 0.25,
}


def get_heading2_texts(doc_path):
    """
    Load a Document and return list of paragraph texts where style is Heading 2.
    Accepts both 'Heading 2' (python-docx name) and XML-level 'Heading2' style val.
    """
    doc = Document(doc_path)
    result = []
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ''
        if style_name in ('Heading 2', 'Heading2'):
            result.append(para.text)
    return result


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # ---- Component 1: All 3 expected output files exist (0.30 pts) ----
    # This FAILS on initial_env (notes_output is empty) and PASSES on golden_env.
    try:
        expected_files = list(EXPECTED_HEADINGS.keys())
        all_exist = all(
            os.path.isfile(os.path.join(NOTES_OUTPUT, f)) for f in expected_files
        )
        if all_exist:
            print(f"PASS: Component 1 — All 3 output files exist in notes_output/ (0.30 pts)")
            total_score += 0.30
        else:
            missing = [f for f in expected_files
                       if not os.path.isfile(os.path.join(NOTES_OUTPUT, f))]
            print(f"FAIL: Component 1 — Missing files: {missing}")
            # If no files exist at all, no point checking further
            if len(missing) == len(expected_files):
                print(f"\nScore: {total_score}/1.0")
                print(f"REWARD: {total_score}")
                return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Components 2-4: Each .odt file has correct Heading 2 titles ----
    for fname, weight in FILE_SCORES.items():
        comp_label = fname.replace('.odt', '')
        file_path = os.path.join(NOTES_OUTPUT, fname)
        try:
            if not os.path.isfile(file_path):
                print(f"FAIL: {comp_label} — file not found, skipping content check")
                continue

            actual_headings = get_heading2_texts(file_path)
            expected = EXPECTED_HEADINGS[fname]

            if actual_headings == expected:
                print(
                    f"PASS: {comp_label} — {len(actual_headings)} Heading 2 paragraphs "
                    f"match expected titles ({weight} pts)"
                )
                total_score += weight
            else:
                # Provide detailed diagnostic output
                print(f"FAIL: {comp_label} — heading mismatch")
                print(f"  Expected ({len(expected)}): {expected}")
                print(f"  Actual   ({len(actual_headings)}): {actual_headings}")

                # Partial sub-credit: check count matches
                if len(actual_headings) == len(expected):
                    matched = sum(1 for a, e in zip(actual_headings, expected) if a.strip() == e.strip())
                    print(f"  Matched {matched}/{len(expected)} headings by text")
        except Exception as e:
            print(f"ERROR: {comp_label} — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
