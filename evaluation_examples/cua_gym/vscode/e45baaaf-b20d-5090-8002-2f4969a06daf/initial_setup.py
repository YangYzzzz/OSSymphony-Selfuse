"""
Initial Setup: Install CMake Tools extension and configure Debug build type
Task ID: vscode_lang_080
Domain: vscode

Creates a CMake project at ~/projects/cmake-app/ with CMakeLists.txt and main.cpp.
Ensures cmake is installed. Opens VSCode with the project folder.
CMake Tools extension is NOT installed (that's the agent's job).
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_080'
PROJECT_DIR = f'{WORKDIR}/projects/cmake-app'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def install_cmake():
    """Install cmake if not present."""
    result = subprocess.run(["which", "cmake"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Installing cmake...")
        subprocess.run("echo 'password' | sudo -S apt-get update -y",
                       shell=True, check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("echo 'password' | sudo -S apt-get install -y cmake build-essential",
                       shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("cmake installed successfully")
    else:
        print("cmake already installed")
    # Verify version
    ver = subprocess.run(["cmake", "--version"], capture_output=True, text=True)
    print(ver.stdout.strip().split('\n')[0])


def create_project():
    """Create a realistic CMake project."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # CMakeLists.txt
    cmake_content = """cmake_minimum_required(VERSION 3.20)
project(cmake_app VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(cmake_app
    src/main.cpp
    src/utils.cpp
)

target_include_directories(cmake_app PRIVATE
    ${CMAKE_SOURCE_DIR}/include
)
"""
    with open(os.path.join(PROJECT_DIR, 'CMakeLists.txt'), 'w') as f:
        f.write(cmake_content)

    # Source directory
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # main.cpp
    main_cpp = """#include <iostream>
#include <string>
#include <vector>
#include "utils.h"

int main(int argc, char* argv[]) {
    std::cout << "CMake App v1.0.0" << std::endl;

    std::vector<std::string> items = {"Alpha", "Beta", "Gamma", "Delta"};

    std::cout << "Processing " << items.size() << " items:" << std::endl;
    for (const auto& item : items) {
        std::cout << "  - " << format_item(item) << std::endl;
    }

    double result = compute_average({85.5, 92.0, 78.3, 96.1, 88.7});
    std::cout << "Average score: " << result << std::endl;

    return 0;
}
"""
    with open(os.path.join(src_dir, 'main.cpp'), 'w') as f:
        f.write(main_cpp)

    # utils.cpp
    utils_cpp = """#include "utils.h"
#include <numeric>
#include <sstream>

std::string format_item(const std::string& name) {
    std::ostringstream oss;
    oss << "[ITEM] " << name;
    return oss.str();
}

double compute_average(const std::vector<double>& values) {
    if (values.empty()) return 0.0;
    double sum = std::accumulate(values.begin(), values.end(), 0.0);
    return sum / static_cast<double>(values.size());
}
"""
    with open(os.path.join(src_dir, 'utils.cpp'), 'w') as f:
        f.write(utils_cpp)

    # include directory
    inc_dir = os.path.join(PROJECT_DIR, 'include')
    os.makedirs(inc_dir, exist_ok=True)

    # utils.h
    utils_h = """#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>

std::string format_item(const std::string& name);
double compute_average(const std::vector<double>& values);

#endif // UTILS_H
"""
    with open(os.path.join(inc_dir, 'utils.h'), 'w') as f:
        f.write(utils_h)

    print(f'Project created at {PROJECT_DIR}')


def ensure_no_cmake_extension():
    """Make sure CMake Tools extension is NOT installed."""
    result = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True)
    if 'ms-vscode.cmake-tools' in result.stdout.lower():
        subprocess.run(["code", "--uninstall-extension", "ms-vscode.cmake-tools"],
                       check=False, capture_output=True)
        print("Removed pre-existing cmake-tools extension")
    else:
        print("CMake Tools extension not installed (expected)")


def setup_vscode_settings():
    """Set up basic VSCode settings WITHOUT any cmake configuration."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any cmake-related settings if they exist
    keys_to_remove = [k for k in settings if 'cmake' in k.lower()]
    for k in keys_to_remove:
        del settings[k]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print("VSCode settings cleaned of cmake config")


def main():
    install_cmake()
    create_project()
    ensure_no_cmake_extension()
    setup_vscode_settings()

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with cmake-app project, DISPLAY=:0')


main()
