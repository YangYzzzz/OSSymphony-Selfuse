"""
Initial Setup: VSCode diff editor - compare two CSS file versions
Task ID: vscode_web_075
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_075'
PROJECT_DIR = f'{WORKDIR}/projects/website'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # styles-old.css: Previous version with some useful styles that are missing in new
    old_css = """\
/* ===========================
   Website Stylesheet - v2.3
   Last updated: 2025-08-10
   Author: Elena Kowalski
   =========================== */

/* --- Reset & Base --- */
*, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #2d3748;
    background-color: #f7fafc;
}

/* --- Typography --- */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 0.75em;
    color: #1a202c;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }

p {
    margin-bottom: 1rem;
    max-width: 65ch;
}

/* --- Links --- */
a {
    color: #3182ce;
    text-decoration: none;
    transition: color 0.2s ease;
}

a:hover {
    color: #2c5282;
    text-decoration: underline;
}

/* --- Navigation Bar --- */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    background-color: #1a202c;
    color: #fff;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
}

.navbar-links {
    display: flex;
    gap: 1.5rem;
    list-style: none;
}

.navbar-links a {
    color: #e2e8f0;
    font-weight: 500;
    padding: 0.5rem 0;
}

.navbar-links a:hover {
    color: #63b3ed;
    text-decoration: none;
}

/* --- Hero Section --- */
.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    padding: 4rem 2rem;
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
}

.hero h1 {
    font-size: 3.5rem;
    color: #fff;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.25rem;
    max-width: 600px;
    opacity: 0.9;
}

/* --- Buttons --- */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.375rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}

.btn-primary {
    background-color: #3182ce;
    color: #fff;
}

.btn-primary:hover {
    background-color: #2c5282;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(49, 130, 206, 0.4);
}

.btn-secondary {
    background-color: #e2e8f0;
    color: #2d3748;
}

.btn-secondary:hover {
    background-color: #cbd5e0;
}

/* --- Card Component --- */
.card {
    background: #fff;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.card-body {
    color: #4a5568;
    font-size: 0.95rem;
}

/* --- Grid Layout --- */
.grid {
    display: grid;
    gap: 1.5rem;
    padding: 2rem;
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }

/* --- Footer --- */
.footer {
    background-color: #1a202c;
    color: #a0aec0;
    padding: 3rem 2rem;
    text-align: center;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
    list-style: none;
}

.footer-links a {
    color: #a0aec0;
}

.footer-links a:hover {
    color: #fff;
}

/* --- Utility Classes --- */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }
.mt-8 { margin-top: 2rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-8 { margin-bottom: 2rem; }

.px-4 { padding-left: 1rem; padding-right: 1rem; }
.py-4 { padding-top: 1rem; padding-bottom: 1rem; }

.hidden { display: none; }
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}

/* --- Tooltip --- */
.tooltip {
    position: relative;
    cursor: help;
}

.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.5rem 0.75rem;
    background: #2d3748;
    color: #fff;
    font-size: 0.8rem;
    border-radius: 0.25rem;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
}

.tooltip:hover::after {
    opacity: 1;
}

/* --- Badge --- */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.badge-success {
    background-color: #c6f6d5;
    color: #276749;
}

.badge-warning {
    background-color: #fefcbf;
    color: #975a16;
}

.badge-danger {
    background-color: #fed7d7;
    color: #9b2c2c;
}

/* --- Responsive --- */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
    }
    .navbar-links {
        flex-direction: column;
        align-items: center;
    }
    .grid-2, .grid-3, .grid-4 {
        grid-template-columns: 1fr;
    }
    .hero h1 {
        font-size: 2.5rem;
    }
}
"""

    # styles-new.css: Current version - missing tooltip, badge, and some utility classes
    new_css = """\
/* ===========================
   Website Stylesheet - v3.0
   Last updated: 2025-11-22
   Author: Elena Kowalski
   =========================== */

/* --- Reset & Base --- */
*, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #2d3748;
    background-color: #f7fafc;
}

/* --- Typography --- */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 0.75em;
    color: #1a202c;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }

p {
    margin-bottom: 1rem;
    max-width: 65ch;
}

/* --- Links --- */
a {
    color: #4299e1;
    text-decoration: none;
    transition: color 0.2s ease, text-decoration 0.2s ease;
}

a:hover {
    color: #2b6cb0;
    text-decoration: underline;
}

/* --- Navigation Bar --- */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    background-color: #1a202c;
    color: #fff;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
}

.navbar-links {
    display: flex;
    gap: 1.5rem;
    list-style: none;
}

.navbar-links a {
    color: #e2e8f0;
    font-weight: 500;
    padding: 0.5rem 0;
}

.navbar-links a:hover {
    color: #63b3ed;
    text-decoration: none;
}

/* --- Hero Section --- */
.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    padding: 4rem 2rem;
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
}

.hero h1 {
    font-size: 3.5rem;
    color: #fff;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}

.hero p {
    font-size: 1.25rem;
    max-width: 600px;
    opacity: 0.9;
}

/* --- Buttons --- */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}

.btn-primary {
    background-color: #4299e1;
    color: #fff;
}

.btn-primary:hover {
    background-color: #3182ce;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(66, 153, 225, 0.4);
}

.btn-secondary {
    background-color: #edf2f7;
    color: #2d3748;
}

.btn-secondary:hover {
    background-color: #e2e8f0;
}

.btn-outline {
    background-color: transparent;
    border: 2px solid #4299e1;
    color: #4299e1;
}

.btn-outline:hover {
    background-color: #4299e1;
    color: #fff;
}

/* --- Card Component --- */
.card {
    background: #fff;
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.card-body {
    color: #4a5568;
    font-size: 0.95rem;
}

.card-footer {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
}

/* --- Grid Layout --- */
.grid {
    display: grid;
    gap: 1.5rem;
    padding: 2rem;
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }

/* --- Footer --- */
.footer {
    background-color: #1a202c;
    color: #a0aec0;
    padding: 3rem 2rem;
    text-align: center;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
    list-style: none;
}

.footer-links a {
    color: #a0aec0;
}

.footer-links a:hover {
    color: #fff;
}

/* --- Utility Classes --- */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }
.mt-8 { margin-top: 2rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-8 { margin-bottom: 2rem; }

.px-4 { padding-left: 1rem; padding-right: 1rem; }
.py-4 { padding-top: 1rem; padding-bottom: 1rem; }

/* --- Responsive --- */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
    }
    .navbar-links {
        flex-direction: column;
        align-items: center;
    }
    .grid-2, .grid-3, .grid-4 {
        grid-template-columns: 1fr;
    }
    .hero h1 {
        font-size: 2.5rem;
    }
}
"""

    with open(f'{PROJECT_DIR}/styles-old.css', 'w') as f:
        f.write(old_css)
    print(f'Created: {PROJECT_DIR}/styles-old.css')

    with open(f'{PROJECT_DIR}/styles-new.css', 'w') as f:
        f.write(new_css)
    print(f'Created: {PROJECT_DIR}/styles-new.css')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
