"""
Reward Script: Create a simple memo in LibreOffice Writer
Task ID: writer_wf_016
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): MEMORANDUM title — centered, bold, 16pt
  Component 2 (0.25): Four header fields (TO, FROM, DATE, RE) with correct content
  Component 3 (0.15): Horizontal line (paragraph bottom border) after header fields
  Component 4 (0.15): Three body paragraphs about leave policy
  Component 5 (0.20): Liberation Sans 11pt font for body text
"""

import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_016'


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice state."""
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

    paragraphs = doc.paragraphs
    if len(paragraphs) == 0:
        print("FAIL: Document has no paragraphs — appears blank")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: MEMORANDUM title — centered, bold, 16pt (0.25 points)
    try:
        p0 = paragraphs[0]
        title_text = p0.text.strip().upper()
        is_memo_title = "MEMORANDUM" in title_text

        # Check alignment is CENTER
        is_centered = p0.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER

        # Check bold and size on runs
        has_bold = False
        has_16pt = False
        for run in p0.runs:
            if run.font.bold:
                has_bold = True
            if run.font.size and abs(run.font.size.pt - 16.0) < 0.5:
                has_16pt = True

        if is_memo_title and is_centered and has_bold and has_16pt:
            print(f"PASS: Component 1 — MEMORANDUM title is centered, bold, 16pt (0.25 pts)")
            total_score += 0.25
        else:
            details = f"text_match={is_memo_title}, centered={is_centered}, bold={has_bold}, 16pt={has_16pt}"
            print(f"FAIL: Component 1 — MEMORANDUM title check: {details}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Four header fields (TO, FROM, DATE, RE) with correct content (0.25 points)
    try:
        # Look through paragraphs for the four required fields
        header_checks = {
            'TO': 'All Department Heads',
            'FROM': 'HR Director',
            'DATE': 'October 15, 2025',
            'RE': 'Updated Leave Policy',
        }
        found_headers = {}

        for p in paragraphs[1:6]:  # Search within first few paragraphs after title
            text = p.text.strip()
            for key, expected_val in header_checks.items():
                prefix = f"{key}:"
                if text.upper().startswith(prefix.upper()):
                    # Check that the value part contains expected content
                    val_part = text[len(prefix):].strip()
                    if expected_val.lower() in val_part.lower():
                        found_headers[key] = True

        num_found = len(found_headers)
        if num_found == 4:
            print(f"PASS: Component 2 — All 4 header fields found with correct content (0.25 pts)")
            total_score += 0.25
        elif num_found >= 2:
            partial = round(0.25 * num_found / 4, 2)
            print(f"PARTIAL: Component 2 — {num_found}/4 header fields found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {num_found}/4 header fields found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Horizontal line (paragraph bottom border) after header fields (0.15 points)
    try:
        # A horizontal line is typically implemented as a paragraph with a bottom border
        found_hline = False
        for p in paragraphs[1:7]:  # Search in paragraphs after title, before body
            pPr = p._element.find(qn('w:pPr'))
            if pPr is not None:
                pBdr = pPr.find(qn('w:pBdr'))
                if pBdr is not None:
                    bottom = pBdr.find(qn('w:bottom'))
                    if bottom is not None:
                        val = bottom.get(qn('w:val'))
                        if val and val != 'none':
                            found_hline = True
                            break

        if found_hline:
            print(f"PASS: Component 3 — Horizontal line (bottom border) found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — No horizontal line (paragraph bottom border) found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Three body paragraphs about leave policy (0.15 points)
    try:
        # Body paragraphs should come after the header section
        # Find paragraphs that are not title, not header fields, not empty/separator
        body_paras = []
        header_done = False
        for p in paragraphs[1:]:
            text = p.text.strip()
            # Skip header fields
            if any(text.upper().startswith(f"{k}:") for k in ['TO', 'FROM', 'DATE', 'RE']):
                continue
            # Skip empty paragraphs (separator lines)
            if not text:
                header_done = True
                continue
            # If we're past header section, these are body paragraphs
            if header_done or not any(text.upper().startswith(f"{k}:") for k in ['TO', 'FROM', 'DATE', 'RE']):
                if len(text) > 20:  # Must be substantial text, not just a word
                    body_paras.append(text)

        num_body = len(body_paras)
        if num_body >= 3:
            print(f"PASS: Component 4 — {num_body} body paragraphs found (0.15 pts)")
            total_score += 0.15
        elif num_body >= 1:
            partial = round(0.15 * num_body / 3, 2)
            print(f"PARTIAL: Component 4 — {num_body}/3 body paragraphs found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No body paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Liberation Sans 11pt font for body text (0.20 points)
    try:
        # Check body paragraph runs for Liberation Sans and 11pt
        body_runs_checked = 0
        liberation_sans_count = 0
        size_11_count = 0

        # Body paragraphs are indices 6, 7, 8 in golden (after title, 4 headers, separator)
        # But we detect dynamically: non-title, non-header, non-empty paragraphs
        for p in paragraphs:
            text = p.text.strip()
            # Skip title, headers, empty
            if not text or len(text) < 20:
                continue
            if text.upper() == 'MEMORANDUM':
                continue
            if any(text.upper().startswith(f"{k}:") for k in ['TO', 'FROM', 'DATE', 'RE']):
                continue
            # This is a body paragraph — check its runs
            for run in p.runs:
                if run.text.strip():
                    body_runs_checked += 1
                    if run.font.name and 'liberation sans' in run.font.name.lower():
                        liberation_sans_count += 1
                    if run.font.size and abs(run.font.size.pt - 11.0) < 0.5:
                        size_11_count += 1

        if body_runs_checked > 0:
            font_ok = liberation_sans_count >= body_runs_checked * 0.8
            size_ok = size_11_count >= body_runs_checked * 0.8
            if font_ok and size_ok:
                print(f"PASS: Component 5 — Body text uses Liberation Sans 11pt ({body_runs_checked} runs checked) (0.20 pts)")
                total_score += 0.20
            elif font_ok or size_ok:
                print(f"PARTIAL: Component 5 — font_ok={font_ok}, size_ok={size_ok} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Body runs: {liberation_sans_count}/{body_runs_checked} Liberation Sans, {size_11_count}/{body_runs_checked} 11pt")
        else:
            print(f"FAIL: Component 5 — No body runs found to check font")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
