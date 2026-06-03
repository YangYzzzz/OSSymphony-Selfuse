"""
Initial Setup: Create Go K8s Deploy project with Go source and Dockerfile
Task ID: vscode_gf6_087
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_087'
PROJECT_DIR = f'{WORKDIR}/projects/go-k8s-deploy'

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

    # --- main.go ---
    main_go = '''\
package main

import (
\t"encoding/json"
\t"fmt"
\t"log"
\t"net/http"
\t"os"
\t"time"
)

type HealthResponse struct {
\tStatus    string `json:"status"`
\tTimestamp string `json:"timestamp"`
}

type APIResponse struct {
\tMessage string `json:"message"`
\tVersion string `json:"version"`
}

var startTime time.Time

func init() {
\tstartTime = time.Now()
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
\tw.Header().Set("Content-Type", "application/json")
\tresp := HealthResponse{
\t\tStatus:    "healthy",
\t\tTimestamp: time.Now().UTC().Format(time.RFC3339),
\t}
\tjson.NewEncoder(w).Encode(resp)
}

func readyHandler(w http.ResponseWriter, r *http.Request) {
\tw.Header().Set("Content-Type", "application/json")
\t// Ready after startup initialization
\tif time.Since(startTime) < 2*time.Second {
\t\tw.WriteHeader(http.StatusServiceUnavailable)
\t\tjson.NewEncoder(w).Encode(map[string]string{"status": "not_ready"})
\t\treturn
\t}
\tjson.NewEncoder(w).Encode(map[string]string{"status": "ready"})
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
\tw.Header().Set("Content-Type", "application/json")
\tresp := APIResponse{
\t\tMessage: "Go K8s Deploy API",
\t\tVersion: "1.0.0",
\t}
\tjson.NewEncoder(w).Encode(resp)
}

func main() {
\tport := os.Getenv("APP_PORT")
\tif port == "" {
\t\tport = "8080"
\t}

\thttp.HandleFunc("/", rootHandler)
\thttp.HandleFunc("/health", healthHandler)
\thttp.HandleFunc("/ready", readyHandler)

\tlog.Printf("Starting server on port %s", port)
\tif err := http.ListenAndServe(fmt.Sprintf(":%s", port), nil); err != nil {
\t\tlog.Fatalf("Server failed to start: %v", err)
\t}
}
'''
    with open(f'{PROJECT_DIR}/main.go', 'w') as f:
        f.write(main_go)

    # --- go.mod ---
    go_mod = '''\
module github.com/acmecorp/go-k8s-deploy

go 1.21
'''
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod)

    # --- Dockerfile ---
    dockerfile = '''\
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /go-k8s-deploy .

FROM alpine:3.19
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go-k8s-deploy .
EXPOSE 8080
CMD ["./go-k8s-deploy"]
'''
    with open(f'{PROJECT_DIR}/Dockerfile', 'w') as f:
        f.write(dockerfile)

    # --- Makefile (NO k8s targets - task asks agent to add them) ---
    makefile = '''\
.PHONY: build run test clean docker-build docker-run

APP_NAME := go-k8s-deploy
DOCKER_IMAGE := $(APP_NAME):latest

build:
\tgo build -o bin/$(APP_NAME) .

run: build
\t./bin/$(APP_NAME)

test:
\tgo test -v ./...

clean:
\trm -rf bin/

docker-build:
\tdocker build -t $(DOCKER_IMAGE) .

docker-run: docker-build
\tdocker run -p 8080:8080 $(DOCKER_IMAGE)
'''
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write(makefile)

    # --- .gitignore ---
    gitignore = '''\
bin/
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
.env
'''
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = '''\
# Go K8s Deploy

A lightweight Go REST API designed for Kubernetes deployment.

## Endpoints

- `GET /` - API info
- `GET /health` - Health check endpoint
- `GET /ready` - Readiness probe endpoint

## Development

```bash
make build    # Build the binary
make run      # Build and run locally
make test     # Run tests
make clean    # Clean build artifacts
```

## Docker

```bash
make docker-build   # Build Docker image
make docker-run     # Run in Docker container
```
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: main.go, go.mod, Dockerfile, Makefile, .gitignore, README.md')

    # Verify no k8s directory exists (negative constraint)
    assert not os.path.exists(f'{PROJECT_DIR}/k8s'), 'k8s/ should not exist in initial state'
    assert not os.path.exists(f'{PROJECT_DIR}/.vscode/tasks.json'), '.vscode/tasks.json should not exist'

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
