"""
Reward Script: Configure project-specific cSpell dictionary with custom words
Task ID: vscode_lp_095
Domain: vs-code (cspell.json verification)
Scoring:
  - Component 1 (0.2): cspell.json exists and is valid JSON with "words" key
  - Component 2 (0.2): "words" is a list containing at least the 6 required terms
  - Component 3 (0.6): Each of the 6 required words present (0.1 each)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_095'

# The task requires these exact words in the cspell.json "words" array
REQUIRED_WORDS = ["FastAPI", "PostgreSQL", "Kubernetes", "pydantic", "uvicorn", "sqlalchemy"]

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Locate cspell.json in the project root
    file_path = os.path.join(WORKDIR, 'workspace', 'cspell.json')

    # Component 1: cspell.json exists and is valid JSON with "words" key (0.2 points)
    # This check FAILS on initial_env (file does not exist) and PASSES on golden_env
    data = None
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 -- cspell.json not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        with open(file_path, 'r') as f:
            data = json.load(f)

        if isinstance(data, dict) and "words" in data:
            print(f"PASS: Component 1 -- cspell.json exists, valid JSON, has 'words' key (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- cspell.json missing 'words' key or not a dict. Keys: {list(data.keys()) if isinstance(data, dict) else type(data).__name__}")
            print("REWARD: 0.0")
            return 0.0
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 -- cspell.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: "words" is a list with at least 6 entries (0.2 points)
    try:
        words_list = data.get("words", [])
        if isinstance(words_list, list) and len(words_list) >= len(REQUIRED_WORDS):
            print(f"PASS: Component 2 -- 'words' is a list with {len(words_list)} entries (0.2 pts)")
            total_score += 0.2
        elif not isinstance(words_list, list):
            print(f"FAIL: Component 2 -- 'words' is not a list, got {type(words_list).__name__}")
        else:
            print(f"FAIL: Component 2 -- 'words' has {len(words_list)} entries, expected at least {len(REQUIRED_WORDS)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Each required word is present in the words list (0.1 points each, 0.6 total)
    # Case-insensitive comparison since cSpell words are case-insensitive
    try:
        words_lower = [w.lower() for w in words_list] if isinstance(words_list, list) else []
        for word in REQUIRED_WORDS:
            if word.lower() in words_lower:
                print(f"PASS: Component 3 -- '{word}' found in words list (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 -- '{word}' NOT found in words list")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
