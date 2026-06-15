"""
Initial Setup: Collapse all expanded folders in VSCode Explorer sidebar
Task ID: vscode_file_053
Domain: vs_code

Creates a big-project directory structure with all folders present and
opens VSCode with the project folder open. Sets VSCode workspace storage
so the explorer tree shows ALL folders EXPANDED (the pre-task state).
"""

import os
import json
import sqlite3
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_053'
PROJECT_DIR = f'{WORKDIR}/big-project'
PROJECT_URI = 'file:///home/user/big-project'
WS_STORAGE = '/home/user/.config/Code/User/workspaceStorage'


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


def create_file(path: str, content: str):
    """Create a file with specified content, making parent dirs as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def setup_workspace_storage_expanded():
    """
    Create or update the VSCode workspace storage for big-project so that
    the explorer treeViewState has ALL folders expanded (initial state).
    This ensures the agent has something to collapse.
    """
    os.makedirs(WS_STORAGE, exist_ok=True)

    # Check if workspace storage for big-project already exists
    ws_dir = None
    if os.path.isdir(WS_STORAGE):
        for entry in os.listdir(WS_STORAGE):
            wjson = os.path.join(WS_STORAGE, entry, 'workspace.json')
            if os.path.isfile(wjson):
                try:
                    with open(wjson) as f:
                        data = json.load(f)
                    if data.get('folder') == PROJECT_URI:
                        ws_dir = os.path.join(WS_STORAGE, entry)
                        break
                except (json.JSONDecodeError, KeyError):
                    pass

    if ws_dir is None:
        # Create a new workspace storage directory with a fixed hash-like name
        import uuid
        ws_dir = os.path.join(WS_STORAGE, uuid.uuid4().hex[:32])
        os.makedirs(ws_dir, exist_ok=True)
        with open(os.path.join(ws_dir, 'workspace.json'), 'w') as f:
            json.dump({"folder": PROJECT_URI}, f)
        print(f'Created new workspace storage at: {ws_dir}')
    else:
        print(f'Found existing workspace storage at: {ws_dir}')

    # Set treeViewState with ALL folders EXPANDED (this is the INITIAL state)
    # The agent's task is to collapse these folders
    expanded_folders = [
        "file:///home/user/big-project",
        "file:///home/user/big-project/src",
        "file:///home/user/big-project/src/components",
        "file:///home/user/big-project/src/components/ui",
        "file:///home/user/big-project/src/components/layout",
        "file:///home/user/big-project/src/pages",
        "file:///home/user/big-project/src/utils",
        "file:///home/user/big-project/tests",
        "file:///home/user/big-project/tests/unit"
    ]
    tree_state = json.dumps({
        "focus": [],
        "selection": [],
        "expanded": expanded_folders,
        "scrollTop": 0
    })

    db_path = os.path.join(ws_dir, 'state.vscdb')
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT UNIQUE, value TEXT)")
    conn.execute(
        "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
        ("workbench.explorer.treeViewState", tree_state)
    )
    conn.commit()
    conn.close()
    print(f'Set treeViewState with {len(expanded_folders)} folders expanded in: {db_path}')
    return ws_dir


def create_initial():
    # Create the project directory structure
    # src/components/ui/Button.jsx
    create_file(f'{PROJECT_DIR}/src/components/ui/Button.jsx', '''\
import React from 'react';

const Button = ({ label, onClick, variant = 'primary', disabled = false }) => {
    return (
        <button
            className={`btn btn-${variant}`}
            onClick={onClick}
            disabled={disabled}
        >
            {label}
        </button>
    );
};

export default Button;
''')

    # src/components/ui/Modal.jsx
    create_file(f'{PROJECT_DIR}/src/components/ui/Modal.jsx', '''\
import React from 'react';

const Modal = ({ isOpen, onClose, title, children }) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-container" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>{title}</h2>
                    <button className="modal-close" onClick={onClose}>×</button>
                </div>
                <div className="modal-body">
                    {children}
                </div>
            </div>
        </div>
    );
};

export default Modal;
''')

    # src/components/layout/Header.jsx
    create_file(f'{PROJECT_DIR}/src/components/layout/Header.jsx', '''\
import React from 'react';
import { Link } from 'react-router-dom';

const Header = ({ user, onLogout }) => {
    return (
        <header className="app-header">
            <nav className="nav-container">
                <div className="nav-brand">
                    <Link to="/">BigProject</Link>
                </div>
                <ul className="nav-links">
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/about">About</Link></li>
                    {user && (
                        <li>
                            <span>{user.name}</span>
                            <button onClick={onLogout}>Logout</button>
                        </li>
                    )}
                </ul>
            </nav>
        </header>
    );
};

export default Header;
''')

    # src/pages/Home.jsx
    create_file(f'{PROJECT_DIR}/src/pages/Home.jsx', '''\
import React, { useState, useEffect } from 'react';
import Button from '../components/ui/Button';

const Home = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulate fetching data
        setTimeout(() => {
            setItems([
                { id: 1, title: 'Project Alpha', status: 'active' },
                { id: 2, title: 'Project Beta', status: 'pending' },
                { id: 3, title: 'Project Gamma', status: 'completed' },
            ]);
            setLoading(false);
        }, 500);
    }, []);

    return (
        <div className="home-page">
            <h1>Welcome to BigProject</h1>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <ul>
                    {items.map(item => (
                        <li key={item.id}>
                            {item.title} - {item.status}
                        </li>
                    ))}
                </ul>
            )}
            <Button label="Create New Project" onClick={() => {}} />
        </div>
    );
};

export default Home;
''')

    # src/pages/About.jsx
    create_file(f'{PROJECT_DIR}/src/pages/About.jsx', '''\
import React from 'react';

const About = () => {
    return (
        <div className="about-page">
            <h1>About BigProject</h1>
            <p>
                BigProject is a comprehensive project management solution
                designed for modern development teams. It provides real-time
                collaboration, task tracking, and resource management tools.
            </p>
            <h2>Our Mission</h2>
            <p>
                To streamline the software development lifecycle by providing
                intuitive tools that reduce overhead and increase productivity.
            </p>
            <h2>Team</h2>
            <ul>
                <li>Sarah Chen - Lead Developer</li>
                <li>Marcus Johnson - UX Designer</li>
                <li>Emily Rodriguez - DevOps Engineer</li>
            </ul>
        </div>
    );
};

export default About;
''')

    # src/utils/helpers.js
    create_file(f'{PROJECT_DIR}/src/utils/helpers.js', '''\
/**
 * Utility helper functions for BigProject
 */

/**
 * Format a date string to a human-readable format
 * @param {string|Date} date - The date to format
 * @returns {string} Formatted date string
 */
export function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Truncate a string to a given length with ellipsis
 * @param {string} str - The string to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated string
 */
export function truncate(str, maxLength = 50) {
    if (str.length <= maxLength) return str;
    return str.slice(0, maxLength - 3) + '...';
}

/**
 * Debounce a function call
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, delay = 300) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), delay);
    };
}

/**
 * Deep clone an object
 * @param {Object} obj - Object to clone
 * @returns {Object} Cloned object
 */
export function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}
''')

    # tests/unit/button.test.js
    create_file(f'{PROJECT_DIR}/tests/unit/button.test.js', '''\
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../../src/components/ui/Button';

describe('Button component', () => {
    test('renders with correct label', () => {
        render(<Button label="Click Me" onClick={() => {}} />);
        expect(screen.getByText('Click Me')).toBeInTheDocument();
    });

    test('calls onClick handler when clicked', () => {
        const mockHandler = jest.fn();
        render(<Button label="Click Me" onClick={mockHandler} />);
        fireEvent.click(screen.getByText('Click Me'));
        expect(mockHandler).toHaveBeenCalledTimes(1);
    });

    test('applies variant class correctly', () => {
        render(<Button label="Danger" onClick={() => {}} variant="danger" />);
        const btn = screen.getByText('Danger');
        expect(btn).toHaveClass('btn-danger');
    });

    test('is disabled when disabled prop is true', () => {
        render(<Button label="Disabled" onClick={() => {}} disabled={true} />);
        const btn = screen.getByText('Disabled');
        expect(btn).toBeDisabled();
    });
});
''')

    # package.json
    create_file(f'{PROJECT_DIR}/package.json', '''\
{
  "name": "big-project",
  "version": "1.0.0",
  "description": "A comprehensive project management application",
  "main": "src/index.js",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "react-scripts": "5.0.1"
  },
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "jest": "^29.0.0"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
''')

    print(f'Project directory created: {PROJECT_DIR}')

    # Set up workspace storage with ALL folders EXPANDED (initial state for the task)
    ws_dir = setup_workspace_storage_expanded()
    print(f'Workspace storage configured with all folders expanded at: {ws_dir}')

    # GUI-ready startup: open VSCode with the big-project folder
    # VSCode will load the workspace storage and show the tree in expanded state
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with big-project folder open (DISPLAY=:0)')


create_initial()
