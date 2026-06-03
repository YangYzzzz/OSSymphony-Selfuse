"""
Reward Script: Strikethrough and double-underline revision markup
Task ID: writer_rd_087
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.30): Deleted phrases have strikethrough formatting
  - Component 2 (0.20): Deleted phrases are colored red (#CC0000)
  - Component 3 (0.30): Inserted phrases have double underline
  - Component 4 (0.20): Inserted phrases are colored blue (#0000CC)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_087'

# The exact phrases that should be marked as deleted (strikethrough + red)
DELETED_PHRASES = [
    'quarterly performance reviews',
    'on the last business day of each month',
    '2.5% per month',
    'three (3) years',
    'sixty (60) days written notice',
]

# The exact phrases that should be marked as inserted (double-underline + blue)
INSERTED_PHRASES = [
    'senior-level analysts with domain expertise',
    'bi-weekly on the 1st and 15th of each month',
    'proprietary algorithms and machine learning models',
]


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for " + domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: " + str(e))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document
    from docx.shared import RGBColor
    from docx.enum.text import WD_UNDERLINE

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file " + file_path + ": " + str(e))
        print("REWARD: 0.0")
        return 0.0

    # Build a lookup: phrase text -> list of (run, font) for matching runs
    # We look for runs whose text matches one of the target phrases
    deleted_runs = {}  # phrase -> list of run objects
    inserted_runs = {}  # phrase -> list of run objects

    for para in doc.paragraphs:
        for run in para.runs:
            text = run.text.strip()
            if text in DELETED_PHRASES:
                if text not in deleted_runs:
                    deleted_runs[text] = []
                deleted_runs[text].append(run)
            if text in INSERTED_PHRASES:
                if text not in inserted_runs:
                    inserted_runs[text] = []
                inserted_runs[text].append(run)

    # Component 1: Deleted phrases have strikethrough (0.30 points)
    # Each of the 5 phrases contributes 0.06 points
    try:
        strike_count = 0
        for phrase in DELETED_PHRASES:
            if phrase in deleted_runs:
                # Check if at least one matching run has strikethrough
                has_strike = any(r.font.strike for r in deleted_runs[phrase])
                if has_strike:
                    strike_count += 1
                    print("PASS: Strikethrough on '" + phrase[:40] + "...'")
                else:
                    print("FAIL: No strikethrough on '" + phrase[:40] + "'")
            else:
                print("FAIL: Deleted phrase not found as run: '" + phrase[:40] + "'")

        if strike_count == 5:
            total_score += 0.30
            print("PASS: Component 1 — All 5 deleted phrases have strikethrough (0.30 pts)")
        elif strike_count > 0:
            partial = round(0.30 * strike_count / 5, 2)
            total_score += partial
            print("PARTIAL: Component 1 — " + str(strike_count) + "/5 deleted phrases have strikethrough (" + str(partial) + " pts)")
        else:
            print("FAIL: Component 1 — No deleted phrases have strikethrough")
    except Exception as e:
        print("ERROR: Component 1 — " + str(e))

    # Component 2: Deleted phrases are colored red #CC0000 (0.20 points)
    try:
        red_count = 0
        target_red = RGBColor(0xCC, 0x00, 0x00)
        for phrase in DELETED_PHRASES:
            if phrase in deleted_runs:
                has_red = any(
                    r.font.color and r.font.color.rgb and str(r.font.color.rgb) == 'CC0000'
                    for r in deleted_runs[phrase]
                )
                if has_red:
                    red_count += 1
                else:
                    actual_colors = [str(r.font.color.rgb) if r.font.color and r.font.color.rgb else 'None' for r in deleted_runs[phrase]]
                    print("FAIL: Red color missing on '" + phrase[:40] + "', found: " + str(actual_colors))

        if red_count == 5:
            total_score += 0.20
            print("PASS: Component 2 — All 5 deleted phrases are red #CC0000 (0.20 pts)")
        elif red_count > 0:
            partial = round(0.20 * red_count / 5, 2)
            total_score += partial
            print("PARTIAL: Component 2 — " + str(red_count) + "/5 deleted phrases are red (" + str(partial) + " pts)")
        else:
            print("FAIL: Component 2 — No deleted phrases have red color")
    except Exception as e:
        print("ERROR: Component 2 — " + str(e))

    # Component 3: Inserted phrases have double underline (0.30 points)
    # Each of the 3 phrases contributes 0.10 points
    try:
        dbl_underline_count = 0
        for phrase in INSERTED_PHRASES:
            if phrase in inserted_runs:
                has_double_ul = any(
                    r.font.underline == WD_UNDERLINE.DOUBLE
                    for r in inserted_runs[phrase]
                )
                if has_double_ul:
                    dbl_underline_count += 1
                    print("PASS: Double underline on '" + phrase[:40] + "...'")
                else:
                    ul_vals = [str(r.font.underline) for r in inserted_runs[phrase]]
                    print("FAIL: No double underline on '" + phrase[:40] + "', found: " + str(ul_vals))
            else:
                print("FAIL: Inserted phrase not found as run: '" + phrase[:40] + "'")

        if dbl_underline_count == 3:
            total_score += 0.30
            print("PASS: Component 3 — All 3 inserted phrases have double underline (0.30 pts)")
        elif dbl_underline_count > 0:
            partial = round(0.30 * dbl_underline_count / 3, 2)
            total_score += partial
            print("PARTIAL: Component 3 — " + str(dbl_underline_count) + "/3 inserted phrases have double underline (" + str(partial) + " pts)")
        else:
            print("FAIL: Component 3 — No inserted phrases have double underline")
    except Exception as e:
        print("ERROR: Component 3 — " + str(e))

    # Component 4: Inserted phrases are colored blue #0000CC (0.20 points)
    try:
        blue_count = 0
        for phrase in INSERTED_PHRASES:
            if phrase in inserted_runs:
                has_blue = any(
                    r.font.color and r.font.color.rgb and str(r.font.color.rgb) == '0000CC'
                    for r in inserted_runs[phrase]
                )
                if has_blue:
                    blue_count += 1
                else:
                    actual_colors = [str(r.font.color.rgb) if r.font.color and r.font.color.rgb else 'None' for r in inserted_runs[phrase]]
                    print("FAIL: Blue color missing on '" + phrase[:40] + "', found: " + str(actual_colors))

        if blue_count == 3:
            total_score += 0.20
            print("PASS: Component 4 — All 3 inserted phrases are blue #0000CC (0.20 pts)")
        elif blue_count > 0:
            partial = round(0.20 * blue_count / 3, 2)
            total_score += partial
            print("PARTIAL: Component 4 — " + str(blue_count) + "/3 inserted phrases are blue (" + str(partial) + " pts)")
        else:
            print("FAIL: Component 4 — No inserted phrases have blue color")
    except Exception as e:
        print("ERROR: Component 4 — " + str(e))

    final_score = min(round(total_score, 2), 1.0)
    print("")
    print("Score: " + str(total_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = WORKDIR + '/' + TASK_ID + '.docx'
if not os.path.exists(file_path):
    print("File not found: " + file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
