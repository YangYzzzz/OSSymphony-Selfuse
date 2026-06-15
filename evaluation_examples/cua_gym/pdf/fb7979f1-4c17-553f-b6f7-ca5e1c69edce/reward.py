"""
Reward Script: Extract page dimensions from PDF and write to text file
Task ID: pdf_mbc_025
Domain: pdf
Scoring:
  Component 1 (0.2): page_dimensions.txt exists and has exactly 4 lines
  Component 2 (0.4): Each line matches 'Page N: WxH' format
  Component 3 (0.4): All dimension values match ground truth exactly
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_025'

# Ground truth from task context
EXPECTED_LINES = [
    "Page 1: 612x792",
    "Page 2: 595x842",
    "Page 3: 612x1008",
    "Page 4: 792x612",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist (no points awarded for existence alone)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has exactly 4 non-empty lines (0.2 points)
    # This checks that the output has the correct number of entries
    try:
        non_empty_lines = [l.strip() for l in lines if l.strip()]
        if len(non_empty_lines) == 4:
            print(f"PASS: Component 1 — File has exactly 4 lines (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 4 lines, found {len(non_empty_lines)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Lines follow 'Page N: WxH' format (0.4 points)
    # Award 0.1 per correctly formatted line
    try:
        import re
        format_score = 0.0
        pattern = r'^Page\s+\d+:\s+\d+x\d+$'
        for i, expected in enumerate(EXPECTED_LINES):
            if i < len(non_empty_lines):
                line = non_empty_lines[i].strip()
                if re.match(pattern, line):
                    print(f"PASS: Component 2.{i+1} — Line {i+1} matches format: '{line}' (0.1 pts)")
                    format_score += 0.1
                else:
                    print(f"FAIL: Component 2.{i+1} — Line {i+1} does not match 'Page N: WxH' format: '{line}'")
            else:
                print(f"FAIL: Component 2.{i+1} — Line {i+1} missing")
        if format_score > 0:
            total_score += format_score
            print(f"  Component 2 subtotal: {format_score:.1f}/0.4")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exact value match for each line (0.4 points)
    # Award 0.1 per exactly matching line
    try:
        value_score = 0.0
        for i, expected in enumerate(EXPECTED_LINES):
            if i < len(non_empty_lines):
                line = non_empty_lines[i].strip()
                if line == expected:
                    print(f"PASS: Component 3.{i+1} — Line {i+1} exact match: '{line}' (0.1 pts)")
                    value_score += 0.1
                else:
                    print(f"FAIL: Component 3.{i+1} — Expected '{expected}', got '{line}'")
            else:
                print(f"FAIL: Component 3.{i+1} — Line {i+1} missing")
        if value_score > 0:
            total_score += value_score
            print(f"  Component 3 subtotal: {value_score:.1f}/0.4")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/page_dimensions.txt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
