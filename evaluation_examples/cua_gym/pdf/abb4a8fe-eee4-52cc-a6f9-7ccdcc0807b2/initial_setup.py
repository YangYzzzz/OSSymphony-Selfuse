"""
Initial Setup: Create a 22-page project proposal PDF with no headers/footers
Task ID: pdf_gf2_034
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
DOCS_DIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf2_034'
OUTPUT = f'{DOCS_DIR}/proposal_final.pdf'

LETTER_W, LETTER_H = 612, 792

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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Define realistic proposal content for 22 pages
    sections = [
        ("Project Proposal 2026", [
            "Prepared by: Meridian Consulting Group",
            "Client: Northstar Technologies Inc.",
            "Date: March 15, 2026",
            "Version: 3.2 (Final Draft)",
            "",
            "Confidential - For Internal Review Only",
            "",
            "This document outlines the comprehensive strategy for the digital transformation "
            "initiative at Northstar Technologies Inc., covering infrastructure modernization, "
            "cloud migration, and enterprise application integration across all business units.",
        ]),
        ("1. Executive Summary", [
            "Northstar Technologies Inc. is embarking on a multi-phase digital transformation "
            "program designed to modernize its core infrastructure, streamline operations, and "
            "position the organization for sustained growth over the next five years.",
            "",
            "The proposed initiative encompasses three primary workstreams: (1) cloud infrastructure "
            "migration, (2) enterprise application consolidation, and (3) data analytics platform "
            "deployment. The total investment required is estimated at $4.7 million over 24 months, "
            "with projected annual cost savings of $1.2 million beginning in Year 3.",
            "",
            "Key benefits include a 40% reduction in IT operational costs, 99.99% system uptime, "
            "enhanced cybersecurity posture, and a unified data platform enabling real-time "
            "business intelligence across all departments.",
            "",
            "The project will be executed in four phases, with clear milestones and deliverables "
            "at each stage. A dedicated governance structure will ensure alignment with corporate "
            "strategy and timely delivery of outcomes.",
        ]),
        ("2. Current State Assessment", [
            "2.1 Infrastructure Overview",
            "",
            "Northstar Technologies currently operates a hybrid IT environment comprising two "
            "on-premises data centers (Dallas and Chicago), legacy ERP systems (SAP R/3), and "
            "a patchwork of cloud services across AWS and Azure. The infrastructure supports "
            "approximately 3,200 employees across 14 office locations.",
            "",
            "The Dallas data center, commissioned in 2012, houses 280 physical servers running "
            "a mix of Windows Server 2016 and Red Hat Enterprise Linux 7. The Chicago facility, "
            "established in 2015, serves primarily as a disaster recovery site with 120 servers.",
            "",
            "2.2 Application Landscape",
            "",
            "The current application portfolio includes 47 business applications, of which 18 are "
            "classified as mission-critical. Notable systems include:",
            "  - SAP R/3 ERP (Finance, HR, Supply Chain) - Version 4.7, deployed 2008",
            "  - Salesforce CRM - Enterprise Edition, 850 active users",
            "  - Microsoft 365 - Full suite, 3,200 licenses",
            "  - Custom inventory management system (Java/Oracle) - Deployed 2014",
            "  - Legacy payroll system (COBOL-based) - Deployed 1998",
            "",
            "2.3 Pain Points and Challenges",
            "",
            "Through interviews with 45 stakeholders across 8 departments and analysis of "
            "12 months of incident data, the following critical pain points were identified:",
            "",
            "  1. System downtime averaging 47 hours per quarter, primarily attributed to aging "
            "     hardware and inadequate failover mechanisms",
            "  2. Data silos preventing cross-departmental reporting and analytics",
            "  3. Manual processes consuming an estimated 12,000 person-hours annually",
            "  4. Security vulnerabilities in legacy systems lacking vendor support",
            "  5. Inability to scale infrastructure to meet seasonal demand fluctuations",
        ]),
        ("3. Proposed Solution Architecture", [
            "3.1 Cloud Migration Strategy",
            "",
            "We propose a phased migration to Amazon Web Services (AWS) as the primary cloud "
            "provider, leveraging a lift-and-shift approach for non-critical workloads and a "
            "re-architecture strategy for mission-critical applications.",
            "",
            "The target architecture will utilize the following AWS services:",
            "  - Amazon EC2 with Auto Scaling for compute workloads",
            "  - Amazon RDS (PostgreSQL) for relational database needs",
            "  - Amazon S3 for object storage and data lake foundation",
            "  - AWS Lambda for serverless microservices",
            "  - Amazon CloudWatch for monitoring and observability",
            "  - AWS CloudFormation for infrastructure as code",
            "",
            "3.2 Enterprise Application Consolidation",
            "",
            "The application consolidation effort will reduce the portfolio from 47 to 28 "
            "applications through a combination of retirement (12 apps), replacement (4 apps), "
            "and integration (3 apps). The remaining applications will be containerized using "
            "Docker and orchestrated via Amazon EKS (Kubernetes).",
            "",
            "3.3 Data Analytics Platform",
            "",
            "A centralized data analytics platform will be built on AWS, featuring:",
            "  - Data ingestion pipelines using AWS Glue and Kinesis",
            "  - Data warehouse on Amazon Redshift (ra3.xlplus, 6-node cluster)",
            "  - Business intelligence layer powered by Tableau Server",
            "  - Machine learning capabilities via Amazon SageMaker",
            "  - Real-time dashboards for executive decision-making",
        ]),
        ("4. Implementation Roadmap", [
            "4.1 Phase 1: Foundation (Months 1-6)",
            "",
            "The foundation phase establishes the cloud landing zone, security framework, and "
            "governance structure required for subsequent phases.",
            "",
            "Key deliverables:",
            "  - AWS landing zone with multi-account strategy",
            "  - Identity and Access Management (IAM) framework",
            "  - Network architecture (VPC, Transit Gateway, Direct Connect)",
            "  - CI/CD pipeline using AWS CodePipeline and GitHub Actions",
            "  - Security baseline (GuardDuty, Security Hub, WAF)",
            "",
            "Estimated cost: $380,000 (professional services: $280,000, infrastructure: $100,000)",
            "",
            "4.2 Phase 2: Migration Wave 1 (Months 4-12)",
            "",
            "The first migration wave targets non-critical workloads and development/testing "
            "environments. Approximately 120 servers will be migrated using AWS Application "
            "Migration Service (MGN).",
            "",
            "Workloads in scope:",
            "  - Development and staging environments (34 servers)",
            "  - Internal collaboration tools (12 servers)",
            "  - File and print services (8 servers)",
            "  - Non-production databases (18 servers)",
            "  - Web applications - internal (14 servers)",
            "  - Monitoring and logging infrastructure (6 servers)",
            "",
            "Estimated cost: $920,000",
        ]),
        ("4. Implementation Roadmap (continued)", [
            "4.3 Phase 3: Migration Wave 2 (Months 10-18)",
            "",
            "The second migration wave addresses mission-critical production workloads, "
            "requiring careful planning, extensive testing, and coordinated cutover windows.",
            "",
            "Applications in scope:",
            "  - SAP migration to SAP S/4HANA on AWS (lift-and-transform)",
            "  - Custom inventory system re-platforming to containerized architecture",
            "  - Oracle database migration to Amazon RDS PostgreSQL",
            "  - Legacy payroll system replacement with Workday HCM",
            "",
            "This phase includes a 90-day parallel-run period for each critical application "
            "to ensure stability and data integrity before decommissioning legacy systems.",
            "",
            "Estimated cost: $1,850,000",
            "",
            "4.4 Phase 4: Optimization and Analytics (Months 16-24)",
            "",
            "The final phase focuses on deploying the data analytics platform, optimizing "
            "cloud spend, and establishing ongoing operational excellence practices.",
            "",
            "Deliverables:",
            "  - Data lake and warehouse deployment",
            "  - ETL pipeline development for all data sources",
            "  - Executive dashboard suite (12 dashboards)",
            "  - Cost optimization review and Reserved Instance purchases",
            "  - Operational runbook documentation",
            "  - Knowledge transfer and staff training program",
            "",
            "Estimated cost: $1,550,000",
        ]),
        ("5. Project Governance", [
            "5.1 Governance Structure",
            "",
            "The project will operate under a three-tier governance model:",
            "",
            "Steering Committee (Monthly):",
            "  - CIO: Sarah Mitchell (Executive Sponsor)",
            "  - CFO: David Park",
            "  - VP Engineering: Rachel Torres",
            "  - VP Operations: James Crawford",
            "  - Program Director: Michael Nguyen (Meridian)",
            "",
            "Project Management Office (Weekly):",
            "  - Program Manager: Lisa Chen (Meridian)",
            "  - Technical Lead: Alexander Petrov (Meridian)",
            "  - Infrastructure Lead: Karen Williams (Northstar)",
            "  - Application Lead: Robert Kim (Northstar)",
            "  - Security Lead: Diana Foster (Northstar)",
            "",
            "Delivery Teams (Daily Standups):",
            "  - Cloud Infrastructure Team (6 engineers)",
            "  - Application Migration Team (8 engineers)",
            "  - Data Engineering Team (5 engineers)",
            "  - Quality Assurance Team (4 engineers)",
            "  - Change Management Team (3 specialists)",
            "",
            "5.2 Communication Plan",
            "",
            "Regular communication cadence will include:",
            "  - Weekly status reports distributed to all stakeholders",
            "  - Monthly steering committee presentations",
            "  - Quarterly town halls for broader organization awareness",
            "  - Dedicated Slack channels for real-time collaboration",
            "  - SharePoint site for document repository and knowledge base",
        ]),
        ("6. Risk Assessment", [
            "6.1 Risk Register",
            "",
            "ID  | Risk Description                           | Likelihood | Impact | Mitigation",
            "----|-------------------------------------------|------------|--------|------------------",
            "R01 | Data loss during migration                 | Low        | Critical| Automated backup verification",
            "R02 | Vendor lock-in with AWS services           | Medium     | High   | Multi-cloud abstraction layer",
            "R03 | Staff resistance to new systems            | High       | Medium | Change management program",
            "R04 | Budget overrun exceeding 15%               | Medium     | High   | Monthly financial reviews",
            "R05 | Timeline delays in SAP migration           | Medium     | Critical| 30-day schedule buffer",
            "R06 | Security breach during transition          | Low        | Critical| Enhanced monitoring during cutover",
            "R07 | Key personnel attrition                    | Medium     | High   | Knowledge redundancy, documentation",
            "R08 | Integration failures between systems       | Medium     | High   | Comprehensive integration testing",
            "R09 | Performance degradation post-migration     | Low        | Medium | Performance baseline and monitoring",
            "R10 | Regulatory compliance gaps                 | Low        | Critical| Compliance audit at each phase gate",
            "",
            "6.2 Risk Mitigation Strategy",
            "",
            "Each identified risk has been assigned a dedicated owner from the project team. "
            "Risk reviews will be conducted bi-weekly, with escalation procedures defined for "
            "any risk that exceeds its acceptable threshold. A contingency budget of $470,000 "
            "(10% of total project cost) has been allocated to address unforeseen challenges.",
            "",
            "For critical risks (R01, R05, R06, R10), additional safeguards include:",
            "  - Automated rollback procedures for all migration activities",
            "  - Dual-environment running during transition periods",
            "  - 24/7 security operations center monitoring during cutover weekends",
            "  - Pre-migration compliance certification from external auditors",
        ]),
        ("7. Budget and Financial Analysis", [
            "7.1 Cost Breakdown",
            "",
            "Category                          | Year 1      | Year 2      | Total",
            "----------------------------------|-------------|-------------|------------",
            "Professional Services (Meridian)   | $1,800,000  | $1,200,000  | $3,000,000",
            "AWS Infrastructure                 | $420,000    | $580,000    | $1,000,000",
            "Software Licenses                  | $180,000    | $120,000    | $300,000",
            "Training and Change Management     | $150,000    | $100,000    | $250,000",
            "Contingency (10%)                  | $255,000    | $215,000    | $470,000",
            "----------------------------------|-------------|-------------|------------",
            "TOTAL                              | $2,805,000  | $2,215,000  | $5,020,000",
            "",
            "Note: The contingency allocation of $470,000 provides buffer for scope adjustments "
            "and unforeseen technical challenges. Unused contingency will be returned to the "
            "general IT capital budget at project close.",
            "",
            "7.2 Return on Investment",
            "",
            "The projected ROI analysis demonstrates a positive return beginning in Year 3:",
            "",
            "  Year 1: Investment of $2,805,000 (net: -$2,805,000)",
            "  Year 2: Investment of $2,215,000, savings of $400,000 (net: -$1,815,000)",
            "  Year 3: Maintenance of $600,000, savings of $1,200,000 (net: +$600,000)",
            "  Year 4: Maintenance of $550,000, savings of $1,400,000 (net: +$850,000)",
            "  Year 5: Maintenance of $500,000, savings of $1,600,000 (net: +$1,100,000)",
            "",
            "Cumulative 5-year savings: $4,600,000",
            "Cumulative 5-year cost: $6,670,000",
            "Break-even point: Month 38",
            "5-year NPV (at 8% discount rate): $1,230,000",
        ]),
        ("8. Technical Specifications", [
            "8.1 Target Infrastructure Specifications",
            "",
            "Compute:",
            "  - Production: 24x m6i.2xlarge instances (8 vCPU, 32 GiB RAM)",
            "  - Database: 6x r6i.4xlarge instances (16 vCPU, 128 GiB RAM)",
            "  - Container orchestration: Amazon EKS with 3 node groups",
            "  - Serverless: 45 Lambda functions (avg. 256 MB memory allocation)",
            "",
            "Storage:",
            "  - Amazon S3: 50 TB initial capacity (Standard + Intelligent-Tiering)",
            "  - Amazon EBS: 12 TB gp3 volumes across production instances",
            "  - Amazon EFS: 2 TB shared file system for legacy application support",
            "",
            "Networking:",
            "  - 3 VPCs (Production, Staging, Development) with VPC peering",
            "  - AWS Transit Gateway connecting all VPCs and on-premises",
            "  - AWS Direct Connect (10 Gbps dedicated) to Dallas data center",
            "  - AWS CloudFront CDN for external-facing applications",
            "",
            "8.2 Security Architecture",
            "",
            "  - AWS Organizations with Service Control Policies",
            "  - AWS SSO integration with existing Active Directory",
            "  - Amazon GuardDuty for threat detection",
            "  - AWS Security Hub for centralized security findings",
            "  - AWS WAF protecting all public-facing endpoints",
            "  - AWS KMS for encryption key management (AES-256)",
            "  - VPC Flow Logs and CloudTrail for audit logging",
            "  - CrowdStrike Falcon for endpoint protection",
        ]),
        ("9. Testing Strategy", [
            "9.1 Testing Phases",
            "",
            "Each migration wave will undergo a rigorous four-phase testing protocol:",
            "",
            "Phase A - Unit Testing:",
            "  - Individual component validation in isolation",
            "  - Automated test suites (target: 85% code coverage)",
            "  - Duration: 2 weeks per application",
            "",
            "Phase B - Integration Testing:",
            "  - End-to-end workflow validation across integrated systems",
            "  - API contract testing between microservices",
            "  - Database migration integrity verification",
            "  - Duration: 3 weeks per migration wave",
            "",
            "Phase C - Performance Testing:",
            "  - Load testing at 150% of peak production traffic",
            "  - Stress testing to identify breaking points",
            "  - Latency benchmarking against pre-migration baselines",
            "  - Duration: 2 weeks per migration wave",
            "",
            "Phase D - User Acceptance Testing (UAT):",
            "  - Business process validation by department representatives",
            "  - Regression testing of all critical workflows",
            "  - Sign-off required from each department head",
            "  - Duration: 3 weeks per migration wave",
            "",
            "9.2 Acceptance Criteria",
            "",
            "Migration will be deemed successful when:",
            "  - All automated tests pass with zero critical failures",
            "  - Performance metrics meet or exceed baseline measurements",
            "  - Data integrity verification shows 100% accuracy",
            "  - UAT sign-off received from all participating departments",
            "  - No P1 or P2 incidents during 72-hour stability window",
        ]),
        ("10. Change Management", [
            "10.1 Change Management Approach",
            "",
            "Successful technology transformation requires more than technical excellence. "
            "Our change management strategy follows the ADKAR model (Awareness, Desire, "
            "Knowledge, Ability, Reinforcement) to ensure sustainable adoption.",
            "",
            "Key activities by phase:",
            "",
            "Awareness (Months 1-3):",
            "  - Executive town hall announcing the initiative",
            "  - Department-specific information sessions",
            "  - FAQ documentation and dedicated intranet page",
            "  - Regular newsletter updates from CIO",
            "",
            "Desire (Months 2-6):",
            "  - Change champion network (2 representatives per department)",
            "  - Early wins showcase events",
            "  - Feedback collection and response mechanisms",
            "",
            "Knowledge (Months 4-18):",
            "  - Role-based training programs (40+ hours per affected employee)",
            "  - Self-service learning portal with video tutorials",
            "  - Hands-on workshops in sandbox environments",
            "  - Quick reference guides for all new systems",
            "",
            "Ability (Months 12-22):",
            "  - Supervised practice periods during parallel operations",
            "  - Dedicated support desks during transition weeks",
            "  - Peer mentoring programs",
            "",
            "Reinforcement (Months 18-24+):",
            "  - Performance metric tracking for new system adoption",
            "  - Recognition programs for early adopters",
            "  - Continuous improvement feedback loops",
        ]),
        ("11. Service Level Agreements", [
            "11.1 Operational SLAs",
            "",
            "The following service level agreements will govern the post-migration environment:",
            "",
            "Service                    | Availability | Response Time | Resolution Time",
            "--------------------------|--------------|---------------|----------------",
            "Core Business Applications | 99.99%       | < 200ms       | P1: 1hr, P2: 4hr",
            "Data Analytics Platform    | 99.95%       | < 500ms       | P1: 2hr, P2: 8hr",
            "Internal Collaboration     | 99.9%        | < 300ms       | P1: 2hr, P2: 8hr",
            "Development Environments   | 99.5%        | < 1000ms      | P1: 4hr, P2: 24hr",
            "Disaster Recovery          | RTO: 4hr     | RPO: 1hr      | Full test quarterly",
            "",
            "11.2 Performance Benchmarks",
            "",
            "All migrated applications must meet or exceed these performance benchmarks:",
            "  - Web application page load time: < 2 seconds (95th percentile)",
            "  - API response time: < 100ms for read operations, < 500ms for writes",
            "  - Batch processing: completion within 80% of current run time",
            "  - Database query performance: no degradation beyond 10% of baseline",
            "  - File transfer throughput: minimum 500 Mbps sustained",
            "",
            "11.3 Monitoring and Alerting",
            "",
            "A comprehensive monitoring stack will be deployed:",
            "  - Amazon CloudWatch for infrastructure metrics",
            "  - AWS X-Ray for distributed tracing",
            "  - PagerDuty integration for on-call alerting",
            "  - Grafana dashboards for operational visibility",
            "  - Custom health check endpoints for all services",
        ]),
        ("12. Staffing and Resource Plan", [
            "12.1 Meridian Consulting Team",
            "",
            "Role                      | Name              | Allocation | Duration",
            "--------------------------|-------------------|------------|----------",
            "Program Director          | Michael Nguyen    | 100%       | 24 months",
            "Program Manager           | Lisa Chen         | 100%       | 24 months",
            "Solution Architect        | Alexander Petrov  | 100%       | 18 months",
            "Cloud Architect           | Priya Sharma      | 100%       | 18 months",
            "Data Architect            | Thomas Mueller    | 75%        | 12 months",
            "Sr. Cloud Engineer (x3)   | Various           | 100%       | 18 months",
            "Application Developer (x4)| Various           | 100%       | 15 months",
            "Data Engineer (x3)        | Various           | 100%       | 12 months",
            "QA Lead                   | Jennifer Santos   | 100%       | 18 months",
            "QA Engineer (x3)          | Various           | 100%       | 15 months",
            "DevOps Engineer (x2)      | Various           | 100%       | 18 months",
            "Change Mgmt Specialist    | Angela Washington | 75%        | 20 months",
            "",
            "12.2 Northstar Internal Resources Required",
            "",
            "  - IT infrastructure team: 4 engineers (50% allocation)",
            "  - Application owners: 8 SMEs (25% allocation during their phase)",
            "  - Department UAT coordinators: 8 staff (10% allocation)",
            "  - IT security team: 2 analysts (30% allocation)",
            "  - Project management office: 1 PMO coordinator (50% allocation)",
        ]),
        ("13. Data Migration Strategy", [
            "13.1 Data Classification",
            "",
            "All data has been classified into four tiers based on criticality and sensitivity:",
            "",
            "Tier 1 - Critical Business Data (2.8 TB):",
            "  - Financial records and transactions",
            "  - Customer data and contracts",
            "  - HR personnel files and payroll data",
            "  - Intellectual property and trade secrets",
            "",
            "Tier 2 - Important Operational Data (8.4 TB):",
            "  - Inventory and supply chain records",
            "  - Project management artifacts",
            "  - Email archives (past 7 years)",
            "  - CRM interaction history",
            "",
            "Tier 3 - Standard Business Data (15.2 TB):",
            "  - Department file shares",
            "  - Training materials",
            "  - Marketing collateral",
            "  - Historical reports",
            "",
            "Tier 4 - Archival Data (23.6 TB):",
            "  - Legacy system backups",
            "  - Decommissioned application data",
            "  - Compliance retention archives",
            "",
            "13.2 Migration Approach by Tier",
            "",
            "Tier 1 data will undergo a verified migration process with checksums, row counts, "
            "and business rule validation at every step. A dedicated data validation team will "
            "certify each Tier 1 migration before cutover approval.",
            "",
            "Tier 2 data will follow standard migration procedures with automated integrity "
            "checks and sampling-based validation.",
            "",
            "Tiers 3 and 4 will use bulk transfer methods (AWS DataSync, Snowball Edge) with "
            "post-migration spot checks.",
        ]),
        ("14. Compliance and Regulatory Considerations", [
            "14.1 Regulatory Framework",
            "",
            "Northstar Technologies operates in a regulated environment with obligations under:",
            "  - SOC 2 Type II (annual audit requirement)",
            "  - PCI DSS Level 2 (payment card processing)",
            "  - GDPR (European customer data)",
            "  - CCPA (California consumer data)",
            "  - HIPAA (employee health plan data)",
            "",
            "14.2 Compliance Strategy",
            "",
            "AWS compliance certifications (SOC 2, PCI DSS, HIPAA) provide the foundation. "
            "Northstar-specific controls will be implemented as follows:",
            "",
            "Data Residency:",
            "  - All Tier 1 data stored in US-East-1 and US-West-2 regions only",
            "  - EU customer data isolated in EU-West-1 per GDPR requirements",
            "  - No data processing in restricted jurisdictions",
            "",
            "Access Controls:",
            "  - Principle of least privilege enforced via IAM policies",
            "  - Multi-factor authentication required for all privileged access",
            "  - Quarterly access reviews with automated revocation",
            "",
            "Audit and Logging:",
            "  - CloudTrail enabled in all accounts and regions",
            "  - Log retention: 7 years (compliance requirement)",
            "  - Tamper-evident logging with CloudTrail Integrity Validation",
            "",
            "14.3 Certification Timeline",
            "",
            "  - SOC 2 Type II: Audit window Month 20-24 (post-migration stabilization)",
            "  - PCI DSS: Assessment at Month 22",
            "  - GDPR Data Protection Impact Assessment: Month 6 and Month 18",
        ]),
        ("15. Disaster Recovery and Business Continuity", [
            "15.1 DR Architecture",
            "",
            "The disaster recovery strategy leverages AWS multi-region capabilities:",
            "",
            "  Primary Region: US-East-1 (N. Virginia)",
            "  Secondary Region: US-West-2 (Oregon)",
            "",
            "Replication Strategy:",
            "  - Amazon RDS: Multi-AZ deployment with cross-region read replicas",
            "  - Amazon S3: Cross-region replication enabled for all critical buckets",
            "  - Amazon EKS: Warm standby cluster in secondary region",
            "  - AWS Route 53: Health-check based failover routing",
            "",
            "15.2 Recovery Objectives",
            "",
            "Application Tier        | RTO        | RPO",
            "-----------------------|------------|----------",
            "Tier 1 (Critical)      | 1 hour     | 15 minutes",
            "Tier 2 (Important)     | 4 hours    | 1 hour",
            "Tier 3 (Standard)      | 24 hours   | 4 hours",
            "Tier 4 (Archival)      | 72 hours   | 24 hours",
            "",
            "15.3 DR Testing Schedule",
            "",
            "Quarterly DR tests will validate failover procedures:",
            "  - Q1: Tabletop exercise with all stakeholders",
            "  - Q2: Partial failover test (Tier 1 applications only)",
            "  - Q3: Full failover test with measured RTO/RPO",
            "  - Q4: Surprise drill (unannounced, business hours)",
        ]),
        ("16. Training and Knowledge Transfer", [
            "16.1 Training Program Overview",
            "",
            "A comprehensive training program ensures Northstar staff can independently "
            "operate and optimize the new environment post-engagement.",
            "",
            "Training Tracks:",
            "",
            "Track A - Cloud Operations (IT Infrastructure Team):",
            "  - AWS Certified Solutions Architect preparation (40 hours)",
            "  - Terraform/Infrastructure as Code workshop (16 hours)",
            "  - Kubernetes administration fundamentals (24 hours)",
            "  - Monitoring and incident response procedures (16 hours)",
            "  Total: 96 hours per engineer",
            "",
            "Track B - Application Support (IT Application Team):",
            "  - New application architecture overview (8 hours per app)",
            "  - CI/CD pipeline operation (16 hours)",
            "  - Container management basics (8 hours)",
            "  - Troubleshooting and log analysis (16 hours)",
            "  Total: 48 hours per engineer",
            "",
            "Track C - Data Operations (Data Team):",
            "  - AWS data services overview (16 hours)",
            "  - ETL pipeline management (24 hours)",
            "  - Tableau administration and dashboard development (16 hours)",
            "  Total: 56 hours per analyst",
            "",
            "Track D - End Users (All Departments):",
            "  - New system orientation (4 hours)",
            "  - Self-service analytics training (8 hours)",
            "  - Security awareness refresher (2 hours)",
            "  Total: 14 hours per employee",
        ]),
        ("17. Success Criteria and KPIs", [
            "17.1 Project Success Criteria",
            "",
            "The project will be measured against these success criteria at completion:",
            "",
            "  1. All migration waves completed within 24-month timeline (+/- 30 days)",
            "  2. Total budget variance within 10% of approved $5.02M",
            "  3. Zero data loss incidents across all tiers",
            "  4. All SLA targets met for 90 consecutive days post-migration",
            "  5. 90% user satisfaction rating on post-migration survey",
            "  6. SOC 2 Type II certification obtained within 6 months of completion",
            "",
            "17.2 Key Performance Indicators",
            "",
            "Infrastructure KPIs:",
            "  - Cloud resource utilization: target > 65%",
            "  - Monthly cloud spend vs. forecast: within 5%",
            "  - Automated deployment success rate: > 98%",
            "  - Mean time to recovery (MTTR): < 30 minutes",
            "",
            "Business KPIs:",
            "  - Employee productivity improvement: 15% (measured by output per FTE)",
            "  - Customer-facing system response time: 50% improvement",
            "  - IT operational cost reduction: 40% by Year 3",
            "  - New feature deployment frequency: 4x improvement",
            "",
            "17.3 Measurement and Reporting",
            "",
            "KPIs will be tracked through automated dashboards accessible to all stakeholders. "
            "Monthly reports will be presented to the steering committee with trend analysis "
            "and recommendations for optimization.",
        ]),
        ("Appendix A: Glossary and References", [
            "Glossary of Terms",
            "",
            "AWS - Amazon Web Services, cloud computing platform",
            "CI/CD - Continuous Integration / Continuous Deployment",
            "COBOL - Common Business Oriented Language",
            "DR - Disaster Recovery",
            "EKS - Elastic Kubernetes Service",
            "ERP - Enterprise Resource Planning",
            "ETL - Extract, Transform, Load",
            "IAM - Identity and Access Management",
            "KPI - Key Performance Indicator",
            "MGN - Application Migration Service",
            "MTTR - Mean Time to Recovery",
            "NPV - Net Present Value",
            "RDS - Relational Database Service",
            "ROI - Return on Investment",
            "RPO - Recovery Point Objective",
            "RTO - Recovery Time Objective",
            "SAP - Systems, Applications, and Products in Data Processing",
            "SLA - Service Level Agreement",
            "SME - Subject Matter Expert",
            "SOC - Service Organization Control",
            "UAT - User Acceptance Testing",
            "VPC - Virtual Private Cloud",
            "WAF - Web Application Firewall",
            "",
            "References",
            "",
            "1. AWS Well-Architected Framework, Amazon Web Services, 2025",
            "2. NIST Cloud Computing Reference Architecture, SP 500-292",
            "3. Gartner Magic Quadrant for Cloud Infrastructure, 2025",
            "4. Northstar Technologies IT Strategic Plan 2024-2028",
            "5. Meridian Consulting Cloud Migration Methodology v4.1",
            "6. AWS Security Best Practices, Amazon Web Services, 2025",
            "",
            "Document Control",
            "",
            "Version | Date       | Author           | Changes",
            "--------|-----------|------------------|------------------------",
            "1.0     | 2025-11-10| Michael Nguyen   | Initial draft",
            "2.0     | 2025-12-15| Lisa Chen        | Incorporated stakeholder feedback",
            "2.5     | 2026-01-20| Alexander Petrov | Technical architecture updates",
            "3.0     | 2026-02-28| Michael Nguyen   | Budget revision and timeline update",
            "3.2     | 2026-03-15| Lisa Chen        | Final review and formatting",
        ]),
    ]

    # We need exactly 22 pages. Generate content across pages.
    # Each section gets roughly 1 page, some sections are longer and span 2 pages.
    for i in range(22):
        page = doc.new_page(width=LETTER_W, height=LETTER_H)

        if i < len(sections):
            title, paragraphs = sections[i]
        else:
            # Extra pages if needed (shouldn't happen with 22 sections)
            title = f"Appendix {chr(65 + i - len(sections))}"
            paragraphs = ["Additional supporting documentation."]

        # Insert section title
        if i == 0:
            # Cover page - centered title
            page.insert_text(
                pymupdf.Point(120, 250),
                title,
                fontsize=28,
                fontname="hebo",
                color=(0.1, 0.15, 0.35),
            )
            y = 310
        else:
            page.insert_text(
                pymupdf.Point(72, 60),
                title,
                fontsize=16,
                fontname="hebo",
                color=(0.1, 0.15, 0.35),
            )
            # Separator line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
            shape.finish(color=(0.3, 0.4, 0.6), width=0.75)
            shape.commit()
            y = 90

        # Insert paragraph content
        for para in paragraphs:
            if not para:
                y += 8
                continue

            # Check if it's a sub-heading (starts with digit and dot, or specific patterns)
            if (para and len(para) < 60 and
                (para[0].isdigit() or para.startswith("Phase") or
                 para.endswith(":") or para.startswith("Track"))):
                page.insert_text(
                    pymupdf.Point(72, y),
                    para,
                    fontsize=11,
                    fontname="hebo",
                    color=(0.15, 0.2, 0.4),
                )
                y += 16
            else:
                # Regular text - use textbox for wrapping
                rect = pymupdf.Rect(72, y - 10, 540, y + 80)
                excess = page.insert_textbox(
                    rect,
                    para,
                    fontsize=10,
                    fontname="helv",
                    color=(0.1, 0.1, 0.1),
                    align=0,  # left align
                )
                # Estimate lines used
                chars_per_line = 80
                lines = max(1, len(para) // chars_per_line + 1)
                y += lines * 13 + 4

            if y > 740:
                break

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 22')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
