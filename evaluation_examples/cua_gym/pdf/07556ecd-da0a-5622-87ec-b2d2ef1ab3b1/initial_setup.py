"""
Initial Setup: GDPR compliance PDF scanner environment
Task ID: pdf_gf3_048
Domain: pdf

Creates 20 PDF files in /home/user/scan/ with various content.
Some contain personal data (emails, EU phone numbers, postal codes,
date of birth patterns, IBAN numbers, IP addresses).
Creates empty /home/user/scripts/ directory.
Opens file manager to show the scan directory.
"""

import os
import shlex
import subprocess
import time
import random

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_048'
SCAN_DIR = f'{WORKDIR}/scan'
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


def create_pdf(filepath, pages_content):
    """Create a PDF with given pages of text content."""
    import pymupdf
    doc = pymupdf.open()
    for page_text in pages_content:
        page = doc.new_page(width=595, height=842)
        # Insert text as a textbox
        rect = pymupdf.Rect(50, 50, 545, 792)
        page.insert_textbox(
            rect,
            page_text,
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=0,
        )
    doc.save(filepath)
    doc.close()


def create_initial():
    os.makedirs(SCAN_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Define 20 PDFs with varied content. Some contain personal data, some don't.
    pdf_specs = [
        {
            "filename": "employee_onboarding_guide.pdf",
            "pages": [
                "Employee Onboarding Guide\n\nWelcome to TechVision GmbH\n\n"
                "This guide covers the steps needed for new employee orientation.\n\n"
                "Contact HR at hr-team@techvision-gmbh.de for questions.\n"
                "Alternatively reach Maria Schneider at maria.schneider@techvision-gmbh.de\n\n"
                "Office phone: +49 30 12345678\n"
                "Emergency line: +49 89 98765432\n\n"
                "Our Berlin office is located at:\n"
                "Friedrichstrasse 42\n10117 Berlin, Germany",
                "Section 2: IT Setup\n\n"
                "Your workstation IP will be assigned from the range 192.168.1.100 to 192.168.1.200.\n"
                "VPN gateway: 10.0.0.1\n\n"
                "Submit your equipment request to it-support@techvision-gmbh.de\n"
                "Include your employee ID and date of birth for verification.\n"
                "Example format: DOB 15/03/1990\n\n"
                "IBAN for expense reimbursement: DE89 3704 0044 0532 0130 00"
            ]
        },
        {
            "filename": "quarterly_sales_report_q3.pdf",
            "pages": [
                "Quarterly Sales Report - Q3 2025\n\nTechVision GmbH\n\n"
                "Total Revenue: EUR 2,345,000\nGross Margin: 42.3%\n"
                "New Clients: 47\nChurn Rate: 2.1%\n\n"
                "Top Performing Region: DACH\nRevenue: EUR 890,000\n\n"
                "Sales Director: Klaus Weber\nReport compiled: September 2025",
                "Regional Breakdown:\n\n"
                "DACH Region: EUR 890,000\n"
                "Benelux: EUR 456,000\n"
                "Nordics: EUR 312,000\n"
                "Southern Europe: EUR 687,000\n\n"
                "Product Mix:\n"
                "Enterprise License: 65%\nSMB License: 25%\nConsulting: 10%"
            ]
        },
        {
            "filename": "customer_feedback_analysis.pdf",
            "pages": [
                "Customer Feedback Analysis 2025\n\n"
                "Survey respondent: Jean-Pierre Dubois\n"
                "Email: jp.dubois@example.fr\n"
                "Phone: +33 1 42 68 53 00\n"
                "Address: 75008 Paris, France\n\n"
                "Feedback: The platform has improved significantly. "
                "Response time decreased from 2.3s to 0.8s.\n"
                "Rating: 4.5/5\n\n"
                "Respondent DOB: 22-06-1985 (for loyalty program verification)",
                "Additional feedback entries:\n\n"
                "Respondent: Sofia Martinez\n"
                "Email: s.martinez@empresa.es\n"
                "Phone: +34 91 123 4567\n"
                "Postal code: 28001 Madrid\n\n"
                "Comment: Excellent customer support experience.\n"
                "Rating: 5/5\n\n"
                "Respondent: Lars Andersen\n"
                "Email: lars.andersen@firma.dk\n"
                "No phone provided\n"
                "Rating: 3.5/5"
            ]
        },
        {
            "filename": "infrastructure_audit_report.pdf",
            "pages": [
                "Infrastructure Audit Report\n\nDate: March 2025\nAuditor: External Security Team\n\n"
                "Network Topology:\n"
                "Primary DNS: 8.8.8.8\n"
                "Secondary DNS: 8.8.4.4\n"
                "Internal gateway: 172.16.0.1\n"
                "Web server cluster: 10.200.15.10, 10.200.15.11, 10.200.15.12\n"
                "Database server: 10.200.16.5\n"
                "Monitoring endpoint: 192.168.50.100\n\n"
                "Findings: 3 critical, 7 medium, 12 low severity issues identified.",
                "Detailed Findings:\n\n"
                "Critical-1: Unpatched Apache server at 10.200.15.10\n"
                "Critical-2: Default credentials on 10.200.16.5 admin panel\n"
                "Critical-3: Open port 22 on public IP 203.0.113.42\n\n"
                "Medium-1: SSL certificate expiring on 10.200.15.11\n"
                "Medium-2: Logging disabled on 172.16.0.1\n"
                "Medium-3: No rate limiting on API gateway 10.200.15.12"
            ]
        },
        {
            "filename": "vendor_contract_template.pdf",
            "pages": [
                "Vendor Service Agreement\n\nBetween: TechVision GmbH\n"
                "And: [Vendor Name]\n\n"
                "Effective Date: [Date]\nDuration: 12 months\n\n"
                "Payment Terms:\n"
                "Bank transfer to IBAN: DE44 5001 0517 5407 3249 31\n"
                "BIC: INGDDEFFXXX\n\n"
                "Contact for billing inquiries:\n"
                "accounts.payable@techvision-gmbh.de\n"
                "Phone: +49 69 7104 0000\n\n"
                "Governing Law: German Commercial Code (HGB)"
            ]
        },
        {
            "filename": "product_roadmap_2026.pdf",
            "pages": [
                "Product Roadmap 2026\n\nTechVision Platform\n\n"
                "Q1 2026: AI-powered analytics dashboard\n"
                "Q2 2026: Multi-language support expansion\n"
                "Q3 2026: Mobile app release (iOS and Android)\n"
                "Q4 2026: Enterprise SSO integration\n\n"
                "Budget Allocation:\n"
                "Engineering: EUR 1,200,000\n"
                "Design: EUR 300,000\n"
                "QA: EUR 200,000\n"
                "Infrastructure: EUR 500,000",
                "Technical Architecture:\n\n"
                "Microservices migration timeline\n"
                "Current monolith decomposition: 60% complete\n"
                "Target: 95% by Q2 2026\n\n"
                "Performance targets:\n"
                "API latency < 100ms (p99)\n"
                "Uptime: 99.95%\n"
                "Max concurrent users: 50,000"
            ]
        },
        {
            "filename": "gdpr_training_materials.pdf",
            "pages": [
                "GDPR Training Materials\n\nData Protection Basics\n\n"
                "Personal data includes any information relating to an identified "
                "or identifiable natural person.\n\n"
                "Examples of personal data:\n"
                "- Full name\n- Email address\n- Phone number\n"
                "- Date of birth\n- IP address\n- IBAN / bank details\n"
                "- Physical address / postal code\n\n"
                "Data processing requires a lawful basis under Article 6 GDPR.",
                "Data Subject Rights:\n\n"
                "1. Right of access (Art. 15)\n"
                "2. Right to rectification (Art. 16)\n"
                "3. Right to erasure (Art. 17)\n"
                "4. Right to restriction (Art. 18)\n"
                "5. Right to data portability (Art. 20)\n"
                "6. Right to object (Art. 21)\n\n"
                "Report breaches within 72 hours to the DPO.\n"
                "DPO contact: dpo@techvision-gmbh.de"
            ]
        },
        {
            "filename": "payroll_summary_march.pdf",
            "pages": [
                "Payroll Summary - March 2025\n\nConfidential\n\n"
                "Employee: Anna Müller\n"
                "DOB: 12/04/1988\n"
                "Email: anna.mueller@techvision-gmbh.de\n"
                "IBAN: DE75 5121 0800 1245 1261 99\n"
                "Gross Salary: EUR 6,500.00\n"
                "Net Salary: EUR 4,120.50\n\n"
                "Employee: Thomas Fischer\n"
                "DOB: 03/11/1992\n"
                "Email: t.fischer@techvision-gmbh.de\n"
                "IBAN: DE02 1203 0000 0000 2020 51\n"
                "Gross Salary: EUR 5,800.00\n"
                "Net Salary: EUR 3,690.00",
                "Employee: Eva Braun\n"
                "DOB: 27/09/1995\n"
                "Email: eva.braun@techvision-gmbh.de\n"
                "IBAN: DE68 2105 0170 0012 3456 78\n"
                "Gross Salary: EUR 7,200.00\n"
                "Net Salary: EUR 4,550.00\n\n"
                "Employee: Markus Schulz\n"
                "DOB: 15/01/1987\n"
                "Email: m.schulz@techvision-gmbh.de\n"
                "Phone: +49 171 2345678\n"
                "IBAN: DE89 3704 0044 0532 0130 00\n"
                "Gross Salary: EUR 8,100.00\n"
                "Net Salary: EUR 5,010.00"
            ]
        },
        {
            "filename": "meeting_notes_board.pdf",
            "pages": [
                "Board Meeting Notes\n\nDate: 15 February 2025\n"
                "Location: Conference Room A, Frankfurt Office\n\n"
                "Attendees:\n"
                "- Dr. Heinrich Vogel (CEO)\n"
                "- Claudia Becker (CFO)\n"
                "- Rainer Hoffmann (CTO)\n\n"
                "Agenda:\n"
                "1. Q4 2024 financial review\n"
                "2. 2025 strategic priorities\n"
                "3. M&A pipeline\n\n"
                "Key Decisions:\n"
                "- Approved EUR 2M investment in AI capabilities\n"
                "- Deferred acquisition of DataSync Solutions to Q3"
            ]
        },
        {
            "filename": "incident_response_log.pdf",
            "pages": [
                "Security Incident Response Log\n\n"
                "Incident ID: INC-2025-0042\nDate: 08 March 2025\n"
                "Severity: High\n\n"
                "Description: Unauthorized access attempt detected from IP 185.220.101.34\n"
                "Target: Customer database at 10.200.16.5\n\n"
                "Affected accounts:\n"
                "- user_id: 10234, email: petra.novak@client-a.cz\n"
                "- user_id: 10235, email: marco.rossi@client-b.it\n"
                "- user_id: 10236, email: elena.popova@client-c.bg\n\n"
                "Source IP geolocation: Eastern Europe\n"
                "Attack vector: SQL injection via search endpoint\n"
                "Status: Contained, patched within 4 hours",
                "Post-Incident Analysis:\n\n"
                "Timeline:\n"
                "14:22 UTC - First suspicious query from 185.220.101.34\n"
                "14:35 UTC - WAF triggered alert\n"
                "14:42 UTC - SOC analyst confirmed attack\n"
                "15:10 UTC - Source IP blocked at firewall\n"
                "18:15 UTC - Vulnerability patched\n\n"
                "Recommendations:\n"
                "1. Implement parameterized queries across all endpoints\n"
                "2. Enable IP reputation scoring on WAF\n"
                "3. Conduct penetration test by end of Q2"
            ]
        },
        {
            "filename": "office_lease_agreement.pdf",
            "pages": [
                "Commercial Lease Agreement\n\n"
                "Landlord: Immobilien AG\n"
                "Contact: vermieter@immobilien-ag.de\n"
                "Phone: +49 30 9876 5432\n\n"
                "Tenant: TechVision GmbH\n"
                "Represented by: Dr. Heinrich Vogel\n\n"
                "Property: Friedrichstrasse 42, 10117 Berlin\n"
                "Floor area: 850 sqm\n"
                "Monthly rent: EUR 12,750.00\n\n"
                "Rent payments to:\n"
                "IBAN: DE33 1002 0890 0012 3456 78\n"
                "Reference: LEASE-TV-2024"
            ]
        },
        {
            "filename": "api_documentation.pdf",
            "pages": [
                "TechVision API Documentation v3.2\n\n"
                "Base URL: https://api.techvision-platform.eu/v3\n\n"
                "Authentication:\n"
                "All requests require Bearer token in Authorization header.\n\n"
                "Endpoints:\n"
                "GET /users - List all users\n"
                "POST /users - Create user\n"
                "GET /users/{id} - Get user details\n"
                "PUT /users/{id} - Update user\n"
                "DELETE /users/{id} - Delete user\n\n"
                "Rate Limiting: 1000 requests per minute per API key\n"
                "Timeout: 30 seconds",
                "Error Codes:\n\n"
                "200 - OK\n400 - Bad Request\n401 - Unauthorized\n"
                "403 - Forbidden\n404 - Not Found\n429 - Rate Limited\n"
                "500 - Internal Server Error\n\n"
                "Webhook Configuration:\n"
                "POST /webhooks with callback URL\n"
                "Supported events: user.created, user.updated, order.completed\n\n"
                "SDK available for Python, Node.js, and Java."
            ]
        },
        {
            "filename": "travel_expense_claims.pdf",
            "pages": [
                "Travel Expense Report\n\n"
                "Employee: Sophie Laurent\n"
                "Email: sophie.laurent@techvision-gmbh.de\n"
                "Phone: +33 6 12 34 56 78\n"
                "Date of birth: 1991-07-14\n\n"
                "Trip: Paris Client Meeting\n"
                "Dates: 10-12 March 2025\n\n"
                "Expenses:\n"
                "Flight CDG-TXL: EUR 342.00\n"
                "Hotel (2 nights): EUR 480.00\n"
                "Meals: EUR 127.50\n"
                "Taxi: EUR 65.00\n"
                "Total: EUR 1,014.50\n\n"
                "Reimburse to IBAN: FR76 3000 6000 0112 3456 7890 189\n"
                "Postal code of residence: 75016 Paris"
            ]
        },
        {
            "filename": "company_policies_handbook.pdf",
            "pages": [
                "TechVision Employee Handbook\n\n"
                "Version 4.1 - January 2025\n\n"
                "Chapter 1: Working Hours\n"
                "Standard hours: 09:00 - 17:30 CET\n"
                "Flexible hours policy: Core hours 10:00 - 15:00\n\n"
                "Chapter 2: Leave Policy\n"
                "Annual leave: 30 days\nSick leave: As per German labor law\n"
                "Parental leave: Up to 3 years (Elternzeit)\n\n"
                "Chapter 3: Remote Work\n"
                "Up to 3 days per week remote work permitted\n"
                "VPN connection required for remote access",
                "Chapter 4: Code of Conduct\n\n"
                "All employees must adhere to the company code of conduct.\n"
                "Report violations to compliance@techvision-gmbh.de\n\n"
                "Chapter 5: Information Security\n"
                "Do not share credentials or access tokens.\n"
                "All devices must have disk encryption enabled.\n"
                "Report security incidents immediately.\n\n"
                "Chapter 6: Diversity & Inclusion\n"
                "TechVision is committed to a diverse and inclusive workplace."
            ]
        },
        {
            "filename": "client_database_export.pdf",
            "pages": [
                "Client Database Export - Confidential\n\n"
                "Export Date: 25 March 2025\n"
                "Record Count: 8\n\n"
                "Client: Müller & Partners\n"
                "Contact: Hans Müller\n"
                "Email: h.mueller@mueller-partners.de\n"
                "Phone: +49 221 987 6543\n"
                "Postal: 50667 Köln\n"
                "IBAN: DE91 1001 0010 0987 6543 21\n\n"
                "Client: Sanchez Consulting\n"
                "Contact: Isabella Sanchez\n"
                "Email: isabella@sanchez-consulting.es\n"
                "Phone: +34 93 876 5432\n"
                "Postal: 08001 Barcelona",
                "Client: Van den Berg Solutions\n"
                "Contact: Pieter van den Berg\n"
                "Email: pieter@vdb-solutions.nl\n"
                "Phone: +31 20 123 4567\n"
                "Postal: 1012 AB Amsterdam\n"
                "IBAN: NL91 ABNA 0417 1643 00\n\n"
                "Client: Rossi Technologies\n"
                "Contact: Giovanni Rossi\n"
                "Email: g.rossi@rossi-tech.it\n"
                "Phone: +39 02 1234 5678\n"
                "Postal: 20121 Milano\n"
                "IBAN: IT60 X054 2811 1010 0000 0123 456\n\n"
                "Client: Nordic Digital AS\n"
                "Contact: Erik Johansson\n"
                "Email: erik@nordic-digital.no\n"
                "Phone: +47 22 12 34 56\n"
                "Postal: 0150 Oslo"
            ]
        },
        {
            "filename": "server_migration_plan.pdf",
            "pages": [
                "Server Migration Plan\n\nProject: Cloud Migration Phase 2\n"
                "Lead: Rainer Hoffmann (CTO)\n\n"
                "Current Infrastructure:\n"
                "Web servers: 10.200.15.10, 10.200.15.11\n"
                "App servers: 10.200.20.1, 10.200.20.2, 10.200.20.3\n"
                "DB primary: 10.200.16.5\n"
                "DB replica: 10.200.16.6\n"
                "Cache: 10.200.30.10\n"
                "Message queue: 10.200.30.20\n\n"
                "Target: AWS eu-central-1\n"
                "Timeline: April - June 2025\n"
                "Budget: EUR 180,000"
            ]
        },
        {
            "filename": "marketing_campaign_brief.pdf",
            "pages": [
                "Marketing Campaign Brief\n\n"
                "Campaign: Spring Launch 2025\n"
                "Budget: EUR 75,000\n"
                "Duration: April 1 - May 31, 2025\n\n"
                "Target audience:\n"
                "- IT decision makers in DACH region\n"
                "- Company size: 200-5000 employees\n"
                "- Industries: Finance, Healthcare, Manufacturing\n\n"
                "Channels:\n"
                "- LinkedIn sponsored posts\n"
                "- Google Ads (search + display)\n"
                "- Industry newsletter placements\n"
                "- Webinar series (3 sessions)\n\n"
                "KPIs: 500 MQLs, 50 SQLs, 10 closed deals"
            ]
        },
        {
            "filename": "applicant_cv_portfolio.pdf",
            "pages": [
                "Curriculum Vitae\n\n"
                "Name: Katarina Novotna\n"
                "Date of Birth: 18.05.1993\n"
                "Email: k.novotna@personal-mail.cz\n"
                "Phone: +420 602 123 456\n"
                "Address: Vinohradska 12, 12000 Praha 2, Czech Republic\n\n"
                "Education:\n"
                "MSc Computer Science - Charles University, Prague (2017)\n"
                "BSc Mathematics - Masaryk University, Brno (2015)\n\n"
                "Experience:\n"
                "Senior Developer at DataFlow s.r.o. (2019-present)\n"
                "Junior Developer at CodeCraft a.s. (2017-2019)",
                "Name: Roberto Esposito\n"
                "Date of Birth: 03.12.1990\n"
                "Email: r.esposito@email.it\n"
                "Phone: +39 333 456 7890\n"
                "Address: Via Roma 45, 00184 Roma, Italy\n"
                "IBAN: IT40 S054 2811 1010 0000 0654 321\n\n"
                "Education:\n"
                "MSc Software Engineering - Sapienza University, Rome (2015)\n\n"
                "Experience:\n"
                "Lead Engineer at InnovateTech S.r.l. (2020-present)\n"
                "Backend Developer at WebAgency S.p.A. (2015-2020)"
            ]
        },
        {
            "filename": "data_processing_agreements.pdf",
            "pages": [
                "Data Processing Agreement (DPA)\n\n"
                "Between:\nData Controller: TechVision GmbH\n"
                "Data Processor: CloudHost Solutions B.V.\n"
                "Contact: legal@cloudhost.nl\n"
                "Phone: +31 70 345 6789\n\n"
                "Scope of Processing:\n"
                "- Customer contact data (name, email, phone)\n"
                "- Usage analytics\n"
                "- Payment information (IBAN, billing address)\n\n"
                "Sub-processors:\n"
                "1. AWS (Frankfurt, eu-central-1)\n"
                "2. Stripe (payment processing)\n"
                "3. SendGrid (email delivery)\n\n"
                "Data Retention: 36 months after contract termination"
            ]
        },
        {
            "filename": "internal_memo_restructuring.pdf",
            "pages": [
                "INTERNAL MEMO - CONFIDENTIAL\n\n"
                "From: Dr. Heinrich Vogel, CEO\n"
                "Date: 20 March 2025\n"
                "Re: Organizational Restructuring\n\n"
                "Dear Team,\n\n"
                "Following the strategic review, we are implementing the following changes:\n\n"
                "1. Engineering and Product departments will merge under CTO leadership\n"
                "2. New Data Science division to be established by Q2\n"
                "3. Regional offices in Amsterdam and Milan will expand\n\n"
                "These changes are effective from April 1, 2025.\n"
                "Questions can be directed to hr@techvision-gmbh.de\n\n"
                "Best regards,\nDr. Heinrich Vogel"
            ]
        },
    ]

    for spec in pdf_specs:
        filepath = os.path.join(SCAN_DIR, spec["filename"])
        create_pdf(filepath, spec["pages"])
        print(f"Created: {filepath}")

    print(f"\nCreated {len(pdf_specs)} PDF files in {SCAN_DIR}")
    print(f"Created empty scripts directory: {SCRIPTS_DIR}")

    # Open file manager to show scan directory
    launch_gui(f'nautilus "{SCAN_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')


create_initial()
