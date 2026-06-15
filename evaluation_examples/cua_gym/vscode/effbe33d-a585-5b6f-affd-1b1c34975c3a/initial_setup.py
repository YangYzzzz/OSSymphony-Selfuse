"""
Initial Setup: Configure Jest test runner in VSCode - create project structure
Task ID: vscode_web_024
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_024'
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
    os.makedirs(f'{PROJECT_DIR}/__tests__', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/utils', exist_ok=True)

    # package.json with jest and ts-jest as devDependencies
    package_json = {
        "name": "react-ts-app",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "jest",
            "lint": "eslint src/"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^5.3.3"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "ts-jest": "^29.1.2",
            "@types/jest": "^29.5.12",
            "@types/react": "^18.2.55",
            "@types/react-dom": "^18.2.19",
            "@testing-library/react": "^14.2.1",
            "@testing-library/jest-dom": "^6.4.2",
            "jest-environment-jsdom": "^29.7.0"
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

    # src/components/Button.tsx
    with open(f'{PROJECT_DIR}/src/components/Button.tsx', 'w') as f:
        f.write('''import React from 'react';
import './Button.css';

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
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};
''')

    # src/components/Button.css
    with open(f'{PROJECT_DIR}/src/components/Button.css', 'w') as f:
        f.write('''.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
}

.btn-danger {
  background-color: #ef4444;
  color: white;
}
''')

    # src/components/UserCard.tsx
    with open(f'{PROJECT_DIR}/src/components/UserCard.tsx', 'w') as f:
        f.write('''import React from 'react';
import './UserCard.css';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  avatarUrl: string;
}

interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
}

export const UserCard: React.FC<UserCardProps> = ({ user, onSelect }) => {
  return (
    <div className="user-card" onClick={() => onSelect?.(user)}>
      <img src={user.avatarUrl} alt={user.name} className="user-avatar" />
      <div className="user-info">
        <h3>{user.name}</h3>
        <p>{user.email}</p>
        <span className="user-role">{user.role}</span>
      </div>
    </div>
  );
};
''')

    # src/components/UserCard.css
    with open(f'{PROJECT_DIR}/src/components/UserCard.css', 'w') as f:
        f.write('''.user-card {
  display: flex;
  align-items: center;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 12px;
}

.user-info h3 {
  margin: 0 0 4px 0;
  font-size: 16px;
}

.user-role {
  background-color: #dbeafe;
  color: #1e40af;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}
''')

    # src/utils/formatters.ts
    with open(f'{PROJECT_DIR}/src/utils/formatters.ts', 'w') as f:
        f.write('''export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3) + '...';
}

export function capitalizeFirst(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}
''')

    # src/App.tsx
    with open(f'{PROJECT_DIR}/src/App.tsx', 'w') as f:
        f.write('''import React, { useState } from 'react';
import { Button } from './components/Button';
import { UserCard } from './components/UserCard';

const sampleUsers = [
  { id: 1, name: 'Sarah Chen', email: 'sarah.chen@example.com', role: 'Engineering Lead', avatarUrl: '/avatars/sarah.png' },
  { id: 2, name: 'Marcus Johnson', email: 'marcus.j@example.com', role: 'Product Manager', avatarUrl: '/avatars/marcus.png' },
  { id: 3, name: 'Aisha Patel', email: 'aisha.p@example.com', role: 'UX Designer', avatarUrl: '/avatars/aisha.png' },
];

function App() {
  const [selectedUser, setSelectedUser] = useState<typeof sampleUsers[0] | null>(null);

  return (
    <div className="app">
      <h1>Team Directory</h1>
      <div className="user-list">
        {sampleUsers.map(user => (
          <UserCard key={user.id} user={user} onSelect={setSelectedUser} />
        ))}
      </div>
      {selectedUser && (
        <div className="selected-info">
          <p>Selected: {selectedUser.name}</p>
          <Button label="Clear Selection" onClick={() => setSelectedUser(null)} variant="secondary" />
        </div>
      )}
    </div>
  );
}

export default App;
''')

    # __tests__/Button.test.tsx
    with open(f'{PROJECT_DIR}/__tests__/Button.test.tsx', 'w') as f:
        f.write('''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../src/components/Button';

describe('Button Component', () => {
  test('renders with correct label', () => {
    render(<Button label="Click Me" onClick={() => {}} />);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Submit" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Submit'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('applies variant class correctly', () => {
    const { container } = render(
      <Button label="Delete" onClick={() => {}} variant="danger" />
    );
    expect(container.querySelector('.btn-danger')).toBeInTheDocument();
  });

  test('is disabled when disabled prop is true', () => {
    render(<Button label="Disabled" onClick={() => {}} disabled={true} />);
    expect(screen.getByText('Disabled')).toBeDisabled();
  });
});
''')

    # __tests__/formatters.test.tsx
    with open(f'{PROJECT_DIR}/__tests__/formatters.test.tsx', 'w') as f:
        f.write('''import { formatCurrency, truncateText, capitalizeFirst } from '../src/utils/formatters';

describe('Formatter Utilities', () => {
  describe('formatCurrency', () => {
    test('formats USD by default', () => {
      expect(formatCurrency(1234.56)).toBe('$1,234.56');
    });

    test('formats with specified currency', () => {
      const result = formatCurrency(99.99, 'EUR');
      expect(result).toContain('99.99');
    });
  });

  describe('truncateText', () => {
    test('returns original text if shorter than maxLength', () => {
      expect(truncateText('Hello', 10)).toBe('Hello');
    });

    test('truncates with ellipsis if text exceeds maxLength', () => {
      expect(truncateText('Hello World This Is Long', 10)).toBe('Hello W...');
    });
  });

  describe('capitalizeFirst', () => {
    test('capitalizes first letter', () => {
      expect(capitalizeFirst('hello')).toBe('Hello');
    });

    test('returns empty string for empty input', () => {
      expect(capitalizeFirst('')).toBe('');
    });
  });
});
''')

    # __tests__/UserCard.test.tsx
    with open(f'{PROJECT_DIR}/__tests__/UserCard.test.tsx', 'w') as f:
        f.write('''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { UserCard } from '../src/components/UserCard';

const mockUser = {
  id: 1,
  name: 'Sarah Chen',
  email: 'sarah.chen@example.com',
  role: 'Engineering Lead',
  avatarUrl: '/avatars/sarah.png',
};

describe('UserCard Component', () => {
  test('displays user name', () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText('Sarah Chen')).toBeInTheDocument();
  });

  test('displays user email', () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText('sarah.chen@example.com')).toBeInTheDocument();
  });

  test('displays user role badge', () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText('Engineering Lead')).toBeInTheDocument();
  });

  test('calls onSelect when card is clicked', () => {
    const handleSelect = jest.fn();
    render(<UserCard user={mockUser} onSelect={handleSelect} />);
    fireEvent.click(screen.getByText('Sarah Chen'));
    expect(handleSelect).toHaveBeenCalledWith(mockUser);
  });
});
''')

    # NO jest.config.js - the task requires creating it
    # NO orta.vscode-jest extension - the task requires installing it

    print(f'Initial project created: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
