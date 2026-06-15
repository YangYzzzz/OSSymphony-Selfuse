"""
Initial Setup: Create a C++ project with tasks.json but no launch.json
Task ID: vscode_td_058
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_058'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'cpp-project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'include'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'bin'), exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create main.cpp
    main_cpp = os.path.join(PROJECT_DIR, 'src', 'main.cpp')
    with open(main_cpp, 'w') as f:
        f.write('''#include <iostream>
#include <vector>
#include <string>
#include "utils.h"

int main() {
    std::vector<std::string> names = {"Alice", "Bob", "Charlie", "Diana"};

    std::cout << "Employee Directory" << std::endl;
    std::cout << "==================" << std::endl;

    for (size_t i = 0; i < names.size(); ++i) {
        std::cout << (i + 1) << ". " << names[i] << std::endl;
    }

    double total_budget = calculate_budget(names.size());
    std::cout << "\\nTotal training budget: $" << total_budget << std::endl;

    return 0;
}
''')

    # Create utils.h
    utils_h = os.path.join(PROJECT_DIR, 'include', 'utils.h')
    with open(utils_h, 'w') as f:
        f.write('''#ifndef UTILS_H
#define UTILS_H

#include <cstddef>

double calculate_budget(size_t employee_count) {
    const double per_person = 1500.0;
    return employee_count * per_person;
}

#endif // UTILS_H
''')

    # Create Makefile
    makefile = os.path.join(PROJECT_DIR, 'Makefile')
    with open(makefile, 'w') as f:
        f.write('''CXX = g++
CXXFLAGS = -g -Wall -std=c++17 -Iinclude
SRC = src/main.cpp
OUT = bin/app

all: $(OUT)

$(OUT): $(SRC)
\tmkdir -p bin
\t$(CXX) $(CXXFLAGS) -o $(OUT) $(SRC)

clean:
\trm -f $(OUT)

.PHONY: all clean
''')

    # Create tasks.json with a "Build" task
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Build",
                "type": "shell",
                "command": "make",
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "problemMatcher": ["$gcc"],
                "detail": "Build the C++ application using make"
            }
        ]
    }
    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    with open(tasks_path, 'w') as f:
        json.dump(tasks_json, f, indent=4)

    # Ensure NO launch.json exists
    launch_path = os.path.join(VSCODE_DIR, 'launch.json')
    if os.path.exists(launch_path):
        os.remove(launch_path)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'tasks.json created at: {tasks_path}')
    print(f'launch.json does NOT exist: {not os.path.exists(launch_path)}')

    # Install C/C++ extension if not already installed
    try:
        result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True, timeout=30)
        if 'ms-vscode.cpptools' not in result.stdout:
            subprocess.run(['code', '--install-extension', 'ms-vscode.cpptools', '--force'],
                           capture_output=True, text=True, timeout=120)
            print('C/C++ extension installed')
        else:
            print('C/C++ extension already installed')
    except Exception as e:
        print(f'Extension check/install note: {e}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
