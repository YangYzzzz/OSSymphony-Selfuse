"""
Initial Setup: Create a monorepo workspace for VSCode tasks.json task
Task ID: vscode_gf3_046
Domain: vscode

Creates a realistic npm workspaces monorepo at /home/user/projects/monorepo/
with multiple packages. Does NOT create .vscode/tasks.json (that's the task).
Opens VSCode with the monorepo folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_046'
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
    # --- Root monorepo structure ---
    os.makedirs(MONOREPO, exist_ok=True)

    # Root package.json with npm workspaces
    root_pkg = {
        "name": "acme-monorepo",
        "version": "1.0.0",
        "private": True,
        "description": "Acme Corp internal monorepo for frontend services",
        "workspaces": [
            "packages/*"
        ],
        "scripts": {
            "build": "npm run build --workspaces",
            "test": "npm run test --workspaces --if-present",
            "lint": "npm run lint --workspaces --if-present"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "prettier": "^3.1.1"
        }
    }
    with open(f'{MONOREPO}/package.json', 'w') as f:
        json.dump(root_pkg, f, indent=2)

    # --- Package: @acme/ui-components ---
    ui_dir = f'{MONOREPO}/packages/ui-components'
    os.makedirs(f'{ui_dir}/src', exist_ok=True)

    ui_pkg = {
        "name": "@acme/ui-components",
        "version": "2.4.1",
        "description": "Shared React UI component library",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc --project tsconfig.json",
            "test": "jest --coverage",
            "lint": "eslint src/"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "@types/react": "^18.2.45",
            "jest": "^29.7.0",
            "typescript": "^5.3.3"
        }
    }
    with open(f'{ui_dir}/package.json', 'w') as f:
        json.dump(ui_pkg, f, indent=2)

    with open(f'{ui_dir}/src/Button.tsx', 'w') as f:
        f.write("""import React from 'react';

interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = 'primary',
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`btn btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
};
""")

    with open(f'{ui_dir}/src/index.ts', 'w') as f:
        f.write("export { Button } from './Button';\nexport { Card } from './Card';\nexport { Modal } from './Modal';\n")

    # --- Package: @acme/api-client ---
    api_dir = f'{MONOREPO}/packages/api-client'
    os.makedirs(f'{api_dir}/src', exist_ok=True)

    api_pkg = {
        "name": "@acme/api-client",
        "version": "1.7.0",
        "description": "HTTP client for Acme internal APIs",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc --project tsconfig.json",
            "test": "jest"
        },
        "dependencies": {
            "axios": "^1.6.2"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "typescript": "^5.3.3"
        }
    }
    with open(f'{api_dir}/package.json', 'w') as f:
        json.dump(api_pkg, f, indent=2)

    with open(f'{api_dir}/src/client.ts', 'w') as f:
        f.write("""import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

export class AcmeApiClient {
  private http: AxiosInstance;

  constructor(baseURL: string, apiKey: string) {
    this.http = axios.create({
      baseURL,
      headers: { 'X-API-Key': apiKey },
      timeout: 10000,
    });
  }

  async getUsers(page: number = 1): Promise<any> {
    const response = await this.http.get('/v2/users', { params: { page } });
    return response.data;
  }

  async getOrders(userId: string): Promise<any> {
    const response = await this.http.get(`/v2/users/${userId}/orders`);
    return response.data;
  }
}
""")

    # --- Package: @acme/eslint-config (shared config, no test script) ---
    config_dir = f'{MONOREPO}/packages/eslint-config'
    os.makedirs(config_dir, exist_ok=True)

    config_pkg = {
        "name": "@acme/eslint-config",
        "version": "1.0.3",
        "description": "Shared ESLint configuration for all Acme packages",
        "main": "index.js",
        "scripts": {
            "build": "echo 'No build step needed for config package'"
        },
        "dependencies": {
            "eslint": "^8.56.0",
            "eslint-config-prettier": "^9.1.0"
        }
    }
    with open(f'{config_dir}/package.json', 'w') as f:
        json.dump(config_pkg, f, indent=2)

    with open(f'{config_dir}/index.js', 'w') as f:
        f.write("""module.exports = {
  extends: ['eslint:recommended', 'prettier'],
  env: { browser: true, node: true, es2022: true },
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  rules: {
    'no-console': 'warn',
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'prefer-const': 'error',
  },
};
""")

    # --- Root config files ---
    with open(f'{MONOREPO}/.gitignore', 'w') as f:
        f.write("node_modules/\ndist/\ncoverage/\n.env\n*.log\n")

    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "commonjs",
            "lib": ["ES2022", "DOM"],
            "outDir": "dist",
            "rootDir": "src",
            "strict": True,
            "esModuleInterop": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "exclude": ["node_modules", "dist"]
    }
    with open(f'{MONOREPO}/tsconfig.base.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    with open(f'{MONOREPO}/README.md', 'w') as f:
        f.write("""# Acme Monorepo

Internal monorepo for Acme Corp frontend services and shared libraries.

## Packages

| Package | Version | Description |
|---------|---------|-------------|
| @acme/ui-components | 2.4.1 | Shared React UI component library |
| @acme/api-client | 1.7.0 | HTTP client for internal APIs |
| @acme/eslint-config | 1.0.3 | Shared ESLint configuration |

## Getting Started

```bash
npm install          # Install all dependencies
npm run build        # Build all packages
npm run test         # Run tests across all packages
```
""")

    print(f'Monorepo created at: {MONOREPO}')
    print(f'Packages: ui-components, api-client, eslint-config')

    # GUI-ready: open VSCode with the monorepo folder
    launch_gui(f'code "{MONOREPO}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
