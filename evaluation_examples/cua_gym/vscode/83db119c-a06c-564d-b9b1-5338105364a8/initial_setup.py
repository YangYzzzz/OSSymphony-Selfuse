"""
Initial Setup: Add #region and #endregion markers to TypeScript file to organize code sections
Task ID: vscode_code_027
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_027'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/api.ts'


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

    # TypeScript file content WITHOUT #region markers (pre-task state)
    ts_content = """import express from 'express';
import { Database } from './db';

interface User {
  id: number;
  name: string;
  email: string;
}

interface Product {
  id: number;
  name: string;
  price: number;
}

function getUsers(db: Database): User[] {
  return db.query('SELECT * FROM users');
}

function getUserById(db: Database, id: number): User | null {
  return db.query('SELECT * FROM users WHERE id = ?', [id]);
}

function getProducts(db: Database): Product[] {
  return db.query('SELECT * FROM products');
}

function getProductById(db: Database, id: number): Product | null {
  return db.query('SELECT * FROM products WHERE id = ?', [id]);
}

export { getUsers, getUserById, getProducts, getProductById };
"""

    with open(OUTPUT, 'w') as f:
        f.write(ts_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the specific TypeScript file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
