"""
Initial Setup: VSCode open with legacy_code.py containing 15 %-style string formats
Task ID: vscode_py_093
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_093'
OUTPUT = f'{WORKDIR}/legacy_code.py'


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
    content = '''\
#!/usr/bin/env python3
"""
Employee Management System - Legacy Module
Handles employee records, reporting, and notifications.
"""

import datetime
import os
import sys


# ---- Configuration ----
APP_NAME = "EmpManager"
VERSION = "2.4.1"
MAX_RETRIES = 3
DB_TIMEOUT = 30


class Employee:
    """Represents an employee record."""

    def __init__(self, emp_id, first_name, last_name, department, salary):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.salary = salary
        self.hire_date = datetime.date.today()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __repr__(self):
        return "Employee(%s, %s, dept=%s)" % (self.emp_id, self.full_name(), self.department)


def connect_database(host, port, db_name):
    """Establish database connection with retry logic."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print("Connecting to %s:%d/%s (attempt %d of %d)" % (host, port, db_name, attempt, MAX_RETRIES))
            # Simulated connection
            return {"host": host, "port": port, "db": db_name, "status": "connected"}
        except Exception as err:
            print("Connection failed: %s" % err)
    return None


def generate_payroll_report(employees, month, year):
    """Generate monthly payroll summary report."""
    total_payroll = sum(emp.salary for emp in employees)
    avg_salary = total_payroll / len(employees) if employees else 0

    header = "=== Payroll Report for %02d/%d ===" % (month, year)
    print(header)

    for emp in employees:
        line = "  %-30s | Department: %-15s | Salary: $%10.2f" % (
            emp.full_name(), emp.department, emp.salary
        )
        print(line)

    summary = "Total: $%.2f | Average: $%.2f | Headcount: %d" % (
        total_payroll, avg_salary, len(employees)
    )
    print(summary)
    return {"total": total_payroll, "average": avg_salary, "count": len(employees)}


def send_notification(recipient, subject, body):
    """Send email notification to an employee."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = "[%s] Sending to <%s>: %s" % (timestamp, recipient, subject)
    print(msg)
    return True


def process_department_transfer(emp, old_dept, new_dept):
    """Handle employee department transfer."""
    log_entry = "Transfer: %s (ID: %s) from %s to %s" % (
        emp.full_name(), emp.emp_id, old_dept, new_dept
    )
    print(log_entry)
    emp.department = new_dept

    notice = "Dear %s, your department has been changed from %s to %s." % (
        emp.first_name, old_dept, new_dept
    )
    send_notification(emp.first_name, "Department Transfer", notice)
    return log_entry


def export_to_csv(employees, filepath):
    """Export employee list to CSV file."""
    print("Exporting %d records to %s" % (len(employees), filepath))
    with open(filepath, "w") as f:
        f.write("ID,Name,Department,Salary,HireDate\\n")
        for emp in employees:
            row = "%s,%s,%s,%.2f,%s\\n" % (
                emp.emp_id, emp.full_name(), emp.department,
                emp.salary, emp.hire_date
            )
            f.write(row)
    print("Export complete: %s (%d employees)" % (filepath, len(employees)))


def validate_salary_range(emp, min_salary, max_salary):
    """Check if employee salary falls within acceptable range."""
    if emp.salary < min_salary or emp.salary > max_salary:
        warning = "WARNING: %s has salary $%.2f outside range [$%d - $%d]" % (
            emp.full_name(), emp.salary, min_salary, max_salary
        )
        print(warning)
        return False
    return True


def main():
    """Main entry point for the employee management system."""
    print("Starting %s v%s" % (APP_NAME, VERSION))

    employees = [
        Employee("E001", "Sarah", "Chen", "Engineering", 95000),
        Employee("E002", "Marcus", "Johnson", "Marketing", 72000),
        Employee("E003", "Aisha", "Patel", "Engineering", 88000),
        Employee("E004", "David", "Kim", "Finance", 81000),
        Employee("E005", "Elena", "Rodriguez", "Marketing", 69000),
    ]

    db = connect_database("db.internal.corp", 5432, "emp_records")
    if db:
        print("Database ready:", db["status"])

    generate_payroll_report(employees, 3, 2025)

    process_department_transfer(employees[1], "Marketing", "Sales")

    export_to_csv(employees, "/tmp/employees_export.csv")

    for emp in employees:
        validate_salary_range(emp, 50000, 120000)

    print("All operations completed successfully.")


if __name__ == "__main__":
    main()
'''

    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Launch VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
