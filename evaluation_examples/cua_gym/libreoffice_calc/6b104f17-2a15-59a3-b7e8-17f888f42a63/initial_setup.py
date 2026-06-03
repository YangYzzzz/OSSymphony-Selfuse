"""
Initial Setup: PDF to Google Docs - Audit Recommendations
Task ID: osworld_multi_apps_pdf_to_gdocs_006
Domain: multi_apps (PDF + Chrome/Google Docs)

Creates:
  - audit_report.pdf on Desktop with Background, Findings, Recommendations, Appendices sections
  - Opens Chrome with Google Drive
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_006'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/audit_report.pdf'


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


def create_audit_pdf():
    """Create a realistic audit report PDF with multiple sections."""
    try:
        from fpdf import FPDF
    except ImportError:
        subprocess.run(['pip3', 'install', 'fpdf2'], check=True)
        from fpdf import FPDF

    os.makedirs(DESKTOP, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 12, 'Annual IT Security Audit Report', ln=True, align='C')
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, 'Fiscal Year 2024-2025 | Prepared by: Compliance & Risk Management Division', ln=True, align='C')
    pdf.ln(6)

    # Horizontal line
    pdf.set_draw_color(100, 100, 100)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # Executive Summary
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, 'Executive Summary', ln=True)
    pdf.set_font('Helvetica', '', 11)
    summary_text = (
        'This annual IT security audit was conducted between January 15 and February 28, 2025, '
        'covering all critical infrastructure components, access control systems, data handling '
        'procedures, and third-party vendor integrations. The audit team reviewed 47 systems '
        'across 8 business units and identified areas of compliance strength as well as '
        'opportunities for improvement. Overall, the organization demonstrates a solid security '
        'posture with targeted vulnerabilities requiring remediation.'
    )
    pdf.multi_cell(0, 6, summary_text)
    pdf.ln(6)

    # Section 1: Background
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 10, '1. Background', ln=True, fill=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(3)

    background_text = (
        'The IT Security Audit was commissioned by the Board of Directors following the '
        'adoption of the updated Information Security Policy (ISP v3.2) in December 2024. '
        'The audit scope was defined to include network perimeter security, identity and '
        'access management (IAM), endpoint protection, cloud infrastructure governance, '
        'data loss prevention (DLP) controls, and incident response readiness.\n\n'
        'The audit team comprised four certified information systems auditors (CISA) and '
        'two external consultants from SecureVision Partners LLC. The methodology followed '
        'the NIST Cybersecurity Framework (CSF 2.0) and ISO/IEC 27001:2022 standards.\n\n'
        'Prior to fieldwork, the team reviewed documentation including network diagrams, '
        'system inventories, change management logs, security incident reports from the '
        'previous 12 months, and vulnerability assessment results from the Q3 2024 scan.'
    )
    pdf.multi_cell(0, 6, background_text)
    pdf.ln(6)

    # Section 2: Findings
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 10, '2. Findings', ln=True, fill=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Finding 2.1 - Multi-Factor Authentication Coverage Gaps', ln=True)
    pdf.set_font('Helvetica', '', 11)
    finding1 = (
        'Risk Level: HIGH\n'
        'Multi-factor authentication (MFA) is not enforced for 23% of privileged accounts '
        'across the organization. Specifically, 14 administrator accounts in the Finance and '
        'HR departments operate with single-factor authentication, creating significant '
        'exposure to credential-based attacks. Industry benchmarks indicate that MFA '
        'enforcement reduces account compromise risk by up to 99.9%.'
    )
    pdf.multi_cell(0, 6, finding1)
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Finding 2.2 - Outdated Software on Production Servers', ln=True)
    pdf.set_font('Helvetica', '', 11)
    finding2 = (
        'Risk Level: HIGH\n'
        'Three production servers (SRV-PROD-012, SRV-PROD-019, SRV-PROD-031) are running '
        'operating system versions that reached end-of-life in September 2024. These systems '
        'no longer receive security patches, leaving them vulnerable to known exploits. '
        'Additionally, 18 workstations in the customer support team have not applied critical '
        'patches released in Q4 2024.'
    )
    pdf.multi_cell(0, 6, finding2)
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Finding 2.3 - Third-Party Vendor Access Controls', ln=True)
    pdf.set_font('Helvetica', '', 11)
    finding3 = (
        'Risk Level: MEDIUM\n'
        'Seven third-party vendors with access to internal systems have not completed the '
        'annual vendor security assessment required by Policy ISP-4.3. Two vendors, '
        'DataSync Solutions and CloudMigrate Inc., were found to have overly broad access '
        'permissions that exceed the principle of least privilege. Access tokens for these '
        'vendors have not been rotated in the past 18 months.'
    )
    pdf.multi_cell(0, 6, finding3)
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Finding 2.4 - Data Retention Policy Non-Compliance', ln=True)
    pdf.set_font('Helvetica', '', 11)
    finding4 = (
        'Risk Level: MEDIUM\n'
        'Audit sampling of the document management system revealed that 31% of records '
        'classified as "confidential" are retained beyond the 7-year policy limit. The '
        'automated data retention enforcement mechanism failed to trigger deletion workflows '
        'for records created before the DRM system migration in January 2022. This '
        'non-compliance creates unnecessary legal exposure.'
    )
    pdf.multi_cell(0, 6, finding4)
    pdf.ln(6)

    # Section 3: Recommendations (KEY SECTION)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 10, '3. Recommendations', ln=True, fill=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(3)

    rec_intro = (
        'Based on the audit findings, the following recommendations are provided to '
        'strengthen the organization\'s security posture and achieve full compliance with '
        'applicable regulatory requirements. Recommendations are prioritized by risk level '
        'and estimated implementation effort.'
    )
    pdf.multi_cell(0, 6, rec_intro)
    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Recommendation R-01: Enforce MFA for All Privileged Accounts (Priority: Critical)', ln=True)
    pdf.set_font('Helvetica', '', 11)
    rec1 = (
        'The IT Security team should immediately enforce multi-factor authentication for '
        'all accounts with privileged access rights, including administrator, system '
        'operator, and service accounts. Implementation should use the existing Okta '
        'platform already deployed for 77% of accounts. A phased rollout should be '
        'completed within 30 days, beginning with Finance and HR departments. '
        'Exemptions should require CISO approval and be documented with compensating '
        'controls. Target completion date: March 31, 2025.'
    )
    pdf.multi_cell(0, 6, rec1)
    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Recommendation R-02: Upgrade End-of-Life Production Systems (Priority: Critical)', ln=True)
    pdf.set_font('Helvetica', '', 11)
    rec2 = (
        'The Infrastructure team must immediately plan and execute migration of the three '
        'identified production servers (SRV-PROD-012, SRV-PROD-019, SRV-PROD-031) to '
        'supported operating system versions. A temporary risk acceptance form should be '
        'completed and signed by the VP of Technology for each affected server while '
        'migration is underway. Additionally, a comprehensive patch management review '
        'should address the 18 unpatched customer support workstations. '
        'Target completion date: April 15, 2025.'
    )
    pdf.multi_cell(0, 6, rec2)
    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Recommendation R-03: Remediate Vendor Access and Complete Assessments (Priority: High)', ln=True)
    pdf.set_font('Helvetica', '', 11)
    rec3 = (
        'Vendor Management should immediately revoke excess permissions for DataSync '
        'Solutions and CloudMigrate Inc. and implement a least-privilege access model '
        'following the principle of minimum necessary access. All seven overdue vendor '
        'security assessments should be completed within 45 days. Access tokens for '
        'all third-party vendors should be rotated on a 90-day schedule going forward, '
        'enforced through the vendor portal. A dedicated vendor risk register should '
        'be established and reviewed quarterly. Target completion date: April 30, 2025.'
    )
    pdf.multi_cell(0, 6, rec3)
    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Recommendation R-04: Resolve Data Retention Compliance Gaps (Priority: High)', ln=True)
    pdf.set_font('Helvetica', '', 11)
    rec4 = (
        'The Legal and Compliance team, in coordination with IT, should initiate a '
        'retrospective data remediation project to identify and appropriately dispose '
        'of records exceeding retention limits. The automated retention workflow should '
        'be debugged and tested to handle records predating the January 2022 DRM '
        'migration. Monthly retention compliance reports should be implemented and '
        'reviewed by the Data Governance Committee. Target completion date: June 30, 2025.'
    )
    pdf.multi_cell(0, 6, rec4)
    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Recommendation R-05: Enhance Incident Response Readiness (Priority: Medium)', ln=True)
    pdf.set_font('Helvetica', '', 11)
    rec5 = (
        'While incident response procedures exist, tabletop exercises have not been '
        'conducted in 14 months. The Security Operations team should schedule bi-annual '
        'incident response tabletop exercises involving key stakeholders from IT, Legal, '
        'Communications, and executive leadership. The incident response playbooks should '
        'be updated to reflect current cloud infrastructure architecture and the '
        'newly adopted zero-trust network model. Target completion date: May 31, 2025.'
    )
    pdf.multi_cell(0, 6, rec5)
    pdf.ln(6)

    # Section 4: Appendices
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 10, '4. Appendices', ln=True, fill=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Appendix A: Audit Scope and Methodology', ln=True)
    pdf.set_font('Helvetica', '', 11)
    appendix_a = (
        'The audit covered the following systems and domains:\n'
        '- Network infrastructure: 12 routers, 34 switches, 6 firewalls\n'
        '- Servers: 47 physical and virtual servers (on-premises and cloud)\n'
        '- Endpoints: 312 workstations and laptops\n'
        '- Cloud platforms: AWS (production), Azure (dev/test), GCP (data analytics)\n'
        '- Third-party integrations: 22 active vendor connections\n'
        '- Applications: 15 business-critical applications\n\n'
        'Audit methodology followed the NIST CSF 2.0 Identify, Protect, Detect, '
        'Respond, and Recover functions. Evidence was collected through interviews, '
        'system configuration reviews, log analysis, and automated vulnerability scans.'
    )
    pdf.multi_cell(0, 6, appendix_a)
    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Appendix B: Risk Rating Criteria', ln=True)
    pdf.set_font('Helvetica', '', 11)
    appendix_b = (
        'Critical: Immediate action required. Exploitation could result in significant '
        'financial loss, regulatory penalties, or major data breach.\n\n'
        'High: Action required within 30 days. Significant vulnerability with moderate '
        'to high likelihood of exploitation.\n\n'
        'Medium: Action required within 90 days. Moderate vulnerability requiring '
        'planned remediation.\n\n'
        'Low: Action required within 180 days. Minor vulnerability with low likelihood '
        'or impact if exploited.'
    )
    pdf.multi_cell(0, 6, appendix_b)
    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, 'Appendix C: Audit Team and Contact Information', ln=True)
    pdf.set_font('Helvetica', '', 11)
    appendix_c = (
        'Lead Auditor: Jennifer Thornton, CISA, CISSP\n'
        'Senior Auditor: Marcus Webb, CISA\n'
        'Auditor: Priya Nair, CIA\n'
        'Auditor: David Okonkwo, CISM\n'
        'External Consultants: SecureVision Partners LLC\n\n'
        'For questions regarding this report, contact: audit@compliance.company.com'
    )
    pdf.multi_cell(0, 6, appendix_c)

    pdf.output(PDF_PATH)
    print(f'PDF created: {PDF_PATH}')
    return PDF_PATH


def setup_chrome_gdrive():
    """
    Set up Chrome to open with Google Drive in the compliance folder view.
    Chrome should already be configured with a Google account on this VM.
    We launch Chrome pointing to Google Drive.
    """
    # Kill existing Chrome instances first to avoid profile lock issues
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    time.sleep(2)

    # Launch Chrome with Google Drive open
    # The task context says Chrome is open with Google Drive
    chrome_cmd = 'google-chrome --no-first-run --disable-default-apps "https://drive.google.com"'
    launch_gui(chrome_cmd, delay_sec=4.0)
    print('Chrome launched with Google Drive')


def create_initial():
    # 1. Create the audit_report.pdf on Desktop
    create_audit_pdf()

    # 2. Launch Chrome with Google Drive
    setup_chrome_gdrive()

    print(f'Initial state created:')
    print(f'  - PDF: {PDF_PATH}')
    print(f'  - Chrome: opened with Google Drive')
    print('GUI_READY: launched required app(s) with DISPLAY=:0')


create_initial()
