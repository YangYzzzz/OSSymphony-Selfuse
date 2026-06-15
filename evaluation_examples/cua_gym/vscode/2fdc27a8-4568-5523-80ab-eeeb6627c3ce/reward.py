"""
Reward Script: Verify Docker Build task with promptString input in tasks.json
Task ID: vscode_td_020
Domain: vscode
Scoring:
  - Component 1 (0.30): "Docker Build" task exists in tasks array
  - Component 2 (0.30): Docker Build command uses ${input:imageTag} correctly
  - Component 3 (0.25): inputs array has promptString entry with id "imageTag"
  - Component 4 (0.15): Original "Run Tests" task is preserved
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_020'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'containerized-app', '.vscode', 'tasks.json')


def load_tasks_json(file_path):
    """Load tasks.json, handling JSONC comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        data = load_tasks_json(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get("tasks", [])
    inputs = data.get("inputs", [])

    # Component 1: "Docker Build" task exists in tasks array (0.30 points)
    # This FAILS on initial (only "Run Tests") and PASSES on golden
    try:
        docker_task = None
        for t in tasks:
            label = t.get("label", "")
            if "docker" in label.lower() and "build" in label.lower():
                docker_task = t
                break

        if docker_task is not None:
            print(f"PASS: Component 1 — Found Docker Build task with label '{docker_task.get('label')}' (0.30 pts)")
            total_score += 0.30
        else:
            labels = [t.get("label", "") for t in tasks]
            print(f"FAIL: Component 1 — No Docker Build task found. Tasks: {labels}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Docker Build command uses ${input:imageTag} (0.30 points)
    # This FAILS on initial (no docker task) and PASSES on golden
    try:
        if docker_task is not None:
            cmd = docker_task.get("command", "")
            # Check that the command references ${input:imageTag} and builds with docker
            has_input_ref = "${input:imageTag}" in cmd
            has_docker_build = "docker build" in cmd.lower()
            has_myapp = "myapp" in cmd

            if has_input_ref and has_docker_build and has_myapp:
                print(f"PASS: Component 2 — Command correctly uses ${{input:imageTag}}: '{cmd}' (0.30 pts)")
                total_score += 0.30
            else:
                missing = []
                if not has_input_ref:
                    missing.append("${input:imageTag} reference")
                if not has_docker_build:
                    missing.append("docker build command")
                if not has_myapp:
                    missing.append("myapp image name")
                print(f"FAIL: Component 2 — Command missing: {', '.join(missing)}. Found: '{cmd}'")
        else:
            print(f"FAIL: Component 2 — No Docker Build task to check command")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: inputs array has promptString entry with id "imageTag" (0.25 points)
    # This FAILS on initial (no inputs array) and PASSES on golden
    try:
        image_tag_input = None
        for inp in inputs:
            if inp.get("id") == "imageTag":
                image_tag_input = inp
                break

        if image_tag_input is not None:
            is_prompt_string = image_tag_input.get("type") == "promptString"
            has_description = bool(image_tag_input.get("description", ""))

            if is_prompt_string and has_description:
                print(f"PASS: Component 3 — inputs has imageTag promptString with description '{image_tag_input.get('description')}' (0.25 pts)")
                total_score += 0.25
            elif is_prompt_string:
                print(f"PARTIAL: Component 3 — imageTag is promptString but missing description (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — imageTag input type is '{image_tag_input.get('type')}', expected 'promptString'")
        else:
            input_ids = [inp.get("id", "") for inp in inputs]
            print(f"FAIL: Component 3 — No input with id 'imageTag' found. Input ids: {input_ids}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Original "Run Tests" task is preserved (0.15 points)
    # This checks that the new task was ADDED without removing the existing one.
    # On initial_env this passes BUT only if there is also a Docker Build task (component 1).
    # We gate this on component 1 passing to ensure it only scores task-introduced changes.
    try:
        run_tests_found = any(
            t.get("label") == "Run Tests" for t in tasks
        )
        # Only award points if docker build task also exists (i.e., task was actually performed)
        if docker_task is not None and run_tests_found:
            print(f"PASS: Component 4 — Original 'Run Tests' task preserved alongside new task (0.15 pts)")
            total_score += 0.15
        elif docker_task is None:
            print(f"FAIL: Component 4 — Docker Build task not present, cannot verify preservation")
        else:
            print(f"FAIL: Component 4 — Original 'Run Tests' task was removed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
