"""
Reward Script: Compress PDF by reducing image DPI, removing thumbnails and metadata
Task ID: pdf_cf_033
Domain: pdf
Scoring:
  Component 1 (0.30): Compressed file exists and is significantly smaller than original
  Component 2 (0.25): Page count preserved (20 pages)
  Component 3 (0.25): Metadata stripped (title, author, subject, keywords, creator, producer all empty)
  Component 4 (0.20): Images are compressed (smaller pixel dimensions than original)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_cf_033'

ORIGINAL_PATH = f'{WORKDIR}/Documents/large_presentation.pdf'
COMPRESSED_PATH = f'{WORKDIR}/Documents/large_presentation_compressed.pdf'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: original file must exist
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: compressed file must exist (task-introduced — does not exist in initial_env)
    if not os.path.exists(COMPRESSED_PATH):
        print(f"CRITICAL: Compressed file not found: {COMPRESSED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    import fitz

    # Load both files
    try:
        orig_doc = fitz.open(ORIGINAL_PATH)
        comp_doc = fitz.open(COMPRESSED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF files: {e}")
        print("REWARD: 0.0")
        return 0.0

    orig_size = os.path.getsize(ORIGINAL_PATH)
    comp_size = os.path.getsize(COMPRESSED_PATH)

    # Component 1: File size significantly reduced (0.30 points)
    # The compressed file must be smaller than the original.
    # Task context says ideally < 5MB; original is ~17MB.
    try:
        ratio = comp_size / orig_size
        if comp_size < orig_size:
            # Graduated scoring: more compression = more points
            if ratio < 0.5:
                # Excellent compression (< 50% of original)
                print(f"PASS: Component 1 — Compressed size {comp_size} is {ratio:.2%} of original {orig_size} (0.30 pts)")
                total_score += 0.30
            else:
                # Some compression achieved but not great
                print(f"PARTIAL: Component 1 — Compressed size {comp_size} is {ratio:.2%} of original {orig_size} (0.15 pts)")
                total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Compressed size {comp_size} >= original {orig_size}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page count preserved at 20 (0.25 points)
    # The compressed PDF must retain all 20 pages from the original.
    try:
        orig_pages = orig_doc.page_count
        comp_pages = comp_doc.page_count
        if comp_pages == 20:
            print(f"PASS: Component 2 — Compressed PDF has {comp_pages} pages (expected 20) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Compressed PDF has {comp_pages} pages, expected 20")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Metadata stripped (0.25 points)
    # Task requires removing embedded metadata. Check that title, author, subject,
    # keywords, creator, producer are all empty or missing.
    try:
        meta = comp_doc.metadata
        metadata_fields = ['title', 'author', 'subject', 'keywords', 'creator', 'producer']
        non_empty = []
        for field in metadata_fields:
            val = meta.get(field, '')
            if val and val.strip():
                non_empty.append(f"{field}='{val}'")

        if len(non_empty) == 0:
            print(f"PASS: Component 3 — All metadata fields stripped (0.25 pts)")
            total_score += 0.25
        elif len(non_empty) <= 2:
            print(f"PARTIAL: Component 3 — Some metadata remains: {non_empty} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Metadata not stripped: {non_empty}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Images compressed (0.20 points)
    # Check that images in the compressed PDF have smaller pixel dimensions
    # than in the original, indicating DPI reduction / image compression.
    try:
        # Sample first page images from both documents
        orig_page = orig_doc[0]
        comp_page = comp_doc[0]

        orig_images = orig_page.get_images(full=True)
        comp_images = comp_page.get_images(full=True)

        if len(comp_images) == 0 and len(orig_images) > 0:
            # Images removed entirely — acceptable form of compression
            print(f"PASS: Component 4 — Images removed from compressed PDF (aggressive compression) (0.20 pts)")
            total_score += 0.20
        elif len(orig_images) > 0 and len(comp_images) > 0:
            # Compare largest image dimensions
            orig_max_pixels = 0
            for img in orig_images:
                xref = img[0]
                try:
                    pix = fitz.Pixmap(orig_doc, xref)
                    pixels = pix.width * pix.height
                    if pixels > orig_max_pixels:
                        orig_max_pixels = pixels
                    pix = None
                except:
                    pass

            comp_max_pixels = 0
            for img in comp_images:
                xref = img[0]
                try:
                    pix = fitz.Pixmap(comp_doc, xref)
                    pixels = pix.width * pix.height
                    if pixels > comp_max_pixels:
                        comp_max_pixels = pixels
                    pix = None
                except:
                    pass

            if orig_max_pixels > 0 and comp_max_pixels < orig_max_pixels:
                print(f"PASS: Component 4 — Images compressed (orig max {orig_max_pixels}px, comp max {comp_max_pixels}px) (0.20 pts)")
                total_score += 0.20
            elif orig_max_pixels > 0 and comp_max_pixels == orig_max_pixels:
                print(f"FAIL: Component 4 — Image dimensions unchanged (orig max {orig_max_pixels}px, comp max {comp_max_pixels}px)")
            else:
                # Cannot determine — give benefit of doubt if file is much smaller
                if comp_size < orig_size * 0.5:
                    print(f"PASS: Component 4 — Cannot compare images directly but file significantly smaller (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — Cannot determine image compression")
        else:
            # No images in original, or same count — check overall compression as proxy
            if comp_size < orig_size * 0.5:
                print(f"PASS: Component 4 — No images to compare but file significantly compressed (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — No images to compare and file not significantly compressed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    orig_doc.close()
    comp_doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
