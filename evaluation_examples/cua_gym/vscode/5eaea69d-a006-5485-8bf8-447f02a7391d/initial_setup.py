"""
Initial Setup: Add function breakpoint for 'processOrder' in VSCode
Task ID: vscode_dbg_045
Domain: vs_code

Creates the initial environment:
- ~/projects/func-bp/ workspace with app.js defining processOrder()
- VSCode launch.json for Node.js debugging
- Opens VSCode with Run & Debug sidebar — NO function breakpoints set
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_045'
PROJECT_DIR = f'{WORKDIR}/projects/func-bp'


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


def create_workspace():
    """Create the func-bp project workspace with realistic JS source files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, '.vscode'), exist_ok=True)

    # app.js — main application file with processOrder and supporting functions
    app_js = """\
/**
 * Order Processing Module
 * Handles e-commerce order lifecycle management
 */

const TAX_RATE = 0.08;
const SHIPPING_THRESHOLD = 50.00;
const FREE_SHIPPING_RATE = 0.00;
const STANDARD_SHIPPING_RATE = 5.99;

/**
 * Validates that an order object has required fields.
 * @param {Object} order
 * @returns {boolean}
 */
function validateOrder(order) {
    if (!order || typeof order !== 'object') {
        return false;
    }
    if (!order.id || !order.customer || !order.items) {
        return false;
    }
    if (!Array.isArray(order.items) || order.items.length === 0) {
        return false;
    }
    return true;
}

/**
 * Calculates the subtotal for a list of order items.
 * @param {Array} items
 * @returns {number}
 */
function calculateSubtotal(items) {
    return items.reduce((sum, item) => {
        return sum + (item.price * item.quantity);
    }, 0);
}

/**
 * Determines shipping cost based on order subtotal.
 * @param {number} subtotal
 * @returns {number}
 */
function calculateShipping(subtotal) {
    return subtotal >= SHIPPING_THRESHOLD ? FREE_SHIPPING_RATE : STANDARD_SHIPPING_RATE;
}

/**
 * Processes a customer order end-to-end: validates, calculates totals,
 * applies tax and shipping, and returns the completed order summary.
 * @param {Object} order - The order object with id, customer, and items
 * @returns {Object} Processed order with totals or error status
 */
function processOrder(order) {
    if (!validateOrder(order)) {
        return { success: false, error: 'Invalid order data', orderId: order && order.id };
    }

    const subtotal = calculateSubtotal(order.items);
    const tax = parseFloat((subtotal * TAX_RATE).toFixed(2));
    const shipping = calculateShipping(subtotal);
    const total = parseFloat((subtotal + tax + shipping).toFixed(2));

    const processedOrder = {
        success: true,
        orderId: order.id,
        customer: order.customer,
        items: order.items,
        subtotal: parseFloat(subtotal.toFixed(2)),
        tax: tax,
        shipping: shipping,
        total: total,
        processedAt: new Date().toISOString(),
        status: 'confirmed'
    };

    console.log(`Order ${order.id} processed successfully. Total: $${total}`);
    return processedOrder;
}

/**
 * Batch processes multiple orders and returns a summary report.
 * @param {Array} orders
 * @returns {Object} Batch processing summary
 */
function processBatch(orders) {
    const results = {
        total: orders.length,
        successful: 0,
        failed: 0,
        orders: []
    };

    for (const order of orders) {
        const result = processOrder(order);
        results.orders.push(result);
        if (result.success) {
            results.successful++;
        } else {
            results.failed++;
        }
    }

    console.log(`Batch complete: ${results.successful}/${results.total} orders processed.`);
    return results;
}

// Sample orders for testing
const sampleOrders = [
    {
        id: 'ORD-2025-001',
        customer: { name: 'Alice Thompson', email: 'alice.thompson@example.com' },
        items: [
            { sku: 'LAPTOP-PRO-15', name: 'Laptop Pro 15"', price: 1299.99, quantity: 1 },
            { sku: 'USB-HUB-7P',   name: '7-Port USB Hub',  price: 34.99,   quantity: 2 }
        ]
    },
    {
        id: 'ORD-2025-002',
        customer: { name: 'Bob Martinez', email: 'bob.martinez@example.com' },
        items: [
            { sku: 'WIRELESS-MOUSE', name: 'Wireless Mouse', price: 29.99, quantity: 1 },
            { sku: 'DESK-PAD-XL',    name: 'Desk Pad XL',    price: 19.99, quantity: 1 }
        ]
    },
    {
        id: 'ORD-2025-003',
        customer: { name: 'Carol Lee', email: 'carol.lee@example.com' },
        items: [
            { sku: 'MONITOR-27',  name: '27" 4K Monitor',   price: 449.00, quantity: 1 },
            { sku: 'HDMI-CABLE',  name: 'HDMI 2.1 Cable',   price: 12.99,  quantity: 2 },
            { sku: 'MONITOR-ARM', name: 'Adjustable Monitor Arm', price: 79.99, quantity: 1 }
        ]
    }
];

// Run batch processing
const report = processBatch(sampleOrders);
console.log('\\nBatch Report:', JSON.stringify(report, null, 2));

module.exports = { processOrder, processBatch, validateOrder, calculateSubtotal, calculateShipping };
"""

    with open(os.path.join(PROJECT_DIR, 'app.js'), 'w') as f:
        f.write(app_js)

    # package.json for Node.js project metadata
    package_json = {
        "name": "func-bp",
        "version": "1.0.0",
        "description": "Order processing module for e-commerce platform",
        "main": "app.js",
        "scripts": {
            "start": "node app.js",
            "test": "echo \"Error: no test specified\" && exit 1"
        },
        "keywords": ["order", "processing", "ecommerce"],
        "author": "Dev Team",
        "license": "MIT"
    }

    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # .vscode/launch.json for Node.js debugging
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "type": "node",
                "request": "launch",
                "name": "Launch app.js",
                "skipFiles": ["<node_internals>/**"],
                "program": "${workspaceFolder}/app.js"
            }
        ]
    }

    with open(os.path.join(PROJECT_DIR, '.vscode', 'launch.json'), 'w') as f:
        json.dump(launch_json, f, indent=4)

    print(f'Workspace created: {PROJECT_DIR}')
    print(f'  - app.js (defines processOrder function)')
    print(f'  - package.json')
    print(f'  - .vscode/launch.json')


def create_initial():
    """Set up initial environment: workspace files + VSCode open on Run & Debug sidebar."""
    create_workspace()

    # Open VSCode with the workspace folder
    # The Run & Debug sidebar will be visible because we set the active viewlet
    # No function breakpoints should exist at this point
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with func-bp workspace and DISPLAY=:0')


create_initial()
