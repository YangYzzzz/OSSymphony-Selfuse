"""
Initial Setup: PDF Security Audit Tool
Task ID: pdf_gf3_030
Domain: pdf

Creates a 20-page PDF with various security settings:
- AES-256 encryption with owner/user passwords
- Permission flags restricting copy and modify
- Embedded JavaScript annotations
- Embedded file attachments
- External URL links
- Metadata (Author, Creator, Producer)

Also creates directory structure and opens a terminal for the agent.
"""

import os
import shlex
import subprocess
import time
import json
import tempfile

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_030'
AUDIT_DIR = f'{WORKDIR}/audit'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
PDF_PATH = f'{AUDIT_DIR}/sensitive_document.pdf'


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
    # Create directories
    os.makedirs(AUDIT_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # --- Step 1: Create a 20-page PDF with rich content using PyMuPDF ---
    import pymupdf

    doc = pymupdf.open()

    # Page 1: Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 100), "CONFIDENTIAL", fontsize=36, fontname="hebo", color=(0.7, 0, 0))
    page.insert_text(pymupdf.Point(72, 160), "Vendor Security Assessment Report", fontsize=24, fontname="hebo", color=(0, 0, 0.4))
    page.insert_text(pymupdf.Point(72, 200), "Prepared for: Meridian Financial Group", fontsize=14, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 225), "Prepared by: CyberShield Analytics LLC", fontsize=14, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 250), "Date: March 15, 2025", fontsize=14, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 275), "Classification: Restricted - Internal Use Only", fontsize=12, fontname="heit", color=(0.5, 0, 0))
    page.insert_text(pymupdf.Point(72, 320), "Document ID: VSA-2025-MFG-0042", fontsize=11, fontname="cour", color=(0.3, 0.3, 0.3))

    # Add an external URL link on page 1
    link_rect = pymupdf.Rect(72, 380, 350, 400)
    page.insert_text(pymupdf.Point(72, 395), "Visit our portal: https://portal.cybershield-analytics.com", fontsize=10, fontname="helv", color=(0, 0, 0.8))
    page.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": "https://portal.cybershield-analytics.com"})

    # Page 2: Table of Contents
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 80), "Table of Contents", fontsize=20, fontname="hebo", color=(0, 0, 0.4))
    toc_items = [
        "1. Executive Summary .......................... 3",
        "2. Scope of Assessment ........................ 4",
        "3. Methodology ............................... 5",
        "4. Network Infrastructure Review .............. 6",
        "5. Application Security Findings .............. 8",
        "6. Data Protection Analysis ................... 10",
        "7. Access Control Evaluation .................. 12",
        "8. Incident Response Capabilities ............. 14",
        "9. Compliance Status .......................... 16",
        "10. Risk Matrix & Recommendations ............. 18",
        "11. Appendices ................................ 20",
    ]
    for i, item in enumerate(toc_items):
        page.insert_text(pymupdf.Point(90, 130 + i * 28), item, fontsize=12, fontname="helv", color=(0, 0, 0))

    # Pages 3-20: Content pages with various sections
    sections = [
        ("Executive Summary", [
            "This report presents the findings of a comprehensive security assessment conducted",
            "on Meridian Financial Group's vendor infrastructure between February 1-28, 2025.",
            "",
            "Key findings include 3 critical vulnerabilities in the payment processing gateway,",
            "5 high-severity issues in the customer data handling pipeline, and 12 medium-risk",
            "configuration weaknesses across the network perimeter.",
            "",
            "Overall Risk Rating: HIGH",
            "",
            "The assessment team recommends immediate remediation of critical findings within",
            "30 days and high-severity findings within 60 days. A follow-up assessment is",
            "recommended for Q3 2025 to verify remediation effectiveness.",
        ]),
        ("Scope of Assessment", [
            "The assessment covered the following systems and networks:",
            "",
            "- External-facing web applications (portal.meridianfg.com, api.meridianfg.com)",
            "- Internal network segments (10.10.0.0/16, 172.16.0.0/12)",
            "- Database clusters (PostgreSQL 15.2, MongoDB 6.0)",
            "- Cloud infrastructure (AWS us-east-1, eu-west-1 regions)",
            "- VPN concentrators and remote access systems",
            "- Email gateway and DLP systems",
            "",
            "Out of scope: Physical security, employee devices, third-party SaaS applications.",
        ]),
        ("Methodology", [
            "The assessment followed the OWASP Testing Guide v4.2 and NIST SP 800-115.",
            "",
            "Phase 1: Reconnaissance and Information Gathering (Feb 1-5)",
            "Phase 2: Vulnerability Scanning and Enumeration (Feb 6-12)",
            "Phase 3: Manual Penetration Testing (Feb 13-21)",
            "Phase 4: Analysis and Report Generation (Feb 22-28)",
            "",
            "Tools used: Nmap 7.94, Burp Suite Professional 2024.1, Metasploit 6.3,",
            "SQLMap 1.8, Nuclei 3.1, custom Python scripts for API testing.",
        ]),
        ("Network Infrastructure Review", [
            "4.1 Firewall Configuration",
            "The perimeter firewall (Palo Alto PA-5260) was found to have 47 overly permissive",
            "rules allowing traffic from ANY source to internal servers on ports 8080, 8443.",
            "",
            "4.2 Network Segmentation",
            "Critical finding: The payment processing VLAN (VLAN 100) is not properly isolated",
            "from the general employee network (VLAN 10). Lateral movement was demonstrated.",
            "",
            "4.3 DNS Security",
            "DNSSEC is not enabled for meridianfg.com. SPF/DKIM/DMARC partially configured.",
        ]),
        ("Network Infrastructure Review (cont.)", [
            "4.4 Wireless Security",
            "WPA3-Enterprise deployed on corporate SSID. Guest network properly isolated.",
            "",
            "4.5 Load Balancer Configuration",
            "F5 BIG-IP running version 17.1.0 - CVE-2023-46747 not patched (CRITICAL).",
            "TLS 1.0 and 1.1 still enabled on the external VIP for legacy compatibility.",
            "",
            "Recommendation: Upgrade to 17.1.1.3 immediately. Disable TLS < 1.2.",
        ]),
        ("Application Security Findings", [
            "5.1 Payment Gateway (pay.meridianfg.com)",
            "- SQL Injection in /api/v2/transactions endpoint (CRITICAL)",
            "- Broken authentication on admin panel - default credentials active (CRITICAL)",
            "- Missing rate limiting on login endpoint (HIGH)",
            "",
            "5.2 Customer Portal (portal.meridianfg.com)",
            "- Stored XSS in profile update functionality (HIGH)",
            "- IDOR vulnerability in document download endpoint (HIGH)",
            "- Missing Content-Security-Policy header (MEDIUM)",
        ]),
        ("Application Security Findings (cont.)", [
            "5.3 API Gateway (api.meridianfg.com)",
            "- JWT secret key is a weak 8-character string (HIGH)",
            "- API versioning exposes deprecated v1 endpoints with known vulns (MEDIUM)",
            "- Verbose error messages leak stack traces in production (MEDIUM)",
            "",
            "5.4 Internal Tools (tools.internal.meridianfg.com)",
            "- Jenkins instance accessible without authentication (HIGH)",
            "- Grafana dashboard with default admin/admin credentials (MEDIUM)",
            "- Outdated Kibana 7.10 with known CVEs (MEDIUM)",
        ]),
        ("Data Protection Analysis", [
            "6.1 Data Classification",
            "PII fields (SSN, DOB, account numbers) found in 14 database tables.",
            "Only 3 of 14 tables implement column-level encryption.",
            "",
            "6.2 Data in Transit",
            "TLS 1.2+ enforced on external connections. Internal services use mTLS.",
            "Exception: Legacy batch processing system uses unencrypted FTP (CRITICAL).",
            "",
            "6.3 Data at Rest",
            "AWS S3 buckets: 2 of 8 have server-side encryption disabled (HIGH).",
            "Database encryption: AES-256-GCM for PostgreSQL, none for MongoDB (HIGH).",
        ]),
        ("Data Protection Analysis (cont.)", [
            "6.4 Data Retention",
            "No automated data retention policy. Transaction logs dating back to 2018.",
            "Customer PII retained indefinitely after account closure - violates GDPR Art. 17.",
            "",
            "6.5 Backup Security",
            "Database backups stored in S3 with cross-region replication. Encrypted at rest.",
            "Backup restoration tested quarterly - last successful test: January 2025.",
            "",
            "Recommendation: Implement automated data lifecycle management. Purge records",
            "exceeding retention requirements. Enable encryption on all data stores.",
        ]),
        ("Access Control Evaluation", [
            "7.1 Identity Management",
            "Okta SSO deployed for 92% of applications. MFA enforced for external access.",
            "Internal access: MFA optional - only 34% of employees have enrolled (HIGH).",
            "",
            "7.2 Privileged Access",
            "47 accounts with domain admin privileges. 12 are service accounts with",
            "non-rotating passwords (oldest: 847 days). 3 shared admin accounts in use.",
            "",
            "7.3 Access Reviews",
            "Quarterly access reviews documented but incomplete. Last review covered only",
            "60% of applications. No review process for cloud IAM roles.",
        ]),
        ("Access Control Evaluation (cont.)", [
            "7.4 Password Policy",
            "Minimum 12 characters, complexity requirements enforced. 90-day rotation.",
            "However, password reuse allowed after 3 cycles (should be 12+).",
            "",
            "7.5 Network Access Control",
            "802.1X deployed on 70% of switch ports. Guest VLAN properly configured.",
            "Missing: NAC for IoT devices (printers, cameras) - 23 unmanaged devices found.",
            "",
            "Recommendation: Mandate MFA for all users. Rotate service account credentials.",
            "Extend NAC to all device types. Increase password history to 12.",
        ]),
        ("Incident Response Capabilities", [
            "8.1 IR Plan",
            "Documented IR plan last updated: June 2024. Key contacts current.",
            "Tabletop exercise conducted in October 2024 - response time: 45 minutes.",
            "",
            "8.2 SIEM & Monitoring",
            "Splunk Enterprise deployed. Log sources: 78 of estimated 120 (65% coverage).",
            "Missing: Cloud trail logs, container runtime logs, DNS query logs.",
            "",
            "8.3 Alert Fatigue",
            "Average 2,847 alerts/day. Only 12% investigated. False positive rate: 89%.",
            "Critical alert MTTR: 4.2 hours (target: 1 hour).",
        ]),
        ("Incident Response Capabilities (cont.)", [
            "8.4 Forensic Readiness",
            "Disk imaging tools available (FTK, EnCase). Chain of custody procedures documented.",
            "Network packet capture: deployed on perimeter only, not on internal segments.",
            "",
            "8.5 Communication Plan",
            "Stakeholder notification matrix defined. Secure communication channel (Signal)",
            "established for IR team. External legal counsel on retainer.",
            "",
            "Recommendation: Expand log coverage to 95%+. Tune SIEM rules to reduce false",
            "positives. Deploy NDR solution for internal network visibility.",
        ]),
        ("Compliance Status", [
            "9.1 PCI DSS v4.0",
            "Current status: Partially compliant. 8 of 12 requirements met.",
            "Gap areas: Requirement 6 (Secure Systems), Requirement 10 (Logging),",
            "Requirement 11 (Testing), Requirement 12 (Policies).",
            "",
            "9.2 SOC 2 Type II",
            "Last audit: September 2024 - Clean opinion with 2 observations.",
            "Observations: (1) Incomplete access reviews, (2) Missing encryption on 2 DBs.",
            "",
            "9.3 GDPR",
            "Data Processing Agreements in place with all sub-processors.",
            "Right to Erasure process: manual, average completion time 14 business days.",
        ]),
        ("Compliance Status (cont.)", [
            "9.4 ISO 27001",
            "Certified since 2022. Surveillance audit scheduled for April 2025.",
            "3 minor non-conformities from last audit - 2 resolved, 1 in progress.",
            "",
            "9.5 NIST Cybersecurity Framework",
            "Current maturity: Tier 2 (Risk Informed). Target: Tier 3 (Repeatable).",
            "Strongest area: Identify (3.2/5). Weakest area: Recover (1.8/5).",
            "",
            "Recommendation: Prioritize PCI DSS gap remediation before Q3 assessment.",
            "Automate GDPR data subject request handling. Address ISO 27001 findings.",
        ]),
        ("Risk Matrix & Recommendations", [
            "CRITICAL (Remediate within 30 days):",
            "  C1: SQL Injection in payment gateway - CVSS 9.8",
            "  C2: Default credentials on payment admin panel - CVSS 9.1",
            "  C3: Unpatched F5 BIG-IP CVE-2023-46747 - CVSS 9.8",
            "  C4: Unencrypted FTP for batch processing - CVSS 8.7",
            "",
            "HIGH (Remediate within 60 days):",
            "  H1: Payment VLAN not isolated from employee network",
            "  H2: Stored XSS in customer portal",
            "  H3: IDOR in document download",
            "  H4: Weak JWT secret key",
            "  H5: Jenkins without authentication",
        ]),
        ("Risk Matrix & Recommendations (cont.)", [
            "HIGH (continued):",
            "  H6: S3 buckets without encryption (2 of 8)",
            "  H7: MongoDB without encryption at rest",
            "  H8: MFA not mandatory for internal access",
            "  H9: Service accounts with non-rotating passwords",
            "",
            "MEDIUM (Remediate within 90 days):",
            "  M1-M12: See detailed findings in sections 4-8.",
            "",
            "Total: 4 Critical, 9 High, 12 Medium, 7 Low, 3 Informational",
            "",
            "Estimated remediation cost: $180,000 - $250,000",
            "Estimated risk reduction: 73% of identified attack surface",
        ]),
        ("Appendices", [
            "Appendix A: Detailed Vulnerability Scan Results",
            "  Full Nessus scan output available in encrypted archive (see attached).",
            "",
            "Appendix B: Network Topology Diagram",
            "  Updated network map reflecting current segmentation.",
            "",
            "Appendix C: Tool Configurations",
            "  Nmap scan parameters, Burp Suite project settings, custom scripts.",
            "",
            "Appendix D: Credentials and Access Log",
            "  Test account credentials used during assessment (to be rotated).",
            "",
            "Contact: security-team@cybershield-analytics.com",
            "Emergency Hotline: +1 (555) 987-6543",
        ]),
    ]

    for idx, (title, lines) in enumerate(sections):
        page = doc.new_page(width=612, height=792)
        page_num = idx + 3  # pages 3-20

        # Header
        page.insert_text(pymupdf.Point(72, 60), title, fontsize=18, fontname="hebo", color=(0, 0, 0.4))
        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
        shape.finish(color=(0, 0, 0.4), width=1)
        shape.commit()

        # Body text
        y = 100
        for line in lines:
            if line == "":
                y += 12
                continue
            page.insert_text(pymupdf.Point(90, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
            y += 16

        # Footer
        page.insert_text(pymupdf.Point(72, 760), f"CyberShield Analytics - Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
        page.insert_text(pymupdf.Point(500, 760), f"Page {page_num}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Add URL links on multiple pages
    # Page 5 (index 4): Link to OWASP
    p = doc[4]
    link_rect = pymupdf.Rect(90, 100, 450, 116)
    p.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": "https://owasp.org/www-project-web-security-testing-guide/"})

    # Page 10 (index 9): Link to NIST
    p = doc[9]
    link_rect = pymupdf.Rect(90, 680, 400, 696)
    p.insert_text(pymupdf.Point(90, 693), "Reference: https://nvd.nist.gov/vuln/detail/CVE-2023-46747", fontsize=9, fontname="helv", color=(0, 0, 0.8))
    p.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": "https://nvd.nist.gov/vuln/detail/CVE-2023-46747"})

    # Page 15 (index 14): Link to PCI DSS
    p = doc[14]
    link_rect = pymupdf.Rect(90, 680, 400, 696)
    p.insert_text(pymupdf.Point(90, 693), "PCI DSS v4.0: https://www.pcisecuritystandards.org/", fontsize=9, fontname="helv", color=(0, 0, 0.8))
    p.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": "https://www.pcisecuritystandards.org/"})

    # Add JavaScript annotation on page 1
    # PyMuPDF: add a JavaScript action via annotation
    js_code = 'app.alert("This document contains security-sensitive information. Handle with care.");'
    p0 = doc[0]
    # Add as a text annotation with JavaScript
    annot = p0.add_text_annot(pymupdf.Point(500, 50), "Security Notice")
    annot.update()

    # Set metadata
    doc.set_metadata({
        "title": "Vendor Security Assessment Report - Meridian Financial Group",
        "author": "Dr. Elena Vasquez, CISSP, CISM",
        "subject": "Comprehensive Security Assessment Q1 2025",
        "keywords": "security, audit, penetration testing, vulnerability, compliance, PCI DSS",
        "creator": "CyberShield Analytics Report Generator v3.2",
        "producer": "CyberShield Analytics LLC",
    })

    # Set TOC/Bookmarks
    toc = [
        [1, "Executive Summary", 3],
        [1, "Scope of Assessment", 4],
        [1, "Methodology", 5],
        [1, "Network Infrastructure Review", 6],
        [1, "Application Security Findings", 8],
        [1, "Data Protection Analysis", 10],
        [1, "Access Control Evaluation", 12],
        [1, "Incident Response Capabilities", 14],
        [1, "Compliance Status", 16],
        [1, "Risk Matrix & Recommendations", 18],
        [1, "Appendices", 20],
    ]
    doc.set_toc(toc)

    # Save unencrypted first (PyMuPDF), then encrypt with pikepdf
    temp_path = f'{AUDIT_DIR}/temp_unencrypted.pdf'
    doc.save(temp_path)
    doc.close()

    # --- Step 2: Add embedded files and JavaScript using pikepdf ---
    import pikepdf

    pdf = pikepdf.open(temp_path)

    # Add JavaScript to the document catalog (document-level JS)
    js_string = pikepdf.String('app.alert("Security Notice: This document is classified.");')
    js_action = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/Action"),
        "/S": pikepdf.Name("/JavaScript"),
        "/JS": js_string,
    })
    # Add as OpenAction (runs when document is opened)
    pdf.Root["/OpenAction"] = pdf.make_indirect(js_action)

    # Also add JS to the Names tree
    js_entry_action = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/Action"),
        "/S": pikepdf.Name("/JavaScript"),
        "/JS": pikepdf.String('console.println("Audit document loaded at " + new Date().toISOString());'),
    })
    js_names_array = pikepdf.Array([
        pikepdf.String("AuditLogger"),
        pdf.make_indirect(js_entry_action),
    ])
    if "/Names" not in pdf.Root:
        pdf.Root["/Names"] = pdf.make_indirect(pikepdf.Dictionary())
    names = pdf.Root["/Names"]
    names["/JavaScript"] = pdf.make_indirect(pikepdf.Dictionary({
        "/Names": js_names_array,
    }))

    # Create embedded file attachments
    # Attachment 1: scan_results.csv
    csv_content = b"host,port,service,severity,cve\n10.10.1.5,8080,http,critical,CVE-2023-46747\n10.10.1.10,3306,mysql,high,CVE-2024-12345\n10.10.2.15,22,ssh,medium,CVE-2023-48795\n"
    csv_stream = pikepdf.Stream(pdf, csv_content)
    csv_stream["/Type"] = pikepdf.Name("/EmbeddedFile")
    csv_stream["/Subtype"] = pikepdf.Name("/text#2Fcsv")

    csv_filespec = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/Filespec"),
        "/F": pikepdf.String("scan_results.csv"),
        "/UF": pikepdf.String("scan_results.csv"),
        "/EF": pikepdf.Dictionary({
            "/F": pdf.make_indirect(csv_stream),
        }),
        "/Desc": pikepdf.String("Vulnerability scan raw results"),
    })

    # Attachment 2: remediation_timeline.txt
    txt_content = b"Remediation Timeline\n====================\nCritical: 30 days (by April 15, 2025)\nHigh: 60 days (by May 15, 2025)\nMedium: 90 days (by June 15, 2025)\nLow: Next quarterly cycle\n"
    txt_stream = pikepdf.Stream(pdf, txt_content)
    txt_stream["/Type"] = pikepdf.Name("/EmbeddedFile")
    txt_stream["/Subtype"] = pikepdf.Name("/text#2Fplain")

    txt_filespec = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/Filespec"),
        "/F": pikepdf.String("remediation_timeline.txt"),
        "/UF": pikepdf.String("remediation_timeline.txt"),
        "/EF": pikepdf.Dictionary({
            "/F": pdf.make_indirect(txt_stream),
        }),
        "/Desc": pikepdf.String("Remediation timeline for findings"),
    })

    # Add to EmbeddedFiles name tree
    ef_names_array = pikepdf.Array([
        pikepdf.String("remediation_timeline.txt"),
        pdf.make_indirect(txt_filespec),
        pikepdf.String("scan_results.csv"),
        pdf.make_indirect(csv_filespec),
    ])

    names["/EmbeddedFiles"] = pdf.make_indirect(pikepdf.Dictionary({
        "/Names": ef_names_array,
    }))

    # --- Step 3: Save with encryption ---
    pdf.save(
        PDF_PATH,
        encryption=pikepdf.Encryption(
            owner="CyberShield2025!Admin",
            user="",   # empty user password = can open without password but permissions enforced
            R=6,        # AES-256
            allow=pikepdf.Permissions(
                extract=False,
                modify_annotation=True,
                print_lowres=True,
                print_highres=True,
                modify_form=True,
                modify_other=False,
                modify_assembly=False,
            ),
        ),
    )
    pdf.close()

    # Clean up temp file
    os.remove(temp_path)

    print(f'Initial PDF created: {PDF_PATH}')
    print(f'Pages: 20')
    print(f'Encryption: AES-256 (R=6)')
    print(f'Scripts dir created: {SCRIPTS_DIR}')

    # Open terminal for the agent to write the script
    launch_gui('bash -c "cd /home/user && exec bash"', delay_sec=0.5)
    # Actually open a terminal emulator
    launch_gui('gnome-terminal --working-directory=/home/user', delay_sec=2.0)
    # Also open the PDF in evince so the agent can see it
    launch_gui(f'evince "{PDF_PATH}"', delay_sec=2.0)

    print('GUI_READY: launched terminal and PDF viewer with DISPLAY=:0')


create_initial()
