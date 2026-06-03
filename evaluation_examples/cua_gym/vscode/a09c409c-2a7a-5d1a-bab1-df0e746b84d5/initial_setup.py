"""
Initial Setup: Configure workspace-level spell checking for ~/projects/technical-blog
Task ID: vscode_gf5_046
Domain: vscode

Creates the technical-blog project with posts/intro.md containing 6 apparent
spelling issues (3 technical terms + 3 genuine typos). No cspell.json,
no Code Spell Checker extension installed.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_046'
PROJECT_DIR = f'{WORKDIR}/projects/technical-blog'
POSTS_DIR = f'{PROJECT_DIR}/posts'

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
    # Create project directory structure
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/assets', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/drafts', exist_ok=True)

    # Create posts/intro.md with 6 apparent spelling issues:
    # Technical terms (not real errors): API, OAuth, middleware
    # Genuine typos: recieve, occured, successfull
    intro_content = """# Introduction to Building Modern Web Services

Welcome to our technical blog! In this series, we will explore the fundamentals
of building robust and scalable web services from the ground up.

## Understanding the Basics

When you build a modern web application, you need to understand how your API
handles incoming requests. Every endpoint in your system should be designed
with security and performance in mind.

A well-structured middleware layer sits between the client request and your
business logic, handling cross-cutting concerns like authentication, logging,
and rate limiting. This is where many developers struggle to find the right
balance between flexibility and simplicity.

## Authentication with OAuth

One of the most common authentication patterns is OAuth. When a user tries
to access a protected resource, the OAuth flow ensures they have the proper
credentials without exposing sensitive information.

We recieve thousands of authentication requests every day, and handling them
efficiently is critical to our platform's reliability. Last quarter, an outage
occured when our token refresh service went down during peak hours.

## Setting Up Your Webhook Pipeline

To keep your services in sync, a webhook pipeline is essential. Whenever a
relevant event happens in one service, it notifies all subscribers via HTTP
callbacks.

Our team has been successfull in reducing webhook delivery latency by 40%
through careful optimization of our message queue infrastructure.

## What's Next

In the upcoming posts, we will dive deeper into each of these topics with
practical code examples and real-world deployment strategies. Stay tuned!
"""
    with open(f'{POSTS_DIR}/intro.md', 'w') as f:
        f.write(intro_content)

    # Create a simple README for the project
    readme_content = """# Technical Blog

A collection of articles about modern web development practices.

## Structure

- `posts/` - Published articles
- `drafts/` - Work in progress
- `assets/` - Images and media
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Create a draft post for extra realism
    draft_content = """# Draft: Database Optimization Tips

TODO: Write about indexing strategies and query optimization.
"""
    with open(f'{PROJECT_DIR}/drafts/database-tips.md', 'w') as f:
        f.write(draft_content)

    # Ensure NO cspell.json exists
    cspell_path = f'{PROJECT_DIR}/cspell.json'
    if os.path.exists(cspell_path):
        os.remove(cspell_path)

    # Ensure Code Spell Checker is NOT installed
    result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True)
    if 'streetsidesoftware.code-spell-checker' in result.stdout.lower():
        subprocess.run(['code', '--uninstall-extension', 'streetsidesoftware.code-spell-checker'],
                       capture_output=True, text=True)

    print(f'Project created: {PROJECT_DIR}')
    print(f'Initial intro.md with 3 technical terms + 3 typos')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
