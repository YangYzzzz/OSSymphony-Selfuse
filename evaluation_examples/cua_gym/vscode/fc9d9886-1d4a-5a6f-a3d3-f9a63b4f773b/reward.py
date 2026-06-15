"""
Reward Script: Convert TODO comments from line-comment to block-comment style
Task ID: vscode_rf_020
Domain: vscode
Scoring:
  Component 1 (0.4): All 6 TODO lines use block-comment style /* ... */
  Component 2 (0.3): No old-style '# TODO:' lines remain (without block wrapping)
  Component 3 (0.3): TODO descriptions preserved and non-TODO lines unmodified
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_020'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'backend', 'task_queue.py')

# The 6 expected TODO description fragments (from task context)
EXPECTED_DESCRIPTIONS = [
    "Implement a TaskResult dataclass to store execution results with timing metadata",
    "Add a metrics collector to track queue throughput and average processing time",
    "Persist completed task results to a SQLite database for audit trail",
    "Add health check endpoint that reports worker status and queue depth",
    "Flush any pending metrics and close database connections on shutdown",
    "Support cron-style expressions instead of simple interval-based scheduling",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 TODO comments use block-comment style (0.4 points)
    # Each TODO line should match pattern: # /* TODO: <desc> */
    try:
        block_todo_pattern = re.compile(r'#\s*/\*\s*TODO:.*\*/')
        block_todo_lines = [l for l in lines if block_todo_pattern.search(l)]
        block_count = len(block_todo_lines)

        if block_count == 6:
            print(f"PASS: Component 1 — All 6 TODO comments use block-comment style (0.4 pts)")
            total_score += 0.4
        elif block_count > 0:
            partial = round(0.4 * (block_count / 6), 2)
            print(f"PARTIAL: Component 1 — {block_count}/6 TODO comments converted ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No block-style TODO comments found (0 of 6)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No old-style '# TODO:' lines remain without block wrapping (0.3 points)
    # Old style: '# TODO: ...' without '/*' on the same line
    try:
        old_style_pattern = re.compile(r'#\s*TODO:')
        old_style_lines = []
        for l in lines:
            if old_style_pattern.search(l) and '/*' not in l:
                old_style_lines.append(l.strip())

        if len(old_style_lines) == 0:
            print(f"PASS: Component 2 — No old-style '# TODO:' comments remain (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — {len(old_style_lines)} old-style TODO comments still present")
            for ol in old_style_lines:
                print(f"  Found: {ol}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: TODO descriptions preserved inside block comments AND structure intact (0.3 points)
    # This component is anchored to the change: descriptions must appear WITHIN /* ... */ blocks
    # This fails on initial_env because initial has no /* */ blocks around TODOs
    try:
        # Check that each description appears inside a block-comment-style TODO line
        block_preserved_count = 0
        block_comment_pattern = re.compile(r'#\s*/\*\s*TODO:\s*(.+?)\s*\*/')
        block_descriptions = []
        for l in lines:
            m = block_comment_pattern.search(l)
            if m:
                block_descriptions.append(m.group(1).strip())

        for desc in EXPECTED_DESCRIPTIONS:
            if any(desc in bd for bd in block_descriptions):
                block_preserved_count += 1
            else:
                print(f"  Missing in block-comment: '{desc[:60]}...'")

        if block_preserved_count == 6:
            # Also verify file structure is intact (non-TODO lines unmodified)
            structural_checks = [
                'class TaskStatus(Enum):',
                'class TaskPriority(Enum):',
                'class TaskQueue:',
                'class ScheduledTaskRunner:',
                'def submit(self',
                'def _process_task(self',
                'def shutdown(self',
            ]
            struct_ok = all(s in content for s in structural_checks)

            if struct_ok:
                print(f"PASS: Component 3 — All 6 descriptions preserved in block comments and structure intact (0.3 pts)")
                total_score += 0.3
            else:
                print(f"PARTIAL: Component 3 — Descriptions in block comments but structure altered (0.15 pts)")
                total_score += 0.15
        elif block_preserved_count > 0:
            partial = round(0.3 * (block_preserved_count / 6), 2)
            print(f"PARTIAL: Component 3 — {block_preserved_count}/6 descriptions in block comments ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No TODO descriptions found inside block comments")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
