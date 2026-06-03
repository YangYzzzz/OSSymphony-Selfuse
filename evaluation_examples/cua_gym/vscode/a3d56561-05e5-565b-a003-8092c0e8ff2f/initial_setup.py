"""
Initial Setup: Configure VSCode with a Rust workspace where rust-analyzer is memory-heavy
Task ID: vscode_fix_062
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

HOME = '/home/user'
WORKSPACE = os.path.join(HOME, 'workspace')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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


def create_rust_workspace():
    """Create a realistic large Rust workspace."""
    os.makedirs(os.path.join(WORKSPACE, 'src'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'src', 'handlers'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'src', 'models'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'src', 'utils'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'tests'), exist_ok=True)

    # Cargo.toml with many dependencies
    cargo_toml = '''\
[package]
name = "inventory-service"
version = "0.4.2"
edition = "2021"
authors = ["Sarah Chen <sarah.chen@acmecorp.io>", "Marcus Johnson <marcus.j@acmecorp.io>"]
description = "High-performance inventory management microservice for AcmeCorp"

[dependencies]
actix-web = "4.4"
actix-rt = "2.9"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1.34", features = ["full"] }
sqlx = { version = "0.7", features = ["runtime-tokio-rustls", "postgres", "chrono", "uuid"] }
chrono = { version = "0.4", features = ["serde"] }
uuid = { version = "1.6", features = ["v4", "serde"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
thiserror = "1.0"
config = "0.14"
dotenv = "0.15"
reqwest = { version = "0.11", features = ["json"] }
redis = { version = "0.24", features = ["tokio-comp"] }
jsonwebtoken = "9.2"

[dev-dependencies]
actix-rt = "2.9"
mockall = "0.12"
criterion = { version = "0.5", features = ["html_reports"] }

[[bench]]
name = "inventory_bench"
harness = false
'''
    with open(os.path.join(WORKSPACE, 'Cargo.toml'), 'w') as f:
        f.write(cargo_toml)

    # src/main.rs
    main_rs = '''\
use actix_web::{web, App, HttpServer, middleware};
use tracing_subscriber::EnvFilter;

mod handlers;
mod models;
mod utils;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();
    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env())
        .init();

    let db_pool = sqlx::postgres::PgPoolOptions::new()
        .max_connections(20)
        .connect(&std::env::var("DATABASE_URL").expect("DATABASE_URL must be set"))
        .await
        .expect("Failed to create pool");

    let redis_client = redis::Client::open(
        std::env::var("REDIS_URL").unwrap_or_else(|_| "redis://127.0.0.1/".to_string())
    ).expect("Invalid Redis URL");

    tracing::info!("Starting inventory service on port 8080");

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(db_pool.clone()))
            .app_data(web::Data::new(redis_client.clone()))
            .configure(handlers::inventory::config)
            .configure(handlers::auth::config)
            .configure(handlers::health::config)
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
'''
    with open(os.path.join(WORKSPACE, 'src', 'main.rs'), 'w') as f:
        f.write(main_rs)

    # src/handlers/mod.rs
    with open(os.path.join(WORKSPACE, 'src', 'handlers', 'mod.rs'), 'w') as f:
        f.write('pub mod inventory;\npub mod auth;\npub mod health;\n')

    # src/handlers/inventory.rs
    inventory_rs = '''\
use actix_web::{web, HttpResponse, get, post, put, delete};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow)]
pub struct InventoryItem {
    pub id: Uuid,
    pub sku: String,
    pub name: String,
    pub description: Option<String>,
    pub quantity: i32,
    pub unit_price: f64,
    pub warehouse_id: Uuid,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Deserialize)]
pub struct CreateItemRequest {
    pub sku: String,
    pub name: String,
    pub description: Option<String>,
    pub quantity: i32,
    pub unit_price: f64,
    pub warehouse_id: Uuid,
}

#[get("/api/v1/inventory")]
async fn list_items(pool: web::Data<PgPool>) -> HttpResponse {
    match sqlx::query_as::<_, InventoryItem>("SELECT * FROM inventory_items ORDER BY created_at DESC")
        .fetch_all(pool.get_ref())
        .await
    {
        Ok(items) => HttpResponse::Ok().json(items),
        Err(e) => {
            tracing::error!("Failed to fetch inventory: {}", e);
            HttpResponse::InternalServerError().json(serde_json::json!({"error": "Database error"}))
        }
    }
}

#[post("/api/v1/inventory")]
async fn create_item(pool: web::Data<PgPool>, item: web::Json<CreateItemRequest>) -> HttpResponse {
    let id = Uuid::new_v4();
    let now = Utc::now();
    match sqlx::query(
        "INSERT INTO inventory_items (id, sku, name, description, quantity, unit_price, warehouse_id, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)"
    )
    .bind(id).bind(&item.sku).bind(&item.name).bind(&item.description)
    .bind(item.quantity).bind(item.unit_price).bind(item.warehouse_id)
    .bind(now).bind(now)
    .execute(pool.get_ref())
    .await
    {
        Ok(_) => HttpResponse::Created().json(serde_json::json!({"id": id})),
        Err(e) => {
            tracing::error!("Failed to create item: {}", e);
            HttpResponse::InternalServerError().json(serde_json::json!({"error": "Failed to create item"}))
        }
    }
}

pub fn config(cfg: &mut web::ServiceConfig) {
    cfg.service(list_items).service(create_item);
}
'''
    with open(os.path.join(WORKSPACE, 'src', 'handlers', 'inventory.rs'), 'w') as f:
        f.write(inventory_rs)

    # src/handlers/auth.rs
    auth_rs = '''\
use actix_web::{web, HttpResponse, post};
use jsonwebtoken::{encode, Header, EncodingKey};
use serde::{Deserialize, Serialize};
use chrono::{Utc, Duration};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
    iat: usize,
    role: String,
}

#[derive(Debug, Deserialize)]
pub struct LoginRequest {
    pub username: String,
    pub password: String,
}

#[post("/api/v1/auth/login")]
async fn login(creds: web::Json<LoginRequest>) -> HttpResponse {
    // Simplified auth for demo
    if creds.username == "admin" && creds.password == "secret" {
        let now = Utc::now();
        let claims = Claims {
            sub: creds.username.clone(),
            exp: (now + Duration::hours(24)).timestamp() as usize,
            iat: now.timestamp() as usize,
            role: "admin".to_string(),
        };
        let secret = std::env::var("JWT_SECRET").unwrap_or_else(|_| "dev-secret".to_string());
        match encode(&Header::default(), &claims, &EncodingKey::from_secret(secret.as_bytes())) {
            Ok(token) => HttpResponse::Ok().json(serde_json::json!({"token": token})),
            Err(_) => HttpResponse::InternalServerError().json(serde_json::json!({"error": "Token generation failed"})),
        }
    } else {
        HttpResponse::Unauthorized().json(serde_json::json!({"error": "Invalid credentials"}))
    }
}

pub fn config(cfg: &mut web::ServiceConfig) {
    cfg.service(login);
}
'''
    with open(os.path.join(WORKSPACE, 'src', 'handlers', 'auth.rs'), 'w') as f:
        f.write(auth_rs)

    # src/handlers/health.rs
    health_rs = '''\
use actix_web::{get, HttpResponse};

#[get("/health")]
async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({"status": "healthy", "version": env!("CARGO_PKG_VERSION")}))
}

pub fn config(cfg: &mut web::ServiceConfig) {
    cfg.service(health_check);
}
'''
    with open(os.path.join(WORKSPACE, 'src', 'handlers', 'health.rs'), 'w') as f:
        f.write(health_rs)

    # src/models/mod.rs
    with open(os.path.join(WORKSPACE, 'src', 'models', 'mod.rs'), 'w') as f:
        f.write('pub mod warehouse;\n')

    # src/models/warehouse.rs
    warehouse_rs = '''\
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow)]
pub struct Warehouse {
    pub id: Uuid,
    pub name: String,
    pub location: String,
    pub capacity: i32,
    pub current_utilization: f64,
}
'''
    with open(os.path.join(WORKSPACE, 'src', 'models', 'warehouse.rs'), 'w') as f:
        f.write(warehouse_rs)

    # src/utils/mod.rs
    with open(os.path.join(WORKSPACE, 'src', 'utils', 'mod.rs'), 'w') as f:
        f.write('pub mod cache;\n')

    # src/utils/cache.rs
    cache_rs = '''\
use redis::AsyncCommands;
use serde::{de::DeserializeOwned, Serialize};

pub async fn get_cached<T: DeserializeOwned>(
    client: &redis::Client,
    key: &str,
) -> Option<T> {
    let mut conn = client.get_multiplexed_tokio_connection().await.ok()?;
    let data: Option<String> = conn.get(key).await.ok()?;
    data.and_then(|s| serde_json::from_str(&s).ok())
}

pub async fn set_cached<T: Serialize>(
    client: &redis::Client,
    key: &str,
    value: &T,
    ttl_seconds: u64,
) -> Result<(), Box<dyn std::error::Error>> {
    let mut conn = client.get_multiplexed_tokio_connection().await?;
    let serialized = serde_json::to_string(value)?;
    conn.set_ex(key, serialized, ttl_seconds).await?;
    Ok(())
}
'''
    with open(os.path.join(WORKSPACE, 'src', 'utils', 'cache.rs'), 'w') as f:
        f.write(cache_rs)

    # Cargo.lock placeholder
    with open(os.path.join(WORKSPACE, 'Cargo.lock'), 'w') as f:
        f.write('# This file is automatically @generated by Cargo.\n# It is not intended for manual editing.\nversion = 3\n')

    # .env file
    with open(os.path.join(WORKSPACE, '.env'), 'w') as f:
        f.write('DATABASE_URL=postgres://inventory:inv_pass_2024@localhost:5432/inventory_db\nREDIS_URL=redis://127.0.0.1:6379/\nJWT_SECRET=acmecorp-jwt-secret-key-2024\nRUST_LOG=info\n')

    print(f'Rust workspace created at: {WORKSPACE}')


def setup_vscode_settings():
    """Set up VSCode settings with rust-analyzer consuming too much memory."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start fresh
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Merge in the initial state settings
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "editor.minimap.enabled": True,
        "workbench.colorTheme": "Default Dark Modern",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "rust-analyzer.cargo.buildScripts.enable": True,
        "rust-analyzer.procMacro.enable": True,
        "rust-analyzer.cargo.allFeatures": True,
        "rust-analyzer.diagnostics.experimental.enable": True,
        "rust-analyzer.inlayHints.parameterHints.enable": True,
        "rust-analyzer.inlayHints.typeHints.enable": True,
        "rust-analyzer.checkOnSave.command": "clippy",
        "terminal.integrated.defaultProfile.linux": "bash",
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured at: {SETTINGS_PATH}')


def main():
    create_rust_workspace()
    setup_vscode_settings()

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
