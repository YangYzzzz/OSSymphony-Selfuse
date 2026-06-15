"""
Reward Script: Add company logo image to header left side and 'Acme Corporation' text to right side
Task ID: writer_fs_078
Domain: libreoffice_writer
Scoring:
  Component 1: Header contains an inline image (0.35 pts)
  Component 2: Header contains 'Acme Corporation' text (0.30 pts)
  Component 3: Image and text on same line via tab alignment (0.35 pts)
"""

import os

from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_078'


def persist_app_state():
    """Try to save any unsaved LibreOffice state via Ctrl+S."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
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
        print("CRITICAL: Document has no sections")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]
    header = section.header

    # Get header paragraphs
    header_paras = header.paragraphs
    if not header_paras:
        print("FAIL: No header paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    # We'll examine the header XML and paragraph structure
    header_xml = header._element.xml

    # Component 1: Header contains an inline image (0.35 points)
    # The golden state has an image embedded in the header via w:drawing/wp:inline
    try:
        has_image_in_header = False

        # Check header part relationships for image
        hdr_part = header.part
        if hasattr(hdr_part, 'rels'):
            for rel_id, rel in hdr_part.rels.items():
                if 'image' in rel.reltype:
                    has_image_in_header = True
                    break

        # Also verify via XML that there's actually a drawing element in the header
        if not has_image_in_header:
            # Fallback: check XML for blip or graphicData
            if 'blip' in header_xml or 'graphicData' in header_xml:
                has_image_in_header = True

        if has_image_in_header:
            print(f"PASS: Component 1 — Header contains an image (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — No image found in header")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header contains 'Acme Corporation' text (0.30 points)
    try:
        header_full_text = ''
        for p in header_paras:
            header_full_text += p.text

        has_acme_text = 'Acme Corporation' in header_full_text

        if has_acme_text:
            print(f"PASS: Component 2 — Header contains 'Acme Corporation' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — 'Acme Corporation' not found in header. Found: {repr(header_full_text[:200])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Image and text on same line with tab alignment (0.35 points)
    # Both elements should be in the SAME paragraph, with a tab character separating them,
    # and a right-aligned tab stop to push text to the right side.
    try:
        same_line = False

        for p in header_paras:
            p_xml = p._element.xml
            p_has_image = 'graphicData' in p_xml or 'blip' in p_xml
            p_has_acme = 'Acme Corporation' in p.text

            if p_has_image and p_has_acme:
                # Check for tab character (w:tab element) in the paragraph XML
                has_tab = '<w:tab' in p_xml and 'w:tab/' in p_xml
                # Also check for right-aligned tab stop in paragraph or section
                has_right_tab = False
                # Check paragraph-level tab stops
                for ts in p.paragraph_format.tab_stops:
                    if str(ts.alignment) in ('RIGHT (2)', 'RIGHT'):
                        has_right_tab = True
                        break
                # Also check XML directly for right tab
                if not has_right_tab:
                    if 'w:val="right"' in p_xml:
                        has_right_tab = True

                if has_tab or has_right_tab:
                    same_line = True
                    print(f"PASS: Component 3 — Image and text in same paragraph with tab alignment (0.35 pts)")
                    print(f"  has_tab_char={has_tab}, has_right_tab_stop={has_right_tab}")
                    total_score += 0.35
                else:
                    # Still same paragraph but no tab — give partial (0.15)
                    same_line = True
                    print(f"PARTIAL: Component 3 — Image and text in same paragraph but no tab alignment (0.15/0.35 pts)")
                    total_score += 0.15
                break

        if not same_line:
            print(f"FAIL: Component 3 — Image and 'Acme Corporation' not found in the same header paragraph")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
