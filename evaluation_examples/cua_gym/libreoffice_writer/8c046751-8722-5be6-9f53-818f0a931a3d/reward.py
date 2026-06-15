"""
Reward Script: Insert bibliography section with 5 entries in hanging indent format
Task ID: writer_biz_077
Domain: libreoffice_writer
Scoring:
  Component 1: References/Bibliography heading exists with Heading 1 style (0.2 pts)
  Component 2: Heading is at end of document (after Conclusion) (0.1 pts)
  Component 3: Exactly 5 bibliography entries present (0.3 pts)
  Component 4: Entries have hanging indent formatting (0.2 pts)
  Component 5: Entries contain proper bibliographic fields (author, title, year, publisher) (0.2 pts)
"""

import os
import re
from docx import Document
from docx.shared import Emu

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_077'


def persist_app_state(domain):
    """Save any unsaved edits in LibreOffice Writer."""
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

    paragraphs = doc.paragraphs

    # Find a References/Bibliography heading
    ref_heading_idx = None
    ref_heading_text = None
    for i, p in enumerate(paragraphs):
        if p.style and p.style.name.startswith('Heading') and re.search(r'(?i)\b(references|bibliography)\b', p.text):
            ref_heading_idx = i
            ref_heading_text = p.text.strip()
            break

    # Component 1: References/Bibliography heading exists with Heading 1 style (0.2 pts)
    try:
        if ref_heading_idx is not None:
            heading_style = paragraphs[ref_heading_idx].style.name
            if heading_style == 'Heading 1':
                print(f"PASS: Component 1 — References heading found with Heading 1 style: '{ref_heading_text}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — References heading found but style is '{heading_style}', expected 'Heading 1'")
        else:
            print("FAIL: Component 1 — No References/Bibliography heading found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Heading is at end of document, after Conclusion section (0.1 pts)
    try:
        if ref_heading_idx is not None:
            # Find the Conclusion heading
            conclusion_idx = None
            for i, p in enumerate(paragraphs):
                if p.style and p.style.name.startswith('Heading') and re.search(r'(?i)\bconclusion\b', p.text):
                    conclusion_idx = i
                    break
            if conclusion_idx is not None and ref_heading_idx > conclusion_idx:
                print(f"PASS: Component 2 — References heading (idx={ref_heading_idx}) is after Conclusion (idx={conclusion_idx}) (0.1 pts)")
                total_score += 0.1
            elif conclusion_idx is None:
                print("FAIL: Component 2 — Could not find Conclusion heading to verify ordering")
            else:
                print(f"FAIL: Component 2 — References heading (idx={ref_heading_idx}) is NOT after Conclusion (idx={conclusion_idx})")
        else:
            print("FAIL: Component 2 — No References heading found, cannot check position")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Identify bibliography entries: paragraphs after the References heading that start with [N]
    bib_entries = []
    if ref_heading_idx is not None:
        for i in range(ref_heading_idx + 1, len(paragraphs)):
            p = paragraphs[i]
            # Stop if we hit another heading
            if p.style and p.style.name.startswith('Heading'):
                break
            text = p.text.strip()
            if text and re.match(r'^\[\d+\]', text):
                bib_entries.append((i, p))

    # Component 3: Exactly 5 bibliography entries present (0.3 pts)
    # Award partial: 0.06 per entry up to 5
    try:
        num_entries = len(bib_entries)
        if num_entries >= 5:
            print(f"PASS: Component 3 — Found {num_entries} bibliography entries (0.3 pts)")
            total_score += 0.3
        elif num_entries > 0:
            partial = num_entries * 0.06
            print(f"PARTIAL: Component 3 — Found {num_entries}/5 bibliography entries ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 3 — No bibliography entries found after References heading")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Entries have hanging indent formatting (0.2 pts)
    # Hanging indent = positive left_indent + negative first_line_indent
    try:
        if len(bib_entries) > 0:
            hanging_count = 0
            for idx, p in bib_entries[:5]:
                pf = p.paragraph_format
                left = pf.left_indent
                first = pf.first_line_indent
                if left is not None and left > 0 and first is not None and first < 0:
                    hanging_count += 1
                else:
                    print(f"  INFO: Entry at idx={idx} — left_indent={left}, first_indent={first} (not hanging)")

            if hanging_count == len(bib_entries[:5]):
                print(f"PASS: Component 4 — All {hanging_count} entries have hanging indent (0.2 pts)")
                total_score += 0.2
            elif hanging_count > 0:
                partial = 0.2 * (hanging_count / len(bib_entries[:5]))
                print(f"PARTIAL: Component 4 — {hanging_count}/{len(bib_entries[:5])} entries have hanging indent ({partial:.2f} pts)")
                total_score += partial
            else:
                print("FAIL: Component 4 — No entries have hanging indent formatting")
        else:
            print("FAIL: Component 4 — No bibliography entries to check indent")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Entries contain proper bibliographic fields (0.2 pts)
    # Each entry should have: author (text before year), year (4-digit), title, publisher/journal
    # We check: has a 4-digit year, has at least 3 comma-separated parts (author, title, source)
    try:
        if len(bib_entries) > 0:
            proper_count = 0
            for idx, p in bib_entries[:5]:
                text = p.text.strip()
                has_year = bool(re.search(r'\b(19|20)\d{2}\b', text))
                # Remove the [N] prefix for field analysis
                content = re.sub(r'^\[\d+\]\s*', '', text)
                # Check for multiple segments (author, title, source, etc.)
                # A proper bib entry typically has commas and periods separating fields
                has_enough_fields = len(content.split(',')) >= 2 and len(content) > 40
                if has_year and has_enough_fields:
                    proper_count += 1
                else:
                    print(f"  INFO: Entry [{idx}] missing fields — year={has_year}, fields={has_enough_fields}: {text[:80]}")

            if proper_count == len(bib_entries[:5]):
                print(f"PASS: Component 5 — All {proper_count} entries have proper bibliographic fields (0.2 pts)")
                total_score += 0.2
            elif proper_count > 0:
                partial = 0.2 * (proper_count / len(bib_entries[:5]))
                print(f"PARTIAL: Component 5 — {proper_count}/{len(bib_entries[:5])} entries have proper fields ({partial:.2f} pts)")
                total_score += partial
            else:
                print("FAIL: Component 5 — No entries have proper bibliographic fields")
        else:
            print("FAIL: Component 5 — No bibliography entries to check fields")
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
