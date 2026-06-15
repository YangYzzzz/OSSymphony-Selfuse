"""
Reward Script: Cut line 7 from ~/Desktop/todo.txt and paste it at line 3.
Task ID: vscode_edit_016
Domain: vs_code
Scoring:
  - Component 1: Target line '- Urgent: fix production bug' is at line 3 (0.4 pts)
  - Component 2: Lines originally at positions 3-6 are now at positions 4-7 (0.3 pts)
  - Component 3: File has exactly 10 lines and all unaffected lines are unchanged (0.3 pts)
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_016'

# Ground truth from task context:
# Initial line 7: '- Urgent: fix production bug'
# After task: line 3 == '- Urgent: fix production bug'
# Lines originally at 3-6 shift down to 4-7
# File remains 10 lines

TARGET_LINE = '- Urgent: fix production bug'

# Lines in initial file (0-indexed positions for reference):
# 0: - Review project milestones for Q2
# 1: - Schedule team sync meeting
# 2: - Update documentation for API endpoints
# 3: - Code review for pull request #42
# 4: - Write unit tests for auth module
# 5: - Send weekly status report to manager
# 6: - Urgent: fix production bug   <-- to be moved
# 7: - Deploy hotfix to staging server
# 8: - Follow up on client feedback
# 9: - Prepare demo for Friday presentation

# Expected golden lines (1-indexed):
# 1: - Review project milestones for Q2          (unchanged)
# 2: - Schedule team sync meeting                (unchanged)
# 3: - Urgent: fix production bug               (MOVED from line 7)
# 4: - Update documentation for API endpoints   (was line 3, shifted +1)
# 5: - Code review for pull request #42         (was line 4, shifted +1)
# 6: - Write unit tests for auth module         (was line 5, shifted +1)
# 7: - Send weekly status report to manager     (was line 6, shifted +1)
# 8: - Deploy hotfix to staging server          (unchanged)
# 9: - Follow up on client feedback             (unchanged)
# 10: - Prepare demo for Friday presentation    (unchanged)

EXPECTED_GOLDEN_LINES = [
    '- Review project milestones for Q2',
    '- Schedule team sync meeting',
    '- Urgent: fix production bug',
    '- Update documentation for API endpoints',
    '- Code review for pull request #42',
    '- Write unit tests for auth module',
    '- Send weekly status report to manager',
    '- Deploy hotfix to staging server',
    '- Follow up on client feedback',
    '- Prepare demo for Friday presentation',
]

# Lines that were originally at positions 3-6 (0-indexed: 2-5) should now be at 4-7 (0-indexed: 3-6)
SHIFTED_LINES = [
    '- Update documentation for API endpoints',   # was line 3, now line 4
    '- Code review for pull request #42',          # was line 4, now line 5
    '- Write unit tests for auth module',          # was line 5, now line 6
    '- Send weekly status report to manager',      # was line 6, now line 7
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.splitlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Target line '- Urgent: fix production bug' is at line 3 (0.4 points)
    # This checks the primary task action — moving line 7 to line 3
    try:
        if len(lines) >= 3:
            actual_line3 = lines[2].strip()  # 0-indexed: line 3 = index 2
            if actual_line3 == TARGET_LINE:
                print(f"PASS: Component 1 — '{TARGET_LINE}' is at line 3 (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — expected '{TARGET_LINE}' at line 3, found: '{actual_line3}'")
        else:
            print(f"FAIL: Component 1 — file has fewer than 3 lines")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Lines originally at positions 3-6 shifted down to positions 4-7 (0.3 points)
    # This checks that the cut-and-paste correctly shifted the intermediate lines
    try:
        if len(lines) >= 7:
            mismatches = [
                (i + 3, expected_line, lines[i + 3].strip())
                for i, expected_line in enumerate(SHIFTED_LINES)
                if lines[i + 3].strip() != expected_line
            ]
            if not mismatches:
                print(f"PASS: Component 2 — lines originally at positions 3-6 correctly shifted to 4-7 (0.3 pts)")
                total_score += 0.3
            else:
                for actual_pos, expected_line, actual_line in mismatches:
                    print(f"FAIL: Component 2 — expected '{expected_line}' at line {actual_pos + 1}, found: '{actual_line}'")
        else:
            print(f"FAIL: Component 2 — file has fewer than 7 lines")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File has exactly 10 lines and all unaffected lines are correct (0.3 points)
    # This verifies structural integrity: the cut removed from original position,
    # no duplicate, no data loss, correct total line count
    try:
        if len(lines) != 10:
            print(f"FAIL: Component 3 — expected 10 lines, found {len(lines)}")
        else:
            # Check that all lines match expected golden state
            line_mismatches = [
                (i + 1, expected, actual.strip())
                for i, (actual, expected) in enumerate(zip(lines, EXPECTED_GOLDEN_LINES))
                if actual.strip() != expected
            ]
            if not line_mismatches:
                print(f"PASS: Component 3 — file has 10 lines and all unaffected lines are intact (0.3 pts)")
                total_score += 0.3
            else:
                for line_num, expected, actual in line_mismatches:
                    print(f"FAIL: Component 3 — line {line_num}: expected '{expected}', found '{actual}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/todo.txt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
