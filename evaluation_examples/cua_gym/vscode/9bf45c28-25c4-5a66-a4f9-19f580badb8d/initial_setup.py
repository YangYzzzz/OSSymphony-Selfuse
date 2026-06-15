"""
Initial Setup: Use the Outline view to navigate through this TypeScript class and find the 'updateUser' method.
Task ID: vscode_code_076
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_076'
PROJECT_DIR = '/home/user/project'
TS_FILE = '/home/user/project/user-service.ts'

TS_CONTENT = """\
import { Database } from './db';
import { Logger } from './logger';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  createdAt: Date;
  updatedAt: Date;
}

class UserService {
  private db: Database;
  private logger: Logger;

  constructor(db: Database, logger: Logger) {
    this.db = db;
    this.logger = logger;
  }

  async getAll(): Promise<User[]> {
    try {
      this.logger.info('Fetching all users');
      const users = await this.db.query('SELECT * FROM users ORDER BY created_at DESC');
      this.logger.info(`Found ${users.length} users`);
      return users as User[];
    } catch (error) {
      this.logger.error('Failed to fetch users', error);
      throw new Error('Could not retrieve users');
    }
  }

  async getById(id: number): Promise<User | null> {
    try {
      this.logger.info(`Fetching user with id=${id}`);
      const result = await this.db.query('SELECT * FROM users WHERE id = ?', [id]);
      if (result.length === 0) {
        this.logger.warn(`User with id=${id} not found`);
        return null;
      }
      return result[0] as User;
    } catch (error) {
      this.logger.error(`Failed to fetch user id=${id}`, error);
      throw new Error(`Could not retrieve user with id=${id}`);
    }
  }

  async createUser(data: Partial<User>): Promise<User> {
    try {
      this.logger.info('Creating new user', { email: data.email });
      if (!data.email || !data.name) {
        throw new Error('Name and email are required');
      }
      const existing = await this.db.query('SELECT id FROM users WHERE email = ?', [data.email]);
      if (existing.length > 0) {
        throw new Error(`User with email ${data.email} already exists`);
      }
      const result = await this.db.execute(
        'INSERT INTO users (name, email, role, created_at, updated_at) VALUES (?, ?, ?, NOW(), NOW())',
        [data.name, data.email, data.role || 'viewer']
      );
      const newUser = await this.getById(result.insertId);
      this.logger.info(`Created user id=${result.insertId}`);
      return newUser!;
    } catch (error) {
      this.logger.error('Failed to create user', error);
      throw error;
    }
  }

  async updateUser(id: number, data: Partial<User>): Promise<User> {
    try {
      this.logger.info(`Updating user id=${id}`, data);
      const existing = await this.getById(id);
      if (!existing) {
        throw new Error(`User with id=${id} not found`);
      }
      const updates: string[] = [];
      const values: any[] = [];
      if (data.name !== undefined) { updates.push('name = ?'); values.push(data.name); }
      if (data.email !== undefined) { updates.push('email = ?'); values.push(data.email); }
      if (data.role !== undefined) { updates.push('role = ?'); values.push(data.role); }
      updates.push('updated_at = NOW()');
      if (updates.length === 1) {
        this.logger.warn(`No fields to update for user id=${id}`);
        return existing;
      }
      values.push(id);
      await this.db.execute(
        `UPDATE users SET ${updates.join(', ')} WHERE id = ?`,
        values
      );
      const updated = await this.getById(id);
      this.logger.info(`Updated user id=${id} successfully`);
      return updated!;
    } catch (error) {
      this.logger.error(`Failed to update user id=${id}`, error);
      throw error;
    }
  }

  async deleteUser(id: number): Promise<boolean> {
    try {
      this.logger.info(`Deleting user id=${id}`);
      const existing = await this.getById(id);
      if (!existing) {
        this.logger.warn(`User id=${id} not found for deletion`);
        return false;
      }
      await this.db.execute('DELETE FROM users WHERE id = ?', [id]);
      this.logger.info(`Deleted user id=${id}`);
      return true;
    } catch (error) {
      this.logger.error(`Failed to delete user id=${id}`, error);
      throw new Error(`Could not delete user with id=${id}`);
    }
  }

  async searchUsers(query: string): Promise<User[]> {
    try {
      this.logger.info(`Searching users with query="${query}"`);
      const pattern = `%${query}%`;
      const results = await this.db.query(
        'SELECT * FROM users WHERE name LIKE ? OR email LIKE ? ORDER BY name ASC',
        [pattern, pattern]
      );
      this.logger.info(`Search returned ${results.length} result(s)`);
      return results as User[];
    } catch (error) {
      this.logger.error('Failed to search users', error);
      throw new Error('User search failed');
    }
  }
}

export { UserService, User };
"""


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write the TypeScript file
    with open(TS_FILE, 'w') as f:
        f.write(TS_CONTENT)
    print(f'TypeScript file created: {TS_FILE}')

    # Ensure cursor state JSON does NOT exist (initial state)
    cursor_state_path = f'{WORKDIR}/{TASK_ID}_cursor_state.json'
    if os.path.exists(cursor_state_path):
        os.remove(cursor_state_path)
        print(f'Removed stale cursor state file: {cursor_state_path}')

    # GUI-ready startup: open VSCode with the TypeScript file
    launch_gui(f'code "{TS_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
