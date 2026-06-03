"""
Reward Script: Create React TypeScript user snippets in VSCode
Task ID: vscode_code_096
Domain: vs_code
Scoring:
  Component 1: typescriptreact.json exists and is valid JSON (0.20 pts)
  Component 2: React Functional Component snippet (prefix 'rfc') with correct body (0.30 pts)
  Component 3: useState Hook snippet (prefix 'ust') with correct body (0.15 pts)
  Component 4: useEffect Hook snippet (prefix 'uef') with correct body (0.20 pts)
  Component 5: Custom Hook snippet (prefix 'hook') with correct body (0.15 pts)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_096'
SNIPPETS_PATH = '/home/user/.config/Code/User/snippets/typescriptreact.json'


def _is_subset(expected, actual):
    """Recursively check that expected is a subset of actual."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    snippets = None

    # ---- Component 1: File exists and is valid JSON (0.20 pts) ----
    # This fails on initial_env (no file) and passes on golden_env (file present)
    try:
        file_exists = os.path.exists(SNIPPETS_PATH)
        if file_exists:
            with open(SNIPPETS_PATH, 'r') as f:
                snippets = json.load(f)
            valid_json = snippets is not None
        else:
            valid_json = False

        if file_exists and valid_json:
            print(f"PASS: Component 1 — typescriptreact.json exists and is valid JSON (0.20 pts)")
            total_score += 0.20
        elif not file_exists:
            print(f"FAIL: Component 1 — {SNIPPETS_PATH} does not exist")
        else:
            print(f"FAIL: Component 1 — File exists but is not valid JSON")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — File exists but contains invalid JSON: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    if snippets is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ---- Component 2: React Functional Component snippet (0.30 pts) ----
    # Verify prefix='rfc' and body contains the TypeScript FC structure
    try:
        expected_rfc = {
            "prefix": "rfc",
            "body": [
                "import React from 'react';",
                "",
                "interface ${1:Component}Props {",
                "  ${2:// props}",
                "}",
                "",
                "const ${1:Component}: React.FC<${1:Component}Props> = ({ ${3:} }) => {",
                "  return (",
                "    <div>",
                "      $0",
                "    </div>",
                "  );",
                "};",
                "",
                "export default ${1:Component};"
            ],
            "description": "React Functional Component with TypeScript"
        }

        rfc_key = "React Functional Component"
        rfc_present = rfc_key in snippets
        rfc_matches = rfc_present and _is_subset(expected_rfc, snippets[rfc_key])

        if rfc_matches:
            print(f"PASS: Component 2 — 'React Functional Component' snippet (prefix='rfc') correct (0.30 pts)")
            total_score += 0.30
        elif not rfc_present:
            print(f"FAIL: Component 2 — '{rfc_key}' snippet not found in file")
        else:
            actual = snippets[rfc_key]
            print(f"FAIL: Component 2 — '{rfc_key}' snippet does not match expected structure")
            print(f"  Expected prefix: 'rfc', actual: {actual.get('prefix')}")
            print(f"  Body matches: {actual.get('body') == expected_rfc['body']}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: useState Hook snippet (0.15 pts) ----
    # Verify prefix='ust' and body contains useState TypeScript line
    try:
        expected_ust = {
            "prefix": "ust",
            "body": [
                "const [${1:state}, set${1/(.*)/${1:/capitalize}/}] = useState<${2:type}>(${3:initialValue});"
            ],
            "description": "useState with TypeScript"
        }

        ust_key = "useState Hook"
        ust_present = ust_key in snippets
        ust_matches = ust_present and _is_subset(expected_ust, snippets[ust_key])

        if ust_matches:
            print(f"PASS: Component 3 — 'useState Hook' snippet (prefix='ust') correct (0.15 pts)")
            total_score += 0.15
        elif not ust_present:
            print(f"FAIL: Component 3 — '{ust_key}' snippet not found in file")
        else:
            actual = snippets[ust_key]
            print(f"FAIL: Component 3 — '{ust_key}' snippet does not match expected structure")
            print(f"  Expected prefix: 'ust', actual: {actual.get('prefix')}")
            print(f"  Body matches: {actual.get('body') == expected_ust['body']}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: useEffect Hook snippet (0.20 pts) ----
    # Verify prefix='uef' and body contains useEffect structure with cleanup
    try:
        expected_uef = {
            "prefix": "uef",
            "body": [
                "useEffect(() => {",
                "  ${1:// effect}",
                "  return () => {",
                "    ${2:// cleanup}",
                "  };",
                "}, [${3:dependencies}]);"
            ],
            "description": "useEffect with cleanup"
        }

        uef_key = "useEffect Hook"
        uef_present = uef_key in snippets
        uef_matches = uef_present and _is_subset(expected_uef, snippets[uef_key])

        if uef_matches:
            print(f"PASS: Component 4 — 'useEffect Hook' snippet (prefix='uef') correct (0.20 pts)")
            total_score += 0.20
        elif not uef_present:
            print(f"FAIL: Component 4 — '{uef_key}' snippet not found in file")
        else:
            actual = snippets[uef_key]
            print(f"FAIL: Component 4 — '{uef_key}' snippet does not match expected structure")
            print(f"  Expected prefix: 'uef', actual: {actual.get('prefix')}")
            print(f"  Body matches: {actual.get('body') == expected_uef['body']}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: Custom Hook snippet (0.15 pts) ----
    # Verify prefix='hook' and body contains custom hook function structure
    try:
        expected_hook = {
            "prefix": "hook",
            "body": [
                "import { useState, useEffect } from 'react';",
                "",
                "function use${1:HookName}(${2:params}): ${3:ReturnType} {",
                "  const [${4:state}, set${4/(.*)/${1:/capitalize}/}] = useState<${5:type}>(${6:initial});",
                "",
                "  useEffect(() => {",
                "    ${7:// effect}",
                "  }, []);",
                "",
                "  return ${4:state};",
                "}",
                "",
                "export default use${1:HookName};"
            ],
            "description": "Custom React Hook"
        }

        hook_key = "Custom Hook"
        hook_present = hook_key in snippets
        hook_matches = hook_present and _is_subset(expected_hook, snippets[hook_key])

        if hook_matches:
            print(f"PASS: Component 5 — 'Custom Hook' snippet (prefix='hook') correct (0.15 pts)")
            total_score += 0.15
        elif not hook_present:
            print(f"FAIL: Component 5 — '{hook_key}' snippet not found in file")
        else:
            actual = snippets[hook_key]
            print(f"FAIL: Component 5 — '{hook_key}' snippet does not match expected structure")
            print(f"  Expected prefix: 'hook', actual: {actual.get('prefix')}")
            print(f"  Body matches: {actual.get('body') == expected_hook['body']}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
