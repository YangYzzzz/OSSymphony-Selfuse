"""
Initial Setup: Set up a Go remote debugging configuration in launch.json
Task ID: vscode_lang_019
Domain: vs_code
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_019'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'
LAUNCH_JSON = f'{VSCODE_DIR}/launch.json'


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
    os.makedirs(f'{PROJECT_DIR}/cmd/server', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/internal/handlers', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/internal/models', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/pkg/middleware', exist_ok=True)

    # Create go.mod
    with open(f'{PROJECT_DIR}/go.mod', 'w') as f:
        f.write("""module github.com/acmecorp/inventory-service

go 1.21

require (
\tgithub.com/gorilla/mux v1.8.1
\tgithub.com/lib/pq v1.10.9
\tgithub.com/sirupsen/logrus v1.9.3
\tgithub.com/joho/godotenv v1.5.1
)
""")

    # Create main.go
    with open(f'{PROJECT_DIR}/cmd/server/main.go', 'w') as f:
        f.write("""package main

import (
\t"fmt"
\t"net/http"
\t"os"

\t"github.com/acmecorp/inventory-service/internal/handlers"
\t"github.com/acmecorp/inventory-service/pkg/middleware"
\t"github.com/gorilla/mux"
\t"github.com/joho/godotenv"
\tlog "github.com/sirupsen/logrus"
)

func main() {
\tif err := godotenv.Load(); err != nil {
\t\tlog.Warn("No .env file found, using system environment")
\t}

\tport := os.Getenv("PORT")
\tif port == "" {
\t\tport = "8080"
\t}

\trouter := mux.NewRouter()
\trouter.Use(middleware.LoggingMiddleware)
\trouter.Use(middleware.CORSMiddleware)

\t// Product routes
\trouter.HandleFunc("/api/v1/products", handlers.ListProducts).Methods("GET")
\trouter.HandleFunc("/api/v1/products/{id}", handlers.GetProduct).Methods("GET")
\trouter.HandleFunc("/api/v1/products", handlers.CreateProduct).Methods("POST")
\trouter.HandleFunc("/api/v1/products/{id}", handlers.UpdateProduct).Methods("PUT")
\trouter.HandleFunc("/api/v1/products/{id}", handlers.DeleteProduct).Methods("DELETE")

\t// Inventory routes
\trouter.HandleFunc("/api/v1/inventory", handlers.GetInventory).Methods("GET")
\trouter.HandleFunc("/api/v1/inventory/{sku}/adjust", handlers.AdjustStock).Methods("POST")

\t// Health check
\trouter.HandleFunc("/health", handlers.HealthCheck).Methods("GET")

\taddr := fmt.Sprintf(":%s", port)
\tlog.Infof("Inventory service starting on %s", addr)

\tif err := http.ListenAndServe(addr, router); err != nil {
\t\tlog.Fatalf("Server failed to start: %v", err)
\t}
}
""")

    # Create handlers
    with open(f'{PROJECT_DIR}/internal/handlers/products.go', 'w') as f:
        f.write("""package handlers

import (
\t"encoding/json"
\t"net/http"

\t"github.com/acmecorp/inventory-service/internal/models"
\t"github.com/gorilla/mux"
\tlog "github.com/sirupsen/logrus"
)

func ListProducts(w http.ResponseWriter, r *http.Request) {
\tproducts, err := models.GetAllProducts()
\tif err != nil {
\t\tlog.Errorf("Failed to fetch products: %v", err)
\t\thttp.Error(w, "Internal server error", http.StatusInternalServerError)
\t\treturn
\t}
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(products)
}

func GetProduct(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tproduct, err := models.GetProductByID(vars["id"])
\tif err != nil {
\t\tlog.Errorf("Product not found: %s", vars["id"])
\t\thttp.Error(w, "Product not found", http.StatusNotFound)
\t\treturn
\t}
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(product)
}

func CreateProduct(w http.ResponseWriter, r *http.Request) {
\tvar product models.Product
\tif err := json.NewDecoder(r.Body).Decode(&product); err != nil {
\t\thttp.Error(w, "Invalid request body", http.StatusBadRequest)
\t\treturn
\t}
\tif err := models.CreateProduct(&product); err != nil {
\t\tlog.Errorf("Failed to create product: %v", err)
\t\thttp.Error(w, "Internal server error", http.StatusInternalServerError)
\t\treturn
\t}
\tw.Header().Set("Content-Type", "application/json")
\tw.WriteHeader(http.StatusCreated)
\tjson.NewEncoder(w).Encode(product)
}

func UpdateProduct(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tvar product models.Product
\tif err := json.NewDecoder(r.Body).Decode(&product); err != nil {
\t\thttp.Error(w, "Invalid request body", http.StatusBadRequest)
\t\treturn
\t}
\tproduct.ID = vars["id"]
\tif err := models.UpdateProduct(&product); err != nil {
\t\tlog.Errorf("Failed to update product %s: %v", vars["id"], err)
\t\thttp.Error(w, "Internal server error", http.StatusInternalServerError)
\t\treturn
\t}
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(product)
}

