"""
Initial Setup: Create cpp-memory-allocator project scaffold with minimal CMakeLists.txt
Task ID: vscode_gf4_037
Domain: vscode (C++ project)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_037'
PROJECT_DIR = f'{WORKDIR}/projects/cpp-memory-allocator'


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
    # 1. Install cmake if not present
    subprocess.run(
        'echo "password" | sudo -S apt-get update -qq && '
        'echo "password" | sudo -S apt-get install -y -qq cmake',
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    # 2. Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # 3. Create minimal CMakeLists.txt (only project name and C++20 standard)
    cmakelists_content = """\
cmake_minimum_required(VERSION 3.14)
project(cpp-memory-allocator)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
"""
    with open(f'{PROJECT_DIR}/CMakeLists.txt', 'w') as f:
        f.write(cmakelists_content)

    print(f'Project scaffold created at: {PROJECT_DIR}')
    print(f'  CMakeLists.txt: minimal (project name + C++20)')
    print(f'  src/: empty directory')
    print(f'  tests/: empty directory')

    # 4. Install C/C++ and CMake Tools extensions
    subprocess.run(['code', '--install-extension', 'ms-vscode.cpptools'],
                   capture_output=True, text=True)
    subprocess.run(['code', '--install-extension', 'ms-vscode.cmake-tools'],
                   capture_output=True, text=True)
    print('VSCode extensions installed: C/C++, CMake Tools')

    # 5. Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
