"""
Reward Script: Enable AutoCorrect numbered list option
Task ID: writer_frd_049
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): ApplyNumbering Enable value is 'true' in registrymodifications.xcu
  Component 2 (0.4): The setting is applied at the correct OOo path and the value is not 'false'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_049'
REGISTRY_PATH = os.path.join(
    WORKDIR, '.config', 'libreoffice', '4', 'user', 'registrymodifications.xcu'
)

# The XCU path that controls "Apply numbering - symbol" in AutoCorrect Options
TARGET_PATH = "/org.openoffice.Office.Writer/AutoFunction/Format/ByInput/ApplyNumbering"


def verify_task():
    """
    Verify that the AutoCorrect 'Apply Numbering' option is enabled.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: registry file must exist
    if not os.path.exists(REGISTRY_PATH):
        print(f"CRITICAL: Registry file not found: {REGISTRY_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read registry file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ApplyNumbering setting exists and is set to true (0.6 points)
    # We look for the specific item with the correct oor:path and check value is 'true'
    try:
        # Pattern: match the item element for ApplyNumbering with Enable prop
        pattern = (
            r'<item\s+oor:path="'
            + re.escape(TARGET_PATH)
            + r'">'
            r'\s*<prop\s+oor:name="Enable"[^>]*>'
            r'\s*<value>(.*?)</value>'
        )
        match = re.search(pattern, content, re.DOTALL)

        if match:
            value = match.group(1).strip().lower()
            if value == 'true':
                print(f"PASS: Component 1 — ApplyNumbering Enable = 'true' (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — ApplyNumbering Enable = '{value}', expected 'true'")
        else:
            # The setting might not be present at all (not yet written to registry)
            print(f"FAIL: Component 1 — ApplyNumbering setting not found in registry")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Verify via a secondary approach — parse all AutoFunction entries
    # and confirm that no conflicting 'false' entry exists for ApplyNumbering (0.4 points)
    # This component also confirms the setting path is correct by checking it independently.
    try:
        # Find ALL lines referencing ApplyNumbering in the AutoFunction path
        lines_with_setting = [
            line.strip() for line in content.split('\n')
            if 'ApplyNumbering' in line and 'AutoFunction' in line
        ]

        if not lines_with_setting:
            print(f"FAIL: Component 2 — No ApplyNumbering AutoFunction entry found in registry")
        else:
            # Check the last occurrence (in case of duplicates, last wins in XCU)
            last_line = lines_with_setting[-1]
            # Extract the value from this line
            val_match = re.search(r'<value>(true|false)</value>', last_line, re.IGNORECASE)
            if val_match:
                final_value = val_match.group(1).strip().lower()
                if final_value == 'true':
                    print(f"PASS: Component 2 — Final ApplyNumbering value is 'true' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 — Final ApplyNumbering value is '{final_value}', expected 'true'")
            else:
                print(f"FAIL: Component 2 — Could not parse value from: {last_line[:120]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
