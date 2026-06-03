"""
Initial Setup: Create student.py with __init__ method missing 'self.' prefix on assignments.
Task ID: vscode_stu_034
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_034'
OUTPUT = f'{WORKDIR}/{TASK_ID}.py'


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
    content = '''\
class Student:
    """Represents a university student record."""

    def __init__(self, name, age, grade, major, gpa):
        name = name
        age = age
        grade = grade
        major = major
        gpa = gpa

    def get_summary(self):
        return f"{self.name} ({self.age}), {self.major} - Grade: {self.grade}, GPA: {self.gpa}"

    def is_honor_roll(self):
        return self.gpa >= 3.5

    def promote(self):
        grade_order = ["Freshman", "Sophomore", "Junior", "Senior"]
        if self.grade in grade_order:
            idx = grade_order.index(self.grade)
            if idx < len(grade_order) - 1:
                self.grade = grade_order[idx + 1]


if __name__ == "__main__":
    s = Student("Alice", 20, "Junior", "Computer Science", 3.8)
    print(s.get_summary())
    print(f"Honor roll: {s.is_honor_roll()}")
'''

    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
