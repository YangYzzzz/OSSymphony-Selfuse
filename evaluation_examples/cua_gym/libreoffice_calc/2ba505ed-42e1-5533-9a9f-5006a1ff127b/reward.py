"""
Reward Script: Configure log analysis workflow in ~/project
Task ID: vscode_wf_093
Domain: vs-code (VSCode configuration)
Scoring:
  Component 1: Extension installed (0.15)
  Component 2: settings.json files.associations (0.15)
  Component 3: settings.json custom highlighter patterns (0.15)
  Component 4: tasks.json tail-logs task (0.15)
  Component 5: tasks.json grep-errors task (0.10)
  Component 6: tasks.json log-stats task (0.10)
  Component 7: scripts/log-stats.sh exists with level-count logic (0.10)
  Component 8: .vscode/log-format.json with log pattern definition (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_093'


def load_json_file(path):
    """Load a JSON file, handling JSONC (comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC compatibility
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension emilast.logfilehighlighter is installed (0.15 points)
    # Check by scanning the extensions directory on disk instead of subprocess
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if os.path.isdir(ext_dir):
            ext_folders = os.listdir(ext_dir)
            found = any('emilast.logfilehighlighter' in f.lower() for f in ext_folders)
            if found:
                print(f"PASS: Component 1 — Extension emilast.logfilehighlighter installed (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Extension not found in {ext_dir}. Folders: {ext_folders}")
        else:
            print(f"FAIL: Component 1 — Extensions directory not found at {ext_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: settings.json has files.associations mapping *.log to log (0.15 points)
    settings_path = os.path.join(VSCODE_DIR, 'settings.json')
    try:
        settings = load_json_file(settings_path)
        assoc = settings.get('files.associations', {})
        if isinstance(assoc, dict) and assoc.get('*.log') == 'log':
            print(f"PASS: Component 2 — files.associations has *.log -> log (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — files.associations missing or wrong. Got: {assoc}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — settings.json not found at {settings_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: settings.json has logFileHighlighter.customPatterns with level patterns (0.15 points)
    try:
        settings = load_json_file(settings_path)
        patterns = settings.get('logFileHighlighter.customPatterns', [])
        if not isinstance(patterns, list) or len(patterns) == 0:
            print(f"FAIL: Component 3 — No customPatterns found")
        else:
            # Check that patterns cover at least ERROR, WARN, INFO levels
            pattern_texts = ' '.join([p.get('pattern', '') for p in patterns])
            has_error = 'ERROR' in pattern_texts
            has_warn = 'WARN' in pattern_texts
            has_info = 'INFO' in pattern_texts
            if has_error and has_warn and has_info:
                print(f"PASS: Component 3 — customPatterns include ERROR, WARN, INFO level patterns (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Missing level patterns. ERROR={has_error}, WARN={has_warn}, INFO={has_info}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tasks.json has 'tail-logs' task (0.15 points)
    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    try:
        tasks_config = load_json_file(tasks_path)
        tasks_list = tasks_config.get('tasks', [])
        tail_task = None
        for t in tasks_list:
            if t.get('label') == 'tail-logs':
                tail_task = t
                break
        if tail_task is not None:
            cmd = tail_task.get('command', '')
            # Should tail/follow a log file
            if 'tail' in cmd and ('app.log' in cmd or 'logs' in cmd):
                print(f"PASS: Component 4 — tail-logs task found with tail command (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — tail-logs task found but command doesn't tail logs: {cmd}")
        else:
            print(f"FAIL: Component 4 — No 'tail-logs' task found in tasks.json")
    except FileNotFoundError:
        print(f"FAIL: Component 4 — tasks.json not found at {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json has 'grep-errors' task (0.10 points)
    try:
        tasks_config = load_json_file(tasks_path)
        tasks_list = tasks_config.get('tasks', [])
        grep_task = None
        for t in tasks_list:
            if t.get('label') == 'grep-errors':
                grep_task = t
                break
        if grep_task is not None:
            cmd = grep_task.get('command', '')
            # Should grep for ERROR and/or WARN
            if 'grep' in cmd.lower() and ('ERROR' in cmd or 'WARN' in cmd):
                print(f"PASS: Component 5 — grep-errors task found filtering for ERROR/WARN (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — grep-errors task found but command doesn't filter errors: {cmd}")
        else:
            print(f"FAIL: Component 5 — No 'grep-errors' task found in tasks.json")
    except FileNotFoundError:
        print(f"FAIL: Component 5 — tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: tasks.json has 'log-stats' task (0.10 points)
    try:
        tasks_config = load_json_file(tasks_path)
        tasks_list = tasks_config.get('tasks', [])
        stats_task = None
        for t in tasks_list:
            if t.get('label') == 'log-stats':
                stats_task = t
                break
        if stats_task is not None:
            cmd = stats_task.get('command', '')
            # Should reference log-stats script
            if 'log-stats' in cmd:
                print(f"PASS: Component 6 — log-stats task found referencing log-stats script (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — log-stats task found but command doesn't reference log-stats: {cmd}")
        else:
            print(f"FAIL: Component 6 — No 'log-stats' task found in tasks.json")
    except FileNotFoundError:
        print(f"FAIL: Component 6 — tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: scripts/log-stats.sh exists and contains level-counting logic (0.10 points)
    stats_script = os.path.join(PROJECT, 'scripts', 'log-stats.sh')
    try:
        if not os.path.isfile(stats_script):
            print(f"FAIL: Component 7 — scripts/log-stats.sh not found")
        else:
            with open(stats_script, 'r') as f:
                script_content = f.read()
            # Must grep for log levels and count them
            has_grep = 'grep' in script_content.lower()
            has_level_refs = sum(1 for lvl in ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']
                                if lvl in script_content)
            if has_grep and has_level_refs >= 3:
                print(f"PASS: Component 7 — log-stats.sh has grep + {has_level_refs} level references (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — log-stats.sh missing grep or level refs (grep={has_grep}, levels={has_level_refs})")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: .vscode/log-format.json exists with pattern and fields (0.10 points)
    log_format_path = os.path.join(VSCODE_DIR, 'log-format.json')
    try:
        log_format = load_json_file(log_format_path)
        has_pattern = 'pattern' in log_format
        has_fields = 'fields' in log_format and isinstance(log_format['fields'], dict)
        # Fields should define timestamp, level, module
        field_names = set(log_format.get('fields', {}).keys()) if has_fields else set()
        has_key_fields = {'timestamp', 'level', 'module'}.issubset(field_names)
        if has_pattern and has_fields and has_key_fields:
            print(f"PASS: Component 8 — log-format.json has pattern + fields (timestamp, level, module) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 8 — log-format.json incomplete. pattern={has_pattern}, fields={has_fields}, key_fields={has_key_fields} (found: {field_names})")
    except FileNotFoundError:
        print(f"FAIL: Component 8 — log-format.json not found at {log_format_path}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
