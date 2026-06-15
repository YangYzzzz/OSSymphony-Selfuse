"""
Initial Setup: Create a Go project workspace with VSCode launch.json and tasks.json
Task ID: vscode_lang_025
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_025'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'mygoapp')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')


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
    os.makedirs(VSCODE_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'bin'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'cmd'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'internal', 'handler'), exist_ok=True)

    # Create main.go
    main_go = os.path.join(PROJECT_DIR, 'main.go')
    with open(main_go, 'w') as f:
        f.write('''package main

import (
\t"fmt"
\t"net/http"

\t"mygoapp/internal/handler"
)

func main() {
\tfmt.Println("Starting MyGoApp server on :8080")

\thttp.HandleFunc("/", handler.HomeHandler)
\thttp.HandleFunc("/api/status", handler.StatusHandler)
\thttp.HandleFunc("/api/health", handler.HealthHandler)

\tif err := http.ListenAndServe(":8080", nil); err != nil {
\t\tfmt.Printf("Server failed to start: %v\\n", err)
\t}
}
''')

    # Create internal/handler/handler.go
    handler_go = os.path.join(PROJECT_DIR, 'internal', 'handler', 'handler.go')
    with open(handler_go, 'w') as f:
        f.write('''package handler

import (
\t"encoding/json"
\t"fmt"
\t"net/http"
\t"time"
)

type StatusResponse struct {
\tStatus    string `json:"status"`
\tTimestamp string `json:"timestamp"`
\tVersion   string `json:"version"`
}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
\tfmt.Fprintf(w, "Welcome to MyGoApp - A lightweight Go web service")
}

func StatusHandler(w http.ResponseWriter, r *http.Request) {
\tresp := StatusResponse{
\t\tStatus:    "running",
\t\tTimestamp: time.Now().Format(time.RFC3339),
\t\tVersion:   "1.2.0",
\t}
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(resp)
}

func HealthHandler(w http.ResponseWriter, r *http.Request) {
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(map[string]string{"health": "ok"})
}
''')

    # Create go.mod
    go_mod = os.path.join(PROJECT_DIR, 'go.mod')
    with open(go_mod, 'w') as f:
        f.write('''module mygoapp

go 1.21
''')

    # Create .vscode/launch.json - with Launch Package config, NO compounds
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Launch Package",
                "type": "go",
                "request": "launch",
                "mode": "auto",
                "program": "${workspaceFolder}"
            }
        ]
    }
    with open(os.path.join(VSCODE_DIR, 'launch.json'), 'w') as f:
        json.dump(launch_json, f, indent=4)

    # Create .vscode/tasks.json - with Go Build task
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Go Build",
                "type": "shell",
                "command": "go",
                "args": [
                    "build",
                    "-o",
                    "${workspaceFolder}/bin/myapp",
                    "${workspaceFolder}/main.go"
                ],
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "problemMatcher": ["$go"]
            }
        ]
    }
    with open(os.path.join(VSCODE_DIR, 'tasks.json'), 'w') as f:
        json.dump(tasks_json, f, indent=4)

    # Create a simple README
    readme = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme, 'w') as f:
        f.write('''# MyGoApp

A lightweight Go web service with status and health endpoints.

## Build

```bash
go build -o bin/myapp main.go
```

## Run

```bash
./bin/myapp
```

## Endpoints

- `/` - Home page
- `/api/status` - Service status with version info
- `/api/health` - Health check endpoint
''')

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'launch.json: {os.path.join(VSCODE_DIR, "launch.json")}')
    print(f'tasks.json: {os.path.join(VSCODE_DIR, "tasks.json")}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
