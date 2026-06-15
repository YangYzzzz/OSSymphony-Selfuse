"""
Reward Script: Set mirrored margins (facing pages) with inner 3cm, outer 2cm
Task ID: writer_tech_074
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): mirrorMargins setting is enabled in document settings
  Component 2 (0.35): Inner margin (left) is approximately 3 cm (1701 twips)
  Component 3 (0.25): Outer margin (right) is approximately 2 cm (1134 twips)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_074'

# Tolerance: 2mm in twips (1 twip = 1/1440 inch = 0.01764 mm, so 2mm ~ 113 twips)
TWIP_TOLERANCE = 113

# Expected values in twips (1 cm = 567 twips approximately)
INNER_MARGIN_TWIPS = 1701  # 3 cm
OUTER_MARGIN_TWIPS = 1134  # 2 cm


def persist_app_state(domain: str):
    """Attempt to save any unsaved changes in LibreOffice."""
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
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: mirrorMargins is enabled in document settings (0.4 points)
    # This is the key setting that enables facing-pages / two-page spread layout.
    # In the initial doc, this element does not exist. In golden, it does.
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        settings_element = doc.settings.element
        mirror_elem = settings_element.find('.//w:mirrorMargins', ns)
        if mirror_elem is not None:
            # mirrorMargins present means mirrored/facing pages enabled
            # Check it's not explicitly disabled (w:val="0" or w:val="false")
            val_attr = mirror_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            if val_attr is None or val_attr in ('1', 'true', 'on'):
                print(f"PASS: Component 1 — mirrorMargins is enabled (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — mirrorMargins element present but disabled (val={val_attr})")
        else:
            print(f"FAIL: Component 1 — mirrorMargins element not found in document settings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Inner margin (left margin in section) is ~3 cm / 1701 twips (0.35 points)
    # With mirrored margins, left_margin = inner margin.
    # In initial doc, left = 1440 twips (1 inch). In golden, left = 1701 twips (3 cm).
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
        pgMar = sectPr.find('.//w:pgMar', ns)
        if pgMar is not None:
            left_twips = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left', '0'))
            diff = abs(left_twips - INNER_MARGIN_TWIPS)
            if diff <= TWIP_TOLERANCE:
                print(f"PASS: Component 2 — Inner margin = {left_twips} twips (~{left_twips/567:.2f} cm), expected ~{INNER_MARGIN_TWIPS} twips (3 cm) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — Inner margin = {left_twips} twips (~{left_twips/567:.2f} cm), expected ~{INNER_MARGIN_TWIPS} twips (3 cm), diff={diff} twips")
        else:
            print(f"FAIL: Component 2 — pgMar element not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Outer margin (right margin in section) is ~2 cm / 1134 twips (0.25 points)
    # In initial doc, right = 1440 twips (1 inch). In golden, right = 1134 twips (2 cm).
    try:
        section = doc.sections[0]
        sectPr = section._sectPr
        pgMar = sectPr.find('.//w:pgMar', ns)
        if pgMar is not None:
            right_twips = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}right', '0'))
            diff = abs(right_twips - OUTER_MARGIN_TWIPS)
            if diff <= TWIP_TOLERANCE:
                print(f"PASS: Component 3 — Outer margin = {right_twips} twips (~{right_twips/567:.2f} cm), expected ~{OUTER_MARGIN_TWIPS} twips (2 cm) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Outer margin = {right_twips} twips (~{right_twips/567:.2f} cm), expected ~{OUTER_MARGIN_TWIPS} twips (2 cm), diff={diff} twips")
        else:
            print(f"FAIL: Component 3 — pgMar element not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved GUI state before verification
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
