"""
Reward Script: Cross-reference fields for Section references in a legal contract
Task ID: writer_legal_053
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): At least 10 REF field instrText elements exist (cross-references present)
  Component 2 (0.3): All 12 expected bookmark targets are referenced correctly
  Component 3 (0.3): Field structure integrity — each REF has begin/instrText/end triplet
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_053'

# The 12 expected cross-reference bookmark targets (derived from task context:
# 12 manual "see Section X.X" references that should become REF fields)
EXPECTED_REF_TARGETS = {
    '_Section_1_1',
    '_Section_3_1',
    '_Section_2_2',
    '_Section_4_3',
    '_Section_6_1',
    '_Section_5_2',
    '_Section_7_2',
    '_Section_8_1',
    '_Section_9_3',
    '_Section_10_2',
    '_Section_3_2',
    '_Section_11_4',
}


def verify_task(file_path):
    """
    Verify that manual section references have been replaced with cross-reference fields.
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

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Component 1: REF field instrText elements exist (0.4 points)
    # In the initial file there are 0 instrText elements; golden should have 12.
    try:
        instr_texts = doc.element.findall('.//w:instrText', ns)
        ref_instrs = []
        for it in instr_texts:
            if it.text and 'REF' in it.text and '\\h' in it.text:
                ref_instrs.append(it.text.strip())

        ref_count = len(ref_instrs)
        print(f"INFO: Found {ref_count} REF instrText elements")

        if ref_count >= 12:
            print(f"PASS: Component 1 — 12+ REF cross-reference fields found ({ref_count}) (0.4 pts)")
            total_score += 0.4
        elif ref_count >= 10:
            partial = 0.4 * (ref_count / 12.0)
            if partial > 0:
                print(f"PARTIAL: Component 1 — {ref_count}/12 REF fields found ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {ref_count} REF fields found, expected >= 10")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct bookmark targets referenced (0.3 points)
    # Each REF field should point to one of the expected section bookmarks.
    try:
        found_targets = set()
        for it in instr_texts:
            if it.text and 'REF' in it.text:
                # Parse bookmark name from instrText like " REF _Section_1_1 \h "
                match = re.search(r'REF\s+(_Section_\d+_\d+)\s', it.text)
                if match:
                    found_targets.add(match.group(1))

        matched = found_targets & EXPECTED_REF_TARGETS
        match_count = len(matched)
        expected_count = len(EXPECTED_REF_TARGETS)

        print(f"INFO: Matched {match_count}/{expected_count} expected bookmark targets")
        if match_count > 0:
            for t in sorted(matched):
                print(f"  Matched: {t}")

        if match_count >= expected_count:
            print(f"PASS: Component 2 — All {expected_count} expected targets referenced (0.3 pts)")
            total_score += 0.3
        elif match_count >= 8:
            partial = 0.3 * (match_count / expected_count)
            if partial > 0:
                print(f"PARTIAL: Component 2 — {match_count}/{expected_count} targets matched ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {match_count}/{expected_count} expected targets matched")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Field structure integrity (0.3 points)
    # Each cross-reference field should have a proper triplet: fldChar(begin), instrText, fldChar(end).
    # 12 REF fields should produce 36 fldChar elements (12 begin + 12 separate + 12 end).
    try:
        fld_chars = doc.element.findall('.//w:fldChar', ns)
        fld_count = len(fld_chars)

        # Count begin/separate/end
        begin_count = 0
        separate_count = 0
        end_count = 0
        for fc in fld_chars:
            fld_type = fc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fldCharType', '')
            if fld_type == 'begin':
                begin_count += 1
            elif fld_type == 'separate':
                separate_count += 1
            elif fld_type == 'end':
                end_count += 1

        print(f"INFO: fldChar elements: {fld_count} total (begin={begin_count}, separate={separate_count}, end={end_count})")

        # We expect at least 12 begin and 12 end for the 12 cross-references
        if begin_count >= 12 and end_count >= 12:
            print(f"PASS: Component 3 — Field structure intact: {begin_count} begin, {end_count} end (0.3 pts)")
            total_score += 0.3
        elif begin_count >= 8 and end_count >= 8:
            partial = 0.3 * min(begin_count, end_count) / 12.0
            if partial > 0:
                print(f"PARTIAL: Component 3 — {begin_count} begin, {end_count} end ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 3 — Insufficient field structure: {begin_count} begin, {end_count} end")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
