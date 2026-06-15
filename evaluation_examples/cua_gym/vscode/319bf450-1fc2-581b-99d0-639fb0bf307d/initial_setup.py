"""
Initial Setup: Go Swagger API documentation project
Task ID: vscode_gf6_084
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_084'
PROJECT_DIR = f'{WORKDIR}/projects/go-swagger'
GO_VERSION = '1.21.13'


def run_cmd(cmd, timeout=120):
    """Run a shell command and print output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print(f"STDERR: {result.stderr.strip()}")
    return result


def install_go():
    """Install Go 1.21 to user's home directory."""
    go_root = f"{WORKDIR}/go-sdk"
    go_bin = f"{go_root}/bin/go"

    check = subprocess.run(f"{go_bin} version", shell=True, capture_output=True, text=True)
    if check.returncode == 0 and "go1.21" in check.stdout:
        print(f"Go already installed: {check.stdout.strip()}")
        os.environ["PATH"] = f"{go_root}/bin:{WORKDIR}/go/bin:" + os.environ.get("PATH", "")
        os.environ["GOPATH"] = f"{WORKDIR}/go"
        os.environ["GOROOT"] = go_root
        return

    print(f"Installing Go {GO_VERSION} to {go_root}...")
    run_cmd(f"wget -q https://go.dev/dl/go{GO_VERSION}.linux-amd64.tar.gz -O /tmp/go.tar.gz", timeout=180)
    run_cmd(f"rm -rf {go_root} && mkdir -p {go_root} && tar -C {WORKDIR} -xzf /tmp/go.tar.gz && mv {WORKDIR}/go {go_root} 2>/dev/null; true")
    # If tar extracted to go/ directly, it may already be go-sdk content — check
    if not os.path.exists(go_bin):
        # tar extracts to 'go' folder; rename
        run_cmd(f"rm -rf {go_root} && tar -C /tmp -xzf /tmp/go.tar.gz && mv /tmp/go {go_root}")
    run_cmd("rm -f /tmp/go.tar.gz")

    # Set env for current session
    os.environ["PATH"] = f"{go_root}/bin:{WORKDIR}/go/bin:" + os.environ.get("PATH", "")
    os.environ["GOPATH"] = f"{WORKDIR}/go"
    os.environ["GOROOT"] = go_root

    # Persist PATH for user
    bashrc = f"{WORKDIR}/.bashrc"
    path_lines = f'\nexport GOROOT={go_root}\nexport GOPATH=$HOME/go\nexport PATH=$GOROOT/bin:$GOPATH/bin:$PATH\n'
    with open(bashrc, 'a') as f:
        f.write(path_lines)

    verify = run_cmd(f"{go_bin} version")
    print(f"Go installed: {verify.stdout.strip()}")


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
    # Install Go first
    install_go()
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/cmd/server', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/internal/handlers', exist_ok=True)

    # --- go.mod ---
    go_mod = """module github.com/user/go-swagger

go 1.21

require (
\tgithub.com/gorilla/mux v1.8.1
)

require github.com/felixge/httpsnoop v1.0.4 // indirect
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod)

    # --- go.sum (minimal, for gorilla/mux) ---
    go_sum = """github.com/felixge/httpsnoop v1.0.4 h1:NFTV2Zj1bL4mc9sqWACXbQFVBBg2W3GPvqp8/ESS2Wg=
