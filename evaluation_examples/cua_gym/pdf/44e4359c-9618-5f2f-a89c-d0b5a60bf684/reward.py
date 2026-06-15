"""
Reward Script: Add reply annotation to existing sticky note on page 6 of team_review.pdf
Task ID: pdf_fm_025
Domain: pdf
Scoring:
  Component 1 (0.3): A second Text annotation exists on page 5 (0-indexed)
  Component 2 (0.3): Reply annotation content matches expected text
  Component 3 (0.2): Reply has IRT (In Reply To) reference to original note
  Component 4 (0.2): Original sticky note preserved with correct content
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_025'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'team_review.pdf')
PAGE_NUM = 5  # page 6 in 1-indexed, 5 in 0-indexed

ORIGINAL_CONTENT = 'Is this figure correct?'
REPLY_CONTENT = 'Yes, verified against source data on 2025-08-15'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc) < PAGE_NUM + 1:
        print(f"CRITICAL: PDF has only {len(doc)} pages, need at least {PAGE_NUM + 1}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[PAGE_NUM]

    # Collect all annotations on the page
    try:
        annots = list(page.annots())
    except Exception as e:
        print(f"CRITICAL: Cannot read annotations: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Separate original and reply annotations
    text_annots = [a for a in annots if a.type[1] == 'Text']
    original_annot = None
    reply_annot = None

    for a in text_annots:
        content = a.info.get('content', '')
        if ORIGINAL_CONTENT in content:
            original_annot = a
        if REPLY_CONTENT in content:
            reply_annot = a

    # Component 1: A second Text annotation exists on page 5 (0.3 points)
    # Initial has 1 Text annot, golden should have >= 2
    try:
        if len(text_annots) >= 2:
            print(f"PASS: Component 1 — Found {len(text_annots)} Text annotations on page {PAGE_NUM} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Found only {len(text_annots)} Text annotation(s), expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Reply annotation has correct content (0.3 points)
    try:
        if reply_annot is not None:
            actual_content = reply_annot.info.get('content', '')
            if REPLY_CONTENT in actual_content:
                print(f"PASS: Component 2 — Reply content matches: {repr(actual_content)} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Reply content mismatch: expected {repr(REPLY_CONTENT)}, found {repr(actual_content)}")
        else:
            print(f"FAIL: Component 2 — No annotation found with reply content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Reply has IRT reference to original note (0.2 points)
    try:
        if reply_annot is not None and original_annot is not None:
            reply_xref = reply_annot.xref
            orig_xref = original_annot.xref
            # Read raw PDF object to check for IRT reference
            reply_obj = doc.xref_object(reply_xref)
            # Check if IRT references the original annotation's xref
            irt_ref = f'{orig_xref} 0 R'
            if f'/IRT {irt_ref}' in reply_obj:
                print(f"PASS: Component 3 — IRT reference found pointing to original (xref {orig_xref}) (0.2 pts)")
                total_score += 0.2
            elif '/IRT' in reply_obj:
                # IRT exists but points elsewhere - give partial credit
                print(f"PARTIAL: Component 3 — IRT reference exists but doesn't point to original note. Object: {reply_obj[:200]}")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — No IRT reference in reply annotation. Object: {reply_obj[:200]}")
        elif reply_annot is None:
            print(f"FAIL: Component 3 — No reply annotation found to check IRT")
        else:
            print(f"FAIL: Component 3 — Original annotation not found to verify IRT target")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Original sticky note preserved (0.2 points)
    # This component checks that the original note still exists AND the reply is present
    # (compound check anchored to the change - the reply being added without destroying original)
    try:
        if original_annot is not None and reply_annot is not None:
            orig_content = original_annot.info.get('content', '')
            if ORIGINAL_CONTENT in orig_content:
                print(f"PASS: Component 4 — Original note preserved with content {repr(orig_content)} alongside reply (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Original note content changed: {repr(orig_content)}")
        elif original_annot is not None and reply_annot is None:
            # Original exists but no reply - this is the initial state, no points
            print(f"FAIL: Component 4 — Original exists but no reply annotation found (initial state)")
        else:
            print(f"FAIL: Component 4 — Original note not found on page {PAGE_NUM}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
