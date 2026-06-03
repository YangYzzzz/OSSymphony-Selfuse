"""
Reward Script: Create a CSS snippet for flexbox container layout with prefix 'flexbox'
Task ID: vscode_code_019
Domain: vs_code
Scoring:
  Component 1: Snippet key 'Flexbox Container' exists in css.json (0.2 pts)
  Component 2: Snippet prefix is 'flexbox' (0.2 pts)
  Component 3: Snippet body contains required CSS flexbox properties (0.4 pts)
  Component 4: Snippet body uses choice tab stops (|option1,option2| format) (0.1 pts)
  Component 5: Snippet description is 'Flexbox container layout' (0.1 pts)
Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_019'
SNIPPETS_PATH = os.path.expanduser('~/.config/Code/User/snippets/css.json')


def verify_task(snippets_path):
    """
    Verify that the CSS snippet for flexbox container has been created.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: css.json must exist and be valid JSON
    try:
        with open(snippets_path, 'r') as f:
            snippets = json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL: css.json not found at {snippets_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: css.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: snippets must be a non-empty dict
    if not isinstance(snippets, dict) or len(snippets) == 0:
        print("FAIL: css.json is empty or not a dict — no snippets found")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: Snippet key 'Flexbox Container' exists (0.2 points)
    try:
        snippet_key = None
        # Check for exact key match first, then case-insensitive
        if 'Flexbox Container' in snippets:
            snippet_key = 'Flexbox Container'
        else:
            # Try case-insensitive lookup
            for key in snippets:
                if key.lower() == 'flexbox container':
                    snippet_key = key
                    break

        if snippet_key is not None:
            print(f"PASS: Component 1 — Snippet key '{snippet_key}' found in css.json (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected snippet key 'Flexbox Container' not found. Keys present: {list(snippets.keys())}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    snippet = snippets[snippet_key]

    # Component 2: Prefix is 'flexbox' (0.2 points)
    try:
        actual_prefix = snippet.get('prefix', None)
        if actual_prefix == 'flexbox':
            print(f"PASS: Component 2 — prefix is 'flexbox' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — expected prefix 'flexbox', found: '{actual_prefix}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Body contains required CSS flexbox properties (0.4 points)
    try:
        body = snippet.get('body', [])
        if not isinstance(body, list):
            print(f"FAIL: Component 3 — 'body' is not a list, got: {type(body)}")
        else:
            body_str = '\n'.join(body)
            # Check for required CSS properties
            required_properties = {
                'display: flex': 'display: flex',
                'flex-direction': 'flex-direction',
                'justify-content': 'justify-content',
                'align-items': 'align-items',
                'gap': 'gap',
            }
            missing = []
            for prop_name, prop_str in required_properties.items():
                if prop_str not in body_str:
                    missing.append(prop_name)

            if not missing:
                print(f"PASS: Component 3 — body contains all required CSS flexbox properties: display:flex, flex-direction, justify-content, align-items, gap (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — body missing required CSS properties: {missing}")
                print(f"  Body content: {body_str[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Body uses choice tab stops (|option1,option2| format) (0.1 points)
    try:
        body = snippet.get('body', [])
        body_str = '\n'.join(body) if isinstance(body, list) else str(body)
        # Choice tab stops look like ${N|option1,option2|}
        import re
        choice_stops = re.findall(r'\$\{\d+\|[^|]+\|[^|]*\}', body_str)
        if len(choice_stops) >= 1:
            print(f"PASS: Component 4 — body uses choice tab stops ({len(choice_stops)} found: {choice_stops[:3]}) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — body does not use choice tab stops (|option1,option2| format). Body: {body_str[:300]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Description is 'Flexbox container layout' (0.1 points)
    try:
        actual_description = snippet.get('description', None)
        if actual_description and actual_description.lower() == 'flexbox container layout':
            print(f"PASS: Component 5 — description is '{actual_description}' (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 — expected description 'Flexbox container layout', found: '{actual_description}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical snippet file path on the VM
if not os.path.exists(SNIPPETS_PATH):
    print(f"File not found: {SNIPPETS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SNIPPETS_PATH)
