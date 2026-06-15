"""
Initial Setup: Create a 3-page business letter PDF with no header/letterhead.
Task ID: pdf_cross_086
Domain: pdf (cross-domain with gimp)
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
TASK_ID = 'pdf_cross_086'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT_PDF = f'{DOCS_DIR}/business_letter.pdf'


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

    # Create a 3-page business letter PDF using pymupdf
    doc = pymupdf.open()

    # --- Page 1: Cover Letter ---
    page1 = doc.new_page(width=612, height=792)

    # Sender address block
    page1.insert_text(pymupdf.Point(72, 72), "Meridian Solutions", fontsize=12, fontname="hebo")
    page1.insert_text(pymupdf.Point(72, 88), "1420 Harbor Boulevard, Suite 300", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 103), "San Francisco, CA 94105", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 118), "Tel: (415) 882-4400  |  Fax: (415) 882-4401", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 133), "Email: info@meridiansolutions.com", fontsize=11, fontname="helv")

    # Separator line
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 150), pymupdf.Point(540, 150))
    shape1.finish(color=(0.5, 0.5, 0.5), width=1)
    shape1.commit()

    # Date and recipient
    page1.insert_text(pymupdf.Point(72, 175), "March 14, 2025", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 210), "Mr. Jonathan Reyes", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 225), "Chief Procurement Officer", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 240), "Pinnacle Industrial Group", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 255), "8200 Commerce Drive", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 270), "Houston, TX 77001", fontsize=11, fontname="helv")

    # Subject
    page1.insert_text(pymupdf.Point(72, 310), "Re: Enterprise Software Integration Proposal — Project Titan", fontsize=11, fontname="hebo")

    # Salutation
    page1.insert_text(pymupdf.Point(72, 340), "Dear Mr. Reyes,", fontsize=11, fontname="helv")

    # Body paragraphs
    body1 = (
        "We are pleased to submit this proposal for the Enterprise Software Integration "
        "initiative at Pinnacle Industrial Group, as discussed during our meeting on "
        "February 28, 2025. Meridian Solutions has successfully delivered end-to-end "
        "digital transformation projects for over 85 organizations across the manufacturing "
        "and logistics sectors over the past twelve years."
    )
    excess = page1.insert_textbox(
        pymupdf.Rect(72, 365, 540, 430),
        body1,
        fontsize=11,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_JUSTIFY
    )

    body2 = (
        "Our proposed solution, Project Titan, encompasses a fully integrated ERP platform "
        "built on Microsoft Dynamics 365, complemented by a custom middleware layer that "
        "will seamlessly interface with your existing SAP legacy systems. The implementation "
        "roadmap is structured across three phases spanning eighteen months, with each phase "
        "delivering measurable operational improvements."
    )
    excess = page1.insert_textbox(
        pymupdf.Rect(72, 445, 540, 510),
        body2,
        fontsize=11,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_JUSTIFY
    )

    body3 = (
        "Phase I (Months 1–4) covers foundational infrastructure deployment and data "
        "migration from legacy systems. Phase II (Months 5–11) delivers core module "
        "go-live for Finance, Supply Chain, and HR Management. Phase III (Months 12–18) "
        "focuses on advanced analytics integration, mobile workforce applications, and "
        "comprehensive user training programs."
    )
    excess = page1.insert_textbox(
        pymupdf.Rect(72, 525, 540, 595),
        body3,
        fontsize=11,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_JUSTIFY
    )

    page1.insert_text(pymupdf.Point(72, 620), "Please refer to the enclosed technical specifications and cost breakdown on the", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 635), "following pages for full details.", fontsize=11, fontname="helv")

    # Closing
    page1.insert_text(pymupdf.Point(72, 670), "Sincerely,", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 710), "Alexandra Hartmann", fontsize=11, fontname="hebo")
    page1.insert_text(pymupdf.Point(72, 725), "Vice President, Enterprise Solutions", fontsize=11, fontname="helv")
    page1.insert_text(pymupdf.Point(72, 740), "Meridian Solutions", fontsize=11, fontname="helv")

    # --- Page 2: Technical Specifications ---
    page2 = doc.new_page(width=612, height=792)

    page2.insert_text(pymupdf.Point(72, 72), "Technical Specifications — Project Titan", fontsize=14, fontname="hebo")

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 92), pymupdf.Point(540, 92))
    shape2.finish(color=(0.2, 0.2, 0.6), width=1.5)
    shape2.commit()

    page2.insert_text(pymupdf.Point(72, 115), "1. Platform Architecture", fontsize=12, fontname="hebo")
    arch_text = (
        "The proposed solution leverages a cloud-native microservices architecture hosted "
        "on Microsoft Azure (East US region). Core services will be containerized using "
        "Docker and orchestrated via Azure Kubernetes Service (AKS), ensuring high "
        "availability with a guaranteed 99.95% uptime SLA."
    )
    page2.insert_textbox(pymupdf.Rect(72, 130, 540, 185), arch_text, fontsize=11, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 205), "2. Integration Capabilities", fontsize=12, fontname="hebo")
    integ_text = (
        "Middleware integration will be implemented using MuleSoft Anypoint Platform, "
        "enabling real-time data exchange between Microsoft Dynamics 365 and your existing "
        "SAP ECC 6.0 installation. The integration layer supports REST, SOAP, and EDI "
        "protocols, with message throughput capacity of 50,000 transactions per hour."
    )
    page2.insert_textbox(pymupdf.Rect(72, 220, 540, 275), integ_text, fontsize=11, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 295), "3. Data Security & Compliance", fontsize=12, fontname="hebo")
    sec_text = (
        "All data in transit and at rest will be encrypted using AES-256 and TLS 1.3 "
        "protocols. The platform is compliant with SOC 2 Type II, ISO 27001, and GDPR "
        "requirements. Role-based access control (RBAC) and multi-factor authentication "
        "(MFA) will be enforced across all user accounts."
    )
    page2.insert_textbox(pymupdf.Rect(72, 310, 540, 365), sec_text, fontsize=11, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 385), "4. Hardware & Network Requirements", fontsize=12, fontname="hebo")
    hw_text = (
        "On-premises components require minimum 10 Gbps network connectivity between "
        "plant floor systems and the corporate WAN. Recommended server specifications: "
        "Dell PowerEdge R750 (2x Intel Xeon Gold 6330, 512 GB RAM, 24TB NVMe SSD RAID-10). "
        "Client workstations require Windows 10 Pro or later with 16 GB RAM minimum."
    )
    page2.insert_textbox(pymupdf.Rect(72, 400, 540, 455), hw_text, fontsize=11, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 475), "5. Implementation Timeline", fontsize=12, fontname="hebo")

    # Timeline table headers
    headers = ["Phase", "Duration", "Key Deliverables", "Milestone Date"]
    col_x = [72, 160, 260, 440]
    page2.insert_text(pymupdf.Point(col_x[0], 495), headers[0], fontsize=10, fontname="hebo")
    page2.insert_text(pymupdf.Point(col_x[1], 495), headers[1], fontsize=10, fontname="hebo")
    page2.insert_text(pymupdf.Point(col_x[2], 495), headers[2], fontsize=10, fontname="hebo")
    page2.insert_text(pymupdf.Point(col_x[3], 495), headers[3], fontsize=10, fontname="hebo")

    shape3 = page2.new_shape()
    shape3.draw_line(pymupdf.Point(72, 500), pymupdf.Point(540, 500))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()

    rows = [
        ["Phase I", "4 months", "Infrastructure, Data Migration", "Jun 30, 2025"],
        ["Phase II", "7 months", "ERP Go-Live, Supply Chain", "Jan 31, 2026"],
        ["Phase III", "7 months", "Analytics, Mobile, Training", "Aug 31, 2026"],
    ]
    row_y = 515
    for row in rows:
        page2.insert_text(pymupdf.Point(col_x[0], row_y), row[0], fontsize=10, fontname="helv")
        page2.insert_text(pymupdf.Point(col_x[1], row_y), row[1], fontsize=10, fontname="helv")
        page2.insert_text(pymupdf.Point(col_x[2], row_y), row[2], fontsize=10, fontname="helv")
        page2.insert_text(pymupdf.Point(col_x[3], row_y), row[3], fontsize=10, fontname="helv")
        row_y += 18

    page2.insert_text(pymupdf.Point(72, row_y + 15), "Page 2 of 3", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 3: Commercial Terms & Cost Breakdown ---
    page3 = doc.new_page(width=612, height=792)

    page3.insert_text(pymupdf.Point(72, 72), "Commercial Terms & Cost Breakdown", fontsize=14, fontname="hebo")

    shape4 = page3.new_shape()
    shape4.draw_line(pymupdf.Point(72, 92), pymupdf.Point(540, 92))
    shape4.finish(color=(0.2, 0.2, 0.6), width=1.5)
    shape4.commit()

    page3.insert_text(pymupdf.Point(72, 115), "Investment Summary", fontsize=12, fontname="hebo")

    cost_items = [
        ("Software Licensing (3-year)", "$486,000"),
        ("Implementation Services", "$312,500"),
        ("Infrastructure & Cloud Setup", "$148,200"),
        ("Data Migration & Integration", "$97,800"),
        ("Training & Change Management", "$64,500"),
        ("Support & Maintenance (Year 1)", "$72,000"),
        ("Contingency Reserve (10%)", "$118,100"),
    ]

    item_y = 140
    for item, cost in cost_items:
        page3.insert_text(pymupdf.Point(90, item_y), f"• {item}", fontsize=11, fontname="helv")
        page3.insert_text(pymupdf.Point(430, item_y), cost, fontsize=11, fontname="helv")
        item_y += 20

    shape5 = page3.new_shape()
    shape5.draw_line(pymupdf.Point(72, item_y + 3), pymupdf.Point(540, item_y + 3))
    shape5.finish(color=(0, 0, 0), width=1)
    shape5.commit()

    page3.insert_text(pymupdf.Point(90, item_y + 20), "Total Project Investment", fontsize=12, fontname="hebo")
    page3.insert_text(pymupdf.Point(430, item_y + 20), "$1,299,100", fontsize=12, fontname="hebo")

    page3.insert_text(pymupdf.Point(72, item_y + 55), "Payment Schedule", fontsize=12, fontname="hebo")

    payment_text = (
        "Payments are structured in six milestone-based installments aligned with project "
        "phase completions: 20% upon contract signing, 15% at Phase I kickoff, 25% at "
        "Phase I completion, 20% at Phase II go-live, 15% at Phase III completion, and "
        "5% upon final acceptance sign-off and warranty activation."
    )
    page3.insert_textbox(pymupdf.Rect(72, item_y + 70, 540, item_y + 130),
                         payment_text, fontsize=11, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, item_y + 155), "Terms & Conditions", fontsize=12, fontname="hebo")

    terms_text = (
        "This proposal is valid for 60 days from the date of issue. All pricing is in "
        "USD and exclusive of applicable taxes. Travel and accommodation expenses incurred "
        "during on-site phases will be billed at cost with advance approval. Meridian "
        "Solutions carries $5M professional liability insurance and $10M general liability "
        "coverage. Contract terms follow our standard Master Services Agreement (MSA) with "
        "California law governing jurisdiction."
    )
    page3.insert_textbox(pymupdf.Rect(72, item_y + 170, 540, item_y + 245),
                         terms_text, fontsize=11, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, item_y + 270), "Next Steps", fontsize=12, fontname="hebo")
    next_steps = [
        "1. Review and approve the technical scope described in Section 1-4.",
        "2. Execute the Master Services Agreement and Statement of Work.",
        "3. Schedule the project kickoff meeting with your steering committee.",
        "4. Meridian Solutions will mobilize the implementation team within 10 business days.",
    ]
    step_y = item_y + 285
    for step in next_steps:
        page3.insert_text(pymupdf.Point(90, step_y), step, fontsize=11, fontname="helv")
        step_y += 18

    page3.insert_text(pymupdf.Point(72, 755), "Page 3 of 3   |   Confidential — Prepared for Pinnacle Industrial Group", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f'Initial file created: {OUTPUT_PDF}')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
