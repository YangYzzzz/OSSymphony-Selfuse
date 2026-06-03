"""
Initial Setup: Set up Go integration test project with testcontainers-go
Task ID: vscode_gf6_070
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_070'
PROJECT_DIR = f'{WORKDIR}/projects/go-integration-tests'


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
    os.makedirs(f'{PROJECT_DIR}/internal/repository', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/migrations', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/cmd', exist_ok=True)

    # --- go.mod (no testcontainers dependency yet) ---
    go_mod = """module github.com/user/go-integration-tests

go 1.21

require (
\tgithub.com/lib/pq v1.10.9
)

require (
\tgithub.com/jmoiron/sqlx v1.3.5 // indirect
)
"""
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write(go_mod)

    # --- go.sum (minimal) ---
    go_sum = """github.com/lib/pq v1.10.9 h1:YXG7RB+JIjhP29X+OtkiDnYaXQwpS4JEWq7dtCCRUEw=
github.com/lib/pq v1.10.9/go.mod h1:AlVN5x4E4T544tWzH6hKFbGRn7nbIqu9HhEDnDfStSo=
github.com/jmoiron/sqlx v1.3.5 h1:vFFPA71p1o5gAeqtEAwLU4dnX2napprKtHr7PYIcN3g0=
github.com/jmoiron/sqlx v1.3.5/go.mod h1:mZiiNNASBKJx/a5YpUCUFnxgSC0Cml8cGSOTDCSWUfE=
"""
    with open(f'{PROJECT_DIR}/go.sum', 'w') as f:
        f.write(go_sum)

    # --- internal/repository/user_repo.go ---
    user_repo = '''package repository

import (
\t"context"
\t"database/sql"
\t"fmt"
\t"time"
)

// User represents a user record in the database.
type User struct {
\tID        int64
\tName      string
\tEmail     string
\tAge       int
\tCreatedAt time.Time
\tUpdatedAt time.Time
}

// UserRepository handles database operations for users.
type UserRepository struct {
\tdb *sql.DB
}

// NewUserRepository creates a new UserRepository instance.
func NewUserRepository(db *sql.DB) *UserRepository {
\treturn &UserRepository{db: db}
}

// Create inserts a new user into the database and returns the created user.
func (r *UserRepository) Create(ctx context.Context, name, email string, age int) (*User, error) {
\tquery := `INSERT INTO users (name, email, age, created_at, updated_at)
\t\tVALUES ($1, $2, $3, NOW(), NOW())
\t\tRETURNING id, name, email, age, created_at, updated_at`

\tuser := &User{}
\terr := r.db.QueryRowContext(ctx, query, name, email, age).Scan(
\t\t&user.ID, &user.Name, &user.Email, &user.Age,
\t\t&user.CreatedAt, &user.UpdatedAt,
\t)
\tif err != nil {
\t\treturn nil, fmt.Errorf("failed to create user: %w", err)
\t}
\treturn user, nil
}

// GetByID retrieves a user by their ID.
func (r *UserRepository) GetByID(ctx context.Context, id int64) (*User, error) {
\tquery := `SELECT id, name, email, age, created_at, updated_at FROM users WHERE id = $1`

\tuser := &User{}
\terr := r.db.QueryRowContext(ctx, query, id).Scan(
\t\t&user.ID, &user.Name, &user.Email, &user.Age,
\t\t&user.CreatedAt, &user.UpdatedAt,
\t)
\tif err != nil {
\t\tif err == sql.ErrNoRows {
\t\t\treturn nil, fmt.Errorf("user with id %d not found", id)
\t\t}
\t\treturn nil, fmt.Errorf("failed to get user: %w", err)
\t}
\treturn user, nil
}

// GetByEmail retrieves a user by their email address.
func (r *UserRepository) GetByEmail(ctx context.Context, email string) (*User, error) {
\tquery := `SELECT id, name, email, age, created_at, updated_at FROM users WHERE email = $1`

\tuser := &User{}
\terr := r.db.QueryRowContext(ctx, query, email).Scan(
\t\t&user.ID, &user.Name, &user.Email, &user.Age,
\t\t&user.CreatedAt, &user.UpdatedAt,
\t)
\tif err != nil {
\t\tif err == sql.ErrNoRows {
\t\t\treturn nil, fmt.Errorf("user with email %s not found", email)
\t\t}
\t\treturn nil, fmt.Errorf("failed to get user by email: %w", err)
\t}
\treturn user, nil
}

// ListAll retrieves all users from the database.
func (r *UserRepository) ListAll(ctx context.Context) ([]*User, error) {
\tquery := `SELECT id, name, email, age, created_at, updated_at FROM users ORDER BY id`

\trows, err := r.db.QueryContext(ctx, query)
\tif err != nil {
\t\treturn nil, fmt.Errorf("failed to list users: %w", err)
\t}
\tdefer rows.Close()

\tvar users []*User
\tfor rows.Next() {
\t\tuser := &User{}
\t\tif err := rows.Scan(&user.ID, &user.Name, &user.Email, &user.Age,
\t\t\t&user.CreatedAt, &user.UpdatedAt); err != nil {
\t\t\treturn nil, fmt.Errorf("failed to scan user: %w", err)
\t\t}
\t\tusers = append(users, user)
\t}
\treturn users, rows.Err()
}

// Delete removes a user by their ID.
func (r *UserRepository) Delete(ctx context.Context, id int64) error {
\tquery := `DELETE FROM users WHERE id = $1`
\tresult, err := r.db.ExecContext(ctx, query, id)
\tif err != nil {
\t\treturn fmt.Errorf("failed to delete user: %w", err)
\t}
\trows, err := result.RowsAffected()
\tif err != nil {
\t\treturn fmt.Errorf("failed to get rows affected: %w", err)
\t}
\tif rows == 0 {
\t\treturn fmt.Errorf("user with id %d not found", id)
\t}
\treturn nil
}
'''
    with open(f'{PROJECT_DIR}/internal/repository/user_repo.go', 'w') as f:
        f.write(user_repo)

    # --- migrations/001_create_users_table.up.sql ---
    migration_up = """-- Migration: Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users (email);
