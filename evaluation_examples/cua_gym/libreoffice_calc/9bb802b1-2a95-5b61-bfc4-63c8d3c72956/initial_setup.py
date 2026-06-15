"""
Initial Setup: Configure VSCode for web development workflow
Task ID: osworld_multi_apps_code_vscode_config_006
Domain: vs-code (multi-app with Chrome)

Sets up the portfolio project folder with HTML/CSS/JS files and opens
VSCode WITHOUT any web dev extensions installed (pre-task state).
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_vscode_config_006'
PROJECT_DIR = f'{WORKDIR}/projects/portfolio'

# VSCode config paths
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_project_files():
    """Create the portfolio project with realistic web dev files."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create index.html - a realistic personal portfolio page
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alex Rivera - Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="site-header">
        <nav class="navbar">
            <div class="logo">Alex Rivera</div>
            <ul class="nav-links">
                <li><a href="#about">About</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="hero" class="hero-section">
            <div class="hero-content">
                <h1>Hi, I'm Alex Rivera</h1>
                <p class="tagline">Full-Stack Developer | Open Source Enthusiast</p>
                <a href="#projects" class="btn btn-primary">View My Work</a>
            </div>
        </section>

        <section id="about" class="about-section">
            <div class="container">
                <h2>About Me</h2>
                <p>I'm a passionate developer with 4 years of experience building web applications.
                   I specialize in React, Node.js, and Python backends. I enjoy turning complex
                   problems into elegant solutions.</p>
            </div>
        </section>

        <section id="projects" class="projects-section">
            <div class="container">
                <h2>Featured Projects</h2>
                <div class="project-grid">
                    <div class="project-card">
                        <h3>TaskFlow</h3>
                        <p>A collaborative project management tool built with React and Express.js.
                           Features real-time updates using WebSockets.</p>
                        <div class="tech-tags">
                            <span class="tag">React</span>
                            <span class="tag">Node.js</span>
                            <span class="tag">MongoDB</span>
                        </div>
                    </div>
                    <div class="project-card">
                        <h3>WeatherDash</h3>
                        <p>A beautiful weather dashboard that shows 7-day forecasts using the
                           OpenWeatherMap API with interactive charts.</p>
                        <div class="tech-tags">
                            <span class="tag">JavaScript</span>
                            <span class="tag">Chart.js</span>
                            <span class="tag">REST API</span>
                        </div>
                    </div>
                    <div class="project-card">
                        <h3>CodeSnap</h3>
                        <p>A VS Code extension that generates beautiful code screenshots for
                           sharing on social media. 2,000+ installs.</p>
                        <div class="tech-tags">
                            <span class="tag">TypeScript</span>
                            <span class="tag">VS Code API</span>
                            <span class="tag">HTML Canvas</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="skills" class="skills-section">
            <div class="container">
                <h2>Skills</h2>
                <div class="skills-grid">
                    <div class="skill-category">
                        <h3>Frontend</h3>
                        <ul>
                            <li>React / Next.js</li>
                            <li>TypeScript</li>
                            <li>HTML5 / CSS3</li>
                            <li>Tailwind CSS</li>
                        </ul>
                    </div>
                    <div class="skill-category">
                        <h3>Backend</h3>
                        <ul>
                            <li>Node.js / Express</li>
                            <li>Python / FastAPI</li>
                            <li>PostgreSQL</li>
                            <li>Redis</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <section id="contact" class="contact-section">
            <div class="container">
                <h2>Get In Touch</h2>
                <p>I'm always open to new opportunities and collaborations.</p>
                <a href="mailto:alex.rivera@example.com" class="btn btn-secondary">Send Email</a>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <p>&copy; 2025 Alex Rivera. All rights reserved.</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
"""

    # Create style.css - realistic portfolio styles (using 4-space indentation intentionally,
    # matching "pre-task" state before agent configures 2-space indentation setting)
    style_css = """/* Portfolio Styles - Alex Rivera */

:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --text-color: #1f2937;
    --light-bg: #f9fafb;
    --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: var(--text-color);
    line-height: 1.6;
}

/* Navigation */
.site-header {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    z-index: 1000;
}

.navbar {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 2rem;
}

.nav-links a {
    text-decoration: none;
    color: var(--text-color);
    font-weight: 500;
    transition: color 0.2s;
}

.nav-links a:hover {
    color: var(--primary-color);
}

/* Hero Section */
.hero-section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    padding-top: 80px;
}

.hero-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    text-align: center;
}

.hero-content h1 {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: var(--text-color);
}

.tagline {
    font-size: 1.25rem;
    color: #6b7280;
    margin-bottom: 2rem;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.875rem 2rem;
    border-radius: 0.5rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--secondary-color);
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}

.btn-secondary:hover {
    background: var(--primary-color);
    color: white;
}

/* Sections */
section {
    padding: 5rem 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

section h2 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-align: center;
}

/* About */
.about-section {
    background: white;
}

