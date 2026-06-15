"""
Reward Script: PDF Portfolio - Merge 5 certificate PDFs with cover page and TOC
Task ID: pdf_ro_034
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists with exactly 7 pages
  Component 2 (0.20): Cover page contains 'Professional Certifications Portfolio'
  Component 3 (0.25): TOC page lists all 5 certificates with correct page numbers
  Component 4 (0.20): Pages 3-7 contain the 5 certificates in correct order
  Component 5 (0.15): Bookmarks exist for navigation (at least 5 entries)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_034'

# Expected certificate names in order
CERT_NAMES = [
    'AWS Solutions Architect',
    'PMP',
    'CISSP',
    'Google Cloud Professional',
    'Kubernetes Administrator',
]

# Expected TOC page numbers (certs start on page 3)
CERT_PAGES = [3, 4, 5, 6, 7]


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

    # Component 1: Output file has exactly 7 pages (0.20 points)
    # Initial env has no output file, so this FAILS on initial
    try:
        page_count = doc.page_count
        if page_count == 7:
            print(f"PASS: Component 1 — Page count is 7 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 7 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cover page contains 'Professional Certifications Portfolio' (0.20 points)
    # The initial env has no output file, so this FAILS on initial
    try:
        cover_page = doc[0]
        cover_text = cover_page.get_text().strip()
        if 'Professional Certifications' in cover_text and 'Portfolio' in cover_text:
            print(f"PASS: Component 2 — Cover page has title text (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Cover page missing title. Found: {cover_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: TOC page lists all 5 certs with correct page numbers (0.25 points)
    # Awards partial credit: 0.05 per cert found on TOC page
    try:
        toc_page = doc[1]
        toc_text = toc_page.get_text()
        toc_score = 0.0
        found_count = 0
        for i, cert_name in enumerate(CERT_NAMES):
            expected_page = str(CERT_PAGES[i])
            # Check cert name appears on TOC page
            if cert_name in toc_text:
                # Check page number also appears
                if expected_page in toc_text:
                    toc_score += 0.05
                    found_count += 1
                    print(f"  TOC: Found '{cert_name}' with page {expected_page}")
                else:
                    print(f"  TOC: Found '{cert_name}' but missing page number {expected_page}")
            else:
                print(f"  TOC: Missing '{cert_name}'")

        if found_count == 5:
            print(f"PASS: Component 3 — All 5 certs listed in TOC with page numbers (0.25 pts)")
            total_score += 0.25
        elif found_count > 0:
            print(f"PARTIAL: Component 3 — {found_count}/5 certs in TOC ({toc_score:.2f} pts)")
            total_score += toc_score
        else:
            print(f"FAIL: Component 3 — No certs found in TOC")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Pages 3-7 contain the 5 certificates in correct order (0.20 points)
    # Awards partial credit: 0.04 per cert found on correct page
    try:
        cert_score = 0.0
        certs_found = 0
        for i, cert_name in enumerate(CERT_NAMES):
            page_idx = i + 2  # pages 3-7 are indices 2-6
            if page_idx < doc.page_count:
                page_text = doc[page_idx].get_text()
                if cert_name in page_text and 'CERTIFICATE' in page_text.upper():
                    cert_score += 0.04
                    certs_found += 1
                    print(f"  Cert page {page_idx+1}: Found '{cert_name}'")
                else:
                    print(f"  Cert page {page_idx+1}: Missing '{cert_name}', found: {page_text[:100]}")
            else:
                print(f"  Cert page {page_idx+1}: Page does not exist")

        if certs_found == 5:
            print(f"PASS: Component 4 — All 5 certs on correct pages (0.20 pts)")
            total_score += 0.20
        elif certs_found > 0:
            print(f"PARTIAL: Component 4 — {certs_found}/5 certs found ({cert_score:.2f} pts)")
            total_score += cert_score
        else:
            print(f"FAIL: Component 4 — No certs found on expected pages")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Bookmarks exist for navigation (0.15 points)
    # At least 5 bookmark entries expected (one per cert, possibly also cover/TOC)
    try:
        toc_entries = doc.get_toc()
        num_entries = len(toc_entries)
        if num_entries >= 5:
            # Verify bookmark entries reference cert names
            bookmark_names = [entry[1] for entry in toc_entries]
            certs_bookmarked = sum(
                1 for cn in CERT_NAMES if any(cn in bn for bn in bookmark_names)
            )
            if certs_bookmarked >= 5:
                print(f"PASS: Component 5 — {num_entries} bookmarks with all cert names (0.15 pts)")
                total_score += 0.15
            elif certs_bookmarked >= 3:
                partial = 0.10
                print(f"PARTIAL: Component 5 — {certs_bookmarked}/5 cert bookmarks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Only {certs_bookmarked}/5 cert names in bookmarks")
        else:
            print(f"FAIL: Component 5 — Expected >= 5 bookmarks, found {num_entries}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
