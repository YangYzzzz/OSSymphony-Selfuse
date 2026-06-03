"""
Reward Script: Configure Java test coverage with Coverage Gutters extension and JaCoCo
Task ID: vscode_lang_065
Domain: vscode
Scoring:
  Component 1: Coverage extension installed (0.25)
  Component 2: JaCoCo coverage data generated - jacoco.exec (0.20)
  Component 3: JaCoCo HTML/XML report in target/site/jacoco/ (0.25)
  Component 4: VSCode workspace configured for coverage display (0.30)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_065'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
EXTENSIONS_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Coverage Gutters extension is installed (0.25 points)
    # Check the extensions directory for ryanluker.vscode-coverage-gutters
    # This extension is NOT installed in initial_env, only in golden_env
    try:
        if os.path.isdir(EXTENSIONS_DIR):
            ext_dirs = os.listdir(EXTENSIONS_DIR)
            coverage_ext_found = any(
                'vscode-coverage-gutters' in d.lower()
                for d in ext_dirs
                if os.path.isdir(os.path.join(EXTENSIONS_DIR, d))
            )
            if coverage_ext_found:
                print("PASS: Component 1 — Coverage Gutters extension is installed (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — Coverage Gutters extension not found in {EXTENSIONS_DIR}. Dirs: {ext_dirs}")
        else:
            print(f"FAIL: Component 1 — Extensions directory not found: {EXTENSIONS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: JaCoCo coverage data generated (0.20 points)
    # jacoco.exec is the binary coverage data file created by running mvn test with JaCoCo
    # This does NOT exist in initial_env (no target/ directory at all)
    try:
        jacoco_exec_path = os.path.join(PROJECT_DIR, 'target', 'jacoco.exec')
        if os.path.isfile(jacoco_exec_path):
            file_size = os.path.getsize(jacoco_exec_path)
            if file_size > 0:
                print(f"PASS: Component 2 — jacoco.exec exists ({file_size} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print("FAIL: Component 2 — jacoco.exec exists but is empty")
        else:
            print(f"FAIL: Component 2 — jacoco.exec not found at {jacoco_exec_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: JaCoCo report exists with real coverage data (0.25 points)
    # target/site/jacoco/ should contain jacoco.xml with coverage counters
    # This does NOT exist in initial_env
    try:
        jacoco_xml_path = os.path.join(PROJECT_DIR, 'target', 'site', 'jacoco', 'jacoco.xml')
        if os.path.isfile(jacoco_xml_path):
            with open(jacoco_xml_path, 'r') as f:
                xml_content = f.read()
            # Verify it contains actual coverage data (counter elements with covered > 0)
            has_covered_lines = 'covered="' in xml_content and 'INSTRUCTION' in xml_content
            if has_covered_lines and len(xml_content) > 500:
                print(f"PASS: Component 3 — JaCoCo XML report exists with coverage data ({len(xml_content)} chars) (0.25 pts)")
                total_score += 0.25
            else:
                print("FAIL: Component 3 — jacoco.xml exists but lacks real coverage data")
        else:
            print(f"FAIL: Component 3 — jacoco.xml not found at {jacoco_xml_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: VSCode workspace settings configured for coverage display (0.30 points)
    # The .vscode/settings.json should have coverage-gutters settings enabling line coverage
    # Initial env only has java.configuration.updateBuildConfiguration, NOT coverage settings
    try:
        vscode_settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        if os.path.isfile(vscode_settings_path):
            with open(vscode_settings_path, 'r') as f:
                settings = json.load(f)

            # Check for coverage-gutters configuration keys
            has_line_coverage = settings.get('coverage-gutters.showLineCoverage') is True
            has_gutter_coverage = settings.get('coverage-gutters.showGutterCoverage') is True
            has_coverage_files = isinstance(settings.get('coverage-gutters.coverageFileNames'), list)

            coverage_checks_passed = 0
            if has_line_coverage:
                coverage_checks_passed += 1
            if has_gutter_coverage:
                coverage_checks_passed += 1
            if has_coverage_files:
                # Verify jacoco.xml is in the file names list
                file_names = settings.get('coverage-gutters.coverageFileNames', [])
                if any('jacoco' in fn.lower() for fn in file_names):
                    coverage_checks_passed += 1

            if coverage_checks_passed >= 3:
                print(f"PASS: Component 4 — Coverage Gutters fully configured (showLine={has_line_coverage}, showGutter={has_gutter_coverage}, fileNames includes jacoco) (0.30 pts)")
                total_score += 0.30
            elif coverage_checks_passed >= 1:
                partial = round(0.30 * coverage_checks_passed / 3, 2)
                print(f"PARTIAL: Component 4 — {coverage_checks_passed}/3 coverage settings found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No coverage-gutters settings found in {vscode_settings_path}")
        else:
            print(f"FAIL: Component 4 — .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
