"""
Reward Script: Literature review co-author lookup task
Task ID: osworld_multi_apps_paper_scholar_browse_014
Domain: multi_apps (LibreOffice Writer + Chrome + PDF)
Scoring:
  - Component 1 (0.4): All 3 numbered list items have non-empty co-author names filled in
  - Component 2 (0.3): At least one of the expected Ion Stoica co-authors is present (Scott Shenker)
  - Component 3 (0.3): All 3 expected co-author names (Scott Shenker, Sylvia Ratnasamy, Joseph M. Hellerstein) are present

Task: The user opened a PDF of the Chord paper (corresponding author: Ion Stoica), searched
Google Scholar for Ion Stoica's co-authors, and wrote the top 3 co-author names into the Writer document.
Initial state: The docx has empty numbered lines "1. ", "2. ", "3. "
Golden state: The docx has "1. Scott Shenker", "2. Sylvia Ratnasamy", "3. Joseph M. Hellerstein"
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_014'

# Expected co-authors from Ion Stoica's Google Scholar profile (top 3 most frequent)
EXPECTED_COAUTHORS = ['Scott Shenker', 'Sylvia Ratnasamy', 'Joseph M. Hellerstein']


def normalize_name(name):
    """Normalize a name for comparison (strip whitespace, lowercase)."""
    return name.strip().lower()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Fill in 3 co-author names of Ion Stoica (corresponding author of Chord paper)
    from Google Scholar into the Writer document.
    """
    total_score = 0.0

    # Load the docx document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract paragraph texts
    paragraphs = [para.text for para in doc.paragraphs]
    print(f"INFO: Document has {len(paragraphs)} paragraphs")
    for i, p in enumerate(paragraphs):
        print(f"  Para {i}: {repr(p)}")

    # Find the numbered list items (paragraphs starting with "1. ", "2. ", "3. ")
    numbered_entries = {}
    for para in paragraphs:
        text = para.strip()
        for num in [1, 2, 3]:
            prefix = f"{num}. "
            if text.startswith(prefix):
                content = text[len(prefix):].strip()
                numbered_entries[num] = content
                break

    print(f"INFO: Numbered entries found: {numbered_entries}")

    # Component 1: All 3 numbered items have non-empty names (0.4 points)
    # In initial state: entries are empty strings after the "X. " prefix
    # In golden state: entries have actual co-author names
    try:
        filled_count = sum(1 for num in [1, 2, 3] if numbered_entries.get(num, ''))
        if filled_count == 3:
            print(f"PASS: Component 1 — All 3 numbered items have co-author names filled in (0.4 pts)")
            total_score += 0.4
        elif filled_count > 0:
            partial = 0.4 * (filled_count / 3)
            print(f"PARTIAL: Component 1 — {filled_count}/3 numbered items have names filled in ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No co-author names found in numbered list items (expected 3, found 0)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Ion Stoica's primary co-author (Scott Shenker) is present (0.3 points)
    # This verifies the agent found the right person's Google Scholar profile
    try:
        all_text = ' '.join(paragraphs).lower()
        shenker_present = 'scott shenker' in all_text
        if shenker_present:
            print(f"PASS: Component 2 — 'Scott Shenker' found in document (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 'Scott Shenker' (Ion Stoica top co-author) not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 expected co-author names are present (0.3 points)
    # Verifies that all specific co-authors from Ion Stoica's Scholar profile are listed
    try:
        all_text_lower = ' '.join(paragraphs).lower()
        expected_lower = [normalize_name(name) for name in EXPECTED_COAUTHORS]
        found_all = all(name in all_text_lower for name in expected_lower)
        found_names = [name for name in EXPECTED_COAUTHORS if normalize_name(name) in all_text_lower]

        if found_all:
            print(f"PASS: Component 3 — All 3 expected co-authors found: {EXPECTED_COAUTHORS} (0.3 pts)")
            total_score += 0.3
        else:
            missing = [name for name in EXPECTED_COAUTHORS if normalize_name(name) not in all_text_lower]
            print(f"FAIL: Component 3 — Missing expected co-authors: {missing} (found: {found_names})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
