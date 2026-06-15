"""
Reward Script: Auto-import useState hook from React in TypeScript file
Task ID: vscode_lp_015
Domain: vscode
Scoring:
  Component 1 (0.5): useState is imported as a named import from 'react'
  Component 2 (0.3): The import statement has correct syntax (destructured braces)
  Component 3 (0.2): File body integrity - component code is preserved after import fix
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_015'
APP_TSX_PATH = os.path.join(WORKDIR, 'workspace', 'src', 'App.tsx')


def verify_task(file_path):
    """
    Verify that useState has been properly imported from react in App.tsx.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.strip().split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: useState is imported as a named import from 'react' (0.5 points)
    # We look for an import statement that imports useState from 'react' or "react"
    try:
        # Match: import ... { ... useState ... } ... from "react" or 'react'
        # This covers: import { useState } from "react";
        #              import React, { useState } from "react";
        #              import { useState, useEffect } from "react";
        pattern_named_import = r'''import\s+.*\{[^}]*\buseState\b[^}]*\}.*from\s+['"]react['"]'''
        has_named_import = bool(re.search(pattern_named_import, content))

        if has_named_import:
            print(f"PASS: Component 1 — useState is imported as named import from 'react' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — useState is not imported as a named import from 'react'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Import statement has correct destructured syntax (0.3 points)
    # Specifically check the first line(s) for a well-formed import with { useState }
    try:
        # More specific check: the import line should be syntactically correct
        # and include useState in braces, with 'from "react"' or "from 'react'"
        # We check that the import is at the top of the file (within first 10 lines)
        top_section = '\n'.join(lines[:10])
        # Pattern: proper destructured import with useState
        pattern_correct_syntax = r'''import\s+(?:React\s*,\s*)?\{[^}]*\buseState\b[^}]*\}\s+from\s+['"]react['"];?'''
        has_correct_syntax = bool(re.search(pattern_correct_syntax, top_section))

        if has_correct_syntax:
            print(f"PASS: Component 2 — Import has correct destructured syntax at top of file (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Import syntax is not correct or not at top of file")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File body integrity (0.2 points)
    # The component body should be preserved — check key markers that exist in both initial and golden
    # but we specifically check that the file still uses useState (meaning the import was needed)
    # AND that the component structure is intact
    try:
        has_fc_component = 'const App: React.FC' in content
        has_usestate_call = 'useState<Product[]>(initialProducts)' in content
        has_search_state = 'useState<string>("")' in content
        has_export = 'export default App' in content

        # These should all be true — but this component only scores if
        # the import was ALSO added (Component 1 passed), making it a compound check
        # anchored to the task change. Without the import fix, the file is broken.
        if has_named_import and has_fc_component and has_usestate_call and has_search_state and has_export:
            print(f"PASS: Component 3 — File body integrity preserved with working imports (0.2 pts)")
            total_score += 0.2
        else:
            if not has_named_import:
                print(f"FAIL: Component 3 — Import not present, file still broken")
            else:
                missing = []
                if not has_fc_component:
                    missing.append('React.FC component declaration')
                if not has_usestate_call:
                    missing.append('useState<Product[]> call')
                if not has_search_state:
                    missing.append('useState<string> call')
                if not has_export:
                    missing.append('export default App')
                print(f"FAIL: Component 3 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(APP_TSX_PATH):
    print(f"File not found: {APP_TSX_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(APP_TSX_PATH)