func DeleteProduct(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tif err := models.DeleteProduct(vars["id"]); err != nil {
\t\tlog.Errorf("Failed to delete product %s: %v", vars["id"], err)
\t\thttp.Error(w, "Internal server error", http.StatusInternalServerError)
\t\treturn
\t}
\tw.WriteHeader(http.StatusNoContent)
}

func HealthCheck(w http.ResponseWriter, r *http.Request) {
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}
""")

    # Create models
    with open(f'{PROJECT_DIR}/internal/models/product.go', 'w') as f:
        f.write("""package models

import "time"

type Product struct {
\tID          string    `json:"id"`
\tSKU         string    `json:"sku"`
\tName        string    `json:"name"`
\tDescription string    `json:"description"`
\tCategory    string    `json:"category"`
\tPrice       float64   `json:"price"`
\tQuantity    int       `json:"quantity"`
\tWarehouse   string    `json:"warehouse"`
\tCreatedAt   time.Time `json:"created_at"`
\tUpdatedAt   time.Time `json:"updated_at"`
}

func GetAllProducts() ([]Product, error) {
\t// TODO: implement database query
\treturn nil, nil
}

func GetProductByID(id string) (*Product, error) {
\t// TODO: implement database query
\treturn nil, nil
}

func CreateProduct(p *Product) error {
\t// TODO: implement database insert
\treturn nil
}

func UpdateProduct(p *Product) error {
\t// TODO: implement database update
\treturn nil
}

func DeleteProduct(id string) error {
\t// TODO: implement database delete
\treturn nil
}
""")

    # Create inventory handler
    with open(f'{PROJECT_DIR}/internal/handlers/inventory.go', 'w') as f:
        f.write("""package handlers

import (
\t"encoding/json"
\t"net/http"

\t"github.com/gorilla/mux"
\tlog "github.com/sirupsen/logrus"
)

type StockAdjustment struct {
\tQuantity int    `json:"quantity"`
\tReason   string `json:"reason"`
}

func GetInventory(w http.ResponseWriter, r *http.Request) {
\t// TODO: implement inventory listing with warehouse filtering
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(map[string]string{"status": "not implemented"})
}

func AdjustStock(w http.ResponseWriter, r *http.Request) {
\tvars := mux.Vars(r)
\tsku := vars["sku"]

\tvar adj StockAdjustment
\tif err := json.NewDecoder(r.Body).Decode(&adj); err != nil {
\t\thttp.Error(w, "Invalid request body", http.StatusBadRequest)
\t\treturn
\t}

\tlog.Infof("Stock adjustment for SKU %s: %+d (%s)", sku, adj.Quantity, adj.Reason)
\t// TODO: implement stock adjustment logic
\tw.WriteHeader(http.StatusOK)
}
""")

    # Create middleware
    with open(f'{PROJECT_DIR}/pkg/middleware/logging.go', 'w') as f:
        f.write("""package middleware

import (
\t"net/http"
\t"time"

\tlog "github.com/sirupsen/logrus"
)

func LoggingMiddleware(next http.Handler) http.Handler {
\treturn http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
\t\tstart := time.Now()
\t\tnext.ServeHTTP(w, r)
\t\tlog.WithFields(log.Fields{
\t\t\t"method":   r.Method,
\t\t\t"path":     r.URL.Path,
\t\t\t"duration": time.Since(start),
\t\t\t"remote":   r.RemoteAddr,
\t\t}).Info("Request processed")
\t})
}

func CORSMiddleware(next http.Handler) http.Handler {
\treturn http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
\t\tw.Header().Set("Access-Control-Allow-Origin", "*")
\t\tw.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
\t\tw.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
\t\tif r.Method == "OPTIONS" {
\t\t\tw.WriteHeader(http.StatusOK)
\t\t\treturn
\t\t}
\t\tnext.ServeHTTP(w, r)
\t})
}
""")

    # Create .env file
    with open(f'{PROJECT_DIR}/.env', 'w') as f:
        f.write("""PORT=8080
DB_HOST=localhost
DB_PORT=5432
DB_NAME=inventory_db
DB_USER=acme_svc
DB_PASSWORD=dev_password_2024
LOG_LEVEL=debug
""")

    # Create .vscode/launch.json with ONLY a local debug configuration
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Launch Server",
                "type": "go",
                "request": "launch",
                "mode": "auto",
                "program": "${workspaceFolder}/cmd/server",
                "env": {
                    "PORT": "8080"
                },
                "args": []
            }
        ]
    }

    with open(LAUNCH_JSON, 'w') as f:
        json.dump(launch_config, f, indent=4)

    # Create .vscode/settings.json
    vscode_settings = {
        "go.lintTool": "golangci-lint",
        "go.lintFlags": ["--fast"],
        "go.formatTool": "goimports",
        "editor.formatOnSave": True,
        "go.testFlags": ["-v", "-count=1"],
        "go.coverOnSave": False
    }

    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'launch.json created: {LAUNCH_JSON}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
