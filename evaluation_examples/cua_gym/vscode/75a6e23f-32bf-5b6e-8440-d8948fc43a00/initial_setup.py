"""
Initial Setup: Create a Python workspace with interactive_script.py that uses input().
No launch.json exists yet. VSCode is opened with the workspace.
Task ID: vscode_py_037
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_037'
WORKSPACE = f'{WORKDIR}/workspace'
SCRIPT_PATH = f'{WORKSPACE}/interactive_script.py'


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

    # Ensure NO .vscode/launch.json exists
    vscode_dir = os.path.join(WORKSPACE, '.vscode')
    launch_json = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json):
        os.remove(launch_json)

    # Create the interactive Python script that reads from stdin
    script_content = '''#!/usr/bin/env python3
"""
Interactive Data Entry Tool
Collects employee information and generates a summary report.
"""

def get_employee_info():
    """Prompt the user for employee details interactively."""
    print("=" * 50)
    print("  Employee Information Entry System")
    print("=" * 50)
    print()

    name = input("Enter employee name: ")
    department = input("Enter department (Engineering/Marketing/Sales/HR): ")

    while True:
        try:
            salary = float(input("Enter annual salary: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    start_date = input("Enter start date (YYYY-MM-DD): ")
    email = input("Enter email address: ")

    return {
        "name": name,
        "department": department,
        "salary": salary,
        "start_date": start_date,
        "email": email,
    }


def display_summary(employee):
    """Display a formatted summary of the employee data."""
    print()
    print("-" * 50)
    print("  Employee Summary")
    print("-" * 50)
    print(f"  Name:       {employee['name']}")
    print(f"  Department: {employee['department']}")
    print(f"  Salary:     ${employee['salary']:,.2f}")
    print(f"  Start Date: {employee['start_date']}")
    print(f"  Email:      {employee['email']}")
    print("-" * 50)


def main():
    employees = []
    while True:
        emp = get_employee_info()
        employees.append(emp)

        another = input("\\nAdd another employee? (yes/no): ").strip().lower()
        if another != "yes":
            break

    print(f"\\n\\nTotal employees entered: {len(employees)}")
    for i, emp in enumerate(employees, 1):
        print(f"\\n--- Employee {i} ---")
        display_summary(emp)

    print("\\nDone! Thank you for using the Employee Entry System.")


if __name__ == "__main__":
    main()
'''

    with open(SCRIPT_PATH, 'w') as f:
        f.write(script_content)

    print(f'Initial file created: {SCRIPT_PATH}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=3.0)
    # Also open the specific script file in the editor
    launch_gui(f'code "{SCRIPT_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
