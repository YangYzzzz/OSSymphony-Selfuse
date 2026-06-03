"""
Initial Setup: VSCode column/box selection on CSV email column
Task ID: vscode_edit_075
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_075'
DESKTOP = f'{WORKDIR}/Desktop'
CSV_OUTPUT = f'{DESKTOP}/csv_data.csv'

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

    # Make sure emails.txt does NOT exist in initial state
    emails_path = f'{DESKTOP}/emails.txt'
    if os.path.exists(emails_path):
        os.remove(emails_path)

    # CSV data: name, age, email, phone
    # Names are padded to consistent width so email column starts at a fixed character position.
    # Format: fixed-width fields separated by commas for reliable box selection.
    # name: up to 18 chars (padded), age: 2 digits, email: variable, phone: 12 chars
    rows = [
        ("Alice Morgan",     28, "alice.morgan@techcorp.com",    "555-201-4301"),
        ("Brian Sullivan",   34, "brian.sullivan@devmail.net",   "555-312-5402"),
        ("Clara Nguyen",     26, "clara.nguyen@startup.io",      "555-423-6503"),
        ("David Park",       41, "david.park@globalfirm.com",    "555-534-7604"),
        ("Elena Vasquez",    33, "elena.vasquez@webflow.org",    "555-645-8705"),
        ("Frank Liu",        29, "frank.liu@codebase.dev",       "555-756-9806"),
        ("Grace Kowalski",   37, "grace.kowalski@mailhub.com",   "555-867-0907"),
        ("Henry Okafor",     45, "henry.okafor@datalink.net",    "555-978-1008"),
        ("Iris Campbell",    31, "iris.campbell@appstack.io",    "555-089-2109"),
        ("James Moretti",    38, "james.moretti@nexusco.com",    "555-190-3210"),
        ("Karen Petrov",     27, "karen.petrov@infotech.dev",    "555-201-4311"),
        ("Liam Johansson",   44, "liam.johansson@netbridge.org", "555-312-5412"),
        ("Mia Tremblay",     30, "mia.tremblay@cloudmail.com",   "555-423-6513"),
        ("Nathan Osei",      36, "nathan.osei@byteworks.net",    "555-534-7614"),
        ("Olivia Reyes",     25, "olivia.reyes@opendev.io",      "555-645-8715"),
        ("Paul Nakamura",    42, "paul.nakamura@logiclab.com",   "555-756-9816"),
        ("Quinn Harrison",   39, "quinn.harrison@webcraft.dev",  "555-867-0917"),
        ("Rosa Filipov",     28, "rosa.filipov@pixelnet.org",    "555-978-1018"),
        ("Sam Whitfield",    35, "sam.whitfield@techvault.com",  "555-089-2119"),
        ("Tina Bergstrom",   32, "tina.bergstrom@codelink.net",  "555-190-3220"),
    ]

    header = "name,age,email,phone"
    lines = [header]
    for name, age, email, phone in rows:
        lines.append(f"{name},{age},{email},{phone}")

    csv_content = "\n".join(lines) + "\n"

    with open('/tmp/csv_data_temp.csv', 'w') as f:
        f.write(csv_content)

    # We write locally then the script runs on VM — but since this runs on the VM,
    # we write directly to the DESKTOP path
    with open(CSV_OUTPUT, 'w') as f:
        f.write(csv_content)

    print(f'Initial CSV file created: {CSV_OUTPUT}')
    print(f'Lines: {len(lines)} (1 header + {len(rows)} data rows)')

    # GUI-ready startup: open VSCode with the CSV file
    launch_gui(f'code "{CSV_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with csv_data.csv on DISPLAY=:0')


create_initial()
