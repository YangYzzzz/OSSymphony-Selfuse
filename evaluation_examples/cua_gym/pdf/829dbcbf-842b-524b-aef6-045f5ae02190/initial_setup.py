"""
Initial Setup: Create a 20-page system_design.pdf with a component diagram on page 10
Task ID: pdf_fm_040
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_040'
DOC_DIR = f'{WORKDIR}/Documents/engineering'
OUTPUT = f'{DOC_DIR}/system_design.pdf'

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

def draw_component_box(shape, x, y, w, h, label, color=(0.2, 0.4, 0.7)):
    """Draw a UML-style component box."""
    rect = pymupdf.Rect(x, y, x + w, y + h)
    shape.draw_rect(rect)
    shape.finish(color=color, fill=(0.9, 0.93, 0.97), width=1.5)
    # Small component icon tabs
    tab_w, tab_h = 12, 6
    shape.draw_rect(pymupdf.Rect(x - 6, y + 8, x + 6, y + 8 + tab_h))
    shape.finish(color=color, fill=(0.85, 0.9, 0.95), width=1)
    shape.draw_rect(pymupdf.Rect(x - 6, y + 18, x + 6, y + 18 + tab_h))
    shape.finish(color=color, fill=(0.85, 0.9, 0.95), width=1)

def draw_arrow(shape, x1, y1, x2, y2, color=(0.3, 0.3, 0.3)):
    """Draw a line with arrowhead."""
    shape.draw_line(pymupdf.Point(x1, y1), pymupdf.Point(x2, y2))
    shape.finish(color=color, width=1.2)

def create_initial():
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # Page titles/content for a realistic 20-page system design document
    chapters = [
        ("System Design Document", "Prepared by: Engineering Team\nVersion 3.2\nDate: March 2025\nConfidential"),
        ("Table of Contents", "1. Executive Summary .............. 3\n2. System Overview ................ 4\n3. Architecture Principles ........ 5\n4. Frontend Architecture .......... 6\n5. Backend Services ............... 7\n6. Data Layer ..................... 8\n7. Authentication & Security ...... 9\n8. Infrastructure ................. 10\n9. Integration Points ............. 11\n10. Component Diagram ............. 12\n11. Data Flow ..................... 13\n12. Deployment Strategy ........... 14\n13. Monitoring & Observability .... 15\n14. Disaster Recovery ............. 16\n15. Performance Requirements ...... 17\n16. Security Compliance ........... 18\n17. Testing Strategy .............. 19\n18. Appendix ...................... 20"),
        ("1. Executive Summary", "This document outlines the complete system architecture for the CloudPlatform v3.2 release. The platform serves 2.4 million monthly active users across 18 regions and processes an average of 45,000 API requests per second during peak hours.\n\nKey architectural decisions include the migration from a monolithic service to a microservices architecture, adoption of event-driven communication patterns, and implementation of a multi-region active-active deployment strategy.\n\nThe system is designed to meet 99.99% availability SLA with sub-200ms p95 latency for all critical user-facing endpoints."),
        ("2. System Overview", "The CloudPlatform consists of four primary subsystems:\n\n2.1 User-Facing Services\n- Web Application (React SPA)\n- Mobile API Gateway\n- Real-time Collaboration Engine\n\n2.2 Core Business Logic\n- Order Processing Pipeline\n- Inventory Management Service\n- Pricing & Promotions Engine\n- Notification Service\n\n2.3 Data Infrastructure\n- PostgreSQL (primary datastore)\n- Redis (caching layer)\n- Elasticsearch (search & analytics)\n- Apache Kafka (event streaming)\n\n2.4 Supporting Services\n- Authentication & Authorization\n- Configuration Management\n- Feature Flag Service\n- Audit Logging"),
        ("3. Architecture Principles", "The following principles guide all architectural decisions:\n\n3.1 Loose Coupling\nServices communicate through well-defined APIs and asynchronous events. No service should have direct database access to another service's data store.\n\n3.2 High Cohesion\nEach microservice owns a single bounded context and manages its own data lifecycle.\n\n3.3 Resilience\nAll services implement circuit breakers, retry logic with exponential backoff, and graceful degradation patterns.\n\n3.4 Observability\nDistributed tracing (OpenTelemetry), structured logging, and metrics collection are mandatory for all services.\n\n3.5 Security by Design\nZero-trust networking, encryption at rest and in transit, and principle of least privilege for all service accounts."),
        ("4. Frontend Architecture", "The web frontend is built as a React Single Page Application with the following structure:\n\n4.1 Technology Stack\n- React 18 with TypeScript\n- Redux Toolkit for state management\n- React Query for server state\n- Tailwind CSS for styling\n- Vite for build tooling\n\n4.2 Module Structure\n- /auth - Authentication flows\n- /dashboard - Main user dashboard\n- /orders - Order management\n- /settings - User preferences\n- /admin - Administrative tools\n\n4.3 Performance Targets\n- First Contentful Paint: < 1.2s\n- Time to Interactive: < 2.5s\n- Lighthouse Score: > 90\n- Bundle size: < 350KB gzipped"),
        ("5. Backend Services", "5.1 API Gateway (Kong)\n- Rate limiting: 1000 req/min per user\n- Request/response transformation\n- API versioning (v1, v2)\n- JWT validation\n\n5.2 Order Processing Service\n- Language: Go 1.21\n- Framework: gRPC + REST gateway\n- Database: PostgreSQL 15\n- Processes 12,000 orders/minute peak\n\n5.3 Inventory Service\n- Language: Python 3.11\n- Framework: FastAPI\n- Database: PostgreSQL 15\n- Real-time stock tracking with Redis\n\n5.4 Notification Service\n- Language: Node.js 20 LTS\n- Channels: Email (SendGrid), SMS (Twilio), Push (FCM)\n- Queue: Kafka consumer groups"),
        ("6. Data Layer", "6.1 Primary Database (PostgreSQL 15)\n- 3-node cluster (primary + 2 replicas)\n- Connection pooling via PgBouncer\n- Automated backups every 6 hours\n- Point-in-time recovery enabled\n\n6.2 Caching (Redis 7)\n- Session storage\n- API response caching (TTL: 60s)\n- Rate limiting counters\n- Pub/Sub for real-time features\n\n6.3 Search (Elasticsearch 8)\n- Product catalog indexing\n- Full-text search with relevance scoring\n- Analytics aggregations\n- Log aggregation (ELK stack)\n\n6.4 Event Streaming (Kafka 3.5)\n- 12 topic partitions for order events\n- Consumer groups per service\n- 7-day retention policy\n- Schema Registry for Avro schemas"),
        ("7. Authentication & Security", "7.1 Identity Provider\n- OAuth 2.0 / OpenID Connect\n- Multi-factor authentication (TOTP, WebAuthn)\n- SSO integration (SAML 2.0)\n- Session management with Redis\n\n7.2 Authorization\n- Role-Based Access Control (RBAC)\n- Attribute-Based Access Control (ABAC) for fine-grained policies\n- Policy engine: Open Policy Agent (OPA)\n\n7.3 Data Protection\n- TLS 1.3 for all communications\n- AES-256 encryption at rest\n- PII tokenization for sensitive fields\n- Key management via AWS KMS\n\n7.4 Compliance\n- SOC 2 Type II certified\n- GDPR compliant with data residency controls\n- PCI DSS Level 1 for payment processing\n- Annual penetration testing"),
    ]

    # Pages 1-9 (indices 0-8): text content pages
    for i, (title, body) in enumerate(chapters):
        page = doc.new_page(width=W, height=H)
        if i == 0:
            # Title page
            page.insert_text(pymupdf.Point(W/2 - 150, 280), title, fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.5))
            page.insert_textbox(pymupdf.Rect(W/2 - 140, 340, W/2 + 140, 500), body, fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3), align=pymupdf.TEXT_ALIGN_CENTER)
        else:
            # Content pages
            page.insert_text(pymupdf.Point(60, 60), title, fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
            # Underline
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(60, 68), pymupdf.Point(W - 60, 68))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()
            page.insert_textbox(pymupdf.Rect(60, 90, W - 60, H - 60), body, fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

        # Page number (skip title page)
        if i > 0:
            page.insert_text(pymupdf.Point(W/2 - 5, H - 30), str(i + 1), fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Page 10 (index 9): Component Diagram - this is the key page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(60, 60), "10. System Component Diagram", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape_underline = page.new_shape()
    shape_underline.draw_line(pymupdf.Point(60, 68), pymupdf.Point(W - 60, 68))
    shape_underline.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape_underline.commit()

    page.insert_text(pymupdf.Point(60, 90), "Figure 10.1: High-Level Component Architecture", fontsize=10, fontname="heit", color=(0.4, 0.4, 0.4))

    # Draw system component diagram in the center of the page
    shape = page.new_shape()

    # --- Top row: Client Layer ---
    # Web App
    draw_component_box(shape, 80, 140, 120, 50, "Web App", (0.2, 0.5, 0.3))
    page.insert_text(pymupdf.Point(105, 172), "Web App", fontsize=9, fontname="hebo", color=(0.2, 0.4, 0.2))
    # Mobile App
    draw_component_box(shape, 250, 140, 120, 50, "Mobile App", (0.2, 0.5, 0.3))
    page.insert_text(pymupdf.Point(268, 172), "Mobile App", fontsize=9, fontname="hebo", color=(0.2, 0.4, 0.2))
    # Third-party Integrations
    draw_component_box(shape, 420, 140, 130, 50, "3rd Party API", (0.2, 0.5, 0.3))
    page.insert_text(pymupdf.Point(438, 172), "3rd Party API", fontsize=9, fontname="hebo", color=(0.2, 0.4, 0.2))

    # --- API Gateway ---
    draw_component_box(shape, 170, 240, 270, 45, "API Gateway", (0.6, 0.3, 0.2))
    page.insert_text(pymupdf.Point(260, 268), "API Gateway (Kong)", fontsize=10, fontname="hebo", color=(0.5, 0.2, 0.1))

    # --- Middle row: Core Services ---
    services = [
        (60, 340, 110, 50, "Order Svc"),
        (190, 340, 110, 50, "Inventory Svc"),
        (320, 340, 110, 50, "Pricing Svc"),
        (450, 340, 110, 50, "Notification Svc"),
    ]
    for sx, sy, sw, sh, label in services:
        draw_component_box(shape, sx, sy, sw, sh, label)
        page.insert_text(pymupdf.Point(sx + 15, sy + 30), label, fontsize=8, fontname="hebo", color=(0.15, 0.3, 0.55))

    # --- Event Bus ---
    shape.draw_rect(pymupdf.Rect(60, 430, 560, 460))
    shape.finish(color=(0.7, 0.4, 0.1), fill=(1.0, 0.95, 0.85), width=1.5, dashes="[4 2]")
    page.insert_text(pymupdf.Point(255, 452), "Apache Kafka Event Bus", fontsize=9, fontname="hebo", color=(0.6, 0.3, 0.0))

    # --- Bottom row: Data Layer ---
    datastores = [
        (70, 500, 100, 50, "PostgreSQL"),
        (200, 500, 100, 50, "Redis"),
        (330, 500, 110, 50, "Elasticsearch"),
        (470, 500, 80, 50, "S3"),
    ]
    for dx, dy, dw, dh, label in datastores:
        shape.draw_rect(pymupdf.Rect(dx, dy, dx + dw, dy + dh))
        shape.finish(color=(0.5, 0.2, 0.5), fill=(0.95, 0.9, 0.95), width=1.5)
        page.insert_text(pymupdf.Point(dx + 10, dy + 30), label, fontsize=8, fontname="hebo", color=(0.4, 0.15, 0.4))

    # --- Arrows / connections ---
    # Client to gateway
    draw_arrow(shape, 140, 190, 250, 240)
    draw_arrow(shape, 310, 190, 310, 240)
    draw_arrow(shape, 480, 190, 380, 240)

    # Gateway to services
    draw_arrow(shape, 230, 285, 115, 340)
    draw_arrow(shape, 280, 285, 245, 340)
    draw_arrow(shape, 350, 285, 375, 340)
    draw_arrow(shape, 400, 285, 505, 340)

    # Services to event bus
    for sx, sy, sw, sh, _ in services:
        draw_arrow(shape, sx + sw/2, sy + sh, sx + sw/2, 430)

    # Event bus to datastores
    draw_arrow(shape, 120, 460, 120, 500)
    draw_arrow(shape, 250, 460, 250, 500)
    draw_arrow(shape, 385, 460, 385, 500)
    draw_arrow(shape, 510, 460, 510, 500)

    shape.commit()

    # Diagram label at bottom
    page.insert_text(pymupdf.Point(170, 590), "Figure 10.1 — CloudPlatform v3.2 Component Architecture", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))

    page.insert_text(pymupdf.Point(W/2 - 5, H - 30), "10", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Pages 11-20 (indices 10-19): remaining content
    remaining_chapters = [
        ("11. Integration Points", "11.1 Payment Gateway Integration\n- Provider: Stripe (primary), PayPal (secondary)\n- Webhook endpoints for async payment confirmations\n- Idempotency keys for retry safety\n- PCI DSS compliance via tokenized card data\n\n11.2 Email Service\n- Provider: SendGrid\n- Templated transactional emails\n- Batch marketing emails via queue\n- Bounce and complaint handling\n\n11.3 CDN Integration\n- CloudFront distribution for static assets\n- Edge caching with 24-hour TTL\n- Origin failover to S3 backup bucket\n- Custom SSL certificate management"),
        ("12. Data Flow", "12.1 Order Processing Flow\n1. User submits order via Web/Mobile → API Gateway\n2. Gateway validates JWT, rate-checks → Order Service\n3. Order Service creates order record → PostgreSQL\n4. Order Service publishes OrderCreated event → Kafka\n5. Inventory Service consumes event → Reserves stock\n6. Pricing Service consumes event → Calculates final price\n7. Payment Service initiates charge → Stripe API\n8. On success: OrderConfirmed event published\n9. Notification Service sends confirmation email\n10. Analytics pipeline processes event for dashboards"),
        ("13. Deployment Strategy", "13.1 Container Orchestration\n- Kubernetes 1.28 on AWS EKS\n- 3 clusters: us-east-1, eu-west-1, ap-southeast-1\n- Cluster autoscaler: 10-100 nodes per cluster\n- Pod autoscaler: CPU/memory targets at 70%\n\n13.2 CI/CD Pipeline\n- GitHub Actions for CI\n- ArgoCD for GitOps deployment\n- Canary releases with Flagger\n- Automated rollback on error rate > 1%\n\n13.3 Infrastructure as Code\n- Terraform for cloud resources\n- Helm charts for Kubernetes manifests\n- Sealed Secrets for credential management"),
        ("14. Monitoring & Observability", "14.1 Metrics\n- Prometheus for metric collection\n- Grafana dashboards per service\n- Custom business metrics (orders/min, revenue/hour)\n- SLO dashboards with burn rate alerts\n\n14.2 Distributed Tracing\n- OpenTelemetry SDK in all services\n- Jaeger for trace visualization\n- 10% sampling rate in production\n- 100% sampling for error traces\n\n14.3 Logging\n- Structured JSON logging\n- Fluentd → Elasticsearch pipeline\n- Kibana for log analysis\n- 30-day retention in hot storage"),
        ("15. Disaster Recovery", "15.1 Recovery Objectives\n- RPO (Recovery Point Objective): 1 hour\n- RTO (Recovery Time Objective): 4 hours\n\n15.2 Backup Strategy\n- Database: WAL archiving to S3 every 5 minutes\n- Full snapshot: daily at 02:00 UTC\n- Cross-region replication to eu-west-1\n- Monthly disaster recovery drill\n\n15.3 Failover Procedures\n- Route 53 health checks with 30-second intervals\n- Automatic DNS failover to secondary region\n- Manual promotion of read replica to primary\n- Runbook stored in internal wiki"),
        ("16. Performance Requirements", "16.1 Latency Targets\n- API Gateway → Service: p50 < 10ms, p99 < 50ms\n- End-to-end (user): p50 < 100ms, p95 < 200ms, p99 < 500ms\n- Database queries: p95 < 20ms\n- Cache hit rate: > 95%\n\n16.2 Throughput Targets\n- API Gateway: 50,000 req/sec sustained\n- Order Processing: 12,000 orders/min peak\n- Event Bus: 100,000 events/sec\n- Search: 5,000 queries/sec\n\n16.3 Resource Limits\n- CPU per pod: 500m request, 2000m limit\n- Memory per pod: 512Mi request, 2Gi limit\n- Disk IOPS: 10,000 provisioned per RDS instance"),
        ("17. Security Compliance", "17.1 Access Control\n- RBAC with 5 predefined roles\n- Service mesh mTLS (Istio)\n- Network policies per namespace\n- VPC peering for cross-account access\n\n17.2 Data Classification\n- Public: marketing content, documentation\n- Internal: system metrics, non-PII logs\n- Confidential: user PII, financial data\n- Restricted: encryption keys, credentials\n\n17.3 Audit\n- CloudTrail for AWS API calls\n- Application audit log for user actions\n- Quarterly access review\n- Automated compliance scanning (Prowler)"),
        ("18. Testing Strategy", "18.1 Unit Testing\n- Coverage target: 80% line coverage\n- Go: standard testing package\n- Python: pytest with fixtures\n- JS: Jest with React Testing Library\n\n18.2 Integration Testing\n- Testcontainers for database/Kafka\n- Contract testing with Pact\n- API schema validation (OpenAPI)\n\n18.3 End-to-End Testing\n- Playwright for UI testing\n- 50 critical path scenarios\n- Nightly runs against staging\n- Visual regression with Percy\n\n18.4 Performance Testing\n- k6 for load testing\n- Weekly soak tests (4 hours)\n- Chaos engineering with Litmus"),
        ("19. Migration Plan", "19.1 Phase 1: Foundation (Weeks 1-4)\n- Deploy Kubernetes clusters\n- Set up CI/CD pipeline\n- Migrate Authentication Service\n- Establish monitoring baseline\n\n19.2 Phase 2: Core Services (Weeks 5-10)\n- Migrate Order Processing Service\n- Migrate Inventory Service\n- Set up Kafka event bus\n- Database migration with minimal downtime\n\n19.3 Phase 3: Complete Migration (Weeks 11-16)\n- Migrate remaining services\n- CDN and edge configuration\n- Performance validation\n- Decommission legacy infrastructure"),
        ("20. Appendix", "A. API Endpoint Reference\n- POST /api/v2/orders — Create new order\n- GET /api/v2/orders/{id} — Retrieve order details\n- PUT /api/v2/orders/{id}/status — Update order status\n- GET /api/v2/inventory?sku={sku} — Check stock level\n- POST /api/v2/auth/token — Generate access token\n- GET /api/v2/users/{id}/profile — Get user profile\n\nB. Environment Variables\n- DATABASE_URL — PostgreSQL connection string\n- REDIS_URL — Redis connection string\n- KAFKA_BROKERS — Kafka broker addresses\n- JWT_SECRET — Token signing key\n- STRIPE_API_KEY — Payment provider key\n\nC. Contact Information\n- Architecture Team: arch@cloudplatform.io\n- DevOps: devops@cloudplatform.io\n- Security: security@cloudplatform.io"),
    ]

    for i, (title, body) in enumerate(remaining_chapters):
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(60, 60), title, fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
        sh = page.new_shape()
        sh.draw_line(pymupdf.Point(60, 68), pymupdf.Point(W - 60, 68))
        sh.finish(color=(0.7, 0.7, 0.7), width=0.5)
        sh.commit()
        page.insert_textbox(pymupdf.Rect(60, 90, W - 60, H - 60), body, fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
        page.insert_text(pymupdf.Point(W/2 - 5, H - 30), str(11 + i), fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Set document metadata
    doc.set_metadata({
        "title": "CloudPlatform v3.2 System Design Document",
        "author": "Engineering Team",
        "subject": "System Architecture",
        "creator": "CloudPlatform Documentation System",
    })

    # Add table of contents bookmarks
    toc = [
        [1, "System Design Document", 1],
        [1, "Table of Contents", 2],
        [1, "1. Executive Summary", 3],
        [1, "2. System Overview", 4],
        [1, "3. Architecture Principles", 5],
        [1, "4. Frontend Architecture", 6],
        [1, "5. Backend Services", 7],
        [1, "6. Data Layer", 8],
        [1, "7. Authentication & Security", 9],
        [1, "8. Infrastructure", 10],
        [1, "10. System Component Diagram", 10],
        [1, "11. Integration Points", 11],
        [1, "12. Data Flow", 12],
        [1, "13. Deployment Strategy", 13],
        [1, "14. Monitoring & Observability", 14],
        [1, "15. Disaster Recovery", 15],
        [1, "16. Performance Requirements", 16],
        [1, "17. Security Compliance", 17],
        [1, "18. Testing Strategy", 18],
        [1, "19. Migration Plan", 19],
        [1, "20. Appendix", 20],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 20')

    # GUI-ready startup: open PDF at page 10 in Evince
    launch_gui(f'evince --page-index=10 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
