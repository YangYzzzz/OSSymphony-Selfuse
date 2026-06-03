"""
Reward Script: Word frequency analysis from legal brief PDF
Task ID: pdf_legal_089
Domain: pdf
Scoring:
  - Component 1: Output file exists and is non-empty (0.10)
  - Component 2: Contains header with source info and stop words note (0.15)
  - Component 3: Contains exactly 50 word entries (0.25)
  - Component 4: Words are sorted by frequency descending (0.20)
  - Component 5: Top words match expected legal brief vocabulary (0.15)
  - Component 6: Each entry has rank, word, and numeric count (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_089'
OUTPUT_FILE = os.path.join(WORKDIR, 'legal', 'opposing', 'word_analysis.txt')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist (this IS task-introduced — file doesn't exist before task)
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(file_path, 'r', encoding='utf-8', errors='replace').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(content.strip()) == 0:
        print("CRITICAL: Output file is empty")
        print("REWARD: 0.0")
        return 0.0

    lines = content.strip().split('\n')

    # Component 1: Output file exists and has meaningful content (0.10 points)
    # This is task-introduced: the file does not exist in initial_env
    try:
        if len(content.strip()) > 100:
            print(f"PASS: Component 1 — Output file exists with {len(content)} chars (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — File too small ({len(content)} chars), expected substantial content")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header contains source info and stop words note (0.15 points)
    try:
        header_text = '\n'.join(lines[:10]).lower()
        has_source = 'brief.pdf' in header_text or 'source' in header_text
        has_stop_words = 'stop' in header_text
        has_word_count = any(c.isdigit() for c in header_text)

        checks_passed = sum([has_source, has_stop_words, has_word_count])
        if checks_passed >= 2:
            print(f"PASS: Component 2 — Header has source info ({has_source}), stop words note ({has_stop_words}), word count ({has_word_count}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Header missing info. source={has_source}, stop_words={has_stop_words}, word_count={has_word_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Contains exactly 50 word entries (0.25 points)
    # Parse lines that look like ranked word entries: number, word, count
    try:
        word_entries = []
        for line in lines:
            line_stripped = line.strip()
            # Match patterns like "1     plaintiff                     66"
            # or "1. plaintiff 66" or "1  plaintiff  66"
            match = re.match(r'^\s*(\d+)[.\s]+([a-zA-Z_]+(?:[a-zA-Z_\-]*[a-zA-Z_])?)\s+(\d+)\s*$', line_stripped)
            if match:
                rank = int(match.group(1))
                word = match.group(2).lower()
                count = int(match.group(3))
                word_entries.append((rank, word, count))

        num_entries = len(word_entries)
        if num_entries == 50:
            print(f"PASS: Component 3 — Exactly 50 word entries found (0.25 pts)")
            total_score += 0.25
        elif 45 <= num_entries <= 55:
            partial = 0.15
            print(f"PARTIAL: Component 3 — {num_entries} entries (expected 50), awarding {partial} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Found {num_entries} word entries, expected 50")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Words are sorted by frequency descending (0.20 points)
    try:
        if len(word_entries) >= 10:
            counts = [entry[2] for entry in word_entries]
            is_descending = all(counts[i] >= counts[i+1] for i in range(len(counts) - 1))
            if is_descending:
                print(f"PASS: Component 4 — Words sorted by frequency descending (0.20 pts)")
                total_score += 0.20
            else:
                # Check if mostly sorted (allow minor ties/inversions)
                inversions = sum(1 for i in range(len(counts)-1) if counts[i] < counts[i+1])
                if inversions <= 2:
                    partial = 0.10
                    print(f"PARTIAL: Component 4 — {inversions} inversions in sort order, awarding {partial} pts")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — {inversions} inversions in sort order, not properly sorted")
        else:
            print(f"FAIL: Component 4 — Not enough word entries ({len(word_entries)}) to verify sort order")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Top words match expected legal brief vocabulary (0.15 points)
    # The legal brief is about patent/pharmaceutical litigation. Key terms should appear.
    try:
        if len(word_entries) >= 10:
            top_words = set(entry[1] for entry in word_entries[:15])
            # Expected key legal terms from the brief
            expected_legal_terms = {'plaintiff', 'patent', 'defendant', 'claim', 'injunction', 'market'}
            matches = top_words & expected_legal_terms
            if len(matches) >= 3:
                print(f"PASS: Component 5 — Top words contain legal terms: {matches} (0.15 pts)")
                total_score += 0.15
            elif len(matches) >= 1:
                partial = 0.07
                print(f"PARTIAL: Component 5 — Some legal terms found: {matches}, awarding {partial} pts")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Top words {top_words} don't match expected legal terms")
        else:
            print(f"FAIL: Component 5 — Not enough entries to verify vocabulary")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Each entry has rank, word, and numeric count format (0.15 points)
    try:
        if len(word_entries) >= 40:
            # Check that ranks are sequential 1..N
            ranks = [entry[0] for entry in word_entries]
            expected_ranks = list(range(1, len(word_entries) + 1))
            if ranks == expected_ranks:
                print(f"PASS: Component 6 — All entries have sequential ranks 1-{len(word_entries)} with word and count (0.15 pts)")
                total_score += 0.15
            else:
                # Still give partial credit if entries parse correctly
                partial = 0.08
                print(f"PARTIAL: Component 6 — Entries parsed but ranks not sequential (found {ranks[:5]}...), awarding {partial} pts")
                total_score += partial
        else:
            print(f"FAIL: Component 6 — Only {len(word_entries)} parseable entries, expected ~50")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
