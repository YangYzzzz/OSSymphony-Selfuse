"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m migrating my Node.js project to CommonJS—could you replace every occurrence of “import” with “require” in /home/user/project/server.js?
Generated: 2025-09-11 13:56:46
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import re


def verify_commonjs_migration():
    """Reward script that verifies the migration of /home/user/project/server.js
    from ES modules to CommonJS.

    Scoring (progressive):
        0.5 pts – No standalone 'import' keywords remain
        0.5 pts – At least one 'require(' call is present
    The script returns a float between 0.0 and 1.0 and prints
    diagnostic information plus the final reward in the form
    'REWARD: X.X'.
    """

    target_path = "/home/user/project/server.js"
    max_score = 1.0
    score = 0.0

    print("--- Verifying CommonJS migration of server.js ---")

    # 0) Prerequisite: file must exist (no points, but task fails if missing)
    if not os.path.isfile(target_path):
        print(f"✗ File not found: {target_path}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ File located: {target_path}")

    # Load file content safely
    try:
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Unable to read file: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"File size: {len(content)} characters")

    # 1) Check: no standalone 'import' keywords remain
    import_regex = re.compile(r"(?:^|[^A-Za-z0-9_.$])import(?![A-Za-z0-9_])", re.MULTILINE)
    import_hits = import_regex.findall(content)
    if import_hits:
        print(f"✗ Found {len(import_hits)} remaining 'import' keyword occurrences")
    else:
        print("✓ No standalone 'import' keywords found (0.5 points)")
        score += 0.5

    # 2) Check: at least one require(...) call exists
    require_regex = re.compile(r"\brequire\s*\(")
    require_hits = require_regex.findall(content)
    if require_hits:
        print(f"✓ Detected {len(require_hits)} require(...) calls (0.5 points)")
        score += 0.5
    else:
        print("✗ No require(...) calls detected")

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_commonjs_migration()
