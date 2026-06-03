"""
Reward Script: Extract URLs/hyperlinks from PDF and save to text file
Task ID: pdf_mbc_077
Domain: pdf
Scoring:
  Component 1 (0.20): links.txt file exists
  Component 2 (0.20): Correct number of lines (15)
  Component 3 (0.30): All URLs are correctly extracted
  Component 4 (0.30): Page numbers are correctly assigned
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_077'

# Expected ground truth: 15 hyperlinks from resource_guide.pdf
# Format: "Page N: https://..." one per line


def get_expected_links_from_pdf(pdf_path):
    """Extract all URI links from the PDF, returning list of (page_num, uri) tuples."""
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    links = []
    doc = pymupdf.open(pdf_path)
    for i in range(doc.page_count):
        page = doc[i]
        for link in page.get_links():
            uri = link.get("uri")
            if uri:
                links.append((i + 1, uri))
    doc.close()
    return links


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    links_file = os.path.join(WORKDIR, 'Documents', 'links.txt')
    pdf_file = os.path.join(WORKDIR, 'Documents', 'resource_guide.pdf')

    # Precondition: PDF must exist (not scored — it's pre-existing)
    if not os.path.exists(pdf_file):
        print(f"CRITICAL: PDF not found at {pdf_file}")
        print("REWARD: 0.0")
        return 0.0

    # Get ground truth links from the PDF itself
    expected_links = get_expected_links_from_pdf(pdf_file)
    expected_count = len(expected_links)
    print(f"INFO: Found {expected_count} links in PDF")

    # Component 1: links.txt file exists with non-empty content (0.20 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if os.path.exists(links_file):
            content = open(links_file, 'r').read().strip()
            if len(content) > 0:
                print(f"PASS: Component 1 — links.txt exists and is non-empty (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — links.txt exists but is empty")
        else:
            print(f"FAIL: Component 1 — links.txt does not exist at {links_file}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Early exit if file doesn't exist
    if not os.path.exists(links_file):
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read and parse links.txt
    try:
        with open(links_file, 'r') as f:
            raw_lines = f.read().strip().split('\n')
        lines = [l.strip() for l in raw_lines if l.strip()]
    except Exception as e:
        print(f"ERROR: Cannot read links.txt: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Correct number of lines (0.20 points)
    # Expected: 15 lines (one per hyperlink)
    try:
        if len(lines) == expected_count:
            print(f"PASS: Component 2 — {len(lines)} lines matches expected {expected_count} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Found {len(lines)} lines, expected {expected_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All URLs are correctly extracted (0.30 points)
    # Check that every expected URL appears in links.txt
    try:
        expected_urls = set(url for _, url in expected_links)
        found_urls = set()
        for line in lines:
            # Extract URL from line — look for http/https pattern
            url_match = re.search(r'(https?://\S+)', line)
            if url_match:
                found_urls.add(url_match.group(1))

        matched_urls = expected_urls & found_urls
        url_ratio = len(matched_urls) / max(len(expected_urls), 1)

        if url_ratio == 1.0:
            print(f"PASS: Component 3 — All {len(expected_urls)} URLs found (0.30 pts)")
            total_score += 0.30
        elif url_ratio >= 0.8:
            partial = round(0.30 * url_ratio, 2)
            print(f"PARTIAL: Component 3 — {len(matched_urls)}/{len(expected_urls)} URLs found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {len(matched_urls)}/{len(expected_urls)} URLs matched")
            missing = expected_urls - found_urls
            for m in list(missing)[:3]:
                print(f"  Missing: {m}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page numbers are correctly assigned (0.30 points)
    # Each line should have the correct page number prefix for its URL
    try:
        # Build a map: url -> expected page number
        url_to_page = {}
        for page_num, url in expected_links:
            url_to_page[url] = page_num

        correct_pages = 0
        total_checked = 0

        for line in lines:
            # Parse "Page N: URL" format
            page_match = re.match(r'[Pp]age\s+(\d+)\s*[:\-]\s*(https?://\S+)', line)
            if page_match:
                found_page = int(page_match.group(1))
                found_url = page_match.group(2)
                total_checked += 1
                if found_url in url_to_page and url_to_page[found_url] == found_page:
                    correct_pages += 1
                else:
                    expected_page = url_to_page.get(found_url, '?')
                    print(f"  Page mismatch for {found_url}: found Page {found_page}, expected Page {expected_page}")

        if total_checked == 0:
            print(f"FAIL: Component 4 — No lines in 'Page N: URL' format found")
        else:
            page_ratio = correct_pages / max(total_checked, 1)
            if page_ratio == 1.0 and total_checked == expected_count:
                print(f"PASS: Component 4 — All {correct_pages} page numbers correct (0.30 pts)")
                total_score += 0.30
            elif page_ratio >= 0.8:
                partial = round(0.30 * page_ratio, 2)
                print(f"PARTIAL: Component 4 — {correct_pages}/{total_checked} page numbers correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Only {correct_pages}/{total_checked} page numbers correct")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
