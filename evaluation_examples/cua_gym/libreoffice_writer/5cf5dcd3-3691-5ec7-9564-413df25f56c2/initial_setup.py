"""
Initial Setup: Create a 50-page Complete_Manual.odt with 6 chapters
Task ID: writer_rm_060
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
OUTPUT = f'{WORKDIR}/Complete_Manual.odt'


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
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H, Span
    from odf.style import Style, TextProperties, ParagraphProperties, PageLayoutProperties, MasterPage, PageLayout

    doc = OpenDocumentText()

    # --- Define styles ---
    # Page layout for A4
    pl = PageLayout(name="PageLayout1")
    pl.addElement(PageLayoutProperties(
        pagewidth="21.001cm", pageheight="29.7cm",
        marginleft="2cm", marginright="2cm",
        margintop="2cm", marginbottom="2cm"
    ))
    doc.automaticstyles.addElement(pl)

    mp = MasterPage(name="Standard", pagelayoutname="PageLayout1")
    doc.masterstyles.addElement(mp)

    # Body text style
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(TextProperties(fontsize="12pt", fontfamily="Liberation Serif"))
    body_style.addElement(ParagraphProperties(marginbottom="0.3cm", margintop="0.1cm"))
    doc.styles.addElement(body_style)

    # Heading 1 style
    h1_style = Style(name="Heading1", family="paragraph")
    h1_style.addElement(TextProperties(fontsize="24pt", fontweight="bold", fontfamily="Liberation Sans"))
    h1_style.addElement(ParagraphProperties(margintop="1cm", marginbottom="0.5cm", breakbefore="page"))
    doc.styles.addElement(h1_style)

    # Heading 2 style
    h2_style = Style(name="Heading2", family="paragraph")
    h2_style.addElement(TextProperties(fontsize="18pt", fontweight="bold", fontfamily="Liberation Sans"))
    h2_style.addElement(ParagraphProperties(margintop="0.7cm", marginbottom="0.3cm"))
    doc.styles.addElement(h2_style)

    # Heading 3 style
    h3_style = Style(name="Heading3", family="paragraph")
    h3_style.addElement(TextProperties(fontsize="14pt", fontweight="bold", fontfamily="Liberation Sans"))
    h3_style.addElement(ParagraphProperties(margintop="0.5cm", marginbottom="0.2cm"))
    doc.styles.addElement(h3_style)

    # Bold span style
    bold_style = Style(name="BoldText", family="text")
    bold_style.addElement(TextProperties(fontweight="bold"))
    doc.styles.addElement(bold_style)

    # Italic span style
    italic_style = Style(name="ItalicText", family="text")
    italic_style.addElement(TextProperties(fontstyle="italic"))
    doc.styles.addElement(italic_style)

    # --- Chapter content definitions ---
    chapters = {
        "Getting Started": {
            "sections": {
                "Welcome to the Platform": [
                    "Welcome to our comprehensive software platform. This manual provides detailed instructions for all aspects of the system, from initial setup through advanced configuration and troubleshooting. The platform has been designed with enterprise-grade reliability and scalability in mind, serving organizations of all sizes across multiple industries.",
                    "Our platform integrates seamlessly with existing enterprise infrastructure, supporting single sign-on through SAML 2.0 and OAuth 2.0 protocols. The architecture follows a microservices pattern, allowing independent scaling of components based on workload demands. Each service communicates through well-defined APIs, ensuring loose coupling and high maintainability.",
                    "The development team has invested significant effort in creating an intuitive user experience while maintaining the powerful capabilities required by advanced users. Whether you are a system administrator deploying the platform for the first time, a developer integrating with our APIs, or an end user performing daily tasks, this manual contains the information you need.",
                ],
                "System Requirements": [
                    "Before beginning the installation process, ensure your environment meets the following minimum requirements. For production deployments, we strongly recommend exceeding these specifications to allow for growth and peak usage periods. Hardware requirements: Intel Xeon E5-2600 v4 or AMD EPYC 7001 series processor with at least 8 cores, 32 GB of ECC RAM (64 GB recommended for production), 500 GB SSD storage with at least 100 MB/s sustained write speed.",
                    "Operating system support includes Ubuntu 20.04 LTS or later, Red Hat Enterprise Linux 8.x or later, CentOS Stream 8 or later, and Windows Server 2019 or later. For containerized deployments, Docker 20.10+ with Docker Compose 2.0+ is required. Kubernetes 1.24+ is supported for orchestrated deployments with Helm 3.x charts provided in the distribution package.",
                    "Network requirements include a minimum of 1 Gbps Ethernet connectivity between cluster nodes, with 10 Gbps recommended for high-throughput workloads. Firewall rules must allow TCP traffic on ports 443 (HTTPS), 8080 (internal API), 5432 (PostgreSQL), and 6379 (Redis). DNS resolution must be configured for all hostnames used by the platform components.",
                    "Database requirements specify PostgreSQL 14.x or later as the primary data store. The database server should have dedicated resources separate from the application servers. For high availability, we recommend configuring streaming replication with automatic failover using Patroni or a similar orchestration tool. Minimum disk allocation for the database is 200 GB, with provisioned IOPS of at least 3000.",
                ],
                "Quick Start Guide": [
                    "For users who want to get up and running quickly, this section provides a streamlined setup process. Download the latest release package from our distribution portal at https://releases.example.com/platform/latest. Extract the archive to your preferred installation directory. The package includes all necessary dependencies and a bootstrap script.",
                    "Run the bootstrap script with administrator privileges: sudo ./bootstrap.sh --mode=quickstart. This will configure a single-node deployment with default settings suitable for evaluation and development purposes. The script automatically detects your operating system, installs required system packages, initializes the database, and starts all services.",
                    "Once the bootstrap completes (typically 5-10 minutes), access the web interface at https://localhost:8443. The default administrator credentials are admin/changeme. You will be prompted to change the password on first login. Navigate to Settings > System to verify all services are running correctly.",
                    "The quick start deployment uses SQLite for simplicity. For production use, you must migrate to PostgreSQL following the instructions in Chapter 3: Configuration. The migration tool preserves all data and settings. We strongly recommend completing this migration before adding users or production data to the system.",
                ],
                "Understanding the Architecture": [
                    "The platform follows a layered architecture pattern with clear separation of concerns. The presentation layer handles all user interface rendering and input validation. Built with React 18 and TypeScript, it communicates with the backend exclusively through RESTful APIs and WebSocket connections for real-time updates.",
                    "The application layer implements business logic through a collection of microservices, each responsible for a specific domain. Key services include the Authentication Service (handles user identity and access control), the Data Processing Service (manages ETL pipelines and data transformations), the Notification Service (delivers alerts via email, SMS, and push notifications), and the Analytics Service (generates reports and dashboards).",
                    "The data layer uses PostgreSQL as the primary relational store, Redis for caching and session management, and Elasticsearch for full-text search capabilities. All data at rest is encrypted using AES-256, and all inter-service communication uses mTLS certificates managed by an internal certificate authority.",
                    "A message broker (RabbitMQ) facilitates asynchronous communication between services. Events published to topic exchanges allow services to react to state changes without direct coupling. This pattern enables the system to handle burst workloads gracefully by queuing messages during peak periods and processing them as capacity becomes available.",
                ],
            }
        },
        "Installation": {
            "sections": {
                "Pre-Installation Checklist": [
                    "Before proceeding with installation, complete the following checklist to avoid common issues. Verify that all system requirements from Chapter 1 are met. Ensure you have root or sudo access to all target machines. Confirm network connectivity between all nodes that will form the cluster, including the ability to resolve hostnames.",
                    "Back up any existing configurations if you are upgrading from a previous version. The installation process will preserve data but may overwrite configuration files. Export your current settings using the backup utility: ./platform-cli backup --output=/backup/pre-upgrade-$(date +%Y%m%d).tar.gz. This creates a compressed archive of all configuration files, database schemas, and user data.",
                    "Verify that required ports are available and not in use by other applications. Use the provided port scanner: ./tools/check-ports.sh. This script tests all required ports and reports conflicts. If conflicts are found, either stop the conflicting services or configure alternative ports in the platform configuration file before proceeding.",
                    "Prepare SSL/TLS certificates for production deployments. The platform requires a valid certificate for the web interface and optionally for internal service communication. You can use certificates from a commercial CA, Let's Encrypt, or generate self-signed certificates for testing. The certificate must include the platform's fully qualified domain name as the subject or a subject alternative name.",
                ],
                "Standard Installation": [
                    "The standard installation process uses our custom installer that handles dependency resolution, configuration, and service setup. Download the installer package appropriate for your operating system from the release portal. Verify the checksum: sha256sum platform-installer-3.2.1-linux-amd64.tar.gz and compare with the published hash.",
                    "Extract and run the installer: tar xzf platform-installer-*.tar.gz && cd platform-installer && sudo ./install.sh. The installer presents a text-based interface for configuration. Accept the license agreement, select the installation type (single-node or cluster), and specify the installation directory (default: /opt/platform).",
                    "For single-node installations, the installer configures all services on the local machine. Specify the database connection parameters when prompted. If PostgreSQL is not already installed, the installer can provision a local instance automatically. Choose strong passwords for the database user and the platform administrator account.",
                    "The installation typically completes in 15-30 minutes depending on hardware and network speed. Upon completion, the installer displays a summary of configured services, their ports, and initial credentials. A detailed log is written to /var/log/platform/install.log for troubleshooting if needed.",
                    "Post-installation verification: Run sudo ./platform-cli health-check to verify all components are functioning correctly. The health check tests database connectivity, service responsiveness, disk space, and memory availability. Address any warnings before putting the system into production.",
                ],
                "Cluster Installation": [
                    "For high-availability deployments, install the platform across multiple nodes. Designate one node as the primary and others as workers. The primary node runs the management services, scheduler, and database (or connects to an external database). Worker nodes run application services and can be added or removed dynamically.",
                    "On the primary node, run the installer with cluster mode: sudo ./install.sh --mode=cluster --role=primary --cluster-name=prod-cluster. The installer generates a cluster join token that worker nodes use to authenticate. The token expires after 24 hours for security; generate a new one with ./platform-cli cluster generate-token if needed.",
                    "On each worker node, run: sudo ./install.sh --mode=cluster --role=worker --primary-host=primary.example.com --token=<join-token>. The worker automatically downloads its configuration from the primary and starts the assigned services. The primary's load balancer automatically detects new workers and begins routing traffic to them.",
                    "Configure shared storage for clusters using NFS, GlusterFS, or a cloud block storage service. All nodes must mount the shared volume at /opt/platform/shared. This volume stores uploaded files, temporary processing data, and shared configuration. Ensure the mount is included in /etc/fstab for persistence across reboots.",
                    "Verify cluster status with: ./platform-cli cluster status. This displays all nodes, their roles, health status, and resource utilization. Nodes marked as 'degraded' should be investigated immediately. Common causes include network partitions, disk space exhaustion, and service crashes.",
                ],
                "Docker Deployment": [
                    "For containerized deployments, use the provided Docker Compose files. The distribution includes configurations for development (docker-compose.dev.yml), staging (docker-compose.staging.yml), and production (docker-compose.prod.yml) environments. Each file is pre-configured with appropriate resource limits and restart policies.",
                    "Prerequisites: Docker 20.10+ and Docker Compose 2.0+. Pull the images: docker compose pull. Start the stack: docker compose -f docker-compose.prod.yml up -d. The first startup takes several minutes as the database is initialized and migrations are applied. Monitor progress with: docker compose logs -f.",
                    "Persistent data is stored in Docker volumes. The production compose file defines volumes for database data, uploaded files, and log storage. Back up these volumes regularly using your preferred backup strategy. We provide a helper script: ./tools/docker-backup.sh that creates consistent snapshots of all volumes.",
                    "For Kubernetes deployments, Helm charts are provided in the helm/ directory. Install with: helm install platform ./helm/platform -f values-production.yaml -n platform --create-namespace. The chart supports horizontal pod autoscaling, pod disruption budgets, and rolling updates with zero downtime.",
                ],
            }
        },
        "Configuration": {
            "sections": {
                "Configuration File Reference": [
                    "The platform uses a hierarchical configuration system with multiple sources. Configuration is loaded in the following priority order (highest to lowest): environment variables, command-line arguments, local configuration file (/etc/platform/config.yml), default values. Each level overrides the one below it, allowing flexible deployment configurations.",
                    "The main configuration file uses YAML format with sections for each service. A complete reference is available at /opt/platform/docs/config-reference.yml. Key sections include: server (HTTP settings, TLS, timeouts), database (connection pool, replication, backup schedule), auth (providers, token lifetime, password policy), and services (per-service configuration).",
                    "Environment variables follow the pattern PLATFORM_SECTION_KEY. For example, PLATFORM_DATABASE_HOST=db.example.com overrides the database.host setting. Array values use comma separation: PLATFORM_AUTH_ALLOWED_DOMAINS=example.com,example.org. Boolean values accept true/false, yes/no, or 1/0.",
                    "Configuration changes require a service restart unless hot-reload is enabled. Enable hot-reload by setting server.hot_reload: true in the configuration file. When enabled, the platform watches the configuration file for changes and applies non-critical settings without downtime. Changes to database connections, TLS certificates, and authentication providers still require a restart.",
                ],
                "Database Configuration": [
                    "PostgreSQL configuration is critical for platform performance. The default connection pool size is 20 connections per service instance. For high-traffic deployments, increase this to 50-100. Set database.pool_size in the configuration file or use PLATFORM_DATABASE_POOL_SIZE environment variable.",
                    "Connection string format: postgresql://user:password@host:port/dbname?sslmode=require. Always use SSL for production database connections. The platform supports connection through PgBouncer for connection pooling at the database level, which is recommended for deployments with more than 5 application nodes.",
                    "Backup configuration: The platform includes an automated backup scheduler. Configure in the database.backup section: schedule (cron format, default: '0 2 * * *' for 2 AM daily), retention_days (default: 30), destination (local path or S3-compatible storage), and compression (gzip or zstd, default: zstd for better compression ratio).",
                    "For read-heavy workloads, configure read replicas in the database.replicas section. Specify multiple replica hosts, and the platform will distribute read queries across them using round-robin or least-connections algorithms. Write operations always go to the primary. The replica_lag_threshold setting (default: 5 seconds) determines when a replica is considered too far behind and excluded from the rotation.",
                    "Database maintenance: Schedule regular VACUUM ANALYZE operations using the built-in maintenance scheduler or an external tool like pg_cron. The platform monitors table bloat and query performance, alerting administrators when maintenance is overdue. Index usage statistics are available in the admin dashboard under Database > Performance.",
                ],
                "Authentication Setup": [
                    "The platform supports multiple authentication methods that can be used simultaneously. Local authentication uses bcrypt-hashed passwords stored in the platform database. Password policy is configurable: minimum length (default: 12), complexity requirements (uppercase, lowercase, digit, special character), and maximum age (default: 90 days).",
                    "LDAP/Active Directory integration: Configure the auth.ldap section with your directory server details. Required settings include server URL (ldaps://ad.example.com:636), base DN (dc=example,dc=com), bind DN and password for service account, and user search filter (default: (sAMAccountName={username})). Group mapping allows automatic role assignment based on directory group membership.",
                    "SAML 2.0 SSO: Upload your Identity Provider's metadata XML to /etc/platform/saml/idp-metadata.xml. Configure the auth.saml section with entity_id, assertion_consumer_service_url, and optionally single_logout_service_url. The platform's SP metadata is available at https://platform.example.com/auth/saml/metadata for registration with your IdP.",
                    "OAuth 2.0 / OpenID Connect: Configure external providers in the auth.oauth section. Pre-built configurations are available for Google Workspace, Microsoft Entra ID, Okta, and Auth0. Custom OIDC providers can be configured by specifying the discovery URL (/.well-known/openid-configuration). Token validation supports RS256, RS384, and RS512 algorithms.",
                    "Multi-factor authentication (MFA): Enable in auth.mfa section. Supported methods include TOTP (Google Authenticator, Authy), WebAuthn/FIDO2 (hardware keys like YubiKey), and SMS (requires Twilio integration). MFA can be enforced globally or per-role. Recovery codes are generated automatically and should be stored securely by users.",
                ],
                "Network and Security": [
                    "TLS configuration: The platform uses TLS 1.2 or 1.3 for all external communications. Configure certificate and key paths in server.tls section. Supported cipher suites are restricted to AEAD ciphers (AES-GCM, ChaCha20-Poly1305) for security. HSTS headers are enabled by default with a max-age of 31536000 seconds (1 year).",
                    "Rate limiting: Configurable per endpoint in the server.rate_limit section. Default limits: 100 requests per minute for API endpoints, 10 login attempts per minute per IP, 1000 webhook deliveries per hour. Limits can be customized per API key or user role. Rate limit headers (X-RateLimit-*) are included in responses.",
                    "CORS configuration: Specify allowed origins in server.cors.allowed_origins. Use specific origins rather than wildcards in production. Allowed methods, headers, and credentials settings are configurable. Pre-flight request caching is set to 3600 seconds by default.",
                    "IP allowlisting: Restrict access to the admin interface and API by IP address or CIDR range. Configure in server.ip_allowlist. This is strongly recommended for production deployments. The allowlist supports IPv4 and IPv6 addresses. Changes to the allowlist take effect immediately without restart.",
                    "Audit logging: All authentication events, configuration changes, and data access are logged to the audit trail. Configure retention and export settings in logging.audit section. Logs can be exported to SIEM systems (Splunk, ELK, Datadog) via syslog or webhook. The audit trail is tamper-evident using cryptographic chaining.",
                ],
            }
        },
        "Usage": {
            "sections": {
                "Dashboard Overview": [
                    "The main dashboard provides a real-time overview of system status, recent activity, and key metrics. The top bar displays system health indicators: a green circle indicates all services are operational, yellow indicates degraded performance, and red indicates a critical issue requiring immediate attention. Click on the indicator for detailed service status.",
                    "The activity feed on the left panel shows recent user actions, system events, and scheduled task completions. Filter by event type, user, or time range using the controls at the top of the feed. Each entry links to the relevant detail page. The feed updates in real-time via WebSocket connection.",
                    "Customizable widgets allow you to arrange the dashboard to show the information most relevant to your role. Available widgets include: Resource Usage (CPU, memory, disk), Active Users, Task Queue Status, Error Rate Graph, Top Queries, and System Alerts. Drag and drop widgets to rearrange, and use the gear icon to configure each widget's settings.",
                    "Keyboard shortcuts accelerate navigation: Ctrl+K opens the command palette for quick access to any page or action, Ctrl+/ toggles the sidebar, and Ctrl+Shift+F opens global search. A complete list of shortcuts is available under Help > Keyboard Shortcuts or by pressing the ? key anywhere in the application.",
                ],
                "Data Management": [
                    "The Data Management module provides tools for importing, transforming, and exporting data. Supported import formats include CSV, JSON, XML, Parquet, and Excel (xlsx). The import wizard guides you through column mapping, data type detection, and validation rules. Large imports (over 1 million rows) are processed asynchronously with progress tracking.",
                    "Data pipelines allow you to create automated workflows for data processing. The visual pipeline editor supports drag-and-drop configuration of steps including: Filter (select rows matching conditions), Transform (apply functions to columns), Aggregate (group and summarize), Join (combine datasets), and Output (write results to tables or files).",
                    "Version control for datasets tracks all changes with full history. Each modification creates a new version with metadata including the user, timestamp, and change description. Roll back to any previous version with a single click. Branching and merging of datasets is supported for collaborative data preparation workflows.",
                    "Data quality rules can be defined per column or per table. Rules include: not null, unique, range checks, regex patterns, referential integrity, and custom SQL expressions. Quality scores are calculated continuously and displayed on the data catalog. Alerts trigger when quality drops below configurable thresholds.",
                    "Export functionality supports the same formats as import, plus additional options for database direct load and API streaming. Schedule regular exports using cron expressions. Exports can be filtered, sorted, and limited. For large exports, the system generates download links valid for 24 hours.",
                ],
                "User Management": [
                    "Administrators manage users through the Admin > Users page. Create individual users or bulk import from CSV. Required fields are username, email, and role. Optional fields include department, phone, and custom attributes. New users receive a welcome email with a secure link to set their password.",
                    "Role-based access control (RBAC) uses a hierarchical model with four default roles: Viewer (read-only access), Editor (read and write data), Manager (team management, report generation), and Administrator (full system access). Custom roles can be created by combining fine-grained permissions. Roles are assigned per workspace, allowing different access levels in different contexts.",
                    "Teams group users for collaborative work. Team members share workspaces, dashboards, and pipelines. Team leads can manage membership and assign roles within their team. Inter-team sharing is controlled by workspace visibility settings: Private (team only), Internal (all authenticated users), or Public (accessible without authentication, read-only).",
                    "User activity monitoring is available under Admin > Activity. View login history, action audit trail, and resource usage per user. Inactive accounts are flagged after configurable periods (default: 90 days). Administrators can disable or delete accounts, with options to transfer owned resources to another user.",
                ],
                "Reporting and Analytics": [
                    "The reporting engine supports both ad-hoc queries and scheduled reports. Create reports using the visual query builder or write SQL directly. The query builder supports joins across multiple tables, aggregations, window functions, and subqueries. Query results can be visualized as tables, charts (line, bar, pie, scatter, heatmap), or exported.",
                    "Scheduled reports run automatically and deliver results via email, Slack, or webhook. Configure the schedule using cron expressions or preset intervals (hourly, daily, weekly, monthly). Reports include the current data snapshot and optionally comparison with previous periods. PDF and Excel attachments are generated automatically.",
                    "Dashboard sharing allows you to publish interactive dashboards for stakeholders. Shared dashboards support parameter filters, allowing viewers to slice data by date range, department, product, or other dimensions. Embedding dashboards in external applications is supported via iframe with authentication tokens.",
                    "The analytics engine calculates derived metrics automatically. Define custom metrics using formulas that reference raw data columns. Metrics support time-series analysis including moving averages, year-over-year growth, and trend detection. Anomaly detection highlights unusual patterns in metrics using statistical methods (z-score, IQR, isolation forest).",
                ],
            }
        },
        "Troubleshooting": {
            "sections": {
                "Common Issues and Solutions": [
                    "Issue: Platform fails to start after installation. Solution: Check the installation log at /var/log/platform/install.log for errors. Common causes include insufficient permissions on the installation directory, port conflicts with existing services, and missing system dependencies. Run ./platform-cli doctor to diagnose system issues automatically.",
                    "Issue: Database connection errors. Solution: Verify PostgreSQL is running and accessible from the platform host. Test connectivity: psql -h db.example.com -U platform -d platformdb. Check that the database user has the required privileges: CREATE, SELECT, INSERT, UPDATE, DELETE on all platform tables. Verify SSL certificate validity if using encrypted connections.",
                    "Issue: High memory usage. Solution: The platform caches frequently accessed data in memory. Default cache size is 2 GB, configurable in server.cache_size. For systems with limited memory, reduce to 512 MB. Monitor memory usage in the admin dashboard or with: ./platform-cli metrics memory. Consider increasing swap space as a safety net.",
                    "Issue: Slow query performance. Solution: Enable query logging with database.log_slow_queries: true and database.slow_query_threshold: 1000 (milliseconds). Review logged queries in Admin > Database > Slow Queries. Common optimizations include adding indexes (the platform suggests indexes based on query patterns), increasing the connection pool, and optimizing complex queries.",
                    "Issue: Authentication failures after IdP change. Solution: Update the IdP metadata in /etc/platform/saml/idp-metadata.xml. Clear the auth cache: ./platform-cli cache clear --scope=auth. Restart the authentication service: ./platform-cli service restart auth. Verify SAML assertions using the debug endpoint: https://platform.example.com/auth/saml/debug.",
                ],
                "Log Analysis": [
                    "Platform logs are stored in /var/log/platform/ with separate files per service. Log levels are configurable per service in the logging section of the configuration file. Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. Production systems should use INFO or WARNING to avoid excessive disk usage.",
                    "Structured logging in JSON format is available for integration with log aggregation systems. Enable with logging.format: json. Each log entry includes: timestamp, service name, log level, message, correlation ID (for request tracing), and optional context fields. The correlation ID allows tracing a request across all services it touches.",
                    "Log rotation is handled automatically by the platform. Default settings: 100 MB per file, 10 files retained, gzip compression for rotated files. Customize in the logging.rotation section. For containerized deployments, logs are written to stdout/stderr and should be captured by the container runtime's logging driver.",
                    "Real-time log viewing is available through the admin interface under System > Logs. Filter by service, level, time range, and search text. The viewer highlights errors in red and warnings in yellow. Click on any entry to see the full context including stack traces and related log entries from other services.",
                    "Audit logs are stored separately in /var/log/platform/audit/ with extended retention (default: 1 year). These logs are append-only and protected against modification. Each entry is cryptographically signed using the platform's internal certificate. Verify audit log integrity with: ./platform-cli audit verify.",
                ],
                "Performance Tuning": [
                    "Connection pool tuning: Monitor active and idle connections in Admin > Database > Connections. If active connections frequently reach the pool maximum, increase database.pool_size. If idle connections are consistently high, decrease database.pool_max_idle. For high-concurrency scenarios, consider using PgBouncer in transaction mode.",
                    "Query optimization: The platform includes a query analyzer that provides execution plans and optimization suggestions. Access it in Admin > Database > Query Analyzer. Paste any slow query to see the execution plan, estimated vs. actual row counts, and recommended indexes. The analyzer also identifies common anti-patterns like N+1 queries.",
                    "Caching strategy: The platform uses a multi-layer cache: L1 (in-process, per-instance) and L2 (Redis, shared). Configure L1 size with server.cache_l1_size (default: 256 MB per instance). L2 uses the configured Redis instance. Cache hit rates are displayed in the admin dashboard. Aim for L1 hit rate above 80% and L2 above 95%.",
                    "Resource allocation for worker processes: Each service runs multiple worker processes. Default is 4 per service, suitable for systems with 8+ cores. Adjust with services.<name>.workers. For CPU-bound services (data processing, analytics), set workers equal to core count. For I/O-bound services (API gateway, notification), set to 2x core count.",
                    "Monitoring and alerting: Prometheus metrics are exposed at /metrics on each service port. Grafana dashboards are provided in /opt/platform/monitoring/grafana/. Key metrics to monitor: request_duration_seconds (p99 should be under 500ms), error_rate (should be under 0.1%), database_query_duration (p99 under 100ms), and cache_hit_ratio (should be above 0.9).",
                ],
                "Disaster Recovery": [
                    "Backup strategy: Follow the 3-2-1 rule: 3 copies of data, on 2 different media types, with 1 offsite. The platform's automated backup creates daily snapshots of the database and weekly full backups of all data including uploaded files and configurations. Verify backups monthly with a test restore procedure.",
                    "Database recovery: Restore from backup using: ./platform-cli db restore --source=/backup/platformdb-20250315-0200.sql.gz. For point-in-time recovery, configure WAL archiving in PostgreSQL and specify the target time: ./platform-cli db restore --source=/backup/base-latest.tar.gz --target-time='2025-03-15 14:30:00 UTC'.",
                    "Service failover: In cluster deployments, service failover is automatic. The primary node runs a health monitor that detects failed workers and redistributes their workload within 30 seconds. If the primary fails, the worker with the lowest ID assumes the primary role through a leader election protocol based on Raft consensus.",
                    "Data export for migration: Export all data using: ./platform-cli export --format=json --output=/export/full-$(date +%Y%m%d)/. This creates a portable archive that can be imported into any platform instance. The export includes all user data, configurations, custom roles, and system metadata. Import with: ./platform-cli import --source=/export/full-20250315/.",
                ],
            }
        },
        "API Reference": {
            "sections": {
                "Authentication API": [
                    "All API requests require authentication using either API keys or OAuth 2.0 bearer tokens. API keys are generated in the admin interface under Settings > API Keys. Each key has configurable permissions and rate limits. Include the key in the Authorization header: Authorization: Bearer <api-key>.",
                    "OAuth 2.0 token endpoint: POST /api/auth/token. Request body: {\"grant_type\": \"client_credentials\", \"client_id\": \"<id>\", \"client_secret\": \"<secret>\"}. Response: {\"access_token\": \"<jwt>\", \"token_type\": \"Bearer\", \"expires_in\": 3600}. Tokens are JWT signed with RS256. Refresh tokens are supported with grant_type=refresh_token.",
                    "Token validation: GET /api/auth/validate. Include the token in the Authorization header. Response includes user details, permissions, and token expiration. Rate limit: 1000 requests per minute. Use this endpoint to validate tokens in microservice architectures where services need to verify caller identity.",
                    "User session management: POST /api/auth/sessions to create a session (login), DELETE /api/auth/sessions/{id} to invalidate a session (logout), GET /api/auth/sessions to list active sessions. Sessions include metadata: IP address, user agent, creation time, and last activity. Administrators can terminate any session.",
                ],
                "Data API": [
                    "CRUD operations follow RESTful conventions. Base URL: /api/v2/data/{table}. GET / returns paginated list (default: 50 items, max: 1000). GET /{id} returns single record. POST / creates a record. PUT /{id} replaces a record. PATCH /{id} partially updates a record. DELETE /{id} removes a record.",
                    "Filtering: Use query parameters for simple filters: ?status=active&department=engineering. Complex filters use the filter parameter with JSON: ?filter={\"salary\":{\"$gt\":50000,\"$lt\":100000}}. Supported operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin, $regex, $exists.",
                    "Sorting: ?sort=name (ascending) or ?sort=-created_at (descending). Multiple sort fields: ?sort=department,-salary. Null values sort last by default. Override with ?null_sort=first.",
                    "Pagination: ?page=1&per_page=50 for offset-based pagination. ?cursor=<token> for cursor-based pagination (recommended for large datasets). Response includes: total_count, page, per_page, next_cursor. Cursor-based pagination provides consistent results even when data changes between requests.",
                    "Batch operations: POST /api/v2/data/{table}/batch for bulk create/update/delete. Request body: {\"operations\": [{\"method\": \"create\", \"data\": {...}}, {\"method\": \"update\", \"id\": \"123\", \"data\": {...}}, {\"method\": \"delete\", \"id\": \"456\"}]}. Maximum 1000 operations per request. Results are returned in the same order with individual success/error status.",
                ],
                "Webhook API": [
                    "Configure webhooks to receive real-time notifications when events occur. POST /api/webhooks to create a webhook. Required fields: url (HTTPS endpoint), events (array of event types), and optional secret (for HMAC signature verification). The platform sends a verification request to the URL before activation.",
                    "Event types follow a resource.action pattern: data.created, data.updated, data.deleted, user.login, user.logout, system.alert, pipeline.completed, pipeline.failed. Use wildcards for broad subscriptions: data.* for all data events, *.failed for all failure events.",
                    "Webhook payload format: {\"event\": \"data.created\", \"timestamp\": \"2025-03-15T14:30:00Z\", \"data\": {...}, \"webhook_id\": \"wh_123\", \"delivery_id\": \"del_456\"}. Payloads are signed with HMAC-SHA256 using the webhook secret. The signature is included in the X-Webhook-Signature header. Always verify signatures before processing payloads.",
                    "Retry policy: Failed deliveries (non-2xx response or timeout after 30 seconds) are retried with exponential backoff: 1 minute, 5 minutes, 30 minutes, 2 hours, 12 hours. After 5 failed attempts, the webhook is marked as failing and an alert is sent to the administrator. Delivery history is available at GET /api/webhooks/{id}/deliveries.",
                    "Testing webhooks: POST /api/webhooks/{id}/test sends a test event to the configured URL with sample data. The response includes the delivery status and any error messages. Use this to verify your endpoint handles events correctly before subscribing to production events.",
                ],
                "Administrative API": [
                    "System health: GET /api/admin/health returns the status of all services and dependencies. Response includes: overall_status (healthy, degraded, critical), services (array of service health), database (connection pool stats, replication lag), cache (hit rates, memory usage), and disk (usage per volume).",
                    "User management: GET /api/admin/users (list, filterable), POST /api/admin/users (create), PATCH /api/admin/users/{id} (update), DELETE /api/admin/users/{id} (disable). Bulk operations: POST /api/admin/users/bulk with array of operations. Export: GET /api/admin/users/export?format=csv.",
                    "Configuration management: GET /api/admin/config returns the current running configuration (secrets are masked). PATCH /api/admin/config updates configuration values. Changes are validated before applying. Some changes require a service restart, indicated in the response. GET /api/admin/config/history shows all configuration changes with timestamps and users.",
                    "Maintenance mode: POST /api/admin/maintenance/enable activates maintenance mode, which displays a maintenance page to users and queues incoming requests. POST /api/admin/maintenance/disable deactivates it and processes queued requests. During maintenance, API requests return 503 Service Unavailable with a Retry-After header.",
                ],
            }
        },
    }

    # --- Generate document content ---
    first_chapter = True
    for chapter_title, chapter_data in chapters.items():
        # Add chapter heading (Heading 1)
        h = H(outlinelevel="1", stylename=h1_style)
        h.addText(chapter_title)
        doc.text.addElement(h)

        # Add intro paragraph
        p = P(stylename=body_style)
        p.addText(f"This chapter covers {chapter_title.lower()} in detail. "
                   "The following sections provide comprehensive information and step-by-step instructions "
                   "to help you understand and work with all aspects of this topic effectively.")
        doc.text.addElement(p)

        for section_title, paragraphs in chapter_data["sections"].items():
            # Section heading (Heading 2)
            h2 = H(outlinelevel="2", stylename=h2_style)
            h2.addText(section_title)
            doc.text.addElement(h2)

            for para_text in paragraphs:
                p = P(stylename=body_style)
                p.addText(para_text)
                doc.text.addElement(p)

                # Add extra filler paragraph for page count
                filler = P(stylename=body_style)
                filler.addText("")
                doc.text.addElement(filler)

        # Add some extra spacing paragraphs between chapters to reach ~50 pages
        for _ in range(3):
            spacer = P(stylename=body_style)
            spacer.addText("")
            doc.text.addElement(spacer)

    doc.save(OUTPUT)
    print(f"Initial file created: {OUTPUT}")

    # Verify file size
    file_size = os.path.getsize(OUTPUT)
    print(f"File size: {file_size} bytes")

    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched LibreOffice Writer with DISPLAY=:0")


create_initial()
