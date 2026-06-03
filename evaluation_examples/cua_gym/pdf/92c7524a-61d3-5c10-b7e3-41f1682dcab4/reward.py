"""
Reward Script: Redact signature blocks on pages 4, 6, 8 with white fill
Task ID: pdf_gf2_029
Domain: pdf
Scoring:
  Component 1 (0.30): Text removed from signature regions on pages 4, 6, 8
  Component 2 (0.25): White-filled rectangles cover signature regions
  Component 3 (0.25): Pixel rendering of signature regions is white
  Component 4 (0.20): Content outside signature regions preserved on redacted pages
"""

import os

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_029'

# The task output file
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'signed_agreement_unsigned.pdf')
# The original source file (for content comparison)
SOURCE_PATH = os.path.join(WORKDIR, 'legal', 'signed_agreement.pdf')

# Signature region: (72, 650) to (540, 720) on pages 4, 6, 8 (0-indexed: 3, 5, 7)
SIG_RECT = fitz.Rect(72, 650, 540, 720)
SIG_PAGES = [3, 5, 7]  # 0-indexed


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

    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have 10 pages
    if len(doc) != 10:
        print(f"CRITICAL: Expected 10 pages, found {len(doc)}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Text removed from signature regions on pages 4, 6, 8 (0.30 points)
    # Each page contributes 0.10 points
    try:
        text_removed_count = 0
        for pn in SIG_PAGES:
            page = doc[pn]
            sig_text = page.get_textbox(SIG_RECT).strip()
            if len(sig_text) == 0:
                text_removed_count += 1
                print(f"PASS: Component 1 — Page {pn+1} signature region text is empty (0.10 pts)")
            else:
                print(f"FAIL: Component 1 — Page {pn+1} signature region still has text: [{sig_text[:60]}...]")

        comp1_score = text_removed_count * 0.10
        total_score += comp1_score
        print(f"Component 1 subtotal: {comp1_score:.2f}/0.30")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: White-filled drawings/rectangles cover signature regions (0.25 points)
    # Check that there is a white-filled drawing covering each signature region
    # Each page contributes ~0.083 points
    try:
        white_fill_count = 0
        for pn in SIG_PAGES:
            page = doc[pn]
            drawings = page.get_drawings()
            found_white_rect = False
            for d in drawings:
                d_rect = fitz.Rect(d['rect'])
                fill_color = d.get('fill')
                # Check if this drawing covers the signature region and has white fill
                if d_rect.intersects(SIG_RECT) and fill_color is not None:
                    # White fill: (1.0, 1.0, 1.0)
                    if (abs(fill_color[0] - 1.0) < 0.01 and
                        abs(fill_color[1] - 1.0) < 0.01 and
                        abs(fill_color[2] - 1.0) < 0.01):
                        found_white_rect = True
                        break

            if found_white_rect:
                white_fill_count += 1
                print(f"PASS: Component 2 — Page {pn+1} has white-filled rectangle in signature region")
            else:
                print(f"FAIL: Component 2 — Page {pn+1} missing white-filled rectangle in signature region")

        comp2_score = round(white_fill_count * (0.25 / 3), 4)
        total_score += comp2_score
        print(f"Component 2 subtotal: {comp2_score:.4f}/0.25")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pixel rendering confirms white in signature regions (0.25 points)
    # Render the signature region and check that center pixels are white (255, 255, 255)
    try:
        white_pixel_count = 0
        for pn in SIG_PAGES:
            page = doc[pn]
            pix = page.get_pixmap(clip=SIG_RECT, dpi=72)
            # Sample multiple points across the region
            sample_points = [
                (pix.width // 4, pix.height // 2),
                (pix.width // 2, pix.height // 2),
                (3 * pix.width // 4, pix.height // 2),
            ]
            all_white = True
            for sx, sy in sample_points:
                pixel = pix.pixel(sx, sy)
                # Allow near-white (250+)
                if pixel[0] < 250 or pixel[1] < 250 or pixel[2] < 250:
                    all_white = False
                    print(f"FAIL: Component 3 — Page {pn+1} pixel at ({sx},{sy}) is {pixel}, not white")
                    break

            if all_white:
                white_pixel_count += 1
                print(f"PASS: Component 3 — Page {pn+1} signature region renders as white")

        comp3_score = round(white_pixel_count * (0.25 / 3), 4)
        total_score += comp3_score
        print(f"Component 3 subtotal: {comp3_score:.4f}/0.25")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content outside signature regions preserved on redacted pages (0.20 points)
    # Compare text above the signature region with the source file
    try:
        source_doc = fitz.open(SOURCE_PATH)
        preserved_count = 0
        above_rect = fitz.Rect(0, 0, 612, 650)

        for pn in SIG_PAGES:
            source_text = source_doc[pn].get_textbox(above_rect).strip()
            output_text = doc[pn].get_textbox(above_rect).strip()

            if len(source_text) > 0 and source_text == output_text:
                preserved_count += 1
                print(f"PASS: Component 4 — Page {pn+1} non-signature content preserved ({len(output_text)} chars)")
            else:
                print(f"FAIL: Component 4 — Page {pn+1} content mismatch. Source: {len(source_text)} chars, Output: {len(output_text)} chars")

        source_doc.close()
        comp4_score = round(preserved_count * (0.20 / 3), 4)
        total_score += comp4_score
        print(f"Component 4 subtotal: {comp4_score:.4f}/0.20")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
