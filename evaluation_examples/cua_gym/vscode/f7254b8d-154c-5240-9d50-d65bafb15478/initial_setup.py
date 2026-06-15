"""
Initial Setup: Configure VSCode tasks.json with pickString input for CMake build config
Task ID: vscode_td_040
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_040'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'cpp-engine')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')


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
    os.makedirs(BUILD_DIR, exist_ok=True)

    # Create a realistic CMakeLists.txt
    cmake_content = """cmake_minimum_required(VERSION 3.16)
project(CppEngine VERSION 1.2.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Source files
set(ENGINE_SOURCES
    src/main.cpp
    src/engine/core.cpp
    src/engine/renderer.cpp
    src/engine/physics.cpp
    src/engine/input_handler.cpp
    src/utils/logger.cpp
    src/utils/config_parser.cpp
)

# Header files
set(ENGINE_HEADERS
    include/engine/core.h
    include/engine/renderer.h
    include/engine/physics.h
    include/engine/input_handler.h
    include/utils/logger.h
    include/utils/config_parser.h
)

add_executable(${PROJECT_NAME} ${ENGINE_SOURCES})

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_SOURCE_DIR}/include
)

# Optional: find packages
find_package(Threads REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE Threads::Threads)

# Install target
install(TARGETS ${PROJECT_NAME} DESTINATION bin)
"""
    with open(os.path.join(PROJECT_DIR, 'CMakeLists.txt'), 'w') as f:
        f.write(cmake_content)

    # Create source directories and sample files
    src_dirs = [
        os.path.join(PROJECT_DIR, 'src'),
        os.path.join(PROJECT_DIR, 'src', 'engine'),
        os.path.join(PROJECT_DIR, 'src', 'utils'),
        os.path.join(PROJECT_DIR, 'include'),
        os.path.join(PROJECT_DIR, 'include', 'engine'),
        os.path.join(PROJECT_DIR, 'include', 'utils'),
    ]
    for d in src_dirs:
        os.makedirs(d, exist_ok=True)

    # main.cpp
    with open(os.path.join(PROJECT_DIR, 'src', 'main.cpp'), 'w') as f:
        f.write("""#include <iostream>
#include "engine/core.h"
#include "utils/logger.h"

int main(int argc, char* argv[]) {
    Logger::init("engine.log");
    Logger::info("CppEngine v1.2.0 starting...");

    Engine::Core engine;
    if (!engine.initialize(800, 600, "CppEngine Demo")) {
        Logger::error("Failed to initialize engine");
        return 1;
    }

    engine.run();
    engine.shutdown();

    Logger::info("CppEngine shut down cleanly");
    return 0;
}
""")

    # core.h
    with open(os.path.join(PROJECT_DIR, 'include', 'engine', 'core.h'), 'w') as f:
        f.write("""#pragma once

namespace Engine {

class Core {
public:
    bool initialize(int width, int height, const char* title);
    void run();
    void shutdown();

private:
    bool m_running = false;
    int m_width = 0;
    int m_height = 0;
};

} // namespace Engine
""")

    # core.cpp
    with open(os.path.join(PROJECT_DIR, 'src', 'engine', 'core.cpp'), 'w') as f:
        f.write("""#include "engine/core.h"
#include "utils/logger.h"

namespace Engine {

bool Core::initialize(int width, int height, const char* title) {
    m_width = width;
    m_height = height;
    m_running = true;
    Logger::info("Engine initialized");
    return true;
}

void Core::run() {
    while (m_running) {
        // Main loop placeholder
        m_running = false;
    }
}

void Core::shutdown() {
    m_running = false;
    Logger::info("Engine shutdown");
}

} // namespace Engine
""")

    # Create placeholder files for other sources
    placeholders = {
        'src/engine/renderer.cpp': '#include "engine/renderer.h"\n// Renderer implementation\n',
        'src/engine/physics.cpp': '#include "engine/physics.h"\n// Physics implementation\n',
        'src/engine/input_handler.cpp': '#include "engine/input_handler.h"\n// Input handler implementation\n',
        'src/utils/logger.cpp': '#include "utils/logger.h"\n#include <iostream>\n#include <fstream>\n\nstd::ofstream Logger::m_logFile;\n\nvoid Logger::init(const std::string& path) { m_logFile.open(path); }\nvoid Logger::info(const std::string& msg) { std::cout << "[INFO] " << msg << std::endl; }\nvoid Logger::error(const std::string& msg) { std::cerr << "[ERROR] " << msg << std::endl; }\n',
        'src/utils/config_parser.cpp': '#include "utils/config_parser.h"\n// Config parser implementation\n',
        'include/engine/renderer.h': '#pragma once\nnamespace Engine { class Renderer {}; }\n',
        'include/engine/physics.h': '#pragma once\nnamespace Engine { class Physics {}; }\n',
        'include/engine/input_handler.h': '#pragma once\nnamespace Engine { class InputHandler {}; }\n',
        'include/utils/logger.h': '#pragma once\n#include <string>\n#include <fstream>\n\nclass Logger {\npublic:\n    static void init(const std::string& path);\n    static void info(const std::string& msg);\n    static void error(const std::string& msg);\nprivate:\n    static std::ofstream m_logFile;\n};\n',
        'include/utils/config_parser.h': '#pragma once\n#include <string>\n#include <map>\n\nclass ConfigParser {\npublic:\n    bool load(const std::string& path);\n    std::string get(const std::string& key) const;\nprivate:\n    std::map<std::string, std::string> m_data;\n};\n',
    }
    for rel_path, content in placeholders.items():
        with open(os.path.join(PROJECT_DIR, rel_path), 'w') as f:
            f.write(content)

    # Create a .gitignore
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write("build/\n*.o\n*.log\ncompile_commands.json\n")

    # Create a README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("# CppEngine\n\nA lightweight C++ game engine demo project.\n\n## Build\n\n```bash\nmkdir build && cd build\ncmake ..\ncmake --build . --config Release\n```\n")

    # Ensure NO .vscode/tasks.json exists (the task requires creating it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    tasks_path = os.path.join(vscode_dir, 'tasks.json')
    if os.path.exists(tasks_path):
        os.remove(tasks_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'CMakeLists.txt: {os.path.join(PROJECT_DIR, "CMakeLists.txt")}')
    print(f'build/ directory: {BUILD_DIR}')
    print(f'.vscode/tasks.json exists: {os.path.exists(tasks_path)}')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
