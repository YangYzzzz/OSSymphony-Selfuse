"""
Initial Setup: Use Find and Replace with regex to add semicolons at the end of lines
Task ID: vscode_edit_037
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_037'
DESKTOP = '/home/user/Desktop'
OUTPUT = f'{DESKTOP}/statements.js'


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

    # 30-line JavaScript file with exactly 12 lines that need semicolons appended.
    # No blank lines, no comment lines (to keep line counting unambiguous).
    #
    # Line-by-line breakdown (NS = needs semicolon):
    # 01: const API_URL = 'https://api.acme.com'   NS  1
    # 02: const TIMEOUT = 3000;                    ;
    # 03: let isConnected = false;                 ;
    # 04: let currentUser = null                   NS  2
    # 05: let retryCount = 0;                      ;
    # 06: function connect(host, port) {           {
    # 07:     const socket = new Socket()          NS  3
    # 08:     socket.setTimeout(TIMEOUT);          ;
    # 09:     socket.connect(port, host);          ;
    # 10:     isConnected = true                   NS  4
    # 11:     return socket                        NS  5
    # 12: }                                        }
    # 13: function disconnect() {                  {
    # 14:     isConnected = false;                 ;
    # 15:     currentUser = null;                  ;
    # 16:     retryCount = 0                       NS  6
    # 17: }                                        }
    # 18: function authenticate(username, pwd) {   {
    # 19:     const token = btoa(username + pwd)   NS  7
    # 20:     currentUser = username;              ;
    # 21:     return token                         NS  8
    # 22: }                                        }
    # 23: function fetchData(endpoint) {           {
    # 24:     const url = API_URL + endpoint       NS  9
    # 25:     const res = fetch(url);              ;
    # 26:     return res                           NS 10
    # 27: }                                        }
    # 28: const defaultHost = 'localhost'          NS 11
    # 29: const defaultPort = 8080;               ;
    # 30: exports.connect = connect                NS 12
    #
    # Totals: 4 '{' lines + 4 '}' lines + 10 ';' lines + 12 NS lines = 30
    js_content = (
        "const API_URL = 'https://api.acme.com'\n"
        "const TIMEOUT = 3000;\n"
        "let isConnected = false;\n"
        "let currentUser = null\n"
        "let retryCount = 0;\n"
        "function connect(host, port) {\n"
        "    const socket = new Socket()\n"
        "    socket.setTimeout(TIMEOUT);\n"
        "    socket.connect(port, host);\n"
        "    isConnected = true\n"
        "    return socket\n"
        "}\n"
        "function disconnect() {\n"
        "    isConnected = false;\n"
        "    currentUser = null;\n"
        "    retryCount = 0\n"
        "}\n"
        "function authenticate(username, pwd) {\n"
        "    const token = btoa(username + pwd)\n"
        "    currentUser = username;\n"
        "    return token\n"
        "}\n"
        "function fetchData(endpoint) {\n"
        "    const url = API_URL + endpoint\n"
        "    const res = fetch(url);\n"
        "    return res\n"
        "}\n"
        "const defaultHost = 'localhost'\n"
        "const defaultPort = 8080;\n"
        "exports.connect = connect"
    )

    # Sanity check line counts before writing
    lines = js_content.split('\n')
    if lines and lines[-1] == '':
        lines = lines[:-1]

    ns_count = sum(
        1 for line in lines
        if not line.rstrip().endswith((';', '{', '}'))
    )
    assert len(lines) == 30, f'Expected 30 lines, got {len(lines)}'
    assert ns_count == 12, f'Expected 12 NS lines, got {ns_count}'

    with open(OUTPUT, 'w') as f:
        f.write(js_content)

    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines: {len(lines)}, NS lines: {ns_count}')

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
