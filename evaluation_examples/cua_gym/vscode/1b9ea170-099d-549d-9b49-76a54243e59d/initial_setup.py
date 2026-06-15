"""
Initial Setup: Configure ESLint React Hooks rules in VSCode
Task ID: vscode_web_073
Domain: vs_code

Creates a React project with ESLint configured but WITHOUT the react-hooks plugin.
The project has a component with hooks violations that are not yet flagged.
eslint-plugin-react-hooks is installed via npm but not configured.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_073'
PROJECT_DIR = f'{WORKDIR}/projects/react-app'
SRC_DIR = f'{PROJECT_DIR}/src'
NODE_MODULES = f'{PROJECT_DIR}/node_modules'

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
    os.makedirs(f'{NODE_MODULES}/eslint-plugin-react-hooks', exist_ok=True)
    os.makedirs(f'{NODE_MODULES}/eslint', exist_ok=True)
    os.makedirs(f'{NODE_MODULES}/eslint-plugin-react', exist_ok=True)
    os.makedirs(f'{NODE_MODULES}/@eslint', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "react-app",
        "version": "1.0.0",
        "description": "Employee Dashboard Application",
        "main": "src/index.jsx",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "lint": "eslint src/",
            "test": "react-scripts test"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "axios": "^1.6.2"
        },
        "devDependencies": {
            "eslint": "^8.56.0",
            "eslint-plugin-react": "^7.33.2",
            "eslint-plugin-react-hooks": "^4.6.0"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- .eslintrc.json (NO react-hooks plugin or rules) ---
    eslintrc = {
        "env": {
            "browser": True,
            "es2021": True
        },
        "extends": [
            "eslint:recommended",
            "plugin:react/recommended"
        ],
        "parserOptions": {
            "ecmaFeatures": {
                "jsx": True
            },
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "plugins": [
            "react"
        ],
        "rules": {
            "react/react-in-jsx-scope": "off",
            "no-unused-vars": "warn",
            "no-console": "warn"
        },
        "settings": {
            "react": {
                "version": "detect"
            }
        }
    }
    with open(f'{PROJECT_DIR}/.eslintrc.json', 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # --- src/App.jsx (has hooks violations that are NOT flagged) ---
    app_jsx = '''\
import React, { useState, useEffect } from 'react';
import axios from 'axios';

/**
 * Employee Dashboard Component
 * Displays a list of employees with search and filter capabilities.
 */
function EmployeeDashboard({ departmentFilter, showInactive }) {
  const [employees, setEmployees] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortField, setSortField] = useState('name');

  // BUG: Conditional hook call - violates rules-of-hooks
  if (showInactive) {
    const [inactiveList, setInactiveList] = useState([]);
  }

  // BUG: Missing dependencies - violates exhaustive-deps
  // departmentFilter and sortField are used but not in the dependency array
  useEffect(() => {
    async function fetchEmployees() {
      try {
        setLoading(true);
        const response = await axios.get('/api/employees', {
          params: {
            department: departmentFilter,
            sort: sortField,
          },
        });
        setEmployees(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchEmployees();
  }, []);  // Missing: departmentFilter, sortField

  const filteredEmployees = employees.filter((emp) =>
    emp.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) return <div className="loading-spinner">Loading employees...</div>;
  if (error) return <div className="error-banner">Error: {error}</div>;

  return (
    <div className="employee-dashboard">
      <h1>Employee Directory</h1>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search employees by name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <div className="sort-controls">
        <label>Sort by: </label>
        <select value={sortField} onChange={(e) => setSortField(e.target.value)}>
          <option value="name">Name</option>
          <option value="department">Department</option>
          <option value="startDate">Start Date</option>
          <option value="salary">Salary</option>
        </select>
      </div>
      <table className="employee-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Department</th>
            <th>Role</th>
            <th>Start Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {filteredEmployees.map((emp) => (
            <tr key={emp.id} className={emp.status === 'inactive' ? 'inactive-row' : ''}>
              <td>{emp.name}</td>
              <td>{emp.department}</td>
              <td>{emp.role}</td>
              <td>{emp.startDate}</td>
              <td>
                <span className={`status-badge ${emp.status}`}>
                  {emp.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="summary">
        <p>Showing {filteredEmployees.length} of {employees.length} employees</p>
      </div>
    </div>
  );
}

export default EmployeeDashboard;
'''
    with open(f'{SRC_DIR}/App.jsx', 'w') as f:
        f.write(app_jsx)

    # --- src/index.jsx ---
    index_jsx = '''\
import React from 'react';
import ReactDOM from 'react-dom/client';
import EmployeeDashboard from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <EmployeeDashboard departmentFilter="Engineering" showInactive={false} />
  </React.StrictMode>
);
'''
    with open(f'{SRC_DIR}/index.jsx', 'w') as f:
        f.write(index_jsx)

    # --- Stub node_modules/eslint-plugin-react-hooks/package.json ---
    hooks_pkg = {
        "name": "eslint-plugin-react-hooks",
        "version": "4.6.0",
        "description": "ESLint rules for React Hooks",
        "main": "index.js"
    }
    with open(f'{NODE_MODULES}/eslint-plugin-react-hooks/package.json', 'w') as f:
        json.dump(hooks_pkg, f, indent=2)

    # Minimal index.js stub so ESLint can load the plugin
    hooks_index = '''\
module.exports = {
  rules: {
    "rules-of-hooks": {
      meta: { type: "problem", docs: { description: "Enforces the Rules of Hooks" } },
      create: function(context) { return {}; }
    },
    "exhaustive-deps": {
      meta: { type: "suggestion", docs: { description: "Verifies the list of dependencies for Hooks" } },
      create: function(context) { return {}; }
    }
  }
};
'''
    with open(f'{NODE_MODULES}/eslint-plugin-react-hooks/index.js', 'w') as f:
        f.write(hooks_index)

    # --- Stub node_modules/eslint-plugin-react/package.json ---
    react_plugin_pkg = {
        "name": "eslint-plugin-react",
        "version": "7.33.2",
        "description": "React specific linting rules for ESLint",
        "main": "index.js"
    }
    with open(f'{NODE_MODULES}/eslint-plugin-react/package.json', 'w') as f:
        json.dump(react_plugin_pkg, f, indent=2)

    with open(f'{NODE_MODULES}/eslint-plugin-react/index.js', 'w') as f:
        f.write('module.exports = { rules: {}, configs: { recommended: { rules: {} } } };\n')

    # --- .vscode/settings.json for workspace ---
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    os.makedirs(vscode_dir, exist_ok=True)
    vscode_settings = {
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "eslint.validate": [
            "javascript",
            "javascriptreact"
        ]
    }
    with open(f'{vscode_dir}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=2)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'  .eslintrc.json: basic config WITHOUT react-hooks plugin')
    print(f'  src/App.jsx: component with hooks violations (not flagged)')
    print(f'  node_modules/eslint-plugin-react-hooks: installed but not configured')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
