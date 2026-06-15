"""
Reward Script: Set PDF initial view with bookmarks panel, page 1, fit width
Task ID: pdf_legal_082
Domain: pdf
Scoring:
  Component 1 (0.30): PageMode is /UseOutlines (bookmarks panel visible)
  Component 2 (0.25): OpenAction targets page 1 (index 0)
  Component 3 (0.30): OpenAction uses /FitH (fit page width to window)
  Component 4 (0.15): Document integrity (30 pages + bookmarks preserved)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_082'
OUTPUT_PATH = f'{WORKDIR}/legal/estate/trust_document_view.pdf'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PageMode is /UseOutlines (bookmarks panel visible) (0.30 points)
    try:
        if '/PageMode' in pdf.Root:
            page_mode = str(pdf.Root['/PageMode'])
            if page_mode == '/UseOutlines':
                print(f"PASS: Component 1 - PageMode is /UseOutlines (bookmarks visible) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 - PageMode is {page_mode}, expected /UseOutlines")
        else:
            print("FAIL: Component 1 - /PageMode not set in catalog")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: OpenAction targets page 1 (index 0) (0.25 points)
    try:
        if '/OpenAction' in pdf.Root:
            oa = pdf.Root['/OpenAction']
            if isinstance(oa, pikepdf.Array) and len(oa) >= 2:
                # Determine which page the OpenAction references
                target_page_obj = oa[0]
                target_page_idx = None
                for i, page in enumerate(pdf.pages):
                    if page.objgen == target_page_obj.objgen:
                        target_page_idx = i
                        break

                if target_page_idx == 0:
                    print(f"PASS: Component 2 - OpenAction targets page 1 (index 0) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 - OpenAction targets page index {target_page_idx}, expected 0")
            else:
                print(f"FAIL: Component 2 - OpenAction format unexpected: {oa}")
        else:
            print("FAIL: Component 2 - /OpenAction not set in catalog")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: OpenAction uses /FitH (fit page width to window) (0.30 points)
    try:
        if '/OpenAction' in pdf.Root:
            oa = pdf.Root['/OpenAction']
            if isinstance(oa, pikepdf.Array) and len(oa) >= 2:
                fit_type = str(oa[1])
                # /FitH and /FitBH both fit the width; /FitH is standard
                if fit_type == '/FitH':
                    print(f"PASS: Component 3 - OpenAction uses /FitH (fit width) (0.30 pts)")
                    total_score += 0.30
                elif fit_type == '/FitBH':
                    # FitBH also fits bounding box width - partial credit
                    print(f"PARTIAL: Component 3 - OpenAction uses /FitBH (bounding box width) instead of /FitH (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 - OpenAction fit type is {fit_type}, expected /FitH")
            else:
                print(f"FAIL: Component 3 - OpenAction format unexpected")
        else:
            print("FAIL: Component 3 - /OpenAction not set in catalog")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Document integrity - 30 pages and bookmarks preserved (0.15 points)
    # This is anchored to the task change: the output file must be a VALID copy with view settings,
    # not a corrupted or truncated file. We check both pages AND that bookmarks survived.
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
        toc = doc.get_toc()
        toc_count = len(toc)
        doc.close()

        pages_ok = (page_count == 30)
        bookmarks_ok = (toc_count >= 10)  # original has 12 bookmarks

        if pages_ok and bookmarks_ok:
            print(f"PASS: Component 4 - Document intact: {page_count} pages, {toc_count} bookmarks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Document integrity: {page_count} pages (expected 30), {toc_count} bookmarks (expected >= 10)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    pdf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
