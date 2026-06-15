"""
Initial Setup: Select lines 10-20 and use Find and Replace within selection to replace null with 0
Task ID: vscode_edit_068
Domain: vs_code
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'vscode_edit_068'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/data.json'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    # 50-line JSON file with:
    #   - 5 null values within lines 10-20
    #   - 7 null values outside that range (lines 1-9 and 21-50)
    # Structure: a realistic employee/project dataset
    # Lines are counted 1-based in the final file.
    #
    # We'll construct the file as a list of lines so we can precisely
    # control where nulls appear.
    #
    # File layout (line numbers, 1-based):
    #   Line  1: {
    #   Line  2:   "company": "Nexus Analytics",
    #   Line  3:   "quarter": "Q1-2025",
    #   Line  4:   "employees": [
    #   Line  5:     {
    #   Line  6:       "id": 1,
    #   Line  7:       "name": "Sarah Chen",
    #   Line  8:       "department": "Engineering",
    #   Line  9:       "manager": null,          <-- null #1 (outside range)
    #   Line 10:       "salary": 85000,
    #   Line 11:       "bonus": null,            <-- null #2 (inside range, line 11)
    #   Line 12:       "office": "San Francisco",
    #   Line 13:       "start_date": "2022-03-15",
    #   Line 14:       "performance": null,      <-- null #3 (inside range, line 14)
    #   Line 15:       "certifications": null,   <-- null #4 (inside range, line 15)
    #   Line 16:       "remote": true
    #   Line 17:     },
    #   Line 18:     {
    #   Line 19:       "id": 2,
    #   Line 20:       "name": "Marcus Johnson", <-- line 20 (no null here itself)
    #   Line 21:       "department": "Marketing",
    #   ...
    #
    # Wait — we need 5 nulls within lines 10-20 exactly. Let me redesign:
    #
    # Line  9: "manager": null,      null #1 OUTSIDE
    # Line 11: "bonus": null,        null #2 INSIDE (11)
    # Line 14: "performance": null,  null #3 INSIDE (14)
    # Line 15: "certifications": null, null #4 INSIDE (15)
    # Line 18: "end_date": null,     null #5 INSIDE (18)
    # Line 19: "notes": null,        null #6 INSIDE (19)
    # Line 23: "phone": null,        null #7 OUTSIDE
    # Line 27: "emergency": null,    null #8 OUTSIDE
    # Line 33: "linkedin": null,     null #9 OUTSIDE
    # Line 38: "alt_email": null,    null #10 OUTSIDE
    # Line 43: "termination": null,  null #11 OUTSIDE
    # Line 48: "feedback": null,     null #12 OUTSIDE
    #
    # That gives: nulls inside lines 10-20: lines 11,14,15,18,19 = 5 nulls (CORRECT)
    # Nulls outside lines 10-20: lines 9,23,27,33,38,43,48 = 7 nulls (CORRECT)

    lines = [
        '{',                                          # 1
        '  "company": "Nexus Analytics",',            # 2
        '  "quarter": "Q1-2025",',                    # 3
        '  "employees": [',                           # 4
        '    {',                                      # 5
        '      "id": 1,',                             # 6
        '      "name": "Sarah Chen",',                # 7
        '      "department": "Engineering",',         # 8
        '      "manager": null,',                     # 9  -- null #1 OUTSIDE
        '      "salary": 85000,',                     # 10
        '      "bonus": null,',                       # 11 -- null #2 INSIDE
        '      "office": "San Francisco",',           # 12
        '      "start_date": "2022-03-15",',          # 13
        '      "performance": null,',                 # 14 -- null #3 INSIDE
        '      "certifications": null,',              # 15 -- null #4 INSIDE
        '      "remote": true,',                      # 16
        '      "years_exp": 5,',                      # 17
        '      "end_date": null,',                    # 18 -- null #5 INSIDE
        '      "notes": null',                        # 19 -- null #6 INSIDE (5 total inside)
        '    },',                                     # 20
        '    {',                                      # 21
        '      "id": 2,',                             # 22
        '      "phone": null,',                       # 23 -- null #7 OUTSIDE
        '      "name": "Marcus Johnson",',            # 24
        '      "department": "Marketing",',           # 25
        '      "salary": 72000,',                     # 26
        '      "emergency": null,',                   # 27 -- null #8 OUTSIDE
        '      "office": "New York",',                # 28
        '      "start_date": "2021-06-01",',          # 29
        '      "performance": "Exceeds",',            # 30
        '      "certifications": ["HubSpot"],',       # 31
        '      "remote": false,',                     # 32
        '      "linkedin": null,',                    # 33 -- null #9 OUTSIDE
        '      "years_exp": 3',                       # 34
        '    },',                                     # 35
        '    {',                                      # 36
        '      "id": 3,',                             # 37
        '      "alt_email": null,',                   # 38 -- null #10 OUTSIDE
        '      "name": "Priya Patel",',               # 39
        '      "department": "Finance",',             # 40
        '      "salary": 91000,',                     # 41
        '      "office": "Chicago",',                 # 42
        '      "termination": null,',                 # 43 -- null #11 OUTSIDE
        '      "start_date": "2020-11-20",',          # 44
        '      "performance": "Outstanding",',        # 45
        '      "certifications": ["CPA", "CFA"],',    # 46
        '      "remote": true,',                      # 47
        '      "feedback": null',                     # 48 -- null #12 OUTSIDE
        '    }',                                      # 49
        '  ]',                                        # 50
        '}',                                          # 51 -- extra closing brace line
    ]

    # We want exactly 50 lines. The above has 51 lines. Remove the last line
    # and merge "  ]" and "}" or restructure. Let's recount and fix:
    # Lines 1-50 should be valid JSON. Let's restructure to exactly 50 lines.

    lines_50 = [
        '{',                                          # 1
        '  "company": "Nexus Analytics",',            # 2
        '  "quarter": "Q1-2025",',                    # 3
        '  "employees": [',                           # 4
        '    {',                                      # 5
        '      "id": 1,',                             # 6
        '      "name": "Sarah Chen",',                # 7
        '      "department": "Engineering",',         # 8
        '      "manager": null,',                     # 9  -- null #1 OUTSIDE
        '      "salary": 85000,',                     # 10
        '      "bonus": null,',                       # 11 -- null #2 INSIDE
        '      "office": "San Francisco",',           # 12
        '      "start_date": "2022-03-15",',          # 13
        '      "performance": null,',                 # 14 -- null #3 INSIDE
        '      "certifications": null,',              # 15 -- null #4 INSIDE
        '      "remote": true,',                      # 16
        '      "years_exp": 5,',                      # 17
        '      "end_date": null,',                    # 18 -- null #5 INSIDE
        '      "notes": null',                        # 19 -- null #6 INSIDE  (5 total inside lines 10-20)
        '    },',                                     # 20
        '    {',                                      # 21
        '      "id": 2,',                             # 22
        '      "phone": null,',                       # 23 -- null #7 OUTSIDE
        '      "name": "Marcus Johnson",',            # 24
        '      "department": "Marketing",',           # 25
        '      "salary": 72000,',                     # 26
        '      "emergency": null,',                   # 27 -- null #8 OUTSIDE
        '      "office": "New York",',                # 28
        '      "start_date": "2021-06-01",',          # 29
        '      "performance": "Exceeds",',            # 30
        '      "certifications": ["HubSpot"],',       # 31
        '      "remote": false,',                     # 32
        '      "linkedin": null,',                    # 33 -- null #9 OUTSIDE
        '      "years_exp": 3',                       # 34
        '    },',                                     # 35
        '    {',                                      # 36
        '      "id": 3,',                             # 37
        '      "alt_email": null,',                   # 38 -- null #10 OUTSIDE
        '      "name": "Priya Patel",',               # 39
        '      "department": "Finance",',             # 40
        '      "salary": 91000,',                     # 41
        '      "office": "Chicago",',                 # 42
        '      "termination": null,',                 # 43 -- null #11 OUTSIDE
        '      "start_date": "2020-11-20",',          # 44
        '      "performance": "Outstanding",',        # 45
        '      "certifications": ["CPA", "CFA"],',    # 46
        '      "remote": true,',                      # 47
        '      "feedback": null',                     # 48 -- null #12 OUTSIDE
        '    }',                                      # 49
        '  ]}',                                       # 50
    ]

    # Verify counts
    content = '\n'.join(lines_50)
    all_lines = content.split('\n')
    assert len(all_lines) == 50, f"Expected 50 lines, got {len(all_lines)}"

    # Count nulls in lines 10-20 (0-indexed: 9-19)
    nulls_inside = sum(1 for i in range(9, 20) if 'null' in all_lines[i])
    nulls_total = content.count('null')
    nulls_outside = nulls_total - nulls_inside

    print(f"Total null count: {nulls_total}")
    print(f"Null count in lines 10-20: {nulls_inside}")
    print(f"Null count outside lines 10-20: {nulls_outside}")

    assert nulls_inside == 5, f"Expected 5 nulls inside lines 10-20, got {nulls_inside}"
    assert nulls_total == 12, f"Expected 12 total nulls, got {nulls_total}"
    assert nulls_outside == 7, f"Expected 7 nulls outside lines 10-20, got {nulls_outside}"

    with open(OUTPUT, 'w') as f:
        f.write(content + '\n')

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open file in VSCode
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with data.json and DISPLAY=:0')


create_initial()
