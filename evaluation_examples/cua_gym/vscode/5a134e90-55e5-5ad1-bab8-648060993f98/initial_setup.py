"""
Initial Setup: Configure a complete Tailwind CSS development setup in ~/project
Task ID: vscode_wf_053
Domain: vs_code

Creates a web project with npm packages simulated (tailwindcss, postcss, autoprefixer)
but NO Tailwind config files and NO VSCode workspace settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
SRC_DIR = os.path.join(PROJECT, 'src')


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
    os.makedirs(SRC_DIR, exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "aurora-landing-page",
        "version": "1.0.0",
        "description": "Aurora SaaS landing page with Tailwind CSS",
        "main": "src/index.html",
        "scripts": {
            "start": "live-server src/",
            "dev": "npx tailwindcss -i ./src/styles.css -o ./dist/output.css --watch"
        },
        "keywords": ["tailwind", "landing-page", "sass"],
        "author": "Elena Rodriguez",
        "license": "MIT",
        "devDependencies": {
            "autoprefixer": "^10.4.17",
            "postcss": "^8.4.35",
            "tailwindcss": "^3.4.1"
        },
        "dependencies": {
            "live-server": "^1.2.2"
        }
    }
    with open(os.path.join(PROJECT, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- src/index.html ---
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aurora - Smart Project Management</title>
    <link href="../dist/output.css" rel="stylesheet">
</head>
<body>
    <header>
        <nav>
            <div>
                <a href="/">Aurora</a>
                <ul>
                    <li><a href="#features">Features</a></li>
                    <li><a href="#pricing">Pricing</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main>
        <section id="hero">
            <h1>Manage Projects with Confidence</h1>
            <p>Aurora brings your team together with intuitive project tracking,
               real-time collaboration, and powerful analytics.</p>
            <div>
                <a href="#signup">Get Started Free</a>
                <a href="#demo">Watch Demo</a>
            </div>
        </section>

        <section id="features">
            <h2>Why Teams Choose Aurora</h2>
            <div>
                <div>
                    <h3>Real-Time Dashboards</h3>
                    <p>Track progress across all projects with customizable widgets
                       and live status updates.</p>
                </div>
                <div>
                    <h3>Smart Scheduling</h3>
                    <p>AI-powered timeline suggestions that adapt to your team's
                       velocity and availability.</p>
                </div>
                <div>
                    <h3>Integrated Chat</h3>
                    <p>Keep discussions contextual with threaded conversations
                       attached to tasks and milestones.</p>
                </div>
            </div>
        </section>

        <section id="pricing">
            <h2>Simple, Transparent Pricing</h2>
            <div>
                <div>
                    <h3>Starter</h3>
                    <p>$12/user/month</p>
                    <ul>
                        <li>Up to 10 projects</li>
                        <li>Basic analytics</li>
                        <li>Email support</li>
                    </ul>
                </div>
                <div>
                    <h3>Professional</h3>
                    <p>$29/user/month</p>
                    <ul>
                        <li>Unlimited projects</li>
                        <li>Advanced analytics</li>
                        <li>Priority support</li>
                        <li>Custom integrations</li>
                    </ul>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Aurora Technologies Inc. All rights reserved.</p>
    </footer>
</body>
</html>
'''
    with open(os.path.join(SRC_DIR, 'index.html'), 'w') as f:
        f.write(index_html)

    # --- src/styles.css (basic, no Tailwind directives yet) ---
    styles_css = '''/* Aurora Landing Page Styles */
/* TODO: Add Tailwind CSS directives and configure build pipeline */

body {
    font-family: system-ui, -apple-system, sans-serif;
    margin: 0;
    padding: 0;
    color: #1a1a2e;
    background-color: #ffffff;
}

header nav {
    display: flex;
    justify-content: space-between;
    padding: 1rem 2rem;
    background-color: #f8f9fa;
}

header nav ul {
    list-style: none;
    display: flex;
    gap: 1.5rem;
}

header nav a {
    text-decoration: none;
    color: #333;
}

#hero {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

#hero h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

#features {
    padding: 3rem 2rem;
}

#pricing {
    padding: 3rem 2rem;
    background-color: #f8f9fa;
}

footer {
    text-align: center;
    padding: 2rem;
    background-color: #1a1a2e;
    color: #ccc;
}
'''
    with open(os.path.join(SRC_DIR, 'styles.css'), 'w') as f:
        f.write(styles_css)

    # --- src/app.js (simple JS for the landing page) ---
    app_js = '''// Aurora Landing Page - Interactive Features
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    console.log('Aurora landing page initialized');
});
'''
    with open(os.path.join(SRC_DIR, 'app.js'), 'w') as f:
        f.write(app_js)

    # --- Simulate node_modules with marker files ---
    # Create minimal node_modules structure to indicate packages are installed
    modules = {
        'tailwindcss': {'version': '3.4.1', 'description': 'A utility-first CSS framework'},
        'postcss': {'version': '8.4.35', 'description': 'Tool for transforming CSS with JS plugins'},
        'autoprefixer': {'version': '10.4.17', 'description': 'Parse CSS and add vendor prefixes'},
    }
    for mod_name, info in modules.items():
        mod_dir = os.path.join(PROJECT, 'node_modules', mod_name)
        os.makedirs(mod_dir, exist_ok=True)
        pkg = {
            "name": mod_name,
            "version": info['version'],
            "description": info['description'],
            "main": "index.js"
        }
        with open(os.path.join(mod_dir, 'package.json'), 'w') as f:
            json.dump(pkg, f, indent=2)
        with open(os.path.join(mod_dir, 'index.js'), 'w') as f:
            f.write(f'// {mod_name} v{info["version"]}\nmodule.exports = {{}};\n')

    # Create dist directory for output
    os.makedirs(os.path.join(PROJECT, 'dist'), exist_ok=True)

    # --- NO tailwind.config.js ---
    # --- NO postcss.config.js ---
    # --- NO .vscode/ directory ---

    print(f'Initial project created at: {PROJECT}')
    print(f'Files: package.json, src/index.html, src/styles.css, src/app.js')
    print(f'node_modules: tailwindcss, postcss, autoprefixer (simulated)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
