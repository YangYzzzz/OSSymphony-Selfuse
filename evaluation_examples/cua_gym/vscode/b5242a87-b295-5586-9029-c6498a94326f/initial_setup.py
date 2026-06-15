"""
Initial Setup: Go Linting Project with intentional lint issues
Task ID: vscode_gf6_007
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_007'
PROJECT_DIR = f'{WORKDIR}/projects/go-linting'

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
    os.makedirs(f'{PROJECT_DIR}/internal/api', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/cmd/server', exist_ok=True)

    # --- go.mod ---
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write("""module github.com/user/go-linting

go 1.21

require (
	github.com/gorilla/mux v1.8.1
)
""")

    # --- go.sum (minimal, realistic) ---
    with open(f'{PROJECT_DIR}/go.sum', 'w') as f:
        f.write("""github.com/gorilla/mux v1.8.1 h1:TuMoUvkRETdXqXClP7nGo15cgOq1dEhsFHXJaguJK/o=
github.com/gorilla/mux v1.8.1/go.mod h1:AKf9I4AEqPTmMytcMc0KkNouC66V3BtZ4qD5fmWSiMQ=
""")

    # --- internal/api/handler.go (WITH 3 intentional lint issues) ---
    with open(f'{PROJECT_DIR}/internal/api/handler.go', 'w') as f:
        f.write('''package api

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// Response represents a standard API response
type Response struct {
	Status  string      `json:"status"`
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
}

// HealthHandler returns the health status of the service
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	resp := Response{
		Status:  "ok",
		Message: "Service is healthy",
	}
	w.Header().Set("Content-Type", "application/json")
	// LINT ISSUE 1: unchecked error return from Encode
	json.NewEncoder(w).Encode(resp)
}

// GetUserHandler retrieves user information by ID
func GetUserHandler(w http.ResponseWriter, r *http.Request) {
	userID := r.URL.Query().Get("id")
	if userID == "" {
		http.Error(w, "missing user id", http.StatusBadRequest)
		return
	}

	// LINT ISSUE 2: inefficient - fetches data then discards it, uses hardcoded values instead
	result := fetchUserFromDB(userID)
	_ = result

	userData := map[string]string{
		"id":    userID,
		"name":  "Alice Martinez",
		"email": "alice.martinez@example.com",
		"role":  "engineer",
	}

	// LINT ISSUE 3: fmt.Println instead of proper logging
	fmt.Println("Fetched user data for ID:", userID)

	resp := Response{
		Status:  "ok",
		Message: "User retrieved successfully",
		Data:    userData,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// CreateUserHandler handles user creation requests
func CreateUserHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var input struct {
		Name  string `json:"name"`
		Email string `json:"email"`
		Role  string `json:"role"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}

	resp := Response{
		Status:  "ok",
		Message: "User created successfully",
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// fetchUserFromDB simulates a database lookup
func fetchUserFromDB(id string) map[string]string {
	return map[string]string{
		"id":   id,
		"name": "Alice Martinez",
	}
}
''')

    # --- cmd/server/main.go ---
    with open(f'{PROJECT_DIR}/cmd/server/main.go', 'w') as f:
        f.write('''package main

import (
	"log"
	"net/http"

	"github.com/user/go-linting/internal/api"
)

func main() {
	http.HandleFunc("/health", api.HealthHandler)
	http.HandleFunc("/user", api.GetUserHandler)
	http.HandleFunc("/user/create", api.CreateUserHandler)

	log.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
''')

    # --- Makefile (with build and test targets, NO lint target) ---
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write("""APP_NAME := go-linting
BUILD_DIR := ./bin

.PHONY: build test clean

build:
\tgo build -o $(BUILD_DIR)/$(APP_NAME) ./cmd/server/

test:
\tgo test -v ./...

clean:
\trm -rf $(BUILD_DIR)
""")

    # --- .vscode/settings.json (basic Go settings, NO tasks.json) ---
    os.makedirs(f'{PROJECT_DIR}/.vscode', exist_ok=True)
    with open(f'{PROJECT_DIR}/.vscode/settings.json', 'w') as f:
        f.write("""{
    "go.useLanguageServer": true,
    "editor.formatOnSave": true,
    "go.lintOnSave": "workspace"
}
""")

    print(f'Initial project created: {PROJECT_DIR}')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