"""
    with open(f'{PROJECT_DIR}/migrations/001_create_users_table.up.sql', 'w') as f:
        f.write(migration_up)

    # --- migrations/002_add_users_status.up.sql ---
    migration_status = """-- Migration: Add status column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'active';

CREATE INDEX idx_users_status ON users (status);
"""
    with open(f'{PROJECT_DIR}/migrations/002_add_users_status.up.sql', 'w') as f:
        f.write(migration_status)

    # --- cmd/main.go ---
    main_go = '''package main

import (
\t"database/sql"
\t"fmt"
\t"log"
\t"os"

\t_ "github.com/lib/pq"
)

func main() {
\tdbURL := os.Getenv("DATABASE_URL")
\tif dbURL == "" {
\t\tdbURL = "postgres://postgres:postgres@localhost:5432/app?sslmode=disable"
\t}

\tdb, err := sql.Open("postgres", dbURL)
\tif err != nil {
\t\tlog.Fatalf("Failed to connect to database: %v", err)
\t}
\tdefer db.Close()

\tif err := db.Ping(); err != nil {
\t\tlog.Fatalf("Failed to ping database: %v", err)
\t}

\tfmt.Println("Connected to database successfully")
}
'''
    with open(f'{PROJECT_DIR}/cmd/main.go', 'w') as f:
        f.write(main_go)

    # --- Makefile (NO test-integration target yet) ---
    makefile = """# Go Integration Tests Project

.PHONY: build run test clean

build:
\tgo build -o bin/app ./cmd/...

run: build
\t./bin/app

test:
\tgo test -v ./...

clean:
\trm -rf bin/
\tgo clean -cache

lint:
\tgolangci-lint run ./...

.DEFAULT_GOAL := build
"""
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write(makefile)

    # --- .gitignore ---
    gitignore = """# Binaries
bin/
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary
*.test

# Output of go coverage
*.out

# Dependency directories
vendor/

# IDE
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = """# Go Integration Tests

A Go application demonstrating database operations with PostgreSQL.

## Project Structure

```
go-integration-tests/
├── cmd/               # Application entry points
│   └── main.go
├── internal/
│   └── repository/    # Database repository layer
│       └── user_repo.go
├── migrations/        # SQL migration files
│   ├── 001_create_users_table.up.sql
│   └── 002_add_users_status.up.sql
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

## Getting Started

```bash
make build
make run
make test
```

## Database

This project uses PostgreSQL. Set the `DATABASE_URL` environment variable
to configure the database connection.
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            print(f'  {fpath}')

    # GUI-ready: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
