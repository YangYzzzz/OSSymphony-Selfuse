"""
Initial Setup: Monorepo workspace with npm packages but no tasks.json
Task ID: vscode_web_071
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_071'
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
    # Create monorepo directory structure
    packages = ['shared', 'frontend', 'backend']
    for pkg in packages:
        os.makedirs(f'{MONOREPO}/packages/{pkg}/src', exist_ok=True)

    os.makedirs(f'{MONOREPO}/.vscode', exist_ok=True)

    # Root package.json with workspaces
    root_pkg = {
        "name": "acme-platform",
        "version": "1.0.0",
        "private": True,
        "description": "Acme Platform monorepo - internal tools and services",
        "workspaces": [
            "packages/*"
        ],
        "scripts": {
            "lint": "eslint . --ext .ts,.tsx",
            "test": "jest --passWithNoTests",
            "clean": "rm -rf packages/*/dist"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "eslint": "^8.56.0",
            "@types/node": "^20.11.0",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1"
        }
    }
    with open(f'{MONOREPO}/package.json', 'w') as f:
        json.dump(root_pkg, f, indent=2)

    # Shared package
    shared_pkg = {
        "name": "@acme/shared",
        "version": "1.2.0",
        "description": "Shared utilities, types, and constants for the Acme platform",
        "main": "dist/index.js",
        "types": "dist/index.d.ts",
        "scripts": {
            "build": "tsc -p tsconfig.json",
            "test": "jest",
            "clean": "rm -rf dist"
        },
        "dependencies": {
            "zod": "^3.22.4"
        },
        "devDependencies": {
            "typescript": "^5.3.3"
        }
    }
    with open(f'{MONOREPO}/packages/shared/package.json', 'w') as f:
        json.dump(shared_pkg, f, indent=2)

    shared_index = '''export interface User {
  id: string;
  email: string;
  displayName: string;
  role: "admin" | "editor" | "viewer";
  createdAt: Date;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
  timestamp: string;
}

export const API_BASE_URL = process.env.API_URL || "https://api.acme-internal.dev";
export const MAX_RETRY_ATTEMPTS = 3;
export const REQUEST_TIMEOUT_MS = 30000;

export function formatCurrency(amount: number, currency: string = "USD"): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount);
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\\w\\s-]/g, "")
    .replace(/\\s+/g, "-")
    .trim();
}
'''
    with open(f'{MONOREPO}/packages/shared/src/index.ts', 'w') as f:
        f.write(shared_index)

    shared_tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "declaration": True,
            "esModuleInterop": True,
            "skipLibCheck": True
        },
        "include": ["src/**/*"]
    }
    with open(f'{MONOREPO}/packages/shared/tsconfig.json', 'w') as f:
        json.dump(shared_tsconfig, f, indent=2)

    # Frontend package
    frontend_pkg = {
        "name": "@acme/frontend",
        "version": "2.0.1",
        "description": "Acme Platform dashboard - React-based internal admin panel",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc -p tsconfig.json && vite build",
            "dev": "vite dev",
            "test": "jest",
            "clean": "rm -rf dist"
        },
        "dependencies": {
            "@acme/shared": "workspace:*",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.21.3"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "vite": "^5.0.12",
            "@vitejs/plugin-react": "^4.2.1"
        }
    }
    with open(f'{MONOREPO}/packages/frontend/package.json', 'w') as f:
        json.dump(frontend_pkg, f, indent=2)

    frontend_index = '''import React from "react";
import { User, formatCurrency, API_BASE_URL } from "@acme/shared";

interface DashboardProps {
  currentUser: User;
}

export const Dashboard: React.FC<DashboardProps> = ({ currentUser }) => {
  const [revenue, setRevenue] = React.useState<number>(0);

  React.useEffect(() => {
    fetch(`${API_BASE_URL}/metrics/revenue`)
      .then((res) => res.json())
      .then((data) => setRevenue(data.total));
  }, []);

  return (
    <div className="dashboard">
      <h1>Welcome, {currentUser.displayName}</h1>
      <div className="metric-card">
        <span>Total Revenue</span>
        <span>{formatCurrency(revenue)}</span>
      </div>
    </div>
  );
};
'''
    with open(f'{MONOREPO}/packages/frontend/src/index.tsx', 'w') as f:
        f.write(frontend_index)

    frontend_tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "ESNext",
            "jsx": "react-jsx",
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "declaration": True,
            "esModuleInterop": True,
            "moduleResolution": "bundler",
            "skipLibCheck": True
        },
        "include": ["src/**/*"]
    }
    with open(f'{MONOREPO}/packages/frontend/tsconfig.json', 'w') as f:
        json.dump(frontend_tsconfig, f, indent=2)

    # Backend package
    backend_pkg = {
        "name": "@acme/backend",
        "version": "1.5.3",
        "description": "Acme Platform API server - Express-based REST service",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc -p tsconfig.json",
            "start": "node dist/index.js",
            "dev": "ts-node-dev --respawn src/index.ts",
            "test": "jest",
            "clean": "rm -rf dist"
        },
        "dependencies": {
            "@acme/shared": "workspace:*",
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "winston": "^3.11.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/express": "^4.17.21",
            "ts-node-dev": "^2.0.0"
        }
    }
    with open(f'{MONOREPO}/packages/backend/package.json', 'w') as f:
        json.dump(backend_pkg, f, indent=2)

    backend_index = '''import express from "express";
import cors from "cors";
import helmet from "helmet";
import { User, ApiResponse, API_BASE_URL, MAX_RETRY_ATTEMPTS } from "@acme/shared";

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(helmet());
app.use(express.json());

const users: User[] = [
  {
    id: "usr_001",
    email: "sarah.chen@acme.dev",
    displayName: "Sarah Chen",
    role: "admin",
    createdAt: new Date("2024-01-15"),
  },
  {
    id: "usr_002",
    email: "marcus.johnson@acme.dev",
    displayName: "Marcus Johnson",
    role: "editor",
    createdAt: new Date("2024-03-22"),
  },
];

app.get("/api/users", (_req, res) => {
  const response: ApiResponse<User[]> = {
    data: users,
    status: 200,
    message: "OK",
    timestamp: new Date().toISOString(),
  };
  res.json(response);
});

app.get("/api/metrics/revenue", (_req, res) => {
  res.json({ total: 284750.0, currency: "USD", period: "Q1-2025" });
});

app.listen(PORT, () => {
  console.log(`Acme API server running on port ${PORT}`);
});
'''
    with open(f'{MONOREPO}/packages/backend/src/index.ts', 'w') as f:
        f.write(backend_index)

    backend_tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "declaration": True,
            "esModuleInterop": True,
            "skipLibCheck": True
        },
        "include": ["src/**/*"]
    }
    with open(f'{MONOREPO}/packages/backend/tsconfig.json', 'w') as f:
        json.dump(backend_tsconfig, f, indent=2)

    # Root tsconfig
    root_tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True
        },
        "references": [
            {"path": "packages/shared"},
            {"path": "packages/frontend"},
            {"path": "packages/backend"}
        ]
    }
    with open(f'{MONOREPO}/tsconfig.json', 'w') as f:
        json.dump(root_tsconfig, f, indent=2)

    # .gitignore
    gitignore = """node_modules/
