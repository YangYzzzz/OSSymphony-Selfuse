"""
Reward Script: Conditional merge field for membership status
Task ID: writer_mt_027
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Field code structure exists in the Status paragraph
  Component 2 (0.4): IF condition references MembershipExpiry and date 2025-06-30
  Component 3 (0.3): True value is "Renewal Required", false value is "Active Member"
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_027'


def persist_app_state(domain):
    """Best-effort save of any unsaved GUI state."""
    import time
    os.environ["DISPLAY"] = ":0"
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
        from docx.oxml.ns import qn
    except ImportError as e:
        print(f"CRITICAL: Cannot import python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the paragraph that starts with "Status:" — expected around P10
    status_para = None
    for para in doc.paragraphs:
        if para.text.strip().startswith("Status:"):
            status_para = para
            break

    if status_para is None:
        print("CRITICAL: No paragraph starting with 'Status:' found")
        print("REWARD: 0.0")
        return 0.0

    # Extract field information from the Status paragraph's XML
    para_elem = status_para._element
    fld_chars = para_elem.findall('.//' + qn('w:fldChar'))
    instr_texts = para_elem.findall('.//' + qn('w:instrText'))

    # Collect all instrText content
    full_instr = ''
    for it in instr_texts:
        if it.text:
            full_instr += it.text

    print(f"DEBUG: Status para text = {repr(status_para.text)}")
    print(f"DEBUG: fldChar count = {len(fld_chars)}")
    print(f"DEBUG: instrText content = {repr(full_instr)}")

    # Component 1: Field code structure exists (0.3 points)
    # The paragraph must contain fldChar begin/separate/end structure
    try:
        fld_types = [fc.get(qn('w:fldCharType')) for fc in fld_chars]
        has_begin = 'begin' in fld_types
        has_separate = 'separate' in fld_types
        has_end = 'end' in fld_types
        if has_begin and has_separate and has_end:
            print(f"PASS: Component 1 — Field code structure found (begin/separate/end) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Missing field structure. Found types: {fld_types}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: IF condition with MembershipExpiry and date (0.4 points)
    # The instrText must contain an IF condition referencing MembershipExpiry
    # and the date threshold 2025-06-30 (or equivalent date representations)
    try:
        instr_normalized = full_instr.strip().upper()
        has_if = instr_normalized.startswith('IF') or ' IF ' in instr_normalized
        has_membership_expiry = 'MEMBERSHIPEXPIRY' in instr_normalized
        # Accept various date formats: 2025-06-30, 2025/06/30, 06/30/2025, June 30
        has_date = bool(
            re.search(r'2025[-/]06[-/]30', full_instr) or
            re.search(r'06[-/]30[-/]2025', full_instr) or
            re.search(r'30[-/]06[-/]2025', full_instr) or
            re.search(r'JUNE\s*30', instr_normalized)
        )

        if has_if and has_membership_expiry and has_date:
            print(f"PASS: Component 2 — IF condition with MembershipExpiry and 2025-06-30 found (0.4 pts)")
            total_score += 0.4
        else:
            details = []
            if not has_if:
                details.append("no IF keyword")
            if not has_membership_expiry:
                details.append("no MembershipExpiry reference")
            if not has_date:
                details.append("no 2025-06-30 date threshold")
            print(f"FAIL: Component 2 — Missing: {', '.join(details)}. instrText={repr(full_instr)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct true/false values (0.3 points)
    # True value should be "Renewal Required", false value should be "Active Member"
    try:
        has_renewal = 'Renewal Required' in full_instr
        has_active = 'Active Member' in full_instr

        if has_renewal and has_active:
            print(f"PASS: Component 3 — Both 'Renewal Required' and 'Active Member' present in field (0.3 pts)")
            total_score += 0.3
        else:
            details = []
            if not has_renewal:
                details.append("missing 'Renewal Required'")
            if not has_active:
                details.append("missing 'Active Member'")
            print(f"FAIL: Component 3 — {', '.join(details)} in instrText={repr(full_instr)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
