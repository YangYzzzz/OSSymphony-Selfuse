"""
Reward Script: Add bibliography entry and cross-reference in LibreOffice Writer
Task ID: osworld_writer_biblio_009
Domain: libreoffice_writer
Scoring:
  - Component 1: Reference 8 (Osei-Bonsu) appended to References section (0.5 pts)
  - Component 2: Reference 8 content is complete and correctly formatted (0.3 pts)
  - Component 3: '(ref needed)' placeholder in third body paragraph replaced with '(8)' (0.2 pts)
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_biblio_009'


def persist_app_state():
    """Send Ctrl+S to save any unsaved LibreOffice edits before scoring."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.2)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that:
    1. Reference 8 (Osei-Bonsu et al., 2023) has been appended to the References section
    2. Reference 8 contains all required citation fields (authors, year, title, journal, volume, issue, pages, DOI)
    3. The '(ref needed)' placeholder in the third body paragraph has been replaced with '(8)'

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraph texts for inspection
    all_texts = [para.text.strip() for para in doc.paragraphs]

    # -----------------------------------------------------------------------
    # Component 1: Reference 8 appended to References section (0.5 points)
    # The task requires adding "8. Osei-Bonsu, A., Mensah, G. K., & Boateng, R. (2023)..."
    # In the initial state there are only 7 references; golden adds an 8th.
    # -----------------------------------------------------------------------
    try:
        ref8_para = None
        for text in all_texts:
            if text.startswith('8.') and 'Osei-Bonsu' in text:
                ref8_para = text
                break

        if ref8_para is not None:
            print(f"PASS: Component 1 — Reference 8 (Osei-Bonsu) found in document (0.5 pts)")
            print(f"       Found: {ref8_para[:120]}")
            total_score += 0.5
        else:
            # Also check if any paragraph mentions Osei-Bonsu (might be unnumbered)
            osei_found = any('Osei-Bonsu' in t for t in all_texts)
            if osei_found:
                print(f"FAIL: Component 1 — Osei-Bonsu found but not numbered '8.' — incorrect formatting")
            else:
                print(f"FAIL: Component 1 — No reference starting with '8.' and containing 'Osei-Bonsu' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Reference 8 content completeness and correctness (0.3 points)
    # Must contain: authors (Osei-Bonsu, Mensah, Boateng), year 2023, journal name,
    # volume 24, issue 3, pages 312-329, and DOI 10.1080/15228916.2023.2180145
    # -----------------------------------------------------------------------
    try:
        if ref8_para is not None:
            checks = {
                'year_2023': '2023' in ref8_para,
                'mensah': 'Mensah' in ref8_para,
                'boateng': 'Boateng' in ref8_para,
                'journal': 'Journal of African Business' in ref8_para,
                'volume_issue_pages': ('24(3)' in ref8_para or ('24' in ref8_para and '312' in ref8_para)),
                'doi': '10.1080/15228916' in ref8_para,
            }
            passed = sum(checks.values())
            total_fields = len(checks)

            if passed == total_fields:
                print(f"PASS: Component 2 — All {total_fields}/{total_fields} citation fields correct (0.3 pts)")
                total_score += 0.3
            elif passed >= 4:
                # Partial credit not possible per design — need all fields for 0.3
                print(f"FAIL: Component 2 — {passed}/{total_fields} fields correct: {checks}")
            else:
                print(f"FAIL: Component 2 — Only {passed}/{total_fields} citation fields present: {checks}")
        else:
            print(f"FAIL: Component 2 — Cannot check citation fields; reference 8 not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Cross-reference '(ref needed)' replaced with '(8)' (0.2 points)
    # The third body paragraph (about regulatory/structural barriers) had "(ref needed)"
    # in the initial file; in the golden it must have "(8)" and NOT "(ref needed)".
    # -----------------------------------------------------------------------
    try:
        # Find the paragraph with the structural barriers content (third body paragraph)
        # It is about "regulatory fragmentation" and "digital literacy deficits"
        third_para_text = None
        for text in all_texts:
            if 'regulatory fragmentation' in text.lower() or 'digital literacy deficits' in text.lower():
                third_para_text = text
                break

        if third_para_text is None:
            print(f"FAIL: Component 3 — Could not locate third body paragraph")
        elif '(ref needed)' in third_para_text:
            print(f"FAIL: Component 3 — '(ref needed)' placeholder still present in third paragraph")
        elif '(8)' in third_para_text:
            print(f"PASS: Component 3 — '(ref needed)' replaced with '(8)' in third paragraph (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Neither '(ref needed)' nor '(8)' found in third paragraph")
            print(f"       Paragraph snippet: {third_para_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: persist unsaved state, then verify
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state()

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
