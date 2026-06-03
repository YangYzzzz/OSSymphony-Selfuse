#!/usr/bin/env python3
"""
initial_setup.py — vscode_prod_042
Sets up the initial state: VSCode open with ~/projects/flask-app/ containing
app.py, requirements.txt, templates/ folder. No .vscode/launch.json exists.
"""
import os
import subprocess
import time

HOME = os.path.expanduser("~")
PROJECT_DIR = os.path.join(HOME, "projects", "flask-app")
TEMPLATES_DIR = os.path.join(PROJECT_DIR, "templates")

# 1. Create project directory structure
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# 2. Create app.py (Flask entry point)
app_py_content = '''\
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
with open(os.path.join(PROJECT_DIR, "app.py"), "w") as f:
    f.write(app_py_content)

# 3. Create requirements.txt
requirements_content = '''\
Flask==3.0.0
Werkzeug==3.0.1
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.7.0
'''
with open(os.path.join(PROJECT_DIR, "requirements.txt"), "w") as f:
    f.write(requirements_content)

# 4. Create template files
index_html = '''\
<!DOCTYPE html>
<html>
<head><title>Flask App</title></head>
<body>
    <h1>Welcome to Flask App</h1>
    <p>This is the home page.</p>
    <a href="/about">About</a>
</body>
</html>
'''
with open(os.path.join(TEMPLATES_DIR, "index.html"), "w") as f:
    f.write(index_html)

about_html = '''\
<!DOCTYPE html>
<html>
<head><title>About - Flask App</title></head>
<body>
    <h1>About</h1>
    <p>This is a Flask web application.</p>
    <a href="/">Home</a>
</body>
</html>
'''
with open(os.path.join(TEMPLATES_DIR, "about.html"), "w") as f:
    f.write(about_html)

# 5. Ensure NO .vscode/launch.json exists
vscode_dir = os.path.join(PROJECT_DIR, ".vscode")
launch_json_path = os.path.join(vscode_dir, "launch.json")
if os.path.exists(launch_json_path):
    os.remove(launch_json_path)

# 6. Launch VSCode with the project folder
env = os.environ.copy()
env["DISPLAY"] = ":0"
subprocess.Popen(
    ["code", PROJECT_DIR],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    env=env,
)
time.sleep(3)

print("SETUP COMPLETE: VSCode opened with ~/projects/flask-app/")
print(f"  - app.py: {os.path.exists(os.path.join(PROJECT_DIR, 'app.py'))}")
print(f"  - requirements.txt: {os.path.exists(os.path.join(PROJECT_DIR, 'requirements.txt'))}")
print(f"  - templates/: {os.path.isdir(TEMPLATES_DIR)}")
print(f"  - .vscode/launch.json: {os.path.exists(launch_json_path)}")
