"""
Initial Setup: Go REST API debug project with swapped min/max bug
Task ID: vscode_gf6_014
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_014'
PROJECT_DIR = f'{WORKDIR}/projects/go-debug'

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

def create_text_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def create_initial():
    # --- go.mod ---
    create_text_file(f'{PROJECT_DIR}/go.mod', """\
module github.com/user/go-debug

go 1.21
""")

    # --- cmd/server/main.go ---
    create_text_file(f'{PROJECT_DIR}/cmd/server/main.go', """\
package main

import (
\t"fmt"
\t"log"
\t"net/http"
\t"os"

\t"github.com/user/go-debug/internal/handlers"
)

func main() {
\tport := os.Getenv("APP_PORT")
\tif port == "" {
\t\tport = "8080"
\t}

\tdbHost := os.Getenv("DB_HOST")
\tif dbHost == "" {
\t\tdbHost = "localhost"
\t}

\tmux := http.NewServeMux()
\tmux.HandleFunc("/api/products", handlers.GetAllProducts)
\tmux.HandleFunc("/api/products/price-range", handlers.GetByPriceRange)

\taddr := fmt.Sprintf(":%s", port)
\tlog.Printf("Starting server on %s (DB: %s)", addr, dbHost)
\tlog.Fatal(http.ListenAndServe(addr, mux))
}
""")

    # --- internal/handlers/products.go (WITH BUG: min/max swapped) ---
    create_text_file(f'{PROJECT_DIR}/internal/handlers/products.go', """\
package handlers

import (
\t"encoding/json"
\t"net/http"
\t"strconv"
)

type Product struct {
\tID    int     `json:"id"`
\tName  string  `json:"name"`
\tPrice float64 `json:"price"`
}

var productCatalog = []Product{
\t{ID: 1, Name: "Wireless Bluetooth Headphones", Price: 79.99},
\t{ID: 2, Name: "USB-C Charging Cable", Price: 12.49},
\t{ID: 3, Name: "Mechanical Keyboard", Price: 149.95},
\t{ID: 4, Name: "27-inch 4K Monitor", Price: 349.00},
\t{ID: 5, Name: "Ergonomic Mouse Pad", Price: 24.99},
\t{ID: 6, Name: "Laptop Stand", Price: 45.00},
\t{ID: 7, Name: "Webcam HD 1080p", Price: 59.99},
\t{ID: 8, Name: "Portable SSD 1TB", Price: 109.99},
\t{ID: 9, Name: "Desk Lamp LED", Price: 34.50},
\t{ID: 10, Name: "Noise Cancelling Earbuds", Price: 199.99},
}

func GetAllProducts(w http.ResponseWriter, r *http.Request) {
\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(productCatalog)
}

// GetByPriceRange filters products by min and max price query parameters.
// BUG: The min and max query param values are parsed into the wrong variables.
func GetByPriceRange(w http.ResponseWriter, r *http.Request) {
\tminStr := r.URL.Query().Get("min")
\tmaxStr := r.URL.Query().Get("max")

\t// BUG: min param is parsed into maxPrice, max param is parsed into minPrice
\tmaxPrice, err := strconv.ParseFloat(minStr, 64)
\tif err != nil {
\t\tmaxPrice = 999999.99
\t}
\tminPrice, err := strconv.ParseFloat(maxStr, 64)
\tif err != nil {
\t\tminPrice = 0
\t}

\tvar filtered []Product
\tfor _, p := range productCatalog {
\t\tif p.Price >= minPrice && p.Price <= maxPrice {
\t\t\tfiltered = append(filtered, p)
\t\t}
\t}

\tw.Header().Set("Content-Type", "application/json")
\tjson.NewEncoder(w).Encode(filtered)
}
""")

    # --- internal/handlers/products_test.go (2 tests that fail due to the bug) ---
    create_text_file(f'{PROJECT_DIR}/internal/handlers/products_test.go', """\
package handlers

import (
\t"encoding/json"
\t"net/http"
\t"net/http/httptest"
\t"testing"
)

func TestGetByPriceRange_MidRange(t *testing.T) {
\t// Should return products between $30 and $100
\treq := httptest.NewRequest("GET", "/api/products/price-range?min=30&max=100", nil)
\tw := httptest.NewRecorder()
\tGetByPriceRange(w, req)

\tif w.Code != http.StatusOK {
\t\tt.Fatalf("expected status 200, got %d", w.Code)
\t}

\tvar products []Product
\tif err := json.NewDecoder(w.Body).Decode(&products); err != nil {
\t\tt.Fatalf("failed to decode response: %v", err)
\t}

\t// Expected: Wireless Bluetooth Headphones ($79.99), Laptop Stand ($45.00),
\t// Webcam HD 1080p ($59.99), Desk Lamp LED ($34.50)
\texpectedCount := 4
\tif len(products) != expectedCount {
\t\tt.Errorf("expected %d products in $30-$100 range, got %d", expectedCount, len(products))
\t\tfor _, p := range products {
\t\t\tt.Logf("  got: %s ($%.2f)", p.Name, p.Price)
\t\t}
\t}

\t// Verify no product is outside the range
\tfor _, p := range products {
\t\tif p.Price < 30 || p.Price > 100 {
\t\t\tt.Errorf("product %q ($%.2f) is outside range $30-$100", p.Name, p.Price)
\t\t}
\t}
}

func TestGetByPriceRange_LowEnd(t *testing.T) {
\t// Should return products under $30
\treq := httptest.NewRequest("GET", "/api/products/price-range?min=0&max=30", nil)
\tw := httptest.NewRecorder()
\tGetByPriceRange(w, req)

\tif w.Code != http.StatusOK {
\t\tt.Fatalf("expected status 200, got %d", w.Code)
\t}

\tvar products []Product
\tif err := json.NewDecoder(w.Body).Decode(&products); err != nil {
\t\tt.Fatalf("failed to decode response: %v", err)
\t}

\t// Expected: USB-C Charging Cable ($12.49), Ergonomic Mouse Pad ($24.99)
\texpectedCount := 2
\tif len(products) != expectedCount {
\t\tt.Errorf("expected %d products in $0-$30 range, got %d", expectedCount, len(products))
\t\tfor _, p := range products {
\t\t\tt.Logf("  got: %s ($%.2f)", p.Name, p.Price)
\t\t}
\t}

\t// Verify no product is outside the range
\tfor _, p := range products {
\t\tif p.Price < 0 || p.Price > 30 {
\t\t\tt.Errorf("product %q ($%.2f) is outside range $0-$30", p.Name, p.Price)
\t\t}
\t}
}
""")

    # Ensure no .vscode directory exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
