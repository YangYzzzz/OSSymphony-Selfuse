"""
Reward Script: Add disclaimer footer to campaign_materials.docx
Task ID: writer_mktg_051
Domain: libreoffice_writer
Scoring:
  Component 1: Disclaimer text present in footer           — 0.40 pts
  Component 2: Disclaimer is italic and ~7pt font size     — 0.35 pts
  Component 3: Original page number retained in footer     — 0.25 pts
  Total: 1.00
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_mktg_051'
DISCLAIMER_TEXT = (
    'This document contains proprietary information of Apex Dynamics, Inc. '
    'Unauthorized distribution is prohibited.'
)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Checks:
    1. The disclaimer text is present in the footer (must not exist in initial_env).
    2. The disclaimer run is italic and approximately 7pt (88900 EMU).
    3. The original page number field (PAGE) is retained in the footer.
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: single section (1 section document as in initial_env)
    if len(doc.sections) == 0:
        print("CRITICAL: No sections found in document.")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]
    footer = section.footer
    footer_paras = footer.paragraphs

    # ---- Component 1: Disclaimer text present in footer (0.40 points) ----
    # This check FAILS on initial_env (footer only has page number, no disclaimer text).
    # It PASSES on golden_env (footer has a second paragraph with the disclaimer).
    try:
        disclaimer_found = False
        disclaimer_para = None
        for para in footer_paras:
            para_text = para.text.strip()
            if DISCLAIMER_TEXT.lower() in para_text.lower():
                disclaimer_found = True
                disclaimer_para = para
                break

        if disclaimer_found:
            print(f"PASS: Component 1 — Disclaimer text found in footer (0.40 pts)")
            total_score += 0.40
        else:
            # Collect all footer text for diagnostic output
            all_footer_texts = [repr(p.text) for p in footer_paras]
            print(f"FAIL: Component 1 — Disclaimer text not found in footer. "
                  f"Footer paragraphs: {all_footer_texts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: Disclaimer is italic and ~7pt (0.35 points) ----
    # This check FAILS on initial_env (no disclaimer paragraph exists).
    # It PASSES on golden_env (disclaimer run has italic=True and size 88900 EMU = 7pt).
    try:
        if disclaimer_para is not None:
            italic_ok = False
            size_ok = False

            for run in disclaimer_para.runs:
                if not run.text.strip():
                    continue
                # Check italic
                if run.font.italic is True:
                    italic_ok = True
                # Check font size: 7pt = 88900 EMU (1pt = 12700 EMU)
                # Also accept if size is None (inherited) but we require explicit 7pt
                if run.font.size is not None:
                    size_pt = run.font.size / 12700
                    if abs(size_pt - 7.0) < 0.5:  # within 0.5pt tolerance
                        size_ok = True

            if italic_ok and size_ok:
                print(f"PASS: Component 2 — Disclaimer is italic and 7pt (0.35 pts)")
                total_score += 0.35
            elif italic_ok and not size_ok:
                # Partial: italic correct but size wrong — award half credit
                # Report failure since the task explicitly required 7pt
                print(f"FAIL: Component 2 — Disclaimer is italic but font size is not 7pt. "
                      f"Found size_emu={[r.font.size for r in disclaimer_para.runs if r.text.strip()]}")
            elif not italic_ok and size_ok:
                print(f"FAIL: Component 2 — Disclaimer is 7pt but not italic.")
            else:
                print(f"FAIL: Component 2 — Disclaimer not italic and not 7pt.")
        else:
            print(f"FAIL: Component 2 — Skipped (no disclaimer paragraph found).")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: Page number retained in footer (0.25 points) ----
    # The initial_env has a page number (PAGE field code) in the footer.
    # The golden_env retains it while adding the disclaimer.
    # This check FAILS on initial_env because: although initial_env HAS the page number,
    # the combined condition (disclaimer present AND page number present) fails since
    # component 1 already verified disclaimer is absent in initial_env.
    # We verify page number retention only if the disclaimer is present (guard on C1).
    try:
        if disclaimer_found:
            # Check for PAGE field code in any footer paragraph
            page_field_found = False
            for para in footer_paras:
                para_xml = para._element.xml
                if 'instrText' in para_xml and 'PAGE' in para_xml:
                    page_field_found = True
                    break

            if page_field_found:
                print(f"PASS: Component 3 — Page number field retained in footer (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Page number field (PAGE) not found in footer. "
                      f"Footer paragraphs count: {len(footer_paras)}")
        else:
            print(f"FAIL: Component 3 — Skipped (disclaimer not present, page-number check skipped).")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/campaign_materials.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
