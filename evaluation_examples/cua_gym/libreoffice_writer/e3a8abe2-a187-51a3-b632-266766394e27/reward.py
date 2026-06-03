"""
Reward Script: Set line spacing and paragraph spacing for a poem document
Task ID: wrpara_048
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Title paragraph has ~36pt space_after
  Component 2 (0.40): All 4 stanza paragraphs have exactly 14pt line spacing
  Component 3 (0.35): All 4 stanza paragraphs have ~24pt space_after
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'wrpara_048'

# Tolerance for spacing comparisons (in EMU). 1pt = 12700 EMU.
# Allow ~1pt tolerance for rounding differences.
TOLERANCE_EMU = 12700 * 1.5  # 1.5pt tolerance


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    paras = doc.paragraphs
    if len(paras) < 5:
        print(f"CRITICAL: Expected at least 5 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    title_para = paras[0]
    stanza_paras = paras[1:5]

    # Expected values in EMU
    EXPECTED_TITLE_SA = Pt(36)    # 457200 EMU
    EXPECTED_STANZA_LS = Pt(14)   # 177800 EMU
    EXPECTED_STANZA_SA = Pt(24)   # 304800 EMU

    # Component 1: Title paragraph has ~36pt space_after (0.25 points)
    try:
        sa = title_para.paragraph_format.space_after
        if sa is not None and abs(int(sa) - int(EXPECTED_TITLE_SA)) <= TOLERANCE_EMU:
            print(f"PASS: Component 1 - Title space_after = {int(sa)/12700:.1f}pt (expected ~36pt) (0.25 pts)")
            total_score += 0.25
        else:
            sa_val = f"{int(sa)/12700:.1f}pt" if sa is not None else "None"
            print(f"FAIL: Component 1 - Title space_after = {sa_val}, expected ~36pt")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All 4 stanza paragraphs have exactly 14pt line spacing (0.40 points)
    # Each stanza contributes 0.10 points
    try:
        stanza_ls_score = 0.0
        from docx.enum.text import WD_LINE_SPACING
        for i, sp in enumerate(stanza_paras):
            ls = sp.paragraph_format.line_spacing
            ls_rule = sp.paragraph_format.line_spacing_rule
            if ls is not None and abs(int(ls) - int(EXPECTED_STANZA_LS)) <= TOLERANCE_EMU:
                # Also check that it's "Exactly" (not proportional)
                if ls_rule == WD_LINE_SPACING.EXACTLY:
                    print(f"  PASS: Stanza {i+1} line_spacing = {int(ls)/12700:.1f}pt, rule=EXACTLY")
                    stanza_ls_score += 0.10
                else:
                    print(f"  PARTIAL: Stanza {i+1} line_spacing = {int(ls)/12700:.1f}pt but rule={ls_rule} (expected EXACTLY)")
                    stanza_ls_score += 0.05
            else:
                ls_val = f"{int(ls)/12700:.1f}pt" if ls is not None else "None"
                print(f"  FAIL: Stanza {i+1} line_spacing = {ls_val}, expected ~14pt EXACTLY")

        if stanza_ls_score >= 0.39:
            print(f"PASS: Component 2 - All stanzas have correct line spacing ({stanza_ls_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 2 - Stanza line spacing score: {stanza_ls_score:.2f}/0.40")
        if stanza_ls_score > 0:
            total_score += stanza_ls_score
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: All 4 stanza paragraphs have ~24pt space_after (0.35 points)
    # Each stanza contributes 0.0875 points
    try:
        stanza_sa_score = 0.0
        for i, sp in enumerate(stanza_paras):
            sa = sp.paragraph_format.space_after
            if sa is not None and abs(int(sa) - int(EXPECTED_STANZA_SA)) <= TOLERANCE_EMU:
                print(f"  PASS: Stanza {i+1} space_after = {int(sa)/12700:.1f}pt (expected ~24pt)")
                stanza_sa_score += 0.0875
            else:
                sa_val = f"{int(sa)/12700:.1f}pt" if sa is not None else "None"
                print(f"  FAIL: Stanza {i+1} space_after = {sa_val}, expected ~24pt")

        if stanza_sa_score >= 0.34:
            print(f"PASS: Component 3 - All stanzas have correct space_after ({stanza_sa_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 3 - Stanza space_after score: {stanza_sa_score:.2f}/0.35")
        if stanza_sa_score > 0:
            total_score += stanza_sa_score
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
