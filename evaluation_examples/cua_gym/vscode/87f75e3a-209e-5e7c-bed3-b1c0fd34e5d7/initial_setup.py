"""
Initial Setup: Close all tabs except the active one (main.py)
Task ID: vscode_stu_019
Domain: vscode

Creates a workspace with 6 Python/text files and opens all of them as tabs
in VSCode, with main.py as the active tab.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_019'
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
    os.makedirs(WORKSPACE, exist_ok=True)

    # --- main.py (the active file the user is working on) ---
    with open(os.path.join(WORKSPACE, 'main.py'), 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Employee Performance Dashboard
Generates quarterly reports from HR data.
"""

import os
import sys
from datetime import datetime

from utils import load_employee_data, calculate_metrics
from config import DB_HOST, DB_PORT, REPORT_OUTPUT_DIR


def generate_quarterly_report(quarter: int, year: int):
    """Generate the performance report for a given quarter."""
    employees = load_employee_data(quarter, year)
    metrics = calculate_metrics(employees)

    report_path = os.path.join(
        REPORT_OUTPUT_DIR,
        f"performance_Q{quarter}_{year}.csv"
    )

    with open(report_path, "w") as report_file:
        report_file.write("Employee,Department,Score,Rating\\n")
        for emp in metrics:
            report_file.write(
                f"{emp['name']},{emp['department']},"
                f"{emp['score']:.2f},{emp['rating']}\\n"
            )

    print(f"Report saved to {report_path}")
    return report_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <quarter> <year>")
        sys.exit(1)

    quarter = int(sys.argv[1])
    year = int(sys.argv[2])

    if quarter < 1 or quarter > 4:
        print("Error: Quarter must be between 1 and 4")
        sys.exit(1)

    print(f"Generating Q{quarter} {year} performance report...")
    report = generate_quarterly_report(quarter, year)
    print(f"Done. Report available at: {report}")


if __name__ == "__main__":
    main()
''')

    # --- utils.py ---
    with open(os.path.join(WORKSPACE, 'utils.py'), 'w') as f:
        f.write('''"""
Utility functions for employee data processing.
"""

import csv
import os
from typing import List, Dict