.about-section p {
    max-width: 700px;
    margin: 0 auto;
    font-size: 1.1rem;
    text-align: center;
    color: #4b5563;
}

/* Projects */
.projects-section {
    background: var(--light-bg);
}

.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.project-card {
    background: white;
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
    transition: transform 0.2s;
}

.project-card:hover {
    transform: translateY(-4px);
}

.project-card h3 {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    color: var(--primary-color);
}

.tech-tags {
    margin-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.tag {
    background: #dbeafe;
    color: var(--primary-color);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}

/* Skills */
.skills-section {
    background: white;
}

.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

.skill-category h3 {
    font-size: 1.125rem;
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.skill-category ul {
    list-style: none;
}

.skill-category li {
    padding: 0.375rem 0;
    color: #4b5563;
    border-bottom: 1px solid #f3f4f6;
}

/* Contact */
.contact-section {
    background: var(--light-bg);
    text-align: center;
}

.contact-section p {
    color: #6b7280;
    margin-bottom: 2rem;
    font-size: 1.1rem;
}

/* Footer */
.site-footer {
    background: #111827;
    color: #9ca3af;
    text-align: center;
    padding: 1.5rem;
    font-size: 0.875rem;
}
"""

    # Create script.js - realistic portfolio JS
    script_js = """// Portfolio - Alex Rivera
// Main JavaScript file

'use strict';

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Active navigation highlight on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

function updateActiveNav() {
    const scrollPos = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');

        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

window.addEventListener('scroll', updateActiveNav);

// Animate project cards on scroll (Intersection Observer)
const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.project-card, .skill-category').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
});

// Add fade-in class styles dynamically
const style = document.createElement('style');
style.textContent = '.fade-in { opacity: 1 !important; transform: translateY(0) !important; }';
document.head.appendChild(style);

// Navbar background on scroll
const header = document.querySelector('.site-header');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.12)';
    } else {
        header.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.05)';
    }
});

console.log('Portfolio loaded successfully.');
"""

    with open(os.path.join(PROJECT_DIR, 'index.html'), 'w') as f:
        f.write(index_html)
    print(f'Created: {PROJECT_DIR}/index.html')

    with open(os.path.join(PROJECT_DIR, 'style.css'), 'w') as f:
        f.write(style_css)
    print(f'Created: {PROJECT_DIR}/style.css')

    with open(os.path.join(PROJECT_DIR, 'script.js'), 'w') as f:
        f.write(script_js)
    print(f'Created: {PROJECT_DIR}/script.js')


def ensure_no_web_dev_extensions():
    """
    Remove any pre-installed web dev extensions that shouldn't exist in initial state.
    The task requires the agent to install these extensions, so they must be absent initially.
    """
    extensions_to_remove = [
        'ritwickdey.liveserver',
        'ecmel.vscode-html-css',
        'formulahendry.auto-rename-tag',
    ]
    for ext_id in extensions_to_remove:
        result = subprocess.run(
            ['code', '--uninstall-extension', ext_id],
            capture_output=True,
            text=True
        )
        # Ignore errors if the extension isn't installed
        if result.returncode == 0:
            print(f'Removed extension: {ext_id}')


def clear_workspace_settings():
    """
    Ensure there are no existing workspace settings for the portfolio project
    that would pre-configure indentation (the agent needs to add these).
    """
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    settings_file = os.path.join(vscode_dir, 'settings.json')
    if os.path.exists(settings_file):
        os.remove(settings_file)
        print(f'Removed pre-existing workspace settings: {settings_file}')
    # Optionally remove the .vscode dir if empty
    if os.path.exists(vscode_dir) and not os.listdir(vscode_dir):
        os.rmdir(vscode_dir)


def setup_minimal_vscode_settings():
    """Set up minimal global VSCode settings (no indentation pre-configured)."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            import re
            content = f.read()
            # Strip JSONC comments
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any pre-existing language-specific indentation settings
    # so the agent must configure them
    for key in list(settings.keys()):
        if '[html]' in key or '[css]' in key or 'tabSize' in key:
            del settings[key]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Cleaned up global VSCode settings: {SETTINGS_PATH}')


def create_initial():
    """Main setup function."""
    print(f'Setting up initial state for task: {TASK_ID}')

    # 1. Create project files
    create_project_files()

    # 2. Remove any web dev extensions (initial state should have none)
    ensure_no_web_dev_extensions()

    # 3. Clear workspace settings
    clear_workspace_settings()

    # 4. Clean up global indentation settings
    setup_minimal_vscode_settings()

    # 5. Launch VSCode with the portfolio folder (GUI-ready)
    print('Launching VSCode with portfolio project...')
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)

    print('GUI_READY: VSCode launched with portfolio project at DISPLAY=:0')
    print(f'Initial state complete. Project at: {PROJECT_DIR}')
    print('Extensions: none (Live Server, HTML CSS Support, Auto Rename Tag NOT installed)')
    print('Workspace settings: none (2-space indentation NOT configured)')


create_initial()
