"""
Initial Setup: Unfold all collapsed code in service.js
Task ID: vscode_code_028
Domain: vs_code

Creates /home/user/project/service.js with ~172 lines of JavaScript code
containing classes and functions with foldable blocks.

Strategy:
1. Kill any existing VSCode processes
2. Create project dir and service.js
3. Directly create workspace storage (no waiting for VSCode to start)
4. Write collapsedRegions into state.vscdb to simulate "all code folded" state
5. Launch VSCode non-blocking (it will read the pre-seeded workspace state)
"""

import os
import shlex
import subprocess
import time
import sqlite3
import json
import hashlib

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_028'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/service.js'
WORKSPACE_STORAGE = '/home/user/.config/Code/User/workspaceStorage'

FOLDER_URI = 'file:///home/user/project'
FILE_URI = 'file:///home/user/project/service.js'


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


def kill_vscode():
    """Kill all running VSCode processes."""
    subprocess.run(['pkill', '-f', 'code'], capture_output=True)
    time.sleep(2)


def find_workspace_hash(folder_uri):
    """Find existing workspace storage directory for given folder URI."""
    if not os.path.exists(WORKSPACE_STORAGE):
        return None
    for d in os.listdir(WORKSPACE_STORAGE):
        wj = os.path.join(WORKSPACE_STORAGE, d, 'workspace.json')
        if os.path.exists(wj):
            try:
                with open(wj) as f:
                    data = json.load(f)
                if data.get('folder') == folder_uri:
                    return d
            except (json.JSONDecodeError, IOError):
                continue
    return None


def write_fold_state_to_db(db_path, fold_state, file_uri):
    """Write folding state to a VSCode workspace state.vscdb SQLite database."""
    editor_state = {
        "textEditorViewState": [
            [
                file_uri,
                {
                    "0": {
                        "cursorState": [
                            {
                                "inSelectionMode": False,
                                "selectionStart": {"lineNumber": 1, "column": 1},
                                "position": {"lineNumber": 1, "column": 1}
                            }
                        ],
                        "viewState": {
                            "scrollLeft": 0,
                            "firstPosition": {"lineNumber": 1, "column": 1},
                            "firstPositionDeltaTop": 0
                        },
                        "contributionsState": {
                            "editor.contrib.folding": fold_state,
                            "editor.contrib.wordHighlighter": False
                        }
                    }
                }
            ]
        ]
    }
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE IF NOT EXISTS ItemTable (key TEXT UNIQUE, value BLOB)')
    conn.execute(
        'INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)',
        ('memento/workbench.editors.files.textFileEditor', json.dumps(editor_state))
    )
    conn.commit()
    conn.close()

    # Verify the write
    conn2 = sqlite3.connect(db_path)
    row = conn2.execute(
        "SELECT value FROM ItemTable WHERE key='memento/workbench.editors.files.textFileEditor'"
    ).fetchone()
    conn2.close()
    if row:
        val = json.loads(row[0])
        regions = (val.get('textEditorViewState', [[]])[0][1]
                   .get('0', {})
                   .get('contributionsState', {})
                   .get('editor.contrib.folding', {})
                   .get('collapsedRegions'))
        print(f'  Verified collapsedRegions in DB: {regions}')
    else:
        print('  WARNING: Could not verify DB write!')


