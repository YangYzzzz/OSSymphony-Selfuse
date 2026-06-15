"""
Initial Setup: Create monorepo project structure for GitHub Actions CI workflow task
Task ID: vscode_gf3_065
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_065'
MONOREPO = f'{WORKDIR}/projects/monorepo'


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
    # ── Root monorepo structure ──────────────────────────────────────────
    os.makedirs(f'{MONOREPO}/.github/workflows', exist_ok=True)
    # NOTE: .github/workflows/ exists but ci.yml does NOT — that is the agent's task

    # Root package.json
    with open(f'{MONOREPO}/package.json', 'w') as f:
        f.write("""{
  "name": "acme-monorepo",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "test": "echo \\"Run tests per-package\\"",
    "lint": "eslint . --ext .ts,.tsx",
    "build": "tsc --build"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "eslint": "^8.56.0",
    "@types/node": "^20.11.5"
  }
}
""")

    # Root tsconfig.json
    with open(f'{MONOREPO}/tsconfig.json', 'w') as f:
        f.write("""{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "composite": true
  },
  "references": [
    { "path": "packages/shared" },
    { "path": "packages/backend" },
    { "path": "packages/frontend" }
  ]
}
""")

    # .gitignore
    with open(f'{MONOREPO}/.gitignore', 'w') as f:
        f.write("""node_modules/
dist/
.env
*.log
coverage/
.turbo/
""")

    # ── packages/shared ──────────────────────────────────────────────────
    shared_src = f'{MONOREPO}/packages/shared/src'
    os.makedirs(shared_src, exist_ok=True)

    with open(f'{MONOREPO}/packages/shared/package.json', 'w') as f:
        f.write("""{
  "name": "@acme/shared",
  "version": "1.2.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest --passWithNoTests"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "ts-jest": "^29.1.1",
    "typescript": "^5.3.3"
  }
}
""")

    with open(f'{MONOREPO}/packages/shared/tsconfig.json', 'w') as f:
        f.write("""{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*"]
}
""")

    with open(f'{shared_src}/index.ts', 'w') as f:
        f.write("""export { formatCurrency } from './formatters';
export { validateEmail, validatePhone } from './validators';
export { Logger } from './logger';
export type { AppConfig, UserProfile, ApiResponse } from './types';
""")

    with open(f'{shared_src}/formatters.ts', 'w') as f:
        f.write("""/**
 * Format a number as USD currency string.
 * @example formatCurrency(1234.5) => "$1,234.50"
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

/**
 * Format an ISO date string to a human-readable form.
 */
export function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
""")

    with open(f'{shared_src}/validators.ts', 'w') as f:
        f.write("""const EMAIL_RE = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
const PHONE_RE = /^\\+?[1-9]\\d{6,14}$/;

export function validateEmail(email: string): boolean {
  return EMAIL_RE.test(email);
}

export function validatePhone(phone: string): boolean {
  return PHONE_RE.test(phone.replace(/[\\s()-]/g, ''));
}
""")

    with open(f'{shared_src}/logger.ts', 'w') as f:
        f.write("""export class Logger {
  constructor(private context: string) {}

  info(message: string, meta?: Record<string, unknown>): void {
    console.log(JSON.stringify({ level: 'info', context: this.context, message, ...meta }));
  }

  warn(message: string, meta?: Record<string, unknown>): void {
    console.warn(JSON.stringify({ level: 'warn', context: this.context, message, ...meta }));
  }

  error(message: string, error?: Error): void {
    console.error(JSON.stringify({
      level: 'error',
      context: this.context,
      message,
      stack: error?.stack,
    }));
  }
}
""")

    with open(f'{shared_src}/types.ts', 'w') as f:
        f.write("""export interface AppConfig {
  port: number;
  dbUrl: string;
  redisUrl: string;
  jwtSecret: string;
  environment: 'development' | 'staging' | 'production';
}

