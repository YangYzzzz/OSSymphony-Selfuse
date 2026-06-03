"""
Initial Setup: Resolve Git merge conflicts in shared_utils.py
Task ID: vscode_rf_048
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_048'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'collaboration')
FILE_PATH = os.path.join(PROJECT_DIR, 'shared_utils.py')


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


def run_cmd(cmd, cwd=None):
    """Run a shell command."""
    subprocess.run(cmd, shell=True, cwd=cwd, check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def create_initial():
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- Build a git repo with a real merge conflict ---

    # Initialize git repo
    run_cmd('git init', cwd=PROJECT_DIR)
    run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Developer"', cwd=PROJECT_DIR)

    # Create the base version of shared_utils.py (before any branch divergence)
    base_content = '''"""
Shared utility functions for the collaboration project.
Provides common helpers used across multiple modules.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# --- Section 1: String Utilities ---

def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    forbidden = ['<', '>', '&', '"', "'"]
    for char in forbidden:
        text = text.replace(char, '')
    return text.strip()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


# --- Section 2: Date Utilities ---

def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format a datetime object to string."""
    return dt.strftime(fmt)


def get_business_days(start: datetime, end: datetime) -> int:
    """Calculate the number of business days between two dates."""
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count


# --- Section 3: Data Processing ---

def merge_dictionaries(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries, with dict2 values taking precedence."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dictionaries(result[key], value)
        else:
            result[key] = value
    return result


def flatten_list(nested: List) -> List:
    """Flatten a nested list into a single level."""
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat
'''

    with open(FILE_PATH, 'w') as f:
        f.write(base_content)

    run_cmd('git add shared_utils.py', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial commit: shared utility functions"', cwd=PROJECT_DIR)

    # --- Create feature-branch with changes ---
    run_cmd('git checkout -b feature-branch', cwd=PROJECT_DIR)

    feature_content = '''"""
Shared utility functions for the collaboration project.
Provides common helpers used across multiple modules.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# --- Section 1: String Utilities ---

def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into single spaces."""
    import re
    return re.sub(r'\\s+', ' ', text).strip()

def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    forbidden = ['<', '>', '&', '"', "'"]
    for char in forbidden:
        text = text.replace(char, '')
    return text.strip()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


# --- Section 2: Date Utilities ---

def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format a datetime object to string."""
    return dt.strftime(fmt)


def get_business_days(start: datetime, end: datetime) -> int:
    """Calculate the number of business days between two dates."""
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count


def parse_relative_date(text: str) -> Optional[datetime]:
    """Parse relative date expressions like 'yesterday', '3 days ago'."""
    import re
    text = text.lower().strip()
    now = datetime.now()
    if text == 'yesterday':
        return now - timedelta(days=1)
    if text == 'today':
        return now
    match = re.match(r'(\\d+)\\s+days?\\s+ago', text)
    if match:
        return now - timedelta(days=int(match.group(1)))
    return None


# --- Section 3: Data Processing ---

