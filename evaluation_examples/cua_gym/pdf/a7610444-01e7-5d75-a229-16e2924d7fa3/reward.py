"""
Reward Script: Create a two-up (2 pages per sheet) version of a PDF
Task ID: pdf_res_058
Domain: pdf
Scoring:
  Component 1 (0.3): Output PDF has exactly 6 pages (12 source / 2)
  Component 2 (0.3): All output pages are landscape orientation (width > height)
  Component 3 (0.4): Content from all 12 source pages is preserved in output
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_058'

SOURCE_PATH = f'{WORKDIR}/papers/printable_paper.pdf'
OUTPUT_PATH = f'{WORKDIR}/papers/printable_paper_2up.pdf'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import fitz  # PyMuPDF

    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: output file must be a valid PDF
    try:
        out_doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: source file must exist and be readable
    try:
        src_doc = fitz.open(SOURCE_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open source PDF: {e}")
        out_doc.close()
        print("REWARD: 0.0")
        return 0.0

    src_page_count = src_doc.page_count
    out_page_count = out_doc.page_count

    # Component 1: Output has exactly 6 pages (12 source pages / 2) (0.3 points)
    try:
        expected_pages = src_page_count // 2
        if src_page_count % 2 != 0:
            expected_pages += 1  # round up for odd source pages

        if out_page_count == expected_pages:
            print(f"PASS: Component 1 -- Output has {out_page_count} pages (expected {expected_pages}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- Output has {out_page_count} pages, expected {expected_pages}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All output pages are landscape orientation (width > height) (0.3 points)
    try:
        landscape_count = 0
        for i in range(out_page_count):
            page = out_doc[i]
            w = page.rect.width
            h = page.rect.height
            if w > h:
                landscape_count += 1
            else:
                print(f"  Page {i}: portrait ({w:.1f}x{h:.1f}), expected landscape")

        if out_page_count > 0 and landscape_count == out_page_count:
            print(f"PASS: Component 2 -- All {out_page_count} output pages are landscape (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- {landscape_count}/{out_page_count} pages are landscape")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Content from all 12 source pages preserved in output (0.4 points)
    # Extract a text snippet from each source page, then check it appears in the output
    try:
        # Get representative text from each source page
        src_snippets = []
        for i in range(src_page_count):
            text = src_doc[i].get_text().strip()
            # Take first meaningful line (skip blanks)
            lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 15]
            if lines:
                src_snippets.append((i, lines[0][:60]))
            else:
                src_snippets.append((i, text[:60] if text else ""))

        # Get all text from output PDF
        out_full_text = ""
        for i in range(out_page_count):
            out_full_text += out_doc[i].get_text() + "\n"

        # Check how many source page snippets are found in output
        found_count = 0
        for page_idx, snippet in src_snippets:
            if snippet and snippet in out_full_text:
                found_count += 1
            elif snippet:
                # Try a shorter snippet for robustness
                short_snippet = snippet[:30]
                if short_snippet in out_full_text:
                    found_count += 1
                else:
                    print(f"  Source page {page_idx} snippet not found: '{snippet[:40]}...'")

        if src_page_count > 0:
            content_ratio = found_count / src_page_count
            if content_ratio >= 0.9:
                print(f"PASS: Component 3 -- {found_count}/{src_page_count} source page contents found in output (0.4 pts)")
                total_score += 0.4
            elif content_ratio >= 0.5:
                partial = round(0.4 * content_ratio, 2)
                print(f"PARTIAL: Component 3 -- {found_count}/{src_page_count} source pages found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- Only {found_count}/{src_page_count} source page contents found")
        else:
            print(f"FAIL: Component 3 -- Source has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    src_doc.close()
    out_doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
