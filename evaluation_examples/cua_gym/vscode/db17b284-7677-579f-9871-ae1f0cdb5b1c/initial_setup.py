"""
Initial Setup: Configure Flask debug session in VSCode
Task ID: vscode_stu_078
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_078'
PROJECT_DIR = f'{WORKDIR}/cs301/flask-app'

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
    os.makedirs(f'{PROJECT_DIR}/templates', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/static/css', exist_ok=True)

    # --- app.py (main Flask application) ---
    app_py = '''\
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# In-memory student records
students = [
    {"id": 1, "name": "Sarah Chen", "major": "Computer Science", "gpa": 3.87},
    {"id": 2, "name": "Marcus Johnson", "major": "Data Science", "gpa": 3.62},
    {"id": 3, "name": "Priya Patel", "major": "Electrical Engineering", "gpa": 3.91},
    {"id": 4, "name": "James O'Brien", "major": "Computer Science", "gpa": 3.45},
    {"id": 5, "name": "Aisha Williams", "major": "Mathematics", "gpa": 3.78},
]


@app.route("/")
def index():
    return render_template("index.html", students=students)


@app.route("/api/students", methods=["GET"])
def get_students():
    major = request.args.get("major")
    if major:
        filtered = [s for s in students if s["major"].lower() == major.lower()]
        return jsonify(filtered)
    return jsonify(students)


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)


@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()
    if not data or "name" not in data or "major" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    new_id = max(s["id"] for s in students) + 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "major": data["major"],
        "gpa": data.get("gpa", 0.0),
    }
    students.append(new_student)
    return jsonify(new_student), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
    with open(f'{PROJECT_DIR}/app.py', 'w') as f:
        f.write(app_py)

    # --- requirements.txt ---
    requirements = '''\
Flask==3.0.2
Werkzeug==3.0.1
Jinja2==3.1.3
python-dotenv==1.0.1
'''
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements)

    # --- templates/index.html ---
    index_html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CS301 Student Portal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>CS301 Student Portal</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Major</th>
                    <th>GPA</th>
                </tr>
            </thead>
            <tbody>
                {% for student in students %}
                <tr>
                    <td>{{ student.id }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.major }}</td>
                    <td>{{ "%.2f"|format(student.gpa) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''
    with open(f'{PROJECT_DIR}/templates/index.html', 'w') as f:
        f.write(index_html)

    # --- static/css/style.css ---
    style_css = '''\
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    padding: 30px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    background-color: #3498db;
    color: white;
}

tr:hover {
    background-color: #f1f1f1;
}
'''
    with open(f'{PROJECT_DIR}/static/css/style.css', 'w') as f:
        f.write(style_css)

    # --- config.py ---
    config_py = '''\
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))
'''
    with open(f'{PROJECT_DIR}/config.py', 'w') as f:
        f.write(config_py)

    # --- .gitignore ---
    gitignore = '''\
__pycache__/
*.pyc
.env
venv/
instance/
.vscode/
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # Ensure NO .vscode/launch.json exists (task requires creating it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json_path = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)
    # Remove .vscode dir entirely if empty
    if os.path.exists(vscode_dir) and not os.listdir(vscode_dir):
        os.rmdir(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: app.py, config.py, requirements.txt, templates/index.html, static/css/style.css')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
