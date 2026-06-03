"""
Initial Setup: Create VSCode workspace with C++ project structure
Task ID: vscode_td_032
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_032'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'myapp')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
BIN_DIR = os.path.join(PROJECT_DIR, 'bin')


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
    os.makedirs(BIN_DIR, exist_ok=True)

    # Create src/main.cpp with realistic C++ content
    main_cpp_content = """#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

struct Employee {
    std::string name;
    std::string department;
    double salary;
};

double calculate_average_salary(const std::vector<Employee>& employees) {
    if (employees.empty()) return 0.0;
    double total = 0.0;
    for (const auto& emp : employees) {
        total += emp.salary;
    }
    return total / employees.size();
}

void print_department_report(const std::vector<Employee>& employees) {
    std::cout << "=== Department Salary Report ===" << std::endl;
    std::cout << std::endl;
    for (const auto& emp : employees) {
        std::cout << emp.name << " (" << emp.department << "): $"
                  << emp.salary << std::endl;
    }
    std::cout << std::endl;
    std::cout << "Average Salary: $" << calculate_average_salary(employees)
              << std::endl;
}

int main() {
    std::vector<Employee> team = {
        {"Sarah Chen", "Engineering", 95000.0},
        {"Marcus Johnson", "Marketing", 78000.0},
        {"Elena Rodriguez", "Engineering", 102000.0},
        {"David Kim", "Design", 85000.0},
        {"Priya Patel", "Marketing", 81000.0},
        {"James Wright", "Engineering", 98000.0}
    };

    print_department_report(team);

    std::cout << "\\nTotal employees: " << team.size() << std::endl;
    return 0;
}
"""
    with open(os.path.join(SRC_DIR, 'main.cpp'), 'w') as f:
        f.write(main_cpp_content)

    # Ensure NO .vscode folder exists (task requires creating it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Project structure created at {PROJECT_DIR}')
    print(f'  src/main.cpp: created')
    print(f'  bin/: created (empty)')
    print(f'  .vscode/: does not exist (as required)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
