"""
Initial Setup: Create Go workspace with build-tagged main.go, no launch.json
Task ID: vscode_td_081
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_081'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-service')
CMD_APP_DIR = os.path.join(PROJECT_DIR, 'cmd', 'app')
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
    os.makedirs(CMD_APP_DIR, exist_ok=True)

    # Create go.mod
    go_mod_content = """module github.com/acme-corp/go-service

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	github.com/stretchr/testify v1.8.4
	go.uber.org/zap v1.26.0
)
"""
    with open(os.path.join(PROJECT_DIR, 'go.mod'), 'w') as f:
        f.write(go_mod_content)

    # Create cmd/app/main.go with build tag constraints
    main_go_content = """//go:build integration

package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

const (
	defaultPort = "8080"
	serviceName = "go-service"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/health", healthHandler)
	mux.HandleFunc("/api/v1/status", statusHandler)

	addr := fmt.Sprintf(":%s", port)
	log.Printf("[%s] Starting server on %s", serviceName, addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"status":"healthy","service":"%s"}`, serviceName)
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"service":"%s","version":"1.4.2","environment":"production"}`, serviceName)
}
"""
    with open(os.path.join(CMD_APP_DIR, 'main.go'), 'w') as f:
        f.write(main_go_content)

    # Create an internal package for realism
    internal_dir = os.path.join(PROJECT_DIR, 'internal', 'config')
    os.makedirs(internal_dir, exist_ok=True)

    config_go_content = """package config

import "os"

type Config struct {
	Port        string
	DatabaseURL string
	LogLevel    string
	Environment string
}

func Load() *Config {
	return &Config{
		Port:        getEnv("PORT", "8080"),
		DatabaseURL: getEnv("DATABASE_URL", "postgres://localhost:5432/goservice"),
		LogLevel:    getEnv("LOG_LEVEL", "info"),
		Environment: getEnv("ENVIRONMENT", "development"),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
"""
    with open(os.path.join(internal_dir, 'config.go'), 'w') as f:
        f.write(config_go_content)

    # Create a test file
    main_test_content = """//go:build integration

package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHealthHandler(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()
	healthHandler(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", w.Code)
	}
}

func TestStatusHandler(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/api/v1/status", nil)
	w := httptest.NewRecorder()
	statusHandler(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", w.Code)
	}
}
"""
    with open(os.path.join(CMD_APP_DIR, 'main_test.go'), 'w') as f:
        f.write(main_test_content)

    # Ensure NO .vscode/launch.json exists (negative constraint)
    launch_json_path = os.path.join(VSCODE_DIR, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  go.mod: {os.path.join(PROJECT_DIR, "go.mod")}')
    print(f'  main.go: {os.path.join(CMD_APP_DIR, "main.go")}')
    print(f'  .vscode/launch.json: DOES NOT EXIST (correct)')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
