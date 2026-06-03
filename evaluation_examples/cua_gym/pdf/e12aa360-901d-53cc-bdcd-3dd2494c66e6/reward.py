"""
Reward Script: Merge three contract PDFs and add sequential page numbers
Task ID: pdf_pw_001
Domain: pdf
Scoring:
  Component 1 (0.25): full_contract.pdf exists with exactly 11 pages
  Component 2 (0.35): Content from source PDFs preserved in correct order
  Component 3 (0.40): Every page has centered "Page N" text at the bottom
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_001'

MERGED_PATH = os.path.join(WORKDIR, 'legal', 'full_contract.pdf')
SOURCE_DIR = os.path.join(WORKDIR, 'legal')
SOURCE_FILES = ['scope_of_work.pdf', 'terms_conditions.pdf', 'signature_page.pdf']
# Expected page counts per source
SOURCE_PAGES = [4, 6, 1]
TOTAL_PAGES = 11


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------
    # Component 1: full_contract.pdf exists with exactly 11 pages (0.25)
    # -----------------------------------------------------------------
    try:
        if not os.path.exists(MERGED_PATH):
            print(f"FAIL: Component 1 — {MERGED_PATH} does not exist")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(MERGED_PATH)
        page_count = doc.page_count

        if page_count == TOTAL_PAGES:
            print(f"PASS: Component 1 — full_contract.pdf has {page_count} pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected {TOTAL_PAGES} pages, found {page_count}")
            doc.close()
            # Still continue to check other components even if page count is wrong
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------
    # Component 2: Content preserved from source PDFs in correct order (0.35)
    # Pages 1-4 from scope_of_work, 5-10 from terms_conditions, 11 from signature_page
    # -----------------------------------------------------------------
    try:
        # Load source PDFs to extract reference text
        source_texts = []
        for src_file in SOURCE_FILES:
            src_path = os.path.join(SOURCE_DIR, src_file)
            if os.path.exists(src_path):
                src_doc = pymupdf.open(src_path)
                for pg in src_doc:
                    source_texts.append(pg.get_text("text").strip())
                src_doc.close()
            else:
                print(f"WARN: Source file {src_file} not found, skipping content check")
                source_texts.append("")

        # Compare merged pages with source pages
        matched_pages = 0
        total_source_pages = len(source_texts)
        merged_page_count = min(doc.page_count, total_source_pages)

        for i in range(merged_page_count):
            merged_text = doc[i].get_text("text").strip()
            # The merged page may have an extra "Page N" line; remove it for comparison
            # Remove the last line if it matches "Page N"
            merged_lines = merged_text.split('\n')
            # Filter out page number lines for comparison
            cleaned_lines = [l for l in merged_lines if not (l.strip().startswith('Page ') and l.strip()[5:].isdigit())]
            cleaned_merged = '\n'.join(cleaned_lines).strip()

            source_text = source_texts[i].strip()

            # Check if the source content is present in the merged page
            # Use a substring check: source text should appear in the merged text
            if source_text and source_text in cleaned_merged:
                matched_pages += 1
            elif source_text:
                # Try a more lenient check: compare first 200 chars
                if len(source_text) > 50 and source_text[:200] in cleaned_merged[:300]:
                    matched_pages += 1
                else:
                    print(f"  Page {i+1}: content mismatch (first 80 chars: src='{source_text[:80]}' merged='{cleaned_merged[:80]}')")

        if total_source_pages > 0:
            content_ratio = matched_pages / total_source_pages
        else:
            content_ratio = 0.0

        if content_ratio >= 0.9:
            print(f"PASS: Component 2 — {matched_pages}/{total_source_pages} pages matched source content (0.35 pts)")
            total_score += 0.35
        elif content_ratio >= 0.5:
            partial = round(0.35 * content_ratio, 2)
            print(f"PARTIAL: Component 2 — {matched_pages}/{total_source_pages} pages matched ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — only {matched_pages}/{total_source_pages} pages matched source content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------
    # Component 3: Every page has "Page N" centered at the bottom (0.40)
    # -----------------------------------------------------------------
    try:
        pages_with_correct_number = 0
        actual_page_count = doc.page_count

        for i in range(actual_page_count):
            page = doc[i]
            page_height = page.rect.height
            page_width = page.rect.width
            expected_text = f"Page {i + 1}"

            # Search for the expected page number text on this page
            instances = page.search_for(expected_text)

            found_at_bottom_center = False
            for inst in instances:
                # Check if instance is near bottom of page (within bottom 80pt)
                if inst.y0 > page_height - 80:
                    # Check if it's roughly centered (center of text within middle 40% of page)
                    text_center_x = (inst.x0 + inst.x1) / 2
                    page_center_x = page_width / 2
                    if abs(text_center_x - page_center_x) < page_width * 0.2:
                        found_at_bottom_center = True
                        break

            if found_at_bottom_center:
                pages_with_correct_number += 1
            else:
                print(f"  Page {i+1}: missing or misplaced page number '{expected_text}'")

        if actual_page_count > 0:
            number_ratio = pages_with_correct_number / actual_page_count
        else:
            number_ratio = 0.0

        if number_ratio == 1.0:
            print(f"PASS: Component 3 — all {actual_page_count} pages have correct centered bottom page numbers (0.40 pts)")
            total_score += 0.40
        elif number_ratio > 0:
            partial = round(0.40 * number_ratio, 2)
            print(f"PARTIAL: Component 3 — {pages_with_correct_number}/{actual_page_count} pages have correct numbers ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no pages have correct centered bottom page numbers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(MERGED_PATH):
    print(f"File not found: {MERGED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
