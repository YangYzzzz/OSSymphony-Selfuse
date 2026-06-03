"""
Initial Setup: C++ Embedded Simulation Framework - Empty Project Skeleton
Task ID: vscode_gf4_055
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_055'
PROJECT_DIR = f'{WORKDIR}/projects/cpp-embedded-sim'

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
    os.makedirs(f'{PROJECT_DIR}/src/hal', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/scheduler', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src/app', exist_ok=True)

    # Create basic CMakeLists.txt (C++20, no Google Test yet)
    cmake_content = """\
cmake_minimum_required(VERSION 3.24)
project(EmbeddedSim LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Source directories
# Add targets here as source files are created
"""
    with open(f'{PROJECT_DIR}/CMakeLists.txt', 'w') as f:
        f.write(cmake_content)

    # Create placeholder .gitkeep files so empty dirs are visible
    for subdir in ['src/hal', 'src/scheduler', 'src/app']:
        gitkeep = f'{PROJECT_DIR}/{subdir}/.gitkeep'
        with open(gitkeep, 'w') as f:
            pass

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  CMakeLists.txt with C++20 standard')
    print(f'  Empty directories: src/hal/, src/scheduler/, src/app/')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
