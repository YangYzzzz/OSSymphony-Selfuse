"""
Initial Setup: Create a user guide PDF with hierarchical bookmarks
Task ID: pdf_mbc_036
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_036'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/user_guide.pdf'


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


def add_page_content(doc, page_num, title, body_paragraphs):
    """Add a page with title and body text to the document."""
    page = doc[page_num]
    # Title
    page.insert_text(
        pymupdf.Point(72, 72),
        title,
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.15, 0.35),
    )
    # Horizontal rule under title
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 85), pymupdf.Point(523, 85))
    shape.finish(color=(0.3, 0.3, 0.6), width=1.5)
    shape.commit()

    # Body text
    y_pos = 110
    for para in body_paragraphs:
        rect = pymupdf.Rect(72, y_pos, 523, y_pos + 80)
        excess = page.insert_textbox(
            rect,
            para,
            fontsize=11,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )
        y_pos += 85


def create_initial():
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Create 16 pages (0-indexed: 0..15, pages 1..16 in 1-indexed)
    for i in range(16):
        doc.new_page(width=595, height=842)

    # --- Page 1 (index 0): Introduction ---
    add_page_content(doc, 0, "Introduction", [
        "Welcome to the DataFlow Analytics Platform User Guide. This comprehensive "
        "documentation will walk you through every aspect of the platform, from initial "
        "setup to advanced data pipeline configurations.",
        "DataFlow Analytics Platform version 4.2 was released in March 2025 and includes "
        "significant improvements to real-time streaming, dashboard customization, and "
        "role-based access control. Over 2,500 organizations worldwide rely on DataFlow "
        "for their business intelligence needs.",
        "This guide is organized into sections that progress from basic concepts to "
        "advanced usage patterns. We recommend reading the Getting Started section first "
        "if you are new to the platform.",
    ])

    # --- Page 2 (index 1): Introduction continued ---
    add_page_content(doc, 1, "Introduction (continued)", [
        "The DataFlow ecosystem consists of three main components: the Ingestion Engine, "
        "the Processing Core, and the Visualization Layer. Each component can be deployed "
        "independently or as part of a unified stack.",
        "System requirements include a minimum of 8 GB RAM, 4 CPU cores, and 50 GB of "
        "available disk space. For production deployments, we recommend 32 GB RAM, 16 cores, "
        "and SSD storage with at least 500 GB capacity.",
    ])

    # --- Page 3 (index 2): Getting Started / Installation ---
    add_page_content(doc, 2, "Getting Started", [
        "This section covers everything you need to get DataFlow up and running on your "
        "infrastructure. We support deployment on Linux (Ubuntu 20.04+, CentOS 8+), "
        "macOS (12+), and Windows Server 2019+.",
        "Installation",
        "To install DataFlow Analytics Platform, download the appropriate package from "
        "https://downloads.dataflow.io/v4.2/ and follow the steps below for your "
        "operating system.",
        "For Ubuntu/Debian systems, run: sudo apt update && sudo apt install dataflow-platform. "
        "For Red Hat/CentOS, use: sudo yum install dataflow-platform. Docker users can pull "
        "the official image: docker pull dataflow/platform:4.2-stable.",
    ])

    # --- Page 4 (index 3): Installation continued ---
    add_page_content(doc, 3, "Installation (continued)", [
        "After installing the base package, verify the installation by running "
        "'dataflow --version' in your terminal. You should see output similar to: "
        "DataFlow Analytics Platform v4.2.1 (build 20250315).",
        "Next, initialize the database schema by running 'dataflow init-db'. This creates "
        "the necessary tables in your configured PostgreSQL instance. Ensure PostgreSQL 14+ "
        "is running before executing this command.",
        "The default admin credentials are set during initialization. You will be prompted "
        "to create an admin username and password. Store these securely as they provide "
        "full system access.",
    ])

    # --- Page 5 (index 4): Configuration ---
    add_page_content(doc, 4, "Configuration", [
        "DataFlow is configured through a YAML file located at /etc/dataflow/config.yml. "
        "This file controls database connections, authentication providers, logging levels, "
        "and resource allocation.",
        "Key configuration parameters include: db_host (default: localhost), db_port "
        "(default: 5432), max_workers (default: 8), cache_size_mb (default: 512), "
        "log_level (options: DEBUG, INFO, WARN, ERROR), and auth_provider (options: "
        "local, ldap, saml, oauth2).",
        "For LDAP integration, set auth_provider to 'ldap' and configure the ldap_host, "
        "ldap_base_dn, and ldap_bind_user parameters. Test the connection with "
        "'dataflow test-auth --provider ldap' before enabling it in production.",
    ])

    # --- Pages 6-9 (indices 5-8): Configuration continued / filler ---
    add_page_content(doc, 5, "Configuration (continued)", [
        "Email notification settings are managed under the 'notifications' section of the "
        "config file. Supported transports include SMTP, SendGrid API, and AWS SES.",
        "Example SMTP configuration: smtp_host: mail.company.com, smtp_port: 587, "
        "smtp_tls: true, smtp_user: dataflow@company.com. Test email delivery with "
        "'dataflow test-email admin@company.com'.",
    ])

    add_page_content(doc, 6, "Data Sources", [
        "DataFlow supports over 40 pre-built connectors for popular databases, APIs, and "
        "file formats. These include PostgreSQL, MySQL, MongoDB, Elasticsearch, REST APIs, "
        "CSV/Excel files, and cloud storage (S3, GCS, Azure Blob).",
        "To add a new data source, navigate to Settings > Data Sources > Add New in the "
        "web interface. Select the connector type and provide the required credentials. "
        "All credentials are encrypted at rest using AES-256.",
    ])

    add_page_content(doc, 7, "Data Pipelines", [
        "Pipelines define how data flows from sources through transformations to destinations. "
        "Each pipeline consists of one or more stages: Extract, Transform, and Load (ETL).",
        "Create a pipeline using the visual pipeline builder or define it in YAML. The visual "
        "builder supports drag-and-drop stage creation with real-time preview of data at "
        "each transformation step.",
    ])

    add_page_content(doc, 8, "Dashboard Design", [
        "The dashboard designer provides a grid-based layout system with support for "
        "charts, tables, KPI cards, and embedded content. Each dashboard can contain "
        "up to 50 widgets arranged across multiple tabs.",
        "Available chart types include: bar, line, area, scatter, pie, donut, treemap, "
        "heatmap, funnel, gauge, and geographic map. Each chart supports customizable "
        "colors, legends, axes, and drill-down interactions.",
    ])

    # --- Page 10 (index 9): Advanced Usage ---
    add_page_content(doc, 9, "Advanced Usage", [
        "This section covers advanced features for power users and administrators, including "
        "custom transformation functions, API automation, scheduled reports, and multi-tenant "
        "deployment strategies.",
        "Custom Functions: DataFlow supports user-defined functions (UDFs) written in Python "
        "or SQL. UDFs can be registered globally or scoped to specific pipelines. To create "
        "a UDF, navigate to Settings > Functions > Create New.",
        "API Automation: The DataFlow REST API provides programmatic access to all platform "
        "features. Authenticate using API keys generated from Settings > API Keys. Rate "
        "limits are set to 1000 requests per minute per key by default.",
    ])

    # --- Pages 11-14 (indices 10-13): Advanced usage continued ---
    add_page_content(doc, 10, "Advanced Usage (continued)", [
        "Scheduled Reports: Configure automated report generation and delivery through the "
        "Scheduler module. Reports can be exported as PDF, Excel, or CSV and delivered via "
        "email, SFTP, or webhook.",
        "Cron expressions control scheduling. Common patterns: '0 8 * * 1-5' (weekdays at "
        "8 AM), '0 0 1 * *' (first of each month), '*/15 * * * *' (every 15 minutes). "
        "Maximum concurrent report jobs: 10 (configurable).",
    ])

    add_page_content(doc, 11, "Performance Tuning", [
        "For large-scale deployments processing over 1 million records per hour, consider "
        "these optimizations: increase max_workers to match CPU core count, enable "
        "query_cache with a size of at least 1 GB, and configure connection pooling.",
        "Database indexing strategy: create indexes on frequently filtered columns. Use "
        "EXPLAIN ANALYZE on slow queries to identify missing indexes. DataFlow's query "
        "analyzer (Settings > Performance > Query Analyzer) provides automated recommendations.",
    ])

    add_page_content(doc, 12, "Security Hardening", [
        "Production deployments should follow these security best practices: enable TLS "
        "for all connections, rotate API keys every 90 days, configure IP allowlisting, "
        "and enable audit logging.",
        "Role-based access control (RBAC) supports custom roles with granular permissions. "
        "Built-in roles include: Viewer (read-only), Editor (create/modify), Admin (full "
        "access), and Super Admin (system configuration).",
    ])

    add_page_content(doc, 13, "Troubleshooting", [
        "Common issues and solutions: If the web interface returns a 502 error, check that "
        "the application server is running with 'systemctl status dataflow'. For database "
        "connection failures, verify PostgreSQL is accessible and credentials are correct.",
        "Log files are located at /var/log/dataflow/. The main application log is app.log, "
        "pipeline execution logs are in pipelines/, and authentication events are recorded "
        "in auth.log. Enable DEBUG logging temporarily for detailed diagnostics.",
    ])

    # --- Page 15 (index 14): FAQ ---
    add_page_content(doc, 14, "Frequently Asked Questions", [
        "Q: How many concurrent users does DataFlow support? "
        "A: The standard license supports up to 100 concurrent users. Enterprise licenses "
        "have no user limit. Performance depends on server resources; we recommend 1 GB RAM "
        "per 25 concurrent users.",
        "Q: Can I migrate data from my existing BI tool? "
        "A: Yes, DataFlow provides migration utilities for Tableau, Power BI, and Looker. "
        "Run 'dataflow migrate --from <tool> --config migration.yml' to transfer dashboards "
        "and data source configurations.",
        "Q: Is there a cloud-hosted version? "
        "A: DataFlow Cloud is available at https://cloud.dataflow.io with managed "
        "infrastructure, automatic updates, and 99.9% uptime SLA. Plans start at $299/month "
        "for teams of up to 10 users.",
    ])

    # --- Page 16 (index 15): FAQ continued ---
    add_page_content(doc, 15, "FAQ (continued)", [
        "Q: How do I upgrade to a newer version? "
        "A: Run 'dataflow upgrade --to <version>' to perform an in-place upgrade. Always "
        "back up your database before upgrading. Downgrades are supported for one major "
        "version back.",
        "Q: Where can I get support? "
        "A: Community support is available at https://community.dataflow.io. Enterprise "
        "customers receive priority support via support@dataflow.io with a guaranteed "
        "4-hour response time during business hours.",
    ])

    # --- Set Table of Contents / Bookmarks ---
    toc = [
        [1, "Introduction", 1],
        [1, "Getting Started", 3],
        [2, "Installation", 3],
        [2, "Configuration", 5],
        [1, "Advanced Usage", 10],
        [1, "FAQ", 15],
    ]
    doc.set_toc(toc)

    # --- Set metadata ---
    doc.set_metadata({
        "title": "DataFlow Analytics Platform User Guide",
        "author": "DataFlow Documentation Team",
        "subject": "User Guide for DataFlow Analytics Platform v4.2",
        "keywords": "dataflow, analytics, user guide, documentation",
        "creator": "DataFlow Docs Generator",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify bookmarks
    doc = pymupdf.open(OUTPUT)
    toc = doc.get_toc()
    print(f'Bookmarks in PDF: {toc}')
    print(f'Page count: {doc.page_count}')
    doc.close()

    # GUI-ready: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
