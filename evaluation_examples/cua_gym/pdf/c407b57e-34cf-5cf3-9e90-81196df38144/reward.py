"""
Reward Script: Create a PDF bibliography with 10 APA-style references
Task ID: pdf_res_071
Domain: pdf
Scoring:
  Component 1: PDF file exists and is loadable (0.1 pts)
  Component 2: PDF has 1-2 pages (0.15 pts)
  Component 3: Contains a "References" heading (0.15 pts)
  Component 4: Contains 10 references (author-year pattern) (0.35 pts)
  Component 5: References have APA components (author, year, title, venue) (0.25 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_071'
FILE_PATH = os.path.join(WORKDIR, 'papers', 'bibliography.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be a valid PDF loadable by PyMuPDF
    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF file exists and is loadable with non-zero size (0.1 pts)
    # This correctly FAILS on initial_env (no file) and PASSES on golden_env.
    try:
        file_size = os.path.getsize(file_path)
        if file_size > 100:
            print(f"PASS: Component 1 -- PDF exists and loadable, size={file_size} bytes (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- PDF file too small: {file_size} bytes")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Extract all text from the PDF
    full_text = ""
    try:
        for page in doc:
            full_text += page.get_text()
    except Exception as e:
        print(f"ERROR: Could not extract text: {e}")
        doc.close()
        print(f"REWARD: {total_score}")
        return total_score

    page_count = doc.page_count
    doc.close()

    # Component 2: PDF has 1-2 pages (0.15 pts)
    try:
        if 1 <= page_count <= 2:
            print(f"PASS: Component 2 -- PDF has {page_count} page(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Expected 1-2 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Contains a "References" heading (0.15 pts)
    try:
        # Check for "References" as a heading (typically on its own line or at the start)
        if re.search(r'(?i)^\s*references\s*$', full_text, re.MULTILINE):
            print(f"PASS: Component 3 -- 'References' heading found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- 'References' heading not found in text")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Contains 10 references identified by APA author-year pattern (0.35 pts)
    # APA references typically start with "Author, X." or "Author, X. X." followed by "(YEAR)."
    try:
        # Pattern: Surname followed by initials, then (year) somewhere after
        # APA format: LastName, F. M. (Year). or LastName, F. M., & LastName, F. M. (Year).
        ref_pattern = r'[A-Z][a-z]+,\s+[A-Z]\.\s*[A-Z]?\.?\s*(?:,\s*(?:&\s*)?[A-Z][a-z]+,\s+[A-Z]\.\s*[A-Z]?\.?\s*)*\((?:19|20)\d{2}\)\.'
        references = re.findall(ref_pattern, full_text)
        ref_count = len(references)

        if ref_count >= 10:
            print(f"PASS: Component 4 -- Found {ref_count} references with APA author-year pattern (0.35 pts)")
            total_score += 0.35
        elif ref_count >= 7:
            partial = round(0.35 * (ref_count / 10), 2)
            print(f"PARTIAL: Component 4 -- Found {ref_count}/10 references ({partial} pts)")
            total_score += partial
        elif ref_count >= 4:
            partial = round(0.35 * (ref_count / 10), 2)
            print(f"PARTIAL: Component 4 -- Found {ref_count}/10 references ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Found only {ref_count} references, expected 10")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: References have complete APA components (0.25 pts)
    # Check that references contain: author names, year, title (italicized text or sentence),
    # and publication venue (journal name, volume, pages)
    try:
        # Count references that have all 4 APA components:
        # 1. Author(s) with initials
        # 2. Year in parentheses
        # 3. Some title text after the year
        # 4. Publication venue with volume/pages pattern like "Journal Name, vol(issue), pages"

        # Split text into reference blocks - each reference starts with a capital letter author name
        # and contains a (year) pattern
        lines = full_text.strip().split('\n')
        # Reconstruct references by joining continuation lines
        ref_blocks = []
        current_block = ""
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            # Skip the heading line
            if re.match(r'^\s*references\s*$', stripped, re.IGNORECASE):
                continue
            # New reference starts with an author pattern (uppercase letter followed by lowercase)
            if re.match(r'^[A-Z][a-z]+,\s+[A-Z]\.', stripped) and current_block:
                ref_blocks.append(current_block.strip())
                current_block = stripped
            else:
                current_block += " " + stripped
        if current_block.strip():
            ref_blocks.append(current_block.strip())

        complete_refs = 0
        for ref in ref_blocks:
            has_author = bool(re.search(r'[A-Z][a-z]+,\s+[A-Z]\.', ref))
            has_year = bool(re.search(r'\((?:19|20)\d{2}\)', ref))
            has_venue = bool(re.search(r'[A-Z][a-z]+[\w\s:]+,\s*\d+', ref))  # Journal, volume pattern
            has_pages = bool(re.search(r'\d+[-\u2013]\d+', ref))  # page range

            if has_author and has_year and has_venue and has_pages:
                complete_refs += 1

        if complete_refs >= 8:
            print(f"PASS: Component 5 -- {complete_refs}/10 references have complete APA components (0.25 pts)")
            total_score += 0.25
        elif complete_refs >= 5:
            partial = round(0.25 * (complete_refs / 10), 2)
            print(f"PARTIAL: Component 5 -- {complete_refs}/10 complete references ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 -- Only {complete_refs} references have complete APA components")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
