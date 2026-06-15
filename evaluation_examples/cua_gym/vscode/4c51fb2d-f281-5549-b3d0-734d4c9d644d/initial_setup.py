"""
Initial Setup: Configure VSCode watcher excludes for monorepo performance
Task ID: vscode_we_023
Domain: vscode

Creates a realistic monorepo project structure and opens VSCode with
empty user settings (no files.watcherExclude configured).
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_023'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(WORKDIR, 'aurora-platform')


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


def create_monorepo():
    """Create a realistic monorepo project structure."""
    # Root-level files
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # package.json (root)
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump({
            "name": "aurora-platform",
            "version": "3.2.1",
            "private": True,
            "workspaces": [
                "packages/*",
                "apps/*"
            ],
            "scripts": {
                "build": "turbo run build",
                "test": "turbo run test",
                "lint": "turbo run lint",
                "dev": "turbo run dev --parallel"
            },
            "devDependencies": {
                "turbo": "^1.10.0",
                "typescript": "^5.2.0",
                "eslint": "^8.50.0",
                "prettier": "^3.0.3"
            }
        }, f, indent=2)

    # .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("node_modules/\ndist/\n.env\n*.log\ncoverage/\n.turbo/\n")

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# Aurora Platform

Enterprise-grade SaaS platform for real-time analytics and workflow automation.

## Architecture

- **apps/web** - Next.js frontend application
- **apps/api** - Express.js REST API server
- **packages/ui** - Shared React component library
- **packages/utils** - Common utility functions
- **packages/config** - Shared ESLint and TypeScript configs

## Getting Started

```bash
npm install
npm run dev
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.
""")

    # turbo.json
    with open(os.path.join(PROJECT_DIR, 'turbo.json'), 'w') as f:
        json.dump({
            "$schema": "https://turbo.build/schema.json",
            "globalDependencies": ["**/.env.*local"],
            "pipeline": {
                "build": {"dependsOn": ["^build"], "outputs": ["dist/**"]},
                "lint": {},
                "test": {"dependsOn": ["build"]}
            }
        }, f, indent=2)

    # tsconfig.base.json
    with open(os.path.join(PROJECT_DIR, 'tsconfig.base.json'), 'w') as f:
        json.dump({
            "compilerOptions": {
                "target": "ES2020",
                "module": "ESNext",
                "moduleResolution": "bundler",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "declaration": True,
                "declarationMap": True,
                "sourceMap": True
            }
        }, f, indent=2)

    # --- apps/web ---
    web_src = os.path.join(PROJECT_DIR, 'apps', 'web', 'src', 'pages')
    os.makedirs(web_src, exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'apps', 'web', 'package.json'), 'w') as f:
        json.dump({
            "name": "@aurora/web",
            "version": "3.2.1",
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.2.0",
                "@aurora/ui": "workspace:*"
            }
        }, f, indent=2)

    with open(os.path.join(web_src, 'index.tsx'), 'w') as f:
        f.write("""import { Dashboard } from '@aurora/ui';
import { useAnalytics } from '../hooks/useAnalytics';

export default function HomePage() {
  const { metrics, isLoading } = useAnalytics();

  if (isLoading) return <Dashboard.Skeleton />;

  return (
    <Dashboard
      revenue={metrics.monthlyRevenue}
      activeUsers={metrics.dailyActiveUsers}
      conversionRate={metrics.conversionRate}
    />
  );
}
""")

    with open(os.path.join(web_src, 'settings.tsx'), 'w') as f:
        f.write("""import { SettingsPanel, Toggle, Select } from '@aurora/ui';
import { useUserPreferences } from '../hooks/useUserPreferences';

export default function SettingsPage() {
  const { prefs, updatePref } = useUserPreferences();

  return (
    <SettingsPanel title="Workspace Settings">
      <Toggle
        label="Enable notifications"
        checked={prefs.notifications}
        onChange={(v) => updatePref('notifications', v)}
      />
      <Select
        label="Default timezone"
        value={prefs.timezone}
        options={['UTC', 'US/Eastern', 'US/Pacific', 'Europe/London']}
        onChange={(v) => updatePref('timezone', v)}
      />
    </SettingsPanel>
  );
}
""")

    # --- apps/api ---
    api_src = os.path.join(PROJECT_DIR, 'apps', 'api', 'src', 'routes')
    os.makedirs(api_src, exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'apps', 'api', 'package.json'), 'w') as f:
        json.dump({
            "name": "@aurora/api",
            "version": "3.2.1",
            "dependencies": {
                "express": "^4.18.0",
                "prisma": "^5.5.0",
                "@aurora/utils": "workspace:*"
            }
        }, f, indent=2)

    with open(os.path.join(api_src, 'analytics.ts'), 'w') as f:
        f.write("""import { Router } from 'express';
import { prisma } from '../db';
import { calculateGrowthRate, formatCurrency } from '@aurora/utils';

const router = Router();

router.get('/metrics', async (req, res) => {
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  const [revenue, users, conversions] = await Promise.all([
    prisma.transaction.aggregate({
      where: { createdAt: { gte: thirtyDaysAgo } },
      _sum: { amount: true },
    }),
    prisma.user.count({ where: { lastActive: { gte: thirtyDaysAgo } } }),
    prisma.funnel.findMany({
      where: { completedAt: { not: null, gte: thirtyDaysAgo } },
    }),
  ]);

  const growthRate = calculateGrowthRate(revenue._sum.amount, 'monthly');

  res.json({
    monthlyRevenue: formatCurrency(revenue._sum.amount || 0),
    dailyActiveUsers: users,
    conversionRate: (conversions.length / users * 100).toFixed(2),
    growthRate,
  });
});

export default router;
""")

    # --- packages/ui ---
    ui_src = os.path.join(PROJECT_DIR, 'packages', 'ui', 'src', 'components')
    os.makedirs(ui_src, exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'packages', 'ui', 'package.json'), 'w') as f:
        json.dump({
            "name": "@aurora/ui",
            "version": "2.8.0",
            "main": "dist/index.js",
            "types": "dist/index.d.ts",
            "dependencies": {
                "react": "^18.2.0",
                "class-variance-authority": "^0.7.0"
            }
        }, f, indent=2)

    with open(os.path.join(ui_src, 'Button.tsx'), 'w') as f:
        f.write("""import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
);

interface ButtonProps extends VariantProps<typeof buttonVariants> {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export function Button({ variant, size, children, onClick, disabled }: ButtonProps) {
  return (
    <button
      className={buttonVariants({ variant, size })}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
""")

    # --- packages/utils ---
    utils_src = os.path.join(PROJECT_DIR, 'packages', 'utils', 'src')
    os.makedirs(utils_src, exist_ok=True)
    with open(os.path.join(PROJECT_DIR, 'packages', 'utils', 'package.json'), 'w') as f:
        json.dump({
            "name": "@aurora/utils",
            "version": "1.4.2",
            "main": "dist/index.js",
            "types": "dist/index.d.ts"
        }, f, indent=2)

    with open(os.path.join(utils_src, 'currency.ts'), 'w') as f:
        f.write("""export function formatCurrency(amount: number, locale = 'en-US', currency = 'USD'): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(amount);
}

export function parseCurrency(formatted: string): number {
  return parseFloat(formatted.replace(/[^0-9.-]/g, ''));
}

export function calculateGrowthRate(current: number, period: 'daily' | 'monthly' | 'yearly'): number {
  const baselines: Record<string, number> = {
    daily: 15200,
    monthly: 456000,
    yearly: 5472000,
  };
  return ((current - baselines[period]) / baselines[period]) * 100;
}
""")

    # --- packages/config ---
    config_dir = os.path.join(PROJECT_DIR, 'packages', 'config')
    os.makedirs(config_dir, exist_ok=True)
    with open(os.path.join(config_dir, 'eslint-preset.js'), 'w') as f:
        f.write("""module.exports = {
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended', 'prettier'],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/no-explicit-any': 'warn',
    'no-console': ['warn', { allow: ['warn', 'error'] }],
  },
};
""")

    # Fake .git directory (just a marker)
    git_dir = os.path.join(PROJECT_DIR, '.git')
    os.makedirs(git_dir, exist_ok=True)
    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write("ref: refs/heads/main\n")

    # Fake node_modules with a couple of marker dirs
    nm_dir = os.path.join(PROJECT_DIR, 'node_modules', '.package-lock.json')
    os.makedirs(os.path.dirname(nm_dir), exist_ok=True)
    with open(nm_dir, 'w') as f:
        f.write("{}\n")

    print(f'Monorepo project created at: {PROJECT_DIR}')


def setup_vscode_settings():
    """Set up VSCode user settings as empty (no watcherExclude)."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'VSCode settings written (empty): {SETTINGS_PATH}')


def create_initial():
    create_monorepo()
    setup_vscode_settings()

    # Launch VSCode with the monorepo folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with aurora-platform monorepo')


create_initial()
