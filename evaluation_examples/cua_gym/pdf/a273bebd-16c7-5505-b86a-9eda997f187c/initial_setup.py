"""
Initial Setup: Create a 25-page user guide PDF with four chapters, no headers.
Task ID: pdf_pw_038
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_038'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/user_guide.pdf'

# Letter size
PAGE_W, PAGE_H = 612, 792

# Chapter definitions with page ranges and content
CHAPTERS = [
    {
        "title": "Chapter 1: Getting Started",
        "pages": 5,
        "sections": [
            ("1.1 Welcome to DataSync Pro", [
                "Welcome to DataSync Pro, the enterprise-grade data synchronization platform designed for modern businesses. This guide will walk you through everything you need to know to get started with our platform, from initial installation to your first successful data sync.",
                "DataSync Pro supports over 40 data sources including PostgreSQL, MySQL, MongoDB, Amazon S3, Google BigQuery, Snowflake, and many more. Whether you are migrating data between cloud providers or maintaining real-time replicas across your infrastructure, DataSync Pro has you covered.",
            ]),
            ("1.2 System Requirements", [
                "Before installing DataSync Pro, ensure your system meets the following minimum requirements: 4 CPU cores (8 recommended), 16 GB RAM (32 GB recommended), 100 GB available disk space, and a stable network connection with at least 100 Mbps bandwidth.",
                "Supported operating systems include Ubuntu 20.04 LTS or later, CentOS 8 or later, Red Hat Enterprise Linux 8+, Debian 11+, and Windows Server 2019 or later. macOS is supported for development environments only.",
                "You will also need Docker 20.10+ and Docker Compose 2.0+ if you plan to use our containerized deployment option, which is recommended for production environments.",
            ]),
            ("1.3 Installation", [
                "To install DataSync Pro, download the latest release from our portal at downloads.datasyncpro.io. Extract the archive and run the installation wizard. On Linux systems, execute: sudo ./install.sh --accept-license.",
                "The installer will verify system requirements, set up the database backend, configure network interfaces, and create the initial administrator account. The entire process typically takes 5-10 minutes depending on your hardware.",
                "After installation, verify the setup by running: datasync status. You should see all services listed as 'running'. If any service shows 'stopped', consult the troubleshooting chapter of this guide.",
            ]),
            ("1.4 Quick Start Tutorial", [
                "Let us set up your first synchronization job. Navigate to the web dashboard at https://localhost:8443 and log in with the admin credentials created during installation.",
                "Click 'New Sync Job' in the top navigation bar. Select your source database type from the dropdown, enter the connection details, and click 'Test Connection'. Once verified, repeat for the destination.",
                "Configure the sync frequency (real-time, hourly, daily, or custom cron), select the tables or collections to synchronize, and click 'Start Sync'. Monitor progress on the dashboard.",
            ]),
            ("1.5 Understanding the Dashboard", [
                "The DataSync Pro dashboard provides real-time visibility into all your synchronization jobs. The main panel shows active jobs with their current status, throughput metrics, and error counts.",
                "The left sidebar contains navigation links to Jobs, Sources, Destinations, Schedules, Alerts, and Settings. Each section provides detailed management capabilities for that aspect of the platform.",
            ]),
        ],
    },
    {
        "title": "Chapter 2: Configuration",
        "pages": 7,
        "sections": [
            ("2.1 Global Settings", [
                "Global settings affect all synchronization jobs and system behavior. Access them through Settings > Global Configuration in the web dashboard, or edit /etc/datasync/global.yaml directly.",
                "Key global settings include the default retry policy (max_retries: 3, backoff_multiplier: 2.0), logging level (INFO for production, DEBUG for troubleshooting), and the data directory path where temporary files are stored during sync operations.",
                "Performance tuning parameters such as max_concurrent_jobs (default: 10), worker_thread_count (default: 4 per job), and buffer_size_mb (default: 256) can significantly impact throughput.",
            ]),
            ("2.2 Source Configuration", [
                "Each data source requires specific connection parameters. For relational databases like PostgreSQL and MySQL, you need: hostname, port, database name, username, password, and optionally an SSL certificate path.",
                "For cloud storage sources like Amazon S3, configure the bucket name, region, access key ID, and secret access key. We recommend using IAM roles instead of static credentials when running on AWS infrastructure.",
                "MongoDB sources require the connection URI in the format mongodb://user:pass@host:port/dbname?replicaSet=rs0. Change Data Capture (CDC) requires a replica set configuration.",
            ]),
            ("2.3 Destination Configuration", [
                "Destination configuration follows similar patterns to source configuration. The key difference is that destinations also support schema mapping and data transformation rules.",
                "When syncing between different database types (e.g., PostgreSQL to BigQuery), DataSync Pro automatically maps data types. You can override these mappings in the destination configuration under the type_mappings section.",
                "For data warehouse destinations like Snowflake and BigQuery, configure the warehouse/dataset, staging area, and load method (append, upsert, or full replace).",
            ]),
            ("2.4 Network and Security Settings", [
                "DataSync Pro supports encrypted connections via TLS 1.2+ for all data transfers. Enable encryption by setting tls_enabled: true in the connection configuration and providing certificate paths.",
                "For environments with strict firewall rules, configure the proxy settings under network.proxy. DataSync Pro supports HTTP, HTTPS, and SOCKS5 proxy protocols.",
                "IP allowlisting can be configured to restrict which hosts can access the management API. Set allowed_ips in /etc/datasync/security.yaml to a list of CIDR ranges.",
            ]),
            ("2.5 Scheduling and Automation", [
                "Synchronization schedules use standard cron expressions with an optional seconds field. For example, '0 */15 * * * *' runs every 15 minutes, while '0 0 2 * * *' runs daily at 2:00 AM.",
                "Event-driven triggers can start sync jobs based on webhook notifications, file system events, or database change events. Configure triggers under the automation section of each job.",
                "Dependency chains allow you to define job sequences where one job starts only after another completes successfully. This is useful for ETL pipelines with multiple stages.",
            ]),
            ("2.6 Data Transformation Rules", [
                "DataSync Pro includes a built-in transformation engine that can modify data during synchronization. Transformations are defined in YAML format and applied per-column.",
                "Common transformations include: type casting (cast: integer), string manipulation (transform: uppercase), date formatting (format: '%Y-%m-%d'), null handling (default: 0), and masking (mask: 'email').",
                "For complex transformations, you can write custom Python functions and register them as plugins. Place your plugin files in /etc/datasync/plugins/ and reference them in the transformation config.",
            ]),
            ("2.7 Monitoring and Alerting", [
                "Configure alert rules to be notified of sync failures, performance degradation, or data quality issues. Alerts can be sent via email, Slack, PagerDuty, or custom webhooks.",
                "Metrics are exposed via a Prometheus-compatible endpoint at /metrics. Key metrics include sync_rows_per_second, sync_lag_seconds, error_count, and job_duration_seconds.",
            ]),
        ],
    },
    {
        "title": "Chapter 3: Advanced Usage",
        "pages": 8,
        "sections": [
            ("3.1 Change Data Capture (CDC)", [
                "Change Data Capture enables real-time synchronization by reading database transaction logs. This approach is significantly more efficient than polling-based sync for large tables.",
                "For PostgreSQL, CDC uses logical replication slots. Ensure wal_level is set to 'logical' in postgresql.conf and create a replication slot: SELECT pg_create_logical_replication_slot('datasync_slot', 'pgoutput').",
                "MySQL CDC requires binlog_format=ROW and binlog_row_image=FULL in the MySQL configuration. The DataSync Pro user needs REPLICATION SLAVE and REPLICATION CLIENT privileges.",
            ]),
            ("3.2 Schema Evolution Handling", [
                "DataSync Pro automatically detects and handles schema changes in source databases. When a new column is added, it can be automatically propagated to the destination.",
                "Schema evolution policies can be set to 'auto' (automatically apply changes), 'notify' (alert administrators), or 'block' (pause sync until manually approved).",
                "For complex schema changes like column renames or type changes, create a migration plan in the web UI under Jobs > [Job Name] > Schema Migrations.",
            ]),
            ("3.3 Conflict Resolution", [
                "When syncing bidirectionally or merging data from multiple sources, conflicts may arise. DataSync Pro supports several resolution strategies: last-writer-wins, source-priority, custom-function, and manual-review.",
                "The last-writer-wins strategy uses timestamps to determine which version to keep. Ensure all sources have synchronized clocks (NTP recommended) for accurate conflict resolution.",
                "Custom conflict resolution functions receive both versions of the conflicting record and must return the resolved version. Register these functions as plugins in /etc/datasync/plugins/conflict_resolvers/.",
            ]),
            ("3.4 Data Validation and Quality Checks", [
                "Define validation rules that run during synchronization to catch data quality issues. Rules can check for null values, data type conformance, referential integrity, and custom business logic.",
                "Validation failures can be configured to log warnings, quarantine bad records, or halt the sync job entirely. Quarantined records are stored in a dedicated table for review.",
                "Built-in validators include: not_null, unique, range(min, max), regex(pattern), foreign_key(table.column), and custom(function_name). Chain multiple validators with AND/OR logic.",
            ]),
            ("3.5 Performance Optimization", [
                "For high-volume synchronization, tune the following parameters: batch_size (number of rows per batch, default 10000), parallel_streams (number of concurrent data streams, default 4), and compression (enable gzip for network transfer).",
                "Partitioned tables benefit from parallel partition sync. Enable this with partition_parallel: true in the job configuration. Each partition is synced by a separate worker thread.",
                "Index management during bulk loads: disable destination indexes before full-table sync and rebuild after completion. Set index_management: auto to let DataSync Pro handle this automatically.",
            ]),
            ("3.6 API Integration", [
                "The DataSync Pro REST API provides programmatic access to all platform features. The base URL is https://localhost:8443/api/v2/. Authenticate using Bearer tokens obtained from /api/v2/auth/token.",
                "Common API operations include: GET /jobs (list all jobs), POST /jobs (create a job), GET /jobs/{id}/status (check job status), POST /jobs/{id}/start (trigger a sync), and DELETE /jobs/{id} (remove a job).",
                "Rate limits are set to 1000 requests per minute per authenticated user. For higher limits, contact your account manager or adjust rate_limit_rpm in the security configuration.",
            ]),
            ("3.7 High Availability Setup", [
                "For production deployments, configure DataSync Pro in a high-availability cluster with at least three nodes. The cluster uses Raft consensus for leader election and job distribution.",
                "Node configuration requires setting cluster.enabled: true, cluster.node_id (unique per node), cluster.peers (list of other node addresses), and cluster.data_dir (for Raft log storage).",
                "During a failover, running jobs are automatically reassigned to healthy nodes. The failover process typically completes within 30 seconds, with zero data loss due to checkpoint-based recovery.",
            ]),
            ("3.8 Custom Connectors", [
                "Extend DataSync Pro by building custom connectors for proprietary or unsupported data sources. The connector SDK provides base classes and interfaces for implementing source and destination connectors.",
                "A minimal connector implementation requires three methods: connect() for establishing the connection, read_batch() or write_batch() for data transfer, and get_schema() for schema discovery.",
            ]),
        ],
    },
    {
        "title": "Chapter 4: Troubleshooting",
        "pages": 5,
        "sections": [
            ("4.1 Common Error Messages", [
                "ERROR: Connection refused - The source or destination database is not accepting connections. Verify the hostname, port, and firewall rules. Ensure the database service is running.",
                "ERROR: Authentication failed - Check the username and password. For databases using certificate-based authentication, verify the certificate path and permissions.",
                "ERROR: Replication slot not found - The CDC replication slot may have been dropped. Recreate it using the appropriate database command and restart the sync job.",
                "ERROR: Out of memory - The sync job exceeded the allocated memory. Reduce batch_size or increase the worker memory limit in global settings.",
            ]),
            ("4.2 Performance Issues", [
                "Symptom: Sync throughput below expected levels. Check network bandwidth between source and destination. Use 'datasync benchmark' to run a connectivity test between endpoints.",
                "Symptom: High CPU usage on the DataSync Pro server. Review the number of concurrent jobs and reduce max_concurrent_jobs if the server is overloaded. Consider scaling horizontally.",
                "Symptom: Destination database experiencing lock contention. Switch to batch upsert mode and increase the batch interval. For PostgreSQL destinations, consider using COPY instead of INSERT.",
            ]),
            ("4.3 Log Analysis", [
                "DataSync Pro logs are stored in /var/log/datasync/ with rotation configured at 100 MB per file and 7 days retention. The main log file is datasync.log.",
                "Enable debug logging temporarily with: datasync config set log_level DEBUG. Remember to set it back to INFO after troubleshooting to avoid excessive disk usage.",
                "Structured log entries include a correlation ID (corr_id) that links all log messages for a single sync operation. Filter by correlation ID to trace a specific job execution.",
            ]),
            ("4.4 Recovery Procedures", [
                "To recover from a failed sync job, first check the job status: datasync job status <job_id>. If the job is in 'failed' state, review the error details and fix the underlying issue.",
                "For checkpoint recovery, DataSync Pro stores progress checkpoints every 60 seconds. When a job restarts after failure, it automatically resumes from the last checkpoint.",
                "In case of data corruption, use the 'datasync verify' command to compare source and destination data. It generates a detailed report of mismatches that can be used for targeted repairs.",
            ]),
            ("4.5 Getting Support", [
                "For additional help, visit our documentation portal at docs.datasyncpro.io or join the community forum at community.datasyncpro.io.",
                "Enterprise customers can open support tickets through the support portal or email support@datasyncpro.io. Include the output of 'datasync diagnostics' in your ticket for faster resolution.",
                "When reporting issues, provide: DataSync Pro version (datasync --version), operating system and version, relevant log entries (with corr_id), and steps to reproduce the problem.",
            ]),
        ],
    },
]


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

    # Content margins
    LEFT_MARGIN = 72
    TOP_MARGIN = 72  # Start content well below header area (y < 40 is empty)
    RIGHT_MARGIN = 540
    BOTTOM_MARGIN = 740
    CONTENT_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

    page_index = 0  # tracks total pages created

    for chapter in CHAPTERS:
        chapter_title = chapter["title"]
        sections = chapter["sections"]
        target_pages = chapter["pages"]

        # Calculate how to distribute sections across pages
        # First page of chapter gets the chapter title
        section_idx = 0

        for p in range(target_pages):
            page = doc.new_page(width=PAGE_W, height=PAGE_H)
            y = TOP_MARGIN

            if p == 0:
                # Chapter title on first page
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN, y),
                    chapter_title,
                    fontsize=22,
                    fontname="hebo",
                    color=(0.1, 0.1, 0.3),
                )
                y += 40

                # Horizontal rule under chapter title
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(LEFT_MARGIN, y), pymupdf.Point(RIGHT_MARGIN, y))
                shape.finish(color=(0.3, 0.3, 0.5), width=1.5)
                shape.commit()
                y += 20

            # Add section content for this page
            while section_idx < len(sections) and y < BOTTOM_MARGIN - 60:
                sec_title, sec_paragraphs = sections[section_idx]

                # Section heading
                if y + 30 > BOTTOM_MARGIN - 60:
                    break
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN, y),
                    sec_title,
                    fontsize=14,
                    fontname="hebo",
                    color=(0.15, 0.15, 0.4),
                )
                y += 24

                # Paragraphs
                for para in sec_paragraphs:
                    if y + 20 > BOTTOM_MARGIN - 20:
                        break
                    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, BOTTOM_MARGIN - 20)
                    excess = page.insert_textbox(
                        rect,
                        para,
                        fontsize=10.5,
                        fontname="helv",
                        color=(0.1, 0.1, 0.1),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY,
                    )
                    # Estimate how much vertical space the text used
                    # Each line is approximately 14 points high
                    chars_per_line = CONTENT_WIDTH / 5.5  # rough estimate
                    num_lines = max(1, len(para) / chars_per_line)
                    text_height = num_lines * 14
                    y += text_height + 10

                section_idx += 1

            # Page number at bottom center
            page_num_text = str(page_index + 1)
            page.insert_text(
                pymupdf.Point(PAGE_W / 2 - 5, PAGE_H - 36),
                page_num_text,
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

            page_index += 1

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_index}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
