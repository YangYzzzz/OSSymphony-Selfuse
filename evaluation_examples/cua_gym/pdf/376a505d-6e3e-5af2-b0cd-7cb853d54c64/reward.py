"""
Reward Script: Verify PDF page dimensions and write results to dimensions.txt
Task ID: pdf_cr_048
Domain: pdf
Scoring:
  Component 1 (0.2): dimensions.txt exists and is non-empty
  Component 2 (0.5): Per-page dimension lines correct (5 pages, 0.1 each)
  Component 3 (0.3): Summary line correct
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_048'

# Expected page dimensions from the PDF (ground truth from VM exploration)
EXPECTED_PAGES = [
    (1, 595, 842, 'A4'),
    (2, 612, 792, 'Letter'),
    (3, 612, 1008, 'Legal'),
    (4, 842, 1191, 'A3'),
    (5, 500, 700, 'Custom'),
]

# Expected summary counts
EXPECTED_TOTAL = 5
EXPECTED_A4 = 1
EXPECTED_LETTER = 1
EXPECTED_OTHER = 3  # Legal + A3 + Custom


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = [l.strip() for l in content.strip().split('\n') if l.strip()]

    # Component 1: dimensions.txt exists and has content (0.2 points)
    # This is task-introduced: the file does NOT exist on initial_env
    try:
        if len(lines) >= 1:
            print(f"PASS: Component 1 — dimensions.txt exists with {len(lines)} lines (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — dimensions.txt is empty")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Per-page dimension lines (0.5 points, 0.1 per page)
    # Each line should be like: "Page X: WxH points (SIZE_NAME)"
    # Tolerance of 2 points for dimension matching
    TOLERANCE = 2
    for page_num, exp_w, exp_h, exp_size in EXPECTED_PAGES:
        try:
            # Search for the line describing this page
            page_pattern = re.compile(
                r'Page\s+' + str(page_num) + r'\s*:\s*(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*points?\s*\((\w+)\)',
                re.IGNORECASE
            )
            matched = False
            for line in lines:
                m = page_pattern.search(line)
                if m:
                    found_w = float(m.group(1))
                    found_h = float(m.group(2))
                    found_size = m.group(3)

                    w_ok = abs(found_w - exp_w) <= TOLERANCE
                    h_ok = abs(found_h - exp_h) <= TOLERANCE
                    size_ok = found_size.lower() == exp_size.lower()

                    if w_ok and h_ok and size_ok:
                        print(f"PASS: Component 2.{page_num} — Page {page_num}: {found_w}x{found_h} ({found_size}) (0.1 pts)")
                        total_score += 0.1
                    else:
                        reasons = []
                        if not w_ok:
                            reasons.append(f"width {found_w} != {exp_w}")
                        if not h_ok:
                            reasons.append(f"height {found_h} != {exp_h}")
                        if not size_ok:
                            reasons.append(f"size '{found_size}' != '{exp_size}'")
                        print(f"FAIL: Component 2.{page_num} — Page {page_num}: {', '.join(reasons)}")
                    matched = True
                    break
            if not matched:
                print(f"FAIL: Component 2.{page_num} — No matching line found for Page {page_num}")
        except Exception as e:
            print(f"ERROR: Component 2.{page_num} — {e}")

    # Component 3: Summary line (0.3 points)
    # Expected: "Total pages: 5, A4: 1, Letter: 1, Other: 3"
    try:
        summary_pattern = re.compile(
            r'Total\s+pages\s*:\s*(\d+)\s*,\s*A4\s*:\s*(\d+)\s*,\s*Letter\s*:\s*(\d+)\s*,\s*Other\s*:\s*(\d+)',
            re.IGNORECASE
        )
        summary_found = False
        for line in lines:
            m = summary_pattern.search(line)
            if m:
                total_p = int(m.group(1))
                a4_c = int(m.group(2))
                letter_c = int(m.group(3))
                other_c = int(m.group(4))

                all_correct = (
                    total_p == EXPECTED_TOTAL
                    and a4_c == EXPECTED_A4
                    and letter_c == EXPECTED_LETTER
                    and other_c == EXPECTED_OTHER
                )

                if all_correct:
                    print(f"PASS: Component 3 — Summary: Total={total_p}, A4={a4_c}, Letter={letter_c}, Other={other_c} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Summary mismatch: Total={total_p}(exp {EXPECTED_TOTAL}), A4={a4_c}(exp {EXPECTED_A4}), Letter={letter_c}(exp {EXPECTED_LETTER}), Other={other_c}(exp {EXPECTED_OTHER})")
                summary_found = True
                break
        if not summary_found:
            print(f"FAIL: Component 3 — No summary line found matching expected format")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Desktop/dimensions.txt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
