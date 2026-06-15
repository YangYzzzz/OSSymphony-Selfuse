"""
Initial Setup: Set up environment for Stable Baselines3 installation task
Task ID: osworld_multi_apps_vscode_env_setup_009
Domain: multi_apps (vscode + terminal)

This script sets up the initial state:
- Chrome open for reference
- A terminal window open
- /home/user/sb3 does NOT exist
- stable-baselines3, gymnasium, torch NOT installed (clean env)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_009'


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
    # Ensure /home/user/sb3 does NOT exist (clean state)
    sb3_dir = os.path.join(WORKDIR, 'sb3')
    if os.path.exists(sb3_dir):
        import shutil
        shutil.rmtree(sb3_dir)
        print(f'Removed existing {sb3_dir} to ensure clean state')

    # Create a README file on the desktop to guide the agent
    readme_path = os.path.join(WORKDIR, 'Desktop', 'task_instructions.txt')
    os.makedirs(os.path.join(WORKDIR, 'Desktop'), exist_ok=True)
    with open(readme_path, 'w') as f:
        f.write(
            "Task: Set up Stable Baselines3 RL Library\n"
            "==========================================\n\n"
            "1. Clone the repository:\n"
            "   git clone https://github.com/DLR-RM/stable-baselines3 /home/user/sb3\n\n"
            "2. Install the package and dependencies:\n"
            "   pip install -e /home/user/sb3[extra]\n"
            "   pip install gymnasium torch\n\n"
            "3. Verify installation:\n"
            "   python -c \"from stable_baselines3 import PPO; print(PPO)\"\n"
        )
    print(f'Created task instructions at {readme_path}')

    # Open Chrome for reference
    launch_gui('google-chrome --new-window "https://github.com/DLR-RM/stable-baselines3"', delay_sec=2.0)
    print('GUI_READY: launched Chrome with stable-baselines3 GitHub page')

    # Open a terminal window
    launch_gui('gnome-terminal --working-directory=/home/user', delay_sec=1.5)
    print('GUI_READY: launched terminal at /home/user')


create_initial()
