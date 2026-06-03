"""
Initial Setup: Create a Rust project workspace for VSCode tasks.json configuration task.
Task ID: vscode_td_037
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_037'
PROJECT_DIR = f'{WORKDIR}/projects/rust-web'

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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    # Ensure NO .vscode folder exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    # Create Cargo.toml
    cargo_toml = """\
[package]
name = "rust-web"
version = "0.1.0"
edition = "2021"
authors = ["Elena Rodriguez <elena@rustdev.io>"]
description = "A lightweight web server built with Actix-web"

[dependencies]
actix-web = "4.4"
actix-rt = "2.9"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1.34", features = ["full"] }
env_logger = "0.10"
log = "0.4"

[dev-dependencies]
actix-test = "0.1"
reqwest = { version = "0.11", features = ["json"] }
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)

    # Create src/main.rs
    main_rs = """\
use actix_web::{web, App, HttpServer, HttpResponse, middleware};
use serde::{Deserialize, Serialize};
use std::sync::Mutex;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Task {
    id: u32,
    title: String,
    completed: bool,
}

struct AppState {
    tasks: Mutex<Vec<Task>>,
}

async fn get_tasks(data: web::Data<AppState>) -> HttpResponse {
    let tasks = data.tasks.lock().unwrap();
    HttpResponse::Ok().json(tasks.clone())
}

async fn add_task(
    data: web::Data<AppState>,
    task: web::Json<Task>,
) -> HttpResponse {
    let mut tasks = data.tasks.lock().unwrap();
    tasks.push(task.into_inner());
    HttpResponse::Created().json(tasks.clone())
}

async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({"status": "healthy"}))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
    log::info!("Starting rust-web server on port 8080");

    let data = web::Data::new(AppState {
        tasks: Mutex::new(vec![
            Task { id: 1, title: "Set up CI pipeline".to_string(), completed: false },
            Task { id: 2, title: "Write API documentation".to_string(), completed: false },
        ]),
    });

    HttpServer::new(move || {
        App::new()
            .app_data(data.clone())
            .route("/health", web::get().to(health_check))
            .route("/tasks", web::get().to(get_tasks))
            .route("/tasks", web::post().to(add_task))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
"""
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(main_rs)

    # Create tests/integration_test.rs
    test_rs = """\
use std::sync::Mutex;

#[cfg(test)]
mod tests {
    #[test]
    fn test_task_creation() {
        let task_title = "Deploy to staging";
        assert!(!task_title.is_empty());
        assert_eq!(task_title.len(), 17);
        println!("Task '{}' created successfully", task_title);
    }

    #[test]
    fn test_task_completion_toggle() {
        let mut completed = false;
        completed = !completed;
        assert!(completed);
        println!("Task completion toggled to: {}", completed);
    }

    #[test]
    fn test_health_endpoint_format() {
        let response = serde_json::json!({"status": "healthy"});
        assert_eq!(response["status"], "healthy");
        println!("Health check response: {}", response);
    }
}
"""
    with open(f'{PROJECT_DIR}/tests/integration_test.rs', 'w') as f:
        f.write(test_rs)

    print(f'Rust project created at: {PROJECT_DIR}')
    print(f'  - Cargo.toml')
    print(f'  - src/main.rs')
    print(f'  - tests/integration_test.rs')
    print(f'  - No .vscode directory')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
