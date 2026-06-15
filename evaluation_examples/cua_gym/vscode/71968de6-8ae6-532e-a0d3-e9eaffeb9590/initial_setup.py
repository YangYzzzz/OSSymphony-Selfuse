"""
Initial Setup: Configure VSCode to auto-organize imports on save for TypeScript
Task ID: vscode_web_094
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_094'
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
PROJECT_DIR = os.path.join(HOME, "projects", "react-ts-app")


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
    """Create a realistic React TypeScript project with messy imports."""
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "components"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "hooks"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, "src", "utils"), exist_ok=True)

    # package.json
    pkg = {
        "name": "react-ts-app",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "typescript": "^5.3.0",
            "axios": "^1.6.0"
        },
        "devDependencies": {
            "eslint": "^8.50.0",
            "@typescript-eslint/parser": "^6.7.0",
            "@typescript-eslint/eslint-plugin": "^6.7.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, "package.json"), "w") as f:
        json.dump(pkg, f, indent=2)

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
    with open(os.path.join(PROJECT_DIR, "tsconfig.json"), "w") as f:
        json.dump(tsconfig, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "parser": "@typescript-eslint/parser",
        "plugins": ["@typescript-eslint"],
        "extends": [
            "eslint:recommended",
            "plugin:@typescript-eslint/recommended"
        ],
        "rules": {
            "no-unused-vars": "warn",
            "@typescript-eslint/no-unused-vars": "warn"
        }
    }
    with open(os.path.join(PROJECT_DIR, ".eslintrc.json"), "w") as f:
        json.dump(eslintrc, f, indent=2)

    # src/App.tsx - with unsorted and unused imports
    app_tsx = '''import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { UserProfile } from './components/UserProfile';
import { formatCurrency, formatDate, capitalizeFirst } from './utils/formatters';
import { DashboardHeader } from './components/DashboardHeader';
import { useLocalStorage } from './hooks/useLocalStorage';
import { DataTable } from './components/DataTable';

interface AppState {
  users: User[];
  loading: boolean;
  error: string | null;
}

interface User {
  id: number;
  name: string;
  email: string;
  department: string;
  salary: number;
  startDate: string;
}

const App: React.FC = () => {
  const [state, setState] = useState<AppState>({
    users: [],
    loading: true,
    error: null,
  });
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/users');
        setState({ users: response.data, loading: false, error: null });
      } catch (err) {
        setState({ users: [], loading: false, error: 'Failed to load users' });
      }
    };
    fetchUsers();
  }, []);

  if (state.loading) return <div>Loading...</div>;
  if (state.error) return <div>Error: {state.error}</div>;

  return (
    <div className={`app ${theme}`}>
      <DashboardHeader title="Employee Dashboard" onToggleTheme={() => setTheme(theme === 'light' ? 'dark' : 'light')} />
      <DataTable users={state.users} />
    </div>
  );
};

export default App;
'''
    with open(os.path.join(PROJECT_DIR, "src", "App.tsx"), "w") as f:
        f.write(app_tsx)

    # src/components/UserProfile.tsx - unused import
    user_profile = '''import React, { memo, useMemo } from 'react';
import { formatDate } from '../utils/formatters';
import { capitalizeFirst } from '../utils/formatters';

interface UserProfileProps {
  name: string;
  email: string;
  department: string;
  startDate: string;
}

export const UserProfile: React.FC<UserProfileProps> = memo(({ name, email, department, startDate }) => {
  return (
    <div className="user-profile">
      <h3>{name}</h3>
      <p>{email}</p>
      <p>Department: {department}</p>
      <p>Started: {formatDate(startDate)}</p>
    </div>
  );
});
'''
    with open(os.path.join(PROJECT_DIR, "src", "components", "UserProfile.tsx"), "w") as f:
        f.write(user_profile)

    # src/components/DashboardHeader.tsx
    dashboard_header = '''import React from 'react';

interface DashboardHeaderProps {
  title: string;
  onToggleTheme: () => void;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({ title, onToggleTheme }) => {
  return (
    <header className="dashboard-header">
      <h1>{title}</h1>
      <button onClick={onToggleTheme}>Toggle Theme</button>
    </header>
  );
};
'''
    with open(os.path.join(PROJECT_DIR, "src", "components", "DashboardHeader.tsx"), "w") as f:
        f.write(dashboard_header)

    # src/components/DataTable.tsx - unsorted imports
    data_table = '''import React, { useState, useMemo } from 'react';
import { formatCurrency } from '../utils/formatters';
import { UserProfile } from './UserProfile';

interface User {
  id: number;
  name: string;
  email: string;
  department: string;
  salary: number;
  startDate: string;
}

interface DataTableProps {
  users: User[];
}

export const DataTable: React.FC<DataTableProps> = ({ users }) => {
  const [sortField, setSortField] = useState<keyof User>('name');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc');

  const sorted = useMemo(() => {
    return [...users].sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];
      if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
  }, [users, sortField, sortDir]);

  return (
    <table>
      <thead>
        <tr>
          <th onClick={() => setSortField('name')}>Name</th>
          <th onClick={() => setSortField('department')}>Department</th>
          <th onClick={() => setSortField('salary')}>Salary</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map(user => (
          <tr key={user.id}>
            <td>{user.name}</td>
            <td>{user.department}</td>
            <td>{formatCurrency(user.salary)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
'''
    with open(os.path.join(PROJECT_DIR, "src", "components", "DataTable.tsx"), "w") as f:
        f.write(data_table)

    # src/hooks/useLocalStorage.ts
    use_local_storage = '''import { useState, useEffect, useCallback } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = useCallback((value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key]);

  return [storedValue, setValue];
}
'''
    with open(os.path.join(PROJECT_DIR, "src", "hooks", "useLocalStorage.ts"), "w") as f:
        f.write(use_local_storage)

    # src/utils/formatters.ts
    formatters = '''export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function capitalizeFirst(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + '...';
}
'''
    with open(os.path.join(PROJECT_DIR, "src", "utils", "formatters.ts"), "w") as f:
        f.write(formatters)

    print(f"Project created: {PROJECT_DIR}")


def setup_vscode_settings():
    """Configure VSCode with ESLint auto-fix on save but NO organize imports."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # ESLint auto-fix on save is already configured (per task context)
    # But NO organizeImports setting — that's the task
    settings.update({
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.codeActionsOnSave": {
            "source.fixAll.eslint": "explicit"
        },
        "eslint.validate": [
            "javascript",
            "javascriptreact",
            "typescript",
            "typescriptreact"
        ],
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.tabSize": 2,
        "files.autoSave": "off"
    })

    # MUST NOT include any organizeImports or language-scoped settings for [typescript]/[typescriptreact]
    # Remove them if they exist
    for key in list(settings.keys()):
        if key in ("[typescript]", "[typescriptreact]"):
            if "editor.codeActionsOnSave" in settings[key]:
                if "source.organizeImports" in settings[key]["editor.codeActionsOnSave"]:
                    del settings[key]["editor.codeActionsOnSave"]["source.organizeImports"]
                    if not settings[key]["editor.codeActionsOnSave"]:
                        del settings[key]["editor.codeActionsOnSave"]
                    if not settings[key]:
                        del settings[key]

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings configured: {SETTINGS_PATH}")
    print("  - ESLint auto-fix on save: enabled")
    print("  - Organize imports on save: NOT configured (this is the task)")


def main():
    create_project()
    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f"GUI_READY: VSCode launched with {PROJECT_DIR}")


main()
