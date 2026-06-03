"""
Initial Setup: Configure VSCode for large JSON file performance
Task ID: vscode_fix_050
Domain: vscode

Creates ~/data-project with a ~50MB data.json file.
VSCode has no performance settings configured.
Opens VSCode with the data-project folder.
"""

import json
import os
import random
import shlex
import subprocess
import time
import string

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_050'
PROJECT_DIR = os.path.join(WORKDIR, 'data-project')
DATA_FILE = os.path.join(PROJECT_DIR, 'data.json')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def generate_large_json(filepath, target_mb=50):
    """Generate a realistic ~50MB JSON data file."""
    random.seed(42)

    departments = ['Engineering', 'Marketing', 'Sales', 'Finance', 'HR',
                    'Operations', 'Legal', 'Product', 'Design', 'Support']
    cities = ['San Francisco', 'New York', 'London', 'Berlin', 'Tokyo',
              'Sydney', 'Toronto', 'Singapore', 'Dublin', 'Austin']
    statuses = ['active', 'inactive', 'on_leave', 'terminated', 'probation']
    titles = ['Software Engineer', 'Senior Engineer', 'Staff Engineer',
              'Engineering Manager', 'Product Manager', 'Designer',
              'Data Analyst', 'Marketing Specialist', 'Sales Representative',
              'Account Executive', 'Financial Analyst', 'HR Coordinator']

    first_names = ['Sarah', 'Marcus', 'Elena', 'James', 'Priya', 'Carlos',
                   'Aisha', 'David', 'Mei', 'Robert', 'Fatima', 'Thomas',
                   'Yuki', 'Ahmed', 'Isabella', 'Chen', 'Olga', 'Michael',
                   'Nadia', 'Patrick']
    last_names = ['Chen', 'Johnson', 'Rodriguez', 'Kim', 'Patel', 'Williams',
                  'Santos', 'Mueller', 'Tanaka', 'Singh', 'O\'Brien', 'Garcia',
                  'Nakamura', 'Hassan', 'Rossi', 'Wang', 'Petrov', 'Anderson',
                  'Kovacs', 'Lee']

    records = []
    record_id = 100000

    # Each record is roughly 500-600 bytes in JSON, so ~90K records for 50MB
    num_records = 90000

    for i in range(num_records):
        record_id += 1
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        dept = random.choice(departments)
        city = random.choice(cities)

        record = {
            "id": record_id,
            "employee_id": f"EMP-{record_id}",
            "first_name": fname,
            "last_name": lname,
            "email": f"{fname.lower()}.{lname.lower().replace(chr(39), '')}_{record_id}@company.com",
            "department": dept,
            "title": random.choice(titles),
            "location": city,
            "salary": round(random.uniform(45000, 185000), 2),
            "hire_date": f"20{random.randint(15,25):02d}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "status": random.choice(statuses),
            "performance_score": round(random.uniform(1.0, 5.0), 2),
            "projects_completed": random.randint(0, 45),
            "notes": f"Annual review scheduled for Q{random.randint(1,4)} 2026. "
                     f"Current project: {''.join(random.choices(string.ascii_uppercase, k=3))}-{random.randint(100,999)}."
        }
        records.append(record)

    data = {
        "metadata": {
            "generated_at": "2026-03-28T14:30:00Z",
            "version": "3.2.1",
            "total_records": num_records,
            "schema_version": "2.0",
            "source": "hr_data_warehouse",
            "export_format": "json_full"
        },
        "records": records
    }

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"Generated {filepath}: {size_mb:.1f} MB with {num_records} records")


def setup_vscode_defaults():
    """Ensure VSCode settings exist but have NO performance optimizations."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any large-file optimization keys if they happen to exist
    keys_to_remove = [
        'files.maxMemoryForLargeFilesMB',
        'editor.largeFileOptimizations',
        'editor.maxTokenizationLineLength',
        'editor.minimap.enabled',
    ]
    for key in keys_to_remove:
        settings.pop(key, None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings written to {SETTINGS_PATH} (no performance optimizations)")


def create_initial():
    # 1. Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"Created project directory: {PROJECT_DIR}")

    # 2. Generate the large JSON data file
    generate_large_json(DATA_FILE, target_mb=50)

    # 3. Add a small README for realism
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write("""# Data Project

## Overview
This project contains employee data exports from the HR data warehouse.

## Files
- `data.json` - Full employee records export (~50MB)

## Usage
Open `data.json` in your editor to inspect or query records.

**Warning**: The data file is very large. Consider using performance
optimizations or streaming parsers for large datasets.
""")

    # 4. Setup VSCode with no performance settings
    setup_vscode_defaults()

    # 5. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with data-project folder with DISPLAY=:0')


create_initial()
