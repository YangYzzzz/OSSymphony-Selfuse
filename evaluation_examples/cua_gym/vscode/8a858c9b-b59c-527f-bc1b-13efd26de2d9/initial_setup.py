"""
Initial Setup: Create a CSS file with kebab-case class selectors for VSCode regex replacement task.
Task ID: vscode_edit_090
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_090'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/refactor.css'


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

    css_content = """\
/* =============================================================
   refactor.css — Application Stylesheet (v2.1)
   Project: WebApp Dashboard
   ============================================================= */

/* ---- Layout: Main Container ---- */
.main-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f4f6f9;
    padding: 0 16px;
    box-sizing: border-box;
}

/* ---- Navigation Bar ---- */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    background-color: #1a1a2e;
    color: #ffffff;
    padding: 0 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

/* ---- Sidebar Panel ---- */
.side-panel {
    width: 240px;
    min-height: calc(100vh - 64px);
    background-color: #16213e;
    color: #e0e0e0;
    padding: 16px 0;
    border-right: 1px solid #0f3460;
}

/* ---- Main Content Area ---- */
.content-area {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    background-color: #ffffff;
    border-radius: 8px;
    margin: 16px;
}

/* ---- Footer Section ---- */
.footer-section {
    background-color: #1a1a2e;
    color: #aaaaaa;
    text-align: center;
    padding: 12px 0;
    font-size: 0.85rem;
    border-top: 1px solid #0f3460;
}

/* ---- Primary Button ---- */
.btn-primary {
    display: inline-block;
    padding: 10px 20px;
    background-color: #e94560;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 600;
    transition: background-color 0.2s ease;
}

/* ---- Card Header ---- */
.card-header {
    background-color: #0f3460;
    color: #ffffff;
    padding: 12px 16px;
    font-size: 1rem;
    font-weight: 700;
    border-radius: 6px 6px 0 0;
    letter-spacing: 0.05em;
}

/* ---- List Item ---- */
.list-item {
    display: flex;
    align-items: center;
    padding: 10px 16px;
    border-bottom: 1px solid #e8ecf0;
    font-size: 0.9rem;
    color: #333333;
    transition: background-color 0.15s ease;
}

/* ---- Form Group ---- */
.form-group {
    margin-bottom: 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

/* ---- Modal Body ---- */
.modal-body {
    padding: 20px 24px;
    background-color: #ffffff;
    border-radius: 0 0 8px 8px;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #444444;
    max-height: 60vh;
    overflow-y: auto;
}
"""

    with open(OUTPUT, 'w') as f:
        f.write(css_content)

    print(f'Initial CSS file created: {OUTPUT}')
    line_count = css_content.count('\n')
    print(f'Line count: {line_count}')

    # GUI-ready startup: open the CSS file in VSCode
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
