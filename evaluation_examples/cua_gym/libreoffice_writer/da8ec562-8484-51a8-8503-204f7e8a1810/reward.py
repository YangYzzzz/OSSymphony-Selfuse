"""
Reward Script: Compare thesis draft with advisor's edited version — accept formatting, reject content changes
Task ID: writer_lec_067
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30) — Formatting accepted: font changed from Times New Roman to Calibri
  Component 2 (0.20) — Formatting accepted: font sizes updated (title 28pt, heading 18pt, body 11pt)
  Component 3 (0.15) — Formatting accepted: line spacing changed from 1.5 to 2.0 for body paragraphs
  Component 4 (0.35) — Content changes rejected: original draft text retained for P[4], P[6], P[9], P[13]
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_067'

# Original draft text for paragraphs where advisor made content changes.
# The golden file should retain the ORIGINAL draft text (content changes rejected).
DRAFT_P4_START = "Climate modeling has undergone significant transformations over the past two decades."
DRAFT_P6_ENDING = "an analysis of model interpretability in the context of climate science."
# P[6] in advisor version had extra sentence about open-source — must NOT appear in golden
ADVISOR_P6_ADDITION = "Additionally, we provide open-source implementations"
DRAFT_P9_START = "The intersection of physics-based and data-driven approaches has been extensively explored by Beucler"
DRAFT_P13_START = "The proposed ClimateTransformer architecture employs a modified vision transformer"


def persist_app_state(domain):
    """Try to save any unsaved changes in LibreOffice Writer."""
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
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs
    if len(paras) < 17:
        print(f"CRITICAL: Expected 17 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Font family changed to Calibri (0.30 points)
    # In the draft, font is Times New Roman. In golden, it should be Calibri.
    # This is a formatting change from the advisor that should be accepted.
    # -------------------------------------------------------------------------
    try:
        calibri_count = 0
        total_runs_checked = 0
        for para in paras:
            for run in para.runs:
                if run.font.name is not None:
                    total_runs_checked += 1
                    if run.font.name == "Calibri":
                        calibri_count += 1

        if total_runs_checked > 0:
            ratio = calibri_count / total_runs_checked
            if ratio >= 0.9:
                print(f"PASS: Component 1 — Font is Calibri ({calibri_count}/{total_runs_checked} runs) (0.30 pts)")
                total_score += 0.30
            elif ratio >= 0.5:
                partial = 0.30 * (ratio - 0.5) / 0.4  # partial credit
                print(f"PARTIAL: Component 1 — {calibri_count}/{total_runs_checked} runs are Calibri ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — Only {calibri_count}/{total_runs_checked} runs are Calibri (expected >=90%)")
        else:
            print("FAIL: Component 1 — No runs with explicit font name found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Font sizes updated (0.20 points)
    # Title: 26pt -> 28pt, Headings: 16pt -> 18pt, Body: 12pt -> 11pt
    # -------------------------------------------------------------------------
    try:
        checks_passed = 0
        checks_total = 3

        # Check title size (P[0])
        title_run = paras[0].runs[0] if paras[0].runs else None
        if title_run and title_run.font.size and abs(title_run.font.size.pt - 28.0) < 0.5:
            checks_passed += 1
            print(f"  PASS: Title font size is {title_run.font.size.pt}pt (expected ~28)")
        else:
            actual = title_run.font.size.pt if title_run and title_run.font.size else None
            print(f"  FAIL: Title font size is {actual}pt (expected ~28)")

        # Check heading size (P[3] — Chapter 1 heading)
        h1_run = paras[3].runs[0] if paras[3].runs else None
        if h1_run and h1_run.font.size and abs(h1_run.font.size.pt - 18.0) < 0.5:
            checks_passed += 1
            print(f"  PASS: Heading font size is {h1_run.font.size.pt}pt (expected ~18)")
        else:
            actual = h1_run.font.size.pt if h1_run and h1_run.font.size else None
            print(f"  FAIL: Heading font size is {actual}pt (expected ~18)")

        # Check body size (P[4] — first body paragraph)
        body_run = paras[4].runs[0] if paras[4].runs else None
        if body_run and body_run.font.size and abs(body_run.font.size.pt - 11.0) < 0.5:
            checks_passed += 1
            print(f"  PASS: Body font size is {body_run.font.size.pt}pt (expected ~11)")
        else:
            actual = body_run.font.size.pt if body_run and body_run.font.size else None
            print(f"  FAIL: Body font size is {actual}pt (expected ~11)")

        if checks_passed == checks_total:
            print(f"PASS: Component 2 — All font sizes correct (0.20 pts)")
            total_score += 0.20
        elif checks_passed > 0:
            partial = 0.20 * checks_passed / checks_total
            print(f"PARTIAL: Component 2 — {checks_passed}/{checks_total} size checks passed ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No font size checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Line spacing changed to 2.0 for body paragraphs (0.15 points)
    # Draft has 1.5 spacing on body paragraphs; advisor changed to 2.0
    # -------------------------------------------------------------------------
    try:
        body_para_indices = [4, 5, 6, 8, 9, 10, 12, 13, 15, 16]
        spacing_correct = 0
        for idx in body_para_indices:
            sp = paras[idx].paragraph_format.line_spacing
            if sp is not None and abs(float(sp) - 2.0) < 0.1:
                spacing_correct += 1

        if spacing_correct >= len(body_para_indices) - 1:
            print(f"PASS: Component 3 — Line spacing is 2.0 for {spacing_correct}/{len(body_para_indices)} body paragraphs (0.15 pts)")
            total_score += 0.15
        elif spacing_correct >= len(body_para_indices) // 2:
            partial = 0.15 * spacing_correct / len(body_para_indices)
            print(f"PARTIAL: Component 3 — Line spacing correct for {spacing_correct}/{len(body_para_indices)} body paragraphs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Line spacing correct for only {spacing_correct}/{len(body_para_indices)} body paragraphs (expected 2.0)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Content changes rejected — original text retained (0.35 points)
    # Advisor changed text in P[4], P[6], P[9], P[13]. Golden should have ORIGINAL draft text.
    # -------------------------------------------------------------------------
    try:
        content_checks_passed = 0
        content_checks_total = 4

        # P[4]: Should start with original draft text, NOT advisor's rewrite
        p4_text = paras[4].text
        if p4_text.startswith(DRAFT_P4_START):
            content_checks_passed += 1
            print(f"  PASS: P[4] retains original draft text")
        else:
            print(f"  FAIL: P[4] does not start with original draft text. Starts with: '{p4_text[:80]}...'")

        # P[6]: Should NOT contain the advisor's added sentence about open-source
        p6_text = paras[6].text
        if ADVISOR_P6_ADDITION not in p6_text and p6_text.rstrip().endswith(DRAFT_P6_ENDING.rstrip('.')):
            content_checks_passed += 1
            print(f"  PASS: P[6] retains original text (no advisor addition)")
        elif ADVISOR_P6_ADDITION not in p6_text:
            content_checks_passed += 1
            print(f"  PASS: P[6] does not contain advisor's added sentence")
        else:
            print(f"  FAIL: P[6] contains advisor's content change")

        # P[9]: Should start with original draft text about Beucler, NOT advisor's rewrite about foundation models
        p9_text = paras[9].text
        if p9_text.startswith(DRAFT_P9_START):
            content_checks_passed += 1
            print(f"  PASS: P[9] retains original draft text")
        else:
            print(f"  FAIL: P[9] does not start with original draft text. Starts with: '{p9_text[:80]}...'")

        # P[13]: Should start with original draft text about "proposed ClimateTransformer"
        p13_text = paras[13].text
        if p13_text.startswith(DRAFT_P13_START):
            content_checks_passed += 1
            print(f"  PASS: P[13] retains original draft text")
        else:
            print(f"  FAIL: P[13] does not start with original draft text. Starts with: '{p13_text[:80]}...'")

        if content_checks_passed == content_checks_total:
            print(f"PASS: Component 4 — All content changes correctly rejected (0.35 pts)")
            total_score += 0.35
        elif content_checks_passed > 0:
            partial = 0.35 * content_checks_passed / content_checks_total
            print(f"PARTIAL: Component 4 — {content_checks_passed}/{content_checks_total} content checks passed ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No content checks passed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    # Also check for thesis_draft.docx as fallback (initial env)
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
