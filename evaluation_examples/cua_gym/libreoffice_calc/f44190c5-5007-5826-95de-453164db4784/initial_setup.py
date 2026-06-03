"""
Initial Setup: Grammar Quiz Compilation Task
Task ID: osworld_multi_apps_grammar_test_compile_001
Domain: multi_apps (OS file management + LibreOffice Writer)

Creates:
  - /home/user/Desktop/quiz_files/quiz_part1.txt  (5 grammar questions, unnumbered)
  - /home/user/Desktop/quiz_files/quiz_part2.txt  (5 grammar questions, unnumbered)

Does NOT create:
  - compiled_quiz.odt (that is the agent's task)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

DESKTOP = '/home/user/Desktop'
QUIZ_DIR = f'{DESKTOP}/quiz_files'

PART1_QUESTIONS = [
    "Which sentence uses the correct subject-verb agreement?",
    "Choose the sentence that correctly uses a semicolon.",
    "Identify the sentence with a dangling modifier.",
    "Which of the following sentences is written in the passive voice?",
    "Select the sentence that correctly uses a comma after an introductory clause.",
]

PART2_QUESTIONS = [
    "Which sentence contains a misplaced modifier?",
    "Choose the sentence that correctly uses the apostrophe for possession.",
    "Identify the sentence that contains a parallel structure error.",
    "Which sentence correctly uses 'whom' instead of 'who'?",
    "Select the sentence that avoids a double negative.",
]


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
    # Create quiz_files directory on Desktop
    os.makedirs(QUIZ_DIR, exist_ok=True)
    print(f'Created directory: {QUIZ_DIR}')

    # Write quiz_part1.txt — 5 grammar questions, unnumbered
    part1_path = f'{QUIZ_DIR}/quiz_part1.txt'
    part1_content = '\n'.join(PART1_QUESTIONS) + '\n'
    Path(part1_path).write_text(part1_content)
    print(f'Created: {part1_path}')

    # Write quiz_part2.txt — 5 grammar questions, unnumbered
    part2_path = f'{QUIZ_DIR}/quiz_part2.txt'
    part2_content = '\n'.join(PART2_QUESTIONS) + '\n'
    Path(part2_path).write_text(part2_content)
    print(f'Created: {part2_path}')

    # Ensure compiled_quiz.odt does NOT exist (negative constraint)
    compiled_path = f'{DESKTOP}/compiled_quiz.odt'
    if os.path.exists(compiled_path):
        os.remove(compiled_path)
        print(f'Removed pre-existing: {compiled_path}')

    # GUI-ready startup: open Nautilus file manager showing the Desktop
    # so the agent can see and interact with quiz_files folder
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager at Desktop with DISPLAY=:0')


create_initial()
