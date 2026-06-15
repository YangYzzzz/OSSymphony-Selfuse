"""
Reward Script: TV Series IMDB Lookup — Most First-Season Episodes
Task ID: osworld_multi_apps_book_reading_rate_006
Domain: libreoffice_calc / libreoffice_writer (multi-app)

Task: Look up Season 1 episode counts for 5 TV series on IMDB, identify the
series with the most first-season episodes, and write its name in
most_episodes.docx on the Desktop.

Expected: most_episodes.docx contains the name of the series with the most
Season 1 episodes. Per IMDB data, Succession has 10 episodes (Season 1),
tied with House of the Dragon (10 episodes). The golden file uses 'Succession'.

Scoring:
  Component 1: most_episodes.docx exists and is non-empty              (0.3 pts)
  Component 2: Document contains a recognizable TV series name         (0.3 pts)
  Component 3: Document contains the correct series with most episodes (0.4 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_reading_rate_006'
DOCX_PATH = f'{WORKDIR}/Desktop/most_episodes.docx'

# All valid series in the task
VALID_SERIES = [
    'succession',
    'the white lotus',
    'euphoria',
    'yellowstone',
    'house of the dragon',
]

# Series with the most first-season episodes per IMDB data in golden file:
# Succession: 10 episodes, House of the Dragon: 10 episodes
# The context also mentions Yellowstone (9 eps) as potentially acceptable due to
# IMDB data variation, but primarily we accept the top-episode series.
# Accept both 10-episode tied leaders and Yellowstone as a near-miss acceptable answer.
CORRECT_ANSWERS = [
    'succession',         # 10 episodes Season 1 (correct per golden file)
    'house of the dragon', # 10 episodes Season 1 (tied per golden file data)
]


def verify_task(docx_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(docx_path):
        print(f"CRITICAL: most_episodes.docx not found at {docx_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the document
    try:
        from docx import Document
        doc = Document(docx_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load {docx_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the document (all paragraphs)
    all_text_parts = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    full_text = ' '.join(all_text_parts).strip()
    full_text_lower = full_text.lower()

    print(f"Document text: {repr(full_text)}")
    print(f"Number of non-empty paragraphs: {len(all_text_parts)}")

    # Component 1: Document is non-empty and contains some text (0.3 points)
    # This checks that the agent actually wrote something in the document
    # (initial_env has an empty document, so this FAILS on initial and PASSES on golden)
    try:
        if full_text and len(full_text) >= 2:
            print(f"PASS: Component 1 — Document is non-empty, text found: {repr(full_text[:80])} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Document is empty or nearly empty (found: {repr(full_text)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document contains a recognizable TV series name from the list (0.3 points)
    # This checks that the agent wrote a valid series name (not random text)
    # (initial_env is empty, so this FAILS on initial and PASSES on golden)
    try:
        found_series = None
        for series in VALID_SERIES:
            if series in full_text_lower:
                found_series = series
                break
        if found_series is not None:
            print(f"PASS: Component 2 — Valid TV series name found: '{found_series}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No recognizable TV series from the list found in: {repr(full_text)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document contains the correct answer — series with MOST first-season episodes (0.4 points)
    # Per IMDB: Succession (10 eps) and House of the Dragon (10 eps) are tied for most.
    # The golden file contains 'Succession'. We accept both 10-episode leaders.
    # (initial_env is empty, so this FAILS on initial and PASSES on golden)
    try:
        matched_answer = next(
            (s for s in CORRECT_ANSWERS if s in full_text_lower),
            None
        )
        if matched_answer is not None:
            print(f"PASS: Component 3 — Correct series (most first-season episodes) identified: '{matched_answer}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 — Expected one of {CORRECT_ANSWERS}, found: {repr(full_text)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical artifact path on the VM
if not os.path.exists(DOCX_PATH):
    print(f"File not found: {DOCX_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DOCX_PATH)
