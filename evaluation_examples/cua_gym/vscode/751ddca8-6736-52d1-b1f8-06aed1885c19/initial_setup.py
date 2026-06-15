"""
Initial Setup: Python venv creation project environment
Task ID: vscode_stu_062
Domain: vscode

Creates a realistic Python web project at ~/cs301/webapp with no virtual environment.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'cs301', 'webapp')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'static', 'css'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'static', 'js'), exist_ok=True)

    # Main application file
    app_py = '''\
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.example.com/v2"

@app.route("/")
def index():
    return render_template("index.html", title="CS301 Web Dashboard")

@app.route("/api/data")
def get_data():
    """Fetch data from external API and return processed results."""
    try:
        response = requests.get(f"{API_BASE_URL}/metrics", timeout=10)
        response.raise_for_status()
        data = response.json()
        return jsonify({"status": "ok", "metrics": data})
    except requests.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 502

@app.route("/api/submit", methods=["POST"])
def submit_data():
    payload = request.get_json()
    if not payload or "name" not in payload:
        return jsonify({"error": "Missing required field: name"}), 400
    try:
        resp = requests.post(
            f"{API_BASE_URL}/submissions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        return jsonify({"status": "submitted", "id": resp.json().get("id")})
    except requests.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 502

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
'''
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_py)

    # HTML template
    index_html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <h1>CS301 Web Application Dashboard</h1>
        <nav>
            <a href="/">Home</a>
            <a href="/api/data">API Data</a>
        </nav>
    </header>
    <main>
        <section id="metrics">
            <h2>System Metrics</h2>
            <div id="metrics-container"></div>
        </section>
        <section id="submit-form">
            <h2>Submit Entry</h2>
            <form id="entry-form">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                <label for="description">Description:</label>
                <textarea id="description" name="description" rows="4"></textarea>
                <button type="submit">Submit</button>
            </form>
        </section>
    </main>
    <script src="/static/js/main.js"></script>
</body>
</html>
'''
    with open(os.path.join(PROJECT_DIR, 'templates', 'index.html'), 'w') as f:
        f.write(index_html)

    # CSS file
    style_css = '''\
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f6f9;
    color: #333;
}
header {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 2rem;
}
header h1 { margin: 0; font-size: 1.5rem; }
nav a {
    color: #ecf0f1;
    margin-right: 1rem;
    text-decoration: none;
}
main { padding: 2rem; max-width: 960px; margin: 0 auto; }
section { margin-bottom: 2rem; }
form label { display: block; margin-top: 0.5rem; font-weight: bold; }
form input, form textarea { width: 100%; padding: 0.5rem; margin-top: 0.25rem; }
button {
    margin-top: 1rem;
    padding: 0.5rem 1.5rem;
    background-color: #2c3e50;
    color: white;
    border: none;
    cursor: pointer;
}
'''
    with open(os.path.join(PROJECT_DIR, 'static', 'css', 'style.css'), 'w') as f:
        f.write(style_css)

    # JS file
    main_js = '''\
document.addEventListener("DOMContentLoaded", function() {
    fetchMetrics();
    document.getElementById("entry-form").addEventListener("submit", handleSubmit);
});

async function fetchMetrics() {
    const container = document.getElementById("metrics-container");
    try {
        const response = await fetch("/api/data");
        const data = await response.json();
        if (data.status === "ok") {
            container.innerHTML = "<pre>" + JSON.stringify(data.metrics, null, 2) + "</pre>";
        } else {
            container.innerHTML = "<p class=\\"error\\">Failed to load metrics</p>";
        }
    } catch (err) {
        container.innerHTML = "<p class=\\"error\\">Network error: " + err.message + "</p>";
    }
}

async function handleSubmit(event) {
    event.preventDefault();
    const formData = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value
    };
    try {
        const response = await fetch("/api/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        alert(result.status === "submitted" ? "Entry submitted!" : "Error: " + result.message);
    } catch (err) {
        alert("Submission failed: " + err.message);
    }
}
'''
    with open(os.path.join(PROJECT_DIR, 'static', 'js', 'main.js'), 'w') as f:
        f.write(main_js)

    # Requirements file (no venv yet, just a hint for the project)
    requirements_txt = '''\
flask>=3.0
requests>=2.31
'''
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_txt)

    # README
    readme = '''\
# CS301 Web Application

A Flask-based web dashboard for CS301 coursework. Uses the `requests` library
to communicate with an external metrics API.

## Setup

1. Create a Python virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

## Project Structure

```
webapp/
  app.py             - Main Flask application
  requirements.txt   - Python dependencies
  templates/         - Jinja2 HTML templates
  static/
    css/             - Stylesheets
    js/              - Client-side JavaScript
```
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Make sure NO venv directory exists
    import shutil
    venv_path = os.path.join(PROJECT_DIR, 'venv')
    if os.path.exists(venv_path):
        shutil.rmtree(venv_path)

    print(f'Initial project created: {PROJECT_DIR}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
