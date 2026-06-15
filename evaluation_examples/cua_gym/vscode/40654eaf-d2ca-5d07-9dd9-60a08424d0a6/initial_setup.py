"""
Initial Setup: Configure Chrome debugger extension settings for React development
Task ID: vscode_we_093
Domain: vscode

Creates a realistic Create React App project structure at ~/projects/my-react-app/
with NO .vscode/launch.json (the agent must create it).
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_093'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'my-react-app')


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
    """Create a realistic Create React App project structure."""

    # Create directory structure
    dirs = [
        os.path.join(PROJECT_DIR, 'src'),
        os.path.join(PROJECT_DIR, 'public'),
        os.path.join(PROJECT_DIR, 'node_modules'),  # empty placeholder
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # package.json
    package_json = {
        "name": "my-react-app",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "@testing-library/jest-dom": "^5.17.0",
            "@testing-library/react": "^13.4.0",
            "@testing-library/user-event": "^13.5.0",
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
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    index_js = """\
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write(index_js)

    # src/App.js
    app_js = """\
import React, { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  const [tasks, setTasks] = useState([
    { id: 1, text: 'Review Q1 analytics report', done: false },
    { id: 2, text: 'Update deployment pipeline', done: true },
    { id: 3, text: 'Prepare sprint demo slides', done: false },
  ]);

  const toggleTask = (id) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, done: !task.done } : task
    ));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Project Dashboard</h1>
        <p>Active tasks: {tasks.filter(t => !t.done).length}</p>
        <button onClick={() => setCount(count + 1)}>
          Refreshed {count} times
        </button>
        <ul>
          {tasks.map(task => (
            <li
              key={task.id}
              onClick={() => toggleTask(task.id)}
              style={{ textDecoration: task.done ? 'line-through' : 'none' }}
            >
              {task.text}
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'App.js'), 'w') as f:
        f.write(app_js)

    # src/App.css
    app_css = """\
.App {
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

.App-header ul {
  list-style: none;
  padding: 0;
  text-align: left;
}

.App-header li {
  cursor: pointer;
  padding: 8px 16px;
  margin: 4px 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'App.css'), 'w') as f:
        f.write(app_css)

    # src/index.css
    index_css = """\
body {
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
    with open(os.path.join(PROJECT_DIR, 'src', 'index.css'), 'w') as f:
        f.write(index_css)

    # src/reportWebVitals.js
    report_wv = """\
const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'reportWebVitals.js'), 'w') as f:
        f.write(report_wv)

    # public/index.html
    index_html = """\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Project Dashboard - React App" />
    <title>Project Dashboard</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write(index_html)

    # .gitignore
    gitignore = """\
/node_modules
/build
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # README.md
    readme = """\
# Project Dashboard

A simple React-based project dashboard for tracking tasks and metrics.

## Getting Started

```bash
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Explicitly ensure NO .vscode directory exists
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'React project created at: {PROJECT_DIR}')
    print(f'No .vscode/launch.json exists (verified)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_project()
