"""
Reward Script: Create footer with case number and page number
Task ID: writer_legal_023
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Footer is active (not linked_to_previous / has content)
  Component 2 (0.35): Footer contains 'Case No. 2024-CV-03891' text
  Component 3 (0.35): Footer contains a PAGE field code for page numbering
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_023'

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
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

    # Precondition: document must have at least one section
    if len(doc.sections) == 0:
        print("FAIL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    # Collect all footer paragraph texts and XML across sections
    footer_texts = []
    footer_instr_texts = []
    for section in doc.sections:
        footer = section.footer
        for para in footer.paragraphs:
            footer_texts.append(para.text)
            for it in para._element.findall('.//w:instrText', NS):
                if it.text:
                    footer_instr_texts.append(it.text)

    # Component 1: Footer is active and has text content (0.3 points)
    # FAILS on initial (footer empty), PASSES on golden
    try:
        if any(t.strip() for t in footer_texts):
            print(f"PASS: Component 1 — Footer has content (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Footer has no text content")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footer contains 'Case No. 2024-CV-03891' (0.35 points)
    # FAILS on initial (no footer text), PASSES on golden
    try:
        if any('Case No. 2024-CV-03891' in t for t in footer_texts):
            print(f"PASS: Component 2 — Footer contains 'Case No. 2024-CV-03891' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Footer does not contain 'Case No. 2024-CV-03891'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer contains a PAGE field code (0.35 points)
    # FAILS on initial (no field codes), PASSES on golden
    try:
        if any('PAGE' in instr.upper() for instr in footer_instr_texts):
            print(f"PASS: Component 3 — Footer contains PAGE field code (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — Footer does not contain a PAGE field code")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
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
