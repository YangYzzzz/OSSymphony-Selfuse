"""
Reward Script: Add semicolons to lines missing them in statements.js
Task ID: vscode_edit_037
Domain: vs_code
Scoring:
  Component 1: All 12 lines that lacked semicolons now end with semicolons (0.6 pts)
               Partial credit: 0.05 per semicolon added, up to 0.6
  Component 2: Full file content matches expected golden content exactly (0.4 pts)
               Checks both that added semicolons are correct AND no line was corrupted
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_037'
FILE_PATH = '/home/user/Desktop/statements.js'

# Lines in the initial file that did NOT end with ; { or }
# (0-indexed). These must gain a semicolon in the golden file.
LINES_NEEDING_SEMICOLONS = [0, 3, 6, 9, 10, 15, 18, 20, 23, 25, 27, 29]

# Expected full content of the golden file — all 30 lines (stripped of trailing newline)
# Derived from the task requirements: append ';' to lines that lacked termination
EXPECTED_LINES = [
    "const API_URL = 'https://api.acme.com';",    # 0: was missing ;
    "const TIMEOUT = 3000;",                       # 1: unchanged
    "let isConnected = false;",                    # 2: unchanged
    "let currentUser = null;",                     # 3: was missing ;
    "let retryCount = 0;",                         # 4: unchanged
    "function connect(host, port) {",              # 5: unchanged
    "    const socket = new Socket();",            # 6: was missing ;
    "    socket.setTimeout(TIMEOUT);",             # 7: unchanged
    "    socket.connect(port, host);",             # 8: unchanged
    "    isConnected = true;",                     # 9: was missing ;
    "    return socket;",                          # 10: was missing ;
    "}",                                           # 11: unchanged
    "function disconnect() {",                     # 12: unchanged
    "    isConnected = false;",                    # 13: unchanged
    "    currentUser = null;",                     # 14: unchanged
    "    retryCount = 0;",                         # 15: was missing ;
    "}",                                           # 16: unchanged
    "function authenticate(username, pwd) {",      # 17: unchanged
    "    const token = btoa(username + pwd);",     # 18: was missing ;
    "    currentUser = username;",                 # 19: unchanged
    "    return token;",                           # 20: was missing ;
    "}",                                           # 21: unchanged
    "function fetchData(endpoint) {",             # 22: unchanged
    "    const url = API_URL + endpoint;",         # 23: was missing ;
    "    const res = fetch(url);",                 # 24: unchanged
    "    return res;",                             # 25: was missing ;
    "}",                                           # 26: unchanged
    "const defaultHost = 'localhost';",            # 27: was missing ;
    "const defaultPort = 8080;",                   # 28: unchanged
    "exports.connect = connect;",                  # 29: was missing ;
]


def verify_task(file_path):
    """
    Verify that all 12 lines missing semicolons now end with semicolons,
    and that no other lines were changed.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.splitlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: All 12 lines that lacked semicolons now end with ';' (0.6 pts)
    # This FAILS on initial_env (0 of 12 have semicolons) and PASSES on golden_env
    # -----------------------------------------------------------------------
    try:
        semicolons_added = 0
        missing_semicolons = []
        for idx in LINES_NEEDING_SEMICOLONS:
            if idx < len(lines):
                line = lines[idx]
                if line.rstrip().endswith(';'):
                    semicolons_added += 1
                else:
                    missing_semicolons.append((idx + 1, line))
            else:
                missing_semicolons.append((idx + 1, '<line missing>'))

        if semicolons_added == 12:
            print(f"PASS: Component 1 — All 12 lines now end with semicolons (0.6 pts)")
            total_score += 0.6
        else:
            partial = round(0.05 * semicolons_added, 3)
            if semicolons_added > 0:
                print(f"PARTIAL: Component 1 — {semicolons_added}/12 lines have semicolons ({partial} pts)")
            else:
                print(f"FAIL: Component 1 — 0/12 lines have semicolons (0.0 pts)")
            if missing_semicolons:
                print(f"  Missing semicolons on lines: {[ln for ln, _ in missing_semicolons]}")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Full file content matches expected golden content (0.4 pts)
    # Verifies: (a) semicolons were added correctly (exact content), and
    #           (b) no previously-terminated lines were corrupted.
    # This FAILS on initial_env because EXPECTED_LINES has semicolons on lines
    # that the initial file lacks. PASSES on golden_env if content matches exactly.
    # -----------------------------------------------------------------------
    try:
        if len(lines) != 30:
            print(f"FAIL: Component 2 — File has {len(lines)} lines, expected 30 (0.0 pts)")
        else:
            mismatched = []
            for i, (actual, expected) in enumerate(zip(lines, EXPECTED_LINES)):
                if actual.rstrip() != expected:
                    mismatched.append((i + 1, repr(actual.rstrip()), repr(expected)))

            if not mismatched:
                print(f"PASS: Component 2 — All 30 lines match expected golden content (0.4 pts)")
                total_score += 0.4
            else:
                # Binary: all-or-nothing for exact content match
                # (partial credit for incomplete semicolons is already covered in Component 1)
                print(f"FAIL: Component 2 — {len(mismatched)}/30 lines do not match expected content (0.0 pts)")
                print(f"  Mismatched lines ({len(mismatched)}):")
                for ln, actual_r, expected_r in mismatched[:5]:
                    print(f"    Line {ln}: actual={actual_r}, expected={expected_r}")
                if len(mismatched) > 5:
                    print(f"    ... and {len(mismatched) - 5} more")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 3), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
