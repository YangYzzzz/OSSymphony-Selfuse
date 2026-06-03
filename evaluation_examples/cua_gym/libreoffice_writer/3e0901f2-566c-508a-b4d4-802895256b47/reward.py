"""
Reward Script: Apply APA-style hanging indent to References section
Task ID: writer_acad_062
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): At least one ref entry has left_indent ~1.27cm (457200 EMU)
  Component 2 (0.4): At least one ref entry has first_line_indent ~-1.27cm (-457200 EMU)
  Component 3 (0.2): ALL reference entries have both correct indents (completeness)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_062'

# Tolerance: 457200 EMU = 1.27cm. Allow +/- 5% tolerance (about 0.06cm)
TARGET_LEFT = 457200       # 1.27 cm in EMU
TARGET_FIRST = -457200     # -1.27 cm in EMU
TOLERANCE = 22860          # ~5% of 457200


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def find_reference_paragraphs(doc):
    """Find all non-empty paragraphs after the References heading."""
    ref_found = False
    ref_paras = []
    for para in doc.paragraphs:
        text = para.text.strip()
        # Detect the References heading
        if not ref_found:
            if text.lower() == 'references' and para.style.name.startswith('Heading'):
                ref_found = True
            continue
        # After heading, collect non-empty paragraphs
        if text:
            ref_paras.append(para)
    return ref_paras


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find reference entries
    ref_paras = find_reference_paragraphs(doc)
    if not ref_paras:
        print("FAIL: No reference entries found after 'References' heading")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(ref_paras)} reference entries")

    # Component 1: At least one ref entry has correct left_indent ~1.27cm (0.4 points)
    # This checks for the hanging indent's left margin setting
    try:
        left_ok_count = 0
        for para in ref_paras:
            left = para.paragraph_format.left_indent
            if left is not None and abs(left - TARGET_LEFT) <= TOLERANCE:
                left_ok_count += 1

        if left_ok_count > 0:
            print(f"PASS: Component 1 — {left_ok_count}/{len(ref_paras)} entries have left_indent ~1.27cm (0.4 pts)")
            total_score += 0.4
        else:
            # Show sample values for debugging
            sample = ref_paras[0].paragraph_format.left_indent
            print(f"FAIL: Component 1 — No entries have left_indent ~1.27cm. Sample value: {sample}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: At least one ref entry has correct first_line_indent ~-1.27cm (0.4 points)
    # This checks for the negative first-line indent (the "hanging" part)
    try:
        first_ok_count = 0
        for para in ref_paras:
            first = para.paragraph_format.first_line_indent
            if first is not None and abs(first - TARGET_FIRST) <= TOLERANCE:
                first_ok_count += 1

        if first_ok_count > 0:
            print(f"PASS: Component 2 — {first_ok_count}/{len(ref_paras)} entries have first_line_indent ~-1.27cm (0.4 pts)")
            total_score += 0.4
        else:
            sample = ref_paras[0].paragraph_format.first_line_indent
            print(f"FAIL: Component 2 — No entries have first_line_indent ~-1.27cm. Sample value: {sample}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ALL reference entries have both correct indents (0.2 points)
    # Completeness check — all 15 entries must be formatted, not just some
    try:
        all_correct = True
        for idx, para in enumerate(ref_paras):
            left = para.paragraph_format.left_indent
            first = para.paragraph_format.first_line_indent
            left_ok = (left is not None and abs(left - TARGET_LEFT) <= TOLERANCE)
            first_ok = (first is not None and abs(first - TARGET_FIRST) <= TOLERANCE)
            if not (left_ok and first_ok):
                all_correct = False
                print(f"FAIL: Component 3 — Entry {idx+1} missing correct indent (left={left}, first={first})")
                break

        if all_correct:
            print(f"PASS: Component 3 — All {len(ref_paras)} entries have correct hanging indent (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Not all entries have correct hanging indent")
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
