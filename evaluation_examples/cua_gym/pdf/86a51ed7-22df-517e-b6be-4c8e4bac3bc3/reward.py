"""
Reward Script: Add margin note to PDF
Task ID: pdf_res_002
Domain: pdf
Scoring:
  Component 1: Output file exists at correct path (0.15)
  Component 2: All 8 pages preserved (0.15)
  Component 3: Text annotation exists on page 4 (0-indexed 3) (0.35)
  Component 4: Annotation content is 'Check methodology section' (0.35)
"""

import os

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_002'

OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'neural_nets_annotated.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'papers', 'neural_nets.pdf')
EXPECTED_PAGE_COUNT = 8
TARGET_PAGE_INDEX = 3  # page 4, 0-indexed
EXPECTED_CONTENT = 'Check methodology section'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at /home/user/papers/neural_nets_annotated.pdf (0.15 points)
    # This is task-introduced: the annotated file does not exist before the task.
    try:
        if os.path.isfile(OUTPUT_PATH):
            file_size = os.path.getsize(OUTPUT_PATH)
            if file_size > 1000:  # sanity: a valid multi-page PDF should be > 1KB
                print(f"PASS: Component 1 — Output file exists ({file_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Output file exists but suspiciously small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 1 — Output file not found at {OUTPUT_PATH}")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Try to open the annotated PDF
    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open {OUTPUT_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All 8 pages preserved (0.15 points)
    # The original PDF has 8 pages; the annotated copy must retain all of them.
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Page count is {page_count} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: A Text annotation (sticky note) exists on page 4 (0-indexed 3) (0.35 points)
    try:
        page = doc[TARGET_PAGE_INDEX]
        annot_iter = page.annots()
        text_annots = []
        if annot_iter:
            for annot in annot_iter:
                if annot.type[0] == 0 or annot.type[1] == "Text":
                    text_annots.append(annot)

        if len(text_annots) > 0:
            print(f"PASS: Component 3 — Found {len(text_annots)} Text annotation(s) on page {TARGET_PAGE_INDEX + 1} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — No Text annotations found on page {TARGET_PAGE_INDEX + 1}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Annotation content matches 'Check methodology section' (0.35 points)
    try:
        page = doc[TARGET_PAGE_INDEX]
        annot_iter = page.annots()
        found_contents = []
        matching_annots = []
        if annot_iter:
            for annot in annot_iter:
                annot_content = annot.info.get("content", "")
                found_contents.append(repr(annot_content))
                # Check for exact or close match (case-insensitive, trimmed)
                if annot_content.strip().lower() == EXPECTED_CONTENT.lower():
                    matching_annots.append(annot_content)

        if len(matching_annots) > 0:
            print(f"PASS: Component 4 — Annotation content matches '{EXPECTED_CONTENT}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 4 — Expected content '{EXPECTED_CONTENT}', found: {found_contents}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
