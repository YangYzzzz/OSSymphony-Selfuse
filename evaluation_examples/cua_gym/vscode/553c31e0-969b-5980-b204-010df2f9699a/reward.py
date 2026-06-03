"""
Reward Script: Enable and configure Rust test coverage display using Coverage Gutters + cargo-tarpaulin
Task ID: vscode_lang_047
Domain: vscode
Scoring:
  Component 1: lcov.info exists and is valid LCOV format (0.35 pts)
  Component 2: Coverage Gutters VSCode settings configured (0.35 pts)
  Component 3: Tarpaulin build artifacts exist (0.15 pts)
  Component 4: lcov.info references correct project source files (0.15 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_047'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([\]}])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: lcov.info exists and is valid LCOV format (0.35 points)
    # This FAILS on initial (no lcov.info) and PASSES on golden (lcov.info present)
    try:
        lcov_path = os.path.join(PROJECT_DIR, 'lcov.info')
        if os.path.exists(lcov_path):
            with open(lcov_path, 'r') as f:
                lcov_content = f.read()

            # Check for valid LCOV structure: must have SF, DA, and end_of_record
            has_sf = bool(re.search(r'^SF:', lcov_content, re.MULTILINE))
            has_da = bool(re.search(r'^DA:', lcov_content, re.MULTILINE))
            has_end = bool(re.search(r'^end_of_record', lcov_content, re.MULTILINE))

            if has_sf and has_da and has_end:
                print(f"PASS: Component 1 -- lcov.info exists with valid LCOV format (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 -- lcov.info exists but invalid format (SF={has_sf}, DA={has_da}, end={has_end})")
        else:
            print(f"FAIL: Component 1 -- lcov.info not found at {lcov_path}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Coverage Gutters settings configured (0.35 points)
    # This FAILS on initial (no coverage-gutters settings) and PASSES on golden
    try:
        settings = load_settings()
        if settings is None:
            print(f"FAIL: Component 2 -- Cannot load settings.json")
        else:
            # Check for key Coverage Gutters settings that indicate configuration
            required_keys = [
                'coverage-gutters.showLineCoverage',
                'coverage-gutters.showGutterCoverage',
            ]
            # At least one display mode must be enabled (true)
            found_keys = sum(1 for key in required_keys if key in settings)
            enabled_count = sum(1 for key in required_keys if settings.get(key) is True)

            # Also check for coverageFileNames or coverageBaseDir (configuration completeness)
            has_file_config = (
                'coverage-gutters.coverageFileNames' in settings
                or 'coverage-gutters.coverageBaseDir' in settings
            )

            if found_keys >= 2 and enabled_count > 0 and has_file_config:
                print(f"PASS: Component 2 -- Coverage Gutters fully configured ({found_keys} display keys, file config present) (0.35 pts)")
                total_score += 0.35
            elif found_keys >= 1 and enabled_count > 0:
                print(f"PARTIAL: Component 2 -- Coverage Gutters partially configured ({found_keys}/2 display keys) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 -- Coverage Gutters not configured (found_keys={found_keys}, enabled={enabled_count}, file_config={has_file_config})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Tarpaulin build artifacts exist (0.15 points)
    # This FAILS on initial (no target/tarpaulin/) and PASSES on golden
    try:
        tarpaulin_dir = os.path.join(PROJECT_DIR, 'target', 'tarpaulin')
        if os.path.isdir(tarpaulin_dir):
            tarpaulin_files = os.listdir(tarpaulin_dir)
            if len(tarpaulin_files) > 0:
                print(f"PASS: Component 3 -- Tarpaulin artifacts found: {tarpaulin_files} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- Tarpaulin dir exists but is empty")
        else:
            print(f"FAIL: Component 3 -- Tarpaulin directory not found at {tarpaulin_dir}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: lcov.info references correct project source files (0.15 points)
    # This FAILS on initial (no lcov.info) and PASSES on golden
    try:
        lcov_path = os.path.join(PROJECT_DIR, 'lcov.info')
        if os.path.exists(lcov_path):
            with open(lcov_path, 'r') as f:
                lcov_content = f.read()

            # Extract SF (source file) entries
            sf_lines = re.findall(r'^SF:(.+)$', lcov_content, re.MULTILINE)

            if len(sf_lines) > 0:
                # Check that referenced source files actually exist in the project
                valid_refs = 0
                for sf in sf_lines:
                    sf = sf.strip()
                    if os.path.exists(sf):
                        valid_refs += 1

                if valid_refs == len(sf_lines):
                    print(f"PASS: Component 4 -- All {valid_refs} source files in lcov.info exist (0.15 pts)")
                    total_score += 0.15
                elif valid_refs > 0:
                    partial = 0.15 * (valid_refs / len(sf_lines))
                    print(f"PARTIAL: Component 4 -- {valid_refs}/{len(sf_lines)} source files exist ({partial:.2f} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 -- None of {len(sf_lines)} source file references are valid")
            else:
                print(f"FAIL: Component 4 -- No SF entries found in lcov.info")
        else:
            print(f"FAIL: Component 4 -- lcov.info not found (cannot check source refs)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
