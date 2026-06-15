"""
Initial Setup: VSCode Go code review — refactor product_service.go
Task ID: vscode_gf6_031
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_031'
PROJECT_DIR = f'{WORKDIR}/projects/code-review-go'

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

def install_go():
    """Install Go 1.21 if not already present."""
    go_dir = f'{WORKDIR}/go-sdk'
    go_bin = f'{go_dir}/go/bin/go'
    if os.path.exists(go_bin):
        print('Go already installed')
        return
    print('Installing Go 1.21...')
    os.makedirs(go_dir, exist_ok=True)
    subprocess.run(
        f'wget -q https://go.dev/dl/go1.21.13.linux-amd64.tar.gz -O /tmp/go.tar.gz && '
        f'tar -C {go_dir} -xzf /tmp/go.tar.gz && '
        f'rm /tmp/go.tar.gz',
        shell=True, check=True,
    )
    print('Go 1.21 installed')

def go_bin():
    return f'{WORKDIR}/go-sdk/go/bin/go'

def setup_go_env():
    """Add Go to PATH for this process and for the user profile."""
    go_path = f'{WORKDIR}/go-sdk/go/bin'
    os.environ['PATH'] = go_path + ':' + os.environ.get('PATH', '')
    os.environ['GOPATH'] = f'{WORKDIR}/go'
    # Persist for user shell
    bashrc = f'{WORKDIR}/.bashrc'
    marker = '# GO_PATH_ADDED'
    try:
        with open(bashrc, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = ''
    if marker not in content:
        with open(bashrc, 'a') as f:
            f.write(f'\n{marker}\nexport PATH={go_path}:$PATH\nexport GOPATH={WORKDIR}/go\n')

def create_initial():
    install_go()
    setup_go_env()

    # Create project directory structure
    service_dir = f'{PROJECT_DIR}/internal/service'
    os.makedirs(service_dir, exist_ok=True)

    # --- go.mod ---
    go_mod = f'{PROJECT_DIR}/go.mod'
    with open(go_mod, 'w') as f:
        f.write("""module github.com/acmecorp/code-review-go

