"""
Reward Script: Modify TOC title style
Task ID: writer_mt_058
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Title text is 'TABLE OF CONTENTS' (all caps)
  Component 2 (0.3): Title font is 18pt bold
  Component 3 (0.4): Title paragraph is center-aligned
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_058'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def find_toc_title_para(doc):
    """
    Find the TOC title paragraph. We look for a paragraph whose text
    resembles 'Table of Contents' or 'TABLE OF CONTENTS' (case-insensitive).
    It should appear early in the document (within the first ~20 paragraphs).
    """
    for i, para in enumerate(doc.paragraphs[:30]):
        text = para.text.strip()
        if text.lower().replace(' ', '') == 'tableofcontents':
            return para, i
    return None, -1


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the TOC title paragraph
    toc_para, toc_idx = find_toc_title_para(doc)
    if toc_para is None:
        print("FAIL: Could not find a TOC title paragraph matching 'table of contents'")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found TOC title at paragraph index {toc_idx}: {repr(toc_para.text)}")

    # Component 1: Title text is 'TABLE OF CONTENTS' in all caps (0.3 points)
    try:
        title_text = toc_para.text.strip()
        if title_text == 'TABLE OF CONTENTS':
            print(f"PASS: Component 1 -- Title text is 'TABLE OF CONTENTS' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- Expected 'TABLE OF CONTENTS', found: {repr(title_text)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Title font is 18pt and bold (0.3 points)
    try:
        runs = toc_para.runs
        if not runs:
            print(f"FAIL: Component 2 -- No runs found in TOC title paragraph")
        else:
            # Check all non-empty runs for bold + 18pt
            content_runs = [r for r in runs if r.text.strip()]
            bold_ok = all(r.font.bold is True for r in content_runs) if content_runs else False
            size_ok = all(r.font.size is not None and r.font.size.pt == 18.0 for r in content_runs) if content_runs else False

            if bold_ok and size_ok:
                print(f"PASS: Component 2 -- Title is 18pt bold (0.3 pts)")
                total_score += 0.3
            else:
                # Report details
                for run in runs:
                    if run.text.strip():
                        sz = run.font.size.pt if run.font.size else None
                        print(f"  Run: text={repr(run.text[:40])}, bold={run.font.bold}, size={sz}")
                if not bold_ok:
                    print(f"FAIL: Component 2 -- Title is not bold")
                if not size_ok:
                    print(f"FAIL: Component 2 -- Title is not 18pt")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Title paragraph is center-aligned (0.4 points)
    try:
        alignment = toc_para.paragraph_format.alignment
        if alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            print(f"PASS: Component 3 -- Title is center-aligned (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 -- Expected CENTER alignment, found: {alignment}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
