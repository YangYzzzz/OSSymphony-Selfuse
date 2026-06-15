"""
Reward Script: Set footer margin spacing to 1.0 cm and footer content height to 1.5 cm
Task ID: writer_fs_073
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): Footer spacing (bottom_margin - footer_distance) == 1.0 cm
  Component 2 (0.5 pts): Footer content height (footer_distance) == 1.5 cm
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_073'

# Tolerance: 0.05 cm (~18 twips) to account for rounding in LibreOffice export
TOLERANCE_CM = 0.05

# Conversion constant: 1 cm = 360000 EMU
CM_TO_EMU = 360000


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
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

    In LibreOffice Writer, the footer page-style settings map to DOCX/OOXML as:
      - footer_distance (w:footer) = distance from page bottom edge to footer start
        This corresponds to the footer "Height" in LibreOffice.
      - bottom_margin (w:bottom) = distance from page bottom edge to body text end
        The "Spacing" (gap between body and footer) = bottom_margin - footer_distance.

    Task requires:
      - Spacing = 1.0 cm  =>  bottom_margin - footer_distance ~= 1.0 cm
      - Height  = 1.5 cm  =>  footer_distance ~= 1.5 cm
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Component 1: Footer content height == 1.5 cm (0.5 points)
    # footer_distance maps to the footer "Height" in LibreOffice
    try:
        footer_dist = section.footer_distance
        if footer_dist is None:
            print("FAIL: Component 1 — footer_distance is None (no footer configured)")
        else:
            footer_height_cm = footer_dist / CM_TO_EMU
            diff = abs(footer_height_cm - 1.5)
            if diff <= TOLERANCE_CM:
                print(f"PASS: Component 1 — Footer height = {footer_height_cm:.4f} cm (expected ~1.5 cm) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — Footer height = {footer_height_cm:.4f} cm, expected ~1.5 cm (diff={diff:.4f})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footer spacing (body-to-footer gap) == 1.0 cm (0.5 points)
    # spacing = bottom_margin - footer_distance
    try:
        bottom_margin = section.bottom_margin
        footer_dist = section.footer_distance
        if bottom_margin is None or footer_dist is None:
            print("FAIL: Component 2 — bottom_margin or footer_distance is None")
        else:
            spacing_cm = (bottom_margin - footer_dist) / CM_TO_EMU
            diff = abs(spacing_cm - 1.0)
            if diff <= TOLERANCE_CM:
                print(f"PASS: Component 2 — Footer spacing = {spacing_cm:.4f} cm (expected ~1.0 cm) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — Footer spacing = {spacing_cm:.4f} cm, expected ~1.0 cm (diff={diff:.4f})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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