def load_employee_data(quarter: int, year: int) -> List[Dict]:
    """Load employee records for the specified quarter."""
    data_file = f"data/employees_Q{quarter}_{year}.csv"
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    employees = []
    with open(data_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append({
                "id": int(row["employee_id"]),
                "name": row["full_name"],
                "department": row["department"],
                "hours_worked": float(row["hours_worked"]),
                "projects_completed": int(row["projects_completed"]),
                "peer_reviews": float(row["peer_review_avg"]),
            })
    return employees


def calculate_metrics(employees: List[Dict]) -> List[Dict]:
    """Calculate performance metrics for each employee."""
    results = []
    for emp in employees:
        score = (
            emp["hours_worked"] * 0.3
            + emp["projects_completed"] * 15
            + emp["peer_reviews"] * 20
        )
        rating = _score_to_rating(score)
        results.append({
            "name": emp["name"],
            "department": emp["department"],
            "score": score,
            "rating": rating,
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)


def _score_to_rating(score: float) -> str:
    if score >= 150:
        return "Exceptional"
    elif score >= 120:
        return "Exceeds Expectations"
    elif score >= 90:
        return "Meets Expectations"
    elif score >= 60:
        return "Needs Improvement"
    else:
        return "Below Expectations"
''')

    # --- config.py ---
    with open(os.path.join(WORKSPACE, 'config.py'), 'w') as f:
        f.write('''"""
Configuration settings for the Performance Dashboard.
"""

import os

# Database connection
DB_HOST = os.getenv("PERF_DB_HOST", "localhost")
DB_PORT = int(os.getenv("PERF_DB_PORT", "5432"))
DB_NAME = os.getenv("PERF_DB_NAME", "employee_perf")
DB_USER = os.getenv("PERF_DB_USER", "dashboard_svc")

# Report output
REPORT_OUTPUT_DIR = os.getenv("REPORT_DIR", "/home/user/reports")

# Scoring weights
WEIGHT_HOURS = 0.3
WEIGHT_PROJECTS = 15.0
WEIGHT_PEER_REVIEW = 20.0

# Rating thresholds
RATING_EXCEPTIONAL = 150
RATING_EXCEEDS = 120
RATING_MEETS = 90
RATING_NEEDS_IMPROVEMENT = 60

# Departments
DEPARTMENTS = [
    "Engineering",
    "Product Management",
    "Design",
    "Marketing",
    "Sales",
    "Human Resources",
    "Finance",
    "Operations",
]
''')

    # --- test.py ---
    with open(os.path.join(WORKSPACE, 'test.py'), 'w') as f:
        f.write('''"""
Unit tests for the employee performance dashboard.
"""

import unittest
import os
import tempfile
from unittest.mock import patch

from utils import calculate_metrics, _score_to_rating


class TestScoreToRating(unittest.TestCase):
    def test_exceptional(self):
        self.assertEqual(_score_to_rating(160), "Exceptional")
        self.assertEqual(_score_to_rating(150), "Exceptional")

    def test_exceeds_expectations(self):
        self.assertEqual(_score_to_rating(130), "Exceeds Expectations")
        self.assertEqual(_score_to_rating(120), "Exceeds Expectations")

    def test_meets_expectations(self):
        self.assertEqual(_score_to_rating(100), "Meets Expectations")
        self.assertEqual(_score_to_rating(90), "Meets Expectations")

    def test_needs_improvement(self):
        self.assertEqual(_score_to_rating(70), "Needs Improvement")
        self.assertEqual(_score_to_rating(60), "Needs Improvement")

    def test_below_expectations(self):
        self.assertEqual(_score_to_rating(50), "Below Expectations")
        self.assertEqual(_score_to_rating(0), "Below Expectations")


class TestCalculateMetrics(unittest.TestCase):
    def test_basic_calculation(self):
        employees = [
            {
                "name": "Sarah Chen",
                "department": "Engineering",
                "hours_worked": 180.0,
                "projects_completed": 5,
                "peer_reviews": 4.2,
            },
            {
                "name": "Marcus Johnson",
                "department": "Marketing",
                "hours_worked": 160.0,
                "projects_completed": 3,
                "peer_reviews": 3.8,
            },
        ]
        results = calculate_metrics(employees)
        self.assertEqual(len(results), 2)
        # Sarah: 180*0.3 + 5*15 + 4.2*20 = 54 + 75 + 84 = 213
        self.assertAlmostEqual(results[0]["score"], 213.0, places=1)
        self.assertEqual(results[0]["rating"], "Exceptional")

    def test_sorted_by_score_desc(self):
        employees = [
            {
                "name": "Low Performer",
                "department": "Sales",
                "hours_worked": 100.0,
                "projects_completed": 1,
                "peer_reviews": 2.0,
            },
            {
                "name": "High Performer",
                "department": "Engineering",
                "hours_worked": 200.0,
                "projects_completed": 8,
                "peer_reviews": 4.9,
            },
        ]
        results = calculate_metrics(employees)
        self.assertEqual(results[0]["name"], "High Performer")
        self.assertEqual(results[1]["name"], "Low Performer")


if __name__ == "__main__":
    unittest.main()
''')

    # --- readme.md ---
    with open(os.path.join(WORKSPACE, 'readme.md'), 'w') as f:
        f.write('''# Employee Performance Dashboard

A command-line tool for generating quarterly employee performance reports
from HR data exports.

## Requirements

- Python 3.8+
- CSV data files in the `data/` directory

## Usage

```bash
python main.py <quarter> <year>
```

For example, to generate the Q2 2025 report:

```bash
python main.py 2 2025
```

## Output

Reports are saved as CSV files in the configured output directory
(default: `/home/user/reports/`). Each report includes:

- Employee name
- Department
- Performance score (weighted composite)
- Rating category

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| PERF_DB_HOST | localhost | Database host |
| PERF_DB_PORT | 5432 | Database port |
| REPORT_DIR | /home/user/reports | Report output directory |

## Scoring Formula

```
score = hours_worked * 0.3 + projects_completed * 15 + peer_review_avg * 20
```

## Rating Thresholds

| Score | Rating |
|-------|--------|
| >= 150 | Exceptional |
| >= 120 | Exceeds Expectations |
| >= 90  | Meets Expectations |
| >= 60  | Needs Improvement |
| < 60   | Below Expectations |
''')

    # --- notes.txt ---
    with open(os.path.join(WORKSPACE, 'notes.txt'), 'w') as f:
        f.write('''Development Notes - Performance Dashboard
==========================================

2025-03-28: Started refactoring the scoring algorithm. The old
linear model was too simplistic. Need to incorporate manager
feedback as a fourth factor. Discussed with Priya from HR and
she suggested weighting it at 25% of the total score.

2025-03-25: Bug report from finance team - the Q4 2024 report
had duplicate entries for employees who transferred departments
mid-quarter. Need to add deduplication logic in load_employee_data().

2025-03-20: Met with stakeholders. They want the following changes
for the next sprint:
  - Add department-level aggregation (avg score per dept)
  - Export to PDF in addition to CSV
  - Add trend charts comparing quarter-over-quarter performance
  - Filter by minimum hours threshold (exclude part-time)

2025-03-15: Initial prototype working. Testing with Q1 2025 sample
data shows reasonable score distribution. Need more edge case tests.

TODO:
  [ ] Add manager feedback weight to scoring formula
  [ ] Fix duplicate employee bug for department transfers
  [ ] Implement PDF export using reportlab
  [ ] Add department aggregation summary section
  [ ] Write integration tests with mock database
  [ ] Set up CI pipeline for automated testing
''')

    print(f'Workspace created at: {WORKSPACE}')
    print('Files: main.py, utils.py, config.py, test.py, readme.md, notes.txt')

    # Kill any existing VSCode instances for a clean start
    subprocess.run(['pkill', '-f', 'code'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    # Open VSCode with all 6 files as tabs; main.py listed last so it becomes active
    files_to_open = [
        os.path.join(WORKSPACE, 'utils.py'),
        os.path.join(WORKSPACE, 'config.py'),
        os.path.join(WORKSPACE, 'test.py'),
        os.path.join(WORKSPACE, 'readme.md'),
        os.path.join(WORKSPACE, 'notes.txt'),
        os.path.join(WORKSPACE, 'main.py'),
    ]

    # Launch VSCode with all files - the last file in the list becomes the active tab
    file_args = ' '.join(f'"{f}"' for f in files_to_open)
    launch_gui(f'code {file_args}', delay_sec=3.0)

    print('GUI_READY: VSCode launched with 6 tabs open, main.py active')


create_initial()
