"""
Reward Script: Add 'USD ' prefix to all dollar-format currency amounts
Task ID: writer_frd_023
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): At least 1 currency amount has USD prefix (basic transformation)
  Component 2 (0.3): All 16 amounts have USD prefix (complete transformation)
  Component 3 (0.3): No bare dollar amounts remain without USD prefix (no missed amounts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_023'

# Expected number of currency amounts from task context
EXPECTED_COUNT = 16


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

    # Collect all paragraph text
    all_text = ""
    for para in doc.paragraphs:
        all_text += para.text + "\n"

    # Count USD-prefixed dollar amounts: "USD $X,XXX.XX"
    usd_prefixed = re.findall(r'USD \$[\d,]+\.\d{2}', all_text)
    usd_count = len(usd_prefixed)

    # Count bare dollar amounts NOT preceded by "USD ": standalone "$X,XXX.XX"
    # Use negative lookbehind to find dollar amounts without USD prefix
    bare_dollar = re.findall(r'(?<!USD )\$[\d,]+\.\d{2}', all_text)
    bare_count = len(bare_dollar)

    # Total dollar amounts (both prefixed and bare)
    total_amounts = usd_count + bare_count

    print(f"INFO: USD-prefixed amounts: {usd_count}")
    print(f"INFO: Bare dollar amounts (no USD): {bare_count}")
    print(f"INFO: Total currency amounts: {total_amounts}")

    # Component 1: At least 1 currency amount has USD prefix (0.4 points)
    # This checks that the basic regex find-and-replace transformation was applied
    try:
        if usd_count >= 1:
            print(f"PASS: Component 1 -- At least one USD-prefixed amount found ({usd_count}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- No USD-prefixed amounts found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 16 expected amounts have USD prefix (0.3 points)
    # Awards partial credit proportional to how many were converted
    try:
        if usd_count >= EXPECTED_COUNT:
            print(f"PASS: Component 2 -- All {EXPECTED_COUNT} amounts have USD prefix ({usd_count}) (0.3 pts)")
            total_score += 0.3
        elif usd_count > 0:
            partial = 0.3 * (usd_count / EXPECTED_COUNT)
            print(f"PARTIAL: Component 2 -- {usd_count}/{EXPECTED_COUNT} amounts have USD prefix ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No USD-prefixed amounts found (expected {EXPECTED_COUNT})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: No bare dollar amounts remain (0.3 points)
    # Verifies completeness: every dollar amount should have USD prefix
    try:
        if bare_count == 0 and usd_count > 0:
            print(f"PASS: Component 3 -- No bare dollar amounts remain (0.3 pts)")
            total_score += 0.3
        elif bare_count > 0:
            # Partial credit if most are converted
            if usd_count > 0:
                converted_ratio = usd_count / (usd_count + bare_count)
                partial = 0.3 * converted_ratio
                print(f"PARTIAL: Component 3 -- {bare_count} bare amounts remain, {converted_ratio:.0%} converted ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- All {bare_count} dollar amounts still bare (no conversion)")
        else:
            print(f"FAIL: Component 3 -- No currency amounts found at all")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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
