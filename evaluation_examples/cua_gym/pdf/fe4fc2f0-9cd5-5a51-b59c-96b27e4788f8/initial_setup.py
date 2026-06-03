"""
Initial Setup: Create 25 PDF files in /home/user/library/ for thumbnail generator task
Task ID: pdf_gf3_034
Domain: pdf

Creates a digital library of 25 diverse PDF documents. No thumbnails directory,
no index.html, and no thumbnail_service.py should exist.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_034'
LIBRARY_DIR = f'{WORKDIR}/library'

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


# 25 PDF documents with realistic titles and content
PDF_CATALOG = [
    ("annual_report_2024.pdf", "Annual Financial Report 2024",
     "Meridian Corp Annual Report\n\nFiscal Year 2024\n\nRevenue: $42.3 Million\nNet Income: $8.7 Million\nTotal Assets: $156.2 Million\n\nThis report summarizes the financial performance of Meridian Corporation for the fiscal year ending December 31, 2024. Key highlights include a 12% increase in revenue driven by expansion into European markets and the successful launch of the Aurora product line.\n\nBoard of Directors:\n- Patricia Langford, Chair\n- David Okonkwo, CEO\n- Rachel Winters, CFO\n- James Tanaka, CTO"),

    ("employee_handbook.pdf", "Employee Handbook - 2025 Edition",
     "Northstar Industries Employee Handbook\n\nEffective January 1, 2025\n\nChapter 1: Company Overview\nNorthstar Industries was founded in 1987 and has grown to over 3,200 employees across 14 offices worldwide.\n\nChapter 2: Employment Policies\n- Standard work hours: 9:00 AM - 5:30 PM\n- Remote work: Up to 3 days per week\n- Probation period: 90 days\n\nChapter 3: Benefits\n- Health insurance (medical, dental, vision)\n- 401(k) with 6% company match\n- 20 days PTO annually"),

    ("project_proposal_atlas.pdf", "Project Atlas - Technical Proposal",
     "Project Atlas: Next-Generation Data Platform\n\nPrepared by: Engineering Division\nDate: March 15, 2025\n\nExecutive Summary\nProject Atlas aims to replace the legacy Oracle-based data warehouse with a modern cloud-native solution built on Apache Spark and Delta Lake.\n\nTimeline: 18 months\nBudget: $2.4 Million\nTeam Size: 12 engineers\n\nKey Deliverables:\n1. Data ingestion pipeline (Q2 2025)\n2. Analytics dashboard (Q3 2025)\n3. ML feature store (Q4 2025)\n4. Full migration (Q1 2026)"),

    ("meeting_minutes_q1.pdf", "Board Meeting Minutes - Q1 2025",
     "Board of Directors Meeting Minutes\nDate: March 28, 2025\nLocation: Conference Room A, HQ Building\n\nAttendees: P. Langford, D. Okonkwo, R. Winters, J. Tanaka, S. Morales\n\nAgenda:\n1. Q1 Financial Review - Revenue of $11.2M (up 8% YoY)\n2. Product Roadmap Update - Aurora v2.0 on track for June release\n3. Hiring Plan - 45 new positions approved for Q2\n4. Office Expansion - Singapore office lease signed\n\nAction Items:\n- R. Winters to present revised budget by April 10\n- J. Tanaka to finalize vendor selection for cloud migration"),

    ("marketing_strategy.pdf", "Digital Marketing Strategy 2025",
     "Digital Marketing Strategy\nFiscal Year 2025\n\nPrepared by: Marketing Department\nLead: Camille Dubois\n\nTarget Audience Analysis:\n- Enterprise B2B (45% of pipeline)\n- Mid-market SaaS companies (35%)\n- Startups and SMBs (20%)\n\nChannel Allocation:\n- Content Marketing: 30% of budget ($450K)\n- Paid Search (Google Ads): 25% ($375K)\n- Social Media (LinkedIn, Twitter): 20% ($300K)\n- Events and Webinars: 15% ($225K)\n- Email Campaigns: 10% ($150K)\n\nKPIs:\n- MQL target: 2,400/quarter\n- CAC target: < $1,200\n- Website traffic: +40% YoY"),

    ("technical_specification.pdf", "Aurora v2.0 Technical Specification",
     "Aurora v2.0 - Technical Specification Document\n\nVersion: 2.0.0-draft\nAuthor: James Tanaka, CTO\nReviewers: Engineering Team\n\nArchitecture Overview:\n- Microservices (Kubernetes)\n- Event-driven (Apache Kafka)\n- GraphQL API layer\n- PostgreSQL + Redis\n\nPerformance Requirements:\n- API latency: < 100ms (p99)\n- Throughput: 10,000 req/sec\n- Uptime: 99.95%\n\nSecurity:\n- OAuth 2.0 + OIDC\n- AES-256 encryption at rest\n- TLS 1.3 in transit\n- SOC 2 Type II compliance"),

    ("sales_report_march.pdf", "Sales Performance Report - March 2025",
     "Monthly Sales Report\nMarch 2025\n\nRegional Breakdown:\n\nNorth America:\n  New Deals: 34\n  Revenue: $3.8M\n  Top Rep: Michael Torres ($620K)\n\nEurope:\n  New Deals: 22\n  Revenue: $2.1M\n  Top Rep: Elise Bergman ($410K)\n\nAsia Pacific:\n  New Deals: 15\n  Revenue: $1.4M\n  Top Rep: Yuki Nakamura ($340K)\n\nTotal Pipeline: $18.7M\nWin Rate: 28%\nAverage Deal Size: $102K"),

    ("training_guide_onboarding.pdf", "New Employee Onboarding Guide",
     "Welcome to Northstar Industries!\n\nOnboarding Checklist\n\nWeek 1: Orientation\n- IT setup (laptop, email, VPN)\n- HR paperwork and benefits enrollment\n- Meet your team and manager\n- Office tour and safety briefing\n\nWeek 2: Product Training\n- Aurora platform overview\n- Customer demo walkthrough\n- Internal tools training (Jira, Confluence, Slack)\n\nWeek 3: Role-Specific Training\n- Shadow experienced team members\n- Complete first practice project\n- Set 30/60/90 day goals with manager\n\nKey Contacts:\n- IT Help Desk: helpdesk@northstar.com\n- HR: hr@northstar.com\n- Facilities: facilities@northstar.com"),

    ("research_paper_ml.pdf", "Machine Learning in Supply Chain Optimization",
     "Machine Learning Applications in Supply Chain Optimization\n\nAuthors: Dr. Priya Sharma, Dr. Liam Fitzgerald\nJournal of Operations Research, Vol. 47, 2024\n\nAbstract:\nThis paper examines the application of deep reinforcement learning to multi-echelon inventory optimization. We propose a novel algorithm, DRL-SCO, that reduces holding costs by 23% and stockout rates by 31% compared to traditional (s,S) policies.\n\nKeywords: supply chain, reinforcement learning, inventory optimization\n\n1. Introduction\nGlobal supply chains face increasing complexity...\n\n2. Related Work\nPrevious approaches include linear programming (Wagner-Whitin), simulation-based methods...\n\n3. Methodology\nWe formulate the problem as a Markov Decision Process..."),

    ("invoice_template.pdf", "Invoice #INV-2025-0847",
     "INVOICE\n\nFrom: Northstar Industries LLC\n123 Innovation Drive, San Jose, CA 95134\n\nTo: Quantum Dynamics Inc.\n456 Tech Boulevard, Austin, TX 78701\n\nInvoice #: INV-2025-0847\nDate: March 20, 2025\nDue Date: April 19, 2025\n\nDescription                    Qty    Rate      Amount\nAurora Platform License         5    $8,000    $40,000\nImplementation Services        120hr   $200    $24,000\nTraining (on-site)              3day  $2,500     $7,500\nAnnual Support Plan             1    $12,000    $12,000\n\nSubtotal:                                      $83,500\nTax (8.25%):                                    $6,889\nTotal:                                         $90,389"),

    ("compliance_policy.pdf", "Data Privacy and Compliance Policy",
     "Data Privacy and Compliance Policy\n\nEffective: January 1, 2025\nVersion: 3.2\nOwner: Legal Department\n\n1. Purpose\nThis policy establishes guidelines for handling personal data in compliance with GDPR, CCPA, and SOC 2 requirements.\n\n2. Scope\nApplies to all employees, contractors, and third-party vendors with access to company systems.\n\n3. Data Classification\n- Public: Marketing materials, press releases\n- Internal: Business plans, financial forecasts\n- Confidential: Customer PII, source code\n- Restricted: Encryption keys, auth tokens\n\n4. Retention\n- Customer data: 7 years after last interaction\n- Employee records: 5 years after termination\n- Financial records: 10 years"),

    ("product_catalog.pdf", "Aurora Product Family Catalog 2025",
     "Aurora Product Family\n2025 Edition\n\nAurora Core\n- Real-time data processing\n- REST and GraphQL APIs\n- Starting at $8,000/month\n\nAurora Analytics\n- Business intelligence dashboards\n- Custom report builder\n- Predictive analytics engine\n- Starting at $4,500/month\n\nAurora Connect\n- 150+ pre-built integrations\n- Custom connector SDK\n- Starting at $2,000/month\n\nAurora Shield\n- Advanced security suite\n- Threat detection\n- Compliance automation\n- Starting at $3,500/month\n\nEnterprise Bundle: All four products\nStarting at $15,000/month (save 17%)"),

    ("risk_assessment.pdf", "IT Security Risk Assessment Report",
     "IT Security Risk Assessment\nQ1 2025\n\nAssessment Team: InfoSec Division\nLead Assessor: Carlos Mendez, CISSP\n\nCritical Risks:\n1. Legacy VPN infrastructure (CVSS 8.7)\n   Mitigation: Migrate to Zero Trust by Q3\n\n2. Unpatched dev servers (CVSS 7.2)\n   Mitigation: Implement automated patching\n\n3. Third-party API key exposure (CVSS 6.8)\n   Mitigation: Deploy secrets vault\n\nMedium Risks:\n4. Insufficient logging on staging (CVSS 5.4)\n5. Weak password policy enforcement (CVSS 5.1)\n\nOverall Risk Score: 7.2 / 10 (High)\nRecommendation: Prioritize items 1-3 within 90 days"),

    ("budget_forecast_2025.pdf", "Annual Budget Forecast 2025-2026",
     "Annual Budget Forecast\nFiscal Years 2025-2026\n\nPrepared by: Rachel Winters, CFO\n\nRevenue Projections:\n  FY2025: $48.5M (projected)\n  FY2026: $58.2M (projected)\n  Growth Rate: 20% YoY\n\nOperating Expenses:\n  Salaries & Benefits: $24.8M\n  Cloud Infrastructure: $6.2M\n  Marketing: $4.5M\n  R&D: $5.1M\n  Office & Facilities: $3.2M\n  Professional Services: $1.8M\n  Total OpEx: $45.6M\n\nCapital Expenditure:\n  Office Buildout (Singapore): $2.1M\n  Equipment: $850K\n  Total CapEx: $2.95M\n\nProjected EBITDA: $12.4M (FY2025)"),

    ("user_manual_aurora.pdf", "Aurora Platform User Manual",
     "Aurora Platform User Manual\n\nVersion 1.8\nLast Updated: February 2025\n\nGetting Started\n\n1. Login to Aurora\n   Navigate to https://app.aurora.io\n   Enter your credentials\n   Complete MFA verification\n\n2. Dashboard Overview\n   The main dashboard displays:\n   - Active data pipelines\n   - System health metrics\n   - Recent alerts\n   - Quick action buttons\n\n3. Creating a Pipeline\n   Step 1: Click 'New Pipeline'\n   Step 2: Select data source\n   Step 3: Configure transformations\n   Step 4: Set destination\n   Step 5: Define schedule\n   Step 6: Review and deploy\n\n4. Troubleshooting\n   Error codes and solutions..."),

    ("quarterly_review_q4.pdf", "Quarterly Business Review - Q4 2024",
     "Quarterly Business Review\nQ4 2024 (October - December)\n\nExecutive Summary:\nQ4 closed strongly with $12.8M in revenue, exceeding target by 7%.\n\nKey Metrics:\n- ARR: $45.2M (up from $39.8M)\n- Net Revenue Retention: 118%\n- Gross Margin: 74%\n- Customer Count: 847 (net +62)\n\nProduct Updates:\n- Aurora v1.8 released (November)\n- 99.97% uptime achieved\n- 34 new integrations shipped\n\nCustomer Wins:\n- Quantum Dynamics ($420K ACV)\n- Stellar Financial ($380K ACV)\n- NovaTech Solutions ($290K ACV)\n\nChallenges:\n- Engineering hiring 15% behind plan\n- APAC expansion slower than projected"),

    ("design_guidelines.pdf", "Brand Design Guidelines",
     "Northstar Industries\nBrand Design Guidelines\n\nVersion 2.1 | 2025\n\nPrimary Colors:\n- Northstar Blue: #003D7A\n- Signal Orange: #FF6B35\n- Slate Gray: #4A5568\n\nSecondary Colors:\n- Sky Blue: #74B9FF\n- Warm White: #FAFAF9\n- Deep Navy: #001F3F\n\nTypography:\n- Headlines: Inter Bold, 24-48pt\n- Body: Inter Regular, 14-16pt\n- Code: JetBrains Mono, 13pt\n\nLogo Usage:\n- Minimum size: 32px height\n- Clear space: 1x logo height on all sides\n- Never stretch, rotate, or recolor\n\nPhotography Style:\n- Natural lighting\n- Authentic workplace scenes\n- Diverse representation"),

    ("incident_report_20250312.pdf", "Incident Report - Service Outage March 12",
     "Incident Report\n\nIncident ID: INC-2025-0312\nSeverity: P1 (Critical)\nDate: March 12, 2025\nDuration: 2 hours 17 minutes (14:23 - 16:40 UTC)\n\nSummary:\nComplete service outage affecting all Aurora platform users due to cascading failure in the authentication service.\n\nRoot Cause:\nA routine database migration script contained an unvalidated index drop that locked the users table. The auth service connection pool exhausted within 3 minutes, causing all API requests to fail.\n\nImpact:\n- 847 customers affected\n- Estimated revenue impact: $45,000\n- SLA credits issued: $12,300\n\nCorrective Actions:\n1. Migration scripts now require staging environment testing\n2. Circuit breaker added to auth service\n3. Connection pool monitoring alerts implemented"),

    ("vendor_contract_cloudpeak.pdf", "Vendor Agreement - CloudPeak Systems",
     "SERVICE AGREEMENT\n\nBetween: Northstar Industries LLC (Client)\nAnd: CloudPeak Systems Inc. (Provider)\n\nEffective Date: April 1, 2025\nTerm: 36 months\n\nServices:\n- Managed Kubernetes cluster hosting\n- 24/7 infrastructure monitoring\n- Disaster recovery (RPO: 15min, RTO: 1hr)\n- Monthly capacity planning reviews\n\nPricing:\n- Base fee: $18,500/month\n- Overage (CPU): $0.12/core-hour\n- Overage (Storage): $0.08/GB-month\n- Annual escalation: max 5%\n\nSLA:\n- Uptime guarantee: 99.95%\n- Response time P1: 15 minutes\n- Response time P2: 1 hour\n- Penalty: 10% monthly credit per 0.1% below SLA"),

    ("performance_review_template.pdf", "Performance Review Template 2025",
     "Annual Performance Review\n\nEmployee Name: _________________________\nDepartment: ___________________________\nReview Period: January - December 2025\nManager: ______________________________\n\nSection 1: Goals Achievement (40%)\nGoal 1: ________________________________\nRating: 1  2  3  4  5\nComments: ______________________________\n\nGoal 2: ________________________________\nRating: 1  2  3  4  5\nComments: ______________________________\n\nSection 2: Core Competencies (30%)\n- Communication:     1  2  3  4  5\n- Technical Skills:  1  2  3  4  5\n- Teamwork:          1  2  3  4  5\n- Leadership:        1  2  3  4  5\n\nSection 3: Development Plan (30%)\nStrengths: _____________________________\nAreas for Growth: ______________________\nTraining Needs: ________________________"),

    ("architecture_diagram_notes.pdf", "System Architecture Documentation",
     "System Architecture Documentation\nAurora Platform v2.0\n\nLayer 1: Client Layer\n- Web Application (React 18)\n- Mobile SDK (iOS/Android)\n- CLI Tool (Go)\n\nLayer 2: API Gateway\n- Kong API Gateway\n- Rate limiting: 1000 req/min per client\n- JWT validation\n- Request routing\n\nLayer 3: Service Mesh\n- Auth Service (Node.js)\n- Pipeline Service (Python/FastAPI)\n- Analytics Service (Scala/Spark)\n- Notification Service (Go)\n\nLayer 4: Data Layer\n- PostgreSQL 15 (primary)\n- Redis 7 (caching)\n- Apache Kafka (event streaming)\n- MinIO (object storage)\n- Elasticsearch (search/logging)\n\nInfrastructure:\n- AWS EKS (Kubernetes)\n- Terraform for IaC\n- ArgoCD for GitOps"),

    ("customer_survey_results.pdf", "Customer Satisfaction Survey Results 2024",
     "Customer Satisfaction Survey\nAnnual Results - 2024\n\nResponse Rate: 42% (356 / 847 customers)\n\nOverall Satisfaction: 4.2 / 5.0\n\nCategory Scores:\n- Product Reliability: 4.4 / 5.0\n- Customer Support: 3.9 / 5.0\n- Documentation: 3.6 / 5.0\n- Value for Money: 4.0 / 5.0\n- Onboarding Experience: 4.1 / 5.0\n\nNet Promoter Score (NPS): 52\n- Promoters (9-10): 62%\n- Passives (7-8): 28%\n- Detractors (0-6): 10%\n\nTop Requested Features:\n1. Advanced reporting (67%)\n2. Mobile app improvements (54%)\n3. Custom dashboards (48%)\n4. Better API documentation (41%)\n5. SSO for all plans (38%)"),

    ("travel_expense_policy.pdf", "Travel and Expense Policy",
     "Travel and Expense Reimbursement Policy\n\nEffective: January 2025\nApplies to: All full-time and contract employees\n\nAir Travel:\n- Domestic: Economy class\n- International (< 6 hours): Economy Plus\n- International (> 6 hours): Business class (VP+ only)\n\nHotel:\n- Maximum nightly rate: $250 (domestic), $350 (international)\n- Exceptions require director approval\n\nMeals (per diem):\n- Breakfast: $20\n- Lunch: $30\n- Dinner: $50\n- International: 1.5x domestic rates\n\nRental Car:\n- Compact or midsize only\n- GPS and toll transponder allowed\n\nExpense Reports:\n- Submit within 14 days of travel\n- Receipts required for all expenses over $25\n- Manager approval within 5 business days"),

    ("release_notes_v18.pdf", "Aurora v1.8 Release Notes",
     "Aurora Platform v1.8 Release Notes\nRelease Date: November 15, 2024\n\nNew Features:\n- Real-time collaboration on pipeline editing\n- Custom dashboard builder with drag-and-drop\n- Webhook support for 34 new integrations\n- Advanced query optimizer (3x faster aggregations)\n\nImprovements:\n- Pipeline deployment time reduced by 40%\n- Memory usage optimization for large datasets\n- Updated UI with dark mode support\n- Enhanced audit logging\n\nBug Fixes:\n- Fixed intermittent timeout on data export (#4521)\n- Resolved CSV parsing issue with Unicode (#4487)\n- Fixed dashboard filter persistence (#4503)\n- Corrected timezone display in scheduler (#4519)\n\nDeprecations:\n- Legacy REST API v1 (sunset: June 2025)\n- MySQL connector v1 (use v2)\n\nKnown Issues:\n- Dark mode may not render correctly in Safari 16"),

    ("disaster_recovery_plan.pdf", "Business Continuity & Disaster Recovery Plan",
     "Business Continuity & Disaster Recovery Plan\n\nDocument ID: BC-DR-2025-001\nClassification: Confidential\nLast Review: February 28, 2025\nNext Review: August 31, 2025\n\nRecovery Objectives:\n- RPO (Recovery Point Objective): 15 minutes\n- RTO (Recovery Time Objective): 1 hour\n- MTPD (Maximum Tolerable Period of Disruption): 4 hours\n\nPrimary Site: AWS us-east-1 (Virginia)\nDR Site: AWS eu-west-1 (Ireland)\n\nFailover Procedure:\n1. Incident commander declares disaster\n2. Route 53 health check triggers DNS failover\n3. DR database promoted to primary (< 5 min)\n4. Verify service health on DR region\n5. Notify customers via status page\n6. Begin root cause analysis on primary\n\nCommunication Tree:\n- L1: On-call SRE team (PagerDuty)\n- L2: VP Engineering (phone call)\n- L3: CTO + CEO (within 30 minutes)\n- L4: Customer communication (within 1 hour)"),
]


def create_pdf(filepath, title, content):
    """Create a single PDF file with realistic content."""
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        title,
        fontsize=18,
        fontname="hebo",
        color=(0, 0.24, 0.48),
    )

    # Horizontal rule under title
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(540, 70))
    shape.finish(color=(0, 0.24, 0.48), width=1.5)
    shape.commit()

    # Body content in a textbox
    rect = pymupdf.Rect(72, 90, 540, 740)
    page.insert_textbox(
        rect,
        content,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer
    page.insert_text(
        pymupdf.Point(72, 770),
        "Northstar Industries - Confidential",
        fontsize=8,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(filepath)
    doc.close()


def create_initial():
    # Ensure library directory exists
    os.makedirs(LIBRARY_DIR, exist_ok=True)

    # Make sure thumbnails directory does NOT exist
    thumbnails_dir = os.path.join(LIBRARY_DIR, 'thumbnails')
    if os.path.exists(thumbnails_dir):
        import shutil
        shutil.rmtree(thumbnails_dir)

    # Make sure scripts dir does NOT exist
    scripts_dir = f'{WORKDIR}/scripts'
    if os.path.exists(scripts_dir):
        import shutil
        shutil.rmtree(scripts_dir)

    # Make sure index.html does NOT exist
    index_path = os.path.join(LIBRARY_DIR, 'index.html')
    if os.path.exists(index_path):
        os.remove(index_path)

    # Create all 25 PDFs
    for filename, title, content in PDF_CATALOG:
        filepath = os.path.join(LIBRARY_DIR, filename)
        create_pdf(filepath, title, content)
        print(f'Created: {filepath}')

    print(f'\nCreated {len(PDF_CATALOG)} PDF files in {LIBRARY_DIR}')

    # Open file manager to show library directory (GUI-ready state)
    launch_gui(f'nautilus "{LIBRARY_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
