"""
Initial Setup: Convert React class component to functional component with hooks
Task ID: vscode_rrt_046
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_046'
PROJECT_DIR = f'{WORKDIR}/projects/app'
OUTPUT = f'{PROJECT_DIR}/Timer.jsx'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create the React class component file (initial state)
    content = """\
import React, { Component } from 'react';

class Timer extends Component {
    constructor(props) {
        super(props);
        this.state = { seconds: 0, running: false };
    }

    start() {
        this.setState({ running: true });
        this.interval = setInterval(() => {
            this.setState(prev => ({ seconds: prev.seconds + 1 }));
        }, 1000);
    }

    stop() {
        clearInterval(this.interval);
        this.setState({ running: false });
    }

    render() {
        return (
            <div>
                <span>{this.state.seconds}s</span>
                <button onClick={() => this.state.running ? this.stop() : this.start()}>
                    {this.state.running ? 'Stop' : 'Start'}
                </button>
            </div>
        );
    }
}
export default Timer;
"""
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Also create a basic package.json to make it look like a real project
    package_json = """\
{
    "name": "timer-app",
    "version": "1.0.0",
    "description": "A simple timer application",
    "main": "index.js",
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },
    "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build"
    }
}
"""
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(package_json)

    # GUI-ready startup: open VSCode with the Timer.jsx file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