dist/
*.js.map
.env
.env.local
coverage/
.turbo/
"""
    with open(f'{MONOREPO}/.gitignore', 'w') as f:
        f.write(gitignore)

    # README
    readme = """# Acme Platform Monorepo

Internal platform for Acme Corp. Contains shared libraries, the admin dashboard, and the API server.

## Packages

- **@acme/shared** — Shared types, utilities, and constants
- **@acme/frontend** — React admin dashboard
- **@acme/backend** — Express REST API server

## Getting Started

```bash
npm install
# Currently you need to cd into each package to build
cd packages/shared && npm run build
cd packages/frontend && npm run build
cd packages/backend && npm run build
```

## TODO

- [ ] Set up VSCode task runner for building individual packages
- [ ] Add CI/CD pipeline
"""
    with open(f'{MONOREPO}/README.md', 'w') as f:
        f.write(readme)

    # NO tasks.json — that is the task the agent must create
    # But make sure .vscode dir exists (it may have other config)
    # Actually remove .vscode/tasks.json if it somehow exists
    tasks_json_path = f'{MONOREPO}/.vscode/tasks.json'
    if os.path.exists(tasks_json_path):
        os.remove(tasks_json_path)

    # Add a basic VSCode settings for the workspace
    vscode_settings = {
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "typescript.tsdk": "node_modules/typescript/lib",
        "files.exclude": {
            "**/node_modules": True,
            "**/dist": True
        }
    }
    with open(f'{MONOREPO}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=2)

    print(f'Monorepo structure created at: {MONOREPO}')
    print(f'Packages: shared, frontend, backend')
    print(f'No tasks.json exists (agent must create it)')

    # Launch VSCode with the monorepo folder
    launch_gui(f'code "{MONOREPO}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
