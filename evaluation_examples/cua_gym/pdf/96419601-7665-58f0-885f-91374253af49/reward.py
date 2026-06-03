"""
Reward Script: Extract text and metadata from a PDF
Task ID: pdf_ro_010
Domain: pdf
Scoring:
  Component 1 (0.30): research_paper.txt exists with substantial text from all pages
  Component 2 (0.20): research_paper.txt preserves paragraph breaks and contains key content
  Component 3 (0.15): Metadata file has correct Title
  Component 4 (0.10): Metadata file has correct Author
  Component 5 (0.10): Metadata file has correct Creation Date
  Component 6 (0.15): Metadata file has correct Page Count
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_010'

TXT_PATH = os.path.join(WORKDIR, 'Documents', 'research_paper.txt')
META_PATH = os.path.join(WORKDIR, 'Documents', 'research_paper_metadata.txt')
PDF_PATH = os.path.join(WORKDIR, 'Documents', 'research_paper.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: the PDF must still exist (not a scoring component)
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: Source PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: research_paper.txt exists with substantial text
    #   from all 22 pages (0.30 points)
    #   - Must NOT exist on initial_env (only the PDF exists initially)
    # ---------------------------------------------------------------
    try:
        if os.path.exists(TXT_PATH):
            with open(TXT_PATH, 'r', encoding='utf-8', errors='replace') as f:
                txt_content = f.read()
            # The golden file is ~28KB / 371 lines. Require at least 10KB
            # to confirm substantial extraction (not a stub).
            if len(txt_content) >= 10000:
                print(f"PASS: Component 1 — research_paper.txt exists with {len(txt_content)} chars (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — research_paper.txt too small: {len(txt_content)} chars (need >=10000)")
        else:
            txt_content = ""
            print(f"FAIL: Component 1 — research_paper.txt not found at {TXT_PATH}")
    except Exception as e:
        txt_content = ""
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: Text content preserves paragraph breaks and
    #   contains key phrases from the paper (0.20 points)
    # ---------------------------------------------------------------
    try:
        if txt_content:
            checks_passed = 0
            total_checks = 4

            # Check paragraph breaks (multiple consecutive newlines)
            if '\n\n' in txt_content or '\n \n' in txt_content:
                checks_passed += 1

            # Check key phrases from different parts of the paper
            key_phrases = [
                'Machine Learning in Healthcare',      # title / early
                'Abstract',                             # beginning
                'Introduction',                         # section 1
                'Background',                           # section 2
            ]
            matched_phrases = sum(1 for p in key_phrases if p in txt_content)
            if matched_phrases >= 3:
                checks_passed += 1

            # Check content from later in the paper (not just page 1)
            later_phrases = [
                'deep learning',
                'clinical',
                'patient',
            ]
            matched_later = sum(1 for p in later_phrases if p.lower() in txt_content.lower())
            if matched_later >= 2:
                checks_passed += 1

            # Check that there are enough lines (paragraph breaks preserved)
            line_count = len(txt_content.strip().split('\n'))
            if line_count >= 50:
                checks_passed += 1

            component2_score = 0.20 * (checks_passed / total_checks)
            if component2_score > 0:
                print(f"PASS: Component 2 — text quality {checks_passed}/{total_checks} checks ({component2_score:.2f} pts)")
                total_score += component2_score
            else:
                print(f"FAIL: Component 2 — text quality 0/{total_checks} checks")
        else:
            print(f"FAIL: Component 2 — no text content to evaluate")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Read metadata file for components 3-6
    # ---------------------------------------------------------------
    meta_content = ""
    meta_lines = {}
    try:
        if os.path.exists(META_PATH):
            with open(META_PATH, 'r', encoding='utf-8', errors='replace') as f:
                meta_content = f.read()
            # Parse key: value lines
            for line in meta_content.strip().split('\n'):
                if ':' in line:
                    key, _, value = line.partition(':')
                    meta_lines[key.strip().lower()] = value.strip()
        else:
            print(f"FAIL: Metadata file not found at {META_PATH}")
    except Exception as e:
        print(f"ERROR: Reading metadata file — {e}")

    # ---------------------------------------------------------------
    # Component 3: Metadata file has correct Title (0.15 points)
    # ---------------------------------------------------------------
    try:
        if 'title' in meta_lines:
            title_val = meta_lines['title']
            if 'Machine Learning in Healthcare' in title_val:
                print(f"PASS: Component 3 — Title correct: '{title_val}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Title mismatch: '{title_val}' (expected 'Machine Learning in Healthcare')")
        else:
            print(f"FAIL: Component 3 — 'Title' key not found in metadata file")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Metadata file has correct Author (0.10 points)
    # ---------------------------------------------------------------
    try:
        if 'author' in meta_lines:
            author_val = meta_lines['author']
            if 'Dr. Sarah Thompson' in author_val:
                print(f"PASS: Component 4 — Author correct: '{author_val}' (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Author mismatch: '{author_val}' (expected 'Dr. Sarah Thompson')")
        else:
            print(f"FAIL: Component 4 — 'Author' key not found in metadata file")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---------------------------------------------------------------
    # Component 5: Metadata file has correct Creation Date (0.10 pts)
    # ---------------------------------------------------------------
    try:
        if 'creation date' in meta_lines:
            date_val = meta_lines['creation date']
            if '2025-11-15' in date_val or '2025/11/15' in date_val or 'November 15, 2025' in date_val or '15/11/2025' in date_val:
                print(f"PASS: Component 5 — Creation Date correct: '{date_val}' (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Creation Date mismatch: '{date_val}' (expected contains '2025-11-15')")
        else:
            print(f"FAIL: Component 5 — 'Creation Date' key not found in metadata file")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ---------------------------------------------------------------
    # Component 6: Metadata file has correct Page Count (0.15 points)
    # ---------------------------------------------------------------
    try:
        if 'page count' in meta_lines:
            pc_val = meta_lines['page count']
            if '22' in pc_val:
                print(f"PASS: Component 6 — Page Count correct: '{pc_val}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — Page Count mismatch: '{pc_val}' (expected '22')")
        else:
            print(f"FAIL: Component 6 — 'Page Count' key not found in metadata file")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
