"""
Reward Script: Extract inline type annotation into a separate named interface 'UserProfile'
Task ID: vscode_rrt_038
Domain: vscode
Scoring:
  Component 1 (0.4): Interface UserProfile is defined with all 4 required fields
  Component 2 (0.2): displayUser uses UserProfile as the user parameter type
  Component 3 (0.2): updateUser uses UserProfile as the user parameter type
  Component 4 (0.2): updateUser uses Partial<UserProfile> for data parameter
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_038'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'app', 'user.ts')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Interface UserProfile is defined with all 4 required fields (0.4 points)
    # We check that an interface named UserProfile exists and contains name, email, age, role fields
    try:
        # Match an interface block named UserProfile
        interface_pattern = r'interface\s+UserProfile\s*\{([^}]*)\}'
        interface_match = re.search(interface_pattern, content, re.DOTALL)

        if interface_match:
            body = interface_match.group(1)
            required_fields = {
                'name': r'name\s*:\s*string',
                'email': r'email\s*:\s*string',
                'age': r'age\s*:\s*number',
                'role': r"role\s*:\s*['\"]admin['\"]\s*\|\s*['\"]user['\"]",
            }
            fields_found = 0
            for field_name, field_pattern in required_fields.items():
                if re.search(field_pattern, body):
                    fields_found += 1
                else:
                    print(f"FAIL: Component 1 — field '{field_name}' not found or incorrect in UserProfile interface")

            if fields_found == 4:
                print(f"PASS: Component 1 — UserProfile interface defined with all 4 fields ({0.4} pts)")
                total_score += 0.4
            elif fields_found > 0:
                partial = round(0.4 * (fields_found / 4), 2)
                print(f"PARTIAL: Component 1 — {fields_found}/4 fields found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — UserProfile interface found but no required fields matched")
        else:
            print(f"FAIL: Component 1 — No 'interface UserProfile' definition found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: displayUser uses UserProfile as the user parameter type (0.2 points)
    try:
        # Match function displayUser with user parameter typed as UserProfile
        display_pattern = r'function\s+displayUser\s*\(\s*user\s*:\s*UserProfile\s*\)'
        if re.search(display_pattern, content):
            print(f"PASS: Component 2 — displayUser uses UserProfile type ({0.2} pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — displayUser does not use UserProfile as user parameter type")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: updateUser uses UserProfile as the user parameter type (0.2 points)
    try:
        # Match function updateUser with first param user: UserProfile
        update_user_pattern = r'function\s+updateUser\s*\(\s*user\s*:\s*UserProfile\s*,'
        if re.search(update_user_pattern, content):
            print(f"PASS: Component 3 — updateUser uses UserProfile for user param ({0.2} pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — updateUser does not use UserProfile as user parameter type")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: updateUser uses Partial<UserProfile> for data parameter (0.2 points)
    try:
        # Match data parameter typed as Partial<UserProfile>
        partial_pattern = r'function\s+updateUser\s*\([^)]*data\s*:\s*Partial\s*<\s*UserProfile\s*>'
        if re.search(partial_pattern, content):
            print(f"PASS: Component 4 — updateUser uses Partial<UserProfile> for data param ({0.2} pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — updateUser does not use Partial<UserProfile> for data parameter")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
