"""
Reward Script: Add hyperlink bookmarks for appendix references and export as PDF
Task ID: pdf_cross_022
Domain: pdf (cross-domain: LibreOffice Writer + PDF export)
Scoring:
  Component 1: PDF file exists at ~/Documents/reference_doc_linked.pdf (0.2 pts)
  Component 2: PDF has correct page count (15 pages) (0.2 pts)
  Component 3: PDF has Appendix TOC/bookmark entries for all 4 appendices (0.3 pts)
  Component 4: PDF has internal hyperlinks from body pages pointing to appendix pages (0.3 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_022'

PDF_PATH = os.path.join(WORKDIR, 'reference_doc_linked.pdf')

# First check if the PDF output file exists; if not, we can return early without needing pymupdf
if not os.path.exists(PDF_PATH):
    print("File not found: %s" % PDF_PATH)
    print("REWARD: 0.0")
    raise SystemExit(0)

# pymupdf is the primary library for PDF verification
try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print("CRITICAL: Cannot import pymupdf or fitz")
        print("REWARD: 0.0")
        raise SystemExit(0)

# Expected values derived from task description:
# - 15-page document with 4 appendices (A, B, C, D on pages 10, 12, 13, 14)
# - 8 references to appendices in body text
EXPECTED_PAGE_COUNT = 15
# Appendix pages (1-indexed): Appendix A=10, B=12, C=13, D=14
# (0-indexed): 9, 11, 12, 13
APPENDIX_PAGES_0IDX = {9, 11, 12, 13}
APPENDIX_NAMES = ['Appendix A', 'Appendix B', 'Appendix C', 'Appendix D']
MIN_INTERNAL_LINKS = 4  # at least 4 of the 8 references should be linked


def verify_task(pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF output file exists at expected path (0.2 points)
    # This FAILS on initial_env (only .odt exists, no PDF) -> PASSES on golden_env
    try:
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            print("PASS: Component 1 - PDF file reference_doc_linked.pdf exists (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 - PDF file reference_doc_linked.pdf not found or empty")
            # Cannot proceed with PDF checks
            print("\nScore: %.1f/1.0" % total_score)
            print("REWARD: %.1f" % total_score)
            return total_score
    except Exception as e:
        print("ERROR: Component 1 - %s" % e)
        print("\nScore: %.1f/1.0" % total_score)
        print("REWARD: %.1f" % total_score)
        return total_score

    # Load the PDF for subsequent checks
    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print("CRITICAL: Cannot open PDF %s: %s" % (pdf_path, e))
        print("\nScore: %.1f/1.0" % total_score)
        print("REWARD: %.1f" % total_score)
        return total_score

    # Component 2: PDF has the correct page count (15 pages) (0.2 points)
    # A truncated or malformed export would fail this check.
    # FAILS on initial (no PDF) -> PASSES on golden (15 pages)
    try:
        actual_pages = doc.page_count
        if actual_pages == EXPECTED_PAGE_COUNT:
            print("PASS: Component 2 - PDF has %d pages as expected (0.2 pts)" % actual_pages)
            total_score += 0.2
        else:
            print("FAIL: Component 2 - Expected %d pages, found %d pages" % (EXPECTED_PAGE_COUNT, actual_pages))
    except Exception as e:
        print("ERROR: Component 2 - %s" % e)

    # Component 3: PDF has Appendix bookmark/TOC entries for all 4 appendices (0.3 points)
    # The internal bookmarks (TOC) must be preserved in the PDF as required by the task.
    # FAILS on initial (no PDF) -> PASSES on golden (4 Appendix entries in TOC)
    try:
        toc = doc.get_toc()
        found_appendices = set()
        for level, title, page in toc:
            for app_name in APPENDIX_NAMES:
                if app_name in title:
                    found_appendices.add(app_name)

        if len(found_appendices) == len(APPENDIX_NAMES):
            print("PASS: Component 3 - PDF TOC contains all 4 Appendix entries %s (0.3 pts)" % sorted(found_appendices))
            total_score += 0.3
        elif len(found_appendices) >= 2:
            # Partial credit: at least half the appendices are bookmarked
            print("PARTIAL: Component 3 - Found %d/4 Appendix TOC entries: %s (0.15 pts)" % (len(found_appendices), sorted(found_appendices)))
            total_score += 0.15
        else:
            print("FAIL: Component 3 - Expected 4 Appendix TOC entries, found %d: %s" % (len(found_appendices), sorted(found_appendices)))
    except Exception as e:
        print("ERROR: Component 3 - %s" % e)

    # Component 4: PDF has internal hyperlinks from body pages pointing to appendix pages (0.3 points)
    # The task requires adding hyperlink bookmarks for each appendix reference found in body text.
    # Links should be GOTO links (kind=1) pointing to the appendix pages.
    # FAILS on initial (no PDF) -> PASSES on golden (7 internal links to appendix pages)
    try:
        internal_goto_links = 0
        links_to_appendix_pages = 0

        for page_num in range(doc.page_count):
            links = doc[page_num].get_links()
            for lnk in links:
                if lnk.get('kind') == 1:  # LINK_GOTO = internal link
                    internal_goto_links += 1
                    target_page = lnk.get('page', -1)
                    if target_page in APPENDIX_PAGES_0IDX:
                        links_to_appendix_pages += 1

        print("INFO: Found %d internal GOTO links total, %d pointing to appendix pages" % (internal_goto_links, links_to_appendix_pages))

        if links_to_appendix_pages >= MIN_INTERNAL_LINKS:
            print("PASS: Component 4 - PDF has %d internal links pointing to appendix pages (>= %d required) (0.3 pts)" % (links_to_appendix_pages, MIN_INTERNAL_LINKS))
            total_score += 0.3
        elif links_to_appendix_pages >= 2:
            # Partial credit: some but not all appendix references are linked
            print("PARTIAL: Component 4 - Found %d internal links to appendix pages (need %d) (0.15 pts)" % (links_to_appendix_pages, MIN_INTERNAL_LINKS))
            total_score += 0.15
        else:
            print("FAIL: Component 4 - Expected >= %d internal links to appendix pages, found %d" % (MIN_INTERNAL_LINKS, links_to_appendix_pages))
    except Exception as e:
        print("ERROR: Component 4 - %s" % e)

    doc.close()

    final_score = min(total_score, 1.0)
    print("\nScore: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


verify_task(PDF_PATH)
