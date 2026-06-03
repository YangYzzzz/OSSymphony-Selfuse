"""
Reward Script: Split tax_forms_bundle.pdf into 4 individual form PDFs
Task ID: pdf_fin_074
Domain: pdf
Scoring:
  - Component 1 (0.15): form_w2.pdf exists with correct page count (4)
  - Component 2 (0.15): form_1099.pdf exists with correct page count (2)
  - Component 3 (0.15): form_1040.pdf exists with correct page count (4)
  - Component 4 (0.15): schedule_c.pdf exists with correct page count (4)
  - Component 5 (0.10): form_w2.pdf content matches source pages 1-4
  - Component 6 (0.10): form_1099.pdf content matches source pages 5-6
  - Component 7 (0.10): form_1040.pdf content matches source pages 7-10
  - Component 8 (0.10): schedule_c.pdf content matches source pages 11-14
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_074'
FORMS_DIR = os.path.join(WORKDIR, 'finance', 'forms')
BUNDLE_PATH = os.path.join(WORKDIR, 'finance', 'tax_forms_bundle.pdf')

# Expected outputs: (filename, expected_page_count, source_pages_0indexed)
EXPECTED_FILES = [
    ('form_w2.pdf', 4, [0, 1, 2, 3]),
    ('form_1099.pdf', 2, [4, 5]),
    ('form_1040.pdf', 4, [6, 7, 8, 9]),
    ('schedule_c.pdf', 4, [10, 11, 12, 13]),
]

# Content identifiers for first page of each form (unique text from bundle)
FIRST_PAGE_MARKERS = {
    'form_w2.pdf': 'Form W-2',
    'form_1099.pdf': 'Form 1099-INT',
    'form_1040.pdf': 'Form 1040',
    'schedule_c.pdf': 'Schedule C',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the source bundle for content comparison
    bundle_page_texts = {}
    try:
        import fitz
        bundle_doc = fitz.open(BUNDLE_PATH)
        for i in range(bundle_doc.page_count):
            bundle_page_texts[i] = bundle_doc[i].get_text().strip()
        bundle_doc.close()
    except Exception as e:
        print(f"WARNING: Could not load bundle for content comparison: {e}")
        # We can still check file existence and page counts

    # Components 1-4: File existence + correct page count (0.15 each = 0.60 total)
    for fname, expected_pages, source_pages in EXPECTED_FILES:
        fpath = os.path.join(FORMS_DIR, fname)
        try:
            if not os.path.exists(fpath):
                print(f"FAIL: {fname} does not exist at {fpath}")
                continue

            import fitz
            doc = fitz.open(fpath)
            actual_pages = doc.page_count
            doc.close()

            if actual_pages == expected_pages:
                print(f"PASS: {fname} has correct page count {actual_pages} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: {fname} has {actual_pages} pages, expected {expected_pages}")
        except Exception as e:
            print(f"ERROR: Could not check {fname}: {e}")

    # Components 5-8: Content verification (0.10 each = 0.40 total)
    # Each split file's pages should match the corresponding source pages from the bundle
    if bundle_page_texts:
        for fname, expected_pages, source_pages in EXPECTED_FILES:
            fpath = os.path.join(FORMS_DIR, fname)
            try:
                if not os.path.exists(fpath):
                    print(f"FAIL: Content check skipped for {fname} - file missing")
                    continue

                import fitz
                doc = fitz.open(fpath)

                if doc.page_count != expected_pages:
                    print(f"FAIL: Content check skipped for {fname} - wrong page count")
                    doc.close()
                    continue

                # Check that the first page contains the expected form marker
                first_page_text = doc[0].get_text().strip()
                marker = FIRST_PAGE_MARKERS[fname]

                if marker not in first_page_text:
                    print(f"FAIL: {fname} first page does not contain '{marker}'")
                    doc.close()
                    continue

                # Check content similarity with source pages
                # Compare text of each page in the split file with corresponding bundle page
                mismatched_pages = []
                for local_idx, bundle_idx in enumerate(source_pages):
                    if bundle_idx not in bundle_page_texts:
                        continue
                    split_text = doc[local_idx].get_text().strip()
                    bundle_text = bundle_page_texts[bundle_idx]
                    # Check that the texts are substantially similar (first 200 chars)
                    if split_text[:200] != bundle_text[:200]:
                        mismatched_pages.append((local_idx + 1, bundle_idx + 1))

                doc.close()

                if len(mismatched_pages) == 0:
                    print(f"PASS: {fname} content matches source pages (0.10 pts)")
                    total_score += 0.10
                else:
                    for lp, bp in mismatched_pages:
                        print(f"  MISMATCH: {fname} page {lp} vs bundle page {bp}")
                    print(f"FAIL: {fname} content does not match source pages")

            except Exception as e:
                print(f"ERROR: Content check for {fname}: {e}")
    else:
        print("SKIP: Content checks skipped - bundle not available for comparison")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
