"""
Reward Script: Format invoice lines with center-aligned tab stops at 10cm
Task ID: osworld_writer_tabstop_003
Domain: libreoffice_writer
Scoring:
  Component 1: All 8 paragraphs have CENTER tab stop at ~10cm  (0.5 pts)
  Component 2: All 8 paragraphs contain a tab inserted after 4 words, dollar amount after tab (0.5 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_003'

# 10cm expressed in EMU (914400 EMU per inch, 2.54 cm per inch)
# 10cm = 10 / 2.54 * 914400 = 3599999.999... ≈ 3600000
# Setup-gen used 3599815 — allow ±5% tolerance (~180000 EMU = ~0.5cm)
TARGET_CM = 10.0
CM_TO_EMU = 914400 / 2.54
TARGET_EMU = TARGET_CM * CM_TO_EMU  # ~3599999 EMU
TOLERANCE_EMU = TARGET_EMU * 0.05   # 5% = ~180000 EMU (~0.5cm)


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

    # Precondition: document has 8 non-empty paragraphs
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    if len(paragraphs) != 8:
        print(f"PRECONDITION FAIL: Expected 8 non-empty paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Each of the 8 paragraphs must have a CENTER-aligned tab stop at ~10cm (0.5 pts)
    # This FAILS on initial (no custom tab stops) and PASSES on golden (CENTER@10cm on all 8)
    try:
        paragraphs_with_center_tabstop = 0
        details_comp1 = []
        for i, para in enumerate(paragraphs):
            # Count qualifying center tab stops at ~10cm for this paragraph
            matching_stops = [
                ts for ts in para.paragraph_format.tab_stops
                if ts.alignment == WD_TAB_ALIGNMENT.CENTER
                and abs(ts.position - TARGET_EMU) <= TOLERANCE_EMU
            ]
            if len(matching_stops) >= 1:
                paragraphs_with_center_tabstop += 1
            else:
                details_comp1.append(f"Para {i} missing CENTER@10cm tabstop")

        if paragraphs_with_center_tabstop == 8:
            print(f"PASS: Component 1 — All 8 paragraphs have CENTER tab stop at ~10cm (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Only {paragraphs_with_center_tabstop}/8 paragraphs have CENTER tab stop at ~10cm")
            for d in details_comp1:
                print(f"  {d}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each of the 8 paragraphs must contain a tab character between
    # the 4th word and the dollar amount (0.5 pts)
    # This FAILS on initial (no tabs in any line) and PASSES on golden (tab after word 4)
    try:
        paragraphs_with_tab_structure = 0
        details_comp2 = []
        for i, para in enumerate(paragraphs):
            text = para.text
            if '\t' not in text:
                details_comp2.append(f"Para {i}: no tab character found in '{text[:50]}'")
                continue
            parts = text.split('\t')
            if len(parts) != 2:
                details_comp2.append(f"Para {i}: expected exactly 1 tab, found {len(parts)-1}: '{text[:50]}'")
                continue
            before_tab = parts[0].strip()
            after_tab = parts[1].strip()
            # Before tab should be exactly 4 words
            words_before = before_tab.split()
            # After tab should start with a dollar sign (invoice amount)
            if len(words_before) == 4 and after_tab.startswith('$'):
                paragraphs_with_tab_structure += 1
            else:
                details_comp2.append(
                    f"Para {i}: words_before_tab={len(words_before)} (expected 4), "
                    f"after_tab_starts_with_dollar={after_tab.startswith('$')}"
                )

        if paragraphs_with_tab_structure == 8:
            print(f"PASS: Component 2 — All 8 paragraphs have tab after 4 words with dollar amount after (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Only {paragraphs_with_tab_structure}/8 paragraphs have correct tab structure")
            for d in details_comp2:
                print(f"  {d}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
