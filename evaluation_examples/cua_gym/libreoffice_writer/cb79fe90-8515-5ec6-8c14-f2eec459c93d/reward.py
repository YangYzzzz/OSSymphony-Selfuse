"""
Reward Script: Set paragraph spacing for company policy document
Task ID: wrpara_021
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Title paragraph has 24pt space_after
  Component 2 (0.4): All 3 section headings have 12pt before, 6pt after
  Component 3 (0.3): All 6 body paragraphs have 0pt before, 6pt after
"""

import os

from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'wrpara_021'

# Tolerance for point comparisons (allow +/- 0.5pt)
PT_TOL = 0.5


def approx_pt(value, expected_pt):
    """Check if a spacing value is approximately equal to expected_pt."""
    if value is None:
        return expected_pt == 0  # None means inherit; only matches 0 if that's expected
    try:
        return abs(value.pt - expected_pt) <= PT_TOL
    except Exception:
        return False


def space_is_zero_or_none(value):
    """Check if spacing is 0 (either explicit 0 or None/inherit)."""
    if value is None:
        return True
    try:
        return abs(value.pt) <= PT_TOL
    except Exception:
        return False


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice before verifying."""
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
    Verify paragraph spacing task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    if len(paragraphs) < 10:
        print(f"FAIL: Expected at least 10 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Identify paragraphs by style
    title_paras = [p for p in paragraphs if p.style and p.style.name == 'Heading 1']
    heading_paras = [p for p in paragraphs if p.style and p.style.name == 'Heading 2']
    body_paras = [p for p in paragraphs if p.style and p.style.name == 'Normal']

    # Precondition: document structure is intact
    if len(title_paras) != 1 or len(heading_paras) != 3 or len(body_paras) != 6:
        print(f"WARN: Unexpected structure: {len(title_paras)} titles, {len(heading_paras)} headings, {len(body_paras)} body")

    # Component 1: Title paragraph has 24pt space_after (0.3 points)
    # Initial state: space_after is None (inherit). Golden: 24pt.
    # This check FAILS on initial (None != 24pt) and PASSES on golden.
    try:
        title = title_paras[0] if title_paras else None
        if title is None:
            print("FAIL: Component 1 -- No Heading 1 paragraph found")
        else:
            pf = title.paragraph_format
            sa = pf.space_after
            if sa is not None and approx_pt(sa, 24.0):
                print(f"PASS: Component 1 -- Title space_after={sa.pt:.1f}pt (expected ~24pt) (0.3 pts)")
                total_score += 0.3
            else:
                sa_val = sa.pt if sa is not None else 'None/inherit'
                print(f"FAIL: Component 1 -- Title space_after={sa_val}, expected ~24pt")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Section headings have 12pt before and 6pt after (0.4 points)
    # Initial state: both are None (inherit). Golden: before=12, after=6.
    # Split: 0.2 for space_before=12pt on all 3, 0.2 for space_after=6pt on all 3.
    try:
        if len(heading_paras) < 3:
            print(f"FAIL: Component 2 -- Only {len(heading_paras)} Heading 2 paragraphs found")
        else:
            before_ok_count = 0
            after_ok_count = 0
            for hp in heading_paras:
                pf = hp.paragraph_format
                sb = pf.space_before
                sa = pf.space_after
                # space_before must be explicitly ~12pt (not None)
                if sb is not None and approx_pt(sb, 12.0):
                    before_ok_count += 1
                # space_after must be explicitly ~6pt (not None)
                if sa is not None and approx_pt(sa, 6.0):
                    after_ok_count += 1

            # Sub-component 2a: space_before=12pt on all 3 headings (0.2 pts)
            if before_ok_count == 3:
                print(f"PASS: Component 2a -- All 3 headings have space_before ~12pt (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2a -- {before_ok_count}/3 headings have space_before ~12pt")

            # Sub-component 2b: space_after=6pt on all 3 headings (0.2 pts)
            if after_ok_count == 3:
                print(f"PASS: Component 2b -- All 3 headings have space_after ~6pt (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2b -- {after_ok_count}/3 headings have space_after ~6pt")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Body paragraphs have 0pt before and 6pt after (0.3 points)
    # Initial state: space_after is None (inherit). Golden: after=6pt, before=0pt.
    # The key discriminator is space_after changing from None to 6pt.
    # space_before=0 is also explicitly set in golden but is effectively 0 in initial too (inherit).
    # So we check: space_after must be explicitly ~6pt (not None). This fails on initial.
    try:
        if len(body_paras) < 6:
            print(f"FAIL: Component 3 -- Only {len(body_paras)} Normal paragraphs found")
        else:
            after_ok_count = 0
            before_ok_count = 0
            for bp in body_paras:
                pf = bp.paragraph_format
                sa = pf.space_after
                sb = pf.space_before
                # space_after must be explicitly ~6pt (not None/inherit)
                if sa is not None and approx_pt(sa, 6.0):
                    after_ok_count += 1
                # space_before should be 0 or None (both acceptable)
                if space_is_zero_or_none(sb):
                    before_ok_count += 1

            # Sub-component 3a: space_after=6pt on all 6 body paragraphs (0.2 pts)
            if after_ok_count == 6:
                print(f"PASS: Component 3a -- All 6 body paragraphs have space_after ~6pt (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3a -- {after_ok_count}/6 body paragraphs have space_after ~6pt")

            # Sub-component 3b: space_before=0pt on all 6 body paragraphs (0.1 pts)
            # Only award if space_after is also correct (compound check anchored to change)
            if before_ok_count == 6 and after_ok_count == 6:
                print(f"PASS: Component 3b -- All 6 body paragraphs have space_before ~0pt AND space_after set (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3b -- {before_ok_count}/6 body paragraphs have space_before ~0pt (requires 3a to pass too)")
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
