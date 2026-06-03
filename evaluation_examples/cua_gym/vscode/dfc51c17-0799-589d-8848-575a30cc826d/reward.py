"""
Reward Script: Configure a code review checklist workflow in ~/project
Task ID: vscode_wf_069
Domain: vscode
Scoring:
  Component 1 (0.20): scripts/review.sh exists and is executable
  Component 2 (0.15): review.sh checks for console.log, TODO, large files, missing tests
  Component 3 (0.15): Extension gruntfuggly.todo-tree is installed
  Component 4 (0.25): settings.json has todo-tree tags and highlight colors configured
  Component 5 (0.25): tasks.json has review-checklist, lint, test, compound review-ready
"""

import os
import json
import re
import stat

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_069'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
TASKS_PATH = os.path.join(PROJECT, '.vscode', 'tasks.json')
REVIEW_SH_PATH = os.path.join(PROJECT, 'scripts', 'review.sh')


def load_json_lenient(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Could not load {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: scripts/review.sh exists and is executable (0.20 points)
    # =========================================================================
    try:
        if os.path.isfile(REVIEW_SH_PATH):
            file_stat = os.stat(REVIEW_SH_PATH)
            # Check if any execute bit is set
            if file_stat.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                print(f"PASS: Component 1 -- review.sh exists and is executable (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 -- review.sh exists but is NOT executable (mode: {oct(file_stat.st_mode)})")
        else:
            print(f"FAIL: Component 1 -- review.sh not found at {REVIEW_SH_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: review.sh contains all 4 required checks (0.15 points)
    # Checks: console.log, TODO comments, large files (>500 lines), missing tests
    # =========================================================================
    try:
        if os.path.isfile(REVIEW_SH_PATH):
            with open(REVIEW_SH_PATH, 'r') as f:
                sh_content = f.read().lower()

            checks_found = 0
            # Check for console.log detection
            if 'console' in sh_content and 'log' in sh_content:
                checks_found += 1
            # Check for TODO comment detection
            if 'todo' in sh_content:
                checks_found += 1
            # Check for large file / line count detection
            if '500' in sh_content or 'large' in sh_content.lower() or 'wc' in sh_content:
                checks_found += 1
            # Check for missing test file detection
            if 'test' in sh_content and ('missing' in sh_content or 'exist' in sh_content or '-f' in sh_content):
                checks_found += 1

            if checks_found >= 4:
                print(f"PASS: Component 2 -- review.sh contains all 4 checks ({checks_found}/4) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- review.sh only has {checks_found}/4 required checks")
        else:
            print(f"FAIL: Component 2 -- review.sh not found, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: Extension gruntfuggly.todo-tree is installed (0.15 points)
    # =========================================================================
    try:
        # Check by looking at extensions directory
        extensions_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        ext_found = False

        # Method 1: Check extensions directory for todo-tree
        if os.path.isdir(extensions_dir):
            for entry in os.listdir(extensions_dir):
                if 'todo-tree' in entry.lower() or 'gruntfuggly' in entry.lower():
                    ext_found = True
                    break

        # Method 2: Check via code CLI (list-extensions output)
        if not ext_found:
            ext_list_path = '/tmp/ext_list.txt'
            os.system('code --list-extensions > /tmp/ext_list.txt 2>/dev/null')
            if os.path.isfile(ext_list_path):
                with open(ext_list_path, 'r') as f:
                    ext_list = f.read().lower()
                if 'todo-tree' in ext_list or 'gruntfuggly' in ext_list:
                    ext_found = True

        if ext_found:
            print(f"PASS: Component 3 -- gruntfuggly.todo-tree extension is installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- gruntfuggly.todo-tree extension not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================================
    # Component 4: settings.json has todo-tree tags and highlight colors (0.25 points)
    # Required: todo-tree.general.tags with TODO, FIXME, HACK, BUG
    #           todo-tree.highlights.customHighlight with different colors per tag
    # =========================================================================
    try:
        settings = load_json_lenient(SETTINGS_PATH)
        if settings is not None:
            comp4_score = 0.0

            # Sub-check 4a: tags configured with all 4 required tags (0.10)
            tags = settings.get('todo-tree.general.tags', [])
            required_tags = {'TODO', 'FIXME', 'HACK', 'BUG'}
            if isinstance(tags, list) and required_tags.issubset(set(tags)):
                print(f"  4a PASS: tags contain {required_tags}")
                comp4_score += 0.10
            else:
                print(f"  4a FAIL: tags = {tags}, expected to contain {required_tags}")

            # Sub-check 4b: customHighlight has entries for all 4 tags with different colors (0.15)
            custom_hl = settings.get('todo-tree.highlights.customHighlight', {})
            if isinstance(custom_hl, dict):
                tags_with_colors = 0
                colors_seen = set()
                for tag in required_tags:
                    if tag in custom_hl:
                        hl = custom_hl[tag]
                        # Check it has some color property
                        color = hl.get('background', hl.get('foreground', hl.get('iconColour', '')))
                        if color:
                            tags_with_colors += 1
                            colors_seen.add(color)

                if tags_with_colors >= 4 and len(colors_seen) >= 2:
                    print(f"  4b PASS: customHighlight has {tags_with_colors} tags with {len(colors_seen)} distinct colors")
                    comp4_score += 0.15
                else:
                    print(f"  4b FAIL: customHighlight has {tags_with_colors} colored tags, {len(colors_seen)} distinct colors")
            else:
                print(f"  4b FAIL: customHighlight not found or not a dict")

            if comp4_score > 0:
                print(f"PASS: Component 4 -- todo-tree settings configured ({comp4_score} pts)")
                total_score += comp4_score
            else:
                print(f"FAIL: Component 4 -- todo-tree settings not properly configured")
        else:
            print(f"FAIL: Component 4 -- settings.json could not be loaded")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # =========================================================================
    # Component 5: tasks.json has all required tasks (0.25 points)
    # Required: review-checklist, lint, test, compound review-ready (with dependsOn)
    # =========================================================================
    try:
        tasks_config = load_json_lenient(TASKS_PATH)
        if tasks_config is not None and 'tasks' in tasks_config:
            tasks_list = tasks_config['tasks']
            task_labels = {t.get('label', ''): t for t in tasks_list}

            comp5_score = 0.0

            # Sub-check 5a: review-checklist task exists and runs a shell script (0.07)
            if 'review-checklist' in task_labels:
                rc_task = task_labels['review-checklist']
                if rc_task.get('type') == 'shell':
                    print(f"  5a PASS: review-checklist task exists as shell task")
                    comp5_score += 0.07
                else:
                    print(f"  5a PARTIAL: review-checklist exists but type={rc_task.get('type')}")
            else:
                print(f"  5a FAIL: review-checklist task not found")

            # Sub-check 5b: lint task exists (0.04)
            if 'lint' in task_labels:
                print(f"  5b PASS: lint task exists")
                comp5_score += 0.04
            else:
                print(f"  5b FAIL: lint task not found")

            # Sub-check 5c: test task exists (0.04)
            if 'test' in task_labels:
                print(f"  5c PASS: test task exists")
                comp5_score += 0.04
            else:
                print(f"  5c FAIL: test task not found")

            # Sub-check 5d: review-ready compound task with dependsOn (0.10)
            if 'review-ready' in task_labels:
                rr_task = task_labels['review-ready']
                depends = rr_task.get('dependsOn', [])
                required_deps = {'lint', 'test', 'review-checklist'}
                if isinstance(depends, list) and required_deps.issubset(set(depends)):
                    print(f"  5d PASS: review-ready compound task depends on {depends}")
                    comp5_score += 0.10
                else:
                    print(f"  5d FAIL: review-ready dependsOn={depends}, expected {required_deps}")
            else:
                print(f"  5d FAIL: review-ready task not found")

            if comp5_score > 0:
                print(f"PASS: Component 5 -- tasks.json configured ({comp5_score} pts)")
                total_score += comp5_score
            else:
                print(f"FAIL: Component 5 -- tasks.json not properly configured")
        else:
            print(f"FAIL: Component 5 -- tasks.json not found or has no tasks array")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
