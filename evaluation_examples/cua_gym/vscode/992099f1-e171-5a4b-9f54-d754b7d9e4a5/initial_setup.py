"""
Initial Setup: Open VSCode with a web project folder for Git initialization
Task ID: vscode_gf5_003
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_003'
PROJECT_DIR = f'{WORKDIR}/projects/web-project'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create index.html with realistic content
    index_html = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Artisan Coffee Roasters</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="logo">
                <h1>Artisan Coffee Roasters</h1>
            </div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#menu">Menu</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="home" class="hero">
            <h2>Freshly Roasted, Perfectly Brewed</h2>
            <p>Discover our hand-selected single-origin beans from farms across Colombia, Ethiopia, and Guatemala.</p>
            <button class="cta-button">Explore Our Blends</button>
        </section>

        <section id="menu" class="menu-section">
            <h2>Our Menu</h2>
            <div class="menu-grid">
                <div class="menu-item">
                    <h3>Espresso</h3>
                    <p>Rich and bold, pulled from our house blend.</p>
                    <span class="price">$3.50</span>
                </div>
                <div class="menu-item">
                    <h3>Pour Over</h3>
                    <p>Single-origin Ethiopian Yirgacheffe, bright and fruity.</p>
                    <span class="price">$4.75</span>
                </div>
                <div class="menu-item">
                    <h3>Cold Brew</h3>
                    <p>Smooth and refreshing, steeped for 18 hours.</p>
                    <span class="price">$5.00</span>
                </div>
            </div>
        </section>

        <section id="about" class="about-section">
            <h2>About Us</h2>
            <p>Founded in 2019, Artisan Coffee Roasters began as a small roastery in Portland, Oregon. We source our beans directly from family-owned farms, ensuring fair trade practices and exceptional quality in every cup.</p>
        </section>

        <section id="contact" class="contact-section">
            <h2>Visit Us</h2>
            <p>742 Hawthorne Blvd, Portland, OR 97214</p>
            <p>Open daily: 7:00 AM - 6:00 PM</p>
            <p>Email: hello@artisancoffeeroasters.com</p>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Artisan Coffee Roasters. All rights reserved.</p>
    </footer>
</body>
</html>
"""
    with open(os.path.join(PROJECT_DIR, 'index.html'), 'w') as f:
        f.write(index_html)

    # Create style.css with realistic content
    style_css = """\
/* Artisan Coffee Roasters - Main Stylesheet */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    line-height: 1.6;
    color: #2c1810;
    background-color: #faf6f1;
}

/* Navigation */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #3c2415;
    color: #faf6f1;
}

.logo h1 {
    font-size: 1.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 2rem;
}

.nav-links a {
    color: #d4a574;
    text-decoration: none;
    font-size: 0.95rem;
    transition: color 0.3s ease;
}

.nav-links a:hover {
    color: #faf6f1;
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 6rem 2rem;
    background: linear-gradient(rgba(60, 36, 21, 0.7), rgba(60, 36, 21, 0.7)),
                url('images/hero-bg.jpg') center/cover;
    color: #faf6f1;
}

.hero h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto 2rem;
}

.cta-button {
    padding: 0.8rem 2rem;
    background-color: #d4a574;
    color: #2c1810;
    border: none;
    font-size: 1rem;
    cursor: pointer;
    letter-spacing: 1px;
    transition: background-color 0.3s ease;
}

.cta-button:hover {
    background-color: #c49464;
}

/* Menu Section */
.menu-section {
    padding: 4rem 2rem;
    text-align: center;
}

.menu-section h2 {
    font-size: 2rem;
    margin-bottom: 2rem;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    max-width: 900px;
    margin: 0 auto;
}

.menu-item {
    padding: 2rem;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.menu-item h3 {
    margin-bottom: 0.5rem;
    color: #3c2415;
}

.price {
    display: block;
    margin-top: 1rem;
    font-weight: bold;
    color: #d4a574;
    font-size: 1.2rem;
}

/* About Section */
.about-section {
    padding: 4rem 2rem;
    background-color: #3c2415;
    color: #faf6f1;
    text-align: center;
}

.about-section h2 {
    margin-bottom: 1rem;
}

.about-section p {
    max-width: 700px;
    margin: 0 auto;
}

/* Contact Section */
.contact-section {
    padding: 4rem 2rem;
    text-align: center;
}

.contact-section h2 {
    margin-bottom: 1rem;
}

.contact-section p {
    margin-bottom: 0.5rem;
}

/* Footer */
footer {
    background-color: #2c1810;
    color: #d4a574;
    text-align: center;
    padding: 1.5rem;
    font-size: 0.85rem;
}
"""
    with open(os.path.join(PROJECT_DIR, 'style.css'), 'w') as f:
        f.write(style_css)

    # Ensure no .git directory exists (clean state)
    git_dir = os.path.join(PROJECT_DIR, '.git')
    if os.path.exists(git_dir):
        import shutil
        shutil.rmtree(git_dir)

    # Ensure no .gitignore exists
    gitignore_path = os.path.join(PROJECT_DIR, '.gitignore')
    if os.path.exists(gitignore_path):
        os.remove(gitignore_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  - index.html')
    print(f'  - style.css')
    print(f'  - No .git directory')
    print(f'  - No .gitignore')

    # GUI-ready: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
