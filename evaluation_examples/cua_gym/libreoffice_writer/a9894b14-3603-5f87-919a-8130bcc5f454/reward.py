"""
Reward Script: Nested conditional mail merge field verification
Task ID: writer_mt_038
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25) - Outer IF field with MERGEFIELD Region = "North"
  Component 2 (0.25) - Inner IF field with MERGEFIELD SalesAmount > 10000
  Component 3 (0.20) - Inner IF results: "Top Performer - North" / "North Region"
  Component 4 (0.15) - Outer IF false result: "Other Region"
  Component 5 (0.15) - Proper nesting (inner IF within outer IF true branch)
"""

import os
import re
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_038'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def extract_field_codes(para_element):
    """
    Extract field code structure from a paragraph element.
    Returns a list of dicts with field info including nesting.

    Field codes in OOXML use fldChar (begin/separate/end) and instrText elements.
    We parse these to reconstruct the nested field structure.
    """
    runs = para_element.findall('.//w:r', NS)

    # Collect all instrText and fldChar elements in order
    tokens = []
    for run in runs:
        fld_char = run.find('w:fldChar', NS)
        instr_text = run.find('w:instrText', NS)
        text_elem = run.find('w:t', NS)

        if fld_char is not None:
            fld_type = fld_char.get(f'{{{WNS}}}fldCharType')
            tokens.append(('fldChar', fld_type))
        if instr_text is not None:
            tokens.append(('instrText', instr_text.text or ''))
        if text_elem is not None and fld_char is None and instr_text is None:
            tokens.append(('text', text_elem.text or ''))

    return tokens


def parse_fields_from_tokens(tokens):
    """
    Parse field tokens into a structured representation.
    Returns list of field dicts with instruction text and nesting depth.
    """
    fields = []
    depth = 0
    current_instr = []
    field_stack = []

    for token_type, token_value in tokens:
        if token_type == 'fldChar':
            if token_value == 'begin':
                depth += 1
                field_stack.append({'depth': depth, 'instr_parts': [], 'result_text': ''})
            elif token_value == 'separate':
                # Switch to result portion
                if field_stack:
                    field_stack[-1]['instr'] = ' '.join(field_stack[-1]['instr_parts'])
            elif token_value == 'end':
                if field_stack:
                    field = field_stack.pop()
                    field['instr'] = ' '.join(field.get('instr_parts', []))
                    fields.append(field)
                depth -= 1
        elif token_type == 'instrText':
            if field_stack:
                field_stack[-1]['instr_parts'].append(token_value.strip())

    return fields


def get_all_instr_texts(para_element):
    """Get all instrText content from a paragraph, concatenated by field."""
    runs = para_element.findall('.//w:r', NS)

    all_instr = []
    current_field_instr = []
    in_field = False
    depth = 0

    for run in runs:
        fld_char = run.find('w:fldChar', NS)
        instr_text = run.find('w:instrText', NS)

        if fld_char is not None:
            fld_type = fld_char.get(f'{{{WNS}}}fldCharType')
            if fld_type == 'begin':
                depth += 1
                if depth == 1:
                    current_field_instr = []
                    in_field = True
            elif fld_type == 'end':
                if depth == 1 and in_field:
                    full_instr = ' '.join(current_field_instr)
                    all_instr.append(full_instr)
                    in_field = False
                depth -= 1

        if instr_text is not None and in_field:
            current_field_instr.append(instr_text.text or '')

    return all_instr


def get_full_field_instruction(para_element):
    """
    Get the FULL concatenated instruction text from all instrText elements
    in the paragraph, preserving order. This captures the entire nested field.
    """
    instr_texts = []
    for run in para_element.findall('.//w:r', NS):
        instr = run.find('w:instrText', NS)
        if instr is not None:
            instr_texts.append(instr.text or '')
    return ''.join(instr_texts)


def count_fld_char_begins(para_element):
    """Count fldChar begin elements in a paragraph."""
    count = 0
    for run in para_element.findall('.//w:r', NS):
        fld_char = run.find('w:fldChar', NS)
        if fld_char is not None:
            if fld_char.get(f'{{{WNS}}}fldCharType') == 'begin':
                count += 1
    return count


