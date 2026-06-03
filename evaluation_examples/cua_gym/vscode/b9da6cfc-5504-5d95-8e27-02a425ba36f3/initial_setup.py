"""
Initial Setup: Configure VSCode with language-specific formatter settings
Task ID: vscode_ext_028
Domain: vs_code

Creates a realistic VSCode environment with:
- Extensions installed: esbenp.prettier-vscode and ms-python.python
- settings.json with general settings but NO language-specific formatter settings
- A workspace with JS/TS/Python files open in VSCode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_028'
SETTINGS_DIR = os.path.join('/home/user', '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(SETTINGS_DIR, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'formatter_project')


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


def create_workspace_files():
    """Create a realistic multi-language project workspace."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # JavaScript file
    js_content = """\
// api/userService.js
// Handles user-related API calls

const BASE_URL = 'https://api.example.com/v1';

async function fetchUser(userId) {
    const response = await fetch(`${BASE_URL}/users/${userId}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

async function updateUser(userId, data) {
    const response = await fetch(`${BASE_URL}/users/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return response.json();
}

async function deleteUser(userId) {
    await fetch(`${BASE_URL}/users/${userId}`, { method: 'DELETE' });
}

module.exports = { fetchUser, updateUser, deleteUser };
"""
    with open(os.path.join(WORKSPACE_DIR, 'userService.js'), 'w') as f:
        f.write(js_content)

    # TypeScript file
    ts_content = """\
// components/DataTable.tsx
// Reusable data table component with sorting and pagination

import React, { useState, useCallback } from 'react';

interface Column<T> {
    key: keyof T;
    header: string;
    sortable?: boolean;
    width?: number;
}

interface DataTableProps<T> {
    data: T[];
    columns: Column<T>[];
    pageSize?: number;
    onRowClick?: (row: T) => void;
}

type SortDirection = 'asc' | 'desc' | null;

function DataTable<T extends { id: string | number }>({
    data,
    columns,
    pageSize = 10,
    onRowClick,
}: DataTableProps<T>) {
    const [currentPage, setCurrentPage] = useState(1);
    const [sortKey, setSortKey] = useState<keyof T | null>(null);
    const [sortDir, setSortDir] = useState<SortDirection>(null);

    const handleSort = useCallback((key: keyof T) => {
        if (sortKey === key) {
            setSortDir(prev => prev === 'asc' ? 'desc' : prev === 'desc' ? null : 'asc');
        } else {
            setSortKey(key);
            setSortDir('asc');
        }
    }, [sortKey]);

    const totalPages = Math.ceil(data.length / pageSize);

    return (
        <div className="data-table-container">
            <table className="data-table">
                <thead>
                    <tr>
                        {columns.map(col => (
                            <th key={String(col.key)} onClick={() => col.sortable && handleSort(col.key)}>
                                {col.header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.slice((currentPage - 1) * pageSize, currentPage * pageSize).map(row => (
                        <tr key={row.id} onClick={() => onRowClick?.(row)}>
                            {columns.map(col => (
                                <td key={String(col.key)}>{String(row[col.key])}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="pagination">
                <button disabled={currentPage === 1} onClick={() => setCurrentPage(p => p - 1)}>Prev</button>
                <span>Page {currentPage} of {totalPages}</span>
                <button disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => p + 1)}>Next</button>
            </div>
        </div>
    );
}

export default DataTable;
"""
    with open(os.path.join(WORKSPACE_DIR, 'DataTable.tsx'), 'w') as f:
        f.write(ts_content)

    # Python file
    py_content = """\
# data_processor.py
# Processes and analyzes sales data from CSV exports

import csv
import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path


class SalesDataProcessor:
    \"\"\"Processes raw sales CSV data and generates summary reports.\"\"\"

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.records = []
        self.summary = {}

    def load_csv(self, filename: str) -> int:
        \"\"\"Load sales records from a CSV file. Returns number of records loaded.\"\"\"
        filepath = self.data_dir / filename
        count = 0
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = {
                    'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                    'product': row['product'],
                    'region': row['region'],
                    'quantity': int(row['quantity']),
                    'unit_price': float(row['unit_price']),
                    'revenue': int(row['quantity']) * float(row['unit_price']),
                }
                self.records.append(record)
                count += 1
        return count

    def compute_monthly_summary(self) -> dict:
        \"\"\"Compute total revenue grouped by month and region.\"\"\"
        monthly = defaultdict(lambda: defaultdict(float))
        for rec in self.records:
            month_key = rec['date'].strftime('%Y-%m')
            monthly[month_key][rec['region']] += rec['revenue']
        self.summary['monthly'] = {k: dict(v) for k, v in monthly.items()}
        return self.summary['monthly']

    def top_products(self, n: int = 5) -> list:
        \"\"\"Return the top N products by total revenue.\"\"\"
        product_revenue = defaultdict(float)
        for rec in self.records:
            product_revenue[rec['product']] += rec['revenue']
        sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:n]

    def export_report(self, output_path: str) -> None:
        \"\"\"Export summary report to JSON.\"\"\"
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_records': len(self.records),
            'monthly_summary': self.summary.get('monthly', {}),
            'top_products': self.top_products(),
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        print(f'Report exported to: {output_path}')


if __name__ == '__main__':
    processor = SalesDataProcessor('/home/user/sales_data')
    records = processor.load_csv('q1_sales.csv')
    print(f'Loaded {records} sales records')
    summary = processor.compute_monthly_summary()
    print(f'Monthly summary computed for {len(summary)} months')
    processor.export_report('/home/user/sales_report.json')
"""
    with open(os.path.join(WORKSPACE_DIR, 'data_processor.py'), 'w') as f:
        f.write(py_content)

    # Package.json for context
    package_json = {
        "name": "formatter-project",
        "version": "1.0.0",
        "description": "Multi-language project for formatter configuration",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js",
            "lint": "eslint src --ext .js,.ts,.tsx"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "typescript": "^5.0.0",
            "@types/react": "^18.2.0",
            "eslint": "^8.0.0"
        }
    }
    with open(os.path.join(WORKSPACE_DIR, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)

    print(f'Workspace files created in: {WORKSPACE_DIR}')


def setup_vscode_settings():
    """Create VSCode settings.json with general settings but NO language-specific formatter settings."""
    os.makedirs(SETTINGS_DIR, exist_ok=True)

    # Read existing settings if present, otherwise start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        import re
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        settings = json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Remove any existing language-specific formatter settings (task not yet done)
    for lang_key in ['[javascript]', '[typescript]', '[python]', '[javascriptreact]', '[typescriptreact]']:
        if lang_key in settings:
            del settings[lang_key]

    # Add realistic general settings (but no language-specific formatters)
    general_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "editor.wordWrap": "on",
        "editor.minimap.enabled": True,
        "editor.lineNumbers": "on",
        "editor.renderWhitespace": "selection",
        "editor.formatOnSave": False,
        "editor.suggestSelection": "first",
        "workbench.colorTheme": "Default Dark+",
        "workbench.startupEditor": "none",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "terminal.integrated.fontSize": 13,
        "explorer.confirmDelete": False,
        "extensions.ignoreRecommendations": False,
    }

    # Only add settings that don't already exist (don't overwrite user preferences)
    for k, v in general_settings.items():
        if k not in settings:
            settings[k] = v

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'VSCode settings written to: {SETTINGS_PATH}')
    print('NOTE: No language-specific formatter settings (task not yet completed)')


def create_initial():
    # 1. Create workspace files
    create_workspace_files()

    # 2. Set up VSCode settings (without formatter settings)
    setup_vscode_settings()

    # 3. GUI-ready startup: open VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with formatter_project workspace (DISPLAY=:0)')


create_initial()
