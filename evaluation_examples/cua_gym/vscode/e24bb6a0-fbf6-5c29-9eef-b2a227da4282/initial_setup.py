"""
Initial Setup: Convert console.log string concatenation to template literals
Task ID: vscode_edit_079
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_079'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/debug.js'


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

    # A 45-line JavaScript debug utility file with 6 console.log statements
    # using string concatenation (NOT template literals)
    js_content = """\
// debug.js - Application Debug Utilities
// Provides helper functions for logging application state

const APP_NAME = "DataSync";
const VERSION = "2.3.1";

function debugUserLogin(userId, username) {
    console.log("User login event: " + userId + " (" + username + ")");
    return true;
}

function debugApiRequest(endpoint, method) {
    console.log("API request: " + method + " " + endpoint);
    const timestamp = new Date().toISOString();
    return timestamp;
}

function debugDatabaseQuery(table, rowCount) {
    console.log("DB query on table: " + table + ", returned " + rowCount + " rows");
}

function debugCacheHit(key, value) {
    console.log("Cache hit for key: " + key + ", value: " + value);
}

function debugErrorOccurred(code, message) {
    console.log("Error " + code + ": " + message);
    return false;
}

function debugSessionExpiry(sessionId, expiresAt) {
    console.log("Session " + sessionId + " expires at " + expiresAt);
}

function getAppVersion() {
    return APP_NAME + " v" + VERSION;
}

function initDebugMode(level) {
    const levels = ["info", "warn", "error", "verbose"];
    if (!levels.includes(level)) {
        throw new Error("Invalid debug level: " + level);
    }
    return level;
}

module.exports = {
    debugUserLogin,
    debugApiRequest,
    debugDatabaseQuery,
    debugCacheHit,
    debugErrorOccurred,
    debugSessionExpiry,
    getAppVersion,
    initDebugMode,
};
"""

    with open(OUTPUT, 'w') as f:
        f.write(js_content)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
