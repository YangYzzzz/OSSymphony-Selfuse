"""
Initial Setup: Configure rust-analyzer custom feature flag
Task ID: vscode_lang_044
Domain: vscode

Creates a Rust project with a Cargo.toml defining [features] test-utils = ["mockall"],
source code gated behind #[cfg(feature = "test-utils")], and opens VSCode.
No rust-analyzer.cargo.features setting exists yet.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_044'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
SRC_DIR = f'{PROJECT_DIR}/src'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    # Create project directories
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- Cargo.toml ---
    cargo_toml = """\
[package]
name = "inventory-manager"
version = "0.3.1"
edition = "2021"
authors = ["Sarah Chen <sarah.chen@example.com>"]
description = "A lightweight inventory management library for warehouse automation"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
chrono = "0.4"
uuid = { version = "1.0", features = ["v4"] }
thiserror = "1.0"

[dev-dependencies]
mockall = "0.11"
tokio = { version = "1.0", features = ["full"] }

[features]
default = []
test-utils = ["mockall"]
async-runtime = ["tokio"]
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)

    # --- src/lib.rs ---
    lib_rs = """\
//! Inventory Manager - Core Library
//!
//! Provides inventory tracking, stock management, and warehouse operations
//! for the automated fulfillment pipeline.

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Represents a single item in the warehouse inventory.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InventoryItem {
    pub id: Uuid,
    pub sku: String,
    pub name: String,
    pub quantity: u32,
    pub unit_price: f64,
    pub warehouse_zone: WarehouseZone,
    pub last_restocked: DateTime<Utc>,
}

/// Warehouse zones for item categorization.
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq)]
pub enum WarehouseZone {
    Electronics,
    Perishables,
    Oversized,
    HazardousMaterials,
    General,
}

/// Errors that can occur during inventory operations.
#[derive(Debug, thiserror::Error)]
pub enum InventoryError {
    #[error("Item not found: {sku}")]
    ItemNotFound { sku: String },
    #[error("Insufficient stock for SKU {sku}: requested {requested}, available {available}")]
    InsufficientStock {
        sku: String,
        requested: u32,
        available: u32,
    },
    #[error("Duplicate SKU: {0}")]
    DuplicateSku(String),
}

/// Core inventory management trait.
pub trait InventoryStore {
    fn add_item(&mut self, item: InventoryItem) -> Result<(), InventoryError>;
    fn remove_item(&mut self, sku: &str) -> Result<InventoryItem, InventoryError>;
    fn get_item(&self, sku: &str) -> Result<&InventoryItem, InventoryError>;
    fn update_quantity(&mut self, sku: &str, delta: i32) -> Result<u32, InventoryError>;
    fn items_by_zone(&self, zone: WarehouseZone) -> Vec<&InventoryItem>;
    fn total_value(&self) -> f64;
}

/// In-memory inventory store implementation.
pub struct MemoryStore {
    items: Vec<InventoryItem>,
}

impl MemoryStore {
    pub fn new() -> Self {
        Self { items: Vec::new() }
    }
}

impl InventoryStore for MemoryStore {
    fn add_item(&mut self, item: InventoryItem) -> Result<(), InventoryError> {
        if self.items.iter().any(|i| i.sku == item.sku) {
            return Err(InventoryError::DuplicateSku(item.sku));
        }
        self.items.push(item);
        Ok(())
    }

    fn remove_item(&mut self, sku: &str) -> Result<InventoryItem, InventoryError> {
        let pos = self
            .items
            .iter()
            .position(|i| i.sku == sku)
            .ok_or_else(|| InventoryError::ItemNotFound {
                sku: sku.to_string(),
            })?;
        Ok(self.items.remove(pos))
    }

    fn get_item(&self, sku: &str) -> Result<&InventoryItem, InventoryError> {
        self.items
            .iter()
            .find(|i| i.sku == sku)
            .ok_or_else(|| InventoryError::ItemNotFound {
                sku: sku.to_string(),
            })
    }

    fn update_quantity(&mut self, sku: &str, delta: i32) -> Result<u32, InventoryError> {
        let item = self
            .items
            .iter_mut()
            .find(|i| i.sku == sku)
            .ok_or_else(|| InventoryError::ItemNotFound {
                sku: sku.to_string(),
            })?;
        let new_qty = (item.quantity as i32 + delta).max(0) as u32;
        if delta < 0 && (-delta as u32) > item.quantity {
            return Err(InventoryError::InsufficientStock {
                sku: sku.to_string(),
                requested: (-delta) as u32,
                available: item.quantity,
            });
        }
        item.quantity = new_qty;
        Ok(new_qty)
    }

    fn items_by_zone(&self, zone: WarehouseZone) -> Vec<&InventoryItem> {
        self.items
            .iter()
            .filter(|i| i.warehouse_zone == zone)
            .collect()
    }

    fn total_value(&self) -> f64 {
        self.items
            .iter()
            .map(|i| i.quantity as f64 * i.unit_price)
            .sum()
    }
}

// === Test utilities (feature-gated) ===
#[cfg(feature = "test-utils")]
pub mod test_helpers {
    use super::*;
    use mockall::mock;

    mock! {
        pub Store {}
        impl InventoryStore for Store {
            fn add_item(&mut self, item: InventoryItem) -> Result<(), InventoryError>;
            fn remove_item(&mut self, sku: &str) -> Result<InventoryItem, InventoryError>;
            fn get_item(&self, sku: &str) -> Result<&InventoryItem, InventoryError>;
            fn update_quantity(&mut self, sku: &str, delta: i32) -> Result<u32, InventoryError>;
            fn items_by_zone(&self, zone: WarehouseZone) -> Vec<&InventoryItem>;
            fn total_value(&self) -> f64;
        }
    }

    /// Create a sample inventory item for testing.
    pub fn sample_item(sku: &str, name: &str, qty: u32, price: f64) -> InventoryItem {
        InventoryItem {
            id: uuid::Uuid::new_v4(),
            sku: sku.to_string(),
            name: name.to_string(),
            quantity: qty,
            unit_price: price,
            warehouse_zone: WarehouseZone::General,
            last_restocked: chrono::Utc::now(),
        }
    }

    /// Build a pre-populated store with common test data.
    pub fn populated_store() -> MemoryStore {
        let mut store = MemoryStore::new();
        store.add_item(sample_item("WH-1001", "Industrial Sensor Pack", 150, 34.99)).unwrap();
        store.add_item(sample_item("WH-1002", "Pallet Jack Wheels (Set of 4)", 42, 89.50)).unwrap();
        store.add_item(sample_item("WH-1003", "Safety Goggles - Anti-Fog", 500, 12.75)).unwrap();
        store.add_item(sample_item("WH-1004", "Barcode Scanner Module", 75, 245.00)).unwrap();
        store
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_and_retrieve() {
        let mut store = MemoryStore::new();
        let item = InventoryItem {
            id: Uuid::new_v4(),
            sku: "TEST-001".to_string(),
            name: "Test Widget".to_string(),
            quantity: 10,
            unit_price: 5.99,
            warehouse_zone: WarehouseZone::General,
            last_restocked: Utc::now(),
        };
        store.add_item(item).unwrap();
        let retrieved = store.get_item("TEST-001").unwrap();
        assert_eq!(retrieved.quantity, 10);
    }

    #[test]
    fn test_total_value() {
        let mut store = MemoryStore::new();
        let item1 = InventoryItem {
            id: Uuid::new_v4(),
            sku: "TV-001".to_string(),
            name: "Flat Screen TV".to_string(),
            quantity: 3,
            unit_price: 499.99,
            warehouse_zone: WarehouseZone::Electronics,
            last_restocked: Utc::now(),
        };
        let item2 = InventoryItem {
            id: Uuid::new_v4(),
            sku: "KB-002".to_string(),
            name: "Mechanical Keyboard".to_string(),
            quantity: 20,
            unit_price: 79.99,
            warehouse_zone: WarehouseZone::Electronics,
            last_restocked: Utc::now(),
        };
        store.add_item(item1).unwrap();
        store.add_item(item2).unwrap();
        let total = store.total_value();
        assert!((total - 3099.77).abs() < 0.01);
    }
}
"""
    with open(f'{SRC_DIR}/lib.rs', 'w') as f:
        f.write(lib_rs)

    # --- .vscode/settings.json (initial: NO rust-analyzer.cargo.features) ---
    vscode_settings = {
        "editor.formatOnSave": True,
        "editor.tabSize": 4,
        "rust-analyzer.checkOnSave.command": "clippy",
        "rust-analyzer.inlayHints.parameterHints.enable": True,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Initial Rust project created: {PROJECT_DIR}')
    print(f'  Cargo.toml: features defined with test-utils')
    print(f'  src/lib.rs: code with #[cfg(feature = "test-utils")] block')
    print(f'  .vscode/settings.json: no rust-analyzer.cargo.features set')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
