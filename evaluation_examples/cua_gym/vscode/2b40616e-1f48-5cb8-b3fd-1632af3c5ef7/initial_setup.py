"""
Initial Setup: SQL Query Optimizer project skeleton
Task ID: vscode_gf4_091
Domain: vscode

Creates ~/projects/python-query-optimizer with:
  - src/__init__.py (empty package marker)
  - fixtures/queries.sql (8 sample SQL queries of varying complexity)
  - Python extension installed
  - VSCode opened with the project folder
  - No virtual environment, no optimizer code, no tests
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_091'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-query-optimizer')

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
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'fixtures'), exist_ok=True)

    # src/__init__.py - empty package marker
    init_path = os.path.join(PROJECT_DIR, 'src', '__init__.py')
    with open(init_path, 'w') as f:
        f.write('')
    print(f'Created: {init_path}')

    # fixtures/queries.sql - 8 sample SQL queries of varying complexity
    queries_sql = """-- Sample SQL queries for testing the query optimizer
-- These queries range from simple selects to complex multi-table joins

-- Query 1: Simple SELECT with WHERE clause
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department_id = 10;

-- Query 2: Two-table JOIN with filter
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE d.location_id = 1700;

-- Query 3: Aggregate with GROUP BY and HAVING
SELECT department_id, COUNT(*) AS headcount, AVG(salary) AS avg_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 6000;

-- Query 4: Multi-table JOIN with ORDER BY
SELECT e.first_name, e.last_name, j.job_title, d.department_name
FROM employees e
JOIN jobs j ON e.job_id = j.job_id
JOIN departments d ON e.department_id = d.department_id
ORDER BY d.department_name, e.last_name;

-- Query 5: Subquery in WHERE clause
SELECT first_name, last_name, salary
FROM employees
WHERE salary > (
    SELECT AVG(salary) FROM employees
);

-- Query 6: Three-table JOIN with multiple conditions
SELECT e.first_name, e.last_name, d.department_name, l.city, l.country_id
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN locations l ON d.location_id = l.location_id
WHERE l.country_id = 'US'
  AND e.salary > 5000;

-- Query 7: Self-join to find employees and their managers
SELECT e.first_name AS employee_name,
       m.first_name AS manager_name,
       e.salary AS employee_salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;

-- Query 8: Complex query with multiple JOINs, subquery, and aggregation
SELECT d.department_name,
       COUNT(e.employee_id) AS total_employees,
       SUM(e.salary) AS total_payroll,
       MAX(e.salary) AS highest_salary
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN locations l ON d.location_id = l.location_id
WHERE d.department_id IN (
    SELECT department_id FROM employees
    GROUP BY department_id
    HAVING COUNT(*) >= 3
)
GROUP BY d.department_name
ORDER BY total_payroll DESC;
"""
    queries_path = os.path.join(PROJECT_DIR, 'fixtures', 'queries.sql')
    with open(queries_path, 'w') as f:
        f.write(queries_sql)
    print(f'Created: {queries_path}')

    # Ensure Python extension is installed in VSCode
    try:
        subprocess.run(['code', '--install-extension', 'ms-python.python'],
                      capture_output=True, text=True, timeout=30)
        print('Python extension installed/verified')
    except Exception as ex:
        print(f'Extension install note: {ex}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print(f'GUI_READY: launched VSCode with {PROJECT_DIR}')

create_initial()
