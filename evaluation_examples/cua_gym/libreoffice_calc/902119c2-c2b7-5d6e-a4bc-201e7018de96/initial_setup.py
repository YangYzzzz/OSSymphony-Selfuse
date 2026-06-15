"""
Initial Setup: Create a Node.js webapp project with ESLint, TypeScript, and Jest configured.
Task ID: vscode_web_087
Domain: vscode (os/file creation)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_087'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src', '__tests__'), exist_ok=True)

    # package.json with ESLint, TypeScript, Jest dependencies
    package_json = {
        "name": "webapp",
        "version": "1.0.0",
        "description": "Customer portal web application",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "lint": "eslint .",
            "test": "jest",
            "start": "node dist/index.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "@types/express": "^4.17.21",
            "@types/cors": "^2.8.17",
            "@types/jest": "^29.5.11",
            "@typescript-eslint/eslint-plugin": "^6.18.0",
            "@typescript-eslint/parser": "^6.18.0",
            "eslint": "^8.56.0",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "typescript": "^5.3.3"
        },
        "author": "Webapp Team",
        "license": "MIT"
    }
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    # tsconfig.json
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
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "**/*.test.ts"]
    }
    with open(os.path.join(PROJECT_DIR, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # .eslintrc.json
    eslintrc = {
        "env": {
            "node": True,
            "jest": True,
            "es2020": True
        },
        "extends": [
            "eslint:recommended",
            "plugin:@typescript-eslint/recommended"
        ],
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaVersion": 2020,
            "sourceType": "module"
        },
        "plugins": ["@typescript-eslint"],
        "rules": {
            "no-unused-vars": "off",
            "@typescript-eslint/no-unused-vars": ["error"],
            "@typescript-eslint/explicit-function-return-type": "warn"
        }
    }
    with open(os.path.join(PROJECT_DIR, '.eslintrc.json'), 'w') as f:
        json.dump(eslintrc, f, indent=2)

    # jest.config.js
    jest_config = """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/__tests__/**'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov'],
};
"""
    with open(os.path.join(PROJECT_DIR, 'jest.config.js'), 'w') as f:
        f.write(jest_config)

    # src/index.ts - main entry point
    index_ts = """import express from 'express';
import cors from 'cors';
import { config } from 'dotenv';
import { UserService } from './services/userService';
import { healthCheck } from './routes/health';

config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/health', healthCheck);

const userService = new UserService();

app.get('/api/users', async (req, res) => {
  try {
    const users = await userService.getAllUsers();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

export default app;
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'index.ts'), 'w') as f:
        f.write(index_ts)

    # src/services/userService.ts
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'services'), exist_ok=True)
    user_service_ts = """export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'editor' | 'viewer';
  createdAt: Date;
}

export class UserService {
  private users: User[] = [
    { id: 1, name: 'Sarah Chen', email: 'sarah.chen@company.com', role: 'admin', createdAt: new Date('2024-01-15') },
    { id: 2, name: 'Marcus Johnson', email: 'marcus.j@company.com', role: 'editor', createdAt: new Date('2024-03-22') },
    { id: 3, name: 'Priya Patel', email: 'priya.p@company.com', role: 'viewer', createdAt: new Date('2024-06-10') },
  ];

  async getAllUsers(): Promise<User[]> {
    return this.users;
  }

  async getUserById(id: number): Promise<User | undefined> {
    return this.users.find(user => user.id === id);
  }

  async createUser(userData: Omit<User, 'id' | 'createdAt'>): Promise<User> {
    const newUser: User = {
      ...userData,
      id: this.users.length + 1,
      createdAt: new Date(),
    };
    this.users.push(newUser);
    return newUser;
  }
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'services', 'userService.ts'), 'w') as f:
        f.write(user_service_ts)

    # src/routes/health.ts
    os.makedirs(os.path.join(PROJECT_DIR, 'src', 'routes'), exist_ok=True)
    health_ts = """import { Request, Response } from 'express';

export function healthCheck(req: Request, res: Response): void {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'routes', 'health.ts'), 'w') as f:
        f.write(health_ts)

    # src/__tests__/userService.test.ts
    test_ts = """import { UserService, User } from '../services/userService';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  test('getAllUsers returns all users', async () => {
    const users = await service.getAllUsers();
    expect(users).toHaveLength(3);
    expect(users[0].name).toBe('Sarah Chen');
  });

  test('getUserById returns correct user', async () => {
    const user = await service.getUserById(1);
    expect(user).toBeDefined();
    expect(user?.email).toBe('sarah.chen@company.com');
  });

  test('getUserById returns undefined for invalid id', async () => {
    const user = await service.getUserById(999);
    expect(user).toBeUndefined();
  });

  test('createUser adds new user with correct fields', async () => {
    const newUser = await service.createUser({
      name: 'Elena Rodriguez',
      email: 'elena.r@company.com',
      role: 'editor',
    });
    expect(newUser.id).toBe(4);
    expect(newUser.name).toBe('Elena Rodriguez');
    expect(newUser.createdAt).toBeInstanceOf(Date);
  });
});
"""
    with open(os.path.join(PROJECT_DIR, 'src', '__tests__', 'userService.test.ts'), 'w') as f:
        f.write(test_ts)

    # .gitignore
    gitignore = """node_modules/
dist/
coverage/
.env
*.js.map
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore)

    # README.md
    readme = """# Webapp - Customer Portal

A TypeScript-based Express server for the customer portal API.

## Getting Started

```bash
npm install
npm run build
npm start
```

## Development

- `npm run lint` - Run ESLint
- `npm run build` - Compile TypeScript
- `npm test` - Run Jest tests

## Project Structure

```
src/
  index.ts          - Express app entry point
  services/         - Business logic
  routes/           - Route handlers
  __tests__/        - Jest test files
```
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # IMPORTANT: .github directory must NOT exist
    # (This is the negative constraint - the task is to create it)

    print(f'Initial project created at: {PROJECT_DIR}')
    print('Contents:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip node_modules if it exists
        dirs[:] = [d for d in dirs if d != 'node_modules']
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
