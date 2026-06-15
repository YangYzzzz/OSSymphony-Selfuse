"""
Reward Script: Apply bold, dark blue font color, light yellow background, and 13pt font to day names
Task ID: writer_txtfmt_061
Domain: libreoffice_writer
Scoring:
  Component 1: All 5 day names are bold (0.25 pts)
  Component 2: All 5 day names have font color #00008B (0.25 pts)
  Component 3: All 5 day names have character background #FFFFCC via shd element (0.25 pts)
  Component 4: All 5 day names have font size 13pt (0.25 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_txtfmt_061'
FILE_PATH = f'{WORKDIR}/Desktop/weekly_schedule.docx'

DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
EXPECTED_FONT_COLOR = '00008B'
EXPECTED_BG_COLOR = 'FFFFCC'
EXPECTED_FONT_SIZE_PT = 13.0


def get_day_name_runs(doc):
    """
    Find paragraphs whose full text matches a day name exactly,
    and return their first run (which should contain the day name).
    Returns a dict: {day_name: run}
    """
    found = {}
    for para in doc.paragraphs:
        stripped = para.text.strip()
        if stripped in DAY_NAMES:
            runs = [r for r in para.runs if r.text.strip()]
            if runs:
                found[stripped] = runs[0]
    return found


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must load
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the day name runs
    try:
        day_runs = get_day_name_runs(doc)
    except Exception as e:
        print(f"CRITICAL: Could not locate day name paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: all 5 day names must be present in the document
    missing = [d for d in DAY_NAMES if d not in day_runs]
    if missing:
        print(f"CRITICAL: Day names not found in document: {missing}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found all 5 day name paragraphs: {list(day_runs.keys())}")

    # Component 1: All 5 day names are bold (0.25 points)
    # FAILS on initial (bold=False) -> PASSES on golden (bold=True)
    try:
        bold_results = {}
        for day, run in day_runs.items():
            bold_results[day] = (run.bold is True)
        bold_pass = all(bold_results.values())
        not_bold = [d for d, v in bold_results.items() if not v]
        if bold_pass:
            print(f"PASS: Component 1 — All 5 day names are bold (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Bold not set on: {not_bold}")
    except Exception as e:
        print(f"ERROR: Component 1 (bold check) — {e}")

    # Component 2: All 5 day names have font color #00008B (0.25 points)
    # FAILS on initial (color=000000) -> PASSES on golden (color=00008B)
    try:
        color_results = {}
        for day, run in day_runs.items():
            try:
                actual_color = str(run.font.color.rgb).upper() if run.font.color and run.font.color.type else None
            except Exception:
                actual_color = None
            # Also check via XML w:color element directly
            if actual_color is None:
                rPr = run._element.find(qn('w:rPr'))
                if rPr is not None:
                    color_elem = rPr.find(qn('w:color'))
                    if color_elem is not None:
                        actual_color = color_elem.get(qn('w:val'), '').upper()
            color_results[day] = actual_color
        color_pass = all(v == EXPECTED_FONT_COLOR for v in color_results.values())
        wrong_color = {d: v for d, v in color_results.items() if v != EXPECTED_FONT_COLOR}
        if color_pass:
            print(f"PASS: Component 2 — All 5 day names have font color #{EXPECTED_FONT_COLOR} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected color #{EXPECTED_FONT_COLOR}, wrong values: {wrong_color}")
    except Exception as e:
        print(f"ERROR: Component 2 (font color check) — {e}")

    # Component 3: All 5 day names have character background #FFFFCC (shd fill) (0.25 points)
    # FAILS on initial (no shd element) -> PASSES on golden (shd fill=FFFFCC)
    try:
        bg_results = {}
        for day, run in day_runs.items():
            rPr = run._element.find(qn('w:rPr'))
            bg_color = None
            if rPr is not None:
                shd = rPr.find(qn('w:shd'))
                if shd is not None:
                    bg_color = shd.get(qn('w:fill'), '').upper()
            bg_results[day] = bg_color
        bg_pass = all(v == EXPECTED_BG_COLOR for v in bg_results.values())
        wrong_bg = {d: v for d, v in bg_results.items() if v != EXPECTED_BG_COLOR}
        if bg_pass:
            print(f"PASS: Component 3 — All 5 day names have character background #{EXPECTED_BG_COLOR} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected background #{EXPECTED_BG_COLOR}, wrong values: {wrong_bg}")
    except Exception as e:
        print(f"ERROR: Component 3 (character background check) — {e}")

    # Component 4: All 5 day names have font size 13pt (0.25 points)
    # FAILS on initial (size=12pt) -> PASSES on golden (size=13pt)
    try:
        size_results = {}
        for day, run in day_runs.items():
            if run.font.size is not None:
                size_pt = run.font.size.pt
            else:
                # Fall back to XML w:sz (half-points)
                rPr = run._element.find(qn('w:rPr'))
                size_pt = None
                if rPr is not None:
                    sz_elem = rPr.find(qn('w:sz'))
                    if sz_elem is not None:
                        sz_val = sz_elem.get(qn('w:val'))
                        if sz_val:
                            size_pt = int(sz_val) / 2.0
            size_results[day] = size_pt
        size_pass = all(v == EXPECTED_FONT_SIZE_PT for v in size_results.values())
        wrong_size = {d: v for d, v in size_results.items() if v != EXPECTED_FONT_SIZE_PT}
        if size_pass:
            print(f"PASS: Component 4 — All 5 day names have font size {EXPECTED_FONT_SIZE_PT}pt (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected {EXPECTED_FONT_SIZE_PT}pt, wrong values: {wrong_size}")
    except Exception as e:
        print(f"ERROR: Component 4 (font size check) — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
