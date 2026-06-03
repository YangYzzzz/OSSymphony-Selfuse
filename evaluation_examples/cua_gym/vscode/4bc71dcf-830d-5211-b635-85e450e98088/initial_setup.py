"""
Initial Setup: Configure advanced Go testing project structure
Task ID: vscode_gf6_034
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_034'
PROJECT_DIR = f'{WORKDIR}/projects/go-test-advanced'


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
    os.makedirs(f'{PROJECT_DIR}/internal/handlers', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/internal/models', exist_ok=True)

    # --- go.mod ---
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write("""module github.com/user/go-test-advanced

go 1.21

require (
	net v0.0.0
)
""")

    # --- internal/models/user.go ---
    with open(f'{PROJECT_DIR}/internal/models/user.go', 'w') as f:
        f.write("""package models

// User represents a user in the system.
type User struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	Email     string `json:"email"`
	Role      string `json:"role"`
	Active    bool   `json:"active"`
	CreatedAt string `json:"created_at"`
}
""")

    # --- internal/handlers/users.go ---
    with open(f'{PROJECT_DIR}/internal/handlers/users.go', 'w') as f:
        f.write("""package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"
	"strings"

	"github.com/user/go-test-advanced/internal/models"
)

// In-memory user store for demonstration
var users = []models.User{
	{ID: 1, Name: "Alice Park", Email: "alice@example.com", Role: "admin", Active: true, CreatedAt: "2024-01-15"},
	{ID: 2, Name: "Bob Martinez", Email: "bob@example.com", Role: "user", Active: true, CreatedAt: "2024-02-20"},
	{ID: 3, Name: "Carol Zhang", Email: "carol@example.com", Role: "editor", Active: false, CreatedAt: "2024-03-10"},
}

// ListUsers handles GET /users and returns all users as JSON.
func ListUsers(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(users)
}

// GetUser handles GET /users/{id} and returns a single user by ID.
func GetUser(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Extract ID from URL path
	parts := strings.Split(strings.TrimPrefix(r.URL.Path, "/users/"), "/")
	if len(parts) == 0 || parts[0] == "" {
		http.Error(w, "User ID required", http.StatusBadRequest)
		return
	}

	id, err := strconv.Atoi(parts[0])
	if err != nil {
		http.Error(w, "Invalid user ID", http.StatusBadRequest)
		return
	}

	for _, u := range users {
		if u.ID == id {
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(u)
			return
		}
	}

	http.Error(w, "User not found", http.StatusNotFound)
}
""")

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: go.mod, internal/models/user.go, internal/handlers/users.go')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
