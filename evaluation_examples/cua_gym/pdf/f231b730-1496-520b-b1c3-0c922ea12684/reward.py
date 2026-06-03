"""
Reward Script: Linearize PDF for fast web viewing with image downsampling
Task ID: pdf_aw_020
Domain: pdf
Scoring:
  Component 1 — Output file exists and is a valid PDF (0.10 pts)
  Component 2 — PDF is linearized for fast web viewing (0.25 pts)
  Component 3 — File size is smaller than original (0.20 pts)
  Component 4 — Images are downsampled (smaller than original 1200x900) (0.25 pts)
  Component 5 — All 100 pages preserved correctly (0.20 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_020'
OUTPUT_PATH = os.path.join(WORKDIR, 'web', 'large_report_web.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'web', 'large_report.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists and is a valid, openable PDF (0.10 points)
    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
        page_count = len(doc)
        doc.close()
        if page_count > 0:
            print(f"PASS: Component 1 — Valid PDF with {page_count} pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: PDF is linearized (has /Linearized in first 4KB) (0.25 points)
    try:
        with open(OUTPUT_PATH, 'rb') as f:
            first_bytes = f.read(4096).decode('latin-1', errors='replace')
        if '/Linearized' in first_bytes:
            print(f"PASS: Component 2 — PDF is linearized (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — /Linearized not found in first 4KB of file")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File size is smaller than original (0.20 points)
    # Original is ~16.6 MB. Task says target < 50 MB; golden is ~3.1 MB.
    try:
        original_size = os.path.getsize(ORIGINAL_PATH)
        output_size = os.path.getsize(OUTPUT_PATH)
        if output_size < original_size:
            print(f"PASS: Component 3 — Output ({output_size/1024/1024:.1f} MB) < Original ({original_size/1024/1024:.1f} MB) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Output ({output_size/1024/1024:.1f} MB) is NOT smaller than original ({original_size/1024/1024:.1f} MB)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Images are downsampled — smaller than original 1200x900 (0.25 points)
    # We check images on several pages to confirm downsampling happened.
    try:
        import fitz
        doc_out = fitz.open(OUTPUT_PATH)
        doc_orig = fitz.open(ORIGINAL_PATH)

        downsampled_count = 0
        checked_count = 0
        sample_pages = [0, 10, 50]

        for pg_idx in sample_pages:
            if pg_idx >= len(doc_out) or pg_idx >= len(doc_orig):
                continue
            out_images = doc_out[pg_idx].get_images(full=True)
            orig_images = doc_orig[pg_idx].get_images(full=True)

            if not orig_images or not out_images:
                continue

            # Compare first image on each sampled page
            orig_xref = orig_images[0][0]
            out_xref = out_images[0][0]

            orig_pix = fitz.Pixmap(doc_orig, orig_xref)
            out_pix = fitz.Pixmap(doc_out, out_xref)

            orig_pixels = orig_pix.width * orig_pix.height
            out_pixels = out_pix.width * out_pix.height

            checked_count += 1
            if out_pixels < orig_pixels:
                downsampled_count += 1
                print(f"  Page {pg_idx}: image downsampled {orig_pix.width}x{orig_pix.height} -> {out_pix.width}x{out_pix.height}")

            orig_pix = None
            out_pix = None

        doc_out.close()
        doc_orig.close()

        if checked_count > 0 and downsampled_count == checked_count:
            print(f"PASS: Component 4 — All {downsampled_count}/{checked_count} sampled images are downsampled (0.25 pts)")
            total_score += 0.25
        elif checked_count > 0 and downsampled_count > 0:
            partial = 0.25 * (downsampled_count / checked_count)
            print(f"PARTIAL: Component 4 — {downsampled_count}/{checked_count} images downsampled ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No images appear downsampled (checked {checked_count} pages)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All 100 pages are preserved (0.20 points)
    try:
        import fitz
        doc_out = fitz.open(OUTPUT_PATH)
        doc_orig = fitz.open(ORIGINAL_PATH)
        out_pages = len(doc_out)
        orig_pages = len(doc_orig)
        doc_out.close()
        doc_orig.close()

        if out_pages == orig_pages:
            print(f"PASS: Component 5 — Page count preserved: {out_pages} pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — Page count mismatch: output has {out_pages}, original has {orig_pages}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