def create_initial():
    # 1. Kill any existing VSCode processes
    print('Killing any existing VSCode processes...')
    kill_vscode()

    # 2. Create project directory and service.js
    os.makedirs(PROJECT_DIR, exist_ok=True)

    js_content = """\
'use strict';

const mysql = require('mysql2/promise');
const redis = require('redis');
const axios = require('axios');

// Configuration constants
const DB_CONFIG = {
    host: 'localhost',
    port: 3306,
    database: 'app_production',
    user: 'app_user',
    password: process.env.DB_PASSWORD || 'changeme',
    connectionLimit: 10,
};

const CACHE_TTL = 3600; // seconds
const API_TIMEOUT = 5000; // ms

class DatabaseService {
    constructor(config = DB_CONFIG) {
        this.config = config;
        this.pool = null;
    }

    async connect() {
        if (!this.pool) {
            this.pool = await mysql.createPool(this.config);
            console.log('[DatabaseService] Connection pool created');
        }
        return this.pool;
    }

    async query(sql, params = []) {
        const pool = await this.connect();
        const [rows] = await pool.execute(sql, params);
        return rows;
    }

    async findById(table, id) {
        const rows = await this.query(
            `SELECT * FROM ?? WHERE id = ? LIMIT 1`,
            [table, id]
        );
        return rows[0] || null;
    }

    async insert(table, data) {
        const keys = Object.keys(data);
        const values = Object.values(data);
        const placeholders = keys.map(() => '?').join(', ');
        const sql = `INSERT INTO ?? (${keys.map(() => '??').join(', ')}) VALUES (${placeholders})`;
        const result = await this.query(sql, [table, ...keys, ...values]);
        return result.insertId;
    }

    async disconnect() {
        if (this.pool) {
            await this.pool.end();
            this.pool = null;
            console.log('[DatabaseService] Pool closed');
        }
    }
}

class CacheService {
    constructor(options = {}) {
        this.host = options.host || '127.0.0.1';
        this.port = options.port || 6379;
        this.client = null;
        this.ttl = options.ttl || CACHE_TTL;
    }

    async connect() {
        if (!this.client) {
            this.client = redis.createClient({
                socket: { host: this.host, port: this.port },
            });
            await this.client.connect();
            console.log('[CacheService] Connected to Redis');
        }
        return this.client;
    }

    async get(key) {
        const client = await this.connect();
        const value = await client.get(key);
        return value ? JSON.parse(value) : null;
    }

    async set(key, value, ttl = this.ttl) {
        const client = await this.connect();
        await client.setEx(key, ttl, JSON.stringify(value));
    }

    async del(key) {
        const client = await this.connect();
        await client.del(key);
    }

    async flush() {
        const client = await this.connect();
        await client.flushDb();
        console.log('[CacheService] Cache flushed');
    }

    async disconnect() {
        if (this.client) {
            await this.client.quit();
            this.client = null;
            console.log('[CacheService] Disconnected from Redis');
        }
    }
}

class ApiService {
    constructor(baseUrl, options = {}) {
        this.baseUrl = baseUrl;
        this.timeout = options.timeout || API_TIMEOUT;
        this.headers = options.headers || { 'Content-Type': 'application/json' };
    }

    async get(path, params = {}) {
        const response = await axios.get(`${this.baseUrl}${path}`, {
            params,
            headers: this.headers,
            timeout: this.timeout,
        });
        return response.data;
    }

    async post(path, body = {}) {
        const response = await axios.post(`${this.baseUrl}${path}`, body, {
            headers: this.headers,
            timeout: this.timeout,
        });
        return response.data;
    }

    async put(path, body = {}) {
        const response = await axios.put(`${this.baseUrl}${path}`, body, {
            headers: this.headers,
            timeout: this.timeout,
        });
        return response.data;
    }

    async delete(path) {
        const response = await axios.delete(`${this.baseUrl}${path}`, {
            headers: this.headers,
            timeout: this.timeout,
        });
        return response.data;
    }
}

function initialize() {
    const db = new DatabaseService(DB_CONFIG);
    const cache = new CacheService({ host: '127.0.0.1', port: 6379, ttl: CACHE_TTL });
    const api = new ApiService('https://api.example.com/v1', { timeout: API_TIMEOUT });

    process.on('SIGTERM', async () => {
        console.log('Shutting down services...');
        await db.disconnect();
        await cache.disconnect();
        process.exit(0);
    });

    return { db, cache, api };
}

module.exports = { DatabaseService, CacheService, ApiService, initialize };
"""

    with open(OUTPUT, 'w') as f:
        f.write(js_content)

    line_count = js_content.count('\n')
    print(f'Initial file created: {OUTPUT} ({line_count} lines)')

    # 3. Create workspace storage directory DIRECTLY (no waiting for VSCode).
    #    VSCode is killed, so we write the DB without risk of overwrite.
    os.makedirs(WORKSPACE_STORAGE, exist_ok=True)

    # Use existing workspace dir if it points to our project, or create md5-based one
    existing_hash = find_workspace_hash(FOLDER_URI)
    if existing_hash:
        ws_dir = os.path.join(WORKSPACE_STORAGE, existing_hash)
        print(f'Using existing workspace storage dir: {existing_hash}')
    else:
        # Create canonical dir with md5 hash of the folder URI
        ws_hash = hashlib.md5(FOLDER_URI.encode()).hexdigest()
        ws_dir = os.path.join(WORKSPACE_STORAGE, ws_hash)
        os.makedirs(ws_dir, exist_ok=True)
        with open(os.path.join(ws_dir, 'workspace.json'), 'w') as f:
            json.dump({"folder": FOLDER_URI}, f)
        print(f'Created new workspace storage dir: {ws_hash}')

    db_path = os.path.join(ws_dir, 'state.vscdb')

    # 4. Write collapsed fold regions to state.vscdb
    # Line ranges: DatabaseService class body (lines 20-60),
    #              CacheService class body (62-115),
    #              ApiService class body (117-155),
    #              initialize function body (157-171)
    fold_state = {
        "lineCount": 173,
        "provider": "syntax",
        "foldedImports": False,
        "collapsedRegions": [[20, 60], [62, 115], [117, 155], [157, 171]]
    }

    write_fold_state_to_db(db_path, fold_state, FILE_URI)
    print(f'Fold state with collapsedRegions written to: {db_path}')

    # 5. Launch VSCode non-blocking — it will read the pre-seeded workspace state
    print('Launching VSCode with project directory...')
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')
    print('Initial setup complete: service.js created with collapsed fold regions in workspace DB.')


create_initial()
