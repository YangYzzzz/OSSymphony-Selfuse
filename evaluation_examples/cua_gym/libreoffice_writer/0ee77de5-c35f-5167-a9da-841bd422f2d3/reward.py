"""
Reward Script: Fahrenheit to Celsius conversion in recipe document
Task ID: writer_frd_038
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.8): Each of 8 temperature values has correct Celsius appended (0.1 each)
  - Component 2 (0.2): All 8 conversions present (completeness bonus)
"""

import os
import re
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_038'

# Expected conversions: Fahrenheit -> Celsius (rounded to nearest integer)
# Formula: C = (F - 32) * 5 / 9
EXPECTED_CONVERSIONS = {
    425: 218,
    165: 74,
    450: 232,
    200: 93,
    275: 135,
    400: 204,
    375: 191,
    350: 177,
}

def persist_app_state(domain: str):
    """Try to save any unsaved changes in LibreOffice."""
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

    # Collect all paragraph text
    all_text = "\n".join(para.text for para in doc.paragraphs)

    # Component 1: Each temperature has correct Celsius appended (0.1 points each, 0.8 total)
    # Pattern: <number>°F (<celsius>°C)
    conversion_count = 0
    per_temp_score = 0.1

    for f_val, expected_c in EXPECTED_CONVERSIONS.items():
        try:
            # Look for the Fahrenheit value followed by Celsius in parentheses
            # Allow small tolerance in Celsius value (+-1 degree)
            pattern = rf'{f_val}°F\s*\((\d+)°C\)'
            match = re.search(pattern, all_text)
            if match:
                actual_c = int(match.group(1))
                if abs(actual_c - expected_c) <= 1:
                    print(f"PASS: {f_val}°F -> ({actual_c}°C) matches expected ({expected_c}°C) ({per_temp_score} pts)")
                    total_score += per_temp_score
                    conversion_count += 1
                else:
                    print(f"FAIL: {f_val}°F -> ({actual_c}°C) does NOT match expected ({expected_c}°C)")
            else:
                print(f"FAIL: {f_val}°F has no Celsius conversion appended")
        except Exception as e:
            print(f"ERROR: checking {f_val}°F conversion: {e}")

    print(f"\nComponent 1 summary: {conversion_count}/8 conversions correct")

    # Component 2: Completeness bonus - all 8 conversions present (0.2 points)
    try:
        if conversion_count == 8:
            print(f"PASS: All 8 temperature conversions present (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Only {conversion_count}/8 conversions — completeness bonus not awarded")
    except Exception as e:
        print(f"ERROR: completeness check: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    # Also check for Cookbook_Recipes.docx as mentioned in task context
    alt_path = f'{WORKDIR}/Cookbook_Recipes.docx'
    if os.path.exists(alt_path):
        file_path = alt_path
    else:
        print(f"File not found: {file_path}")
        print("REWARD: 0.0")
else:
    verify_task(file_path)
