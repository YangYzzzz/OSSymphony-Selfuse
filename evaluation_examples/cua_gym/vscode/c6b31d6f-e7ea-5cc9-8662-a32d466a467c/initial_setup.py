"""
Initial Setup: Create fetcher.js with 5 function declarations (3 missing async keyword)
Task ID: vscode_edit_082
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_082'
OUTPUT = f'{WORKDIR}/fetcher.js'

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
    os.makedirs(WORKDIR, exist_ok=True)

    # JavaScript file with 5 function declarations:
    # - fetchUser, fetchPosts, fetchComments: use 'await' but are missing 'async'
    # - parseData, formatOutput: do NOT use await
    js_content = """\
// fetcher.js — API data fetching utilities

const BASE_URL = 'https://api.example.com';

function fetchUser(userId) {
    const response = await fetch(`${BASE_URL}/users/${userId}`);
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    const data = await response.json();
    return data;
}

function fetchPosts(userId, limit = 10) {
    const response = await fetch(`${BASE_URL}/posts?userId=${userId}&limit=${limit}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch posts: ${response.status}`);
    }
    const posts = await response.json();
    return posts;
}

function fetchComments(postId) {
    const response = await fetch(`${BASE_URL}/comments?postId=${postId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch comments: ${response.status}`);
    }
    const comments = await response.json();
    return comments.filter(c => c.approved);
}

function parseData(rawData) {
    if (!rawData || typeof rawData !== 'object') {
        return null;
    }
    return {
        id: rawData.id,
        name: rawData.name || 'Unknown',
        email: rawData.email || '',
        createdAt: new Date(rawData.createdAt).toISOString(),
    };
}

function formatOutput(data, style = 'json') {
    if (style === 'json') {
        return JSON.stringify(data, null, 2);
    }
    if (style === 'csv') {
        const headers = Object.keys(data[0] || {}).join(',');
        const rows = data.map(row => Object.values(row).join(','));
        return [headers, ...rows].join('\\n');
    }
    return String(data);
}

module.exports = { fetchUser, fetchPosts, fetchComments, parseData, formatOutput };
"""

    with open(OUTPUT, 'w') as f:
        f.write(js_content)

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with fetcher.js and DISPLAY=:0')

create_initial()
