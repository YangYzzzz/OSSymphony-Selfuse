"""
Initial Setup: Python performance profiling project with slow data processor
Task ID: vscode_gf6_026
Domain: vscode
"""

import csv
import os
import random
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_026'
PROJECT_DIR = f'{WORKDIR}/projects/perf-profiling'
SRC_DIR = f'{PROJECT_DIR}/src'
DATA_DIR = f'{PROJECT_DIR}/data'
VENV_DIR = f'{PROJECT_DIR}/venv'


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


def create_project_structure():
    """Create the project directory structure."""
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # Create __init__.py for src package
    with open(f'{SRC_DIR}/__init__.py', 'w') as f:
        f.write('')


def create_slow_data_processor():
    """Create the intentionally slow data_processor.py with O(n^2) deduplication."""
    code = '''\
#!/usr/bin/env python3
"""
Data Processor - Reads large_dataset.csv and processes rows.
Performs deduplication and aggregation on transaction data.
"""

import csv
import os
import sys
import time


def load_csv(filepath):
    """Load CSV data from file."""
    rows = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def process_row(row, seen_transactions):
    """
    Process a single row and check for duplicate transaction IDs.
    Uses a list scan for deduplication (slow for large datasets).
    """
    txn_id = row['transaction_id']

    # Check if this transaction ID was already seen
    # NOTE: This is O(n) per call because we search through a list
    if txn_id in seen_transactions:
        return None  # duplicate, skip

    # Add to seen list (O(1) append, but the 'in' check above is O(n))
    seen_transactions.append(txn_id)

    # Process the row data
    amount = float(row['amount'])
    category = row['category']
    return {
        'transaction_id': txn_id,
        'customer': row['customer_name'],
        'amount': amount,
        'category': category,
        'region': row['region'],
    }


def aggregate_by_category(processed_rows):
    """Aggregate totals by category."""
    totals = {}
    for row in processed_rows:
        cat = row['category']
        if cat not in totals:
            totals[cat] = {'count': 0, 'total_amount': 0.0}
        totals[cat]['count'] += 1
        totals[cat]['total_amount'] += row['amount']
    return totals


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_path = os.path.join(project_dir, 'data', 'large_dataset.csv')

    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        sys.exit(1)

    print(f"Loading data from {data_path}...")
    start_time = time.time()

    rows = load_csv(data_path)
    print(f"Loaded {len(rows)} rows in {time.time() - start_time:.2f}s")

    print("Processing rows...")
    process_start = time.time()

    seen_transactions = []  # Using a list - causes O(n^2) behavior!
    processed = []

    for row in rows:
        result = process_row(row, seen_transactions)
        if result is not None:
            processed.append(result)

    process_time = time.time() - process_start
    print(f"Processed {len(processed)} unique rows in {process_time:.2f}s")

    # Aggregate results
    totals = aggregate_by_category(processed)
    print("\\nCategory Summary:")
    print("-" * 50)
    for cat, data in sorted(totals.items()):
        print(f"  {cat:20s}  Count: {data['count']:6d}  Total: ${data['total_amount']:12,.2f}")

    total_time = time.time() - start_time
    print(f"\\nTotal execution time: {total_time:.2f}s")


if __name__ == '__main__':
    main()
'''
    with open(f'{SRC_DIR}/data_processor.py', 'w') as f:
        f.write(code)
    print(f'Created: {SRC_DIR}/data_processor.py')


def create_large_dataset():
    """Create a 100,000-row CSV dataset."""
    random.seed(42)

    categories = [
        'Electronics', 'Clothing', 'Home & Garden', 'Sports',
        'Books', 'Automotive', 'Health', 'Food & Beverage',
        'Office Supplies', 'Toys'
    ]

    regions = [
        'North America', 'Europe', 'Asia Pacific',
        'Latin America', 'Middle East'
    ]

    first_names = [
        'Sarah', 'Marcus', 'Elena', 'David', 'Priya', 'James',
        'Maria', 'Robert', 'Yuki', 'Chen', 'Fatima', 'Alex',
        'Lisa', 'Omar', 'Sofia', 'Wei', 'Anna', 'Carlos',
        'Kenji', 'Aisha', 'Thomas', 'Rachel', 'Ahmed', 'Julia'
    ]

    last_names = [
        'Chen', 'Johnson', 'Patel', 'Rodriguez', 'Kim', 'Williams',
        'Garcia', 'Mueller', 'Tanaka', 'Singh', 'Brown', 'Wilson',
        'Anderson', 'Taylor', 'Moore', 'Jackson', 'Lee', 'Lopez'
    ]

    filepath = f'{DATA_DIR}/large_dataset.csv'
    num_rows = 100000
    # ~5% duplicates to make deduplication meaningful
    num_unique = int(num_rows * 0.95)

    unique_ids = [f'TXN-{i:07d}' for i in range(1, num_unique + 1)]
    # Add duplicates by sampling from existing IDs
    duplicate_ids = random.choices(unique_ids, k=num_rows - num_unique)
    all_ids = unique_ids + duplicate_ids
    random.shuffle(all_ids)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['transaction_id', 'customer_name', 'amount', 'category', 'region', 'date'])

        for i, txn_id in enumerate(all_ids):
            customer = f'{random.choice(first_names)} {random.choice(last_names)}'
            amount = round(random.uniform(5.99, 2499.99), 2)
            category = random.choice(categories)
            region = random.choice(regions)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date = f'2025-{month:02d}-{day:02d}'
            writer.writerow([txn_id, customer, amount, category, region, date])

    print(f'Created: {filepath} ({num_rows} rows)')


def create_venv():
    """Create a Python virtual environment with required packages (except snakeviz)."""
    # Install virtualenv if not available
    subprocess.run(
        ['pip3', 'install', '--user', 'virtualenv'],
        capture_output=True
    )
    # Create venv using virtualenv (python3-venv may not be installed)
    subprocess.run(
        ['python3', '-m', 'virtualenv', VENV_DIR],
        check=True
    )
    print(f'Created venv at {VENV_DIR}')

    # Install basic packages (NOT snakeviz - that's part of the task)
    pip_path = f'{VENV_DIR}/bin/pip'
    subprocess.run(
        [pip_path, 'install', '--quiet', 'pandas', 'matplotlib'],
        check=True
    )
    print('Installed base packages in venv (pandas, matplotlib)')


def create_readme():
    """Create a README for the project."""
    readme = """\
# Performance Profiling Project

A data processing pipeline that reads transaction data from CSV and performs
deduplication and aggregation.

## Project Structure

```
perf-profiling/
├── src/
│   ├── __init__.py
│   └── data_processor.py    # Main processing script
├── data/
│   └── large_dataset.csv    # 100K row transaction dataset
├── venv/                    # Python virtual environment
└── README.md
```

## Usage

```bash
source venv/bin/activate
python src/data_processor.py
```

## Known Issues

- Processing 100K rows is currently very slow (~30 seconds).
  Performance profiling is recommended to identify bottlenecks.
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)
    print(f'Created: {PROJECT_DIR}/README.md')


def main():
    print('=== Setting up perf-profiling project ===')

    create_project_structure()
    create_slow_data_processor()
    create_large_dataset()
    create_venv()
    create_readme()

    # Ensure no profile.out or launch.json exist (clean state)
    for path in [f'{PROJECT_DIR}/profile.out', f'{PROJECT_DIR}/.vscode/launch.json']:
        if os.path.exists(path):
            os.remove(path)

    print('\n=== Project setup complete ===')

    # GUI-ready: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
