"""
Initial Setup: Set up auto-import suggestions for React components
Task ID: vscode_web_025
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_025'
PROJECT_DIR = f'{WORKDIR}/projects/react-ts-app'


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
    os.makedirs(f'{PROJECT_DIR}/src/pages', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "react-ts-app",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "typescript": "^5.3.3"
        },
        "devDependencies": {
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
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
            "jsx": "react-jsx",
            "baseUrl": "src"
        },
        "include": ["src"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- .vscode/settings.json (empty / minimal, NO TypeScript settings) ---
    vscode_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 2
    }
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # --- src/components/Button.tsx ---
    button_tsx = '''import React from 'react';

interface ButtonProps {
    label: string;
    onClick: () => void;
    variant?: 'primary' | 'secondary' | 'danger';
    disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
    label,
    onClick,
    variant = 'primary',
    disabled = false,
}) => {
    const getClassName = () => {
        const base = 'btn';
        return `${base} btn-${variant}`;
    };

    return (
        <button
            className={getClassName()}
            onClick={onClick}
            disabled={disabled}
        >
            {label}
        </button>
    );
};

export default Button;
'''
    with open(f'{PROJECT_DIR}/src/components/Button.tsx', 'w') as f:
        f.write(button_tsx)

    # --- src/components/Card.tsx ---
    card_tsx = '''import React from 'react';

interface CardProps {
    title: string;
    children: React.ReactNode;
    elevation?: 'low' | 'medium' | 'high';
}

export const Card: React.FC<CardProps> = ({
    title,
    children,
    elevation = 'medium',
}) => {
    return (
        <div className={`card card-elevation-${elevation}`}>
            <div className="card-header">
                <h3>{title}</h3>
            </div>
            <div className="card-body">
                {children}
            </div>
        </div>
    );
};

export default Card;
'''
    with open(f'{PROJECT_DIR}/src/components/Card.tsx', 'w') as f:
        f.write(card_tsx)

    # --- src/components/NavBar.tsx ---
    navbar_tsx = '''import React from 'react';

interface NavItem {
    label: string;
    href: string;
    isActive?: boolean;
}

interface NavBarProps {
    brand: string;
    items: NavItem[];
    onItemClick: (href: string) => void;
}

export const NavBar: React.FC<NavBarProps> = ({
    brand,
    items,
    onItemClick,
}) => {
    return (
        <nav className="navbar">
            <span className="navbar-brand">{brand}</span>
            <ul className="navbar-nav">
                {items.map((item, index) => (
                    <li
                        key={index}
                        className={`nav-item ${item.isActive ? 'active' : ''}`}
                    >
                        <a
                            href={item.href}
                            onClick={(e) => {
                                e.preventDefault();
                                onItemClick(item.href);
                            }}
                        >
                            {item.label}
                        </a>
                    </li>
                ))}
            </ul>
        </nav>
    );
};

export default NavBar;
'''
    with open(f'{PROJECT_DIR}/src/components/NavBar.tsx', 'w') as f:
        f.write(navbar_tsx)

    # --- src/components/index.ts ---
    index_ts = '''export { Button } from './Button';
export { Card } from './Card';
export { NavBar } from './NavBar';
'''
    with open(f'{PROJECT_DIR}/src/components/index.ts', 'w') as f:
        f.write(index_ts)

    # --- src/App.tsx (does NOT import components - that's the task) ---
    app_tsx = '''import React from 'react';

const App: React.FC = () => {
    return (
        <div className="App">
            <h1>Welcome to React TypeScript App</h1>
            <p>Start building your components here.</p>
        </div>
    );
};

export default App;
'''
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write(app_tsx)

    # --- src/index.tsx ---
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
    with open(f'{PROJECT_DIR}/src/index.tsx', 'w') as f:
        f.write(index_tsx)

    # --- src/pages/Dashboard.tsx ---
    dashboard_tsx = '''import React from 'react';

const Dashboard: React.FC = () => {
    return (
        <div className="dashboard">
            <h2>Dashboard</h2>
            <div className="dashboard-grid">
                <div className="metric-card">
                    <h4>Total Users</h4>
                    <span className="metric-value">1,247</span>
                </div>
                <div className="metric-card">
                    <h4>Revenue</h4>
                    <span className="metric-value">$45,230</span>
                </div>
                <div className="metric-card">
                    <h4>Active Sessions</h4>
                    <span className="metric-value">342</span>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
'''
    with open(f'{PROJECT_DIR}/src/pages/Dashboard.tsx', 'w') as f:
        f.write(dashboard_tsx)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Workspace settings: {PROJECT_DIR}/.vscode/settings.json')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
