"""
Initial Setup: Install Jest Runner extension and configure settings in VSCode
Task ID: vscode_gf3_039
Domain: vscode

Creates a realistic Node.js API project with Jest test files,
then opens VSCode with the test file. No Jest Runner extension
installed, no jestrunner settings configured.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_039'
PROJECT_DIR = f'{WORKDIR}/projects/node-api'
TEST_DIR = f'{PROJECT_DIR}/src/__tests__'
SRC_DIR = f'{PROJECT_DIR}/src'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'
TEST_FILE = f'{TEST_DIR}/userService.test.js'


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


def create_project():
    """Create the Node.js API project structure."""
    # Create directories
    os.makedirs(TEST_DIR, exist_ok=True)
    os.makedirs(f'{SRC_DIR}/models', exist_ok=True)
    os.makedirs(f'{SRC_DIR}/services', exist_ok=True)
    os.makedirs(f'{SRC_DIR}/routes', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/node_modules/.bin', exist_ok=True)

    # package.json
    package_json = {
        "name": "node-api",
        "version": "1.2.0",
        "description": "User management REST API",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "nodemon src/index.js",
            "test": "jest --verbose",
            "test:watch": "jest --watch",
            "test:coverage": "jest --coverage"
        },
        "dependencies": {
            "express": "^4.18.2",
            "mongoose": "^7.6.3",
            "bcryptjs": "^2.4.3",
            "jsonwebtoken": "^9.0.2",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "jest": "^29.7.0",
            "supertest": "^6.3.3",
            "nodemon": "^3.0.1"
        },
        "jest": {
            "testEnvironment": "node",
            "collectCoverageFrom": ["src/**/*.js", "!src/index.js"],
            "coverageDirectory": "coverage"
        }
    }
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # jest.config.js
    with open(f'{PROJECT_DIR}/jest.config.js', 'w') as f:
        f.write("""module.exports = {
  testEnvironment: 'node',
  verbose: true,
  collectCoverageFrom: ['src/**/*.js', '!src/index.js'],
  coverageDirectory: 'coverage',
  testMatch: ['**/__tests__/**/*.test.js'],
  setupFilesAfterSetup: ['./src/__tests__/setup.js'],
};
""")

    # src/models/User.js
    with open(f'{SRC_DIR}/models/User.js', 'w') as f:
        f.write("""const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true, minlength: 8 },
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
  isActive: { type: Boolean, default: true },
  lastLogin: { type: Date },
  createdAt: { type: Date, default: Date.now },
});

userSchema.pre('save', async function (next) {
  if (this.isModified('password')) {
    this.password = await bcrypt.hash(this.password, 10);
  }
  next();
});

