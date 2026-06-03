"""
Initial Setup: Create a password-protected PDF with specific permissions
Task ID: pdf_mbc_034
Domain: pdf

Creates ~/Secure/restricted_doc.pdf with:
- Owner password: ownerPW
- No user password
- Printing: allowed
- Copying: disallowed
- Modifying: disallowed
- Annotating: allowed
"""

import os
import shlex
import subprocess
import time
import pymupdf
import pikepdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_034'
SECURE_DIR = f'{WORKDIR}/Secure'
OUTPUT = f'{SECURE_DIR}/restricted_doc.pdf'
TEMP_PDF = f'{SECURE_DIR}/_temp_unencrypted.pdf'


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
    # Ensure directory exists
    os.makedirs(SECURE_DIR, exist_ok=True)

    # Step 1: Create a realistic multi-page PDF document using PyMuPDF
    doc = pymupdf.open()

    # --- Page 1: Cover page ---
    page1 = doc.new_page(width=612, height=792)  # Letter size
    # Title
    page1.insert_text(
        pymupdf.Point(72, 120),
        "CONFIDENTIAL",
        fontsize=14,
        fontname="hebo",
        color=(0.8, 0.0, 0.0),
    )
    page1.insert_text(
        pymupdf.Point(72, 180),
        "Meridian Technologies Inc.",
        fontsize=28,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )
    page1.insert_text(
        pymupdf.Point(72, 220),
        "Internal Security Audit Report",
        fontsize=18,
        fontname="heit",
        color=(0.2, 0.2, 0.2),
    )
    page1.insert_text(
        pymupdf.Point(72, 280),
        "Prepared by: Information Security Division",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(72, 300),
        "Report Date: March 15, 2025",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(72, 320),
        "Classification: Restricted Access Only",
        fontsize=12,
        fontname="hebo",
        color=(0.8, 0.0, 0.0),
    )

    # Horizontal rule
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 340), pymupdf.Point(540, 340))
    shape1.finish(color=(0.0, 0.15, 0.45), width=2)
    shape1.commit()

    page1.insert_textbox(
        pymupdf.Rect(72, 360, 540, 500),
        "This document contains proprietary information belonging to Meridian Technologies Inc. "
        "Unauthorized reproduction, distribution, or disclosure of this material is strictly prohibited. "
        "Access to this document is limited to authorized personnel with appropriate security clearance. "
        "Any breach of these restrictions will be subject to disciplinary action and potential legal proceedings.",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 2: Executive Summary ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 72),
        "1. Executive Summary",
        fontsize=18,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )

    summary_text = (
        "The Q1 2025 security audit of Meridian Technologies' infrastructure revealed "
        "a generally robust security posture with several areas requiring immediate attention. "
        "The audit covered 147 endpoints across 12 departments, evaluating network security, "
        "access controls, data protection protocols, and incident response capabilities.\n\n"
        "Key findings include:\n"
        "- 94% compliance rate with corporate security policies\n"
        "- 3 critical vulnerabilities identified in legacy systems\n"
        "- Employee phishing susceptibility reduced from 23% to 8% since last audit\n"
        "- Data encryption coverage increased to 99.2% across all storage systems\n"
        "- Two departments flagged for incomplete access review procedures\n\n"
        "Overall risk assessment: MODERATE. Remediation timeline for critical items: 30 days."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 100, 540, 500),
        summary_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 3: Findings Detail ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(
        pymupdf.Point(72, 72),
        "2. Detailed Findings",
        fontsize=18,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )

    findings_text = (
        "2.1 Network Infrastructure\n"
        "The perimeter firewall configuration was reviewed and found to be compliant with "
        "industry best practices. Internal segmentation between departments has been properly "
        "maintained. The VPN gateway showed no signs of unauthorized access attempts.\n\n"
        "2.2 Access Controls\n"
        "Multi-factor authentication (MFA) has been deployed across 98% of user accounts. "
        "The remaining 2% consist of legacy service accounts scheduled for migration in Q2 2025. "
        "Privileged access management (PAM) logs indicate proper rotation of administrative credentials.\n\n"
        "2.3 Data Protection\n"
        "All databases containing PII are encrypted at rest using AES-256. Transit encryption "
        "via TLS 1.3 is enforced on all internal and external communication channels. "
        "Backup integrity checks passed with 100% verification rate.\n\n"
        "2.4 Incident Response\n"
        "The mean time to detect (MTTD) security incidents improved from 4.2 hours to 1.8 hours. "
        "The security operations center (SOC) successfully handled 42 incidents during the audit period, "
        "with zero data breach events."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 100, 540, 700),
        findings_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 4: Recommendations ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(
        pymupdf.Point(72, 72),
        "3. Recommendations",
        fontsize=18,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )

    rec_text = (
        "Based on the findings of this audit, the following actions are recommended:\n\n"
        "Priority: CRITICAL\n"
        "- Patch CVE-2025-0142 on legacy application servers within 14 days\n"
        "- Upgrade the authentication module on the HR portal to eliminate SQL injection vector\n"
        "- Replace outdated SSL certificates on three internal web services\n\n"
        "Priority: HIGH\n"
        "- Complete MFA rollout for remaining 2% of service accounts\n"
        "- Implement network micro-segmentation for the R&D department\n"
        "- Update disaster recovery runbooks to reflect current infrastructure\n\n"
        "Priority: MEDIUM\n"
        "- Conduct refresher security training for Finance and Legal departments\n"
        "- Review and update data retention policies for archived project files\n"
        "- Deploy endpoint detection and response (EDR) on 12 newly provisioned workstations\n\n"
        "Next audit scheduled: July 2025"
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 100, 540, 650),
        rec_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Set metadata
    doc.set_metadata({
        "title": "Internal Security Audit Report - Q1 2025",
        "author": "Information Security Division",
        "subject": "Security Audit",
        "keywords": "security, audit, confidential, restricted",
        "creator": "Meridian Technologies Inc.",
    })

    # Add TOC
    toc = [
        [1, "Executive Summary", 2],
        [1, "Detailed Findings", 3],
        [2, "Network Infrastructure", 3],
        [2, "Access Controls", 3],
        [2, "Data Protection", 3],
        [2, "Incident Response", 3],
        [1, "Recommendations", 4],
    ]
    doc.set_toc(toc)

    # Save unencrypted temp file
    doc.save(TEMP_PDF)
    doc.close()
    print(f'Temporary unencrypted PDF created: {TEMP_PDF}')

    # Step 2: Encrypt with pikepdf - owner password, no user password
    # Permissions: printing=allowed, copying=disallowed, modifying=disallowed, annotating=allowed
    pdf = pikepdf.open(TEMP_PDF)
    pdf.save(
        OUTPUT,
        encryption=pikepdf.Encryption(
            owner="ownerPW",
            user="",            # no user password (can open without password)
            R=6,                # AES-256
            allow=pikepdf.Permissions(
                print_lowres=True,
                print_highres=True,
                extract=False,           # copying disallowed
                modify_other=False,      # modifying disallowed
                modify_annotation=True,  # annotating allowed
                modify_form=True,        # form filling allowed (part of annotation)
                modify_assembly=False,   # page assembly disallowed
            ),
        ),
    )
    pdf.close()
    print(f'Encrypted PDF created: {OUTPUT}')

    # Remove temp file
    os.remove(TEMP_PDF)

    # Step 3: Launch Evince to open the PDF for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

    # Also open a terminal for the agent to use Python
    launch_gui('bash -c "cd /home/user/Secure && exec bash"', delay_sec=1.0)


create_initial()
