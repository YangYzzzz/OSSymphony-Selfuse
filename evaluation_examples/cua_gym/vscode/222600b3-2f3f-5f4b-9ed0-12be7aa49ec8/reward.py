"""
Reward Script: Format Selection on settings object in config.js
Task ID: vscode_code_006
Domain: vs_code
Scoring:
  - Component 1: settings object is reformatted to multi-line with sub-keys on own lines (0.40 pts)
  - Component 2: settings sub-key indentation structure is correct (nested at 4+ spaces) (0.30 pts)
  - Component 3: non-settings lines unchanged AND all data values preserved in reformatted file (0.30 pts)
    - NOTE: Component 3 only awards points in combination with Component 1 having passed.

All components fail on initial_env (settings is a single compact line).
All components pass on golden_env (settings is properly reformatted).
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_006'

FILE_PATH = '/home/user/project/config.js'

# Expected unchanged lines (from task context — must be EXACTLY these)
EXPECTED_NAME_LINE = "  name: 'MyApp',"
EXPECTED_VERSION_LINE = "  version: '1.0.0',"
EXPECTED_DESCRIPTION_LINE = "  description: 'A sample application'"

# Sub-keys that must appear on their own lines in the reformatted settings
EXPECTED_SETTINGS_KEYS = [
    'debug', 'logging', 'level', 'format', 'output',
    'file', 'console', 'rotation', 'maxSize', 'maxFiles',
    'cache', 'enabled', 'ttl',
]


def verify_task(file_path):
    """
    Verify that the settings object in config.js was properly reformatted
    with Format Selection, while leaving other lines untouched.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
        print(f"INFO: File loaded, {len(lines)} lines total")
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Detect if settings is in single-line compact form (initial state) or multi-line (golden state)
    # In initial env: settings: {debug:true,logging:{...},cache:{...}} — all on ONE line
    # In golden env: settings starts on one line but the brace content spans many lines
    def _detect_compact_settings(file_lines):
        """Returns True if the settings key has an inline compact single-line value."""
        for line in file_lines:
            if re.match(r'\s*settings\s*:', line):
                stripped = line.strip()
                # Compact form: has debug, logging, and cache all inline on this single line
                return (
                    'debug' in stripped
                    and 'logging' in stripped
                    and 'cache' in stripped
                    and len(stripped) > 80
                )
        return False

    settings_is_compact = _detect_compact_settings(lines)

    # Component 1: settings object reformatted to multi-line (0.40 points)
    # FAILS on initial (compact single-line) — PASSES on golden (multi-line)
    try:
        if settings_is_compact:
            print("FAIL: Component 1 — settings is still a compact single-line object (initial state)")
        else:
            # Count how many expected sub-keys appear on their own dedicated lines
            keys_on_own_line = 0
            for key in EXPECTED_SETTINGS_KEYS:
                pattern = re.compile(r'^\s{4,}' + re.escape(key) + r'\s*:', re.MULTILINE)
                if pattern.search(content):
                    keys_on_own_line += 1

            if keys_on_own_line >= len(EXPECTED_SETTINGS_KEYS) - 1:
                print(f"PASS: Component 1 — settings reformatted; {keys_on_own_line}/{len(EXPECTED_SETTINGS_KEYS)} sub-keys on own indented lines (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 — settings appears multi-line but only {keys_on_own_line}/{len(EXPECTED_SETTINGS_KEYS)} sub-keys found on own lines")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: indentation structure is correct (0.30 points)
    # Nested objects (logging, output, rotation, cache) must have their contents
    # indented deeper than the settings-level keys.
    # FAILS on initial (all keys are inline, no multi-line indentation) — PASSES on golden
    try:
        if settings_is_compact:
            print("FAIL: Component 2 — settings is compact, indentation structure cannot be verified (initial state)")
        else:
            # Top-level settings keys (direct children) should be at 4-space indent
            # Deeper nested keys should be at 6+ spaces
            # Check: rotation sub-keys (maxSize, maxFiles) must be at >= 6 spaces indent
            rotation_deep_indent = re.search(r'^ {6,}maxSize\s*:', content, re.MULTILINE)
            cache_deep_indent = re.search(r'^ {6,}enabled\s*:', content, re.MULTILINE)
            output_deep_indent = re.search(r'^ {6,}file\s*:', content, re.MULTILINE)
            logging_deep_indent = re.search(r'^ {6,}level\s*:', content, re.MULTILINE)

            indent_checks_passed = sum([
                bool(rotation_deep_indent),
                bool(cache_deep_indent),
                bool(output_deep_indent),
                bool(logging_deep_indent),
            ])

            if indent_checks_passed >= 3:
                print(f"PASS: Component 2 — indentation structure correct, {indent_checks_passed}/4 nested key depth checks passed (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — only {indent_checks_passed}/4 nested indent checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Non-settings lines unchanged AND all data values preserved (0.30 points)
    # This checks that the Format Selection was scoped correctly (only settings reformatted)
    # AND that no data was corrupted during reformatting.
    # FAILS on initial because settings_is_compact means the settings object hasn't been
    # reformatted — so we require settings NOT to be compact as a gate condition.
    try:
        if settings_is_compact:
            print("FAIL: Component 3 — settings is compact (initial state), format selection not applied")
        else:
            # Check non-settings lines are unchanged
            name_ok = any(line == EXPECTED_NAME_LINE for line in lines)
            version_ok = any(line == EXPECTED_VERSION_LINE for line in lines)
            desc_ok = any(line == EXPECTED_DESCRIPTION_LINE for line in lines)

            # Check all data values are preserved
            values_ok = all([
                bool(re.search(r'debug\s*:\s*true', content)),
                bool(re.search(r"level\s*:\s*'info'", content)),
                bool(re.search(r"format\s*:\s*'json'", content)),
                bool(re.search(r"file\s*:\s*'/var/log/app\.log'", content)),
                bool(re.search(r'console\s*:\s*true', content)),
                bool(re.search(r"maxSize\s*:\s*'10mb'", content)),
                bool(re.search(r'maxFiles\s*:\s*5', content)),
                bool(re.search(r'enabled\s*:\s*true', content)),
                bool(re.search(r'ttl\s*:\s*3600', content)),
            ])

            lines_ok = name_ok and version_ok and desc_ok

            if lines_ok and values_ok:
                print(f"PASS: Component 3 — unchanged lines intact + all 9 data values preserved (0.30 pts)")
                total_score += 0.30
            elif not lines_ok:
                missing_lines = []
                if not name_ok:
                    missing_lines.append('name')
                if not version_ok:
                    missing_lines.append('version')
                if not desc_ok:
                    missing_lines.append('description')
                print(f"FAIL: Component 3 — unchanged lines check failed: {missing_lines}")
            else:
                print(f"FAIL: Component 3 — some settings data values missing from reformatted file")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entry point: test against canonical artifact path on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
