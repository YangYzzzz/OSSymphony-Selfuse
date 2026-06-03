"""
Reward Script: Format academic paper with structured headings and generate TOC
Task ID: writer_pd_006
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Heading 1 count == 5
  Component 2 (0.25): Heading 2 count == 12
  Component 3 (0.20): Heading 3 count == 8
  Component 4 (0.30): TOC field code present with levels 1-3
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_006'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


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

    # Count heading styles
    heading1_count = 0
    heading2_count = 0
    heading3_count = 0
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ''
        if style_name == 'Heading 1':
            heading1_count += 1
        elif style_name == 'Heading 2':
            heading2_count += 1
        elif style_name == 'Heading 3':
            heading3_count += 1

    # Component 1: Heading 1 count == 5 (0.25 points)
    try:
        if heading1_count == 5:
            print(f"PASS: Component 1 — Heading 1 count is 5 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 5 Heading 1, found {heading1_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Heading 2 count == 12 (0.25 points)
    try:
        if heading2_count == 12:
            print(f"PASS: Component 2 — Heading 2 count is 12 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected 12 Heading 2, found {heading2_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Heading 3 count == 8 (0.20 points)
    try:
        if heading3_count == 8:
            print(f"PASS: Component 3 — Heading 3 count is 8 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected 8 Heading 3, found {heading3_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: TOC field code present covering levels 1-3 (0.30 points)
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        body = doc.element.body
        instrs = body.findall('.//w:instrText', ns)
        # Filter to TOC instrTexts that reference levels 1-3
        toc_instrs = [i for i in instrs
                      if 'TOC' in (i.text or '').upper() and '1-3' in (i.text or '')]

        if len(toc_instrs) > 0:
            print(f"PASS: Component 4 — TOC field code found with levels 1-3 (0.30 pts)")
            total_score += 0.30
        else:
            # Check for any TOC field at all
            any_toc = any('TOC' in (i.text or '').upper() for i in instrs)
            if any_toc:
                print(f"FAIL: Component 4 — TOC field found but does not cover levels 1-3")
            else:
                print(f"FAIL: Component 4 — No TOC field code found (instrTexts: {len(instrs)})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
