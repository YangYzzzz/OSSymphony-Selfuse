"""
Reward Script: Apply numbered list with alternating indent levels to process_flow.docx
Task ID: writer_list_043
Domain: libreoffice_writer
Scoring:
  Component 1: All 6 paragraphs have numbered list applied (numId is set)  — 0.30 pts
  Component 2: Items 1, 3, 5 (0-indexed: 0, 2, 4) are at list level 0    — 0.35 pts
  Component 3: Items 2, 4, 6 (0-indexed: 1, 3, 5) are at list level 1    — 0.35 pts
  Total: 1.00

Task context:
  The file ~/Desktop/process_flow.docx originally has 6 plain text paragraphs.
  After the task: items 1, 3, 5 (positions 0, 2, 4) should be at list level 1 (ilvl=0),
  and items 2, 4, 6 (positions 1, 3, 5) should be indented as level 2 sub-items (ilvl=1).
"""

import os

# python-docx is available on the VM
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_list_043'

# Expected paragraph texts in order
EXPECTED_TEXTS = [
    "Receive customer order",
    "Validate order details and inventory",
    "Process payment transaction",
    "Generate shipping label",
    "Ship order to customer",
    "Send delivery confirmation email",
]

# Level-1 items (0-indexed positions): items 1, 3, 5 → indices 0, 2, 4
LEVEL1_INDICES = {0, 2, 4}
# Level-2 items (0-indexed positions): items 2, 4, 6 → indices 1, 3, 5
LEVEL2_INDICES = {1, 3, 5}


def get_num_properties(para):
    """Extract ilvl and numId from a paragraph's XML numPr element."""
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        return None, None
    numPr = pPr.find(qn('w:numPr'))
    if numPr is None:
        return None, None
    ilvl_el = numPr.find(qn('w:ilvl'))
    numId_el = numPr.find(qn('w:numId'))
    ilvl = int(ilvl_el.get(qn('w:val'))) if ilvl_el is not None else None
    numId = int(numId_el.get(qn('w:val'))) if numId_el is not None else None
    return ilvl, numId


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — treat failure as precondition gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition check: Verify correct number of paragraphs and text content
    paragraphs = [p for p in doc.paragraphs]
    non_empty = [p for p in paragraphs if p.text.strip()]
    if len(non_empty) < 6:
        print(f"CRITICAL: Expected at least 6 non-empty paragraphs, found {len(non_empty)}")
        print("REWARD: 0.0")
        return 0.0

    # Use first 6 non-empty paragraphs (the task items)
    task_paras = non_empty[:6]

    # Verify correct texts are present (precondition gate — not scored)
    for i, (para, expected) in enumerate(zip(task_paras, EXPECTED_TEXTS)):
        if expected.lower() not in para.text.lower():
            print(f"WARN: Para[{i}] text mismatch: expected {expected!r}, found {para.text!r}")

    # -----------------------------------------------------------------------
    # Component 1: All 6 paragraphs have a numbered list applied (numId > 0)
    # This checks that ANY numbering was applied at all (fails on initial_env
    # where all numIds are None).
    # Points: 0.30
    # -----------------------------------------------------------------------
    try:
        all_numbered = True
        missing_numbering = []
        for i, para in enumerate(task_paras):
            ilvl, numId = get_num_properties(para)
            if numId is None or numId == 0:
                all_numbered = False
                missing_numbering.append(i)
                print(f"FAIL: Component 1 — Para[{i}] '{para.text[:30]}' has no numbering (numId={numId})")

        if all_numbered:
            print(f"PASS: Component 1 — All 6 paragraphs have numbered list applied (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — {len(missing_numbering)} paragraph(s) missing numbering: indices {missing_numbering}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Items at positions 1, 3, 5 (0-indexed: 0, 2, 4) are
    # at list indent level 0 (ilvl=0), i.e., top-level numbered items.
    # Points: 0.35
    # -----------------------------------------------------------------------
    try:
        level1_correct = True
        level1_errors = []
        for idx in sorted(LEVEL1_INDICES):
            para = task_paras[idx]
            ilvl, numId = get_num_properties(para)
            if ilvl != 0:
                level1_correct = False
                level1_errors.append((idx, ilvl))
                print(f"FAIL: Component 2 — Para[{idx}] '{para.text[:30]}' expected ilvl=0, found ilvl={ilvl}")

        if level1_correct:
            print(f"PASS: Component 2 — Items 1,3,5 (indices 0,2,4) are at level 0 (ilvl=0) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — {len(level1_errors)} level-1 item(s) have wrong indent level: {level1_errors}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Items at positions 2, 4, 6 (0-indexed: 1, 3, 5) are
    # at list indent level 1 (ilvl=1), i.e., sub-items (1.1, 2.1, 3.1).
    # Points: 0.35
    # -----------------------------------------------------------------------
    try:
        level2_correct = True
        level2_errors = []
        for idx in sorted(LEVEL2_INDICES):
            para = task_paras[idx]
            ilvl, numId = get_num_properties(para)
            if ilvl != 1:
                level2_correct = False
                level2_errors.append((idx, ilvl))
                print(f"FAIL: Component 3 — Para[{idx}] '{para.text[:30]}' expected ilvl=1, found ilvl={ilvl}")

        if level2_correct:
            print(f"PASS: Component 3 — Items 2,4,6 (indices 1,3,5) are at level 1 (ilvl=1) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — {len(level2_errors)} level-2 item(s) have wrong indent level: {level2_errors}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/process_flow.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
