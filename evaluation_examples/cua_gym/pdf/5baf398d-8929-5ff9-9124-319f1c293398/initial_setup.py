"""
Initial Setup: Create source PDF files for PDF processing pipeline task.
Task ID: pdf_fm_095
Domain: pdf
Creates: ~/Documents/project_docs/report.pdf (25pp), appendix_a.pdf (10pp), appendix_b.pdf (8pp)
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_095'
DOCS_DIR = f'{WORKDIR}/Documents/project_docs'

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


def create_report_pdf(path, num_pages=25):
    """Create a realistic 25-page project report PDF."""
    doc = pymupdf.open()

    # Page 1: Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(306, 250), "PROJECT ATLAS", fontsize=36, fontname="hebo",
                     color=(0.0, 0.15, 0.4))
    page.insert_text(pymupdf.Point(306, 300), "Comprehensive Technical Report", fontsize=18,
                     fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(306, 370), "Prepared by: Team Alpha", fontsize=14,
                     fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(306, 395), "Date: March 15, 2025", fontsize=12,
                     fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(306, 420), "Version 3.2 - Internal Distribution",
                     fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))

    # Chapters and content for remaining pages
    chapters = [
        ("1. Executive Summary", [
            "Project Atlas represents a transformative initiative to modernize the organization's core infrastructure. "
            "Over the past eighteen months, the team has successfully migrated 94% of legacy systems to cloud-native "
            "architectures, resulting in a 37% reduction in operational costs and a 52% improvement in system reliability.",
            "Key achievements include the deployment of a distributed microservices platform serving 2.3 million daily "
            "active users, the implementation of automated CI/CD pipelines reducing deployment cycles from weeks to hours, "
            "and the establishment of comprehensive monitoring dashboards providing real-time visibility into system health.",
            "This report details the technical approach, implementation timeline, resource utilization, risk mitigation "
            "strategies, and recommendations for the next phase of digital transformation."
        ]),
        ("2. Project Background and Objectives", [
            "The initiative was conceived in Q3 2023 following a comprehensive audit of existing infrastructure that "
            "revealed critical vulnerabilities in scalability, security posture, and operational efficiency. The legacy "
            "monolithic architecture, originally deployed in 2016, had reached end-of-life for several key components.",
            "Primary objectives established by the steering committee included: achieving 99.95% uptime SLA across all "
            "production services, reducing mean time to recovery (MTTR) from 4.2 hours to under 15 minutes, enabling "
            "horizontal scaling to accommodate projected 300% user growth over the next three years, and implementing "
            "zero-trust security architecture compliant with ISO 27001 and SOC 2 Type II standards.",
            "Budget allocation of $4.7M was approved across three fiscal quarters, with contingency reserves of 12% "
            "for unforeseen technical challenges. The core team consisted of 14 engineers, 3 project managers, "
            "2 security specialists, and 1 UX researcher."
        ]),
        ("3. Technical Architecture", [
            "The new architecture employs a service mesh topology built on Kubernetes orchestration with Istio for "
            "traffic management and mutual TLS encryption. The compute layer leverages a multi-region deployment "
            "across three availability zones, with automated failover configured for sub-second recovery.",
            "Data persistence is handled through a polyglot approach: PostgreSQL 15 for transactional workloads with "
            "read replicas achieving sub-millisecond replication lag, Apache Cassandra for time-series telemetry data "
            "ingesting 850,000 events per second, Redis Cluster for session management and caching with 99.7% hit rates, "
            "and MinIO for object storage handling 2.1 TB of daily uploads.",
            "The API gateway processes an average of 45,000 requests per second during peak hours, with P99 latency "
            "maintained below 120ms through intelligent load balancing and circuit breaker patterns."
        ]),
        ("4. Implementation Timeline and Milestones", [
            "Phase 1 (Q4 2023 - Q1 2024): Foundation and Core Services. Completed Kubernetes cluster provisioning, "
            "established CI/CD pipelines with GitLab CI, deployed authentication and authorization services with "
            "OpenID Connect integration. Achieved milestone: first production workload migrated on December 18, 2023.",
            "Phase 2 (Q1 2024 - Q2 2024): Data Layer Migration. Executed zero-downtime migration of 847 database "
            "tables containing 14.3 billion records. Implemented Change Data Capture (CDC) streams using Debezium "
            "for real-time synchronization during the parallel-run period. Validation confirmed data integrity "
            "with zero discrepancies across all migrated datasets.",
            "Phase 3 (Q2 2024 - Q3 2024): Application Modernization. Decomposed the monolithic application into "
            "47 bounded-context microservices. Each service underwent independent load testing, security scanning, "
            "and compliance verification before production promotion.",
            "Phase 4 (Q3 2024 - Q1 2025): Optimization and Hardening. Focused on performance tuning, cost optimization "
            "through right-sizing and spot instance utilization, and implementation of advanced observability with "
            "distributed tracing using OpenTelemetry."
        ]),
        ("5. Performance Metrics and Analysis", [
            "System reliability improved from 99.2% to 99.97% measured over the trailing 90-day period. The number "
            "of severity-1 incidents decreased from an average of 3.4 per month to 0.2 per month. Mean time to "
            "detection (MTTD) improved from 23 minutes to 47 seconds through automated anomaly detection.",
            "Application performance benchmarks show significant improvements: API response times decreased by 64% "
            "(P50: 12ms, P95: 45ms, P99: 118ms), database query execution times improved by 78% through query "
            "optimization and strategic indexing, and frontend page load times decreased from 3.2 seconds to 0.8 seconds "
            "measured via Real User Monitoring (RUM) across global endpoints.",
            "Cost efficiency metrics demonstrate a 37% reduction in total infrastructure spending despite 180% increase "
            "in compute capacity. The unit economics improved from $0.0047 per transaction to $0.0019 per transaction, "
            "achieved primarily through containerization efficiency and reserved capacity planning."
        ]),
        ("6. Security Assessment and Compliance", [
            "The zero-trust architecture implementation encompasses network microsegmentation, mutual TLS for all "
            "service-to-service communication, just-in-time access provisioning, and continuous authentication "
            "verification. Penetration testing conducted by CyberShield Associates identified zero critical and "
            "two medium-severity findings, both remediated within 48 hours.",
            "Compliance certifications achieved: SOC 2 Type II (audit completed February 2025), ISO 27001:2022 "
            "(certification received January 2025), GDPR data processing assessment (completed December 2024), "
            "and PCI DSS Level 1 for payment processing components (validated November 2024).",
            "Vulnerability management metrics show 100% of critical CVEs patched within 24 hours, 98.7% of high-severity "
            "vulnerabilities resolved within 72 hours, and automated dependency scanning covering 100% of production "
            "container images with daily refresh cycles."
        ]),
        ("7. Risk Management and Mitigation", [
            "The project risk register tracked 34 identified risks across technical, operational, and organizational "
            "categories. Of these, 28 were successfully mitigated, 4 were accepted with documented residual risk, "
            "and 2 materialized but were contained within acceptable impact parameters.",
            "Key risk materializations included: an unexpected vendor API deprecation during Phase 2 requiring "
            "14 days of additional integration work (mitigated through contract escalation and parallel development), "
            "and a temporary capacity constraint in the staging environment causing a 3-week delay in Phase 3 load "
            "testing (resolved through dynamic provisioning of additional test infrastructure).",
            "Ongoing risk monitoring employs automated dashboards tracking 67 risk indicators with configurable "
            "alerting thresholds. Quarterly risk reviews are conducted with the steering committee to reassess "
            "priorities and allocate mitigation resources."
        ]),
        ("8. Recommendations and Next Steps", [
            "Based on the outcomes achieved and lessons learned, the following recommendations are proposed for "
            "the next phase of the initiative: expand the platform to support edge computing workloads for IoT "
            "sensor data processing, implement AIOps capabilities for predictive incident management, and establish "
            "a developer platform team to improve self-service infrastructure provisioning.",
            "Budget projection for Phase 5 (Q2 2025 - Q4 2025) estimates $2.1M for edge infrastructure deployment, "
            "$890K for AIOps tooling and integration, and $650K for platform engineering staffing. Expected ROI "
            "is projected at 240% over a 24-month horizon based on operational savings and revenue enablement.",
            "The team recommends transitioning to a product-oriented operating model with dedicated stream-aligned "
            "teams for each major business domain, supported by a platform team providing shared capabilities "
            "and a dedicated enabling team for skills development and knowledge transfer."
        ]),
    ]

    page_num = 1  # title page is page 1
    for chapter_title, paragraphs in chapters:
        # Each chapter gets multiple pages
        pages_for_chapter = max(2, (len(paragraphs) + 1))
        for cp in range(pages_for_chapter):
            page_num += 1
            if page_num > num_pages:
                break
            page = doc.new_page(width=612, height=792)

            if cp == 0:
                # Chapter title page
                page.insert_text(pymupdf.Point(72, 72), chapter_title, fontsize=20,
                                 fontname="hebo", color=(0.0, 0.15, 0.4))
                y_pos = 110
                for para in paragraphs:
                    rect = pymupdf.Rect(72, y_pos, 540, y_pos + 150)
                    excess = page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                                                  color=(0.1, 0.1, 0.1),
                                                  align=pymupdf.TEXT_ALIGN_JUSTIFY)
                    y_pos += 160
                    if y_pos > 700:
                        break
            else:
                # Continuation page with more detail
                page.insert_text(pymupdf.Point(72, 72), f"{chapter_title} (continued)", fontsize=14,
                                 fontname="hebo", color=(0.2, 0.2, 0.2))
                detail_text = (
                    f"Detailed analysis for {chapter_title.split('.')[1].strip() if '.' in chapter_title else chapter_title} "
                    f"continues with additional supporting data and cross-references to supplementary materials. "
                    f"The quantitative assessment demonstrates measurable progress against established baselines, "
                    f"with variance analysis highlighting areas requiring continued attention in the next reporting period. "
                    f"Stakeholder feedback collected through structured interviews and survey instruments confirms "
                    f"alignment between project outcomes and organizational strategic objectives."
                )
                rect = pymupdf.Rect(72, 100, 540, 700)
                page.insert_textbox(rect, detail_text, fontsize=11, fontname="helv",
                                     color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        if page_num >= num_pages:
            break

    # Fill remaining pages if needed
    while doc.page_count < num_pages:
        page = doc.new_page(width=612, height=792)
        pg = doc.page_count
        page.insert_text(pymupdf.Point(72, 72), f"Supporting Analysis - Section {pg - 16}",
                         fontsize=16, fontname="hebo", color=(0.2, 0.2, 0.2))
        filler = (
            "This section provides supplementary analytical content supporting the findings presented "
            "in the main body of the report. Cross-referencing with Appendix A data tables confirms "
            "the statistical significance of observed trends at the 95% confidence interval. "
            "Additional visualization of the temporal distribution patterns can be found in the "
            "accompanying dashboard accessible via the project SharePoint site."
        )
        rect = pymupdf.Rect(72, 100, 540, 700)
        page.insert_textbox(rect, filler, fontsize=11, fontname="helv",
                             color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    doc.save(path)
    doc.close()
    print(f"Created report.pdf with {num_pages} pages at {path}")


def create_appendix_a_pdf(path, num_pages=10):
    """Create a 10-page appendix with data tables and references."""
    doc = pymupdf.open()

    # Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 100), "Appendix A", fontsize=28, fontname="hebo",
                     color=(0.0, 0.15, 0.4))
    page.insert_text(pymupdf.Point(72, 140), "Data Tables and Statistical Analysis",
                     fontsize=16, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 180),
                     "This appendix contains the raw data tables, statistical computations, and "
                     "methodology notes referenced throughout the main report. All figures are "
                     "derived from production telemetry data collected between October 2023 and "
                     "February 2025.", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    tables_data = [
        ("Table A.1: Monthly Active Users", [
            ["Month", "MAU", "DAU", "Peak Concurrent", "Avg Session (min)"],
            ["Oct 2023", "1,234,567", "412,189", "87,432", "14.3"],
            ["Nov 2023", "1,298,044", "432,681", "91,205", "15.1"],
            ["Dec 2023", "1,356,782", "452,261", "95,834", "14.8"],
            ["Jan 2024", "1,423,901", "474,634", "102,456", "15.7"],
            ["Feb 2024", "1,512,345", "504,115", "108,923", "16.2"],
            ["Mar 2024", "1,634,567", "544,856", "118,734", "16.8"],
        ]),
        ("Table A.2: Infrastructure Cost Breakdown ($)", [
            ["Category", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
            ["Compute", "234,500", "218,300", "195,600", "178,400", "162,100"],
            ["Storage", "89,200", "92,100", "87,500", "84,300", "79,800"],
            ["Networking", "45,600", "43,200", "41,800", "38,900", "36,200"],
            ["Monitoring", "12,300", "12,300", "14,500", "14,500", "14,500"],
            ["Security", "28,900", "31,200", "31,200", "33,400", "33,400"],
            ["Total", "410,500", "397,100", "370,600", "349,500", "326,000"],
        ]),
        ("Table A.3: API Performance Percentiles (ms)", [
            ["Endpoint", "P50", "P75", "P90", "P95", "P99"],
            ["/api/users", "8", "12", "18", "24", "45"],
            ["/api/orders", "15", "22", "35", "48", "89"],
            ["/api/products", "6", "9", "14", "19", "38"],
            ["/api/search", "23", "34", "52", "71", "134"],
            ["/api/analytics", "45", "67", "98", "125", "234"],
            ["/api/auth", "5", "7", "11", "15", "28"],
        ]),
    ]

    for idx, (table_title, rows) in enumerate(tables_data):
        page = doc.new_page(width=612, height=792)
        page.insert_text(pymupdf.Point(72, 72), table_title, fontsize=14, fontname="hebo",
                         color=(0.0, 0.15, 0.4))
        y = 100
        for row in rows:
            x = 72
            for cell in row:
                page.insert_text(pymupdf.Point(x, y), str(cell), fontsize=9, fontname="helv",
                                 color=(0.1, 0.1, 0.1))
                x += 100
            y += 18

        # Add analysis text below table
        analysis = (
            f"Statistical analysis of {table_title.lower()} indicates consistent trends across "
            f"the measured time periods. The coefficient of variation remains within acceptable "
            f"bounds (CV < 0.15) for all primary metrics, confirming the reliability of "
            f"the sampling methodology employed."
        )
        rect = pymupdf.Rect(72, y + 20, 540, y + 120)
        page.insert_textbox(rect, analysis, fontsize=10, fontname="helv",
                             color=(0.2, 0.2, 0.2), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Fill remaining pages
    while doc.page_count < num_pages:
        page = doc.new_page(width=612, height=792)
        pg = doc.page_count
        page.insert_text(pymupdf.Point(72, 72), f"Appendix A - Supplementary Data Set {pg - 3}",
                         fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))
        supp_text = (
            "Supplementary data set providing additional granularity for the metrics presented "
            "in the preceding tables. Raw measurement values are available upon request from "
            "the project data steward. All values have been validated against source system "
            "extracts with reconciliation performed on a monthly cadence."
        )
        rect = pymupdf.Rect(72, 100, 540, 700)
        page.insert_textbox(rect, supp_text, fontsize=11, fontname="helv",
                             color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    doc.save(path)
    doc.close()
    print(f"Created appendix_a.pdf with {num_pages} pages at {path}")


def create_appendix_b_pdf(path, num_pages=8):
    """Create an 8-page appendix with reference materials and glossary."""
    doc = pymupdf.open()

    # Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 100), "Appendix B", fontsize=28, fontname="hebo",
                     color=(0.0, 0.15, 0.4))
    page.insert_text(pymupdf.Point(72, 140), "Reference Materials and Glossary",
                     fontsize=16, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 180),
                     "This appendix provides reference documentation, acronym definitions, "
                     "and a comprehensive glossary of technical terms used throughout the "
                     "Project Atlas report and its appendices.", fontsize=11, fontname="helv",
                     color=(0.2, 0.2, 0.2))

    # Glossary pages
    glossary_entries = [
        ("AIOps", "Artificial Intelligence for IT Operations - the application of machine learning to automate and enhance IT operations processes."),
        ("CDC", "Change Data Capture - a design pattern for tracking and propagating data changes from source systems in real-time."),
        ("CI/CD", "Continuous Integration / Continuous Deployment - automated software delivery pipeline methodology."),
        ("CVE", "Common Vulnerabilities and Exposures - a standardized identifier for known security vulnerabilities."),
        ("DAU", "Daily Active Users - the count of unique users engaging with the platform within a 24-hour period."),
        ("GDPR", "General Data Protection Regulation - European Union data privacy and protection regulation."),
        ("IoT", "Internet of Things - interconnected computing devices embedded in everyday objects enabling data exchange."),
        ("MAU", "Monthly Active Users - unique users engaging with the platform within a 30-day rolling window."),
        ("MTTD", "Mean Time to Detection - average duration between incident occurrence and automated detection."),
        ("MTTR", "Mean Time to Recovery - average duration from incident detection to full service restoration."),
        ("P50/P95/P99", "Percentile latency measurements indicating the response time below which 50%, 95%, or 99% of requests complete."),
        ("PCI DSS", "Payment Card Industry Data Security Standard - security standard for organizations handling credit card data."),
        ("RUM", "Real User Monitoring - performance measurement using data collected from actual end-user browser sessions."),
        ("SLA", "Service Level Agreement - contractual commitment defining expected service availability and performance."),
        ("SOC 2", "Service Organization Control 2 - audit framework for evaluating organizational controls over data security."),
        ("TLS", "Transport Layer Security - cryptographic protocol providing secure communication over computer networks."),
    ]

    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Glossary of Terms", fontsize=18, fontname="hebo",
                     color=(0.0, 0.15, 0.4))
    y = 110
    for term, definition in glossary_entries[:10]:
        page.insert_text(pymupdf.Point(72, y), f"{term}:", fontsize=11, fontname="hebo",
                         color=(0.1, 0.1, 0.1))
        rect = pymupdf.Rect(72, y + 4, 540, y + 40)
        page.insert_textbox(rect, definition, fontsize=10, fontname="helv",
                             color=(0.2, 0.2, 0.2))
        y += 48
        if y > 720:
            break

    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Glossary of Terms (continued)", fontsize=18,
                     fontname="hebo", color=(0.0, 0.15, 0.4))
    y = 110
    for term, definition in glossary_entries[10:]:
        page.insert_text(pymupdf.Point(72, y), f"{term}:", fontsize=11, fontname="hebo",
                         color=(0.1, 0.1, 0.1))
        rect = pymupdf.Rect(72, y + 4, 540, y + 40)
        page.insert_textbox(rect, definition, fontsize=10, fontname="helv",
                             color=(0.2, 0.2, 0.2))
        y += 48

    # References pages
    references = [
        "Kubernetes Documentation, v1.28. The Linux Foundation. https://kubernetes.io/docs/",
        "Istio Service Mesh Architecture, v1.20. Istio Authors. https://istio.io/latest/docs/",
        "PostgreSQL 15 Documentation. The PostgreSQL Global Development Group, 2024.",
        "Apache Cassandra Architecture Guide, v4.1. Apache Software Foundation.",
        "NIST Cybersecurity Framework v2.0. National Institute of Standards and Technology, 2024.",
        "ISO/IEC 27001:2022 Information Security Management. International Organization for Standardization.",
        "PCI DSS v4.0 Requirements and Testing Procedures. PCI Security Standards Council, 2023.",
        "Site Reliability Engineering. Beyer, Jones, Petoff, Murphy. O'Reilly Media, 2016.",
        "Designing Data-Intensive Applications. Martin Kleppmann. O'Reilly Media, 2017.",
        "The Phoenix Project. Gene Kim, Kevin Behr, George Spafford. IT Revolution Press, 2013.",
        "Accelerate: Building and Scaling High Performing Technology Organizations. Forsgren, Humble, Kim. 2018.",
        "OpenTelemetry Specification v1.0. Cloud Native Computing Foundation, 2024.",
    ]

    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "References", fontsize=18, fontname="hebo",
                     color=(0.0, 0.15, 0.4))
    y = 110
    for i, ref in enumerate(references, 1):
        page.insert_text(pymupdf.Point(72, y), f"[{i}]", fontsize=10, fontname="hebo",
                         color=(0.1, 0.1, 0.1))
        rect = pymupdf.Rect(95, y - 4, 540, y + 22)
        page.insert_textbox(rect, ref, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 30

    # Fill remaining pages
    while doc.page_count < num_pages:
        page = doc.new_page(width=612, height=792)
        pg = doc.page_count
        titles = [
            "Configuration Parameters Reference",
            "Network Architecture Diagrams Description",
            "Change Log and Version History",
            "Approval and Sign-off Records",
        ]
        title = titles[pg - 5] if pg - 5 < len(titles) else f"Additional Reference Material {pg}"
        page.insert_text(pymupdf.Point(72, 72), title, fontsize=16, fontname="hebo",
                         color=(0.2, 0.2, 0.2))
        content = (
            "This section contains additional reference materials supporting the Project Atlas "
            "technical report. Configuration parameters listed herein reflect production values "
            "as of the report publication date. Any modifications to these parameters should "
            "follow the change management process documented in Section 7 of the main report."
        )
        rect = pymupdf.Rect(72, 100, 540, 700)
        page.insert_textbox(rect, content, fontsize=11, fontname="helv",
                             color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    doc.save(path)
    doc.close()
    print(f"Created appendix_b.pdf with {num_pages} pages at {path}")


def create_initial():
    # Ensure directory exists
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    # Create the three source PDFs
    create_report_pdf(f'{DOCS_DIR}/report.pdf', num_pages=25)
    create_appendix_a_pdf(f'{DOCS_DIR}/appendix_a.pdf', num_pages=10)
    create_appendix_b_pdf(f'{DOCS_DIR}/appendix_b.pdf', num_pages=8)

    print(f"All initial files created in {DOCS_DIR}")

    # Open the file manager to show the documents directory
    launch_gui(f'nautilus "{DOCS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
