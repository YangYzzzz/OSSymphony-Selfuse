"""
Reward Script: Insert signature line with signer properties
Task ID: writer_fp_034
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Signer name 'John Smith' present after 'Authorized by:'
  Component 2 (0.25): Title 'Chief Financial Officer' present
  Component 3 (0.25): Email 'jsmith@company.com' present
  Component 4 (0.20): Signature line visual elements (instruction text, X marker, or line)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fp_034'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify signature line insertion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the 'Authorized by:' paragraph and collect all text after it
    paragraphs = doc.paragraphs
    auth_index = None
    for i, para in enumerate(paragraphs):
        if 'Authorized by:' in para.text:
            auth_index = i
            break

    if auth_index is None:
        print("FAIL: Could not find 'Authorized by:' paragraph — document structure unexpected")
        print("REWARD: 0.0")
        return 0.0

    # Collect paragraphs after 'Authorized by:'
    after_auth = paragraphs[auth_index + 1:]
    after_auth_texts = [p.text.strip() for p in after_auth]
    after_auth_texts_lower = [t.lower() for t in after_auth_texts]

    print(f"INFO: Found 'Authorized by:' at paragraph {auth_index}")
    print(f"INFO: {len(after_auth)} paragraphs follow it")
    for idx, t in enumerate(after_auth_texts):
        if t:
            print(f"  After[{idx}]: {repr(t[:80])}")

    # Component 1: Signer name 'John Smith' present after 'Authorized by:' (0.30 points)
    try:
        name_found = any('john smith' in t for t in after_auth_texts_lower)
        if name_found:
            print(f"PASS: Component 1 — 'John Smith' found in signature area (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — 'John Smith' not found after 'Authorized by:'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title 'Chief Financial Officer' present (0.25 points)
    try:
        title_found = any('chief financial officer' in t for t in after_auth_texts_lower)
        if title_found:
            print(f"PASS: Component 2 — 'Chief Financial Officer' found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — 'Chief Financial Officer' not found after 'Authorized by:'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Email 'jsmith@company.com' present (0.25 points)
    try:
        email_found = any('jsmith@company.com' in t for t in after_auth_texts_lower)
        if email_found:
            print(f"PASS: Component 3 — 'jsmith@company.com' found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — 'jsmith@company.com' not found after 'Authorized by:'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Signature line visual elements (0.20 points)
    # Check for instruction text, X marker, horizontal line/tabs, or a drawing/object element
    try:
        has_instruction = any(
            'sign here' in t or 'sign above' in t or 'sign below' in t
            for t in after_auth_texts_lower
        )
        has_x_marker = any(t == 'x' for t in after_auth_texts_lower)
        has_line_element = any('\t' in p.text and len(p.text.strip()) == 0 for p in after_auth)
        # Also check for underscores as a line
        has_underscore_line = any('___' in t for t in after_auth_texts)

        # Check for actual w:drawing child elements (not namespace declarations) in signature area
        ns_w = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        has_drawing = any(
            len(p._element.findall('.//w:drawing', ns_w)) > 0
            for p in after_auth
        )

        visual_elements = sum([has_instruction, has_x_marker, has_line_element, has_underscore_line, has_drawing])
        print(f"  instruction={has_instruction}, x_marker={has_x_marker}, line_element={has_line_element}, "
              f"underscore_line={has_underscore_line}, drawing={has_drawing}")

        if visual_elements >= 1:
            print(f"PASS: Component 4 — Signature line visual elements found ({visual_elements} indicators) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — No signature line visual elements found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
