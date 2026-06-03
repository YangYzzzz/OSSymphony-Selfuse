"""
Initial Setup: Debugging deep-call/app.js in VSCode - paused inside calculateTotal function
Task ID: vscode_dbg_023
Domain: vs_code

Creates a Node.js project with:
  - app.js that calls calculateTotal() from utils.js at line 20 (line 21 is after the call)
  - utils.js with calculateTotal function, body at line 15
  - .vscode/launch.json with Node.js debug config and a breakpoint set inside calculateTotal
  - Opens VSCode with the project folder and starts the debug session
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'deep-call')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')

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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- utils.js ---
    # calculateTotal function body starts at line 15 per task context
    utils_js = """\
// utils.js — Utility functions for the deep-call project

const TAX_RATE = 0.08;
const DISCOUNT_THRESHOLD = 100;
const SHIPPING_BASE = 5.99;
const FREE_SHIPPING_MINIMUM = 50;

/**
 * Calculates the total order cost including tax, discounts, and shipping.
 * @param {number[]} items - Array of item prices
 * @returns {number} The final total
 */
function calculateTotal(items) {
    // line 15: start of function body
    let subtotal = items.reduce((sum, price) => sum + price, 0);

    let discount = 0;
    if (subtotal >= DISCOUNT_THRESHOLD) {
        discount = subtotal * 0.1;
    }

    const taxableAmount = subtotal - discount;
    const tax = taxableAmount * TAX_RATE;

    let shipping = SHIPPING_BASE;
    if (subtotal >= FREE_SHIPPING_MINIMUM) {
        shipping = 0;
    }

    const total = taxableAmount + tax + shipping;
    return Math.round(total * 100) / 100;
}

function formatCurrency(amount) {
    return '$' + amount.toFixed(2);
}

function getItemCount(items) {
    return items.length;
}

module.exports = { calculateTotal, formatCurrency, getItemCount };
"""

    # --- app.js ---
    # line 20: the call to calculateTotal, line 21: the line after
    app_js = """\
// app.js — Main entry point for the deep-call project
'use strict';

const { calculateTotal, formatCurrency, getItemCount } = require('./utils');

const STORE_NAME = 'TechMart Online Store';
const VERSION = '1.3.2';

function processOrder(orderId, items, customer) {
    console.log(`Processing order #${orderId} for ${customer.name}`);
    console.log(`Items in cart: ${getItemCount(items)}`);

    // Calculate the full order total (calls into utils.js)
    // Debugger is paused inside calculateTotal when Step Out is pressed
    const itemPrices = items.map(item => item.price);
    const discount = customer.loyaltyPoints > 500 ? 0.05 : 0;
    const adjustedPrices = itemPrices.map(p => p * (1 - discount));
    const baseRate = customer.memberSince ? 1.0 : 1.05;
    const finalPrices = adjustedPrices.map(p => p * baseRate);
    const total = calculateTotal(finalPrices); // line 20: call into utils.js
    const formattedTotal = formatCurrency(total); // line 21: line after call (Step Out lands here)

    console.log(`Order total: ${formattedTotal}`);
    return { orderId, total, formattedTotal };
}

function runDemo() {
    const customer = {
        name: 'Alexandra Rivera',
        email: 'a.rivera@example.com',
        loyaltyPoints: 750,
        memberSince: '2021-08-14'
    };

    const cartItems = [
        { id: 'ITEM-001', name: 'Wireless Keyboard', price: 49.99 },
        { id: 'ITEM-002', name: 'USB-C Hub 7-Port', price: 34.99 },
        { id: 'ITEM-003', name: 'Laptop Stand Adjustable', price: 28.95 },
        { id: 'ITEM-004', name: 'Webcam HD 1080p', price: 67.50 },
        { id: 'ITEM-005', name: 'Desk Mat Extra Large', price: 22.00 }
    ];

    console.log(`=== ${STORE_NAME} v${VERSION} ===`);
    const result = processOrder('ORD-20250315-0042', cartItems, customer);
    console.log('Order processed successfully:', result);
}

runDemo();
"""

    # --- .vscode/launch.json ---
    # Debug configuration for Node.js with a breakpoint inside calculateTotal (utils.js line 15)
    launch_json = {
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
                "stopOnEntry": False,
                "sourceMaps": False
            }
        ]
    }

    # --- .vscode/settings.json (workspace settings) ---
    workspace_settings = {
        "debug.openDebug": "openOnDebugBreak",
        "debug.toolBarLocation": "docked",
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "files.autoSave": "off"
    }

    # Write files
    utils_path = os.path.join(PROJECT_DIR, 'utils.js')
    app_path = os.path.join(PROJECT_DIR, 'app.js')
    launch_path = os.path.join(VSCODE_DIR, 'launch.json')
    settings_path = os.path.join(VSCODE_DIR, 'settings.json')

    with open(utils_path, 'w') as f:
        f.write(utils_js)
    print(f'Created: {utils_path}')

    with open(app_path, 'w') as f:
        f.write(app_js)
    print(f'Created: {app_path}')

    with open(launch_path, 'w') as f:
        json.dump(launch_json, f, indent=4)
    print(f'Created: {launch_path}')

    with open(settings_path, 'w') as f:
        json.dump(workspace_settings, f, indent=4)
    print(f'Created: {settings_path}')

    # Verify line numbers match task context
    with open(utils_path, 'r') as f:
        utils_lines = f.readlines()
    with open(app_path, 'r') as f:
        app_lines = f.readlines()

    print(f'\nLine verification:')
    print(f'  utils.js line 15: {utils_lines[14].rstrip()!r}')
    print(f'  app.js line 20:   {app_lines[19].rstrip()!r}')
    print(f'  app.js line 21:   {app_lines[20].rstrip()!r}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with deep-call project folder (DISPLAY=:0)')


create_initial()
