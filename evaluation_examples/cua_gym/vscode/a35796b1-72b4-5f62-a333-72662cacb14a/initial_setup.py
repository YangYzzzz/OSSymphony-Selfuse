"""
Initial Setup: Duplicate lines 20-25 of template.py and paste below with renamed variables
Task ID: vscode_edit_065
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'vscode_edit_065'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/template.py'


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

    # 50-line Python file
    # Lines 20-25 (1-indexed) define a data processing block
    # using variables input_data, processed, and result
    lines = [
        "#!/usr/bin/env python3\n",                                  # line 1
        '"""Data pipeline utilities for batch processing jobs."""\n', # line 2
        "\n",                                                         # line 3
        "import os\n",                                               # line 4
        "import sys\n",                                              # line 5
        "import json\n",                                             # line 6
        "import logging\n",                                          # line 7
        "\n",                                                         # line 8
        "LOG = logging.getLogger(__name__)\n",                       # line 9
        "\n",                                                         # line 10
        "\n",                                                         # line 11
        "def load_config(config_path):\n",                           # line 12
        "    with open(config_path, 'r') as f:\n",                   # line 13
        "        return json.load(f)\n",                             # line 14
        "\n",                                                         # line 15
        "\n",                                                         # line 16
        "def process_batch(config_path, source_dir):\n",             # line 17
        "    config = load_config(config_path)\n",                   # line 18
        "    LOG.info('Starting batch processing ...')\n",           # line 19
        "    input_data = [f for f in os.listdir(source_dir)\n",     # line 20
        "                  if f.endswith('.csv')]\n",                 # line 21
        "    processed = [item.strip() for item in input_data]\n",   # line 22
        "    result = {'count': len(processed),\n",                  # line 23
        "              'files': processed,\n",                       # line 24
        "              'source': source_dir}\n",                     # line 25
        "    LOG.info('Batch finished: %d files', result['count'])\n", # line 26
        "    return result\n",                                        # line 27
        "\n",                                                         # line 28
        "\n",                                                         # line 29
        "def validate_output(result, required_keys=None):\n",        # line 30
        "    if required_keys is None:\n",                           # line 31
        "        required_keys = ['count', 'files', 'source']\n",    # line 32
        "    for key in required_keys:\n",                           # line 33
        "        if key not in result:\n",                           # line 34
        "            raise KeyError(f'Missing key: {key}')\n",       # line 35
        "    return True\n",                                         # line 36
        "\n",                                                         # line 37
        "\n",                                                         # line 38
        "def write_report(result, output_path):\n",                  # line 39
        "    with open(output_path, 'w') as f:\n",                   # line 40
        "        json.dump(result, f, indent=4)\n",                  # line 41
        "    LOG.info('Report written to %s', output_path)\n",       # line 42
        "\n",                                                         # line 43
        "\n",                                                         # line 44
        "if __name__ == '__main__':\n",                              # line 45
        "    logging.basicConfig(level=logging.INFO)\n",             # line 46
        "    config_path = sys.argv[1]\n",                           # line 47
        "    source_dir = sys.argv[2]\n",                            # line 48
        "    output_path = sys.argv[3]\n",                           # line 49
        "    res = process_batch(config_path, source_dir)\n",        # line 50
    ]

    assert len(lines) == 50, f"Expected 50 lines, got {len(lines)}"

    with open(OUTPUT, 'w') as f:
        f.writelines(lines)

    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines: {len(lines)}')

    # GUI-ready startup: open VSCode with the Desktop folder and the target file
    launch_gui(f'code "{DESKTOP}"', delay_sec=2.0)
    time.sleep(1.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
