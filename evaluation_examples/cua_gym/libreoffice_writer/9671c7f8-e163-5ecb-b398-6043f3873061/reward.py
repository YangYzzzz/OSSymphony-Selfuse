"""
Reward Script: Modify list numbering format to '1.)' style
Task ID: writer_list_057
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): The ListNumber style abstractNum (abstractNumId=7) has lvlText="%1.)"
  Component 2 (0.4): All decimal numbering abstractNums in the document use "%1.)" format
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_list_057'

FILE_PATH = f'{WORKDIR}/Desktop/ranking.docx'

TARGET_LVL_TEXT = '%1.)'   # Expected format after task completion
INITIAL_LVL_TEXT = '%1.'   # Original format before task


def verify_task(file_path):
    """
    Verify that the list numbering format was changed from '%1.' to '%1.)'.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load document - fail fast if file is unreadable
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: numbering part must exist
    try:
        numbering_part = doc.part.numbering_part
        abstractNums = numbering_part._element.findall(qn('w:abstractNum'))
    except Exception as e:
        print(f"CRITICAL: Cannot read numbering part: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ----------------------------------------------------------------
    # Component 1: The ListNumber style abstractNum uses '%1.)' format
    #   The 'List Number' paragraphs in this document use numId=5 which
    #   links to abstractNumId=7 (pStyle='ListNumber'). In the golden
    #   file this abstractNum must have lvlText='%1.)' instead of '%1.'.
    #   Weight: 0.6
    # ----------------------------------------------------------------
    try:
        # Collect all ListNumber pStyle lvlText values from numbering part
        list_number_lvl_texts = []
        for abstractNum in abstractNums:
            for lvl in abstractNum.findall(qn('w:lvl')):
                pStyle = lvl.find(qn('w:pStyle'))
                if pStyle is not None and pStyle.get(qn('w:val')) == 'ListNumber':
                    lvlText = lvl.find(qn('w:lvlText'))
                    actual_val = lvlText.get(qn('w:val')) if lvlText is not None else None
                    list_number_lvl_texts.append(actual_val)

        if not list_number_lvl_texts:
            print("FAIL: Component 1 — ListNumber pStyle abstractNum not found in numbering part")
        elif all(val == TARGET_LVL_TEXT for val in list_number_lvl_texts):
            print(f"PASS: Component 1 — ListNumber abstractNum has lvlText='{list_number_lvl_texts[0]}' (0.6 pts)")
            total_score += 0.6
        else:
            for val in list_number_lvl_texts:
                if val != TARGET_LVL_TEXT:
                    print(f"FAIL: Component 1 — ListNumber abstractNum lvlText expected '{TARGET_LVL_TEXT}', found '{val}'")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: ALL decimal numbering abstractNums use '%1.)' format
    #   The task instruction asks to change ALL numbered items to the
    #   '1.)' format. In the golden file, every decimal-type abstractNum
    #   (not just the ListNumber one) should have lvlText='%1.)'.
    #   This verifies the change was applied globally (not just to one level).
    #   Weight: 0.4
    # ----------------------------------------------------------------
    try:
        decimal_abs_nums = []
        for abstractNum in abstractNums:
            for lvl in abstractNum.findall(qn('w:lvl')):
                numFmt = lvl.find(qn('w:numFmt'))
                if numFmt is not None and numFmt.get(qn('w:val')) == 'decimal':
                    lvlText = lvl.find(qn('w:lvlText'))
                    actual_val = lvlText.get(qn('w:val')) if lvlText is not None else None
                    abs_id = abstractNum.get(qn('w:abstractNumId'))
                    decimal_abs_nums.append((abs_id, actual_val))

        if not decimal_abs_nums:
            print("FAIL: Component 2 — No decimal numbering abstractNums found")
        else:
            all_correct = all(val == TARGET_LVL_TEXT for _, val in decimal_abs_nums)
            incorrect = [(abs_id, val) for abs_id, val in decimal_abs_nums if val != TARGET_LVL_TEXT]
            if all_correct:
                print(f"PASS: Component 2 — All {len(decimal_abs_nums)} decimal abstractNums have lvlText='{TARGET_LVL_TEXT}' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — {len(incorrect)} of {len(decimal_abs_nums)} decimal abstractNums still have wrong format:")
                for abs_id, val in incorrect:
                    print(f"  abstractNumId={abs_id} has lvlText='{val}' (expected '{TARGET_LVL_TEXT}')")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
