"""
Initial Setup: Enable and configure Rust test coverage display using Coverage Gutters
Task ID: vscode_lang_047
Domain: vscode

Creates a Rust project with tests, installs cargo-tarpaulin and Coverage Gutters
extension (unconfigured). No coverage data exists yet.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_047'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


def run(cmd, check=True, timeout=60, **kwargs):
    """Run a shell command with error handling."""
    print(f'  CMD: {cmd}')
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        timeout=timeout, **kwargs
    )
    if result.stdout.strip():
        print(f'  OUT: {result.stdout.strip()[:500]}')
    if result.stderr.strip():
        print(f'  ERR: {result.stderr.strip()[:500]}')
    if check and result.returncode != 0:
        raise RuntimeError(f'Command failed ({result.returncode}): {cmd}\n{result.stderr}')
    return result


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


def ensure_rust():
    """Ensure Rust is available on PATH."""
    os.environ['PATH'] = f'{WORKDIR}/.cargo/bin:' + os.environ.get('PATH', '')
    run('rustc --version')
    run('cargo --version')
    run('cargo tarpaulin --version')


def create_rust_project():
    """Create a Rust project with meaningful code and tests."""
    print("Creating Rust project...")
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Cargo.toml
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write("""[package]
name = "inventory_tracker"
version = "0.1.0"
edition = "2021"
description = "A simple inventory tracking library for a retail store"

