"""
Initial Setup: Create a Rust project workspace for VSCode tasks.json creation task
Task ID: vscode_lang_031
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_031'
PROJECT_DIR = f'{WORKDIR}/projects/myrustapp'

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
    # Create the Rust project directory structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Create Cargo.toml
    cargo_toml = """[package]
name = "myrustapp"
version = "0.1.0"
edition = "2021"
authors = ["Elena Rodriguez <elena.rodriguez@techcorp.io>"]
description = "A CLI tool for processing CSV data files and generating reports"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
csv = "1.3"
clap = { version = "4.4", features = ["derive"] }

[dev-dependencies]
assert_cmd = "2.0"
predicates = "3.0"
"""
    with open(f'{PROJECT_DIR}/Cargo.toml', 'w') as f:
        f.write(cargo_toml)

    # Create main.rs with realistic Rust code
    main_rs = '''use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::PathBuf;

/// Represents a single data record from a CSV file.
#[derive(Debug, Clone)]
struct Record {
    name: String,
    department: String,
    salary: f64,
    start_date: String,
}

impl Record {
    fn from_csv_line(line: &str) -> Option<Self> {
        let fields: Vec<&str> = line.split(',').collect();
        if fields.len() < 4 {
            return None;
        }
        Some(Record {
            name: fields[0].trim().to_string(),
            department: fields[1].trim().to_string(),
            salary: fields[2].trim().parse().unwrap_or(0.0),
            start_date: fields[3].trim().to_string(),
        })
    }
}

fn load_records(path: &PathBuf) -> io::Result<Vec<Record>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut records = Vec::new();
    let mut lines = reader.lines();

    // Skip header line
    lines.next();

    for line in lines {
        let line = line?;
        if let Some(record) = Record::from_csv_line(&line) {
            records.push(record);
        }
    }
    Ok(records)
}

fn calculate_average_salary(records: &[Record]) -> f64 {
    if records.is_empty() {
        return 0.0;
    }
    let total: f64 = records.iter().map(|r| r.salary).sum();
    total / records.len() as f64
}

fn filter_by_department(records: &[Record], department: &str) -> Vec<Record> {
    records
        .iter()
        .filter(|r| r.department == department)
        .cloned()
        .collect()
}

fn main() {
    println!("CSV Data Processor v0.1.0");
    println!("Usage: myrustapp <csv_file> [--department <name>]");

    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Error: Please provide a CSV file path");
        std::process::exit(1);
    }

    let path = PathBuf::from(&args[1]);
    match load_records(&path) {
        Ok(records) => {
            println!("Loaded {} records", records.len());
            println!("Average salary: ${:.2}", calculate_average_salary(&records));

            if args.len() > 3 && args[2] == "--department" {
                let filtered = filter_by_department(&records, &args[3]);
                println!(
                    "Department '{}': {} employees",
                    args[3],
                    filtered.len()
                );
            }
        }
        Err(e) => {
            eprintln!("Error reading file: {}", e);
            std::process::exit(1);
        }
    }
}
'''
    with open(f'{PROJECT_DIR}/src/main.rs', 'w') as f:
        f.write(main_rs)

    # Create a lib.rs with utility functions
    lib_rs = '''/// Utility module for string formatting in reports.
pub fn format_currency(amount: f64) -> String {
    format!("${:.2}", amount)
}

pub fn format_percentage(value: f64) -> String {
    format!("{:.1}%", value * 100.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_currency() {
        assert_eq!(format_currency(1234.5), "$1234.50");
        assert_eq!(format_currency(0.0), "$0.00");
    }

    #[test]
    fn test_format_percentage() {
        assert_eq!(format_percentage(0.75), "75.0%");
        assert_eq!(format_percentage(1.0), "100.0%");
    }
}
'''
    with open(f'{PROJECT_DIR}/src/lib.rs', 'w') as f:
        f.write(lib_rs)

    # Create a README
    readme = """# myrustapp

A CLI tool for processing CSV data files and generating department reports.

## Building

```bash
cargo build
```

## Testing

```bash
cargo test
```

## Usage

```bash
cargo run -- data.csv --department Engineering
```
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Create sample data file
    sample_csv = """name,department,salary,start_date
Sarah Chen,Engineering,95000,2023-01-15
Marcus Johnson,Marketing,72000,2022-06-01
Anika Patel,Engineering,88500,2023-03-20
David Kim,Sales,68000,2021-11-10
Lisa Thompson,Marketing,75000,2022-09-15
James Wilson,Engineering,102000,2020-04-01
Maria Garcia,Sales,71000,2023-05-12
Robert Brown,HR,65000,2022-01-20
"""
    with open(f'{PROJECT_DIR}/sample_data.csv', 'w') as f:
        f.write(sample_csv)

    # Ensure NO .vscode/tasks.json exists (negative constraint)
    tasks_json_path = f'{PROJECT_DIR}/.vscode/tasks.json'
    if os.path.exists(tasks_json_path):
        os.remove(tasks_json_path)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Verified: No .vscode/tasks.json exists')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
