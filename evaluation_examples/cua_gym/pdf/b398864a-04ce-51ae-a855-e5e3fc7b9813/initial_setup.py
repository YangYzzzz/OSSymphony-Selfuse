"""
Initial Setup: Create a 20-page technical specification PDF with 'Appendix' appearing 9 times.
Task ID: pdf_gf2_035
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user/Documents'
OUTPUT = f'{WORKDIR}/technical_spec.pdf'

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
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter)
    W, H = 612, 792
    LEFT = 72
    RIGHT = W - 72
    TOP = 72
    BOTTOM = H - 72
    TEXT_WIDTH = RIGHT - LEFT

    # We need 'Appendix' to appear exactly 9 times across 20 pages.
    # Distribution plan:
    #   Page 1 (title): 0
    #   Page 2 (TOC): 1 occurrence ("Appendix A: Glossary" in TOC)
    #   Pages 3-7 (Intro, Requirements, Architecture, Implementation, Testing): 0
    #   Page 8 (Integration): 1 occurrence ("See Appendix B for details")
    #   Pages 9-10 (Performance, Security): 0
    #   Page 11 (Deployment): 1 occurrence ("Refer to Appendix C")
    #   Pages 12-14 (Maintenance, API Reference, Data Models): 0
    #   Page 15 (Error Handling): 1 occurrence ("Appendix D contains error codes")
    #   Page 16 (Migration Guide): 0
    #   Page 17 (Compliance): 1 occurrence ("as outlined in Apend... Appendix E")
    #   Page 18 (Appendix A title + 2 refs): 3 occurrences
    #   Page 19 (Appendix B): 1 occurrence
    #   Page 20 (References): 0
    # Total: 1+1+1+1+1+3+1 = 9

    sections = []

    # --- Page 1: Title Page ---
    sections.append({
        'title': None,
        'content': [
            (250, 'hebo', 24, 'CloudSync Platform'),
            (290, 'hebo', 20, 'Technical Specification Document'),
            (340, 'helv', 14, 'Version 3.2.1'),
            (370, 'helv', 12, 'Prepared by: Engineering Division'),
            (390, 'helv', 12, 'Meridian Software Solutions, Inc.'),
            (420, 'helv', 12, 'Document ID: TSP-2025-0472'),
            (440, 'helv', 12, 'Classification: Internal / Confidential'),
            (480, 'helv', 11, 'Last Updated: March 15, 2025'),
            (500, 'helv', 11, 'Review Cycle: Quarterly'),
        ]
    })

    # --- Page 2: Table of Contents ---  (1 occurrence of 'Appendix')
    sections.append({
        'title': 'Table of Contents',
        'content_lines': [
            '1. Introduction .................................................. 3',
            '2. System Requirements .......................................... 4',
            '3. Architecture Overview ......................................... 5',
            '4. Implementation Details ........................................ 6',
            '5. Testing Strategy .............................................. 7',
            '6. Integration Guidelines ........................................ 8',
            '7. Performance Benchmarks ........................................ 9',
            '8. Security Framework ............................................ 10',
            '9. Deployment Procedures ......................................... 11',
            '10. Maintenance & Support ........................................ 12',
            '11. API Reference ................................................ 13',
            '12. Data Models .................................................. 14',
            '13. Error Handling ............................................... 15',
            '14. Migration Guide .............................................. 16',
            '15. Compliance & Regulations ..................................... 17',
            'Appendix A: Glossary of Terms .................................... 18',
            'B: Supplementary Diagrams ........................................ 19',
            '16. References ................................................... 20',
        ]
    })

    # --- Page 3: Introduction ---
    sections.append({
        'title': '1. Introduction',
        'content_lines': [
            'The CloudSync Platform is a distributed cloud-based synchronization system designed to',
            'provide real-time data replication across geographically distributed data centers. This',
            'document outlines the complete technical specification for version 3.2.1 of the platform,',
            'covering all aspects from high-level architecture to implementation-specific details.',
            '',
            'The platform serves as the backbone for enterprise-grade data consistency, supporting',
            'over 2.4 million concurrent connections with sub-millisecond latency guarantees. Built',
            'on a microservices architecture, it leverages Apache Kafka for event streaming, Redis',
            'for distributed caching, and PostgreSQL 16 for persistent storage.',
            '',
            'Key objectives of this release include:',
            '  - Enhanced throughput: 340% improvement over version 3.1.0',
            '  - Reduced failover time: from 12 seconds to under 800 milliseconds',
            '  - Multi-region conflict resolution using vector clock algorithms',
            '  - Native support for ARM64 architecture (AWS Graviton3)',
            '',
            'This specification is intended for senior engineers, system architects, and DevOps',
            'teams responsible for deploying and maintaining the CloudSync infrastructure.',
        ]
    })

    # --- Page 4: System Requirements ---
    sections.append({
        'title': '2. System Requirements',
        'content_lines': [
            'Minimum Hardware Requirements (per node):',
            '  - CPU: 8 cores / 16 threads (Intel Xeon Gold 6348 or equivalent)',
            '  - RAM: 64 GB DDR4 ECC (128 GB recommended for production)',
            '  - Storage: 2 TB NVMe SSD (Samsung PM9A3 or equivalent)',
            '  - Network: 25 Gbps Ethernet (dual-port for redundancy)',
            '',
            'Software Dependencies:',
            '  - Operating System: Ubuntu 22.04 LTS or RHEL 9.x',
            '  - Container Runtime: Docker 24.0+ or containerd 1.7+',
            '  - Orchestration: Kubernetes 1.28+ with Calico CNI',
            '  - JVM: OpenJDK 21 (Temurin distribution)',
            '  - Python: 3.11+ (for monitoring scripts and data pipelines)',
            '',
            'Network Requirements:',
            '  - Inter-node latency: < 5ms within same region',
            '  - Cross-region bandwidth: minimum 10 Gbps dedicated',
            '  - DNS resolution: internal service mesh (Istio 1.20+)',
            '  - TLS 1.3 mandatory for all inter-service communication',
            '',
            'Storage Configuration:',
            '  - RAID 10 for database volumes',
            '  - Separate volumes for WAL logs and data files',
            '  - Minimum 20,000 IOPS per storage volume',
        ]
    })

    # --- Page 5: Architecture Overview ---
    sections.append({
        'title': '3. Architecture Overview',
        'content_lines': [
            'The CloudSync Platform follows a layered microservices architecture with clear',
            'separation of concerns across five primary layers:',
            '',
            'Layer 1 - Ingestion Gateway:',
            '  Handles incoming client connections via gRPC and REST APIs. The gateway performs',
            '  authentication, rate limiting (token bucket algorithm, 10K req/s per tenant),',
            '  and request routing to appropriate service clusters.',
            '',
            'Layer 2 - Event Processing:',
            '  Apache Kafka clusters (3 brokers minimum) process incoming sync events. Each',
            '  event is assigned a globally unique timestamp using hybrid logical clocks (HLC).',
            '  Partition strategy: hash(tenant_id + resource_id) mod 256.',
            '',
            'Layer 3 - Conflict Resolution Engine:',
            '  Implements Lamport timestamps with vector clock fallback for concurrent writes.',
            '  The engine uses a three-phase merge protocol:',
            '    Phase 1: Detect conflicts via version vector comparison',
            '    Phase 2: Apply domain-specific merge strategies (LWW, CRDT, custom)',
            '    Phase 3: Propagate resolved state to all replicas',
            '',
            'Layer 4 - Persistence:',
            '  PostgreSQL 16 with logical replication for cross-region data consistency.',
            '  Connection pooling via PgBouncer (max 500 connections per pool).',
            '',
            'Layer 5 - Monitoring & Observability:',
            '  Prometheus + Grafana for metrics, Jaeger for distributed tracing,',
            '  and ELK stack for centralized logging.',
        ]
    })

    # --- Page 6: Implementation Details ---
    sections.append({
        'title': '4. Implementation Details',
        'content_lines': [
            'Core Service Implementation:',
            '',
            'The synchronization engine is implemented in Rust (v1.75) for the hot path,',
            'with Go (v1.22) services handling orchestration and coordination. Key modules:',
            '',
            'sync-core (Rust):',
            '  - Binary protocol parser with zero-copy deserialization (serde + rkyv)',
            '  - Lock-free concurrent hash map for in-flight operation tracking',
            '  - Custom memory allocator (jemalloc) tuned for 64-byte cache lines',
            '  - Throughput: 1.2M operations/second on single node benchmark',
            '',
            'coordinator-svc (Go):',
            '  - Raft consensus implementation for leader election',
            '  - gRPC streaming for real-time state propagation',
            '  - Circuit breaker pattern (Hystrix-compatible) for downstream calls',
            '  - Health check interval: 250ms with 3-strike failure detection',
            '',
            'Data Serialization:',
            '  All inter-service communication uses Protocol Buffers v3 with the following',
            '  schema versioning strategy:',
            '    - Major version: breaking changes (new .proto file)',
            '    - Minor version: additive fields (backward compatible)',
            '    - Wire format: varint encoding with LZ4 compression (ratio ~3.2:1)',
            '',
            'Concurrency Model:',
            '  The platform uses a hybrid threading model combining OS threads for CPU-bound',
            '  work (Rust tokio runtime, 4 worker threads per core) with green threads for',
            '  I/O-bound operations (Go goroutines, default GOMAXPROCS).',
        ]
    })

    # --- Page 7: Testing Strategy ---
    sections.append({
        'title': '5. Testing Strategy',
        'content_lines': [
            'The CloudSync testing framework operates across four levels:',
            '',
            'Unit Tests:',
            '  - Coverage target: 85% line coverage, 75% branch coverage',
            '  - Framework: Rust (cargo test), Go (testing + testify)',
            '  - Mocking: mockall (Rust), gomock (Go)',
            '  - Execution time budget: < 5 minutes for full unit suite',
            '',
            'Integration Tests:',
            '  - Testcontainers for ephemeral Kafka, PostgreSQL, Redis instances',
            '  - Contract tests using Pact framework for API compatibility',
            '  - Chaos injection: network partitions, random process kills',
            '  - Target: 100% of critical paths covered',
            '',
            'Performance Tests:',
            '  - Load testing with k6 (100K virtual users, 30-minute sustained)',
            '  - Latency percentiles: p50 < 2ms, p95 < 10ms, p99 < 50ms',
            '  - Throughput regression gate: no more than 5% degradation',
            '  - Memory leak detection: RSS growth < 1% over 24-hour soak test',
            '',
            'End-to-End Tests:',
            '  - Selenium-based UI verification for admin dashboard',
            '  - Multi-region simulation using network namespaces',
            '  - Data integrity validation: SHA-256 checksum comparison',
            '  - Full E2E suite runtime: approximately 45 minutes',
            '',
            'All tests run in CI/CD pipeline (GitHub Actions) with parallel execution.',
            'Flaky test quarantine policy: 3 consecutive failures triggers isolation.',
        ]
    })

    # --- Page 8: Integration Guidelines --- (1 occurrence: "See Appendix B")
    sections.append({
        'title': '6. Integration Guidelines',
        'content_lines': [
            'Third-party systems can integrate with CloudSync via the following channels:',
            '',
            'REST API (v3):',
            '  Base URL: https://api.cloudsync.io/v3/',
            '  Authentication: OAuth 2.0 with PKCE flow',
            '  Rate limits: 1,000 requests/minute (Standard), 10,000 (Enterprise)',
            '  Pagination: cursor-based with opaque continuation tokens',
            '',
            'Webhook Notifications:',
            '  CloudSync delivers real-time event notifications via HTTPS webhooks.',
            '  Supported events: sync.completed, sync.failed, conflict.detected,',
            '  resource.created, resource.updated, resource.deleted.',
            '  Retry policy: exponential backoff (1s, 2s, 4s, 8s, 16s) with 5 attempts.',
            '',
            'SDK Support:',
            '  Official SDKs available for: Python, Java, Go, TypeScript, C#.',
            '  Community SDKs: Rust, Ruby, PHP (maintained by partner organizations).',
            '',
            'See Appendix B for detailed integration sequence diagrams and sample',
            'request/response payloads for each endpoint.',
            '',
            'Migration from v2 API:',
            '  The v3 API is not backward-compatible with v2. Key changes include:',
            '  - Authentication switch from API keys to OAuth 2.0',
            '  - Resource identifiers changed from integer IDs to UUIDs',
            '  - Batch operations now use JSON:API bulk extension',
            '  - Deprecated endpoints removed: /sync/legacy, /admin/v1',
        ]
    })

    # --- Page 9: Performance Benchmarks ---
    sections.append({
        'title': '7. Performance Benchmarks',
        'content_lines': [
            'Benchmark Environment:',
            '  - 5-node cluster (c6i.8xlarge instances on AWS)',
            '  - Network: 25 Gbps dedicated VPC peering',
            '  - Dataset: 50 million records (avg 2.4 KB per record)',
            '',
            'Results Summary (v3.2.1 vs v3.1.0):',
            '',
            '  Metric                    v3.1.0      v3.2.1      Change',
            '  -------------------------------------------------------',
            '  Write throughput (ops/s)   312,000     1,064,000   +341%',
            '  Read throughput (ops/s)    890,000     2,150,000   +142%',
            '  p50 latency (ms)          3.2         1.1         -66%',
            '  p99 latency (ms)          45.0        12.3        -73%',
            '  Failover time (s)         12.4        0.78        -94%',
            '  Memory per node (GB)      48.2        31.7        -34%',
            '  CPU utilization (%)       78          52          -33%',
            '',
            'The dramatic improvements in v3.2.1 are attributed to:',
            '  1. Migration from Java to Rust for the sync-core module',
            '  2. Adoption of io_uring for asynchronous I/O on Linux 5.15+',
            '  3. Custom memory allocator replacing system malloc',
            '  4. Batch commit optimization reducing fsync calls by 87%',
            '',
            'Scalability testing confirms linear throughput scaling up to 20 nodes,',
            'with diminishing returns beyond 24 nodes due to coordination overhead.',
        ]
    })

    # --- Page 10: Security Framework ---
    sections.append({
        'title': '8. Security Framework',
        'content_lines': [
            'The CloudSync security model implements defense-in-depth across all layers:',
            '',
            'Authentication & Authorization:',
            '  - OAuth 2.0 with PKCE for client applications',
            '  - mTLS (mutual TLS) for inter-service communication',
            '  - RBAC with fine-grained permissions (read, write, admin, audit)',
            '  - Session tokens: JWT with RS256 signing, 15-minute expiry',
            '  - MFA enforcement for admin-level operations',
            '',
            'Encryption:',
            '  - Data at rest: AES-256-GCM with envelope encryption (AWS KMS)',
            '  - Data in transit: TLS 1.3 (ECDHE-ECDSA-AES256-GCM-SHA384)',
            '  - Key rotation: automatic every 90 days, manual rotation supported',
            '  - Client-side encryption option for sensitive payloads',
            '',
            'Audit & Compliance:',
            '  - All API calls logged with request/response metadata',
            '  - Immutable audit trail stored in append-only log (Kafka topic)',
            '  - GDPR data residency controls: per-tenant region pinning',
            '  - SOC 2 Type II certified (annual audit by Deloitte)',
            '  - HIPAA-compliant configuration available for healthcare tenants',
            '',
            'Vulnerability Management:',
            '  - Weekly dependency scanning (Snyk + Trivy)',
            '  - Quarterly penetration testing by external firm',
            '  - Bug bounty program via HackerOne (scope: *.cloudsync.io)',
            '  - Mean time to patch critical vulnerabilities: < 48 hours',
        ]
    })

    # --- Page 11: Deployment Procedures --- (1 occurrence: "Refer to Appendix C")
    sections.append({
        'title': '9. Deployment Procedures',
        'content_lines': [
            'CloudSync deployments follow a blue-green strategy with automated rollback:',
            '',
            'Pre-deployment Checklist:',
            '  1. All CI/CD pipeline stages passed (build, test, security scan)',
            '  2. Change request approved by at least 2 senior engineers',
            '  3. Deployment window confirmed (Tuesday/Thursday, 02:00-06:00 UTC)',
            '  4. Rollback plan documented and tested in staging environment',
            '',
            'Deployment Steps:',
            '  1. Deploy new version to "green" environment',
            '  2. Run smoke tests against green (5-minute timeout)',
            '  3. Shift 10% traffic via weighted DNS (canary phase, 15 minutes)',
            '  4. Monitor error rates and latency dashboards',
            '  5. If metrics nominal: shift 50%, then 100% traffic',
            '  6. Decommission "blue" environment after 24-hour bake period',
            '',
            'Rollback Criteria (automatic):',
            '  - Error rate exceeds 0.1% (5xx responses)',
            '  - p99 latency exceeds 100ms for more than 2 minutes',
            '  - Any health check failure on critical service',
            '',
            'Refer to Appendix C for environment-specific configuration templates',
            'and Terraform modules used for infrastructure provisioning.',
            '',
            'Database migrations are handled separately via Flyway with a strict',
            'forward-only policy. Schema changes must be backward-compatible for',
            'at least one release cycle to support rolling deployments.',
        ]
    })

    # --- Page 12: Maintenance & Support ---
    sections.append({
        'title': '10. Maintenance & Support',
        'content_lines': [
            'Operational Runbooks:',
            '',
            'Incident Response:',
            '  - Severity 1 (service down): 15-minute response, 1-hour resolution target',
            '  - Severity 2 (degraded): 30-minute response, 4-hour resolution target',
            '  - Severity 3 (minor): next business day response',
            '  - On-call rotation: weekly, 2 primary + 1 backup engineer',
            '',
            'Routine Maintenance Tasks:',
            '  - Log rotation: daily, 30-day retention (90 days for audit logs)',
            '  - Database vacuuming: weekly (autovacuum + manual full vacuum monthly)',
            '  - Certificate renewal: automated via cert-manager (Let\'s Encrypt)',
            '  - Dependency updates: monthly security patches, quarterly minor versions',
            '',
            'Monitoring Alerts:',
            '  - Disk usage > 80%: warning (PagerDuty, Slack)',
            '  - Disk usage > 90%: critical (PagerDuty + phone call)',
            '  - Replication lag > 5 seconds: warning',
            '  - Replication lag > 30 seconds: critical',
            '  - Connection pool exhaustion > 85%: warning',
            '',
            'Capacity Planning:',
            '  Current utilization (as of Q1 2025):',
            '  - Storage: 12.4 TB / 20 TB allocated (62%)',
            '  - Compute: average 52% CPU across 15 nodes',
            '  - Network: peak 8.2 Gbps / 25 Gbps capacity (33%)',
            '  Projected growth: 40% YoY, next capacity expansion: Q3 2025',
        ]
    })

    # --- Page 13: API Reference ---
    sections.append({
        'title': '11. API Reference',
        'content_lines': [
            'Core Endpoints:',
            '',
            'POST /v3/sync/push',
            '  Description: Push local changes to CloudSync',
            '  Request Body: { "changes": [...], "base_version": "uuid" }',
            '  Response: 200 OK { "version": "uuid", "conflicts": [...] }',
            '  Rate Limit: 500 req/min (Standard), 5000 (Enterprise)',
            '',
            'GET /v3/sync/pull?since={version}',
            '  Description: Pull remote changes since specified version',
            '  Response: 200 OK { "changes": [...], "current_version": "uuid" }',
            '  Pagination: cursor-based, max 1000 changes per page',
            '',
            'POST /v3/sync/resolve',
            '  Description: Submit conflict resolution decisions',
            '  Request Body: { "conflict_id": "uuid", "resolution": "local|remote|merge" }',
            '  Response: 200 OK { "resolved_version": "uuid" }',
            '',
            'GET /v3/resources/{id}',
            '  Description: Retrieve a specific synchronized resource',
            '  Response: 200 OK { "id": "uuid", "data": {...}, "metadata": {...} }',
            '',
            'DELETE /v3/resources/{id}',
            '  Description: Soft-delete a resource (recoverable for 30 days)',
            '  Response: 204 No Content',
            '',
            'GET /v3/admin/health',
            '  Description: System health check (no authentication required)',
            '  Response: 200 OK { "status": "healthy", "components": {...} }',
        ]
    })

    # --- Page 14: Data Models ---
    sections.append({
        'title': '12. Data Models',
        'content_lines': [
            'Core Entity Schema:',
            '',
            'SyncResource:',
            '  - id: UUID (v4, globally unique)',
            '  - tenant_id: UUID (foreign key to Tenant)',
            '  - resource_type: VARCHAR(64) (e.g., "document", "image", "config")',
            '  - content_hash: CHAR(64) (SHA-256 of resource content)',
            '  - version_vector: JSONB (e.g., {"node_a": 5, "node_b": 3})',
            '  - created_at: TIMESTAMPTZ (ISO 8601)',
            '  - updated_at: TIMESTAMPTZ',
            '  - deleted_at: TIMESTAMPTZ (nullable, soft delete)',
            '  - metadata: JSONB (user-defined key-value pairs)',
            '',
            'SyncEvent:',
            '  - event_id: BIGSERIAL (monotonically increasing)',
            '  - resource_id: UUID (foreign key to SyncResource)',
            '  - operation: ENUM (CREATE, UPDATE, DELETE, CONFLICT, RESOLVE)',
            '  - payload: BYTEA (compressed Protocol Buffer)',
            '  - hlc_timestamp: BIGINT (hybrid logical clock value)',
            '  - origin_node: VARCHAR(128) (node identifier)',
            '  - kafka_offset: BIGINT (for exactly-once processing)',
            '',
            'ConflictRecord:',
            '  - conflict_id: UUID',
            '  - resource_id: UUID',
            '  - local_version: JSONB (version vector)',
            '  - remote_version: JSONB (version vector)',
            '  - resolution_strategy: VARCHAR(32)',
            '  - resolved_by: UUID (nullable, user who resolved)',
            '  - resolved_at: TIMESTAMPTZ (nullable)',
            '',
            'Indexes: B-tree on (tenant_id, resource_type), GIN on metadata JSONB,',
            'BRIN on created_at for time-range queries.',
        ]
    })

    # --- Page 15: Error Handling --- (1 occurrence: "Appendix D contains error codes")
    sections.append({
        'title': '13. Error Handling',
        'content_lines': [
            'Error Response Format (JSON:API compliant):',
            '  {',
            '    "errors": [{',
            '      "status": "409",',
            '      "code": "SYNC_CONFLICT",',
            '      "title": "Synchronization Conflict Detected",',
            '      "detail": "Resource version mismatch on field: content",',
            '      "source": { "pointer": "/data/attributes/content" }',
            '    }]',
            '  }',
            '',
            'Error Categories:',
            '  4xx Client Errors:',
            '    400 - Invalid request format or missing required fields',
            '    401 - Authentication failure (expired token, invalid credentials)',
            '    403 - Insufficient permissions for requested operation',
            '    404 - Resource not found or soft-deleted',
            '    409 - Synchronization conflict requiring resolution',
            '    429 - Rate limit exceeded (Retry-After header included)',
            '',
            '  5xx Server Errors:',
            '    500 - Unhandled internal error (auto-reported to engineering)',
            '    502 - Upstream service unavailable (Kafka, PostgreSQL)',
            '    503 - Service temporarily unavailable (maintenance or overload)',
            '    504 - Operation timeout (default: 30 seconds)',
            '',
            'Appendix D contains error codes with detailed descriptions, common',
            'causes, and recommended remediation steps for each error type.',
            '',
            'Circuit Breaker States:',
            '  - CLOSED: normal operation, all requests forwarded',
            '  - OPEN: failure threshold exceeded, requests fail-fast for 30s',
            '  - HALF-OPEN: single probe request allowed to test recovery',
        ]
    })

    # --- Page 16: Migration Guide ---
    sections.append({
        'title': '14. Migration Guide',
        'content_lines': [
            'Migrating from CloudSync v2.x to v3.x:',
            '',
            'Phase 1 - Assessment (1-2 weeks):',
            '  - Inventory all v2 API integrations using access logs',
            '  - Identify deprecated endpoints in use (/sync/legacy, /admin/v1)',
            '  - Assess custom webhook handlers for compatibility',
            '  - Document all API key credentials for OAuth 2.0 migration',
            '',
            'Phase 2 - Development (2-4 weeks):',
            '  - Update SDK to v3 (pip install cloudsync-sdk>=3.0)',
            '  - Replace API key auth with OAuth 2.0 PKCE flow',
            '  - Convert integer resource IDs to UUID format',
            '  - Update webhook handlers for new event schema',
            '  - Implement cursor-based pagination (replacing offset-based)',
            '',
            'Phase 3 - Testing (1-2 weeks):',
            '  - Run integration tests against v3 staging environment',
            '  - Perform load testing at 2x expected production volume',
            '  - Validate data integrity with cross-version checksum comparison',
            '  - Test rollback procedure to v2 (dual-write period)',
            '',
            'Phase 4 - Cutover (1 week):',
            '  - Enable dual-write mode (v2 + v3 simultaneously)',
            '  - Gradual traffic shift: 10% -> 50% -> 100% over 3 days',
            '  - Monitor error rates and latency during transition',
            '  - Decommission v2 endpoints after 30-day grace period',
            '',
            'Known Breaking Changes:',
            '  - Batch sync limit reduced from 10,000 to 5,000 items',
            '  - Webhook signature algorithm changed from HMAC-SHA1 to HMAC-SHA256',
            '  - Resource metadata field renamed from "tags" to "metadata"',
        ]
    })

    # --- Page 17: Compliance & Regulations --- (1 occurrence: "as outlined in Appendix E")
    sections.append({
        'title': '15. Compliance & Regulations',
        'content_lines': [
            'CloudSync maintains compliance with the following regulatory frameworks:',
            '',
            'GDPR (General Data Protection Regulation):',
            '  - Data residency: EU tenant data stored exclusively in eu-west-1',
            '  - Right to erasure: automated within 72 hours of request',
            '  - Data portability: export in JSON, CSV, or Protocol Buffer format',
            '  - Privacy impact assessment: updated annually',
            '  - Data Protection Officer: privacy@cloudsync.io',
            '',
            'SOC 2 Type II:',
            '  - Annual audit by Deloitte (last completed: December 2024)',
            '  - Trust Service Criteria: Security, Availability, Confidentiality',
            '  - Audit report available to customers under NDA',
            '',
            'HIPAA (Health Insurance Portability and Accountability Act):',
            '  - Business Associate Agreement (BAA) available for healthcare tenants',
            '  - PHI encryption: AES-256 at rest, TLS 1.3 in transit',
            '  - Access logging: all PHI access recorded with user identity',
            '  - Breach notification: within 24 hours of confirmed incident',
            '',
            'PCI DSS Level 1:',
            '  - Cardholder data isolated in dedicated encryption scope',
            '  - Quarterly vulnerability scans by Approved Scanning Vendor',
            '  - Annual on-site assessment for Level 1 compliance',
            '',
            'Full compliance documentation and certification copies are available',
            'as outlined in Appendix E of the supplementary materials package.',
        ]
    })

    # --- Page 18: Appendix A --- (3 occurrences: title + 2 in text)
    sections.append({
        'title': 'Appendix A: Glossary of Terms',
        'content_lines': [
            'CRDT (Conflict-free Replicated Data Type):',
            '  A data structure that can be replicated across multiple nodes and',
            '  updated independently without coordination, guaranteeing convergence.',
            '',
            'HLC (Hybrid Logical Clock):',
            '  A clock mechanism combining physical timestamps with logical counters',
            '  to provide globally consistent ordering of distributed events.',
            '',
            'LWW (Last-Writer-Wins):',
            '  A conflict resolution strategy where the most recent write (by timestamp)',
            '  takes precedence. Simple but may lose concurrent updates.',
            '',
            'mTLS (Mutual TLS):',
            '  A TLS handshake where both client and server authenticate each other',
            '  using X.509 certificates. Used for service-to-service communication.',
            '',
            'Vector Clock:',
            '  A mechanism for tracking causality in distributed systems. Each node',
            '  maintains a counter, and the vector of all counters determines ordering.',
            '',
            'WAL (Write-Ahead Log):',
            '  A logging mechanism where changes are written to a persistent log before',
            '  being applied to the database, ensuring durability and crash recovery.',
            '',
            'Note: Terms specific to the integration layer are documented in the',
            'companion Appendix reference guide. Additional terminology related to',
            'the Appendix B supplementary diagrams may also be relevant.',
        ]
    })

    # --- Page 19: Appendix B --- (1 occurrence in title)
    sections.append({
        'title': 'Appendix B: Supplementary Diagrams',
        'content_lines': [
            'This section contains supplementary architectural and sequence diagrams',
            'referenced throughout the technical specification.',
            '',
            'Diagram B.1 - Data Flow Overview:',
            '  Client -> API Gateway -> Kafka Topic -> Sync Engine -> PostgreSQL',
            '                                      -> Redis Cache',
            '                                      -> Webhook Dispatcher',
            '',
            'Diagram B.2 - Conflict Resolution Sequence:',
            '  1. Node A sends update (version: {a:5, b:3})',
            '  2. Node B sends update (version: {a:4, b:4})',
            '  3. Coordinator detects concurrent versions (neither dominates)',
            '  4. Merge strategy applied based on resource type configuration',
            '  5. Resolved version propagated: {a:5, b:4, coordinator:1}',
            '',
            'Diagram B.3 - Blue-Green Deployment Flow:',
            '  Active (Blue) <- 100% Traffic <- Load Balancer',
            '  Standby (Green) <- 0% Traffic',
            '  [Deploy to Green] -> [Smoke Test] -> [Canary 10%] -> [Full Switch]',
            '',
            'Diagram B.4 - Authentication Flow (OAuth 2.0 PKCE):',
            '  1. Client generates code_verifier and code_challenge',
            '  2. Redirect to /authorize with code_challenge',
            '  3. User authenticates, receives authorization code',
            '  4. Client exchanges code + code_verifier for access token',
            '  5. Access token (JWT, 15-min expiry) used for API calls',
            '  6. Refresh token (7-day expiry) used to obtain new access tokens',
        ]
    })

    # --- Page 20: References ---
    sections.append({
        'title': '16. References',
        'content_lines': [
            '[1] Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a',
            '    Distributed System." Communications of the ACM, 21(7), 558-565.',
            '',
            '[2] Shapiro, M. et al. (2011). "Conflict-Free Replicated Data Types."',
            '    Proceedings of the 13th International Symposium on Stabilization,',
            '    Safety, and Security of Distributed Systems (SSS 2011).',
            '',
            '[3] Kleppmann, M. (2017). "Designing Data-Intensive Applications."',
            '    O\'Reilly Media. ISBN: 978-1449373320.',
            '',
            '[4] Vogels, W. (2009). "Eventually Consistent." Communications of the ACM,',
            '    52(1), 40-44.',
            '',
            '[5] Ongaro, D. & Ousterhout, J. (2014). "In Search of an Understandable',
            '    Consensus Algorithm (Raft)." USENIX ATC 2014.',
            '',
            '[6] AWS Well-Architected Framework (2024). "Reliability Pillar."',
            '    Amazon Web Services. https://docs.aws.amazon.com/wellarchitected/',
            '',
            '[7] NIST SP 800-53 Rev. 5 (2020). "Security and Privacy Controls for',
            '    Information Systems and Organizations." National Institute of',
            '    Standards and Technology.',
            '',
            '[8] PostgreSQL 16 Documentation (2024). "Logical Replication."',
            '    https://www.postgresql.org/docs/16/logical-replication.html',
            '',
            '[9] Apache Kafka Documentation (2024). "Design." Version 3.7.',
            '    https://kafka.apache.org/documentation/#design',
            '',
            'Document Revision History:',
            '  v3.2.1 - March 2025: Performance benchmarks updated, security patches',
            '  v3.2.0 - January 2025: ARM64 support, new deployment procedures',
            '  v3.1.0 - October 2024: Initial v3 release',
        ]
    })

    # Now render all sections into the PDF
    for idx, section in enumerate(sections):
        page = doc.new_page(width=W, height=H)

        if idx == 0:
            # Title page - special layout
            for (y, fontname, fontsize, text) in section['content']:
                tw = page.rect.width
                text_rect = pymupdf.Rect(LEFT, y, RIGHT, y + fontsize + 10)
                page.insert_textbox(text_rect, text, fontsize=fontsize, fontname=fontname,
                                    color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)
        else:
            y_pos = TOP
            # Section title
            if section.get('title'):
                page.insert_text(pymupdf.Point(LEFT, y_pos + 18), section['title'],
                                 fontsize=18, fontname='hebo', color=(0, 0.15, 0.4))
                y_pos += 36

                # Separator line
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(LEFT, y_pos), pymupdf.Point(RIGHT, y_pos))
                shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
                shape.commit()
                y_pos += 12

            # Content lines
            if 'content_lines' in section:
                for line in section['content_lines']:
                    if line == '':
                        y_pos += 8
                        continue
                    if y_pos > BOTTOM - 20:
                        break
                    page.insert_text(pymupdf.Point(LEFT, y_pos + 11), line,
                                     fontsize=10, fontname='helv', color=(0, 0, 0))
                    y_pos += 15

        # Page number (skip title page)
        if idx > 0:
            page.insert_text(pymupdf.Point(W / 2 - 10, H - 36),
                             str(idx + 1), fontsize=9, fontname='helv', color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()

    # Verify 'Appendix' count
    verify_doc = pymupdf.open(OUTPUT)
    count = 0
    for page in verify_doc:
        instances = page.search_for('Appendix')
        count += len(instances)
    page_count = verify_doc.page_count
    verify_doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total "Appendix" occurrences found: {count}')
    print(f'Page count: {page_count}')

    # Verify no annotations
    verify_doc = pymupdf.open(OUTPUT)
    annot_count = 0
    for page in verify_doc:
        for annot in page.annots():
            annot_count += 1
    verify_doc.close()
    print(f'Annotation count: {annot_count}')

    # Open in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