export interface UserProfile {
  id: string;
  email: string;
  displayName: string;
  avatarUrl?: string;
  createdAt: string;
  lastLoginAt: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
  meta?: {
    page: number;
    pageSize: number;
    total: number;
  };
}
""")

    # ── packages/backend ─────────────────────────────────────────────────
    backend_src = f'{MONOREPO}/packages/backend/src'
    os.makedirs(backend_src, exist_ok=True)

    with open(f'{MONOREPO}/packages/backend/package.json', 'w') as f:
        f.write("""{
  "name": "@acme/backend",
  "version": "2.1.0",
  "main": "dist/server.js",
  "scripts": {
    "dev": "ts-node-dev --respawn src/server.ts",
    "build": "tsc",
    "test": "jest --coverage",
    "start": "node dist/server.js"
  },
  "dependencies": {
    "@acme/shared": "workspace:*",
    "express": "^4.18.2",
    "pg": "^8.11.3",
    "redis": "^4.6.12",
    "jsonwebtoken": "^9.0.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.1",
    "typescript": "^5.3.3",
    "ts-node-dev": "^2.0.0",
    "supertest": "^6.3.3"
  }
}
""")

    with open(f'{MONOREPO}/packages/backend/tsconfig.json', 'w') as f:
        f.write("""{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*"],
  "references": [
    { "path": "../shared" }
  ]
}
""")

    with open(f'{backend_src}/server.ts', 'w') as f:
        f.write("""import express from 'express';
import { Logger } from '@acme/shared';
import { userRouter } from './routes/users';
import { orderRouter } from './routes/orders';

const app = express();
const logger = new Logger('server');

app.use(express.json());
app.use('/api/users', userRouter);
app.use('/api/orders', orderRouter);

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
  logger.info(`Server started on port ${PORT}`);
});

export { app };
""")

    os.makedirs(f'{backend_src}/routes', exist_ok=True)

    with open(f'{backend_src}/routes/users.ts', 'w') as f:
        f.write("""import { Router } from 'express';
import { validateEmail, Logger } from '@acme/shared';

const router = Router();
const logger = new Logger('users');

router.get('/', async (_req, res) => {
  logger.info('Fetching all users');
  res.json({ success: true, data: [] });
});

router.post('/', async (req, res) => {
  const { email, displayName } = req.body;

  if (!email || !validateEmail(email)) {
    return res.status(400).json({
      success: false,
      error: { code: 'INVALID_EMAIL', message: 'A valid email address is required.' },
    });
  }

  logger.info('Creating user', { email, displayName });
  res.status(201).json({ success: true, data: { email, displayName } });
});

export { router as userRouter };
""")

    with open(f'{backend_src}/routes/orders.ts', 'w') as f:
        f.write("""import { Router } from 'express';
import { formatCurrency, Logger } from '@acme/shared';

const router = Router();
const logger = new Logger('orders');

router.get('/:orderId', async (req, res) => {
  const { orderId } = req.params;
  logger.info('Fetching order', { orderId });

  // Simulated order lookup
  const order = {
    id: orderId,
    items: [
      { sku: 'WIDGET-001', name: 'Premium Widget', quantity: 3, unitPrice: 29.99 },
      { sku: 'GADGET-042', name: 'Deluxe Gadget', quantity: 1, unitPrice: 149.50 },
    ],
    total: formatCurrency(3 * 29.99 + 149.50),
    status: 'shipped',
    createdAt: '2025-11-20T14:30:00Z',
  };

  res.json({ success: true, data: order });
});

