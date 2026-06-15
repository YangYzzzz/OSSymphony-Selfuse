"""
Reward Script: Rust CLI Tool with clap, serde, serde_json, anyhow
Task ID: vscode_gf4_022
Domain: vscode
Scoring:
  Component 1 (0.30): Cargo.toml has all 4 required dependencies
  Component 2 (0.30): src/main.rs uses clap derive Parser with 3 subcommands
  Component 3 (0.20): src/main.rs handles JSON data with serde_json
  Component 4 (0.20): tests/integration_test.rs exists with Command-based tests
"""

import os
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'rust-cli-tool')
CARGO_TOML = os.path.join(PROJECT_DIR, 'Cargo.toml')
MAIN_RS = os.path.join(PROJECT_DIR, 'src', 'main.rs')
INTEGRATION_TEST = os.path.join(PROJECT_DIR, 'tests', 'integration_test.rs')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Component 1: Cargo.toml has all 4 required dependencies (0.30 points) ----
    try:
        if not os.path.exists(CARGO_TOML):
            print("FAIL: Component 1 -- Cargo.toml not found")
        else:
            with open(CARGO_TOML, 'r') as f:
                cargo_content = f.read()
            cargo_lower = cargo_content.lower()

            deps_found = 0
            # Check for clap with derive feature
            if 'clap' in cargo_lower and 'derive' in cargo_lower:
                deps_found += 1
                print("PASS: Component 1a -- clap with derive feature found")
            else:
                print("FAIL: Component 1a -- clap with derive feature not found")

            # Check for serde as a standalone dependency (not just serde_json)
            if re.search(r'^serde\s*=', cargo_content, re.MULTILINE):
                deps_found += 1
                print("PASS: Component 1b -- serde found")
            else:
                print("FAIL: Component 1b -- serde not found as standalone dependency")

            # Check for serde_json
            if 'serde_json' in cargo_lower:
                deps_found += 1
                print("PASS: Component 1c -- serde_json found")
            else:
                print("FAIL: Component 1c -- serde_json not found")

            # Check for anyhow
            if 'anyhow' in cargo_lower:
                deps_found += 1
                print("PASS: Component 1d -- anyhow found")
            else:
                print("FAIL: Component 1d -- anyhow not found")

            if deps_found == 4:
                total_score += 0.30
                print(f"PASS: Component 1 -- All 4 dependencies found (0.30 pts)")
            elif deps_found >= 2:
                partial = round(0.30 * (deps_found / 4.0), 2)
                total_score += partial
                print(f"PARTIAL: Component 1 -- {deps_found}/4 dependencies ({partial} pts)")
            else:
                print(f"FAIL: Component 1 -- Only {deps_found}/4 dependencies found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ---- Component 2: src/main.rs uses clap derive Parser with 3 subcommands (0.30 points) ----
    try:
        if not os.path.exists(MAIN_RS):
            print("FAIL: Component 2 -- src/main.rs not found")
        else:
            with open(MAIN_RS, 'r') as f:
                main_content = f.read()

            comp2_parts = 0

            # Check for derive(Parser)
            if re.search(r'#\[derive\([^)]*Parser[^)]*\)\]', main_content):
                comp2_parts += 1
                print("PASS: Component 2a -- #[derive(Parser)] found")
            else:
                print("FAIL: Component 2a -- #[derive(Parser)] not found")

            # Check for Subcommand derive
            if re.search(r'#\[derive\([^)]*Subcommand[^)]*\)\]', main_content) or \
               re.search(r'#\[command\(subcommand\)\]', main_content):
                comp2_parts += 1
                print("PASS: Component 2b -- Subcommand derive/attribute found")
            else:
                print("FAIL: Component 2b -- Subcommand derive/attribute not found")

            # Check for Add subcommand with name and value fields
            if re.search(r'Add\s*\{[^}]*name\s*:', main_content, re.DOTALL) and \
               re.search(r'Add\s*\{[^}]*value\s*:', main_content, re.DOTALL):
                comp2_parts += 1
                print("PASS: Component 2c -- 'Add' subcommand with name/value fields")
            else:
                print("FAIL: Component 2c -- 'Add' subcommand missing or lacks name/value")

            # Check for List subcommand with format flag
            if re.search(r'List\s*\{[^}]*format\s*:', main_content, re.DOTALL):
                comp2_parts += 1
                print("PASS: Component 2d -- 'List' subcommand with format flag")
            else:
                print("FAIL: Component 2d -- 'List' subcommand missing or lacks format")

            # Check for Delete subcommand with id field
            if re.search(r'Delete\s*\{[^}]*id\s*:', main_content, re.DOTALL):
                comp2_parts += 1
                print("PASS: Component 2e -- 'Delete' subcommand with id field")
            else:
                print("FAIL: Component 2e -- 'Delete' subcommand missing or lacks id")

            # 5 parts: derive(Parser), Subcommand, Add, List, Delete
            if comp2_parts == 5:
                total_score += 0.30
                print(f"PASS: Component 2 -- Full CLI structure (0.30 pts)")
            elif comp2_parts >= 1:
                partial = round(0.30 * (comp2_parts / 5.0), 2)
                total_score += partial
                print(f"PARTIAL: Component 2 -- {comp2_parts}/5 parts ({partial} pts)")
            else:
                print("FAIL: Component 2 -- No CLI structure found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ---- Component 3: src/main.rs handles JSON data with serde_json (0.20 points) ----
    try:
        if not os.path.exists(MAIN_RS):
            print("FAIL: Component 3 -- src/main.rs not found")
        else:
            with open(MAIN_RS, 'r') as f:
                main_content = f.read()

            comp3_parts = 0

            # Check for Serialize/Deserialize derives on data structs
            if re.search(r'#\[derive\([^)]*Serialize[^)]*\)\]', main_content) and \
               re.search(r'#\[derive\([^)]*Deserialize[^)]*\)\]', main_content):
                comp3_parts += 1
                print("PASS: Component 3a -- Serialize/Deserialize derives found")
            else:
                print("FAIL: Component 3a -- Serialize/Deserialize derives not found")

            # Check for serde_json usage (from_str, to_string, etc.)
            if re.search(r'serde_json::(from_str|to_string|from_reader|to_writer)', main_content):
                comp3_parts += 1
                print("PASS: Component 3b -- serde_json serialization functions used")
            else:
                print("FAIL: Component 3b -- serde_json serialization functions not found")

            # Check for JSON data file path (should reference a .json file)
            if re.search(r'data\.json|\.config.*\.json', main_content):
                comp3_parts += 1
                print("PASS: Component 3c -- JSON data file path referenced")
            else:
                print("FAIL: Component 3c -- No JSON data file path found")

            # Check for file read/write operations (fs::read_to_string, fs::write, etc.)
            if re.search(r'(fs::read_to_string|fs::write|fs::read|File::open|File::create)', main_content):
                comp3_parts += 1
                print("PASS: Component 3d -- File I/O operations found")
            else:
                print("FAIL: Component 3d -- No file I/O operations found")

            if comp3_parts == 4:
                total_score += 0.20
                print(f"PASS: Component 3 -- Full JSON handling (0.20 pts)")
            elif comp3_parts >= 1:
                partial = round(0.20 * (comp3_parts / 4.0), 2)
                total_score += partial
                print(f"PARTIAL: Component 3 -- {comp3_parts}/4 parts ({partial} pts)")
            else:
                print("FAIL: Component 3 -- No JSON handling found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ---- Component 4: tests/integration_test.rs with Command-based tests (0.20 points) ----
    try:
        if not os.path.exists(INTEGRATION_TEST):
            print("FAIL: Component 4 -- tests/integration_test.rs not found")
        else:
            with open(INTEGRATION_TEST, 'r') as f:
                test_content = f.read()

            comp4_parts = 0

            # Check for use of std::process::Command
            if 'std::process::Command' in test_content or 'Command::new' in test_content:
                comp4_parts += 1
                print("PASS: Component 4a -- std::process::Command usage found")
            else:
                print("FAIL: Component 4a -- std::process::Command not used")

            # Check for #[test] annotations (at least 2 tests)
            test_count = len(re.findall(r'#\[test\]', test_content))
            if test_count >= 2:
                comp4_parts += 1
                print(f"PASS: Component 4b -- {test_count} #[test] functions found (>=2)")
            else:
                print(f"FAIL: Component 4b -- Only {test_count} #[test] functions (need >=2)")

            # Check that tests exercise CLI subcommands (at least 2 of add/list/delete)
            subcmds_tested = 0
            test_lower = test_content.lower()
            if re.search(r'"add"', test_content):
                subcmds_tested += 1
            if re.search(r'"list"', test_content):
                subcmds_tested += 1
            if re.search(r'"delete"', test_content):
                subcmds_tested += 1
            if subcmds_tested >= 2:
                comp4_parts += 1
                print(f"PASS: Component 4c -- Tests exercise {subcmds_tested}/3 subcommands")
            else:
                print(f"FAIL: Component 4c -- Tests only exercise {subcmds_tested}/3 subcommands")

            # Check for assertions
            assert_count = len(re.findall(r'assert!|assert_eq!|assert_ne!', test_content))
            if assert_count >= 2:
                comp4_parts += 1
                print(f"PASS: Component 4d -- {assert_count} assertions found (>=2)")
            else:
                print(f"FAIL: Component 4d -- Only {assert_count} assertions found")

            if comp4_parts == 4:
                total_score += 0.20
                print(f"PASS: Component 4 -- Full integration tests (0.20 pts)")
            elif comp4_parts >= 1:
                partial = round(0.20 * (comp4_parts / 4.0), 2)
                total_score += partial
                print(f"PARTIAL: Component 4 -- {comp4_parts}/4 parts ({partial} pts)")
            else:
                print("FAIL: Component 4 -- Integration tests inadequate")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
