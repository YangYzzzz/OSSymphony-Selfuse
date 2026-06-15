"""
Reward Script: Verify stamp annotations on invoice PDF
Task ID: pdf_ro_045
Domain: pdf
Scoring:
  - Component 1 (0.25): "PAID" stamp on page 1 - green, ~24pt, bold, near (400, 100)
  - Component 2 (0.30): "VOID" stamp on page 2 - red, ~48pt, bold, near center, rotated
  - Component 3 (0.30): "COPY" stamp on all 3 pages - gray, ~14pt, near (450, 750)
  - Component 4 (0.15): Document integrity - 3 pages, original content preserved
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_045'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'invoice_stamped.pdf')


def get_stamp_spans(page, stamp_text):
    """Find all text spans matching stamp_text exactly, return list of span dicts."""
    results = []
    data = page.get_text('dict')
    for block in data.get('blocks', []):
        if block.get('type', -1) != 0:
            continue
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                if span.get('text', '').strip() == stamp_text:
                    results.append(span)
    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: "PAID" stamp on page 0 - green, ~24pt, bold (0.25 points)
    try:
        if page_count >= 1:
            page0 = doc[0]
            paid_spans = get_stamp_spans(page0, 'PAID')
            if len(paid_spans) >= 1:
                span = paid_spans[0]
                c = span.get('color', 0)
                rgb = ((c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)
                sz = span.get('size', 0)
                flags = span.get('flags', 0)
                is_bold = bool(flags & 16)
                bbox = span.get('bbox', (0, 0, 0, 0))

                sub_score = 0.0
                # Check green color: expect (0, ~170, 0) with tolerance
                if rgb[0] <= 30 and rgb[1] >= 100 and rgb[2] <= 30:
                    sub_score += 0.08
                    print(f"PASS: PAID color is green {rgb}")
                else:
                    print(f"FAIL: PAID color expected green, got {rgb}")

                # Check font size ~24pt (tolerance +/- 2)
                if abs(sz - 24.0) <= 2.0:
                    sub_score += 0.06
                    print(f"PASS: PAID size is {sz}pt (expected ~24)")
                else:
                    print(f"FAIL: PAID size expected ~24pt, got {sz}")

                # Check bold
                if is_bold:
                    sub_score += 0.05
                    print(f"PASS: PAID is bold (flags={flags})")
                else:
                    print(f"FAIL: PAID expected bold, flags={flags}")

                # Check position: near (400, 100) with tolerance
                # bbox = (x0, y0, x1, y1); origin point should be near (400, 100)
                bx = bbox[0]
                by = bbox[1]
                if abs(bx - 400) <= 50 and by <= 200:
                    sub_score += 0.06
                    print(f"PASS: PAID position bbox starts at ({bx:.0f}, {by:.0f})")
                else:
                    print(f"FAIL: PAID position expected near (400, 100), bbox starts at ({bx:.0f}, {by:.0f})")

                if sub_score > 0:
                    total_score += sub_score
                print(f"  Component 1 subtotal: {sub_score}/0.25")
            else:
                print(f"FAIL: Component 1 - 'PAID' text not found on page 0")
        else:
            print(f"FAIL: Component 1 - document has no pages")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: "VOID" stamp on page 1 - red, ~48pt, bold, near center (0.30 points)
    try:
        if page_count >= 2:
            page1 = doc[1]
            void_spans = get_stamp_spans(page1, 'VOID')
            if len(void_spans) >= 1:
                span = void_spans[0]
                c = span.get('color', 0)
                rgb = ((c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)
                sz = span.get('size', 0)
                flags = span.get('flags', 0)
                is_bold = bool(flags & 16)
                bbox = span.get('bbox', (0, 0, 0, 0))

                sub_score = 0.0
                # Check red color: expect (255, 0, 0) with tolerance
                if rgb[0] >= 200 and rgb[1] <= 50 and rgb[2] <= 50:
                    sub_score += 0.08
                    print(f"PASS: VOID color is red {rgb}")
                else:
                    print(f"FAIL: VOID color expected red, got {rgb}")

                # Check font size ~48pt (tolerance +/- 3)
                if abs(sz - 48.0) <= 3.0:
                    sub_score += 0.07
                    print(f"PASS: VOID size is {sz}pt (expected ~48)")
                else:
                    print(f"FAIL: VOID size expected ~48pt, got {sz}")

                # Check bold
                if is_bold:
                    sub_score += 0.05
                    print(f"PASS: VOID is bold (flags={flags})")
                else:
                    print(f"FAIL: VOID expected bold, flags={flags}")

                # Check near center of page 2 (Letter: 612x792)
                # bbox center should be in the general center area
                bcx = (bbox[0] + bbox[2]) / 2
                bcy = (bbox[1] + bbox[3]) / 2
                page_w = page1.rect.width
                page_h = page1.rect.height
                # Center tolerance: within 30% of page dimensions from center
                if (abs(bcx - page_w / 2) < page_w * 0.35 and
                        abs(bcy - page_h / 2) < page_h * 0.35):
                    sub_score += 0.05
                    print(f"PASS: VOID near center, bbox center=({bcx:.0f}, {bcy:.0f}), page=({page_w:.0f}x{page_h:.0f})")
                else:
                    print(f"FAIL: VOID expected near center, bbox center=({bcx:.0f}, {bcy:.0f})")

                # Check rotation: the bbox should be wider/taller than normal text
                # because 30-deg rotation stretches the bounding box.
                # A non-rotated "VOID" at 48pt would be ~140px wide and ~35px tall.
                # A 30-deg rotated "VOID" bbox should be significantly taller.
                bw = bbox[2] - bbox[0]
                bh = bbox[3] - bbox[1]
                aspect = bh / bw if bw > 0 else 0
                # Rotated text at 30 deg: bbox aspect should be >0.5 (non-rotated ~0.25)
                if bh > 50:
                    sub_score += 0.05
                    print(f"PASS: VOID appears rotated (bbox {bw:.0f}x{bh:.0f}, aspect={aspect:.2f})")
                else:
                    print(f"FAIL: VOID does not appear rotated (bbox {bw:.0f}x{bh:.0f})")

                if sub_score > 0:
                    total_score += sub_score
                print(f"  Component 2 subtotal: {sub_score}/0.30")
            else:
                print(f"FAIL: Component 2 - 'VOID' text not found on page 1")
        else:
            print(f"FAIL: Component 2 - document has fewer than 2 pages")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: "COPY" stamp on ALL 3 pages - gray, ~14pt (0.30 points)
    try:
        copy_found_pages = 0
        copy_color_ok = 0
        copy_size_ok = 0
        copy_pos_ok = 0

        for pg_idx in range(min(page_count, 3)):
            page = doc[pg_idx]
            copy_spans = get_stamp_spans(page, 'COPY')
            if len(copy_spans) >= 1:
                copy_found_pages += 1
                span = copy_spans[0]
                c = span.get('color', 0)
                rgb = ((c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)
                sz = span.get('size', 0)
                bbox = span.get('bbox', (0, 0, 0, 0))

                # Check gray color: R ~= G ~= B, around 128
                if (abs(rgb[0] - rgb[1]) <= 20 and abs(rgb[1] - rgb[2]) <= 20 and
                        60 <= rgb[0] <= 200):
                    copy_color_ok += 1

                # Check size ~14pt
                if abs(sz - 14.0) <= 2.0:
                    copy_size_ok += 1

                # Check position near (450, 750)
                bx = bbox[0]
                by = bbox[1]
                if abs(bx - 450) <= 60 and abs(by - 735) <= 60:
                    copy_pos_ok += 1

        sub_score = 0.0

        # COPY on all 3 pages (0.15 points)
        if copy_found_pages == 3:
            sub_score += 0.15
            print(f"PASS: COPY found on all 3 pages")
        elif copy_found_pages > 0:
            partial = 0.15 * (copy_found_pages / 3)
            sub_score += partial
            print(f"PARTIAL: COPY found on {copy_found_pages}/3 pages ({partial:.3f} pts)")
        else:
            print(f"FAIL: COPY not found on any page")

        # COPY color correct on all pages (0.08 points)
        if copy_found_pages > 0 and copy_color_ok == copy_found_pages:
            sub_score += 0.08
            print(f"PASS: COPY color is gray on all {copy_color_ok} pages")
        elif copy_color_ok > 0:
            print(f"PARTIAL: COPY color correct on {copy_color_ok}/{copy_found_pages} pages")
        else:
            print(f"FAIL: COPY color not gray")

        # COPY size correct (0.04 points)
        if copy_found_pages > 0 and copy_size_ok == copy_found_pages:
            sub_score += 0.04
            print(f"PASS: COPY size is ~14pt on all pages")
        else:
            print(f"FAIL: COPY size not ~14pt on all pages ({copy_size_ok}/{copy_found_pages})")

        # COPY position correct (0.03 points)
        if copy_found_pages > 0 and copy_pos_ok == copy_found_pages:
            sub_score += 0.03
            print(f"PASS: COPY position near (450, 750) on all pages")
        else:
            print(f"FAIL: COPY position not near (450, 750) ({copy_pos_ok}/{copy_found_pages})")

        if sub_score > 0:
            total_score += sub_score
        print(f"  Component 3 subtotal: {sub_score}/0.30")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Document integrity - 3 pages and original content (0.15 points)
    try:
        sub_score = 0.0

        # Check page count is still 3
        if page_count == 3:
            sub_score += 0.05
            print(f"PASS: Page count is 3")
        else:
            print(f"FAIL: Expected 3 pages, got {page_count}")

        # Check original invoice content preserved on page 0
        page0_text = doc[0].get_text('text')
        if 'INVOICE' in page0_text and 'INV-2025' in page0_text:
            sub_score += 0.05
            print(f"PASS: Original invoice content preserved on page 0")
        else:
            print(f"FAIL: Original invoice content missing on page 0")

        # Check original content preserved on other pages
        page2_text = doc[2].get_text('text') if page_count >= 3 else ''
        if len(page2_text.strip()) > 50:
            sub_score += 0.05
            print(f"PASS: Page 2 has content (original preserved)")
        else:
            print(f"FAIL: Page 2 appears empty or too short")

        if sub_score > 0:
            total_score += sub_score
        print(f"  Component 4 subtotal: {sub_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
