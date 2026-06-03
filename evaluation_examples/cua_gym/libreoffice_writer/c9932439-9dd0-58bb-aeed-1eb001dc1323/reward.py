"""
Reward Script: Staircase left indent on 8 paragraphs
Task ID: wrpara_041
Domain: libreoffice_writer
Scoring: Paragraphs 1-7 each earn ~0.1429 pts for correct left indent (i * 0.5 cm).
         Paragraph 0 is 0cm in both initial and golden (precondition, not scored).
         Total: 7 components summing to 1.0.
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'wrpara_041'

# Tolerance for floating-point comparison (~0.5mm)
TOLERANCE_CM = 0.05

# EMU per cm
EMU_PER_CM = 360000.0


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
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
    Verify staircase left indent pattern.
    Paragraphs 1-7 must have left_indent == i * 0.5 cm.
    Paragraph 0 is a precondition (0cm in both envs) and not scored.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    # 7 scored paragraphs (1-7), each worth 1/7 of the total
    POINTS_PER_PARA = 1.0 / 7.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    if len(paragraphs) < 8:
        print(f"FAIL: Expected at least 8 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    for i in range(8):
        expected_cm = i * 0.5
        try:
            indent = paragraphs[i].paragraph_format.left_indent
            # None means 0 indent (inherited default)
            if indent is None:
                actual_cm = 0.0
            else:
                actual_cm = indent / EMU_PER_CM

            if abs(actual_cm - expected_cm) <= TOLERANCE_CM:
                if i == 0:
                    # Para 0 is 0cm in both initial and golden — precondition, no points
                    print(f"PASS: Para {i} indent={actual_cm:.2f}cm == expected {expected_cm:.2f}cm (precondition, 0 pts)")
                else:
                    print(f"PASS: Para {i} indent={actual_cm:.2f}cm == expected {expected_cm:.2f}cm ({POINTS_PER_PARA:.4f} pts)")
                    total_score += POINTS_PER_PARA
            else:
                print(f"FAIL: Para {i} indent={actual_cm:.2f}cm, expected {expected_cm:.2f}cm")
        except Exception as e:
            print(f"ERROR: Para {i} — {e}")

    final_score = round(min(total_score, 1.0), 4)
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
