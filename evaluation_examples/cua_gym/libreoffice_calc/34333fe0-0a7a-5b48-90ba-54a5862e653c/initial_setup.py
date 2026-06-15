"""
Initial Setup: Set up a Python project in ~/project with main.py and requirements.txt.
VSCode is open with the project folder. No virtual environment, no pylint, empty settings.
Task ID: vscode_wf_011
Domain: vscode (os)
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
SETTINGS_PATH = os.path.join(VSCODE_DIR, 'settings.json')


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
    # Ensure project directory exists
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Remove any pre-existing venv if it exists (idempotent)
    venv_path = os.path.join(PROJECT_DIR, 'venv')
    if os.path.exists(venv_path):
        import shutil
        shutil.rmtree(venv_path)

    # Create main.py with realistic Python content
    main_py_content = '''"""
Employee Performance Analytics Tool
Reads employee data and generates quarterly reports.
"""

import csv
import os
from datetime import datetime


def load_employee_data(filepath: str) -> list:
    """Load employee records from a CSV file."""
    employees = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append({
                'name': row['name'],
                'department': row['department'],
                'performance_score': float(row['performance_score']),
                'hire_date': row['hire_date'],
                'salary': float(row['salary']),
            })
    return employees


def calculate_department_averages(employees: list) -> dict:
    """Calculate average performance score by department."""
    dept_scores = {}
    dept_counts = {}
    for emp in employees:
        dept = emp['department']
        dept_scores[dept] = dept_scores.get(dept, 0) + emp['performance_score']
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    return {dept: dept_scores[dept] / dept_counts[dept] for dept in dept_scores}


def generate_report(employees: list, output_path: str):
    """Generate a quarterly performance summary report."""
    averages = calculate_department_averages(employees)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(output_path, 'w') as f:
        f.write(f"Quarterly Performance Report\\n")
        f.write(f"Generated: {timestamp}\\n")
        f.write(f"{'='*50}\\n\\n")

        f.write("Department Averages:\\n")
        for dept, avg in sorted(averages.items()):
            f.write(f"  {dept}: {avg:.2f}\\n")

        f.write(f"\\nTotal Employees: {len(employees)}\\n")


if __name__ == '__main__':
    data_file = os.path.join(os.path.dirname(__file__), 'data', 'employees.csv')
    if os.path.exists(data_file):
        data = load_employee_data(data_file)
        generate_report(data, 'quarterly_report.txt')
        print("Report generated successfully.")
    else:
        print(f"Data file not found: {data_file}")
'''
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_py_content)

    # Create requirements.txt with common dependencies (but NOT pylint)
    requirements_content = '''# Project dependencies
requests>=2.28.0
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
'''
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # Create empty .vscode/settings.json
    os.makedirs(VSCODE_DIR, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'  main.py: created')
    print(f'  requirements.txt: created')
    print(f'  .vscode/settings.json: empty')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
