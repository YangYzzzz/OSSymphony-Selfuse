"""
Initial Setup: PDF merge task - create source PDFs and merge list
Task ID: pdf_cross_126
Domain: pdf (cross-domain: VSCode + Terminal + PDF)
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
TASK_ID = 'pdf_cross_126'
DOCS_DIR = f'{WORKDIR}/Documents'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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


def create_pdf_with_content(path, title, pages_data):
    """Create a PDF with given title and multiple pages of content."""
    doc = pymupdf.open()
    for page_num, (heading, paragraphs) in enumerate(pages_data):
        page = doc.new_page(width=612, height=792)  # Letter size

        # Draw a light header background
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, 612, 60))
        shape.finish(fill=(0.15, 0.35, 0.65), color=None)
        shape.commit()

        # Page title / header
        page.insert_text(
            pymupdf.Point(36, 40),
            title,
            fontsize=14,
            fontname="hebo",
            color=(1.0, 1.0, 1.0),
        )

        # Page number
        page.insert_text(
            pymupdf.Point(540, 40),
            f"Page {page_num + 1}",
            fontsize=10,
            fontname="helv",
            color=(1.0, 1.0, 1.0),
        )

        # Section heading
        page.insert_text(
            pymupdf.Point(36, 90),
            heading,
            fontsize=16,
            fontname="hebo",
            color=(0.15, 0.35, 0.65),
        )

        # Horizontal rule
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(36, 100), pymupdf.Point(576, 100))
        shape2.finish(color=(0.15, 0.35, 0.65), width=1.5)
        shape2.commit()

        # Body paragraphs
        y = 120
        for para in paragraphs:
            rect = pymupdf.Rect(36, y, 576, y + 400)
            excess = page.insert_textbox(
                rect,
                para,
                fontsize=11,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            # Estimate paragraph height: roughly 14pt per line, ~80 chars/line
            lines = max(1, len(para) // 80 + 1)
            y += lines * 16 + 12
            if y > 720:
                break

        # Footer
        shape3 = page.new_shape()
        shape3.draw_line(pymupdf.Point(36, 750), pymupdf.Point(576, 750))
        shape3.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape3.commit()
        page.insert_text(
            pymupdf.Point(36, 768),
            "Confidential — Internal Use Only",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(path)
    doc.close()
    print(f"  Created: {path} ({len(pages_data)} pages)")


def create_initial():
    # Ensure directories exist
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # --- Create intro.pdf (3 pages) ---
    create_pdf_with_content(
        f'{DOCS_DIR}/intro.pdf',
        'Technical Documentation — Project Overview',
        [
            (
                "Introduction",
                [
                    "This document provides a comprehensive introduction to the Advanced Data Processing "
                    "System (ADPS), a robust platform designed to handle large-scale data ingestion, "
                    "transformation, and analytics workloads in enterprise environments.",

                    "The system was developed in response to growing demand for scalable, fault-tolerant "
                    "data pipelines that can integrate seamlessly with existing business intelligence "
                    "infrastructure. Since its initial deployment in March 2023, ADPS has processed "
                    "over 2.4 terabytes of data across 17 production environments.",

                    "Key stakeholders include the Data Engineering team (led by Sarah Chen), the "
                    "Analytics division (Marcus Johnson, Director), and the Platform Infrastructure "
                    "group. External partners such as DataBridge Corp and NovaTech Solutions also "
                    "contribute modules to the integration layer.",
                ]
            ),
            (
                "System Architecture Overview",
                [
                    "ADPS follows a microservices architecture with four primary layers: ingestion, "
                    "transformation, storage, and serving. Each layer exposes a well-defined REST API, "
                    "enabling independent scaling and deployment.",

                    "The ingestion layer supports 12 data source connectors including PostgreSQL, "
                    "MongoDB, Apache Kafka, and AWS S3. Throughput benchmarks recorded during Q4 2024 "
                    "testing showed sustained rates of 850,000 records per second on standard EC2 "
                    "m5.xlarge instances.",

                    "Fault tolerance is achieved through a combination of write-ahead logging (WAL), "
                    "idempotent consumers, and a distributed checkpoint mechanism backed by Apache "
                    "ZooKeeper 3.8.1. Recovery time objectives (RTO) average 4.2 seconds in "
                    "controlled failover tests conducted by the QA team.",
                ]
            ),
            (
                "Scope and Objectives",
                [
                    "This documentation suite covers installation, configuration, operational procedures, "
                    "and troubleshooting for ADPS version 3.2.1. It is intended for system administrators, "
                    "DevOps engineers, and senior data engineers with at least two years of experience "
                    "working with distributed systems.",

                    "Readers are expected to have working knowledge of Linux system administration, "
                    "container orchestration (Kubernetes 1.28+), and familiarity with Python 3.10+ "
                    "and SQL. Background in Apache Spark or similar batch processing frameworks is "
                    "helpful but not required.",
                ]
            ),
        ]
    )

    # --- Create chapter1.pdf (4 pages) ---
    create_pdf_with_content(
        f'{DOCS_DIR}/chapter1.pdf',
        'Technical Documentation — Chapter 1: Installation',
        [
            (
                "1.1 Prerequisites and System Requirements",
                [
                    "Before installing ADPS, ensure the target environment meets the minimum hardware "
                    "and software requirements. The recommended production configuration uses dedicated "
                    "servers with 32 CPU cores, 128 GB RAM, and NVMe SSD storage with at least 2 TB "
                    "available capacity.",

                    "Operating system support includes Ubuntu 22.04 LTS, RHEL 8.6+, and CentOS Stream 9. "
                    "Docker Engine 24.0+ and Kubernetes 1.28+ are required for containerized deployments. "
                    "Bare-metal installations are supported but require manual dependency management.",

                    "Network requirements: all cluster nodes must have bidirectional connectivity on "
                    "ports 2181 (ZooKeeper), 9092 (Kafka), 5432 (PostgreSQL internal), and 8080-8099 "
                    "(ADPS service mesh). A minimum 10 Gbps intra-cluster network is strongly recommended.",
                ]
            ),
            (
                "1.2 Package Installation",
                [
                    "Download the ADPS distribution package from the internal artifact repository at "
                    "https://artifacts.internal.corp/adps/releases/3.2.1/. The SHA-256 checksum must "
                    "be verified before proceeding: "
                    "a7f3c9e2b1d458f0ea23567cd890ab12ef45678901234567890abcdef123456.",

                    "Extract the archive to /opt/adps and run the bootstrap script as root: "
                    "sudo bash /opt/adps/scripts/bootstrap.sh --env production --region us-east-1. "
                    "The bootstrap script automatically detects hardware configuration, sets kernel "
                    "parameters (vm.swappiness=10, net.core.somaxconn=65535), and installs "
                    "all required system packages via apt or yum.",

                    "Post-installation verification is performed by running the built-in health check: "
                    "adps-ctl status --verbose. Expected output shows all 8 core services in RUNNING "
                    "state within 90 seconds of startup. If any service fails to start, consult the "
                    "troubleshooting guide in Appendix B.",
                ]
            ),
            (
                "1.3 Database Initialization",
                [
                    "ADPS requires a dedicated PostgreSQL 15 instance for its metadata store. Create "
                    "the database using: createdb -U postgres adps_metadata. Then run the schema "
                    "migration: adps-migrate up --target latest --db-url postgresql://adps:pass@localhost/adps_metadata.",

                    "Default database credentials should be changed immediately after installation. "
                    "Use the adps-admin tool: adps-admin set-password --role adps_service. Passwords "
                    "must be at least 16 characters and include uppercase, lowercase, digits, and "
                    "special characters per corporate security policy SEC-2024-007.",
                ]
            ),
            (
                "1.4 Initial Configuration",
                [
                    "The primary configuration file is located at /etc/adps/adps.yaml. Key parameters "
                    "include cluster_id (must be globally unique), storage_backend (supported values: "
                    "local, s3, gcs, azure-blob), and replication_factor (default: 3 for production).",

                    "Environment-specific configuration overrides are supported via /etc/adps/conf.d/*.yaml. "
                    "All files in this directory are merged at startup in alphabetical order. Use numeric "
                    "prefixes (e.g., 10-network.yaml, 20-storage.yaml) to control merge order when "
                    "override precedence matters.",
                ]
            ),
        ]
    )

    # --- Create chapter2.pdf (4 pages) ---
    create_pdf_with_content(
        f'{DOCS_DIR}/chapter2.pdf',
        'Technical Documentation — Chapter 2: Configuration',
        [
            (
                "2.1 Core Configuration Parameters",
                [
                    "ADPS exposes over 200 configurable parameters organized into functional categories. "
                    "This chapter covers the most commonly tuned parameters for production deployments. "
                    "A complete reference is available in the online documentation portal.",

                    "The ingestion.batch_size parameter controls how many records are grouped into a "
                    "single processing batch. Default value is 1000; for high-latency sources, reducing "
                    "to 100-250 can improve responsiveness. For bulk historical loads, values of 5000-10000 "
                    "typically yield better throughput. Benchmarks conducted by the performance team "
                    "in November 2024 showed optimal throughput at batch_size=2500 for mixed workloads.",

                    "The transformation.thread_pool_size controls parallelism in the transformation "
                    "layer. Rule of thumb: set to (CPU cores - 2) to leave headroom for I/O threads. "
                    "Values above 64 provide diminishing returns and may cause thread contention on "
                    "most server configurations tested in lab environments.",
                ]
            ),
            (
                "2.2 Storage Backend Configuration",
                [
                    "For AWS S3 storage, set storage_backend: s3 and provide bucket name, region, and "
                    "IAM role ARN. Cross-region replication should be enabled for disaster recovery. "
                    "S3 Transfer Acceleration is supported but adds approximately $0.04 per GB transferred.",

                    "Local SSD storage configuration requires specifying the mount point via "
                    "storage.local.data_path. Ensure the filesystem uses XFS with reflink support "
                    "disabled for best performance. Recommended inode ratio: 1 inode per 16 KB "
                    "(mkfs.xfs -i size=512 -n size=8192 /dev/nvme0n1).",

                    "Storage compression can reduce disk usage by 40-70% depending on data type. "
                    "LZ4 provides the best compression/speed tradeoff for time-series data. Zstandard "
                    "(zstd) level 3 is recommended for compliance archival workloads where storage "
                    "cost optimization outweighs CPU overhead concerns.",
                ]
            ),
            (
                "2.3 Network and Security Settings",
                [
                    "TLS encryption is mandatory for all inter-service communication in production. "
                    "Certificate rotation is automated via the built-in cert-manager integration. "
                    "Certificates are renewed 30 days before expiration by default. The renewal "
                    "window can be adjusted via security.cert_renewal_threshold_days.",

                    "mTLS (mutual TLS) authentication between ADPS components uses certificates issued "
                    "by the internal CA. The CA certificate must be deployed to all nodes before "
                    "starting the cluster. Use adps-pki init-ca to generate the CA and "
                    "adps-pki issue-cert --role <service_name> for individual service certificates.",
                ]
            ),
            (
                "2.4 Performance Tuning",
                [
                    "JVM heap sizing for Java-based components: allocate 50-70% of available RAM to "
                    "the heap. For a 64 GB node, set -Xms20g -Xmx40g. Use G1GC for heaps above 8 GB. "
                    "GC pause targets should be set to 200ms: -XX:MaxGCPauseMillis=200.",

                    "Linux kernel tuning: set transparent huge pages to madvise, disable NUMA "
                    "balancing for latency-sensitive workloads, and configure IRQ affinity to pin "
                    "network interrupts to a dedicated CPU core. These optimizations reduced 99th "
                    "percentile latency by 23% in production benchmarks at DataBridge Corp.",
                ]
            ),
        ]
    )

    # --- Create chapter3.pdf (3 pages) ---
    create_pdf_with_content(
        f'{DOCS_DIR}/chapter3.pdf',
        'Technical Documentation — Chapter 3: Operations',
        [
            (
                "3.1 Monitoring and Observability",
                [
                    "ADPS exposes Prometheus metrics on port 9090 (configurable). The Grafana dashboard "
                    "bundle is available at /opt/adps/grafana/dashboards/ and includes 14 pre-built "
                    "dashboards covering ingestion lag, transformation throughput, error rates, "
                    "and resource utilization.",

                    "Key SLI/SLO targets for production deployments: ingestion latency p99 < 500ms, "
                    "transformation throughput > 500K records/sec, end-to-end pipeline latency < 2s, "
                    "and error rate < 0.01%. Alerting rules are configured in "
                    "/etc/adps/alerting/rules.yaml and dispatched via PagerDuty integration.",

                    "Distributed tracing is available via OpenTelemetry. Enable it with "
                    "observability.tracing.enabled: true and configure the OTLP exporter endpoint. "
                    "Jaeger UI is the recommended trace visualization tool; the team at "
                    "NovaTech Solutions contributed the custom sampling strategy for burst traffic.",
                ]
            ),
            (
                "3.2 Backup and Recovery Procedures",
                [
                    "Full cluster backups must be performed daily. Use the adps-backup utility: "
                    "adps-backup create --type full --destination s3://backup-bucket/adps/daily/. "
                    "The backup includes all metadata, pipeline configurations, and recent WAL segments. "
                    "Backup duration for a typical production cluster is 15-45 minutes.",

                    "Point-in-time recovery (PITR) is supported for the metadata database. Continuous "
                    "WAL archiving must be enabled: set wal_archive_enabled: true in adps.yaml. "
                    "Recovery testing should be performed monthly by the operations team. The last "
                    "documented recovery drill achieved RTO of 18 minutes for a full cluster restore.",
                ]
            ),
            (
                "3.3 Upgrade Procedures",
                [
                    "Rolling upgrades are supported for minor and patch versions (e.g., 3.2.0 → 3.2.1). "
                    "Use the upgrade controller: adps-upgrade start --target-version 3.2.1 --strategy rolling. "
                    "The upgrade pauses ingestion briefly on each node; plan for 5-10% throughput reduction "
                    "during the upgrade window.",

                    "Major version upgrades (e.g., 3.x → 4.x) require a maintenance window and database "
                    "schema migration. Refer to the version-specific upgrade guide in the release notes. "
                    "Always test major upgrades in staging environments for at least 72 hours before "
                    "applying to production.",
                ]
            ),
        ]
    )

    # --- Create appendix.pdf (2 pages) ---
    create_pdf_with_content(
        f'{DOCS_DIR}/appendix.pdf',
        'Technical Documentation — Appendix',
        [
            (
                "Appendix A: Error Code Reference",
                [
                    "ADPS_E001 — Connection timeout: The source connector failed to establish a connection "
                    "within the configured timeout period (default: 30s). Check network connectivity, "
                    "firewall rules, and source system availability. Increase connection.timeout_ms if "
                    "the source system is under high load.",

                    "ADPS_E002 — Schema mismatch: The incoming record schema does not match the registered "
                    "schema version in the schema registry. This typically occurs after upstream schema "
                    "changes without a corresponding ADPS schema update. Run adps-schema update to "
                    "synchronize. Contact the data engineering team if auto-update fails.",

                    "ADPS_E003 — Storage write failure: The storage backend returned an error during write. "
                    "Common causes: disk full (check storage.local.data_path utilization), S3 permissions "
                    "denied (verify IAM role policy), or network partition. ADPS will retry with exponential "
                    "backoff up to 10 times before marking the batch as failed and alerting on-call.",

                    "ADPS_E004 — Transformation pipeline crash: An unhandled exception occurred in a "
                    "transformation function. Check the transformation worker logs at "
                    "/var/log/adps/transform-worker.log. Common root causes include null pointer "
                    "exceptions in custom UDFs, memory overflow for oversized batches, and version "
                    "conflicts in user-provided Python dependencies.",
                ]
            ),
            (
                "Appendix B: Glossary and References",
                [
                    "WAL (Write-Ahead Log): A durability mechanism where changes are written to a log "
                    "before being applied to the main data store. Ensures crash recovery and supports "
                    "point-in-time recovery scenarios in ADPS metadata database.",

                    "PITR (Point-in-Time Recovery): The ability to restore a database to any consistent "
                    "state between the last full backup and the current time, using continuous WAL "
                    "archiving. ADPS supports PITR with 1-second granularity.",

                    "RTO (Recovery Time Objective): The maximum acceptable time to restore a system "
                    "after a failure. ADPS targets RTO < 5 minutes for single-node failures and "
                    "< 30 minutes for full cluster recovery.",

                    "SLI/SLO: Service Level Indicator / Service Level Objective. Quantitative targets "
                    "defining acceptable service quality. ADPS SLOs are defined in the Service Agreement "
                    "document SVC-2024-042 maintained by the Platform Infrastructure team.",
                ]
            ),
        ]
    )

    # --- Create merge_list.txt ---
    merge_list_path = f'{DOCS_DIR}/merge_list.txt'
    with open(merge_list_path, 'w') as f:
        f.write('/home/user/Documents/intro.pdf\n')
        f.write('/home/user/Documents/chapter1.pdf\n')
        f.write('/home/user/Documents/chapter2.pdf\n')
        f.write('/home/user/Documents/chapter3.pdf\n')
        f.write('/home/user/Documents/appendix.pdf\n')
    print(f"  Created: {merge_list_path}")

    # Verify scripts directory exists (agent will create merge_pdfs.py there)
    print(f"  Scripts directory: {SCRIPTS_DIR} (exists: {os.path.isdir(SCRIPTS_DIR)})")

    # Confirm merged_output.pdf does NOT exist
    merged_path = f'{DOCS_DIR}/merged_output.pdf'
    if os.path.exists(merged_path):
        os.remove(merged_path)
        print(f"  Removed pre-existing: {merged_path}")

    # Confirm merge_pdfs.py does NOT exist
    script_path = f'{SCRIPTS_DIR}/merge_pdfs.py'
    if os.path.exists(script_path):
        os.remove(script_path)
        print(f"  Removed pre-existing: {script_path}")

    print("Initial files created successfully.")

    # GUI-ready startup: open VSCode in the scripts directory
    # Also open a terminal so the agent can run the script
    launch_gui(f'code "{SCRIPTS_DIR}"', delay_sec=3.0)
    launch_gui('bash -c "DISPLAY=:0 gnome-terminal -- bash"', delay_sec=1.5)
    print('GUI_READY: launched VSCode and gnome-terminal with DISPLAY=:0')


create_initial()
