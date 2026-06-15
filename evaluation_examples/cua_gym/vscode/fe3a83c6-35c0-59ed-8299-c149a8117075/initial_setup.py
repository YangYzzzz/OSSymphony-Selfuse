"""
Initial Setup: Configure c_cpp_properties.json for mixed C/C++ project
Task ID: vscode_lang_085
Domain: vscode

Creates a mixed C/C++ project with a basic c_cpp_properties.json that does NOT
differentiate between C and C++ standards (uses older defaults).
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_085'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
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
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/include', exist_ok=True)

    # --- c_cpp_properties.json: single config WITHOUT cStandard/cppStandard differentiation ---
    # Uses older defaults (c11 / c++14) - the task is to update these
    cpp_properties = {
        "configurations": [
            {
                "name": "Linux",
                "includePath": [
                    "${workspaceFolder}/**",
                    "/usr/include",
                    "/usr/local/include"
                ],
                "defines": [],
                "compilerPath": "/usr/bin/gcc",
                "cStandard": "c11",
                "cppStandard": "c++14",
                "intelliSenseMode": "linux-gcc-x64"
            }
        ],
        "version": 4
    }
    with open(f'{VSCODE_DIR}/c_cpp_properties.json', 'w') as f:
        json.dump(cpp_properties, f, indent=4)

    # --- C source file using C17 features (will show warnings with c11) ---
    c_source = '''#include <stdio.h>
#include <stdbool.h>
#include <string.h>

// Sensor data processing module
typedef struct {
    int sensor_id;
    double temperature;
    double humidity;
    bool is_active;
    char location[64];
} SensorReading;

static inline double celsius_to_fahrenheit(double celsius) {
    return celsius * 9.0 / 5.0 + 32.0;
}

void print_sensor_summary(const SensorReading readings[], int count) {
    printf("\\n=== Sensor Summary Report ===\\n");
    printf("%-10s %-15s %-12s %-12s %-8s\\n",
           "ID", "Location", "Temp (C)", "Humidity", "Active");
    printf("--------------------------------------------------------------\\n");

    double total_temp = 0.0;
    int active_count = 0;

    for (int i = 0; i < count; i++) {
        printf("%-10d %-15s %-12.1f %-12.1f %-8s\\n",
               readings[i].sensor_id,
               readings[i].location,
               readings[i].temperature,
               readings[i].humidity,
               readings[i].is_active ? "Yes" : "No");

        total_temp += readings[i].temperature;
        if (readings[i].is_active) active_count++;
    }

    printf("\\nAverage Temperature: %.1f C (%.1f F)\\n",
           total_temp / count,
           celsius_to_fahrenheit(total_temp / count));
    printf("Active Sensors: %d / %d\\n", active_count, count);
}

int main(void) {
    SensorReading readings[] = {
        {101, "Lab A",     22.5, 45.2, true},
        {102, "Lab B",     24.1, 52.8, true},
        {103, "Server Rm", 28.7, 38.5, true},
        {104, "Lobby",     21.0, 60.1, false},
        {105, "Warehouse", 18.3, 72.4, true},
        {106, "Roof",      31.2, 35.0, false},
    };

    int count = sizeof(readings) / sizeof(readings[0]);
    print_sensor_summary(readings, count);

    return 0;
}
'''
    with open(f'{PROJECT_DIR}/src/sensor_monitor.c', 'w') as f:
        f.write(c_source)

    # --- C++ source file using C++20 features (concepts, ranges) ---
    cpp_source = '''#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <cmath>

// Employee performance tracking system

struct Employee {
    std::string name;
    std::string department;
    int employee_id;
    double performance_score;
    int projects_completed;
    double salary;
};

class PerformanceTracker {
public:
    void add_employee(const Employee& emp) {
        employees_.push_back(emp);
    }

    double average_score() const {
        if (employees_.empty()) return 0.0;
        double total = 0.0;
        for (const auto& emp : employees_) {
            total += emp.performance_score;
        }
        return total / employees_.size();
    }

    std::vector<Employee> top_performers(double threshold) const {
        std::vector<Employee> result;
        for (const auto& emp : employees_) {
            if (emp.performance_score >= threshold) {
                result.push_back(emp);
            }
        }
        std::sort(result.begin(), result.end(),
            [](const Employee& a, const Employee& b) {
                return a.performance_score > b.performance_score;
            });
        return result;
    }

    void print_department_summary() const {
        std::cout << "\\n=== Department Performance Summary ===\\n";
        std::cout << "Total Employees: " << employees_.size() << "\\n";
        std::cout << "Average Score: " << average_score() << "\\n\\n";

        for (const auto& emp : employees_) {
            std::cout << "  " << emp.name
                      << " (" << emp.department << ")"
                      << " - Score: " << emp.performance_score
                      << " | Projects: " << emp.projects_completed
                      << "\\n";
        }
    }

private:
    std::vector<Employee> employees_;
};

int main() {
    PerformanceTracker tracker;

    tracker.add_employee({"Alice Nakamura", "Engineering", 1001, 92.5, 8, 125000});
    tracker.add_employee({"Carlos Rivera", "Engineering", 1002, 88.3, 6, 118000});
    tracker.add_employee({"Priya Sharma", "Data Science", 1003, 95.1, 10, 135000});
    tracker.add_employee({"David Kim", "Marketing", 1004, 78.6, 4, 95000});
    tracker.add_employee({"Elena Volkov", "Data Science", 1005, 91.2, 7, 128000});
    tracker.add_employee({"James Okafor", "Product", 1006, 85.4, 5, 110000});
    tracker.add_employee({"Maria Santos", "Engineering", 1007, 90.0, 9, 130000});
    tracker.add_employee({"Wei Zhang", "Product", 1008, 82.1, 3, 105000});

    tracker.print_department_summary();

    auto stars = tracker.top_performers(90.0);
    std::cout << "\\nTop Performers (score >= 90):\\n";
    for (const auto& emp : stars) {
        std::cout << "  " << emp.name << ": " << emp.performance_score << "\\n";
    }

    return 0;
}
'''
    with open(f'{PROJECT_DIR}/src/performance_tracker.cpp', 'w') as f:
        f.write(cpp_source)

    # --- Header file ---
    header = '''#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>

// Common utility macros
#define LOG_INFO(msg)  printf("[INFO]  %s\\n", msg)
#define LOG_WARN(msg)  printf("[WARN]  %s\\n", msg)
#define LOG_ERROR(msg) printf("[ERROR] %s\\n", msg)

// Math helpers
static inline double clamp(double value, double min_val, double max_val) {
    if (value < min_val) return min_val;
    if (value > max_val) return max_val;
    return value;
}

#endif // UTILS_H
'''
    with open(f'{PROJECT_DIR}/include/utils.h', 'w') as f:
        f.write(header)

    # --- Makefile ---
    makefile = '''CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -Iinclude
CXXFLAGS = -Wall -Wextra -Iinclude
SRCDIR = src
BUILDDIR = build

.PHONY: all clean

all: $(BUILDDIR)/sensor_monitor $(BUILDDIR)/performance_tracker

$(BUILDDIR)/sensor_monitor: $(SRCDIR)/sensor_monitor.c
\tmkdir -p $(BUILDDIR)
\t$(CC) $(CFLAGS) -o $@ $<

$(BUILDDIR)/performance_tracker: $(SRCDIR)/performance_tracker.cpp
\tmkdir -p $(BUILDDIR)
\t$(CXX) $(CXXFLAGS) -o $@ $<

clean:
\trm -rf $(BUILDDIR)
'''
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write(makefile)

    # --- README ---
    readme = '''# Sensor & Performance Tracking Suite

A mixed C/C++ project for IoT sensor monitoring and employee performance analytics.

## Components

- **sensor_monitor.c** - Real-time sensor data collection and reporting (C)
- **performance_tracker.cpp** - Employee performance analytics engine (C++)

## Build

```bash
make all
```

## Requirements

- GCC 10+ (for C17 support)
- G++ 10+ (for C++20 support)
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'c_cpp_properties.json: cStandard=c11, cppStandard=c++14')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
