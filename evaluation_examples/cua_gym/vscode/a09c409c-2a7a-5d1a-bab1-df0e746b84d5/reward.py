"""
Reward Script: Configure workspace-level spell checking for ~/projects/technical-blog
Task ID: vscode_gf5_046
Domain: vscode
Scoring:
  Component 1 (0.25): Code Spell Checker extension installed
  Component 2 (0.30): cspell.json exists with correct 5 technical words
  Component 3 (0.15): "recieve" corrected to "receive" in intro.md
  Component 4 (0.15): "occured" corrected to "occurred" in intro.md
  Component 5 (0.15): "successfull" corrected to "successful" in intro.md
"""

import os
import json
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_046'
BLOG_DIR = os.path.join(WORKDIR, 'projects', 'technical-blog')
INTRO_PATH = os.path.join(BLOG_DIR, 'posts', 'intro.md')
CSPELL_PATH = os.path.join(BLOG_DIR, 'cspell.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Code Spell Checker extension is installed (0.25 points)
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower().split('\n')
        if 'streetsidesoftware.code-spell-checker' in extensions:
            print("PASS: Component 1 — Code Spell Checker extension is installed (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Code Spell Checker not found in installed extensions: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: cspell.json exists with the 5 required technical words (0.30 points)
    try:
        if not os.path.exists(CSPELL_PATH):
            print(f"FAIL: Component 2 — cspell.json does not exist at {CSPELL_PATH}")
        else:
            with open(CSPELL_PATH, 'r') as f:
                cspell_config = json.load(f)
            words_list = cspell_config.get('words', [])
            # Normalize to lowercase for comparison
            words_lower = [w.lower() for w in words_list]
            required_words = ['api', 'endpoint', 'middleware', 'oauth', 'webhook']
            missing = [w for w in required_words if w not in words_lower]
            if len(missing) == 0:
                print(f"PASS: Component 2 — cspell.json has all 5 technical words: {words_list} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — cspell.json missing words: {missing}. Found: {words_list}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Read intro.md for typo checks (Components 3-5)
    try:
        with open(INTRO_PATH, 'r') as f:
            intro_content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read {INTRO_PATH}: {e}")
        intro_content = None

    if intro_content is not None:
        # Component 3: "recieve" corrected to "receive" (0.15 points)
        try:
            content_lower = intro_content.lower()
            if 'recieve' in content_lower:
                print("FAIL: Component 3 — 'recieve' typo still present in intro.md")
            elif 'receive' in content_lower:
                print("PASS: Component 3 — 'recieve' corrected to 'receive' (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 3 — neither 'recieve' nor 'receive' found in intro.md")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

        # Component 4: "occured" corrected to "occurred" (0.15 points)
        try:
            if 'occured' in content_lower:
                print("FAIL: Component 4 — 'occured' typo still present in intro.md")
            elif 'occurred' in content_lower:
                print("PASS: Component 4 — 'occured' corrected to 'occurred' (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 4 — neither 'occured' nor 'occurred' found in intro.md")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")

        # Component 5: "successfull" corrected to "successful" (0.15 points)
        try:
            if 'successfull ' in content_lower or content_lower.rstrip().endswith('successfull'):
                print("FAIL: Component 5 — 'successfull' typo still present in intro.md")
            elif 'successful' in content_lower:
                print("PASS: Component 5 — 'successfull' corrected to 'successful' (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: Component 5 — neither 'successfull' nor 'successful' found in intro.md")
        except Exception as e:
            print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
