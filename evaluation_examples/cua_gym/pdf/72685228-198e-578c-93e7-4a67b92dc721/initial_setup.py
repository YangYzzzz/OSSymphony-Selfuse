"""
Initial Setup: Create a non-linearized ~200-page technical manual PDF
Task ID: pdf_mbc_026
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
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/large_manual.pdf'


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


def create_manual():
    """Create a realistic ~200-page non-linearized technical manual."""
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (US Letter)
    W, H = 612, 792
    MARGIN = 72  # 1 inch
    TEXT_W = W - 2 * MARGIN

    # Chapters for a technical manual
    chapters = [
        ("Chapter 1: System Overview", [
            "1.1 Introduction to the Platform",
            "1.2 Architecture Components",
            "1.3 Deployment Models",
            "1.4 Hardware Requirements",
            "1.5 Software Prerequisites",
            "1.6 Network Topology",
            "1.7 Security Architecture",
            "1.8 High Availability Design",
        ]),
        ("Chapter 2: Installation Guide", [
            "2.1 Pre-Installation Checklist",
            "2.2 Operating System Setup",
            "2.3 Database Configuration",
            "2.4 Application Server Deployment",
            "2.5 Load Balancer Setup",
            "2.6 SSL Certificate Installation",
            "2.7 Post-Installation Verification",
            "2.8 Troubleshooting Installation Issues",
        ]),
        ("Chapter 3: Configuration Reference", [
            "3.1 Global Configuration Parameters",
            "3.2 Database Connection Settings",
            "3.3 Authentication and Authorization",
            "3.4 Logging and Monitoring",
            "3.5 Performance Tuning",
            "3.6 Cache Configuration",
            "3.7 Email and Notification Settings",
            "3.8 API Gateway Configuration",
        ]),
        ("Chapter 4: User Management", [
            "4.1 User Roles and Permissions",
            "4.2 Creating User Accounts",
            "4.3 Group Management",
            "4.4 Single Sign-On Integration",
            "4.5 Multi-Factor Authentication",
            "4.6 Password Policies",
            "4.7 Session Management",
            "4.8 Audit Trail and Compliance",
        ]),
        ("Chapter 5: Data Management", [
            "5.1 Data Import Procedures",
            "5.2 Export and Reporting",
            "5.3 Backup and Recovery",
            "5.4 Data Retention Policies",
            "5.5 Database Maintenance",
            "5.6 Data Migration Strategies",
            "5.7 Archival Procedures",
            "5.8 Data Integrity Checks",
        ]),
        ("Chapter 6: API Reference", [
            "6.1 REST API Overview",
            "6.2 Authentication Endpoints",
            "6.3 Resource Management Endpoints",
            "6.4 Query and Search API",
            "6.5 Webhook Configuration",
            "6.6 Rate Limiting and Throttling",
            "6.7 Error Handling",
            "6.8 SDK Integration Guide",
        ]),
        ("Chapter 7: Monitoring and Diagnostics", [
            "7.1 System Health Dashboard",
            "7.2 Performance Metrics",
            "7.3 Log Analysis",
            "7.4 Alert Configuration",
            "7.5 Capacity Planning",
            "7.6 Incident Response Procedures",
            "7.7 Root Cause Analysis Tools",
            "7.8 Reporting and SLA Tracking",
        ]),
        ("Chapter 8: Troubleshooting Guide", [
            "8.1 Common Error Messages",
            "8.2 Connection Issues",
            "8.3 Performance Degradation",
            "8.4 Data Synchronization Problems",
            "8.5 Authentication Failures",
            "8.6 Memory and Resource Issues",
            "8.7 Network Connectivity Problems",
            "8.8 Recovery Procedures",
        ]),
        ("Chapter 9: Advanced Topics", [
            "9.1 Custom Plugin Development",
            "9.2 Workflow Automation",
            "9.3 Integration Patterns",
            "9.4 Clustering and Scaling",
            "9.5 Disaster Recovery Planning",
            "9.6 Compliance and Regulatory Requirements",
            "9.7 Performance Benchmarking",
            "9.8 Migration from Legacy Systems",
        ]),
        ("Chapter 10: Appendices", [
            "10.1 Glossary of Terms",
            "10.2 Configuration Parameter Reference",
            "10.3 Error Code Reference",
            "10.4 Command-Line Interface Reference",
            "10.5 Third-Party Licenses",
            "10.6 Release Notes",
            "10.7 Change Log",
            "10.8 Contact and Support",
        ]),
    ]

    # Sample paragraph text for filling pages
    paragraphs = [
        "The enterprise platform provides a comprehensive solution for managing distributed workloads across "
        "multiple data centers. The architecture is designed to support horizontal scaling with automatic failover "
        "and load balancing capabilities. Each component in the system communicates through a secure message bus "
        "that ensures data integrity and reliable delivery of messages between services.",

        "Configuration management is handled through a centralized configuration server that distributes settings "
        "to all nodes in the cluster. Changes to configuration parameters are propagated in real-time without "
        "requiring service restarts. The configuration system supports versioning, rollback, and environment-specific "
        "overrides to facilitate development, staging, and production deployments.",

        "The monitoring subsystem collects metrics from all running services at configurable intervals. These "
        "metrics are stored in a time-series database optimized for high-throughput writes and efficient range "
        "queries. Dashboards provide real-time visibility into system health, performance trends, and capacity "
        "utilization across all infrastructure components.",

        "Security is enforced at multiple layers including network perimeter controls, application-level "
        "authentication, and data encryption both in transit and at rest. The platform supports integration with "
        "enterprise identity providers through SAML 2.0 and OAuth 2.0 protocols. All administrative actions are "
        "logged to an immutable audit trail for compliance and forensic analysis.",

        "Data management capabilities include automated backup scheduling with configurable retention policies, "
        "point-in-time recovery for database systems, and cross-region replication for disaster recovery scenarios. "
        "The backup system supports incremental and differential backup strategies to minimize storage requirements "
        "and reduce backup windows.",

        "The API gateway serves as the single entry point for all client requests, providing request routing, "
        "protocol translation, and rate limiting. The gateway supports OpenAPI 3.0 specification for automatic "
        "documentation generation and client SDK creation. Response caching at the gateway level reduces backend "
        "load and improves response times for frequently accessed resources.",

        "Performance tuning involves adjusting thread pool sizes, connection pool limits, memory allocation, and "
        "garbage collection parameters. The platform includes built-in profiling tools that identify bottlenecks "
        "and suggest optimization strategies. Benchmark tests should be conducted under realistic load conditions "
        "to validate performance improvements before deploying to production.",

        "Troubleshooting complex issues often requires correlating events across multiple system components. The "
        "distributed tracing system assigns unique trace identifiers to each request, allowing engineers to follow "
        "the complete path of a transaction through the system. Trace data is enriched with timing information, "
        "error details, and contextual metadata to accelerate root cause analysis.",
    ]

    page_count = 0

    # Title page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, 280), "ENTERPRISE PLATFORM", fontsize=28, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(MARGIN, 330), "Technical Reference Manual", fontsize=20, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(MARGIN, 380), "Version 4.2.1", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(MARGIN, 420), "Revision Date: March 15, 2025", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(MARGIN, 460), "Prepared by: Systems Engineering Division", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(MARGIN, 490), "Document Classification: Internal Use Only", fontsize=10, fontname="heit", color=(0.5, 0.5, 0.5))
    page_count += 1

    # Table of contents page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "TABLE OF CONTENTS", fontsize=18, fontname="hebo", color=(0, 0, 0))
    y = MARGIN + 60
    for ch_title, sections in chapters:
        page.insert_text(pymupdf.Point(MARGIN, y), ch_title, fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 18
        for sec in sections:
            page.insert_text(pymupdf.Point(MARGIN + 20, y), sec, fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 14
            if y > H - MARGIN - 20:
                page = doc.new_page(width=W, height=H)
                page_count += 1
                y = MARGIN + 20
        y += 8
    page_count += 1

    # Generate chapter content
    para_idx = 0
    for ch_idx, (ch_title, sections) in enumerate(chapters):
        # Chapter title page
        page = doc.new_page(width=W, height=H)
        page_count += 1

        # Draw a line under the chapter title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN, MARGIN + 40), pymupdf.Point(W - MARGIN, MARGIN + 40))
        shape.finish(color=(0, 0, 0.5), width=2)
        shape.commit()

        page.insert_text(pymupdf.Point(MARGIN, MARGIN + 30), ch_title, fontsize=22, fontname="hebo", color=(0, 0, 0.5))
        y_pos = MARGIN + 70

        for sec_idx, section in enumerate(sections):
            # Section heading
            if y_pos > H - MARGIN - 100:
                page = doc.new_page(width=W, height=H)
                page_count += 1
                y_pos = MARGIN + 20

            page.insert_text(pymupdf.Point(MARGIN, y_pos), section, fontsize=14, fontname="hebo", color=(0, 0, 0))
            y_pos += 28

            # Add 2-4 paragraphs per section
            num_paras = 2 + (sec_idx % 3)
            for p in range(num_paras):
                text = paragraphs[para_idx % len(paragraphs)]
                para_idx += 1

                rect = pymupdf.Rect(MARGIN, y_pos, W - MARGIN, H - MARGIN)
                excess = page.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

                # Estimate lines used (rough: ~80 chars per line at fontsize 10 on letter)
                chars_per_line = int(TEXT_W / (10 * 0.5))
                num_lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
                y_pos += num_lines * 14 + 10

                if y_pos > H - MARGIN - 60:
                    page = doc.new_page(width=W, height=H)
                    page_count += 1
                    y_pos = MARGIN + 20

            y_pos += 10

    # Pad to reach ~200 pages with additional reference content
    while page_count < 200:
        page = doc.new_page(width=W, height=H)
        page_count += 1

        # Header
        page.insert_text(pymupdf.Point(MARGIN, MARGIN + 15), "Appendix: Configuration Parameter Reference",
                        fontsize=12, fontname="hebo", color=(0, 0, 0))

        # Page number footer
        page.insert_text(pymupdf.Point(W / 2 - 10, H - MARGIN / 2),
                        f"Page {page_count}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

        y = MARGIN + 40
        # Fill with configuration parameter entries
        param_prefixes = ["server", "database", "cache", "auth", "logging", "network", "api", "queue", "storage", "monitor"]
        param_suffixes = ["timeout", "max_connections", "buffer_size", "retry_count", "interval",
                         "threshold", "port", "host", "enabled", "level"]

        for i in range(15):
            if y > H - MARGIN - 50:
                break
            prefix = param_prefixes[(page_count + i) % len(param_prefixes)]
            suffix = param_suffixes[(page_count + i) % len(param_suffixes)]
            param_name = f"{prefix}.{suffix}"
            page.insert_text(pymupdf.Point(MARGIN, y), param_name, fontsize=10, fontname="cobo", color=(0, 0, 0.4))
            y += 14
            desc = f"Controls the {suffix.replace('_', ' ')} setting for the {prefix} subsystem. Default value depends on deployment configuration."
            page.insert_textbox(pymupdf.Rect(MARGIN + 20, y, W - MARGIN, y + 30), desc,
                              fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 35

    # Set metadata
    doc.set_metadata({
        "title": "Enterprise Platform Technical Reference Manual",
        "author": "Systems Engineering Division",
        "subject": "Technical Documentation",
        "keywords": "enterprise, platform, technical, manual, reference",
        "creator": "Documentation Team",
        "producer": "PyMuPDF",
    })

    # Build table of contents bookmarks
    toc = []
    pg = 3  # chapters start after title + TOC pages
    for ch_idx, (ch_title, sections) in enumerate(chapters):
        toc.append([1, ch_title, pg])
        for sec in sections:
            toc.append([2, sec, pg])
        pg += 2 + len(sections)  # rough estimate
        pg = min(pg, doc.page_count)
    doc.set_toc(toc)

    # Save WITHOUT linearization (important - this must be non-linearized)
    doc.save(OUTPUT, deflate=True, garbage=3)
    doc.close()

    print(f"Initial file created: {OUTPUT}")
    print(f"Total pages: {page_count}")


create_manual()

# Open a terminal for the user (task requires using qpdf from command line)
launch_gui('bash -c "cd /home/user/Documents && exec gnome-terminal"', delay_sec=2.0)
print("GUI_READY: launched terminal with DISPLAY=:0")
