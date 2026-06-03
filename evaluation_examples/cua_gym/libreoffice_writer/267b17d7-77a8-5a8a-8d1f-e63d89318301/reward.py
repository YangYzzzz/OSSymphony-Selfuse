"""
Reward Script: Insert citations and generate bibliography in Literature_Review.docx
Task ID: writer_pd_017
Domain: libreoffice_writer
Scoring:
  Component 1: Smith (2024) citation in body text (0.15 pts)
  Component 2: Johnson & Lee (2023) citation in body text (0.15 pts)
  Component 3: Williams et al. (2025) citation in body text (0.15 pts)
  Component 4: Bibliography entry for Smith (2024) under References (0.15 pts)
  Component 5: Bibliography entry for Johnson & Lee (2023) under References (0.15 pts)
  Component 6: Bibliography entry for Williams et al. (2025) under References (0.15 pts)
  Component 7: All 3 bibliography entries present in References section (0.10 pts)
  Total: 1.0
"""

import os
import time


WORKDIR = '/home/user'
TASK_ID = 'writer_pd_017'


def persist_app_state(domain: str):
    """Attempt to save any unsaved GUI edits via Ctrl+S."""
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
    Verify task completion with progressive scoring.
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

    paragraphs = doc.paragraphs

    # -------------------------------------------------------------------------
    # Find the "References" heading index — bibliography entries must come after
    # -------------------------------------------------------------------------
    references_idx = None
    for i, p in enumerate(paragraphs):
        if p.text.strip().lower() == 'references' and 'Heading' in (p.style.name or ''):
            references_idx = i
            break

    if references_idx is None:
        # Fallback: search for any paragraph whose text is "References"
        for i, p in enumerate(paragraphs):
            if p.text.strip() == 'References':
                references_idx = i
                break

    # Collect body text (before References) and bibliography text (after References)
    body_texts = []
    bib_texts = []
    if references_idx is not None:
        body_texts = [p.text for p in paragraphs[:references_idx]]
        bib_texts = [p.text.strip() for p in paragraphs[references_idx + 1:] if p.text.strip()]
    else:
        # No References heading found — treat all as body
        body_texts = [p.text for p in paragraphs]

    body_full = '\n'.join(body_texts)
    bib_full = '\n'.join(bib_texts)

    # -------------------------------------------------------------------------
    # Component 1: Smith (2024) citation in body text (0.15 pts)
    # The citation "(Smith, 2024)" should appear in the body paragraphs.
    # -------------------------------------------------------------------------
    try:
        has_smith_cite = ('Smith' in body_full and '2024' in body_full
                          and ('(Smith, 2024)' in body_full or '(Smith 2024)' in body_full
                               or 'Smith, 2024' in body_full or 'Smith (2024)' in body_full))
        if has_smith_cite:
            print("PASS: Component 1 — Smith (2024) citation found in body text (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 — Smith (2024) citation not found in body text")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Johnson & Lee (2023) citation in body text (0.15 pts)
    # -------------------------------------------------------------------------
    try:
        has_johnson_cite = ('Johnson' in body_full and 'Lee' in body_full and '2023' in body_full
                            and ('Johnson & Lee, 2023' in body_full
                                 or 'Johnson and Lee, 2023' in body_full
                                 or 'Johnson & Lee (2023)' in body_full
                                 or 'Johnson and Lee (2023)' in body_full
                                 or '(Johnson & Lee, 2023)' in body_full
                                 or '(Johnson and Lee, 2023)' in body_full))
        if has_johnson_cite:
            print("PASS: Component 2 — Johnson & Lee (2023) citation found in body text (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 — Johnson & Lee (2023) citation not found in body text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Williams et al. (2025) citation in body text (0.15 pts)
    # -------------------------------------------------------------------------
    try:
        has_williams_cite = ('Williams' in body_full and '2025' in body_full
                             and ('Williams et al., 2025' in body_full
                                  or 'Williams et al. (2025)' in body_full
                                  or '(Williams et al., 2025)' in body_full
                                  or '(Williams et al. 2025)' in body_full))
        if has_williams_cite:
            print("PASS: Component 3 — Williams et al. (2025) citation found in body text (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 3 — Williams et al. (2025) citation not found in body text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Bibliography entry for Smith (2024) under References (0.15 pts)
    # Must contain author name, year, and be in the references section.
    # -------------------------------------------------------------------------
    try:
        smith_bib_found = any('Smith' in b and '2024' in b for b in bib_texts)
        if smith_bib_found:
            print("PASS: Component 4 — Bibliography entry for Smith (2024) found in References (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — No bibliography entry for Smith (2024) in References section. Bib entries found: {len(bib_texts)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------------
    # Component 5: Bibliography entry for Johnson & Lee (2023) under References (0.15 pts)
    # -------------------------------------------------------------------------
    try:
        johnson_bib_found = any('Johnson' in b and '2023' in b for b in bib_texts)
        if johnson_bib_found:
            print("PASS: Component 5 — Bibliography entry for Johnson & Lee (2023) found in References (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — No bibliography entry for Johnson & Lee (2023) in References section. Bib entries found: {len(bib_texts)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -------------------------------------------------------------------------
    # Component 6: Bibliography entry for Williams et al. (2025) under References (0.15 pts)
    # -------------------------------------------------------------------------
    try:
        williams_bib_found = any('Williams' in b and '2025' in b for b in bib_texts)
        if williams_bib_found:
            print("PASS: Component 6 — Bibliography entry for Williams et al. (2025) found in References (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — No bibliography entry for Williams et al. (2025) in References section. Bib entries found: {len(bib_texts)}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # -------------------------------------------------------------------------
    # Component 7: All 3 bibliography entries present (completeness bonus) (0.10 pts)
    # This checks that all three are present together — not just individually.
    # -------------------------------------------------------------------------
    try:
        all_three = (
            any('Smith' in b and '2024' in b for b in bib_texts)
            and any('Johnson' in b and '2023' in b for b in bib_texts)
            and any('Williams' in b and '2025' in b for b in bib_texts)
        )
        if all_three and len(bib_texts) >= 3:
            print("PASS: Component 7 — All 3 bibliography entries present in References section (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — Not all 3 bibliography entries present. Found {len(bib_texts)} entries.")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
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
