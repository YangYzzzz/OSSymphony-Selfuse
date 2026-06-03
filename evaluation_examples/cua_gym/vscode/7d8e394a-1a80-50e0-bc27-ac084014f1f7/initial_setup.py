"""
Initial Setup: Open Markdown preview for a document, then add a Mermaid diagram
Task ID: vscode_rf_027
Domain: vscode

Creates ~/projects/architecture/system_design.md with architecture documentation
about a data processing pipeline. Installs Mermaid preview extension. Opens VSCode
with the file (preview pane NOT open - that's the agent's task).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_027'
PROJECT_DIR = f'{WORKDIR}/projects/architecture'
OUTPUT = f'{PROJECT_DIR}/system_design.md'


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create the system_design.md with realistic architecture documentation
    content = """# System Design: Data Processing Pipeline

## Overview

This document outlines the architecture for our real-time data processing pipeline
deployed across the analytics infrastructure at Meridian Technologies. The system
handles approximately 2.4 million events per hour from various data sources including
IoT sensors, application logs, and third-party API feeds.

## Architecture Stages

### 1. Ingestion

The ingestion layer serves as the entry point for all incoming data streams. It employs
Apache Kafka as the primary message broker with the following configuration:

- **Cluster**: 6 broker nodes across 3 availability zones
- **Topics**: `raw-events`, `sensor-data`, `api-feeds`, `app-logs`
- **Throughput**: Peak 45,000 messages/second
- **Retention**: 72 hours for raw topics

Data sources connect via REST endpoints or native Kafka producers. The ingestion
service performs initial schema validation and assigns partition keys based on the
source identifier and event timestamp.

### 2. Processing

The processing layer transforms and enriches raw data using Apache Flink streaming
jobs. Key transformations include:

- **Deduplication**: Window-based dedup using event fingerprints (SHA-256)
- **Enrichment**: Geo-IP lookup, device classification, user session stitching
- **Aggregation**: 1-minute and 5-minute tumbling window aggregates
- **Anomaly Detection**: Statistical outlier detection using z-score thresholds

The Flink cluster runs with 24 task manager slots and checkpoints every 30 seconds
to a shared S3 state backend. Processing latency targets are sub-500ms for 99th
percentile events.

### 3. Storage

Processed data is persisted to multiple storage backends optimized for different
access patterns:

| Storage Backend | Use Case | Retention |
|----------------|----------|-----------|
| TimescaleDB | Time-series queries | 90 days |
| Apache Parquet on S3 | Historical analytics | 2 years |
| Redis Cluster | Real-time dashboards | 24 hours |
| Elasticsearch | Full-text search & logs | 30 days |

The storage router determines the destination based on event type and downstream
consumer requirements. Write amplification is managed through batched inserts
with configurable flush intervals.

## Monitoring & Alerting

Pipeline health is monitored through Prometheus metrics exported from each stage.
Grafana dashboards provide real-time visibility into:

- Message lag per Kafka consumer group
- Flink job backpressure and checkpoint duration
- Storage write latency and error rates
- End-to-end pipeline latency (ingestion timestamp to storage commit)

## Deployment

All components are containerized and deployed on Kubernetes (EKS) with Helm charts.
Auto-scaling policies adjust Flink task managers and Kafka consumer instances based
on CPU utilization and consumer lag metrics.

## Future Considerations

- Migration from batch Parquet writes to Apache Iceberg for ACID table support
- Integration of ML inference stage between Processing and Storage
- Multi-region replication for disaster recovery
"""

    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Install the Markdown Preview Mermaid Support extension
    subprocess.run(['code', '--install-extension', 'bierner.markdown-mermaid', '--force'],
                   capture_output=True, text=True, timeout=60)
    print('Mermaid extension installed')

    # Open VSCode with the project folder and the specific file
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
