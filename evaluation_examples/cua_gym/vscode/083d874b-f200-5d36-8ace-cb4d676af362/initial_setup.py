"""
Initial Setup: Generate a table of contents for documentation.md using Markdown All in One
Task ID: vscode_lp_029
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_029'
OUTPUT = f'{WORKDIR}/{TASK_ID}.md'

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

MARKDOWN_CONTENT = """# Project Aurora Documentation

## Introduction

Project Aurora is a next-generation data analytics platform designed for enterprise teams
that need real-time insights from distributed data sources. Built on a microservices
architecture, Aurora provides seamless integration with existing data warehouses, streaming
pipelines, and business intelligence tools.

This documentation covers the complete setup, configuration, and operational guide for
deploying and managing Project Aurora in production environments.

## Installation

### System Requirements

Before installing Project Aurora, ensure your environment meets the following minimum
requirements:

- **Operating System**: Ubuntu 22.04 LTS, RHEL 8+, or macOS 13+
- **CPU**: 8 cores minimum (16 recommended for production)
- **Memory**: 32 GB RAM minimum (64 GB recommended)
- **Storage**: 500 GB SSD with at least 200 GB free space
- **Network**: Gigabit Ethernet with stable connectivity to data sources

### Package Installation

To install Project Aurora using the official package manager:

```bash
curl -fsSL https://releases.aurora-analytics.io/install.sh | bash
aurora-cli init --config /etc/aurora/default.yaml
aurora-cli verify --all
```

For air-gapped environments, download the offline bundle from the releases portal and
follow the manual installation procedure in Appendix A.

## Configuration

### Database Connection

Aurora supports PostgreSQL 14+, MySQL 8+, and ClickHouse as backend databases. Configure
the primary connection in `/etc/aurora/database.yaml`:

```yaml
database:
  engine: postgresql
  host: db-primary.internal.example.com
  port: 5432
  name: aurora_production
  pool_size: 25
  ssl_mode: verify-full
  ssl_cert: /etc/aurora/certs/client.pem
```

### Authentication Setup

Aurora integrates with SAML 2.0, OAuth 2.0, and LDAP identity providers. To configure
SSO with your organization's identity provider:

1. Navigate to **Admin Panel > Security > Authentication**
2. Select your identity provider type
3. Upload the metadata XML or enter the configuration endpoints
4. Map user attributes (email, display name, groups)
5. Test the connection with a pilot user group before enabling for all users

## API Reference

### REST Endpoints

The Aurora REST API follows OpenAPI 3.1 specification. All endpoints require
authentication via Bearer token or API key.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v2/datasets` | GET | List all accessible datasets |
| `/api/v2/datasets/{id}` | GET | Retrieve dataset metadata |
| `/api/v2/queries` | POST | Submit an analytical query |
| `/api/v2/queries/{id}/results` | GET | Fetch query results |
| `/api/v2/dashboards` | GET | List dashboards |
| `/api/v2/exports/{format}` | POST | Export data in specified format |

### WebSocket Streaming

For real-time data feeds, connect to the WebSocket endpoint at
`wss://aurora.example.com/ws/v2/stream`. The streaming protocol supports backpressure
and automatic reconnection with configurable retry policies.

## Deployment Guide

### Kubernetes Deployment

Aurora ships with Helm charts for Kubernetes deployment. The recommended production
topology includes:

- 3 API gateway replicas behind a load balancer
- 5 query engine workers with horizontal pod autoscaling
- 2 scheduler instances in active-passive configuration
- Dedicated monitoring namespace with Prometheus and Grafana

```bash
helm repo add aurora https://charts.aurora-analytics.io
helm install aurora-prod aurora/aurora-platform \\
  --namespace aurora-system \\
  --values production-values.yaml \\
  --set global.domain=aurora.example.com
```

### High Availability

To achieve 99.99% uptime SLA, deploy Aurora across multiple availability zones with
the following considerations:

- Database replication with automatic failover (pg_auto_failover or Patroni)
- Shared storage via distributed file system (Ceph or AWS EFS)
- Cross-region disaster recovery with RPO < 5 minutes

## Monitoring and Observability

### Metrics Collection

Aurora exposes Prometheus-compatible metrics on port 9090 by default. Key metrics
to monitor include:

- `aurora_query_duration_seconds` - Query execution time histogram
- `aurora_active_connections` - Current database connection count
- `aurora_cache_hit_ratio` - Query cache effectiveness
- `aurora_ingestion_lag_seconds` - Data pipeline processing delay
- `aurora_error_rate` - Request error rate by endpoint

### Log Management

Structured JSON logs are written to `/var/log/aurora/` with automatic rotation.
Configure log shipping to your centralized logging platform using the built-in
Fluentd sidecar or the Aurora log forwarder agent.

## Troubleshooting

### Common Issues

**Query timeout errors**: Increase the `query.timeout_seconds` parameter in the
configuration file. For complex analytical queries spanning large datasets, consider
enabling query result caching and materialized views.

**Connection pool exhaustion**: Monitor the `aurora_active_connections` metric.
If connections frequently reach the pool limit, increase `database.pool_size` or
optimize long-running queries that hold connections.

**Memory pressure on worker nodes**: Aurora query workers cache intermediate results
in memory. If workers experience OOM kills, either increase the memory limit or
reduce `worker.max_concurrent_queries`.

### Diagnostic Commands

```bash
aurora-cli status --verbose
aurora-cli health-check --include-dependencies
aurora-cli logs --tail 100 --level error
aurora-cli metrics snapshot --output /tmp/aurora-diagnostics.json
```

## Security Best Practices

### Network Security

- Deploy Aurora behind a reverse proxy (nginx, Envoy, or cloud load balancer)
- Enable TLS 1.3 for all client-facing connections
- Restrict database access to Aurora service accounts only
- Use network policies in Kubernetes to isolate Aurora namespaces
- Rotate API keys and service tokens every 90 days

### Data Protection

All data at rest is encrypted using AES-256-GCM. Data in transit is protected by
TLS 1.2+ with certificate pinning support. For compliance with GDPR and SOC 2
requirements, enable the audit logging module and configure data retention policies
according to your organization's data governance framework.

### Access Control

Aurora implements role-based access control (RBAC) with four built-in roles:

- **Viewer**: Read-only access to assigned dashboards and datasets
- **Analyst**: Can create queries, dashboards, and scheduled reports
- **Admin**: Full platform configuration and user management
- **Super Admin**: Infrastructure-level access including database management
"""

def create_initial():
    # Write the markdown file
    with open(OUTPUT, 'w') as f:
        f.write(MARKDOWN_CONTENT.lstrip())

    print(f'Initial file created: {OUTPUT}')

    # Ensure Markdown All in One extension is installed
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'yzhang.markdown-all-in-one' not in result.stdout:
            print('Installing Markdown All in One extension...')
            subprocess.run(
                ['code', '--install-extension', 'yzhang.markdown-all-in-one'],
                capture_output=True, text=True, timeout=120
            )
            print('Extension installed.')
        else:
            print('Markdown All in One extension already installed.')
    except Exception as e:
        print(f'Warning: Could not check/install extension: {e}')

    # Launch VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
