"""
Reward Script: Modify TOC heading to 'TABLE OF CONTENTS' in Heading 1, centered, no chapter number
Task ID: writer_acad_034
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): TOC heading text is "TABLE OF CONTENTS" (uppercase)
  Component 2 (0.30): TOC heading paragraph uses Heading 1 style
  Component 3 (0.20): TOC heading paragraph is center-aligned
  Component 4 (0.15): No chapter number prefix on the TOC heading
"""

import os
import re
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_034'


def persist_app_state(domain):
    """Best-effort save any unsaved LibreOffice edits."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def find_toc_heading(doc):
    """
    Find the TOC heading paragraph. We look for a paragraph whose text
    contains 'table of contents' (case-insensitive) near the top of the document
    (before the actual chapter content begins), typically within the first ~20 paragraphs.
    """
    for i, para in enumerate(doc.paragraphs):
        if i > 40:
            break
        text = para.text.strip()
        if text and 'table of contents' in text.lower():
            return para, i
    return None, -1


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

    # Find the TOC heading paragraph
    toc_para, toc_idx = find_toc_heading(doc)
    if toc_para is None:
        print("CRITICAL: Could not find any paragraph containing 'Table of Contents'")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found TOC heading at paragraph index {toc_idx}: '{toc_para.text}'")
    print(f"INFO: Style='{toc_para.style.name}', Alignment={toc_para.paragraph_format.alignment}")

    # Component 1: TOC heading text is "TABLE OF CONTENTS" (0.35 points)
    # Initial has "Table of Contents" (mixed case); golden should have "TABLE OF CONTENTS"
    try:
        toc_text = toc_para.text.strip()
        if toc_text == "TABLE OF CONTENTS":
            print(f"PASS: Component 1 -- TOC text is 'TABLE OF CONTENTS' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- Expected 'TABLE OF CONTENTS', found '{toc_text}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: TOC heading uses Heading 1 style (0.30 points)
    # Initial has style 'Normal'; golden should have 'Heading 1'
    try:
        style_name = toc_para.style.name if toc_para.style else "None"
        if style_name == "Heading 1":
            print(f"PASS: Component 2 -- TOC style is 'Heading 1' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- Expected style 'Heading 1', found '{style_name}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: TOC heading is center-aligned (0.20 points)
    # Initial has LEFT alignment; golden should have CENTER
    try:
        alignment = toc_para.paragraph_format.alignment
        if alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            print(f"PASS: Component 3 -- TOC is center-aligned (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- Expected CENTER alignment, found {alignment}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Correct text with Heading 1 style and no chapter number prefix (0.15 points)
    # The task requires: text "TABLE OF CONTENTS" in Heading 1 style WITHOUT a chapter number prefix.
    # This compound check ensures the heading is properly formatted as a whole:
    # uppercase text + Heading 1 style + no numbering prefix.
    # This FAILS on initial (which has "Table of Contents" in Normal style).
    try:
        toc_text = toc_para.text.strip()
        style_name = toc_para.style.name if toc_para.style else "None"
        # Check for common chapter numbering patterns at start of text
        has_number_prefix = bool(re.match(r'^\d+[\.\s:]', toc_text)) or \
                           bool(re.match(r'^Chapter\s+\d+', toc_text, re.IGNORECASE))

        if toc_text == "TABLE OF CONTENTS" and style_name == "Heading 1" and not has_number_prefix:
            print(f"PASS: Component 4 -- Heading 1 + uppercase + no chapter prefix (0.15 pts)")
            total_score += 0.15
        else:
            reasons = []
            if toc_text != "TABLE OF CONTENTS":
                reasons.append(f"text is '{toc_text}' not 'TABLE OF CONTENTS'")
            if style_name != "Heading 1":
                reasons.append(f"style is '{style_name}' not 'Heading 1'")
            if has_number_prefix:
                reasons.append("chapter number prefix detected")
            print(f"FAIL: Component 4 -- {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