github.com/felixge/httpsnoop v1.0.4/go.mod h1:m8KPJKqk1gH5J9DgRY2ASl2lWCfGKXixSwevea8zH2U=
github.com/gorilla/mux v1.8.1 h1:TuMoUvkRETdXqYzB1b7+FJFi4wnSEVLsVChQPGPuuC0=
github.com/gorilla/mux v1.8.1/go.mod h1:AKf9I4AEqPTmMytcMc0KkNouC66V3BtZ4qD5fmWSiMQ=
"""
    with open(f'{PROJECT_DIR}/go.sum', 'w') as f:
        f.write(go_sum)

    # --- cmd/server/main.go (standard net/http server, NO swagger annotations) ---
    main_go = '''package main

import (
\t"fmt"
\t"log"
\t"net/http"

\t"github.com/gorilla/mux"
\t"github.com/user/go-swagger/internal/handlers"
)

func main() {
\tr := mux.NewRouter()

\t// API routes
\tapi := r.PathPrefix("/api/v1").Subrouter()
\tapi.HandleFunc("/users", handlers.ListUsers).Methods("GET")
\tapi.HandleFunc("/users", handlers.CreateUser).Methods("POST")
\tapi.HandleFunc("/users/{id}", handlers.GetUser).Methods("GET")
\tapi.HandleFunc("/users/{id}", handlers.UpdateUser).Methods("PUT")
\tapi.HandleFunc("/users/{id}", handlers.DeleteUser).Methods("DELETE")

\tfmt.Println("Server starting on :8080")
\tlog.Fatal(http.ListenAndServe(":8080", r))
}
'''
    with open(f'{PROJECT_DIR}/cmd/server/main.go', 'w') as f:
        f.write(main_go)

    # --- internal/handlers/users.go (5 handler functions, NO swagger annotations) ---
    users_go = '''package handlers

import (
\t"encoding/json"
\t"net/http"
\t"strconv"
\t"sync"

\t"github.com/gorilla/mux"
)

// User represents a user in the system
type User struct {
\tID        int    `json:"id"`
\tFirstName string `json:"first_name"`
\tLastName  string `json:"last_name"`
\tEmail     string `json:"email"`
\tRole      string `json:"role"`
\tActive    bool   `json:"active"`
}

// ErrorResponse represents an error response
type ErrorResponse struct {
\tCode    int    `json:"code"`
\tMessage string `json:"message"`
}

var (
\tmu    sync.RWMutex
\tusers = map[int]*User{
\t\t1: {ID: 1, FirstName: "Sarah", LastName: "Chen", Email: "sarah.chen@example.com", Role: "admin", Active: true},
\t\t2: {ID: 2, FirstName: "Marcus", LastName: "Johnson", Email: "marcus.j@example.com", Role: "developer", Active: true},
\t\t3: {ID: 3, FirstName: "Priya", LastName: "Patel", Email: "priya.p@example.com", Role: "designer", Active: true},
\t}
\tnextID = 4
)

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
\tw.Header().Set("Content-Type", "application/json")
\tw.WriteHeader(status)
\tjson.NewEncoder(w).Encode(data)
}

func respondError(w http.ResponseWriter, status int, message string) {
\trespondJSON(w, status, ErrorResponse{Code: status, Message: message})
}

// ListUsers returns all users
func ListUsers(w http.ResponseWriter, r *http.Request) {
\tmu.RLock()
\tdefer mu.RUnlock()

\tuserList := make([]*User, 0, len(users))
\tfor _, u := range users {
\t\tuserList = append(userList, u)
\t}
\trespondJSON(w, http.StatusOK, userList)
}

// CreateUser creates a new user
func CreateUser(w http.ResponseWriter, r *http.Request) {
\tvar u User
\tif err := json.NewDecoder(r.Body).Decode(&u); err != nil {
\t\trespondError(w, http.StatusBadRequest, "Invalid request body")
\t\treturn
\t}

\tmu.Lock()
\tu.ID = nextID
\tnextID++
\tusers[u.ID] = &u
\tmu.Unlock()

\trespondJSON(w, http.StatusCreated, u)
}

// GetUser returns a user by ID
func GetUser(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tid, err := strconv.Atoi(vars["id"])
\tif err != nil {
\t\trespondError(w, http.StatusBadRequest, "Invalid user ID")
\t\treturn
\t}

\tmu.RLock()
\tu, ok := users[id]
\tmu.RUnlock()

\tif !ok {
\t\trespondError(w, http.StatusNotFound, "User not found")
\t\treturn
\t}
\trespondJSON(w, http.StatusOK, u)
}

// UpdateUser updates an existing user
func UpdateUser(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tid, err := strconv.Atoi(vars["id"])
\tif err != nil {
\t\trespondError(w, http.StatusBadRequest, "Invalid user ID")
\t\treturn
\t}

\tmu.Lock()
\tdefer mu.Unlock()

\texisting, ok := users[id]
\tif !ok {
\t\trespondError(w, http.StatusNotFound, "User not found")
\t\treturn
\t}

\tvar updated User
\tif err := json.NewDecoder(r.Body).Decode(&updated); err != nil {
\t\trespondError(w, http.StatusBadRequest, "Invalid request body")
\t\treturn
\t}

\tupdated.ID = existing.ID
\tusers[id] = &updated
\trespondJSON(w, http.StatusOK, updated)
}

// DeleteUser removes a user by ID
func DeleteUser(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tid, err := strconv.Atoi(vars["id"])
\tif err != nil {
\t\trespondError(w, http.StatusBadRequest, "Invalid user ID")
\t\treturn
\t}

\tmu.Lock()
\tdefer mu.Unlock()

\tif _, ok := users[id]; !ok {
\t\trespondError(w, http.StatusNotFound, "User not found")
\t\treturn
\t}

\tdelete(users, id)
\tw.WriteHeader(http.StatusNoContent)
}
'''
    with open(f'{PROJECT_DIR}/internal/handlers/users.go', 'w') as f:
        f.write(users_go)

    # --- Makefile (basic, NO docs target) ---
    makefile = """APP_NAME=go-swagger
BUILD_DIR=bin

.PHONY: build run clean test

build:
\tgo build -o $(BUILD_DIR)/$(APP_NAME) ./cmd/server

run:
\tgo run ./cmd/server

clean:
\trm -rf $(BUILD_DIR)

test:
\tgo test ./...
"""
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write(makefile)

    # --- .gitignore ---
    gitignore = """bin/
*.exe
*.out
vendor/
.env
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = """# Go Swagger API

A REST API for user management built with Go and gorilla/mux.

## Endpoints

- `GET /api/v1/users` - List all users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Running

```bash
make run
```
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
