"""
Initial Setup: Create 5 PDF versions of a compliance document in /home/user/versions/
Task ID: pdf_gf3_045
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
VERSIONS_DIR = f'{WORKDIR}/versions'

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


# ── Content for each version ──────────────────────────────────────────────
# A compliance manual that evolves across 5 versions

V1_PAGES = [
    # Page 1: Title + TOC
    (
        "Global Data Protection Compliance Manual\n"
        "Version 1.0 - January 2024\n"
        "Prepared by: Meridian Compliance Group\n\n"
        "Table of Contents\n\n"
        "1. Introduction and Purpose\n"
        "2. Scope and Applicability\n"
        "3. Data Classification Framework\n"
        "4. Access Control Policies\n"
        "5. Incident Response Procedures"
    ),
    # Page 2: Introduction
    (
        "1. Introduction and Purpose\n\n"
        "This manual establishes the comprehensive data protection framework\n"
        "for Meridian Technologies Inc. and all subsidiary operations across\n"
        "North America, Europe, and Asia-Pacific regions.\n\n"
        "The manual provides binding guidance on the collection, processing,\n"
        "storage, and disposal of personal data in compliance with applicable\n"
        "regulations including GDPR, CCPA, and PIPEDA.\n\n"
        "All employees, contractors, and third-party service providers with\n"
        "access to company data systems must adhere to the policies outlined\n"
        "in this document. Non-compliance may result in disciplinary action\n"
        "up to and including termination of employment or contract."
    ),
    # Page 3: Scope
    (
        "2. Scope and Applicability\n\n"
        "This policy applies to all personal data processed by Meridian\n"
        "Technologies regardless of format (digital or physical) or storage\n"
        "location (on-premises servers, cloud platforms, or portable media).\n\n"
        "Covered data categories:\n"
        "  - Employee personal records (HR, payroll, benefits)\n"
        "  - Customer account information and transaction histories\n"
        "  - Vendor and partner contact details\n"
        "  - Website visitor analytics and cookie data\n"
        "  - Internal communications metadata\n\n"
        "Geographic coverage includes all offices in the United States,\n"
        "Canada, United Kingdom, Germany, and Singapore."
    ),
    # Page 4: Data Classification
    (
        "3. Data Classification Framework\n\n"
        "All data processed by Meridian Technologies must be classified\n"
        "according to the following tiers:\n\n"
        "Tier 1 - Public: Information approved for external distribution.\n"
        "Examples: published marketing materials, public financial filings.\n\n"
        "Tier 2 - Internal: Business information not intended for public\n"
        "release. Examples: internal memos, project timelines, org charts.\n\n"
        "Tier 3 - Confidential: Sensitive business data requiring access\n"
        "controls. Examples: financial projections, strategic plans,\n"
        "employee performance reviews.\n\n"
        "Tier 4 - Restricted: Highly sensitive data with strict regulatory\n"
        "requirements. Examples: social security numbers, health records,\n"
        "payment card data, biometric identifiers."
    ),
    # Page 5: Access Control
    (
        "4. Access Control Policies\n\n"
        "Access to data systems is governed by the principle of least\n"
        "privilege. Users receive only the minimum access necessary to\n"
        "perform their assigned duties.\n\n"
        "Authentication requirements:\n"
        "  - All system access requires multi-factor authentication (MFA)\n"
        "  - Passwords must be at least 12 characters with complexity rules\n"
        "  - Password rotation every 90 days\n"
        "  - Account lockout after 5 failed attempts\n\n"
        "Access review cycle:\n"
        "  - Quarterly review of all user access privileges\n"
        "  - Immediate revocation upon employee termination\n"
        "  - Annual recertification by department managers\n\n"
        "Contact: security@meridian-tech.com for access requests."
    ),
]

V2_PAGES = [
    # Page 1: Updated title
    (
        "Global Data Protection Compliance Manual\n"
        "Version 2.0 - March 2024\n"
        "Prepared by: Meridian Compliance Group\n\n"
        "Table of Contents\n\n"
        "1. Introduction and Purpose\n"
        "2. Scope and Applicability\n"
        "3. Data Classification Framework\n"
        "4. Access Control Policies\n"
        "5. Incident Response Procedures\n"
        "6. Data Retention and Disposal"
    ),
    # Page 2: Introduction - minor updates
    (
        "1. Introduction and Purpose\n\n"
        "This manual establishes the comprehensive data protection framework\n"
        "for Meridian Technologies Inc. and all subsidiary operations across\n"
        "North America, Europe, Asia-Pacific, and Latin America regions.\n\n"
        "The manual provides binding guidance on the collection, processing,\n"
        "storage, transfer, and disposal of personal data in compliance with\n"
        "applicable regulations including GDPR, CCPA, PIPEDA, and LGPD.\n\n"
        "All employees, contractors, and third-party service providers with\n"
        "access to company data systems must adhere to the policies outlined\n"
        "in this document. Non-compliance may result in disciplinary action\n"
        "up to and including termination of employment or contract.\n\n"
        "Effective date: March 15, 2024. Supersedes Version 1.0."
    ),
    # Page 3: Scope - expanded
    (
        "2. Scope and Applicability\n\n"
        "This policy applies to all personal data processed by Meridian\n"
        "Technologies regardless of format (digital or physical) or storage\n"
        "location (on-premises servers, cloud platforms, or portable media).\n\n"
        "Covered data categories:\n"
        "  - Employee personal records (HR, payroll, benefits)\n"
        "  - Customer account information and transaction histories\n"
        "  - Vendor and partner contact details\n"
        "  - Website visitor analytics and cookie data\n"
        "  - Internal communications metadata\n"
        "  - Biometric access control data\n"
        "  - IoT sensor telemetry from smart building systems\n\n"
        "Geographic coverage includes all offices in the United States,\n"
        "Canada, United Kingdom, Germany, Singapore, and Brazil."
    ),
    # Page 4: Data Classification - same
    (
        "3. Data Classification Framework\n\n"
        "All data processed by Meridian Technologies must be classified\n"
        "according to the following tiers:\n\n"
        "Tier 1 - Public: Information approved for external distribution.\n"
        "Examples: published marketing materials, public financial filings.\n\n"
        "Tier 2 - Internal: Business information not intended for public\n"
        "release. Examples: internal memos, project timelines, org charts.\n\n"
        "Tier 3 - Confidential: Sensitive business data requiring access\n"
        "controls. Examples: financial projections, strategic plans,\n"
        "employee performance reviews.\n\n"
        "Tier 4 - Restricted: Highly sensitive data with strict regulatory\n"
        "requirements. Examples: social security numbers, health records,\n"
        "payment card data, biometric identifiers."
    ),
    # Page 5: Access Control - updated
    (
        "4. Access Control Policies\n\n"
        "Access to data systems is governed by the principle of least\n"
        "privilege. Users receive only the minimum access necessary to\n"
        "perform their assigned duties.\n\n"
        "Authentication requirements:\n"
        "  - All system access requires multi-factor authentication (MFA)\n"
        "  - Passwords must be at least 14 characters with complexity rules\n"
        "  - Password rotation every 60 days\n"
        "  - Account lockout after 3 failed attempts\n"
        "  - Hardware security keys required for Tier 4 data access\n\n"
        "Access review cycle:\n"
        "  - Monthly review of privileged user access\n"
        "  - Quarterly review of all user access privileges\n"
        "  - Immediate revocation upon employee termination\n"
        "  - Annual recertification by department managers\n\n"
        "Contact: security@meridian-tech.com for access requests."
    ),
]

V3_PAGES = [
    # Page 1: Updated title
    (
        "Global Data Protection Compliance Manual\n"
        "Version 3.0 - June 2024\n"
        "Prepared by: Meridian Compliance Group\n"
        "Reviewed by: External Audit Team (Deloitte)\n\n"
        "Table of Contents\n\n"
        "1. Introduction and Purpose\n"
        "2. Scope and Applicability\n"
        "3. Data Classification Framework\n"
        "4. Access Control Policies\n"
        "5. Incident Response Procedures\n"
        "6. Data Retention and Disposal\n"
        "7. Cross-Border Data Transfer"
    ),
    # Page 2: Introduction
    (
        "1. Introduction and Purpose\n\n"
        "This manual establishes the comprehensive data protection framework\n"
        "for Meridian Technologies Inc. and all subsidiary operations across\n"
        "North America, Europe, Asia-Pacific, and Latin America regions.\n\n"
        "The manual provides binding guidance on the collection, processing,\n"
        "storage, transfer, and disposal of personal data in compliance with\n"
        "applicable regulations including GDPR, CCPA, PIPEDA, LGPD, and\n"
        "the newly enacted EU AI Act.\n\n"
        "All employees, contractors, and third-party service providers with\n"
        "access to company data systems must adhere to the policies outlined\n"
        "in this document. Non-compliance may result in disciplinary action\n"
        "up to and including termination of employment or contract.\n\n"
        "This version incorporates recommendations from the Q1 2024 external\n"
        "audit conducted by Deloitte.\n\n"
        "Effective date: June 1, 2024. Supersedes Version 2.0."
    ),
    # Page 3: Scope
    (
        "2. Scope and Applicability\n\n"
        "This policy applies to all personal data processed by Meridian\n"
        "Technologies regardless of format (digital or physical) or storage\n"
        "location (on-premises servers, cloud platforms, or portable media).\n\n"
        "Covered data categories:\n"
        "  - Employee personal records (HR, payroll, benefits)\n"
        "  - Customer account information and transaction histories\n"
        "  - Vendor and partner contact details\n"
        "  - Website visitor analytics and cookie data\n"
        "  - Internal communications metadata\n"
        "  - Biometric access control data\n"
        "  - IoT sensor telemetry from smart building systems\n"
        "  - AI model training datasets containing personal data\n\n"
        "Geographic coverage includes all offices in the United States,\n"
        "Canada, United Kingdom, Germany, France, Singapore, Brazil,\n"
        "and Japan."
    ),
    # Page 4: Data Classification - expanded
    (
        "3. Data Classification Framework\n\n"
        "All data processed by Meridian Technologies must be classified\n"
        "according to the following tiers:\n\n"
        "Tier 1 - Public: Information approved for external distribution.\n"
        "Examples: published marketing materials, public financial filings.\n"
        "Retention: Indefinite. No special handling required.\n\n"
        "Tier 2 - Internal: Business information not intended for public\n"
        "release. Examples: internal memos, project timelines, org charts.\n"
        "Retention: 3 years after creation. Encrypted at rest.\n\n"
        "Tier 3 - Confidential: Sensitive business data requiring access\n"
        "controls. Examples: financial projections, strategic plans,\n"
        "employee performance reviews.\n"
        "Retention: 5 years. Encrypted in transit and at rest.\n\n"
        "Tier 4 - Restricted: Highly sensitive data with strict regulatory\n"
        "requirements. Examples: social security numbers, health records,\n"
        "payment card data, biometric identifiers.\n"
        "Retention: Per regulatory mandate. AES-256 encryption required."
    ),
    # Page 5: Access Control
    (
        "4. Access Control Policies\n\n"
        "Access to data systems is governed by the principle of least\n"
        "privilege and zero-trust architecture principles.\n\n"
        "Authentication requirements:\n"
        "  - All system access requires multi-factor authentication (MFA)\n"
        "  - Passwords must be at least 14 characters with complexity rules\n"
        "  - Password rotation every 60 days\n"
        "  - Account lockout after 3 failed attempts\n"
        "  - Hardware security keys required for Tier 4 data access\n"
        "  - Session timeout after 15 minutes of inactivity\n\n"
        "Access review cycle:\n"
        "  - Monthly review of privileged user access\n"
        "  - Quarterly review of all user access privileges\n"
        "  - Immediate revocation upon employee termination\n"
        "  - Annual recertification by department managers\n"
        "  - Automated anomaly detection on access patterns\n\n"
        "Contact: security@meridian-tech.com for access requests."
    ),
]

V4_PAGES = [
    # Page 1
    (
        "Global Data Protection Compliance Manual\n"
        "Version 4.0 - September 2024\n"
        "Prepared by: Meridian Compliance Group\n"
        "Reviewed by: External Audit Team (Deloitte)\n"
        "Approved by: Chief Information Security Officer\n\n"
        "Table of Contents\n\n"
        "1. Introduction and Purpose\n"
        "2. Scope and Applicability\n"
        "3. Data Classification Framework\n"
        "4. Access Control Policies\n"
        "5. Incident Response Procedures\n"
        "6. Data Retention and Disposal\n"
        "7. Cross-Border Data Transfer\n"
        "8. Vendor Risk Management"
    ),
    # Page 2
    (
        "1. Introduction and Purpose\n\n"
        "This manual establishes the comprehensive data protection framework\n"
        "for Meridian Technologies Inc. and all subsidiary operations\n"
        "worldwide.\n\n"
        "The manual provides binding guidance on the collection, processing,\n"
        "storage, transfer, and disposal of personal data in compliance with\n"
        "applicable regulations including GDPR, CCPA, PIPEDA, LGPD, the\n"
        "EU AI Act, and the UK Data Protection Act 2018.\n\n"
        "All employees, contractors, and third-party service providers with\n"
        "access to company data systems must adhere to the policies outlined\n"
        "in this document. Non-compliance may result in disciplinary action\n"
        "up to and including termination of employment or contract.\n\n"
        "This version adds vendor risk management requirements following\n"
        "the SolarTech supply chain incident of July 2024.\n\n"
        "Effective date: September 1, 2024. Supersedes Version 3.0."
    ),
    # Page 3
    (
        "2. Scope and Applicability\n\n"
        "This policy applies to all personal data processed by Meridian\n"
        "Technologies regardless of format (digital or physical) or storage\n"
        "location (on-premises servers, cloud platforms, edge computing\n"
        "nodes, or portable media).\n\n"
        "Covered data categories:\n"
        "  - Employee personal records (HR, payroll, benefits)\n"
        "  - Customer account information and transaction histories\n"
        "  - Vendor and partner contact details and security assessments\n"
        "  - Website visitor analytics and cookie data\n"
        "  - Internal communications metadata\n"
        "  - Biometric access control data\n"
        "  - IoT sensor telemetry from smart building systems\n"
        "  - AI model training datasets containing personal data\n"
        "  - Supply chain partner shared datasets\n\n"
        "Geographic coverage: All countries where Meridian maintains\n"
        "offices or processes data of local residents."
    ),
    # Page 4
    (
        "3. Data Classification Framework\n\n"
        "All data processed by Meridian Technologies must be classified\n"
        "according to the following tiers:\n\n"
        "Tier 1 - Public: Information approved for external distribution.\n"
        "Examples: published marketing materials, public financial filings.\n"
        "Retention: Indefinite. No special handling required.\n\n"
        "Tier 2 - Internal: Business information not intended for public\n"
        "release. Examples: internal memos, project timelines, org charts.\n"
        "Retention: 3 years after creation. Encrypted at rest.\n\n"
        "Tier 3 - Confidential: Sensitive business data requiring access\n"
        "controls. Examples: financial projections, strategic plans,\n"
        "employee performance reviews, vendor security assessments.\n"
        "Retention: 5 years. Encrypted in transit and at rest.\n\n"
        "Tier 4 - Restricted: Highly sensitive data with strict regulatory\n"
        "requirements. Examples: social security numbers, health records,\n"
        "payment card data, biometric identifiers.\n"
        "Retention: Per regulatory mandate. AES-256 encryption required.\n"
        "Automated data loss prevention (DLP) monitoring enabled."
    ),
    # Page 5
    (
        "4. Access Control Policies\n\n"
        "Access to data systems is governed by the principle of least\n"
        "privilege and zero-trust architecture principles.\n\n"
        "Authentication requirements:\n"
        "  - All system access requires multi-factor authentication (MFA)\n"
        "  - Passwords must be at least 16 characters with complexity rules\n"
        "  - Password rotation every 60 days\n"
        "  - Account lockout after 3 failed attempts\n"
        "  - Hardware security keys required for Tier 3 and Tier 4 data\n"
        "  - Session timeout after 15 minutes of inactivity\n"
        "  - Continuous authentication for remote access sessions\n\n"
        "Access review cycle:\n"
        "  - Weekly review of administrator and root access\n"
        "  - Monthly review of privileged user access\n"
        "  - Quarterly review of all user access privileges\n"
        "  - Immediate revocation upon employee termination\n"
        "  - Annual recertification by department managers\n"
        "  - Automated anomaly detection on access patterns\n\n"
        "Contact: security@meridian-tech.com for access requests."
    ),
]

V5_PAGES = [
    # Page 1
    (
        "Global Data Protection Compliance Manual\n"
        "Version 5.0 - December 2024\n"
        "Prepared by: Meridian Compliance Group\n"
        "Reviewed by: External Audit Team (Deloitte)\n"
        "Approved by: Chief Information Security Officer\n"
        "Board Ratification: December 10, 2024\n\n"
        "Table of Contents\n\n"
        "1. Introduction and Purpose\n"
        "2. Scope and Applicability\n"
        "3. Data Classification Framework\n"
        "4. Access Control Policies\n"
        "5. Incident Response Procedures\n"
        "6. Data Retention and Disposal\n"
        "7. Cross-Border Data Transfer\n"
        "8. Vendor Risk Management\n"
        "9. AI and Automated Decision-Making"
    ),
    # Page 2
    (
        "1. Introduction and Purpose\n\n"
        "This manual establishes the comprehensive data protection framework\n"
        "for Meridian Technologies Inc. and all subsidiary operations\n"
        "worldwide.\n\n"
        "The manual provides binding guidance on the collection, processing,\n"
        "storage, transfer, and disposal of personal data in compliance with\n"
        "applicable regulations including GDPR, CCPA, PIPEDA, LGPD, the\n"
        "EU AI Act, the UK Data Protection Act 2018, and China's PIPL.\n\n"
        "All employees, contractors, and third-party service providers with\n"
        "access to company data systems must adhere to the policies outlined\n"
        "in this document. Non-compliance may result in disciplinary action\n"
        "up to and including termination of employment or contract.\n\n"
        "Version 5.0 introduces governance for AI systems and automated\n"
        "decision-making processes that utilize personal data.\n\n"
        "Effective date: January 1, 2025. Supersedes Version 4.0."
    ),
    # Page 3
    (
        "2. Scope and Applicability\n\n"
        "This policy applies to all personal data processed by Meridian\n"
        "Technologies regardless of format (digital or physical) or storage\n"
        "location (on-premises servers, cloud platforms, edge computing\n"
        "nodes, or portable media).\n\n"
        "Covered data categories:\n"
        "  - Employee personal records (HR, payroll, benefits)\n"
        "  - Customer account information and transaction histories\n"
        "  - Vendor and partner contact details and security assessments\n"
        "  - Website visitor analytics and cookie data\n"
        "  - Internal communications metadata\n"
        "  - Biometric access control data\n"
        "  - IoT sensor telemetry from smart building systems\n"
        "  - AI model training datasets containing personal data\n"
        "  - Supply chain partner shared datasets\n"
        "  - Automated decision outputs affecting individuals\n\n"
        "Geographic coverage: All countries where Meridian maintains\n"
        "offices or processes data of local residents."
    ),
    # Page 4
    (
        "3. Data Classification Framework\n\n"
        "All data processed by Meridian Technologies must be classified\n"
        "according to the following tiers:\n\n"
        "Tier 1 - Public: Information approved for external distribution.\n"
        "Examples: published marketing materials, public financial filings.\n"
        "Retention: Indefinite. No special handling required.\n\n"
        "Tier 2 - Internal: Business information not intended for public\n"
        "release. Examples: internal memos, project timelines, org charts.\n"
        "Retention: 3 years after creation. Encrypted at rest.\n\n"
        "Tier 3 - Confidential: Sensitive business data requiring access\n"
        "controls. Examples: financial projections, strategic plans,\n"
        "employee performance reviews, vendor security assessments,\n"
        "AI model evaluation reports.\n"
        "Retention: 5 years. Encrypted in transit and at rest.\n\n"
        "Tier 4 - Restricted: Highly sensitive data with strict regulatory\n"
        "requirements. Examples: social security numbers, health records,\n"
        "payment card data, biometric identifiers, AI training data\n"
        "containing protected attributes.\n"
        "Retention: Per regulatory mandate. AES-256 encryption required.\n"
        "Automated data loss prevention (DLP) monitoring enabled."
    ),
    # Page 5
    (
        "4. Access Control Policies\n\n"
        "Access to data systems is governed by the principle of least\n"
        "privilege and zero-trust architecture principles.\n\n"
        "Authentication requirements:\n"
        "  - All system access requires multi-factor authentication (MFA)\n"
        "  - Passkeys or FIDO2 keys preferred over passwords\n"
        "  - If passwords used: at least 16 chars with complexity rules\n"
        "  - Password rotation every 60 days\n"
        "  - Account lockout after 3 failed attempts\n"
        "  - Hardware security keys required for Tier 3 and Tier 4 data\n"
        "  - Session timeout after 10 minutes of inactivity\n"
        "  - Continuous authentication for remote access sessions\n"
        "  - AI system access requires additional data ethics approval\n\n"
        "Access review cycle:\n"
        "  - Weekly review of administrator and root access\n"
        "  - Monthly review of privileged user access\n"
        "  - Quarterly review of all user access privileges\n"
        "  - Immediate revocation upon employee termination\n"
        "  - Annual recertification by department managers\n"
        "  - Automated anomaly detection on access patterns\n"
        "  - AI model access audited by Data Ethics Board quarterly\n\n"
        "Contact: security@meridian-tech.com for access requests."
    ),
]


def create_pdf(filepath, pages):
    """Create a PDF with the given page content."""
    doc = pymupdf.open()
    for page_text in pages:
        page = doc.new_page(width=595, height=842)  # A4
        # Title area
        rect = pymupdf.Rect(54, 54, 541, 788)
        page.insert_textbox(
            rect,
            page_text,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )
    doc.save(filepath)
    doc.close()
    print(f'Created: {filepath}')


def create_initial():
    os.makedirs(VERSIONS_DIR, exist_ok=True)

    create_pdf(f'{VERSIONS_DIR}/v1.pdf', V1_PAGES)
    create_pdf(f'{VERSIONS_DIR}/v2.pdf', V2_PAGES)
    create_pdf(f'{VERSIONS_DIR}/v3.pdf', V3_PAGES)
    create_pdf(f'{VERSIONS_DIR}/v4.pdf', V4_PAGES)
    create_pdf(f'{VERSIONS_DIR}/v5.pdf', V5_PAGES)

    print('All 5 PDF versions created in /home/user/versions/')

    # Open v1.pdf in evince
    launch_gui(f'evince "{VERSIONS_DIR}/v1.pdf"', delay_sec=2.0)
    print('GUI_READY: launched evince with v1.pdf on DISPLAY=:0')


create_initial()
