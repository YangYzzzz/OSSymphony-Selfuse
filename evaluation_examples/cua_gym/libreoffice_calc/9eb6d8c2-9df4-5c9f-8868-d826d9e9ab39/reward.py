"""
Reward Script: Two-up page layout from handout.pdf
Task ID: pdf_gf2_046
Domain: pdf (libreoffice_calc listed but actual domain is PDF manipulation)
Scoring:
  Component 1: Page count == 6                         (0.25 pts)
  Component 2: All pages are landscape Letter 792x612  (0.25 pts)
  Component 3: Content pairing correct                 (0.35 pts)
  Component 4: All source content preserved            (0.15 pts)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_046'
SOURCE_PATH = f'{WORKDIR}/Documents/handout.pdf'
RESULT_PATH = f'{WORKDIR}/Documents/handout_2up.pdf'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: result file must exist
    if not os.path.exists(RESULT_PATH):
        print(f"CRITICAL: Result file not found: {RESULT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: source file must exist (needed for content verification)
    if not os.path.exists(SOURCE_PATH):
        print(f"CRITICAL: Source file not found: {SOURCE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        result_doc = pymupdf.open(RESULT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open result PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        source_doc = pymupdf.open(SOURCE_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open source PDF: {e}")
        result_doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count == 6 (0.25 points)
    # Source has 12 pages, 2-up layout means 12/2 = 6 result pages
    try:
        result_page_count = result_doc.page_count
        if result_page_count == 6:
            print(f"PASS: Component 1 - Page count is 6 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - Expected 6 pages, found {result_page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All pages are landscape Letter (792x612) (0.25 points)
    # Landscape Letter: width=792, height=612
    try:
        landscape_count = 0
        tolerance = 2.0  # allow small rounding differences
        for i in range(result_doc.page_count):
            page = result_doc[i]
            w, h = page.rect.width, page.rect.height
            if abs(w - 792.0) <= tolerance and abs(h - 612.0) <= tolerance:
                landscape_count += 1
            else:
                print(f"FAIL: Component 2 - Page {i} is {w}x{h}, expected 792x612")
        if landscape_count == result_doc.page_count and result_doc.page_count > 0:
            print(f"PASS: Component 2 - All {landscape_count} pages are landscape Letter 792x612 (0.25 pts)")
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Content pairing correct (0.35 points)
    # Each 2up page should contain text from two consecutive source pages:
    # 2up page 0 = source pages 0,1; 2up page 1 = source pages 2,3; etc.
    try:
        # Extract a unique text snippet from each source page
        source_snippets = []
        for i in range(source_doc.page_count):
            text = source_doc[i].get_text("text").strip()
            # Get first meaningful line (skip very short lines)
            lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 15]
            snippet = lines[0] if lines else text[:50]
            source_snippets.append(snippet)
            print(f"  Source page {i} snippet: '{snippet[:60]}...'")

        pairing_score = 0.0
        num_pairs = min(result_doc.page_count, 6)
        points_per_pair = 0.35 / 6.0

        for pair_idx in range(num_pairs):
            result_text = result_doc[pair_idx].get_text("text")
            src_left = pair_idx * 2      # odd source page (1-indexed: pages 1,3,5,...)
            src_right = pair_idx * 2 + 1  # even source page (1-indexed: pages 2,4,6,...)

            left_found = False
            right_found = False

            if src_left < len(source_snippets):
                left_found = source_snippets[src_left] in result_text
            if src_right < len(source_snippets):
                right_found = source_snippets[src_right] in result_text

            if left_found and right_found:
                print(f"  Pair {pair_idx}: Both source pages {src_left}&{src_right} found - PASS")
                pairing_score += points_per_pair
            elif left_found or right_found:
                found_side = "left" if left_found else "right"
                print(f"  Pair {pair_idx}: Only {found_side} source page found - PARTIAL")
                pairing_score += points_per_pair * 0.5
            else:
                print(f"  Pair {pair_idx}: Neither source page {src_left} nor {src_right} found - FAIL")

        if pairing_score > 0:
            total_score += round(pairing_score, 4)
            print(f"PASS: Component 3 - Content pairing score: {pairing_score:.4f}/0.35")
        else:
            print(f"FAIL: Component 3 - No correct content pairings found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: All source content preserved (0.15 points)
    # Verify that text from all 12 source pages appears somewhere in the result
    try:
        # Get all text from result document
        all_result_text = ""
        for i in range(result_doc.page_count):
            all_result_text += result_doc[i].get_text("text")

        pages_found = 0
        for i in range(source_doc.page_count):
            src_text = source_doc[i].get_text("text").strip()
            # Use first significant line as fingerprint
            lines = [l.strip() for l in src_text.split('\n') if len(l.strip()) > 15]
            if lines and lines[0] in all_result_text:
                pages_found += 1
            elif not lines:
                # If no significant lines, count as found (empty page)
                pages_found += 1

        completeness = pages_found / source_doc.page_count
        comp4_score = 0.15 * completeness
        if comp4_score > 0:
            total_score += round(comp4_score, 4)
        if completeness >= 1.0:
            print(f"PASS: Component 4 - All {source_doc.page_count} source pages preserved (0.15 pts)")
        else:
            print(f"PARTIAL: Component 4 - {pages_found}/{source_doc.page_count} source pages found ({comp4_score:.4f}/0.15 pts)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    source_doc.close()
    result_doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
