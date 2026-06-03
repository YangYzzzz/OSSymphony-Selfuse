"""
Initial Setup: Compare two assignment files side by side using VSCode diff
Task ID: vscode_stu_084
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_084'
HW_DIR = os.path.join(WORKDIR, 'cs101', 'hw6')


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
    os.makedirs(HW_DIR, exist_ok=True)

    # version1.py - Original version of the assignment
    version1_content = '''"""
CS101 - Homework 6: Student Grade Analyzer
Author: Emily Rodriguez
Date: 2025-09-28
"""

import statistics


def load_grades(filename):
    """Load student grades from a CSV-style text file."""
    grades = {}
    with open(filename, 'r') as f:
        header = f.readline().strip().split(',')
        for line in f:
            parts = line.strip().split(',')
            name = parts[0]
            scores = [int(x) for x in parts[1:]]
            grades[name] = scores
    return grades


def calculate_average(scores):
    """Calculate the average of a list of scores."""
    if not scores:
        return 0
    return sum(scores) / len(scores)


def find_top_student(grades):
    """Find the student with the highest average."""
    best_name = None
    best_avg = 0
    for name, scores in grades.items():
        avg = calculate_average(scores)
        if avg > best_avg:
            best_avg = avg
            best_name = name
    return best_name, best_avg


def get_grade_letter(score):
    """Convert numeric score to letter grade."""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def print_report(grades):
    """Print a formatted grade report."""
    print("=" * 50)
    print("GRADE REPORT")
    print("=" * 50)
    for name, scores in grades.items():
        avg = calculate_average(scores)
        letter = get_grade_letter(avg)
        print(f"{name}: Average = {avg:.1f} ({letter})")
    print("-" * 50)
    top_name, top_avg = find_top_student(grades)
    print(f"Top Student: {top_name} with {top_avg:.1f}")


if __name__ == '__main__':
    sample_grades = {
        'Alice Chen': [92, 88, 95, 91],
        'Bob Martinez': [78, 82, 75, 80],
        'Carol Williams': [95, 97, 93, 98],
        'David Kim': [65, 70, 68, 72],
        'Eva Johnson': [88, 85, 90, 87],
    }
    print_report(sample_grades)
'''

    # version2.py - Updated version with several differences
    version2_content = '''"""
CS101 - Homework 6: Student Grade Analyzer
Author: Emily Rodriguez
Date: 2025-10-05
Version: 2.0 - Added median calculation and curve support
"""

import statistics
from collections import defaultdict


def load_grades(filename):
    """Load student grades from a CSV-style text file."""
    grades = {}
    with open(filename, 'r') as f:
        header = f.readline().strip().split(',')
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 2:
                continue
            name = parts[0].strip()
            scores = [int(x) for x in parts[1:] if x.strip()]
            grades[name] = scores
    return grades


def calculate_average(scores):
    """Calculate the average of a list of scores."""
    if not scores:
        return 0.0
    return statistics.mean(scores)


def calculate_median(scores):
    """Calculate the median of a list of scores."""
    if not scores:
        return 0.0
    return statistics.median(scores)


def find_top_student(grades):
    """Find the student with the highest average."""
    best_name = None
    best_avg = -1
    for name, scores in grades.items():
        avg = calculate_average(scores)
        if avg > best_avg:
            best_avg = avg
            best_name = name
    return best_name, best_avg


def apply_curve(scores, curve_points=5):
    """Apply a curve to all scores, capping at 100."""
    return [min(100, s + curve_points) for s in scores]


def get_grade_letter(score):
    """Convert numeric score to letter grade using plus/minus system."""
    if score >= 93:
        return 'A'
    elif score >= 90:
        return 'A-'
    elif score >= 87:
        return 'B+'
    elif score >= 83:
        return 'B'
    elif score >= 80:
        return 'B-'
    elif score >= 77:
        return 'C+'
    elif score >= 73:
        return 'C'
    elif score >= 70:
        return 'C-'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def get_class_statistics(grades):
    """Calculate overall class statistics."""
    all_averages = [calculate_average(s) for s in grades.values()]
    return {
        'class_mean': statistics.mean(all_averages),
        'class_median': statistics.median(all_averages),
        'class_stdev': statistics.stdev(all_averages) if len(all_averages) > 1 else 0,
    }


def print_report(grades, apply_curve_flag=False):
    """Print a formatted grade report with optional curve."""
    print("=" * 60)
    print("GRADE REPORT")
    if apply_curve_flag:
        print("(5-point curve applied)")
    print("=" * 60)
    for name, scores in sorted(grades.items()):
        if apply_curve_flag:
            scores = apply_curve(scores)
        avg = calculate_average(scores)
        med = calculate_median(scores)
        letter = get_grade_letter(avg)
        print(f"{name}: Avg = {avg:.1f}, Median = {med:.1f} ({letter})")
    print("-" * 60)
    top_name, top_avg = find_top_student(grades)
    stats = get_class_statistics(grades)
    print(f"Top Student: {top_name} with {top_avg:.1f}")
    print(f"Class Mean: {stats['class_mean']:.1f}")
    print(f"Class Median: {stats['class_median']:.1f}")


if __name__ == '__main__':
    sample_grades = {
        'Alice Chen': [92, 88, 95, 91],
        'Bob Martinez': [78, 82, 75, 80],
        'Carol Williams': [95, 97, 93, 98],
        'David Kim': [65, 70, 68, 72],
        'Eva Johnson': [88, 85, 90, 87],
        'Frank Lee': [73, 79, 81, 76],
    }
    print_report(sample_grades, apply_curve_flag=False)
'''

    v1_path = os.path.join(HW_DIR, 'version1.py')
    v2_path = os.path.join(HW_DIR, 'version2.py')

    with open(v1_path, 'w') as f:
        f.write(version1_content)
    print(f'Created: {v1_path}')

    with open(v2_path, 'w') as f:
        f.write(version2_content)
    print(f'Created: {v2_path}')

    # Launch VSCode with the hw6 folder open
    launch_gui(f'code "{HW_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0 on ~/cs101/hw6')


create_initial()
