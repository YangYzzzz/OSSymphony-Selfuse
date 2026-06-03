"""
Reward Script: Apply Heading 2 style to subsection titles in employee handbook
Task ID: writer_hr_018
Domain: libreoffice_writer
Scoring:
  - 0.2 points per subsection title correctly styled as 'Heading 2'
  - 5 subsections: Eligibility, Coverage Period, Claims Process, Appeals, Contact Information
  - Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_018'

# The 5 subsection titles that must have Heading 2 style applied
EXPECTED_HEADINGS = [
    'Eligibility',
    'Coverage Period',
    'Claims Process',
    'Appeals',
    'Contact Information',
]

POINTS_PER_HEADING = 0.2


def verify_task(file_path):
    """
    Verify that all 5 subsection titles have Heading 2 paragraph style.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a lookup: paragraph text (stripped) -> style name
    para_styles = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            para_styles[text] = para.style.name if para.style else 'None'

    # Check each expected subsection title
    for heading_text in EXPECTED_HEADINGS:
        try:
            style = para_styles.get(heading_text)
            if style is None:
                print(f"FAIL: Subsection '{heading_text}' not found in document")
            elif style == 'Heading 2':
                print(f"PASS: '{heading_text}' has style 'Heading 2' ({POINTS_PER_HEADING} pts)")
                total_score += POINTS_PER_HEADING
            else:
                print(f"FAIL: '{heading_text}' has style '{style}', expected 'Heading 2'")
        except Exception as e:
            print(f"ERROR: Could not check '{heading_text}': {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
