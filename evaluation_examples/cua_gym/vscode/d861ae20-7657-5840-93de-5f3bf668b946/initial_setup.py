"""
Initial Setup: Merge 'feature/search' into main with a merge conflict in search.py
Task ID: vscode_git_045
Domain: vs_code

Creates a git repository at /home/user/webapp with:
  - main branch: search() has pagination logic
  - feature/search branch: search() has fuzzy matching logic
  - Both modified the same function -> merge conflict when merging feature/search into main
  - VSCode opened with the webapp folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
REPO_DIR = f'{WORKDIR}/webapp'


def run(cmd, cwd=None, check=True, env=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        shlex.split(cmd) if isinstance(cmd, str) else cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
        env=env,
    )
    return result


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
    if os.path.exists(REPO_DIR):
        run(f'rm -rf {REPO_DIR}')

    os.makedirs(REPO_DIR, exist_ok=True)

    # Git env for consistent authorship
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    def git(cmd, cwd=REPO_DIR):
        return run(f'git {cmd}', cwd=cwd, env=git_env)

    # ---- Initialize repo ----
    git('init')
    git('config user.email "dev@example.com"')
    git('config user.name "Dev User"')
    # Ensure default branch is named 'main' regardless of git version defaults
    git('config init.defaultBranch main')

    # ---- Create initial commit on main (common base) ----
    # The base version of search.py — no pagination, no fuzzy matching
    base_search_py = '''\
"""
Search module for webapp.
"""
import re


def search(query, data):
    """
    Search through data for items matching the query.

    Args:
        query (str): The search string.
        data (list): List of strings to search through.

    Returns:
        list: Matching items.
    """
    results = []
    for item in data:
        if query.lower() in item.lower():
            results.append(item)
    return results


def highlight_matches(query, text):
    """Wrap matched portions of text with <mark> tags."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group()}</mark>", text)
'''

    # Other files in the repo
    app_py = '''\
"""
Main application entry point for webapp.
"""
from search import search


def run_app():
    catalog = [
        "Python Programming Fundamentals",
        "Advanced Web Development",
        "Data Science with Pandas",
        "Machine Learning Basics",
        "REST API Design Principles",
        "Docker and Kubernetes",
        "JavaScript ES6 Features",
        "Database Design and SQL",
        "Cloud Architecture Patterns",
        "Agile Development Practices",
    ]

    print("=== Webapp Search Demo ===")
    query = "python"
    results = search(query, catalog)
    print(f"Results for '{query}': {results}")


if __name__ == "__main__":
    run_app()
'''

    readme_md = '''\
# Webapp

A simple web application with search functionality.

## Modules

- `search.py` — Core search logic
- `app.py` — Application entry point

## Usage

```bash
python app.py
```
'''

    requirements_txt = '''\
# No external dependencies required
'''

    # Write files and make initial commit
    def write_file(name, content):
        with open(os.path.join(REPO_DIR, name), 'w') as f:
            f.write(content)

    write_file('search.py', base_search_py)
    write_file('app.py', app_py)
    write_file('README.md', readme_md)
    write_file('requirements.txt', requirements_txt)

    git('add .')
    git('commit -m "Initial commit: basic search functionality"')

    # Rename to 'main' in case git defaulted to 'master'
    git('branch -M main')

    # ---- Create feature/search branch from common base ----
    git('checkout -b feature/search')

    # feature/search: modifies search() to add fuzzy matching
    feature_search_py = '''\
"""
Search module for webapp.
"""
import re


def search(query, data, fuzzy=False):
    """
    Search through data for items matching the query.

    Args:
        query (str): The search string.
        data (list): List of strings to search through.
        fuzzy (bool): Enable fuzzy matching (allows partial character matches).

    Returns:
        list: Matching items.
    """
    results = []
    for item in data:
        if fuzzy:
            # Fuzzy matching: all characters in query appear in order in item
            pattern = '.*'.join(re.escape(c) for c in query.lower())
            if re.search(pattern, item.lower()):
                results.append(item)
        else:
            if query.lower() in item.lower():
                results.append(item)
    return results


def highlight_matches(query, text):
    """Wrap matched portions of text with <mark> tags."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group()}</mark>", text)
'''

    write_file('search.py', feature_search_py)
    git('add search.py')
    git('commit -m "feat: add fuzzy matching to search function"')

    # ---- Switch back to main and add pagination ----
    git('checkout main')

    # main branch: modifies search() to add pagination
    main_search_py = '''\
"""
Search module for webapp.
"""
import re


def search(query, data, page=1, page_size=10):
    """
    Search through data for items matching the query.

    Args:
        query (str): The search string.
        data (list): List of strings to search through.
        page (int): Page number (1-indexed) for pagination.
        page_size (int): Number of results per page.

    Returns:
        list: Matching items for the requested page.
    """
    results = []
    for item in data:
        if query.lower() in item.lower():
            results.append(item)
    # Apply pagination
    start = (page - 1) * page_size
    end = start + page_size
    return results[start:end]


def highlight_matches(query, text):
    """Wrap matched portions of text with <mark> tags."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group()}</mark>", text)
'''

    write_file('search.py', main_search_py)
    git('add search.py')
    git('commit -m "feat: add pagination to search function"')

    # Now main and feature/search have diverged on search.py
    # Attempting to merge feature/search into main will produce a conflict
    print(f'Repository created at {REPO_DIR}')
    print('Branches: main (with pagination), feature/search (with fuzzy matching)')
    print('Ready for merge conflict task')

    # Open VSCode with the webapp folder
    launch_gui(f'code "{REPO_DIR}"', delay_sec=2.5)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
