"""
Reward Script: Add [tool.pytest.ini_options] section to pyproject.toml in VSCode
Task ID: osworld_multi_apps_vscode_config_edit_009
Domain: vs-code / os (TOML file editing)
Scoring:
  - Component 1: [tool.pytest.ini_options] section exists in pyproject.toml   (0.30 pts)
  - Component 2: testpaths = ["tests"] is set correctly                        (0.25 pts)
  - Component 3: addopts = "-v --tb=short" is set correctly                    (0.25 pts)
  - Component 4: minversion = "7.0" is set correctly                           (0.20 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_config_edit_009'
TOML_PATH = os.path.join(WORKDIR, 'Code', 'tests', 'pyproject.toml')


def parse_toml_sections(content):
    """
    Simple TOML section parser.
    Returns a dict mapping section header (e.g. 'tool.pytest.ini_options')
    to the raw text lines of that section.
    """
    sections = {}
    current_section = None
    current_lines = []

    for line in content.splitlines():
        stripped = line.strip()
        # Match section header like [tool.pytest.ini_options]
        section_match = re.match(r'^\[([^\]]+)\]$', stripped)
        if section_match:
            if current_section is not None:
                sections[current_section] = current_lines
            current_section = section_match.group(1)
            current_lines = []
        else:
            if current_section is not None:
                current_lines.append(line)

    if current_section is not None:
        sections[current_section] = current_lines

    return sections


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Read the pyproject.toml file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"INFO: Successfully read file: {file_path} ({len(content)} bytes)")
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse TOML sections
    try:
        sections = parse_toml_sections(content)
        print(f"INFO: Found sections: {list(sections.keys())}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse TOML structure: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: [tool.pytest.ini_options] section exists (0.30 points)
    # This is the main deliverable — the section must be present in the file
    try:
        pytest_section_key = 'tool.pytest.ini_options'
        if pytest_section_key in sections:
            print(f"PASS: Component 1 — [tool.pytest.ini_options] section found (0.30 pts)")
            total_score += 0.30
            pytest_lines = sections[pytest_section_key]
        else:
            print(f"FAIL: Component 1 — [tool.pytest.ini_options] section NOT found in pyproject.toml")
            print(f"      Available sections: {list(sections.keys())}")
            # Without the section, no sub-components can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    pytest_section_text = '\n'.join(pytest_lines)
    print(f"DEBUG: [tool.pytest.ini_options] section content:\n{pytest_section_text}")

    # Component 2: testpaths = ["tests"] is correctly set (0.25 points)
    try:
        # Match: testpaths = ["tests"] with possible whitespace variations
        testpaths_match = re.search(
            r'testpaths\s*=\s*\["tests"\]',
            pytest_section_text
        )
        if testpaths_match:
            print(f"PASS: Component 2 — testpaths = [\"tests\"] found (0.25 pts)")
            total_score += 0.25
        else:
            # Check if testpaths key exists but with wrong value
            testpaths_key = re.search(r'testpaths\s*=\s*(.+)', pytest_section_text)
            if testpaths_key:
                print(f"FAIL: Component 2 — testpaths key found but value is wrong: {testpaths_key.group(1).strip()}")
                print(f"      Expected: testpaths = [\"tests\"]")
            else:
                print(f"FAIL: Component 2 — testpaths key not found in [tool.pytest.ini_options] section")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: addopts = "-v --tb=short" is correctly set (0.25 points)
    try:
        # Match: addopts = "-v --tb=short" with possible whitespace variations
        addopts_match = re.search(
            r'addopts\s*=\s*"-v --tb=short"',
            pytest_section_text
        )
        if addopts_match:
            print(f"PASS: Component 3 — addopts = \"-v --tb=short\" found (0.25 pts)")
            total_score += 0.25
        else:
            # Check if addopts key exists but with wrong value
            addopts_key = re.search(r'addopts\s*=\s*(.+)', pytest_section_text)
            if addopts_key:
                print(f"FAIL: Component 3 — addopts key found but value is wrong: {addopts_key.group(1).strip()}")
                print(f"      Expected: addopts = \"-v --tb=short\"")
            else:
                print(f"FAIL: Component 3 — addopts key not found in [tool.pytest.ini_options] section")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: minversion = "7.0" is correctly set (0.20 points)
    try:
        # Match: minversion = "7.0" with possible whitespace variations
        minversion_match = re.search(
            r'minversion\s*=\s*"7\.0"',
            pytest_section_text
        )
        if minversion_match:
            print(f"PASS: Component 4 — minversion = \"7.0\" found (0.20 pts)")
            total_score += 0.20
        else:
            # Check if minversion key exists but with wrong value
            minversion_key = re.search(r'minversion\s*=\s*(.+)', pytest_section_text)
            if minversion_key:
                print(f"FAIL: Component 4 — minversion key found but value is wrong: {minversion_key.group(1).strip()}")
                print(f"      Expected: minversion = \"7.0\"")
            else:
                print(f"FAIL: Component 4 — minversion key not found in [tool.pytest.ini_options] section")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical task file path on VM
if not os.path.exists(TOML_PATH):
    print(f"File not found: {TOML_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TOML_PATH)
