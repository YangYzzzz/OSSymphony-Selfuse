"""
Initial Setup: Configure VSCode with a TypeScript project (no tasks.json)
Task ID: vscode_td_016
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_016'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ts-lib')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
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
    # Create project directories
    os.makedirs(SRC_DIR, exist_ok=True)
    # Ensure .vscode dir exists but NO tasks.json
    os.makedirs(VSCODE_DIR, exist_ok=True)
    # Remove tasks.json if it somehow exists
    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    # --- package.json ---
    package_json = {
        "name": "ts-lib",
        "version": "1.0.0",
        "description": "A TypeScript utility library for data transformation and validation",
        "main": "dist/index.js",
        "types": "dist/index.d.ts",
        "scripts": {
            "build": "tsc",
            "watch": "tsc --watch",
            "test": "jest",
            "lint": "eslint src/**/*.ts"
        },
        "keywords": ["typescript", "utility", "validation"],
        "author": "Elena Rodriguez <elena@dataforge.io>",
        "license": "MIT",
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/node": "^20.10.0",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "eslint": "^8.56.0"
        }
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True,
            "resolveJsonModule": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "**/*.test.ts"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- src/index.ts ---
    index_ts = '''\
import { validateEmail, sanitizeInput, formatCurrency } from './utils';

export interface TransformOptions {
  trimWhitespace: boolean;
  convertCase: 'upper' | 'lower' | 'title' | 'none';
  maxLength?: number;
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  sanitizedValue?: string;
}

export function transformString(input: string, options: TransformOptions): string {
  let result = input;

  if (options.trimWhitespace) {
    result = result.trim();
  }

  switch (options.convertCase) {
    case 'upper':
      result = result.toUpperCase();
      break;
    case 'lower':
      result = result.toLowerCase();
      break;
    case 'title':
      result = result.replace(/\\b\\w/g, (char) => char.toUpperCase());
      break;
    case 'none':
      break;
  }

  if (options.maxLength && result.length > options.maxLength) {
    result = result.substring(0, options.maxLength);
  }

  return result;
}

export function validateUserInput(email: string, displayName: string): ValidationResult {
  const errors: string[] = [];

  if (!validateEmail(email)) {
    errors.push('Invalid email format');
  }

  const sanitized = sanitizeInput(displayName);
  if (sanitized.length < 2) {
    errors.push('Display name must be at least 2 characters');
  }

  if (sanitized.length > 50) {
    errors.push('Display name must not exceed 50 characters');
  }

  return {
    isValid: errors.length === 0,
    errors,
    sanitizedValue: sanitized,
  };
}

export { validateEmail, sanitizeInput, formatCurrency };
'''
    with open(os.path.join(SRC_DIR, 'index.ts'), 'w') as f:
        f.write(index_ts)

    # --- src/utils.ts ---
    utils_ts = '''\
export function validateEmail(email: string): boolean {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}

export function sanitizeInput(input: string): string {
  return input
    .replace(/[<>]/g, '')
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .trim();
}

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return formatter.format(amount);
}

export function debounce<T extends (...args: any[]) => void>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  return (...args: Parameters<T>) => {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      func(...args);
      timeoutId = null;
    }, wait);
  };
}

export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map((item) => deepClone(item)) as unknown as T;
  }

  const cloned = {} as T;
  for (const key of Object.keys(obj as object)) {
    (cloned as any)[key] = deepClone((obj as any)[key]);
  }
  return cloned;
}
'''
    with open(os.path.join(SRC_DIR, 'utils.ts'), 'w') as f:
        f.write(utils_ts)

    # --- .vscode/settings.json (workspace settings, NOT tasks.json) ---
    vscode_settings = {
        "typescript.tsdk": "node_modules/typescript/lib",
        "editor.tabSize": 2,
        "editor.formatOnSave": True
    }
    with open(os.path.join(VSCODE_DIR, 'settings.json'), 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'tsconfig.json: {os.path.join(PROJECT_DIR, "tsconfig.json")}')
    print(f'No tasks.json exists (as expected)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
