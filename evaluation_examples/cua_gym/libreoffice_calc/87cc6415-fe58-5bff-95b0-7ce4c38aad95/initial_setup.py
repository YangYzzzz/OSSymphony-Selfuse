"""
Initial Setup: Create reference_doc.odt for pdf_cross_022
Task ID: pdf_cross_022
Domain: pdf (cross-domain with LibreOffice Writer)

Creates a 15-page ODT document with 4 appendices and 8 body text references.
The document does NOT have hyperlinks/bookmarks yet - the agent must add those.
"""

import os
import shlex
import subprocess
import time
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_022'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT_ODT = f'{DOCS_DIR}/reference_doc.odt'


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

    mimetype = 'application/vnd.oasis.opendocument.text'

    manifest_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">\n'
        ' <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.text"/>\n'
        ' <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>\n'
        ' <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>\n'
        ' <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>\n'
        ' <manifest:file-entry manifest:full-path="settings.xml" manifest:media-type="text/xml"/>\n'
        '</manifest:manifest>'
    )

    meta_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"\n'
        '  xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
        '  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"\n'
        '  office:version="1.2">\n'
        ' <office:meta>\n'
        '  <dc:title>Technical Reference Manual</dc:title>\n'
        '  <dc:creator>Dr. Elena Vasquez</dc:creator>\n'
        '  <dc:subject>System Architecture Reference</dc:subject>\n'
        ' </office:meta>\n'
        '</office:document-meta>'
    )

    settings_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"\n'
        '  office:version="1.2">\n'
        ' <office:settings/>\n'
        '</office:document-settings>'
    )

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<office:document-styles\n'
        '  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"\n'
        '  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"\n'
        '  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"\n'
        '  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"\n'
        '  office:version="1.2">\n'
        ' <office:styles>\n'
        '  <style:style style:name="Standard" style:family="paragraph" style:class="text">\n'
        '   <style:text-properties fo:font-size="11pt"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_1" style:display-name="Heading 1" style:family="paragraph"\n'
        '    style:parent-style-name="Standard" style:class="text">\n'
        '   <style:paragraph-properties fo:margin-top="6mm" fo:margin-bottom="3mm"\n'
        '     fo:page-break-before="always"/>\n'
        '   <style:text-properties fo:font-size="18pt" fo:font-weight="bold" fo:color="#003366"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Heading_2" style:display-name="Heading 2" style:family="paragraph"\n'
        '    style:parent-style-name="Standard" style:class="text">\n'
        '   <style:paragraph-properties fo:margin-top="4mm" fo:margin-bottom="2mm"/>\n'
        '   <style:text-properties fo:font-size="14pt" fo:font-weight="bold" fo:color="#003366"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Body_Text" style:display-name="Body Text" style:family="paragraph"\n'
        '    style:parent-style-name="Standard">\n'
        '   <style:paragraph-properties fo:margin-bottom="3mm" fo:text-align="justify"\n'
        '     fo:line-height="150%"/>\n'
        '   <style:text-properties fo:font-size="11pt"/>\n'
        '  </style:style>\n'
        '  <style:style style:name="Appendix_Heading" style:display-name="Appendix Heading"\n'
        '    style:family="paragraph" style:parent-style-name="Heading_1">\n'
        '   <style:text-properties fo:font-size="20pt" fo:font-weight="bold" fo:color="#660000"/>\n'
        '  </style:style>\n'
        ' </office:styles>\n'
        ' <office:automatic-styles>\n'
        '  <style:page-layout style:name="PageLayout">\n'
        '   <style:page-layout-properties fo:page-width="210mm" fo:page-height="297mm"\n'
        '     fo:margin-top="25mm" fo:margin-bottom="25mm"\n'
        '     fo:margin-left="30mm" fo:margin-right="25mm"/>\n'
        '  </style:page-layout>\n'
        ' </office:automatic-styles>\n'
        ' <office:master-styles>\n'
        '  <style:master-page style:name="Standard" style:page-layout-name="PageLayout"/>\n'
        ' </office:master-styles>\n'
        '</office:document-styles>'
    )

    def esc(text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def para(text, style="Body_Text"):
        return '<text:p text:style-name="{}">{}</text:p>\n'.format(style, esc(text))

    def heading(text, level=1, style=None):
        if style is None:
            style = 'Heading_{}'.format(level)
        return '<text:p text:style-name="{}">{}</text:p>\n'.format(style, esc(text))

    body_parts = []

    # Page 1: Title / Cover
    body_parts.append(heading("Technical Reference Manual", 1))
    body_parts.append(para("Version 3.2 | March 2025"))
    body_parts.append(para("Prepared by: Dr. Elena Vasquez, Systems Architecture Division"))
    body_parts.append(para("Organization: NovaTech Engineering Group"))
    body_parts.append(para("Classification: Internal Use Only"))
    body_parts.append(para("This manual provides comprehensive reference material for system architects, senior developers, and infrastructure engineers working on the NovaTech Distributed Platform."))

    # Page 2: Table of Contents
    body_parts.append(heading("Table of Contents", 1))
    body_parts.append(para("1. Executive Overview ........ 3"))
    body_parts.append(para("2. System Architecture ........ 4"))
    body_parts.append(para("3. Core Components ........ 5"))
    body_parts.append(para("4. Data Flow Design ........ 6"))
    body_parts.append(para("5. Security Framework ........ 7"))
    body_parts.append(para("6. Performance Specifications ........ 8"))
    body_parts.append(para("7. Deployment Guidelines ........ 9"))
    body_parts.append(para("Appendix A: API Reference ........ 10"))
    body_parts.append(para("Appendix B: Configuration Templates ........ 12"))
    body_parts.append(para("Appendix C: Error Codes and Diagnostics ........ 13"))
    body_parts.append(para("Appendix D: Glossary of Terms ........ 14"))

    # Page 3: Chapter 1 - Executive Overview (references Appendix A)
    body_parts.append(heading("1. Executive Overview", 1))
    body_parts.append(para("The NovaTech Distributed Platform (NDP) represents the third generation of our enterprise infrastructure solution. This document serves as the authoritative technical reference for all platform components, integration points, and operational procedures."))
    body_parts.append(para("This revision incorporates feedback from Q4 2024 performance reviews and aligns with the updated ISO 27001:2022 compliance requirements. Engineers are advised to review Appendix A for the complete listing of updated API endpoints introduced in this version."))
    body_parts.append(para("The platform achieves 99.97% uptime through its distributed fault-tolerance architecture. Load balancing occurs automatically across all registered service nodes, with failover completing within 250 milliseconds under normal conditions."))
    body_parts.append(para("Key improvements in version 3.2 include enhanced container orchestration, native support for GraphQL subscriptions, and reduced cold-start latency from 850ms to under 200ms."))

    # Page 4: Chapter 2 - System Architecture (references Appendix B)
    body_parts.append(heading("2. System Architecture", 1))
    body_parts.append(para("The NovaTech Distributed Platform employs a microservices architecture organized into five logical tiers: Presentation, Gateway, Service Mesh, Data, and Infrastructure. Each tier maintains strict boundary contracts through versioned interfaces."))
    body_parts.append(para("Service discovery is handled by the embedded Consul cluster, which maintains real-time health checks for all registered services. A complete reference of service registration parameters is available in Appendix B under the configuration template section for service mesh components."))
    body_parts.append(para("Inter-service communication uses gRPC over mTLS for synchronous calls and Apache Kafka for event-driven messaging. The event schema registry enforces Avro schema compatibility across all message buses."))
    body_parts.append(para("The architecture diagram (Figure 2.1) illustrates the primary data pathways. All external-facing services route through the API Gateway layer, which handles authentication, rate limiting, and request transformation."))

    # Page 5: Chapter 3 - Core Components (references Appendix C, Appendix B)
    body_parts.append(heading("3. Core Components", 1))
    body_parts.append(heading("3.1 Authentication Service", 2))
    body_parts.append(para("The Authentication Service implements OAuth 2.0 with PKCE and supports SAML 2.0 federation for enterprise SSO integration. Token lifetimes and refresh policies are configurable per tenant. All token validation errors are documented in Appendix C with their corresponding diagnostic codes."))
    body_parts.append(heading("3.2 Data Access Layer", 2))
    body_parts.append(para("The Data Access Layer (DAL) abstracts all persistence operations behind a unified repository interface. Supported backends include PostgreSQL 15, MongoDB 6.0, Redis 7.2, and Apache Cassandra 4.1. Connection pool sizing guidelines are specified in Appendix B."))
    body_parts.append(heading("3.3 Notification Engine", 2))
    body_parts.append(para("Notifications are dispatched through a priority-based queue with three lanes: critical (SLA: 100ms), standard (SLA: 2s), and bulk (SLA: 30s). The engine supports email, SMS, push, and webhook delivery channels."))

    # Page 6: Chapter 4 - Data Flow Design (references Appendix A)
    body_parts.append(heading("4. Data Flow Design", 1))
    body_parts.append(para("Data ingestion follows the CQRS pattern with separate read and write models. Write operations are validated against JSON Schema definitions (see Appendix A for schema endpoint documentation) before being committed to the event log."))
    body_parts.append(para("The platform processes approximately 45,000 transactions per second at peak load. Each transaction traverses the following stages: ingestion, validation, transformation, routing, persistence, and acknowledgment."))
    body_parts.append(para("Idempotency keys are required for all write operations. The platform maintains an idempotency cache for 24 hours, preventing duplicate processing of retried requests."))
    body_parts.append(para("Read replicas are provisioned automatically based on query volume patterns. The read routing layer directs OLAP queries to dedicated analytical nodes separate from the OLTP primary cluster."))

    # Page 7: Chapter 5 - Security Framework (references Appendix D, Appendix C)
    body_parts.append(heading("5. Security Framework", 1))
    body_parts.append(para("All network traffic is encrypted using TLS 1.3. Certificate rotation occurs every 90 days through the automated PKI pipeline. Certificate serial numbers and revocation procedures are catalogued in Appendix D under PKI terminology definitions."))
    body_parts.append(para("The platform implements defense-in-depth across seven security layers: network perimeter, WAF, API gateway policies, service mesh policies, application controls, data encryption, and audit logging."))
    body_parts.append(para("Penetration testing is conducted quarterly. The most recent assessment (Q3 2024) identified three medium-severity findings, all of which have been remediated in this release. Details of the remediation procedures follow the guidelines outlined in Appendix C for security-related diagnostic events."))
    body_parts.append(para("Role-based access control (RBAC) is enforced at the API Gateway layer. Service accounts use short-lived tokens (15-minute TTL) that are automatically rotated by the secrets management system."))

    # Page 8: Chapter 6 - Performance Specifications (references Appendix B)
    body_parts.append(heading("6. Performance Specifications", 1))
    body_parts.append(para("Baseline performance benchmarks were measured on the reference hardware configuration: 32-core AMD EPYC 7543 processors, 256GB DDR4-3200 ECC RAM, NVMe SSD arrays with 3.2GB/s sustained throughput."))
    body_parts.append(para("The 99th percentile API response time target is 180ms for standard queries and 800ms for complex analytical queries. These targets are enforced through circuit breakers configured per the templates in Appendix B."))
    body_parts.append(para("Memory utilization at peak load averages 68% of allocated capacity, leaving a 32% buffer for burst handling. Garbage collection pauses are capped at 50ms through careful heap sizing and G1GC tuning."))
    body_parts.append(para("Horizontal scaling is triggered automatically when CPU utilization exceeds 75% for more than 3 consecutive minutes. Scale-in events are deferred for 10 minutes after a scale-out to prevent oscillation."))

    # Page 9: Chapter 7 - Deployment Guidelines (references Appendix C, Appendix B)
    body_parts.append(heading("7. Deployment Guidelines", 1))
    body_parts.append(para("Production deployments follow a blue-green strategy with automated canary analysis. New versions receive 5% of traffic initially, with gradual ramp-up based on error rate and latency SLO compliance."))
    body_parts.append(para("The deployment pipeline consists of six stages: build, unit test, integration test, staging deployment, smoke test, and production promotion. Average pipeline completion time is 23 minutes from commit to production."))
    body_parts.append(para("Container images are built from hardened base images that comply with CIS Docker Benchmark Level 2. All images are scanned for CVEs using Trivy before staging promotion. Critical CVEs block the pipeline automatically."))
    body_parts.append(para("Rollback procedures are fully automated. The system monitors key SLOs for 15 minutes post-deployment. If any SLO breaches the threshold, automatic rollback initiates within 30 seconds. Refer to Appendix C for the complete list of rollback trigger codes."))
    body_parts.append(para("Infrastructure as Code templates for all supported cloud providers (AWS, Azure, GCP, Alibaba Cloud) are provided in Appendix B. These templates implement the recommended multi-region active-active configuration."))

    # Page 10: Appendix A - API Reference
    body_parts.append(heading("Appendix A: API Reference", 1, "Appendix_Heading"))
    body_parts.append(para("This appendix provides a complete reference for all public API endpoints exposed by the NovaTech Distributed Platform version 3.2. Endpoints are organized by service domain."))
    body_parts.append(heading("A.1 Authentication Endpoints", 2))
    body_parts.append(para("POST /api/v3/auth/token - Obtain access token using client credentials or authorization code grant. Required parameters: grant_type, client_id, client_secret or code. Returns: access_token (JWT), refresh_token, expires_in, scope."))
    body_parts.append(para("POST /api/v3/auth/refresh - Refresh an expired access token using a valid refresh token. Required: refresh_token, client_id. Returns: new access_token, new refresh_token."))
    body_parts.append(para("DELETE /api/v3/auth/token - Revoke an access or refresh token. Required: token, token_type_hint."))
    body_parts.append(heading("A.2 Resource Management Endpoints", 2))
    body_parts.append(para("GET /api/v3/resources - List all resources accessible to the authenticated service account. Supports pagination via cursor parameter."))
    body_parts.append(para("POST /api/v3/resources - Create a new resource. Request body must conform to the ResourceSpec schema."))
    body_parts.append(para("GET /api/v3/resources/{id} - Retrieve a specific resource by identifier. Returns full resource representation including audit trail."))
    body_parts.append(para("PATCH /api/v3/resources/{id} - Update specific fields via JSON Patch format (RFC 6902)."))
    body_parts.append(para("DELETE /api/v3/resources/{id} - Soft-delete a resource. Resource remains retrievable for 30 days before permanent deletion."))

    # Page 11: Appendix A continued
    body_parts.append(heading("A.3 Event Stream Endpoints", 2))
    body_parts.append(para("GET /api/v3/events/stream - Subscribe to real-time event stream using Server-Sent Events. Parameters: filter, since, limit."))
    body_parts.append(para("GET /api/v3/events/{correlationId} - Retrieve all events associated with a correlation ID. Useful for distributed tracing and audit purposes."))
    body_parts.append(heading("A.4 Health and Metrics Endpoints", 2))
    body_parts.append(para("GET /api/v3/health - System health check. Returns aggregate health status and component-level details. Does not require authentication."))
    body_parts.append(para("GET /api/v3/health/ready - Readiness probe for Kubernetes deployments. Returns HTTP 200 when all dependencies are available."))
    body_parts.append(para("GET /api/v3/metrics - Prometheus-compatible metrics endpoint. Exposes over 200 application and infrastructure metrics."))
    body_parts.append(para("All API calls must include the X-Request-ID header for distributed tracing."))

    # Page 12: Appendix B - Configuration Templates
    body_parts.append(heading("Appendix B: Configuration Templates", 1, "Appendix_Heading"))
    body_parts.append(para("This appendix provides standardized configuration templates for all major platform components. Templates are provided in YAML format and are compatible with the NDP Configuration Management System (CMS) v2.4 and later."))
    body_parts.append(heading("B.1 Service Mesh Configuration", 2))
    body_parts.append(para("service_mesh: name: service_name, version: version, replicas: min: 2, max: 20, target_cpu_utilization: 75, circuit_breaker: failure_threshold: 5, recovery_timeout_ms: 30000, half_open_max_calls: 3, timeouts: connect_ms: 500, read_ms: 5000, write_ms: 5000, retry: max_attempts: 3, initial_backoff_ms: 100, max_backoff_ms: 10000"))
    body_parts.append(heading("B.2 Database Connection Pool", 2))
    body_parts.append(para("database: primary: host: db_host, port: 5432, database: db_name, pool_size: 20, max_overflow: 10, pool_timeout_sec: 30, pool_recycle_sec: 3600, read_replicas: host: replica1_host weight: 50, host: replica2_host weight: 50"))

    # Page 13: Appendix C - Error Codes
    body_parts.append(heading("Appendix C: Error Codes and Diagnostics", 1, "Appendix_Heading"))
    body_parts.append(para("This appendix catalogues all error codes, warning codes, and diagnostic events generated by the NovaTech Distributed Platform. Codes are organized by service category."))
    body_parts.append(heading("C.1 Authentication Error Codes", 2))
    body_parts.append(para("AUTH-001: Invalid client credentials. Verify client_id and client_secret."))
    body_parts.append(para("AUTH-002: Token expired. The access token has exceeded its configured TTL. Obtain a new token using the refresh grant."))
    body_parts.append(para("AUTH-003: Insufficient scope. Re-authenticate requesting the additional scope."))
    body_parts.append(para("AUTH-004: Token revoked. The token has been explicitly revoked due to security policy enforcement."))
    body_parts.append(para("AUTH-005: MFA challenge required. Direct the user to the MFA challenge endpoint."))
    body_parts.append(heading("C.2 Service Error Codes", 2))
    body_parts.append(para("SVC-001: Resource not found. SVC-002: Resource already exists (duplicate idempotency key). SVC-003: Validation failed. SVC-004: Rate limit exceeded - Retry-After header indicates wait time."))
    body_parts.append(para("SVC-100: Circuit opened due to failure threshold breach. SVC-101: Circuit in half-open state. SVC-102: Circuit closed - service restored."))
    body_parts.append(heading("C.3 Rollback Trigger Codes", 2))
    body_parts.append(para("DEPLOY-001: Error rate SLO breach (threshold: over 1% 5xx errors over 5-minute window). DEPLOY-002: Latency P99 SLO breach. DEPLOY-003: Memory utilization critical. DEPLOY-004: Health check consecutive failures."))

    # Page 14: Appendix D - Glossary
    body_parts.append(heading("Appendix D: Glossary of Terms", 1, "Appendix_Heading"))
    body_parts.append(para("This appendix defines technical terms and acronyms used throughout this reference manual."))
    body_parts.append(heading("D.1 Architecture Terms", 2))
    body_parts.append(para("CQRS (Command Query Responsibility Segregation): An architectural pattern that separates read operations from write operations into distinct models. The NDP uses CQRS to optimize throughput and scalability."))
    body_parts.append(para("Circuit Breaker: A resilience pattern that monitors service calls and automatically stops forwarding requests when failure rates exceed a threshold."))
    body_parts.append(para("Event Sourcing: A persistence approach where application state is derived from an append-only log of domain events. Enables full audit trails and temporal queries."))
    body_parts.append(para("Service Mesh: An infrastructure layer that manages service-to-service communication, providing mutual TLS, load balancing, observability, and traffic management."))
    body_parts.append(heading("D.2 Security Terms", 2))
    body_parts.append(para("mTLS (Mutual Transport Layer Security): A variant of TLS in which both the client and server authenticate each other using certificates. Used throughout the NDP service mesh."))
    body_parts.append(para("PKCE (Proof Key for Code Exchange): A security extension to OAuth 2.0 that prevents authorization code interception attacks. Mandatory for all public clients."))
    body_parts.append(para("PKI (Public Key Infrastructure): The set of roles, policies, hardware, software, and procedures needed to manage digital certificates. The NDP operates an internal PKI."))
    body_parts.append(para("Zero Trust: A security model that requires strict identity verification for every user and device attempting to access resources, regardless of network location."))

    # Page 15: References / Index
    body_parts.append(heading("References and Further Reading", 1))
    body_parts.append(para("The following standards, frameworks, and publications informed the design of the NovaTech Distributed Platform version 3.2."))
    body_parts.append(para("ISO/IEC 27001:2022 - Information security, cybersecurity and privacy protection."))
    body_parts.append(para("NIST SP 800-204C - Implementation of DevSecOps for a Microservices-based Application with Service Mesh."))
    body_parts.append(para("CNCF Microservices Patterns - Cloud Native Computing Foundation reference architecture."))
    body_parts.append(para("RFC 6902 - JavaScript Object Notation (JSON) Patch specification."))
    body_parts.append(para("RFC 7636 - Proof Key for Code Exchange by OAuth Public Clients."))
    body_parts.append(para("Google SRE Handbook - Site Reliability Engineering: How Google Runs Production Systems."))
    body_parts.append(para("Sam Newman - Building Microservices, 2nd Edition. O'Reilly Media, 2021."))
    body_parts.append(para("Chris Richardson - Microservices Patterns. Manning Publications, 2018."))
    body_parts.append(para("Martin Fowler - Patterns of Enterprise Application Architecture. Addison-Wesley Professional, 2002."))

    content = ''.join(body_parts)

    content_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<office:document-content\n'
        '  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"\n'
        '  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"\n'
        '  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"\n'
        '  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"\n'
        '  office:version="1.2">\n'
        ' <office:automatic-styles/>\n'
        ' <office:body>\n'
        '  <office:text>\n'
        + content +
        '  </office:text>\n'
        ' </office:body>\n'
        '</office:document-content>'
    )

    # Write ODT zip
    with zipfile.ZipFile(OUTPUT_ODT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/manifest.xml', manifest_xml)
        z.writestr('meta.xml', meta_xml)
        z.writestr('settings.xml', settings_xml)
        z.writestr('styles.xml', styles_xml)
        z.writestr('content.xml', content_xml)

    print(f"Initial file created: {OUTPUT_ODT}")
    print(f"File size: {os.path.getsize(OUTPUT_ODT)} bytes")

    # GUI-ready startup: open the ODT in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT_ODT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with reference_doc.odt on DISPLAY=:0')


create_initial()
