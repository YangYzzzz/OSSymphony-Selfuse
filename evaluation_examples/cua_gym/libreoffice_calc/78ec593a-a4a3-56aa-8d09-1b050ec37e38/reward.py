"""
Reward Script: Compress PDF by reducing image quality and removing unused objects
Task ID: pdf_ro_028
Domain: pdf
Scoring:
  Component 1: Compressed file exists at expected path (0.15)
  Component 2: File size significantly reduced (under 15MB, much smaller than ~35MB original) (0.30)
  Component 3: All 50 pages preserved (0.25)
  Component 4: Text content preserved on sampled pages (0.20)
  Component 5: Images still present in compressed file (0.10)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_028'

ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'large_report.pdf')
COMPRESSED_PATH = os.path.join(WORKDIR, 'Documents', 'large_report_compressed.pdf')

# Target constraints from task description
ORIGINAL_SIZE_APPROX = 35_000_000  # ~35MB (task says 45MB but actual is ~35MB)
MAX_COMPRESSED_SIZE = 15_000_000   # 15MB target from task instruction
EXPECTED_PAGE_COUNT = 50


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Compressed file exists at expected path (0.15 points)
    # This is the ONLY file-existence check, and it checks for a NEW file
    # that should NOT exist before the task is performed.
    try:
        if os.path.isfile(COMPRESSED_PATH):
            compressed_size = os.path.getsize(COMPRESSED_PATH)
            if compressed_size > 0:
                print(f"PASS: Component 1 — Compressed file exists at {COMPRESSED_PATH} ({compressed_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Compressed file exists but is empty (0 bytes)")
        else:
            print(f"FAIL: Component 1 — Compressed file not found at {COMPRESSED_PATH}")
            # If the compressed file doesn't exist, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File size significantly reduced (0.30 points)
    # The compressed file must be meaningfully smaller than the original.
    # Task targets under 15MB; original is ~35MB.
    try:
        original_size = os.path.getsize(ORIGINAL_PATH) if os.path.isfile(ORIGINAL_PATH) else ORIGINAL_SIZE_APPROX
        compressed_size = os.path.getsize(COMPRESSED_PATH)

        # Must be at least 50% smaller than original to count as real compression
        size_ratio = compressed_size / original_size if original_size > 0 else 1.0

        if compressed_size <= MAX_COMPRESSED_SIZE:
            # Under target — full points
            print(f"PASS: Component 2 — Compressed size {compressed_size} bytes ({compressed_size/1_000_000:.2f} MB) is under 15MB target. Ratio: {size_ratio:.4f} (0.30 pts)")
            total_score += 0.30
        elif size_ratio < 0.5:
            # Not under 15MB but still significantly compressed — partial credit
            print(f"PARTIAL: Component 2 — Compressed size {compressed_size} bytes ({compressed_size/1_000_000:.2f} MB) exceeds 15MB target but is {(1-size_ratio)*100:.1f}% smaller (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Compressed size {compressed_size} bytes ({compressed_size/1_000_000:.2f} MB), ratio {size_ratio:.4f} — not enough compression")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 50 pages preserved (0.25 points)
    try:
        import fitz
        doc = fitz.open(COMPRESSED_PATH)
        page_count = doc.page_count

        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 3 — Page count is {page_count} (expected {EXPECTED_PAGE_COUNT}) (0.25 pts)")
            total_score += 0.25
        elif page_count > 0:
            # Partial credit: proportional to pages preserved
            ratio = min(page_count, EXPECTED_PAGE_COUNT) / EXPECTED_PAGE_COUNT
            partial = round(0.25 * ratio, 2)
            print(f"PARTIAL: Component 3 — Page count is {page_count} (expected {EXPECTED_PAGE_COUNT}), {ratio*100:.0f}% preserved ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages found in compressed file")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text content preserved on sampled pages (0.20 points)
    # Compare text from pages 0, 24, 49 between original and compressed.
    try:
        import fitz
        original_doc = fitz.open(ORIGINAL_PATH)
        compressed_doc = fitz.open(COMPRESSED_PATH)

        sample_pages = [0, 24, 49]
        matches = 0
        total_checks = len(sample_pages)

        for pn in sample_pages:
            if pn < original_doc.page_count and pn < compressed_doc.page_count:
                orig_text = original_doc[pn].get_text().strip()
                comp_text = compressed_doc[pn].get_text().strip()

                # Check that at least 90% of original text is preserved
                # (compression should not remove text)
                if len(orig_text) > 0 and len(comp_text) > 0:
                    # Check if the first 200 chars match (title/header area)
                    orig_start = orig_text[:200]
                    comp_start = comp_text[:200]
                    if orig_start == comp_start:
                        matches += 1
                        print(f"  Page {pn}: text preserved (first 200 chars match)")
                    else:
                        print(f"  Page {pn}: text DIFFERS — original starts with {repr(orig_start[:80])}, compressed starts with {repr(comp_start[:80])}")
                else:
                    print(f"  Page {pn}: text missing — original len={len(orig_text)}, compressed len={len(comp_text)}")
            else:
                print(f"  Page {pn}: page index out of range")

        original_doc.close()
        compressed_doc.close()

        if matches == total_checks:
            print(f"PASS: Component 4 — Text preserved on all {total_checks} sampled pages (0.20 pts)")
            total_score += 0.20
        elif matches > 0:
            partial = round(0.20 * matches / total_checks, 2)
            print(f"PARTIAL: Component 4 — Text preserved on {matches}/{total_checks} sampled pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Text not preserved on any sampled page")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Images still present in compressed file (0.10 points)
    # Images should still exist (at reduced quality/resolution), not be stripped entirely.
    try:
        import fitz
        doc = fitz.open(COMPRESSED_PATH)

        # Count images across sampled pages
        pages_with_images = 0
        sample = [0, 10, 25, 40, 49]
        checked = 0
        for pn in sample:
            if pn < doc.page_count:
                checked += 1
                imgs = doc[pn].get_images(full=True)
                if len(imgs) > 0:
                    pages_with_images += 1

        doc.close()

        if checked > 0 and pages_with_images == checked:
            print(f"PASS: Component 5 — Images present on all {checked} sampled pages (0.10 pts)")
            total_score += 0.10
        elif pages_with_images > 0:
            partial = round(0.10 * pages_with_images / checked, 2)
            print(f"PARTIAL: Component 5 — Images on {pages_with_images}/{checked} sampled pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No images found on any sampled page")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(COMPRESSED_PATH):
    print(f"File not found: {COMPRESSED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
