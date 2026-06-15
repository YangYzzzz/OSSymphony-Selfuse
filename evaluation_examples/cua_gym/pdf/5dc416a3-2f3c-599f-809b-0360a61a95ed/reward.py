"""
Reward Script: Extract URLs from PDF and categorize by domain
Task ID: pdf_cross_102
Domain: pdf (cross-domain: Python scripting + PDF)
Scoring:
  - Component 1: ~/scripts/extract_urls.py exists and is non-empty Python file (0.2 pts)
  - Component 2: ~/Documents/url_report.json exists, is valid JSON,
                 and has correct structure {domain: {count: N, urls: [...]}} (0.3 pts)
  - Component 3: Key expected domains (github.com, docs.python.org, stackoverflow.com)
                 are present in url_report.json (0.2 pts)
  - Component 4: Total URL count is >= 30 across all domains (0.15 pts)
  - Component 5: extract_urls.py uses pymupdf/fitz for PDF link extraction (0.15 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_102'

SCRIPT_PATH = os.path.join(WORKDIR, 'scripts', 'extract_urls.py')
REPORT_PATH = os.path.join(WORKDIR, 'Documents', 'url_report.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ~/scripts/extract_urls.py exists and is a non-empty Python file (0.2 pts)
    try:
        if not os.path.exists(SCRIPT_PATH):
            print(f"FAIL: Component 1 — ~/scripts/extract_urls.py does not exist")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read().strip()
            if len(script_content) < 50:
                print(f"FAIL: Component 1 — extract_urls.py is too short or empty (len={len(script_content)})")
            else:
                print(f"PASS: Component 1 — extract_urls.py exists with {len(script_content)} chars (0.2 pts)")
                total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ~/Documents/url_report.json exists, is valid JSON,
    # has domain keys with {count: N, urls: [...]} structure (0.3 pts)
    report_data = None
    try:
        if not os.path.exists(REPORT_PATH):
            print(f"FAIL: Component 2 — ~/Documents/url_report.json does not exist")
        else:
            with open(REPORT_PATH, 'r') as f:
                report_data = json.load(f)
            # Verify top-level structure: should be a dict
            if not isinstance(report_data, dict):
                print(f"FAIL: Component 2 — url_report.json is not a JSON object (dict), got {type(report_data)}")
                report_data = None
            elif len(report_data) == 0:
                print(f"FAIL: Component 2 — url_report.json is an empty object (no domains)")
                report_data = None
            else:
                # Verify each domain entry has {count: N, urls: [...]} format
                valid_structure = True
                invalid_domains = []
                for domain, entry in report_data.items():
                    if not isinstance(entry, dict):
                        valid_structure = False
                        invalid_domains.append(f"{domain}: entry is not a dict")
                        continue
                    if 'count' not in entry:
                        valid_structure = False
                        invalid_domains.append(f"{domain}: missing 'count' key")
                    elif not isinstance(entry['count'], int):
                        valid_structure = False
                        invalid_domains.append(f"{domain}: 'count' is not an integer")
                    if 'urls' not in entry:
                        valid_structure = False
                        invalid_domains.append(f"{domain}: missing 'urls' key")
                    elif not isinstance(entry['urls'], list):
                        valid_structure = False
                        invalid_domains.append(f"{domain}: 'urls' is not a list")
                    elif isinstance(entry.get('count'), int) and entry['count'] != len(entry['urls']):
                        # count should match length of urls list
                        valid_structure = False
                        invalid_domains.append(f"{domain}: count={entry['count']} != len(urls)={len(entry['urls'])}")

                if valid_structure:
                    print(f"PASS: Component 2 — url_report.json is valid JSON with correct structure, {len(report_data)} domains (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — url_report.json structure invalid: {invalid_domains[:3]}")
                    report_data = None
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — url_report.json is not valid JSON: {e}")
        report_data = None
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Key expected domains present in url_report.json (0.2 pts)
    # Expected domains from task context: github.com, docs.python.org, stackoverflow.com
    try:
        if report_data is None:
            print(f"FAIL: Component 3 — url_report.json not available (see Component 2)")
        else:
            expected_domains = ['github.com', 'docs.python.org', 'stackoverflow.com']
            present_domains = [d for d in expected_domains if d in report_data]
            if len(present_domains) >= 3:
                print(f"PASS: Component 3 — All 3 key domains present: {present_domains} (0.2 pts)")
                total_score += 0.2
            elif len(present_domains) >= 2:
                # Partial credit: 2 out of 3 key domains
                print(f"PARTIAL: Component 3 — {len(present_domains)}/3 key domains present: {present_domains} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — Only {len(present_domains)}/3 key domains present: {present_domains}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Total URL count >= 30 (0.15 pts)
    try:
        if report_data is None:
            print(f"FAIL: Component 4 — url_report.json not available (see Component 2)")
        else:
            total_urls = sum(entry['count'] for entry in report_data.values()
                             if isinstance(entry, dict) and isinstance(entry.get('count'), int))
            if total_urls >= 30:
                print(f"PASS: Component 4 — Total URL count = {total_urls} (>= 30) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Total URL count = {total_urls} (< 30, expected >= 30)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: extract_urls.py uses pymupdf/fitz for PDF link extraction (0.15 pts)
    # This verifies the script actually does what was asked (extracts from PDF, not just hardcoded)
    try:
        if not os.path.exists(SCRIPT_PATH):
            print(f"FAIL: Component 5 — extract_urls.py does not exist")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()
            # Script must import a PDF library and use get_links or similar
            uses_pdf_lib = ('pymupdf' in script_content or 'fitz' in script_content or
                            'pikepdf' in script_content or 'pdfminer' in script_content or
                            'PyPDF' in script_content)
            has_link_extraction = ('get_links' in script_content or 'annots' in script_content or
                                   'link' in script_content.lower())
            has_json_output = ('json' in script_content and
                               ('url_report' in script_content or 'json.dump' in script_content))

            if uses_pdf_lib and has_link_extraction and has_json_output:
                print(f"PASS: Component 5 — Script uses PDF library for link extraction and outputs JSON (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if not uses_pdf_lib:
                    details.append("no PDF library import found")
                if not has_link_extraction:
                    details.append("no link extraction code found")
                if not has_json_output:
                    details.append("no JSON output code found")
                print(f"FAIL: Component 5 — {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
