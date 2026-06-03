"""
Initial Setup: Configure Live Server extension settings in VSCode
Task ID: vscode_ext_022
Domain: vs_code

Sets up VSCode with the Live Server extension installed but WITHOUT the
target settings (port 5500 and NoBrowser=false). The agent must configure
these settings via the VSCode Settings UI.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_022'

# VSCode config paths (on the VM)
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')

# Workspace folder for VSCode to open
WORKSPACE_DIR = os.path.join(HOME, 'live_server_project')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def load_settings():
    """Load existing VSCode settings, or return empty dict."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        import re
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def setup_initial():
    """Create initial state: Live Server installed, but NOT configured with target settings."""

    # 1. Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # 2. Write initial settings WITHOUT target Live Server values
    #    (if any liveServer settings exist, remove port=5500 and NoBrowser=false)
    settings = load_settings()

    # Remove any accidental pre-existing target settings so initial state is clean
    if 'liveServer.settings.port' in settings:
        del settings['liveServer.settings.port']
    if 'liveServer.settings.NoBrowser' in settings:
        del settings['liveServer.settings.NoBrowser']

    # Add some other settings to make it a realistic settings file
    settings.setdefault('editor.fontSize', 14)
    settings.setdefault('editor.tabSize', 4)
    settings.setdefault('editor.wordWrap', 'on')
    settings.setdefault('workbench.colorTheme', 'Default Dark Modern')
    settings.setdefault('files.autoSave', 'afterDelay')

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Settings written to: {SETTINGS_PATH}')
    print(f'Confirmed: liveServer.settings.port NOT set')
    print(f'Confirmed: liveServer.settings.NoBrowser NOT set')

    # 3. Create a realistic web project workspace for the agent to work in
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Create index.html
    index_html = os.path.join(WORKSPACE_DIR, 'index.html')
    with open(index_html, 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web Project</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>My Web Project</h1>
        <nav>
            <a href="index.html">Home</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
        </nav>
    </header>
    <main>
        <section class="hero">
            <h2>Welcome to My Project</h2>
            <p>This is a simple web project for development with Live Server.</p>
            <button onclick="showMessage()">Click Me</button>
        </section>
        <section class="features">
            <div class="feature">
                <h3>Feature One</h3>
                <p>Automatic browser refresh on file save.</p>
            </div>
            <div class="feature">
                <h3>Feature Two</h3>
                <p>Local development server with hot reload.</p>
            </div>
        </section>
    </main>
    <footer>
        <p>&copy; 2025 My Web Project</p>
    </footer>
    <script src="app.js"></script>
</body>
</html>
""")

    # Create styles.css
    styles_css = os.path.join(WORKSPACE_DIR, 'styles.css')
    with open(styles_css, 'w') as f:
        f.write("""* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

nav a {
    color: white;
    text-decoration: none;
    margin-left: 1rem;
    font-size: 0.95rem;
}

nav a:hover {
    text-decoration: underline;
}

.hero {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, #3498db, #2ecc71);
    color: white;
}

.features {
    display: flex;
    gap: 1.5rem;
    padding: 2rem;
    max-width: 900px;
    margin: 0 auto;
}

.feature {
    flex: 1;
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

footer {
    text-align: center;
    padding: 1rem;
    background-color: #2c3e50;
    color: #aaa;
    font-size: 0.85rem;
}
""")

    # Create app.js
    app_js = os.path.join(WORKSPACE_DIR, 'app.js')
    with open(app_js, 'w') as f:
        f.write("""// Main application script

function showMessage() {
    alert('Hello from My Web Project!');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded successfully.');

    // Animate feature cards on scroll
    const features = document.querySelectorAll('.feature');
    features.forEach((feature, index) => {
        feature.style.opacity = '0';
        feature.style.transform = 'translateY(20px)';
        setTimeout(() => {
            feature.style.transition = 'all 0.4s ease';
            feature.style.opacity = '1';
            feature.style.transform = 'translateY(0)';
        }, index * 150);
    });
});
""")

    print(f'Workspace created at: {WORKSPACE_DIR}')

    # 4. Install Live Server extension if not already installed
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True
        )
        if 'ritwickdey.liveserver' not in result.stdout.lower():
            subprocess.run(
                ['code', '--install-extension', 'ritwickdey.liveserver'],
                capture_output=True, text=True
            )
            print('Live Server extension installed.')
        else:
            print('Live Server extension already installed.')
    except Exception as e:
        print(f'Note: Could not verify extension via CLI: {e}')

    # 5. Launch VSCode with the workspace (GUI-ready startup)
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print(f'GUI_READY: VSCode launched with {WORKSPACE_DIR} on DISPLAY=:0')


setup_initial()
