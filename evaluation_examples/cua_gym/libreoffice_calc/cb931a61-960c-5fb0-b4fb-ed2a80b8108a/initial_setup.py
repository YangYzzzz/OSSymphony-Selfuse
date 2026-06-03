"""
Initial Setup: Configure shell to auto-activate Python venv
Task ID: osworld_multi_apps_cli_path_fix_006
Domain: os (shell configuration)

Creates the initial state:
  - Virtual environment exists at /opt/venvs/datascience
  - ~/.bashrc does NOT contain the activation line
  - Terminal is open
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_006'
VENV_PATH = '/opt/venvs/datascience'
BASHRC_PATH = os.path.join(WORKDIR, '.bashrc')
ACTIVATION_LINE = 'source /opt/venvs/datascience/bin/activate'


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
    # Step 1: Create the virtual environment at /opt/venvs/datascience if not present
    # Use sudo with password to create /opt/venvs if needed (system directory)
    if not os.path.isdir('/opt/venvs'):
        subprocess.run(
            'echo "password" | sudo -S mkdir -p /opt/venvs',
            shell=True, check=True
        )
        subprocess.run(
            'echo "password" | sudo -S chmod 777 /opt/venvs',
            shell=True, check=True
        )
    if not os.path.isdir(VENV_PATH):
        print(f'Creating virtual environment at {VENV_PATH}...')
        subprocess.run(
            ['python3', '-m', 'venv', '--without-pip', VENV_PATH],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f'Virtual environment created: {VENV_PATH}')
    else:
        print(f'Virtual environment already exists: {VENV_PATH}')

    # Verify the activate script exists
    activate_script = os.path.join(VENV_PATH, 'bin', 'activate')
    if os.path.isfile(activate_script):
        print(f'Activation script confirmed: {activate_script}')
    else:
        raise RuntimeError(f'Activation script not found: {activate_script}')

    # Step 2: Ensure ~/.bashrc exists but does NOT contain the activation line
    # Read existing bashrc content
    if os.path.isfile(BASHRC_PATH):
        with open(BASHRC_PATH, 'r') as f:
            content = f.read()
    else:
        # Create a basic .bashrc if it doesn't exist
        content = (
            '# ~/.bashrc: executed by bash(1) for non-login shells.\n\n'
            '# If not running interactively, do nothing\n'
            'case $- in\n'
            '    *i*) ;;\n'
            '      *) return;;\n'
            'esac\n\n'
            '# History settings\n'
            'HISTCONTROL=ignoreboth\n'
            'HISTSIZE=1000\n'
            'HISTFILESIZE=2000\n\n'
            '# Append to history, do not overwrite\n'
            'shopt -s histappend\n\n'
            '# Set a basic prompt\n'
            'PS1="${debian_chroot:+($debian_chroot)}\\u@\\h:\\w\\$ "\n\n'
            '# Color support\n'
            "if [ -x /usr/bin/dircolors ]; then\n"
            '    eval "$(dircolors -b)"\n'
            '    alias ls=\'ls --color=auto\'\n'
            '    alias grep=\'grep --color=auto\'\n'
            'fi\n\n'
            '# Alias definitions\n'
            'alias ll=\'ls -alF\'\n'
            'alias la=\'ls -A\'\n'
            'alias l=\'ls -CF\'\n\n'
            '# Enable programmable completion\n'
            'if ! shopt -oq posix; then\n'
            '  if [ -f /usr/share/bash-completion/bash_completion ]; then\n'
            '    . /usr/share/bash-completion/bash_completion\n'
            '  elif [ -f /etc/bash_completion ]; then\n'
            '    . /etc/bash_completion\n'
            '  fi\n'
            'fi\n'
        )

    # Remove any existing activation line variants to ensure clean state
    lines = content.splitlines(keepends=True)
    cleaned_lines = [
        line for line in lines
        if ACTIVATION_LINE not in line
        and '/opt/venvs/datascience' not in line
    ]
    cleaned_content = ''.join(cleaned_lines)

    with open(BASHRC_PATH, 'w') as f:
        f.write(cleaned_content)
    print(f'~/.bashrc is set — does NOT contain venv activation line.')

    # Step 3: Open a terminal so the agent can see the shell
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched gnome-terminal with DISPLAY=:0')


create_initial()
