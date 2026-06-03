"""
Reward Script: VSCode Performance Investigation Workflow
Task ID: vscode_wf_055
Domain: vscode (file-based verification)
Scoring:
  Component 1: tasks.json has cProfile profiling task (0.25)
  Component 2: launch.json has profiling debug configuration (0.2)
  Component 3: profile.prof exists and is valid pstats data (0.2)
  Component 4: performance_report.md documents top 5 slowest functions (0.35)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_055'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json has a cProfile profiling task (0.25 points)
    # Task requirement: "add a tasks.json task that runs cProfile on the main script and outputs to profile.prof"
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if not os.path.exists(tasks_path):
            print("FAIL: Component 1 -- tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(cleaned)

            tasks_list = tasks_data.get('tasks', [])
            found_profiling_task = False
            for task in tasks_list:
                cmd = task.get('command', '')
                label = task.get('label', '')
                # Check if the task runs cProfile and outputs to profile.prof
                if 'cProfile' in cmd or 'cprofile' in cmd.lower():
                    if 'profile.prof' in cmd:
                        found_profiling_task = True
                        break

            if found_profiling_task:
                print(f"PASS: Component 1 -- tasks.json has cProfile profiling task outputting to profile.prof (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- tasks.json exists but no cProfile task outputting to profile.prof found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: launch.json has a profiling/debug configuration (0.2 points)
    # Task requirement: "create a profiling launch configuration in launch.json"
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        if not os.path.exists(launch_path):
            print("FAIL: Component 2 -- launch.json does not exist")
        else:
            with open(launch_path, 'r') as f:
                content = f.read()
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_data = json.loads(cleaned)

            configurations = launch_data.get('configurations', [])
            found_profiling_config = False
            for config in configurations:
                name = config.get('name', '').lower()
                request = config.get('request', '')
                config_type = config.get('type', '')
                program = config.get('program', '')
                # Check for a Python debug/profiling configuration referencing main.py
                if ('python' in config_type.lower() or 'debugpy' in config_type.lower()):
                    if 'main.py' in program or 'main' in program:
                        found_profiling_config = True
                        break

            if found_profiling_config:
                print(f"PASS: Component 2 -- launch.json has Python profiling configuration for main.py (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 -- launch.json exists but no Python profiling config targeting main.py found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: profile.prof exists and is a valid pstats profile (0.2 points)
    # Task requirement: "Run the profiling task" producing profile.prof
    try:
        prof_path = os.path.join(PROJECT, 'profile.prof')
        if not os.path.exists(prof_path):
            print("FAIL: Component 3 -- profile.prof does not exist")
        else:
            # Verify it's a valid pstats file by loading it
            import pstats
            stats = pstats.Stats(prof_path)
            num_entries = len(stats.stats)
            if num_entries > 0:
                print(f"PASS: Component 3 -- profile.prof is a valid pstats file with {num_entries} entries (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 -- profile.prof exists but has 0 entries")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: performance_report.md documents top 5 slowest functions (0.35 points)
    # Task requirement: "Create a performance_report.md documenting findings"
    # with "identifying the top 5 slowest functions"
    try:
        report_path = os.path.join(PROJECT, 'performance_report.md')
        if not os.path.exists(report_path):
            print("FAIL: Component 4 -- performance_report.md does not exist")
        else:
            with open(report_path, 'r') as f:
                report_content = f.read()

            report_lower = report_content.lower()
            sub_score = 0.0

            # 4a: Report exists and has substantial content (0.1 points)
            if len(report_content) > 100:
                sub_score += 0.1
                print(f"PASS: Component 4a -- performance_report.md has substantial content ({len(report_content)} chars)")
            else:
                print(f"FAIL: Component 4a -- performance_report.md is too short ({len(report_content)} chars)")

            # 4b: Report mentions profiling methodology (0.05 points)
            if 'cprofile' in report_lower or 'pstats' in report_lower or 'profil' in report_lower:
                sub_score += 0.05
                print("PASS: Component 4b -- report mentions profiling methodology")
            else:
                print("FAIL: Component 4b -- report does not mention profiling methodology")

            # 4c: Report contains function timing data -- at least 5 function entries (0.15 points)
            # Look for patterns like time values (seconds) and function names
            # Count rows that look like profiling data (numbers + function references)
            timing_pattern = re.findall(r'\d+\.\d+\s*s|\d+\.\d+\s*\|', report_content)
            function_refs = re.findall(r'`[^`]+`|__\w+__|\.py:\d+|{built-in|<\w+>', report_content)
            if len(timing_pattern) >= 5 and len(function_refs) >= 3:
                sub_score += 0.15
                print(f"PASS: Component 4c -- report has timing data ({len(timing_pattern)} timing entries, {len(function_refs)} function refs)")
            elif len(timing_pattern) >= 3 or len(function_refs) >= 3:
                sub_score += 0.05
                print(f"PARTIAL: Component 4c -- some timing/function data found ({len(timing_pattern)} timing, {len(function_refs)} func refs)")
            else:
                print(f"FAIL: Component 4c -- insufficient timing/function data ({len(timing_pattern)} timing, {len(function_refs)} func refs)")

            # 4d: Report mentions top 5 / slowest / performance analysis (0.05 points)
            if ('top 5' in report_lower or 'top five' in report_lower or
                'slowest' in report_lower or 'most time' in report_lower or
                ('rank' in report_lower and 'function' in report_lower)):
                sub_score += 0.05
                print("PASS: Component 4d -- report references top 5 slowest functions")
            else:
                print("FAIL: Component 4d -- report does not reference top 5 slowest functions")

            total_score += sub_score
            print(f"Component 4 total: {sub_score}/0.35")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
