"""
Initial Setup: Create ~/projects/docs with 20 markdown/text files containing TODO comments
Task ID: vscode_gf5_008
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_008'
DOCS_DIR = f'{WORKDIR}/projects/docs'


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


# Files with "TODO: fix" (8 files) - these are the ones the agent must replace
# Files with other TODO variants (12 files) - these must remain unchanged

FILES = {
    # --- Files containing "TODO: fix" (8 files) ---
    "api-reference.md": """# API Reference

## Authentication Module

The authentication module handles user login, token management, and session control.

### Endpoints

#### POST /api/auth/login

Authenticates a user and returns a JWT token.

**Parameters:**
- `username` (string, required): The user's email address
- `password` (string, required): The user's password

**Response:**
```json
{
  "token": "eyJhbGciOi...",
  "expires_in": 3600
}
```

> TODO: fix the token expiration logic that causes premature logout after 30 minutes

#### POST /api/auth/refresh

Refreshes an existing JWT token before it expires.

> TODO: review the refresh token rotation policy

---

## Data Processing Module

### GET /api/data/export

Exports filtered dataset as CSV or JSON.

> TODO: fix encoding issues with non-ASCII characters in CSV export
""",

    "deployment-guide.md": """# Deployment Guide

## Prerequisites

- Docker 24.0+
- Kubernetes 1.28+
- Helm 3.13+
- AWS CLI v2 configured with appropriate IAM role

## Step 1: Build Container Images

```bash
docker build -t myapp-api:latest -f Dockerfile.api .
docker build -t myapp-worker:latest -f Dockerfile.worker .
```

TODO: fix the multi-stage build that leaves intermediate layers in the final image

