"""
Reward Script: Create envelope with addressee and return address in Writer document
Task ID: writer_lec_036
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.25): Envelope section exists (landscape, envelope-sized page)
  - Component 2 (0.25): Return address contains correct sender info
  - Component 3 (0.30): Addressee contains correct recipient info
  - Component 4 (0.20): Addressee is indented/positioned to the right of return address
"""

import os
from docx import Document
from docx.shared import Inches, Emu
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_036'


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify envelope creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sections = doc.sections
    paragraphs = doc.paragraphs

    # Component 1: Envelope section exists (0.25 points)
    # The golden doc has 2 sections; section 0 is the envelope (landscape, ~9.5 x 4.1 inches)
    # The initial doc has only 1 section (portrait, standard letter size)
    # We check: at least 2 sections AND one section has landscape orientation with height < 6 inches (envelope-sized)
    try:
        envelope_section = None
        if len(sections) >= 2:
            for sec in sections:
                height_in = sec.page_height / 914400.0
                width_in = sec.page_width / 914400.0
                # Envelope: landscape orientation with small height (< 6 inches) and width > height
                if height_in < 6.0 and width_in > height_in:
                    envelope_section = sec
                    break

        if envelope_section is not None:
            print(f"PASS: Component 1 -- Envelope section found "
                  f"({envelope_section.page_width/914400:.2f} x {envelope_section.page_height/914400:.2f} in) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- No envelope section found. "
                  f"Sections: {len(sections)}, need >=2 with one envelope-sized landscape section")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Return address contains correct sender info (0.25 points)
    # Expected: John Smith, 456 Oak Street, Boston, MA 02101
    try:
        all_text = ' '.join(p.text for p in paragraphs).lower()
        sender_checks = [
            'john smith' in all_text,
            '456 oak street' in all_text,
            'boston' in all_text,
            '02101' in all_text,
        ]
        sender_pass_count = sum(sender_checks)

        if sender_pass_count == 4:
            print(f"PASS: Component 2 -- Return address complete: John Smith, 456 Oak Street, Boston, MA 02101 (0.25 pts)")
            total_score += 0.25
        elif sender_pass_count >= 2:
            partial = 0.25 * (sender_pass_count / 4.0)
            print(f"PARTIAL: Component 2 -- Return address {sender_pass_count}/4 items found ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Return address missing or incomplete. Found {sender_pass_count}/4 items")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Addressee contains correct recipient info (0.30 points)
    # Expected: Ms. Sarah Johnson, Acme Corp, 123 Business Ave, Suite 400, New York, NY 10001
    try:
        addressee_checks = [
            'sarah johnson' in all_text,
            'acme corp' in all_text,
            '123 business ave' in all_text,
            'suite 400' in all_text,
            'new york' in all_text,
            '10001' in all_text,
        ]
        addr_pass_count = sum(addressee_checks)

        if addr_pass_count == 6:
            print(f"PASS: Component 3 -- Addressee complete: Ms. Sarah Johnson at Acme Corp, New York (0.30 pts)")
            total_score += 0.30
        elif addr_pass_count >= 3:
            partial = 0.30 * (addr_pass_count / 6.0)
            print(f"PARTIAL: Component 3 -- Addressee {addr_pass_count}/6 items found ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- Addressee missing or incomplete. Found {addr_pass_count}/6 items")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Addressee is indented/positioned differently from return address (0.20 points)
    # In the golden file, addressee paragraphs have left_indent > 0 while return address has no indent.
    # This distinguishes the envelope layout from just plain text in a document.
    try:
        # Find paragraphs containing addressee text and check indentation
        addressee_indent_count = 0
        return_addr_no_indent_count = 0

        for para in paragraphs:
            text_lower = para.text.strip().lower()
            indent = para.paragraph_format.left_indent

            # Check if addressee paragraph is indented
            if 'sarah johnson' in text_lower or 'acme corp' in text_lower:
                if indent is not None and indent > 0:
                    addressee_indent_count += 1

            # Check that return address is NOT indented (or at least less indented)
            if 'john smith' in text_lower or '456 oak street' in text_lower:
                if indent is None or indent == 0:
                    return_addr_no_indent_count += 1

        if addressee_indent_count > 0 and return_addr_no_indent_count > 0:
            print(f"PASS: Component 4 -- Addressee indented, return address at left margin (0.20 pts)")
            total_score += 0.20
        elif addressee_indent_count > 0:
            print(f"PARTIAL: Component 4 -- Addressee indented but return address position unclear (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- Addressee not indented differently from return address")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
