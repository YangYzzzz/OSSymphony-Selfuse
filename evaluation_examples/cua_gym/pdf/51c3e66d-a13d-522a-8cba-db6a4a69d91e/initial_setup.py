"""
Initial Setup: Create a 30-page technical manual PDF with no bookmarks
Task ID: pdf_mbc_038
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_038'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/manual.pdf'

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

    # Page dimensions (Letter)
    W, H = 612, 792

    # Content structure for a realistic technical manual
    chapters = {
        1: ("Part I: Basics", "Chapter 1: Overview",
            "This chapter provides a comprehensive overview of the system architecture, "
            "core components, and fundamental concepts. Understanding these basics is essential "
            "before proceeding to installation and configuration."),
        8: (None, "Chapter 2: Setup",
            "This chapter walks through the complete setup process including system requirements, "
            "dependency installation, environment configuration, and initial verification steps."),
        15: ("Part II: Advanced", "Chapter 3: Customization",
             "This chapter covers advanced customization options including theme configuration, "
             "plugin development, API integrations, and workflow automation techniques."),
        22: (None, "Chapter 4: Troubleshooting",
             "This chapter addresses common issues and their resolutions, diagnostic tools, "
             "log analysis techniques, and escalation procedures for complex problems."),
    }

    filler_topics = [
        "System requirements specify a minimum of 8 GB RAM and 20 GB available disk space. "
        "A 64-bit operating system is required, with Ubuntu 22.04 LTS or later recommended.",

        "The configuration file is located at /etc/app/config.yaml. Key parameters include "
        "the database connection string, logging verbosity, and network interface bindings.",

        "Performance tuning involves adjusting thread pool sizes, cache expiration policies, "
        "and connection pooling parameters to match your workload characteristics.",

        "Security hardening includes enabling TLS 1.3, configuring certificate pinning, "
        "rotating API keys on a 90-day schedule, and implementing role-based access control.",

        "Backup procedures should run nightly using the integrated snapshot mechanism. "
        "Retention policy defaults to 30 days but can be extended for compliance needs.",

        "Monitoring dashboards display CPU utilization, memory consumption, request latency "
        "percentiles (p50, p95, p99), and error rates across all service endpoints.",

        "Database migration scripts are versioned and applied automatically during upgrades. "
        "Always create a backup before running migrations on production environments.",

        "Load balancing distributes incoming requests across healthy backend instances using "
        "round-robin scheduling with sticky session support for stateful workflows.",

        "Container orchestration with Kubernetes simplifies deployment, scaling, and "
        "management. Helm charts are provided for standard and high-availability configurations.",

        "API rate limiting protects backend services from overload. Default limits are "
        "1000 requests per minute per client, adjustable via the admin console.",

        "Plugin architecture allows extending core functionality without modifying source code. "
        "Plugins register lifecycle hooks and can expose custom REST endpoints.",

        "Audit logging captures all administrative actions with timestamps, user identities, "
        "and affected resources. Logs are immutable and forwarded to the SIEM system.",

        "Disaster recovery procedures include cross-region replication, automated failover "
        "detection, and runbook-driven restoration with target RTO of 15 minutes.",

        "Integration testing validates end-to-end workflows across service boundaries. "
        "The test harness provisions isolated environments and synthetic data sets.",

        "Release management follows semantic versioning. Major releases receive 18 months of "
        "support. Patch releases address critical security vulnerabilities within 48 hours.",

        "User management supports LDAP, SAML 2.0, and OpenID Connect for enterprise SSO. "
        "Local accounts are available for development and small-team deployments.",

        "Network topology requires outbound HTTPS access to the update server and telemetry "
        "endpoint. All internal service communication uses mutual TLS on port 8443.",

        "Storage backends include local filesystem, Amazon S3, Azure Blob Storage, and "
        "Google Cloud Storage. Object lifecycle policies automate tier transitions.",

        "Internationalization supports 24 languages with dynamic locale detection. "
        "Translation files follow the ICU MessageFormat standard.",

        "Accessibility compliance targets WCAG 2.1 Level AA. Automated scans run during "
        "CI builds and flag regressions before code merges.",

        "Command-line interface provides scriptable access to all platform capabilities. "
        "Output formats include JSON, YAML, and human-readable tables.",

        "Webhook notifications alert external systems on key events such as deployments, "
        "incidents, and configuration changes. Payload signing prevents tampering.",

        "Data export supports CSV, JSON Lines, and Parquet formats. Large exports run "
        "asynchronously and deliver results via a presigned download URL.",

        "Capacity planning tools project resource needs based on historical usage trends "
        "and configurable growth assumptions over 6, 12, and 24-month horizons.",

        "Service mesh integration with Istio provides advanced traffic management, "
        "circuit breaking, canary deployments, and distributed tracing with Jaeger.",
    ]

    for page_num in range(30):
        page = doc.new_page(width=W, height=H)
        pg = page_num + 1  # 1-indexed page number

        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 60), pymupdf.Point(W - 72, 60))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()

        # Header text
        page.insert_text(pymupdf.Point(72, 52), "Technical Reference Manual v3.2",
                         fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
        page.insert_text(pymupdf.Point(W - 120, 52), f"Page {pg}",
                         fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

        # Footer line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(72, H - 50), pymupdf.Point(W - 72, H - 50))
        shape2.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape2.commit()

        y = 90

        if pg in chapters:
            part_title, chapter_title, intro_text = chapters[pg]

            if part_title:
                # Part title
                page.insert_text(pymupdf.Point(72, y + 20), part_title,
                                 fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
                y += 50

            # Chapter title
            page.insert_text(pymupdf.Point(72, y + 20), chapter_title,
                             fontsize=18, fontname="hebo", color=(0.15, 0.15, 0.15))
            y += 45

            # Horizontal rule under chapter title
            shape3 = page.new_shape()
            shape3.draw_line(pymupdf.Point(72, y), pymupdf.Point(W - 72, y))
            shape3.finish(color=(0.2, 0.4, 0.7), width=1.5)
            shape3.commit()
            y += 20

            # Intro paragraph
            rect = pymupdf.Rect(72, y, W - 72, y + 80)
            page.insert_textbox(rect, intro_text, fontsize=11, fontname="helv",
                                color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 90
        else:
            # Section heading for non-chapter pages
            section_num = pg
            page.insert_text(pymupdf.Point(72, y + 15),
                             f"Section {section_num}",
                             fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))
            y += 40

        # Fill remaining space with realistic filler content
        filler_idx = page_num % len(filler_topics)
        paragraphs_to_add = 3 + (page_num % 3)

        for i in range(paragraphs_to_add):
            if y > H - 100:
                break
            text = filler_topics[(filler_idx + i) % len(filler_topics)]
            rect = pymupdf.Rect(72, y, W - 72, y + 70)
            page.insert_textbox(rect, text, fontsize=10, fontname="helv",
                                color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 78

    # Explicitly ensure NO bookmarks
    doc.set_toc([])

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify no bookmarks
    verify_doc = pymupdf.open(OUTPUT)
    toc = verify_doc.get_toc()
    print(f'Verification - Page count: {verify_doc.page_count}, Bookmarks: {len(toc)}')
    verify_doc.close()

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
