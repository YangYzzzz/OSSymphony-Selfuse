"""
Initial Setup: Docker development environment for Go web service
Task ID: vscode_gf6_044
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_044'
PROJECT_DIR = f'{WORKDIR}/projects/go-docker-dev'

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
    os.makedirs(f'{PROJECT_DIR}/cmd/server', exist_ok=True)

    # --- go.mod ---
    go_mod_content = """module github.com/user/go-docker-dev

go 1.21
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod_content)

    # --- cmd/server/main.go ---
    main_go_content = '''package main

import (
\t"fmt"
\t"log"
\t"net/http"
\t"os"
\t"time"
)

func main() {
\tport := os.Getenv("PORT")
\tif port == "" {
\t\tport = "8080"
\t}

\tmux := http.NewServeMux()

\tmux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
\t\tfmt.Fprintf(w, "Hello from go-docker-dev! Server time: %s", time.Now().Format(time.RFC3339))
\t})

\tmux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
\t\tw.WriteHeader(http.StatusOK)
\t\tfmt.Fprintln(w, "ok")
\t})

\tlog.Printf("Starting server on port %s", port)
\tif err := http.ListenAndServe(":"+port, mux); err != nil {
\t\tlog.Fatalf("Server failed to start: %v", err)
\t}
}
'''
    with open(f'{PROJECT_DIR}/cmd/server/main.go', 'w') as f:
        f.write(main_go_content)

    # --- Makefile (only 'build' target) ---
    makefile_content = """.PHONY: build

build:
\tgo build -o bin/server ./cmd/server
"""
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write(makefile_content)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Files: go.mod, cmd/server/main.go, Makefile')

    # GUI-ready startup: open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
