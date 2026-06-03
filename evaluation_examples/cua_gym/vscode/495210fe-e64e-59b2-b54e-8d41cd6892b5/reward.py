"""
Reward Script: Database seed/reset workflow for VSCode
Task ID: vscode_gf3_073
Domain: vscode
Scoring:
  Component 1 (0.35): db-seed.js exists with correct structure
  Component 2 (0.35): .vscode/tasks.json with 'DB: Reset & Seed' task
  Component 3 (0.30): .vscode/keybindings.json maps Ctrl+Shift+Alt+S to the task
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_073'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'backend')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: db-seed.js exists and has proper content (0.35 points)
    seed_path = os.path.join(PROJECT_DIR, 'scripts', 'db-seed.js')
    try:
        if not os.path.isfile(seed_path):
            print(f"FAIL: Component 1 — db-seed.js not found at {seed_path}")
        else:
            with open(seed_path, 'r') as f:
                content = f.read()
            content_lower = content.lower()

            checks_passed = 0
            total_checks = 5

            # 1a: Connects to PostgreSQL (pg/Pool reference)
            if re.search(r"(require\s*\(\s*['\"]pg['\"]\s*\)|from\s+['\"]pg['\"]|Pool|Client)", content):
                checks_passed += 1
                print("PASS: Component 1a — PostgreSQL connection found")
            else:
                print("FAIL: Component 1a — No PostgreSQL connection (pg/Pool/Client) found")

            # 1b: Truncates tables in reverse dependency order (comments before posts before users)
            truncate_matches = re.findall(r'truncate\s+(?:table\s+)?(\w+)', content_lower)
            if len(truncate_matches) >= 3:
                # Check order: comments should come before posts, posts before users
                try:
                    idx_comments = next(i for i, t in enumerate(truncate_matches) if 'comment' in t)
                    idx_posts = next(i for i, t in enumerate(truncate_matches) if 'post' in t)
                    idx_users = next(i for i, t in enumerate(truncate_matches) if 'user' in t)
                    if idx_comments < idx_posts < idx_users:
                        checks_passed += 1
                        print("PASS: Component 1b — Truncation in reverse dependency order (comments->posts->users)")
                    else:
                        print(f"FAIL: Component 1b — Wrong truncation order: {truncate_matches}")
                except StopIteration:
                    print(f"FAIL: Component 1b — Could not find all three tables in truncations: {truncate_matches}")
            else:
                print(f"FAIL: Component 1b — Expected >=3 truncate statements, found {len(truncate_matches)}")

            # 1c: Has batch inserts (INSERT INTO ... VALUES with multiple value groups)
            if re.search(r'insert\s+into', content_lower) and ('values' in content_lower):
                checks_passed += 1
                print("PASS: Component 1c — Batch INSERT statements found")
            else:
                print("FAIL: Component 1c — No batch INSERT statements found")

            # 1d: Seed data for users (10 records with realistic names)
            # Count user seed entries - look for name patterns in arrays/objects
            user_name_pattern = re.findall(r"name:\s*['\"]([^'\"]+)['\"]", content)
            if len(user_name_pattern) >= 10:
                checks_passed += 1
                print(f"PASS: Component 1d — Found {len(user_name_pattern)} user records with names")
            else:
                # Alternative: count array elements
                print(f"FAIL: Component 1d — Expected >=10 user names, found {len(user_name_pattern)}")

            # 1e: Seed data counts - posts (30) and comments (100)
            has_30_posts = bool(re.search(r'(30|postTitles|post_titles)', content) or
                               len(re.findall(r"['\"][^'\"]{10,}['\"]", content)) >= 30)
            has_100_comments = bool(re.search(r'100|commentBod|comment_bod', content))
            if has_30_posts and has_100_comments:
                checks_passed += 1
                print("PASS: Component 1e — Posts (30) and comments (100) seed data present")
            else:
                print(f"FAIL: Component 1e — Posts 30 ref: {has_30_posts}, Comments 100 ref: {has_100_comments}")

            component1_score = 0.35 * (checks_passed / total_checks)
            total_score += component1_score
            print(f"Component 1 subtotal: {checks_passed}/{total_checks} checks passed ({component1_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .vscode/tasks.json with 'DB: Reset & Seed' task (0.35 points)
    tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
    try:
        if not os.path.isfile(tasks_path):
            print(f"FAIL: Component 2 — tasks.json not found at {tasks_path}")
        else:
            with open(tasks_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            tasks_data = json.loads(cleaned)

            tasks_list = tasks_data.get('tasks', [])
            # Find the 'DB: Reset & Seed' task
            matching_task = None
            for t in tasks_list:
                label = t.get('label', '')
                if 'reset' in label.lower() and 'seed' in label.lower():
                    matching_task = t
                    break

            if matching_task is None:
                print(f"FAIL: Component 2 — No task with 'Reset' and 'Seed' in label. Found: {[t.get('label') for t in tasks_list]}")
            else:
                sub_checks = 0
                total_sub = 2

                # 2a: Task label matches
                if matching_task.get('label', '') == 'DB: Reset & Seed':
                    sub_checks += 1
                    print(f"PASS: Component 2a — Task label is exactly 'DB: Reset & Seed'")
                else:
                    # Partial: label contains reset & seed but not exact
                    sub_checks += 0.5
                    print(f"PARTIAL: Component 2a — Task label is '{matching_task.get('label')}', expected 'DB: Reset & Seed'")

                # 2b: Task references db-seed.js
                task_str = json.dumps(matching_task).lower()
                if 'db-seed' in task_str or 'db_seed' in task_str:
                    sub_checks += 1
                    print("PASS: Component 2b — Task references db-seed script")
                else:
                    print(f"FAIL: Component 2b — Task does not reference db-seed script")

                component2_score = 0.35 * (sub_checks / total_sub)
                total_score += component2_score
                print(f"Component 2 subtotal: {sub_checks}/{total_sub} checks ({component2_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .vscode/keybindings.json maps Ctrl+Shift+Alt+S (0.30 points)
    keybindings_path = os.path.join(PROJECT_DIR, '.vscode', 'keybindings.json')
    try:
        if not os.path.isfile(keybindings_path):
            print(f"FAIL: Component 3 — keybindings.json not found at {keybindings_path}")
        else:
            with open(keybindings_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments (first line may be a comment)
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            bindings = json.loads(cleaned)

            if not isinstance(bindings, list):
                print("FAIL: Component 3 — keybindings.json is not a list")
            else:
                matching_binding = None
                for b in bindings:
                    key = b.get('key', '').lower().replace(' ', '')
                    # Normalize: ctrl+shift+alt+s in any order of modifiers
                    modifiers = set()
                    parts = key.split('+')
                    letter = ''
                    for p in parts:
                        if p in ('ctrl', 'shift', 'alt', 'meta'):
                            modifiers.add(p)
                        else:
                            letter = p
                    if modifiers == {'ctrl', 'shift', 'alt'} and letter == 's':
                        matching_binding = b
                        break

                if matching_binding is None:
                    print(f"FAIL: Component 3 — No keybinding for Ctrl+Shift+Alt+S found. Bindings: {bindings}")
                else:
                    sub_checks = 0
                    total_sub = 2

                    # 3a: Key is correct (already matched)
                    sub_checks += 1
                    print("PASS: Component 3a — Keybinding Ctrl+Shift+Alt+S found")

                    # 3b: Binding references the task (runTask with 'DB: Reset & Seed')
                    command = matching_binding.get('command', '').lower()
                    args = str(matching_binding.get('args', '')).lower()
                    if 'runtask' in command and ('reset' in args and 'seed' in args):
                        sub_checks += 1
                        print("PASS: Component 3b — Binding runs 'DB: Reset & Seed' task")
                    elif 'runtask' in command:
                        sub_checks += 0.5
                        print(f"PARTIAL: Component 3b — Binding runs a task but args='{matching_binding.get('args')}'")
                    else:
                        print(f"FAIL: Component 3b — Binding command is '{matching_binding.get('command')}', expected workbench.action.tasks.runTask")

                    component3_score = 0.30 * (sub_checks / total_sub)
                    total_score += component3_score
                    print(f"Component 3 subtotal: {sub_checks}/{total_sub} checks ({component3_score:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
