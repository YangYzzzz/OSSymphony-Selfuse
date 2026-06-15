"""
Reward Script: Configure full print setup on 'Annual Report' sheet
Task ID: calc_ggf_030
Domain: libreoffice_calc
Scoring:
  - Component 1: Paper size A3 + landscape orientation (0.20)
  - Component 2: Print area A1:N60 (0.20)
  - Component 3: Repeating title rows 1-3 (0.20)
  - Component 4: Repeating title columns A-B (0.15)
  - Component 5: Scale set to 85% (0.10)
  - Component 6: Centered footer with page numbering (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_030'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice state before verification."""
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
    Verify print setup configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that 'Annual Report' sheet exists
    if 'Annual Report' not in wb.sheetnames:
        print("CRITICAL: 'Annual Report' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Annual Report']
    ps = ws.page_setup

    # Component 1: Paper size = A3 (8) and orientation = landscape (0.20 points)
    try:
        paper_ok = (ps.paperSize is not None and int(ps.paperSize) == 8)
        orient_ok = (ps.orientation is not None and str(ps.orientation).lower() == 'landscape')
        if paper_ok and orient_ok:
            print(f"PASS: Component 1 — Paper size A3 ({ps.paperSize}) + landscape ({ps.orientation}) (0.20 pts)")
            total_score += 0.20
        elif paper_ok:
            print(f"PARTIAL: Component 1 — Paper size A3 correct, but orientation={ps.orientation} (0.10 pts)")
            total_score += 0.10
        elif orient_ok:
            print(f"PARTIAL: Component 1 — Orientation landscape correct, but paperSize={ps.paperSize} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Expected paper=8(A3) landscape, found paper={ps.paperSize} orient={ps.orientation}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Print area = A1:N60 (0.20 points)
    try:
        print_area = ws.print_area
        # print_area may be a string like "'Annual Report'!$A$1:$N$60" or "$A$1:$N$60"
        # Normalize: remove sheet name prefix, dollar signs, spaces
        area_str = str(print_area) if print_area else ''
        # Extract just the cell range part
        normalized = area_str.upper().replace('$', '').replace(' ', '')
        # Remove possible sheet name prefix (e.g., "'ANNUAL REPORT'!")
        if '!' in normalized:
            normalized = normalized.split('!')[-1]
        # Remove quotes/brackets
        normalized = normalized.strip("'\"[]")

        if normalized == 'A1:N60':
            print(f"PASS: Component 2 — Print area is A1:N60 (raw: {print_area}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected print area A1:N60, found: {print_area} (normalized: {normalized})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Repeating title rows = rows 1-3 (0.20 points)
    try:
        title_rows = ws.print_title_rows
        # Expected: "$1:$3" or "1:3"
        rows_str = str(title_rows) if title_rows else ''
        normalized_rows = rows_str.replace('$', '').replace(' ', '')
        if normalized_rows == '1:3':
            print(f"PASS: Component 3 — Title rows are 1:3 (raw: {title_rows}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected title rows 1:3, found: {title_rows}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Repeating title columns = A-B (0.15 points)
    try:
        title_cols = ws.print_title_cols
        # Expected: "$A:$B" or "A:B"
        cols_str = str(title_cols) if title_cols else ''
        normalized_cols = cols_str.replace('$', '').replace(' ', '').upper()
        if normalized_cols == 'A:B':
            print(f"PASS: Component 4 — Title columns are A:B (raw: {title_cols}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected title columns A:B, found: {title_cols}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Scale = 85% (0.10 points)
    try:
        scale_val = ps.scale
        if scale_val is not None and int(scale_val) == 85:
            print(f"PASS: Component 5 — Scale is 85% ({scale_val}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Expected scale 85, found: {scale_val}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Centered footer with page numbering "Page &P of &N" (0.15 points)
    try:
        footer = ws.oddFooter
        center_text = footer.center.text if footer and footer.center else ''
        # The footer should contain a pattern like "Page &P of &N" or "Page X of Y"
        # In openpyxl, &P = page number, &N = total pages
        if center_text:
            # Normalize and check for the "Page &P of &N" pattern
            norm_footer = center_text.strip()
            # Check for exact or close match: "Page &P of &N"
            if '&P' in norm_footer and '&N' in norm_footer:
                # Verify it's roughly "Page &P of &N" format
                pattern = re.compile(r'[Pp]age\s*&P\s*of\s*&N', re.IGNORECASE)
                if pattern.search(norm_footer):
                    print(f"PASS: Component 6 — Footer center has 'Page &P of &N' (raw: {center_text}) (0.15 pts)")
                    total_score += 0.15
                else:
                    # Has &P and &N but not in exact "Page X of Y" format — partial credit
                    print(f"PARTIAL: Component 6 — Footer has &P and &N but not in 'Page X of Y' format: {center_text} (0.08 pts)")
                    total_score += 0.08
            else:
                print(f"FAIL: Component 6 — Footer center missing &P or &N: {center_text}")
        else:
            # Also check left and right footer sections
            left_text = footer.left.text if footer and footer.left else ''
            right_text = footer.right.text if footer and footer.right else ''
            print(f"FAIL: Component 6 — No centered footer text. Left: {left_text}, Right: {right_text}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_calc")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
