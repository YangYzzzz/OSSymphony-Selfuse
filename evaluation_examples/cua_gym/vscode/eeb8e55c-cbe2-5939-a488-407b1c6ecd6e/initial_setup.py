"""
Initial Setup: Stage modified files and create a commit in VSCode
Task ID: vscode_web_011
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_011'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'


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


def run(cmd, cwd=None):
    """Run a shell command."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}\nSTDERR: {result.stderr}")
    return result


def create_initial():
    # 1. Create project directory structure
    dirs = [
        f'{PROJECT_DIR}/src/components',
        f'{PROJECT_DIR}/src/styles',
        f'{PROJECT_DIR}/public',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 2. Initialize git repo with an initial commit
    run('git init', cwd=PROJECT_DIR)
    run('git config user.email "developer@webapp.dev"', cwd=PROJECT_DIR)
    run('git config user.name "Developer"', cwd=PROJECT_DIR)

    # 3. Create initial committed files (the base state before modifications)

    # package.json
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write('''{
  "name": "webapp",
  "version": "1.2.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}
''')

    # src/App.jsx - original version (before modification)
    with open(f'{PROJECT_DIR}/src/App.jsx', 'w') as f:
        f.write('''import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to WebApp</h1>
      </header>
      <main>
        <p>This is the main content area.</p>
      </main>
    </div>
  );
}

export default App;
''')

    # src/App.css
    with open(f'{PROJECT_DIR}/src/App.css', 'w') as f:
        f.write('''.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}

main {
  padding: 20px;
}
''')

    # src/components/Nav.jsx - original (empty placeholder)
    with open(f'{PROJECT_DIR}/src/components/Nav.jsx', 'w') as f:
        f.write('''import React from 'react';

function Nav() {
  return (
    <nav>
      <a href="/">Home</a>
    </nav>
  );
}

export default Nav;
''')

    # src/styles/nav.css - original (empty placeholder)
    with open(f'{PROJECT_DIR}/src/styles/nav.css', 'w') as f:
        f.write('''nav {
  padding: 10px;
}

nav a {
  text-decoration: none;
  color: #333;
}
''')

    # public/index.html
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebApp</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
''')

    # 4. Make the initial commit
    run('git add -A', cwd=PROJECT_DIR)
    run('git commit -m "Initial commit: basic React project structure"', cwd=PROJECT_DIR)

    # 5. Now modify the three files to create the "modified but unstaged" state

    # Modified src/components/Nav.jsx - responsive navigation component
    with open(f'{PROJECT_DIR}/src/components/Nav.jsx', 'w') as f:
        f.write('''import React, { useState } from 'react';
import '../styles/nav.css';

function Nav() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="responsive-nav">
      <div className="nav-brand">
        <a href="/">WebApp</a>
        <button className="nav-toggle" onClick={toggleMenu}>
          {isMenuOpen ? '\\u2715' : '\\u2630'}
        </button>
      </div>
      <ul className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/services">Services</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  );
}

export default Nav;
''')

    # Modified src/styles/nav.css - responsive styles
    with open(f'{PROJECT_DIR}/src/styles/nav.css', 'w') as f:
        f.write('''.responsive-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1a1a2e;
  color: white;
  flex-wrap: wrap;
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-toggle {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  color: #e0e0e0;
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-links li a:hover {
  color: #00d2ff;
}

@media (max-width: 768px) {
  .nav-toggle {
    display: block;
  }

  .nav-links {
    display: none;
    flex-basis: 100%;
    flex-direction: column;
    text-align: center;
    padding: 1rem 0;
  }

  .nav-links.active {
    display: flex;
  }
}
''')

    # Modified src/App.jsx - imports Nav component
    with open(f'{PROJECT_DIR}/src/App.jsx', 'w') as f:
        f.write('''import React from 'react';
import Nav from './components/Nav';
import './App.css';

function App() {
  return (
    <div className="App">
      <Nav />
      <header className="App-header">
        <h1>Welcome to WebApp</h1>
      </header>
      <main>
        <p>This is the main content area.</p>
      </main>
    </div>
  );
}

export default App;
''')

    print(f'Project created at: {PROJECT_DIR}')
    print('Three files modified (unstaged): src/components/Nav.jsx, src/styles/nav.css, src/App.jsx')

    # 6. Verify git status shows modifications
    result = run('git status', cwd=PROJECT_DIR)
    print(f'Git status:\n{result.stdout}')

    # 7. Launch VSCode with the project and Source Control panel visible
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
