"""
Reward Script: Two-level numbered list for thesis outline
Task ID: writer_acad_072
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Level 1 items have correct "N." numbering
  Component 2 (0.35): Level 2 items have correct "N.M" numbering
  Component 3 (0.30): Level 2 items are indented relative to Level 1
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_072'

# Expected structure: (paragraph_index, level, expected_prefix)
# Level 1 items (main chapters)
LEVEL1_ITEMS = [
    (2, "Introduction"),
    (6, "Literature Review"),
    (10, "Methodology"),
    (14, "Results and Analysis"),
    (17, "Discussion"),
    (21, "Conclusion and Future Directions"),
]

# Level 2 items grouped by parent
LEVEL2_ITEMS = [
    (3, 1, 1, "Background and Motivation"),
    (4, 1, 2, "Research Questions and Objectives"),
    (5, 1, 3, "Scope and Limitations of the Study"),
    (7, 2, 1, "Historical Development of AI in Medicine"),
    (8, 2, 2, "Current Applications of Machine Learning in Diagnostics"),
    (9, 2, 3, "Ethical Frameworks for AI-Assisted Decision Making"),
    (11, 3, 1, "Research Design and Approach"),
    (12, 3, 2, "Data Collection Methods and Sources"),
    (13, 3, 3, "Analytical Framework and Statistical Tools"),
    (15, 4, 1, "Quantitative Findings from Hospital Case Studies"),
    (16, 4, 2, "Qualitative Assessment of Clinician Perspectives"),
    (18, 5, 1, "Interpretation of Key Findings"),
    (19, 5, 2, "Comparison with Existing Literature"),
    (20, 5, 3, "Implications for Healthcare Policy"),
    (22, 6, 1, "Summary of Contributions"),
    (23, 6, 2, "Recommendations for Practitioners"),
    (24, 6, 3, "Proposed Areas for Further Research"),
]


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    paras = doc.paragraphs
    if len(paras) < 25:
        print(f"FAIL: Expected at least 25 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Level 1 items have correct "N." numbering (0.35 points)
    # Each of the 6 level-1 items should start with "N. " where N is 1-6
    try:
        l1_pass = 0
        l1_total = len(LEVEL1_ITEMS)
        for idx, (pidx, topic_name) in enumerate(LEVEL1_ITEMS):
            expected_num = idx + 1
            text = paras[pidx].text.strip()
            # Check if text starts with "N." or "N. " pattern
            pattern = rf'^{expected_num}\.\s+'
            if re.match(pattern, text) and topic_name.lower() in text.lower():
                l1_pass += 1
                print(f"  PASS: P{pidx} has correct L1 numbering: [{text[:50]}]")
            else:
                print(f"  FAIL: P{pidx} expected '{expected_num}. {topic_name}', got [{text[:50]}]")

        if l1_pass == l1_total:
            print(f"PASS: Component 1 -- All {l1_total} Level 1 items correctly numbered (0.35 pts)")
            total_score += 0.35
        elif l1_pass > 0:
            partial = round(0.35 * l1_pass / l1_total, 3)
            print(f"PARTIAL: Component 1 -- {l1_pass}/{l1_total} Level 1 items numbered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No Level 1 items have correct numbering")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Level 2 items have correct "N.M" numbering (0.35 points)
    # Each sub-item should start with "N.M " where N is parent number and M is sub-number
    try:
        l2_pass = 0
        l2_total = len(LEVEL2_ITEMS)
        for pidx, parent_num, sub_num, topic_name in LEVEL2_ITEMS:
            text = paras[pidx].text.strip()
            # Check for "N.M " or "N.M. " pattern
            pattern = rf'^{parent_num}\.{sub_num}\s+'
            if re.match(pattern, text) and topic_name.lower() in text.lower():
                l2_pass += 1
            else:
                print(f"  FAIL: P{pidx} expected '{parent_num}.{sub_num} {topic_name}', got [{text[:60]}]")

        if l2_pass == l2_total:
            print(f"PASS: Component 2 -- All {l2_total} Level 2 items correctly numbered (0.35 pts)")
            total_score += 0.35
        elif l2_pass > 0:
            partial = round(0.35 * l2_pass / l2_total, 3)
            print(f"PARTIAL: Component 2 -- {l2_pass}/{l2_total} Level 2 items numbered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No Level 2 items have correct numbering")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Level 2 items are indented (0.30 points)
    # Level 2 items should have left_indent > 0 (golden has 457200 EMU = 0.5 inches)
    # Level 1 items should NOT be indented (or less indented than Level 2)
    try:
        l2_indented = 0
        l2_indent_total = len(LEVEL2_ITEMS)
        for pidx, _, _, _ in LEVEL2_ITEMS:
            left_indent = paras[pidx].paragraph_format.left_indent
            if left_indent is not None and left_indent > 0:
                l2_indented += 1
            else:
                print(f"  FAIL: P{pidx} has no indentation (left_indent={left_indent})")

        # Also check that Level 1 items are NOT indented (or less)
        l1_not_indented = 0
        for pidx, _ in LEVEL1_ITEMS:
            left_indent = paras[pidx].paragraph_format.left_indent
            if left_indent is None or left_indent == 0:
                l1_not_indented += 1

        # Need both: L2 indented AND L1 not indented
        l2_ratio = l2_indented / l2_indent_total if l2_indent_total > 0 else 0
        l1_ratio = l1_not_indented / len(LEVEL1_ITEMS) if len(LEVEL1_ITEMS) > 0 else 0

        if l2_ratio >= 0.8 and l1_ratio >= 0.8:
            print(f"PASS: Component 3 -- Level 2 indented ({l2_indented}/{l2_indent_total}), Level 1 not indented ({l1_not_indented}/{len(LEVEL1_ITEMS)}) (0.30 pts)")
            total_score += 0.30
        elif l2_ratio > 0:
            partial_indent = round(0.30 * l2_ratio * 0.8, 3)  # penalize if L1 also indented
            print(f"PARTIAL: Component 3 -- {l2_indented}/{l2_indent_total} L2 indented, {l1_not_indented}/{len(LEVEL1_ITEMS)} L1 not indented ({partial_indent} pts)")
            total_score += partial_indent
        else:
            print(f"FAIL: Component 3 -- No Level 2 items are indented")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
