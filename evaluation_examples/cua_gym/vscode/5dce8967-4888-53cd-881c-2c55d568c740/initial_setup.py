"""
Initial Setup: Configure a multi-language debugging workflow in ~/project
Task ID: vscode_wf_078
Domain: vscode

Creates:
  ~/project/backend/app.py          - Python Flask backend
  ~/project/frontend/src/index.ts   - TypeScript frontend
  ~/project/frontend/tsconfig.json  - TypeScript config
  ~/project/frontend/package.json   - Node.js package manifest
  ~/project/native/lib.c            - C shared library source
  ~/project/native/Makefile         - Build file for native lib
  ~/project/.vscode/                - Empty (NO launch.json)

Opens VSCode with ~/project folder.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')

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
    # ---- Directory structure ----
    dirs = [
        os.path.join(PROJECT, 'backend'),
        os.path.join(PROJECT, 'frontend', 'src'),
        os.path.join(PROJECT, 'frontend', 'dist'),
        os.path.join(PROJECT, 'native'),
        os.path.join(PROJECT, '.vscode'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # ---- backend/app.py ----
    backend_app = '''\
"""
Inventory Management API — Flask Backend
Serves REST endpoints for product catalog and order processing.
"""
from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "inventory.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/products", methods=["GET"])
def list_products():
    db = get_db()
    cursor = db.execute(
        "SELECT id, name, sku, price, quantity FROM products ORDER BY name"
    )
    products = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify({"products": products, "count": len(products)})


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    db.close()
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(dict(product))


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data or "items" not in data:
        return jsonify({"error": "Missing order items"}), 400

    db = get_db()
    total = 0.0
    order_items = []
    for item in data["items"]:
        cursor = db.execute(
            "SELECT id, name, price, quantity FROM products WHERE id = ?",
            (item["product_id"],),
        )
        product = cursor.fetchone()
        if product is None:
            db.close()
            return jsonify({"error": f"Product {item['product_id']} not found"}), 404
        qty = item.get("quantity", 1)
        if qty > product["quantity"]:
            db.close()
            return jsonify({"error": f"Insufficient stock for {product['name']}"}), 400
        subtotal = product["price"] * qty
        total += subtotal
        order_items.append({
            "product_id": product["id"],
            "name": product["name"],
            "quantity": qty,
            "subtotal": subtotal,
        })

    order_id = int(datetime.now().timestamp() * 1000)
    db.close()
    return jsonify({
        "order_id": order_id,
        "items": order_items,
        "total": round(total, 2),
        "status": "confirmed",
        "created_at": datetime.now().isoformat(),
    }), 201


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "version": "2.4.1"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
'''
    with open(os.path.join(PROJECT, 'backend', 'app.py'), 'w') as f:
        f.write(backend_app)

    # ---- backend/requirements.txt ----
    with open(os.path.join(PROJECT, 'backend', 'requirements.txt'), 'w') as f:
        f.write("flask>=2.3.0\nrequests>=2.28.0\nsqlite3-api>=2.0.0\n")

    # ---- frontend/src/index.ts ----
    frontend_src = '''\
/**
 * Inventory Dashboard — TypeScript Frontend
 * Fetches product data from the backend API and renders
 * an interactive table with search, sort, and pagination.
 */

interface Product {
    id: number;
    name: string;
    sku: string;
    price: number;
    quantity: number;
}

interface ApiResponse<T> {
    products: T[];
    count: number;
}

const API_BASE = "http://localhost:5001/api";

class InventoryDashboard {
    private products: Product[] = [];
    private filteredProducts: Product[] = [];
    private currentPage: number = 1;
    private pageSize: number = 20;
    private sortField: keyof Product = "name";
    private sortAsc: boolean = true;

    constructor(private containerEl: HTMLElement) {
        this.init();
    }

    private async init(): Promise<void> {
        try {
            await this.fetchProducts();
            this.render();
            this.attachEventListeners();
        } catch (error) {
            console.error("Failed to initialize dashboard:", error);
            this.renderError("Unable to connect to the inventory service.");
        }
    }

    private async fetchProducts(): Promise<void> {
        const response = await fetch(`${API_BASE}/products`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const data: ApiResponse<Product> = await response.json();
        this.products = data.products;
        this.filteredProducts = [...this.products];
    }

    private render(): void {
        const start = (this.currentPage - 1) * this.pageSize;
        const pageItems = this.filteredProducts.slice(start, start + this.pageSize);

        const rows = pageItems
            .map(
                (p) => `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.sku}</td>
                <td>$${p.price.toFixed(2)}</td>
                <td class="${p.quantity < 10 ? "low-stock" : ""}">${p.quantity}</td>
            </tr>`
            )
            .join("");

        this.containerEl.innerHTML = `
            <div class="toolbar">
                <input type="text" id="search" placeholder="Search products..." />
                <span class="count">${this.filteredProducts.length} products</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th data-field="id">ID</th>
                        <th data-field="name">Name</th>
                        <th data-field="sku">SKU</th>
                        <th data-field="price">Price</th>
                        <th data-field="quantity">Stock</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
            <div class="pagination">
                <button id="prev" ${this.currentPage === 1 ? "disabled" : ""}>Previous</button>
                <span>Page ${this.currentPage} of ${Math.ceil(this.filteredProducts.length / this.pageSize)}</span>
                <button id="next" ${start + this.pageSize >= this.filteredProducts.length ? "disabled" : ""}>Next</button>
            </div>`;
    }

    private attachEventListeners(): void {
        const searchInput = document.getElementById("search") as HTMLInputElement;
        if (searchInput) {
            searchInput.addEventListener("input", () => {
                const query = searchInput.value.toLowerCase();
                this.filteredProducts = this.products.filter(
                    (p) =>
                        p.name.toLowerCase().includes(query) ||
                        p.sku.toLowerCase().includes(query)
                );
                this.currentPage = 1;
                this.render();
                this.attachEventListeners();
            });
        }
    }

    private renderError(message: string): void {
        this.containerEl.innerHTML = `<div class="error">${message}</div>`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("app");
    if (container) {
        new InventoryDashboard(container);
    }
});
'''
    with open(os.path.join(PROJECT, 'frontend', 'src', 'index.ts'), 'w') as f:
        f.write(frontend_src)

    # ---- frontend/tsconfig.json ----
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020", "DOM"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    with open(os.path.join(PROJECT, 'frontend', 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=4)

    # ---- frontend/package.json ----
    package_json = {
        "name": "inventory-dashboard",
        "version": "1.0.0",
        "description": "TypeScript frontend for inventory management",
        "main": "dist/index.js",
        "scripts": {
            "build": "tsc",
            "start": "node dist/index.js"
        },
        "dependencies": {},
        "devDependencies": {
            "typescript": "^5.3.0"
        }
    }
    with open(os.path.join(PROJECT, 'frontend', 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=4)

    # ---- native/lib.c ----
    native_lib = '''\
/**
 * Native Performance Library — Shared C module
 * Provides optimized array operations called via FFI from
 * the Python backend for bulk inventory calculations.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_ITEMS 10000

typedef struct {
    int id;
    char name[128];
    double price;
    int quantity;
} InventoryItem;

static InventoryItem inventory[MAX_ITEMS];
static int inventory_count = 0;

/**
 * Add an item to the in-memory inventory cache.
 * Returns 0 on success, -1 if cache is full.
 */
int add_item(int id, const char *name, double price, int quantity) {
    if (inventory_count >= MAX_ITEMS) {
        fprintf(stderr, "Inventory cache full (max %d items)\\n", MAX_ITEMS);
        return -1;
    }
    InventoryItem *item = &inventory[inventory_count++];
    item->id = id;
    strncpy(item->name, name, sizeof(item->name) - 1);
    item->name[sizeof(item->name) - 1] = '\\0';
    item->price = price;
    item->quantity = quantity;
    return 0;
}

/**
 * Calculate the total value of all inventory items.
 */
double total_inventory_value(void) {
    double total = 0.0;
    for (int i = 0; i < inventory_count; i++) {
        total += inventory[i].price * inventory[i].quantity;
    }
    return total;
}

/**
 * Find the item with the highest stock value (price * quantity).
 * Returns the item ID, or -1 if inventory is empty.
 */
int highest_value_item(void) {
    if (inventory_count == 0) return -1;

    int best_idx = 0;
    double best_val = inventory[0].price * inventory[0].quantity;

    for (int i = 1; i < inventory_count; i++) {
        double val = inventory[i].price * inventory[i].quantity;
        if (val > best_val) {
            best_val = val;
            best_idx = i;
        }
    }
    return inventory[best_idx].id;
}

/**
 * Apply a percentage discount to all items above a given price threshold.
 * Returns the number of items affected.
 */
int apply_bulk_discount(double threshold, double discount_pct) {
    int affected = 0;
    double multiplier = 1.0 - (discount_pct / 100.0);
    for (int i = 0; i < inventory_count; i++) {
        if (inventory[i].price > threshold) {
            inventory[i].price *= multiplier;
            affected++;
        }
    }
    return affected;
}

/**
 * Reset the inventory cache.
 */
void clear_inventory(void) {
    inventory_count = 0;
    memset(inventory, 0, sizeof(inventory));
}

int main(void) {
    printf("Inventory native library loaded.\\n");
    add_item(1, "Wireless Mouse", 29.99, 150);
    add_item(2, "Mechanical Keyboard", 89.50, 75);
    add_item(3, "USB-C Hub", 45.00, 200);
    add_item(4, "Monitor Stand", 120.00, 30);

    printf("Total inventory value: $%.2f\\n", total_inventory_value());
    printf("Highest value item ID: %d\\n", highest_value_item());

    int discounted = apply_bulk_discount(50.0, 10.0);
    printf("Discounted %d items above $50\\n", discounted);
    printf("New total value: $%.2f\\n", total_inventory_value());

    clear_inventory();
    return 0;
}
'''
    with open(os.path.join(PROJECT, 'native', 'lib.c'), 'w') as f:
        f.write(native_lib)

    # ---- native/Makefile ----
    makefile = '''\
CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = lib

all: $(TARGET)

$(TARGET): lib.c
\t$(CC) $(CFLAGS) -o $(TARGET) lib.c -lm

debug: lib.c
\t$(CC) $(CFLAGS) -ggdb3 -o $(TARGET) lib.c -lm

clean:
\trm -f $(TARGET)

.PHONY: all debug clean
'''
    with open(os.path.join(PROJECT, 'native', 'Makefile'), 'w') as f:
        f.write(makefile)

    # ---- Ensure .vscode dir exists but NO launch.json ----
    vscode_dir = os.path.join(PROJECT, '.vscode')
    launch_json_path = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Initial project created at: {PROJECT}')
    print('Directory structure:')
    for root, dirs, files in os.walk(PROJECT):
        level = root.replace(PROJECT, '').count(os.sep)
        indent = '  ' * level
        print(f'{indent}{os.path.basename(root)}/')
        sub_indent = '  ' * (level + 1)
        for fname in files:
            print(f'{sub_indent}{fname}')

    # ---- Compile native library for debugging ----
    subprocess.run(['gcc', '-g', '-Wall', '-O0', '-o',
                    os.path.join(PROJECT, 'native', 'lib'),
                    os.path.join(PROJECT, 'native', 'lib.c'), '-lm'],
                   capture_output=True)
    print('Native library compiled with debug symbols.')

    # ---- GUI: Open VSCode with the project folder ----
    launch_gui(f'code "{PROJECT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
