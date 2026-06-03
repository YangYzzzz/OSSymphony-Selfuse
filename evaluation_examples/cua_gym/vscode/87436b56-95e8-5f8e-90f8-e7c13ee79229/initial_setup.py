"""
initial_setup.py - Create empty typescript-app directory and open VSCode with it.
Runs on the initial VM.
"""
import os
import subprocess
import shlex
import time

HOME = os.path.expanduser("~")
PROJECT_DIR = os.path.join(HOME, "projects", "typescript-app")

# 1. Create the empty project directory
os.makedirs(PROJECT_DIR, exist_ok=True)

# 2. Launch VSCode with the project folder
env = os.environ.copy()
env["DISPLAY"] = ":0"
subprocess.Popen(
    shlex.split(f'code "{PROJECT_DIR}"'),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    env=env,
)
time.sleep(3)

print(f"[OK] Created {PROJECT_DIR} and launched VSCode")
