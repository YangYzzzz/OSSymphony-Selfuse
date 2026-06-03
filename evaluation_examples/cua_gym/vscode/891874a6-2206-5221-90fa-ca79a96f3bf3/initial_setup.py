"""
Initial Setup: Create a Python project with interactive quiz script, no launch.json.
Task ID: vscode_td_085
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_085'
PROJECT_DIR = f'{WORKDIR}/projects/interactive-app'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(SRC_DIR, exist_ok=True)

    # Create src/quiz.py - an interactive quiz that uses input()
    quiz_content = '''#!/usr/bin/env python3
"""Interactive Quiz Application - Tests general knowledge with user input."""

import random


QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
        "answer": "C",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
        "answer": "B",
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"],
        "answer": "D",
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["A) Charles Dickens", "B) William Shakespeare", "C) Jane Austen", "D) Mark Twain"],
        "answer": "B",
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["A) CO2", "B) NaCl", "C) H2O", "D) O2"],
        "answer": "C",
    },
]


def run_quiz():
    """Run the interactive quiz, prompting the user for answers."""
    print("=" * 50)
    print("  Welcome to the General Knowledge Quiz!")
    print("=" * 50)
    print()

    name = input("Enter your name: ")
    print(f"\\nHello, {name}! Let\'s begin.\\n")

    score = 0
    selected = random.sample(QUESTIONS, min(3, len(QUESTIONS)))

    for i, q in enumerate(selected, 1):
        print(f"Question {i}: {q[\'question\']}")
        for opt in q["options"]:
            print(f"  {opt}")
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer == q["answer"]:
            print("Correct!\\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was {q[\'answer\']}.\\n")

    print(f"\\n{name}, you scored {score}/{len(selected)}.")
    play_again = input("Play again? (yes/no): ").strip().lower()
    if play_again == "yes":
        run_quiz()
    else:
        print("Thanks for playing! Goodbye.")


if __name__ == "__main__":
    run_quiz()
'''
    with open(f'{SRC_DIR}/quiz.py', 'w') as f:
        f.write(quiz_content)

    # Create a simple README for the project
    readme_content = '''# Interactive App

A collection of interactive Python scripts that demonstrate user input handling.

## Running

```bash
python3 src/quiz.py
```

## Requirements

- Python 3.8+
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme_content)

    # Create a requirements.txt (empty - no external deps)
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('# No external dependencies required\n')

    # Ensure NO .vscode/launch.json exists (the task is to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json):
        os.remove(launch_json)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'Quiz script: {SRC_DIR}/quiz.py')
    print(f'.vscode/launch.json exists: {os.path.exists(launch_json)}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
