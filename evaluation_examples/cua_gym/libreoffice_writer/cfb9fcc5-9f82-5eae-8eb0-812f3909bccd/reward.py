"""
Reward Script: Decimal-aligned tab stop at 10cm for product price list
Task ID: wrpara_024
Domain: libreoffice_writer
Scoring:
  Precondition gate: 6 product lines with tab + price must exist (0 points - gate only)
  Component 1 (0.6): All 6 product lines have a DECIMAL tab stop
  Component 2 (0.4): All DECIMAL tab stops positioned at 10cm (within tolerance)
"""

import os
import re

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'wrpara_024'

# 10cm in EMU = 10 * 360000 = 3600000. Allow 1% tolerance (~0.1cm)
TARGET_POSITION_EMU = 3600000
POSITION_TOLERANCE = 36000  # ~0.1cm tolerance

# Expected product lines (paragraphs with tab + dollar price)
EXPECTED_PRICES = ['$12.50', '$9.99', '$125.00', '$3.75', '$42.10', '$1,250.00']


def find_product_paragraphs(doc):
    """Find paragraphs that contain a tab character followed by a $ price."""
    product_paras = []
    for para in doc.paragraphs:
        text = para.text
        if '\t' in text and '$' in text:
            product_paras.append(para)
    return product_paras


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

    product_paras = find_product_paragraphs(doc)
    if len(product_paras) < 6:
        print(f"PRECONDITION: Expected 6 product lines, found {len(product_paras)}. Document may be corrupted.")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify text content is intact (no points awarded)
    try:
        para_texts = [para.text for para in product_paras]
        found_prices = sum(1 for price in EXPECTED_PRICES if any(price in text for text in para_texts))
        if found_prices < 6:
            print(f"PRECONDITION: Only {found_prices}/6 expected prices found. Document may be corrupted.")
            print("REWARD: 0.0")
            return 0.0
        print(f"PRECONDITION: All 6 product prices present (gate passed, 0 pts)")
    except Exception as e:
        print(f"ERROR: Precondition check failed: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 product lines have a DECIMAL tab stop (0.6 points)
    try:
        decimal_tab_count = 0
        for para in product_paras:
            tab_stops = para.paragraph_format.tab_stops
            if any(ts.alignment == WD_TAB_ALIGNMENT.DECIMAL for ts in tab_stops):
                decimal_tab_count += 1

        if decimal_tab_count == 6:
            print(f"PASS: Component 1 - All 6 product lines have DECIMAL tab stops (0.6 pts)")
            total_score += 0.6
        elif decimal_tab_count > 0:
            partial = round(0.6 * (decimal_tab_count / 6), 2)
            print(f"PARTIAL: Component 1 - {decimal_tab_count}/6 lines have DECIMAL tab stops ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No product lines have DECIMAL tab stops (0/6)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All DECIMAL tab stops are at 10cm position (0.4 points)
    try:
        correct_position_count = 0
        for para in product_paras:
            tab_stops = para.paragraph_format.tab_stops
            for ts in tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.DECIMAL:
                    if abs(ts.position - TARGET_POSITION_EMU) <= POSITION_TOLERANCE:
                        correct_position_count += 1
                    else:
                        print(f"  INFO: DECIMAL tab at {ts.position} EMU ({ts.position/360000:.2f} cm), expected ~10.00 cm")
                    break  # only check first decimal tab per paragraph

        if correct_position_count == 6:
            print(f"PASS: Component 2 - All 6 DECIMAL tabs at 10cm position (0.4 pts)")
            total_score += 0.4
        elif correct_position_count > 0:
            partial = round(0.4 * (correct_position_count / 6), 2)
            print(f"PARTIAL: Component 2 - {correct_position_count}/6 tabs at correct position ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No DECIMAL tabs at 10cm position (0/6)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
