"""
Initial Setup: Create a git repo with app.py on main branch, open VSCode
Task ID: vscode_stu_055
Domain: vscode (git operations)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_055'
PROJECT_DIR = f'{WORKDIR}/workspace'


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


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result.stdout.strip()


def create_initial():
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create app.py with realistic content (NO comment at line 1)
    app_py_content = '''from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demo purposes
tasks = []
task_id_counter = 1


@app.route('/')
def index():
    """Render the main task dashboard."""
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task to the list."""
    global task_id_counter
    title = request.form.get('title', '').strip()
    if title:
        tasks.append({
            'id': task_id_counter,
            'title': title,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'completed': False
        })
        task_id_counter += 1
    return redirect(url_for('index'))


@app.route('/complete/<int:tid>')
def complete_task(tid):
    """Mark a task as completed."""
    for task in tasks:
        if task['id'] == tid:
            task['completed'] = True
            break
    return redirect(url_for('index'))


@app.route('/delete/<int:tid>')
def delete_task(tid):
    """Delete a task from the list."""
    global tasks
    tasks = [t for t in tasks if t['id'] != tid]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_py_content)

    # Create a requirements.txt for realism
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('flask==3.0.0\ngunicorn==21.2.0\n')

    # Create a README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('# Task Manager App\n\nA simple Flask-based task management application.\n\n## Setup\n\n```bash\npip install -r requirements.txt\npython app.py\n```\n')

    # Initialize git repo
    run_cmd('git init', cwd=PROJECT_DIR)
    run_cmd('git config user.email "student@university.edu"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Student"', cwd=PROJECT_DIR)

    # Ensure we are on main branch
    run_cmd('git checkout -b main', cwd=PROJECT_DIR)

    # Stage and commit all files
    run_cmd('git add -A', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial commit: task manager app"', cwd=PROJECT_DIR)

    print(f'Git repo initialized at {PROJECT_DIR} on branch main')
    print(f'app.py created with realistic Flask content')

    # Open VSCode with the workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
