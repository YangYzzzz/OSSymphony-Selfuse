"""
Initial Setup: Create a reviewed PDF document with interactive annotations
Task ID: pdf_gf2_042
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_042'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/reviewed_doc.pdf'


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
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page content for 8 pages of a realistic "reviewed" technical document ---

    page_contents = [
        # Page 1: Title page
        {
            "title": "Cloud Infrastructure Migration Plan",
            "subtitle": "Enterprise Architecture Division",
            "body": (
                "Prepared by: Elena Vasquez, Principal Architect\n"
                "Date: March 15, 2025\n"
                "Version: 2.4 (Under Review)\n"
                "Classification: Internal - Confidential\n\n"
                "This document outlines the phased migration strategy for transitioning "
                "legacy on-premises infrastructure to a hybrid cloud environment. "
                "The plan covers network topology redesign, data sovereignty compliance, "
                "application containerization, and rollback procedures."
            ),
        },
        # Page 2: Executive Summary
        {
            "title": "1. Executive Summary",
            "body": (
                "The current infrastructure supporting Meridian Financial Services operates "
                "across three data centers in Dallas, Frankfurt, and Singapore. Annual "
                "operational costs have reached $4.2M with a projected 18% year-over-year "
                "increase. Server utilization averages 23% during off-peak hours.\n\n"
                "This migration plan proposes a 14-month transition to AWS and Azure, "
                "targeting a 35% cost reduction while improving service availability from "
                "99.7% to 99.95%. The approach uses a lift-and-shift strategy for legacy "
                "applications and refactoring for customer-facing services.\n\n"
                "Key milestones include the Phase 1 pilot (Q2 2025), database migration "
                "(Q3 2025), and full production cutover (Q1 2026). Total estimated budget: "
                "$1.8M including contingency reserves."
            ),
        },
        # Page 3: Current Architecture
        {
            "title": "2. Current Architecture Assessment",
            "body": (
                "2.1 Hardware Inventory\n\n"
                "Dallas Data Center:\n"
                "  - 48 Dell PowerEdge R740xd servers (2019)\n"
                "  - 12 NetApp FAS8200 storage arrays\n"
                "  - Cisco Nexus 9000 series switches\n"
                "  - Total capacity: 2.4 PB raw storage\n\n"
                "Frankfurt Data Center:\n"
                "  - 32 HPE ProLiant DL380 Gen10 servers (2020)\n"
                "  - 8 Pure Storage FlashArray//X50\n"
                "  - Juniper QFX5200 switches\n"
                "  - Total capacity: 1.6 PB raw storage\n\n"
                "Singapore Data Center:\n"
                "  - 24 Lenovo ThinkSystem SR650 servers (2021)\n"
                "  - 6 Dell EMC PowerStore 500T\n"
                "  - Arista 7280R3 switches\n"
                "  - Total capacity: 960 TB raw storage\n\n"
                "2.2 Software Stack\n\n"
                "Production workloads include 147 applications spanning Java EE, .NET Framework, "
                "Python microservices, and legacy COBOL batch processing systems. Database tier "
                "consists of Oracle 19c, PostgreSQL 14, and MongoDB 6.0 clusters."
            ),
        },
        # Page 4: Migration Strategy
        {
            "title": "3. Migration Strategy",
            "body": (
                "3.1 Phase 1: Pilot Migration (Q2 2025)\n\n"
                "Selected workloads for the pilot phase:\n"
                "  - Internal HR portal (low risk, 200 users)\n"
                "  - Development/staging environments\n"
                "  - Non-critical reporting dashboards\n\n"
                "Target platform: AWS us-east-1 region\n"
                "Estimated duration: 6 weeks\n"
                "Success criteria: <50ms latency increase, zero data loss\n\n"
                "3.2 Phase 2: Database Migration (Q3 2025)\n\n"
                "Oracle-to-Aurora migration using AWS DMS with Change Data Capture. "
                "PostgreSQL clusters will use native logical replication for minimal "
                "downtime cutover. MongoDB will migrate to Atlas with oplog tailing.\n\n"
                "3.3 Phase 3: Application Refactoring (Q4 2025)\n\n"
                "Customer-facing applications will be containerized using Docker and "
                "orchestrated via Amazon EKS. API gateway migration from on-premises "
                "Kong to AWS API Gateway with custom Lambda authorizers."
            ),
        },
        # Page 5: Risk Assessment
        {
            "title": "4. Risk Assessment",
            "body": (
                "Risk ID  | Description                          | Likelihood | Impact  | Mitigation\n"
                "---------|--------------------------------------|-----------|---------|------------------\n"
                "R-001    | Data loss during migration            | Low       | Critical| Parallel run + backup\n"
                "R-002    | Extended downtime beyond window       | Medium    | High    | Rollback automation\n"
                "R-003    | GDPR compliance gap in transit        | Low       | Critical| Encrypted transfer\n"
                "R-004    | Application incompatibility           | Medium    | Medium  | Pre-migration testing\n"
                "R-005    | Cost overrun exceeding 20%            | Medium    | Medium  | Monthly budget reviews\n"
                "R-006    | Key personnel unavailability          | Low       | High    | Cross-training program\n"
                "R-007    | Vendor lock-in with single provider   | High      | Medium  | Multi-cloud strategy\n"
                "R-008    | Network latency for Singapore users   | Medium    | High    | CDN + edge deployment\n\n"
                "Overall risk rating: MODERATE\n"
                "The review committee recommends proceeding with enhanced monitoring "
                "during Phase 1 to validate latency and compliance assumptions."
            ),
        },
        # Page 6: Cost Analysis
        {
            "title": "5. Cost Analysis",
            "body": (
                "5.1 Current Annual Costs\n\n"
                "Category               | Annual Cost\n"
                "-----------------------|------------\n"
                "Hardware maintenance    | $890,000\n"
                "Data center leases     | $1,240,000\n"
                "Network bandwidth      | $380,000\n"
                "Staffing (ops team)    | $1,450,000\n"
                "Software licenses      | $240,000\n"
                "Total                  | $4,200,000\n\n"
                "5.2 Projected Cloud Costs (Year 1)\n\n"
                "Category               | Annual Cost\n"
                "-----------------------|------------\n"
                "AWS compute (EC2/EKS)  | $720,000\n"
                "Azure services         | $340,000\n"
                "Data transfer          | $180,000\n"
                "Managed databases      | $290,000\n"
                "Staffing (reduced)     | $980,000\n"
                "Migration project      | $1,800,000\n"
                "Total Year 1           | $4,310,000\n\n"
                "5.3 Projected Cloud Costs (Year 2+)\n\n"
                "Steady-state annual cost: $2,730,000 (35% reduction)\n"
                "Break-even point: Month 16 post-migration start"
            ),
        },
        # Page 7: Security & Compliance
        {
            "title": "6. Security and Compliance Framework",
            "body": (
                "6.1 Data Sovereignty Requirements\n\n"
                "European customer data must remain within EU boundaries per GDPR Article 44. "
                "The Frankfurt deployment will utilize AWS eu-central-1 and Azure Germany West "
                "Central regions exclusively for PII processing.\n\n"
                "6.2 Encryption Standards\n\n"
                "  - Data at rest: AES-256 with customer-managed keys (AWS KMS / Azure Key Vault)\n"
                "  - Data in transit: TLS 1.3 minimum, mutual TLS for service-to-service\n"
                "  - Database: Transparent Data Encryption (TDE) for Oracle and Aurora\n\n"
                "6.3 Access Control\n\n"
                "Migration from on-premises Active Directory to Azure AD with conditional access "
                "policies. Service accounts will use short-lived tokens via AWS STS and Azure "
                "Managed Identities. Privileged access requires MFA and just-in-time elevation.\n\n"
                "6.4 Audit Trail\n\n"
                "All infrastructure changes logged via AWS CloudTrail and Azure Monitor. "
                "SIEM integration with Splunk for real-time threat detection. Monthly "
                "compliance reports generated automatically for SOC 2 Type II certification."
            ),
        },
        # Page 8: Timeline & Approvals
        {
            "title": "7. Implementation Timeline and Approvals",
            "body": (
                "7.1 Key Milestones\n\n"
                "Date         | Milestone                        | Owner\n"
                "-------------|----------------------------------|------------------\n"
                "Apr 2025     | Architecture review complete      | Elena Vasquez\n"
                "May 2025     | Pilot environment provisioned     | DevOps Team\n"
                "Jun 2025     | Phase 1 pilot migration complete  | Migration Lead\n"
                "Aug 2025     | Database migration (Dallas)       | DBA Team\n"
                "Oct 2025     | Application refactoring complete  | Dev Team\n"
                "Dec 2025     | Security audit passed             | CISO Office\n"
                "Jan 2026     | Production cutover (Dallas)       | Ops Team\n"
                "Mar 2026     | Full migration complete           | Program Manager\n\n"
                "7.2 Required Approvals\n\n"
                "This document requires sign-off from:\n"
                "  - CTO: Marcus Chen\n"
                "  - CISO: Priya Sharma\n"
                "  - CFO: Robert Tanaka\n"
                "  - VP Engineering: David Okonkwo\n\n"
                "Status: PENDING REVIEW\n"
                "Review deadline: April 30, 2025"
            ),
        },
    ]

    # Create all 8 pages with content
    for i, content in enumerate(page_contents):
        page = doc.new_page(width=595, height=842)  # A4

        # Title
        page.insert_text(
            pymupdf.Point(72, 72),
            content["title"],
            fontsize=18 if i == 0 else 14,
            fontname="hebo",
            color=(0, 0, 0.5),
        )

        # Subtitle (page 1 only)
        y_start = 100
        if "subtitle" in content:
            page.insert_text(
                pymupdf.Point(72, 98),
                content["subtitle"],
                fontsize=13,
                fontname="heit",
                color=(0.3, 0.3, 0.3),
            )
            y_start = 130

        # Body text in a textbox
        rect = pymupdf.Rect(72, y_start, 523, 790)
        page.insert_textbox(
            rect,
            content["body"],
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
        )

    # --- Add 12 annotations across pages ---

    # 5 sticky notes
    sticky_notes = [
        (0, pymupdf.Point(500, 120), "Need to update version number before final submission."),
        (1, pymupdf.Point(500, 200), "Verify the 99.95% availability target with SRE team."),
        (2, pymupdf.Point(500, 350), "Check if Singapore hardware refresh is still on schedule."),
        (4, pymupdf.Point(500, 180), "Risk R-003 needs legal team confirmation on encryption approach."),
        (7, pymupdf.Point(500, 400), "CFO requested updated cost projections by April 15."),
    ]

    for page_num, point, content in sticky_notes:
        page = doc[page_num]
        annot = page.add_text_annot(point, content, icon="Note")
        annot.set_colors(stroke=(1, 0.8, 0))  # orange
        annot.update()

    # 4 highlight annotations
    highlights = [
        (1, "35% cost reduction"),
        (3, "zero data loss"),
        (5, "$2,730,000"),
        (6, "TLS 1.3 minimum"),
    ]

    for page_num, search_text in highlights:
        page = doc[page_num]
        instances = page.search_for(search_text)
        if instances:
            annot = page.add_highlight_annot(instances[0])
            annot.set_colors(stroke=(1, 1, 0))  # yellow highlight
            annot.update()

    # 3 freetext annotations
    freetext_annots = [
        (2, pymupdf.Rect(72, 750, 350, 780), "Reviewer: Consider consolidating Dallas and Frankfurt inventories."),
        (5, pymupdf.Rect(72, 750, 400, 780), "Reviewer: Year 1 costs seem high - need contingency breakdown."),
        (6, pymupdf.Rect(72, 750, 380, 780), "Reviewer: Add PCI-DSS compliance requirements for payment data."),
    ]

    for page_num, rect, text in freetext_annots:
        page = doc[page_num]
        annot = page.add_freetext_annot(
            rect,
            text,
            fontsize=9,
            fontname="helv",
            text_color=(0.8, 0, 0),
            fill_color=(1, 1, 0.85),
        )
        annot.update()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify annotation counts
    doc = pymupdf.open(OUTPUT)
    total_annots = 0
    for page in doc:
        annots = list(page.annots())
        total_annots += len(annots)
    doc.close()
    print(f'Total annotations in initial PDF: {total_annots}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
