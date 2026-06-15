"""
Reward Script: Strip all metadata from sensitive_doc.pdf and save as sensitive_doc_anon.pdf
Task ID: pdf_gf2_015
Domain: pdf
Scoring:
  Component 1 (0.30): Output file exists with correct page count (4 pages)
  Component 2 (0.35): Standard metadata fields (title, author, subject, keywords, creator, producer) are all empty
  Component 3 (0.20): XMP metadata stream absent and docinfo empty (pikepdf verification)
  Component 4 (0.15): Page content preserved (text on each page matches source)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_015'

SOURCE_PATH = os.path.join(WORKDIR, 'Documents', 'sensitive_doc.pdf')
ANON_PATH = os.path.join(WORKDIR, 'Documents', 'sensitive_doc_anon.pdf')

EXPECTED_PAGE_COUNT = 4


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source file must exist
    if not os.path.exists(SOURCE_PATH):
        print(f"CRITICAL: Source file not found: {SOURCE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: anon file must exist (gate, not scored)
    if not os.path.exists(ANON_PATH):
        print(f"FAIL: Anonymized file not found: {ANON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists with correct page count (0.30 points)
    try:
        import pymupdf
        doc = pymupdf.open(ANON_PATH)
        page_count = doc.page_count
        doc.close()
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 -- Anon PDF has {page_count} pages as expected (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Standard metadata fields are all empty (0.35 points)
    try:
        import pymupdf
        doc = pymupdf.open(ANON_PATH)
        meta = doc.metadata
        doc.close()

        fields_to_check = ['title', 'author', 'subject', 'keywords', 'creator', 'producer']
        all_empty = True
        for field in fields_to_check:
            value = meta.get(field, '')
            if value is None:
                value = ''
            if value.strip() != '':
                print(f"FAIL: Component 2 -- Metadata field '{field}' is not empty: '{value}'")
                all_empty = False

        if all_empty:
            print(f"PASS: Component 2 -- All 6 standard metadata fields are empty (0.35 pts)")
            total_score += 0.35
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: XMP metadata absent and docinfo empty via pikepdf (0.20 points)
    try:
        import pikepdf
        pdf = pikepdf.open(ANON_PATH)

        xmp_absent = '/Metadata' not in pdf.Root
        docinfo_empty = len(list(pdf.docinfo.keys())) == 0 if pdf.docinfo else True

        # Also check XMP fields via the metadata API
        xmp_clean = True
        try:
            with pdf.open_metadata() as xmp_meta:
                identifying_keys = [
                    'dc:title', 'dc:creator', 'dc:subject', 'dc:description',
                    'pdf:Keywords', 'pdf:Producer', 'xmp:CreatorTool'
                ]
                for k in identifying_keys:
                    val = xmp_meta.get(k, '')
                    if val and str(val).strip() != '':
                        print(f"FAIL: Component 3 -- XMP key '{k}' has value: '{val}'")
                        xmp_clean = False
        except Exception:
            # If XMP metadata stream doesn't exist, that's fine
            pass

        pdf.close()

        if xmp_absent and docinfo_empty and xmp_clean:
            print(f"PASS: Component 3 -- No XMP metadata stream, docinfo empty, XMP clean (0.20 pts)")
            total_score += 0.20
        else:
            if not xmp_absent:
                print(f"FAIL: Component 3 -- /Metadata stream still present in PDF")
            if not docinfo_empty:
                print(f"FAIL: Component 3 -- docinfo still has keys")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Page content preserved (0.15 points)
    try:
        import pymupdf
        src_doc = pymupdf.open(SOURCE_PATH)
        anon_doc = pymupdf.open(ANON_PATH)

        content_match = True
        for i in range(min(src_doc.page_count, anon_doc.page_count)):
            src_text = src_doc[i].get_text('text')
            anon_text = anon_doc[i].get_text('text')
            if src_text.strip() != anon_text.strip():
                print(f"FAIL: Component 4 -- Page {i} text differs (src len={len(src_text)}, anon len={len(anon_text)})")
                content_match = False
                break

        src_doc.close()
        anon_doc.close()

        if content_match:
            print(f"PASS: Component 4 -- All page content preserved (0.15 pts)")
            total_score += 0.15
        # else already printed
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
