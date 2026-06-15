"""
Initial Setup: Configure VSCode TypeScript workspace version
Task ID: vscode_web_086
Domain: vscode

Creates a React+TypeScript project with TypeScript 5.4 installed in node_modules,
while VSCode is using its built-in TypeScript 5.2. The user needs to switch to
the workspace version.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_086'
PROJECT_DIR = f'{WORKDIR}/projects/react-ts-app'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
VSCODE_PROJECT_SETTINGS = f'{PROJECT_DIR}/.vscode'


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
    """Create a realistic React+TypeScript project structure."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json
    package_json = {
        "name": "react-ts-app",
        "version": "1.0.0",
        "private": True,
        "description": "Employee Dashboard - React TypeScript Application",
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^5.4.2",
            "web-vitals": "^3.5.2"
        },
        "devDependencies": {
            "@types/react": "^18.2.65",
            "@types/react-dom": "^18.2.22"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
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

    # Create src directory
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/components', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/public', exist_ok=True)

    # src/App.tsx - Uses TypeScript 5.4 features (NoInfer utility type)
    app_tsx = '''\
import React, { useState } from 'react';
import { EmployeeDashboard } from './components/EmployeeDashboard';
import { ThemeProvider } from './components/ThemeProvider';

// TypeScript 5.4 feature: NoInfer utility type
function createConfig<T>(defaults: T, overrides?: NoInfer<Partial<T>>): T {
  return { ...defaults, ...overrides };
}

interface AppConfig {
  title: string;
  maxItems: number;
  theme: 'light' | 'dark';
  refreshInterval: number;
}

const appConfig = createConfig<AppConfig>({
  title: 'Employee Dashboard',
  maxItems: 50,
  theme: 'light',
  refreshInterval: 30000,
});

function App() {
  const [config] = useState(appConfig);

  return (
    <ThemeProvider theme={config.theme}>
      <div className="App">
        <header>
          <h1>{config.title}</h1>
        </header>
        <main>
          <EmployeeDashboard maxItems={config.maxItems} />
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;
'''
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write(app_tsx)

    # src/components/EmployeeDashboard.tsx
    dashboard_tsx = '''\
import React, { useState, useEffect } from 'react';

interface Employee {
  id: number;
  name: string;
  department: string;
  salary: number;
  startDate: string;
  isActive: boolean;
}

interface DashboardProps {
  maxItems: number;
}

// TypeScript 5.4 feature: Improved type narrowing in closures
export function EmployeeDashboard({ maxItems }: DashboardProps) {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [filter, setFilter] = useState<string | null>(null);

  useEffect(() => {
    const sampleData: Employee[] = [
      { id: 1, name: 'Sarah Chen', department: 'Engineering', salary: 125000, startDate: '2022-03-15', isActive: true },
      { id: 2, name: 'Marcus Johnson', department: 'Marketing', salary: 92000, startDate: '2021-08-01', isActive: true },
      { id: 3, name: 'Priya Patel', department: 'Engineering', salary: 118000, startDate: '2023-01-10', isActive: true },
      { id: 4, name: 'David Kim', department: 'Finance', salary: 105000, startDate: '2020-11-20', isActive: false },
      { id: 5, name: 'Elena Rodriguez', department: 'Product', salary: 135000, startDate: '2022-06-15', isActive: true },
      { id: 6, name: 'James Wright', department: 'Engineering', salary: 142000, startDate: '2019-04-01', isActive: true },
      { id: 7, name: 'Aisha Mohammed', department: 'Marketing', salary: 88000, startDate: '2023-09-12', isActive: true },
      { id: 8, name: 'Carlos Mendez', department: 'Finance', salary: 97000, startDate: '2021-02-28', isActive: true },
    ];
    setEmployees(sampleData.slice(0, maxItems));
  }, [maxItems]);

  // TypeScript 5.4: Better narrowing after last assignment
  const filtered = filter !== null
    ? employees.filter(e => e.department === filter)
    : employees;

  const departments = [...new Set(employees.map(e => e.department))];

  return (
    <div>
      <div className="filters">
        <button onClick={() => setFilter(null)}>All</button>
        {departments.map(dept => (
          <button key={dept} onClick={() => setFilter(dept)}>
            {dept}
          </button>
        ))}
      </div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Department</th>
            <th>Salary</th>
            <th>Start Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(emp => (
            <tr key={emp.id}>
              <td>{emp.name}</td>
              <td>{emp.department}</td>
              <td>${emp.salary.toLocaleString()}</td>
              <td>{emp.startDate}</td>
              <td>{emp.isActive ? 'Active' : 'Inactive'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
'''
    with open(f'{PROJECT_DIR}/src/components/EmployeeDashboard.tsx', 'w') as f:
        f.write(dashboard_tsx)

    # src/components/ThemeProvider.tsx
    theme_tsx = '''\
import React, { createContext, useContext, ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
}

const ThemeContext = createContext<ThemeContextType>({ theme: 'light' });

interface ThemeProviderProps {
  theme: Theme;
  children: ReactNode;
}

export function ThemeProvider({ theme, children }: ThemeProviderProps) {
  return (
    <ThemeContext.Provider value={{ theme }}>
      <div data-theme={theme}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextType {
  return useContext(ThemeContext);
}
'''
    with open(f'{PROJECT_DIR}/src/components/ThemeProvider.tsx', 'w') as f:
        f.write(theme_tsx)

    # src/index.tsx
    index_tsx = '''\
import React from 'react';
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
    with open(f'{PROJECT_DIR}/src/index.tsx', 'w') as f:
        f.write(index_tsx)

    # public/index.html
    index_html = '''\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Employee Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
