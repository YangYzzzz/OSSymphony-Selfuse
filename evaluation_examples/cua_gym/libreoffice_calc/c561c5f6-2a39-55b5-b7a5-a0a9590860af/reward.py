"""
Reward Script: Fix citation errors in assignment.docx to match APA 7th edition standards
Task ID: osworld_multi_apps_misc_049
Domain: libreoffice_writer
Scoring:
  Component 1: Author name format — surnames listed first with initials after (0.35 pts)
  Component 2: Book/journal titles italicized in references (0.40 pts)
  Component 3: URL references include "Retrieved ... from" retrieval date (0.25 pts)
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_049'
FILE_PATH = '/home/user/Desktop/coursework/assignment.docx'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the References section
    ref_paragraphs = []
    in_refs = False
    for para in doc.paragraphs:
        if para.text.strip() == 'References' and para.style.name.startswith('Heading'):
            in_refs = True
            continue
        if in_refs and para.text.strip():
            ref_paragraphs.append(para)

    if not ref_paragraphs:
        print("FAIL: Could not find References section or it is empty")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(ref_paragraphs)} reference entries")
    for i, p in enumerate(ref_paragraphs):
        print(f"  ref[{i}]: {p.text[:80]!r}")

    # Component 1: Author name format — surnames listed first with initials after
    # In APA 7th edition, format is: Surname, I. I. (year)
    # Initial state (incorrect): B. S. Bloom (1984)
    # Golden state (correct):    Bloom, B. S. (1984)
    # We check that citations start with "Surname, I." pattern (surname then comma then initials)
    # rather than "I. I. Surname" pattern (initials first)
    try:
        import re
        # Pattern for correct APA surname-first format: "Word, I." at start of citation
        # A correct entry starts with e.g. "Bloom, B. S." or "Johnson, L.,"
        correct_surname_pattern = re.compile(r'^[A-Z][a-zA-Z]+,\s+[A-Z]\.')
        # Incorrect pattern: starts with initial like "B. S. Bloom" or "R. J. Means"
        incorrect_initials_pattern = re.compile(r'^[A-Z]\.\s+[A-Z]\.\s+[A-Z]')

        correct_count = 0
        incorrect_count = 0
        for ref_para in ref_paragraphs:
            text = ref_para.text.strip()
            if correct_surname_pattern.match(text):
                correct_count += 1
            elif incorrect_initials_pattern.match(text):
                incorrect_count += 1

        total_refs = len(ref_paragraphs)
        print(f"INFO: Author format — correct surname-first: {correct_count}/{total_refs}, "
              f"incorrect initials-first: {incorrect_count}/{total_refs}")

        # All references must use surname-first format, none should use initials-first
        if correct_count == total_refs and incorrect_count == 0:
            print(f"PASS: Component 1 — All {total_refs} references use surname-first APA format (0.35 pts)")
            total_score += 0.35
        elif correct_count > 0 and incorrect_count == 0:
            print(f"PARTIAL: Component 1 — {correct_count}/{total_refs} references use surname-first, "
                  f"but {total_refs - correct_count} could not be verified (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — {incorrect_count} references still use initials-first format. "
                  f"Expected: 'Bloom, B. S. (1984)...', found initials-first entries.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Book/journal/report titles italicized
    # In APA 7th edition, book titles and journal names must be italicized
    # Initial state: titles are NOT italic (italic=None for title runs)
    # Golden state: title runs have italic=True
    try:
        # Identify title runs in each reference paragraph (usually run index 1)
        # Strategy: find runs that contain the title text (typically between author/year and publisher/journal info)
        # and check if they are italic.
        italic_title_count = 0
        non_italic_title_count = 0

        # Known titles to check for italicization (based on task context and VM exploration)
        expected_italic_substrings = [
            'Educational Researcher',          # journal name in ref[0]
            'Evaluation of evidence-based',    # article title in ref[1]
            'Student success prediction',       # book title in ref[2]
            'NMC horizon report',               # book title in ref[3]
            'Online Learning',                  # journal name in ref[4]
            'The Internet and Higher Education' # journal name in ref[5]
        ]

        for ref_para in ref_paragraphs:
            for run in ref_para.runs:
                run_text = run.text.strip()
                for expected in expected_italic_substrings:
                    if expected.lower() in run_text.lower():
                        if run.italic is True:
                            italic_title_count += 1
                            print(f"  PASS: Title/journal '{run_text[:50]}' is italic")
                        else:
                            non_italic_title_count += 1
                            print(f"  FAIL: Title/journal '{run_text[:50]}' is NOT italic (italic={run.italic})")
                        break  # only count each run once

        total_title_checks = italic_title_count + non_italic_title_count
        print(f"INFO: Italic checks — {italic_title_count}/{total_title_checks} title runs correctly italicized")

        if total_title_checks > 0 and italic_title_count == total_title_checks:
            print(f"PASS: Component 2 — All {italic_title_count} book/journal titles are italicized (0.40 pts)")
            total_score += 0.40
        elif italic_title_count >= total_title_checks * 0.5 and total_title_checks > 0:
            print(f"PARTIAL: Component 2 — {italic_title_count}/{total_title_checks} titles italicized (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Only {italic_title_count}/{total_title_checks} titles italicized. "
                  f"Book and journal titles must be in italic format per APA 7th edition.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: URL references include retrieval date ("Retrieved ... from")
    # Task context: "URLs are missing retrieval dates"
    # Initial state: plain URL without retrieval date (e.g., "https://www2.ed.gov/...")
    # Golden state: "Retrieved November 15, 2024, from https://www2.ed.gov/..."
    # Two references have URLs (ref[1] and ref[4] in references section)
    try:
        import re
        # Pattern for APA 7th edition retrieval statement
        retrieval_pattern = re.compile(r'Retrieved\s+\w+\s+\d+,\s+\d{4},?\s+from\s+https?://', re.IGNORECASE)

        url_refs_with_retrieval = 0
        url_refs_without_retrieval = 0

        for ref_para in ref_paragraphs:
            text = ref_para.text
            if 'https://' in text or 'http://' in text:
                # This reference has a URL
                if retrieval_pattern.search(text):
                    url_refs_with_retrieval += 1
                    print(f"  PASS: URL reference has retrieval date: '{text[:80]}'")
                else:
                    url_refs_without_retrieval += 1
                    print(f"  FAIL: URL reference missing retrieval date: '{text[:80]}'")

        total_url_refs = url_refs_with_retrieval + url_refs_without_retrieval
        print(f"INFO: URL retrieval dates — {url_refs_with_retrieval}/{total_url_refs} URL refs have retrieval dates")

        if total_url_refs > 0 and url_refs_with_retrieval == total_url_refs:
            print(f"PASS: Component 3 — All {url_refs_with_retrieval} URL references include retrieval date (0.25 pts)")
            total_score += 0.25
        elif url_refs_with_retrieval > 0:
            print(f"PARTIAL: Component 3 — {url_refs_with_retrieval}/{total_url_refs} URL refs have retrieval dates (0.12 pts)")
            total_score += 0.12
        else:
            print(f"FAIL: Component 3 — No URL references include retrieval date. "
                  f"Expected format: 'Retrieved Month DD, YYYY, from https://...'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
