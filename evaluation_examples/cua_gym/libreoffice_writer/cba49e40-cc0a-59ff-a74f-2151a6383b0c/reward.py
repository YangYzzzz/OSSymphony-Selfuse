"""
Reward Script: Apply Body Text style to content paragraphs in a white paper
Task ID: writer_para_037
Domain: libreoffice_writer
Scoring:
  Component 1: Paragraph 3 has 'Body Text' style (0.25 points)
  Component 2: Paragraph 5 has 'Body Text' style (0.25 points)
  Component 3: Paragraph 7 has 'Body Text' style (0.25 points)
  Component 4: Paragraph 9 has 'Body Text' style (0.25 points)
  Precondition gate: Heading paragraphs (1, 2, 4, 6, 8) must retain their styles
Total: 1.0

Note: Heading style preservation is a precondition gate (not scored) since those styles
are also present in the initial document and don't represent task-introduced changes.
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_para_037'


def verify_task(file_path):
    """
    Verify that paragraphs 3, 5, 7, and 9 have 'Body Text' style applied.
    Each paragraph style change earns 0.25 points (total: 1.0).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Validate the document has at least 9 paragraphs
    paragraphs = doc.paragraphs
    if len(paragraphs) < 9:
        print(f"CRITICAL: Document has only {len(paragraphs)} paragraphs, expected at least 9")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: Heading paragraphs must retain their original styles
    # (This is a gate, not a scoring component — heading styles are pre-existing in initial_env)
    try:
        heading_checks = {
            1: (paragraphs[0].style.name, 'Heading 1'),
            2: (paragraphs[1].style.name, 'Heading 2'),
            4: (paragraphs[3].style.name, 'Heading 2'),
            6: (paragraphs[5].style.name, 'Heading 2'),
            8: (paragraphs[7].style.name, 'Heading 2'),
        }
        for para_num, (actual_style, expected_style) in heading_checks.items():
            if actual_style != expected_style:
                print(f"GATE FAIL: Paragraph {para_num} has style '{actual_style}', expected '{expected_style}'")
                print("REWARD: 0.0")
                return 0.0
        print("GATE PASS: All heading paragraphs retain correct styles (not scored — precondition)")
    except Exception as e:
        print(f"GATE ERROR: Could not check heading styles: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Paragraph 3 has 'Body Text' style (0.25 points)
    # Paragraph 3 is the content under 'Introduction' heading
    try:
        para3 = paragraphs[2]  # 0-indexed: index 2 = paragraph 3
        p3_style = para3.style.name
        if p3_style == 'Body Text':
            print(f"PASS: Component 1 — Paragraph 3 has 'Body Text' style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Paragraph 3 has style '{p3_style}', expected 'Body Text'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraph 5 has 'Body Text' style (0.25 points)
    # Paragraph 5 is the content under 'Current Challenges' heading
    try:
        para5 = paragraphs[4]  # 0-indexed: index 4 = paragraph 5
        p5_style = para5.style.name
        if p5_style == 'Body Text':
            print(f"PASS: Component 2 — Paragraph 5 has 'Body Text' style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Paragraph 5 has style '{p5_style}', expected 'Body Text'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraph 7 has 'Body Text' style (0.25 points)
    # Paragraph 7 is the content under 'Proposed Solution' heading
    try:
        para7 = paragraphs[6]  # 0-indexed: index 6 = paragraph 7
        p7_style = para7.style.name
        if p7_style == 'Body Text':
            print(f"PASS: Component 3 — Paragraph 7 has 'Body Text' style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Paragraph 7 has style '{p7_style}', expected 'Body Text'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Paragraph 9 has 'Body Text' style (0.25 points)
    # Paragraph 9 is the content under 'Implementation Roadmap' heading
    try:
        para9 = paragraphs[8]  # 0-indexed: index 8 = paragraph 9
        p9_style = para9.style.name
        if p9_style == 'Body Text':
            print(f"PASS: Component 4 — Paragraph 9 has 'Body Text' style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Paragraph 9 has style '{p9_style}', expected 'Body Text'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
