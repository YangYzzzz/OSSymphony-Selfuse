"""
Reward Script: Insert paragraph below 'Section 3: Methodology' heading
Task ID: writer_edit_034
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5): New paragraph with exact required text exists in document
  - Component 2 (0.3): New paragraph is positioned between heading and 'Data was collected from...'
  - Component 3 (0.2): New paragraph uses Normal (body text) style, not a heading
Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_034'

TARGET_TEXT = 'This section describes the research methodology used in this study.'
HEADING_TEXT = 'Section 3: Methodology'
FOLLOWING_TEXT_START = 'Data was collected from'


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

    paragraphs = doc.paragraphs

    # Component 1: New paragraph with exact required text exists in document (0.5 points)
    # This paragraph should NOT exist in the initial file, only in the golden file.
    try:
        new_para_found = False
        new_para_idx = -1
        for idx, para in enumerate(paragraphs):
            if para.text.strip() == TARGET_TEXT:
                new_para_found = True
                new_para_idx = idx
                break

        if new_para_found:
            print(f"PASS: Component 1 — New paragraph with required text found at index {new_para_idx} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected paragraph '{TARGET_TEXT}' not found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: New paragraph is positioned correctly — after heading 'Section 3: Methodology'
    # and before the paragraph starting with 'Data was collected from' (0.3 points)
    try:
        if new_para_idx >= 0:
            # Check that the paragraph immediately before is the Section 3 heading
            prev_ok = False
            next_ok = False

            if new_para_idx > 0:
                prev_para = paragraphs[new_para_idx - 1]
                if prev_para.text.strip() == HEADING_TEXT:
                    prev_ok = True
                    print(f"  INFO: Paragraph before new para is heading '{prev_para.text.strip()}' (correct)")
                else:
                    print(f"  FAIL: Paragraph before new para is '{prev_para.text.strip()}', expected '{HEADING_TEXT}'")
            else:
                print(f"  FAIL: New paragraph is at index 0 — cannot have heading before it")

            if new_para_idx < len(paragraphs) - 1:
                next_para = paragraphs[new_para_idx + 1]
                if next_para.text.strip().startswith(FOLLOWING_TEXT_START):
                    next_ok = True
                    print(f"  INFO: Paragraph after new para starts with '{FOLLOWING_TEXT_START}' (correct)")
                else:
                    print(f"  FAIL: Paragraph after new para is '{next_para.text.strip()[:80]}', expected to start with '{FOLLOWING_TEXT_START}'")
            else:
                print(f"  FAIL: New paragraph is last — no following paragraph found")

            if prev_ok and next_ok:
                print(f"PASS: Component 2 — New paragraph correctly positioned between heading and body text (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — New paragraph not in correct position")
        else:
            print(f"FAIL: Component 2 — Cannot check position because new paragraph not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: New paragraph uses Normal (body text) style, not a heading (0.2 points)
    try:
        if new_para_idx >= 0:
            new_para = paragraphs[new_para_idx]
            style_name = new_para.style.name if new_para.style else 'Unknown'
            # Accept 'Normal' or 'Body Text' styles (not Heading styles)
            is_normal_style = 'Heading' not in style_name and 'Title' not in style_name
            if is_normal_style:
                print(f"PASS: Component 3 — New paragraph style is '{style_name}' (non-heading, 0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — New paragraph style is '{style_name}', expected a Normal/body style")
        else:
            print(f"FAIL: Component 3 — Cannot check style because new paragraph not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in Desktop
file_path = f'{WORKDIR}/Desktop/research_report.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
