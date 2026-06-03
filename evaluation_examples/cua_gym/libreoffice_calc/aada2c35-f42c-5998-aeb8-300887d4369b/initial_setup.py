"""
Initial Setup: Open VSCode with a Jupyter notebook containing two cells
Task ID: vscode_prod_009
Domain: libreoffice_calc (VSCode + Jupyter)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_009'
PROJECT_DIR = f'{WORKDIR}/projects/data-science'
OUTPUT = f'{PROJECT_DIR}/analysis.ipynb'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Build the Jupyter notebook with 2 cells:
    # Cell 1: Markdown title
    # Cell 2: Code cell importing pandas and numpy (already executed)
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Data Science Analysis\n",
                    "\n",
                    "Exploratory data analysis for Q1 2025 performance metrics."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbformat_minor": 0,
                "pygments_lexer": "ipython3",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(OUTPUT, 'w') as f:
        json.dump(notebook, f, indent=1)

    print(f'Initial file created: {OUTPUT}')

    # Launch VSCode with the project directory and open the notebook
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
