"""
Initial Setup: Resolve merge conflict in package.json
Task ID: vscode_git_052
Domain: vs_code

Creates a git repository at /home/user/webapp with an active merge conflict
in package.json. The main branch added "axios": "^1.4.0" and the
feature/analytics branch added "chart.js": "^4.3.0". Both are needed.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_052'
REPO_PATH = f'{WORKDIR}/webapp'


def run_cmd(cmd, cwd=None, env=None, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, env=env,
        capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f'CMD FAILED: {cmd}')
        print(f'STDOUT: {result.stdout}')
        print(f'STDERR: {result.stderr}')
        raise RuntimeError(f'Command failed: {cmd}')
    return result.stdout.strip()


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
    # Remove existing repo if present (idempotent)
    if os.path.exists(REPO_PATH):
        subprocess.run(f'rm -rf "{REPO_PATH}"', shell=True)

    os.makedirs(REPO_PATH, exist_ok=True)

    # Set up git config (required for commits)
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    def git(cmd, check=True):
        return run_cmd(f'git {cmd}', cwd=REPO_PATH, env=git_env, check=check)

    # Initialize repository (force main branch name)
    git('init -b main')
    git('config user.email "dev@example.com"')
    git('config user.name "Dev User"')

    # Create initial package.json (base state before either branch)
    base_package_json = '''{
  "name": "webapp",
  "version": "1.0.0",
  "description": "A modern web application for analytics and data visualization",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "webpack --mode production",
    "lint": "eslint src/"
  },
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21",
    "moment": "^2.29.4",
    "dotenv": "^16.0.3"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "nodemon": "^3.0.1",
    "webpack": "^5.88.2",
    "webpack-cli": "^5.1.4",
    "eslint": "^8.45.0"
  },
  "keywords": ["webapp", "analytics", "dashboard"],
  "author": "Dev Team <team@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/example/webapp.git"
  }
}
'''

    # Create other project files
    index_js = '''const express = require('express');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to WebApp', version: '1.0.0' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
'''

    readme_md = '''# WebApp

A modern web application for analytics and data visualization.

## Getting Started

```bash
npm install
npm run dev
```

## Scripts

- `npm start` - Start production server
- `npm run dev` - Start development server with hot reload
- `npm test` - Run test suite
- `npm run build` - Build for production
- `npm run lint` - Lint source files

## License

MIT
'''

    gitignore = '''node_modules/
.env
dist/
*.log
.DS_Store
coverage/
'''

    # Write initial files
    with open(f'{REPO_PATH}/package.json', 'w') as f:
        f.write(base_package_json)
    with open(f'{REPO_PATH}/index.js', 'w') as f:
        f.write(index_js)
    with open(f'{REPO_PATH}/README.md', 'w') as f:
        f.write(readme_md)
    with open(f'{REPO_PATH}/.gitignore', 'w') as f:
        f.write(gitignore)

    # Initial commit on main
    git('add .')
    git('commit -m "Initial project setup with base dependencies"')

    # Create feature/analytics branch from main
    git('checkout -b feature/analytics')

    # On feature/analytics: add chart.js dependency
    feature_package_json = '''{
  "name": "webapp",
  "version": "1.0.0",
  "description": "A modern web application for analytics and data visualization",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "webpack --mode production",
    "lint": "eslint src/"
  },
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21",
    "moment": "^2.29.4",
    "dotenv": "^16.0.3",
    "chart.js": "^4.3.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "nodemon": "^3.0.1",
    "webpack": "^5.88.2",
    "webpack-cli": "^5.1.4",
    "eslint": "^8.45.0"
  },
  "keywords": ["webapp", "analytics", "dashboard"],
  "author": "Dev Team <team@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/example/webapp.git"
  }
}
'''
    with open(f'{REPO_PATH}/package.json', 'w') as f:
        f.write(feature_package_json)

    git('add package.json')
    git('commit -m "feat(analytics): add chart.js for data visualization"')

    # Switch back to main and add axios dependency
    git('checkout main')

    main_package_json = '''{
  "name": "webapp",
  "version": "1.0.0",
  "description": "A modern web application for analytics and data visualization",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "webpack --mode production",
    "lint": "eslint src/"
  },
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21",
    "moment": "^2.29.4",
    "dotenv": "^16.0.3",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "nodemon": "^3.0.1",
    "webpack": "^5.88.2",
    "webpack-cli": "^5.1.4",
    "eslint": "^8.45.0"
  },
  "keywords": ["webapp", "analytics", "dashboard"],
  "author": "Dev Team <team@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/example/webapp.git"
  }
}
'''
    with open(f'{REPO_PATH}/package.json', 'w') as f:
        f.write(main_package_json)

    git('add package.json')
    git('commit -m "feat(http): add axios for HTTP client requests"')

    # Now attempt to merge feature/analytics into main — this will conflict
    result = subprocess.run(
        'git merge feature/analytics',
        shell=True, cwd=REPO_PATH, env=git_env,
        capture_output=True, text=True
    )
    # Merge should fail with conflict (returncode != 0)
    print(f'Merge result returncode: {result.returncode}')
    print(f'Merge stdout: {result.stdout}')
    print(f'Merge stderr: {result.stderr}')

    # Verify conflict markers exist in package.json
    with open(f'{REPO_PATH}/package.json', 'r') as f:
        content = f.read()
    if '<<<<<<< HEAD' in content:
        print('Merge conflict markers confirmed in package.json')
    else:
        print('WARNING: No conflict markers found - conflict may not have been created')

    print(f'Initial repository created at: {REPO_PATH}')
    print('Merge conflict is active in package.json')

    # GUI-ready startup: open VSCode with the webapp folder
    launch_gui(f'code "{REPO_PATH}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with webapp folder (DISPLAY=:0)')


create_initial()
