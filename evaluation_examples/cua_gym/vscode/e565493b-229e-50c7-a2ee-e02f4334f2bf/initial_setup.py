"""
Initial Setup: Create a React components project with jest, no tasks.json
Task ID: vscode_td_022
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_022'
PROJECT_DIR = f'{WORKDIR}/projects/react-components'


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
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/__tests__', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # package.json with jest dependency
    package_json = {
        "name": "react-components",
        "version": "1.2.0",
        "description": "Reusable React component library for internal dashboard",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "@testing-library/react": "^14.1.2",
            "@testing-library/jest-dom": "^6.1.4",
            "eslint": "^8.55.0"
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version"]
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # src/index.js
    with open(f'{PROJECT_DIR}/src/index.js', 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/App.js
    with open(f'{PROJECT_DIR}/src/App.js', 'w') as f:
        f.write("""import React from 'react';
import { DataTable } from './components/DataTable';
import { StatusBadge } from './components/StatusBadge';

function App() {
  const sampleData = [
    { id: 1, name: 'Sarah Chen', department: 'Engineering', status: 'active' },
    { id: 2, name: 'Marcus Johnson', department: 'Marketing', status: 'active' },
    { id: 3, name: 'Priya Sharma', department: 'Design', status: 'on-leave' },
  ];

  return (
    <div className="app-container">
      <h1>Team Dashboard</h1>
      <DataTable data={sampleData} />
    </div>
  );
}

export default App;
""")

    # src/components/DataTable.js
    with open(f'{PROJECT_DIR}/src/components/DataTable.js', 'w') as f:
        f.write("""import React from 'react';
import { StatusBadge } from './StatusBadge';

export function DataTable({ data, onRowClick }) {
  if (!data || data.length === 0) {
    return <p className="empty-state">No records found.</p>;
  }

  const columns = Object.keys(data[0]).filter(key => key !== 'id');

  return (
    <table className="data-table">
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col}>{col.charAt(0).toUpperCase() + col.slice(1)}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr key={row.id} onClick={() => onRowClick && onRowClick(row)}>
            {columns.map(col => (
              <td key={col}>
                {col === 'status' ? <StatusBadge status={row[col]} /> : row[col]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
""")

    # src/components/StatusBadge.js
    with open(f'{PROJECT_DIR}/src/components/StatusBadge.js', 'w') as f:
        f.write("""import React from 'react';

const STATUS_COLORS = {
  active: '#22c55e',
  inactive: '#94a3b8',
  'on-leave': '#f59e0b',
  terminated: '#ef4444',
};

export function StatusBadge({ status }) {
  const color = STATUS_COLORS[status] || '#6b7280';

  return (
    <span
      className="status-badge"
      style={{
        backgroundColor: color,
        color: '#fff',
        padding: '2px 8px',
        borderRadius: '12px',
        fontSize: '0.85em',
      }}
    >
      {status}
    </span>
  );
}
""")

    # src/__tests__/DataTable.test.js
    with open(f'{PROJECT_DIR}/src/__tests__/DataTable.test.js', 'w') as f:
        f.write("""import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { DataTable } from '../components/DataTable';

describe('DataTable', () => {
  const mockData = [
    { id: 1, name: 'Alice Wang', department: 'Engineering', status: 'active' },
    { id: 2, name: 'Bob Martinez', department: 'Sales', status: 'inactive' },
  ];

  test('renders table headers from data keys', () => {
    render(<DataTable data={mockData} />);
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Department')).toBeInTheDocument();
    expect(screen.getByText('Status')).toBeInTheDocument();
  });

  test('renders all data rows', () => {
    render(<DataTable data={mockData} />);
    expect(screen.getByText('Alice Wang')).toBeInTheDocument();
    expect(screen.getByText('Bob Martinez')).toBeInTheDocument();
  });

  test('shows empty state when no data', () => {
    render(<DataTable data={[]} />);
    expect(screen.getByText('No records found.')).toBeInTheDocument();
  });
});
""")

    # src/__tests__/StatusBadge.test.js
    with open(f'{PROJECT_DIR}/src/__tests__/StatusBadge.test.js', 'w') as f:
        f.write("""import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { StatusBadge } from '../components/StatusBadge';

describe('StatusBadge', () => {
  test('renders status text', () => {
    render(<StatusBadge status="active" />);
    expect(screen.getByText('active')).toBeInTheDocument();
  });

  test('applies green color for active status', () => {
    render(<StatusBadge status="active" />);
    const badge = screen.getByText('active');
    expect(badge).toHaveStyle({ backgroundColor: '#22c55e' });
  });

  test('applies amber color for on-leave status', () => {
    render(<StatusBadge status="on-leave" />);
    const badge = screen.getByText('on-leave');
    expect(badge).toHaveStyle({ backgroundColor: '#f59e0b' });
  });
});
""")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
build/
coverage/
.env.local
.DS_Store
""")

    # README.md
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# React Components Library

Internal reusable component library for the team dashboard application.

## Getting Started

```bash
npm install
npm start
```

## Running Tests

```bash
npm test
```

## Components

- **DataTable** - Sortable data table with row click handlers
- **StatusBadge** - Color-coded status indicator
""")

    # Ensure NO .vscode/tasks.json exists (the task is to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    tasks_path = f'{vscode_dir}/tasks.json'
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'package.json with jest: {PROJECT_DIR}/package.json')
    print(f'No .vscode/tasks.json exists (verified)')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
