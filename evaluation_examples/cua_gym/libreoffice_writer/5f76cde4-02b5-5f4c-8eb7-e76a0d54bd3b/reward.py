"""
Reward Script: Demote items 2, 4, and 6 in numbered list to level 2 sub-items
Task ID: writer_list_027
Domain: libreoffice_writer
Scoring:
  Component 1: "Design promotional materials" demoted to list level 2 (0.35 pts)
  Component 2: "Monitor engagement metrics" demoted to list level 2 (0.35 pts)
  Component 3: "Prepare summary report" demoted to list level 2 (0.30 pts)
  Total: 1.0

Verification strategy:
  - Load the .docx file from ~/Desktop/task_breakdown.docx
  - For each target paragraph, check either:
      (a) The paragraph style is 'List Number 2' (the python-docx style name for level-2 numbering), OR
      (b) The paragraph has an explicit ilvl=1 in its numPr XML element
  - The three level-1 paragraphs (Plan..., Execute..., Analyze...) must remain at level 1.
  - Initial env: all paragraphs are 'List Number' style at ilvl=0 → score 0.0
  - Golden env: items 2, 4, 6 (1-indexed) promoted to 'List Number 2' → score 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_list_027'
FILE_PATH = f'{WORKDIR}/Desktop/task_breakdown.docx'

# Target texts that should be demoted to level 2
LEVEL2_TARGETS = [
    "Design promotional materials",
    "Monitor engagement metrics",
    "Prepare summary report",
]

# Texts that must remain at level 1
LEVEL1_TARGETS = [
    "Plan the marketing campaign",
    "Execute social media strategy",
    "Analyze campaign results",
]


def get_para_ilvl(para):
    """
    Return the list indent level (ilvl) for a paragraph.
    Returns the integer ilvl if explicitly set in numPr, else None.
    """
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        return None
    numPr = pPr.find(qn('w:numPr'))
    if numPr is None:
        return None
    ilvl_elem = numPr.find(qn('w:ilvl'))
    if ilvl_elem is None:
        return None
    val = ilvl_elem.get(qn('w:val'))
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def is_at_level2(para):
    """
    Determine if a paragraph has been demoted to list level 2.
    Accept either:
      - style name is 'List Number 2' (or contains '2' for level 2 numbering styles)
      - explicit ilvl == 1 in numPr XML
    """
    style_name = para.style.name if para.style else ""
    # Style-based detection (python-docx uses 'List Number 2' for level 2)
    if "List Number 2" in style_name:
        return True
    # XML-based detection: ilvl=1 means level 2 (0-indexed)
    ilvl = get_para_ilvl(para)
    if ilvl is not None and ilvl >= 1:
        return True
    return False


def verify_task(file_path):
    """
    Verify task completion: items 2, 4, 6 demoted to list level 2.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a text -> paragraph lookup
    para_map = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            para_map[text] = para

    # Precondition: verify all expected paragraphs exist
    all_texts = list(para_map.keys())
    for expected in LEVEL2_TARGETS + LEVEL1_TARGETS:
        if expected not in para_map:
            print(f"PRECONDITION FAIL: paragraph '{expected}' not found in document")
            print(f"  Found paragraphs: {all_texts}")
            print("REWARD: 0.0")
            return 0.0

    print(f"PRECONDITION PASS: all 6 expected paragraphs found")

    # Component 1: "Design promotional materials" is at level 2 (0.35 points)
    try:
        para = para_map["Design promotional materials"]
        style_name = para.style.name if para.style else "None"
        ilvl = get_para_ilvl(para)
        at_level2 = is_at_level2(para)
        if at_level2:
            print(f"PASS: Component 1 — 'Design promotional materials' is at level 2 "
                  f"(style='{style_name}', ilvl={ilvl}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — 'Design promotional materials' is NOT at level 2 "
                  f"(style='{style_name}', ilvl={ilvl}); expected 'List Number 2' or ilvl=1")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: "Monitor engagement metrics" is at level 2 (0.35 points)
    try:
        para = para_map["Monitor engagement metrics"]
        style_name = para.style.name if para.style else "None"
        ilvl = get_para_ilvl(para)
        at_level2 = is_at_level2(para)
        if at_level2:
            print(f"PASS: Component 2 — 'Monitor engagement metrics' is at level 2 "
                  f"(style='{style_name}', ilvl={ilvl}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — 'Monitor engagement metrics' is NOT at level 2 "
                  f"(style='{style_name}', ilvl={ilvl}); expected 'List Number 2' or ilvl=1")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "Prepare summary report" is at level 2 (0.30 points)
    try:
        para = para_map["Prepare summary report"]
        style_name = para.style.name if para.style else "None"
        ilvl = get_para_ilvl(para)
        at_level2 = is_at_level2(para)
        if at_level2:
            print(f"PASS: Component 3 — 'Prepare summary report' is at level 2 "
                  f"(style='{style_name}', ilvl={ilvl}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — 'Prepare summary report' is NOT at level 2 "
                  f"(style='{style_name}', ilvl={ilvl}); expected 'List Number 2' or ilvl=1")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
