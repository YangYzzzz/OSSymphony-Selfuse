"""
Initial Setup: Configure Rust Analyzer extension settings in VSCode
Task ID: vscode_we_083
Domain: vscode

Creates a Rust project workspace and opens VSCode with empty user settings.
The rust-analyzer extension should already be installed on the VM image.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_083'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')


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


def create_rust_project():
    """Create a realistic Rust project structure."""
    src_dir = os.path.join(WORKSPACE_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)

    # Cargo.toml
    cargo_toml = """\
[package]
name = "inventory-manager"
version = "0.3.1"
edition = "2021"
authors = ["Sarah Chen <sarah.chen@techcorp.io>"]
description = "A warehouse inventory management system with REST API"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1", features = ["full"] }
axum = "0.7"
sqlx = { version = "0.7", features = ["runtime-tokio-rustls", "postgres"] }
tracing = "0.1"
tracing-subscriber = "0.3"
chrono = { version = "0.4", features = ["serde"] }
uuid = { version = "1", features = ["v4", "serde"] }
thiserror = "1.0"

[dev-dependencies]
tower = { version = "0.4", features = ["util"] }
hyper = { version = "1", features = ["full"] }

[features]
default = ["postgres"]
postgres = ["sqlx/postgres"]
mysql = ["sqlx/mysql"]
audit-log = []
"""
    with open(os.path.join(WORKSPACE_DIR, 'Cargo.toml'), 'w') as f:
        f.write(cargo_toml)

    # src/main.rs
    main_rs = """\
use axum::{routing::get, Router, Json};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use std::sync::Arc;
use tracing::info;

#[derive(Debug, Serialize, Deserialize)]
struct InventoryItem {
    id: uuid::Uuid,
    name: String,
    sku: String,
    quantity: i32,
    unit_price: f64,
    warehouse_location: String,
    last_updated: chrono::NaiveDateTime,
}

#[derive(Debug, Serialize, Deserialize)]
struct CreateItemRequest {
    name: String,
    sku: String,
    quantity: i32,
    unit_price: f64,
    warehouse_location: String,
}

struct AppState {
    db: PgPool,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let database_url = std::env::var("DATABASE_URL")
        .unwrap_or_else(|_| "postgres://localhost/inventory".to_string());

    let pool = PgPool::connect(&database_url).await?;
    let state = Arc::new(AppState { db: pool });

    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/items", get(list_items).post(create_item))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    info!("Server starting on port 3000");
    axum::serve(listener, app).await?;

    Ok(())
}

async fn health_check() -> &'static str {
    "OK"
}

async fn list_items(
    axum::extract::State(state): axum::extract::State<Arc<AppState>>,
) -> Json<Vec<InventoryItem>> {
    let items = sqlx::query_as!(
        InventoryItem,
        "SELECT id, name, sku, quantity, unit_price, warehouse_location, last_updated FROM items ORDER BY name"
    )
    .fetch_all(&state.db)
    .await
    .unwrap_or_default();

    Json(items)
}

async fn create_item(
    axum::extract::State(state): axum::extract::State<Arc<AppState>>,
    Json(req): Json<CreateItemRequest>,
) -> Json<InventoryItem> {
    let item = sqlx::query_as!(
        InventoryItem,
        r#"
        INSERT INTO items (id, name, sku, quantity, unit_price, warehouse_location, last_updated)
        VALUES ($1, $2, $3, $4, $5, $6, NOW())
        RETURNING id, name, sku, quantity, unit_price, warehouse_location, last_updated
        "#,
        uuid::Uuid::new_v4(),
        req.name,
        req.sku,
        req.quantity,
        req.unit_price,
        req.warehouse_location,
    )
    .fetch_one(&state.db)
    .await
    .expect("Failed to insert item");

    Json(item)
}
"""
    with open(os.path.join(src_dir, 'main.rs'), 'w') as f:
        f.write(main_rs)

    # src/lib.rs - additional module
    lib_rs = """\
pub mod models;
pub mod errors;

use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("Item not found: {0}")]
    NotFound(uuid::Uuid),
    #[error("Validation error: {0}")]
    Validation(String),
}
"""
    with open(os.path.join(src_dir, 'lib.rs'), 'w') as f:
        f.write(lib_rs)

    print(f"Rust project created at {WORKSPACE_DIR}")


def setup_vscode_settings():
    """Ensure VSCode user settings are empty (no rust-analyzer config)."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    # Write empty settings - no rust-analyzer configuration
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f"VSCode settings reset to empty: {SETTINGS_PATH}")


def main():
    create_rust_project()
    setup_vscode_settings()

    # Launch VSCode with the Rust workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with Rust workspace on DISPLAY=:0')


main()