export { router as orderRouter };
""")

    # ── packages/frontend ────────────────────────────────────────────────
    frontend_src = f'{MONOREPO}/packages/frontend/src'
    os.makedirs(f'{frontend_src}/components', exist_ok=True)

    with open(f'{MONOREPO}/packages/frontend/package.json', 'w') as f:
        f.write("""{
  "name": "@acme/frontend",
  "version": "1.5.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "test": "jest --passWithNoTests",
    "start": "next start"
  },
  "dependencies": {
    "@acme/shared": "workspace:*",
    "next": "^14.0.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "jest": "^29.7.0",
    "typescript": "^5.3.3",
    "@testing-library/react": "^14.1.2"
  }
}
""")

    with open(f'{MONOREPO}/packages/frontend/tsconfig.json', 'w') as f:
        f.write("""{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "jsx": "preserve",
    "outDir": "dist",
    "rootDir": "src",
    "module": "esnext",
    "moduleResolution": "bundler"
  },
  "include": ["src/**/*"],
  "references": [
    { "path": "../shared" }
  ]
}
""")

    with open(f'{frontend_src}/app.tsx', 'w') as f:
        f.write("""import React from 'react';
import { Dashboard } from './components/Dashboard';
import { Sidebar } from './components/Sidebar';

export default function App() {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 overflow-auto p-8">
        <Dashboard />
      </main>
    </div>
  );
}
""")

    with open(f'{frontend_src}/components/Dashboard.tsx', 'w') as f:
        f.write("""import React from 'react';
import { formatCurrency } from '@acme/shared';

interface MetricCardProps {
  title: string;
  value: number;
  change: number;
}

function MetricCard({ title, value, change }: MetricCardProps) {
  const isPositive = change >= 0;
  return (
    <div className="rounded-xl bg-white p-6 shadow-sm border border-gray-200">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <p className="mt-2 text-3xl font-semibold text-gray-900">
        {formatCurrency(value)}
      </p>
      <span className={`text-sm ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
        {isPositive ? '+' : ''}{change.toFixed(1)}%
      </span>
    </div>
  );
}

export function Dashboard() {
  const metrics = [
    { title: 'Total Revenue', value: 284350, change: 12.5 },
    { title: 'Active Subscriptions', value: 1847, change: 3.2 },
    { title: 'Avg Order Value', value: 67.42, change: -1.8 },
    { title: 'Customer Lifetime Value', value: 432.10, change: 8.7 },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Analytics Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((m) => (
          <MetricCard key={m.title} {...m} />
        ))}
      </div>
    </div>
  );
}
""")

    with open(f'{frontend_src}/components/Sidebar.tsx', 'w') as f:
        f.write("""import React from 'react';

const NAV_ITEMS = [
  { label: 'Dashboard', icon: '📊', href: '/' },
  { label: 'Orders', icon: '📦', href: '/orders' },
  { label: 'Customers', icon: '👥', href: '/customers' },
  { label: 'Products', icon: '🏷️', href: '/products' },
  { label: 'Settings', icon: '⚙️', href: '/settings' },
];

export function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-4">
      <div className="flex items-center gap-2 mb-8">
        <span className="text-xl font-bold text-indigo-600">Acme</span>
      </div>
      <nav className="space-y-1">
        {NAV_ITEMS.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100"
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}
      </nav>
    </aside>
  );
}
""")

    # ── Existing workflow (lint only — NOT the CI workflow the agent must create) ──
    with open(f'{MONOREPO}/.github/workflows/lint.yml', 'w') as f:
        f.write("""name: Lint

on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
""")

    # README
    with open(f'{MONOREPO}/README.md', 'w') as f:
        f.write("""# Acme Monorepo

Production monorepo for the Acme SaaS platform.

## Packages

| Package | Description | Version |
|---------|-------------|---------|
| `@acme/shared` | Shared utilities, types, validators | 1.2.0 |
| `@acme/backend` | Express REST API | 2.1.0 |
| `@acme/frontend` | Next.js dashboard | 1.5.0 |

## Development

```bash
npm install          # Install all dependencies
npm run build        # Build all packages
npm run test         # Run all test suites
```

## CI/CD

Currently we have a basic lint workflow. We need a smarter CI pipeline that
only runs tests for packages affected by each commit — running the full suite
on every push wastes 15-20 minutes of CI time for small changes.
""")

    print(f'Monorepo structure created at {MONOREPO}')

    # GUI-ready: open VSCode with the monorepo folder
    launch_gui(f'code "{MONOREPO}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