def verify_task(file_path):
    """
    Verify nested conditional mail merge fields with progressive scoring.
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

    # Find the paragraph that should contain the conditional fields
    # It should be the "Award Category:" paragraph (para index ~9)
    target_para = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.startswith('Award Category:'):
            target_para = p
            break

    if target_para is None:
        print("FAIL: Could not find 'Award Category:' paragraph")
        print("REWARD: 0.0")
        return 0.0

    para_xml = target_para._element
    full_instr = get_full_field_instruction(para_xml)
    num_field_begins = count_fld_char_begins(para_xml)

    print(f"INFO: Found 'Award Category:' paragraph")
    print(f"INFO: Number of field begins: {num_field_begins}")
    print(f"INFO: Full instruction text: {repr(full_instr)}")

    # Component 1: Outer IF field with MERGEFIELD Region = "North" (0.25 points)
    # The instruction text should contain an IF field checking Region against "North"
    try:
        has_outer_if = False
        has_region_merge = False
        has_north_check = False

        if num_field_begins >= 2:  # At least outer IF + Region MERGEFIELD
            has_outer_if = ' IF ' in full_instr

        if has_outer_if:
            has_region_merge = 'MERGEFIELD Region' in full_instr

        if has_region_merge:
            # Check for Region = "North" or Region EQ "North" pattern
            north_pattern = re.search(r'Region\s.*?=\s*"North"', full_instr, re.IGNORECASE)
            if north_pattern:
                has_north_check = True

        if has_outer_if and has_region_merge and has_north_check:
            print(f"PASS: Component 1 - Outer IF with MERGEFIELD Region = 'North' found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - Missing outer IF/Region check. "
                  f"outer_if={has_outer_if}, region_merge={has_region_merge}, north_check={has_north_check}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Inner IF field with MERGEFIELD SalesAmount > 10000 (0.25 points)
    try:
        has_sales_merge = 'MERGEFIELD SalesAmount' in full_instr
        has_inner_if = False
        has_gt_10000 = False

        if has_sales_merge:
            # There should be multiple IF instructions (outer + inner)
            if_count = full_instr.count(' IF ')
            has_inner_if = if_count >= 2

        if has_inner_if:
            # Check for SalesAmount > 10000 or SalesAmount GT 10000
            gt_pattern = re.search(r'SalesAmount\s.*?>\s*"?10000"?', full_instr)
            if gt_pattern is None:
                gt_pattern = re.search(r'SalesAmount\s.*?GT\s*"?10000"?', full_instr, re.IGNORECASE)
            if gt_pattern:
                has_gt_10000 = True

        if has_sales_merge and has_inner_if and has_gt_10000:
            print(f"PASS: Component 2 - Inner IF with MERGEFIELD SalesAmount > 10000 found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Missing inner IF/SalesAmount check. "
                  f"sales_merge={has_sales_merge}, inner_if={has_inner_if}, gt_10000={has_gt_10000}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Inner IF results - "Top Performer - North" / "North Region" (0.20 points)
    try:
        has_top_performer = 'Top Performer - North' in full_instr or 'Top Performer - North' in target_para.text
        has_north_region = 'North Region' in full_instr or 'North Region' in target_para.text

        # Verify these are in the correct context (inner IF true/false branches)
        # The instruction should have pattern like: "Top Performer - North" "North Region"
        inner_results_ok = False
        if has_top_performer and has_north_region:
            # Check ordering: Top Performer should be true branch (before North Region in inner IF)
            tp_pos = full_instr.find('Top Performer - North')
            nr_pos = full_instr.find('North Region')
            if tp_pos >= 0 and nr_pos >= 0 and tp_pos < nr_pos:
                inner_results_ok = True

        if inner_results_ok:
            print(f"PASS: Component 3 - Inner IF results 'Top Performer - North' / 'North Region' correct (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - Missing or incorrect inner IF results. "
                  f"top_performer={has_top_performer}, north_region={has_north_region}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Outer IF false result - "Other Region" (0.15 points)
    try:
        has_other_region = 'Other Region' in full_instr or 'Other Region' in target_para.text

        # Verify "Other Region" appears after the inner IF block (in outer false branch)
        other_in_correct_position = False
        if has_other_region:
            or_pos = full_instr.find('Other Region')
            # "Other Region" should appear after "North Region" (it's the outer false branch)
            nr_pos = full_instr.find('North Region')
            if or_pos >= 0 and (nr_pos < 0 or or_pos > nr_pos):
                other_in_correct_position = True

        if has_other_region and other_in_correct_position:
            print(f"PASS: Component 4 - Outer IF false result 'Other Region' found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Missing 'Other Region' in outer IF false branch. "
                  f"has_other_region={has_other_region}, correct_position={other_in_correct_position}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Proper nesting - inner IF within outer IF (0.15 points)
    # This checks structural nesting: at least 4 field begins (outer IF, Region MERGEFIELD,
    # inner IF, SalesAmount MERGEFIELD)
    try:
        nesting_ok = False

        # We need at least 4 fldChar begins for proper nesting:
        # 1. Outer IF begin
        # 2. Region MERGEFIELD begin
        # 3. Inner IF begin
        # 4. SalesAmount MERGEFIELD begin
        if num_field_begins >= 4:
            # Verify the structure: tokens should show nested begin/end pairs
            tokens = extract_field_codes(para_xml)

            # Walk through tokens to verify nesting structure
            depth_at_inner_if = -1
            found_nested_structure = False
            depth = 0
            saw_outer_if = False
            saw_inner_if = False

            for ttype, tval in tokens:
                if ttype == 'fldChar':
                    if tval == 'begin':
                        depth += 1
                    elif tval == 'end':
                        depth -= 1
                elif ttype == 'instrText':
                    if 'IF' in tval and not saw_outer_if:
                        saw_outer_if = True
                    elif 'IF' in tval and saw_outer_if:
                        saw_inner_if = True
                        if depth >= 2:  # Inner IF is at depth >= 2, meaning it's nested
                            found_nested_structure = True

            nesting_ok = found_nested_structure

        if nesting_ok:
            print(f"PASS: Component 5 - Proper nesting verified ({num_field_begins} field begins, inner IF at depth >= 2) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - Nesting not proper. field_begins={num_field_begins}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
