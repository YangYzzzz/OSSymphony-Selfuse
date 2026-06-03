"""
Initial Setup: JSDoc-driven type system for a JavaScript project
Task ID: vscode_gf3_077
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_077'
PROJECT_ROOT = f'{WORKDIR}/projects/js-app'
SRC_DIR = f'{PROJECT_ROOT}/src'
API_DIR = f'{SRC_DIR}/api'
CLIENT_FILE = f'{API_DIR}/client.js'


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
    # Create directory structure
    os.makedirs(API_DIR, exist_ok=True)
    os.makedirs(f'{SRC_DIR}/models', exist_ok=True)
    os.makedirs(f'{SRC_DIR}/utils', exist_ok=True)

    # --- src/api/client.js (NO JSDoc typedefs, NO @ts-check, NO @template) ---
    client_js = '''\
const BASE_URL = 'https://api.example.com/v2';

const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

let authToken = null;

/**
 * Sets the authentication token for subsequent API requests.
 * @param {string} token - The bearer token to use.
 */
function setAuthToken(token) {
  authToken = token;
}

/**
 * Builds request headers, optionally including the auth token.
 * @returns {object} The merged headers object.
 */
function buildHeaders() {
  const headers = { ...DEFAULT_HEADERS };
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }
  return headers;
}

/**
 * Performs a GET request to the specified endpoint.
 * @param {string} endpoint - The API endpoint path.
 * @param {object} [queryParams] - Optional query string parameters.
 * @returns {Promise<object>} The parsed JSON response.
 */
async function get(endpoint, queryParams = {}) {
  const url = new URL(`${BASE_URL}${endpoint}`);
  Object.entries(queryParams).forEach(([key, value]) => {
    url.searchParams.append(key, value);
  });

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: buildHeaders(),
  });

  if (!response.ok) {
    throw new Error(`GET ${endpoint} failed with status ${response.status}`);
  }

  return response.json();
}

/**
 * Performs a POST request to the specified endpoint.
 * @param {string} endpoint - The API endpoint path.
 * @param {object} body - The request body to send as JSON.
 * @returns {Promise<object>} The parsed JSON response.
 */
async function post(endpoint, body) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: buildHeaders(),
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`POST ${endpoint} failed with status ${response.status}`);
  }

  return response.json();
}

/**
 * Fetches a single user by their ID.
 * @param {number} userId - The ID of the user to retrieve.
 * @returns {Promise<object>} The user data from the API.
 */
async function fetchUser(userId) {
  const result = await get(`/users/${userId}`);
  return result.data;
}

/**
 * Creates a new user account.
 * @param {string} name - Full name of the user.
 * @param {string} email - Email address.
 * @param {string} role - User role (e.g., 'admin', 'editor', 'viewer').
 * @returns {Promise<object>} The created user object.
 */
async function createUser(name, email, role) {
  const result = await post('/users', { name, email, role });
  return result.data;
}

/**
 * Fetches a paginated list of resources from the given endpoint.
 * @param {string} endpoint - The API endpoint to query.
 * @param {number} [page=1] - The page number to fetch.
 * @param {number} [pageSize=20] - Number of items per page.
 * @returns {Promise<object>} The paginated result with items and metadata.
 */
async function fetchPaginated(endpoint, page = 1, pageSize = 20) {
  const result = await get(endpoint, { page, pageSize });
  return {
    items: result.data,
    totalCount: result.meta.totalCount,
    currentPage: result.meta.page,
    totalPages: Math.ceil(result.meta.totalCount / pageSize),
    hasNextPage: page < Math.ceil(result.meta.totalCount / pageSize),
  };
}

/**
 * Searches users by a query string with pagination support.
 * @param {string} query - The search term.
 * @param {number} [page=1] - Page number.
 * @returns {Promise<object>} Paginated search results.
 */
async function searchUsers(query, page = 1) {
  return fetchPaginated(`/users/search?q=${encodeURIComponent(query)}`, page, 10);
}

/**
 * Deletes a user by ID.
 * @param {number} userId - The ID of the user to delete.
 * @returns {Promise<object>} The API response confirming deletion.
 */
async function deleteUser(userId) {
  const response = await fetch(`${BASE_URL}/users/${userId}`, {
    method: 'DELETE',
    headers: buildHeaders(),
  });

  if (!response.ok) {
    throw new Error(`DELETE /users/${userId} failed with status ${response.status}`);
  }

  return response.json();
}

module.exports = {
  setAuthToken,
  get,
  post,
  fetchUser,
  createUser,
  fetchPaginated,
  searchUsers,
  deleteUser,
};
'''
    with open(CLIENT_FILE, 'w') as f:
        f.write(client_js)
    print(f'Created: {CLIENT_FILE}')

    # --- src/models/user.js (supporting file for realism) ---
    user_model = '''\
/**
 * Validates a user object has the required fields.
 * @param {object} user - The user object to validate.
 * @returns {boolean} True if the user is valid.
 */
function validateUser(user) {
  if (!user || typeof user !== 'object') return false;
  if (!user.name || typeof user.name !== 'string') return false;
  if (!user.email || !user.email.includes('@')) return false;
  if (!['admin', 'editor', 'viewer'].includes(user.role)) return false;
  return true;
}

/**
 * Formats a user object for display.
 * @param {object} user - The user object.
 * @returns {string} A formatted string representation.
 */
function formatUserDisplay(user) {
  return `${user.name} <${user.email}> [${user.role}]`;
}

module.exports = { validateUser, formatUserDisplay };
'''
    with open(f'{SRC_DIR}/models/user.js', 'w') as f:
        f.write(user_model)

    # --- src/utils/logger.js (supporting file for realism) ---
    logger_js = '''\
const LOG_LEVELS = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };
let currentLevel = LOG_LEVELS.INFO;

function setLevel(level) {
  currentLevel = LOG_LEVELS[level] || LOG_LEVELS.INFO;
}

function log(level, message, data) {
  if (LOG_LEVELS[level] >= currentLevel) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level}] ${message}`, data || '');
  }
}

module.exports = {
  setLevel,
  debug: (msg, data) => log('DEBUG', msg, data),
  info: (msg, data) => log('INFO', msg, data),
  warn: (msg, data) => log('WARN', msg, data),
  error: (msg, data) => log('ERROR', msg, data),
};
'''
    with open(f'{SRC_DIR}/utils/logger.js', 'w') as f:
        f.write(logger_js)

    # --- package.json (project file for realism) ---
    package_json = {
        "name": "js-app",
        "version": "1.0.0",
        "description": "Internal API client library for user management",
        "main": "src/api/client.js",
        "scripts": {
            "start": "node src/index.js",
            "test": "jest"
        },
        "dependencies": {
            "node-fetch": "^2.6.7"
        },
        "devDependencies": {
            "jest": "^29.5.0"
        }
    }
    import json
    with open(f'{PROJECT_ROOT}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    # NO jsconfig.json — the task is to create it
    print(f'Project structure created at {PROJECT_ROOT}')

    # GUI-ready: open VSCode with the client.js file
    launch_gui(f'code "{PROJECT_ROOT}"', delay_sec=2.0)
    launch_gui(f'code "{CLIENT_FILE}"', delay_sec=1.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
