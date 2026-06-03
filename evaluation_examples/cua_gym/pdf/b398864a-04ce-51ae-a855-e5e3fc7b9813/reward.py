"""
Reward Script: Find all 'Appendix' occurrences in technical_spec.pdf and add
yellow sticky note annotations with 'Cross-reference needed here' at each.
Save as technical_spec_reviewed.pdf.

Task ID: pdf_gf2_035
Domain: pdf

Scoring:
  Component 1 (0.15): Output file exists, valid PDF, 20 pages preserved
  Component 2 (0.35): Exactly 9 Text (sticky note) annotations total
  Component 3 (0.25): All annotations have content 'Cross-reference needed here'
  Component 4 (0.15): All annotations have yellow color (stroke ~[1,1,0])
  Component 5 (0.10): Annotations appear on correct pages (matching 'Appendix' locations)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_035'

OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'technical_spec_reviewed.pdf')
SOURCE_PATH = os.path.join(WORKDIR, 'Documents', 'technical_spec.pdf')

EXPECTED_ANNOTATION_COUNT = 9
EXPECTED_PAGE_COUNT = 20
EXPECTED_CONTENT = 'Cross-reference needed here'

# Pages (0-indexed) where 'Appendix' appears in the source PDF, with counts
# Page 1: 1, Page 7: 1, Page 10: 1, Page 14: 1, Page 16: 1, Page 17: 3, Page 18: 1
EXPECTED_PAGES_WITH_APPENDIX = {1: 1, 7: 1, 10: 1, 14: 1, 16: 1, 17: 3, 18: 1}


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # ---- Component 1: Output file exists, valid PDF, 20 pages preserved (0.15 pts) ----
    try:
        if not os.path.exists(OUTPUT_PATH):
            print(f"FAIL: Component 1 — Output file not found: {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(OUTPUT_PATH)
        page_count = doc.page_count

        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — Valid PDF with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all Text annotations across all pages
    try:
        all_text_annots = []  # list of (page_idx, annot_info)
        for i in range(doc.page_count):
            page = doc[i]
            if page.annots():
                for annot in page.annots():
                    if annot.type[1] == 'Text':
                        all_text_annots.append({
                            'page': i,
                            'content': annot.info.get('content', ''),
                            'colors': annot.colors,
                        })
    except Exception as e:
        print(f"ERROR: Could not enumerate annotations: {e}")
        doc.close()
        print(f"REWARD: {total_score}")
        return total_score

    text_annot_count = len(all_text_annots)

    # ---- Component 2: Exactly 9 Text annotations total (0.35 pts) ----
    try:
        if text_annot_count == EXPECTED_ANNOTATION_COUNT:
            print(f"PASS: Component 2 — Found {text_annot_count} Text annotations (0.35 pts)")
            total_score += 0.35
        elif text_annot_count > 0:
            # Partial credit: proportional to how close we are
            ratio = min(text_annot_count, EXPECTED_ANNOTATION_COUNT) / EXPECTED_ANNOTATION_COUNT
            partial = round(0.35 * ratio, 3)
            print(f"PARTIAL: Component 2 — Found {text_annot_count} Text annotations, expected {EXPECTED_ANNOTATION_COUNT} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No Text annotations found, expected {EXPECTED_ANNOTATION_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: All annotations have correct content (0.25 pts) ----
    try:
        if text_annot_count == 0:
            print("FAIL: Component 3 — No annotations to check content")
        else:
            correct_content = sum(1 for a in all_text_annots if a['content'].strip() == EXPECTED_CONTENT)
            if correct_content == text_annot_count:
                print(f"PASS: Component 3 — All {correct_content} annotations have correct content (0.25 pts)")
                total_score += 0.25
            elif correct_content > 0:
                ratio = correct_content / text_annot_count
                partial = round(0.25 * ratio, 3)
                print(f"PARTIAL: Component 3 — {correct_content}/{text_annot_count} annotations have correct content ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No annotations have expected content '{EXPECTED_CONTENT}'")
                for a in all_text_annots[:3]:
                    print(f"  Found content: {repr(a['content'])}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: All annotations have yellow color (0.15 pts) ----
    try:
        if text_annot_count == 0:
            print("FAIL: Component 4 — No annotations to check color")
        else:
            yellow_count = 0
            for a in all_text_annots:
                stroke = a['colors'].get('stroke', [])
                if stroke and len(stroke) >= 3:
                    # Yellow = (1.0, 1.0, 0.0) with tolerance
                    if (abs(stroke[0] - 1.0) < 0.1 and
                        abs(stroke[1] - 1.0) < 0.1 and
                        abs(stroke[2] - 0.0) < 0.1):
                        yellow_count += 1

            if yellow_count == text_annot_count:
                print(f"PASS: Component 4 — All {yellow_count} annotations have yellow color (0.15 pts)")
                total_score += 0.15
            elif yellow_count > 0:
                ratio = yellow_count / text_annot_count
                partial = round(0.15 * ratio, 3)
                print(f"PARTIAL: Component 4 — {yellow_count}/{text_annot_count} annotations are yellow ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 4 — No annotations have yellow color")
                for a in all_text_annots[:3]:
                    print(f"  Found stroke color: {a['colors'].get('stroke', 'N/A')}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: Annotations on correct pages (0.10 pts) ----
    try:
        if text_annot_count == 0:
            print("FAIL: Component 5 — No annotations to check page locations")
        else:
            # Count annotations per page
            annot_page_counts = {}
            for a in all_text_annots:
                p = a['page']
                annot_page_counts[p] = annot_page_counts.get(p, 0) + 1

            # Check match with expected pages
            matching_pages = 0
            total_expected_pages = len(EXPECTED_PAGES_WITH_APPENDIX)
            for page_idx, expected_count in EXPECTED_PAGES_WITH_APPENDIX.items():
                if annot_page_counts.get(page_idx, 0) == expected_count:
                    matching_pages += 1

            if matching_pages == total_expected_pages:
                print(f"PASS: Component 5 — Annotations on all correct pages with correct counts (0.10 pts)")
                total_score += 0.10
            elif matching_pages > 0:
                ratio = matching_pages / total_expected_pages
                partial = round(0.10 * ratio, 3)
                print(f"PARTIAL: Component 5 — {matching_pages}/{total_expected_pages} pages match expected annotation counts ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Annotation page distribution does not match")
                print(f"  Expected: {EXPECTED_PAGES_WITH_APPENDIX}")
                print(f"  Found: {annot_page_counts}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
