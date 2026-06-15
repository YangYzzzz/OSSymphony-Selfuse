"""
Reward Script: Configure page style with mirrored margins for binding
Task ID: writer_bs_093
Domain: libreoffice_writer
Scoring:
  Component 1: Inner (left) margin = 3.5 cm  (0.25 pts)
  Component 2: Outer (right) margin = 2.0 cm (0.25 pts)
  Component 3: Top margin = 2.5 cm           (0.15 pts)
  Component 4: Bottom margin = 2.5 cm        (0.15 pts)
  Component 5: Mirrored page layout enabled   (0.20 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_093'

# Tolerance for margin checks: 0.02 cm in EMU
# 1 cm = 914400/2.54 = ~360000 EMU
# 0.02 cm = ~7200 EMU — tight enough to distinguish 2.50 cm from 2.54 cm
# (golden top/bottom = 899795 EMU ≈ 2.4994 cm, initial = 914400 EMU = 2.54 cm, diff ~14600 EMU)
TOLERANCE_EMU = int(0.02 * 914400 / 2.54)  # ~7200 EMU


def emu_to_cm(emu):
    """Convert EMU to centimeters."""
    return emu / 914400.0 * 2.54


def margin_matches(actual_emu, expected_cm):
    """Check if an EMU margin value matches the expected cm within tolerance."""
    expected_emu = int(expected_cm / 2.54 * 914400)
    return abs(actual_emu - expected_emu) <= TOLERANCE_EMU


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
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

    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Component 1: Inner (left) margin = 3.5 cm (0.25 points)
    # Initial state has 2.54 cm; golden has 3.5 cm. This check FAILS on initial.
    try:
        left_cm = emu_to_cm(section.left_margin)
        if margin_matches(section.left_margin, 3.5):
            print(f"PASS: Component 1 — Inner (left) margin = {left_cm:.2f} cm (expected ~3.5 cm) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Inner (left) margin = {left_cm:.4f} cm, expected ~3.5 cm")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Outer (right) margin = 2.0 cm (0.25 points)
    # Initial state has 2.54 cm; golden has 2.0 cm. This check FAILS on initial.
    try:
        right_cm = emu_to_cm(section.right_margin)
        if margin_matches(section.right_margin, 2.0):
            print(f"PASS: Component 2 — Outer (right) margin = {right_cm:.2f} cm (expected ~2.0 cm) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Outer (right) margin = {right_cm:.4f} cm, expected ~2.0 cm")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Top margin = 2.5 cm (0.15 points)
    # Initial state has 2.54 cm; golden has 2.5 cm. Different enough to distinguish.
    try:
        top_cm = emu_to_cm(section.top_margin)
        if margin_matches(section.top_margin, 2.5):
            print(f"PASS: Component 3 — Top margin = {top_cm:.2f} cm (expected ~2.5 cm) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Top margin = {top_cm:.4f} cm, expected ~2.5 cm")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Bottom margin = 2.5 cm (0.15 points)
    # Initial state has 2.54 cm; golden has 2.5 cm. Different enough to distinguish.
    try:
        bottom_cm = emu_to_cm(section.bottom_margin)
        if margin_matches(section.bottom_margin, 2.5):
            print(f"PASS: Component 4 — Bottom margin = {bottom_cm:.2f} cm (expected ~2.5 cm) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Bottom margin = {bottom_cm:.4f} cm, expected ~2.5 cm")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Mirrored page layout enabled (0.20 points)
    # Initial state has NO mirrorMargins element; golden HAS it. This check FAILS on initial.
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        settings_element = doc.settings.element
        mirror_elements = settings_element.findall('.//w:mirrorMargins', ns)
        if len(mirror_elements) > 0:
            # mirrorMargins present — check it's not explicitly set to false
            val_attr = mirror_elements[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            # If val is absent or "1" or "true", mirroring is ON
            # If val is "0" or "false", mirroring is OFF
            if val_attr in (None, '1', 'true', 'on'):
                print(f"PASS: Component 5 — Mirrored page layout is enabled (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — mirrorMargins element present but val={val_attr} (not enabled)")
        else:
            print(f"FAIL: Component 5 — mirrorMargins element not found in document settings")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
