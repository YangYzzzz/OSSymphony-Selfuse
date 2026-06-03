"""
Initial Setup: Create undocumented JS utility file and open in VSCode
Task ID: vscode_gf3_018
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_018'
PROJECT_DIR = f'{WORKDIR}/projects'
LIB_DIR = f'{PROJECT_DIR}/lib'
OUTPUT = f'{LIB_DIR}/utils.js'


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
    os.makedirs(LIB_DIR, exist_ok=True)

    # Create package.json for a realistic project
    package_json = '''{
  "name": "ecommerce-utils",
  "version": "2.1.0",
  "description": "Utility library for the StoreFront e-commerce platform",
  "main": "lib/utils.js",
  "author": "Elena Rodriguez",
  "license": "MIT"
}
'''
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(package_json)

    # Create the main utils.js file with undocumented calculateDiscount function
    utils_js = """'use strict';

const TAX_RATES = {
    US: 0.0825,
    CA: 0.13,
    UK: 0.20,
    DE: 0.19,
    JP: 0.10,
};

/**
 * Formats a monetary value to two decimal places with currency symbol.
 * @param {number} amount - The raw monetary amount.
 * @param {string} [currency='USD'] - ISO 4217 currency code.
 * @returns {string} Formatted currency string, e.g. "$12.50".
 */
function formatCurrency(amount, currency = 'USD') {
    const symbols = { USD: '$', EUR: '\\u20ac', GBP: '\\u00a3', CAD: 'C$', JPY: '\\u00a5' };
    const symbol = symbols[currency] || currency + ' ';
    return `${symbol}${amount.toFixed(2)}`;
}

function calculateDiscount(price, percentage, maxDiscount) {
    if (typeof price !== 'number' || typeof percentage !== 'number') {
        throw new TypeError('Price and percentage must be numbers');
    }
    if (price < 0 || percentage < 0 || percentage > 100) {
        throw new RangeError('Price must be non-negative and percentage must be between 0 and 100');
    }
    let discount = price * (percentage / 100);
    if (typeof maxDiscount === 'number' && maxDiscount >= 0) {
        discount = Math.min(discount, maxDiscount);
    }
    return Math.round((price - discount) * 100) / 100;
}

/**
 * Calculates the total price including applicable tax.
 * @param {number} subtotal - Pre-tax subtotal amount.
 * @param {string} region - Two-letter region code (e.g. 'US', 'UK').
 * @returns {number} Total amount including tax, rounded to two decimals.
 */
function calculateTax(subtotal, region) {
    const rate = TAX_RATES[region] || 0;
    return Math.round(subtotal * (1 + rate) * 100) / 100;
}

/**
 * Validates an email address format using a basic regex pattern.
 * @param {string} email - The email address string to validate.
 * @returns {boolean} True if the email matches a valid pattern.
 */
function isValidEmail(email) {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
}

/**
 * Generates a random alphanumeric order reference ID.
 * @param {number} [length=8] - Desired length of the generated ID.
 * @returns {string} Random order reference string.
 */
function generateOrderId(length = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

module.exports = {
    formatCurrency,
    calculateDiscount,
    calculateTax,
    isValidEmail,
    generateOrderId,
};
"""
    with open(OUTPUT, 'w') as f:
        f.write(utils_js)

    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
