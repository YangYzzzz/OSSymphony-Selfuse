"""
Initial Setup: PDF text replacement tool environment
Task ID: pdf_gf3_044
Domain: pdf

Creates:
- /home/user/docs/original.pdf (10-page business document)
- /home/user/config/replace_patterns.json (5 find/replace patterns)
- /home/user/scripts/ (empty directory for agent to create script in)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_044'

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


def create_original_pdf():
    """Create a realistic 10-page business document PDF."""
    import pymupdf

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # --- Page 1: Title Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "Nexora Technologies Inc.", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 170), "Annual Product Strategy Report", fontsize=20, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 210), "Fiscal Year 2024-2025", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 260), "Prepared by: Dr. Evelyn Hartfield", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 280), "Chief Product Officer", fontsize=11, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 310), "Date: March 15, 2024", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 340), "Classification: Internal - Confidential", fontsize=10, fontname="hebo", color=(0.6, 0, 0))
    page.insert_text(pymupdf.Point(72, 700), "Nexora Technologies Inc. | 1200 Innovation Drive, San Mateo, CA 94402", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    # --- Page 2: Table of Contents ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    toc_items = [
        ("1. Executive Summary", "3"),
        ("2. Product Portfolio Overview", "4"),
        ("3. CloudSync Platform Update", "5"),
        ("4. DataVault Enterprise Suite", "6"),
        ("5. Market Analysis & Competitors", "7"),
        ("6. Customer Feedback Summary", "8"),
        ("7. Revenue Projections", "9"),
        ("8. Strategic Recommendations", "10"),
    ]
    y = 120
    for title, pg in toc_items:
        page.insert_text(pymupdf.Point(90, y), title, fontsize=12, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(480, y), pg, fontsize=12, fontname="helv", color=(0, 0, 0))
        y += 28

    # --- Page 3: Executive Summary ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    exec_text = (
        "Nexora Technologies enters fiscal year 2025 with strong momentum across its core product lines. "
        "Our flagship CloudSync Platform has achieved 23% year-over-year growth, serving over 4,200 enterprise "
        "customers globally. The DataVault Enterprise Suite, launched in Q2 2024, has exceeded initial adoption "
        "targets by 35%.\n\n"
        "Key highlights from the period include:\n\n"
        "- CloudSync Platform revenue reached $142.8 million, up from $116.1 million in the prior year\n"
        "- DataVault Enterprise Suite onboarded 780 new accounts in its first full year\n"
        "- Customer retention rate improved to 94.2%, compared to 91.7% in the previous period\n"
        "- Dr. Evelyn Hartfield led the successful integration of AI-powered analytics into CloudSync\n\n"
        "Looking ahead to 2025, Nexora Technologies plans to invest heavily in machine learning capabilities "
        "and expand the DataVault product line with a new compliance module targeting healthcare and financial "
        "services sectors. The board has approved a $28.5 million R&D budget allocation for these initiatives.\n\n"
        "This report was prepared on March 15, 2024 by the Office of the Chief Product Officer."
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 700), exec_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 4: Product Portfolio Overview ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2. Product Portfolio Overview", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    portfolio_text = (
        "Nexora Technologies maintains three primary product lines as of March 15, 2024:\n\n"
        "CloudSync Platform (Launched 2019)\n"
        "Enterprise cloud synchronization and collaboration platform. Supports real-time document sharing, "
        "version control, and team workspaces. Current version: CloudSync 5.2.\n\n"
        "DataVault Enterprise Suite (Launched Q2 2024)\n"
        "Comprehensive data management and governance solution. Includes data cataloging, lineage tracking, "
        "quality monitoring, and compliance reporting. Dr. Evelyn Hartfield personally oversaw the architecture.\n\n"
        "NexGuard Security Module (Launched 2021)\n"
        "Integrated security layer providing encryption at rest and in transit, SSO integration, "
        "and audit logging. Compatible with both CloudSync and DataVault products.\n\n"
        "Product Ownership:\n"
        "- CloudSync Platform: Marcus Reeves (VP Engineering)\n"
        "- DataVault Enterprise Suite: Dr. Evelyn Hartfield (CPO)\n"
        "- NexGuard Security Module: Priya Venkatesh (Director of Security)\n\n"
        "All products are developed at our San Mateo headquarters by Nexora Technologies engineering teams."
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 720), portfolio_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 5: CloudSync Platform Update ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "3. CloudSync Platform Update", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    cs_text = (
        "The CloudSync Platform continued its growth trajectory throughout 2024. Key metrics as of "
        "March 15, 2024:\n\n"
        "Performance Metrics:\n"
        "- Monthly Active Users: 1.2 million (up 18% YoY)\n"
        "- Average Response Time: 45ms (improved from 62ms)\n"
        "- Uptime SLA Achievement: 99.97%\n"
        "- Storage Under Management: 8.4 PB\n\n"
        "Feature Releases in 2024:\n"
        "- CloudSync AI Assistant (January 2024): Natural language search and document summarization\n"
        "- Enhanced Collaboration Spaces (March 2024): Threaded discussions within shared workspaces\n"
        "- CloudSync Mobile 3.0 (June 2024): Redesigned mobile experience with offline capabilities\n"
        "- Enterprise Admin Dashboard (September 2024): Centralized management for IT administrators\n\n"
        "Notable Enterprise Deployments:\n"
        "- Meridian Financial Group: 12,000 seats deployed across 15 offices\n"
        "- Atlas Healthcare Systems: Integration with EHR platforms completed\n"
        "- Pinnacle Manufacturing: Factory floor data sync for IoT devices\n\n"
        "CloudSync remains the core revenue driver for Nexora Technologies."
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 720), cs_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 6: DataVault Enterprise Suite ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4. DataVault Enterprise Suite", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    dv_text = (
        "DataVault Enterprise Suite has completed its first full year since launch. Performance review "
        "as of March 15, 2024:\n\n"
        "Adoption Metrics:\n"
        "- Total Enterprise Accounts: 780\n"
        "- Data Sources Connected: 45,000+\n"
        "- Compliance Reports Generated: 2.1 million\n"
        "- Average Deployment Time: 6.2 weeks (down from 9.8 weeks at launch)\n\n"
        "Key Components:\n"
        "1. Data Catalog: Automated metadata discovery and classification\n"
        "2. Lineage Tracker: Visual data flow mapping across systems\n"
        "3. Quality Monitor: Rule-based and ML-driven data quality scoring\n"
        "4. Compliance Center: Pre-built templates for GDPR, HIPAA, SOX, and CCPA\n\n"
        "Customer Success Stories:\n"
        "- Sterling Insurance Corp: Reduced compliance audit preparation from 6 weeks to 3 days\n"
        "- Pacific Northwest Hospital Network: Achieved HIPAA compliance certification in record time\n"
        "- Greenfield Energy Solutions: Consolidated data from 200+ IoT sensors into unified catalog\n\n"
        "Dr. Evelyn Hartfield noted: 'DataVault represents Nexora Technologies' commitment to making "
        "data governance accessible and actionable for organizations of all sizes.'"
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 720), dv_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 7: Market Analysis ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "5. Market Analysis & Competitors", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    market_text = (
        "The enterprise software market continues to expand, with cloud-first solutions driving the "
        "majority of new deployments. Nexora Technologies maintains competitive positioning in two "
        "key segments.\n\n"
        "Cloud Collaboration Market (CloudSync):\n"
        "- Total Addressable Market: $48.2 billion (2024 estimate)\n"
        "- Nexora Technologies Market Share: 2.9%\n"
        "- Primary Competitors: Dropbox Business, Box Enterprise, Microsoft SharePoint\n"
        "- Differentiator: Real-time sync speed and developer API ecosystem\n\n"
        "Data Governance Market (DataVault):\n"
        "- Total Addressable Market: $12.7 billion (2024 estimate)\n"
        "- Nexora Technologies Market Share: 1.1% (first year)\n"
        "- Primary Competitors: Collibra, Alation, Informatica\n"
        "- Differentiator: Integrated compliance automation and ease of deployment\n\n"
        "Strategic Positioning:\n"
        "Nexora Technologies' unique advantage lies in offering both collaboration and governance "
        "in a unified platform. No competitor currently provides seamless integration between "
        "cloud collaboration tools and enterprise data governance. This integration capability "
        "positions Nexora Technologies favorably for large-scale enterprise contracts."
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 720), market_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 8: Customer Feedback ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "6. Customer Feedback Summary", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    feedback_text = (
        "Nexora Technologies conducted its annual customer satisfaction survey in February 2024, "
        "receiving 1,847 responses from enterprise account holders.\n\n"
        "Overall Satisfaction Score: 4.3/5.0 (up from 4.1/5.0)\n\n"
        "Top Positive Themes:\n"
        "- 'CloudSync's real-time collaboration is best in class' - IT Director, Meridian Financial\n"
        "- 'DataVault simplified our SOX compliance workflow enormously' - CFO, Sterling Insurance\n"
        "- 'Nexora Technologies support team resolves issues within hours, not days'\n"
        "- 'The API documentation for CloudSync is comprehensive and well-maintained'\n\n"
        "Top Areas for Improvement:\n"
        "- Mobile app performance on Android devices (addressed in CloudSync Mobile 3.0)\n"
        "- DataVault onboarding documentation needs expansion\n"
        "- Request for native integration with Salesforce CRM\n"
        "- NexGuard audit log export should support more formats\n\n"
        "Net Promoter Score: 52 (Industry Average: 38)\n\n"
        "Dr. Evelyn Hartfield has committed to addressing the top three improvement areas in the "
        "Q2 2025 product roadmap. The customer feedback review was completed on March 15, 2024."
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 720), feedback_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 9: Revenue Projections ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "7. Revenue Projections", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    revenue_text = (
        "Financial projections for Nexora Technologies fiscal year 2025, prepared March 15, 2024:\n\n"
        "CloudSync Platform:\n"
        "- FY2024 Actual: $142.8 million\n"
        "- FY2025 Projected: $175.6 million (+23% growth)\n"
        "- Key Driver: Enterprise tier upgrades and seat expansion\n\n"
        "DataVault Enterprise Suite:\n"
        "- FY2024 Actual: $24.3 million (partial year)\n"
        "- FY2025 Projected: $58.7 million (+142% growth)\n"
        "- Key Driver: Healthcare and financial services verticals\n\n"
        "NexGuard Security Module:\n"
        "- FY2024 Actual: $18.9 million\n"
        "- FY2025 Projected: $22.1 million (+17% growth)\n"
        "- Key Driver: Bundled sales with DataVault\n\n"
        "Total Revenue:\n"
        "- FY2024 Actual: $186.0 million\n"
        "- FY2025 Projected: $256.4 million (+37.8% growth)\n\n"
        "R&D Investment: $28.5 million (11.1% of projected revenue)\n"
        "Headcount Growth: 245 new positions planned (current: 1,180)\n\n"
        "These projections assume stable market conditions and successful execution of the "
        "healthcare compliance module launch in Q3 2025."
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 720), revenue_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 10: Strategic Recommendations ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "8. Strategic Recommendations", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    strat_text = (
        "Based on the analysis presented in this report, Dr. Evelyn Hartfield and the product "
        "leadership team at Nexora Technologies recommend the following strategic priorities "
        "for fiscal year 2025:\n\n"
        "1. Accelerate DataVault Healthcare Module\n"
        "   Priority: Critical | Timeline: Q3 2025 | Budget: $8.2 million\n"
        "   The healthcare vertical represents the largest near-term revenue opportunity for "
        "   DataVault. HIPAA compliance automation is the #1 requested feature.\n\n"
        "2. Launch CloudSync Developer Platform\n"
        "   Priority: High | Timeline: Q2 2025 | Budget: $5.4 million\n"
        "   Open CloudSync APIs to third-party developers to build marketplace integrations.\n\n"
        "3. Expand APAC Sales Team\n"
        "   Priority: High | Timeline: Q1 2025 | Budget: $4.8 million\n"
        "   Establish regional offices in Singapore and Tokyo to capture growing demand.\n\n"
        "4. Invest in AI/ML Research Lab\n"
        "   Priority: Medium | Timeline: Q2 2025 | Budget: $6.1 million\n"
        "   Build dedicated ML team for predictive analytics across all Nexora Technologies products.\n\n"
        "5. Strengthen Partner Ecosystem\n"
        "   Priority: Medium | Timeline: Ongoing | Budget: $4.0 million\n"
        "   Develop certified integration partnerships with Salesforce, ServiceNow, and Workday.\n\n"
        "Total Strategic Investment: $28.5 million\n\n"
        "Report prepared by Dr. Evelyn Hartfield, Chief Product Officer, Nexora Technologies.\n"
        "Date: March 15, 2024 | Classification: Internal - Confidential"
    )
    page.insert_textbox(pymupdf.Rect(72, 105, 540, 720), strat_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    output_path = f'{WORKDIR}/docs/original.pdf'
    doc.save(output_path)
    doc.close()
    print(f'Created: {output_path} ({len(doc) if False else 10} pages)')


def create_replace_patterns():
    """Create 5 find/replace patterns in JSON config."""
    patterns = [
        {
            "search": "Nexora Technologies",
            "replace": "Vantage Systems"
        },
        {
            "search": "CloudSync",
            "replace": "SkyBridge"
        },
        {
            "search": "Dr\\. Evelyn Hartfield",
            "replace": "[REDACTED]"
        },
        {
            "search": "March 15, 2024",
            "replace": "January 10, 2025"
        },
        {
            "search": "DataVault",
            "replace": "InfoKeeper"
        }
    ]
    output_path = f'{WORKDIR}/config/replace_patterns.json'
    with open(output_path, 'w') as f:
        json.dump(patterns, f, indent=2)
    print(f'Created: {output_path} ({len(patterns)} patterns)')


def create_initial():
    # Create directory structure
    os.makedirs(f'{WORKDIR}/docs', exist_ok=True)
    os.makedirs(f'{WORKDIR}/config', exist_ok=True)
    os.makedirs(f'{WORKDIR}/scripts', exist_ok=True)

    # Create the 10-page PDF
    create_original_pdf()

    # Create the replacement patterns config
    create_replace_patterns()

    print(f'Initial setup complete.')

    # GUI-ready: open a terminal so the agent can work
    launch_gui('bash -c "cd /home/user && xterm -geometry 100x40 -e bash"', delay_sec=1.0)
    # Also open the PDF so the agent can see the document
    launch_gui(f'evince "{WORKDIR}/docs/original.pdf"', delay_sec=2.0)
    print('GUI_READY: launched terminal and PDF viewer with DISPLAY=:0')


create_initial()
