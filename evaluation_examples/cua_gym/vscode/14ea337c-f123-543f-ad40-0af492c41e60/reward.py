"""
Reward Script: Remove all console.log lines from app.js using multi-cursor
Task ID: vscode_prod_040
Domain: vscode
Scoring:
  Component 1 (0.4): No console.log statements remain in app.js
  Component 2 (0.3): Line count reduced appropriately (removed ~12 lines)
  Component 3 (0.3): Surrounding code structure is intact
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_040'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'debug-cleanup', 'app.js')

# Known structural markers from the initial file that should survive deletion.
# These are non-console.log lines that must remain intact.
STRUCTURAL_MARKERS = [
    "const express = require('express');",
    "const helmet = require('helmet');",
    "const { Pool } = require('pg');",
    "const app = express();",
    "app.use(helmet());",
    "app.use(express.json());",
    "app.get('/api/tasks',",
    "app.post('/api/tasks',",
    "app.put('/api/tasks/:id',",
    "app.delete('/api/tasks/:id',",
    "app.listen(PORT,",
]

# Original line count and console.log count from initial state
INITIAL_LINE_COUNT = 206
INITIAL_CONSOLE_LOG_COUNT = 12


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
            lines = content.splitlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    line_count = len(lines)

    # Component 1: No console.log statements remain (0.4 points)
    # This is the core task requirement. In initial_env there are 12 console.log lines.
    try:
        console_log_lines = [
            (i + 1, line.strip())
            for i, line in enumerate(lines)
            if 'console.log' in line
        ]
        console_log_count = len(console_log_lines)

        if console_log_count == 0:
            print(f"PASS: Component 1 — No console.log statements remain (0.4 pts)")
            total_score += 0.4
        else:
            # Partial credit: proportion of console.log lines removed
            removed = INITIAL_CONSOLE_LOG_COUNT - console_log_count
            if removed > 0:
                partial = 0.4 * (removed / INITIAL_CONSOLE_LOG_COUNT)
                print(f"PARTIAL: Component 1 — {console_log_count} console.log remain "
                      f"({removed}/{INITIAL_CONSOLE_LOG_COUNT} removed, {partial:.2f} pts)")
                for ln, text in console_log_lines[:5]:
                    print(f"  Remaining: line {ln}: {text}")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — All {console_log_count} console.log still present")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Line count reduced appropriately (0.3 points)
    # Initial file has 206 lines, 12 console.log lines. After removal, expect ~194 lines
    # (some console.log lines may leave blank lines, so allow a range).
    try:
        expected_min = INITIAL_LINE_COUNT - INITIAL_CONSOLE_LOG_COUNT - 5  # 189
        expected_max = INITIAL_LINE_COUNT - INITIAL_CONSOLE_LOG_COUNT + 2  # 196

        if line_count < INITIAL_LINE_COUNT and expected_min <= line_count <= expected_max:
            print(f"PASS: Component 2 — Line count is {line_count} "
                  f"(expected {expected_min}-{expected_max}) (0.3 pts)")
            total_score += 0.3
        elif line_count < INITIAL_LINE_COUNT and line_count < expected_min:
            # Some lines removed but maybe too many - partial credit
            partial = 0.15
            print(f"PARTIAL: Component 2 — Line count is {line_count}, "
                  f"below expected range {expected_min}-{expected_max} ({partial} pts)")
            total_score += partial
        elif line_count < INITIAL_LINE_COUNT:
            # Some lines removed but not enough
            partial = 0.15
            print(f"PARTIAL: Component 2 — Line count is {line_count}, "
                  f"above expected range {expected_min}-{expected_max} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Line count is {line_count}, "
                  f"not reduced from {INITIAL_LINE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Code structure intact AND console.log removed (0.3 points)
    # Compound check: structural markers must be present AND console.log must be gone.
    # This ensures we only award points for a clean deletion (task-introduced change),
    # not for a pre-existing state where markers already exist.
    try:
        markers_found = 0
        markers_missing = []
        for marker in STRUCTURAL_MARKERS:
            if marker in content:
                markers_found += 1
            else:
                markers_missing.append(marker)

        total_markers = len(STRUCTURAL_MARKERS)
        # Both conditions must hold: markers intact AND no console.log
        if markers_found == total_markers and console_log_count == 0:
            print(f"PASS: Component 3 — All {total_markers} structural markers intact "
                  f"AND 0 console.log remain (0.3 pts)")
            total_score += 0.3
        elif console_log_count > 0:
            print(f"FAIL: Component 3 — console.log still present ({console_log_count}), "
                  f"cannot award structure-integrity points")
        elif markers_found < total_markers:
            # console.log removed but some code structure damaged
            ratio = markers_found / total_markers
            partial = round(0.3 * ratio * 0.5, 2)  # reduced credit for damaged structure
            print(f"PARTIAL: Component 3 — {markers_found}/{total_markers} markers intact, "
                  f"some structure lost ({partial} pts)")
            for m in markers_missing[:3]:
                print(f"  Missing: {m}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Neither condition met")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
