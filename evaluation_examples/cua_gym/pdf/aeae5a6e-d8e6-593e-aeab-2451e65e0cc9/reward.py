"""
Reward Script: Compress PDF by downsampling images to 150 DPI
Task ID: pdf_legal_081
Domain: pdf
Scoring:
  Component 1 (0.15): Compressed file exists at correct output path
  Component 2 (0.25): All 500 pages preserved in compressed file
  Component 3 (0.30): File size significantly smaller than original (~150MB threshold)
  Component 4 (0.30): Text content preserved across sampled pages
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_081'

ORIGINAL_PATH = os.path.join(WORKDIR, 'legal', 'production', 'large_production.pdf')
COMPRESSED_PATH = os.path.join(WORKDIR, 'legal', 'production', 'large_production_compressed.pdf')
EXPECTED_PAGE_COUNT = 500
# Original is ~536MB; task says "currently 150MB" but actual is larger.
# Task requires output to be "significantly smaller than 150MB".
# We use 150MB as upper threshold for compressed file.
MAX_COMPRESSED_SIZE_BYTES = 150 * 1024 * 1024  # 150 MB


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Precondition: original file must still exist ----
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file missing: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # ================================================================
    # Component 1: Compressed file exists at the correct output path
    #   (0.15 points)
    #   This FAILS on initial_env (file does not exist) and
    #   PASSES on golden_env (file was created by compression).
    # ================================================================
    try:
        if os.path.isfile(COMPRESSED_PATH):
            compressed_size = os.path.getsize(COMPRESSED_PATH)
            if compressed_size > 0:
                print(f"PASS: Component 1 — Compressed file exists at {COMPRESSED_PATH} "
                      f"(size: {compressed_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Compressed file exists but is empty (0 bytes)")
        else:
            print(f"FAIL: Component 1 — Compressed file not found at {COMPRESSED_PATH}")
            # No compressed file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ================================================================
    # Component 2: Page count preserved (all 500 pages)
    #   (0.25 points)
    # ================================================================
    try:
        import fitz
        doc = fitz.open(COMPRESSED_PATH)
        page_count = doc.page_count

        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Page count is {page_count} "
                  f"(expected {EXPECTED_PAGE_COUNT}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Page count is {page_count}, "
                  f"expected {EXPECTED_PAGE_COUNT}")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ================================================================
    # Component 3: File size significantly reduced
    #   (0.30 points)
    #   The compressed file must be smaller than 150 MB AND
    #   smaller than the original file.
    # ================================================================
    try:
        original_size = os.path.getsize(ORIGINAL_PATH)
        compressed_size = os.path.getsize(COMPRESSED_PATH)

        is_smaller_than_original = compressed_size < original_size
        is_below_threshold = compressed_size < MAX_COMPRESSED_SIZE_BYTES

        if is_smaller_than_original and is_below_threshold:
            ratio = compressed_size / original_size * 100
            print(f"PASS: Component 3 — Compressed size {compressed_size} bytes "
                  f"({compressed_size/1024/1024:.1f} MB) is {ratio:.1f}% of original "
                  f"({original_size/1024/1024:.1f} MB) and below 150 MB threshold (0.30 pts)")
            total_score += 0.30
        elif is_smaller_than_original and not is_below_threshold:
            # Partial credit: smaller but not below 150MB threshold
            print(f"PARTIAL: Component 3 — Compressed ({compressed_size/1024/1024:.1f} MB) "
                  f"is smaller than original but still above 150 MB threshold")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Compressed size {compressed_size} bytes "
                  f"is NOT smaller than original {original_size} bytes")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ================================================================
    # Component 4: Text content preserved across sampled pages
    #   (0.30 points)
    #   Compare text from several sampled pages between original and
    #   compressed to ensure text was not lost during compression.
    #   We check pages 0, 100, 250, 499 (spread across the document).
    # ================================================================
    try:
        import fitz
        orig_doc = fitz.open(ORIGINAL_PATH)
        comp_doc = fitz.open(COMPRESSED_PATH)

        sample_pages = [0, 100, 250, 499]
        pages_with_matching_text = 0
        pages_checked = 0

        for pg_idx in sample_pages:
            if pg_idx < orig_doc.page_count and pg_idx < comp_doc.page_count:
                pages_checked += 1
                orig_text = orig_doc[pg_idx].get_text().strip()
                comp_text = comp_doc[pg_idx].get_text().strip()

                if len(orig_text) == 0:
                    # Skip pages with no text in original
                    pages_with_matching_text += 1
                    continue

                # Check if at least 80% of original text content is preserved
                # (minor differences due to compression are acceptable)
                orig_words = set(orig_text.split())
                comp_words = set(comp_text.split())

                if len(orig_words) == 0:
                    pages_with_matching_text += 1
                    continue

                overlap = len(orig_words & comp_words) / len(orig_words)
                if overlap >= 0.8:
                    pages_with_matching_text += 1
                    print(f"  Page {pg_idx}: text overlap {overlap*100:.0f}% — OK")
                else:
                    print(f"  Page {pg_idx}: text overlap {overlap*100:.0f}% — DEGRADED")

        orig_doc.close()
        comp_doc.close()

        if pages_checked > 0 and pages_with_matching_text == pages_checked:
            print(f"PASS: Component 4 — Text preserved on all {pages_checked} sampled pages (0.30 pts)")
            total_score += 0.30
        elif pages_checked > 0:
            # Partial credit proportional to pages that passed
            partial = 0.30 * (pages_with_matching_text / pages_checked)
            print(f"PARTIAL: Component 4 — Text preserved on {pages_with_matching_text}/{pages_checked} "
                  f"sampled pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages could be checked for text preservation")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
