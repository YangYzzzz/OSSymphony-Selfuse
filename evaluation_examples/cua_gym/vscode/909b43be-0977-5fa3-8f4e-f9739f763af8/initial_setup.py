"""
Initial Setup: Create a web development workspace with VSCode settings, keybindings,
and extensions configured, but no profile export done yet.
Task ID: vscode_web_077
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_077'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')


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
    """Create a realistic web development project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'styles'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'utils'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'public'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'tests'), exist_ok=True)

    # package.json
    package_json = {
        "name": "team-webapp",
        "version": "2.1.0",
        "description": "Internal team dashboard for project tracking and analytics",
        "main": "src/index.js",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "lint": "eslint src/",
            "format": "prettier --write \"src/**/*.{js,jsx,css}\""
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.1",
            "axios": "^1.6.2",
            "chart.js": "^4.4.1",
            "react-chartjs-2": "^5.2.0",
            "@mui/material": "^5.14.20",
            "@emotion/react": "^11.11.1",
            "@emotion/styled": "^11.11.0"
        },
        "devDependencies": {
            "eslint": "^8.55.0",
            "eslint-config-prettier": "^9.1.0",
            "prettier": "^3.1.0",
            "@testing-library/react": "^14.1.2",
            "jest": "^29.7.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # index.html
    with open(os.path.join(PROJECT_DIR, 'public', 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Dashboard</title>
    <link rel="stylesheet" href="../src/styles/main.css">
</head>
<body>
    <div id="root"></div>
</body>
</html>
""")

    # src/index.js
    with open(os.path.join(PROJECT_DIR, 'src', 'index.js'), 'w') as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/main.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

    # src/App.js
    with open(os.path.join(PROJECT_DIR, 'src', 'App.js'), 'w') as f:
        f.write("""import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ProjectList from './components/ProjectList';
import Analytics from './components/Analytics';
import Header from './components/Header';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main className="app-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<ProjectList />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
""")

    # src/components/Dashboard.js
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Dashboard.js'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchMetrics } from '../utils/api';
import { Bar } from 'react-chartjs-2';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        const data = await fetchMetrics();
        setMetrics(data);
      } catch (error) {
        console.error('Failed to load metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    loadMetrics();
  }, []);

  if (loading) return <div className="loading-spinner">Loading...</div>;

  return (
    <div className="dashboard">
      <h1>Team Dashboard</h1>
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Active Projects</h3>
          <span className="metric-value">{metrics?.activeProjects || 0}</span>
        </div>
        <div className="metric-card">
          <h3>Completed Tasks</h3>
          <span className="metric-value">{metrics?.completedTasks || 0}</span>
        </div>
        <div className="metric-card">
          <h3>Team Members</h3>
          <span className="metric-value">{metrics?.teamMembers || 0}</span>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
""")

    # src/components/Header.js
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Header.js'), 'w') as f:
        f.write("""import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="app-header">
      <nav>
        <Link to="/" className="nav-logo">TeamDash</Link>
        <div className="nav-links">
          <Link to="/">Dashboard</Link>
          <Link to="/projects">Projects</Link>
          <Link to="/analytics">Analytics</Link>
        </div>
      </nav>
    </header>
  );
};

export default Header;
""")

    # src/components/ProjectList.js
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'ProjectList.js'), 'w') as f:
        f.write("""import React, { useState, useEffect } from 'react';
import { fetchProjects } from '../utils/api';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetchProjects().then(setProjects);
  }, []);

  return (
    <div className="project-list">
      <h1>Projects</h1>
      <table className="project-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Lead</th>
            <th>Due Date</th>
          </tr>
        </thead>
        <tbody>
          {projects.map(project => (
            <tr key={project.id}>
              <td>{project.name}</td>
              <td><span className={`status-${project.status}`}>{project.status}</span></td>
              <td>{project.lead}</td>
              <td>{project.dueDate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProjectList;
""")

    # src/components/Analytics.js
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'Analytics.js'), 'w') as f:
        f.write("""import React from 'react';
import { Line } from 'react-chartjs-2';

const Analytics = () => {
  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Tasks Completed',
        data: [12, 19, 15, 25, 22, 30],
        borderColor: '#4CAF50',
        tension: 0.4,
      },
      {
        label: 'Bugs Reported',
        data: [5, 8, 3, 7, 4, 2],
        borderColor: '#FF5722',
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="analytics">
      <h1>Analytics</h1>
      <div className="chart-container">
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Analytics;
""")

    # src/utils/api.js
    with open(os.path.join(PROJECT_DIR, 'src', 'utils', 'api.js'), 'w') as f:
        f.write("""import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

export const fetchMetrics = async () => {
  const response = await axios.get(`${API_BASE}/metrics`);
  return response.data;
};

export const fetchProjects = async () => {
  const response = await axios.get(`${API_BASE}/projects`);
  return response.data;
};

export const updateProject = async (id, data) => {
  const response = await axios.put(`${API_BASE}/projects/${id}`, data);
  return response.data;
};
""")

    # src/styles/main.css
    with open(os.path.join(PROJECT_DIR, 'src', 'styles', 'main.css'), 'w') as f:
        f.write("""/* Team Dashboard Styles */
:root {
  --primary: #1976d2;
  --secondary: #424242;
  --accent: #82b1ff;
  --background: #fafafa;
  --surface: #ffffff;
  --text-primary: #212121;
  --text-secondary: #757575;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--background);
  color: var(--text-primary);
}

.app-header {
  background-color: var(--primary);
  padding: 0 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-header nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-logo {
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  text-decoration: none;
}

.nav-links a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  margin-left: 2rem;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: white;
}

.app-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.metric-card {
  background: var(--surface);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary);
}

.project-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.project-table th,
.project-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.loading-spinner {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
}

.chart-container {
  background: var(--surface);
  border-radius: 8px;
  padding: 2rem;
  margin-top: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}
""")

    # .eslintrc.json
    with open(os.path.join(PROJECT_DIR, '.eslintrc.json'), 'w') as f:
        json.dump({
            "extends": ["react-app", "prettier"],
            "rules": {
                "no-unused-vars": "warn",
                "no-console": "warn",
                "react/prop-types": "off"
            }
        }, f, indent=2)

    # .prettierrc
    with open(os.path.join(PROJECT_DIR, '.prettierrc'), 'w') as f:
        json.dump({
            "semi": True,
            "singleQuote": True,
            "tabWidth": 2,
            "trailingComma": "es5",
            "printWidth": 100
        }, f, indent=2)

    # tests/Dashboard.test.js
    with open(os.path.join(PROJECT_DIR, 'tests', 'Dashboard.test.js'), 'w') as f:
        f.write("""import { render, screen, waitFor } from '@testing-library/react';
import Dashboard from '../src/components/Dashboard';
import { fetchMetrics } from '../src/utils/api';

jest.mock('../src/utils/api');

describe('Dashboard', () => {
  it('renders loading state initially', () => {
    fetchMetrics.mockResolvedValue({ activeProjects: 5 });
    render(<Dashboard />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('displays metrics after loading', async () => {
    fetchMetrics.mockResolvedValue({
      activeProjects: 8,
      completedTasks: 42,
      teamMembers: 12,
    });
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText('8')).toBeInTheDocument();
      expect(screen.getByText('42')).toBeInTheDocument();
    });
  });
});
""")

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# Team Dashboard Web Application