'''
    with open(f'{PROJECT_DIR}/public/index.html', 'w') as f:
        f.write(index_html)

    print(f'Project created at: {PROJECT_DIR}')


def create_node_modules_typescript():
    """Create a fake TypeScript 5.4 installation in node_modules."""
    ts_lib_dir = f'{PROJECT_DIR}/node_modules/typescript/lib'
    os.makedirs(ts_lib_dir, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/typescript/bin', exist_ok=True)

    # TypeScript package.json (this is what VSCode reads to determine version)
    ts_package = {
        "name": "typescript",
        "version": "5.4.2",
        "description": "TypeScript is a language for application scale JavaScript development",
        "main": "./lib/typescript.js",
        "typesVersions": {"*": {"*": ["lib/*"]}},
        "bin": {
            "tsc": "./bin/tsc",
            "tsserver": "./bin/tsserver"
        }
    }
    with open(f'{PROJECT_DIR}/node_modules/typescript/package.json', 'w') as f:
        json.dump(ts_package, f, indent=2)

    # Create minimal tsserver.js stub (VSCode tries to load this)
    tsserver_stub = '''\
// Stub tsserver.js for TypeScript 5.4.2
// This is a minimal stub to allow VSCode to detect the workspace version.
"use strict";
module.exports = require("./typescript.js");
'''
    with open(f'{ts_lib_dir}/tsserver.js', 'w') as f:
        f.write(tsserver_stub)

    # Create minimal typescript.js stub
    typescript_stub = '''\
// Stub typescript.js for TypeScript 5.4.2
"use strict";
module.exports = {
    version: "5.4.2",
    sys: undefined,
    ScriptTarget: {},
    ModuleKind: {}
};
'''
    with open(f'{ts_lib_dir}/typescript.js', 'w') as f:
        f.write(typescript_stub)

    # Create tsc bin stub
    tsc_stub = '''\
#!/usr/bin/env node
require("../lib/typescript.js");
'''
    with open(f'{PROJECT_DIR}/node_modules/typescript/bin/tsc', 'w') as f:
        f.write(tsc_stub)
    os.chmod(f'{PROJECT_DIR}/node_modules/typescript/bin/tsc', 0o755)

    # Create tsserver bin stub
    tsserver_bin = '''\
#!/usr/bin/env node
require("../lib/tsserver.js");
'''
    with open(f'{PROJECT_DIR}/node_modules/typescript/bin/tsserver', 'w') as f:
        f.write(tsserver_bin)
    os.chmod(f'{PROJECT_DIR}/node_modules/typescript/bin/tsserver', 0o755)

    # Create node_modules/.package-lock.json for realism
    os.makedirs(f'{PROJECT_DIR}/node_modules/.cache', exist_ok=True)

    print(f'TypeScript 5.4.2 installed in: {ts_lib_dir}')


def setup_vscode_settings():
    """Configure VSCode user settings - NO typescript.tsdk (using built-in TS 5.2)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # User-level settings - typical developer setup, no typescript.tsdk
    user_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "terminal.integrated.fontSize": 13,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }

    settings_path = f'{VSCODE_USER}/settings.json'
    with open(settings_path, 'w') as f:
        json.dump(user_settings, f, indent=4)

    # Ensure NO workspace-level .vscode/settings.json with typescript.tsdk
    # Create the .vscode dir but with only minimal workspace settings (no tsdk)
    os.makedirs(VSCODE_PROJECT_SETTINGS, exist_ok=True)
    workspace_settings = {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    }
    with open(f'{VSCODE_PROJECT_SETTINGS}/settings.json', 'w') as f:
        json.dump(workspace_settings, f, indent=4)

    print('VSCode settings configured (no typescript.tsdk)')


def main():
    create_project()
    create_node_modules_typescript()
    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with react-ts-app project')


main()
