"""
Initial Setup: Multi-cursor editing to add 'export' before function declarations
Task ID: vscode_edit_043
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_043'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/modules.js'


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

    # 55-line JavaScript file with function declarations on lines 5, 18, 31, 44
    # Lines 5, 18, 31, 44 begin with 'function ' (NOT 'export function ')
    lines = [
        '// modules.js',                                                     # 1
        '// Utility module for e-commerce order processing',                 # 2
        '// Author: Dev Team | Version: 2.1.0',                             # 3
        '',                                                                  # 4
        'function calculateTotal(items) {',                                 # 5
        '    if (!items || items.length === 0) {',                          # 6
        '        return 0;',                                                 # 7
        '    }',                                                             # 8
        '    let total = 0;',                                                # 9
        '    for (const item of items) {',                                  # 10
        '        total += item.price * item.quantity;',                     # 11
        '    }',                                                             # 12
        '    const tax = 0.08;',                                            # 13
        '    return total * (1 + tax);',                                    # 14
        '}',                                                                 # 15
        '',                                                                  # 16
        '// Format a numeric value as a currency string',                   # 17
        'function formatCurrency(amount, currency) {',                      # 18
        '    if (typeof amount !== "number") {',                            # 19
        '        throw new TypeError("amount must be a number");',          # 20
        '    }',                                                             # 21
        '    const opts = {',                                               # 22
        '        style: "currency",',                                       # 23
        '        currency: currency || "USD",',                             # 24
        '        minimumFractionDigits: 2,',                                # 25
        '        maximumFractionDigits: 2,',                                # 26
        '    };',                                                            # 27
        '    return new Intl.NumberFormat("en-US", opts).format(amount);',  # 28
        '}',                                                                 # 29
        '',                                                                  # 30
        'function validateEmail(email) {',                                  # 31
        '    if (!email || typeof email !== "string") {',                   # 32
        '        return false;',                                             # 33
        '    }',                                                             # 34
        r'    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;',                   # 35
        '    const addr = email.trim().toLowerCase();',                     # 36
        '    if (addr.length > 254) {',                                     # 37
        '        return false;',                                             # 38
        '    }',                                                             # 39
        '    return re.test(addr);',                                        # 40
        '}',                                                                 # 41
        '',                                                                  # 42
        '// Build a summary report from an array of order objects',         # 43
        'function generateReport(data) {',                                  # 44
        '    let revenue = 0;',                                             # 45
        '    for (const order of data) {',                                  # 46
        '        revenue += order.amount;',                                 # 47
        '    }',                                                             # 48
        '    return {',                                                      # 49
        '        totalOrders: data.length,',                                # 50
        '        totalRevenue: revenue,',                                   # 51
        '        averageOrder: data.length > 0 ? revenue / data.length : 0,', # 52
        '        generatedAt: new Date().toISOString(),',                   # 53
        '    };',                                                            # 54
        '}',                                                                 # 55
    ]

    content = '\n'.join(lines) + '\n'

    with open(OUTPUT, 'w') as f:
        f.write(content)

    # Verify the file has exactly 55 lines and correct function positions
    with open(OUTPUT, 'r') as f:
        file_lines = f.readlines()

    print(f'File created: {OUTPUT} ({len(file_lines)} lines)')
    for idx in [4, 17, 30, 43]:
        print(f'  Line {idx+1:2}: {file_lines[idx].rstrip()}')

    # GUI-ready startup: open VSCode with the specific file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with modules.js on DISPLAY=:0')


create_initial()
