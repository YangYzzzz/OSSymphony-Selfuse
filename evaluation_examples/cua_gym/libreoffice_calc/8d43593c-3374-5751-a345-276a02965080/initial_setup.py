"""
Initial Setup: VSCode Remote SSH server cache cleanup
Task ID: vscode_fix_089
Domain: vscode (OS-level file operations)

Creates a simulated ~/.vscode-server directory structure with:
- Multiple old server versions in bin/ (only one is "current")
- Duplicate/old extension versions in extensions/
- Filler data to simulate ~5GB usage
"""

import os
import shlex
import subprocess
import time
import json
import hashlib
import random

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_089'
VSCODE_SERVER = os.path.join(WORKDIR, '.vscode-server')
BIN_DIR = os.path.join(VSCODE_SERVER, 'bin')
EXT_DIR = os.path.join(VSCODE_SERVER, 'extensions')
DATA_DIR = os.path.join(VSCODE_SERVER, 'data')


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


def create_fake_file(path, size_kb=10):
    """Create a file with random-ish content of approximately size_kb KB."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = os.urandom(size_kb * 1024)
    with open(path, 'wb') as f:
        f.write(content)


def create_server_version(commit_hash, is_current=False, size_mb=50):
    """Create a fake VSCode server version directory."""
    version_dir = os.path.join(BIN_DIR, commit_hash)
    os.makedirs(version_dir, exist_ok=True)

    # Create main binary placeholder
    node_path = os.path.join(version_dir, 'node')
    create_fake_file(node_path, size_kb=size_mb * 20)  # scaled down for demo

    # Create server executable
    server_path = os.path.join(version_dir, 'bin', 'code-server')
    os.makedirs(os.path.dirname(server_path), exist_ok=True)
    with open(server_path, 'w') as f:
        f.write('#!/bin/bash\n# VSCode Server Stub\necho "VSCode Server"\n')
    os.chmod(server_path, 0o755)

    # Create package.json with version info
    pkg = {
        "name": "code-oss-dev",
        "version": "1.87.0" if not is_current else "1.92.1",
        "commit": commit_hash,
        "date": "2024-02-15" if not is_current else "2025-03-20"
    }
    with open(os.path.join(version_dir, 'package.json'), 'w') as f:
        json.dump(pkg, f, indent=2)

    # Create node_modules directory with some files
    nm_dir = os.path.join(version_dir, 'node_modules')
    os.makedirs(nm_dir, exist_ok=True)
    for mod in ['graceful-fs', 'minimist', 'semver', 'vscode-textmate']:
        mod_dir = os.path.join(nm_dir, mod)
        os.makedirs(mod_dir, exist_ok=True)
        create_fake_file(os.path.join(mod_dir, 'index.js'), size_kb=5)

    # Create out/ directory with bundled files
    out_dir = os.path.join(version_dir, 'out')
    os.makedirs(out_dir, exist_ok=True)
    for subdir in ['vs/base', 'vs/editor', 'vs/workbench', 'vs/platform']:
        os.makedirs(os.path.join(out_dir, subdir), exist_ok=True)
        create_fake_file(os.path.join(out_dir, subdir, 'main.js'), size_kb=100)

    return version_dir


def create_extension(publisher, name, version, size_kb=200):
    """Create a fake extension directory."""
    ext_id = f'{publisher}.{name}-{version}'
    ext_dir = os.path.join(EXT_DIR, ext_id)
    os.makedirs(ext_dir, exist_ok=True)

    # package.json
    pkg = {
        "name": name,
        "publisher": publisher,
        "version": version,
        "displayName": name.replace('-', ' ').title(),
        "description": f"A VSCode extension for {name}",
        "engines": {"vscode": "^1.85.0"}
    }
    with open(os.path.join(ext_dir, 'package.json'), 'w') as f:
        json.dump(pkg, f, indent=2)

    # Extension files
    out_dir = os.path.join(ext_dir, 'out')
    os.makedirs(out_dir, exist_ok=True)
    create_fake_file(os.path.join(out_dir, 'extension.js'), size_kb=size_kb)

    # README
    with open(os.path.join(ext_dir, 'README.md'), 'w') as f:
        f.write(f'# {pkg["displayName"]}\n\n{pkg["description"]}\n\nVersion {version}\n')

    return ext_dir


def create_initial():
    # Clean slate
    if os.path.exists(VSCODE_SERVER):
        import shutil
        shutil.rmtree(VSCODE_SERVER)

    os.makedirs(BIN_DIR, exist_ok=True)
    os.makedirs(EXT_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- Server Versions in bin/ ---
    # Current version commit hash (the one to KEEP)
    current_commit = 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0'

    # Old versions (should be removed in golden)
    old_commits = [
        'f0e1d2c3b4a5f6e7d8c9b0a1f2e3d4c5b6a7f8e9',  # v1.85.0
        '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b',  # v1.86.2
        'b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0',  # v1.87.0
        '2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d',  # v1.89.1
    ]

    # Create all server versions
    for old_hash in old_commits:
        create_server_version(old_hash, is_current=False, size_mb=40)
        print(f'  Created old server version: {old_hash[:12]}...')

    create_server_version(current_commit, is_current=True, size_mb=40)
    print(f'  Created current server version: {current_commit[:12]}...')

    # Mark the current version
    # VSCode uses a .current file and also a symlink-like reference
    with open(os.path.join(BIN_DIR, '.current'), 'w') as f:
        f.write(current_commit)

    # --- Extensions with duplicates ---
    # Python extension - multiple versions (keep latest only)
    create_extension('ms-python', 'python', '2024.2.1', size_kb=300)
    create_extension('ms-python', 'python', '2024.8.0', size_kb=300)
    create_extension('ms-python', 'python', '2025.1.0', size_kb=300)  # latest

    # Pylance - multiple versions
    create_extension('ms-python', 'vscode-pylance', '2024.3.100', size_kb=500)
    create_extension('ms-python', 'vscode-pylance', '2025.1.50', size_kb=500)  # latest

    # GitLens - multiple versions
    create_extension('eamodio', 'gitlens', '14.5.0', size_kb=400)
    create_extension('eamodio', 'gitlens', '15.0.4', size_kb=400)
    create_extension('eamodio', 'gitlens', '15.2.1', size_kb=400)  # latest

    # Prettier - multiple versions
    create_extension('esbenp', 'prettier-vscode', '10.1.0', size_kb=150)
    create_extension('esbenp', 'prettier-vscode', '11.0.0', size_kb=150)  # latest

    # Remote SSH - single version (keep as-is)
    create_extension('ms-vscode-remote', 'remote-ssh', '0.110.1', size_kb=250)

    # Docker - multiple versions
    create_extension('ms-azuretools', 'vscode-docker', '1.28.0', size_kb=350)
    create_extension('ms-azuretools', 'vscode-docker', '1.29.1', size_kb=350)  # latest

    # ESLint - single version (keep as-is)
    create_extension('dbaeumer', 'vscode-eslint', '3.0.5', size_kb=200)

    print(f'\nExtensions created in {EXT_DIR}')

    # --- Data directory (user data, logs) ---
    # Create some logs
    log_dir = os.path.join(DATA_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    for i in range(5):
        create_fake_file(os.path.join(log_dir, f'server-log-{i}.txt'), size_kb=50)

    # Create machine settings
    machine_dir = os.path.join(DATA_DIR, 'Machine')
    os.makedirs(machine_dir, exist_ok=True)
    with open(os.path.join(machine_dir, 'settings.json'), 'w') as f:
        json.dump({"remote.SSH.remotePlatform": {"dev-server": "linux"}}, f, indent=2)

    # --- Create a disk usage report file on the desktop ---
    report_path = os.path.join(WORKDIR, f'{TASK_ID}_disk_report.txt')
    with open(report_path, 'w') as f:
        f.write("=== Disk Space Report - Remote Development Server ===\n")
        f.write("Date: 2025-03-25\n")
        f.write("Hostname: dev-server-prod-03\n\n")
        f.write("Filesystem      Size  Used Avail Use%  Mounted on\n")
        f.write("/dev/sda1        50G   47G  2.1G  96%  /\n")
        f.write("/dev/sda2       200G  180G   15G  93%  /data\n\n")
        f.write("--- Top Space Consumers in /home/user ---\n")
        f.write("5.2G    /home/user/.vscode-server\n")
        f.write("2.1G    /home/user/.vscode-server/bin\n")
        f.write("2.8G    /home/user/.vscode-server/extensions\n")
        f.write("0.3G    /home/user/.vscode-server/data\n\n")
        f.write("WARNING: Disk usage at 96%. Immediate cleanup recommended.\n")
        f.write("SUGGESTION: Remove old server versions from ~/.vscode-server/bin/\n")
        f.write("            and duplicate extension versions from ~/.vscode-server/extensions/\n")

    print(f'Disk report created: {report_path}')

    # Show total size
    result = subprocess.run(['du', '-sh', VSCODE_SERVER], capture_output=True, text=True)
    print(f'Total .vscode-server size: {result.stdout.strip()}')

    # List all directories
    print('\n--- Server versions (bin/) ---')
    for d in sorted(os.listdir(BIN_DIR)):
        if d != '.current':
            is_cur = '(CURRENT)' if d == current_commit else '(old)'
            print(f'  {d[:12]}... {is_cur}')

    print('\n--- Extensions ---')
    for d in sorted(os.listdir(EXT_DIR)):
        print(f'  {d}')

    # GUI startup: open a terminal to show the disk situation
    launch_gui('code "/home/user"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
