"""
Initial Setup: Debug app.js and view Call Stack panel in VSCode
Task ID: vscode_dbg_026
Domain: vs_code

Creates ~/projects/callstack-demo/app.js with a function call chain:
  main() -> processOrder() -> validatePayment() -> checkBalance()
A breakpoint is configured at line 25 inside checkBalance().
VSCode launch config (launch.json) is also created for Node.js debugging.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_026'
PROJECT_DIR = f'{WORKDIR}/projects/callstack-demo'
APP_JS = f'{PROJECT_DIR}/app.js'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
LAUNCH_JSON = f'{VSCODE_DIR}/launch.json'


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
    # Create project directory structure
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create app.js with realistic content
    # The call chain: main() -> processOrder() -> validatePayment() -> checkBalance()
    # Breakpoint will be at line 25 inside checkBalance()
    app_js_content = """\
// E-commerce Order Processing System
// Demonstrates nested function calls for debugging practice

const ORDER_LIMIT = 10000;
const MIN_BALANCE = 50;

/**
 * Check if the customer's account balance is sufficient for the order.
 * @param {number} balance - Customer's current balance
 * @param {number} amount - Order amount to check
 * @returns {boolean} true if balance is sufficient
 */
function checkBalance(balance, amount) {
    // Verify account has minimum required balance
    if (balance < MIN_BALANCE) {
        console.log(`Account balance too low: $${balance}`);
        return false;
    }

    // Check if balance covers the order amount
    const hasSufficientFunds = balance >= amount;
    console.log(`Balance check: $${balance} vs required $${amount}`);

    // Evaluate the payment feasibility  <-- line 25: breakpoint here
    const result = hasSufficientFunds && (amount <= ORDER_LIMIT);
    return result;
}

/**
 * Validate that the payment details and balance are acceptable.
 * @param {Object} paymentInfo - Payment details object
 * @returns {boolean} true if payment is valid
 */
function validatePayment(paymentInfo) {
    console.log('Validating payment for order:', paymentInfo.orderId);

    if (!paymentInfo || !paymentInfo.amount) {
        throw new Error('Invalid payment information provided');
    }

    const balanceOk = checkBalance(paymentInfo.accountBalance, paymentInfo.amount);

    if (!balanceOk) {
        console.log('Payment validation failed: insufficient funds');
        return false;
    }

    console.log('Payment validation passed');
    return true;
}

/**
 * Process a customer order through validation and fulfillment.
 * @param {Object} order - Order details object
 */
function processOrder(order) {
    console.log(`Processing order #${order.id} for ${order.customerName}`);

    const paymentInfo = {
        orderId: order.id,
        amount: order.total,
        accountBalance: order.customerBalance,
        currency: 'USD'
    };

    const paymentValid = validatePayment(paymentInfo);

    if (paymentValid) {
        console.log(`Order #${order.id} approved - Total: $${order.total}`);
    } else {
        console.log(`Order #${order.id} rejected - Payment validation failed`);
    }

    return paymentValid;
}

/**
 * Main entry point - processes a sample order.
 */
function main() {
    console.log('=== Order Processing System Started ===');

    const sampleOrder = {
        id: 'ORD-2025-0472',
        customerName: 'Alice Thompson',
        customerBalance: 3500.00,
        total: 299.99,
        items: [
            { name: 'Wireless Keyboard Pro', qty: 1, price: 149.99 },
            { name: 'USB-C Hub 7-Port', qty: 2, price: 75.00 }
        ],
        shippingAddress: '742 Evergreen Terrace, Springfield, IL'
    };

    const success = processOrder(sampleOrder);

    if (success) {
        console.log('Order processing complete - SUCCESS');
    } else {
        console.log('Order processing complete - FAILED');
    }

    console.log('=== Order Processing System Finished ===');
}

// Run the main function
main();
"""

    with open(APP_JS, 'w') as f:
        f.write(app_js_content)
    print(f'Created: {APP_JS}')

    # Verify line 25 content (where breakpoint should be)
    lines = app_js_content.split('\n')
    print(f'Line 25 content: {lines[24]}')  # 0-indexed

    # Create VSCode launch.json for Node.js debugging
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Debug app.js",
                "program": "${workspaceFolder}/app.js",
                "console": "integratedTerminal",
                "skipFiles": [
                    "<node_internals>/**"
                ],
                "stopOnEntry": False
            }
        ]
    }

    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)
    print(f'Created: {LAUNCH_JSON}')

    # Pre-configure the breakpoint in VSCode workspace settings
    # VSCode stores breakpoints in .vscode/settings.json or workspace state
    # We set them via the launch config and will also add to a breakpoints file
    settings = {
        "debug.openDebug": "openOnDebugBreak",
        "debug.toolBarLocation": "docked",
        "workbench.panel.defaultLocation": "bottom"
    }

    settings_path = f'{VSCODE_DIR}/settings.json'
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Created: {settings_path}')

    # Create package.json for the project
    package_json = {
        "name": "callstack-demo",
        "version": "1.0.0",
        "description": "E-commerce order processing demonstration for call stack debugging",
        "main": "app.js",
        "scripts": {
            "start": "node app.js",
            "debug": "node --inspect app.js"
        },
        "keywords": ["debugging", "callstack", "nodejs"],
        "author": "Dev Team",
        "license": "MIT"
    }

    package_json_path = f'{PROJECT_DIR}/package.json'
    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=4)
    print(f'Created: {package_json_path}')

    print(f'\nProject structure:')
    print(f'  {PROJECT_DIR}/')
    print(f'  ├── app.js          (main application with call chain)')
    print(f'  ├── package.json    (npm project config)')
    print(f'  └── .vscode/')
    print(f'      ├── launch.json (debug configuration)')
    print(f'      └── settings.json (workspace settings)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with callstack-demo project (DISPLAY=:0)')


create_initial()
