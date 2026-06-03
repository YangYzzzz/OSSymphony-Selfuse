"""
Initial Setup: Multi-cursor editing task - modernize.js with var declarations
Task ID: vscode_edit_062
Domain: vs_code

JS File Line Structure (40 lines, 8 var declarations):
  Line  4: var TAX_RATE = 0.08;                    -> const (never reassigned)
  Line  5: var FREE_SHIPPING_THRESHOLD = 50.0;     -> const (never reassigned)
  Line  6: var MAX_ITEMS_PER_ORDER = 100;          -> const (never reassigned)
  Line  9: var formatter = new Intl...;            -> const (never reassigned)
  Line 15: var total = cart.subtotal;              -> LET   (reassigned on line 16)
  Line 21: var DISCOUNT_RATES = {...};             -> const (never reassigned)
  Line 26: var BASE_RATE = 4.99;                  -> const (never reassigned)
  Line 28: var shippingCost = BASE_RATE;           -> LET   (reassigned on lines 30/32)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_062'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/modernize.js'


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

    # Build lines list to verify line numbers exactly
    lines = [
        "// modernize.js - Shopping cart module",                           #  1
        "// This file needs to be updated to use modern ES6+ syntax.",      #  2
        "",                                                                  #  3
        "var TAX_RATE = 0.08;",                                             #  4  -> const
        "var FREE_SHIPPING_THRESHOLD = 50.0;",                              #  5  -> const
        "var MAX_ITEMS_PER_ORDER = 100;",                                   #  6  -> const
        "",                                                                  #  7
        "function formatPrice(amount) {",                                   #  8
        "    var formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });",  #  9  -> const
        "    return formatter.format(amount);",                             # 10
        "}",                                                                # 11
        "",                                                                 # 12
        "function processOrder(cart) {",                                    # 13
        "    if (cart.items.length > MAX_ITEMS_PER_ORDER) return null;",   # 14
        "    var total = cart.subtotal;",                                   # 15  -> LET (reassigned line 16)
        "    total += total * TAX_RATE;",                                   # 16
        "    return formatPrice(total);",                                   # 17
        "}",                                                                # 18
        "",                                                                 # 19
        "function getPromoDiscount(code) {",                               # 20
        "    var DISCOUNT_RATES = { 'SAVE10': 0.10, 'SAVE20': 0.20, 'SAVE30': 0.30 };",  # 21  -> const
        "    return DISCOUNT_RATES[code] || 0;",                           # 22
        "}",                                                                # 23
        "",                                                                 # 24
        "function calculateShipping(subtotal, isExpress) {",               # 25
        "    var BASE_RATE = 4.99;",                                        # 26  -> const
        "    // Adjust shipping cost based on subtotal and delivery type",  # 27
        "    var shippingCost = BASE_RATE;",                               # 28  -> LET (reassigned lines 30/32)
        "    if (subtotal >= FREE_SHIPPING_THRESHOLD) {",                  # 29
        "        shippingCost = 0;",                                        # 30
        "    } else if (isExpress) {",                                     # 31
        "        shippingCost = BASE_RATE * 1.5;",                        # 32
        "    }",                                                            # 33
        "    return shippingCost;",                                        # 34
        "}",                                                                # 35
        "",                                                                 # 36
        "module.exports = {",                                              # 37
        "    formatPrice: formatPrice,",                                    # 38
        "    processOrder: processOrder,",                                  # 39
        "    calculateShipping: calculateShipping",                        # 40
        "};",                                                               # 41 <- OOPS, that's 41 lines with the closing brace
    ]

    # Verify line count
    assert len(lines) == 41, f"Expected 41 lines but got {len(lines)}"
    # Wait - we need exactly 40 lines. Remove line 39 (processOrder export) to get 40 total.
    # Actually the closing "};" is line 41. To get 40, we need to remove one line.
    # Let's combine the module.exports into one line:
    lines = lines[:36]  # lines 1-36
    lines.append("module.exports = { formatPrice, processOrder, getPromoDiscount, calculateShipping };")  # line 37
    lines.append("// End of modernize.js")  # line 38
    lines.append("")  # line 39
    lines.append("// Version: 1.0.0 | Last modified: 2025-01-15")  # line 40

    assert len(lines) == 40, f"Expected 40 lines but got {len(lines)}"

    # Count var declarations
    var_count = sum(1 for line in lines if line.strip().startswith('var '))
    assert var_count == 8, f"Expected 8 var declarations but found {var_count}"

    js_content = "\n".join(lines) + "\n"

    with open(OUTPUT, 'w') as f:
        f.write(js_content)

    print(f'Initial file created: {OUTPUT}')
    print(f'File has {len(lines)} lines and {var_count} var declarations')

    # Verify line 15 and line 28 have var declarations
    assert lines[14].strip().startswith('var '), f"Line 15 should be var: {lines[14]}"
    assert lines[27].strip().startswith('var '), f"Line 28 should be var: {lines[27]}"
    print(f'Line 15: {lines[14]}')
    print(f'Line 28: {lines[27]}')

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