userSchema.methods.comparePassword = async function (candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
""")

    # src/services/userService.js
    with open(f'{SRC_DIR}/services/userService.js', 'w') as f:
        f.write("""const User = require('../models/User');
const jwt = require('jsonwebtoken');

class UserService {
  async createUser(userData) {
    const existingUser = await User.findOne({ email: userData.email });
    if (existingUser) {
      throw new Error('Email already registered');
    }
    const user = new User(userData);
    await user.save();
    return user;
  }

  async getUserById(id) {
    const user = await User.findById(id).select('-password');
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async updateUser(id, updates) {
    const allowedUpdates = ['name', 'email', 'role', 'isActive'];
    const filteredUpdates = {};
    for (const key of Object.keys(updates)) {
      if (allowedUpdates.includes(key)) {
        filteredUpdates[key] = updates[key];
      }
    }
    const user = await User.findByIdAndUpdate(id, filteredUpdates, {
      new: true,
      runValidators: true,
    }).select('-password');
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async deleteUser(id) {
    const user = await User.findByIdAndDelete(id);
    if (!user) {
      throw new Error('User not found');
    }
    return { message: 'User deleted successfully' };
  }

  async listUsers(filters = {}) {
    const query = {};
    if (filters.role) query.role = filters.role;
    if (filters.isActive !== undefined) query.isActive = filters.isActive;
    return User.find(query).select('-password').sort({ createdAt: -1 });
  }

  generateToken(user) {
    return jwt.sign(
      { id: user._id, email: user.email, role: user.role },
      process.env.JWT_SECRET || 'dev-secret-key',
      { expiresIn: '24h' }
    );
  }

  async authenticateUser(email, password) {
    const user = await User.findOne({ email });
    if (!user || !(await user.comparePassword(password))) {
      throw new Error('Invalid credentials');
    }
    user.lastLogin = new Date();
    await user.save();
    return { user, token: this.generateToken(user) };
  }
}

module.exports = new UserService();
""")

    # src/routes/userRoutes.js
    with open(f'{SRC_DIR}/routes/userRoutes.js', 'w') as f:
        f.write("""const express = require('express');
const router = express.Router();
const userService = require('../services/userService');

router.post('/register', async (req, res) => {
  try {
    const user = await userService.createUser(req.body);
    const token = userService.generateToken(user);
    res.status(201).json({ user, token });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const result = await userService.authenticateUser(email, password);
    res.json(result);
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const user = await userService.getUserById(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

router.put('/:id', async (req, res) => {
  try {
    const user = await userService.updateUser(req.params.id, req.body);
    res.json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.delete('/:id', async (req, res) => {
  try {
    const result = await userService.deleteUser(req.params.id);
    res.json(result);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

router.get('/', async (req, res) => {
  try {
    const users = await userService.listUsers(req.query);
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
""")

    # src/index.js
    with open(f'{SRC_DIR}/index.js', 'w') as f:
        f.write("""require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const userRoutes = require('./routes/userRoutes');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/node-api';

app.use(express.json());
app.use('/api/users', userRoutes);

app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

mongoose.connect(MONGO_URI)
  .then(() => {
    console.log('Connected to MongoDB');
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  })
  .catch((err) => {
    console.error('MongoDB connection error:', err);
    process.exit(1);
  });

module.exports = app;
""")

    # Test setup file
    with open(f'{TEST_DIR}/setup.js', 'w') as f:
        f.write("""const mongoose = require('mongoose');

beforeAll(async () => {
  const mongoUri = process.env.MONGO_TEST_URI || 'mongodb://localhost:27017/node-api-test';
  await mongoose.connect(mongoUri);
});

afterAll(async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.connection.close();
});

afterEach(async () => {
  const collections = mongoose.connection.collections;
  for (const key in collections) {
    await collections[key].deleteMany({});
  }
});
""")

    # Main test file with multiple describe blocks and test cases
    with open(TEST_FILE, 'w') as f:
        f.write("""const UserService = require('../../services/userService');
const User = require('../../models/User');

// Mock the User model
jest.mock('../../models/User');

describe('UserService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    const validUserData = {
      name: 'Sarah Chen',
      email: 'sarah.chen@techcorp.io',
      password: 'SecurePass123!',
      role: 'user',
    };

    test('should create a new user successfully', async () => {
      User.findOne.mockResolvedValue(null);
      const mockUser = { ...validUserData, _id: 'abc123', save: jest.fn() };
      User.mockImplementation(() => mockUser);

      const result = await UserService.createUser(validUserData);
      expect(result.name).toBe('Sarah Chen');
      expect(result.email).toBe('sarah.chen@techcorp.io');
    });

    test('should throw error if email already exists', async () => {
      User.findOne.mockResolvedValue({ email: 'sarah.chen@techcorp.io' });

      await expect(
        UserService.createUser(validUserData)
      ).rejects.toThrow('Email already registered');
    });

    test('should assign default role as user', async () => {
      User.findOne.mockResolvedValue(null);
      const mockUser = { ...validUserData, role: 'user', save: jest.fn() };
      User.mockImplementation(() => mockUser);

      const result = await UserService.createUser({
        name: 'Marcus Johnson',
        email: 'marcus.j@techcorp.io',
        password: 'AnotherPass456!',
      });
      expect(result.role).toBe('user');
    });
  });

  describe('getUserById', () => {
    test('should return user without password', async () => {
      const mockUser = {
        _id: 'user123',
        name: 'Elena Rodriguez',
        email: 'elena.r@techcorp.io',
        role: 'admin',
      };
      User.findById.mockReturnValue({
        select: jest.fn().mockResolvedValue(mockUser),
      });

      const result = await UserService.getUserById('user123');
      expect(result.name).toBe('Elena Rodriguez');
      expect(result).not.toHaveProperty('password');
    });

    test('should throw error if user not found', async () => {
      User.findById.mockReturnValue({
        select: jest.fn().mockResolvedValue(null),
      });

      await expect(
        UserService.getUserById('nonexistent')
      ).rejects.toThrow('User not found');
    });
  });

  describe('updateUser', () => {
    test('should update allowed fields only', async () => {
      const updatedUser = {
        _id: 'user456',
        name: 'Updated Name',
        email: 'updated@techcorp.io',
        role: 'admin',
      };
      User.findByIdAndUpdate.mockReturnValue({
        select: jest.fn().mockResolvedValue(updatedUser),
      });

      const result = await UserService.updateUser('user456', {
        name: 'Updated Name',
        password: 'shouldBeIgnored',
      });
      expect(result.name).toBe('Updated Name');
    });

    test('should throw error for non-existent user', async () => {
      User.findByIdAndUpdate.mockReturnValue({
        select: jest.fn().mockResolvedValue(null),
      });

      await expect(
        UserService.updateUser('nonexistent', { name: 'Test' })
      ).rejects.toThrow('User not found');
    });

    test('should filter out disallowed update fields', async () => {
      User.findByIdAndUpdate.mockReturnValue({
        select: jest.fn().mockResolvedValue({ _id: 'user789' }),
      });

      await UserService.updateUser('user789', {
        name: 'Valid',
        password: 'NotAllowed',
        createdAt: 'NotAllowed',
      });

      expect(User.findByIdAndUpdate).toHaveBeenCalledWith(
        'user789',
        { name: 'Valid' },
        expect.any(Object)
      );
    });
  });

  describe('deleteUser', () => {
    test('should delete user successfully', async () => {
      User.findByIdAndDelete.mockResolvedValue({ _id: 'user101' });

      const result = await UserService.deleteUser('user101');
      expect(result.message).toBe('User deleted successfully');
    });

    test('should throw error if user not found', async () => {
      User.findByIdAndDelete.mockResolvedValue(null);

      await expect(
        UserService.deleteUser('nonexistent')
      ).rejects.toThrow('User not found');
    });
  });

  describe('listUsers', () => {
    test('should return all users without filters', async () => {
      const mockUsers = [
        { name: 'Sarah Chen', email: 'sarah@techcorp.io' },
        { name: 'Marcus Johnson', email: 'marcus@techcorp.io' },
        { name: 'Elena Rodriguez', email: 'elena@techcorp.io' },
      ];
      User.find.mockReturnValue({
        select: jest.fn().mockReturnValue({
          sort: jest.fn().mockResolvedValue(mockUsers),
        }),
      });

      const result = await UserService.listUsers();
      expect(result).toHaveLength(3);
    });

    test('should filter users by role', async () => {
      const adminUsers = [
        { name: 'Elena Rodriguez', role: 'admin' },
      ];
      User.find.mockReturnValue({
        select: jest.fn().mockReturnValue({
          sort: jest.fn().mockResolvedValue(adminUsers),
        }),
      });

      const result = await UserService.listUsers({ role: 'admin' });
      expect(result).toHaveLength(1);
      expect(User.find).toHaveBeenCalledWith({ role: 'admin' });
    });

    test('should filter users by active status', async () => {
      User.find.mockReturnValue({
        select: jest.fn().mockReturnValue({
          sort: jest.fn().mockResolvedValue([]),
        }),
      });

      await UserService.listUsers({ isActive: false });
      expect(User.find).toHaveBeenCalledWith({ isActive: false });
    });
  });

  describe('authenticateUser', () => {
    test('should authenticate valid credentials', async () => {
      const mockUser = {
        _id: 'auth1',
        email: 'sarah@techcorp.io',
        role: 'user',
        comparePassword: jest.fn().mockResolvedValue(true),
        save: jest.fn(),
      };
      User.findOne.mockResolvedValue(mockUser);

      const result = await UserService.authenticateUser(
        'sarah@techcorp.io',
        'SecurePass123!'
      );
      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
    });

    test('should reject invalid password', async () => {
      const mockUser = {
        comparePassword: jest.fn().mockResolvedValue(false),
      };
      User.findOne.mockResolvedValue(mockUser);

      await expect(
        UserService.authenticateUser('sarah@techcorp.io', 'wrong')
      ).rejects.toThrow('Invalid credentials');
    });

    test('should reject non-existent email', async () => {
      User.findOne.mockResolvedValue(null);

      await expect(
        UserService.authenticateUser('nobody@techcorp.io', 'password')
      ).rejects.toThrow('Invalid credentials');
    });
  });
});
""")

    # .env file
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write("""PORT=3000
MONGO_URI=mongodb://localhost:27017/node-api
MONGO_TEST_URI=mongodb://localhost:27017/node-api-test
JWT_SECRET=a7f3c9e2b1d4f6a8c0e3b5d7f9a1c3e5
NODE_ENV=development
""")

    # .gitignore
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""node_modules/
coverage/
.env
*.log
dist/
""")

    # Create a fake npx in node_modules/.bin for realism
    with open(f'{PROJECT_DIR}/node_modules/.bin/jest', 'w') as f:
        f.write("#!/usr/bin/env node\nconsole.log('jest v29.7.0');\n")
    os.chmod(f'{PROJECT_DIR}/node_modules/.bin/jest', 0o755)

    print(f'Project created at {PROJECT_DIR}')
    print(f'Test file created at {TEST_FILE}')


def setup_vscode_settings():
    """Set up VSCode settings WITHOUT any jestrunner configuration."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Basic VSCode settings (no jestrunner settings!)
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "terminal.integrated.defaultProfile.linux": "bash",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    # Ensure no jestrunner settings exist
    keys_to_remove = [k for k in settings if k.startswith('jestrunner.')]
    for k in keys_to_remove:
        del settings[k]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to {SETTINGS_PATH}')


def create_initial():
    create_project()
    setup_vscode_settings()

    # Open VSCode with the test file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{TEST_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
