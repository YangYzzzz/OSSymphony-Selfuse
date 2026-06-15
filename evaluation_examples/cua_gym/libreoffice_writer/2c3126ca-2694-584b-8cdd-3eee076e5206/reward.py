"""
Reward Script: Insert a cross-reference to 'Figure 5: Network Architecture Diagram'
Task ID: writer_tm_087
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4) - REF field instruction referencing _Ref_Fig5 exists in paragraph 10
  Component 2 (0.3) - Field display text contains 'Figure 5'
  Component 3 (0.3) - Field has \h hyperlink switch and proper begin/separate/end structure
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_087'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a cross-reference field to Figure 5 has been inserted
    in the document at the expected location (paragraph 10).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Find the paragraph that originally contained "The network layout is illustrated in"
    # This is paragraph index 10 in both initial and golden, but we search by text to be robust
    target_para = None
    target_idx = None
    for i, p in enumerate(doc.paragraphs):
        if 'network layout is illustrated in' in p.text.lower():
            target_para = p
            target_idx = i
            break

    if target_para is None:
        print("FAIL: Could not find the target paragraph containing 'network layout is illustrated in'")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found target paragraph at index {target_idx}: {target_para.text[:80]!r}")

    # Collect all instrText elements in this paragraph
    instr_texts = target_para._element.findall('.//w:instrText', ns)
    instr_combined = ' '.join((it.text or '') for it in instr_texts).strip()
    print(f"INFO: instrText in target paragraph: {instr_combined!r}")

    # Also check fldChar elements
    fld_chars = target_para._element.findall('.//w:fldChar', ns)
    fld_types = [fc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fldCharType') for fc in fld_chars]
    print(f"INFO: fldChar types in target paragraph: {fld_types}")

    # Component 1: REF field instruction referencing _Ref_Fig5 (0.4 points)
    # This FAILS on initial (no instrText) and PASSES on golden
    try:
        ref_in_instr = instr_combined and 'REF' in instr_combined.upper()
        fig5_in_instr = '_Ref_Fig5' in instr_combined or 'Fig5' in instr_combined or 'Figure_5' in instr_combined
        if ref_in_instr and fig5_in_instr:
            print(f"PASS: Component 1 - REF field referencing Fig5 found: {instr_combined!r} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - No REF field referencing Fig5 in target paragraph")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Field display text contains 'Figure 5' (0.3 points)
    # In the initial, paragraph text is just "The network layout is illustrated in "
    # In the golden, it includes "Figure 5: Network Architecture Diagram"
    try:
        # The cross-reference display text appears in the paragraph text
        para_text = target_para.text
        has_figure5_text = 'Figure 5' in para_text

        if has_figure5_text:
            print(f"PASS: Component 2 - 'Figure 5' text found in paragraph: {para_text[:100]!r} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - 'Figure 5' not in paragraph text: {para_text[:100]!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Proper field structure with \h hyperlink switch (0.3 points)
    # The field must have begin/separate/end fldChar elements AND \h in instrText
    try:
        proper_structure = ('begin' in fld_types and 'separate' in fld_types and 'end' in fld_types)
        hyperlink_switch = (len(instr_combined) > 0 and '\\h' in instr_combined)

        if proper_structure and hyperlink_switch:
            print(f"PASS: Component 3 - Proper field structure with \\h switch (0.3 pts)")
            total_score += 0.3
        elif proper_structure:
            # Partial credit: field structure present but missing \h switch
            print(f"PARTIAL: Component 3 - Field structure present but missing \\h switch (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - No proper field structure. fldChar types={fld_types}, instrText={instr_combined!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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
