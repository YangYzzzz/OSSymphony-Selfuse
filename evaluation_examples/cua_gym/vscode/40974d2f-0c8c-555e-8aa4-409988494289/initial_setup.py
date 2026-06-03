"""
Initial Setup: Copy relative path of Header.tsx and paste into App.tsx import
Task ID: vscode_lp_065
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_065'
PROJECT_DIR = f'{WORKDIR}/workspace'
SRC_DIR = f'{PROJECT_DIR}/src'
COMPONENTS_DIR = f'{SRC_DIR}/components'


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
    os.makedirs(COMPONENTS_DIR, exist_ok=True)

    # --- package.json ---
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write('''{
  "name": "dashboard-app",
  "version": "1.2.0",
  "private": true,
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
''')

    # --- tsconfig.json ---
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        f.write('''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
''')

    # --- src/index.tsx ---
    with open(f'{SRC_DIR}/index.tsx', 'w') as f:
        f.write('''import React from 'react';
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
''')

    # --- src/components/Header.tsx ---
    with open(f'{COMPONENTS_DIR}/Header.tsx', 'w') as f:
        f.write('''import React from 'react';

interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Dashboard' }) => {
  return (
    <header className="app-header">
      <nav className="header-nav">
        <h1>{title}</h1>
        <ul className="nav-links">
          <li><a href="/home">Home</a></li>
          <li><a href="/reports">Reports</a></li>
          <li><a href="/settings">Settings</a></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
''')

    # --- src/components/Sidebar.tsx ---
    with open(f'{COMPONENTS_DIR}/Sidebar.tsx', 'w') as f:
        f.write('''import React from 'react';

const Sidebar: React.FC = () => {
  const menuItems = [
    { label: 'Overview', icon: 'dashboard' },
    { label: 'Analytics', icon: 'chart' },
    { label: 'Users', icon: 'people' },
    { label: 'Notifications', icon: 'bell' },
  ];

  return (
    <aside className="sidebar">
      <ul>
        {menuItems.map((item) => (
          <li key={item.label}>
            <span className={`icon-${item.icon}`} />
            {item.label}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
''')

    # --- src/App.tsx (INITIAL STATE: incomplete import) ---
    with open(f'{SRC_DIR}/App.tsx', 'w') as f:
        f.write('''import React from 'react';
import Sidebar from './components/Sidebar';
// TODO: import Header from its relative path

const App: React.FC = () => {
  return (
    <div className="app-container">
      {/* Header component needs to be imported above */}
      <Sidebar />
      <main className="content">
        <h2>Welcome to the Dashboard</h2>
        <p>Select a section from the sidebar to get started.</p>
      </main>
    </div>
  );
};

export default App;
''')

    # --- src/App.css ---
    with open(f'{SRC_DIR}/App.css', 'w') as f:
        f.write('''.app-container {
  display: flex;
  min-height: 100vh;
}

.app-header {
  background-color: #1a1a2e;
  color: #ffffff;
  padding: 0 24px;
}

.header-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 16px;
}

.sidebar {
  width: 220px;
  background-color: #16213e;
  color: #e0e0e0;
  padding: 16px;
}

.content {
  flex: 1;
  padding: 24px;
  background-color: #f4f4f8;
}
''')

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'App.tsx location: {SRC_DIR}/App.tsx')

    # Open VSCode with the project workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open App.tsx specifically so the agent sees it
    launch_gui(f'code "{SRC_DIR}/App.tsx"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
