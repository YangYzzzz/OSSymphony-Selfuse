"""
Initial Setup: Create a 15-page project plan PDF with section headings in 14pt bold.
Task ID: pdf_fm_032
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_032'
OUTPUT = f'{WORKDIR}/Documents/project_plan.pdf'

# Section headings and which page (0-indexed) they appear on
HEADINGS = {
    0: "Project Overview",
    1: "Objectives",
    2: "Timeline",
    3: "Resources",
    4: "Risk Assessment",
}
# Budget Summary also on page 4 (second heading)
HEADING_PAGE4_EXTRA = "Budget Summary"

# Body content for each page to make it realistic
PAGE_CONTENT = {
    0: [
        "The Meridian Digital Transformation Initiative represents a comprehensive effort to modernize",
        "our organization's technology infrastructure and business processes. This project was initiated",
        "in response to growing market pressures and the need to remain competitive in an increasingly",
        "digital landscape. The initiative encompasses multiple workstreams spanning across engineering,",
        "operations, marketing, and customer success departments.",
        "",
        "Key stakeholders include the executive leadership team, department heads, and external",
        "technology partners. The project is sponsored by Chief Technology Officer Sarah Chen and",
        "managed by Senior Program Manager David Rodriguez.",
        "",
        "The expected duration of the project is 18 months, with phased delivery milestones",
        "scheduled at quarterly intervals. Total investment approved: $4.2 million.",
    ],
    1: [
        "The primary objectives of the Meridian Initiative are outlined below:",
        "",
        "1. Migrate legacy systems to cloud-native architecture by Q3 2026",
        "2. Implement automated CI/CD pipelines for all production services",
        "3. Reduce mean time to recovery (MTTR) from 4 hours to under 30 minutes",
        "4. Achieve 99.95% uptime SLA across all customer-facing applications",
        "5. Consolidate data warehousing into a unified analytics platform",
        "6. Enable real-time reporting dashboards for all business units",
        "7. Reduce infrastructure costs by 35% through optimization and consolidation",
        "",
        "Secondary objectives include improving developer experience, establishing a platform",
        "engineering team, and creating comprehensive API documentation for all internal services.",
        "These objectives align with the company's five-year strategic plan approved by the board.",
    ],
    2: [
        "Phase 1 - Discovery and Planning (Months 1-3):",
        "  - Conduct technology audit of existing systems",
        "  - Map dependencies and integration points",
        "  - Define migration strategy and sequence",
        "  - Establish governance and communication frameworks",
        "",
        "Phase 2 - Foundation (Months 4-6):",
        "  - Set up cloud infrastructure (AWS and Azure hybrid)",
        "  - Implement identity and access management overhaul",
        "  - Deploy monitoring and observability stack",
        "",
        "Phase 3 - Migration (Months 7-12):",
        "  - Migrate Tier 1 applications (CRM, ERP, billing)",
        "  - Migrate Tier 2 applications (internal tools, HR systems)",
        "  - Data migration and validation",
        "",
        "Phase 4 - Optimization (Months 13-18):",
        "  - Performance tuning and cost optimization",
        "  - Training and knowledge transfer",
        "  - Decommission legacy systems",
    ],
    3: [
        "The following resources have been allocated to the Meridian Initiative:",
        "",
        "Engineering Team:",
        "  - 8 Senior Software Engineers (full-time)",
        "  - 4 DevOps Engineers (full-time)",
        "  - 2 Data Engineers (full-time)",
        "  - 3 QA Engineers (part-time, 50% allocation)",
        "",
        "Infrastructure:",
        "  - AWS account with $150,000/month budget ceiling",
        "  - Azure tenant for hybrid workloads ($40,000/month)",
        "  - Development and staging environments",
        "",
        "External Partners:",
        "  - CloudBridge Consulting (cloud architecture advisory)",
        "  - Nexus Security (penetration testing and compliance)",
        "  - DataFlow Analytics (data migration specialists)",
        "",
        "Training Budget: $180,000 for certifications and workshops",
    ],
    4: [
        "Identified risks and mitigation strategies:",
        "",
        "R1 - Data Loss During Migration (Severity: Critical)",
        "  Mitigation: Triple-backup strategy with point-in-time recovery testing",
        "  Owner: Marcus Johnson, Lead Data Engineer",
        "",
        "R2 - Extended Downtime (Severity: High)",
        "  Mitigation: Blue-green deployment with automated rollback",
        "  Owner: Priya Patel, DevOps Lead",
        "",
        "R3 - Vendor Lock-in (Severity: Medium)",
        "  Mitigation: Multi-cloud strategy with abstraction layers",
        "  Owner: Alex Thompson, Cloud Architect",
        "",
        "R4 - Skill Gaps (Severity: Medium)",
        "  Mitigation: Training program and external consultants",
        "  Owner: Jennifer Wu, Engineering Manager",
    ],
}

# Additional pages (5-14) with filler content
ADDITIONAL_PAGES = {
    5: ("Stakeholder Analysis", [
        "This section identifies all project stakeholders and their interests.",
        "",
        "Executive Sponsors:",
        "  - Sarah Chen, CTO - Overall project accountability",
        "  - Michael Torres, CFO - Budget oversight and ROI tracking",
        "",
        "Department Representatives:",
        "  - Lisa Park, VP Engineering - Technical direction",
        "  - James Wilson, VP Operations - Process integration",
        "  - Maria Garcia, VP Marketing - Customer experience impact",
        "",
        "External Stakeholders:",
        "  - Board of Directors - Quarterly progress reviews",
        "  - Key enterprise clients - Migration communication plan",
        "  - Regulatory bodies - Compliance verification",
    ]),
    6: ("Communication Plan", [
        "Regular communication cadences established for the project:",
        "",
        "Weekly: Standup meetings (Mon/Wed/Fri) with core team",
        "Bi-weekly: Sprint reviews and retrospectives",
        "Monthly: Steering committee updates with executive sponsors",
        "Quarterly: Board presentation with KPIs and financial summary",
        "",
        "Communication channels:",
        "  - Slack: #meridian-project (daily updates)",
        "  - Confluence: Project wiki and documentation",
        "  - Jira: Task tracking and sprint management",
        "  - Email: Formal announcements and escalations",
    ]),
    7: ("Technical Architecture", [
        "The target architecture leverages microservices deployed on Kubernetes:",
        "",
        "Core Platform Services:",
        "  - API Gateway (Kong) for traffic management",
        "  - Service mesh (Istio) for inter-service communication",
        "  - Event streaming (Apache Kafka) for async processing",
        "  - Distributed caching (Redis Cluster) for performance",
        "",
        "Data Layer:",
        "  - PostgreSQL for transactional data",
        "  - MongoDB for document storage",
        "  - Elasticsearch for search and analytics",
        "  - S3/Blob Storage for binary assets",
        "",
        "Observability:",
        "  - Prometheus + Grafana for metrics",
        "  - Jaeger for distributed tracing",
        "  - ELK stack for centralized logging",
    ]),
    8: ("Security Requirements", [
        "Security measures to be implemented throughout the project:",
        "",
        "Authentication and Authorization:",
        "  - OAuth 2.0 / OpenID Connect for all services",
        "  - Role-based access control (RBAC) with least privilege",
        "  - Multi-factor authentication for all admin access",
        "",
        "Data Protection:",
        "  - AES-256 encryption at rest",
        "  - TLS 1.3 for all data in transit",
        "  - Data classification and handling procedures",
        "",
        "Compliance:",
        "  - SOC 2 Type II certification maintenance",
        "  - GDPR data processing requirements",
        "  - Annual penetration testing schedule",
    ]),
    9: ("Testing Strategy", [
        "Comprehensive testing approach for the migration:",
        "",
        "Unit Testing: Minimum 80% code coverage for all new services",
        "Integration Testing: API contract testing with Pact framework",
        "Performance Testing: Load testing with k6 simulating 10x current traffic",
        "Security Testing: OWASP Top 10 scanning with ZAP and Snyk",
        "UAT: Two-week user acceptance testing per phase",
        "",
        "Migration-Specific Testing:",
        "  - Data integrity validation (row counts, checksums)",
        "  - Feature parity verification against legacy systems",
        "  - Rollback procedure testing before each migration window",
        "  - Disaster recovery drills quarterly",
    ]),
    10: ("Change Management", [
        "Organizational change management plan:",
        "",
        "Impact Assessment:",
        "  - 200+ employees affected by new systems",
        "  - 15 business processes to be redesigned",
        "  - 8 legacy applications to be decommissioned",
        "",
        "Training Program:",
        "  - Week 1-2: Overview sessions for all staff",
        "  - Week 3-4: Hands-on workshops by department",
        "  - Week 5-6: Advanced training for power users",
        "  - Ongoing: Self-paced learning modules on LMS",
        "",
        "Support Plan:",
        "  - Dedicated help desk during transition (60 days)",
        "  - Champions network in each department",
        "  - FAQ and troubleshooting knowledge base",
    ]),
    11: ("Quality Metrics", [
        "Key performance indicators to measure project success:",
        "",
        "Technical Metrics:",
        "  - System uptime: Target 99.95% (current: 99.2%)",
        "  - API response time: P95 < 200ms (current: P95 = 850ms)",
        "  - Deployment frequency: Daily (current: bi-weekly)",
        "  - MTTR: < 30 minutes (current: 4 hours)",
        "",
        "Business Metrics:",
        "  - Infrastructure cost reduction: 35% by month 18",
        "  - Developer productivity: 40% improvement in velocity",
        "  - Customer satisfaction (CSAT): Maintain > 4.5/5.0",
        "  - Time to market for new features: 50% reduction",
    ]),
    12: ("Vendor Management", [
        "External vendor relationships and contracts:",
        "",
        "CloudBridge Consulting:",
        "  - Contract value: $420,000",
        "  - Duration: 12 months",
        "  - Deliverables: Architecture review, migration playbooks",
        "",
        "Nexus Security:",
        "  - Contract value: $95,000",
        "  - Duration: 18 months (quarterly engagements)",
        "  - Deliverables: Pen testing reports, compliance advisory",
        "",
        "DataFlow Analytics:",
        "  - Contract value: $280,000",
        "  - Duration: 6 months",
        "  - Deliverables: Data migration tooling, validation scripts",
    ]),
    13: ("Lessons Learned Template", [
        "This section will be populated throughout the project lifecycle.",
        "",
        "Format for each lesson:",
        "  - Date identified",
        "  - Phase/Sprint where encountered",
        "  - Description of the situation",
        "  - Impact on project (schedule, cost, quality)",
        "  - Root cause analysis",
        "  - Recommended action",
        "  - Status (Open / In Progress / Resolved)",
        "",
        "Review Schedule:",
        "  - Sprint retrospectives: Capture immediate lessons",
        "  - Phase gates: Consolidate and categorize lessons",
        "  - Project close: Final lessons learned workshop",
    ]),
    14: ("Appendix", [
        "Supporting documents and references:",
        "",
        "A. Original RFP for Cloud Migration Services",
        "B. Technology Vendor Evaluation Matrix",
        "C. Network Architecture Diagrams",
        "D. Data Flow Diagrams",
        "E. Compliance Checklist (SOC 2, GDPR)",
        "F. Glossary of Technical Terms",
        "G. Contact Directory for Project Team",
        "H. Escalation Procedures",
        "I. Change Request Form Template",
        "J. Meeting Minutes Archive Location",
        "",
        "All appendix documents are available on the project Confluence wiki",
        "at: https://meridian-project.atlassian.net/wiki/spaces/MDI",
    ]),
}


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
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # Pages 0-4: main sections with headings
    for page_idx in range(5):
        page = doc.new_page(width=595, height=842)  # A4

        heading = HEADINGS[page_idx]
        y = 72

        # Insert heading in 14pt bold
        page.insert_text(
            pymupdf.Point(72, y),
            heading,
            fontsize=14,
            fontname="hebo",  # Helvetica-Bold
            color=(0, 0, 0),
        )
        y += 30

        # If page 4, add extra heading "Budget Summary" lower on the page
        if page_idx == 4:
            # First add Risk Assessment body content
            body_lines = PAGE_CONTENT[page_idx]
            for line in body_lines:
                page.insert_text(
                    pymupdf.Point(72, y),
                    line,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 16

            y += 20
            # Add Budget Summary heading
            page.insert_text(
                pymupdf.Point(72, y),
                HEADING_PAGE4_EXTRA,
                fontsize=14,
                fontname="hebo",
                color=(0, 0, 0),
            )
            y += 30

            # Budget Summary body content
            budget_lines = [
                "Approved total budget: $4,200,000",
                "",
                "Breakdown by category:",
                "  Personnel costs: $2,100,000 (50%)",
                "  Cloud infrastructure: $1,050,000 (25%)",
                "  External consulting: $795,000 (19%)",
                "  Training and certifications: $180,000 (4%)",
                "  Contingency reserve: $75,000 (2%)",
                "",
                "Monthly burn rate (average): $233,333",
                "Projected completion within budget: Yes (5% contingency remaining)",
            ]
            for line in budget_lines:
                page.insert_text(
                    pymupdf.Point(72, y),
                    line,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 16
        else:
            # Regular body content
            body_lines = PAGE_CONTENT[page_idx]
            for line in body_lines:
                page.insert_text(
                    pymupdf.Point(72, y),
                    line,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 16

    # Pages 5-14: additional sections
    for page_idx in range(5, 15):
        page = doc.new_page(width=595, height=842)
        title, lines = ADDITIONAL_PAGES[page_idx]
        y = 72

        # These headings are in 12pt regular (NOT 14pt bold) - they are NOT section headings
        page.insert_text(
            pymupdf.Point(72, y),
            title,
            fontsize=12,
            fontname="hebo",
            color=(0.2, 0.2, 0.2),
        )
        y += 28

        for line in lines:
            page.insert_text(
                pymupdf.Point(72, y),
                line,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
            )
            y += 16

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
