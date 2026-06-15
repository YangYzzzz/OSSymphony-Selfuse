"""
Initial Setup: Configure a Valgrind debug task in tasks.json
Task ID: vscode_lang_095
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_095'
WORKSPACE = f'{WORKDIR}/workspace'


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
    os.makedirs(f'{WORKSPACE}/src', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/build', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/.vscode', exist_ok=True)

    # --- C source file with intentional memory leaks ---
    c_source = r"""#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    int age;
    double salary;
} Employee;

Employee *create_employee(const char *name, int age, double salary) {
    Employee *emp = (Employee *)malloc(sizeof(Employee));
    emp->name = (char *)malloc(strlen(name) + 1);
    strcpy(emp->name, name);
    emp->age = age;
    emp->salary = salary;
    return emp;
}

void process_data(int count) {
    // Intentional leak: allocated buffer never freed
    char *buffer = (char *)malloc(256);
    snprintf(buffer, 256, "Processing %d records...", count);
    printf("%s\n", buffer);
    // Missing: free(buffer);
}

double *compute_averages(double *values, int n) {
    // Intentional leak: returned pointer often not freed by caller
    double *result = (double *)malloc(n * sizeof(double));
    double running_sum = 0.0;
    for (int i = 0; i < n; i++) {
        running_sum += values[i];
        result[i] = running_sum / (i + 1);
    }
    return result;
}

int main() {
    printf("Employee Management System v2.1\n");
    printf("================================\n\n");

    // Create employees (leak: emp2 and emp3 name fields not freed)
    Employee *emp1 = create_employee("Sarah Chen", 34, 95000.0);
    Employee *emp2 = create_employee("Marcus Johnson", 28, 72000.0);
    Employee *emp3 = create_employee("Priya Patel", 41, 108000.0);

    printf("Employee: %s, Age: %d, Salary: $%.2f\n", emp1->name, emp1->age, emp1->salary);
    printf("Employee: %s, Age: %d, Salary: $%.2f\n", emp2->name, emp2->age, emp2->salary);
    printf("Employee: %s, Age: %d, Salary: $%.2f\n", emp3->name, emp3->age, emp3->salary);

    // Process some data (leaks buffer internally)
    process_data(150);

    // Compute averages (leak: result never freed)
    double salaries[] = {95000.0, 72000.0, 108000.0};
    double *avgs = compute_averages(salaries, 3);
    printf("\nRunning salary averages:\n");
    for (int i = 0; i < 3; i++) {
        printf("  After %d employees: $%.2f\n", i + 1, avgs[i]);
    }

    // Only free emp1 properly
    free(emp1->name);
    free(emp1);

    // emp2 and emp3 leaked (both struct and name)
    // avgs leaked
    // buffer in process_data leaked

    printf("\nDone. (Memory leaks present for Valgrind testing)\n");
    return 0;
}
"""
    with open(f'{WORKSPACE}/src/main.c', 'w') as f:
        f.write(c_source)

    # --- Makefile ---
    makefile = """CC = gcc
CFLAGS = -Wall -Wextra -g -O0
SRC_DIR = src
BUILD_DIR = build

all: $(BUILD_DIR)/main

$(BUILD_DIR)/main: $(SRC_DIR)/main.c
\t@mkdir -p $(BUILD_DIR)
\t$(CC) $(CFLAGS) -o $@ $<

clean:
\trm -rf $(BUILD_DIR)/*

.PHONY: all clean
"""
    with open(f'{WORKSPACE}/Makefile', 'w') as f:
        f.write(makefile)

    # --- Compile the program so build/main exists ---
    result = subprocess.run(
        ['gcc', '-Wall', '-Wextra', '-g', '-O0', '-o',
         f'{WORKSPACE}/build/main', f'{WORKSPACE}/src/main.c'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Compilation warning/error: {result.stderr}")
    else:
        print(f"Compiled build/main successfully")

    # --- .vscode/tasks.json with only the Build task ---
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Build C",
                "type": "shell",
                "command": "make all",
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "options": {
                    "cwd": "${workspaceFolder}"
                },
                "problemMatcher": ["$gcc"],
                "detail": "Compile the C project using make"
            }
        ]
    }
    with open(f'{WORKSPACE}/.vscode/tasks.json', 'w') as f:
        json.dump(tasks_config, f, indent=4)

    print(f'Initial workspace created at: {WORKSPACE}')
    print(f'tasks.json contains only Build C task')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
