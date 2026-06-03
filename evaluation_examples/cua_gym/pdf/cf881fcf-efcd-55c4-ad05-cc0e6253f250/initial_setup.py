"""
Initial Setup: Create ~/Documents/spec_doc.pdf with 20 pages (no page numbers)
Task ID: pdf_adv_193
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
DOCS_DIR = '/home/user/Documents'
TASK_ID = 'pdf_adv_193'
OUTPUT = f'{DOCS_DIR}/spec_doc.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page size: A4
    PAGE_W, PAGE_H = 595, 842

    # -- Document metadata --
    doc.set_metadata({
        "title": "Technical Specification Document",
        "author": "Engineering Team",
        "subject": "System Architecture and Design",
        "keywords": "specification, architecture, design, API",
        "creator": "CUA-Gym",
    })

    # Content sections for 20 pages (realistic spec doc)
    sections = [
        # (page_title, paragraphs)
        ("Cover Page", [
            "TECHNICAL SPECIFICATION DOCUMENT",
            "System Architecture and API Design Reference",
            "Version 3.2 — March 2025",
            "Prepared by: Engineering Team",
            "Approved by: Technical Review Board",
            "Classification: Internal Use Only",
        ]),
        ("Table of Contents", [
            "1. Executive Summary ........................ 3",
            "2. System Overview .......................... 4",
            "3. Architecture Design ...................... 5",
            "4. API Reference ............................ 6",
            "5. Data Models .............................. 7",
            "6. Authentication & Security ................ 8",
            "7. Performance Requirements ................. 9",
            "8. Error Handling .......................... 10",
            "9. Deployment Configuration ................ 11",
            "10. Database Schema ........................ 12",
            "11. Caching Strategy ....................... 13",
            "12. Monitoring & Logging ................... 14",
            "13. Integration Guidelines ................. 15",
            "14. Migration Procedures ................... 16",
            "15. Testing Framework ...................... 17",
            "16. Compliance & Auditing .................. 18",
            "17. Disaster Recovery ...................... 19",
            "18. Appendix & References .................. 20",
        ]),
        ("1. Executive Summary", [
            "This document provides a comprehensive technical specification for the NextGen Platform, "
            "a distributed microservices architecture designed to handle enterprise-scale workloads "
            "with high availability and fault tolerance.",
            "The system processes over 2 million transactions per day across 12 geographic regions, "
            "with a 99.99% SLA commitment to enterprise clients.",
            "Key design principles: horizontal scalability, service isolation, event-driven "
            "communication, and automated failover.",
            "Core technologies: Kubernetes 1.29, Apache Kafka 3.6, PostgreSQL 16, Redis 7.2, "
            "and gRPC for inter-service communication.",
        ]),
        ("2. System Overview", [
            "The NextGen Platform consists of 47 microservices organized into 6 functional domains: "
            "Identity, Commerce, Analytics, Notification, Reporting, and Infrastructure.",
            "Service mesh: Istio 1.20 with mTLS for all east-west traffic. Ingress via NGINX "
            "configured with rate limiting (5,000 RPS per tenant).",
            "Data sovereignty: Tenant data is isolated at the database cluster level using "
            "namespace-based partitioning. PII data encrypted at rest with AES-256.",
            "Traffic routing: 80/20 canary deployments with automated rollback triggered by "
            "error rate > 0.5% or P99 latency > 200ms.",
        ]),
        ("3. Architecture Design", [
            "3.1 Microservices Topology",
            "Each service is deployed as a StatefulSet (stateful) or Deployment (stateless) in "
            "Kubernetes. Resource limits: CPU 2 cores, Memory 4Gi per replica.",
            "3.2 Event Streaming",
            "Apache Kafka with 3 brokers per region. Topics partitioned by tenant_id (128 "
            "partitions). Retention: 7 days for transactional topics, 30 days for audit logs.",
            "3.3 State Management",
            "Redis Cluster (6 nodes) for session state and rate-limit counters. TTL: 3600s "
            "for sessions, 60s for rate-limit windows.",
        ]),
        ("4. API Reference", [
            "4.1 REST API Conventions",
            "Base URL: https://api.nextgen.internal/v3",
            "Authentication: Bearer token (JWT, RS256, 1-hour expiry)",
            "Pagination: cursor-based using X-Cursor header",
            "Rate limiting: 1000 requests/minute per API key",
            "4.2 Core Endpoints",
            "POST /transactions — Create transaction (max 100 items/request)",
            "GET /transactions/{id} — Retrieve transaction by UUID",
            "PATCH /transactions/{id}/status — Update transaction status",
            "DELETE /transactions/{id} — Soft-delete (retains audit record)",
            "GET /reports/summary?from={date}&to={date} — Aggregate report",
        ]),
        ("5. Data Models", [
            "5.1 Transaction Entity",
            "id: UUID v4 (primary key)",
            "tenant_id: UUID (foreign key, indexed)",
            "amount: DECIMAL(18,6) — supports up to 6 decimal places",
            "currency: CHAR(3) — ISO 4217 code",
            "status: ENUM(pending, processing, settled, failed, reversed)",
            "created_at: TIMESTAMPTZ — UTC",
            "metadata: JSONB — up to 64KB, indexed with GIN",
            "5.2 Audit Log",
            "All mutations logged to immutable append-only table.",
            "Columns: event_id, entity_type, entity_id, actor_id, action, before, after, ts",
        ]),
        ("6. Authentication & Security", [
            "6.1 Token Issuance",
            "Tokens issued by identity service using RS256 (2048-bit key pair, rotated quarterly).",
            "Claims: sub (user_id), tid (tenant_id), scope (space-separated permissions), exp, iat.",
            "6.2 Authorization Model",
            "RBAC with 5 system roles: Super Admin, Org Admin, Manager, Analyst, Read-Only.",
            "Fine-grained permissions: 127 individual permission bits organized into 8 modules.",
            "6.3 Security Controls",
            "OWASP Top 10 mitigations applied. Penetration testing quarterly by third-party.",
            "WAF rules: SQLI, XSS, CSRF, path traversal, and custom rules for API abuse.",
        ]),
        ("7. Performance Requirements", [
            "7.1 Latency SLOs",
            "P50 < 20ms, P95 < 80ms, P99 < 150ms for read operations.",
            "P50 < 50ms, P95 < 200ms, P99 < 500ms for write operations.",
            "7.2 Throughput Targets",
            "Peak throughput: 50,000 RPS across all services combined.",
            "Burst capacity: 3x normal load for up to 60 seconds.",
            "7.3 Scalability",
            "Horizontal auto-scaling: HPA triggers at 70% CPU or 80% memory utilization.",
            "Scale-out time: < 90 seconds from trigger to new pod healthy.",
        ]),
        ("8. Error Handling", [
            "8.1 Error Response Format",
            '{"error": {"code": "VALIDATION_FAILED", "message": "...", "details": [...], '
            '"request_id": "uuid", "timestamp": "ISO8601"}}',
            "8.2 Retry Policy",
            "Exponential backoff: base 100ms, multiplier 2, jitter ±25%, max retries 5.",
            "Non-retryable: 400, 401, 403, 404, 409, 422.",
            "Retryable: 429, 500, 502, 503, 504.",
            "8.3 Circuit Breaker",
            "Opens after 5 consecutive failures or error rate > 50% over 10-second window.",
            "Half-open probe: single request every 30 seconds until recovery confirmed.",
        ]),
        ("9. Deployment Configuration", [
            "9.1 Container Images",
            "Base image: distroless/java21 (no shell, minimal attack surface).",
            "Registry: ECR private registry, images scanned with Trivy on every build.",
            "9.2 Kubernetes Resources",
            "Namespace per domain (identity, commerce, analytics, notification, reporting).",
            "PodDisruptionBudgets: minAvailable=2 for all production deployments.",
            "NetworkPolicies: deny-all default, explicit allow rules per service pair.",
            "9.3 Environment Variables",
            "All secrets from AWS Secrets Manager via External Secrets Operator.",
            "Config: ConfigMap with hot-reload via inotify watcher (no restart required).",
        ]),
        ("10. Database Schema", [
            "10.1 PostgreSQL Cluster Configuration",
            "Primary + 2 read replicas per region. Patroni for automated failover (<30s).",
            "pgBouncer connection pooling: max 1000 connections, pool_mode=transaction.",
            "10.2 Key Tables",
            "transactions (partitioned by created_at, monthly partitions, 5-year retention)",
            "accounts (unpartitioned, ~10M rows, regularly vacuumed)",
            "audit_log (append-only, partitioned by week, compressed with pg_compress)",
            "10.3 Indexes",
            "Composite indexes on (tenant_id, status, created_at) for common query patterns.",
            "Partial indexes on active records to reduce index bloat.",
        ]),
        ("11. Caching Strategy", [
            "11.1 Cache Hierarchy",
            "L1: In-process cache (Caffeine), max 10,000 entries, TTL 30s.",
            "L2: Redis Cluster, distributed cache, TTL varies by data type.",
            "L3: CDN edge cache (CloudFront) for static API responses.",
            "11.2 Cache Key Design",
            "Format: {service}:{version}:{entity_type}:{id}:{variant}",
            "Example: commerce:v3:product:uuid-1234:pricing",
            "11.3 Cache Invalidation",
            "Event-driven invalidation via Kafka topic cache.invalidation.",
            "TTL-based fallback for non-critical data. No cache stampede protection via locks.",
        ]),
        ("12. Monitoring & Logging", [
            "12.1 Metrics Stack",
            "Prometheus (scrape interval 15s) → Thanos (long-term storage, 1 year) → Grafana.",
            "Custom metrics: transaction_rate, error_rate_by_code, cache_hit_ratio, queue_depth.",
            "12.2 Distributed Tracing",
            "OpenTelemetry SDK in all services. Jaeger for trace storage (7-day retention).",
            "Sampling: 100% for errors, 1% for normal traffic, 10% for new deployments.",
            "12.3 Log Aggregation",
            "Fluentd → Elasticsearch (hot: 7 days, warm: 30 days, cold: 1 year).",
            "Structured JSON logs with mandatory fields: timestamp, level, service, trace_id, span_id.",
        ]),
        ("13. Integration Guidelines", [
            "13.1 Webhook Integration",
            "Event delivery: at-least-once with idempotency keys.",
            "Retry schedule: 1m, 5m, 30m, 2h, 24h (5 attempts total).",
            "Signature: HMAC-SHA256 of payload with tenant-specific secret, in X-Signature header.",
            "13.2 SDK Support",
            "Official SDKs: Python 3.10+, Node.js 18+, Java 17+, Go 1.21+.",
            "SDK features: auto-retry, connection pooling, request signing, pagination helpers.",
            "13.3 Sandbox Environment",
            "Identical to production but with synthetic data. Reset daily at 02:00 UTC.",
            "Test card numbers and bank accounts provided in developer documentation.",
        ]),
        ("14. Migration Procedures", [
            "14.1 Zero-Downtime Migrations",
            "All schema changes must be backward-compatible for at least 2 release cycles.",
            "Process: expand phase (add columns/tables) → migrate data → contract phase (drop old).",
            "14.2 Data Migration Tools",
            "pg_migrate for schema changes. Custom scripts for data backfill with progress tracking.",
            "Max batch size: 10,000 rows per transaction to avoid lock contention.",
            "14.3 Rollback Procedures",
            "All migrations must have a tested rollback script.",
            "Rollback time SLO: < 15 minutes for any database migration.",
        ]),
        ("15. Testing Framework", [
            "15.1 Test Pyramid",
            "Unit tests: 70% coverage minimum, pytest + unittest.mock.",
            "Integration tests: test containers (Docker) for each service dependency.",
            "Contract tests: Pact framework for producer/consumer API contracts.",
            "E2E tests: Playwright for critical user journeys, runs on every staging deploy.",
            "15.2 Performance Testing",
            "k6 load tests run weekly in staging: 10m ramp-up to 10,000 RPS, 30m sustained.",
            "Chaos engineering: LitmusChaos experiments scheduled bi-weekly.",
            "15.3 Test Data Management",
            "Faker-based synthetic data generation. PII never used in non-production environments.",
        ]),
        ("16. Compliance & Auditing", [
            "16.1 Regulatory Compliance",
            "PCI-DSS Level 1 certification (annual audit by QSA).",
            "SOC 2 Type II attestation (covers security, availability, confidentiality).",
            "GDPR/CCPA: right-to-erasure implemented via soft-delete + scheduled purge job.",
            "16.2 Audit Trail",
            "All data mutations logged with actor, timestamp, before/after state.",
            "Audit logs are immutable (insert-only table with no UPDATE/DELETE grants).",
            "Retention: 7 years for financial transactions, 3 years for access logs.",
            "16.3 Key Management",
            "AWS KMS for envelope encryption. Key rotation: 90 days for data keys.",
        ]),
        ("17. Disaster Recovery", [
            "17.1 Recovery Objectives",
            "RTO (Recovery Time Objective): 4 hours for complete region failure.",
            "RPO (Recovery Point Objective): 15 minutes (based on replication lag).",
            "17.2 Backup Strategy",
            "Database: continuous WAL archiving to S3 + daily pg_dump snapshots.",
            "Object storage: S3 cross-region replication (3 regions).",
            "Configuration: GitOps (ArgoCD) — full cluster recoverable from git in < 1 hour.",
            "17.3 Failover Testing",
            "Annual DR drill with full region simulation. Results documented and reviewed.",
            "Automated failover tests monthly for individual service and database failures.",
        ]),
        ("18. Appendix & References", [
            "A. Glossary",
            "SLA — Service Level Agreement",
            "RPS — Requests Per Second",
            "mTLS — Mutual Transport Layer Security",
            "WAF — Web Application Firewall",
            "HPA — Horizontal Pod Autoscaler",
            "B. Reference Architecture",
            "See architecture diagram repository: git@github.com:company/arch-diagrams.git",
            "C. Change Log",
            "v3.2 (2025-03) — Added caching strategy section, updated DR objectives",
            "v3.1 (2024-12) — Revised authentication section with new key rotation policy",
            "v3.0 (2024-09) — Major revision: migrated to Kubernetes-first architecture",
            "D. Contact",
            "Technical questions: engineering-platform@company.internal",
            "Security concerns: security@company.internal",
        ]),
    ]

    for page_idx, (section_title, paragraphs) in enumerate(sections):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        # --- Section title / header ---
        y = 80
        page.insert_text(
            pymupdf.Point(72, y),
            section_title,
            fontsize=16,
            fontname="hebo",  # Helvetica-Bold
            color=(0.1, 0.1, 0.4),
        )

        # Horizontal rule under title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y + 8), pymupdf.Point(PAGE_W - 72, y + 8))
        shape.finish(color=(0.3, 0.3, 0.6), width=1.5)
        shape.commit()

        y = 120
        for para in paragraphs:
            # Insert each paragraph as a textbox to handle wrapping
            rect = pymupdf.Rect(72, y, PAGE_W - 72, y + 50)
            fontname = "tiro"  # Times-Roman for body text
            fontsize = 11

            # If line looks like a heading/sub-heading (short, no spaces at start)
            if para.startswith(("A.", "B.", "C.", "D.")) or (
                len(para) < 60 and not para.startswith(" ") and para[0].isdigit()
            ):
                fontname = "hebo"
                fontsize = 11

            excess = page.insert_textbox(
                rect,
                para,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            # Estimate lines used: approximately 14pt per line
            approx_lines = max(1, -int(excess / 14) + 1) if excess < 0 else 1
            char_per_line = int((PAGE_W - 144) / (fontsize * 0.55))
            lines_used = max(1, (len(para) + char_per_line - 1) // char_per_line)
            y += lines_used * 16 + 6

            if y > PAGE_H - 80:
                break

        # --- Footer with document info (but NO page numbers — that's the task) ---
        footer_y = PAGE_H - 35
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, footer_y - 8), pymupdf.Point(PAGE_W - 72, footer_y - 8))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

        page.insert_text(
            pymupdf.Point(72, footer_y),
            "Technical Specification Document  |  Version 3.2  |  CONFIDENTIAL",
            fontsize=7,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )
        # NOTE: NO page number text — that's what the agent must add.

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 20')

    # GUI-ready startup: open with Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