[dependencies]
""")

    # src/lib.rs - a realistic library with testable functions
    with open(f'{PROJECT_DIR}/src/lib.rs', 'w') as f:
        f.write(r'''/// Represents a product in the inventory
#[derive(Debug, Clone, PartialEq)]
pub struct Product {
    pub name: String,
    pub sku: String,
    pub price: f64,
    pub quantity: u32,
}

impl Product {
    pub fn new(name: &str, sku: &str, price: f64, quantity: u32) -> Self {
        Product {
            name: name.to_string(),
            sku: sku.to_string(),
            price,
            quantity,
        }
    }

    pub fn total_value(&self) -> f64 {
        self.price * self.quantity as f64
    }

    pub fn restock(&mut self, amount: u32) {
        self.quantity += amount;
    }

    pub fn sell(&mut self, amount: u32) -> Result<u32, String> {
        if amount > self.quantity {
            Err(format!(
                "Insufficient stock for {}: requested {}, available {}",
                self.name, amount, self.quantity
            ))
        } else {
            self.quantity -= amount;
            Ok(self.quantity)
        }
    }
}

/// Manages a collection of products
pub struct Inventory {
    products: Vec<Product>,
}

impl Inventory {
    pub fn new() -> Self {
        Inventory {
            products: Vec::new(),
        }
    }

    pub fn add_product(&mut self, product: Product) {
        self.products.push(product);
    }

    pub fn find_by_sku(&self, sku: &str) -> Option<&Product> {
        self.products.iter().find(|p| p.sku == sku)
    }

    pub fn total_inventory_value(&self) -> f64 {
        self.products.iter().map(|p| p.total_value()).sum()
    }

    pub fn low_stock_products(&self, threshold: u32) -> Vec<&Product> {
        self.products
            .iter()
            .filter(|p| p.quantity < threshold)
            .collect()
    }

    pub fn product_count(&self) -> usize {
        self.products.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_product_creation() {
        let product = Product::new("Wireless Mouse", "WM-001", 29.99, 150);
        assert_eq!(product.name, "Wireless Mouse");
        assert_eq!(product.sku, "WM-001");
        assert_eq!(product.price, 29.99);
        assert_eq!(product.quantity, 150);
    }

    #[test]
    fn test_total_value() {
        let product = Product::new("USB Cable", "UC-100", 9.99, 50);
        let value = product.total_value();
        assert!((value - 499.50).abs() < 0.01);
    }

    #[test]
    fn test_restock() {
        let mut product = Product::new("Keyboard", "KB-200", 49.99, 30);
        product.restock(20);
        assert_eq!(product.quantity, 50);
    }

    #[test]
    fn test_sell_success() {
        let mut product = Product::new("Monitor", "MN-300", 299.99, 10);
        let result = product.sell(3);
        assert_eq!(result, Ok(7));
        assert_eq!(product.quantity, 7);
    }

    #[test]
    fn test_sell_insufficient_stock() {
        let mut product = Product::new("Laptop Stand", "LS-050", 45.00, 5);
        let result = product.sell(10);
        assert!(result.is_err());
        assert_eq!(product.quantity, 5);
    }

    #[test]
    fn test_inventory_add_and_find() {
        let mut inv = Inventory::new();
        inv.add_product(Product::new("Headphones", "HP-400", 79.99, 25));
        inv.add_product(Product::new("Webcam", "WC-150", 59.99, 40));

        let found = inv.find_by_sku("HP-400");
        assert!(found.is_some());
        assert_eq!(found.unwrap().name, "Headphones");

        let not_found = inv.find_by_sku("XX-999");
        assert!(not_found.is_none());
    }

    #[test]
    fn test_inventory_total_value() {
        let mut inv = Inventory::new();
        inv.add_product(Product::new("Mouse Pad", "MP-010", 12.99, 100));
        inv.add_product(Product::new("USB Hub", "UH-020", 24.99, 60));
        let total = inv.total_inventory_value();
        assert!((total - 2798.40).abs() < 0.01);
    }

    #[test]
    fn test_low_stock_products() {
        let mut inv = Inventory::new();
        inv.add_product(Product::new("Cable Organizer", "CO-001", 8.99, 3));
        inv.add_product(Product::new("Desk Lamp", "DL-002", 34.99, 50));
        inv.add_product(Product::new("Screen Cleaner", "SC-003", 5.99, 7));

        let low = inv.low_stock_products(10);
        assert_eq!(low.len(), 2);
    }
}
''')

    # src/main.rs
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(r'''use inventory_tracker::{Inventory, Product};

fn main() {
    let mut inventory = Inventory::new();

    inventory.add_product(Product::new("Wireless Mouse", "WM-001", 29.99, 150));
    inventory.add_product(Product::new("Mechanical Keyboard", "KB-200", 89.99, 45));
    inventory.add_product(Product::new("4K Monitor", "MN-300", 349.99, 12));
    inventory.add_product(Product::new("USB-C Hub", "UH-020", 24.99, 80));
    inventory.add_product(Product::new("Laptop Stand", "LS-050", 45.00, 5));

    println!("=== Inventory Report ===");
    println!("Total products: {}", inventory.product_count());
    println!("Total value: ${:.2}", inventory.total_inventory_value());

    let low_stock = inventory.low_stock_products(15);
    println!("\nLow stock items (< 15 units):");
    for product in low_stock {
        println!("  - {} (SKU: {}): {} units", product.name, product.sku, product.quantity);
    }
}
''')

    print(f'Rust project created at {PROJECT_DIR}')


def install_coverage_gutters():
    """Install Coverage Gutters extension but do NOT configure it."""
    print("Installing Coverage Gutters extension...")
    run('code --install-extension ryanluker.vscode-coverage-gutters --force', timeout=60)
    print("Coverage Gutters extension installed (unconfigured)")


def setup_initial():
    ensure_rust()
    create_rust_project()

    # Build the project first so it's ready
    print("Building project...")
    run(f'cd {PROJECT_DIR} && cargo build', timeout=120)

    install_coverage_gutters()

    # DO NOT configure coverage gutters settings - that's the task
    # DO NOT generate lcov.info - that's the task
    # Make sure no lcov.info exists
    lcov_path = f'{PROJECT_DIR}/lcov.info'
    if os.path.exists(lcov_path):
        os.remove(lcov_path)
        print("Removed stale lcov.info")

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with Rust project')


setup_initial()
