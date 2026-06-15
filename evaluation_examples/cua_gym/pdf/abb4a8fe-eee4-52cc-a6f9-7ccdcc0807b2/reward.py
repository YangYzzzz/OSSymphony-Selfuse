"""
Reward Script: Add running header and footer to PDF
Task ID: pdf_gf2_034
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists and has 22 pages
  - Component 2 (0.35): Footer 'Page N of 22' on every page
  - Component 3 (0.30): Header 'Project Proposal 2026' on every page
  - Component 4 (0.20): Font, size, and color correct for header/footer text
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_034'
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'proposal_final_numbered.pdf')
EXPECTED_PAGES = 22
EXPECTED_HEADER = 'Project Proposal 2026'
EXPECTED_GRAY_COLOR = 8421504  # RGB gray (128,128,128)


def get_header_footer_spans(page):
    """Extract text spans that are in header (top 40pt) or footer (below y=740) regions."""
    data = page.get_text("dict")
    header_spans = []
    footer_spans = []
    for block in data["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                bbox = span["bbox"]
                # Header region: y0 < 40 (top of page)
                if bbox[1] < 40:
                    header_spans.append(span)
                # Footer region: y0 > 740 (bottom of page, y=760 target)
                if bbox[1] > 740:
                    footer_spans.append(span)
    return header_spans, footer_spans


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
        import fitz
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_pages = len(doc)

    # Component 1: Output file has exactly 22 pages (0.15 points)
    # This checks the output file exists with correct page count.
    # The initial_env has no output file at all, so this fails on initial.
    try:
        if num_pages == EXPECTED_PAGES:
            print(f"PASS: Component 1 -- Output file has {num_pages} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGES} pages, found {num_pages}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Footer 'Page N of 22' present on every page (0.35 points)
    # Awards partial credit proportional to pages with correct footer.
    try:
        pages_with_footer = 0
        footer_pattern = re.compile(r'Page\s+(\d+)\s+of\s+22')
        for i in range(num_pages):
            page = doc[i]
            _, footer_spans = get_header_footer_spans(page)
            page_num_expected = i + 1
            for span in footer_spans:
                txt = span["text"].strip()
                m = footer_pattern.search(txt)
                if m and int(m.group(1)) == page_num_expected:
                    pages_with_footer += 1
                    break

        footer_ratio = pages_with_footer / EXPECTED_PAGES if EXPECTED_PAGES > 0 else 0
        if footer_ratio == 1.0:
            print(f"PASS: Component 2 -- Footer found on all {pages_with_footer}/{EXPECTED_PAGES} pages (0.35 pts)")
            total_score += 0.35
        elif footer_ratio > 0:
            partial = round(0.35 * footer_ratio, 4)
            print(f"PARTIAL: Component 2 -- Footer on {pages_with_footer}/{EXPECTED_PAGES} pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No correct footer found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Header 'Project Proposal 2026' on every page (0.30 points)
    # Awards partial credit proportional to pages with correct header.
    try:
        pages_with_header = 0
        for i in range(num_pages):
            page = doc[i]
            header_spans, _ = get_header_footer_spans(page)
            for span in header_spans:
                txt = span["text"].strip()
                if txt == EXPECTED_HEADER:
                    pages_with_header += 1
                    break

        header_ratio = pages_with_header / EXPECTED_PAGES if EXPECTED_PAGES > 0 else 0
        if header_ratio == 1.0:
            print(f"PASS: Component 3 -- Header found on all {pages_with_header}/{EXPECTED_PAGES} pages (0.30 pts)")
            total_score += 0.30
        elif header_ratio > 0:
            partial = round(0.30 * header_ratio, 4)
            print(f"PARTIAL: Component 3 -- Header on {pages_with_header}/{EXPECTED_PAGES} pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No correct header found on any page")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Font, size, and color correct for header/footer (0.20 points)
    # Check a sample of pages (first, middle, last) for correct styling.
    # Expects: Helvetica, 8pt, gray color (8421504).
    try:
        sample_pages = [0, num_pages // 2, num_pages - 1]
        style_checks_passed = 0
        total_style_checks = 0

        for i in sample_pages:
            if i >= num_pages:
                continue
            page = doc[i]
            header_spans, footer_spans = get_header_footer_spans(page)

            # Check footer style
            for span in footer_spans:
                if 'Page' in span["text"] and 'of' in span["text"]:
                    total_style_checks += 1
                    font_ok = 'helv' in span["font"].lower() or 'helvetica' in span["font"].lower()
                    size_ok = abs(span["size"] - 8.0) < 1.0
                    color_ok = span["color"] == EXPECTED_GRAY_COLOR or (
                        # Also accept nearby gray values
                        abs(span["color"] - EXPECTED_GRAY_COLOR) < 200000
                    )
                    if font_ok and size_ok and color_ok:
                        style_checks_passed += 1
                    else:
                        print(f"  Style issue on page {i} footer: font={span['font']}, size={span['size']}, color={span['color']}")
                    break

            # Check header style
            for span in header_spans:
                if EXPECTED_HEADER in span["text"]:
                    total_style_checks += 1
                    font_ok = 'helv' in span["font"].lower() or 'helvetica' in span["font"].lower()
                    size_ok = abs(span["size"] - 8.0) < 1.0
                    color_ok = span["color"] == EXPECTED_GRAY_COLOR or (
                        abs(span["color"] - EXPECTED_GRAY_COLOR) < 200000
                    )
                    if font_ok and size_ok and color_ok:
                        style_checks_passed += 1
                    else:
                        print(f"  Style issue on page {i} header: font={span['font']}, size={span['size']}, color={span['color']}")
                    break

        if total_style_checks > 0:
            style_ratio = style_checks_passed / total_style_checks
            if style_ratio == 1.0:
                print(f"PASS: Component 4 -- All style checks passed ({style_checks_passed}/{total_style_checks}) (0.20 pts)")
                total_score += 0.20
            elif style_ratio > 0:
                partial = round(0.20 * style_ratio, 4)
                print(f"PARTIAL: Component 4 -- {style_checks_passed}/{total_style_checks} style checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- No style checks passed")
        else:
            print(f"FAIL: Component 4 -- No header/footer spans found to check style")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
