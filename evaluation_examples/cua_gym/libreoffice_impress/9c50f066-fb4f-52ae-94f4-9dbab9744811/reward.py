"""
Reward Script: Presentation Audit Report Generation
Task ID: impress_gf5_043
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.15): Audit file exists with 4 sections
  - Component 2 (0.20): Section 1 - slides with no speaker notes correctly identified
  - Component 3 (0.20): Section 2 - overloaded slides (>100 words) correctly identified
  - Component 4 (0.20): Section 3 - slides with no images correctly identified
  - Component 5 (0.15): Section 4 - slides with long titles correctly identified
  - Component 6 (0.10): Summary line with correct totals
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_gf5_043'
AUDIT_FILE = f'{WORKDIR}/presentation_audit.txt'

# Expected ground truth values derived from the 20-slide presentation:
# Section 1 (No speaker notes): slides 2, 5, 8, 11, 14, 17 (count=6)
# Section 2 (Overloaded >100 words): slides 3, 7, 12, 16 (count=4)
# Section 3 (No images): slides 1, 4, 6, 9, 10, 13, 15, 18 (count=8)
# Section 4 (Title >60 chars): slides 4, 10, 19 (count=3)
# Total issues: 6+4+8+3 = 21

EXPECTED_NO_NOTES = {2, 5, 8, 11, 14, 17}
EXPECTED_OVERLOADED = {3, 7, 12, 16}
EXPECTED_NO_IMAGES = {1, 4, 6, 9, 10, 13, 15, 18}
EXPECTED_LONG_TITLES = {4, 10, 19}
EXPECTED_TOTAL_ISSUES = 21


def extract_slide_numbers(text):
    """Extract slide numbers from a line like 'Slides: 2, 5, 8, 11'."""
    numbers = set()
    # Find numbers after "Slides:" or "slides:" pattern
    match = re.search(r'[Ss]lides?:\s*([\d,\s]+)', text)
    if match:
        nums_str = match.group(1)
        for n in re.findall(r'\d+', nums_str):
            numbers.add(int(n))
    return numbers


def extract_count(text):
    """Extract count from a line like 'Count: 6'."""
    match = re.search(r'[Cc]ount:\s*(\d+)', text)
    if match:
        return int(match.group(1))
    return None


def parse_section(lines, section_start_idx, next_section_idx=None):
    """Parse a section starting at the given line index up to next_section_idx.
    Returns (slide_numbers_set, count_int)."""
    slides = set()
    count = None
    end_idx = next_section_idx if next_section_idx is not None else min(section_start_idx + 15, len(lines))
    for i in range(section_start_idx, end_idx):
        line = lines[i]
        s = extract_slide_numbers(line)
        if s:
            slides = s
        c = extract_count(line)
        if c is not None:
            count = c
    return slides, count


def verify_task():
    """
    Verify that the presentation audit report was correctly generated.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: audit file must exist
    if not os.path.exists(AUDIT_FILE):
        print(f"CRITICAL: Audit file not found: {AUDIT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(AUDIT_FILE).read()
        lines = content.strip().split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read audit file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File structure - has 4 sections (0.15 points)
    try:
        section_count = 0
        section_indices = []
        for i, line in enumerate(lines):
            if re.search(r'[Ss]ection\s+\d+', line):
                section_count += 1
                section_indices.append(i)

        if section_count >= 4:
            print(f"PASS: Component 1 — Audit file has {section_count} sections (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 4 sections, found {section_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        section_indices = []

    # Build section boundaries for accurate parsing
    section_bounds = []
    for idx_i, si in enumerate(section_indices):
        next_si = section_indices[idx_i + 1] if idx_i + 1 < len(section_indices) else len(lines)
        section_bounds.append((si, next_si))

    # Component 2: Section 1 - No Speaker Notes (0.20 points)
    try:
        if len(section_bounds) >= 1:
            slides, count = parse_section(lines, section_bounds[0][0], section_bounds[0][1])
            slides_match = (slides == EXPECTED_NO_NOTES)
            count_match = (count == len(EXPECTED_NO_NOTES))
            if slides_match and count_match:
                print(f"PASS: Component 2 — No-notes slides correct: {sorted(slides)}, count={count} (0.20 pts)")
                total_score += 0.20
            elif slides_match or count_match:
                print(f"PARTIAL: Component 2 — slides={sorted(slides)} (exp {sorted(EXPECTED_NO_NOTES)}), count={count} (exp {len(EXPECTED_NO_NOTES)}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — slides={sorted(slides)} (exp {sorted(EXPECTED_NO_NOTES)}), count={count} (exp {len(EXPECTED_NO_NOTES)})")
        else:
            print("FAIL: Component 2 — No sections found in audit file")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Section 2 - Overloaded Slides (0.20 points)
    try:
        if len(section_bounds) >= 2:
            slides, count = parse_section(lines, section_bounds[1][0], section_bounds[1][1])
            slides_match = (slides == EXPECTED_OVERLOADED)
            count_match = (count == len(EXPECTED_OVERLOADED))
            if slides_match and count_match:
                print(f"PASS: Component 3 — Overloaded slides correct: {sorted(slides)}, count={count} (0.20 pts)")
                total_score += 0.20
            elif slides_match or count_match:
                print(f"PARTIAL: Component 3 — slides={sorted(slides)} (exp {sorted(EXPECTED_OVERLOADED)}), count={count} (exp {len(EXPECTED_OVERLOADED)}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — slides={sorted(slides)} (exp {sorted(EXPECTED_OVERLOADED)}), count={count} (exp {len(EXPECTED_OVERLOADED)})")
        else:
            print("FAIL: Component 3 — Section 2 not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Section 3 - No Images (0.20 points)
    try:
        if len(section_bounds) >= 3:
            slides, count = parse_section(lines, section_bounds[2][0], section_bounds[2][1])
            slides_match = (slides == EXPECTED_NO_IMAGES)
            count_match = (count == len(EXPECTED_NO_IMAGES))
            if slides_match and count_match:
                print(f"PASS: Component 4 — No-images slides correct: {sorted(slides)}, count={count} (0.20 pts)")
                total_score += 0.20
            elif slides_match or count_match:
                print(f"PARTIAL: Component 4 — slides={sorted(slides)} (exp {sorted(EXPECTED_NO_IMAGES)}), count={count} (exp {len(EXPECTED_NO_IMAGES)}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — slides={sorted(slides)} (exp {sorted(EXPECTED_NO_IMAGES)}), count={count} (exp {len(EXPECTED_NO_IMAGES)})")
        else:
            print("FAIL: Component 4 — Section 3 not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Section 4 - Long Titles (0.15 points)
    try:
        if len(section_bounds) >= 4:
            slides, count = parse_section(lines, section_bounds[3][0], section_bounds[3][1])
            slides_match = (slides == EXPECTED_LONG_TITLES)
            count_match = (count == len(EXPECTED_LONG_TITLES))
            if slides_match and count_match:
                print(f"PASS: Component 5 — Long-title slides correct: {sorted(slides)}, count={count} (0.15 pts)")
                total_score += 0.15
            elif slides_match or count_match:
                print(f"PARTIAL: Component 5 — slides={sorted(slides)} (exp {sorted(EXPECTED_LONG_TITLES)}), count={count} (exp {len(EXPECTED_LONG_TITLES)}) (0.075 pts)")
                total_score += 0.075
            else:
                print(f"FAIL: Component 5 — slides={sorted(slides)} (exp {sorted(EXPECTED_LONG_TITLES)}), count={count} (exp {len(EXPECTED_LONG_TITLES)})")
        else:
            print("FAIL: Component 5 — Section 4 not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Summary line (0.10 points)
    try:
        summary_line = ""
        for line in lines:
            if 'audited' in line.lower() and 'issues' in line.lower():
                summary_line = line
                break
        if summary_line:
            audited_match = re.search(r'audited:\s*(\d+)', summary_line, re.IGNORECASE)
            issues_match = re.search(r'issues\s+found:\s*(\d+)', summary_line, re.IGNORECASE)
            if audited_match and issues_match:
                audited_num = int(audited_match.group(1))
                issues_num = int(issues_match.group(1))
                if audited_num == 20 and issues_num == EXPECTED_TOTAL_ISSUES:
                    print(f"PASS: Component 6 — Summary correct: audited={audited_num}, issues={issues_num} (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 6 — Summary: audited={audited_num} (exp 20), issues={issues_num} (exp {EXPECTED_TOTAL_ISSUES})")
            else:
                print(f"FAIL: Component 6 — Summary line format invalid: {summary_line}")
        else:
            print("FAIL: Component 6 — Summary line not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
