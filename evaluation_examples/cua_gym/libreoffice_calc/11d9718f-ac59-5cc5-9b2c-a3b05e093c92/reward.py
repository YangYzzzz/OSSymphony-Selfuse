"""
Reward Script: Search for 'confidential' in contract.pdf and write results to search_results.txt
Task ID: pdf_cr_049
Domain: libreoffice_calc (PDF task)
Scoring:
  Component 1 (0.15): search_results.txt exists at correct path
  Component 2 (0.25): Lines follow expected format with Page number and [CONFIDENTIAL] marker
  Component 3 (0.25): Total occurrences line present with correct count matching PDF
  Component 4 (0.15): Results cover occurrences across multiple pages (>=6 of 8 pages)
  Component 5 (0.20): Context snippets match actual text from the PDF
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_049'
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'contract.pdf')
RESULTS_PATH = os.path.join(WORKDIR, 'Desktop', 'search_results.txt')


def count_pdf_occurrences(pdf_path):
    """Count actual occurrences of 'confidential' (case-insensitive) in the PDF."""
    try:
        import pymupdf
        doc = pymupdf.open(pdf_path)
        total = 0
        page_counts = {}
        for i, page in enumerate(doc):
            text = page.get_text()
            matches = list(re.finditer(r'confidential', text, re.IGNORECASE))
            if matches:
                page_counts[i + 1] = len(matches)
                total += len(matches)
        doc.close()
        return total, page_counts
    except Exception as e:
        print(f"ERROR: Could not analyze PDF: {e}")
        return None, None


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

    # Component 1: search_results.txt exists at correct path (0.15 points)
    try:
        if os.path.exists(RESULTS_PATH):
            content = open(RESULTS_PATH, 'r', encoding='utf-8', errors='replace').read().strip()
            if len(content) > 0:
                print(f"PASS: Component 1 — search_results.txt exists and is non-empty ({len(content)} chars) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — search_results.txt exists but is empty")
        else:
            print(f"FAIL: Component 1 — search_results.txt not found at {RESULTS_PATH}")
            # If file doesn't exist, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the file content for subsequent checks
    lines = content.split('\n')

    # Component 2: Lines follow expected format (0.25 points)
    # Expected: "Page X: ...context... [CONFIDENTIAL] ...context..."
    try:
        # Separate occurrence lines from the total line
        occurrence_lines = []
        total_line = None
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r'^total\s+occurrences\s*:', stripped, re.IGNORECASE):
                total_line = stripped
            elif re.match(r'^page\s+\d+\s*:', stripped, re.IGNORECASE):
                occurrence_lines.append(stripped)

        if len(occurrence_lines) == 0:
            print(f"FAIL: Component 2 — No occurrence lines found matching 'Page X: ...' format")
        else:
            # Check how many lines have proper format with [CONFIDENTIAL] marker
            well_formatted = 0
            for occ_line in occurrence_lines:
                # Must have "Page <num>:" and some form of "confidential" in brackets or context
                if re.match(r'^Page\s+\d+\s*:', occ_line, re.IGNORECASE):
                    # Check for CONFIDENTIAL keyword (in brackets or in context)
                    if re.search(r'confidential', occ_line, re.IGNORECASE):
                        well_formatted += 1

            format_ratio = well_formatted / len(occurrence_lines) if occurrence_lines else 0
            if format_ratio >= 0.8:
                print(f"PASS: Component 2 — {well_formatted}/{len(occurrence_lines)} lines properly formatted (0.25 pts)")
                total_score += 0.25
            elif format_ratio >= 0.5:
                partial = round(0.25 * format_ratio, 2)
                print(f"PARTIAL: Component 2 — {well_formatted}/{len(occurrence_lines)} lines formatted ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Only {well_formatted}/{len(occurrence_lines)} lines properly formatted")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Total occurrences count is correct (0.25 points)
    try:
        actual_total, page_counts = count_pdf_occurrences(PDF_PATH)
        if actual_total is None:
            print(f"ERROR: Component 3 — Could not count PDF occurrences")
        elif total_line is not None:
            # Extract reported total
            match = re.search(r'(\d+)', total_line)
            if match:
                reported_total = int(match.group(1))
                # Also check occurrence lines count as secondary validation
                if reported_total == actual_total:
                    print(f"PASS: Component 3 — Total occurrences: {reported_total} matches PDF count ({actual_total}) (0.25 pts)")
                    total_score += 0.25
                elif abs(reported_total - actual_total) <= 3:
                    # Close but not exact — partial credit
                    if abs(reported_total - actual_total) <= 3:
                        partial = 0.12
                        print(f"PARTIAL: Component 3 — Reported {reported_total}, actual {actual_total} (close, {partial} pts)")
                        total_score += partial
                else:
                    print(f"FAIL: Component 3 — Reported {reported_total} occurrences, actual PDF has {actual_total}")
            else:
                print(f"FAIL: Component 3 — Total line found but no number: '{total_line}'")
        else:
            # No total line, check if count of occurrence lines is reasonable
            if len(occurrence_lines) > 0 and abs(len(occurrence_lines) - actual_total) <= 3:
                partial = 0.10
                print(f"PARTIAL: Component 3 — No 'Total occurrences' line but {len(occurrence_lines)} occurrence lines (close to {actual_total}) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No 'Total occurrences' line found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Results cover multiple pages (0.15 points)
    try:
        pages_mentioned = set()
        for occ_line in occurrence_lines:
            m = re.match(r'^Page\s+(\d+)\s*:', occ_line, re.IGNORECASE)
            if m:
                pages_mentioned.add(int(m.group(1)))

        if page_counts:
            expected_pages = set(page_counts.keys())
            covered = pages_mentioned & expected_pages
            coverage_ratio = len(covered) / len(expected_pages) if expected_pages else 0

            if coverage_ratio >= 0.9:
                print(f"PASS: Component 4 — Covers {len(covered)}/{len(expected_pages)} pages with occurrences (0.15 pts)")
                total_score += 0.15
            elif coverage_ratio >= 0.6:
                partial = round(0.15 * coverage_ratio, 2)
                print(f"PARTIAL: Component 4 — Covers {len(covered)}/{len(expected_pages)} pages ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Only covers {len(covered)}/{len(expected_pages)} pages")
        else:
            # Fallback: just check page coverage
            if len(pages_mentioned) >= 6:
                print(f"PASS: Component 4 — Mentions {len(pages_mentioned)} different pages (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Only mentions {len(pages_mentioned)} pages")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Context snippets are accurate (0.20 points)
    # Verify that at least some of the context text actually appears in the PDF
    try:
        import pymupdf
        doc = pymupdf.open(PDF_PATH)
        page_texts = {}
        for i, page in enumerate(doc):
            page_texts[i + 1] = page.get_text()
        doc.close()

        verified_count = 0
        check_count = min(len(occurrence_lines), 10)  # Check up to 10 lines
        for occ_line in occurrence_lines[:check_count]:
            m = re.match(r'^Page\s+(\d+)\s*:\s*(.*)', occ_line, re.IGNORECASE)
            if m:
                page_num = int(m.group(1))
                context_text = m.group(2)
                # Extract a meaningful snippet from the context (strip markers/ellipses)
                # Remove [CONFIDENTIAL] markers and ellipses to get raw context
                snippet = re.sub(r'\[CONFIDENTIAL\]', '', context_text, flags=re.IGNORECASE)
                snippet = re.sub(r'\.\.\.', '', snippet).strip()
                # Take a substring (at least 10 chars) and check if it appears in the page
                if page_num in page_texts and len(snippet) >= 10:
                    # Normalize whitespace for comparison
                    normalized_page = re.sub(r'\s+', ' ', page_texts[page_num])
                    normalized_snippet = re.sub(r'\s+', ' ', snippet)
                    # Check if a significant portion of the snippet exists in the page
                    # Use a substring of at least 15 chars
                    words = normalized_snippet.split()
                    if len(words) >= 3:
                        # Check if a 3+ word phrase from the snippet is in the page
                        test_phrase = ' '.join(words[:4])
                        if test_phrase.lower() in normalized_page.lower():
                            verified_count += 1
                        else:
                            # Try last few words
                            test_phrase = ' '.join(words[-4:])
                            if test_phrase.lower() in normalized_page.lower():
                                verified_count += 1

        if check_count > 0:
            accuracy_ratio = verified_count / check_count
            if accuracy_ratio >= 0.7:
                print(f"PASS: Component 5 — {verified_count}/{check_count} checked snippets verified in PDF (0.20 pts)")
                total_score += 0.20
            elif accuracy_ratio >= 0.4:
                partial = round(0.20 * accuracy_ratio, 2)
                print(f"PARTIAL: Component 5 — {verified_count}/{check_count} snippets verified ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Only {verified_count}/{check_count} snippets verified in PDF")
        else:
            print(f"FAIL: Component 5 — No occurrence lines to verify")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(RESULTS_PATH):
    print(f"File not found: {RESULTS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
