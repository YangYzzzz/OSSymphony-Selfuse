"""
Initial Setup: Create a C++ CMake project with tasks.json but no launch.json
Task ID: vscode_td_071
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_071'
PROJECT_DIR = f'{WORKDIR}/projects/cmake-app'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/include', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/build/bin', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create CMakeLists.txt
    cmake_content = """cmake_minimum_required(VERSION 3.16)
project(myapp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(myapp
    src/main.cpp
    src/config_parser.cpp
    src/logger.cpp
)

target_include_directories(myapp PRIVATE include)

# Enable debugging symbols for Debug build
set(CMAKE_BUILD_TYPE Debug)
"""
    with open(f'{PROJECT_DIR}/CMakeLists.txt', 'w') as f:
        f.write(cmake_content)

    # Create main.cpp
    main_cpp = """#include <iostream>
#include <vector>
#include <string>
#include "config_parser.h"
#include "logger.h"

int main(int argc, char* argv[]) {
    Logger logger("myapp");
    logger.info("Application starting...");

    ConfigParser config;
    if (argc > 1) {
        config.loadFromFile(argv[1]);
    } else {
        config.loadDefaults();
    }

    std::vector<std::string> modules = config.getActiveModules();
    logger.info("Loaded " + std::to_string(modules.size()) + " modules");

    for (const auto& mod : modules) {
        logger.info("Initializing module: " + mod);
    }

    logger.info("Application ready. Entering main loop...");

    int exitCode = 0;
    // Main application loop would go here

    logger.info("Shutting down with exit code " + std::to_string(exitCode));
    return exitCode;
}
"""
    with open(f'{PROJECT_DIR}/src/main.cpp', 'w') as f:
        f.write(main_cpp)

    # Create config_parser.cpp
    config_parser_cpp = """#include "config_parser.h"
#include <fstream>
#include <sstream>

void ConfigParser::loadFromFile(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open config file: " + path);
    }

    std::string line;
    while (std::getline(file, line)) {
        auto pos = line.find('=');
        if (pos != std::string::npos) {
            std::string key = line.substr(0, pos);
            std::string value = line.substr(pos + 1);
            settings_[key] = value;
        }
    }
}

void ConfigParser::loadDefaults() {
    settings_["app.name"] = "myapp";
    settings_["app.version"] = "1.0.0";
    settings_["log.level"] = "info";
    activeModules_ = {"core", "network", "storage"};
}

std::vector<std::string> ConfigParser::getActiveModules() const {
    return activeModules_;
}
"""
    with open(f'{PROJECT_DIR}/src/config_parser.cpp', 'w') as f:
        f.write(config_parser_cpp)

    # Create logger.cpp
    logger_cpp = """#include "logger.h"
#include <iostream>
#include <ctime>

Logger::Logger(const std::string& name) : name_(name) {}

void Logger::info(const std::string& message) {
    log("INFO", message);
}

void Logger::warn(const std::string& message) {
    log("WARN", message);
}

void Logger::error(const std::string& message) {
    log("ERROR", message);
}

void Logger::log(const std::string& level, const std::string& message) {
    time_t now = time(nullptr);
    char buf[20];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", localtime(&now));
    std::cout << "[" << buf << "] [" << level << "] [" << name_ << "] " << message << std::endl;
}
"""
    with open(f'{PROJECT_DIR}/src/logger.cpp', 'w') as f:
        f.write(logger_cpp)

    # Create header files
    config_parser_h = """#ifndef CONFIG_PARSER_H
#define CONFIG_PARSER_H

#include <string>
#include <map>
#include <vector>

class ConfigParser {
public:
    void loadFromFile(const std::string& path);
    void loadDefaults();
    std::vector<std::string> getActiveModules() const;

private:
    std::map<std::string, std::string> settings_;
    std::vector<std::string> activeModules_;
};

#endif // CONFIG_PARSER_H
"""
    with open(f'{PROJECT_DIR}/include/config_parser.h', 'w') as f:
        f.write(config_parser_h)

    logger_h = """#ifndef LOGGER_H
#define LOGGER_H

#include <string>

class Logger {
public:
    explicit Logger(const std::string& name);
    void info(const std::string& message);
    void warn(const std::string& message);
    void error(const std::string& message);

private:
    std::string name_;
    void log(const std::string& level, const std::string& message);
};

#endif // LOGGER_H
"""
    with open(f'{PROJECT_DIR}/include/logger.h', 'w') as f:
        f.write(logger_h)

    # Create .vscode/tasks.json with "CMake Build" task
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "CMake Build",
                "type": "shell",
                "command": "cmake",
                "args": [
                    "--build",
                    "${workspaceFolder}/build",
                    "--config",
                    "Debug"
                ],
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "problemMatcher": ["$gcc"],
                "detail": "Build the CMake project in Debug mode"
            },
            {
                "label": "CMake Configure",
                "type": "shell",
                "command": "cmake",
                "args": [
                    "-S",
                    "${workspaceFolder}",
                    "-B",
                    "${workspaceFolder}/build",
                    "-DCMAKE_BUILD_TYPE=Debug"
                ],
                "problemMatcher": [],
                "detail": "Configure CMake project"
            }
        ]
    }
    with open(f'{VSCODE_DIR}/tasks.json', 'w') as f:
        json.dump(tasks_json, f, indent=4)

    # Ensure NO launch.json exists
    launch_path = f'{VSCODE_DIR}/launch.json'
    if os.path.exists(launch_path):
        os.remove(launch_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  CMakeLists.txt: exists')
    print(f'  .vscode/tasks.json: exists with "CMake Build" task')
    print(f'  .vscode/launch.json: does NOT exist')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
