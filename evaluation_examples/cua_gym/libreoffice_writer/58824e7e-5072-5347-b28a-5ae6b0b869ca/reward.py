"""
Reward Script: Add citation to reference list and insert cross-reference
Task ID: osworld_writer_biblio_001
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): Reference entry 4 added to References section (Smith et al. 2023)
  Component 2 (0.3 pts): [REF] placeholder in second paragraph replaced with (4) or [4]
  Component 3 (0.2 pts): [REF] fully removed from document (no leftover placeholder)
Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_biblio_001'


def persist_app_state():
    """Best-effort save for LibreOffice Writer GUI edits."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def find_para_with(doc, condition_fn):
    """Return first paragraph matching condition_fn, or None."""
    for para in doc.paragraphs:
        if condition_fn(para.text):
            return para
    return None


def find_ref_placeholder_text(doc):
    """Return text of the first paragraph containing [REF], or empty string."""
    para = find_para_with(doc, lambda t: '[REF]' in t)
    return para.text if para is not None else ""


def find_cross_ref_para_text(doc):
    """Return text of paragraph containing (4) or [4] near 'labeled data', or empty string."""
    para = find_para_with(
        doc,
        lambda t: ('(4)' in t or '[4]' in t) and 'labeled data' in t
    )
    return para.text if para is not None else ""


def find_ref4_entry_text(doc):
    """Return text of the 4th reference entry starting with '4.' and 'Smith', or empty string."""
    para = find_para_with(doc, lambda t: t.strip().startswith('4.') and 'Smith' in t)
    return para.text.strip() if para is not None else ""


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Verifies:
    1. The 4th reference entry (Smith, J., & Lee, K. 2023) appears in the References section
    2. The [REF] placeholder replaced with (4) or [4] in the second body paragraph
    3. No [REF] placeholder remains anywhere in the document
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Reference entry 4 (Smith et al. 2023) added to References
    # section (0.5 points)
    # Must start with "4." and contain author/title/journal/year fields.
    # -----------------------------------------------------------------------
    try:
        ref4_text = find_ref4_entry_text(doc)

        if not ref4_text:
            print("FAIL: Component 1 — No reference entry starting with '4.' containing 'Smith' found")
        else:
            # Check key APA citation fields
            field_checks = {
                'author_smith': 'Smith, J.' in ref4_text,
                'author_lee': 'Lee, K.' in ref4_text,
                'year_2023': '2023' in ref4_text,
                'title_keyword': 'Deep learning' in ref4_text or 'deep learning' in ref4_text,
                'journal_name': (
                    'Journal of Artificial Intelligence Research' in ref4_text
                    or 'JAIR' in ref4_text
                ),
            }

            passed = sum(1 for v in field_checks.values() if v)
            total_fields = len(field_checks)

            if passed == total_fields:
                print(f"PASS: Component 1 — Reference 4 found with all required fields: "
                      f"{ref4_text[:80]!r} (0.5 pts)")
                total_score += 0.5
            elif passed >= 3:
                # Partial credit if most fields present
                partial = 0.3
                missing = [k for k, v in field_checks.items() if not v]
                print(f"PARTIAL: Component 1 — Reference 4 found but {len(missing)} field(s) missing: "
                      f"{missing}. ({partial} pts)")
                total_score += partial
            else:
                missing = [k for k, v in field_checks.items() if not v]
                print(f"FAIL: Component 1 — Reference 4 entry incomplete ({passed}/{total_fields} fields): "
                      f"missing {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: [REF] placeholder replaced with cross-reference (4) or [4]
    # in the paragraph about 'labeled data' (second body paragraph) (0.3 points)
    # -----------------------------------------------------------------------
    try:
        cross_ref_para_text = find_cross_ref_para_text(doc)

        if cross_ref_para_text:
            print(f"PASS: Component 2 — Cross-reference (4)/[4] found in correct paragraph "
                  f"(near 'labeled data'). (0.3 pts)")
            total_score += 0.3
        else:
            # Diagnose: does the labeled-data paragraph exist at all?
            labeled_para = find_para_with(doc, lambda t: 'labeled data' in t)
            if labeled_para is not None:
                snippet = labeled_para.text[100:150]
                print(f"FAIL: Component 2 — 'labeled data' paragraph found but "
                      f"no (4) or [4] cross-reference present. Snippet: {snippet!r}")
            else:
                print("FAIL: Component 2 — Cannot locate expected paragraph with 'labeled data'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: [REF] placeholder fully removed from document (0.2 points)
    # No [REF] text should remain anywhere after the task completes.
    # We award this component when [REF] is gone; the cross-ref check in
    # Component 2 already verifies proper replacement separately.
    # -----------------------------------------------------------------------
    try:
        stale_placeholder_text = find_ref_placeholder_text(doc)

        if stale_placeholder_text:
            snippet = stale_placeholder_text[80:120]
            print(f"FAIL: Component 3 — [REF] placeholder still present: {snippet!r}")
        if not stale_placeholder_text:
            print("PASS: Component 3 — [REF] placeholder no longer present in document. (0.2 pts)")
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
