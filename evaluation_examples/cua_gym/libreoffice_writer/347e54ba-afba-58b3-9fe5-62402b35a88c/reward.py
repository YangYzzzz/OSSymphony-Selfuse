"""
Reward Script: Apply heading hierarchy to advanced_textbook.docx
Task ID: writer_struct_051
Domain: libreoffice_writer

Scoring:
  Component 1: 2 Heading 1 paragraphs applied correctly  — 0.3 points
  Component 2: 4 Heading 2 paragraphs applied correctly  — 0.4 points
  Component 3: 4 Heading 3 paragraphs applied correctly  — 0.3 points
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_051'
FILE_PATH = f'{WORKDIR}/advanced_textbook.docx'

# Exact paragraph texts and expected styles per task description
HEADING1_TEXTS = {
    'Part I: Foundations',
    'Part II: Applications',
}

HEADING2_TEXTS = {
    'Chapter 1: Theoretical Framework',
    'Chapter 2: Historical Context',
    'Chapter 3: Case Studies',
    'Chapter 4: Implementation',
}

HEADING3_TEXTS = {
    'Section 1.1: Core Axioms',
    'Section 1.2: Derived Principles',
    'Section 3.1: Legal Cases',
    'Section 3.2: Business Cases',
}


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

    # Build a dict: paragraph text -> style name (for non-empty paragraphs)
    para_styles = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            para_styles[text] = para.style.name

    # Component 1: Heading 1 applied to 'Part I: Foundations' and 'Part II: Applications' (0.3 points)
    try:
        h1_found = []
        h1_missing = []
        for expected_text in HEADING1_TEXTS:
            # Use startswith to handle exact match with potential trailing whitespace
            matched = None
            for text, style in para_styles.items():
                if text == expected_text:
                    matched = style
                    break
            if matched == 'Heading 1':
                h1_found.append(expected_text)
                print(f"PASS: '{expected_text}' has style 'Heading 1'")
            elif matched is not None:
                h1_missing.append(expected_text)
                print(f"FAIL: '{expected_text}' has style '{matched}', expected 'Heading 1'")
            else:
                h1_missing.append(expected_text)
                print(f"FAIL: '{expected_text}' not found in document")

        if len(h1_found) == 2:
            print(f"PASS: Component 1 — Both Heading 1 paragraphs correct (0.3 pts)")
            total_score += 0.3
        elif len(h1_found) == 1:
            print(f"PARTIAL: Component 1 — 1/2 Heading 1 paragraphs correct (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — 0/2 Heading 1 paragraphs correct")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Heading 2 applied to 4 chapter paragraphs (0.4 points)
    try:
        h2_found = []
        h2_missing = []
        for expected_text in HEADING2_TEXTS:
            matched = None
            for text, style in para_styles.items():
                if text == expected_text:
                    matched = style
                    break
            if matched == 'Heading 2':
                h2_found.append(expected_text)
                print(f"PASS: '{expected_text}' has style 'Heading 2'")
            elif matched is not None:
                h2_missing.append(expected_text)
                print(f"FAIL: '{expected_text}' has style '{matched}', expected 'Heading 2'")
            else:
                h2_missing.append(expected_text)
                print(f"FAIL: '{expected_text}' not found in document")

        n = len(h2_found)
        if n == 4:
            print(f"PASS: Component 2 — All 4 Heading 2 paragraphs correct (0.4 pts)")
            total_score += 0.4
        elif n == 3:
            print(f"PARTIAL: Component 2 — 3/4 Heading 2 paragraphs correct (0.3 pts)")
            total_score += 0.3
        elif n == 2:
            print(f"PARTIAL: Component 2 — 2/4 Heading 2 paragraphs correct (0.2 pts)")
            total_score += 0.2
        elif n == 1:
            print(f"PARTIAL: Component 2 — 1/4 Heading 2 paragraphs correct (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — 0/4 Heading 2 paragraphs correct")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Heading 3 applied to 4 section paragraphs (0.3 points)
    try:
        h3_found = []
        h3_missing = []
        for expected_text in HEADING3_TEXTS:
            matched = None
            for text, style in para_styles.items():
                if text == expected_text:
                    matched = style
                    break
            if matched == 'Heading 3':
                h3_found.append(expected_text)
                print(f"PASS: '{expected_text}' has style 'Heading 3'")
            elif matched is not None:
                h3_missing.append(expected_text)
                print(f"FAIL: '{expected_text}' has style '{matched}', expected 'Heading 3'")
            else:
                h3_missing.append(expected_text)
                print(f"FAIL: '{expected_text}' not found in document")

        n = len(h3_found)
        if n == 4:
            print(f"PASS: Component 3 — All 4 Heading 3 paragraphs correct (0.3 pts)")
            total_score += 0.3
        elif n == 3:
            print(f"PARTIAL: Component 3 — 3/4 Heading 3 paragraphs correct (0.225 pts)")
            total_score += 0.225
        elif n == 2:
            print(f"PARTIAL: Component 3 — 2/4 Heading 3 paragraphs correct (0.15 pts)")
            total_score += 0.15
        elif n == 1:
            print(f"PARTIAL: Component 3 — 1/4 Heading 3 paragraphs correct (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 3 — 0/4 Heading 3 paragraphs correct")
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
