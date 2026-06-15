"""
Initial Setup: Create source PDF files for portfolio merge task
Task ID: pdf_gf2_036
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_036'
PORTFOLIO_DIR = f'{WORKDIR}/portfolio'

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

def create_resume():
    """Create a realistic 2-page resume PDF."""
    doc = pymupdf.open()

    # Page 1 - Header and Experience
    page1 = doc.new_page(width=612, height=792)
    y = 60

    page1.insert_text(pymupdf.Point(72, y), "ELENA VASQUEZ", fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 28
    page1.insert_text(pymupdf.Point(72, y), "Senior Software Engineer", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 20
    page1.insert_text(pymupdf.Point(72, y), "elena.vasquez@email.com | (415) 555-0187 | San Francisco, CA", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    y += 14
    page1.insert_text(pymupdf.Point(72, y), "linkedin.com/in/elenavasquez | github.com/evasquez", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    # Horizontal line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, y + 12), pymupdf.Point(540, y + 12))
    shape.finish(color=(0.1, 0.2, 0.4), width=1.5)
    shape.commit()
    y += 30

    page1.insert_text(pymupdf.Point(72, y), "PROFESSIONAL SUMMARY", fontsize=12, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 18
    rect = pymupdf.Rect(72, y, 540, y + 60)
    page1.insert_textbox(rect,
        "Results-driven software engineer with 8+ years of experience designing scalable distributed systems "
        "and leading cross-functional engineering teams. Expertise in cloud-native architectures, microservices, "
        "and high-throughput data pipelines. Proven track record of reducing infrastructure costs by 40% while "
        "improving system reliability to 99.99% uptime.",
        fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 70

    page1.insert_text(pymupdf.Point(72, y), "PROFESSIONAL EXPERIENCE", fontsize=12, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 20

    experiences = [
        ("Lead Software Engineer", "Meridian Technologies, San Francisco, CA", "March 2021 - Present",
         ["Architected event-driven microservices platform processing 2M+ events/day using Kafka and Kubernetes",
          "Led team of 12 engineers in migrating monolithic application to cloud-native architecture on AWS",
          "Reduced deployment time from 4 hours to 15 minutes through CI/CD pipeline optimization",
          "Implemented automated testing framework achieving 94% code coverage across 200+ microservices"]),
        ("Senior Software Engineer", "Cascade Data Systems, Oakland, CA", "June 2018 - February 2021",
         ["Designed real-time analytics pipeline handling 500GB daily data ingestion using Apache Spark",
          "Built RESTful API gateway serving 10K+ requests/second with sub-50ms latency",
          "Mentored 5 junior engineers and established code review best practices for the team",
          "Received Outstanding Contributor Award for Q3 2020 data platform reliability improvements"]),
    ]

    for title, company, dates, bullets in experiences:
        page1.insert_text(pymupdf.Point(72, y), title, fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 14
        page1.insert_text(pymupdf.Point(72, y), company, fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))
        page1.insert_text(pymupdf.Point(400, y), dates, fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 16
        for bullet in bullets:
            rect = pymupdf.Rect(90, y, 540, y + 28)
            page1.insert_textbox(rect, f"• {bullet}", fontsize=9.5, fontname="helv", color=(0, 0, 0))
            y += 28
        y += 8

    # Page 2 - More Experience, Education, Skills
    page2 = doc.new_page(width=612, height=792)
    y = 60

    page2.insert_text(pymupdf.Point(72, y), "Software Engineer", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 14
    page2.insert_text(pymupdf.Point(72, y), "NovaByte Solutions, San Jose, CA", fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))
    page2.insert_text(pymupdf.Point(400, y), "August 2016 - May 2018", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 16
    novabyte_bullets = [
        "Developed microservices for e-commerce platform serving 2M+ monthly active users",
        "Optimized PostgreSQL queries reducing average response time by 65%",
        "Implemented OAuth 2.0 authentication system with SAML SSO integration",
    ]
    for bullet in novabyte_bullets:
        rect = pymupdf.Rect(90, y, 540, y + 28)
        page2.insert_textbox(rect, f"• {bullet}", fontsize=9.5, fontname="helv", color=(0, 0, 0))
        y += 28
    y += 15

    page2.insert_text(pymupdf.Point(72, y), "EDUCATION", fontsize=12, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 20
    page2.insert_text(pymupdf.Point(72, y), "Master of Science in Computer Science", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 14
    page2.insert_text(pymupdf.Point(72, y), "Stanford University, Stanford, CA — GPA: 3.92/4.0", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page2.insert_text(pymupdf.Point(420, y), "June 2016", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 18
    page2.insert_text(pymupdf.Point(72, y), "Bachelor of Science in Computer Engineering", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 14
    page2.insert_text(pymupdf.Point(72, y), "University of California, Berkeley — GPA: 3.85/4.0", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page2.insert_text(pymupdf.Point(420, y), "May 2014", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 25

    page2.insert_text(pymupdf.Point(72, y), "TECHNICAL SKILLS", fontsize=12, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 20
    skills = [
        ("Languages:", "Python, Go, Java, TypeScript, Rust, SQL"),
        ("Frameworks:", "Django, FastAPI, Spring Boot, React, gRPC"),
        ("Cloud & DevOps:", "AWS (ECS, Lambda, DynamoDB), GCP, Docker, Kubernetes, Terraform"),
        ("Data:", "PostgreSQL, Redis, Kafka, Apache Spark, Elasticsearch"),
        ("Tools:", "Git, Jenkins, GitHub Actions, Datadog, Grafana, Jira"),
    ]
    for label, values in skills:
        page2.insert_text(pymupdf.Point(72, y), label, fontsize=10, fontname="hebo", color=(0, 0, 0))
        page2.insert_text(pymupdf.Point(160, y), values, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 16

    y += 15
    page2.insert_text(pymupdf.Point(72, y), "CERTIFICATIONS", fontsize=12, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 20
    certs = [
        "AWS Certified Solutions Architect - Professional (2023)",
        "Certified Kubernetes Administrator (CKA) (2022)",
        "Google Cloud Professional Data Engineer (2021)",
    ]
    for cert in certs:
        page2.insert_text(pymupdf.Point(90, y), f"• {cert}", fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 16

    path = f'{PORTFOLIO_DIR}/resume.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({2} pages)')
    return path

def create_cover_letter():
    """Create a realistic 1-page cover letter PDF."""
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    y = 72

    page.insert_text(pymupdf.Point(72, y), "Elena Vasquez", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 18
    page.insert_text(pymupdf.Point(72, y), "1247 Mission Street, Apt 8B", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 14
    page.insert_text(pymupdf.Point(72, y), "San Francisco, CA 94103", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 14
    page.insert_text(pymupdf.Point(72, y), "elena.vasquez@email.com | (415) 555-0187", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 28

    page.insert_text(pymupdf.Point(72, y), "March 15, 2025", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 28

    page.insert_text(pymupdf.Point(72, y), "David Chen, VP of Engineering", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 14
    page.insert_text(pymupdf.Point(72, y), "Horizon Cloud Technologies", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 14
    page.insert_text(pymupdf.Point(72, y), "500 Howard Street, Suite 1200", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 14
    page.insert_text(pymupdf.Point(72, y), "San Francisco, CA 94105", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 28

    page.insert_text(pymupdf.Point(72, y), "Dear Mr. Chen,", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 22

    paragraphs = [
        "I am writing to express my strong interest in the Principal Engineer position at Horizon Cloud "
        "Technologies, as advertised on your careers page. With over eight years of experience building "
        "scalable distributed systems and leading high-performing engineering teams, I am confident in my "
        "ability to drive technical innovation and deliver exceptional results for your organization.",

        "In my current role as Lead Software Engineer at Meridian Technologies, I have architected an "
        "event-driven microservices platform that processes over 2 million events daily. I led a team of "
        "12 engineers through a complete cloud migration that reduced infrastructure costs by 40% while "
        "achieving 99.99% uptime. My experience with Kubernetes, Kafka, and AWS aligns directly with the "
        "cloud-native infrastructure that Horizon is building.",

        "What excites me most about Horizon Cloud Technologies is your commitment to democratizing cloud "
        "computing for mid-market enterprises. Having worked extensively with organizations transitioning "
        "to cloud-native architectures, I understand the unique challenges and opportunities in this space. "
        "I am particularly drawn to your multi-tenant platform architecture and would welcome the opportunity "
        "to contribute to its next phase of growth.",

        "I have enclosed my resume and work samples for your review. I would welcome the opportunity to "
        "discuss how my experience in distributed systems, team leadership, and cloud architecture can "
        "contribute to Horizon's mission. Thank you for your time and consideration.",
    ]

    for para in paragraphs:
        rect = pymupdf.Rect(72, y, 540, y + 65)
        page.insert_textbox(rect, para, fontsize=10.5, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 65

    y += 5
    page.insert_text(pymupdf.Point(72, y), "Sincerely,", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 28
    page.insert_text(pymupdf.Point(72, y), "Elena Vasquez", fontsize=11, fontname="heit", color=(0.1, 0.2, 0.4))

    path = f'{PORTFOLIO_DIR}/cover_letter.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({1} page)')
    return path

def create_work_samples():
    """Create a realistic 8-page work samples PDF."""
    doc = pymupdf.open()

    # Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(150, 300), "Work Samples Portfolio", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.4))
    page.insert_text(pymupdf.Point(200, 340), "Elena Vasquez — 2025", fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 355), pymupdf.Point(462, 355))
    shape.finish(color=(0.1, 0.2, 0.4), width=2)
    shape.commit()
    page.insert_text(pymupdf.Point(170, 390), "Distributed Systems | Cloud Architecture | Data Engineering", fontsize=12, fontname="heit", color=(0.4, 0.4, 0.4))

    # Project pages
    projects = [
        ("Project 1: Event-Driven Microservices Platform",
         "Meridian Technologies | 2021-2024",
         "Designed and implemented an event-driven architecture handling 2M+ events/day.",
         [
             "Architecture Overview: Built on Apache Kafka with Kubernetes orchestration. The platform consists of "
             "47 microservices communicating via async event streams. Each service owns its data store (PostgreSQL "
             "or DynamoDB) following the database-per-service pattern.",
             "Key Technical Decisions: Chose event sourcing over traditional CRUD for order processing pipeline, "
             "reducing data inconsistencies by 92%. Implemented saga pattern for distributed transactions across "
             "payment, inventory, and shipping services.",
             "Performance Results: Achieved p99 latency of 45ms for critical paths. System handles 25K concurrent "
             "connections with auto-scaling from 3 to 48 pods based on Kafka consumer lag metrics.",
             "Monitoring & Observability: Deployed comprehensive observability stack with Datadog APM, custom "
             "Grafana dashboards, and PagerDuty integration. Reduced MTTR from 45 minutes to 8 minutes.",
         ]),
        ("Project 2: Real-Time Analytics Pipeline",
         "Cascade Data Systems | 2019-2021",
         "Built data pipeline ingesting 500GB daily from 200+ source systems.",
         [
             "Pipeline Architecture: Designed lambda architecture combining batch (Apache Spark) and stream "
             "(Kafka Streams) processing. Data flows through ingestion, transformation, enrichment, and "
             "serving layers with exactly-once processing guarantees.",
             "Data Quality Framework: Implemented automated data quality checks using Great Expectations, "
             "catching 99.7% of data anomalies before they reach the serving layer. Created custom validation "
             "rules for financial data compliance (SOX, PCI-DSS).",
             "Cost Optimization: Migrated from EMR to Spark on Kubernetes, reducing compute costs by 55%. "
             "Implemented intelligent data partitioning and compaction reducing storage costs by 35%.",
             "Impact: Enabled real-time customer segmentation that increased marketing campaign ROI by 28%. "
             "Dashboard query latency improved from 30 seconds to under 2 seconds.",
         ]),
        ("Project 3: Cloud Migration & Infrastructure",
         "Meridian Technologies | 2022-2023",
         "Led migration of monolithic Java application to cloud-native microservices on AWS.",
         [
             "Migration Strategy: Adopted strangler fig pattern to incrementally decompose the monolith. "
             "Identified 12 bounded contexts and prioritized migration based on business value and technical debt. "
             "Created automated testing harness to verify behavioral parity during migration.",
             "Infrastructure as Code: All infrastructure defined in Terraform with modular composition. "
             "Implemented GitOps workflow using ArgoCD for Kubernetes deployments. Created reusable Terraform "
             "modules adopted by 5 other teams in the organization.",
             "Security & Compliance: Implemented zero-trust networking with Istio service mesh. All inter-service "
             "communication uses mTLS. Integrated HashiCorp Vault for secrets management with automatic rotation.",
             "Results: Reduced deployment frequency from monthly to multiple daily releases. Infrastructure costs "
             "decreased 40% through right-sizing and spot instance utilization. Team velocity increased 3x.",
         ]),
    ]

    for title, subtitle, summary, sections in projects:
        # First page of project
        page = doc.new_page(width=612, height=792)
        y = 72
        page.insert_text(pymupdf.Point(72, y), title, fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.4))
        y += 22
        page.insert_text(pymupdf.Point(72, y), subtitle, fontsize=11, fontname="heit", color=(0.4, 0.4, 0.4))
        y += 20
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        y += 15

        rect = pymupdf.Rect(72, y, 540, y + 35)
        page.insert_textbox(rect, summary, fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 45

        for i, section in enumerate(sections):
            rect = pymupdf.Rect(72, y, 540, y + 80)
            page.insert_textbox(rect, section, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 85

        # Second page of project with additional details / diagrams placeholder
        page2 = doc.new_page(width=612, height=792)
        y = 72
        page2.insert_text(pymupdf.Point(72, y), f"{title} — Technical Details", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))
        y += 25

        # Draw architecture diagram placeholder
        shape2 = page2.new_shape()
        diagram_rect = pymupdf.Rect(100, y, 512, y + 180)
        shape2.draw_rect(diagram_rect)
        shape2.finish(color=(0.6, 0.6, 0.6), fill=(0.95, 0.95, 0.98), width=1)
        shape2.commit()
        page2.insert_text(pymupdf.Point(240, y + 90), "Architecture Diagram", fontsize=12, fontname="heit", color=(0.5, 0.5, 0.5))
        y += 200

        tech_details = [
            "Technology Stack: The solution leverages industry-standard tools and frameworks chosen for "
            "reliability, scalability, and team expertise. All components are containerized and deployed "
            "via Helm charts with environment-specific value overrides.",
            "Testing Strategy: Comprehensive test suite including unit tests (pytest), integration tests "
            "(Testcontainers), contract tests (Pact), and end-to-end tests (Cypress). Test coverage "
            "maintained above 90% with automated quality gates in CI pipeline.",
            "Lessons Learned: Early investment in observability pays dividends during incident response. "
            "Feature flags enable safe deployment of risky changes. Documentation-driven development "
            "improves onboarding time and cross-team collaboration significantly.",
        ]
        for detail in tech_details:
            rect = pymupdf.Rect(72, y, 540, y + 70)
            page2.insert_textbox(rect, detail, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 75

    # Final page (page 8) - Summary / Contact
    page_final = doc.new_page(width=612, height=792)
    y = 200
    page_final.insert_text(pymupdf.Point(180, y), "Thank You", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.4))
    y += 50
    rect = pymupdf.Rect(120, y, 492, y + 40)
    page_final.insert_textbox(rect,
        "For additional details on any project, or to discuss collaboration opportunities, "
        "please reach out via email or LinkedIn.",
        fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3), align=pymupdf.TEXT_ALIGN_CENTER)
    y += 60
    page_final.insert_text(pymupdf.Point(200, y), "elena.vasquez@email.com", fontsize=12, fontname="helv", color=(0.1, 0.2, 0.4))
    y += 20
    page_final.insert_text(pymupdf.Point(200, y), "linkedin.com/in/elenavasquez", fontsize=12, fontname="helv", color=(0.1, 0.2, 0.4))

    path = f'{PORTFOLIO_DIR}/work_samples.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({8} pages)')
    return path

def create_initial():
    os.makedirs(PORTFOLIO_DIR, exist_ok=True)

    resume_path = create_resume()
    cover_letter_path = create_cover_letter()
    work_samples_path = create_work_samples()

    # Verify page counts
    for name, expected in [('resume.pdf', 2), ('cover_letter.pdf', 1), ('work_samples.pdf', 8)]:
        doc = pymupdf.open(f'{PORTFOLIO_DIR}/{name}')
        actual = doc.page_count
        doc.close()
        print(f'  {name}: {actual} pages (expected {expected})')
        assert actual == expected, f'{name} has {actual} pages, expected {expected}'

    print(f'\nAll source PDFs created in {PORTFOLIO_DIR}')

    # Open file manager to show the portfolio directory (GUI-ready state)
    launch_gui(f'nautilus "{PORTFOLIO_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')

create_initial()
