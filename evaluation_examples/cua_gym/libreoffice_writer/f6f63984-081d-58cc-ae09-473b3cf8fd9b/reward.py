"""
Reward Script: Linked header-footer system with chapter field and page numbering
Task ID: writer_biz_071
Domain: libreoffice_writer
Scoring:
  Component 1: Header contains STYLEREF "Heading 1" field (0.30)
  Component 2: Footer contains "Confidential - Meridian Solutions Inc." text (0.30)
  Component 3: Footer contains PAGE field code (0.20)
  Component 4: Footer contains NUMPAGES field code (0.20)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_071'

def persist_app_state(domain: str):
    """Attempt to save any unsaved GUI state."""
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
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    # We check the first section's header and footer.
    # The task says "linked header-footer system" so section 0 is the relevant one.
    section = doc.sections[0]
    header = section.header
    footer = section.footer

    header_xml = header._element.xml
    footer_xml = footer._element.xml

    # Component 1: Header contains STYLEREF "Heading 1" field (0.30 points)
    # The golden header uses a STYLEREF field referencing "Heading 1" to display
    # the current chapter title. This MUST NOT exist in the initial file.
    try:
        # Look for instrText containing STYLEREF and Heading 1
        has_styleref = bool(re.search(
            r'instrText[^>]*>.*?STYLEREF.*?Heading\s*1',
            header_xml,
            re.DOTALL | re.IGNORECASE
        ))
        if has_styleref:
            print(f"PASS: Component 1 - Header has STYLEREF 'Heading 1' field (0.30 pts)")
            total_score += 0.30
        else:
            # Also accept CHAPTER field as an alternative way to show chapter title
            has_chapter_field = bool(re.search(
                r'instrText[^>]*>.*?CHAPTER',
                header_xml,
                re.DOTALL | re.IGNORECASE
            ))
            if has_chapter_field:
                print(f"PASS: Component 1 - Header has CHAPTER field (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 - Header lacks STYLEREF 'Heading 1' or CHAPTER field")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Footer contains "Confidential - Meridian Solutions Inc." text (0.30 points)
    # The golden footer must contain this exact confidential text.
    try:
        # Check footer paragraph text for the confidential string
        footer_text = ""
        for para in footer.paragraphs:
            footer_text += para.text

        has_confidential = "Confidential - Meridian Solutions Inc." in footer_text
        if has_confidential:
            print(f"PASS: Component 2 - Footer contains 'Confidential - Meridian Solutions Inc.' (0.30 pts)")
            total_score += 0.30
        else:
            # Also check case-insensitively for near-matches
            has_confidential_ci = "confidential" in footer_text.lower() and "meridian" in footer_text.lower()
            if has_confidential_ci:
                print(f"PARTIAL: Component 2 - Footer has confidential text but not exact match: {repr(footer_text)} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 - Footer text does not contain confidential string. Found: {repr(footer_text)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Footer contains PAGE field code (0.20 points)
    # The golden footer uses a PAGE field for "Page X" display.
    try:
        # Look for instrText containing PAGE (but not NUMPAGES)
        # We need to find PAGE as a standalone field, not just part of NUMPAGES
        has_page_field = bool(re.search(
            r'instrText[^>]*>[^<]*\bPAGE\b(?!\s*S)',
            footer_xml,
            re.IGNORECASE
        ))
        if has_page_field:
            print(f"PASS: Component 3 - Footer has PAGE field code (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - Footer lacks PAGE field code")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Footer contains NUMPAGES field code (0.20 points)
    # The golden footer uses NUMPAGES for total page count display ("of Y").
    try:
        has_numpages = bool(re.search(
            r'instrText[^>]*>[^<]*NUMPAGES',
            footer_xml,
            re.IGNORECASE
        ))
        if has_numpages:
            print(f"PASS: Component 4 - Footer has NUMPAGES field code (0.20 pts)")
            total_score += 0.20
        else:
            # Also accept SECTIONPAGES as an alternative
            has_sectionpages = bool(re.search(
                r'instrText[^>]*>[^<]*SECTIONPAGES',
                footer_xml,
                re.IGNORECASE
            ))
            if has_sectionpages:
                print(f"PASS: Component 4 - Footer has SECTIONPAGES field code (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - Footer lacks NUMPAGES/SECTIONPAGES field code")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (Writer may have unsaved GUI edits)
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
