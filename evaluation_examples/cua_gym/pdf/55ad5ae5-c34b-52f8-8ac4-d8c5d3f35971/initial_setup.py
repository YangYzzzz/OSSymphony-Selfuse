"""
Initial Setup: Create a 6-page reviewed draft PDF with 12 annotations
Task ID: pdf_gf1_026
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_026'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/reviewed_draft.pdf'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 120), "Strategic Technology Roadmap 2025-2027",
                     fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.3))
    page.insert_text(pymupdf.Point(72, 160), "Prepared by: Elena Martinez, VP of Engineering",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 185), "Date: March 15, 2025",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 210), "Status: Draft - Under Review",
                     fontsize=12, fontname="hebo", color=(0.7, 0.0, 0.0))

    rect = pymupdf.Rect(72, 260, 523, 500)
    page.insert_textbox(rect,
        "This document outlines the technology strategy for Meridian Systems Inc. over the next "
        "three fiscal years. It covers infrastructure modernization, AI integration roadmap, "
        "security framework updates, and talent development initiatives. All department heads "
        "are requested to review sections relevant to their teams and provide feedback by "
        "April 1, 2025. Key stakeholders include the CTO, VP of Product, Director of IT "
        "Operations, and Chief Information Security Officer.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Annotation 1: Sticky note on title page
    annot = page.add_text_annot(
        pymupdf.Point(450, 115),
        "Should we update the title to include Q3 focus areas? - David",
        icon="Comment"
    )
    annot.set_colors(stroke=(1, 0.8, 0))
    annot.update()

    # Annotation 2: Highlight on "Draft - Under Review"
    instances = page.search_for("Draft - Under Review")
    if instances:
        annot = page.add_highlight_annot(instances[0])
        annot.set_colors(stroke=(1, 1, 0))
        annot.update()

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 100, 523, 350)
    page.insert_textbox(rect,
        "Meridian Systems is entering a critical phase of digital transformation. Our legacy "
        "infrastructure, while reliable, is approaching end-of-life for several core components. "
        "The proposed roadmap allocates $4.2M in FY2025, $3.8M in FY2026, and $2.9M in FY2027 "
        "toward modernization efforts. Key initiatives include migrating 60% of on-premise "
        "workloads to AWS by Q4 2025, implementing a unified observability platform, and "
        "establishing an internal ML operations team. The expected ROI is a 35% reduction in "
        "operational costs by 2027 and a 50% improvement in deployment frequency.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 380), "1.1 Budget Overview",
                     fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 405, 523, 550)
    page.insert_textbox(rect,
        "The total three-year investment is projected at $10.9M, distributed across four "
        "primary pillars: Infrastructure (42%), AI/ML Integration (25%), Security (20%), "
        "and Talent Development (13%). This represents a 15% increase over the previous "
        "three-year cycle, justified by the accelerated pace of technological change and "
        "competitive pressure from emerging market players.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Annotation 3: Highlight on budget figure
    instances = page.search_for("$4.2M in FY2025")
    if instances:
        annot = page.add_highlight_annot(instances[0])
        annot.set_colors(stroke=(0.6, 1, 0.6))  # green highlight
        annot.update()

    # Annotation 4: Sticky note about ROI
    annot = page.add_text_annot(
        pymupdf.Point(500, 280),
        "The 35% cost reduction seems optimistic. Can we get supporting data from finance? - Sarah",
        icon="Note"
    )
    annot.set_colors(stroke=(1, 0.5, 0.5))
    annot.update()

    # --- Page 3: Infrastructure Modernization ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "2. Infrastructure Modernization",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 100, 523, 320)
    page.insert_textbox(rect,
        "The infrastructure modernization initiative targets the migration of our primary "
        "data center operations to a hybrid cloud architecture. Currently, Meridian operates "
        "312 physical servers across two data centers in Portland and Atlanta. Phase 1 involves "
        "migrating non-critical development environments (estimated 85 servers) to AWS EC2 and "
        "EKS by June 2025. Phase 2 will address production workloads with a blue-green "
        "deployment strategy, targeting September 2025 for the first production migration. "
        "The Portland facility will be retained as a disaster recovery site with reduced "
        "capacity, while the Atlanta lease will be evaluated for early termination, potentially "
        "saving $180,000 annually.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 350), "2.1 Migration Timeline",
                     fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 375, 523, 520)
    page.insert_textbox(rect,
        "Q1 2025: Assessment and planning, vendor selection\n"
        "Q2 2025: Dev/staging environment migration (85 servers)\n"
        "Q3 2025: First production workload migration (40 servers)\n"
        "Q4 2025: Remaining production workloads (120 servers)\n"
        "Q1-Q2 2026: Legacy system decommissioning and optimization\n"
        "Q3 2026: Full hybrid operation validation",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Annotation 5: Underline on "blue-green deployment"
    instances = page.search_for("blue-green deployment strategy")
    if instances:
        annot = page.add_underline_annot(instances[0])
        annot.set_colors(stroke=(0, 0, 1))
        annot.update()

    # Annotation 6: Sticky note on timeline
    annot = page.add_text_annot(
        pymupdf.Point(480, 370),
        "Q3 seems aggressive for production migration. Need buffer for compliance checks. - Raj",
        icon="Comment"
    )
    annot.set_colors(stroke=(0.3, 0.6, 1))
    annot.update()

    # --- Page 4: AI/ML Integration ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "3. AI and Machine Learning Integration",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 100, 523, 350)
    page.insert_textbox(rect,
        "The AI/ML integration pillar represents our most forward-looking investment. We propose "
        "establishing a dedicated MLOps team of 6 engineers, led by a Principal ML Engineer hire "
        "targeted for Q2 2025. Initial projects include deploying predictive maintenance models "
        "for our SaaS platform, reducing customer churn by an estimated 12-18% through proactive "
        "engagement scoring, and automating 40% of tier-1 support tickets using a fine-tuned "
        "language model. The infrastructure will be built on AWS SageMaker with a projected "
        "compute budget of $45,000/month in year one, scaling to $72,000/month by year three "
        "as model complexity increases.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 380), "3.1 Priority Use Cases",
                     fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 405, 523, 560)
    page.insert_textbox(rect,
        "1. Predictive Maintenance Alerts - Reduce downtime by 28%\n"
        "2. Customer Churn Prediction - Improve retention by 12-18%\n"
        "3. Automated Support Triage - Handle 40% of tier-1 tickets\n"
        "4. Revenue Forecasting - Accuracy improvement from 78% to 92%\n"
        "5. Anomaly Detection - Real-time infrastructure monitoring",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Annotation 7: Highlight on compute budget
    instances = page.search_for("$45,000/month")
    if instances:
        annot = page.add_highlight_annot(instances[0])
        annot.set_colors(stroke=(1, 0.8, 0.5))  # orange highlight
        annot.update()

    # Annotation 8: Underline on MLOps team
    instances = page.search_for("dedicated MLOps team of 6 engineers")
    if instances:
        annot = page.add_underline_annot(instances[0])
        annot.set_colors(stroke=(0.8, 0, 0))
        annot.update()

    # --- Page 5: Security Framework ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "4. Security Framework Updates",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 100, 523, 350)
    page.insert_textbox(rect,
        "Our security posture requires significant strengthening to support the cloud migration "
        "and AI initiatives. The current SOC 2 Type II certification will be maintained while "
        "we pursue ISO 27001 certification by Q4 2026. Key investments include implementing a "
        "zero-trust network architecture, deploying endpoint detection and response across all "
        "employee devices (approximately 850 endpoints), and establishing a 24/7 security "
        "operations center through a managed services partnership with CrowdStrike. Annual "
        "penetration testing will be supplemented with continuous automated vulnerability "
        "scanning using Qualys. The security budget of $2.18M over three years includes "
        "$400,000 for an incident response retainer.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 380), "4.1 Compliance Roadmap",
                     fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 405, 523, 520)
    page.insert_textbox(rect,
        "SOC 2 Type II - Maintain (ongoing)\n"
        "ISO 27001 - Target Q4 2026\n"
        "GDPR Compliance Audit - Q2 2025\n"
        "PCI DSS Level 1 - Q1 2026\n"
        "HIPAA Readiness Assessment - Q3 2026 (contingent on healthcare vertical expansion)",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Annotation 9: Sticky note on security
    annot = page.add_text_annot(
        pymupdf.Point(490, 95),
        "We should also consider FedRAMP if we're pursuing government contracts. - Lisa",
        icon="Note"
    )
    annot.set_colors(stroke=(1, 0.6, 0.8))
    annot.update()

    # Annotation 10: Highlight on zero-trust
    instances = page.search_for("zero-trust network architecture")
    if instances:
        annot = page.add_highlight_annot(instances[0])
        annot.set_colors(stroke=(0.5, 0.8, 1))  # light blue highlight
        annot.update()

    # --- Page 6: Talent Development ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "5. Talent Development",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 100, 523, 350)
    page.insert_textbox(rect,
        "The success of all technical initiatives depends on our ability to attract, retain, "
        "and upskill engineering talent. The talent development pillar allocates $1.42M over "
        "three years for training programs, conference attendance, certification support, and "
        "a new internal mentorship platform. Specific initiatives include sponsoring 20 engineers "
        "for AWS Solutions Architect certification, launching a bi-annual hackathon with $25,000 "
        "in prizes, and establishing partnerships with three universities for intern pipelines. "
        "Attrition in the engineering department was 18% last year; our target is to reduce this "
        "to below 10% by implementing competitive compensation reviews and flexible work "
        "arrangements.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 380), "5.1 Key Hires Planned",
                     fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.3))

    rect = pymupdf.Rect(72, 405, 523, 550)
    page.insert_textbox(rect,
        "Principal ML Engineer - Q2 2025 ($220K-$260K)\n"
        "Senior Cloud Architect - Q1 2025 ($195K-$230K)\n"
        "Security Operations Lead - Q2 2025 ($175K-$210K)\n"
        "DevOps Engineers (x3) - Q1-Q2 2025 ($140K-$165K each)\n"
        "Data Engineers (x2) - Q3 2025 ($150K-$180K each)",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Annotation 11: Underline on attrition
    instances = page.search_for("18% last year")
    if instances:
        annot = page.add_underline_annot(instances[0])
        annot.set_colors(stroke=(1, 0, 0))
        annot.update()

    # Annotation 12: Sticky note about compensation
    annot = page.add_text_annot(
        pymupdf.Point(460, 400),
        "These salary ranges need approval from HR and finance before publishing. - Michael",
        icon="Comment"
    )
    annot.set_colors(stroke=(0.9, 0.9, 0))
    annot.update()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify annotations count
    doc = pymupdf.open(OUTPUT)
    total_annots = 0
    for p in doc:
        total_annots += len(list(p.annots()))
    doc.close()
    print(f'Total annotations: {total_annots}')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
