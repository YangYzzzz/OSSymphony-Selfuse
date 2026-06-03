"""
Initial Setup: Create Go API project structure for VSCode debugging task
Task ID: vscode_td_065
Domain: vs_code

Creates ~/projects/go-api with cmd/server/main.go and supporting files.
NO .vscode/launch.json — the agent must create that.
Opens VSCode with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-api')
CMD_DIR = os.path.join(PROJECT_DIR, 'cmd', 'server')


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
    os.makedirs(CMD_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'internal', 'handlers'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'internal', 'models'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'pkg', 'config'), exist_ok=True)

    # go.mod
    with open(os.path.join(PROJECT_DIR, 'go.mod'), 'w') as f:
        f.write("""module github.com/acmecorp/go-api

go 1.21

require (
\tgithub.com/gorilla/mux v1.8.1
\tgithub.com/lib/pq v1.10.9
\tgithub.com/joho/godotenv v1.5.1
)
""")

    # cmd/server/main.go
    with open(os.path.join(CMD_DIR, 'main.go'), 'w') as f:
        f.write("""package main

import (
\t"fmt"
\t"log"
\t"net/http"
\t"os"

\t"github.com/acmecorp/go-api/internal/handlers"
\t"github.com/acmecorp/go-api/pkg/config"
\t"github.com/gorilla/mux"
)

func main() {
\tcfg, err := config.Load()
\tif err != nil {
\t\tlog.Fatalf("Failed to load configuration: %v", err)
\t}

\trouter := mux.NewRouter()
\tapiRouter := router.PathPrefix("/api/v1").Subrouter()

\tuserHandler := handlers.NewUserHandler(cfg.DatabaseURL)
\tapiRouter.HandleFunc("/users", userHandler.ListUsers).Methods("GET")
\tapiRouter.HandleFunc("/users/{id}", userHandler.GetUser).Methods("GET")
\tapiRouter.HandleFunc("/users", userHandler.CreateUser).Methods("POST")
\tapiRouter.HandleFunc("/users/{id}", userHandler.UpdateUser).Methods("PUT")
\tapiRouter.HandleFunc("/users/{id}", userHandler.DeleteUser).Methods("DELETE")

\tport := os.Getenv("PORT")
\tif port == "" {
\t\tport = cfg.Port
\t}

\taddr := fmt.Sprintf(":%s", port)
\tlog.Printf("Starting server on %s", addr)
\tif err := http.ListenAndServe(addr, router); err != nil {
\t\tlog.Fatalf("Server failed: %v", err)
\t}
}
""")

    # internal/handlers/user.go
    with open(os.path.join(PROJECT_DIR, 'internal', 'handlers', 'user.go'), 'w') as f:
        f.write("""package handlers

import (
\t"encoding/json"
\t"net/http"

\t"github.com/acmecorp/go-api/internal/models"
\t"github.com/gorilla/mux"
)

type UserHandler struct {
\tdbURL string
}

func NewUserHandler(dbURL string) *UserHandler {
\treturn &UserHandler{dbURL: dbURL}
}

func (h *UserHandler) ListUsers(w http.ResponseWriter, r *http.Request) {
\tusers := []models.User{
\t\t{ID: "1", Name: "Sarah Chen", Email: "sarah.chen@acmecorp.com", Role: "engineer"},
\t\t{ID: "2", Name: "Marcus Johnson", Email: "marcus.j@acmecorp.com", Role: "designer"},
\t}
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(users)
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tuser := models.User{ID: vars["id"], Name: "Sarah Chen", Email: "sarah.chen@acmecorp.com", Role: "engineer"}
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(user)
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
\tw.WriteHeader(http.StatusCreated)
}

func (h *UserHandler) UpdateUser(w http.ResponseWriter, r *http.Request) {
\tw.WriteHeader(http.StatusOK)
}

func (h *UserHandler) DeleteUser(w http.ResponseWriter, r *http.Request) {
\tw.WriteHeader(http.StatusNoContent)
}
""")

    # internal/models/user.go
    with open(os.path.join(PROJECT_DIR, 'internal', 'models', 'user.go'), 'w') as f:
        f.write("""package models

type User struct {
\tID    string `json:"id"`
\tName  string `json:"name"`
\tEmail string `json:"email"`
\tRole  string `json:"role"`
}
""")

    # pkg/config/config.go
    with open(os.path.join(PROJECT_DIR, 'pkg', 'config', 'config.go'), 'w') as f:
        f.write("""package config

import (
\t"os"

\t"github.com/joho/godotenv"
)

type Config struct {
\tPort        string
\tDatabaseURL string
\tEnvironment string
}

func Load() (*Config, error) {
\t_ = godotenv.Load()

\tcfg := &Config{
\t\tPort:        getEnv("PORT", "8080"),
\t\tDatabaseURL: getEnv("DATABASE_URL", "postgres://localhost:5432/goapi?sslmode=disable"),
\t\tEnvironment: getEnv("ENVIRONMENT", "development"),
\t}
\treturn cfg, nil
}

func getEnv(key, fallback string) string {
\tif value, ok := os.LookupEnv(key); ok {
\t\treturn value
\t}
\treturn fallback
}
""")

    # .env file
    with open(os.path.join(PROJECT_DIR, '.env'), 'w') as f:
        f.write("""PORT=8080
DATABASE_URL=postgres://localhost:5432/goapi?sslmode=disable
ENVIRONMENT=development
""")

    # README.md
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write("""# Go API Server

A REST API server built with Go and Gorilla Mux.

## Project Structure

```
go-api/
  cmd/server/        - Application entry point
  internal/handlers/ - HTTP request handlers
  internal/models/   - Data models
  pkg/config/        - Configuration loading
```

## Running

```bash
go run cmd/server/main.go
```

The server starts on port 8080 by default.
""")

    # Ensure NO .vscode/launch.json exists (the task requires the agent to create it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json):
        os.remove(launch_json)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Main file: {os.path.join(CMD_DIR, "main.go")}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
