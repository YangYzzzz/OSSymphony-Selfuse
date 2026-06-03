"""
Reward Script: Create a custom VSCode task for Lighthouse CI audit
Task ID: vscode_web_068
Domain: vscode
Scoring:
  Component 1 (0.25): tasks.json exists and is valid JSON with tasks array
  Component 2 (0.25): A task labeled 'Lighthouse Audit' exists
  Component 3 (0.20): Task command invokes lighthouse (npx lhci or lighthouse)
  Component 4 (0.15): Task has a custom problemMatcher object (not just a string)
  Component 5 (0.15): problemMatcher targets accessibility violations with warning severity
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_068'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'webapp', '.vscode', 'tasks.json')


def strip_jsonc_comments(text):
    """Strip single-line // comments from JSONC content."""
    return re.sub(r'//.*$', '', text, flags=re.MULTILINE)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON with tasks array (0.25 points)
    tasks_data = None
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 — tasks.json not found at {TASKS_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        with open(TASKS_JSON_PATH, 'r') as f:
            raw = f.read()

        # Handle JSONC (JSON with comments)
        cleaned = strip_jsonc_comments(raw)
        tasks_data = json.loads(cleaned)

        if 'tasks' in tasks_data and isinstance(tasks_data['tasks'], list) and len(tasks_data['tasks']) > 0:
            print(f"PASS: Component 1 — tasks.json exists with {len(tasks_data['tasks'])} task(s) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — tasks.json missing 'tasks' array or it is empty")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Lighthouse Audit task
    lighthouse_task = None
    for task in tasks_data.get('tasks', []):
        label = task.get('label', '')
        if isinstance(label, str) and 'lighthouse' in label.lower() and 'audit' in label.lower():
            lighthouse_task = task
            break

    # Component 2: Task labeled 'Lighthouse Audit' exists (0.25 points)
    try:
        if lighthouse_task is not None:
            print(f"PASS: Component 2 — Found task with label '{lighthouse_task.get('label')}' (0.25 pts)")
            total_score += 0.25
        else:
            labels = [t.get('label', '<no label>') for t in tasks_data.get('tasks', [])]
            print(f"FAIL: Component 2 — No task with 'Lighthouse Audit' label found. Labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Task command runs lighthouse (0.20 points)
    try:
        if lighthouse_task is not None:
            command = lighthouse_task.get('command', '')
            if isinstance(command, str) and ('lhci' in command.lower() or 'lighthouse' in command.lower()):
                print(f"PASS: Component 3 — Task command invokes lighthouse: '{command}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Task command does not reference lighthouse: '{command}'")
        else:
            print(f"FAIL: Component 3 — No lighthouse task found to check command")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Task has a custom problemMatcher object (0.15 points)
    try:
        if lighthouse_task is not None:
            pm = lighthouse_task.get('problemMatcher')
            # A custom problemMatcher is an object (dict) or array of objects, not a string reference
            if isinstance(pm, dict):
                # Check it has meaningful keys (owner, pattern, etc.)
                if 'pattern' in pm or 'owner' in pm:
                    print(f"PASS: Component 4 — Custom problemMatcher object found with keys: {list(pm.keys())} (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — problemMatcher is a dict but lacks 'pattern' or 'owner' keys: {list(pm.keys())}")
            elif isinstance(pm, list):
                # Array of matchers
                has_custom = any(isinstance(m, dict) and ('pattern' in m or 'owner' in m) for m in pm)
                if has_custom:
                    print(f"PASS: Component 4 — Custom problemMatcher array found (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — problemMatcher array lacks custom matcher objects")
            else:
                print(f"FAIL: Component 4 — problemMatcher is not a custom object: {type(pm).__name__} = {pm}")
        else:
            print(f"FAIL: Component 4 — No lighthouse task found to check problemMatcher")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: problemMatcher targets accessibility with warning severity (0.15 points)
    try:
        if lighthouse_task is not None:
            pm = lighthouse_task.get('problemMatcher')
            matchers = []
            if isinstance(pm, dict):
                matchers = [pm]
            elif isinstance(pm, list):
                matchers = [m for m in pm if isinstance(m, dict)]

            matching_matchers = [
                m for m in matchers
                if (('accessibility' in str(m.get('owner', '')).lower()
                     or 'a11y' in str(m.get('owner', '')).lower()
                     or 'lighthouse' in str(m.get('owner', '')).lower())
                    and str(m.get('severity', '')).lower() == 'warning')
            ]

            if len(matching_matchers) > 0:
                print(f"PASS: Component 5 — problemMatcher configured for accessibility violations with warning severity (0.15 pts)")
                total_score += 0.15
            else:
                # Partial: check just severity=warning OR accessibility owner
                for matcher in matchers:
                    owner = str(matcher.get('owner', '')).lower()
                    severity = str(matcher.get('severity', '')).lower()
                    if severity == 'warning' or 'accessibility' in owner or 'a11y' in owner:
                        print(f"FAIL: Component 5 — Partial match: owner='{matcher.get('owner')}', severity='{matcher.get('severity')}'. Need both accessibility owner and warning severity.")
                        break
                else:
                    print(f"FAIL: Component 5 — problemMatcher does not target accessibility or use warning severity")
        else:
            print(f"FAIL: Component 5 — No lighthouse task found to check problemMatcher config")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
