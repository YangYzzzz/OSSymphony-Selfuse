"""
Reward Script: Format file paths with Liberation Mono, dark blue, italic
Task ID: writer_tech_049
Domain: libreoffice_writer
Scoring: 6 file paths must each have Liberation Mono font, dark blue color, and italic.
  Component 1 (0.5): All 6 file paths found as separate styled runs
  Component 2 (0.3): Font is Liberation Mono on all file path runs
  Component 3 (0.2): Color is dark blue (00008B) and italic on all file path runs
"""

import os
from math import sqrt
from docx import Document
from docx.shared import Pt, RGBColor

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_049'

# The 6 file paths expected in the document
EXPECTED_PATHS = [
    '/etc/config.yaml',
    '~/.ssh/authorized_keys',
    '/var/log/syslog',
    '/usr/local/bin/deploy.sh',
    '~/.bashrc',
    '/opt/app/settings.json',
]

DARK_BLUE = RGBColor(0x00, 0x00, 0x8B)  # #00008B


def color_distance(c1, c2):
    """Euclidean RGB distance between two RGBColor values."""
    return sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)


def find_styled_path_runs(doc):
    """
    Find runs whose text matches one of the expected file paths.
    Returns a dict: {path_text: run_object} for paths found as dedicated runs.
    """
    found = {}
    for para in doc.paragraphs:
        for run in para.runs:
            text = run.text.strip()
            if text in EXPECTED_PATHS:
                found[text] = run
    return found


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

    # Find file path runs that are styled (split into their own run)
    styled_runs = find_styled_path_runs(doc)
    found_count = len(styled_runs)
    print(f"INFO: Found {found_count}/6 file paths as separate styled runs")
    for path_text in EXPECTED_PATHS:
        if path_text in styled_runs:
            print(f"  FOUND: '{path_text}'")
        else:
            print(f"  MISSING: '{path_text}'")

    # Component 1: File paths exist as separate runs (0.5 points, proportional)
    # This checks that the paths were split out from surrounding text into their own runs
    try:
        if found_count > 0:
            comp1_score = 0.5 * (found_count / 6.0)
            print(f"PASS: Component 1 — {found_count}/6 file paths found as styled runs ({comp1_score:.2f} pts)")
            total_score += comp1_score
        else:
            print(f"FAIL: Component 1 — No file paths found as separate runs")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Font is Liberation Mono on all found path runs (0.3 points)
    try:
        if found_count == 0:
            print(f"FAIL: Component 2 — No styled runs to check font")
        else:
            mono_count = 0
            for path_text, run in styled_runs.items():
                font_name = run.font.name
                if font_name and 'liberation mono' in font_name.lower():
                    mono_count += 1
                    print(f"  Font OK: '{path_text}' -> {font_name}")
                else:
                    print(f"  Font FAIL: '{path_text}' -> {font_name}")

            if mono_count > 0:
                comp2_score = 0.3 * (mono_count / 6.0)
                print(f"PASS: Component 2 — {mono_count}/6 have Liberation Mono ({comp2_score:.2f} pts)")
                total_score += comp2_score
            else:
                print(f"FAIL: Component 2 — No runs have Liberation Mono font")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Color is dark blue AND italic on all found path runs (0.2 points)
    try:
        if found_count == 0:
            print(f"FAIL: Component 3 — No styled runs to check color/italic")
        else:
            styled_ok_count = 0
            for path_text, run in styled_runs.items():
                is_italic = run.font.italic is True
                has_color = False
                if run.font.color and run.font.color.rgb:
                    dist = color_distance(run.font.color.rgb, DARK_BLUE)
                    has_color = dist < 30  # tolerance for slight variations
                    print(f"  Style '{path_text}': italic={is_italic}, color={run.font.color.rgb}, dist={dist:.1f}")
                else:
                    print(f"  Style '{path_text}': italic={is_italic}, color=None")

                if is_italic and has_color:
                    styled_ok_count += 1

            if styled_ok_count > 0:
                comp3_score = 0.2 * (styled_ok_count / 6.0)
                print(f"PASS: Component 3 — {styled_ok_count}/6 have dark blue + italic ({comp3_score:.2f} pts)")
                total_score += comp3_score
            else:
                print(f"FAIL: Component 3 — No runs have both dark blue color and italic")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state
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
