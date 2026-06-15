"""
Reward Script: Verify PDF metadata report generation
Task ID: pdf_legal_094
Domain: pdf
Scoring:
  Gate: metadata_report.txt exists (0.0 if not)
  Component 1 (0.3): Report contains all 6 PDF filenames
  Component 2 (0.4): Correct metadata (title, author, creation date) per file
  Component 3 (0.3): Correct page counts per file
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_094'
REPORT_PATH = os.path.join(WORKDIR, 'legal', 'filing_batch', 'metadata_report.txt')
PDF_DIR = os.path.join(WORKDIR, 'legal', 'filing_batch')

# Expected PDF metadata extracted from the actual files via PyMuPDF
EXPECTED_PDFS = {
    'appellate_brief_chen_v_state.pdf': {
        'title': "Appellant's Opening Brief - Chen v. State of New York",
        'author': 'Attorney Priya Narasimhan',
        'pages': 4,
    },
    'court_order_injunction_biosynth.pdf': {
        'title': 'Preliminary Injunction Order - FTC v. BioSynth Laboratories',
        'author': 'Hon. Judge Margaret Liu',
        'pages': 3,
    },
    'expert_witness_declaration_patel.pdf': {
        'title': 'Declaration of Expert Witness Dr. Rajan Patel',
        'author': 'Dr. Rajan Patel',
        'pages': 4,
    },
    'motion_to_dismiss_henderson.pdf': {
        'title': 'Motion to Dismiss - Henderson v. Pacific Northwest Industries',
        'author': 'Attorney Rachel Whitfield',
        'pages': 3,
    },
    'settlement_agreement_garcia.pdf': {
        'title': 'Settlement Agreement - Garcia v. Meridian Health Systems',
        'author': 'Mediator Douglas Tanaka',
        'pages': 5,
    },
    'subpoena_duces_tecum_morrison.pdf': {
        'title': 'Subpoena Duces Tecum - In re Morrison Financial Group Investigation',
        'author': 'Assistant U.S. Attorney Katherine Voss',
        'pages': 2,
    },
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: metadata_report.txt must exist (this is the task output)
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: Report file not found at {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(REPORT_PATH, 'r') as f:
            report_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read report file: {e}")
        print("REWARD: 0.0")
        return 0.0

    report_lower = report_content.lower()
    report_lines = [line.strip() for line in report_content.strip().split('\n') if line.strip()]

    # Component 1: Report contains all 6 PDF filenames (0.3 points)
    # Award partial: 0.05 per filename found
    try:
        filenames_found = 0
        for fname in EXPECTED_PDFS:
            if fname.lower() in report_lower:
                filenames_found += 1
            else:
                print(f"FAIL: Component 1 — filename '{fname}' not found in report")

        if filenames_found == 6:
            print(f"PASS: Component 1 — all 6 PDF filenames present ({0.3} pts)")
            total_score += 0.3
        elif filenames_found > 0:
            partial = round(0.05 * filenames_found, 2)
            print(f"PARTIAL: Component 1 — {filenames_found}/6 filenames found ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 1 — no PDF filenames found in report")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct metadata (title, author, creation date) per file (0.4 points)
    # For each file, check if its title and author appear in the same line or report
    # Award ~0.067 per file with correct metadata
    try:
        metadata_score = 0
        per_file_weight = 0.4 / 6.0

        for fname, meta in EXPECTED_PDFS.items():
            # Find the line(s) containing this filename
            matching_lines = [line for line in report_lines if fname.lower() in line.lower()]
            if not matching_lines:
                print(f"FAIL: Component 2 — no line found for '{fname}'")
                continue

            # Check the line(s) for title and author
            combined = ' '.join(matching_lines).lower()
            title_found = meta['title'].lower() in combined
            author_found = meta['author'].lower() in combined
            # Check for some date-like content (any date reference)
            has_date = any(c.isdigit() for c in combined) and ('20' in combined or 'date' in combined.lower())

            checks_passed = sum([title_found, author_found, has_date])
            if checks_passed == 3:
                metadata_score += 1
                print(f"PASS: Component 2 — '{fname}': title, author, date all present")
            elif checks_passed > 0:
                metadata_score += checks_passed / 3.0
                missing = []
                if not title_found:
                    missing.append('title')
                if not author_found:
                    missing.append('author')
                if not has_date:
                    missing.append('date')
                print(f"PARTIAL: Component 2 — '{fname}': missing {missing}")
            else:
                print(f"FAIL: Component 2 — '{fname}': no metadata found")

        comp2_points = round(per_file_weight * metadata_score, 4)
        if comp2_points > 0:
            print(f"PASS: Component 2 — metadata score: {comp2_points:.2f}/{0.4} pts")
            total_score += comp2_points
        else:
            print("FAIL: Component 2 — no metadata verified")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct page counts per file (0.3 points)
    # Award 0.05 per file with correct page count
    try:
        pages_correct = 0
        per_file_weight_pages = 0.3 / 6.0

        for fname, meta in EXPECTED_PDFS.items():
            expected_pages = meta['pages']
            matching_lines = [line for line in report_lines if fname.lower() in line.lower()]
            if not matching_lines:
                print(f"FAIL: Component 3 — no line found for '{fname}'")
                continue

            combined = ' '.join(matching_lines)
            # Check if the expected page count appears in the line
            if str(expected_pages) in combined:
                pages_correct += 1
                print(f"PASS: Component 3 — '{fname}': page count {expected_pages} found")
            else:
                print(f"FAIL: Component 3 — '{fname}': expected page count {expected_pages} not in line")

        comp3_points = round(per_file_weight_pages * pages_correct, 4)
        if comp3_points > 0:
            print(f"PASS: Component 3 — page count score: {comp3_points:.2f}/{0.3} pts")
            total_score += comp3_points
        else:
            print("FAIL: Component 3 — no page counts verified")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
