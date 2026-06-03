"""
Initial Setup: Migrate Jest test suite to Vitest
Task ID: vscode_gf6_079
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_079'
PROJECT_DIR = f'{WORKDIR}/projects/ts-vitest'

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


NVM_ENV = 'export NVM_DIR="$HOME/.nvm"; [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh";'

def shell(cmd, **kwargs):
    """Run a shell command with nvm sourced."""
    return subprocess.run(
        f'bash -c \'{NVM_ENV} {cmd}\'',
        shell=True, capture_output=True, text=True, **kwargs,
    )

def install_node():
    """Install Node.js 18 via nvm (no root needed)."""
    print("Installing nvm and Node.js 18...")
    subprocess.run(
        'bash -c "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash"',
        shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    result = shell('nvm install 18', timeout=120)
    print(f"nvm install output: {result.stdout[-300:]}")
    if result.returncode != 0:
        print(f"nvm install stderr: {result.stderr[-300:]}")
    result = shell('node --version')
    print(f"Node.js installed: {result.stdout.strip()}")
    result = shell('npm --version')
    print(f"npm version: {result.stdout.strip()}")


def create_project():
    """Create the ts-vitest project with Jest setup."""
    # Create directory structure
    os.makedirs(f'{PROJECT_DIR}/src/services', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests/__tests__', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)

    # --- tsconfig.json ---
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": ".",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True,
            "types": ["jest", "node"]
        },
        "include": ["src/**/*", "tests/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)

    # --- package.json ---
    package_json = {
        "name": "ts-vitest",
        "version": "1.0.0",
        "description": "User management service with comprehensive test suite",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "test": "jest",
            "test:watch": "jest --watch",
            "test:coverage": "jest --coverage",
            "lint": "eslint src/ tests/"
        },
        "devDependencies": {
            "typescript": "^5.3.0",
            "jest": "^29.7.0",
            "ts-jest": "^29.1.0",
            "ts-node": "^10.9.0",
            "@types/jest": "^29.5.0",
            "@types/node": "^20.10.0"
        },
        "dependencies": {}
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # --- jest.config.ts ---
    jest_config = '''import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
  ],
  coverageDirectory: 'coverage',
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};

export default config;
'''
    with open(f'{PROJECT_DIR}/jest.config.ts', 'w') as f:
        f.write(jest_config)

    # --- src/services/userService.ts ---
    user_service = '''export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'editor' | 'viewer';
  active: boolean;
  createdAt: Date;
  lastLogin?: Date;
}

export interface CreateUserDTO {
  name: string;
  email: string;
  role: 'admin' | 'editor' | 'viewer';
}

export interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findAll(): Promise<User[]>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<boolean>;
}

export interface EmailService {
  sendWelcomeEmail(email: string, name: string): Promise<void>;
  sendDeactivationEmail(email: string, name: string): Promise<void>;
}

export interface Logger {
  info(message: string, meta?: Record<string, unknown>): void;
  error(message: string, meta?: Record<string, unknown>): void;
  warn(message: string, meta?: Record<string, unknown>): void;
}

export class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly emailService: EmailService,
    private readonly logger: Logger,
  ) {}

  async createUser(dto: CreateUserDTO): Promise<User> {
    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) {
      this.logger.warn('Attempted to create duplicate user', { email: dto.email });
      throw new Error(`User with email ${dto.email} already exists`);
    }

    const user: User = {
      id: this.generateId(),
      name: dto.name,
      email: dto.email,
      role: dto.role,
      active: true,
      createdAt: new Date(),
    };

    const saved = await this.userRepo.save(user);
    await this.emailService.sendWelcomeEmail(saved.email, saved.name);
    this.logger.info('User created', { userId: saved.id, email: saved.email });
    return saved;
  }

  async getUserById(id: string): Promise<User> {
    const user = await this.userRepo.findById(id);
    if (!user) {
      throw new Error(`User with id ${id} not found`);
    }
    return user;
  }

  async deactivateUser(id: string): Promise<User> {
    const user = await this.userRepo.findById(id);
    if (!user) {
      throw new Error(`User with id ${id} not found`);
    }
    if (!user.active) {
      this.logger.warn('User already deactivated', { userId: id });
      return user;
    }

    user.active = false;
    const updated = await this.userRepo.save(user);
    await this.emailService.sendDeactivationEmail(updated.email, updated.name);
    this.logger.info('User deactivated', { userId: id });
    return updated;
  }

  async updateUserRole(id: string, role: User['role']): Promise<User> {
    const user = await this.userRepo.findById(id);
    if (!user) {
      throw new Error(`User with id ${id} not found`);
    }
    if (!user.active) {
      throw new Error('Cannot update role of deactivated user');
    }

    user.role = role;
    const updated = await this.userRepo.save(user);
    this.logger.info('User role updated', { userId: id, newRole: role });
    return updated;
  }

  async listActiveUsers(): Promise<User[]> {
    const all = await this.userRepo.findAll();
    return all.filter(u => u.active);
  }

  async deleteUser(id: string): Promise<void> {
    const user = await this.userRepo.findById(id);
    if (!user) {
      throw new Error(`User with id ${id} not found`);
    }
    const deleted = await this.userRepo.delete(id);
    if (!deleted) {
      throw new Error(`Failed to delete user ${id}`);
    }
    this.logger.info('User deleted', { userId: id, email: user.email });
  }

  private generateId(): string {
    return Math.random().toString(36).substring(2, 15) +
           Math.random().toString(36).substring(2, 15);
  }
}
'''
    with open(f'{PROJECT_DIR}/src/services/userService.ts', 'w') as f:
        f.write(user_service)

    # --- tests/__tests__/userService.test.ts --- (12 tests using jest.fn(), jest.mock(), jest.spyOn())
    test_file = '''import { UserService, UserRepository, EmailService, Logger, User, CreateUserDTO } from '../../src/services/userService';

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepo: jest.Mocked<UserRepository>;
  let mockEmailService: jest.Mocked<EmailService>;
  let mockLogger: jest.Mocked<Logger>;

  const mockUser: User = {
    id: 'usr-abc123',
    name: 'Alice Chen',
    email: 'alice.chen@example.com',
    role: 'editor',
    active: true,
    createdAt: new Date('2024-01-15'),
  };

  beforeEach(() => {
    mockUserRepo = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      findAll: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
    };

    mockEmailService = {
      sendWelcomeEmail: jest.fn(),
      sendDeactivationEmail: jest.fn(),
    };

    mockLogger = {
      info: jest.fn(),
      error: jest.fn(),
      warn: jest.fn(),
    };

    userService = new UserService(mockUserRepo, mockEmailService, mockLogger);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  // Test 1: Create user successfully
  it('should create a new user and send welcome email', async () => {
    const dto: CreateUserDTO = { name: 'Bob Park', email: 'bob@example.com', role: 'viewer' };
    mockUserRepo.findByEmail.mockResolvedValue(null);
    mockUserRepo.save.mockImplementation(async (user) => user);

    const result = await userService.createUser(dto);

    expect(result.name).toBe('Bob Park');
    expect(result.email).toBe('bob@example.com');
    expect(result.active).toBe(true);
    expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith('bob@example.com', 'Bob Park');
    expect(mockLogger.info).toHaveBeenCalled();
  });

  // Test 2: Create user with duplicate email
  it('should throw when creating user with existing email', async () => {
    mockUserRepo.findByEmail.mockResolvedValue(mockUser);

    await expect(userService.createUser({
      name: 'Duplicate',
      email: 'alice.chen@example.com',
      role: 'viewer',
    })).rejects.toThrow('User with email alice.chen@example.com already exists');
    expect(mockLogger.warn).toHaveBeenCalled();
  });

  // Test 3: Get user by ID
  it('should return a user by their ID', async () => {
    mockUserRepo.findById.mockResolvedValue(mockUser);

    const result = await userService.getUserById('usr-abc123');

    expect(result).toEqual(mockUser);
    expect(mockUserRepo.findById).toHaveBeenCalledWith('usr-abc123');
  });

  // Test 4: Get user by ID - not found
  it('should throw when user not found by ID', async () => {
    mockUserRepo.findById.mockResolvedValue(null);

    await expect(userService.getUserById('nonexistent'))
      .rejects.toThrow('User with id nonexistent not found');
  });

  // Test 5: Deactivate user
  it('should deactivate an active user and send email', async () => {
    mockUserRepo.findById.mockResolvedValue({ ...mockUser });
    mockUserRepo.save.mockImplementation(async (user) => user);

    const result = await userService.deactivateUser('usr-abc123');

    expect(result.active).toBe(false);
    expect(mockEmailService.sendDeactivationEmail).toHaveBeenCalledWith(
      'alice.chen@example.com',
      'Alice Chen',
    );
    expect(mockLogger.info).toHaveBeenCalled();
  });

  // Test 6: Deactivate already-deactivated user
  it('should return user unchanged if already deactivated', async () => {
    const deactivated = { ...mockUser, active: false };
    mockUserRepo.findById.mockResolvedValue(deactivated);

    const result = await userService.deactivateUser('usr-abc123');

    expect(result.active).toBe(false);
    expect(mockEmailService.sendDeactivationEmail).not.toHaveBeenCalled();
    expect(mockLogger.warn).toHaveBeenCalled();
  });

  // Test 7: Deactivate non-existent user
  it('should throw when deactivating nonexistent user', async () => {
    mockUserRepo.findById.mockResolvedValue(null);

    await expect(userService.deactivateUser('no-user'))
      .rejects.toThrow('User with id no-user not found');
  });

  // Test 8: Update user role
  it('should update user role successfully', async () => {
    mockUserRepo.findById.mockResolvedValue({ ...mockUser });
    mockUserRepo.save.mockImplementation(async (user) => user);

    const result = await userService.updateUserRole('usr-abc123', 'admin');

    expect(result.role).toBe('admin');
    expect(mockLogger.info).toHaveBeenCalled();
  });

  // Test 9: Update role of deactivated user
  it('should throw when updating role of deactivated user', async () => {
    mockUserRepo.findById.mockResolvedValue({ ...mockUser, active: false });

    await expect(userService.updateUserRole('usr-abc123', 'admin'))
      .rejects.toThrow('Cannot update role of deactivated user');
  });

  // Test 10: List active users
  it('should return only active users', async () => {
    const users: User[] = [
      { ...mockUser, id: 'u1', active: true },
      { ...mockUser, id: 'u2', active: false },
      { ...mockUser, id: 'u3', active: true },
    ];
    mockUserRepo.findAll.mockResolvedValue(users);

    const result = await userService.listActiveUsers();

    expect(result).toHaveLength(2);
    expect(result.every(u => u.active)).toBe(true);
  });

  // Test 11: Delete user successfully
  it('should delete a user by ID', async () => {
    mockUserRepo.findById.mockResolvedValue(mockUser);
    mockUserRepo.delete.mockResolvedValue(true);

    await userService.deleteUser('usr-abc123');

    expect(mockUserRepo.delete).toHaveBeenCalledWith('usr-abc123');
    expect(mockLogger.info).toHaveBeenCalled();
  });

  // Test 12: Delete non-existent user
  it('should throw when deleting nonexistent user', async () => {
    mockUserRepo.findById.mockResolvedValue(null);

    await expect(userService.deleteUser('no-user'))
      .rejects.toThrow('User with id no-user not found');
  });
});
'''
    with open(f'{PROJECT_DIR}/tests/__tests__/userService.test.ts', 'w') as f:
        f.write(test_file)

    # --- .vscode/settings.json (basic, NO vitest settings) ---
    vscode_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.formatOnSave": True,
        "typescript.tsdk": "node_modules/typescript/lib",
        "files.exclude": {
            "**/.git": True,
            "**/node_modules": True,
            "**/dist": True
        }
    }
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=2)

    print(f'Project files created at {PROJECT_DIR}')


def install_dependencies():
    """Install npm dependencies."""
    print('Installing npm dependencies...')
    result = shell(f'cd "{PROJECT_DIR}" && npm install', timeout=120)
    if result.returncode != 0:
        print(f'npm install stderr: {result.stderr[-500:]}')
    print(f'npm install complete. stdout tail: {result.stdout[-500:] if result.stdout else "(empty)"}')

    # Verify Jest works
    result = shell(f'cd "{PROJECT_DIR}" && npx jest --version', timeout=30)
    print(f'Jest version: {result.stdout.strip()}')


def create_initial():
    install_node()
    create_project()
    install_dependencies()

    # Verify tests pass with Jest
    print('Running Jest tests...')
    result = shell(f'cd "{PROJECT_DIR}" && npx jest --verbose 2>&1', timeout=60)
    print(f'Jest test output:\n{result.stdout[-1000:]}')
    if result.returncode != 0:
        print(f'Jest stderr:\n{result.stderr[-500:]}')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
