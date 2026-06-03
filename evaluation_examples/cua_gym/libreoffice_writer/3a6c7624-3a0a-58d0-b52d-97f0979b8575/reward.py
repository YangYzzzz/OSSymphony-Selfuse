"""
Reward Script: Add 4 bibliography entries and insert 4 in-text citations
Task ID: osworld_writer_bibliography_crossref_010
Domain: libreoffice_writer
Scoring:
  Component 1: 4 new bibliography entries added (Wilson 2019, Zhang 2020, Brown 2021, Taylor 2022) — 0.4 pts (0.1 each)
  Component 2: In-text citations (Wilson 2019), (Zhang 2020), (Brown 2021) inserted after paragraphs 1-3 — 0.3 pts (0.1 each)
  Component 3: (Taylor, 2022) citation present within paragraph 4 (discourse analysis paragraph) — 0.3 pts
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_bibliography_crossref_010'


def persist_app_state():
    """Best-effort save for any open LibreOffice Writer instance."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the linguistics document has been correctly updated with:
    1. Four new bibliography entries (Wilson 2019, Zhang 2020, Brown 2021, Taylor 2022)
    2. Three in-text citation paragraphs: (Wilson, 2019) after para 1, (Zhang, 2020) after para 2,
       (Brown, 2021) after para 3
    3. (Taylor, 2022) embedded within paragraph 4 (discourse analysis paragraph)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
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

    # Collect all paragraph texts for analysis
    all_texts = [p.text for p in doc.paragraphs]
    full_doc_text = '\n'.join(all_texts)

    # ------------------------------------------------------------------
    # Component 1: 4 new bibliography entries added (0.4 pts, 0.1 each)
    # We look for the bibliography section and check for the 4 new entries.
    # Initial doc has 2 entries (Chomsky, Tomasello). Golden should have 4 more.
    # ------------------------------------------------------------------

    # Find the bibliography section
    bib_start = -1
    for i, text in enumerate(all_texts):
        if text.strip() == 'Bibliography' or text.strip() == '2. Bibliography':
            bib_start = i
            break

    if bib_start == -1:
        print("WARN: Could not find 'Bibliography' section heading")
        bib_texts = all_texts  # fallback: search whole doc
    else:
        bib_texts = all_texts[bib_start:]

    bib_section = '\n'.join(bib_texts)

    # Component 1a: Wilson (2019) bibliography entry
    try:
        # Look for: Wilson ... 2019 ... Modern Linguistics ... Springer
        wilson_bib = bool(
            re.search(r'Wilson', bib_section) and
            re.search(r'2019', bib_section) and
            re.search(r'Modern Linguistics', bib_section, re.IGNORECASE) and
            re.search(r'Springer', bib_section, re.IGNORECASE)
        )
        if wilson_bib:
            print("PASS: Component 1a — Wilson (2019) bibliography entry found (0.1 pts)")
            total_score += 0.1
        else:
            # Partial: at least Wilson 2019 is present
            wilson_partial = bool(re.search(r'Wilson.*2019', bib_section) or re.search(r'2019.*Wilson', bib_section))
            if wilson_partial:
                print("PARTIAL: Component 1a — Wilson (2019) partial bibliography entry found (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 1a — Wilson (2019) Modern Linguistics Springer not found in bibliography")
    except Exception as e:
        print(f"ERROR: Component 1a — {e}")

    # Component 1b: Zhang (2020) bibliography entry
    try:
        zhang_bib = bool(
            re.search(r'Zhang', bib_section) and
            re.search(r'2020', bib_section) and
            re.search(r'Computational Syntax', bib_section, re.IGNORECASE) and
            re.search(r'MIT Press', bib_section, re.IGNORECASE)
        )
        if zhang_bib:
            print("PASS: Component 1b — Zhang (2020) bibliography entry found (0.1 pts)")
            total_score += 0.1
        else:
            zhang_partial = bool(re.search(r'Zhang.*2020', bib_section) or re.search(r'2020.*Zhang', bib_section))
            if zhang_partial:
                print("PARTIAL: Component 1b — Zhang (2020) partial bibliography entry found (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 1b — Zhang (2020) Computational Syntax MIT Press not found in bibliography")
    except Exception as e:
        print(f"ERROR: Component 1b — {e}")

    # Component 1c: Brown (2021) bibliography entry
    try:
        brown_bib = bool(
            re.search(r'Brown', bib_section) and
            re.search(r'2021', bib_section) and
            re.search(r'Pragmatics', bib_section, re.IGNORECASE) and
            re.search(r'Oxford', bib_section, re.IGNORECASE)
        )
        if brown_bib:
            print("PASS: Component 1c — Brown (2021) bibliography entry found (0.1 pts)")
            total_score += 0.1
        else:
            brown_partial = bool(re.search(r'Brown.*2021', bib_section) or re.search(r'2021.*Brown', bib_section))
            if brown_partial:
                print("PARTIAL: Component 1c — Brown (2021) partial bibliography entry found (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 1c — Brown (2021) Pragmatics Oxford not found in bibliography")
    except Exception as e:
        print(f"ERROR: Component 1c — {e}")

    # Component 1d: Taylor (2022) bibliography entry
    try:
        taylor_bib = bool(
            re.search(r'Taylor', bib_section) and
            re.search(r'2022', bib_section) and
            re.search(r'Discourse Analysis', bib_section, re.IGNORECASE) and
            re.search(r'Routledge', bib_section, re.IGNORECASE)
        )
        if taylor_bib:
            print("PASS: Component 1d — Taylor (2022) bibliography entry found (0.1 pts)")
            total_score += 0.1
        else:
            taylor_partial = bool(re.search(r'Taylor.*2022', bib_section) or re.search(r'2022.*Taylor', bib_section))
            if taylor_partial:
                print("PARTIAL: Component 1d — Taylor (2022) partial bibliography entry found (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 1d — Taylor (2022) Discourse Analysis Routledge not found in bibliography")
    except Exception as e:
        print(f"ERROR: Component 1d — {e}")

    # ------------------------------------------------------------------
    # Component 2: In-text citations for Wilson, Zhang, Brown (0.3 pts, 0.1 each)
    # Task: "(Wilson, 2019)" after paragraph 1, "(Zhang, 2020)" after paragraph 2,
    #       "(Brown, 2021)" after paragraph 3
    # In the golden doc, these appear as standalone paragraphs after each body paragraph.
    # The format can be: a standalone paragraph with the citation, OR embedded in the paragraph.
    # ------------------------------------------------------------------

    # Component 2a: (Wilson, 2019) citation in text (not in bibliography section)
    try:
        # Search in the body text (before bibliography section)
        body_texts = all_texts[:bib_start] if bib_start > 0 else all_texts
        body_section = '\n'.join(body_texts)

        # Check for (Wilson, 2019) citation pattern — flexible matching
        wilson_cite = bool(
            re.search(r'\(Wilson,?\s*2019\)', body_section) or
            re.search(r'Wilson\s*\(2019\)', body_section)
        )
        if wilson_cite:
            print("PASS: Component 2a — (Wilson, 2019) in-text citation found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2a — (Wilson, 2019) in-text citation not found in body text")
    except Exception as e:
        print(f"ERROR: Component 2a — {e}")

    # Component 2b: (Zhang, 2020) citation in text
    try:
        zhang_cite = bool(
            re.search(r'\(Zhang,?\s*2020\)', body_section) or
            re.search(r'Zhang\s*\(2020\)', body_section)
        )
        if zhang_cite:
            print("PASS: Component 2b — (Zhang, 2020) in-text citation found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2b — (Zhang, 2020) in-text citation not found in body text")
    except Exception as e:
        print(f"ERROR: Component 2b — {e}")

    # Component 2c: (Brown, 2021) citation in text
    try:
        brown_cite = bool(
            re.search(r'\(Brown,?\s*2021\)', body_section) or
            re.search(r'Brown\s*\(2021\)', body_section)
        )
        if brown_cite:
            print("PASS: Component 2c — (Brown, 2021) in-text citation found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2c — (Brown, 2021) in-text citation not found in body text")
    except Exception as e:
        print(f"ERROR: Component 2c — {e}")

    # ------------------------------------------------------------------
    # Component 3: (Taylor, 2022) citation within the discourse analysis paragraph (0.3 pts)
    # Task: insert citation "in paragraph 4" (the discourse analysis paragraph).
    # In golden doc, paragraph 14 (index) contains "(Taylor, 2022)" inline.
    # We verify the discourse analysis paragraph contains the Taylor citation.
    # ------------------------------------------------------------------
    try:
        # The fourth body paragraph is about discourse analysis
        # It should contain both the discourse analysis content AND the (Taylor, 2022) citation
        discourse_para_text = None
        search_texts = body_texts if bib_start > 0 else all_texts

        for text in search_texts:
            if ('Discourse analysis' in text or 'discourse analysis' in text):
                if re.search(r'\(Taylor,?\s*2022\)', text) or re.search(r'Taylor\s*\(2022\)', text):
                    discourse_para_text = text[:100]
                    break

        if discourse_para_text is not None:
            print(f"PASS: Component 3 — (Taylor, 2022) citation embedded in discourse analysis paragraph (0.3 pts)")
            print(f"      Para text: {discourse_para_text!r}...")
            total_score += 0.3
        else:
            # Check if (Taylor, 2022) appears anywhere in the body at all (partial credit)
            taylor_anywhere = bool(
                re.search(r'\(Taylor,?\s*2022\)', body_section) or
                re.search(r'Taylor\s*\(2022\)', body_section)
            )
            if taylor_anywhere:
                print("PARTIAL: Component 3 — (Taylor, 2022) citation found in body but not within discourse analysis paragraph (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 3 — (Taylor, 2022) citation not found in body text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM environment
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
