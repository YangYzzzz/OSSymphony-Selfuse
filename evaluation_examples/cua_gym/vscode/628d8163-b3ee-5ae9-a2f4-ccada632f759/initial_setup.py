"""
Initial Setup: Create project structure for stdin-processor Python project
Task ID: vscode_td_063
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_063'
PROJECT_DIR = f'{WORKDIR}/projects/stdin-processor'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/data', exist_ok=True)

    # Create src/process.py - a script that reads from stdin
    process_py = '''\
#!/usr/bin/env python3
"""Process data from standard input.

Reads lines from stdin, parses CSV-formatted records,
and produces summary statistics.
"""

import sys
import csv
from collections import defaultdict


def process_input(stream):
    """Read CSV data from a stream and compute per-category totals."""
    reader = csv.DictReader(stream)
    totals = defaultdict(float)
    count = defaultdict(int)

    for row in reader:
        category = row.get("category", "unknown")
        try:
            amount = float(row.get("amount", 0))
        except ValueError:
            continue
        totals[category] += amount
        count[category] += 1

    return totals, count


def main():
    """Entry point: read from stdin and print summary."""
    print("Reading data from stdin...")
    totals, count = process_input(sys.stdin)

    print("\\n=== Summary by Category ===")
    for cat in sorted(totals.keys()):
        avg = totals[cat] / count[cat] if count[cat] else 0
        print(f"  {cat}: total={totals[cat]:.2f}, count={count[cat]}, avg={avg:.2f}")

    grand_total = sum(totals.values())
    print(f"\\nGrand Total: {grand_total:.2f}")


if __name__ == "__main__":
    main()
'''
    with open(f'{PROJECT_DIR}/src/process.py', 'w') as f:
        f.write(process_py)

    # Create data/input.txt - sample CSV input
    input_txt = '''\
category,amount,description
electronics,249.99,Wireless headphones
groceries,45.30,Weekly produce
electronics,899.00,Laptop stand and dock
clothing,78.50,Winter jacket
groceries,32.15,Dairy products
electronics,129.95,USB-C hub
clothing,156.00,Running shoes
groceries,67.80,Meat and seafood
clothing,42.99,Cotton t-shirts pack
electronics,59.99,Phone case bundle
groceries,28.45,Bakery items
clothing,210.00,Formal dress shirt
groceries,51.20,Frozen meals
electronics,349.00,Mechanical keyboard
clothing,95.75,Denim jeans
'''
    with open(f'{PROJECT_DIR}/data/input.txt', 'w') as f:
        f.write(input_txt)

    # Create a simple README for the project
    readme = '''\
# Stdin Processor

A command-line tool that reads CSV data from standard input and produces
summary statistics grouped by category.

## Usage

```bash
cat data/input.txt | python3 src/process.py
```

Or pipe from another command:

```bash
curl -s https://example.com/data.csv | python3 src/process.py
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # NOTE: Do NOT create .vscode/launch.json - that is the task
    print(f'Project created at: {PROJECT_DIR}')
    print(f'  src/process.py - main script')
    print(f'  data/input.txt - sample input')
    print(f'  README.md - project description')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
