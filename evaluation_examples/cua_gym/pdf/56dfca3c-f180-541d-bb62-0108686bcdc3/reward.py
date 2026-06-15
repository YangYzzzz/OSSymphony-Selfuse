"""
Reward Script: Convert ~/Documents/diagram.svg to PDF preserving vector graphics quality
Task ID: pdf_mbc_088
Domain: pdf
Scoring:
  - Component 1 (0.3): PDF file exists and is a valid PDF with at least 1 page
  - Component 2 (0.3): Text from SVG is selectable in the PDF
  - Component 3 (0.2): Vector graphics preserved (drawings present, not rasterized)
  - Component 4 (0.2): Reasonable file size (not a bloated raster dump)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_088'
PDF_PATH = os.path.join(WORKDIR, 'Documents', 'diagram.pdf')

# Key text elements from the SVG flowchart that should be selectable
EXPECTED_TEXTS = [
    "Software Release Process",
    "Start Release",
    "Code Review",
    "Tests Pass",
    "Fix Bugs",
    "Build Package",
    "Deploy",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists and is a valid PDF (0.3 points)
    # This is a task-introduced change: initial_env has no diagram.pdf
    try:
        import fitz  # PyMuPDF
        if not os.path.exists(PDF_PATH):
            print(f"FAIL: Component 1 — PDF file not found at {PDF_PATH}")
            print("REWARD: 0.0")
            return 0.0

        doc = fitz.open(PDF_PATH)
        page_count = doc.page_count
        if page_count >= 1:
            print(f"PASS: Component 1 — Valid PDF with {page_count} page(s) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
            doc.close()
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Text is selectable — key flowchart labels are extractable (0.3 points)
    # The SVG has text labels; a proper vector conversion should preserve them as selectable text
    try:
        page = doc[0]
        text = page.get_text().strip()
        found_count = 0
        for expected in EXPECTED_TEXTS:
            if expected.lower() in text.lower():
                found_count += 1
            else:
                print(f"  INFO: Text '{expected}' not found in PDF text")

        ratio = found_count / len(EXPECTED_TEXTS)
        if ratio >= 0.7:
            print(f"PASS: Component 2 — {found_count}/{len(EXPECTED_TEXTS)} key texts found, selectable (0.3 pts)")
            total_score += 0.3
        elif ratio >= 0.3:
            partial = round(0.3 * ratio, 2)
            print(f"PARTIAL: Component 2 — {found_count}/{len(EXPECTED_TEXTS)} key texts found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {found_count}/{len(EXPECTED_TEXTS)} key texts found in PDF")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Vector graphics preserved (0.2 points)
    # A proper SVG-to-PDF conversion preserves vector paths as drawings, not raster images
    # If the PDF has drawings and few/no embedded raster images, vectors are preserved
    try:
        page = doc[0]
        drawings = page.get_drawings()
        images = page.get_images(full=True)
        num_drawings = len(drawings)
        num_images = len(images)

        if num_drawings >= 5 and num_images == 0:
            # Many vector paths, no raster images — ideal vector conversion
            print(f"PASS: Component 3 — {num_drawings} vector drawings, {num_images} raster images (0.2 pts)")
            total_score += 0.2
        elif num_drawings >= 5 and num_images <= 2:
            # Mostly vector with a few small raster elements — acceptable
            print(f"PASS: Component 3 — {num_drawings} vector drawings, {num_images} raster images (0.2 pts)")
            total_score += 0.2
        elif num_drawings >= 1:
            # Some vector content but mixed
            print(f"PARTIAL: Component 3 — {num_drawings} drawings, {num_images} images (0.1 pts)")
            total_score += 0.1
        else:
            # No vector drawings — likely rasterized
            print(f"FAIL: Component 3 — No vector drawings found ({num_images} raster images). SVG likely rasterized.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Reasonable file size (0.2 points)
    # A vector PDF from this small SVG should be well under 1MB
    # A rasterized version would be much larger
    try:
        file_size = os.path.getsize(PDF_PATH)
        file_size_kb = file_size / 1024

        if file_size_kb < 500:
            print(f"PASS: Component 4 — File size {file_size_kb:.1f} KB, reasonable for vector PDF (0.2 pts)")
            total_score += 0.2
        elif file_size_kb < 2000:
            print(f"PARTIAL: Component 4 — File size {file_size_kb:.1f} KB, somewhat large (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — File size {file_size_kb:.1f} KB, too large — likely rasterized")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
