"""
Initial Setup: Create a multi-page PDF with structural issues for validation
Task ID: pdf_cr_045
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'pdf_cr_045'
OUTPUT = f'{DESKTOP}/report.pdf'


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
    os.makedirs(DESKTOP, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title Page (A4) ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(150, 200),
        "Quarterly Infrastructure Review",
        fontsize=24,
        fontname="hebo",
        color=(0, 0, 0.4),
    )
    page.insert_text(
        pymupdf.Point(150, 260),
        "Prepared by: Network Operations Division",
        fontsize=14,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(150, 290),
        "Date: March 15, 2025",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(150, 320),
        "Classification: Internal Use Only",
        fontsize=11,
        fontname="heit",
        color=(0.5, 0.0, 0.0),
    )

    # --- Page 2: Executive Summary (A4) ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(72, 72),
        "1. Executive Summary",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )
    summary_text = (
        "During Q1 2025, the infrastructure team completed 94% of planned maintenance "
        "windows without service disruption. Total uptime across all critical systems "
        "averaged 99.97%, exceeding our SLA target of 99.95%. Three major incidents were "
        "recorded, all resolved within the 4-hour response window. The primary data center "
        "in Austin processed 2.3 billion API requests, a 17% increase over Q4 2024. "
        "Storage utilization reached 78% capacity, triggering the planned expansion "
        "initiative scheduled for Q2. Network latency between regions remained below "
        "the 45ms threshold, with an average of 31ms for cross-region calls."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 523, 400),
        summary_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(
        pymupdf.Point(72, 430),
        "Key Metrics:",
        fontsize=13,
        fontname="hebo",
        color=(0, 0, 0),
    )
    metrics = [
        "  - System Uptime: 99.97%",
        "  - API Requests Processed: 2.3 billion",
        "  - Incident Response Time (avg): 1h 42m",
        "  - Storage Utilization: 78%",
        "  - Network Latency (avg): 31ms",
        "  - Completed Maintenance Windows: 47/50",
    ]
    y = 455
    for line in metrics:
        page.insert_text(
            pymupdf.Point(72, y),
            line,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
        )
        y += 18

    # --- Page 3: Incident Report (A4) ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(72, 72),
        "2. Incident Report",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )
    incidents = [
        ("INC-2025-0041", "Jan 12", "Database failover triggered during peak load",
         "Resolved", "2h 15m"),
        ("INC-2025-0058", "Feb 03", "CDN cache invalidation caused 502 errors",
         "Resolved", "0h 47m"),
        ("INC-2025-0073", "Mar 08", "Authentication service timeout in EU region",
         "Resolved", "3h 22m"),
    ]
    y = 110
    for inc_id, date, desc, status, duration in incidents:
        page.insert_text(
            pymupdf.Point(72, y),
            f"{inc_id} ({date})",
            fontsize=12,
            fontname="hebo",
            color=(0.1, 0.1, 0.1),
        )
        y += 18
        page.insert_text(
            pymupdf.Point(90, y),
            f"Description: {desc}",
            fontsize=10,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )
        y += 16
        page.insert_text(
            pymupdf.Point(90, y),
            f"Status: {status} | Resolution Time: {duration}",
            fontsize=10,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )
        y += 28

    # --- Page 4: BLANK PAGE (intentional structural issue) ---
    page = doc.new_page(width=595, height=842)
    # This page is intentionally left blank - no text, no images

    # --- Page 5: Capacity Planning (LETTER SIZE - intentional inconsistent dimension) ---
    page = doc.new_page(width=612, height=792)  # US Letter instead of A4
    page.insert_text(
        pymupdf.Point(72, 72),
        "3. Capacity Planning",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )
    capacity_text = (
        "Current storage allocation stands at 78% across all data centers. "
        "The Austin facility is projected to reach 90% by end of Q2 2025 if "
        "current growth rates continue. The Chicago backup site has 340TB of "
        "available capacity. We recommend provisioning an additional 500TB at "
        "the Austin facility and upgrading the Chicago-Austin replication link "
        "from 10Gbps to 40Gbps to accommodate the projected data growth."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 350),
        capacity_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    # Add a table-like structure
    page.insert_text(pymupdf.Point(72, 380), "Data Center Capacity Overview:",
                     fontsize=12, fontname="hebo", color=(0, 0, 0))
    table_lines = [
        "  Location        Allocated    Used     Available    Utilization",
        "  Austin           1,200 TB    936 TB    264 TB       78.0%",
        "  Chicago            800 TB    412 TB    388 TB       51.5%",
        "  Frankfurt          600 TB    498 TB    102 TB       83.0%",
        "  Singapore          400 TB    287 TB    113 TB       71.8%",
    ]
    y = 405
    for line in table_lines:
        page.insert_text(pymupdf.Point(72, y), line, fontsize=10,
                         fontname="cour", color=(0, 0, 0))
        y += 16

    # --- Page 6: Security Assessment (A4) ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(72, 72),
        "4. Security Assessment",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )
    security_text = (
        "The quarterly vulnerability scan identified 12 critical, 45 high, and "
        "183 medium-severity findings across the production environment. All critical "
        "vulnerabilities were patched within the 72-hour SLA. The penetration test "
        "conducted by Meridian Security Partners on February 20-24 found no exploitable "
        "paths to customer data. Two recommendations were issued regarding TLS configuration "
        "on legacy API endpoints, both scheduled for remediation in Sprint 14."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 100, 523, 350),
        security_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 7: Recommendations (A4) ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(72, 72),
        "5. Recommendations",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )
    recommendations = [
        "1. Provision 500TB additional storage at Austin data center by end of Q2.",
        "2. Upgrade Chicago-Austin replication link to 40Gbps.",
        "3. Remediate legacy TLS configurations on API endpoints (Sprint 14).",
        "4. Implement automated failover testing for database clusters.",
        "5. Expand CDN edge locations to reduce latency in APAC region.",
        "6. Review and update incident response runbooks for authentication services.",
        "7. Begin procurement for Frankfurt facility expansion (projected Q3 need).",
    ]
    y = 110
    for rec in recommendations:
        page.insert_text(
            pymupdf.Point(72, y),
            rec,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
        )
        y += 22

    # Set metadata
    doc.set_metadata({
        "title": "Quarterly Infrastructure Review - Q1 2025",
        "author": "Network Operations Division",
        "subject": "Infrastructure Performance and Planning",
        "keywords": "infrastructure, quarterly, review, 2025, Q1",
        "creator": "Internal Report Generator",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