go 1.21
""")

    # --- internal/service/product_service.go ---
    service_file = f'{service_dir}/product_service.go'
    with open(service_file, 'w') as f:
        f.write('''package service

import (
\t"database/sql"
\t"fmt"
\t"log"
)

// Product represents a product in the catalog.
type Product struct {
\tID          int
\tName        string
\tDescription string
\tPrice       float64
\tCategory    string
\tInStock     bool
}

// ProductService handles business logic for products.
type ProductService struct {
\tdb *sql.DB
}

// NewProductService creates a new ProductService with the given database connection.
func NewProductService(db *sql.DB) *ProductService {
\treturn &ProductService{db: db}
}

// FindByID retrieves a single product by its ID.
func (s *ProductService) FindByID(id int) (*Product, error) {
\tlog.Printf("Finding product with ID: %d", id)

\trow := s.db.QueryRow(
\t\t"SELECT id, name, description, price, category, in_stock FROM products WHERE id = $1", id,
\t)

\tp := &Product{}
\terr := row.Scan(&p.ID, &p.Name, &p.Description, &p.Price, &p.Category, &p.InStock)
\tif err != nil {
\t\tif err == sql.ErrNoRows {
\t\t\tlog.Printf("Product with ID %d not found", id)
\t\t\treturn nil, fmt.Errorf("product not found: %d", id)
\t\t}
\t\tlog.Printf("Error finding product: %v", err)
\t\treturn nil, fmt.Errorf("failed to find product: %w", err)
\t}

\tlog.Printf("Found product: %s", p.Name)
\treturn p, nil
}

// FindAll retrieves all products from the database.
func (s *ProductService) FindAll() ([]*Product, error) {
\tlog.Printf("Fetching all products")

\trows, err := s.db.Query(
\t\t"SELECT id, name, description, price, category, in_stock FROM products",
\t)
\tif err != nil {
\t\tlog.Printf("Error fetching products: %v", err)
\t\treturn nil, fmt.Errorf("failed to fetch products: %w", err)
\t}
\tdefer rows.Close()

\tvar products []*Product
\tfor rows.Next() {
\t\tp := &Product{}
\t\terr := rows.Scan(&p.ID, &p.Name, &p.Description, &p.Price, &p.Category, &p.InStock)
\t\tif err != nil {
\t\t\tlog.Printf("Error scanning product row: %v", err)
\t\t\treturn nil, fmt.Errorf("failed to scan product: %w", err)
\t\t}
\t\tproducts = append(products, p)
\t}

\tif err = rows.Err(); err != nil {
\t\tlog.Printf("Error iterating product rows: %v", err)
\t\treturn nil, fmt.Errorf("row iteration error: %w", err)
\t}

\tlog.Printf("Fetched %d products", len(products))
\treturn products, nil
}

// Save creates or updates a product in the database.
func (s *ProductService) Save(product *Product) error {
\tlog.Printf("Saving product: %s", product.Name)

\tif product.ID == 0 {
\t\terr := s.db.QueryRow(
\t\t\t"INSERT INTO products (name, description, price, category, in_stock) VALUES ($1, $2, $3, $4, $5) RETURNING id",
\t\t\tproduct.Name, product.Description, product.Price, product.Category, product.InStock,
\t\t).Scan(&product.ID)
\t\tif err != nil {
\t\t\tlog.Printf("Error inserting product: %v", err)
\t\t\treturn fmt.Errorf("failed to insert product: %w", err)
\t\t}
\t\tlog.Printf("Inserted product with ID: %d", product.ID)
\t} else {
\t\t_, err := s.db.Exec(
\t\t\t"UPDATE products SET name=$1, description=$2, price=$3, category=$4, in_stock=$5 WHERE id=$6",
\t\t\tproduct.Name, product.Description, product.Price, product.Category, product.InStock, product.ID,
\t\t)
\t\tif err != nil {
\t\t\tlog.Printf("Error updating product: %v", err)
\t\t\treturn fmt.Errorf("failed to update product: %w", err)
\t\t}
\t\tlog.Printf("Updated product with ID: %d", product.ID)
\t}

\treturn nil
}

// Delete removes a product from the database by its ID.
func (s *ProductService) Delete(id int) error {
\tlog.Printf("Deleting product with ID: %d", id)

\tresult, err := s.db.Exec("DELETE FROM products WHERE id = $1", id)
\tif err != nil {
\t\tlog.Printf("Error deleting product: %v", err)
\t\treturn fmt.Errorf("failed to delete product: %w", err)
\t}

\trowsAffected, err := result.RowsAffected()
\tif err != nil {
\t\tlog.Printf("Error checking rows affected: %v", err)
\t\treturn fmt.Errorf("failed to check deletion result: %w", err)
\t}

\tif rowsAffected == 0 {
\t\tlog.Printf("No product found with ID: %d", id)
\t\treturn fmt.Errorf("product not found: %d", id)
\t}

\tlog.Printf("Deleted product with ID: %d", id)
\treturn nil
}
''')

    # Verify go build works with initial code
    result = subprocess.run(
        f'{go_bin()} build ./...',
        shell=True, capture_output=True, text=True,
        cwd=PROJECT_DIR,
        env={**os.environ, 'GOPATH': f'{WORKDIR}/go', 'HOME': WORKDIR},
    )
    if result.returncode != 0:
        print(f'WARNING: go build failed: {result.stderr}')
    else:
        print('Initial go build succeeded')

    # Install Go VSCode extension
    subprocess.run(['code', '--install-extension', 'golang.go'], capture_output=True, text=True)
    print('Installed Go extension for VSCode')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: VSCode opened with {PROJECT_DIR}')

create_initial()
