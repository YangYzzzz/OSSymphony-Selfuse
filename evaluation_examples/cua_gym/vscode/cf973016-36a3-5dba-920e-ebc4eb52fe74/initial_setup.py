"""
Initial Setup: ESLint airbnb config with missing peer dependencies
Task ID: vscode_fix_059
Domain: vs_code

Creates a React project with eslint-config-airbnb installed but missing
peer dependencies (eslint-plugin-import, eslint-plugin-jsx-a11y,
eslint-plugin-react, eslint-plugin-react-hooks). ESLint will fail to
load the airbnb config.
"""

import json
import os
import shlex
import shutil
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'react-project')
NODE_DIR = os.path.join(WORKDIR, '.local', 'node')


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


def run_cmd(cmd, **kwargs):
    """Run a shell command with node in PATH."""
    env = os.environ.copy()
    node_bin = os.path.join(NODE_DIR, 'bin')
    env['PATH'] = f"{node_bin}:{env.get('PATH', '')}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                            timeout=kwargs.get('timeout', 180), env=env)
    if result.stdout:
        print(result.stdout[-1500:])
    if result.returncode != 0 and result.stderr:
        print(f"STDERR: {result.stderr[-500:]}")
    return result


def install_node():
    """Install Node.js to user's home directory (no sudo required)."""
    node_bin = os.path.join(NODE_DIR, 'bin', 'node')
    if os.path.exists(node_bin):
        print(f"Node.js already installed at {node_bin}")
        return

    print("Installing Node.js 18 (user-local)...")
    os.makedirs(NODE_DIR, exist_ok=True)
    tarball = '/tmp/node.tar.xz'

    # Download Node.js binary
    subprocess.run(
        ['curl', '-fsSL', '-o', tarball,
         'https://nodejs.org/dist/v18.20.2/node-v18.20.2-linux-x64.tar.xz'],
        check=True, timeout=120
    )

    # Extract to NODE_DIR
    subprocess.run(
        ['tar', '-xf', tarball, '--strip-components=1', '-C', NODE_DIR],
        check=True, timeout=60
    )

    # Verify
    result = subprocess.run([node_bin, '--version'], capture_output=True, text=True)
    print(f"Node.js version: {result.stdout.strip()}")

    npm_bin = os.path.join(NODE_DIR, 'bin', 'npm')
    result = subprocess.run([npm_bin, '--version'], capture_output=True, text=True)
    print(f"npm version: {result.stdout.strip()}")


def create_initial():
    # Step 0: Install Node.js
    install_node()

    # Step 1: Create project directory structure
    if os.path.exists(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "react-project",
        "version": "1.0.0",
        "description": "Employee dashboard application",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1"
        },
        "devDependencies": {
            "eslint": "^8.50.0",
            "eslint-config-airbnb": "^19.0.4"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- .eslintrc.json ---
    eslintrc = {
        "extends": "airbnb",
        "env": {
            "browser": True,
            "es2021": True
        },
        "parserOptions": {
            "ecmaFeatures": {
                "jsx": True
            },
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "rules": {
            "react/react-in-jsx-scope": "off"
        }
    }
    with open(os.path.join(PROJECT_DIR, '.eslintrc.json'), 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # --- src/index.js ---
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write("""\
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # --- src/App.js ---
    with open(os.path.join(PROJECT_DIR, 'src', 'App.js'), 'w') as f:
        f.write("""\
import React, { useState } from 'react';
import EmployeeList from './components/EmployeeList';

function App() {
  const [employees] = useState([
    { id: 1, name: 'Sarah Chen', department: 'Engineering', salary: 95000 },
    { id: 2, name: 'Marcus Johnson', department: 'Marketing', salary: 78000 },
    { id: 3, name: 'Emily Rodriguez', department: 'Design', salary: 82000 },
    { id: 4, name: 'David Kim', department: 'Engineering', salary: 91000 },
    { id: 5, name: 'Rachel Thompson', department: 'Sales', salary: 73000 },
  ]);

  return (
    <div className="App">
      <h1>Employee Dashboard</h1>
      <EmployeeList employees={employees} />
    </div>
  );
}

export default App;
""")

    # --- src/components/EmployeeList.js ---
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'EmployeeList.js'), 'w') as f:
        f.write("""\
import React from 'react';

function EmployeeList({ employees }) {
  const totalSalary = employees.reduce((sum, emp) => sum + emp.salary, 0);
  const avgSalary = totalSalary / employees.length;

  return (
    <div className="employee-list">
      <h2>Team Members</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Department</th>
            <th>Salary</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((emp) => (
            <tr key={emp.id}>
              <td>{emp.name}</td>
              <td>{emp.department}</td>
              <td>${emp.salary.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p>Average Salary: ${avgSalary.toLocaleString()}</p>
    </div>
  );
}

export default EmployeeList;
""")

    # --- public/index.html ---
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Employee Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
""")

    # Step 2: Install eslint + eslint-config-airbnb (with --legacy-peer-deps)
    print("Installing eslint and eslint-config-airbnb...")
    run_cmd(f'cd {PROJECT_DIR} && npm install --save-dev eslint@8.50.0 eslint-config-airbnb@19.0.4 --legacy-peer-deps',
            timeout=300)

    # Step 3: Remove peer dependencies to create the broken state
    node_modules = os.path.join(PROJECT_DIR, 'node_modules')
    for pkg in ['eslint-plugin-import', 'eslint-plugin-jsx-a11y',
                'eslint-plugin-react', 'eslint-plugin-react-hooks']:
        pkg_path = os.path.join(node_modules, pkg)
        if os.path.exists(pkg_path):
            shutil.rmtree(pkg_path)
            print(f"Removed {pkg} from node_modules")
        else:
            print(f"{pkg} not in node_modules (already absent)")

    # Step 4: Restore clean package.json (without peer deps in devDependencies)
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)
    print("Restored clean package.json")

    # Verify broken state
    print("\nVerifying broken state...")
    for pkg in ['eslint-plugin-import', 'eslint-plugin-jsx-a11y',
                'eslint-plugin-react', 'eslint-plugin-react-hooks']:
        pkg_path = os.path.join(node_modules, pkg)
        status = "MISSING (correct)" if not os.path.exists(pkg_path) else "EXISTS (wrong!)"
        print(f"  {pkg}: {status}")

    print(f"\nProject created at {PROJECT_DIR}")

    # Step 5: Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with react-project')


create_initial()
