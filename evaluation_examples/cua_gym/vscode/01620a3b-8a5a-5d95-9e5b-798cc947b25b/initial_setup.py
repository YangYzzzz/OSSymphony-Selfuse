"""
Initial Setup: Set up a Python project with type checking
Task ID: vscode_wf_025
Domain: vscode

Creates ~/project with Python files containing type annotations.
VSCode settings exist but without typeCheckingMode.
mypy and pyright are NOT installed. No mypy.ini exists.
Opens VSCode with ~/project.
"""

import json
import os
import shlex
import subprocess
import time

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "project")
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
    """Create Python files with type annotations in ~/project."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Main application file with type annotations
    main_py = '''\
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employee:
    name: str
    department: str
    salary: float
    hire_date: datetime
    manager: Optional[str] = None


def calculate_department_budget(employees: List[Employee], department: str) -> float:
    """Calculate total salary budget for a given department."""
    total: float = 0.0
    for emp in employees:
        if emp.department == department:
            total += emp.salary
    return total


def get_employee_by_name(
    employees: List[Employee], name: str
) -> Optional[Employee]:
    """Find an employee by name, returning None if not found."""
    for emp in employees:
        if emp.name == name:
            return emp
    return None


def build_department_roster(
    employees: List[Employee],
) -> Dict[str, List[str]]:
    """Group employee names by department."""
    roster: Dict[str, List[str]] = {}
    for emp in employees:
        if emp.department not in roster:
            roster[emp.department] = []
        roster[emp.department].append(emp.name)
    return roster


def format_salary_report(employees: List[Employee]) -> str:
    """Generate a formatted salary report string."""
    lines: List[str] = ["=== Salary Report ==="]
    for emp in sorted(employees, key=lambda e: e.salary, reverse=True):
        lines.append(f"  {emp.name:<25} {emp.department:<15} ${emp.salary:>10,.2f}")
    total = sum(e.salary for e in employees)
    lines.append(f"\\n  Total Budget: ${total:,.2f}")
    return "\\n".join(lines)


if __name__ == "__main__":
    team: List[Employee] = [
        Employee("Sarah Chen", "Engineering", 125000.0, datetime(2022, 3, 15)),
        Employee("Marcus Johnson", "Marketing", 95000.0, datetime(2021, 7, 1), "Lisa Park"),
        Employee("Anika Patel", "Engineering", 118000.0, datetime(2023, 1, 10), "Sarah Chen"),
        Employee("James Wright", "Sales", 88000.0, datetime(2020, 11, 22)),
        Employee("Lisa Park", "Marketing", 105000.0, datetime(2019, 5, 3)),
    ]

    eng_budget: float = calculate_department_budget(team, "Engineering")
    print(f"Engineering budget: ${eng_budget:,.2f}")

    found: Optional[Employee] = get_employee_by_name(team, "Anika Patel")
    if found:
        print(f"Found: {found.name} in {found.department}")

    roster: Dict[str, List[str]] = build_department_roster(team)
    for dept, names in roster.items():
        print(f"{dept}: {', '.join(names)}")

    print(format_salary_report(team))
'''
    with open(os.path.join(PROJECT_DIR, "main.py"), "w") as f:
        f.write(main_py)

    # Utility module with type annotations
    utils_py = '''\
from typing import TypeVar, Callable, Sequence, Optional
import math

T = TypeVar("T")


def find_first(items: Sequence[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """Return the first item matching the predicate, or None."""
    for item in items:
        if predicate(item):
            return item
    return None


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max bounds."""
    return max(min_val, min(max_val, value))


def percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values."""
    if old_value == 0:
        raise ValueError("Cannot compute percentage change from zero.")
    return ((new_value - old_value) / abs(old_value)) * 100.0


def round_to_nearest(value: float, nearest: float) -> float:
    """Round a value to the nearest multiple of a given number."""
    return round(value / nearest) * nearest


def weighted_average(
    values: Sequence[float], weights: Sequence[float]
) -> float:
    """Compute the weighted average of a sequence of values."""
    if len(values) != len(weights):
        raise ValueError("Values and weights must have the same length.")
    total_weight: float = sum(weights)
    if total_weight == 0:
        raise ValueError("Sum of weights cannot be zero.")
    return sum(v * w for v, w in zip(values, weights)) / total_weight


def euclidean_distance(
    point_a: tuple[float, float], point_b: tuple[float, float]
) -> float:
    """Calculate the Euclidean distance between two 2D points."""
    dx: float = point_b[0] - point_a[0]
    dy: float = point_b[1] - point_a[1]
    return math.sqrt(dx * dx + dy * dy)
'''
    with open(os.path.join(PROJECT_DIR, "utils.py"), "w") as f:
        f.write(utils_py)

    # Config module
    config_py = '''\
from typing import Dict, Any, Optional
from pathlib import Path
import json


class AppConfig:
    """Application configuration manager with type-safe access."""

    def __init__(self, config_path: Path) -> None:
        self._path: Path = config_path
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            with open(self._path, "r") as f:
                self._data = json.load(f)

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(self._data, f, indent=2)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get_string(self, key: str, default: str = "") -> str:
        val = self._data.get(key, default)
        return str(val)

    def get_int(self, key: str, default: int = 0) -> int:
        val = self._data.get(key, default)
        return int(val)

    def get_bool(self, key: str, default: bool = False) -> bool:
        return bool(self._data.get(key, default))
'''
    with open(os.path.join(PROJECT_DIR, "config.py"), "w") as f:
        f.write(config_py)

    print(f"Created project files in {PROJECT_DIR}")


def setup_vscode_settings():
    """Set up VSCode settings WITHOUT typeCheckingMode."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Add some reasonable default settings but NOT typeCheckingMode
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "files.autoSave": "afterDelay",
    })

    # Ensure typeCheckingMode is NOT present
    if "python.analysis.typeCheckingMode" in settings:
        del settings["python.analysis.typeCheckingMode"]

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

    print(f"VSCode settings written to {SETTINGS_PATH}")


def ensure_no_mypy_pyright():
    """Ensure mypy and pyright are NOT installed."""
    for pkg in ["mypy", "pyright"]:
        subprocess.run(
            ["pip3", "uninstall", "-y", pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    print("Ensured mypy and pyright are not installed")


def ensure_no_mypy_ini():
    """Ensure mypy.ini does NOT exist in ~/project."""
    ini_path = os.path.join(PROJECT_DIR, "mypy.ini")
    if os.path.exists(ini_path):
        os.remove(ini_path)
    print("Ensured mypy.ini does not exist in ~/project")


def main():
    create_project_files()
    setup_vscode_settings()
    ensure_no_mypy_pyright()
    ensure_no_mypy_ini()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched VSCode with ~/project and DISPLAY=:0")


main()
