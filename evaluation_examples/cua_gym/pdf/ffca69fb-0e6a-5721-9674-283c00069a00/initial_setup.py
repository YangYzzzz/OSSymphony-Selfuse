"""
Initial Setup: Create project_charter.pdf with an existing sticky note annotation on page 2
Task ID: pdf_basic_092
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

WORKDIR = '/home/user/Desktop'
TASK_ID = 'project_charter'
OUTPUT = f'{WORKDIR}/{TASK_ID}.pdf'


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
    doc = pymupdf.open()

    # ---- PAGE 1: Cover / Introduction ----
    page1 = doc.new_page(width=612, height=792)

    # Title
    page1.insert_text(
        pymupdf.Point(72, 80),
        "PROJECT CHARTER",
        fontsize=28,
        fontname="hebo",
        color=(0.05, 0.2, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(72, 120),
        "Enterprise Resource Planning (ERP) System Modernization",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.1),
    )

    # Separator line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 135), pymupdf.Point(540, 135))
    shape.finish(color=(0.05, 0.2, 0.5), width=2)
    shape.commit()

    # Document metadata block
    meta_lines = [
        ("Project ID:", "PRJ-2025-047"),
        ("Version:", "1.3"),
        ("Status:", "Active"),
        ("Date Issued:", "January 15, 2025"),
        ("Prepared by:", "Dr. Alexandra Pemberton, PMO Director"),
        ("Sponsor:", "Marcus T. Hollingsworth, Chief Operating Officer"),
    ]
    y = 165
    for label, value in meta_lines:
        page1.insert_text(pymupdf.Point(90, y), label, fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
        page1.insert_text(pymupdf.Point(200, y), value, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 20

    # Section: Executive Summary
    page1.insert_text(pymupdf.Point(72, 310), "1. Executive Summary", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 322), pymupdf.Point(540, 322))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    summary_text = (
        "This Project Charter formally authorizes the Enterprise Resource Planning (ERP) System "
        "Modernization project for Nexus Global Solutions, Inc. The initiative addresses critical "
        "limitations in our legacy SAP R/3 infrastructure, which has been in operation since 2009 "
        "and no longer meets the scalability and integration requirements of our expanded operations "
        "across 14 international offices.\n\n"
        "The modernization effort will migrate core business processes — including finance, supply "
        "chain management, human resources, and procurement — to SAP S/4HANA Cloud, with phased "
        "deployment across three regional clusters beginning Q2 2025."
    )
    rect1 = pymupdf.Rect(72, 335, 540, 560)
    page1.insert_textbox(rect1, summary_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    # Section: Project Objectives
    page1.insert_text(pymupdf.Point(72, 580), "2. Project Objectives", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 592), pymupdf.Point(540, 592))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    objectives = [
        "1. Decommission legacy SAP R/3 system by December 31, 2025.",
        "2. Achieve full S/4HANA Cloud deployment across all regional offices by Q4 2025.",
        "3. Reduce IT infrastructure operating costs by 30% within 18 months post-launch.",
        "4. Improve reporting cycle time from 5 days to real-time dashboards.",
        "5. Ensure 99.9% system uptime SLA compliance post-migration.",
    ]
    y = 610
    for obj in objectives:
        page1.insert_text(pymupdf.Point(90, y), obj, fontsize=10.5, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 18

    # Footer
    page1.insert_text(pymupdf.Point(72, 760), "CONFIDENTIAL — NEXUS GLOBAL SOLUTIONS, INC.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page1.insert_text(pymupdf.Point(500, 760), "Page 1 of 5", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 2: Scope & Stakeholders ----
    page2 = doc.new_page(width=612, height=792)

    page2.insert_text(pymupdf.Point(72, 60), "3. Project Scope", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    scope_text = (
        "The scope of this project encompasses the full lifecycle migration from the existing SAP R/3 "
        "platform to SAP S/4HANA Cloud, including data migration, process redesign, integration "
        "development, user training, and hypercare support. The following functional modules are "
        "in scope:\n\n"
        "IN SCOPE:\n"
        "  • Financial Accounting (FI) and Controlling (CO)\n"
        "  • Materials Management (MM) and Procurement\n"
        "  • Sales and Distribution (SD)\n"
        "  • Human Capital Management (HCM)\n"
        "  • Plant Maintenance (PM)\n"
        "  • Business Intelligence and Analytics (BW/4HANA)\n\n"
        "OUT OF SCOPE:\n"
        "  • Custom legacy third-party integrations (separate project)\n"
        "  • Customer Relationship Management (CRM) — deferred to Phase 2\n"
        "  • Physical hardware procurement and data center upgrades"
    )
    rect2 = pymupdf.Rect(72, 85, 540, 380)
    page2.insert_textbox(rect2, scope_text, fontsize=10.5, fontname="helv", color=(0.1, 0.1, 0.1))

    page2.insert_text(pymupdf.Point(72, 400), "4. Key Stakeholders", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(72, 412), pymupdf.Point(540, 412))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    stakeholders = [
        ("Executive Sponsor", "Marcus T. Hollingsworth", "COO"),
        ("Project Manager", "Dr. Alexandra Pemberton", "PMO"),
        ("Technical Lead", "Rajiv Subramaniam", "IT Architecture"),
        ("Business Analyst Lead", "Carolyn Whitfield", "Finance"),
        ("Change Management", "Derek Okonkwo", "HR"),
        ("SAP Implementation Partner", "Accenture Federal Services", "External"),
        ("Quality Assurance Lead", "Svetlana Kozlov", "IT QA"),
    ]

    # Table header
    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(72, 422, 540, 442))
    shape.finish(color=(0.05, 0.2, 0.5), fill=(0.05, 0.2, 0.5), width=0)
    shape.commit()

    page2.insert_text(pymupdf.Point(78, 436), "Role", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page2.insert_text(pymupdf.Point(220, 436), "Name", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page2.insert_text(pymupdf.Point(380, 436), "Department", fontsize=10, fontname="hebo", color=(1, 1, 1))

    y = 455
    for i, (role, name, dept) in enumerate(stakeholders):
        bg_color = (0.93, 0.95, 0.98) if i % 2 == 0 else (1, 1, 1)
        shape = page2.new_shape()
        shape.draw_rect(pymupdf.Rect(72, y - 12, 540, y + 6))
        shape.finish(color=bg_color, fill=bg_color, width=0)
        shape.commit()
        page2.insert_text(pymupdf.Point(78, y), role, fontsize=9.5, fontname="helv", color=(0.1, 0.1, 0.1))
        page2.insert_text(pymupdf.Point(220, y), name, fontsize=9.5, fontname="helv", color=(0.1, 0.1, 0.1))
        page2.insert_text(pymupdf.Point(380, y), dept, fontsize=9.5, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 19

    # ---- ADD EXISTING STICKY NOTE ANNOTATION ON PAGE 2 ----
    # This is the old sticky note that the agent must DELETE
    annot = page2.add_text_annot(
        pymupdf.Point(490, 400),
        "Pending review by finance committee - awaiting sign-off from CFO",
        icon="Note"
    )
    annot.set_colors(stroke=(1, 0.6, 0.0))  # orange icon color
    annot.set_info(title="J. Reynolds", content="Pending review by finance committee - awaiting sign-off from CFO")
    annot.update()

    # Footer
    page2.insert_text(pymupdf.Point(72, 760), "CONFIDENTIAL — NEXUS GLOBAL SOLUTIONS, INC.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page2.insert_text(pymupdf.Point(500, 760), "Page 2 of 5", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 3: Timeline & Budget ----
    page3 = doc.new_page(width=612, height=792)

    page3.insert_text(pymupdf.Point(72, 60), "5. Project Timeline", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page3.new_shape()
    shape.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    milestones = [
        ("Phase 1 Kickoff", "January 20, 2025", "Project team assembled, initial workshops complete"),
        ("Blueprint Design", "March 14, 2025", "Business process redesign documents finalized"),
        ("Development Complete", "June 30, 2025", "All custom ABAP development and integrations ready"),
        ("UAT Start", "July 15, 2025", "User Acceptance Testing begins with key business users"),
        ("UAT Sign-off", "August 29, 2025", "All UAT defects resolved, formal sign-off received"),
        ("Go-Live Region 1", "September 15, 2025", "EMEA offices go live on SAP S/4HANA Cloud"),
        ("Go-Live Region 2", "November 1, 2025", "APAC offices go live"),
        ("Go-Live Region 3", "December 1, 2025", "Americas offices go live, full rollout complete"),
        ("Hypercare End", "March 31, 2026", "30-day hypercare period ends, BAU support begins"),
    ]

    # Table header
    shape = page3.new_shape()
    shape.draw_rect(pymupdf.Rect(72, 82, 540, 100))
    shape.finish(color=(0.05, 0.2, 0.5), fill=(0.05, 0.2, 0.5), width=0)
    shape.commit()
    page3.insert_text(pymupdf.Point(78, 95), "Milestone", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page3.insert_text(pymupdf.Point(215, 95), "Target Date", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page3.insert_text(pymupdf.Point(315, 95), "Description", fontsize=10, fontname="hebo", color=(1, 1, 1))

    y = 116
    for i, (milestone, date, desc) in enumerate(milestones):
        bg_color = (0.93, 0.95, 0.98) if i % 2 == 0 else (1, 1, 1)
        shape = page3.new_shape()
        shape.draw_rect(pymupdf.Rect(72, y - 12, 540, y + 8))
        shape.finish(color=bg_color, fill=bg_color, width=0)
        shape.commit()
        page3.insert_text(pymupdf.Point(78, y), milestone, fontsize=9, fontname="hebo", color=(0.1, 0.1, 0.1))
        page3.insert_text(pymupdf.Point(215, y), date, fontsize=9, fontname="helv", color=(0.1, 0.1, 0.1))
        page3.insert_text(pymupdf.Point(315, y), desc, fontsize=8.5, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 22

    page3.insert_text(pymupdf.Point(72, 340), "6. Budget Summary", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page3.new_shape()
    shape.draw_line(pymupdf.Point(72, 352), pymupdf.Point(540, 352))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    budget_items = [
        ("SAP S/4HANA Cloud Licensing (3-year)", "$1,250,000"),
        ("Accenture Implementation Services", "$3,800,000"),
        ("Internal IT Staff (dedicated)", "$620,000"),
        ("Training & Change Management", "$180,000"),
        ("Data Migration & Testing Tools", "$95,000"),
        ("Infrastructure & Security Upgrades", "$210,000"),
        ("Contingency Reserve (10%)", "$615,500"),
        ("TOTAL PROJECT BUDGET", "$6,770,500"),
    ]

    y = 370
    for i, (item, amount) in enumerate(budget_items):
        if item.startswith("TOTAL"):
            shape = page3.new_shape()
            shape.draw_rect(pymupdf.Rect(72, y - 12, 540, y + 8))
            shape.finish(color=(0.85, 0.9, 0.95), fill=(0.85, 0.9, 0.95), width=0)
            shape.commit()
            page3.insert_text(pymupdf.Point(78, y), item, fontsize=10, fontname="hebo", color=(0.05, 0.2, 0.5))
            page3.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="hebo", color=(0.05, 0.2, 0.5))
        else:
            page3.insert_text(pymupdf.Point(78, y), item, fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
            page3.insert_text(pymupdf.Point(460, y), amount, fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    page3.insert_text(pymupdf.Point(72, 760), "CONFIDENTIAL — NEXUS GLOBAL SOLUTIONS, INC.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page3.insert_text(pymupdf.Point(500, 760), "Page 3 of 5", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 4: Risks & Assumptions ----
    page4 = doc.new_page(width=612, height=792)

    page4.insert_text(pymupdf.Point(72, 60), "7. Risk Register", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page4.new_shape()
    shape.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    risks = [
        ("R-001", "Data Migration Integrity Loss", "High", "Critical", "Engage specialist data migration consultants; run parallel systems for 60 days post go-live"),
        ("R-002", "Key User Resistance to Change", "Medium", "High", "Dedicated change management program; executive sponsorship communications"),
        ("R-003", "SAP Licensing Cost Overrun", "Low", "High", "Fixed-price contract negotiated; quarterly license reconciliation"),
        ("R-004", "Integration Failures with Legacy Systems", "High", "Medium", "API gateway architecture; staged integration testing protocol"),
        ("R-005", "Timeline Delay due to Resource Unavailability", "Medium", "Medium", "Resource backup plans; vendor SLAs for consultant availability"),
        ("R-006", "Security Vulnerabilities in Cloud Migration", "Low", "Critical", "Penetration testing; ISO 27001 audit; cloud security posture management"),
    ]

    y = 90
    for i, (rid, risk, prob, impact, mitigation) in enumerate(risks):
        bg_color = (0.98, 0.95, 0.93) if i % 2 == 0 else (1, 1, 1)
        shape = page4.new_shape()
        shape.draw_rect(pymupdf.Rect(72, y, 540, y + 50))
        shape.finish(color=bg_color, fill=bg_color, width=0)
        shape.commit()
        shape2 = page4.new_shape()
        shape2.draw_rect(pymupdf.Rect(72, y, 540, y + 50))
        shape2.finish(color=(0.8, 0.8, 0.8), width=0.3)
        shape2.commit()
        page4.insert_text(pymupdf.Point(78, y + 14), f"{rid}: {risk}", fontsize=9.5, fontname="hebo", color=(0.1, 0.1, 0.1))
        page4.insert_text(pymupdf.Point(78, y + 28), f"Probability: {prob}  |  Impact: {impact}", fontsize=8.5, fontname="helv", color=(0.4, 0.4, 0.4))
        page4.insert_text(pymupdf.Point(78, y + 42), f"Mitigation: {mitigation}", fontsize=8, fontname="helv", color=(0.2, 0.4, 0.2))
        y += 58

    page4.insert_text(pymupdf.Point(72, 460), "8. Assumptions & Constraints", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page4.new_shape()
    shape.draw_line(pymupdf.Point(72, 472), pymupdf.Point(540, 472))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    assumptions = [
        "Executive leadership will provide timely decisions and approvals within 5 business days.",
        "SAP S/4HANA Cloud environment will be provisioned by Accenture within agreed SLA timelines.",
        "Business unit SMEs will be available for at least 30% of their time during UAT phase.",
        "Existing network infrastructure is sufficient to support cloud-based ERP operations.",
        "All data cleansing activities will be completed by the data migration team by May 31, 2025.",
        "Legal and compliance review of cloud data residency requirements will conclude by Feb 28, 2025.",
    ]

    y = 490
    for assumption in assumptions:
        page4.insert_text(pymupdf.Point(90, y), f"• {assumption}", fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    page4.insert_text(pymupdf.Point(72, 760), "CONFIDENTIAL — NEXUS GLOBAL SOLUTIONS, INC.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page4.insert_text(pymupdf.Point(500, 760), "Page 4 of 5", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 5: Approval & Sign-off ----
    page5 = doc.new_page(width=612, height=792)

    page5.insert_text(pymupdf.Point(72, 60), "9. Approvals & Authorization", fontsize=14, fontname="hebo", color=(0.05, 0.2, 0.5))
    shape = page5.new_shape()
    shape.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    approval_text = (
        "By signing below, the named individuals acknowledge that they have reviewed this Project "
        "Charter and authorize the initiation of the ERP System Modernization Project as described "
        "herein. This document will serve as the formal agreement between the project team and the "
        "sponsoring organization."
    )
    rect5 = pymupdf.Rect(72, 85, 540, 150)
    page5.insert_textbox(rect5, approval_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    signatories = [
        ("Marcus T. Hollingsworth", "Chief Operating Officer", "Executive Sponsor"),
        ("Dr. Alexandra Pemberton", "PMO Director", "Project Manager"),
        ("Rajiv Subramaniam", "VP IT Architecture", "Technical Lead"),
        ("Sandra Ellison-Park", "Chief Financial Officer", "Budget Authority"),
        ("Thomas R. Blackwell", "Chief Information Officer", "IT Governance"),
    ]

    y = 175
    for name, title, role in signatories:
        # Signature block
        shape = page5.new_shape()
        shape.draw_rect(pymupdf.Rect(72, y, 540, y + 70))
        shape.finish(color=(0.94, 0.96, 0.99), fill=(0.94, 0.96, 0.99), width=0)
        shape.commit()
        shape2 = page5.new_shape()
        shape2.draw_rect(pymupdf.Rect(72, y, 540, y + 70))
        shape2.finish(color=(0.75, 0.8, 0.88), width=0.7)
        shape2.commit()

        page5.insert_text(pymupdf.Point(82, y + 18), "Name:", fontsize=9, fontname="hebo", color=(0.3, 0.3, 0.3))
        page5.insert_text(pymupdf.Point(130, y + 18), name, fontsize=10, fontname="hebo", color=(0.05, 0.2, 0.5))
        page5.insert_text(pymupdf.Point(82, y + 33), "Title:", fontsize=9, fontname="hebo", color=(0.3, 0.3, 0.3))
        page5.insert_text(pymupdf.Point(130, y + 33), title, fontsize=9.5, fontname="helv", color=(0.1, 0.1, 0.1))
        page5.insert_text(pymupdf.Point(82, y + 47), "Role:", fontsize=9, fontname="hebo", color=(0.3, 0.3, 0.3))
        page5.insert_text(pymupdf.Point(130, y + 47), role, fontsize=9.5, fontname="helv", color=(0.1, 0.1, 0.1))

        # Signature line
        shape3 = page5.new_shape()
        shape3.draw_line(pymupdf.Point(350, y + 52), pymupdf.Point(530, y + 52))
        shape3.finish(color=(0.4, 0.4, 0.4), width=0.8)
        shape3.commit()
        page5.insert_text(pymupdf.Point(350, y + 62), "Signature / Date", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

        y += 82

    page5.insert_text(pymupdf.Point(72, 760), "CONFIDENTIAL — NEXUS GLOBAL SOLUTIONS, INC.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page5.insert_text(pymupdf.Point(500, 760), "Page 5 of 5", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Ensure output directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open project_charter.pdf in Evince at page 2
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.5)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
