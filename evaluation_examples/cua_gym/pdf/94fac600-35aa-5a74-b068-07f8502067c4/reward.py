"""
Reward Script: Strip all metadata including XMP from settlement_agreement.pdf,
set only Title to 'Confidential' and Author to 'Legal Department',
save as settlement_clean.pdf.

Task ID: pdf_mbc_020
Domain: pdf

Scoring:
  Component 1 (0.15): Output file exists at ~/Legal/settlement_clean.pdf
  Component 2 (0.25): Title metadata is 'Confidential'
  Component 3 (0.25): Author metadata is 'Legal Department'
  Component 4 (0.20): Other standard metadata fields stripped (subject, keywords, creator, creationDate, modDate)
  Component 5 (0.15): XMP metadata cleaned (no XMP keys)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_020'
OUTPUT_PATH = os.path.join(WORKDIR, 'Legal', 'settlement_clean.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists (0.15 points)
    # This is a task-introduced change: settlement_clean.pdf does not exist in initial_env
    if not os.path.exists(file_path):
        print(f"FAIL: Component 1 - Output file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    print(f"PASS: Component 1 - Output file exists at {file_path} (0.15 pts)")
    total_score += 0.15

    # Load the PDF with PyMuPDF
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        meta = doc.metadata
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Title is 'Confidential' (0.25 points)
    try:
        title = meta.get('title', '') or ''
        if title.strip() == 'Confidential':
            print(f"PASS: Component 2 - Title is 'Confidential' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Expected title 'Confidential', found: {repr(title)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Author is 'Legal Department' (0.25 points)
    try:
        author = meta.get('author', '') or ''
        if author.strip() == 'Legal Department':
            print(f"PASS: Component 3 - Author is 'Legal Department' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Expected author 'Legal Department', found: {repr(author)}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Other standard metadata fields stripped (0.20 points)
    # Check that subject, keywords, creator, creationDate, modDate are all empty
    try:
        fields_to_check = ['subject', 'keywords', 'creator', 'creationDate', 'modDate']
        all_empty = True
        for field in fields_to_check:
            value = meta.get(field, '') or ''
            if value.strip():
                print(f"  INFO: Field '{field}' not empty: {repr(value)}")
                all_empty = False

        if all_empty:
            print(f"PASS: Component 4 - All other metadata fields stripped (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - Some metadata fields still contain values")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    doc.close()

    # Component 5: XMP metadata cleaned (0.15 points)
    # Use pikepdf to check XMP metadata has no meaningful keys
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
        xmp_clean = True
        try:
            with pdf.open_metadata() as xmp_meta:
                xmp_keys = list(xmp_meta.keys())
                if len(xmp_keys) > 0:
                    print(f"  INFO: XMP still has keys: {xmp_keys}")
                    xmp_clean = False
        except Exception:
            # If metadata cannot be opened, consider it cleaned
            xmp_clean = True

        pdf.close()

        if xmp_clean:
            print(f"PASS: Component 5 - XMP metadata cleaned (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - XMP metadata still contains entries")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
