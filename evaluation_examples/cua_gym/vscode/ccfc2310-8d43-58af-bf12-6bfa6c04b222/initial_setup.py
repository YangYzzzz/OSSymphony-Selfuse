"""
Initial Setup: Enable bracket pair colorization in VSCode
Task ID: vscode_code_047
Domain: vs_code

Creates:
  - /home/user/project/nested.js  with deeply nested callbacks
  - ~/.config/Code/User/settings.json with bracket pair colorization explicitly DISABLED
Then opens VSCode with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_047'
PROJECT_DIR = f'{WORKDIR}/project'
NESTED_JS = f'{PROJECT_DIR}/nested.js'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # --- Create project directory and nested.js ---
    os.makedirs(PROJECT_DIR, exist_ok=True)

    nested_js_content = """\
// nested.js — example with deeply nested callbacks (hard to read without bracket colorization)

function fetchUserData(userId, callback) {
    getDatabase(function(db) {
        db.query('SELECT * FROM users WHERE id = ?', [userId], function(err, rows) {
            if (err) {
                handleError(err, function(errInfo) {
                    logError(errInfo, function(logResult) {
                        if (logResult.success) {
                            callback(null, {
                                error: true,
                                message: errInfo.message,
                                logged: true
                            });
                        } else {
                            retryLog(errInfo, 3, function(retryResult) {
                                callback(null, {
                                    error: true,
                                    message: errInfo.message,
                                    logged: false,
                                    retried: retryResult.attempts
                                });
                            });
                        }
                    });
                });
            } else {
                rows.forEach(function(row) {
                    processRow(row, function(processedData) {
                        validateData(processedData, function(isValid) {
                            if (isValid) {
                                transformData(processedData, function(finalData) {
                                    saveToCache(userId, finalData, function(cacheResult) {
                                        if (cacheResult.hit) {
                                            callback(null, finalData);
                                        } else {
                                            fallbackStorage(finalData, function(stored) {
                                                callback(null, {
                                                    data: finalData,
                                                    cached: false,
                                                    stored: stored
                                                });
                                            });
                                        }
                                    });
                                });
                            } else {
                                sanitizeData(processedData, function(cleanData) {
                                    callback(null, {
                                        data: cleanData,
                                        sanitized: true
                                    });
                                });
                            }
                        });
                    });
                });
            }
        });
    });
}

function processOrderPipeline(orderId, options, done) {
    loadOrder(orderId, function(order) {
        checkInventory(order.items, function(inventory) {
            if (inventory.allAvailable) {
                reserveItems(order.items, function(reservation) {
                    chargePayment(order.payment, reservation.total, function(payResult) {
                        if (payResult.success) {
                            scheduleShipping(order.address, reservation, function(shipInfo) {
                                sendConfirmation(order.email, shipInfo, function(emailSent) {
                                    done(null, {
                                        orderId: orderId,
                                        reservationId: reservation.id,
                                        paymentId: payResult.transactionId,
                                        shipmentId: shipInfo.trackingNumber,
                                        emailSent: emailSent
                                    });
                                });
                            });
                        } else {
                            releaseReservation(reservation.id, function(released) {
                                done(new Error('Payment failed'), {
                                    orderId: orderId,
                                    released: released
                                });
                            });
                        }
                    });
                });
            } else {
                notifyBackorder(order.email, inventory.missingItems, function(notified) {
                    done(null, {
                        orderId: orderId,
                        status: 'backorder',
                        missingItems: inventory.missingItems,
                        notified: notified
                    });
                });
            }
        });
    });
}

module.exports = { fetchUserData, processOrderPipeline };
"""

    with open(NESTED_JS, 'w') as f:
        f.write(nested_js_content)
    print(f'Created: {NESTED_JS}')

    # --- Configure VSCode settings: explicitly disable bracket pair colorization ---
    # This ensures the initial state is clearly "not done" — agent must enable it
    update_settings({
        "editor.bracketPairColorization.enabled": False,
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.wordWrap": "off",
        "files.autoSave": "afterDelay"
    })
    print(f'VSCode settings configured: {SETTINGS_PATH}')

    # --- GUI-ready startup: open VSCode with the project folder ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
