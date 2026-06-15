"""
Initial Setup: Create react-app project folder without .vscode directory
Task ID: vscode_ext_021
Domain: vs_code

Creates ~/projects/react-app/ with realistic React project files,
but WITHOUT any .vscode/ directory (the agent must create it).
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_021'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'


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
    # Ensure the projects/react-app directory exists (no .vscode inside)
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Ensure .vscode does NOT exist (clean state for the task)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # Create a realistic React app project structure
    # package.json
    package_json = {
        "name": "react-app",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "web-vitals": "^2.1.4"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "eslintConfig": {
            "extends": ["react-app", "react-app/jest"]
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # README.md
    readme_content = """# React App

A modern React application bootstrapped with Create React App.

## Getting Started

### Prerequisites

- Node.js >= 14.0.0
- npm >= 6.14.0

### Installation

```bash
npm install
```

### Running the App

```bash
npm start
```

Opens the app at [http://localhost:3000](http://localhost:3000).

### Building for Production

```bash
npm run build
```

## Project Structure

```
react-app/
  src/
    App.js
    App.css
    index.js
    components/
      Header.js
      Footer.js
  public/
    index.html
    favicon.ico
  package.json
  README.md
```
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # .gitignore
    gitignore_content = """# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore_content)

    # src/ directory with App.js
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    app_js = """import React, { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to React App</h1>
        <p>Build fast, modern web applications.</p>
        <button onClick={() => setCount(count + 1)}>
          Count: {count}
        </button>
      </header>
    </div>
  );
}

export default App;
"""
    with open(os.path.join(src_dir, 'App.js'), 'w') as f:
        f.write(app_js)

    app_css = """.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}

.App-header button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #61dafb;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
"""
    with open(os.path.join(src_dir, 'App.css'), 'w') as f:
        f.write(app_css)

    index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
    with open(os.path.join(src_dir, 'index.js'), 'w') as f:
        f.write(index_js)

    index_css = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
"""
    with open(os.path.join(src_dir, 'index.css'), 'w') as f:
        f.write(index_css)

    # components/ subdirectory
    components_dir = os.path.join(src_dir, 'components')
    os.makedirs(components_dir, exist_ok=True)

    header_js = """import React from 'react';

function Header({ title }) {
  return (
    <header>
      <nav>
        <h2>{title || 'React App'}</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
"""
    with open(os.path.join(components_dir, 'Header.js'), 'w') as f:
        f.write(header_js)

    footer_js = """import React from 'react';

function Footer() {
  return (
    <footer>
      <p>&copy; {new Date().getFullYear()} React App. All rights reserved.</p>
    </footer>
  );
}

export default Footer;
"""
    with open(os.path.join(components_dir, 'Footer.js'), 'w') as f:
        f.write(footer_js)

    # public/ directory
    public_dir = os.path.join(PROJECT_DIR, 'public')
    os.makedirs(public_dir, exist_ok=True)

    index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Web site created using create-react-app" />
    <title>React App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""
    with open(os.path.join(public_dir, 'index.html'), 'w') as f:
        f.write(index_html)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'No .vscode/ directory — agent must create it with extensions.json')

    # GUI-ready startup: open VSCode with the react-app folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with react-app folder (DISPLAY=:0)')


create_initial()
