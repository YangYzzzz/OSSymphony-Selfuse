"""
Reward Script: Verify that 5 missing React component imports were added to Dashboard.tsx
Task ID: vscode_web_088
Domain: vscode
Scoring:
  - Component 1 (0.1 pts each x5 = 0.5): Each of the 5 import statements is present
  - Component 2 (0.1 pts each x5 = 0.5): Each import references the correct relative path
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_088'

# The 5 components that must be imported
REQUIRED_COMPONENTS = ['Header', 'Sidebar', 'Card', 'Chart', 'Footer']

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file should still contain the Dashboard component (not corrupted)
    if 'const Dashboard' not in content:
        print("CRITICAL: Dashboard component not found — file may be corrupted")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Each required import statement is present (0.1 pts each, total 0.5)
    # We check that each component has an import line (import X from '...')
    for comp in REQUIRED_COMPONENTS:
        try:
            # Match patterns like:
            #   import Header from '../components/Header';
            #   import { Header } from '../components/Header';
            #   import Header from "./components/Header";
            pattern = rf'''import\s+(?:\{{\s*)?{comp}(?:\s*\}})?\s+from\s+['"]'''
            if re.search(pattern, content):
                print(f"PASS: Component 1/{comp} — import statement found (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1/{comp} — no import statement found for {comp}")
        except Exception as e:
            print(f"ERROR: Component 1/{comp} — {e}")

    # Component 2: Each import references the correct path (../components/ or ./components/)
    # (0.1 pts each, total 0.5)
    for comp in REQUIRED_COMPONENTS:
        try:
            # The import path should reference the components directory
            # Accept both ../components/X and ./components/X (relative path variants)
            pattern = rf'''import\s+(?:\{{\s*)?{comp}(?:\s*\}})?\s+from\s+['"]\.{{1,2}}/components/{comp}['"]'''
            if re.search(pattern, content):
                print(f"PASS: Component 2/{comp} — correct import path for {comp} (0.1 pts)")
                total_score += 0.1
            else:
                # Check if there's any import for the component (might have wrong path)
                basic_pattern = rf'''import\s+(?:\{{\s*)?{comp}(?:\s*\}})?\s+from\s+'''
                if re.search(basic_pattern, content):
                    print(f"FAIL: Component 2/{comp} — {comp} imported but from wrong path")
                else:
                    print(f"FAIL: Component 2/{comp} — no import found for {comp}")
        except Exception as e:
            print(f"ERROR: Component 2/{comp} — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/projects/react-ts-app/src/pages/Dashboard.tsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
