"""
Reward Script: Booklet printing setup - A5 page size with booklet margins
Task ID: writer_rd_074
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Page width is A5 (~14.8 cm / 8391 twips)
  Component 2 (0.30): Page height is A5 (~21.0 cm / 11906 twips)
  Component 3 (0.20): Inner (left/binding) margin is ~2.0 cm (1134 twips)
  Component 4 (0.20): Outer/top/bottom margins are ~1.5 cm (850 twips)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_074'


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

    section = doc.sections[0]

    # Extract raw twip values from XML for precision
    try:
        ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        sect_pr = section._sectPr
        pg_sz = sect_pr.find(f'{{{ns}}}pgSz')
        pg_mar = sect_pr.find(f'{{{ns}}}pgMar')

        w_twips = int(pg_sz.get(f'{{{ns}}}w'))
        h_twips = int(pg_sz.get(f'{{{ns}}}h'))
        left_twips = int(pg_mar.get(f'{{{ns}}}left'))
        right_twips = int(pg_mar.get(f'{{{ns}}}right'))
        top_twips = int(pg_mar.get(f'{{{ns}}}top'))
        bottom_twips = int(pg_mar.get(f'{{{ns}}}bottom'))

        print(f"DEBUG: page width={w_twips} twips, height={h_twips} twips")
        print(f"DEBUG: margins L={left_twips} R={right_twips} T={top_twips} B={bottom_twips} twips")
    except Exception as e:
        print(f"ERROR: Could not parse section XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # A5 dimensions: 148mm x 210mm = 8391 x 11906 twips (1 twip = 1/20 pt = 1/1440 inch)
    # Allow tolerance of ~3mm (~170 twips) for rounding
    TOLERANCE = 170

    # Component 1: Page width is A5 (~8391 twips / 14.8 cm) (0.30 points)
    # Initial is A4: 11906 twips. Golden should be ~8391.
    try:
        expected_w = 8391
        if abs(w_twips - expected_w) <= TOLERANCE:
            print(f"PASS: Component 1 — Page width {w_twips} twips is A5 (expected ~{expected_w}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Page width {w_twips} twips, expected ~{expected_w} (A5)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page height is A5 (~11906 twips / 21.0 cm) (0.30 points)
    # Initial is A4: 16838 twips. Golden should be ~11906.
    try:
        expected_h = 11906
        if abs(h_twips - expected_h) <= TOLERANCE:
            print(f"PASS: Component 2 — Page height {h_twips} twips is A5 (expected ~{expected_h}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Page height {h_twips} twips, expected ~{expected_h} (A5)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Inner (left/binding) margin ~2.0 cm (1134 twips) (0.20 points)
    # Initial is 1440 twips (2.54 cm). Golden should be ~1134 twips (2.0 cm).
    # This is the binding margin for booklet folding.
    try:
        expected_left = 1134
        if abs(left_twips - expected_left) <= TOLERANCE:
            print(f"PASS: Component 3 — Inner margin {left_twips} twips (~2.0 cm for binding) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Inner margin {left_twips} twips, expected ~{expected_left} (2.0 cm)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Outer/top/bottom margins ~1.5 cm (850 twips) (0.20 points)
    # Initial is 1440 twips (2.54 cm). Golden should be ~850 twips (1.5 cm) for all three.
    try:
        expected_outer = 850
        right_ok = abs(right_twips - expected_outer) <= TOLERANCE
        top_ok = abs(top_twips - expected_outer) <= TOLERANCE
        bottom_ok = abs(bottom_twips - expected_outer) <= TOLERANCE

        if right_ok and top_ok and bottom_ok:
            print(f"PASS: Component 4 — Outer margins R={right_twips}, T={top_twips}, B={bottom_twips} (~1.5 cm each) (0.20 pts)")
            total_score += 0.20
        else:
            details = []
            if not right_ok:
                details.append(f"right={right_twips}")
            if not top_ok:
                details.append(f"top={top_twips}")
            if not bottom_ok:
                details.append(f"bottom={bottom_twips}")
            print(f"FAIL: Component 4 — Margins not ~{expected_outer} twips: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved GUI changes
def persist_app_state(domain):
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

persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
