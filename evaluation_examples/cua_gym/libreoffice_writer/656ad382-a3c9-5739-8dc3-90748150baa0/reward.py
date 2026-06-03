"""
Reward Script: Continuous footnote numbering across master document subdocuments
Task ID: writer_rm_082
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): start-value in styles.xml forms a continuous sequence across chapters
  Component 2 (0.5): Citation numbers in content.xml are actually continuous (no restarts)
  Precondition gate: All 39 footnotes must be preserved (no scoring, just early exit if broken)
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_082'

# Expected chapter footnote counts (from task context)
CHAPTER_COUNTS = [5, 8, 7, 5, 6, 8]  # Ch1-Ch6
TOTAL_FOOTNOTES = sum(CHAPTER_COUNTS)  # 39


def get_start_value(odt_path):
    """Extract text:start-value from footnote notes-configuration in styles.xml."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        styles = z.read('styles.xml').decode('utf-8')
        match = re.search(r'text:start-value="(\d+)"', styles)
        if match:
            return int(match.group(1))
    return None


def get_citation_numbers(odt_path):
    """Extract all footnote citation numbers from content.xml."""
    with zipfile.ZipFile(odt_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')
        citations = re.findall(
            r'<text:note-citation[^>]*>(\d+)</text:note-citation>',
            content
        )
        return [int(c) for c in citations]


def verify_task():
    """
    Verify continuous footnote numbering across all subdocuments.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: all 6 chapter files must exist
    chapter_files = []
    for ch in range(1, 7):
        fpath = os.path.join(WORKDIR, f'Chapter{ch}.odt')
        if not os.path.exists(fpath):
            print(f"CRITICAL: Chapter{ch}.odt not found at {fpath}")
            print("REWARD: 0.0")
            return 0.0
        chapter_files.append(fpath)

    # Precondition gate: footnote count must be preserved
    # This is NOT a scoring component -- it's a gate to ensure no data corruption
    all_citations = []
    per_chapter_citations = []
    for fpath in chapter_files:
        cites = get_citation_numbers(fpath)
        per_chapter_citations.append(cites)
        all_citations.extend(cites)

    per_ch_counts = [len(c) for c in per_chapter_citations]
    if per_ch_counts != CHAPTER_COUNTS:
        print(f"PRECONDITION FAIL: Footnote counts changed. Expected {CHAPTER_COUNTS}, got {per_ch_counts}")
        print("REWARD: 0.0")
        return 0.0
    print(f"PRECONDITION OK: All {TOTAL_FOOTNOTES} footnotes preserved across 6 chapters")

    # Component 1: start-value configuration forms continuous sequence (0.5 points)
    # Initial state: all chapters have start-value=0 (each restarts at footnote 1)
    # Golden state: Ch1=0, Ch2=5, Ch3=13, Ch4=20, Ch5=25, Ch6=31
    # The key change: chapters 2-6 must have non-zero start-values that equal
    # the cumulative footnote count of all preceding chapters.
    try:
        start_values = []
        for fpath in chapter_files:
            sv = get_start_value(fpath)
            start_values.append(sv)

        print(f"  Start-values: {start_values}")

        # Expected start-values for continuous numbering
        expected_start_values = []
        cumulative = 0
        for count in CHAPTER_COUNTS:
            expected_start_values.append(cumulative)
            cumulative += count

        # Count how many chapters (2-6) have correct non-zero start-values
        # Chapter 1 has start-value=0 in both initial and golden, so we only
        # score chapters 2-6 (the actual changes)
        correct_chapters = 0
        scorable_chapters = 5  # chapters 2-6
        for i in range(1, 6):
            if start_values[i] == expected_start_values[i]:
                correct_chapters += 1
                print(f"  Chapter{i+1}: start-value={start_values[i]} == expected {expected_start_values[i]} -- CORRECT")
            else:
                print(f"  Chapter{i+1}: start-value={start_values[i]} != expected {expected_start_values[i]} -- WRONG")

        if correct_chapters == scorable_chapters:
            print(f"PASS: Component 1 -- All start-values match continuous sequence (0.5 pts)")
            total_score += 0.5
        elif correct_chapters > 0:
            partial = 0.5 * (correct_chapters / scorable_chapters)
            print(f"PARTIAL: Component 1 -- {correct_chapters}/{scorable_chapters} chapters correct ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No chapters have correct start-values")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Citation numbers are continuous across chapters (0.5 points)
    # Initial state: each chapter restarts at 1 (1,2,3.. then 1,2,3.. etc.)
    # Golden state: continuous sequence 1,2,...,39
    # The key change: chapters 2-6 have renumbered citations instead of restarting.
    try:
        print(f"  All citations collected: {all_citations}")

        expected_sequence = list(range(1, TOTAL_FOOTNOTES + 1))
        if all_citations == expected_sequence:
            print(f"PASS: Component 2 -- Citations form continuous sequence 1-{TOTAL_FOOTNOTES} (0.5 pts)")
            total_score += 0.5
        else:
            # Partial credit: count how many chapter boundaries have continuous numbering
            continuous_boundaries = 0
            total_boundaries = 5  # between 6 chapters
            for i in range(len(per_chapter_citations) - 1):
                if per_chapter_citations[i] and per_chapter_citations[i + 1]:
                    last_of_prev = per_chapter_citations[i][-1]
                    first_of_next = per_chapter_citations[i + 1][0]
                    if first_of_next == last_of_prev + 1:
                        continuous_boundaries += 1
                        print(f"  Boundary Ch{i+1}->Ch{i+2}: continuous ({last_of_prev} -> {first_of_next})")
                    else:
                        print(f"  Boundary Ch{i+1}->Ch{i+2}: BREAK ({last_of_prev} -> {first_of_next})")

            if continuous_boundaries > 0:
                partial = 0.5 * (continuous_boundaries / total_boundaries)
                print(f"PARTIAL: Component 2 -- {continuous_boundaries}/{total_boundaries} boundaries continuous ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- No continuous boundaries found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
