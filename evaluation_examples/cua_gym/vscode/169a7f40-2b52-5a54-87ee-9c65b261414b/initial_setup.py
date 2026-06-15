"""
Initial Setup: Configure file nesting in VSCode explorer
Task ID: vscode_web_032
Domain: vscode

Creates a React project with component files (tsx, module.css, test.tsx)
and opens VSCode with default settings (no file nesting configured).
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_032'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')
COMPONENTS_DIR = os.path.join(PROJECT_DIR, 'src', 'components')
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


# ---------- Component file templates ----------

COMPONENTS = {
    'Button': {
        'tsx': '''\
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ label, onClick, variant = 'primary', disabled = false }) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};

export default Button;
''',
        'module.css': '''\
.button {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s ease;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.primary:hover {
  background-color: #2563eb;
}

.secondary {
  background-color: #e5e7eb;
  color: #374151;
}

.danger {
  background-color: #ef4444;
  color: white;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
''',
        'test.tsx': '''\
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Submit" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Submit'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button label="Save" onClick={() => {}} disabled />);
    expect(screen.getByText('Save')).toBeDisabled();
  });
});
''',
    },
    'Header': {
        'tsx': '''\
import React from 'react';
import styles from './Header.module.css';

interface HeaderProps {
  title: string;
  subtitle?: string;
  showNavigation?: boolean;
}

const Header: React.FC<HeaderProps> = ({ title, subtitle, showNavigation = true }) => {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <h1 className={styles.title}>{title}</h1>
        {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
      </div>
      {showNavigation && (
        <nav className={styles.nav}>
          <a href="/dashboard">Dashboard</a>
          <a href="/settings">Settings</a>
          <a href="/profile">Profile</a>
        </nav>
      )}
    </header>
  );
};

export default Header;
''',
        'module.css': '''\
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #1e293b;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand {
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 20px;
  margin: 0;
}

.subtitle {
  font-size: 13px;
  color: #94a3b8;
  margin: 4px 0 0;
}

.nav {
  display: flex;
  gap: 20px;
}

.nav a {
  color: #cbd5e1;
  text-decoration: none;
  font-size: 14px;
}

.nav a:hover {
  color: white;
}
''',
        'test.tsx': '''\
import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from './Header';

describe('Header', () => {
  it('renders title', () => {
    render(<Header title="My App" />);
    expect(screen.getByText('My App')).toBeInTheDocument();
  });

  it('renders subtitle when provided', () => {
    render(<Header title="Dashboard" subtitle="Welcome back" />);
    expect(screen.getByText('Welcome back')).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(<Header title="App" />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
  });
});
''',
    },
    'Sidebar': {
        'tsx': '''\
import React, { useState } from 'react';
import styles from './Sidebar.module.css';

interface SidebarItem {
  id: string;
  label: string;
  icon: string;
  href: string;
}

interface SidebarProps {
  items: SidebarItem[];
  collapsed?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ items, collapsed = false }) => {
  const [activeItem, setActiveItem] = useState<string>(items[0]?.id || '');

  return (
    <aside className={`${styles.sidebar} ${collapsed ? styles.collapsed : ''}`}>
      <ul className={styles.menu}>
        {items.map((item) => (
          <li
            key={item.id}
            className={`${styles.menuItem} ${activeItem === item.id ? styles.active : ''}`}
            onClick={() => setActiveItem(item.id)}
          >
            <span className={styles.icon}>{item.icon}</span>
            {!collapsed && <span className={styles.label}>{item.label}</span>}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
''',
        'module.css': '''\
.sidebar {
  width: 240px;
  background-color: #f8fafc;
  border-right: 1px solid #e2e8f0;
  padding: 12px 0;
  height: 100vh;
  transition: width 0.2s ease;
}

.collapsed {
  width: 60px;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menuItem {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  cursor: pointer;
  color: #475569;
  transition: background-color 0.15s ease;
}

.menuItem:hover {
  background-color: #e2e8f0;
}

.active {
  background-color: #dbeafe;
  color: #1d4ed8;
  font-weight: 500;
}

.icon {
  font-size: 18px;
  width: 28px;
  text-align: center;
}

.label {
  margin-left: 10px;
  font-size: 14px;
}
''',
        'test.tsx': '''\
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Sidebar from './Sidebar';

const mockItems = [
  { id: 'home', label: 'Home', icon: 'H', href: '/' },
  { id: 'analytics', label: 'Analytics', icon: 'A', href: '/analytics' },
  { id: 'reports', label: 'Reports', icon: 'R', href: '/reports' },
];

describe('Sidebar', () => {
  it('renders all menu items', () => {
    render(<Sidebar items={mockItems} />);
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Analytics')).toBeInTheDocument();
    expect(screen.getByText('Reports')).toBeInTheDocument();
  });

  it('highlights active item on click', () => {
    render(<Sidebar items={mockItems} />);
    fireEvent.click(screen.getByText('Analytics'));
    // Active state should be applied
  });
});
''',
    },
    'Card': {
        'tsx': '''\
import React from 'react';
import styles from './Card.module.css';

interface CardProps {
  title: string;
  description: string;
  imageUrl?: string;
  footer?: React.ReactNode;
}

const Card: React.FC<CardProps> = ({ title, description, imageUrl, footer }) => {
  return (
    <div className={styles.card}>
      {imageUrl && (
        <div className={styles.imageContainer}>
          <img src={imageUrl} alt={title} className={styles.image} />
        </div>
      )}
      <div className={styles.body}>
        <h3 className={styles.title}>{title}</h3>
        <p className={styles.description}>{description}</p>
      </div>
      {footer && <div className={styles.footer}>{footer}</div>}
    </div>
  );
};

export default Card;
''',
        'module.css': '''\
.card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.imageContainer {
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.body {
  padding: 16px;
}

.title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  color: #1e293b;
}

.description {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.footer {
  padding: 12px 16px;
  border-top: 1px solid #e2e8f0;
  background-color: #f8fafc;
}
''',
        'test.tsx': '''\
import React from 'react';
import { render, screen } from '@testing-library/react';
import Card from './Card';

describe('Card', () => {
  it('renders title and description', () => {
    render(<Card title="Project Alpha" description="A cutting-edge web application" />);
    expect(screen.getByText('Project Alpha')).toBeInTheDocument();
    expect(screen.getByText('A cutting-edge web application')).toBeInTheDocument();
  });

  it('renders image when imageUrl is provided', () => {
    render(
      <Card
        title="Photo Gallery"
        description="Browse latest photos"
        imageUrl="/images/gallery.jpg"
      />
    );
    expect(screen.getByAltText('Photo Gallery')).toBeInTheDocument();
  });

  it('renders footer when provided', () => {
    render(
      <Card
        title="Task"
        description="Complete the sprint"
        footer={<span>Due: March 15</span>}
      />
    );
    expect(screen.getByText('Due: March 15')).toBeInTheDocument();
  });
});
''',
    },
}

# Additional project files
PACKAGE_JSON = '''\
{
  "name": "react-app",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^5.3.3"
  },
  "devDependencies": {
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.2.0",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "jest": "^29.7.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}
'''

TSCONFIG_JSON = '''\
{
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
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
'''

APP_TSX = '''\
import React from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Card from './components/Card';
import Button from './components/Button';

const sidebarItems = [
  { id: 'dashboard', label: 'Dashboard', icon: 'D', href: '/dashboard' },
  { id: 'projects', label: 'Projects', icon: 'P', href: '/projects' },
  { id: 'team', label: 'Team', icon: 'T', href: '/team' },
  { id: 'settings', label: 'Settings', icon: 'S', href: '/settings' },
];

const App: React.FC = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Header title="React Dashboard" subtitle="Component Library Demo" />
      <div style={{ display: 'flex', flex: 1 }}>
        <Sidebar items={sidebarItems} />
        <main style={{ flex: 1, padding: '24px', background: '#f1f5f9' }}>
          <h2>Welcome to the Dashboard</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginTop: '16px' }}>
            <Card title="Active Users" description="1,247 users online right now" />
            <Card title="Revenue" description="$45,230 this month" />
            <Card title="Tasks" description="23 tasks pending review" />
          </div>
          <div style={{ marginTop: '24px' }}>
            <Button label="Create New Project" onClick={() => alert('New project')} variant="primary" />
          </div>
        </main>
      </div>
    </div>
  );
};

export default App;
'''


def create_initial():
    # Create project structure
    os.makedirs(COMPONENTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)

    # Write component files
    for comp_name, files in COMPONENTS.items():
        for file_type, content in files.items():
            if file_type == 'tsx':
                filename = f'{comp_name}.tsx'
            elif file_type == 'module.css':
                filename = f'{comp_name}.module.css'
            elif file_type == 'test.tsx':
                filename = f'{comp_name}.test.tsx'
            filepath = os.path.join(COMPONENTS_DIR, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f'Created: {filepath}')

    # Write App.tsx
    app_path = os.path.join(PROJECT_DIR, 'src', 'App.tsx')
    with open(app_path, 'w') as f:
        f.write(APP_TSX)
    print(f'Created: {app_path}')

    # Write package.json
    pkg_path = os.path.join(PROJECT_DIR, 'package.json')
    with open(pkg_path, 'w') as f:
        f.write(PACKAGE_JSON)
    print(f'Created: {pkg_path}')

    # Write tsconfig.json
    tsc_path = os.path.join(PROJECT_DIR, 'tsconfig.json')
    with open(tsc_path, 'w') as f:
        f.write(TSCONFIG_JSON)
    print(f'Created: {tsc_path}')

    # Ensure VSCode settings directory exists but do NOT set any fileNesting settings
    os.makedirs(VSCODE_USER, exist_ok=True)
    # Load existing settings or create empty
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Make sure no fileNesting settings exist
    keys_to_remove = [k for k in settings if 'fileNesting' in k]
    for k in keys_to_remove:
        del settings[k]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Settings cleaned (no fileNesting): {SETTINGS_PATH}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
