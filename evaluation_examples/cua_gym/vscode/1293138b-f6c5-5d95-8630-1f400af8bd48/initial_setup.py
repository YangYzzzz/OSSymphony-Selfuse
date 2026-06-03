"""
Initial Setup: Set up file nesting rules for .spec.ts and .module.css files
Task ID: vscode_lp_064
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
WORKSPACE = f'{WORKDIR}/workspace'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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
    """Create a realistic React TypeScript project structure."""
    # Create directories
    src_dir = f'{WORKSPACE}/src'
    components_dir = f'{src_dir}/components'
    utils_dir = f'{src_dir}/utils'
    hooks_dir = f'{src_dir}/hooks'

    for d in [components_dir, utils_dir, hooks_dir]:
        os.makedirs(d, exist_ok=True)

    # --- Component: Button ---
    with open(f'{components_dir}/Button.tsx', 'w') as f:
        f.write('''import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  onClick: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = 'primary',
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default Button;
''')

    with open(f'{components_dir}/Button.spec.ts', 'w') as f:
        f.write('''import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button Component', () => {
  it('renders with label text', () => {
    render(<Button label="Click Me" onClick={() => {}} />);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('applies primary variant by default', () => {
    const { container } = render(<Button label="Test" onClick={() => {}} />);
    expect(container.firstChild).toHaveClass('primary');
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Click" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
''')

    with open(f'{components_dir}/Button.module.css', 'w') as f:
        f.write('''.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.primary {
  background-color: #3b82f6;
  color: #ffffff;
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
  color: #ffffff;
}
''')

    # --- Component: Header ---
    with open(f'{components_dir}/Header.tsx', 'w') as f:
        f.write('''import React from 'react';
import styles from './Header.module.css';

interface HeaderProps {
  title: string;
  subtitle?: string;
  showNavigation?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  title,
  subtitle,
  showNavigation = true,
}) => {
  return (
    <header className={styles.header}>
      <div className={styles.titleSection}>
        <h1>{title}</h1>
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
''')

    with open(f'{components_dir}/Header.spec.ts', 'w') as f:
        f.write('''import { render, screen } from '@testing-library/react';
import Header from './Header';

describe('Header Component', () => {
  it('renders the title', () => {
    render(<Header title="My App" />);
    expect(screen.getByText('My App')).toBeInTheDocument();
  });

  it('renders subtitle when provided', () => {
    render(<Header title="App" subtitle="Welcome back" />);
    expect(screen.getByText('Welcome back')).toBeInTheDocument();
  });

  it('shows navigation by default', () => {
    render(<Header title="App" />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });
});
''')

    with open(f'{components_dir}/Header.module.css', 'w') as f:
        f.write('''.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #1f2937;
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.titleSection h1 {
  font-size: 24px;
  margin: 0;
}

.subtitle {
  font-size: 14px;
  color: #9ca3af;
  margin: 4px 0 0;
}

.nav {
  display: flex;
  gap: 16px;
}

.nav a {
  color: #d1d5db;
  text-decoration: none;
  font-size: 14px;
}
''')

    # --- Component: DataTable ---
    with open(f'{components_dir}/DataTable.tsx', 'w') as f:
        f.write('''import React from 'react';
import styles from './DataTable.module.css';

interface Column {
  key: string;
  header: string;
  width?: number;
}

interface DataTableProps {
  columns: Column[];
  data: Record<string, any>[];
  onRowClick?: (row: Record<string, any>) => void;
}

export const DataTable: React.FC<DataTableProps> = ({
  columns,
  data,
  onRowClick,
}) => {
  return (
    <table className={styles.table}>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key} style={{ width: col.width }}>
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx} onClick={() => onRowClick?.(row)}>
            {columns.map((col) => (
              <td key={col.key}>{row[col.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;
''')

    with open(f'{components_dir}/DataTable.spec.ts', 'w') as f:
        f.write('''import { render, screen } from '@testing-library/react';
import DataTable from './DataTable';

const mockColumns = [
  { key: 'name', header: 'Name' },
  { key: 'email', header: 'Email' },
  { key: 'role', header: 'Role' },
];

const mockData = [
  { name: 'Sarah Chen', email: 'sarah@example.com', role: 'Engineer' },
  { name: 'Marcus Johnson', email: 'marcus@example.com', role: 'Designer' },
];

describe('DataTable Component', () => {
  it('renders column headers', () => {
    render(<DataTable columns={mockColumns} data={mockData} />);
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Email')).toBeInTheDocument();
  });

  it('renders data rows', () => {
    render(<DataTable columns={mockColumns} data={mockData} />);
    expect(screen.getByText('Sarah Chen')).toBeInTheDocument();
    expect(screen.getByText('marcus@example.com')).toBeInTheDocument();
  });
});
''')

    with open(f'{components_dir}/DataTable.module.css', 'w') as f:
        f.write('''.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table th {
  background-color: #f3f4f6;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #e5e7eb;
}

.table td {
  padding: 10px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.table tr:hover {
  background-color: #f9fafb;
  cursor: pointer;
}
''')

    # --- Utility files ---
    with open(f'{utils_dir}/formatters.ts', 'w') as f:
        f.write('''export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function truncateText(text: string, maxLength: number = 100): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}
''')

    with open(f'{utils_dir}/formatters.spec.ts', 'w') as f:
        f.write('''import { formatCurrency, formatDate, truncateText } from './formatters';

describe('formatCurrency', () => {
  it('formats USD by default', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
  });
});

describe('truncateText', () => {
  it('truncates long text', () => {
    const long = 'A'.repeat(200);
    expect(truncateText(long, 100)).toHaveLength(103);
  });
});
''')

    # --- Hook files ---
    with open(f'{hooks_dir}/useDebounce.ts', 'w') as f:
        f.write('''import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
''')

    with open(f'{hooks_dir}/useDebounce.spec.ts', 'w') as f:
        f.write('''import { renderHook, act } from '@testing-library/react-hooks';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  jest.useFakeTimers();

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('hello', 500));
    expect(result.current).toBe('hello');
  });

  it('updates value after delay', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'hello' } }
    );
    rerender({ value: 'world' });
    act(() => jest.advanceTimersByTime(500));
    expect(result.current).toBe('world');
  });
});
''')

    # --- Root project files ---
    with open(f'{WORKSPACE}/package.json', 'w') as f:
        f.write('''{
  "name": "analytics-dashboard",
  "version": "1.2.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest --coverage",
    "lint": "eslint src/ --ext .ts,.tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "^14.0.0",
    "typescript": "^5.3.0"
  },
  "devDependencies": {
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.0"
  }
}
''')

    with open(f'{WORKSPACE}/tsconfig.json', 'w') as f:
        f.write('''{
  "compilerOptions": {
    "target": "es2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules"]
}
''')

    with open(f'{src_dir}/App.tsx', 'w') as f:
        f.write('''import React from 'react';
import Header from './components/Header';
import DataTable from './components/DataTable';
import Button from './components/Button';

const columns = [
  { key: 'name', header: 'Employee', width: 200 },
  { key: 'department', header: 'Department', width: 150 },
  { key: 'revenue', header: 'Revenue ($)', width: 120 },
];

const data = [
  { name: 'Sarah Chen', department: 'Engineering', revenue: 45230 },
  { name: 'Marcus Johnson', department: 'Marketing', revenue: 38750 },
  { name: 'Priya Patel', department: 'Sales', revenue: 62100 },
  { name: 'James Wilson', department: 'Engineering', revenue: 51890 },
];

function App() {
  return (
    <div>
      <Header title="Analytics Dashboard" subtitle="Q4 2025 Performance" />
      <main style={{ padding: 24 }}>
        <DataTable columns={columns} data={data} />
        <Button label="Export Report" onClick={() => console.log('export')} />
      </main>
    </div>
  );
}

export default App;
''')

    print(f'Project created at: {WORKSPACE}')


def setup_vscode_settings():
    """Set up VSCode settings WITHOUT file nesting (that's the task)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Add some standard settings but NO file nesting config
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "typescript.updateImportsOnFileMove.enabled": "always",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })

    # Ensure no file nesting settings exist
    settings.pop("explorer.fileNesting.enabled", None)
    settings.pop("explorer.fileNesting.patterns", None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to: {SETTINGS_PATH}')


def main():
    create_project()
    setup_vscode_settings()

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
