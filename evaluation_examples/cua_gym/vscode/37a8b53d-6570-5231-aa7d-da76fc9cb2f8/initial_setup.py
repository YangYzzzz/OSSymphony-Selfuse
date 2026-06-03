"""
Initial Setup: Configure custom problem matchers for VSCode build tools
Task ID: vscode_gf6_086
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_086'
PROJECT_DIR = f'{WORKDIR}/projects/vscode-problem-matchers'

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
    src_dir = os.path.join(PROJECT_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # --- src/app.py: Python file with 3 syntax errors ---
    app_py_content = '''\
import os
import sys
from datetime import datetime

class DataProcessor:
    """Processes incoming data files and generates reports."""

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.processed_count = 0

    def load_config(self, config_path):
        """Load configuration from a JSON file."""
        with open(config_path, 'r') as f
            config = json.load(f)
        return config

    def process_batch(self, batch_id, records):
        """Process a batch of records and return summary statistics."""
        results = []
        for record in records:
            if record['status'] == 'active'
                transformed = self._transform_record(record)
                results.append(transformed)
            else:
                self._log_skipped(record)
        self.processed_count += len(results)
        return {'batch_id': batch_id, 'count': len(results)}

    def _transform_record(self, record):
        """Apply transformation rules to a single record."""
        output = {
            'id': record['id'],
            'timestamp': datetime.now().isoformat(),
            'value': record['amount'] * 1.15,
            'category': record.get('category', 'uncategorized')
        }
        return output

    def _log_skipped(self, record):
        """Log records that were skipped during processing."""
        print(f"Skipped record {record['id']}: status={record['status']}")

    def generate_report(self, output_path):
        """Generate a summary report of all processed batches."""
        report_lines = [
            f"Processing Report - {datetime.now().strftime('%Y-%m-%d')}",
            f"Total records processed: {self.processed_count}",
            ""
        ]
        with open(output_path 'w') as f:
            f.write('\\n'.join(report_lines))
        print(f"Report saved to {output_path}")


def main():
    processor = DataProcessor('/data/input', '/data/output')
    config = processor.load_config('/etc/app/config.json')
    sample_records = [
        {'id': 'R001', 'status': 'active', 'amount': 150.00, 'category': 'sales'},
        {'id': 'R002', 'status': 'inactive', 'amount': 75.50},
        {'id': 'R003', 'status': 'active', 'amount': 230.00, 'category': 'returns'},
    ]
    result = processor.process_batch('BATCH-2025-001', sample_records)
    print(f"Processed {result['count']} records in batch {result['batch_id']}")
    processor.generate_report('/data/output/report.txt')


if __name__ == '__main__':
    main()
'''
    with open(os.path.join(src_dir, 'app.py'), 'w') as f:
        f.write(app_py_content)

    # --- build.sh: mock build tool that outputs errors ---
    build_sh_content = '''\
#!/bin/bash
# mybuild - Custom Rust-like build tool for vscode-problem-matchers
echo "mybuild v2.1.0 - Starting build..."
echo "Compiling src/app.py..."
echo "ERROR: src/app.py:17:42: SyntaxError: expected colon after expression"
echo "ERROR: src/app.py:27:45: SyntaxError: expected colon after expression"
echo "ERROR: src/app.py:52:30: SyntaxError: missing comma in function call"
echo ""
echo "Build failed with 3 error(s), 0 warning(s)"
exit 1
'''
    build_sh_path = os.path.join(PROJECT_DIR, 'build.sh')
    with open(build_sh_path, 'w') as f:
        f.write(build_sh_content)
    os.chmod(build_sh_path, 0o755)

    # --- lint.sh: mock linter that outputs warnings ---
    lint_sh_content = '''\
#!/bin/bash
# project-lint - Custom linter for vscode-problem-matchers
echo "project-lint v1.3.0 - Linting src/app.py..."
echo "WARN [missing-import] src/app.py line 1: Module 'json' is used but not imported"
echo "WARN [unused-variable] src/app.py line 12: Variable 'processed_count' is assigned but never read externally"
echo "WARN [broad-exception] src/app.py line 40: Consider catching specific exceptions instead of bare except"
echo ""
echo "Lint complete: 0 error(s), 3 warning(s)"
exit 0
'''
    lint_sh_path = os.path.join(PROJECT_DIR, 'lint.sh')
    with open(lint_sh_path, 'w') as f:
        f.write(lint_sh_content)
    os.chmod(lint_sh_path, 0o755)

    # --- NO .vscode/ directory (task requires agent to create it) ---

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/app.py: Python file with 3 syntax errors')
    print(f'  build.sh: Mock build tool')
    print(f'  lint.sh: Mock linter')
    print(f'  No .vscode/ directory')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
