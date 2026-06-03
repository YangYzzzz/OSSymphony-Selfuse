"""
Initial Setup: Configure VSCode with default 4-space indentation
Task ID: vscode_we_014
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_014'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')


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
    # 1. Create workspace directory with sample files
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Sample JavaScript file
    js_content = """// utils.js - Utility functions for the project

function formatCurrency(amount) {
    return '$' + amount.toFixed(2);
}

function calculateTax(subtotal, rate) {
    const tax = subtotal * rate;
    return Math.round(tax * 100) / 100;
}

function generateInvoiceNumber() {
    const timestamp = Date.now();
    const random = Math.floor(Math.random() * 1000);
    return `INV-${timestamp}-${random}`;
}

module.exports = {
    formatCurrency,
    calculateTax,
    generateInvoiceNumber
};
"""
    with open(os.path.join(WORKSPACE_DIR, 'utils.js'), 'w') as f:
        f.write(js_content)

    # Sample TypeScript file
    ts_content = """// models.ts - Data models for the application

interface Employee {
    id: number;
    name: string;
    department: string;
    salary: number;
    startDate: Date;
}

interface Department {
    id: number;
    name: string;
    budget: number;
    headCount: number;
}

class EmployeeService {
    private employees: Employee[] = [];

    addEmployee(employee: Employee): void {
        this.employees.push(employee);
    }

    getByDepartment(dept: string): Employee[] {
        return this.employees.filter(e => e.department === dept);
    }

    getTotalSalary(): number {
        return this.employees.reduce((sum, e) => sum + e.salary, 0);
    }
}

export { Employee, Department, EmployeeService };
"""
    with open(os.path.join(WORKSPACE_DIR, 'models.ts'), 'w') as f:
        f.write(ts_content)

    # Sample Python file (to show contrast with 4-space default)
    py_content = """# analytics.py - Data analytics module

import statistics
from typing import List, Dict


def calculate_metrics(values: List[float]) -> Dict[str, float]:
    \"\"\"Calculate basic statistical metrics for a dataset.\"\"\"
    return {
        'mean': statistics.mean(values),
        'median': statistics.median(values),
        'stdev': statistics.stdev(values) if len(values) > 1 else 0.0,
        'min': min(values),
        'max': max(values),
    }


def generate_report(data: Dict[str, List[float]]) -> str:
    \"\"\"Generate a summary report from categorized data.\"\"\"
    lines = ["=== Analytics Report ===\\n"]
    for category, values in data.items():
        metrics = calculate_metrics(values)
        lines.append(f"Category: {category}")
        lines.append(f"  Count: {len(values)}")
        lines.append(f"  Mean:  {metrics['mean']:.2f}")
        lines.append(f"  Median: {metrics['median']:.2f}")
        lines.append("")
    return "\\n".join(lines)
"""
    with open(os.path.join(WORKSPACE_DIR, 'analytics.py'), 'w') as f:
        f.write(py_content)

    # 2. Set up VSCode settings with only the global tabSize
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {
        "editor.tabSize": 4
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings created at: {SETTINGS_PATH}')
    print(f'Workspace created at: {WORKSPACE_DIR}')

    # 3. Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
