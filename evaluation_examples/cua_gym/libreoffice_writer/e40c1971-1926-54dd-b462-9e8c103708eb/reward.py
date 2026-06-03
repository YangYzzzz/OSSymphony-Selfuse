"""
Reward Script: Insert date/time field in footer showing DD/MM/YYYY HH:MM format
Task ID: writer_tm_068
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Footer has non-empty content (field codes or text present)
  Component 2 (0.4): Footer contains a DATE field with DD/MM/YYYY format
  Component 3 (0.3): Footer contains a TIME field with HH:mm format
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_068'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the document footer contains date/time fields in DD/MM/YYYY HH:MM format.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Namespace for XML queries
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Get footer from section 0
    try:
        section = doc.sections[0]
        footer = section.footer
        footer_xml = etree.tostring(footer._element, pretty_print=True).decode()
    except Exception as e:
        print(f"CRITICAL: Cannot access footer: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all instrText elements from the footer
    instr_texts = []
    try:
        for elem in footer._element.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}instrText'):
            if elem.text:
                instr_texts.append(elem.text.strip())
    except Exception as e:
        print(f"ERROR: Could not parse footer XML: {e}")

    print(f"DEBUG: Footer instrText fields found: {instr_texts}")

    # Also check footer text content (cached values from field codes or plain text)
    footer_text = ""
    try:
        for para in footer.paragraphs:
            footer_text += para.text
    except Exception:
        pass
    print(f"DEBUG: Footer text content: {repr(footer_text)}")

    # Component 1: Footer has non-empty content — field codes or text (0.3 points)
    # This checks that the footer is not empty (as it is in initial_env)
    try:
        has_field_codes = len(instr_texts) > 0
        has_text_content = len(footer_text.strip()) > 0
        if has_field_codes or has_text_content:
            print(f"PASS: Component 1 — Footer has content (fields={len(instr_texts)}, text={repr(footer_text.strip()[:50])}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Footer is empty (no field codes, no text)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footer contains DATE field with DD/MM/YYYY format (0.4 points)
    # The golden file uses: DATE \@ "DD/MM/YYYY"
    # We accept variations: DATE or CREATEDATE or SAVEDATE with DD/MM/YYYY pattern
    try:
        date_field_found = False
        for instr in instr_texts:
            # Check for a date-related field with DD/MM/YYYY format pattern
            # Accept: DATE, CREATEDATE, SAVEDATE, PRINTDATE, or even combined DATE with date format
            if re.search(r'(DATE|CREATEDATE|SAVEDATE|PRINTDATE)', instr, re.IGNORECASE):
                if re.search(r'DD/MM/YYYY', instr, re.IGNORECASE):
                    date_field_found = True
                    print(f"PASS: Component 2 — DATE field with DD/MM/YYYY format found: {repr(instr)} (0.4 pts)")
                    break

        if not date_field_found:
            # Also check if there's a combined datetime field that includes DD/MM/YYYY
            for instr in instr_texts:
                if re.search(r'DD/MM/YYYY', instr, re.IGNORECASE):
                    date_field_found = True
                    print(f"PASS: Component 2 — Field with DD/MM/YYYY format found: {repr(instr)} (0.4 pts)")
                    break

        if date_field_found:
            total_score += 0.4
        else:
            # Check if footer text at least has a date pattern DD/MM/YYYY as static text
            if re.search(r'\d{2}/\d{2}/\d{4}', footer_text):
                # Static date text (no field code) - give partial credit
                print(f"FAIL: Component 2 — Footer has date text but no DATE field code. Expected a field, not static text.")
            else:
                print(f"FAIL: Component 2 — No DATE field with DD/MM/YYYY format found in footer. instrTexts: {instr_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer contains TIME field with HH:mm format (0.3 points)
    # The golden file uses: TIME \@ "HH:mm"
    # Accept variations: TIME field or combined with HH:mm or HH:MM pattern
    try:
        time_field_found = False
        for instr in instr_texts:
            if re.search(r'TIME', instr, re.IGNORECASE):
                if re.search(r'HH[:/]mm|HH[:/]MM', instr, re.IGNORECASE):
                    time_field_found = True
                    print(f"PASS: Component 3 — TIME field with HH:mm format found: {repr(instr)} (0.3 pts)")
                    break

        if not time_field_found:
            # Check for combined DATE field that also includes time format HH:mm
            for instr in instr_texts:
                if re.search(r'HH[:/]mm|HH[:/]MM', instr, re.IGNORECASE):
                    time_field_found = True
                    print(f"PASS: Component 3 — Field with HH:mm time format found: {repr(instr)} (0.3 pts)")
                    break

        if time_field_found:
            total_score += 0.3
        else:
            # Check if footer has time pattern as static text
            if re.search(r'\d{2}:\d{2}', footer_text):
                print(f"FAIL: Component 3 — Footer has time text but no TIME field code. Expected a field, not static text.")
            else:
                print(f"FAIL: Component 3 — No TIME field with HH:mm format found in footer. instrTexts: {instr_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
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
