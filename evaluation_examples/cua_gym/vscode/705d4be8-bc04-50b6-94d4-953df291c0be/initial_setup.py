"""
Initial Setup: Create a React TypeScript project with Jest tests, no debug config.
Task ID: vscode_web_056
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-ts-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')

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
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'utils', '__tests__'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'components'), exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "react-ts-app",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "typescript": "^4.9.5"
        },
        "devDependencies": {
            "@testing-library/jest-dom": "^5.16.5",
            "@testing-library/react": "^14.0.0",
            "@types/jest": "^29.5.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "jest": "^29.5.0",
            "ts-jest": "^29.1.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
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
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- jest.config.js ---
    jest_config = """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts?(x)', '**/?(*.)+(spec|test).ts?(x)'],
  transform: {
    '^.+\\\\.tsx?$': 'ts-jest'
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts'
  ]
};
"""
    with open(os.path.join(PROJECT_DIR, 'jest.config.js'), 'w') as f:
        f.write(jest_config)

    # --- src/utils/helpers.ts (the module under test) ---
    helpers_ts = """/**
 * Utility helper functions for the React TS App.
 * Used across various components for data processing.
 */

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function calculateDiscount(
  originalPrice: number,
  discountPercent: number
): number {
  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error('Discount percentage must be between 0 and 100');
  }
  return originalPrice * (1 - discountPercent / 100);
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\\w\\s-]/g, '')
    .replace(/[\\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3) + '...';
}

export function groupBy<T>(array: T[], key: keyof T): Record<string, T[]> {
  return array.reduce((result, item) => {
    const groupKey = String(item[key]);
    if (!result[groupKey]) {
      result[groupKey] = [];
    }
    result[groupKey].push(item);
    return result;
  }, {} as Record<string, T[]>);
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  waitMs: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), waitMs);
  };
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'utils', 'helpers.ts'), 'w') as f:
        f.write(helpers_ts)

    # --- src/utils/__tests__/helpers.test.ts (file to be debugged) ---
    helpers_test_ts = """import {
  formatCurrency,
  calculateDiscount,
  slugify,
  truncateText,
  groupBy,
} from '../helpers';

describe('formatCurrency', () => {
  it('should format USD amounts correctly', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
    expect(formatCurrency(0)).toBe('$0.00');
    expect(formatCurrency(999999.99)).toBe('$999,999.99');
  });

  it('should handle EUR currency', () => {
    const result = formatCurrency(45.5, 'EUR');
    expect(result).toContain('45.50');
  });

  it('should round to two decimal places', () => {
    expect(formatCurrency(19.999)).toBe('$20.00');
    expect(formatCurrency(100.001)).toBe('$100.00');
  });
});

describe('calculateDiscount', () => {
  it('should apply discount correctly', () => {
    expect(calculateDiscount(100, 20)).toBe(80);
    expect(calculateDiscount(250, 10)).toBe(225);
    expect(calculateDiscount(50, 50)).toBe(25);
  });

  it('should handle 0% discount', () => {
    expect(calculateDiscount(100, 0)).toBe(100);
  });

  it('should handle 100% discount', () => {
    expect(calculateDiscount(100, 100)).toBe(0);
  });

  it('should throw for invalid discount percentages', () => {
    expect(() => calculateDiscount(100, -5)).toThrow();
    expect(() => calculateDiscount(100, 150)).toThrow();
  });
});

describe('slugify', () => {
  it('should convert text to URL-friendly slugs', () => {
    expect(slugify('Hello World')).toBe('hello-world');
    expect(slugify('React TypeScript App')).toBe('react-typescript-app');
  });

  it('should handle special characters', () => {
    expect(slugify('Price: $100!')).toBe('price-100');
    expect(slugify('hello---world')).toBe('hello-world');
  });

  it('should trim leading and trailing dashes', () => {
    expect(slugify('  Hello World  ')).toBe('hello-world');
  });
});

describe('truncateText', () => {
  it('should truncate long text with ellipsis', () => {
    expect(truncateText('This is a very long sentence', 15)).toBe('This is a ve...');
  });

  it('should return original text if within limit', () => {
    expect(truncateText('Short', 10)).toBe('Short');
  });

  it('should handle exact length text', () => {
    expect(truncateText('Exact', 5)).toBe('Exact');
  });
});

describe('groupBy', () => {
  const employees = [
    { name: 'Sarah Chen', department: 'Engineering', salary: 95000 },
    { name: 'Marcus Johnson', department: 'Marketing', salary: 72000 },
    { name: 'Aisha Patel', department: 'Engineering', salary: 88000 },
    { name: 'David Kim', department: 'Marketing', salary: 68000 },
    { name: 'Elena Rodriguez', department: 'Design', salary: 82000 },
  ];

  it('should group by department', () => {
    const grouped = groupBy(employees, 'department');
    expect(Object.keys(grouped)).toHaveLength(3);
    expect(grouped['Engineering']).toHaveLength(2);
    expect(grouped['Marketing']).toHaveLength(2);
    expect(grouped['Design']).toHaveLength(1);
  });

  it('should preserve all items in groups', () => {
    const grouped = groupBy(employees, 'department');
    const totalItems = Object.values(grouped).flat().length;
    expect(totalItems).toBe(employees.length);
  });
});
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'utils', '__tests__', 'helpers.test.ts'), 'w') as f:
        f.write(helpers_test_ts)

    # --- src/components/App.tsx (basic app component) ---
    app_tsx = """import React from 'react';
import { formatCurrency, truncateText } from '../utils/helpers';

interface Product {
  id: number;
  name: string;
  price: number;
  description: string;
}

const sampleProducts: Product[] = [
  {
    id: 1,
    name: 'Wireless Bluetooth Headphones',
    price: 79.99,
    description: 'Premium noise-cancelling headphones with 30-hour battery life and comfortable over-ear design.',
  },
  {
    id: 2,
    name: 'Mechanical Keyboard',
    price: 149.95,
    description: 'RGB backlit mechanical keyboard with Cherry MX Brown switches and aluminum frame.',
  },
  {
    id: 3,
    name: 'USB-C Hub Adapter',
    price: 34.50,
    description: 'Multi-port adapter with HDMI, USB 3.0, SD card reader, and ethernet port.',
  },
];

const App: React.FC = () => {
  return (
    <div className="app">
      <h1>Product Catalog</h1>
      <div className="product-list">
        {sampleProducts.map((product) => (
          <div key={product.id} className="product-card">
            <h2>{product.name}</h2>
            <p className="price">{formatCurrency(product.price)}</p>
            <p className="description">{truncateText(product.description, 80)}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'components', 'App.tsx'), 'w') as f:
        f.write(app_tsx)

    # --- .vscode/settings.json (basic workspace settings, NO launch config) ---
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # Ensure NO launch.json exists (negative constraint)
    launch_json_path = os.path.join(VSCODE_DIR, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Test file: {PROJECT_DIR}/src/utils/__tests__/helpers.test.ts')
    print(f'No launch.json present (as required)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
