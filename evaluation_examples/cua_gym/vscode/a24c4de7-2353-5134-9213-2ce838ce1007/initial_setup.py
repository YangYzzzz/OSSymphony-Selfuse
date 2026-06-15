"""
Initial Setup: Configure rust-analyzer to use nightly toolchain
Task ID: vscode_lang_035
Domain: vscode

Creates a Rust project that uses nightly features but currently has no
rust-toolchain.toml and no rust-analyzer nightly config. The agent must
configure the workspace to use the nightly toolchain.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_035'
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
    # Create project directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- Cargo.toml ---
    cargo_toml = """\
[package]
name = "sensor-dashboard"
version = "0.3.1"
edition = "2021"
authors = ["Elena Vasquez <elena.vasquez@sensortech.io>"]
description = "Real-time sensor data aggregation and dashboard service"

[dependencies]
tokio = { version = "1.35", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
chrono = "0.4"
uuid = { version = "1.6", features = ["v4"] }
thiserror = "1.0"
tracing = "0.1"
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)

    # --- src/main.rs --- uses nightly features that will error on stable
    main_rs = """\
#![feature(let_chains)]
#![feature(lazy_cell)]

use std::collections::HashMap;
use std::sync::LazyCell;

/// Global configuration loaded once at startup.
static CONFIG: LazyCell<SensorConfig> = LazyCell::new(|| {
    SensorConfig::from_env().expect("Failed to load sensor configuration")
});

#[derive(Debug, Clone)]
struct SensorReading {
    sensor_id: String,
    timestamp: u64,
    temperature: f64,
    humidity: f64,
    pressure: f64,
    status: SensorStatus,
}

#[derive(Debug, Clone, PartialEq)]
enum SensorStatus {
    Online,
    Degraded,
    Offline,
    Calibrating,
}

#[derive(Debug, Clone)]
struct SensorConfig {
    poll_interval_ms: u64,
    max_retries: u32,
    alert_threshold_temp: f64,
    alert_threshold_humidity: f64,
    data_retention_hours: u64,
}

impl SensorConfig {
    fn from_env() -> Result<Self, Box<dyn std::error::Error>> {
        Ok(SensorConfig {
            poll_interval_ms: 500,
            max_retries: 3,
            alert_threshold_temp: 85.0,
            alert_threshold_humidity: 95.0,
            data_retention_hours: 72,
        })
    }
}

/// Aggregate sensor readings and compute statistics.
fn aggregate_readings(readings: &[SensorReading]) -> HashMap<String, SensorStats> {
    let mut stats_map: HashMap<String, Vec<&SensorReading>> = HashMap::new();

    for reading in readings {
        stats_map
            .entry(reading.sensor_id.clone())
            .or_default()
            .push(reading);
    }

    let mut result = HashMap::new();
    for (sensor_id, sensor_readings) in &stats_map {
        let temps: Vec<f64> = sensor_readings.iter().map(|r| r.temperature).collect();
        let avg_temp = temps.iter().sum::<f64>() / temps.len() as f64;
        let max_temp = temps.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let min_temp = temps.iter().cloned().fold(f64::INFINITY, f64::min);

        // Using let-chains (nightly feature)
        let alert = if let Some(latest) = sensor_readings.last()
            && latest.temperature > CONFIG.alert_threshold_temp
        {
            true
        } else {
            false
        };

        result.insert(
            sensor_id.clone(),
            SensorStats {
                avg_temperature: avg_temp,
                max_temperature: max_temp,
                min_temperature: min_temp,
                reading_count: sensor_readings.len(),
                alert_triggered: alert,
            },
        );
    }

    result
}

#[derive(Debug)]
struct SensorStats {
    avg_temperature: f64,
    max_temperature: f64,
    min_temperature: f64,
    reading_count: usize,
    alert_triggered: bool,
}

/// Filter readings by status, returning only online or degraded sensors.
fn filter_active_readings(readings: &[SensorReading]) -> Vec<&SensorReading> {
    readings
        .iter()
        .filter(|r| {
            matches!(r.status, SensorStatus::Online | SensorStatus::Degraded)
        })
        .collect()
}

fn main() {
    println!("Sensor Dashboard v{}", env!("CARGO_PKG_VERSION"));
    println!("Configuration: {:?}", *CONFIG);

    let sample_readings = vec![
        SensorReading {
            sensor_id: "SENS-A100".to_string(),
            timestamp: 1704067200,
            temperature: 72.3,
            humidity: 45.2,
            pressure: 1013.25,
            status: SensorStatus::Online,
        },
        SensorReading {
            sensor_id: "SENS-A100".to_string(),
            timestamp: 1704067800,
            temperature: 73.1,
            humidity: 44.8,
            pressure: 1013.10,
            status: SensorStatus::Online,
        },
        SensorReading {
            sensor_id: "SENS-B205".to_string(),
            timestamp: 1704067200,
            temperature: 88.7,
            humidity: 62.1,
            pressure: 1012.90,
            status: SensorStatus::Degraded,
        },
        SensorReading {
            sensor_id: "SENS-C310".to_string(),
            timestamp: 1704067200,
            temperature: 65.4,
            humidity: 51.3,
            pressure: 1014.05,
            status: SensorStatus::Offline,
        },
    ];

    let active = filter_active_readings(&sample_readings);
    println!("Active sensors: {}", active.len());

    let stats = aggregate_readings(&sample_readings);
    for (id, s) in &stats {
        println!(
            "{}: avg={:.1}F, max={:.1}F, min={:.1}F, readings={}, alert={}",
            id, s.avg_temperature, s.max_temperature, s.min_temperature,
            s.reading_count, s.alert_triggered
        );
    }
}
"""
    with open(f'{SRC_DIR}/main.rs', 'w') as f:
        f.write(main_rs)

    # --- src/lib.rs --- additional module
    lib_rs = """\
#![feature(let_chains)]

use std::collections::HashMap;

/// Data store for time-series sensor readings with configurable retention.
pub struct TimeSeriesStore {
    data: HashMap<String, Vec<(u64, f64)>>,
    retention_seconds: u64,
}

impl TimeSeriesStore {
    pub fn new(retention_seconds: u64) -> Self {
        Self {
            data: HashMap::new(),
            retention_seconds,
        }
    }

    pub fn insert(&mut self, key: &str, timestamp: u64, value: f64) {
        self.data
            .entry(key.to_string())
            .or_default()
            .push((timestamp, value));
    }

    /// Prune entries older than the retention window.
    pub fn prune(&mut self, current_time: u64) {
        let cutoff = current_time.saturating_sub(self.retention_seconds);
        for entries in self.data.values_mut() {
            entries.retain(|&(ts, _)| ts >= cutoff);
        }
    }

    /// Get the moving average for a key within a time window.
    pub fn moving_average(&self, key: &str, window_start: u64, window_end: u64) -> Option<f64> {
        if let Some(entries) = self.data.get(key)
            && !entries.is_empty()
        {
            let windowed: Vec<f64> = entries
                .iter()
                .filter(|(ts, _)| *ts >= window_start && *ts <= window_end)
                .map(|(_, v)| *v)
                .collect();

            if windowed.is_empty() {
                None
            } else {
                Some(windowed.iter().sum::<f64>() / windowed.len() as f64)
            }
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_average() {
        let mut store = TimeSeriesStore::new(3600);
        store.insert("temp_sensor_1", 1000, 72.0);
        store.insert("temp_sensor_1", 1100, 74.0);
        store.insert("temp_sensor_1", 1200, 76.0);

        let avg = store.moving_average("temp_sensor_1", 1000, 1200);
        assert!((avg.unwrap() - 74.0).abs() < f64::EPSILON);
    }

    #[test]
    fn test_prune() {
        let mut store = TimeSeriesStore::new(100);
        store.insert("sensor_a", 100, 50.0);
        store.insert("sensor_a", 250, 55.0);
        store.prune(300);

        // Only the entry at 250 should remain (300 - 100 = cutoff at 200)
        let avg = store.moving_average("sensor_a", 0, 300);
        assert!((avg.unwrap() - 55.0).abs() < f64::EPSILON);
    }
}
"""
    with open(f'{SRC_DIR}/lib.rs', 'w') as f:
        f.write(lib_rs)

    # --- .vscode/settings.json --- minimal, NO nightly config
    vscode_settings = {
        "editor.formatOnSave": True,
        "editor.tabSize": 4,
        "rust-analyzer.checkOnSave": True,
        "rust-analyzer.check.command": "clippy"
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    # --- .vscode/extensions.json --- recommend rust-analyzer
    extensions_json = {
        "recommendations": [
            "rust-lang.rust-analyzer"
        ]
    }
    with open(f'{VSCODE_DIR}/extensions.json', 'w') as f:
        json.dump(extensions_json, f, indent=4)

    # NO rust-toolchain.toml (agent must create it)

    print(f'Initial Rust project created: {PROJECT_DIR}')
    print(f'  Cargo.toml, src/main.rs, src/lib.rs')
    print(f'  .vscode/settings.json (no nightly config)')
    print(f'  No rust-toolchain.toml exists')

    # Launch VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