def merge_dictionaries(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries, with dict2 values taking precedence."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dictionaries(result[key], value)
        else:
            result[key] = value
    return result


def flatten_list(nested: List) -> List:
    """Flatten a nested list into a single level."""
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat
'''

    with open(FILE_PATH, 'w') as f:
        f.write(feature_content)

    run_cmd('git add shared_utils.py', cwd=PROJECT_DIR)
    run_cmd('git commit -m "feature-branch: add normalize_whitespace and parse_relative_date"', cwd=PROJECT_DIR)

    # --- Go back to main and make conflicting changes ---
    run_cmd('git checkout master || git checkout main', cwd=PROJECT_DIR)

    main_content = '''"""
Shared utility functions for the collaboration project.
Provides common helpers used across multiple modules.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# --- Section 1: String Utilities ---

def extract_emails(text: str) -> List[str]:
    """Extract all email addresses from a text string."""
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    forbidden = ['<', '>', '&', '"', "'"]
    for char in forbidden:
        text = text.replace(char, '')
    return text.strip()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


# --- Section 2: Date Utilities ---

def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format a datetime object to string."""
    return dt.strftime(fmt)


def get_business_days(start: datetime, end: datetime) -> int:
    """Calculate the number of business days between two dates."""
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count


def calculate_date_range(center: datetime, span_days: int = 7) -> tuple:
    """Calculate a date range centered on a given date."""
    half = span_days // 2
    start = center - timedelta(days=half)
    end = center + timedelta(days=span_days - half)
    return (start, end)


# --- Section 3: Data Processing ---

def merge_dictionaries(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries, with dict2 values taking precedence."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dictionaries(result[key], value)
        else:
            result[key] = value
    return result


def flatten_list(nested: List) -> List:
    """Flatten a nested list into a single level."""
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat
'''

    with open(FILE_PATH, 'w') as f:
        f.write(main_content)

    run_cmd('git add shared_utils.py', cwd=PROJECT_DIR)
    run_cmd('git commit -m "main: add extract_emails and calculate_date_range"', cwd=PROJECT_DIR)

    # --- Attempt merge to create conflicts ---
    try:
        run_cmd('git merge feature-branch', cwd=PROJECT_DIR)
    except subprocess.CalledProcessError:
        # Expected: merge conflict
        pass

    # Verify the conflict markers exist
    with open(FILE_PATH, 'r') as f:
        content = f.read()

    if '<<<<<<<' not in content:
        print("WARNING: No conflict markers found. Creating manual conflict file.")
        # Fallback: manually write the conflicted file
        write_manual_conflict()
    else:
        print(f"Merge conflict created successfully in {FILE_PATH}")
        print(f"Conflict markers found in file.")

    # Show file content for debugging
    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if '<<<<<<<' in line or '=======' in line or '>>>>>>>' in line:
            print(f"  Line {i}: {line.rstrip()}")

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Also open the conflicted file
    launch_gui(f'code "{FILE_PATH}"', delay_sec=2.0)

    print(f'Initial setup complete: {FILE_PATH}')
    print('GUI_READY: launched VSCode with DISPLAY=:0')


def write_manual_conflict():
    """Fallback: write a file with manual conflict markers if git merge didn't produce them."""
    conflict_content = '''"""
Shared utility functions for the collaboration project.
Provides common helpers used across multiple modules.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# --- Section 1: String Utilities ---

<<<<<<< HEAD
def extract_emails(text: str) -> List[str]:
    """Extract all email addresses from a text string."""
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)
=======
def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into single spaces."""
    import re
    return re.sub(r'\\s+', ' ', text).strip()
>>>>>>> feature-branch

def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    forbidden = ['<', '>', '&', '"', "'"]
    for char in forbidden:
        text = text.replace(char, '')
    return text.strip()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


# --- Section 2: Date Utilities ---

def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format a datetime object to string."""
    return dt.strftime(fmt)


def get_business_days(start: datetime, end: datetime) -> int:
    """Calculate the number of business days between two dates."""
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count


<<<<<<< HEAD
def calculate_date_range(center: datetime, span_days: int = 7) -> tuple:
    """Calculate a date range centered on a given date."""
    half = span_days // 2
    start = center - timedelta(days=half)
    end = center + timedelta(days=span_days - half)
    return (start, end)
=======
def parse_relative_date(text: str) -> Optional[datetime]:
    """Parse relative date expressions like 'yesterday', '3 days ago'."""
    import re
    text = text.lower().strip()
    now = datetime.now()
    if text == 'yesterday':
        return now - timedelta(days=1)
    if text == 'today':
        return now
    match = re.match(r'(\\d+)\\s+days?\\s+ago', text)
    if match:
        return now - timedelta(days=int(match.group(1)))
    return None
>>>>>>> feature-branch


# --- Section 3: Data Processing ---

def merge_dictionaries(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries, with dict2 values taking precedence."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dictionaries(result[key], value)
        else:
            result[key] = value
    return result


def flatten_list(nested: List) -> List:
    """Flatten a nested list into a single level."""
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat
'''
    with open(FILE_PATH, 'w') as f:
        f.write(conflict_content)
    print(f"Manual conflict file written to {FILE_PATH}")


create_initial()
