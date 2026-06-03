"""
Reward Script: Envelope printing setup for mail merge
Task ID: writer_mt_012
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30) - Envelope page dimensions (#10: 9.5 x 4.125 inches, landscape)
  Component 2 (0.30) - Return address in upper-left with correct content
  Component 3 (0.25) - Recipient merge fields centered with correct content
  Component 4 (0.15) - Merge field format correctness (all 5 fields present)
"""

import os

from docx import Document
from docx.shared import Inches, Emu
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_012'

# Tolerance for dimension checks (in inches)
DIM_TOLERANCE = 0.25


def verify_task(file_path):
    """
    Verify envelope mail merge setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Envelope page dimensions - #10 format (0.30 points)
    # #10 envelope: 9.5" x 4.125" in landscape orientation
    # This check FAILS on initial (8.5x11 portrait) and PASSES on golden
    try:
        section = doc.sections[0]
        pw_in = section.page_width / 914400.0
        ph_in = section.page_height / 914400.0
        orient = section.orientation

        is_landscape = (orient == WD_ORIENT.LANDSCAPE)
        # Check dimensions: width ~9.5, height ~4.125 (landscape envelope)
        width_ok = abs(pw_in - 9.5) < DIM_TOLERANCE
        height_ok = abs(ph_in - 4.125) < DIM_TOLERANCE

        if is_landscape and width_ok and height_ok:
            print(f"PASS: Component 1 - Envelope #10 dimensions correct: {pw_in:.3f}x{ph_in:.3f}in landscape (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - Expected #10 envelope (9.5x4.125 landscape), found {pw_in:.3f}x{ph_in:.3f}in orient={orient}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Return address in upper-left (0.30 points)
    # The first paragraph must contain "Acme Corp", "123 Business Blvd", "Springfield, IL 62701"
    # and be left-aligned. This FAILS on initial (no paragraphs/text) and PASSES on golden.
    try:
        paragraphs = doc.paragraphs
        if len(paragraphs) < 1 or not paragraphs[0].text.strip():
            print(f"FAIL: Component 2 - No return address paragraph found (doc has {len(paragraphs)} paragraphs)")
        else:
            first_text = paragraphs[0].text
            has_acme = 'Acme Corp' in first_text
            has_blvd = '123 Business Blvd' in first_text
            has_springfield = 'Springfield' in first_text and 'IL' in first_text and '62701' in first_text

            # Alignment: left or None (default=left)
            align = paragraphs[0].paragraph_format.alignment
            is_left = (align is None or align == WD_PARAGRAPH_ALIGNMENT.LEFT)

            if has_acme and has_blvd and has_springfield and is_left:
                print(f"PASS: Component 2 - Return address correct and left-aligned (0.30 pts)")
                total_score += 0.30
            else:
                missing = []
                if not has_acme:
                    missing.append("'Acme Corp'")
                if not has_blvd:
                    missing.append("'123 Business Blvd'")
                if not has_springfield:
                    missing.append("'Springfield, IL 62701'")
                if not is_left:
                    missing.append(f"left-align (found {align})")
                print(f"FAIL: Component 2 - Return address issues: missing {', '.join(missing)}. Text: {first_text[:100]!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Recipient merge fields centered (0.25 points)
    # A center-aligned paragraph must contain merge field placeholders for recipient address.
    # This FAILS on initial (no text) and PASSES on golden.
    try:
        # Find center-aligned paragraph with RecipientName
        centered_recipient_para = next(
            (p for p in paragraphs
             if p.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER
             and 'RecipientName' in p.text),
            None
        )

        if centered_recipient_para is None:
            print(f"FAIL: Component 3 - No center-aligned paragraph with RecipientName found")
        else:
            text = centered_recipient_para.text
            has_street = 'Street' in text
            has_city = 'City' in text
            has_state = 'State' in text
            has_zip = 'Zip' in text

            if has_street and has_city and has_state and has_zip:
                print(f"PASS: Component 3 - Recipient merge fields centered with all address components (0.25 pts)")
                total_score += 0.25
            else:
                missing = [f for f in ['Street', 'City', 'State', 'Zip'] if f not in text]
                print(f"FAIL: Component 3 - Centered recipient paragraph missing fields: {missing}. Text: {text[:100]!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: All 5 merge fields present in correct format (0.15 points)
    # Check that all 5 data source fields appear as merge field placeholders.
    # This FAILS on initial (no text at all) and PASSES on golden.
    try:
        full_text = '\n'.join(p.text for p in paragraphs)
        required_fields = ['RecipientName', 'Street', 'City', 'State', 'Zip']
        found_fields = [f for f in required_fields if f in full_text]

        if len(found_fields) == 5:
            print(f"PASS: Component 4 - All 5 merge fields present: {found_fields} (0.15 pts)")
            total_score += 0.15
        else:
            missing = [f for f in required_fields if f not in full_text]
            print(f"FAIL: Component 4 - Missing merge fields: {missing}. Found: {found_fields}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
