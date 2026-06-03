"""
Initial Setup: Configure VSCode per-language indentation settings
Task ID: vscode_web_054
Domain: vscode

Creates a polyglot project with .js, .ts, .json, .py, and .go files,
all using default 4-space indentation. No language-specific settings exist.
"""

import json
import os
import shlex
import subprocess
import time

HOME = os.path.expanduser("~")
PROJECT_DIR = os.path.join(HOME, "projects", "polyglot")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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


def create_project_files():
    """Create a realistic polyglot project with multiple file types."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # JavaScript file
    js_content = '''\
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/api/users', (req, res) => {
    const users = [
        { id: 1, name: 'Sarah Chen', role: 'engineer' },
        { id: 2, name: 'Marcus Johnson', role: 'designer' },
        { id: 3, name: 'Emily Rodriguez', role: 'manager' },
    ];
    res.json({ success: true, data: users });
});

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', uptime: process.uptime() });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
'''
    with open(os.path.join(PROJECT_DIR, "server.js"), "w") as f:
        f.write(js_content)

    # TypeScript file
    ts_content = '''\
interface User {
    id: number;
    name: string;
    email: string;
    department: string;
}

interface ApiResponse<T> {
    success: boolean;
    data: T;
    timestamp: Date;
}

class UserService {
    private users: User[] = [];

    addUser(user: User): void {
        this.users.push(user);
    }

    getUserById(id: number): User | undefined {
        return this.users.find(u => u.id === id);
    }

    getAllUsers(): ApiResponse<User[]> {
        return {
            success: true,
            data: this.users,
            timestamp: new Date(),
        };
    }
}

export { UserService, User, ApiResponse };
'''
    with open(os.path.join(PROJECT_DIR, "userService.ts"), "w") as f:
        f.write(ts_content)

    # JSON config file
    json_content = {
        "name": "polyglot-project",
        "version": "1.2.0",
        "description": "Multi-language demo project for team collaboration",
        "scripts": {
            "start": "node server.js",
            "build": "tsc && go build -o bin/worker ./cmd/worker",
            "test": "pytest tests/ && jest --coverage",
            "lint": "eslint . && golangci-lint run"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "jest": "^29.7.0",
            "@types/express": "^4.17.21"
        }
    }
    with open(os.path.join(PROJECT_DIR, "package.json"), "w") as f:
        json.dump(json_content, f, indent=4)

    # Python file
    py_content = '''\
"""Data processing module for the polyglot project."""

import csv
import statistics
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class SalesRecord:
    date: datetime
    product: str
    quantity: int
    unit_price: float
    region: str

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


class SalesAnalyzer:
    """Analyzes sales records and generates summary reports."""

    def __init__(self, records: List[SalesRecord]):
        self.records = records

    def total_revenue(self) -> float:
        return sum(r.total for r in self.records)

    def average_order_value(self) -> float:
        totals = [r.total for r in self.records]
        return statistics.mean(totals) if totals else 0.0

    def top_products(self, n: int = 5) -> List[tuple]:
        product_totals: dict = {}
        for record in self.records:
            product_totals[record.product] = (
                product_totals.get(record.product, 0.0) + record.total
            )
        sorted_products = sorted(
            product_totals.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_products[:n]

    def revenue_by_region(self) -> dict:
        region_totals: dict = {}
        for record in self.records:
            region_totals[record.region] = (
                region_totals.get(record.region, 0.0) + record.total
            )
        return region_totals


def load_csv(filepath: str) -> List[SalesRecord]:
    records = []
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append(
                SalesRecord(
                    date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    product=row["product"],
                    quantity=int(row["quantity"]),
                    unit_price=float(row["unit_price"]),
                    region=row["region"],
                )
            )
    return records


if __name__ == "__main__":
    sample_records = [
        SalesRecord(datetime(2025, 1, 15), "Widget Pro", 42, 29.99, "North America"),
        SalesRecord(datetime(2025, 1, 16), "Gadget Plus", 18, 49.50, "Europe"),
        SalesRecord(datetime(2025, 2, 1), "Widget Pro", 35, 29.99, "Asia Pacific"),
    ]
    analyzer = SalesAnalyzer(sample_records)
    print(f"Total Revenue: ${analyzer.total_revenue():,.2f}")
    print(f"Average Order: ${analyzer.average_order_value():,.2f}")
'''
    with open(os.path.join(PROJECT_DIR, "analytics.py"), "w") as f:
        f.write(py_content)

    # Go file
    go_content = '''\
package main

import (
\t"encoding/json"
\t"fmt"
\t"log"
\t"net/http"
\t"sync"
\t"time"
)

type Task struct {
\tID        int       `json:"id"`
\tTitle     string    `json:"title"`
\tStatus    string    `json:"status"`
\tAssignee  string    `json:"assignee"`
\tCreatedAt time.Time `json:"created_at"`
}

type TaskStore struct {
\tmu    sync.RWMutex
\ttasks []Task
\tnextID int
}

func NewTaskStore() *TaskStore {
\treturn &TaskStore{
\t\ttasks:  make([]Task, 0),
\t\tnextID: 1,
\t}
}

func (s *TaskStore) Add(title, assignee string) Task {
\ts.mu.Lock()
\tdefer s.mu.Unlock()
\ttask := Task{
\t\tID:        s.nextID,
\t\tTitle:     title,
\t\tStatus:    "pending",
\t\tAssignee:  assignee,
\t\tCreatedAt: time.Now(),
\t}
\ts.tasks = append(s.tasks, task)
\ts.nextID++
\treturn task
}

func (s *TaskStore) List() []Task {
\ts.mu.RLock()
\tdefer s.mu.RUnlock()
\tresult := make([]Task, len(s.tasks))
\tcopy(result, s.tasks)
\treturn result
}

func main() {
\tstore := NewTaskStore()
\tstore.Add("Set up CI pipeline", "Sarah Chen")
\tstore.Add("Review API endpoints", "Marcus Johnson")
\tstore.Add("Update documentation", "Emily Rodriguez")

\thttp.HandleFunc("/tasks", func(w http.ResponseWriter, r *http.Request) {
\t\tw.Header().Set("Content-Type", "application/json")
\t\tjson.NewEncoder(w).Encode(store.List())
\t})

\tfmt.Println("Task worker starting on :8080")
\tlog.Fatal(http.ListenAndServe(":8080", nil))
}
'''
    with open(os.path.join(PROJECT_DIR, "worker.go"), "w") as f:
        f.write(go_content)

    print(f"Project files created in {PROJECT_DIR}")


def setup_vscode_settings():
    """Set up default VSCode settings with NO language-specific overrides."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any existing language-specific sections to ensure clean state
    lang_keys = [k for k in settings if k.startswith("[") and k.endswith("]")]
    for k in lang_keys:
        del settings[k]

    # Set default editor settings (no language-specific overrides)
    settings.update({
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "editor.fontSize": 14,
        "editor.wordWrap": "off",
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
    })

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings written to {SETTINGS_PATH}")


def main():
    create_project_files()
    setup_vscode_settings()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


main()
