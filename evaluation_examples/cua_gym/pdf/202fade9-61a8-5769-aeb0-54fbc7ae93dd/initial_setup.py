"""
Initial Setup: Create a 28-page technical specification PDF (unencrypted)
Task ID: pdf_mbc_006
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/design_spec.pdf'


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
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Technical specification content for a 28-page document
    # "CloudBridge Platform - Technical Design Specification v3.2"

    W, H = 612, 792  # Letter size
    MARGIN = 72
    TEXT_WIDTH = W - 2 * MARGIN

    chapters = [
        {
            "title": "CloudBridge Platform\nTechnical Design Specification v3.2",
            "is_cover": True,
            "subtitle": "Prepared by: Systems Architecture Division\nDate: March 15, 2025\nClassification: Internal Use Only\nDocument ID: CB-TDS-2025-032",
        },
        {
            "title": "Table of Contents",
            "body": (
                "1. Executive Summary .......................... 3\n"
                "2. System Architecture Overview ............... 4\n"
                "3. Authentication & Authorization ............. 6\n"
                "4. Data Layer Architecture .................... 8\n"
                "5. API Gateway Design ......................... 10\n"
                "6. Message Queue Infrastructure ............... 12\n"
                "7. Caching Strategy ........................... 14\n"
                "8. Search Engine Integration .................. 16\n"
                "9. Monitoring & Observability ................. 18\n"
                "10. Deployment Pipeline ....................... 20\n"
                "11. Security Considerations ................... 22\n"
                "12. Performance Benchmarks .................... 24\n"
                "13. Disaster Recovery ......................... 26\n"
                "14. Appendices ................................ 28\n"
            ),
        },
        {
            "title": "1. Executive Summary",
            "body": (
                "The CloudBridge Platform is a next-generation microservices architecture designed to handle "
                "enterprise-scale workloads with a target throughput of 50,000 requests per second at P99 latency "
                "below 200ms. This document outlines the technical design decisions, infrastructure components, and "
                "integration patterns that form the backbone of the platform.\n\n"
                "Key objectives include:\n"
                "- Horizontal scalability across 12 geographic regions\n"
                "- Zero-downtime deployments with blue-green strategy\n"
                "- End-to-end encryption for data in transit and at rest\n"
                "- Compliance with SOC 2 Type II and ISO 27001 standards\n"
                "- Multi-tenant isolation with resource quotas\n\n"
                "The platform serves as the foundation for CloudBridge's suite of enterprise SaaS products, "
                "including the Workflow Engine (WFE), Analytics Dashboard (AD), and Integration Hub (IH). "
                "Current production traffic averages 28,000 RPS with seasonal peaks reaching 47,000 RPS during "
                "quarter-end processing cycles.\n\n"
                "This specification supersedes CB-TDS-2024-019 and incorporates feedback from the Q4 2024 "
                "architecture review board, including revised caching policies and updated failover procedures."
            ),
        },
        {
            "title": "2. System Architecture Overview",
            "body": (
                "2.1 High-Level Architecture\n\n"
                "The platform follows a layered microservices architecture with clear separation of concerns:\n\n"
                "Layer 1 - Edge (CDN & Load Balancing):\n"
                "  - Cloudflare Enterprise for DDoS protection and static asset caching\n"
                "  - AWS ALB with weighted target groups for traffic distribution\n"
                "  - Geographic DNS routing via Route 53 latency-based records\n\n"
                "Layer 2 - API Gateway:\n"
                "  - Kong Gateway (v3.4) with custom authentication plugins\n"
                "  - Rate limiting: 1,000 req/min per tenant (configurable)\n"
                "  - Request transformation and protocol bridging (REST/gRPC)\n\n"
                "Layer 3 - Service Mesh:\n"
                "  - Istio 1.20 with mTLS enforcement\n"
                "  - Circuit breaker: 5 consecutive failures trigger 30s open state\n"
                "  - Retry policy: 3 attempts with exponential backoff (100ms base)\n\n"
                "Layer 4 - Data:\n"
                "  - PostgreSQL 16 (primary OLTP) with Citus extension for sharding\n"
                "  - Redis 7.2 cluster (caching and session management)\n"
                "  - Apache Kafka 3.6 (event streaming, 72-hour retention)\n"
                "  - Elasticsearch 8.12 (full-text search and log aggregation)\n\n"
                "2.2 Service Inventory\n\n"
                "The platform comprises 34 microservices organized into 6 bounded contexts. "
                "Each service maintains its own database schema and communicates via well-defined APIs "
                "or asynchronous event channels."
            ),
        },
        {
            "title": "2. System Architecture Overview (continued)",
            "body": (
                "2.3 Service Communication Patterns\n\n"
                "Synchronous communication uses gRPC with Protocol Buffers v3 for internal service-to-service "
                "calls. External-facing endpoints expose RESTful APIs with OpenAPI 3.1 specifications.\n\n"
                "Service Dependencies Matrix:\n\n"
                "  Service          | Upstream Deps  | Downstream Deps | Protocol\n"
                "  ---------------  | -------------- | --------------- | --------\n"
                "  auth-service     | user-store     | api-gateway     | gRPC\n"
                "  user-store       | postgres-shard | auth-service    | gRPC\n"
                "  billing-engine   | payment-gw     | notification    | gRPC\n"
                "  workflow-engine  | task-queue      | analytics       | Kafka\n"
                "  analytics-svc    | clickhouse     | dashboard-api   | gRPC\n"
                "  notification-svc | smtp-relay     | billing-engine  | Kafka\n\n"
                "2.4 Network Topology\n\n"
                "VPC CIDR: 10.0.0.0/16\n"
                "  - Public subnets: 10.0.1.0/24, 10.0.2.0/24 (ALB, NAT Gateway)\n"
                "  - Private subnets: 10.0.10.0/24 through 10.0.15.0/24 (services)\n"
                "  - Database subnets: 10.0.20.0/24, 10.0.21.0/24 (isolated)\n\n"
                "Inter-region connectivity uses AWS Transit Gateway with encrypted peering. "
                "Latency between us-east-1 and eu-west-1 averages 78ms."
            ),
        },
        {
            "title": "3. Authentication & Authorization",
            "body": (
                "3.1 Authentication Flow\n\n"
                "The platform implements OAuth 2.0 with PKCE for public clients and client credentials "
                "grant for service-to-service authentication. JWT tokens are issued with RS256 signing "
                "using 2048-bit RSA keys rotated every 90 days.\n\n"
                "Token Specifications:\n"
                "  - Access token TTL: 15 minutes\n"
                "  - Refresh token TTL: 7 days (sliding window)\n"
                "  - ID token: OpenID Connect compliant\n"
                "  - Token size: ~1.2KB average (compressed claims)\n\n"
                "3.2 Authorization Model\n\n"
                "Role-Based Access Control (RBAC) with hierarchical permission inheritance:\n\n"
                "  Role               | Permissions                    | Max Sessions\n"
                "  ----------------   | ------------------------------ | ------------\n"
                "  Platform Admin     | Full system access             | 3\n"
                "  Tenant Admin       | Tenant-scoped management       | 5\n"
                "  Developer          | API access, sandbox env        | 10\n"
                "  Viewer             | Read-only dashboard access     | 20\n"
                "  Service Account    | Programmatic API access        | 1\n\n"
                "3.3 Multi-Factor Authentication\n\n"
                "MFA is mandatory for Platform Admin and Tenant Admin roles. Supported factors:\n"
                "  - TOTP (Google Authenticator, Authy)\n"
                "  - WebAuthn/FIDO2 hardware keys (YubiKey 5 series)\n"
                "  - SMS OTP (fallback only, not recommended)"
            ),
        },
        {
            "title": "3. Authentication & Authorization (continued)",
            "body": (
                "3.4 Session Management\n\n"
                "Sessions are stored in Redis with the following structure:\n"
                "  Key: session:{user_id}:{session_id}\n"
                "  TTL: Matches refresh token expiry\n"
                "  Fields: device_fingerprint, ip_address, created_at, last_active\n\n"
                "Concurrent session limits are enforced per role. When a new session exceeds the limit, "
                "the oldest inactive session is terminated with a WebSocket notification to the client.\n\n"
                "3.5 API Key Management\n\n"
                "Service accounts use API keys with the following characteristics:\n"
                "  - Format: cb_live_{32-char-hex} or cb_test_{32-char-hex}\n"
                "  - Keys are hashed with bcrypt (cost factor 12) before storage\n"
                "  - Rate limits are bound to the key, not the originating IP\n"
                "  - Key rotation requires a 24-hour overlap period\n\n"
                "3.6 Audit Logging\n\n"
                "All authentication events are logged to a dedicated audit stream:\n"
                "  - Login success/failure (including IP, device, geo-location)\n"
                "  - Token refresh events\n"
                "  - Permission escalation attempts\n"
                "  - MFA enrollment/removal\n"
                "  - API key creation/revocation\n\n"
                "Audit logs are retained for 365 days in compliance with SOC 2 requirements and are "
                "immutable once written (append-only Kafka topic with compaction disabled)."
            ),
        },
        {
            "title": "4. Data Layer Architecture",
            "body": (
                "4.1 Database Strategy\n\n"
                "Primary OLTP: PostgreSQL 16.2 with Citus 12.1 extension\n"
                "  - Sharding key: tenant_id (hash-based distribution)\n"
                "  - Coordinator node: db-coord-01 (r6g.2xlarge)\n"
                "  - Worker nodes: 8x db-worker (r6g.xlarge)\n"
                "  - Replication: Streaming with 2 synchronous standbys\n"
                "  - Connection pooling: PgBouncer (transaction mode, 200 max connections)\n\n"
                "OLAP: ClickHouse 24.1\n"
                "  - Used for analytics queries and reporting dashboards\n"
                "  - Data pipeline: Kafka -> Debezium -> ClickHouse (5-minute lag)\n"
                "  - Materialized views for pre-aggregated metrics\n\n"
                "4.2 Schema Design Principles\n\n"
                "All tables follow these conventions:\n"
                "  - UUID v7 primary keys (time-ordered for index efficiency)\n"
                "  - tenant_id column on every table (shard key)\n"
                "  - created_at, updated_at timestamps (UTC, microsecond precision)\n"
                "  - soft-delete via deleted_at column (NULL = active)\n"
                "  - Row-level security policies for tenant isolation\n\n"
                "4.3 Migration Strategy\n\n"
                "Database migrations use Flyway with the following workflow:\n"
                "  1. Developer creates migration in migrations/V{version}__{description}.sql\n"
                "  2. CI validates migration against shadow database\n"
                "  3. Rolling deployment applies migration before code deployment\n"
                "  4. Backward-compatible changes only (no column drops in same release)"
            ),
        },
        {
            "title": "4. Data Layer Architecture (continued)",
            "body": (
                "4.4 Data Partitioning\n\n"
                "Time-series data is partitioned by month using PostgreSQL declarative partitioning:\n\n"
                "  Table: events\n"
                "    Partition key: created_at (RANGE)\n"
                "    Retention: 24 months online, then archived to S3 Glacier\n"
                "    Partition size: ~50GB per month per tenant shard\n\n"
                "  Table: audit_logs\n"
                "    Partition key: logged_at (RANGE)\n"
                "    Retention: 12 months online (regulatory requirement)\n"
                "    Partition size: ~20GB per month\n\n"
                "4.5 Backup and Recovery\n\n"
                "  - Continuous WAL archiving to S3 (RPO: < 1 second)\n"
                "  - Full base backup: Daily at 02:00 UTC\n"
                "  - Point-in-time recovery tested monthly\n"
                "  - Cross-region backup replication (us-east-1 -> eu-west-1)\n"
                "  - Recovery Time Objective (RTO): 15 minutes\n"
                "  - Recovery Point Objective (RPO): 1 second\n\n"
                "4.6 Data Encryption\n\n"
                "  - At rest: AES-256 via AWS KMS (per-tenant CMK)\n"
                "  - In transit: TLS 1.3 for all database connections\n"
                "  - Application-level: Sensitive fields encrypted with envelope encryption\n"
                "  - Key rotation: Automatic every 365 days via KMS"
            ),
        },
        {
            "title": "5. API Gateway Design",
            "body": (
                "5.1 Gateway Architecture\n\n"
                "Kong Gateway v3.4 deployed in DB-less mode with declarative configuration "
                "managed via GitOps (ArgoCD). The gateway handles:\n\n"
                "  - Request authentication and authorization\n"
                "  - Rate limiting and throttling\n"
                "  - Request/response transformation\n"
                "  - API versioning (URI path-based: /v1/, /v2/)\n"
                "  - CORS policy enforcement\n"
                "  - Request logging and tracing\n\n"
                "5.2 Rate Limiting Configuration\n\n"
                "  Tier       | Requests/min | Burst | Concurrent\n"
                "  ---------- | ------------ | ----- | ----------\n"
                "  Free       | 100          | 20    | 5\n"
                "  Starter    | 1,000        | 200   | 25\n"
                "  Business   | 10,000       | 2,000 | 100\n"
                "  Enterprise | 50,000       | 10,000| 500\n\n"
                "Rate limits are enforced using a sliding window algorithm backed by Redis. "
                "When a limit is exceeded, the gateway returns HTTP 429 with Retry-After header.\n\n"
                "5.3 API Versioning Strategy\n\n"
                "  - Major versions in URI path (/v1/, /v2/)\n"
                "  - Minor versions via Accept header (application/vnd.cloudbridge.v1.2+json)\n"
                "  - Deprecation notice: 6-month sunset period with Sunset header\n"
                "  - Maximum 2 major versions maintained concurrently"
            ),
        },
        {
            "title": "5. API Gateway Design (continued)",
            "body": (
                "5.4 Custom Plugins\n\n"
                "The following custom Kong plugins have been developed:\n\n"
                "  Plugin: cb-tenant-resolver\n"
                "    Purpose: Extract tenant context from JWT claims or API key\n"
                "    Phase: access\n"
                "    Latency impact: < 2ms\n\n"
                "  Plugin: cb-request-enrichment\n"
                "    Purpose: Add correlation ID, request metadata headers\n"
                "    Phase: access\n"
                "    Headers added: X-Correlation-ID, X-Tenant-ID, X-Request-Start\n\n"
                "  Plugin: cb-response-sanitizer\n"
                "    Purpose: Remove internal headers, mask sensitive data in error responses\n"
                "    Phase: header_filter, body_filter\n"
                "    Headers removed: X-Internal-*, X-Debug-*\n\n"
                "5.5 Health Check Endpoints\n\n"
                "  Endpoint          | Method | Auth     | Purpose\n"
                "  ---------------   | ------ | -------- | ------------------\n"
                "  /health/live      | GET    | None     | Liveness probe\n"
                "  /health/ready     | GET    | None     | Readiness probe\n"
                "  /health/detailed  | GET    | Admin    | Full system status\n"
                "  /metrics          | GET    | Internal | Prometheus metrics\n\n"
                "Health checks run every 10 seconds. A service is removed from the load balancer "
                "pool after 3 consecutive failed health checks and restored after 2 successes."
            ),
        },
        {
            "title": "6. Message Queue Infrastructure",
            "body": (
                "6.1 Kafka Cluster Configuration\n\n"
                "Apache Kafka 3.6.1 deployed on dedicated EC2 instances:\n"
                "  - Brokers: 6x i3.2xlarge (NVMe storage for optimal I/O)\n"
                "  - Controllers: 3x m6i.xlarge (KRaft mode, no ZooKeeper)\n"
                "  - Replication factor: 3\n"
                "  - Min in-sync replicas: 2\n"
                "  - Default retention: 72 hours\n"
                "  - Max message size: 10MB (compressed)\n\n"
                "6.2 Topic Design\n\n"
                "  Topic                     | Partitions | Retention | Consumers\n"
                "  ------------------------  | ---------- | --------- | ---------\n"
                "  user.events               | 32         | 72h       | analytics, audit\n"
                "  billing.transactions      | 16         | 168h      | billing-engine\n"
                "  workflow.tasks             | 64         | 24h       | workflow-engine\n"
                "  notifications.outbound    | 16         | 12h       | notification-svc\n"
                "  system.audit              | 8          | 720h      | compliance-svc\n"
                "  data.changelog            | 32         | 168h      | search-indexer\n\n"
                "6.3 Consumer Group Strategy\n\n"
                "Each consuming service operates its own consumer group with auto-commit disabled. "
                "Offset commits occur after successful processing to ensure at-least-once delivery. "
                "Dead letter queues (DLQ) capture messages that fail after 5 retry attempts.\n\n"
                "Consumer lag is monitored via Burrow with alerts triggered at:\n"
                "  - Warning: lag > 1,000 messages for 5 minutes\n"
                "  - Critical: lag > 10,000 messages for 2 minutes"
            ),
        },
        {
            "title": "6. Message Queue Infrastructure (continued)",
            "body": (
                "6.4 Schema Registry\n\n"
                "Confluent Schema Registry manages Avro schemas for all Kafka topics:\n"
                "  - Compatibility mode: BACKWARD (default)\n"
                "  - Schema evolution rules enforced in CI pipeline\n"
                "  - Schema ID embedded in message headers\n\n"
                "6.5 Event Sourcing Patterns\n\n"
                "The workflow engine uses event sourcing for state management:\n\n"
                "  Event Types:\n"
                "    WorkflowCreated -> WorkflowStepStarted -> WorkflowStepCompleted\n"
                "    -> WorkflowCompleted | WorkflowFailed | WorkflowCancelled\n\n"
                "  Aggregate State Reconstruction:\n"
                "    Events are replayed from the changelog topic to rebuild workflow state.\n"
                "    Snapshots are taken every 100 events to limit replay time.\n"
                "    Maximum replay window: 10,000 events (older workflows archived).\n\n"
                "6.6 Cross-Region Replication\n\n"
                "MirrorMaker 2 replicates critical topics between regions:\n"
                "  - Replicated topics: user.events, billing.transactions, system.audit\n"
                "  - Replication lag SLA: < 30 seconds\n"
                "  - Conflict resolution: Last-writer-wins with vector clocks\n"
                "  - Bandwidth allocation: 500 Mbps dedicated inter-region link\n\n"
                "During regional failover, consumers switch to the mirror cluster within 60 seconds "
                "using custom consumer interceptors that detect broker unavailability."
            ),
        },
        {
            "title": "7. Caching Strategy",
            "body": (
                "7.1 Cache Architecture\n\n"
                "Redis 7.2 cluster with 6 nodes (3 primary, 3 replica):\n"
                "  - Instance type: r6g.xlarge (26 GiB RAM per node)\n"
                "  - Total cluster memory: 156 GiB\n"
                "  - Eviction policy: allkeys-lfu\n"
                "  - Persistence: RDB snapshots every 5 minutes + AOF\n\n"
                "7.2 Cache Layers\n\n"
                "  Layer          | Technology      | TTL        | Hit Rate Target\n"
                "  -------------- | --------------- | ---------- | ---------------\n"
                "  L1 (In-process)| Caffeine        | 60s        | 40%\n"
                "  L2 (Shared)   | Redis Cluster   | 300s-3600s | 85%\n"
                "  L3 (CDN)      | Cloudflare      | 86400s     | 95%\n\n"
                "7.3 Cache Invalidation\n\n"
                "Write-through caching with event-driven invalidation:\n"
                "  1. Service writes to database\n"
                "  2. Debezium captures change event\n"
                "  3. Cache invalidation consumer receives event\n"
                "  4. Redis keys matching the entity pattern are deleted\n"
                "  5. Next read triggers cache repopulation (lazy loading)\n\n"
                "Cache stampede protection:\n"
                "  - Probabilistic early expiration (beta = 1.0)\n"
                "  - Request coalescing for identical cache misses\n"
                "  - Background refresh for hot keys (access count > 100/min)"
            ),
        },
        {
            "title": "7. Caching Strategy (continued)",
            "body": (
                "7.4 Session Cache Design\n\n"
                "User sessions are cached with the following key structure:\n"
                "  session:{user_id}:{session_id} -> {\n"
                "    'access_token_hash': 'sha256:...',\n"
                "    'refresh_token_hash': 'sha256:...',\n"
                "    'permissions': ['read:users', 'write:workflows'],\n"
                "    'tenant_id': 'tenant_abc',\n"
                "    'created_at': '2025-03-15T10:30:00Z',\n"
                "    'last_active': '2025-03-15T14:22:00Z',\n"
                "    'device': 'Chrome/122, macOS 14.3'\n"
                "  }\n\n"
                "Session lookup latency: P50 = 0.3ms, P99 = 1.2ms\n\n"
                "7.5 Cache Monitoring\n\n"
                "  Metric                | Alert Threshold | Action\n"
                "  --------------------- | --------------- | ------\n"
                "  Memory usage          | > 80%           | Scale cluster\n"
                "  Hit rate              | < 70%           | Review TTL config\n"
                "  Eviction rate         | > 1000/sec      | Increase memory\n"
                "  Connection count      | > 5000          | Review pool config\n"
                "  Replication lag       | > 500ms         | Check network\n\n"
                "7.6 Cache Warming\n\n"
                "On deployment, critical caches are pre-warmed:\n"
                "  - Tenant configuration: All active tenant configs loaded\n"
                "  - Permission policies: RBAC rules for all roles\n"
                "  - Feature flags: All flag states for all tenants\n"
                "  - Warm-up duration: ~45 seconds for full cache population"
            ),
        },
        {
            "title": "8. Search Engine Integration",
            "body": (
                "8.1 Elasticsearch Cluster\n\n"
                "Elasticsearch 8.12 deployed with dedicated node roles:\n"
                "  - Master nodes: 3x m6i.xlarge (cluster coordination)\n"
                "  - Data nodes: 6x r6i.2xlarge (hot tier, NVMe)\n"
                "  - Warm nodes: 3x r6i.xlarge (older indices)\n"
                "  - Ingest nodes: 2x c6i.xlarge (pipeline processing)\n\n"
                "8.2 Index Design\n\n"
                "  Index Pattern          | Shards | Replicas | Lifecycle\n"
                "  ---------------------  | ------ | -------- | ---------\n"
                "  workflows-*            | 6      | 1        | Hot 7d -> Warm 30d -> Delete 90d\n"
                "  documents-*            | 4      | 1        | Hot 30d -> Warm 90d -> Delete 365d\n"
                "  audit-logs-*           | 2      | 1        | Hot 30d -> Warm 365d\n"
                "  user-activity-*        | 4      | 1        | Hot 7d -> Warm 30d -> Delete 60d\n\n"
                "8.3 Search Features\n\n"
                "Full-text search capabilities:\n"
                "  - Multi-field search with field boosting\n"
                "  - Fuzzy matching (edit distance: 2)\n"
                "  - Synonym expansion (custom synonym files per tenant)\n"
                "  - Autocomplete with edge n-gram tokenizer\n"
                "  - Faceted search with aggregations\n"
                "  - Highlighting with configurable fragment size\n\n"
                "Search latency: P50 = 15ms, P99 = 120ms (across 500M documents)"
            ),
        },
        {
            "title": "8. Search Engine Integration (continued)",
            "body": (
                "8.4 Indexing Pipeline\n\n"
                "Data flows from source systems to Elasticsearch via a multi-stage pipeline:\n\n"
                "  Stage 1: Change Data Capture (Debezium)\n"
                "    - Captures INSERT/UPDATE/DELETE from PostgreSQL\n"
                "    - Publishes to Kafka data.changelog topic\n\n"
                "  Stage 2: Transformation (Kafka Streams)\n"
                "    - Denormalizes data for search-optimized structure\n"
                "    - Enriches with tenant-specific metadata\n"
                "    - Applies field-level security annotations\n\n"
                "  Stage 3: Bulk Indexing\n"
                "    - Elasticsearch bulk API with 1000 document batches\n"
                "    - Indexing throughput: 5,000 documents/second\n"
                "    - Index refresh interval: 5 seconds (configurable per index)\n\n"
                "8.5 Security Integration\n\n"
                "Document-level security ensures tenant isolation:\n"
                "  - Each document tagged with tenant_id and access_roles\n"
                "  - Query-time filtering via Elasticsearch DLS (Document Level Security)\n"
                "  - Field-level masking for PII data in search results\n\n"
                "8.6 Reindexing Strategy\n\n"
                "Zero-downtime reindexing using alias rotation:\n"
                "  1. Create new index with updated mapping: workflows-v2\n"
                "  2. Start reindex task from workflows-v1 to workflows-v2\n"
                "  3. Enable dual-write: new documents go to both indices\n"
                "  4. When reindex completes, swap alias to workflows-v2\n"
                "  5. Delete workflows-v1 after 24h validation period"
            ),
        },
        {
            "title": "9. Monitoring & Observability",
            "body": (
                "9.1 Observability Stack\n\n"
                "The platform uses a unified observability stack:\n"
                "  - Metrics: Prometheus + Grafana\n"
                "  - Logs: Fluent Bit -> Elasticsearch -> Kibana\n"
                "  - Traces: OpenTelemetry -> Jaeger\n"
                "  - Alerts: PagerDuty integration via Alertmanager\n\n"
                "9.2 Key Performance Indicators\n\n"
                "  SLI                    | Target SLO  | Measurement\n"
                "  ---------------------- | ----------- | -----------\n"
                "  Availability           | 99.95%      | Successful responses / total\n"
                "  Latency (P50)          | < 50ms      | API gateway response time\n"
                "  Latency (P99)          | < 200ms     | API gateway response time\n"
                "  Error rate             | < 0.1%      | 5xx responses / total\n"
                "  Throughput             | > 50K RPS   | Requests per second capacity\n\n"
                "9.3 Alert Routing\n\n"
                "  Severity | Response Time | Notification | Escalation\n"
                "  -------- | ------------- | ------------ | ----------\n"
                "  P1       | 5 min         | PagerDuty    | VP Eng (15 min)\n"
                "  P2       | 30 min        | PagerDuty    | Team Lead (1h)\n"
                "  P3       | 4 hours       | Slack        | None\n"
                "  P4       | Next sprint   | Jira ticket  | None\n\n"
                "On-call rotation: 1-week shifts, 2-person primary/secondary, follow-the-sun model "
                "across US, EU, and APAC teams."
            ),
        },
        {
            "title": "9. Monitoring & Observability (continued)",
            "body": (
                "9.4 Custom Dashboards\n\n"
                "Grafana dashboards are organized by audience:\n\n"
                "  Dashboard: Platform Overview\n"
                "    Audience: SRE team\n"
                "    Panels: Request rate, error rate, latency histograms, resource utilization\n"
                "    Refresh: 10 seconds\n\n"
                "  Dashboard: Tenant Health\n"
                "    Audience: Customer Success\n"
                "    Panels: Per-tenant usage, quota utilization, feature adoption\n"
                "    Refresh: 1 minute\n\n"
                "  Dashboard: Business Metrics\n"
                "    Audience: Leadership\n"
                "    Panels: DAU/MAU, revenue per request, conversion funnels\n"
                "    Refresh: 5 minutes\n\n"
                "9.5 Distributed Tracing\n\n"
                "OpenTelemetry instrumentation captures end-to-end request traces:\n"
                "  - Trace context propagation: W3C Trace Context format\n"
                "  - Sampling rate: 1% for normal traffic, 100% for errors\n"
                "  - Span attributes: tenant_id, user_id, request_path, response_code\n"
                "  - Trace retention: 7 days in Jaeger, 30 days in S3 archive\n\n"
                "9.6 Log Aggregation\n\n"
                "Structured JSON logging with mandatory fields:\n"
                "  {timestamp, level, service, correlation_id, tenant_id, message, stack_trace}\n\n"
                "Log volume: ~2TB/day across all services\n"
                "Retention: 30 days hot (Elasticsearch), 90 days warm, 365 days cold (S3)"
            ),
        },
        {
            "title": "10. Deployment Pipeline",
            "body": (
                "10.1 CI/CD Architecture\n\n"
                "GitHub Actions orchestrates the deployment pipeline:\n\n"
                "  Stage 1: Build (2 min)\n"
                "    - Compile, lint, unit tests\n"
                "    - Docker image build with multi-stage Dockerfile\n"
                "    - Image vulnerability scan (Trivy)\n\n"
                "  Stage 2: Test (5 min)\n"
                "    - Integration tests against ephemeral database\n"
                "    - Contract tests (Pact)\n"
                "    - Performance regression tests (k6)\n\n"
                "  Stage 3: Deploy Staging (3 min)\n"
                "    - ArgoCD sync to staging cluster\n"
                "    - Smoke tests and synthetic monitoring\n"
                "    - Manual approval gate for production\n\n"
                "  Stage 4: Deploy Production (10 min)\n"
                "    - Blue-green deployment via ALB target group switch\n"
                "    - Canary analysis: 5% traffic for 10 minutes\n"
                "    - Full rollout if error rate < 0.1%\n"
                "    - Automatic rollback if P99 latency > 500ms\n\n"
                "10.2 Container Strategy\n\n"
                "  - Base image: distroless/static-debian12\n"
                "  - Multi-architecture: amd64, arm64\n"
                "  - Image registry: ECR with cross-region replication\n"
                "  - Image signing: Cosign with Sigstore\n"
                "  - SBOM: Generated with Syft, stored in ECR alongside image"
            ),
        },
        {
            "title": "10. Deployment Pipeline (continued)",
            "body": (
                "10.3 Kubernetes Configuration\n\n"
                "EKS 1.29 with managed node groups:\n\n"
                "  Node Group     | Instance Type | Min | Max | Purpose\n"
                "  -------------- | ------------- | --- | --- | -------\n"
                "  general        | m6i.2xlarge   | 6   | 20  | API services\n"
                "  compute        | c6i.4xlarge   | 2   | 10  | Data processing\n"
                "  memory         | r6i.2xlarge   | 3   | 8   | Caching, search\n"
                "  spot           | m6i.xlarge    | 0   | 30  | Batch jobs, dev\n\n"
                "Horizontal Pod Autoscaler targets:\n"
                "  - CPU utilization: 70%\n"
                "  - Memory utilization: 80%\n"
                "  - Custom metric: requests_per_second (via KEDA)\n\n"
                "10.4 Feature Flags\n\n"
                "LaunchDarkly integration for progressive feature rollout:\n"
                "  - Flag evaluation: server-side SDK (Go, Java, Python)\n"
                "  - Targeting: per-tenant, per-user, percentage rollout\n"
                "  - Kill switches: instant disable without deployment\n"
                "  - Flag lifecycle: proposed -> active -> complete -> archived\n\n"
                "10.5 Database Migration Coordination\n\n"
                "Schema changes are deployed before application code:\n"
                "  1. Migration runs against shadow DB (validation)\n"
                "  2. Migration applied to production (backward-compatible)\n"
                "  3. New application version deployed\n"
                "  4. Old application version drained (5-minute grace period)\n"
                "  5. Cleanup migration (optional, next release)"
            ),
        },
        {
            "title": "11. Security Considerations",
            "body": (
                "11.1 Threat Model\n\n"
                "The platform's threat model addresses the following attack vectors:\n\n"
                "  Threat                    | Mitigation                      | Severity\n"
                "  ------------------------- | ------------------------------- | --------\n"
                "  SQL Injection             | Parameterized queries, ORM      | Critical\n"
                "  XSS                       | CSP headers, output encoding    | High\n"
                "  CSRF                      | SameSite cookies, CSRF tokens   | High\n"
                "  SSRF                      | Egress filtering, URL validation| High\n"
                "  Privilege Escalation      | RBAC, principle of least priv.  | Critical\n"
                "  Data Exfiltration         | DLP policies, egress monitoring | Critical\n"
                "  Supply Chain Attack       | SBOM, image signing, dep audit  | High\n\n"
                "11.2 Network Security\n\n"
                "  - WAF: AWS WAF with OWASP Core Rule Set\n"
                "  - DDoS: Cloudflare Enterprise + AWS Shield Advanced\n"
                "  - Network policies: Calico with default-deny ingress\n"
                "  - Service mesh mTLS: Istio auto-rotated certificates\n"
                "  - Secrets management: HashiCorp Vault (auto-unseal via KMS)\n\n"
                "11.3 Compliance\n\n"
                "  - SOC 2 Type II: Annual audit by Deloitte\n"
                "  - ISO 27001: Certified since January 2024\n"
                "  - GDPR: Data Processing Agreement template for EU customers\n"
                "  - CCPA: Consumer data deletion within 45 days\n"
                "  - HIPAA: BAA available for healthcare tier customers"
            ),
        },
        {
            "title": "11. Security Considerations (continued)",
            "body": (
                "11.4 Vulnerability Management\n\n"
                "Continuous security scanning across the SDLC:\n\n"
                "  Phase        | Tool           | Frequency    | SLA\n"
                "  ------------ | -------------- | ------------ | ---\n"
                "  Code         | Semgrep        | Every commit | Fix before merge\n"
                "  Dependencies | Dependabot     | Daily        | Critical: 24h\n"
                "  Containers   | Trivy          | Every build  | Critical: block deploy\n"
                "  Infrastructure| tfsec         | Every commit | High: 7 days\n"
                "  Runtime      | Falco          | Continuous   | P1 alert\n"
                "  Penetration  | HackerOne      | Quarterly    | Per severity SLA\n\n"
                "11.5 Incident Response\n\n"
                "Security incident response follows the NIST framework:\n"
                "  1. Detection: Automated alerts from WAF, IDS, and anomaly detection\n"
                "  2. Containment: Network isolation, credential rotation, affected service quarantine\n"
                "  3. Eradication: Root cause analysis, patch deployment\n"
                "  4. Recovery: Service restoration, data integrity verification\n"
                "  5. Post-mortem: Blameless review within 72 hours\n\n"
                "11.6 Data Classification\n\n"
                "  Level          | Examples                       | Controls\n"
                "  -------------- | ------------------------------ | --------\n"
                "  Public         | Marketing content, docs        | None\n"
                "  Internal       | Architecture docs, runbooks    | Auth required\n"
                "  Confidential   | Customer data, financials      | Encryption + RBAC\n"
                "  Restricted     | Credentials, PII, PHI          | Vault + audit log"
            ),
        },
        {
            "title": "12. Performance Benchmarks",
            "body": (
                "12.1 Load Test Results (March 2025)\n\n"
                "Test environment: Production-equivalent (50% scale)\n"
                "Tool: k6 with distributed execution (10 load generators)\n\n"
                "  Scenario                  | RPS    | P50    | P99    | Error Rate\n"
                "  ------------------------- | ------ | ------ | ------ | ----------\n"
                "  API Read (cache hit)      | 45,000 | 12ms   | 45ms   | 0.01%\n"
                "  API Read (cache miss)     | 20,000 | 35ms   | 120ms  | 0.03%\n"
                "  API Write                 | 8,000  | 45ms   | 180ms  | 0.05%\n"
                "  Search query              | 5,000  | 25ms   | 95ms   | 0.02%\n"
                "  File upload (5MB)         | 500    | 800ms  | 2.5s   | 0.1%\n"
                "  Batch import (1000 rows)  | 50     | 3.2s   | 8.5s   | 0.2%\n\n"
                "12.2 Resource Utilization Under Load\n\n"
                "At 40,000 RPS sustained:\n"
                "  - API pods CPU: 65% average, 82% peak\n"
                "  - API pods memory: 2.1 GiB / 4 GiB limit\n"
                "  - Database CPU: 45% average, 70% peak\n"
                "  - Redis memory: 78 GiB / 156 GiB cluster total\n"
                "  - Kafka disk I/O: 450 MB/s write, 1.2 GB/s read\n"
                "  - Network throughput: 8 Gbps ingress, 12 Gbps egress\n\n"
                "12.3 Scalability Projections\n\n"
                "Linear scaling verified up to 100,000 RPS with proportional resource addition. "
                "Database becomes the bottleneck at ~80,000 RPS; mitigation: additional Citus "
                "worker nodes or read replica promotion."
            ),
        },
        {
            "title": "12. Performance Benchmarks (continued)",
            "body": (
                "12.4 Latency Optimization History\n\n"
                "Key optimizations implemented in Q1 2025:\n\n"
                "  Optimization                        | Impact (P99)\n"
                "  ----------------------------------- | ------------\n"
                "  Connection pooling (PgBouncer)       | -35ms\n"
                "  gRPC compression (gzip)              | -12ms\n"
                "  Redis pipeline batching              | -8ms\n"
                "  JIT compilation warm-up              | -15ms\n"
                "  DNS caching (CoreDNS tuning)         | -5ms\n"
                "  Protobuf serialization optimization  | -7ms\n"
                "  Total improvement                    | -82ms\n\n"
                "12.5 Capacity Planning\n\n"
                "Growth forecast and infrastructure requirements:\n\n"
                "  Quarter | Projected RPS | Compute Nodes | DB Storage | Monthly Cost\n"
                "  ------- | ------------- | ------------- | ---------- | -----------\n"
                "  Q2 2025 | 55,000        | 24            | 8 TB       | $127,000\n"
                "  Q3 2025 | 65,000        | 28            | 12 TB      | $148,000\n"
                "  Q4 2025 | 80,000        | 36            | 18 TB      | $185,000\n"
                "  Q1 2026 | 100,000       | 48            | 25 TB      | $235,000\n\n"
                "Reserved instances cover 60% of baseline compute. Spot instances handle burst "
                "capacity with a 10-minute termination notice handler for graceful shutdown."
            ),
        },
        {
            "title": "13. Disaster Recovery",
            "body": (
                "13.1 DR Strategy\n\n"
                "The platform implements an active-passive disaster recovery strategy with "
                "the following objectives:\n"
                "  - Recovery Time Objective (RTO): 15 minutes\n"
                "  - Recovery Point Objective (RPO): 1 second (database), 30 seconds (Kafka)\n"
                "  - Failover scope: Full regional failover (us-east-1 -> eu-west-1)\n\n"
                "13.2 Failover Procedure\n\n"
                "Automated failover sequence (triggered by Route 53 health check failure):\n\n"
                "  T+0:00  Health check fails (3 consecutive probes)\n"
                "  T+0:30  Route 53 begins DNS failover\n"
                "  T+1:00  DR region database promoted from standby\n"
                "  T+2:00  Kafka consumers switched to mirror cluster\n"
                "  T+3:00  Application pods scaled up in DR region\n"
                "  T+5:00  Cache warming initiated\n"
                "  T+8:00  Synthetic monitoring confirms service availability\n"
                "  T+10:00 DR region fully operational, PagerDuty updated\n\n"
                "13.3 DR Testing\n\n"
                "  Test Type            | Frequency  | Duration   | Impact\n"
                "  -------------------- | ---------- | ---------- | ------\n"
                "  Tabletop exercise    | Monthly    | 2 hours    | None\n"
                "  Component failover   | Quarterly  | 30 minutes | Minimal\n"
                "  Full regional failover| Bi-annual | 4 hours    | Read-only mode\n"
                "  Chaos engineering    | Weekly     | Varies     | Controlled blast radius"
            ),
        },
        {
            "title": "13. Disaster Recovery (continued)",
            "body": (
                "13.4 Backup Verification\n\n"
                "Automated backup verification runs daily:\n\n"
                "  Check                          | Method               | Alert on Failure\n"
                "  ------------------------------ | -------------------- | ----------------\n"
                "  Database backup integrity       | Restore to temp DB   | P1\n"
                "  WAL continuity                  | Gap detection        | P1\n"
                "  S3 object count                 | Cross-region compare | P2\n"
                "  Elasticsearch snapshot          | Restore to dev       | P2\n"
                "  Kafka topic offset sync         | Mirror lag check     | P2\n\n"
                "13.5 Runbook: Regional Failover\n\n"
                "Step-by-step procedure for manual failover initiation:\n\n"
                "  1. Confirm primary region is genuinely unavailable (not a monitoring false positive)\n"
                "  2. Notify stakeholders via PagerDuty and Slack #incident channel\n"
                "  3. Execute: aws rds failover-db-cluster --db-cluster-id prod-primary\n"
                "  4. Update Route 53 health check to force failover (if not auto-triggered)\n"
                "  5. Monitor DR region scaling events in Kubernetes dashboard\n"
                "  6. Verify data consistency: run integrity check script\n"
                "  7. Update status page: status.cloudbridge.io\n"
                "  8. Begin root cause analysis for primary region failure\n\n"
                "13.6 Communication Protocol\n\n"
                "During a DR event:\n"
                "  - Internal: Slack #incident channel, PagerDuty conference bridge\n"
                "  - External: Status page update within 10 minutes\n"
                "  - Customer notification: Email within 30 minutes (affected tenants)\n"
                "  - Post-incident report: Published within 72 hours"
            ),
        },
        {
            "title": "14. Appendices",
            "body": (
                "Appendix A: Glossary\n\n"
                "  Term          | Definition\n"
                "  ------------- | ------------------------------------------\n"
                "  CUA           | Computer Use Agent\n"
                "  RBAC          | Role-Based Access Control\n"
                "  mTLS          | Mutual Transport Layer Security\n"
                "  WAF           | Web Application Firewall\n"
                "  DLS           | Document Level Security\n"
                "  SBOM          | Software Bill of Materials\n"
                "  KRaft         | Kafka Raft consensus protocol\n"
                "  DLQ           | Dead Letter Queue\n"
                "  CMK           | Customer Managed Key\n"
                "  SSRF          | Server-Side Request Forgery\n\n"
                "Appendix B: Reference Architecture Diagrams\n\n"
                "  Diagram B.1: High-level system architecture (see Confluence: /arch/hld)\n"
                "  Diagram B.2: Network topology (see Confluence: /arch/network)\n"
                "  Diagram B.3: Data flow diagram (see Confluence: /arch/dataflow)\n"
                "  Diagram B.4: Deployment pipeline (see Confluence: /arch/cicd)\n\n"
                "Appendix C: Contact Information\n\n"
                "  Role                | Name            | Email\n"
                "  ------------------- | --------------- | -------------------\n"
                "  Chief Architect     | Sarah Chen      | s.chen@cloudbridge.io\n"
                "  Lead SRE            | Marcus Johnson  | m.johnson@cloudbridge.io\n"
                "  Security Lead       | Priya Patel     | p.patel@cloudbridge.io\n"
                "  Database Lead       | Erik Lindqvist  | e.lindqvist@cloudbridge.io\n"
                "  Platform Lead       | James Okafor    | j.okafor@cloudbridge.io\n\n"
                "Document revision history:\n"
                "  v3.2 (2025-03-15): Updated caching strategy, added chaos engineering\n"
                "  v3.1 (2025-01-10): Revised DR procedures, added capacity planning\n"
                "  v3.0 (2024-11-01): Major rewrite for Kubernetes migration\n"
                "  v2.5 (2024-08-15): Added search engine integration chapter"
            ),
        },
    ]

    # Build TOC entries
    toc_entries = []
    page_num = 1

    for i, ch in enumerate(chapters):
        if ch.get("is_cover"):
            # Cover page
            page = doc.new_page(width=W, height=H)
            # Title centered
            title_rect = pymupdf.Rect(MARGIN, 250, W - MARGIN, 400)
            page.insert_textbox(
                title_rect,
                ch["title"],
                fontsize=28,
                fontname="hebo",
                color=(0.1, 0.15, 0.35),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            # Subtitle
            sub_rect = pymupdf.Rect(MARGIN, 420, W - MARGIN, 580)
            page.insert_textbox(
                sub_rect,
                ch["subtitle"],
                fontsize=13,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            # Decorative line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(150, 410), pymupdf.Point(W - 150, 410))
            shape.finish(color=(0.2, 0.3, 0.6), width=2)
            shape.commit()
            toc_entries.append([1, "Cover", page_num])
        else:
            page = doc.new_page(width=W, height=H)
            # Header
            page.insert_text(
                pymupdf.Point(MARGIN, 50),
                "CloudBridge Platform - Technical Design Specification v3.2",
                fontsize=8,
                fontname="heit",
                color=(0.5, 0.5, 0.5),
            )
            # Header line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(MARGIN, 58), pymupdf.Point(W - MARGIN, 58))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()

            # Chapter title
            page.insert_text(
                pymupdf.Point(MARGIN, 90),
                ch["title"],
                fontsize=18,
                fontname="hebo",
                color=(0.1, 0.15, 0.35),
            )

            # Body text
            if "body" in ch:
                body_rect = pymupdf.Rect(MARGIN, 110, W - MARGIN, H - 60)
                page.insert_textbox(
                    body_rect,
                    ch["body"],
                    fontsize=10,
                    fontname="helv",
                    color=(0.1, 0.1, 0.1),
                    align=pymupdf.TEXT_ALIGN_LEFT,
                )

            # Footer with page number
            page.insert_text(
                pymupdf.Point(W / 2 - 10, H - 40),
                str(page_num),
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

            toc_entries.append([1, ch["title"], page_num])

        page_num += 1

    # Set TOC bookmarks
    doc.set_toc(toc_entries)

    # Set metadata
    doc.set_metadata({
        "title": "CloudBridge Platform - Technical Design Specification v3.2",
        "author": "Systems Architecture Division",
        "subject": "Technical Design Specification",
        "keywords": "cloudbridge, architecture, microservices, specification",
        "creator": "CloudBridge Documentation Team",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {len(chapters)}')

    # Open in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
