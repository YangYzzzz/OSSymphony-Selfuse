"""
Reward Script: Add CONFIDENTIAL watermark to NDA PDF
Task ID: pdf_gf2_004
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with correct page count (6 pages)
  Component 2 (0.35): All 6 pages have large "CONFIDENTIAL" watermark text (fontsize >= 40)
  Component 3 (0.20): Watermark color is red (close to RGB 0.8, 0, 0)
  Component 4 (0.15): Watermark is approximately centered on each page
  Component 5 (0.15): Original document text is preserved
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_004'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    output_path = f'{WORKDIR}/legal/nda_draft_watermarked.pdf'
    source_path = f'{WORKDIR}/legal/nda_draft.pdf'

    # Precondition: output file must exist
    if not os.path.exists(output_path):
        print(f"CRITICAL: Output file not found: {output_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(output_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: Output file has 6 pages (0.15 points)
    try:
        if page_count == 6:
            print(f"PASS: Component 1 -- Page count is 6 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected 6 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 6 pages have large "CONFIDENTIAL" watermark text (0.35 points)
    # The watermark must be large text (>= 40pt) distinct from the body text (~11pt)
    try:
        pages_with_watermark = 0
        for i in range(page_count):
            page = doc[i]
            data = page.get_text("dict")
            found_watermark = False
            for block in data["blocks"]:
                if block.get("type") != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if "CONFIDENTIAL" in span["text"].upper() and span["size"] >= 40:
                            found_watermark = True
                            break
                    if found_watermark:
                        break
                if found_watermark:
                    break
            if found_watermark:
                pages_with_watermark += 1

        if pages_with_watermark == page_count and page_count == 6:
            print(f"PASS: Component 2 -- All {page_count} pages have CONFIDENTIAL watermark (0.35 pts)")
            total_score += 0.35
        elif pages_with_watermark > 0:
            partial = 0.35 * (pages_with_watermark / max(page_count, 6))
            print(f"PARTIAL: Component 2 -- {pages_with_watermark}/{page_count} pages have watermark ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No pages have large CONFIDENTIAL watermark text")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Watermark color is red, close to RGB (204, 0, 0) i.e. (0.8, 0, 0) (0.20 points)
    try:
        pages_with_red = 0
        for i in range(page_count):
            page = doc[i]
            data = page.get_text("dict")
            found_red = False
            for block in data["blocks"]:
                if block.get("type") != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if "CONFIDENTIAL" in span["text"].upper() and span["size"] >= 40:
                            c = span["color"]
                            r = (c >> 16) & 0xFF
                            g = (c >> 8) & 0xFF
                            b = c & 0xFF
                            # Check if red channel is high (>= 150) and green/blue are low (<= 50)
                            if r >= 150 and g <= 50 and b <= 50:
                                found_red = True
                                print(f"  Page {i} watermark color: RGB({r},{g},{b}) -- red")
                            else:
                                print(f"  Page {i} watermark color: RGB({r},{g},{b}) -- NOT red enough")
                            break
                    if found_red:
                        break
                if found_red:
                    break
            if found_red:
                pages_with_red += 1

        if pages_with_red == page_count and page_count > 0:
            print(f"PASS: Component 3 -- All pages have red watermark (0.20 pts)")
            total_score += 0.20
        elif pages_with_red > 0:
            partial = 0.20 * (pages_with_red / page_count)
            print(f"PARTIAL: Component 3 -- {pages_with_red}/{page_count} pages have red watermark ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No pages have red-colored watermark")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Watermark is approximately centered on each page (0.15 points)
    # Page size is 612x792 (Letter). Center is at (306, 396).
    # We check that the watermark bbox center is within roughly the middle 70% of the page.
    try:
        pages_centered = 0
        for i in range(page_count):
            page = doc[i]
            pw, ph = page.rect.width, page.rect.height
            data = page.get_text("dict")
            found_centered = False
            for block in data["blocks"]:
                if block.get("type") != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if "CONFIDENTIAL" in span["text"].upper() and span["size"] >= 40:
                            bbox = span["bbox"]  # (x0, y0, x1, y1)
                            cx = (bbox[0] + bbox[2]) / 2
                            cy = (bbox[1] + bbox[3]) / 2
                            # Check center is within middle 70% of page
                            x_ok = pw * 0.15 < cx < pw * 0.85
                            y_ok = ph * 0.15 < cy < ph * 0.85
                            if x_ok and y_ok:
                                found_centered = True
                            else:
                                print(f"  Page {i} watermark center ({cx:.0f},{cy:.0f}) not centered on {pw:.0f}x{ph:.0f} page")
                            break
                    if found_centered:
                        break
                if found_centered:
                    break
            if found_centered:
                pages_centered += 1

        if pages_centered == page_count and page_count > 0:
            print(f"PASS: Component 4 -- Watermark centered on all pages (0.15 pts)")
            total_score += 0.15
        elif pages_centered > 0:
            partial = 0.15 * (pages_centered / page_count)
            print(f"PARTIAL: Component 4 -- {pages_centered}/{page_count} pages centered ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Watermark not centered")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    # Component 5: Original document text is preserved (0.15 points)
    # Check that the source NDA text is still present in the watermarked PDF
    try:
        if os.path.exists(source_path):
            src_doc = pymupdf.open(source_path)
            out_doc = pymupdf.open(output_path)

            # Sample key phrases from the NDA that must still be present
            key_phrases = [
                "NON-DISCLOSURE AGREEMENT",
                "NDA-2025-0472",
                "DEFINITIONS",
                "OBLIGATIONS OF RECEIVING PARTY",
                "GENERAL PROVISIONS",
            ]

            out_text = ""
            for page in out_doc:
                out_text += page.get_text("text")

            phrases_found = sum(1 for phrase in key_phrases if phrase in out_text)

            src_doc.close()
            out_doc.close()

            if phrases_found == len(key_phrases):
                print(f"PASS: Component 5 -- All {len(key_phrases)} key phrases preserved (0.15 pts)")
                total_score += 0.15
            elif phrases_found > 0:
                partial = 0.15 * (phrases_found / len(key_phrases))
                print(f"PARTIAL: Component 5 -- {phrases_found}/{len(key_phrases)} key phrases found ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- Original document text not preserved")
        else:
            print(f"WARN: Component 5 -- Source file not found, skipping preservation check")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
