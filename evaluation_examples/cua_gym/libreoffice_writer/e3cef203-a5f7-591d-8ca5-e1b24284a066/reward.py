"""
Reward Script: Format sourdough blog post in LibreOffice Writer
Task ID: writer_creative_022
Domain: libreoffice_writer
Scoring:
  - Component 1: Title 'The Art of Sourdough...' has Heading 1 style (0.3 pts)
  - Component 2: All 5 section headers have Heading 2 style (0.4 pts)
  - Component 3: Measurement values (500g, 350ml, 100g, 10g) are bold in ingredient lines (0.3 pts)
"""

import os

from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_creative_022'
FILE_PATH = f'{WORKDIR}/sourdough_blog.docx'

# Expected section headers (must all be Heading 2)
EXPECTED_HEADERS = [
    'Why Sourdough?',
    'Getting Started: Your First Starter',
    'The Basic Recipe',
    'The Baking Process',
    'Tips for Success',
]

# Expected measurement tokens to be bold (first run in each ingredient line)
EXPECTED_MEASUREMENTS = ['500g', '350ml', '100g', '10g']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a map: paragraph text (stripped) -> paragraph object
    # to facilitate lookup of specific paragraphs
    paragraphs = doc.paragraphs

    # -------------------------------------------------------------------
    # Component 1: Title has Heading 1 style (0.3 points)
    # In initial_env all paragraphs use 'Normal' style — this FAILS on initial.
    # In golden_env the title paragraph uses 'Heading 1' — PASSES on golden.
    # -------------------------------------------------------------------
    try:
        title_text = "The Art of Sourdough: A Beginner's Journey"
        title_para = None
        for para in paragraphs:
            if para.text.strip() == title_text:
                title_para = para
                break

        if title_para is None:
            print(f"FAIL: Component 1 — title paragraph not found in document")
        else:
            style_name = title_para.style.name
            # Accept 'Heading 1' or styles that inherit from heading 1
            if 'Heading 1' in style_name or style_name == 'Title':
                print(f"PASS: Component 1 — Title has style '{style_name}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — Title style is '{style_name}', expected 'Heading 1'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: All 5 section headers have Heading 2 style (0.4 points)
    # In initial_env all are 'Normal' — this FAILS on initial.
    # In golden_env all 5 use 'Heading 2' — PASSES on golden.
    # Award partial credit: 0.08 per header (5 headers × 0.08 = 0.40)
    # -------------------------------------------------------------------
    try:
        # Build a set of paragraph texts for quick lookup
        para_style_map = {}
        for para in paragraphs:
            para_style_map[para.text.strip()] = para.style.name

        headers_found = 0
        for header in EXPECTED_HEADERS:
            style = para_style_map.get(header, None)
            if style and 'Heading 2' in style:
                headers_found += 1
                print(f"PASS: Component 2 — '{header}' has style '{style}'")
            else:
                actual = style if style else 'NOT FOUND'
                print(f"FAIL: Component 2 — '{header}' style is '{actual}', expected 'Heading 2'")

        if headers_found > 0:
            header_score = round(headers_found * 0.08, 4)
            total_score += header_score
            print(f"Component 2 subtotal: {headers_found}/5 headers correct = {header_score} pts")
        else:
            print("Component 2 subtotal: 0/5 headers correct = 0.0 pts")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: Measurement values in ingredient lines are bold (0.3 points)
    # In initial_env ingredient lines have one run (bold=False) — FAILS on initial.
    # In golden_env ingredient lines have two runs: first run bold=True (measurement),
    # second run bold=False (rest of ingredient text) — PASSES on golden.
    # Award partial credit: 0.075 per measurement (4 × 0.075 = 0.30)
    # -------------------------------------------------------------------
    try:
        measurements_bold = 0

        for para in paragraphs:
            para_text = para.text.strip()
            # Find ingredient lines containing a measurement prefix
            for measurement in EXPECTED_MEASUREMENTS:
                if para_text.startswith(measurement):
                    # The measurement token must be the text of a bold run
                    # Check each run: the measurement prefix must appear in a bold run
                    bold_runs_matching = [
                        run for run in para.runs
                        if run.font.bold is True
                        and run.text.strip().startswith(measurement)
                    ]
                    if bold_runs_matching:
                        measurements_bold += 1
                        print(f"PASS: Component 3 — '{measurement}' is bold in line '{para_text[:30]}'")
                    else:
                        run_details = [(r.text, r.font.bold) for r in para.runs]
                        print(f"FAIL: Component 3 — '{measurement}' not bold in '{para_text[:30]}', runs={run_details}")

        if measurements_bold > 0:
            measurement_score = round(measurements_bold * 0.075, 4)
            total_score += measurement_score
            print(f"Component 3 subtotal: {measurements_bold}/4 measurements bold = {measurement_score} pts")
        else:
            print("Component 3 subtotal: 0/4 measurements bold = 0.0 pts")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
