"""
Reward Script: Extract URLs from PDF and save to text file
Task ID: pdf_res_045
Domain: pdf
Scoring:
  Component 1 (0.3): all_links.txt exists with valid URL content
  Component 2 (0.3): File contains >= 20 valid URLs, one per line
  Component 3 (0.4): Extracted URLs match actual PDF hyperlinks (>= 80% overlap)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_045'

# Expected PDF path and output path
PDF_PATH = os.path.join(WORKDIR, 'papers', 'web_references.pdf')
LINKS_PATH = os.path.join(WORKDIR, 'papers', 'all_links.txt')


def extract_pdf_links(pdf_path):
    """Extract all http/https URI links from the PDF using PyMuPDF."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        links = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            for link in page.get_links():
                uri = link.get('uri', '')
                if uri and (uri.startswith('http://') or uri.startswith('https://')):
                    links.append(uri.strip())
        doc.close()
        return links
    except Exception as e:
        print(f"ERROR: Could not extract links from PDF: {e}")
        return []


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF must exist (gate, not scored)
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read the output file
    try:
        with open(LINKS_PATH, 'r') as f:
            raw_content = f.read()
        lines = [line.strip() for line in raw_content.strip().split('\n') if line.strip()]
    except FileNotFoundError:
        print(f"FAIL: Output file not found at {LINKS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read {LINKS_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File exists and contains valid URL lines (0.3 points)
    # This checks that the file was created AND has meaningful content (URLs)
    try:
        url_pattern = re.compile(r'^https?://\S+$')
        valid_urls = [line for line in lines if url_pattern.match(line)]

        if len(valid_urls) >= 1:
            print(f"PASS: Component 1 — all_links.txt exists with {len(valid_urls)} valid URLs (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — File exists but no valid URLs found. Lines: {len(lines)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File contains at least 20 valid URLs, one per line (0.3 points)
    try:
        if len(valid_urls) >= 20:
            print(f"PASS: Component 2 — {len(valid_urls)} valid URLs found (>= 20 required) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Only {len(valid_urls)} valid URLs found, need >= 20")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: URLs match actual PDF hyperlinks with >= 80% overlap (0.4 points)
    try:
        pdf_links = extract_pdf_links(PDF_PATH)
        if not pdf_links:
            print(f"FAIL: Component 3 — Could not extract links from PDF for comparison")
        else:
            # Normalize URLs for comparison (strip trailing slashes)
            def normalize_url(u):
                return u.strip().rstrip('/')

            pdf_link_set = set(normalize_url(u) for u in pdf_links)
            file_link_set = set(normalize_url(u) for u in valid_urls)

            # Check how many PDF links are present in the file
            matched = pdf_link_set.intersection(file_link_set)
            overlap_ratio = len(matched) / len(pdf_link_set) if pdf_link_set else 0.0

            print(f"  PDF links: {len(pdf_link_set)}, File links: {len(file_link_set)}, Matched: {len(matched)}")
            print(f"  Overlap ratio: {overlap_ratio:.2%}")

            if overlap_ratio >= 0.80:
                print(f"PASS: Component 3 — {overlap_ratio:.0%} overlap with PDF links (>= 80% required) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — Only {overlap_ratio:.0%} overlap with PDF links, need >= 80%")
                # Partial credit: proportional if >= 50%
                if overlap_ratio >= 0.50:
                    partial = 0.4 * (overlap_ratio - 0.50) / 0.30  # Scale from 0.5-0.8 range
                    partial = round(min(partial, 0.3), 2)
                    print(f"  Partial credit: {partial} pts for {overlap_ratio:.0%} overlap")
                    total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
