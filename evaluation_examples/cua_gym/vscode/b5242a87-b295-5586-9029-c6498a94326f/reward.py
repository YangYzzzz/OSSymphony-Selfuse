"""
Reward Script: Go linting setup and lint fix verification
Task ID: vscode_gf6_007
Domain: vscode
Scoring:
  Component 1: golangci-lint binary installed (0.15)
  Component 2: .golangci.yml config correct (0.25)
  Component 3: Makefile lint target exists (0.15)
  Component 4: .vscode/tasks.json golangci-lint task (0.15)
  Component 5: handler.go lint issues fixed (0.30)
"""

import os
import json
import re

WORKDIR = '/home/user/projects/go-linting'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: golangci-lint binary is installed and accessible (0.15 points)
    try:
        # Check common install locations
        golangci_paths = [
            '/home/user/go/bin/golangci-lint',
            '/usr/local/bin/golangci-lint',
            '/usr/bin/golangci-lint',
        ]
        binary_found = False
        for p in golangci_paths:
            if os.path.isfile(p) and os.access(p, os.X_OK):
                binary_found = True
                print(f"PASS: Component 1 -- golangci-lint binary found at {p} (0.15 pts)")
                total_score += 0.15
                break
        if not binary_found:
            # Also check PATH via shutil.which
            import shutil
            which_result = shutil.which('golangci-lint')
            if which_result:
                binary_found = True
                print(f"PASS: Component 1 -- golangci-lint found in PATH at {which_result} (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 1 -- golangci-lint binary not found in any expected location")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: .golangci.yml exists with correct configuration (0.25 points)
    golangci_yml_path = os.path.join(WORKDIR, '.golangci.yml')
    try:
        if not os.path.isfile(golangci_yml_path):
            print("FAIL: Component 2 -- .golangci.yml does not exist")
        else:
            with open(golangci_yml_path, 'r') as f:
                content = f.read()

            comp2_score = 0.0

            # Check required linters are enabled
            required_linters = ['gofmt', 'govet', 'errcheck', 'staticcheck', 'gosimple', 'ineffassign']
            linters_found = []
            for linter in required_linters:
                if re.search(r'[-\s]' + re.escape(linter) + r'\s*$', content, re.MULTILINE):
                    linters_found.append(linter)

            if len(linters_found) == len(required_linters):
                comp2_score += 0.15
                print(f"PASS: Component 2a -- All 6 required linters found: {linters_found}")
            else:
                missing = set(required_linters) - set(linters_found)
                print(f"FAIL: Component 2a -- Missing linters: {missing}")

            # Check timeout setting (5m)
            if re.search(r'timeout:\s*5m', content):
                comp2_score += 0.05
                print("PASS: Component 2b -- timeout: 5m found")
            else:
                print("FAIL: Component 2b -- timeout: 5m not found")

            # Check vendor/ exclusion
            if 'vendor' in content:
                comp2_score += 0.05
                print("PASS: Component 2c -- vendor/ exclusion found")
            else:
                print("FAIL: Component 2c -- vendor/ exclusion not found")

            total_score += comp2_score
            print(f"Component 2 total: {comp2_score}/0.25")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Makefile has 'lint' target that runs golangci-lint (0.15 points)
    makefile_path = os.path.join(WORKDIR, 'Makefile')
    try:
        if not os.path.isfile(makefile_path):
            print("FAIL: Component 3 -- Makefile does not exist")
        else:
            with open(makefile_path, 'r') as f:
                makefile_content = f.read()

            # Check for lint target that calls golangci-lint
            has_lint_target = bool(re.search(r'^lint\s*:', makefile_content, re.MULTILINE))
            has_golangci_cmd = 'golangci-lint' in makefile_content

            if has_lint_target and has_golangci_cmd:
                print("PASS: Component 3 -- Makefile has 'lint' target running golangci-lint (0.15 pts)")
                total_score += 0.15
            elif has_lint_target:
                print("FAIL: Component 3 -- lint target exists but doesn't reference golangci-lint")
            else:
                print("FAIL: Component 3 -- No 'lint' target in Makefile")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: .vscode/tasks.json has golangci-lint task (0.15 points)
    tasks_path = os.path.join(WORKDIR, '.vscode', 'tasks.json')
    try:
        if not os.path.isfile(tasks_path):
            print("FAIL: Component 4 -- .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            tasks_json = json.loads(cleaned)

            tasks_list = tasks_json.get('tasks', [])
            found_task = False
            for task in tasks_list:
                label = task.get('label', '').lower()
                command = task.get('command', '').lower()
                if 'golangci' in label and ('make lint' in command or 'golangci-lint' in command):
                    found_task = True
                    break

            if found_task:
                print("PASS: Component 4 -- tasks.json has golangci-lint task running 'make lint' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- No golangci-lint task found in tasks.json. Labels: {[t.get('label') for t in tasks_list]}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: handler.go lint issues are fixed (0.30 points)
    handler_path = os.path.join(WORKDIR, 'internal', 'api', 'handler.go')
    try:
        if not os.path.isfile(handler_path):
            print("FAIL: Component 5 -- handler.go does not exist")
        else:
            with open(handler_path, 'r') as f:
                handler_content = f.read()

            comp5_score = 0.0

            # Fix 1: Unchecked error returns from json.NewEncoder(w).Encode() should be checked
            # In initial: bare `json.NewEncoder(w).Encode(resp)` without error capture
            # In golden: `if err := json.NewEncoder(w).Encode(resp); err != nil {`
            # Check that there are NO bare Encode calls (all should be error-checked)
            bare_encode_calls = re.findall(r'^\s+json\.NewEncoder\(w\)\.Encode\(\w+\)\s*$', handler_content, re.MULTILINE)
            checked_encode_calls = re.findall(r'err\s*:?=\s*json\.NewEncoder\(w\)\.Encode', handler_content)

            if len(bare_encode_calls) == 0 and len(checked_encode_calls) > 0:
                comp5_score += 0.10
                print(f"PASS: Component 5a -- All Encode calls have error checking ({len(checked_encode_calls)} checked, 0 bare)")
            else:
                print(f"FAIL: Component 5a -- Found {len(bare_encode_calls)} bare Encode calls, {len(checked_encode_calls)} checked")

            # Fix 2: No unused variable 'result' -- the variable should either be used or removed
            # In initial: `result := fetchUserFromDB(userID)` followed by `_ = result`
            if 'result := fetchUserFromDB' not in handler_content and '_ = result' not in handler_content:
                comp5_score += 0.10
                print("PASS: Component 5b -- Unused variable 'result' has been removed/refactored")
            else:
                print("FAIL: Component 5b -- Unused variable 'result' pattern still present")

            # Fix 3: fmt.Println replaced with proper logging (log package)
            # In initial: uses `"fmt"` import and `fmt.Println(...)` for logging
            # In golden: uses `"log"` import and `log.Printf(...)`
            # Only match fmt.Println in actual code lines, not in comments
            uses_fmt_println = False
            for line in handler_content.split('\n'):
                stripped = line.strip()
                # Skip comment-only lines
                if stripped.startswith('//') or stripped.startswith('/*'):
                    continue
                # Check for fmt.Println in non-comment portion of line
                code_part = line.split('//')[0]  # strip inline comments
                if 'fmt.Println' in code_part:
                    uses_fmt_println = True
                    break
            uses_log = bool(re.search(r'log\.(Printf|Println|Print)\(', handler_content))

            if not uses_fmt_println and uses_log:
                comp5_score += 0.10
                print("PASS: Component 5c -- fmt.Println replaced with log package")
            elif not uses_fmt_println:
                comp5_score += 0.05
                print("PARTIAL: Component 5c -- fmt.Println removed but log package not clearly used")
            else:
                print("FAIL: Component 5c -- fmt.Println still present in handler.go")

            total_score += comp5_score
            print(f"Component 5 total: {comp5_score}/0.30")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
