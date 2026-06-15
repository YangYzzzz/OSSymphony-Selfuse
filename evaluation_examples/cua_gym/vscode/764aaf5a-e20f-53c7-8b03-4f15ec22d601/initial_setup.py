"""
Initial Setup: Set up a backend project structure for database testing workflow.
Task ID: vscode_gf3_079
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_079'
PROJECT_ROOT = f'{WORKDIR}/projects/backend'

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
    dirs = [
        f'{PROJECT_ROOT}/src',
        f'{PROJECT_ROOT}/src/repositories',
        f'{PROJECT_ROOT}/src/models',
        f'{PROJECT_ROOT}/src/migrations',
        f'{PROJECT_ROOT}/src/__tests__/unit',
        # Note: src/__tests__/integration/ directory intentionally NOT created
        # The task asks the agent to create the integration test file
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # --- package.json ---
    package_json = {
        "name": "backend-service",
        "version": "1.0.0",
        "description": "User management backend service",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "dev": "ts-node src/index.ts",
            "test": "jest",
            "test:unit": "jest --testPathPattern=unit",
            "migrate": "ts-node src/migrations/run.ts"
        },
        "dependencies": {
            "pg": "^8.11.3",
            "express": "^4.18.2",
            "dotenv": "^16.3.1",
            "bcrypt": "^5.1.1",
            "uuid": "^9.0.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/node": "^20.10.0",
            "@types/pg": "^8.10.9",
            "@types/express": "^4.17.21",
            "@types/bcrypt": "^5.0.2",
            "@types/uuid": "^9.0.7",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.1",
            "@types/jest": "^29.5.11",
            "testcontainers": "^10.4.0"
        }
    }
    with open(f'{PROJECT_ROOT}/package.json', 'w') as f:
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
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "src/__tests__"]
    }
    with open(f'{PROJECT_ROOT}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- jest.config.ts (without integration testTimeout) ---
    jest_config = """\
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: [
    '**/__tests__/**/*.test.ts',
  ],
  moduleFileExtensions: ['ts', 'js', 'json'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/__tests__/**',
    '!src/migrations/**',
  ],
};

export default config;
"""
    with open(f'{PROJECT_ROOT}/jest.config.ts', 'w') as f:
        f.write(jest_config)

    # --- src/models/User.ts ---
    user_model = """\
export interface User {
  id: string;
  email: string;
  username: string;
  password_hash: string;
  full_name: string;
  role: 'admin' | 'editor' | 'viewer';
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface CreateUserInput {
  email: string;
  username: string;
  password_hash: string;
  full_name: string;
  role?: 'admin' | 'editor' | 'viewer';
}

export interface UpdateUserInput {
  email?: string;
  username?: string;
  full_name?: string;
  role?: 'admin' | 'editor' | 'viewer';
  is_active?: boolean;
}
"""
    with open(f'{PROJECT_ROOT}/src/models/User.ts', 'w') as f:
        f.write(user_model)

    # --- src/repositories/UserRepository.ts ---
    user_repo = """\
import { Pool, PoolClient } from 'pg';
import { User, CreateUserInput, UpdateUserInput } from '../models/User';
import { v4 as uuidv4 } from 'uuid';

export class UserRepository {
  private pool: Pool;

  constructor(pool: Pool) {
    this.pool = pool;
  }

  async findById(id: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] || null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return result.rows[0] || null;
  }

  async findByUsername(username: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE username = $1',
      [username]
    );
    return result.rows[0] || null;
  }

  async create(input: CreateUserInput): Promise<User> {
    const id = uuidv4();
    const result = await this.pool.query(
      `INSERT INTO users (id, email, username, password_hash, full_name, role, is_active, created_at, updated_at)
       VALUES ($1, $2, $3, $4, $5, $6, true, NOW(), NOW())
       RETURNING *`,
      [id, input.email, input.username, input.password_hash, input.full_name, input.role || 'viewer']
    );
    return result.rows[0];
  }

  async update(id: string, input: UpdateUserInput): Promise<User | null> {
    const fields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    if (input.email !== undefined) {
      fields.push(\`email = $\${paramIndex++}\`);
      values.push(input.email);
    }
    if (input.username !== undefined) {
      fields.push(\`username = $\${paramIndex++}\`);
      values.push(input.username);
    }
    if (input.full_name !== undefined) {
      fields.push(\`full_name = $\${paramIndex++}\`);
      values.push(input.full_name);
    }
    if (input.role !== undefined) {
      fields.push(\`role = $\${paramIndex++}\`);
      values.push(input.role);
    }
    if (input.is_active !== undefined) {
      fields.push(\`is_active = $\${paramIndex++}\`);
      values.push(input.is_active);
    }

    if (fields.length === 0) return this.findById(id);

    fields.push(\`updated_at = NOW()\`);
    values.push(id);

    const result = await this.pool.query(
      \`UPDATE users SET \${fields.join(', ')} WHERE id = $\${paramIndex} RETURNING *\`,
      values
    );
    return result.rows[0] || null;
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.pool.query(
      'DELETE FROM users WHERE id = $1',
      [id]
    );
    return (result.rowCount ?? 0) > 0;
  }

  async findAll(limit: number = 50, offset: number = 0): Promise<User[]> {
    const result = await this.pool.query(
      'SELECT * FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2',
      [limit, offset]
    );
    return result.rows;
  }

  async countByRole(role: string): Promise<number> {
    const result = await this.pool.query(
      'SELECT COUNT(*) as count FROM users WHERE role = $1',
      [role]
    );
    return parseInt(result.rows[0].count, 10);
  }
}
"""
    with open(f'{PROJECT_ROOT}/src/repositories/UserRepository.ts', 'w') as f:
        f.write(user_repo)

    # --- src/migrations/001_create_users.ts ---
    migration = """\
import { Pool } from 'pg';

export async function up(pool: Pool): Promise<void> {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS users (
      id UUID PRIMARY KEY,
      email VARCHAR(255) UNIQUE NOT NULL,
      username VARCHAR(100) UNIQUE NOT NULL,
      password_hash VARCHAR(255) NOT NULL,
      full_name VARCHAR(255) NOT NULL,
      role VARCHAR(20) NOT NULL DEFAULT 'viewer'
        CHECK (role IN ('admin', 'editor', 'viewer')),
      is_active BOOLEAN NOT NULL DEFAULT true,
      created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
    CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
    CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
  `);
}

export async function down(pool: Pool): Promise<void> {
  await pool.query('DROP TABLE IF EXISTS users CASCADE');
}
"""
    with open(f'{PROJECT_ROOT}/src/migrations/001_create_users.ts', 'w') as f:
        f.write(migration)

    # --- src/migrations/run.ts ---
    run_migrations = """\
import { Pool } from 'pg';
import { up } from './001_create_users';

async function runMigrations() {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
  });

  try {
    console.log('Running migrations...');
    await up(pool);
    console.log('Migrations completed successfully.');
  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

runMigrations();
"""
    with open(f'{PROJECT_ROOT}/src/migrations/run.ts', 'w') as f:
        f.write(run_migrations)

    # --- src/index.ts ---
    index_ts = """\
import express from 'express';
import { Pool } from 'pg';
import { UserRepository } from './repositories/UserRepository';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

const userRepo = new UserRepository(pool);

app.get('/api/users', async (req, res) => {
  try {
    const users = await userRepo.findAll();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await userRepo.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
"""
    with open(f'{PROJECT_ROOT}/src/index.ts', 'w') as f:
        f.write(index_ts)

    # --- src/__tests__/unit/userRepository.test.ts (basic unit test) ---
    unit_test = """\
import { UserRepository } from '../../repositories/UserRepository';

describe('UserRepository', () => {
  it('should be defined', () => {
    expect(UserRepository).toBeDefined();
  });

  it('should accept a pool in the constructor', () => {
    const mockPool = {} as any;
    const repo = new UserRepository(mockPool);
    expect(repo).toBeInstanceOf(UserRepository);
  });
});
"""
    with open(f'{PROJECT_ROOT}/src/__tests__/unit/userRepository.test.ts', 'w') as f:
        f.write(unit_test)

    # --- .env.example ---
    env_example = """\
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/backend_db
PORT=3000
NODE_ENV=development
"""
    with open(f'{PROJECT_ROOT}/.env.example', 'w') as f:
        f.write(env_example)

    # --- .gitignore ---
    gitignore = """\
node_modules/
dist/
.env
coverage/
*.js.map
"""
    with open(f'{PROJECT_ROOT}/.gitignore', 'w') as f:
        f.write(gitignore)

    print(f'Initial project structure created at: {PROJECT_ROOT}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_ROOT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
