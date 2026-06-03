"""
Reward Script: Use column/box selection in VSCode to copy email column and paste into emails.txt
Task ID: vscode_edit_075
Domain: vs_code
Scoring:
  - Component 1: emails.txt exists at ~/Desktop/emails.txt with non-empty content (0.3 pts)
  - Component 2: emails.txt contains exactly 20 non-empty lines (0.3 pts)
  - Component 3: emails.txt contains exactly the correct 20 email addresses (0.4 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_075'

# Expected email addresses from csv_data.csv (column 3 of all 20 data rows)
EXPECTED_EMAILS = [
    "alice.morgan@techcorp.com",
    "brian.sullivan@devmail.net",
    "clara.nguyen@startup.io",
    "david.park@globalfirm.com",
    "elena.vasquez@webflow.org",
    "frank.liu@codebase.dev",
    "grace.kowalski@mailhub.com",
    "henry.okafor@datalink.net",
    "iris.campbell@appstack.io",
    "james.moretti@nexusco.com",
    "karen.petrov@infotech.dev",
    "liam.johansson@netbridge.org",
    "mia.tremblay@cloudmail.com",
    "nathan.osei@byteworks.net",
    "olivia.reyes@opendev.io",
    "paul.nakamura@logiclab.com",
    "quinn.harrison@webcraft.dev",
    "rosa.filipov@pixelnet.org",
    "sam.whitfield@techvault.com",
    "tina.bergstrom@codelink.net",
]


def verify_task(emails_path):
    """
    Verify that the emails.txt file was created correctly with 20 email addresses,
    one per line, matching the email column from csv_data.csv.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: emails.txt exists and has non-empty content (0.3 points)
    # This verifies the file was actually created as part of the task.
    # On initial_env, no emails.txt exists, so this FAILS. On golden_env it PASSES.
    try:
        if not os.path.exists(emails_path):
            print(f"FAIL: Component 1 — emails.txt does not exist at {emails_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(emails_path, 'r') as f:
            content = f.read()

        if len(content.strip()) > 0:
            print(f"PASS: Component 1 — emails.txt exists with non-empty content ({len(content)} bytes) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — emails.txt exists but is empty")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: emails.txt has exactly 20 non-empty lines (0.3 points)
    # This verifies that all 20 data rows had their email extracted (not more, not fewer).
    try:
        with open(emails_path, 'r') as f:
            lines = f.readlines()

        non_empty_lines = [line.strip() for line in lines if line.strip()]
        line_count = len(non_empty_lines)

        if line_count == 20:
            print(f"PASS: Component 2 — emails.txt has exactly 20 non-empty lines (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected 20 non-empty lines, found {line_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: emails.txt contains exactly the correct 20 email addresses (0.4 points)
    # This verifies the content accuracy - correct emails extracted from the email column.
    # Accepts any order but verifies exact email list matches the email column.
    try:
        with open(emails_path, 'r') as f:
            lines = f.readlines()

        actual_emails = [line.strip() for line in lines if line.strip()]
        actual_set = set(actual_emails)
        expected_set = set(EXPECTED_EMAILS)

        # Check if all expected emails are present
        missing = expected_set - actual_set
        extra = actual_set - expected_set

        if not missing and not extra:
            print(f"PASS: Component 3 — all 20 correct email addresses found in emails.txt (0.4 pts)")
            total_score += 0.4
        else:
            if missing:
                print(f"FAIL: Component 3 — {len(missing)} expected emails missing: {list(missing)[:3]}...")
            if extra:
                print(f"FAIL: Component 3 — {len(extra)} unexpected entries found: {list(extra)[:3]}...")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
emails_path = f'{WORKDIR}/Desktop/emails.txt'
verify_task(emails_path)
