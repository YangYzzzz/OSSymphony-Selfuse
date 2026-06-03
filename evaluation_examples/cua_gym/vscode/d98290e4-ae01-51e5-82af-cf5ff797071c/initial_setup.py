"""
Initial Setup: Configure VSCode workbench layout for web development
Task ID: vscode_web_061
Domain: vscode

Creates a realistic web development project and opens VSCode with default settings.
No layout customizations are applied -- the agent must do that.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_061'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')


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


def create_project():
    """Create a realistic web development project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # index.html
    with open(os.path.join(PROJECT_DIR, 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskFlow - Project Management Dashboard</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header class="main-header">
        <nav class="navbar">
            <div class="logo">TaskFlow</div>
            <ul class="nav-links">
                <li><a href="#dashboard">Dashboard</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#team">Team</a></li>
                <li><a href="#settings">Settings</a></li>
            </ul>
        </nav>
    </header>
    <main id="app">
        <section class="dashboard-grid">
            <div class="widget" id="task-summary"></div>
            <div class="widget" id="timeline"></div>
            <div class="widget" id="team-activity"></div>
        </section>
    </main>
    <script src="js/app.js"></script>
</body>
</html>
""")

    # CSS
    css_dir = os.path.join(PROJECT_DIR, 'css')
    os.makedirs(css_dir, exist_ok=True)
    with open(os.path.join(css_dir, 'styles.css'), 'w') as f:
        f.write("""/* TaskFlow - Main Stylesheet */
:root {
    --primary-color: #3b82f6;
    --secondary-color: #10b981;
    --bg-dark: #1e293b;
    --bg-light: #f8fafc;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-light);
    color: var(--text-primary);
    line-height: 1.6;
}

.main-header {
    background-color: var(--bg-dark);
    padding: 0 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
    max-width: 1280px;
    margin: 0 auto;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    letter-spacing: -0.025em;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: #94a3b8;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.nav-links a:hover {
    color: white;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
    max-width: 1280px;
    margin: 0 auto;
}

.widget {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border-color);
    min-height: 200px;
}
""")

    # JavaScript
    js_dir = os.path.join(PROJECT_DIR, 'js')
    os.makedirs(js_dir, exist_ok=True)
    with open(os.path.join(js_dir, 'app.js'), 'w') as f:
        f.write("""// TaskFlow - Main Application
'use strict';

const API_BASE = '/api/v1';

class TaskManager {
    constructor() {
        this.tasks = [];
        this.projects = [];
        this.currentFilter = 'all';
        this.init();
    }

    async init() {
        try {
            await this.loadTasks();
            this.renderDashboard();
            this.setupEventListeners();
            console.log('TaskFlow initialized successfully');
        } catch (error) {
            console.error('Failed to initialize TaskFlow:', error);
        }
    }

    async loadTasks() {
        // Simulated task data for development
        this.tasks = [
            { id: 1, title: 'Redesign landing page', status: 'in-progress', assignee: 'Sarah Chen', priority: 'high', dueDate: '2025-04-15' },
            { id: 2, title: 'Implement OAuth2 flow', status: 'todo', assignee: 'Marcus Rivera', priority: 'high', dueDate: '2025-04-20' },
            { id: 3, title: 'Database migration script', status: 'completed', assignee: 'Aisha Patel', priority: 'medium', dueDate: '2025-04-10' },
            { id: 4, title: 'Unit tests for payment module', status: 'in-progress', assignee: 'James Liu', priority: 'medium', dueDate: '2025-04-18' },
            { id: 5, title: 'API rate limiting middleware', status: 'todo', assignee: 'Elena Kowalski', priority: 'low', dueDate: '2025-04-25' },
        ];

        this.projects = [
            { id: 'proj-001', name: 'Website Redesign', progress: 65, members: 4 },
            { id: 'proj-002', name: 'Mobile App v2', progress: 30, members: 6 },
            { id: 'proj-003', name: 'API Gateway', progress: 85, members: 3 },
        ];
    }

    renderDashboard() {
        this.renderTaskSummary();
        this.renderTimeline();
        this.renderTeamActivity();
    }

    renderTaskSummary() {
        const container = document.getElementById('task-summary');
        if (!container) return;

        const total = this.tasks.length;
        const completed = this.tasks.filter(t => t.status === 'completed').length;
        const inProgress = this.tasks.filter(t => t.status === 'in-progress').length;

        container.innerHTML = `
            <h3>Task Summary</h3>
            <div class="summary-stats">
                <div class="stat"><span class="stat-value">${total}</span><span class="stat-label">Total</span></div>
                <div class="stat"><span class="stat-value">${inProgress}</span><span class="stat-label">In Progress</span></div>
                <div class="stat"><span class="stat-value">${completed}</span><span class="stat-label">Completed</span></div>
            </div>
        `;
    }

    renderTimeline() {
        const container = document.getElementById('timeline');
        if (!container) return;
        container.innerHTML = '<h3>Project Timeline</h3><p>Timeline visualization loading...</p>';
    }

    renderTeamActivity() {
        const container = document.getElementById('team-activity');
        if (!container) return;
        container.innerHTML = '<h3>Team Activity</h3><p>Recent activity feed loading...</p>';
    }

    setupEventListeners() {
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.getAttribute('href').substring(1);
                this.navigateTo(section);
            });
        });
    }

    navigateTo(section) {
        console.log(`Navigating to: ${section}`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new TaskManager();
});
""")

    # package.json
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump({
            "name": "taskflow-dashboard",
            "version": "1.2.0",
            "description": "Project management dashboard for team collaboration",
            "main": "js/app.js",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
                "lint": "eslint . --ext .js,.html",
                "test": "vitest run"
            },
            "author": "TaskFlow Engineering Team",
            "license": "MIT",
            "devDependencies": {
                "vite": "^5.1.0",
                "eslint": "^8.56.0",
                "vitest": "^1.2.0"
            }
        }, f, indent=2)

    # README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# TaskFlow Dashboard

A project management dashboard built with vanilla JavaScript.

## Getting Started

```bash
npm install
npm run dev
```

## Project Structure

```
webapp/
  index.html       - Main entry point
  css/styles.css    - Global styles
  js/app.js         - Application logic
  package.json      - Dependencies and scripts
```

## Team

- Sarah Chen - Frontend Lead
- Marcus Rivera - Backend Engineer
- Aisha Patel - Database Architect
- James Liu - QA Engineer
- Elena Kowalski - DevOps
""")

    print(f'Project created at: {PROJECT_DIR}')


def setup_vscode_defaults():
    """Ensure VSCode settings exist with minimal defaults -- NO layout customizations."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Write clean default settings (no layout customizations)
    settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written: {SETTINGS_PATH}')


def main():
    create_project()
    setup_vscode_defaults()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
