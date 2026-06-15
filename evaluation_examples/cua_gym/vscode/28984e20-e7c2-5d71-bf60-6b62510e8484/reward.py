"""
Reward Script: Rust data processor project setup in VSCode
Task ID: vscode_gf4_030
Domain: vscode
Scoring:
  Component 1: Cargo.toml has required dependencies (0.25 pts)
  Component 2: processor.rs exists with DataRecord struct + derive macros (0.20 pts)
  Component 3: processor.rs has all 4 required functions (0.20 pts)
  Component 4: main.rs uses the processor module (0.15 pts)
  Component 5: At least 4 test functions in #[cfg(test)] module (0.20 pts)
"""

import os
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'rust-data-processor')
CARGO_PATH = os.path.join(PROJECT_DIR, 'Cargo.toml')
PROCESSOR_PATH = os.path.join(PROJECT_DIR, 'src', 'processor.rs')
MAIN_PATH = os.path.join(PROJECT_DIR, 'src', 'main.rs')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Cargo.toml has required dependencies (0.25 pts)
    try:
        with open(CARGO_PATH, 'r') as f:
            cargo_content = f.read().lower()

        required_deps = ['csv', 'serde', 'anyhow', 'rayon']
        found_deps = []
        missing_deps = []
        for dep in required_deps:
            # Check for dep as a key in [dependencies] section
            # Patterns: dep = "..." or dep = { ... }
            if re.search(r'(?:^|\n)\s*' + re.escape(dep) + r'\s*=', cargo_content):
                found_deps.append(dep)
            else:
                missing_deps.append(dep)

        # Also check serde has derive feature
        serde_has_derive = bool(re.search(r'serde\s*=\s*\{[^}]*features\s*=\s*\[.*derive.*\]', cargo_content))

        if len(found_deps) == len(required_deps) and serde_has_derive:
            print(f"PASS: Component 1 - All required dependencies found with serde derive feature (0.25 pts)")
            total_score += 0.25
        elif len(found_deps) == len(required_deps):
            # All deps found but serde derive feature missing - partial credit
            print(f"PARTIAL: Component 1 - All deps found but serde derive feature missing (0.15 pts)")
            total_score += 0.15
        elif len(found_deps) > 0:
            partial = 0.25 * (len(found_deps) / len(required_deps))
            print(f"PARTIAL: Component 1 - Found {found_deps}, missing {missing_deps} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No required dependencies found in Cargo.toml")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: processor.rs exists with DataRecord struct + derive macros (0.20 pts)
    try:
        if not os.path.exists(PROCESSOR_PATH):
            print(f"FAIL: Component 2 - processor.rs not found at {PROCESSOR_PATH}")
        else:
            with open(PROCESSOR_PATH, 'r') as f:
                proc_content = f.read()

            has_struct = bool(re.search(r'struct\s+DataRecord\b', proc_content))
            has_fields = all(
                re.search(pattern, proc_content)
                for pattern in [
                    r'id\s*:\s*u32',
                    r'name\s*:\s*String',
                    r'value\s*:\s*f64',
                    r'category\s*:\s*String',
                ]
            )
            has_deserialize = bool(re.search(r'Deserialize', proc_content))
            has_serialize = bool(re.search(r'Serialize', proc_content))

            if has_struct and has_fields and has_deserialize and has_serialize:
                print(f"PASS: Component 2 - DataRecord struct with correct fields and derive macros (0.20 pts)")
                total_score += 0.20
            elif has_struct and has_fields:
                print(f"PARTIAL: Component 2 - DataRecord struct found but missing derive macros (0.10 pts)")
                total_score += 0.10
            elif has_struct:
                print(f"PARTIAL: Component 2 - DataRecord struct found but fields incorrect (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 2 - DataRecord struct not found in processor.rs")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: processor.rs has all 4 required functions (0.20 pts)
    try:
        if not os.path.exists(PROCESSOR_PATH):
            print(f"FAIL: Component 3 - processor.rs not found")
        else:
            with open(PROCESSOR_PATH, 'r') as f:
                proc_content = f.read()

            required_fns = ['load_csv', 'filter_by_category', 'compute_stats', 'export_json']
            found_fns = []
            missing_fns = []
            for fn_name in required_fns:
                if re.search(r'fn\s+' + re.escape(fn_name) + r'\s*\(', proc_content):
                    found_fns.append(fn_name)
                else:
                    missing_fns.append(fn_name)

            if len(found_fns) == len(required_fns):
                print(f"PASS: Component 3 - All 4 required functions found: {found_fns} (0.20 pts)")
                total_score += 0.20
            elif len(found_fns) > 0:
                partial = 0.20 * (len(found_fns) / len(required_fns))
                print(f"PARTIAL: Component 3 - Found {found_fns}, missing {missing_fns} ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 - No required functions found in processor.rs")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: main.rs uses the processor module (0.15 pts)
    try:
        with open(MAIN_PATH, 'r') as f:
            main_content = f.read()

        has_mod_processor = bool(re.search(r'mod\s+processor', main_content))
        has_use_processor = bool(re.search(r'use\s+processor\s*::', main_content))
        # Also check that main.rs has more than just fn main() {}
        has_substantial_main = len(main_content.strip()) > 30

        if has_mod_processor and has_use_processor and has_substantial_main:
            print(f"PASS: Component 4 - main.rs declares and uses processor module (0.15 pts)")
            total_score += 0.15
        elif has_mod_processor and has_substantial_main:
            print(f"PARTIAL: Component 4 - main.rs declares mod processor but no use statement (0.10 pts)")
            total_score += 0.10
        elif has_mod_processor or has_use_processor:
            print(f"PARTIAL: Component 4 - main.rs partially uses processor module (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 - main.rs does not use processor module")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: At least 4 test functions in #[cfg(test)] module (0.20 pts)
    try:
        if not os.path.exists(PROCESSOR_PATH):
            print(f"FAIL: Component 5 - processor.rs not found")
        else:
            with open(PROCESSOR_PATH, 'r') as f:
                proc_content = f.read()

            has_cfg_test = bool(re.search(r'#\[cfg\(test\)\]', proc_content))
            # Count #[test] annotations
            test_fns = re.findall(r'#\[test\]\s*\n\s*fn\s+\w+', proc_content)
            num_tests = len(test_fns)

            if has_cfg_test and num_tests >= 4:
                print(f"PASS: Component 5 - #[cfg(test)] module with {num_tests} test functions (0.20 pts)")
                total_score += 0.20
            elif has_cfg_test and num_tests >= 2:
                partial = 0.20 * (num_tests / 4.0)
                print(f"PARTIAL: Component 5 - #[cfg(test)] module with only {num_tests} tests ({partial:.2f} pts)")
                total_score += partial
            elif has_cfg_test:
                print(f"PARTIAL: Component 5 - #[cfg(test)] module found but only {num_tests} test(s) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 - No #[cfg(test)] module found in processor.rs")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
