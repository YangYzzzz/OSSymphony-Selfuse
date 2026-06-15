"""
Reward Script: Format only the SQL query string inside the getUsers function
Task ID: vscode_code_007
Domain: vs_code
Scoring:
  Component 1: SQL template literal is multi-line (>= 5 non-empty lines) (0.40 pts)
  Component 2: All 6 SQL clauses (SELECT, FROM, INNER JOIN, WHERE, ORDER BY, LIMIT)
               each start their own line (0.40 pts)
  Component 3: All original SQL identifiers and data values preserved in reformatted query (0.20 pts)
  Total: 1.00

Gate (no score): Outer JS file structure (require, async function, return, module.exports) intact.
  If missing, return 0.0 immediately.

Design rationale:
  - Components 1, 2, and 3 all exclusively measure the formatting change
    (single-line -> multi-line), not pre-existing properties.
  - Component 3 is gated on Component 1 passing (multi-line check),
    preventing it from passing on initial_env where the query is single-line
    but all identifiers exist.
  - "Rest of file unchanged" is purely a precondition gate (no score).
"""

import os
import re

FILE_PATH = '/home/user/project/db.js'


def verify_task(file_path):
    """
    Verify that the SQL query inside getUsers() has been reformatted to multi-line,
    with each clause on its own line, while the surrounding file structure is unchanged.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: load file ---
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Precondition gate: outer JS structure must be intact ---
    outer_checks = {
        "require('./database') import": bool(re.search(r"const\s+db\s*=\s*require\(['\"]\.\/database['\"]\)", content)),
        "async function getUsers()": bool(re.search(r"async\s+function\s+getUsers\s*\(\s*\)", content)),
        "return db.execute(query)": bool(re.search(r"return\s+db\.execute\(query\)", content)),
        "module.exports = { getUsers }": bool(re.search(r"module\.exports\s*=\s*\{\s*getUsers\s*\}", content)),
    }
    failed_outer = [k for k, v in outer_checks.items() if not v]
    if failed_outer:
        print(f"GATE FAIL: Outer file structure is missing required elements: {failed_outer}")
        print("REWARD: 0.0")
        return 0.0
    print("GATE PASS: Outer JS structure intact (precondition only, no score)")

    # --- Precondition gate: find the template literal ---
    tl_match = re.search(r'const\s+query\s*=\s*`([^`]*)`', content, re.DOTALL)
    if not tl_match:
        print("GATE FAIL: Could not find 'const query = `...`' template literal in getUsers")
        print("REWARD: 0.0")
        return 0.0

    query_body = tl_match.group(1)
    query_lines = [line.strip() for line in query_body.split('\n') if line.strip()]
    print(f"INFO: Query template literal has {len(query_lines)} non-empty lines")

    # ---- Component 1: SQL template literal is multi-line (0.40 pts) ----
    # Initial state: entire SQL is ONE line (1 non-empty line in the template literal).
    # After reformatting: must span at least 5 lines (SELECT, FROM, INNER JOIN, WHERE, ORDER BY/LIMIT).
    # This FAILS on initial_env (1 line), PASSES on golden_env (>= 5 lines).
    try:
        if len(query_lines) >= 5:
            print(f"PASS: Component 1 — SQL template literal spans {len(query_lines)} lines (>= 5 required) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — SQL template literal has {len(query_lines)} line(s) (expected >= 5); SQL not reformatted to multi-line")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: All required SQL clauses are each on their own line (0.40 pts) ----
    # Required: SELECT, FROM, INNER JOIN, WHERE, ORDER BY, LIMIT — each must start its own line.
    # This FAILS on initial_env (single-line query), PASSES on golden_env (clause-per-line).
    try:
        required_clauses = ['SELECT', 'FROM', 'INNER JOIN', 'WHERE', 'ORDER BY', 'LIMIT']
        clause_found = {}
        for clause in required_clauses:
            found = any(line.upper().startswith(clause) for line in query_lines)
            clause_found[clause] = found

        all_found = all(clause_found.values())
        missing = [c for c, v in clause_found.items() if not v]

        if all_found:
            print(f"PASS: Component 2 — All 6 SQL clauses on separate lines: {required_clauses} (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 2 — Missing clauses on their own lines: {missing}")
            print(f"  Detected query lines: {query_lines}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: SQL preserves key identifiers and is correctly reformatted (0.20 pts) ----
    # After reformatting, all key table/column identifiers, conditions, and values must be present.
    # Gated on Component 1 (multi-line check) to prevent passing on initial_env where the SQL
    # is single-line but all identifiers naturally exist.
    try:
        full_query_text = query_body.replace('\n', ' ').lower()

        # Key identifiers from the original SQL that must be preserved
        required_tokens = [
            'select',
            'u.id',
            'u.name',
            'u.email',
            'p.role',
            'p.department',
            'from users',
            'inner join profiles',
            'u.id = p.user_id',
            'where',
            'u.active',
            "engineering",
            'order by',
            'u.name asc',
            'limit 100',
        ]

        tokens_found = [t for t in required_tokens if t in full_query_text]
        tokens_missing = [t for t in required_tokens if t not in full_query_text]

        # Only award these 0.20 pts if the SQL is ALSO multi-line (Component 1 passed)
        if len(query_lines) >= 5 and len(tokens_missing) == 0:
            print(f"PASS: Component 3 — All {len(required_tokens)} SQL identifiers/values preserved in reformatted query (0.20 pts)")
            total_score += 0.20
        elif len(query_lines) < 5:
            print(f"FAIL: Component 3 — SQL is not multi-line; content preservation check skipped (requires Component 1 to pass first)")
        else:
            print(f"FAIL: Component 3 — Missing SQL identifiers/values: {tokens_missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — runs on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
