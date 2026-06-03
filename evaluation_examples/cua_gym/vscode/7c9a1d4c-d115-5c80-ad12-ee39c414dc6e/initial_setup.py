"""
Initial Setup: Add a debug configuration for Go tests in launch.json
Task ID: vscode_lang_011
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_011'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'mygoapp')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
LAUNCH_JSON = os.path.join(VSCODE_DIR, 'launch.json')


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
    os.makedirs(os.path.join(PROJECT_DIR, 'cmd', 'mygoapp'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'pkg', 'utils'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'internal', 'handler'), exist_ok=True)

    # Create go.mod
    go_mod = """module github.com/acmecorp/mygoapp

go 1.21

require (
\tgithub.com/gorilla/mux v1.8.1
\tgithub.com/stretchr/testify v1.8.4
)
"""
    with open(os.path.join(PROJECT_DIR, 'go.mod'), 'w') as f:
        f.write(go_mod)

    # Create main.go
    main_go = """package main

import (
\t"fmt"
\t"log"
\t"net/http"

\t"github.com/acmecorp/mygoapp/internal/handler"
\t"github.com/gorilla/mux"
)

func main() {
\tr := mux.NewRouter()
\tr.HandleFunc("/api/health", handler.HealthCheck).Methods("GET")
\tr.HandleFunc("/api/users", handler.ListUsers).Methods("GET")
\tr.HandleFunc("/api/users/{id}", handler.GetUser).Methods("GET")

\tfmt.Println("Starting server on :8080")
\tlog.Fatal(http.ListenAndServe(":8080", r))
}
"""
    with open(os.path.join(PROJECT_DIR, 'cmd', 'mygoapp', 'main.go'), 'w') as f:
        f.write(main_go)

    # Create pkg/utils/stringutil.go
    stringutil_go = """package utils

import (
\t"strings"
\t"unicode"
)

// Capitalize returns the string with the first letter uppercased.
func Capitalize(s string) string {
\tif len(s) == 0 {
\t\treturn s
\t}
\trunes := []rune(s)
\trunes[0] = unicode.ToUpper(runes[0])
\treturn string(runes)
}

// SlugifyTitle converts a title string into a URL-friendly slug.
func SlugifyTitle(title string) string {
\ttitle = strings.ToLower(title)
\ttitle = strings.TrimSpace(title)
\ttitle = strings.ReplaceAll(title, " ", "-")
\treturn title
}

// TruncateWithEllipsis truncates s to maxLen characters, appending "..." if truncated.
func TruncateWithEllipsis(s string, maxLen int) string {
\tif len(s) <= maxLen {
\t\treturn s
\t}
\tif maxLen <= 3 {
\t\treturn s[:maxLen]
\t}
\treturn s[:maxLen-3] + "..."
}
"""
    with open(os.path.join(PROJECT_DIR, 'pkg', 'utils', 'stringutil.go'), 'w') as f:
        f.write(stringutil_go)

    # Create pkg/utils/stringutil_test.go
    stringutil_test_go = """package utils

import "testing"

func TestCapitalize(t *testing.T) {
\ttests := []struct {
\t\tinput    string
\t\texpected string
\t}{
\t\t{"hello", "Hello"},
\t\t{"world", "World"},
\t\t{"", ""},
\t\t{"Already", "Already"},
\t}
\tfor _, tt := range tests {
\t\tresult := Capitalize(tt.input)
\t\tif result != tt.expected {
\t\t\tt.Errorf("Capitalize(%q) = %q, want %q", tt.input, result, tt.expected)
\t\t}
\t}
}

func TestSlugifyTitle(t *testing.T) {
\ttests := []struct {
\t\tinput    string
\t\texpected string
\t}{
\t\t{"Hello World", "hello-world"},
\t\t{"  Spaces Around  ", "spaces-around"},
\t\t{"already-slugged", "already-slugged"},
\t}
\tfor _, tt := range tests {
\t\tresult := SlugifyTitle(tt.input)
\t\tif result != tt.expected {
\t\t\tt.Errorf("SlugifyTitle(%q) = %q, want %q", tt.input, result, tt.expected)
\t\t}
\t}
}

func TestTruncateWithEllipsis(t *testing.T) {
\ttests := []struct {
\t\tinput    string
\t\tmaxLen   int
\t\texpected string
\t}{
\t\t{"short", 10, "short"},
\t\t{"a long string here", 10, "a long..."},
\t\t{"ab", 2, "ab"},
\t}
\tfor _, tt := range tests {
\t\tresult := TruncateWithEllipsis(tt.input, tt.maxLen)
\t\tif result != tt.expected {
\t\t\tt.Errorf("TruncateWithEllipsis(%q, %d) = %q, want %q", tt.input, tt.maxLen, result, tt.expected)
\t\t}
\t}
}
"""
    with open(os.path.join(PROJECT_DIR, 'pkg', 'utils', 'stringutil_test.go'), 'w') as f:
        f.write(stringutil_test_go)

    # Create internal/handler/handler.go
    handler_go = """package handler

import (
\t"encoding/json"
\t"net/http"

\t"github.com/gorilla/mux"
)

type User struct {
\tID    string `json:"id"`
\tName  string `json:"name"`
\tEmail string `json:"email"`
}

var users = []User{
\t{ID: "1", Name: "Sarah Chen", Email: "sarah.chen@acmecorp.com"},
\t{ID: "2", Name: "Marcus Johnson", Email: "marcus.j@acmecorp.com"},
\t{ID: "3", Name: "Priya Patel", Email: "priya.p@acmecorp.com"},
}

func HealthCheck(w http.ResponseWriter, r *http.Request) {
\tw.WriteHeader(http.StatusOK)
\tjson.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func ListUsers(w http.ResponseWriter, r *http.Request) {
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(users)
}

func GetUser(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tfor _, u := range users {
\t\tif u.ID == vars["id"] {
\t\t\tw.Header().Set("Content-Type", "application/json")
\t\t\tjson.NewEncoder(w).Encode(u)
\t\t\treturn
\t\t}
\t}
\thttp.Error(w, "user not found", http.StatusNotFound)
}
"""
    with open(os.path.join(PROJECT_DIR, 'internal', 'handler', 'handler.go'), 'w') as f:
        f.write(handler_go)

    # Create .vscode/launch.json with ONLY the initial "Launch Package" config
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Launch Package",
                "type": "go",
                "request": "launch",
                "mode": "auto",
                "program": "${workspaceFolder}/cmd/mygoapp"
            }
        ]
    }
    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'launch.json created: {LAUNCH_JSON}')

    # Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
