"""
Initial Setup: Configure C/C++ extension to use clang-format with LLVM style
Task ID: vscode_lang_083
Domain: vscode

Creates a C++ project workspace with a sample file. No .clang-format file,
no formatting settings configured. VSCode opened with the workspace.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
WORKSPACE = os.path.join(HOME, "workspace")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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
    # Create workspace directory
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create a realistic C++ source file
    cpp_content = """\
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

struct Employee {
    std::string name;
    std::string department;
    double salary;
    int years_of_service;
};

class PayrollSystem {
public:
    void addEmployee(const std::string& name, const std::string& dept,
                     double salary, int years) {
        employees.push_back({name, dept, salary, years});
    }

    double calculateTotalPayroll() const {
        double total = 0.0;
        for (const auto& emp : employees) {
            total += emp.salary;
        }
        return total;
    }

    void printReport() const {
        std::cout << "=== Payroll Report ===" << std::endl;
        for (const auto& emp : employees) {
            std::cout << emp.name << " | " << emp.department
                      << " | $" << emp.salary
                      << " | " << emp.years_of_service << " years"
                      << std::endl;
        }
        std::cout << "Total: $" << calculateTotalPayroll() << std::endl;
    }

    std::vector<Employee> getByDepartment(const std::string& dept) const {
        std::vector<Employee> result;
        std::copy_if(employees.begin(), employees.end(),
                     std::back_inserter(result),
                     [&dept](const Employee& e) {
                         return e.department == dept;
                     });
        return result;
    }

private:
    std::vector<Employee> employees;
};

int main() {
    PayrollSystem payroll;
    payroll.addEmployee("Sarah Chen", "Engineering", 95000.0, 5);
    payroll.addEmployee("Marcus Johnson", "Marketing", 72000.0, 3);
    payroll.addEmployee("Aisha Patel", "Engineering", 88000.0, 4);
    payroll.addEmployee("David Kim", "Finance", 81000.0, 6);
    payroll.addEmployee("Elena Rodriguez", "Marketing", 68000.0, 2);

    payroll.printReport();

    auto engineers = payroll.getByDepartment("Engineering");
    std::cout << "\\nEngineering team: " << engineers.size() << " members" << std::endl;

    return 0;
}
"""
    cpp_path = os.path.join(WORKSPACE, "main.cpp")
    with open(cpp_path, "w") as f:
        f.write(cpp_content)

    # Create a simple header file
    header_content = """\
#ifndef PAYROLL_H
#define PAYROLL_H

#include <string>
#include <vector>

namespace payroll {

struct Employee {
    std::string name;
    std::string department;
    double salary;
    int years_of_service;
};

double calculateBonus(const Employee& emp);
std::vector<Employee> filterBySalary(const std::vector<Employee>& employees, double threshold);

}  // namespace payroll

#endif  // PAYROLL_H
"""
    header_path = os.path.join(WORKSPACE, "payroll.h")
    with open(header_path, "w") as f:
        f.write(header_content)

    # Create a CMakeLists.txt for the project
    cmake_content = """\
cmake_minimum_required(VERSION 3.14)
project(PayrollSystem LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(payroll main.cpp)
"""
    cmake_path = os.path.join(WORKSPACE, "CMakeLists.txt")
    with open(cmake_path, "w") as f:
        f.write(cmake_content)

    # Ensure NO .clang-format file exists
    clang_format_path = os.path.join(WORKSPACE, ".clang-format")
    if os.path.exists(clang_format_path):
        os.remove(clang_format_path)

    # Load existing VSCode settings and ensure no C_Cpp formatting settings
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                import re
                content = f.read()
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                settings = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any existing C_Cpp formatting settings
    for key in ["C_Cpp.formatting", "C_Cpp.clang_format_style",
                "C_Cpp.clang_format_path", "C_Cpp.clang_format_fallbackStyle"]:
        settings.pop(key, None)

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"Workspace created at: {WORKSPACE}")
    print(f"C++ file: {cpp_path}")
    print(f"Settings cleaned: {SETTINGS_PATH}")

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_initial()
