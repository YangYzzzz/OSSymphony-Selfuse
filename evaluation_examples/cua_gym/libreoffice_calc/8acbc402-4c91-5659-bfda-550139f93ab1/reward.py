"""
Reward Script: Word Frequency Python Script Task
Task ID: osworld_multi_apps_code_script_output_006
Domain: os (Python scripting)
Scoring:
  Component 1: word_freq.txt exists and has exactly 10 lines (0.3 pts)
  Component 2: All lines match 'word: count' format (0.2 pts)
  Component 3: Top words and counts are correct (case-insensitive, alphabetic-only) (0.3 pts)
  Component 4: Lines are sorted in descending order by count (0.2 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_006'

WORD_FREQ_PATH = '/home/user/data/word_freq.txt'
ARTICLE_PATH = '/home/user/data/article.txt'

# Ground truth top-10 words computed from article.txt using the same algorithm:
# re.findall(r'[a-zA-Z]+', text.lower()), sorted descending by count
# Verified against golden_env output:
# and: 26, the: 18, of: 15, to: 12, energy: 12,
# more: 9, technology: 8, in: 8, are: 8, climate: 7
EXPECTED_TOP10 = [
    ("and", 26),
    ("the", 18),
    ("of", 15),
    ("to", 12),
    ("energy", 12),
    ("more", 9),
    ("technology", 8),
    ("in", 8),
    ("are", 8),
    ("climate", 7),
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: word_freq.txt must exist to score any points
    if not os.path.isfile(WORD_FREQ_PATH):
        print(f"FAIL: word_freq.txt not found at {WORD_FREQ_PATH}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the output file
    try:
        with open(WORD_FREQ_PATH, 'r') as f:
            content = f.read()
        lines = [line for line in content.splitlines() if line.strip()]
    except Exception as e:
        print(f"CRITICAL: Cannot read {WORD_FREQ_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: word_freq.txt exists and has exactly 10 lines (0.3 pts)
    try:
        line_count = len(lines)
        if line_count == 10:
            print(f"PASS: Component 1 — word_freq.txt exists with exactly 10 lines (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected 10 lines, found {line_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All lines match 'word: count' format (0.2 pts)
    try:
        pattern = re.compile(r'^[a-z]+:\s*\d+$')
        malformed = [line for line in lines if not pattern.match(line.strip())]
        if not malformed:
            print(f"PASS: Component 2 — all lines match 'word: count' format (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — {len(malformed)} lines have incorrect format: {malformed[:3]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Parse lines into (word, count) tuples for components 3 and 4
    parsed = []
    try:
        for line in lines:
            m = re.match(r'^([a-z]+):\s*(\d+)$', line.strip())
            if m:
                parsed.append((m.group(1), int(m.group(2))))
    except Exception as e:
        print(f"ERROR: Parsing lines for components 3/4 — {e}")

    # Component 3: Top words and counts match ground truth (0.3 pts)
    # We verify that the set of (word, count) pairs matches exactly the expected top-10
    try:
        parsed_set = set(parsed)
        expected_set = set(EXPECTED_TOP10)
        matching = parsed_set & expected_set
        match_fraction = len(matching) / len(expected_set)
        if match_fraction == 1.0:
            print(f"PASS: Component 3 — all 10 (word, count) pairs match ground truth (0.3 pts)")
            total_score += 0.3
        elif match_fraction >= 0.8:
            partial = round(0.3 * match_fraction, 2)
            print(f"PARTIAL: Component 3 — {len(matching)}/10 pairs match ground truth ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — only {len(matching)}/10 (word, count) pairs match ground truth")
            print(f"  Expected: {sorted(EXPECTED_TOP10, key=lambda x: -x[1])}")
            print(f"  Found:    {sorted(parsed, key=lambda x: -x[1])}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Lines are sorted in descending order by count (0.2 pts)
    # This verifies the sort is correct — lines must be ordered from highest to lowest count
    try:
        if len(parsed) >= 2:
            counts = [c for _, c in parsed]
            is_sorted_desc = all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1))
            if is_sorted_desc:
                print(f"PASS: Component 4 — lines are sorted descending by count (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — lines are NOT sorted descending: {counts}")
        else:
            print(f"FAIL: Component 4 — not enough lines to check sort order ({len(parsed)} lines parsed)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
