"""
Initial Setup: Create C++ project for VSCode tasks.json task
Task ID: vscode_gf5_016
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_016'
PROJECT_DIR = f'{WORKDIR}/projects/cpp-project'
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

    # Create a realistic C++ source file
    main_cpp = '''\
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>

struct Employee {
    std::string name;
    std::string department;
    double salary;
};

double calculate_average_salary(const std::vector<Employee>& employees) {
    if (employees.empty()) return 0.0;
    double total = std::accumulate(employees.begin(), employees.end(), 0.0,
        [](double sum, const Employee& e) { return sum + e.salary; });
    return total / employees.size();
}

void print_department_report(const std::vector<Employee>& employees) {
    std::cout << "=== Department Salary Report ===" << std::endl;
    std::cout << std::string(50, '-') << std::endl;

    for (const auto& emp : employees) {
        std::cout << emp.name << " | "
                  << emp.department << " | $"
                  << emp.salary << std::endl;
    }

    std::cout << std::string(50, '-') << std::endl;
    std::cout << "Average salary: $"
              << calculate_average_salary(employees) << std::endl;
    std::cout << "Total employees: " << employees.size() << std::endl;
}

int main() {
    std::vector<Employee> team = {
        {"Sarah Chen", "Engineering", 95000.0},
        {"Marcus Johnson", "Marketing", 78000.0},
        {"Priya Patel", "Engineering", 102000.0},
        {"David Kim", "Design", 84000.0},
        {"Elena Rodriguez", "Marketing", 81000.0},
        {"James O'Brien", "Engineering", 98500.0},
        {"Aisha Mohammed", "Design", 87000.0},
        {"Robert Taylor", "Marketing", 76500.0}
    };

    print_department_report(team);

    // Filter engineering team
    std::vector<Employee> engineers;
    std::copy_if(team.begin(), team.end(), std::back_inserter(engineers),
        [](const Employee& e) { return e.department == "Engineering"; });

    std::cout << "\\nEngineering team average: $"
              << calculate_average_salary(engineers) << std::endl;

    return 0;
}
'''

    with open(f'{SRC_DIR}/main.cpp', 'w') as f:
        f.write(main_cpp)

    print(f'Created project structure at {PROJECT_DIR}')
    print(f'  src/main.cpp: C++ program with employee salary report')

    # Ensure NO .vscode directory exists (the task is to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)
        print(f'  Removed existing .vscode directory')

    # Ensure NO bin/ directory exists
    bin_dir = f'{PROJECT_DIR}/bin'
    if os.path.exists(bin_dir):
        import shutil
        shutil.rmtree(bin_dir)
        print(f'  Removed existing bin directory')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
