"""
Reward Script: Format 'CONFIDENTIAL' title with condensed character spacing reduced by 1.5pt
Task ID: writer_txtfmt_032
Domain: libreoffice_writer
Scoring:
  Component 1 (0.7): CONFIDENTIAL title has character spacing condensed by 1.5pt (w:spacing val = -30 twips)
  Component 2 (0.3): CONFIDENTIAL character spacing is exactly -30 twips AND original font properties
                     (Bold, 16pt, Arial) are intact — compound check anchored to the change
"""

import os
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_032'
FILE_NAME = 'classified_report.docx'

# Character spacing in OOXML is stored in twentieths of a point (twips)
# Condensed by 1.5pt = -1.5pt * 20 = -30 twips
EXPECTED_SPACING_VAL = -30
EXPECTED_SPACING_TOLERANCE = 2  # allow ±2 twips tolerance


def verify_task(file_path):
    """
    Verify that the CONFIDENTIAL title has condensed character spacing of 1.5pt.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document - if it fails, we can't verify anything
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: Find the CONFIDENTIAL paragraph (should be first paragraph)
    confidential_para = None
    try:
        for para in doc.paragraphs:
            if para.text.strip() == 'CONFIDENTIAL':
                confidential_para = para
                break
        if confidential_para is None:
            print("FAIL: Could not find 'CONFIDENTIAL' paragraph in document")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
        else:
            print(f"INFO: Found 'CONFIDENTIAL' paragraph")
    except Exception as e:
        print(f"ERROR: Could not locate CONFIDENTIAL paragraph: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: extract spacing value from the CONFIDENTIAL run
    def get_spacing_val():
        """Returns integer spacing value in twips, or None if not set."""
        for run in confidential_para.runs:
            rpr = run._element.find(qn('w:rPr'))
            if rpr is not None:
                spacing_elem = rpr.find(qn('w:spacing'))
                if spacing_elem is not None:
                    raw_val = spacing_elem.get(qn('w:val'))
                    if raw_val is not None:
                        return int(raw_val)
        return None

    # Component 1: CONFIDENTIAL title has condensed character spacing of 1.5pt (0.7 points)
    # This check FAILS on initial_env (no spacing element) and PASSES on golden_env (val=-30).
    # In OOXML, character spacing (w:spacing w:val) is stored in twentieths of a point.
    # Condensed 1.5pt = -30 twips (negative value means condensed/reduced spacing).
    try:
        spacing_val = get_spacing_val()

        if spacing_val is not None:
            if abs(spacing_val - EXPECTED_SPACING_VAL) <= EXPECTED_SPACING_TOLERANCE:
                print(f"PASS: Component 1 — CONFIDENTIAL character spacing is {spacing_val} twips "
                      f"(= condensed {abs(spacing_val)/20.0:.1f}pt, expected condensed 1.5pt) (0.7 pts)")
                total_score += 0.7
            else:
                actual_pt = spacing_val / 20.0
                print(f"FAIL: Component 1 — CONFIDENTIAL character spacing is {spacing_val} twips "
                      f"({actual_pt:.2f}pt), expected {EXPECTED_SPACING_VAL} twips (condensed 1.5pt)")
        else:
            print(f"FAIL: Component 1 — No character spacing element found on CONFIDENTIAL title "
                  f"(expected condensed 1.5pt = -30 twips; spacing element absent)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check character spacing: {e}")

    # Component 2: Character spacing is exactly -30 twips AND original font properties are intact
    # (Bold, 16pt, Arial). This is a compound check anchored to the task change:
    # it only passes when the spacing was applied WITHOUT corrupting the rest of the title formatting.
    # This FAILS on initial_env (spacing is absent) and PASSES on golden_env.
    try:
        spacing_val = get_spacing_val()
        # Only evaluate font integrity if the spacing change was actually applied
        if spacing_val is not None and abs(spacing_val - EXPECTED_SPACING_VAL) <= EXPECTED_SPACING_TOLERANCE:
            comp2_pass = False
            comp2_details = "No text runs found in CONFIDENTIAL paragraph"
            for run in confidential_para.runs:
                if run.text.strip():
                    is_bold = run.font.bold is True
                    size_ok = run.font.size is not None and abs(run.font.size.pt - 16.0) < 0.5
                    name_ok = run.font.name == 'Arial'
                    font_issues = []
                    if not is_bold:
                        font_issues.append(f"bold={run.font.bold} (expected True)")
                    if not size_ok:
                        actual_size = run.font.size.pt if run.font.size else None
                        font_issues.append(f"size={actual_size}pt (expected 16.0pt)")
                    if not name_ok:
                        font_issues.append(f"name={run.font.name!r} (expected 'Arial')")
                    # comp2_pass derived from absence of issues (not hardcoded)
                    comp2_pass = (len(font_issues) == 0)
                    if comp2_pass:
                        comp2_details = (f"bold={run.font.bold}, size={run.font.size.pt}pt, "
                                         f"name={run.font.name}")
                    else:
                        comp2_details = f"Font properties changed: {', '.join(font_issues)}"
                    break
            if comp2_pass:
                print(f"PASS: Component 2 — Spacing applied AND font properties intact: "
                      f"{comp2_details} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — {comp2_details}")
        else:
            # Spacing not applied → this compound check necessarily fails (correct for initial_env)
            print(f"FAIL: Component 2 — Skipped (requires spacing to be applied first; "
                  f"spacing_val={spacing_val})")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check compound font integrity: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on VM
file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