Internal dashboard for project tracking, team metrics, and analytics visualization.

## Quick Start

```bash
npm install
npm start
```

## Team Members
- Sarah Chen (Frontend Lead)
- Marcus Rivera (Backend)
- Aisha Patel (UI/UX Design)
- James Okafor (DevOps)

## Tech Stack
- React 18 with React Router v6
- Material UI for component library
- Chart.js for data visualization
- Axios for API communication
- ESLint + Prettier for code quality
""")

    print(f'Project created at: {PROJECT_DIR}')


def configure_vscode_settings():
    """Configure VSCode settings for web development."""
    settings = {
        "security.workspace.trust.enabled": False,
        "security.workspace.trust.startupPrompt": "never",
        "security.workspace.trust.emptyWindow": False,
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "editor.formatOnSave": True,
        "editor.formatOnPaste": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.bracketPairColorization.enabled": True,
        "editor.guides.bracketPairs": "active",
        "editor.minimap.enabled": False,
        "editor.suggestSelection": "first",
        "editor.linkedEditing": True,
        "workbench.colorTheme": "Visual Studio Dark",
        "workbench.iconTheme": "vs-seti",
        "workbench.startupEditor": "none",
        "terminal.integrated.defaultProfile.linux": "bash",
        "emmet.includeLanguages": {
            "javascript": "javascriptreact"
        },
        "emmet.triggerExpansionOnTab": True,
        "javascript.updateImportsOnFileMove.enabled": "always",
        "typescript.updateImportsOnFileMove.enabled": "always",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "files.exclude": {
            "**/.git": True,
            "**/.DS_Store": True,
            "**/node_modules": True,
            "**/coverage": True
        },
        "search.exclude": {
            "**/node_modules": True,
            "**/build": True,
            "**/dist": True
        },
        "eslint.validate": [
            "javascript",
            "javascriptreact",
            "typescript",
            "typescriptreact"
        ],
        "[javascript]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[javascriptreact]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[css]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[html]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[json]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        }
    }

    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Settings written to: {SETTINGS_PATH}')


def configure_keybindings():
    """Set up web development keybindings."""
    keybindings = [
        {
            "key": "ctrl+shift+f",
            "command": "editor.action.formatDocument",
            "when": "editorTextFocus"
        },
        {
            "key": "ctrl+shift+l",
            "command": "eslint.executeAutofix",
            "when": "editorTextFocus"
        },
        {
            "key": "ctrl+shift+e",
            "command": "workbench.action.toggleSidebarVisibility"
        },
        {
            "key": "ctrl+shift+t",
            "command": "workbench.action.terminal.toggleTerminal"
        },
        {
            "key": "ctrl+shift+d",
            "command": "editor.action.copyLinesDownAction",
            "when": "editorTextFocus"
        },
        {
            "key": "alt+up",
            "command": "editor.action.moveLinesUpAction",
            "when": "editorTextFocus"
        },
        {
            "key": "alt+down",
            "command": "editor.action.moveLinesDownAction",
            "when": "editorTextFocus"
        },
        {
            "key": "ctrl+d",
            "command": "editor.action.addSelectionToNextFindMatch",
            "when": "editorFocus"
        }
    ]

    os.makedirs(os.path.dirname(KEYBINDINGS_PATH), exist_ok=True)
    with open(KEYBINDINGS_PATH, 'w') as f:
        json.dump(keybindings, f, indent=4)
    print(f'Keybindings written to: {KEYBINDINGS_PATH}')


def configure_snippets():
    """Set up JavaScript/React snippets."""
    os.makedirs(SNIPPETS_DIR, exist_ok=True)

    js_snippets = {
        "React Functional Component": {
            "prefix": "rfc",
            "body": [
                "import React from 'react';",
                "",
                "const ${1:ComponentName} = (${2:props}) => {",
                "  return (",
                "    <div className=\"${3:container}\">",
                "      $0",
                "    </div>",
                "  );",
                "};",
                "",
                "export default ${1:ComponentName};"
            ],
            "description": "Create a React Functional Component"
        },
        "useState Hook": {
            "prefix": "us",
            "body": [
                "const [${1:state}, set${1/(.*)/${1:/capitalize}/}] = useState(${2:initialValue});"
            ],
            "description": "React useState Hook"
        },
        "useEffect Hook": {
            "prefix": "ue",
            "body": [
                "useEffect(() => {",
                "  ${1:// effect}",
                "  return () => {",
                "    ${2:// cleanup}",
                "  };",
                "}, [${3:dependencies}]);"
            ],
            "description": "React useEffect Hook"
        },
        "Console Log": {
            "prefix": "cl",
            "body": ["console.log('${1:label}:', ${2:value});"],
            "description": "Console log with label"
        }
    }

    with open(os.path.join(SNIPPETS_DIR, 'javascript.json'), 'w') as f:
        json.dump(js_snippets, f, indent=4)
    print(f'Snippets written to: {SNIPPETS_DIR}')


def main():
    # Create the web project
    create_project()

    # Configure VSCode
    configure_vscode_settings()
    configure_keybindings()
    configure_snippets()

    # Ensure no profile export file exists (negative constraint)
    profile_file = os.path.join(WORKDIR, f'{TASK_ID}.code-profile')
    if os.path.exists(profile_file):
        os.remove(profile_file)

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
