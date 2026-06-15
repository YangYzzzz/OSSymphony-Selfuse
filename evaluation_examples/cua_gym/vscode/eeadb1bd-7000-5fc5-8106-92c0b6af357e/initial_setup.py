"""
Initial Setup: Configure a React webapp project for accessibility auditing in VSCode.
Task ID: vscode_gf3_016
Domain: vscode

Creates:
- /home/user/projects/webapp/ project structure with App.tsx
- VSCode settings with NO axe-linter configuration
- axe Accessibility Linter extension NOT installed
- Opens VSCode with the App.tsx file
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_016'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
SRC_DIR = f'{PROJECT_DIR}/src'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    """Create the React webapp project structure."""
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # package.json
    package_json = {
        "name": "webapp",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^4.9.5"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "esModuleInterop": True,
            "allowSyntheticDefaultImports": True,
            "strict": True,
            "forceConsistentCasingInFileNames": True,
            "noFallthroughCasesInSwitch": True,
            "module": "esnext",
            "moduleResolution": "node",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx"
        },
        "include": ["src"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # App.tsx - a realistic React component with some accessibility concerns
    app_tsx = '''import React, { useState } from 'react';

interface Employee {
  id: number;
  name: string;
  department: string;
  email: string;
  status: 'active' | 'on-leave' | 'terminated';
}

const employees: Employee[] = [
  { id: 1, name: 'Sarah Chen', department: 'Engineering', email: 'sarah.chen@acmecorp.io', status: 'active' },
  { id: 2, name: 'Marcus Johnson', department: 'Marketing', email: 'marcus.j@acmecorp.io', status: 'active' },
  { id: 3, name: 'Priya Patel', department: 'Design', email: 'priya.p@acmecorp.io', status: 'on-leave' },
  { id: 4, name: 'James O\\'Brien', department: 'Engineering', email: 'james.ob@acmecorp.io', status: 'active' },
  { id: 5, name: 'Aisha Williams', department: 'Product', email: 'aisha.w@acmecorp.io', status: 'terminated' },
  { id: 6, name: 'Carlos Mendez', department: 'Engineering', email: 'carlos.m@acmecorp.io', status: 'active' },
  { id: 7, name: 'Emily Zhang', department: 'QA', email: 'emily.z@acmecorp.io', status: 'active' },
  { id: 8, name: 'David Kim', department: 'Design', email: 'david.k@acmecorp.io', status: 'on-leave' },
];

const statusColors: Record<string, string> = {
  active: '#2d8a4e',
  'on-leave': '#c9a227',
  terminated: '#c94444',
};

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState<string>('all');

  const departments = ['all', ...new Set(employees.map(e => e.department))];

  const filteredEmployees = employees.filter(emp => {
    const matchesSearch = emp.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDept = selectedDepartment === 'all' || emp.department === selectedDepartment;
    return matchesSearch && matchesDept;
  });

  return (
    <div style={{ padding: '24px', fontFamily: 'Inter, sans-serif' }}>
      <div style={{ marginBottom: '20px' }}>
        <h1 style={{ fontSize: '28px', color: '#1a1a2e' }}>Employee Directory</h1>
        <p style={{ color: '#6b7280', marginTop: '4px' }}>
          Manage and review team members across departments
        </p>
      </div>

      <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Search employees..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: '10px 14px',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            fontSize: '14px',
            flex: 1,
          }}
        />
        <select
          value={selectedDepartment}
          onChange={(e) => setSelectedDepartment(e.target.value)}
          style={{
            padding: '10px 14px',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            fontSize: '14px',
          }}
        >
          {departments.map(dept => (
            <option key={dept} value={dept}>
              {dept === 'all' ? 'All Departments' : dept}
            </option>
          ))}
        </select>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
              <th style={{ textAlign: 'left', padding: '12px 16px', color: '#374151', fontWeight: 600 }}>Name</th>
              <th style={{ textAlign: 'left', padding: '12px 16px', color: '#374151', fontWeight: 600 }}>Department</th>
              <th style={{ textAlign: 'left', padding: '12px 16px', color: '#374151', fontWeight: 600 }}>Email</th>
              <th style={{ textAlign: 'left', padding: '12px 16px', color: '#374151', fontWeight: 600 }}>Status</th>
              <th style={{ textAlign: 'left', padding: '12px 16px', color: '#374151', fontWeight: 600 }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredEmployees.map(emp => (
              <tr key={emp.id} style={{ borderBottom: '1px solid #f3f4f6' }}>
                <td style={{ padding: '12px 16px', fontWeight: 500 }}>{emp.name}</td>
                <td style={{ padding: '12px 16px', color: '#6b7280' }}>{emp.department}</td>
                <td style={{ padding: '12px 16px', color: '#6b7280' }}>{emp.email}</td>
                <td style={{ padding: '12px 16px' }}>
                  <span
                    style={{
                      display: 'inline-block',
                      padding: '2px 10px',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: 500,
                      color: '#fff',
                      backgroundColor: statusColors[emp.status],
                    }}
                  >
                    {emp.status}
                  </span>
                </td>
                <td style={{ padding: '12px 16px' }}>
                  <div onClick={() => alert(`Viewing ${emp.name}`)}>
                    <span style={{ color: '#3b82f6', cursor: 'pointer' }}>View</span>
                  </div>
                  <div onClick={() => alert(`Editing ${emp.name}`)}>
                    <span style={{ color: '#3b82f6', cursor: 'pointer', marginLeft: '12px' }}>Edit</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredEmployees.length === 0 && (
        <div style={{ textAlign: 'center', padding: '40px', color: '#9ca3af' }}>
          No employees found matching your criteria.
        </div>
      )}

      <div style={{ marginTop: '20px', fontSize: '13px', color: '#9ca3af' }}>
        Showing {filteredEmployees.length} of {employees.length} employees
      </div>
    </div>
  );
}

export default App;
'''

    with open(f'{SRC_DIR}/App.tsx', 'w') as f:
        f.write(app_tsx)

    # index.tsx
    index_tsx = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
    with open(f'{SRC_DIR}/index.tsx', 'w') as f:
        f.write(index_tsx)

    # public/index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Acme Corp - Employee Directory</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
'''
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write(index_html)

    print(f'Project created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Set up VSCode settings WITHOUT any axe-linter configuration."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Ensure NO axe-linter settings exist
    keys_to_remove = [k for k in settings if k.startswith('axe-linter')]
    for k in keys_to_remove:
        del settings[k]

    # Add some baseline VSCode settings for realism
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark+",
        "typescript.tsdk": "node_modules/typescript/lib",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written: {SETTINGS_PATH}')


def ensure_extension_not_installed():
    """Make sure axe Accessibility Linter is not installed."""
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'deque-systems.vscode-axe-linter' in result.stdout:
            subprocess.run(
                ['code', '--uninstall-extension', 'deque-systems.vscode-axe-linter'],
                capture_output=True, text=True, timeout=60
            )
            print('Uninstalled axe Accessibility Linter extension.')
        else:
            print('axe Accessibility Linter extension not installed (correct).')
    except Exception as e:
        print(f'Extension check warning: {e}')


def main():
    create_project()
    setup_vscode_settings()
    ensure_extension_not_installed()

    # Open VSCode with the App.tsx file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{SRC_DIR}/App.tsx"', delay_sec=2.0)
    print(f'GUI_READY: VSCode launched with {SRC_DIR}/App.tsx')


main()
