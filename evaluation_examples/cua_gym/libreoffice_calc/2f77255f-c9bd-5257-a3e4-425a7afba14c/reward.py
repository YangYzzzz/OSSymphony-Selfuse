"""
Reward Script: Extract hyperlinks from PDF and save to links.txt
Task ID: pdf_ro_042
Domain: pdf
Scoring:
  Component 1 (0.20): links.txt has approximately correct number of lines (~26)
  Component 2 (0.25): Lines follow 'Page X: [link_text] -> URL' format
  Component 3 (0.35): All URLs from PDF are captured in links.txt
  Component 4 (0.20): Link text labels match PDF link annotations
"""

import os
import re
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_042'
LINKS_FILE = os.path.join(WORKDIR, 'Documents', 'links.txt')
PDF_FILE = os.path.join(WORKDIR, 'Documents', 'web_report.pdf')

# Expected format regex: 'Page X: [link_text] -> URL'
LINE_PATTERN = re.compile(r'^Page\s+(\d+):\s+\[(.+?)\]\s*->\s*(\S+)$')


def extract_pdf_links(pdf_path):
    """Extract all URI links from the PDF, returning list of (page_num, uri) tuples."""
    links = []
    try:
        doc = fitz.open(pdf_path)
        for i in range(doc.page_count):
            page_links = doc[i].get_links()
            for link in page_links:
                uri = link.get('uri', '')
                if uri:
                    links.append((i + 1, uri))  # 1-indexed page
        doc.close()
    except Exception as e:
        print(f"ERROR: Cannot extract links from PDF: {e}")
    return links


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: links.txt must exist
    if not os.path.exists(LINKS_FILE):
        print(f"CRITICAL: links.txt not found at {LINKS_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: PDF must exist (to cross-reference)
    if not os.path.exists(PDF_FILE):
        print(f"CRITICAL: PDF not found at {PDF_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Read links.txt lines
    try:
        with open(LINKS_FILE, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"CRITICAL: Cannot read links.txt: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract ground truth links from PDF
    pdf_links = extract_pdf_links(PDF_FILE)
    expected_count = len(pdf_links)
    print(f"INFO: PDF contains {expected_count} URI links across all pages")
    print(f"INFO: links.txt contains {len(lines)} non-empty lines")

    # Component 1: Line count approximately matches PDF link count (0.20 points)
    # Allow a tolerance of +/- 3 for minor differences in link detection
    try:
        count_diff = abs(len(lines) - expected_count)
        if count_diff == 0:
            print(f"PASS: Component 1 — Exact line count match: {len(lines)} lines (0.20 pts)")
            total_score += 0.20
        elif count_diff <= 3:
            partial = 0.20 * (1 - count_diff * 0.15)
            print(f"PARTIAL: Component 1 — Line count {len(lines)} vs expected {expected_count}, diff={count_diff} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Line count {len(lines)} vs expected {expected_count}, diff={count_diff}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Format compliance — lines match 'Page X: [text] -> URL' (0.25 points)
    try:
        valid_format_count = 0
        parsed_entries = []
        for line in lines:
            match = LINE_PATTERN.match(line)
            if match:
                valid_format_count += 1
                page_num = int(match.group(1))
                link_text = match.group(2)
                url = match.group(3)
                parsed_entries.append((page_num, link_text, url))

        if len(lines) > 0:
            format_ratio = valid_format_count / len(lines)
        else:
            format_ratio = 0.0

        if format_ratio >= 0.95:
            print(f"PASS: Component 2 — {valid_format_count}/{len(lines)} lines have correct format (0.25 pts)")
            total_score += 0.25
        elif format_ratio >= 0.7:
            partial = 0.25 * format_ratio
            print(f"PARTIAL: Component 2 — {valid_format_count}/{len(lines)} lines have correct format ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {valid_format_count}/{len(lines)} lines have correct format")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: URL coverage — all PDF URIs appear in links.txt (0.35 points)
    try:
        # Collect all URLs found in parsed entries
        found_urls = set()
        for entry in parsed_entries:
            found_urls.add(entry[2].rstrip('/'))

        expected_urls = set()
        for _, uri in pdf_links:
            expected_urls.add(uri.rstrip('/'))

        if len(expected_urls) > 0:
            matched = len(expected_urls.intersection(found_urls))
            coverage = matched / len(expected_urls)
        else:
            coverage = 0.0

        if coverage >= 0.95:
            print(f"PASS: Component 3 — {matched}/{len(expected_urls)} URLs captured (0.35 pts)")
            total_score += 0.35
        elif coverage >= 0.5:
            partial = 0.35 * coverage
            print(f"PARTIAL: Component 3 — {matched}/{len(expected_urls)} URLs captured ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {matched}/{len(expected_urls)} URLs captured")
            # Show missing URLs
            missing = expected_urls - found_urls
            for url in list(missing)[:5]:
                print(f"  MISSING: {url}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Link text accuracy — page numbers and link text match (0.20 points)
    try:
        # Check that page numbers in links.txt match the actual pages where links appear in PDF
        pdf_page_url_map = {}
        for page_num, uri in pdf_links:
            pdf_page_url_map[uri.rstrip('/')] = page_num

        correct_page_count = 0
        has_link_text_count = 0
        for entry in parsed_entries:
            page_num, link_text, url = entry
            url_stripped = url.rstrip('/')
            # Check page number accuracy
            if url_stripped in pdf_page_url_map:
                if pdf_page_url_map[url_stripped] == page_num:
                    correct_page_count += 1
            # Check link text is non-empty and meaningful (not just the URL repeated)
            if link_text and link_text != url:
                has_link_text_count += 1

        if len(parsed_entries) > 0:
            page_accuracy = correct_page_count / len(parsed_entries)
            text_accuracy = has_link_text_count / len(parsed_entries)
            combined = (page_accuracy + text_accuracy) / 2.0
        else:
            combined = 0.0

        if combined >= 0.9:
            print(f"PASS: Component 4 — Page accuracy: {correct_page_count}/{len(parsed_entries)}, "
                  f"text labels: {has_link_text_count}/{len(parsed_entries)} (0.20 pts)")
            total_score += 0.20
        elif combined >= 0.5:
            partial = 0.20 * combined
            print(f"PARTIAL: Component 4 — Page accuracy: {correct_page_count}/{len(parsed_entries)}, "
                  f"text labels: {has_link_text_count}/{len(parsed_entries)} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Page accuracy: {correct_page_count}/{len(parsed_entries)}, "
                  f"text labels: {has_link_text_count}/{len(parsed_entries)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
