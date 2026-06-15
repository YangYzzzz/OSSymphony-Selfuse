"""
Initial Setup: Create a C++ project workspace with src/main.cpp (uses threading) but no CMakeLists.txt.
Task ID: vscode_lang_081
Domain: vscode (OS/file-based)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_081'
PROJECT_DIR = f'{WORKDIR}/projects/cppapp'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(SRC_DIR, exist_ok=True)

    # Create src/main.cpp — a realistic C++ file that uses pthreads
    main_cpp_content = """\
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>

std::mutex cout_mutex;

void worker(int id, int iterations) {
    for (int i = 0; i < iterations; ++i) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        std::lock_guard<std::mutex> lock(cout_mutex);
        std::cout << "Worker " << id << " completed iteration " << i + 1
                  << "/" << iterations << std::endl;
    }
}

int main() {
    const int num_threads = 4;
    const int work_per_thread = 3;
    std::vector<std::thread> threads;

    std::cout << "Starting " << num_threads << " worker threads..." << std::endl;

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(worker, i + 1, work_per_thread);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "All workers finished." << std::endl;
    return 0;
}
"""
    with open(f'{SRC_DIR}/main.cpp', 'w') as f:
        f.write(main_cpp_content)

    # Ensure NO CMakeLists.txt exists (negative constraint)
    cmake_path = f'{PROJECT_DIR}/CMakeLists.txt'
    if os.path.exists(cmake_path):
        os.remove(cmake_path)

    print(f'Project structure created at {PROJECT_DIR}')
    print(f'  src/main.cpp: C++ file with threading')
    print(f'  CMakeLists.txt: NOT present (task requires agent to create it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
