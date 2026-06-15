"""
Reward Script: Set a left-aligned tab stop at 5cm and type a two-column list
              of 3 country-capital pairs using the tab stop for alignment.
Task ID: wrpara_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): Document has exactly 3 non-empty paragraphs
  Component 2 (0.4): Correct country-capital pairs with tab separation
  Component 3 (0.4): Left-aligned tab stop at ~5cm on each paragraph
"""

import os

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'wrpara_009'

# 5 cm in EMU (1 cm = 360000 EMU)
TARGET_TAB_POS = 5 * 360000  # 1800000 EMU
TAB_TOLERANCE = 72000  # ~0.2 cm tolerance

# Expected country-capital pairs (order matters per task context)
EXPECTED_PAIRS = [
    ("France", "Paris"),
    ("Germany", "Berlin"),
    ("Japan", "Tokyo"),
]


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

    # Filter to non-empty paragraphs only
    non_empty_paras = [p for p in doc.paragraphs if p.text.strip()]

    # Component 1: Document has exactly 3 non-empty paragraphs (0.2 points)
    try:
        num_paras = len(non_empty_paras)
        if num_paras == 3:
            print(f"PASS: Component 1 — 3 non-empty paragraphs found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected 3 non-empty paragraphs, found {num_paras}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct country-capital pairs with tab separation (0.4 points)
    # Each pair is worth ~0.133 points
    try:
        pairs_score = 0.0
        per_pair = 0.4 / 3.0

        for idx, expected in enumerate(EXPECTED_PAIRS):
            country, capital = expected
            if idx < len(non_empty_paras):
                para_text = non_empty_paras[idx].text.strip()
                # Check that text contains tab character separating country and capital
                if '\t' in para_text:
                    parts = para_text.split('\t')
                    found_country = parts[0].strip()
                    found_capital = parts[-1].strip()
                    if found_country == country and found_capital == capital:
                        print(f"PASS: Component 2.{idx+1} — '{country}\\t{capital}' found ({per_pair:.3f} pts)")
                        pairs_score += per_pair
                    else:
                        print(f"FAIL: Component 2.{idx+1} — expected '{country}\\t{capital}', found '{found_country}\\t{found_capital}'")
                else:
                    print(f"FAIL: Component 2.{idx+1} — no tab character in paragraph: '{para_text}'")
            else:
                print(f"FAIL: Component 2.{idx+1} — paragraph {idx} not found")

        total_score += pairs_score
        if pairs_score > 0:
            print(f"  Component 2 subtotal: {pairs_score:.3f}/0.4")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Left-aligned tab stop at ~5cm on each paragraph (0.4 points)
    # Each paragraph's tab stop is worth ~0.133 points
    try:
        tab_score = 0.0
        per_tab = 0.4 / 3.0

        for idx in range(min(3, len(non_empty_paras))):
            para = non_empty_paras[idx]
            tab_stops = []
            for ts in para.paragraph_format.tab_stops:
                # Filter out CLEAR and default LEFT@0 stops
                if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                    continue
                if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0:
                    continue
                tab_stops.append(ts)

            found_valid = False
            for ts in tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.LEFT and abs(ts.position - TARGET_TAB_POS) <= TAB_TOLERANCE:
                    print(f"PASS: Component 3.{idx+1} — LEFT tab stop at {ts.position} EMU (~{ts.position/360000:.2f}cm), target 5.00cm ({per_tab:.3f} pts)")
                    tab_score += per_tab
                    found_valid = True
                    break

            if not found_valid:
                positions = [(str(ts.alignment), ts.position) for ts in tab_stops]
                print(f"FAIL: Component 3.{idx+1} — no LEFT tab stop at ~5cm found. Tab stops: {positions}")

        total_score += tab_score
        if tab_score > 0:
            print(f"  Component 3 subtotal: {tab_score:.3f}/0.4")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
