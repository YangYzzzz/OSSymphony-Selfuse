"""
Reward Script: Verify that survey_table.txt was created from the table on page 2 of survey_results.pdf.
Task ID: pdf_basic_068
Domain: pdf

Task: Open survey_results.pdf in Evince, select and copy the text from the
      table on page 2, and paste it into ~/Desktop/survey_table.txt.

Scoring rubric (total = 1.0):
  Component 1 (0.20): survey_table.txt exists at ~/Desktop/
  Component 2 (0.30): survey_table.txt contains the product line names from the table
  Component 3 (0.30): survey_table.txt contains the numeric score values from the table
  Component 4 (0.20): survey_table.txt contains all 6 data product lines (CRM Pro,
                       Analytics Suite, Mobile App, Enterprise Portal, Data Connector,
                       Support Hub)

  Precondition (not scored): survey_results.pdf existence is verified as a gate —
  if the PDF is missing it indicates a corrupted environment, but its mere presence
  does not indicate task completion and is NOT a scoring component.
"""

import os
import re

DESKTOP_DIR = os.path.expanduser("~/Desktop")
TXT_PATH = os.path.join(DESKTOP_DIR, "survey_table.txt")
PDF_PATH = os.path.join(DESKTOP_DIR, "survey_results.pdf")


def check_txt_exists():
    """Component 1: survey_table.txt exists."""
    return os.path.isfile(TXT_PATH)


def check_product_names():
    """
    Component 2: survey_table.txt contains key product line names from the page-2 table.
    Checks for at least 4 of the 6 data product lines for partial credit.
    """
    if not os.path.isfile(TXT_PATH):
        return 0.0
    try:
        content = open(TXT_PATH, encoding="utf-8", errors="replace").read()
        product_names = [
            "CRM Pro",
            "Analytics Suite",
            "Mobile App",
            "Enterprise Portal",
            "Data Connector",
            "Support Hub",
        ]
        found = sum(1 for name in product_names if name in content)
        if found == len(product_names):
            return 1.0
        elif found >= 4:
            return 0.7
        elif found >= 2:
            return 0.4
        return 0.0
    except Exception as e:
        print(f"ERROR checking product names: {e}")
        return 0.0


def check_numeric_scores():
    """
    Component 3: survey_table.txt contains numeric score values present in the table.
    The table contains scores like 4.3, 4.1, 4.4, 4.5, 3.8, 3.6, 4.0, 3.9, 4.2, etc.
    We require at least 8 distinct score values matching the table's data.
    """
    if not os.path.isfile(TXT_PATH):
        return 0.0
    try:
        content = open(TXT_PATH, encoding="utf-8", errors="replace").read()
        # Expected numeric values appearing in the table (scores and N-counts)
        expected_values = [
            "4.3", "4.1", "4.4",     # CRM Pro
            "4.5", "4.6",            # Mobile App
            "3.8", "3.6",            # Enterprise Portal
            "4.2", "3.9",            # Analytics Suite / Support Hub
            "1247",                  # All Products N
        ]
        found = sum(1 for v in expected_values if v in content)
        if found >= 9:
            return 1.0
        elif found >= 6:
            return 0.7
        elif found >= 3:
            return 0.4
        return 0.0
    except Exception as e:
        print(f"ERROR checking numeric scores: {e}")
        return 0.0


def check_all_product_lines():
    """
    Component 4: All 6 data product lines present in survey_table.txt.
    Returns 1.0 only if all 6 are present.
    """
    if not os.path.isfile(TXT_PATH):
        return 0.0
    try:
        content = open(TXT_PATH, encoding="utf-8", errors="replace").read()
        product_names = [
            "CRM Pro",
            "Analytics Suite",
            "Mobile App",
            "Enterprise Portal",
            "Data Connector",
            "Support Hub",
        ]
        missing = [name for name in product_names if name not in content]
        if not missing:
            print(f"PASS: All 6 product lines present in survey_table.txt")
            return 1.0
        else:
            print(f"FAIL: Missing product lines: {missing}")
            return 0.0
    except Exception as e:
        print(f"ERROR checking all product lines: {e}")
        return 0.0


def compute_reward():
    """Compute the final reward score."""
    # Precondition gate: if PDF is missing, environment is broken
    if not os.path.isfile(PDF_PATH):
        print(f"PRECONDITION FAIL: {PDF_PATH} does not exist — environment broken")
        print("REWARD: 0.0")
        return 0.0

    checks = [
        {
            "name": "txt_file_exists",
            "func": check_txt_exists,
            "weight": 0.20,
        },
        {
            "name": "product_names_present",
            "func": check_product_names,
            "weight": 0.30,
        },
        {
            "name": "numeric_scores_present",
            "func": check_numeric_scores,
            "weight": 0.30,
        },
        {
            "name": "all_product_lines",
            "func": check_all_product_lines,
            "weight": 0.20,
        },
    ]

    total_weight = sum(c["weight"] for c in checks)
    score = 0.0
    details = {}

    for check in checks:
        try:
            result = check["func"]()
            if isinstance(result, bool):
                result = 1.0 if result else 0.0
            result = float(result)
        except Exception as e:
            print(f"ERROR: check '{check['name']}' raised exception: {e}")
            result = 0.0

        weighted = result * check["weight"]
        score += weighted
        details[check["name"]] = result
        status = "PASS" if result >= 0.9 else ("PARTIAL" if result > 0.0 else "FAIL")
        print(f"  [{status}] {check['name']}: {result:.2f} (weight={check['weight']:.2f}, contribution={weighted:.3f})")

    reward = round(score / total_weight, 4)

    print(f"\nScore: {score:.4f}/{total_weight:.2f}")
    print(f"REWARD: {reward}")
    return reward


if __name__ == "__main__":
    print(f"=== Reward Verification: pdf_basic_068 ===")
    print(f"Checking: {TXT_PATH}")
    print(f"PDF:      {PDF_PATH}")
    print()
    compute_reward()
