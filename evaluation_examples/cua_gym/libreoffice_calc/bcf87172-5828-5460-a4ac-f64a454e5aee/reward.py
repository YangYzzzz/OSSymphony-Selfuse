"""
Reward Script: Set up VSCode for Julia development
Task ID: osworld_multi_apps_vscode_ext_script_007
Domain: vscode + os (multi-app)
Scoring:
  Component 1 (0.4): Julia extension (julialang.language-julia) is installed
  Component 2 (0.3): ~/Desktop/stats.jl exists
  Component 3 (0.3): stats.jl contains required Julia code (rand(100), mean/std functions, println)
Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_007'

# Paths
EXTENSIONS_JSON = os.path.join(WORKDIR, '.vscode', 'extensions', 'extensions.json')
STATS_JL_PATH = os.path.join(WORKDIR, 'Desktop', 'stats.jl')
JULIA_EXTENSION_ID = 'julialang.language-julia'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Julia extension is installed (0.4 points)
    # Check via extensions.json which is populated when extensions are installed
    # Initial env has empty extensions.json ([]), golden env has julialang.language-julia
    try:
        julia_ext_found = False

        # Primary check: extensions.json file records installed extensions
        if os.path.exists(EXTENSIONS_JSON):
            try:
                with open(EXTENSIONS_JSON, 'r') as f:
                    content = f.read().strip()
                # extensions.json can have comments, try parsing
                extensions = json.loads(content)
                for ext in extensions:
                    ext_id = ext.get('identifier', {}).get('id', '').lower()
                    if ext_id == JULIA_EXTENSION_ID.lower():
                        julia_ext_found = True
                        break
            except (json.JSONDecodeError, ValueError):
                pass

        # Secondary check: extension directory exists in .vscode/extensions/
        if not julia_ext_found:
            ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
            if os.path.isdir(ext_dir):
                for entry in os.listdir(ext_dir):
                    if entry.lower().startswith('julialang.language-julia'):
                        julia_ext_found = True
                        break

        if julia_ext_found:
            print(f"PASS: Component 1 — Julia extension '{JULIA_EXTENSION_ID}' is installed (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Julia extension '{JULIA_EXTENSION_ID}' not found in extensions.json or extensions directory")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: stats.jl file exists at ~/Desktop/stats.jl (0.3 points)
    # Initial env has no stats.jl; golden env has the file
    try:
        if os.path.isfile(STATS_JL_PATH):
            file_size = os.path.getsize(STATS_JL_PATH)
            if file_size > 0:
                print(f"PASS: Component 2 — stats.jl exists at {STATS_JL_PATH} (size: {file_size} bytes) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — stats.jl exists but is empty at {STATS_JL_PATH}")
        else:
            print(f"FAIL: Component 2 — stats.jl not found at {STATS_JL_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: stats.jl contains required Julia code (0.3 points)
    # Verifies: rand(100) call, mean/std computation, println for output
    # All four sub-checks must pass for full component credit
    try:
        if not os.path.isfile(STATS_JL_PATH):
            print(f"FAIL: Component 3 — stats.jl not found, cannot verify content")
        else:
            with open(STATS_JL_PATH, 'r') as f:
                content = f.read()

            checks = {}

            # Sub-check 3a: generates 100 random numbers using rand(100) or similar
            # Must use rand with 100 as argument to generate 100 numbers
            checks['rand_100'] = bool(re.search(r'\brand\s*\(\s*100\s*\)', content))

            # Sub-check 3b: computes mean using built-in mean() function
            checks['mean_fn'] = bool(re.search(r'\bmean\s*\(', content))

            # Sub-check 3c: computes standard deviation using built-in std() function
            checks['std_fn'] = bool(re.search(r'\bstd\s*\(', content))

            # Sub-check 3d: prints results using println
            checks['println'] = bool(re.search(r'\bprintln\s*\(', content))

            passed = sum(1 for v in checks.values() if v)
            total_checks = len(checks)

            for check_name, result in checks.items():
                status = "PASS" if result else "FAIL"
                print(f"  {status}: stats.jl sub-check '{check_name}' — {'found' if result else 'not found'}")

            if passed == total_checks:
                print(f"PASS: Component 3 — stats.jl contains all required Julia code "
                      f"(rand(100), mean, std, println) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — stats.jl missing required Julia code "
                      f"({passed}/{total_checks} sub-checks passed)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
