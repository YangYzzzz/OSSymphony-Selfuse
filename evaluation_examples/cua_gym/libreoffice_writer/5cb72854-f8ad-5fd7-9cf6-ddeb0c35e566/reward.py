"""
Reward Script: Format WHEREAS clauses with small caps and bold
Task ID: writer_legal_070
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): All 6 WHEREAS runs are bold
  Component 2 (0.3): All 6 WHEREAS runs have small caps
  Component 3 (0.2): Remaining clause text retains regular weight (not bold)
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_070'
NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def find_whereas_paragraphs(doc):
    """Find all paragraphs that start with WHEREAS."""
    results = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text.upper().startswith('WHEREAS'):
            results.append(para)
    return results


def check_run_small_caps(run):
    """Check if a run has smallCaps formatting via XML."""
    rpr = run._element.find(f'{{{NS}}}rPr')
    if rpr is None:
        return False
    sm = rpr.find(f'{{{NS}}}smallCaps')
    if sm is None:
        return False
    # If element exists with no val attribute, it means true
    val = sm.get(f'{{{NS}}}val')
    if val is None:
        return True
    # val can be "1", "true", "on" for true; "0", "false", "off" for false
    return val.lower() in ('1', 'true', 'on')


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

    # Find WHEREAS paragraphs
    whereas_paras = find_whereas_paragraphs(doc)
    num_found = len(whereas_paras)
    print(f"Found {num_found} WHEREAS paragraphs")

    if num_found != 6:
        print(f"FAIL: Expected 6 WHEREAS paragraphs, found {num_found}")
        # If zero found, nothing to score
        if num_found == 0:
            print("REWARD: 0.0")
            return 0.0

    # Component 1: All WHEREAS runs are bold (0.5 points)
    # Each clause contributes 0.5/6 points
    try:
        bold_count = 0
        for i, para in enumerate(whereas_paras):
            # The first run should be the WHEREAS word
            if len(para.runs) == 0:
                print(f"  Clause {i+1}: no runs found")
                continue
            first_run = para.runs[0]
            first_text = first_run.text.strip().upper()
            if 'WHEREAS' in first_text and first_run.bold is True:
                bold_count += 1
                print(f"  Clause {i+1}: WHEREAS run is bold - PASS")
            else:
                print(f"  Clause {i+1}: WHEREAS run bold={first_run.bold}, text={repr(first_run.text[:20])} - FAIL")

        if bold_count > 0:
            component1 = 0.5 * (bold_count / len(whereas_paras))
            total_score += component1
            print(f"PASS: Component 1 - WHEREAS bold: {bold_count}/{len(whereas_paras)} ({component1:.3f} pts)")
        else:
            print(f"FAIL: Component 1 - No WHEREAS runs are bold")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All WHEREAS runs have small caps (0.3 points)
    # Each clause contributes 0.3/6 points
    try:
        smallcaps_count = 0
        for i, para in enumerate(whereas_paras):
            if len(para.runs) == 0:
                continue
            first_run = para.runs[0]
            first_text = first_run.text.strip().upper()
            if 'WHEREAS' in first_text and check_run_small_caps(first_run):
                smallcaps_count += 1
                print(f"  Clause {i+1}: WHEREAS run has small caps - PASS")
            else:
                print(f"  Clause {i+1}: WHEREAS run smallCaps={check_run_small_caps(first_run)} - FAIL")

        if smallcaps_count > 0:
            component2 = 0.3 * (smallcaps_count / len(whereas_paras))
            total_score += component2
            print(f"PASS: Component 2 - WHEREAS small caps: {smallcaps_count}/{len(whereas_paras)} ({component2:.3f} pts)")
        else:
            print(f"FAIL: Component 2 - No WHEREAS runs have small caps")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: WHEREAS is bold+smallcaps AND remaining text is regular weight (0.2 points)
    # Compound check: anchored to the task change (WHEREAS must be formatted correctly)
    # AND the rest of the clause retains regular formatting (not accidentally bolded)
    try:
        compound_count = 0
        for i, para in enumerate(whereas_paras):
            if len(para.runs) < 2:
                continue
            first_run = para.runs[0]
            first_text = first_run.text.strip().upper()
            # Gate: WHEREAS must be bold AND small caps (the task change)
            whereas_formatted = ('WHEREAS' in first_text
                                 and first_run.bold is True
                                 and check_run_small_caps(first_run))
            if not whereas_formatted:
                print(f"  Clause {i+1}: WHEREAS not fully formatted, compound check FAIL")
                continue
            # Check all runs after the first (WHEREAS) run are NOT bold
            all_regular = True
            for run in para.runs[1:]:
                if run.text.strip() == '':
                    continue
                if run.bold is True:
                    all_regular = False
                    print(f"  Clause {i+1}: non-WHEREAS run is bold: {repr(run.text[:30])} - FAIL")
                    break
            if all_regular:
                compound_count += 1

        if compound_count > 0:
            component3 = 0.2 * (compound_count / len(whereas_paras))
            total_score += component3
            print(f"PASS: Component 3 - Compound (formatted WHEREAS + regular rest): {compound_count}/{len(whereas_paras)} ({component3:.3f} pts)")
        else:
            print(f"FAIL: Component 3 - Compound check failed (WHEREAS not formatted or rest text is bold)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state('libreoffice_writer')

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