## Step 2: Push to ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker push myapp-api:latest
```

## Step 3: Deploy with Helm

```bash
helm upgrade --install myapp ./charts/myapp -f values-production.yaml
```

TODO: fix the health check endpoint that returns 200 even when database is unreachable
""",

    "database-schema.md": """# Database Schema Documentation

## Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(512) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |
| is_active | BOOLEAN | DEFAULT TRUE |

TODO: fix the cascading delete that orphans user_preferences rows when a user is removed

## Orders Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY |
| user_id | UUID | FOREIGN KEY (users.id) |
| total_amount | DECIMAL(10,2) | NOT NULL |
| status | VARCHAR(50) | DEFAULT 'pending' |
| created_at | TIMESTAMP | DEFAULT NOW() |

TODO: implement partitioning for the orders table by quarter
""",

    "troubleshooting.txt": """Troubleshooting Guide - Common Issues
======================================

Issue 1: Application fails to start on port 8080
-------------------------------------------------
Symptom: "Address already in use" error on startup.
Cause: A previous instance did not shut down cleanly.
Solution: Run `lsof -i :8080` to find the orphan process and kill it.

TODO: fix the graceful shutdown handler that doesn't release the port on SIGTERM

Issue 2: Slow query performance on reports page
------------------------------------------------
Symptom: Reports page takes >10 seconds to load.
Cause: Missing index on orders.created_at column.
Solution: Run migration 20250315_add_orders_index.sql

TODO: review the query optimizer hints for the monthly aggregation report

Issue 3: File upload fails for files larger than 5MB
----------------------------------------------------
Symptom: 413 Request Entity Too Large from nginx proxy.
Cause: Default nginx client_max_body_size is 1MB.

TODO: fix the nginx configuration that silently drops the connection instead of returning proper error
""",

    "changelog.md": """# Changelog

## [2.4.1] - 2025-03-28

### Fixed
- Corrected timezone handling in scheduled report generation
- Fixed memory leak in WebSocket connection pool

### Changed
- Updated dependency: express 4.18.2 -> 4.19.0

## [2.4.0] - 2025-03-15

### Added
- Multi-tenant support for enterprise customers
- Dashboard widget for real-time monitoring

### Known Issues
- TODO: fix the race condition in concurrent session creation that causes duplicate entries
- TODO: review the notification batching algorithm for high-traffic periods

## [2.3.0] - 2025-02-28

### Added
- PDF export for invoices
- Bulk import via CSV upload
""",

    "security-audit.md": """# Security Audit Report - Q1 2025

## Summary

Overall risk rating: **Medium**

Audit period: January 1 - March 31, 2025
Auditor: Chen Wei, Senior Security Engineer

## Findings

### Critical

1. **SQL Injection in Search Endpoint** (CVE-2025-0042)
   - Location: `/api/search?q=`
   - Impact: Full database read access
   - Status: Patched in v2.4.1
   - TODO: fix the parameterized query fallback that still uses string concatenation for LIKE clauses

### High

2. **Insecure Direct Object Reference in User Profiles**
   - Location: `/api/users/{id}/profile`
   - Impact: Any authenticated user can view other profiles
   - Status: Under remediation

### Medium

3. **Missing Rate Limiting on Login Endpoint**
   - TODO: implement rate limiting middleware using sliding window algorithm
   - Priority: High

4. **Outdated TLS Configuration**
   - TODO: fix the TLS 1.0 fallback that is still enabled on the load balancer
""",

    "architecture-decisions.md": """# Architecture Decision Records

## ADR-001: Use PostgreSQL as Primary Database

**Status:** Accepted
**Date:** 2024-11-15
**Context:** Need a reliable, ACID-compliant database for financial transactions.

**Decision:** Use PostgreSQL 16 with connection pooling via PgBouncer.
**Consequences:** Requires team training on PostgreSQL-specific features.

## ADR-002: Migrate from REST to GraphQL

**Status:** Proposed
**Date:** 2025-02-20
**Context:** Frontend team needs more flexible data fetching to reduce over-fetching.

**Decision:** Implement GraphQL gateway with Apollo Server.

TODO: fix the schema stitching configuration that causes type conflicts between microservices

## ADR-003: Adopt Event-Driven Architecture

**Status:** In Progress
**Date:** 2025-03-01
**Context:** Synchronous inter-service communication creates tight coupling.

**Decision:** Use Apache Kafka for asynchronous event streaming.

TODO: review the dead letter queue policy for failed event processing
""",

    "testing-strategy.txt": """Testing Strategy Document
=========================

1. Unit Testing
   - Framework: pytest (Python), Jest (JavaScript)
   - Coverage target: 80% line coverage
   - Run on every commit via pre-commit hooks

2. Integration Testing
   - Use Docker Compose to spin up dependent services
   - Test database migrations in isolated environments
   - TODO: fix the test database seeding script that creates inconsistent foreign key references

3. End-to-End Testing
   - Framework: Playwright
   - Run against staging environment nightly
   - Cover critical user journeys: login, checkout, report generation

4. Performance Testing
   - Tool: k6
   - Baseline: 500 concurrent users, <200ms p95 latency
   - TODO: review the load test scenarios for the new GraphQL endpoints

5. Security Testing
   - SAST: SonarQube integrated in CI pipeline
   - DAST: OWASP ZAP weekly scans
""",

    # --- Files with other TODO variants (12 files) ---
    "onboarding.md": """# Developer Onboarding Guide

## Welcome!

Welcome to the engineering team. This guide will help you get set up.

## Day 1: Environment Setup

1. Clone the main repository: `git clone git@github.com:company/main-app.git`
2. Install dependencies: `npm install && pip install -r requirements.txt`
3. Set up local database: `docker compose up -d postgres redis`
4. Run migrations: `python manage.py migrate`

TODO: review the local development environment setup for M1/M2 Mac compatibility

## Day 2: Architecture Overview

- Read ADR documents in `/docs/architecture-decisions.md`
- Review the system diagram on Confluence
- Shadow a senior engineer during sprint standup
""",

    "monitoring-setup.md": """# Monitoring & Observability Setup

## Prometheus Configuration

Metrics are collected via Prometheus and visualized in Grafana.

### Key Dashboards

1. **Application Health** - Request rate, error rate, latency percentiles
2. **Infrastructure** - CPU, memory, disk usage per pod
3. **Business Metrics** - Active users, transactions per minute

### Alert Rules

```yaml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
```

TODO: implement the custom Grafana panel for displaying deployment annotations
""",

    "contributing.md": """# Contributing Guidelines

## Code Style

- Python: Follow PEP 8, enforced by `black` and `flake8`
- JavaScript: ESLint with Airbnb config
- All code must pass CI checks before merge

## Pull Request Process

1. Create a feature branch from `develop`
2. Write tests for new functionality
3. Update documentation if needed
4. Request review from at least 2 team members
5. Squash merge into `develop`

TODO: add the automated changelog generation from PR titles

## Commit Messages

Use conventional commits format:
```
feat(auth): add OAuth2 support for Google login
fix(api): correct pagination offset calculation
```
""",

    "release-process.md": """# Release Process

## Version Numbering

We follow semantic versioning (SemVer): MAJOR.MINOR.PATCH

## Release Checklist

- [ ] All CI tests pass on release branch
- [ ] Changelog updated with all changes
- [ ] Database migration scripts reviewed
- [ ] Performance benchmarks compared with previous release
- [ ] Security scan completed with no critical findings

## Rollback Procedure

1. Identify the issue via monitoring alerts
2. Revert the Helm release: `helm rollback myapp`
3. Verify service health
4. Post-mortem within 24 hours

TODO: document the canary deployment strategy for gradual rollouts
""",

    "data-pipeline.md": """# Data Pipeline Architecture

## Overview

Our data pipeline processes ~50M events daily from application logs, user interactions, and third-party integrations.

## Components

### Ingestion Layer
- Apache Kafka with 12 partitions per topic
- Schema Registry for Avro serialization
- Average throughput: 15,000 events/second

### Processing Layer
- Apache Flink for stream processing
- Batch jobs via Apache Airflow (scheduled every 6 hours)

### Storage Layer
- Raw data: Amazon S3 (Parquet format)
- Processed data: PostgreSQL analytical tables
- Real-time queries: Apache Druid

TODO: review the data retention policy for compliance with GDPR requirements
""",

    "infrastructure.txt": """Infrastructure Documentation
============================

Cloud Provider: AWS (us-east-1, eu-west-1)

Compute:
  - EKS cluster: 3 node groups (general, compute-optimized, memory-optimized)
  - EC2 instances for legacy batch processing
  - Lambda functions for event-driven microservices

Storage:
  - RDS PostgreSQL (db.r6g.xlarge, Multi-AZ)
  - ElastiCache Redis (cache.r6g.large, 3-node cluster)
  - S3 buckets for static assets and data lake

Networking:
  - VPC with public/private subnets across 3 AZs
  - ALB for HTTP/HTTPS traffic
  - NLB for gRPC services

TODO: implement the disaster recovery plan for cross-region failover
""",

    "api-versioning.md": """# API Versioning Strategy

## Current Approach

We use URL-based versioning: `/api/v1/`, `/api/v2/`

## Migration Timeline

| Version | Status | Deprecation Date | Sunset Date |
|---------|--------|-------------------|-------------|
| v1 | Deprecated | 2025-01-01 | 2025-06-30 |
| v2 | Current | - | - |
| v3 | In Development | - | - |

## Breaking Changes Policy

- Minimum 6 months between deprecation announcement and sunset
- All breaking changes documented in migration guide
- Client SDKs updated before new version GA

TODO: add backward compatibility tests for v1 to v2 migration edge cases
""",

    "code-review-checklist.md": """# Code Review Checklist

## Functionality
- [ ] Does the code do what the PR description claims?
- [ ] Are edge cases handled?
- [ ] Are error messages helpful and actionable?

## Testing
- [ ] Are there unit tests for new logic?
- [ ] Do integration tests cover the happy path?
- [ ] Are negative test cases included?

## Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all user-facing endpoints
- [ ] SQL queries use parameterized statements

## Performance
- [ ] No N+1 query patterns
- [ ] Large data sets paginated
- [ ] Caching strategy appropriate

TODO: add section on accessibility review requirements for frontend changes
""",

    "team-processes.md": """# Team Processes

## Sprint Cycle

- Sprint length: 2 weeks
- Planning: Monday morning
- Daily standup: 9:30 AM
- Retrospective: Last Friday afternoon
- Demo: Last Thursday afternoon

## On-Call Rotation

Each engineer is on-call for one week every 6 weeks.

| Week | Primary | Secondary |
|------|---------|-----------|
| 1 | Sarah Chen | Marcus Johnson |
| 2 | Priya Patel | David Kim |
| 3 | Alex Rivera | Emma Thompson |
| 4 | James Wilson | Lisa Zhang |
| 5 | Omar Hassan | Rachel Green |
| 6 | Michael Brown | Yuki Tanaka |

TODO: implement the automated on-call handoff notification system
""",

    "environment-variables.txt": """Environment Variables Reference
================================

Application:
  APP_NAME=myapp
  APP_ENV=production|staging|development
  APP_PORT=8080
  APP_LOG_LEVEL=info|debug|warn|error

Database:
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=myapp_production
  DB_USER=myapp_service
  DB_PASSWORD=<from-vault>
  DB_POOL_SIZE=20
  DB_SSL_MODE=verify-full

Redis:
  REDIS_URL=redis://localhost:6379/0
  REDIS_PASSWORD=<from-vault>
  REDIS_MAX_CONNECTIONS=50

External Services:
  SMTP_HOST=smtp.sendgrid.net
  SMTP_PORT=587
  STRIPE_API_KEY=<from-vault>
  AWS_REGION=us-east-1

TODO: add the feature flag service configuration variables
""",

    "incident-response.md": """# Incident Response Playbook

## Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| SEV1 | Complete service outage | 15 minutes | All APIs returning 500 |
| SEV2 | Major feature degraded | 30 minutes | Payment processing failing |
| SEV3 | Minor feature impacted | 2 hours | Search results slow |
| SEV4 | Cosmetic/low impact | Next business day | UI alignment issue |

## Response Steps

1. **Acknowledge** - Respond in #incidents Slack channel
2. **Assess** - Determine severity and impact scope
3. **Communicate** - Update status page
4. **Mitigate** - Apply temporary fix if available
5. **Resolve** - Deploy permanent fix
6. **Post-mortem** - Conduct within 48 hours

TODO: add the escalation matrix for weekend and holiday incidents
""",

    "performance-benchmarks.md": """# Performance Benchmarks

## Baseline Metrics (v2.4.0)

### API Response Times (p95)
| Endpoint | Latency | Throughput |
|----------|---------|------------|
| GET /api/users | 45ms | 2,500 req/s |
| POST /api/orders | 120ms | 800 req/s |
| GET /api/reports | 850ms | 150 req/s |
| GET /api/search | 200ms | 1,200 req/s |

### Database Query Performance
| Query | Avg Time | Max Time |
|-------|----------|----------|
| User lookup by email | 2ms | 15ms |
| Order history (30 days) | 45ms | 200ms |
| Monthly report aggregate | 1.2s | 3.5s |
| Full-text search | 35ms | 150ms |

### Infrastructure Utilization
- CPU: 35% average, 72% peak (during report generation)
- Memory: 60% average, 85% peak
- Disk I/O: 200 IOPS average

TODO: review the caching strategy for the reports endpoint to reduce p95 latency
""",
}


def create_initial():
    # Create the docs directory
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Write all files
    for filename, content in FILES.items():
        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content.lstrip('\n'))

    print(f'Created {len(FILES)} files in {DOCS_DIR}')

    # List files with TODO: fix to verify count
    fix_count = 0
    for filename, content in FILES.items():
        if 'TODO: fix' in content:
            occurrences = content.count('TODO: fix')
            fix_count += occurrences
            print(f'  {filename}: {occurrences} occurrence(s) of "TODO: fix"')
    print(f'Total "TODO: fix" occurrences: {fix_count}')

    # Launch VSCode with the docs folder
    launch_gui(f'code "{DOCS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
