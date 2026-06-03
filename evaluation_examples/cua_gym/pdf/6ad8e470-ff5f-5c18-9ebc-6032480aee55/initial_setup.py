"""
Initial Setup: Create an 8-page policy draft PDF with no annotations
Task ID: pdf_fm_042
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
TASK_ID = 'pdf_fm_042'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/policy_draft.pdf'

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

    # Page dimensions (Letter size)
    W, H = 612, 792

    # ----- Policy document content across 8 pages -----
    pages_content = [
        {
            "title": "Meridian Technologies Inc.",
            "subtitle": "Information Security Policy",
            "body": (
                "Document Reference: MT-ISP-2025-003\n"
                "Effective Date: March 1, 2025\n"
                "Review Date: March 1, 2026\n"
                "Classification: Internal Use Only\n\n"
                "This document establishes the information security policies and procedures "
                "for Meridian Technologies Inc. and all its subsidiaries. Compliance with this "
                "policy is mandatory for all employees, contractors, and third-party partners "
                "who access company information systems or handle sensitive data.\n\n"
                "Approved by: Dr. Elena Vasquez, Chief Information Security Officer\n"
                "Reviewed by: Board of Directors, January 15, 2025"
            ),
        },
        {
            "title": "1. Purpose and Scope",
            "body": (
                "1.1 Purpose\n\n"
                "The purpose of this Information Security Policy is to protect the confidentiality, "
                "integrity, and availability of all information assets owned by or entrusted to "
                "Meridian Technologies Inc. This policy provides a framework for establishing, "
                "implementing, maintaining, and continuously improving information security "
                "management across the organization.\n\n"
                "1.2 Scope\n\n"
                "This policy applies to:\n"
                "  - All employees (full-time, part-time, and temporary)\n"
                "  - Contractors, consultants, and third-party service providers\n"
                "  - All information systems, networks, and data repositories\n"
                "  - Physical and virtual infrastructure across all office locations\n"
                "  - Cloud-based services and applications used for business purposes\n\n"
                "1.3 Definitions\n\n"
                "Confidential Data: Information whose unauthorized disclosure could cause "
                "significant harm to the organization, including trade secrets, customer PII, "
                "financial records, and proprietary algorithms.\n\n"
                "Critical Systems: Infrastructure components whose failure would directly "
                "impact business operations, including production databases, authentication "
                "servers, and core networking equipment."
            ),
        },
        {
            "title": "2. Access Control",
            "body": (
                "2.1 Authentication Requirements\n\n"
                "All users must authenticate using multi-factor authentication (MFA) before "
                "accessing any company information system. Password requirements include:\n"
                "  - Minimum length: 14 characters\n"
                "  - Must include uppercase, lowercase, numbers, and special characters\n"
                "  - Password rotation: every 90 days\n"
                "  - No reuse of the last 12 passwords\n"
                "  - Account lockout after 5 failed attempts (30-minute cooldown)\n\n"
                "2.2 Role-Based Access Control (RBAC)\n\n"
                "Access to information systems shall be granted based on the principle of "
                "least privilege. Each employee is assigned a role that determines their "
                "access permissions. Access reviews are conducted quarterly by department "
                "managers in coordination with the IT Security team.\n\n"
                "2.3 Privileged Access Management\n\n"
                "Administrative and privileged accounts require additional controls:\n"
                "  - Separate credentials from standard user accounts\n"
                "  - Session recording for all privileged activities\n"
                "  - Just-in-time (JIT) access provisioning where possible\n"
                "  - Monthly review of all privileged account usage"
            ),
        },
        {
            "title": "3. Data Classification and Handling",
            "body": (
                "3.1 Classification Levels\n\n"
                "All data processed by Meridian Technologies must be classified into one of "
                "four categories:\n\n"
                "  Level 1 - Public: Information intended for public release. No special "
                "handling required.\n\n"
                "  Level 2 - Internal: General business information not intended for public "
                "disclosure. Standard access controls apply.\n\n"
                "  Level 3 - Confidential: Sensitive business data requiring restricted access. "
                "Encryption required at rest and in transit.\n\n"
                "  Level 4 - Restricted: Highly sensitive data including PII, financial records, "
                "and trade secrets. Maximum security controls enforced.\n\n"
                "3.2 Data Handling Procedures\n\n"
                "Data owners are responsible for classifying their data and ensuring appropriate "
                "handling procedures are followed. The Data Governance Committee, chaired by "
                "Chief Data Officer Marcus Thornton, reviews classification disputes quarterly."
            ),
        },
        {
            "title": "4. Incident Response",
            "body": (
                "4.1 Incident Classification\n\n"
                "Security incidents are classified by severity:\n\n"
                "  Critical (P1): Active data breach, ransomware attack, or compromise of "
                "production systems. Response time: 15 minutes. Escalation to CISO and "
                "executive leadership immediately.\n\n"
                "  High (P2): Detected intrusion attempt, malware infection on endpoints, "
                "or unauthorized access to confidential data. Response time: 1 hour.\n\n"
                "  Medium (P3): Phishing attempts, policy violations, suspicious activity "
                "on non-critical systems. Response time: 4 hours.\n\n"
                "  Low (P4): Minor policy deviations, informational alerts, false positives "
                "requiring documentation. Response time: 24 hours.\n\n"
                "4.2 Response Team\n\n"
                "The Computer Security Incident Response Team (CSIRT) consists of:\n"
                "  - Incident Commander: Sarah Kim, Director of Security Operations\n"
                "  - Technical Lead: James Okafor, Senior Security Engineer\n"
                "  - Communications: Patricia Reyes, VP of Corporate Communications\n"
                "  - Legal Counsel: Robert Chen, Associate General Counsel\n"
                "  - External Forensics: Contracted with CyberShield Partners LLC"
            ),
        },
        {
            "title": "5. Network Security",
            "body": (
                "5.1 Network Architecture\n\n"
                "The corporate network shall be segmented into distinct security zones:\n"
                "  - DMZ: Public-facing services (web servers, email gateways)\n"
                "  - Corporate Zone: Standard employee workstations and applications\n"
                "  - Restricted Zone: Financial systems and HR databases\n"
                "  - Development Zone: Software development and testing environments\n"
                "  - Management Zone: Network management and monitoring infrastructure\n\n"
                "5.2 Firewall and IDS/IPS Configuration\n\n"
                "All network traffic between zones must pass through next-generation firewalls "
                "with deep packet inspection enabled. Intrusion detection and prevention systems "
                "(IDS/IPS) monitor all inter-zone traffic with rule sets updated weekly.\n\n"
                "5.3 Remote Access\n\n"
                "Remote access to the corporate network is permitted only through the approved "
                "VPN solution with split-tunneling disabled. All VPN connections require MFA "
                "and are logged for audit purposes. Connection timeout: 8 hours maximum."
            ),
        },
        {
            "title": "6. Physical Security and Asset Management",
            "body": (
                "6.1 Physical Access Controls\n\n"
                "All Meridian Technologies facilities employ the following physical security measures:\n"
                "  - Badge-based access control at all entry points\n"
                "  - CCTV surveillance with 90-day retention\n"
                "  - Visitor registration and escort requirements\n"
                "  - Server rooms: biometric access + dual-person integrity\n"
                "  - Clean desk policy enforced during non-business hours\n\n"
                "6.2 Asset Management\n\n"
                "All company-owned devices must be registered in the IT Asset Management System "
                "(ITAMS). Asset inventory reconciliation is performed quarterly. Lost or stolen "
                "devices must be reported within 1 hour of discovery.\n\n"
                "6.3 Equipment Disposal\n\n"
                "End-of-life equipment containing storage media must be processed through "
                "the approved data destruction vendor. Hard drives are degaussed and physically "
                "shredded. SSDs undergo cryptographic erasure followed by physical destruction. "
                "Certificates of destruction are maintained for 7 years."
            ),
        },
        {
            "title": "7. Compliance and Enforcement",
            "body": (
                "7.1 Regulatory Compliance\n\n"
                "Meridian Technologies maintains compliance with the following standards:\n"
                "  - ISO 27001:2022 (Information Security Management)\n"
                "  - SOC 2 Type II (Service Organization Controls)\n"
                "  - GDPR (General Data Protection Regulation)\n"
                "  - CCPA (California Consumer Privacy Act)\n"
                "  - PCI DSS v4.0 (Payment Card Industry Data Security Standard)\n"
                "  - HIPAA (where applicable for healthcare client data)\n\n"
                "7.2 Policy Violations\n\n"
                "Violations of this policy may result in disciplinary action, up to and including "
                "termination of employment. Severity of consequences depends on:\n"
                "  - Nature and impact of the violation\n"
                "  - Whether the violation was intentional or negligent\n"
                "  - Prior history of policy non-compliance\n"
                "  - Degree of cooperation during investigation\n\n"
                "7.3 Policy Review\n\n"
                "This policy shall be reviewed annually by the Information Security Steering "
                "Committee and updated as necessary to address emerging threats and regulatory "
                "changes. Next scheduled review: January 2026.\n\n"
                "Document End - Meridian Technologies Inc. Confidential"
            ),
        },
    ]

    for i, page_data in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        y = 72  # start 1 inch from top

        # Title
        if i == 0:
            # Cover page - larger title
            page.insert_text(
                pymupdf.Point(72, y + 30),
                page_data["title"],
                fontsize=22,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            y += 60
            page.insert_text(
                pymupdf.Point(72, y + 20),
                page_data["subtitle"],
                fontsize=18,
                fontname="helv",
                color=(0.2, 0.2, 0.4),
            )
            y += 50
            # Horizontal rule
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(W - 72, y))
            shape.finish(color=(0.3, 0.3, 0.5), width=1.5)
            shape.commit()
            y += 20
        else:
            page.insert_text(
                pymupdf.Point(72, y + 16),
                page_data["title"],
                fontsize=16,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            y += 40

        # Body text in a textbox
        body_rect = pymupdf.Rect(72, y, W - 72, H - 72)
        page.insert_textbox(
            body_rect,
            page_data["body"],
            fontsize=10.5,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(W / 2 - 10, H - 40),
            f"Page {i + 1} of 8",
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
