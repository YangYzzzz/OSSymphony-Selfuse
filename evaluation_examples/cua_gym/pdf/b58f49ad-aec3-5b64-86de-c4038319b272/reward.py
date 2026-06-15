"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the project timeline table from 'project_plan.pdf' (page 6) in /home/user/Projects and save to 'timeline_data.xlsx'.
Generated: 2025-11-29 09:24:06
Status: success
Model: o3
Total Steps: 9
"""

import pathlib
from typing import Tuple

# Reward Script: Verify timeline_data.xlsx was correctly created from project_plan.pdf (page 6)
# Author: Auto-generated reward script
# --------------------------------------------------------------
# SCORING RUBRIC (progressive)
#   0.25 – Header row matches exactly Phase/Start/End/Owner
#   0.25 – All four required phases are present (Planning, Design, Implementation, Testing)
#   0.25 – Start & End dates for every phase match expected values
#   0.25 – Owners for every phase match expected values
#   1.00 – All checks pass
# --------------------------------------------------------------

EXPECTED_HEADER: Tuple[str, str, str, str] = (
    "Phase",
    "Start",
    "End",
    "Owner",
)

EXPECTED_ROWS = {
    "Planning": ("2024-01-01", "2024-01-15", "Alice"),
    "Design": ("2024-01-16", "2024-02-15", "Bob"),
    "Implementation": ("2024-02-16", "2024-04-30", "Charlie"),
    "Testing": ("2024-05-01", "2024-05-31", "Dana"),
}


def _cell_to_str(value):
    """Helper to normalise cell values into comparable strings."""
    import datetime as _dt

    if value is None:
        return ""
    if isinstance(value, (_dt.date, _dt.datetime)):
        return value.strftime("%Y-%m-%d")
    return str(value).strip()


def verify_timeline_excel() -> float:
    """Main verification routine – returns reward score between 0.0 and 1.0."""
    import openpyxl

    # --------------- Locate Excel file ----------------
    xlsx_path = pathlib.Path("/home/user/Projects/timeline_data.xlsx")
    if not xlsx_path.exists():
        print(f"✗ Missing Excel file: {xlsx_path}")
        print("REWARD: 0.0")
        return 0.0

    # --------------- Load Workbook -------------------
    try:
        wb = openpyxl.load_workbook(xlsx_path)
    except Exception as e:
        print(f"✗ Failed to load workbook: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active  # first sheet is sufficient
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("✗ Workbook is empty – no data rows found")
        print("REWARD: 0.0")
        return 0.0

    # --------------- Check Header --------------------
    header = tuple(_cell_to_str(c) for c in rows[0])
    header_ok = header == EXPECTED_HEADER
    if header_ok:
        print("✓ Header matches expected")
    else:
        print(f"✗ Header mismatch. Found {header} – Expected {EXPECTED_HEADER}")

    # --------------- Build Data Mapping --------------
    data_mapping = {}
    for row in rows[1:]:
        if not any(row):  # skip entirely blank rows
            continue
        phase, start, end, owner = row[:4]
        phase_key = _cell_to_str(phase)
        data_mapping[phase_key] = (
            _cell_to_str(start),
            _cell_to_str(end),
            _cell_to_str(owner),
        )

    # --------------- Phase Presence ------------------
    phases_ok = all(phase in data_mapping for phase in EXPECTED_ROWS)
    if phases_ok:
        print("✓ All required phases present")
    else:
        missing = [p for p in EXPECTED_ROWS if p not in data_mapping]
        print(f"✗ Missing phases: {missing}")

    # --------------- Dates & Owners ------------------
    dates_ok = True
    owners_ok = True
    for phase, (exp_start, exp_end, exp_owner) in EXPECTED_ROWS.items():
        if phase not in data_mapping:
            dates_ok = owners_ok = False
            continue
        start, end, owner = data_mapping[phase]
        if (start, end) != (exp_start, exp_end):
            print(f"✗ Date mismatch for {phase}: Found {start}->{end} – Expected {exp_start}->{exp_end}")
            dates_ok = False
        if owner != exp_owner:
            print(f"✗ Owner mismatch for {phase}: Found '{owner}' – Expected '{exp_owner}'")
            owners_ok = False

    if dates_ok:
        print("✓ All start/end dates match expected")
    if owners_ok:
        print("✓ All owners match expected")

    # --------------- Progressive Scoring -------------
    score = 0.0
    if header_ok:
        score += 0.25
    if phases_ok:
        score += 0.25
    if dates_ok:
        score += 0.25
    if owners_ok:
        score += 0.25

    final_score = round(min(score, 1.0), 2)  # keep within [0,1]
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_timeline_excel()
