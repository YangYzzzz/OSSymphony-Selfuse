"""
Reward Script: Verify brand color palette applied to section heading borders
Task ID: writer_tech_076
Domain: libreoffice_writer
Scoring:
  - 5 components (0.2 each): each Heading 1 paragraph must have a bottom border
    with the correct brand color (not the initial black #000000).
  - Component 1: "Architecture Overview"      -> #1976D2 (Primary Blue)
  - Component 2: "API Reference"              -> #607D8B (Secondary Gray)
  - Component 3: "Deployment Pipeline"        -> #43A047 (Accent Green)
  - Component 4: "Security Controls"          -> #FB8C00 (Warning Orange)
  - Component 5: "Monitoring & Observability" -> #E53935 (Error Red)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_076'

# Expected brand colors for each heading (order matters)
EXPECTED_COLORS = [
    ("1. Architecture Overview",      "1976D2"),
    ("2. API Reference",              "607D8B"),
    ("3. Deployment Pipeline",        "43A047"),
    ("4. Security Controls",          "FB8C00"),
    ("5. Monitoring & Observability", "E53935"),
]

POINTS_PER_HEADING = 0.2


def get_bottom_border_color(para):
    """Extract the bottom border color from a paragraph's XML properties."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        return None
    bottom = pBdr.find(qn('w:bottom'))
    if bottom is None:
        return None
    color = bottom.get(qn('w:color'))
    return color.upper() if color else None


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

    # Collect all Heading 1 paragraphs in order
    heading_paras = []
    for para in doc.paragraphs:
        if para.style and para.style.name == 'Heading 1':
            heading_paras.append(para)

    if len(heading_paras) < 5:
        print(f"FAIL: Expected 5 Heading 1 paragraphs, found {len(heading_paras)}")
        print(f"REWARD: 0.0")
        return 0.0

    # Check each heading's bottom border color
    for idx, (expected_text, expected_color) in enumerate(EXPECTED_COLORS):
        comp_num = idx + 1
        try:
            para = heading_paras[idx]
            actual_text = para.text.strip()
            actual_color = get_bottom_border_color(para)

            # Normalize for comparison
            expected_upper = expected_color.upper()
            actual_upper = actual_color.upper() if actual_color else None

            # The key check: border color must be the brand color, NOT black (000000)
            if actual_upper == expected_upper:
                print(f"PASS: Component {comp_num} -- '{actual_text}' has bottom border color #{actual_upper} ({POINTS_PER_HEADING} pts)")
                total_score += POINTS_PER_HEADING
            else:
                print(f"FAIL: Component {comp_num} -- '{actual_text}' expected border color #{expected_upper}, found #{actual_upper}")
        except Exception as e:
            print(f"ERROR: Component {comp_num} -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
