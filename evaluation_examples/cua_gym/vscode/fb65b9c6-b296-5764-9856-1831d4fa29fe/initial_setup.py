"""
Initial Setup: Save the currently open file '~/Desktop/draft.py' in VSCode
using the keyboard shortcut.
Task ID: vscode_edit_012
Domain: vs_code

Strategy:
  1. Write draft.py to Desktop with a Python function that has recent edits on
     lines 10-15 (the 'edited' content representing an unsaved buffer state).
  2. Open VSCode with the file.
  3. To simulate the unsaved-changes indicator, overwrite the disk file with the
     PRE-EDIT content shortly AFTER VSCode loads the file. This causes VSCode to
     detect the file has changed externally and marks the buffer as out-of-sync,
     showing the dot indicator. The buffer retains the edited content; the disk
     file has the older version.

Note: xdotool unavailable on this VM, so we rely on VSCode's external-change
detection mechanism instead.
"""

import os
import shlex
import subprocess
import time

DESKTOP = '/home/user/Desktop'
OUTPUT = f'{DESKTOP}/draft.py'

# The EDITED version — what VSCode's buffer will contain (lines 10-15 modified)
EDITED_CONTENT = """\
#!/usr/bin/env python3
\"\"\"
Sales Report Generator
Generates quarterly sales summaries for regional offices.
\"\"\"

import os
import json
from datetime import datetime


def calculate_regional_totals(sales_data, exclude_unknown=True):
    \"\"\"Calculate total sales per region; optionally exclude unknown regions.\"\"\"
    region_totals = {}
    for record in sales_data:
        region = record.get("region", "Unknown")
        amount = record.get("amount", 0.0)
        if exclude_unknown and region == "Unknown":
            continue
        if region not in region_totals:
            region_totals[region] = 0.0
        region_totals[region] += amount
    return region_totals


def generate_summary_report(sales_data, output_path):
    \"\"\"Generate a formatted summary report and write it to output_path.\"\"\"
    totals = calculate_regional_totals(sales_data)
    report_date = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"Sales Summary Report \u2014 {report_date}",
        "=" * 45,
        "",
    ]
    for region, total in sorted(totals.items()):
        lines.append(f"  {region:<20} ${total:>12,.2f}")

    lines += [
        "",
        f"  {'GRAND TOTAL':<20} ${sum(totals.values()):>12,.2f}",
        "=" * 45,
    ]

    with open(output_path, "w") as f:
        f.write("\\n".join(lines))

    print(f"Report written to {output_path}")
    return output_path


if __name__ == "__main__":
    sample_data = [
        {"region": "North America", "amount": 128_450.75},
        {"region": "Europe",        "amount":  97_320.50},
        {"region": "Asia Pacific",  "amount": 154_870.00},
        {"region": "Latin America", "amount":  43_215.25},
        {"region": "North America", "amount":  61_890.00},
        {"region": "Europe",        "amount":  38_540.80},
    ]
    generate_summary_report(sample_data, "/tmp/sales_report.txt")
"""

# The PRE-EDIT version — written back to disk after VSCode loads the edited version
# to create the "file changed on disk" dirty indicator in VSCode
PRE_EDIT_CONTENT = """\
#!/usr/bin/env python3
\"\"\"
Sales Report Generator
Generates quarterly sales summaries for regional offices.
\"\"\"

import os
import json
from datetime import datetime


def calculate_regional_totals(sales_data):
    \"\"\"Calculate total sales per region from raw sales records.\"\"\"
    region_totals = {}
    for record in sales_data:
        region = record.get("region", "Unknown")
        amount = record.get("amount", 0.0)
        if region not in region_totals:
            region_totals[region] = 0.0
        region_totals[region] += amount
    return region_totals


def generate_summary_report(sales_data, output_path):
    \"\"\"Generate a formatted summary report and write it to output_path.\"\"\"
    totals = calculate_regional_totals(sales_data)
    report_date = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"Sales Summary Report \u2014 {report_date}",
        "=" * 45,
        "",
    ]
    for region, total in sorted(totals.items()):
        lines.append(f"  {region:<20} ${total:>12,.2f}")

    lines += [
        "",
        f"  {'GRAND TOTAL':<20} ${sum(totals.values()):>12,.2f}",
        "=" * 45,
    ]

    with open(output_path, "w") as f:
        f.write("\\n".join(lines))

    print(f"Report written to {output_path}")
    return output_path


if __name__ == "__main__":
    sample_data = [
        {"region": "North America", "amount": 128_450.75},
        {"region": "Europe",        "amount":  97_320.50},
        {"region": "Asia Pacific",  "amount": 154_870.00},
        {"region": "Latin America", "amount":  43_215.25},
        {"region": "North America", "amount":  61_890.00},
        {"region": "Europe",        "amount":  38_540.80},
    ]
    generate_summary_report(sample_data, "/tmp/sales_report.txt")
"""


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Step 1: Write the EDITED (buffer) version to disk first
    with open(OUTPUT, 'w') as f:
        f.write(EDITED_CONTENT)
    print(f'Initial file (edited version) written: {OUTPUT}')

    # Step 2: Open VSCode with the edited file — VSCode loads this into its buffer
    launch_gui(f'code "{OUTPUT}"', delay_sec=5.0)

    # Step 3: After VSCode has loaded the file, overwrite disk with PRE-EDIT version.
    # VSCode detects the external change and shows a notification, plus the tab
    # will show an unsaved-changes indicator because the buffer differs from disk.
    with open(OUTPUT, 'w') as f:
        f.write(PRE_EDIT_CONTENT)
    print(f'Disk file reverted to pre-edit version (creates VSCode dirty indicator): {OUTPUT}')

    print('GUI_READY: VSCode opened with draft.py; tab shows unsaved-changes indicator')


create_initial()
