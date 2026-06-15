"""
Initial Setup: Proposal feedback PDF with 6 pages for annotation task
Task ID: pdf_basic_159
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
TASK_ID = 'pdf_basic_159'
OUTPUT_NAMED = f'{WORKDIR}/Desktop/proposal_feedback.pdf'


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


def add_text_block(page, text, x0, y0, x1, y1, fontsize=11, fontname='helv', bold=False):
    """Insert text in a rectangle; returns y-advance based on height."""
    if bold:
        fontname = 'hebo'
    rect = pymupdf.Rect(x0, y0, x1, y1)
    page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)


def build_page4(doc):
    """Build page 4: Budget Analysis — key sentence must be on this page."""
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 72), "SECTION 3: BUDGET ANALYSIS",
                      fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    y = 110
    lh = 15  # line height for 11pt text
    gap = 10  # gap between paragraphs

    # 3.1 heading
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + lh + 2), "3.1 Cost Breakdown Review",
                         fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += lh + gap

    # 3.1 paragraph 1
    para31a = ("The total proposed budget of $350,000 has been analyzed against benchmark data "
               "from comparable infrastructure modernization projects. The committee has identified "
               "several areas where the cost estimates appear misaligned with market rates.")
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + 50), para31a,
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 52

    # 3.1 CapEx line
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + lh + 2),
                         "Capital Expenditure (CapEx): $180,000",
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += lh + 2

    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + 30),
                         ("The hardware and licensing costs are reasonable. Cloud infrastructure "
                          "commitments are appropriately priced using reserved instance pricing."),
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 32

    # 3.1 OpEx line
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + lh + 2),
                         "Operational Expenditure (OpEx): $120,000/year",
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += lh + 2

    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + 40),
                         ("Ongoing operational costs are underestimated by approximately 15-20%. "
                          "Industry benchmarks suggest $140,000-$150,000 annually for a system "
                          "of this complexity."),
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 42

    # 3.2 heading
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + lh + 2), "3.2 Funding Concerns",
                         fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += lh + gap

    # KEY SENTENCE — must be on a single line, searchable
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + lh + 4),
                         "Budget allocation is insufficient for the scope of work described in the proposal.",
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += lh + 6

    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + 35),
                         ("The current allocation does not account for potential vendor cost escalations, "
                          "staff training expenses ($25,000 estimated), or contingency reserves."),
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 37

    # 3.3 heading
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + lh + 2), "3.3 Recommended Adjustments",
                         fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += lh + gap

    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + 20),
                         "The finance committee recommends the following budget adjustments:",
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 20

    bullets = [
        "- Increase contingency reserve from 5% to 12% of total project cost",
        "- Add dedicated training budget line item: $25,000",
        "- Include post-implementation support contract: $30,000/year",
        "- Revise OpEx estimates upward to reflect market rates",
    ]
    for bullet in bullets:
        page4.insert_textbox(pymupdf.Rect(82, y, 540, y + lh + 2), bullet,
                             fontsize=11, fontname="helv", color=(0, 0, 0))
        y += lh + 3

    y += gap
    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + lh + 2),
                         "Revised Total Estimate: $420,000 - $450,000",
                         fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += lh + gap

    page4.insert_textbox(pymupdf.Rect(72, y, 540, y + 40),
                         ("The proposal team must resubmit the budget section with revised figures "
                          "before the committee can provide final approval on financial aspects."),
                         fontsize=11, fontname="helv", color=(0, 0, 0))


def create_initial():
    doc = pymupdf.open()

    # ---- Page 1: Executive Summary ----
    page1 = doc.new_page(width=612, height=792)
    page1.insert_text(pymupdf.Point(72, 72), "PROPOSAL FEEDBACK REPORT",
                      fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    page1.insert_text(pymupdf.Point(72, 105), "Project: Digital Infrastructure Modernization Initiative",
                      fontsize=12, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 125), "Review Date: March 10, 2025",
                      fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(72, 145), "Reviewer: Strategic Planning Committee",
                      fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    rect1 = pymupdf.Rect(72, 175, 540, 460)
    page1.insert_textbox(rect1,
        "EXECUTIVE SUMMARY\n\n"
        "This feedback report provides a comprehensive evaluation of the submitted proposal "
        "for the Digital Infrastructure Modernization Initiative. The committee has reviewed "
        "all aspects of the proposal including technical feasibility, resource requirements, "
        "timeline projections, risk assessment, and financial planning.\n\n"
        "Overall, the proposal demonstrates strong technical merit and a clear understanding of "
        "organizational needs. However, several sections require revision before final approval "
        "can be granted. The committee has identified key areas of concern and provided specific "
        "recommendations for improvement.\n\n"
        "The proposal team is encouraged to address all feedback points and resubmit within "
        "30 days for final review.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT)

    page1.insert_text(pymupdf.Point(72, 480), "Overall Rating: CONDITIONAL APPROVAL",
                      fontsize=12, fontname="hebo", color=(0.8, 0.4, 0))
    page1.insert_text(pymupdf.Point(72, 500), "Sections Requiring Revision: 3 of 8",
                      fontsize=11, fontname="helv", color=(0, 0, 0))

    # ---- Page 2: Technical Assessment ----
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 72), "SECTION 1: TECHNICAL ASSESSMENT",
                      fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    rect2 = pymupdf.Rect(72, 110, 540, 500)
    page2.insert_textbox(rect2,
        "1.1 Infrastructure Architecture\n\n"
        "The proposed cloud-hybrid architecture is well-designed and aligns with current industry "
        "best practices. The three-tier approach (presentation, application, data) provides "
        "appropriate separation of concerns and supports scalability requirements.\n\n"
        "FEEDBACK: The committee approves the core architectural design. The proposed use of "
        "containerization (Docker/Kubernetes) for application deployment demonstrates forward-thinking "
        "and will reduce operational overhead significantly.\n\n"
        "1.2 Security Framework\n\n"
        "The security framework addresses most compliance requirements for ISO 27001 and SOC 2 Type II. "
        "The inclusion of zero-trust network architecture is commendable. However, the proposal lacks "
        "specific details regarding data encryption standards for data at rest in the legacy system "
        "migration phase.\n\n"
        "RECOMMENDATION: Provide explicit encryption specifications (AES-256 minimum) for all "
        "data migration processes. Include a data classification matrix in the appendix.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT)

    page2.insert_text(pymupdf.Point(72, 520), "Technical Score: 82/100 — APPROVED WITH MINOR REVISIONS",
                      fontsize=11, fontname="hebo", color=(0.2, 0.5, 0.2))

    # ---- Page 3: Timeline and Milestones ----
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 72), "SECTION 2: TIMELINE AND MILESTONES",
                      fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    rect3 = pymupdf.Rect(72, 110, 540, 580)
    page3.insert_textbox(rect3,
        "2.1 Project Timeline Review\n\n"
        "The proposed 18-month implementation timeline has been reviewed against similar projects "
        "completed within the organization over the past five years. The committee finds the timeline "
        "to be optimistic but achievable given adequate resource allocation.\n\n"
        "Phase 1 (Months 1-4): Infrastructure Setup — APPROVED\n"
        "The infrastructure setup phase is well-scoped and includes appropriate buffer time "
        "for procurement delays. Vendor selection criteria are clearly defined.\n\n"
        "Phase 2 (Months 5-10): Application Migration — CONDITIONAL\n"
        "The migration phase timeline assumes zero-downtime migrations for all 47 applications. "
        "This is unrealistic given the complexity of the legacy ERP system. The committee "
        "recommends scheduling a 48-hour maintenance window for ERP migration.\n\n"
        "Phase 3 (Months 11-15): Testing and Validation — APPROVED\n"
        "The testing phase includes adequate time for user acceptance testing and performance "
        "benchmarking. The inclusion of a 30-day parallel run period is appropriate.\n\n"
        "Phase 4 (Months 16-18): Cutover and Stabilization — APPROVED\n"
        "The cutover plan is comprehensive and includes rollback procedures.\n\n"
        "2.2 Risk Buffer Assessment\n\n"
        "The proposed 10% time buffer (approximately 2 months) is considered minimal. "
        "The committee recommends increasing this to 15-20% based on organizational change history.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT)

    # ---- Page 4: Budget Analysis ----
    build_page4(doc)

    # ---- Page 5: Resource Planning ----
    page5 = doc.new_page(width=612, height=792)
    page5.insert_text(pymupdf.Point(72, 72), "SECTION 4: RESOURCE PLANNING",
                      fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    rect5 = pymupdf.Rect(72, 110, 540, 580)
    page5.insert_textbox(rect5,
        "4.1 Staffing Requirements\n\n"
        "The proposal identifies the following key personnel for project execution:\n\n"
        "Project Manager: Diana Reyes (Senior PM, 12 years experience) — APPROVED\n"
        "Technical Lead: Robert Nakamura (Infrastructure Architect) — APPROVED\n"
        "Security Officer: Priya Sharma (CISSP certified) — APPROVED\n"
        "Change Manager: Thomas Okafor (Organizational Change) — APPROVED\n\n"
        "The proposed team composition is appropriate and demonstrates strong alignment "
        "between project requirements and personnel capabilities.\n\n"
        "4.2 External Vendor Requirements\n\n"
        "The proposal includes engagement with three external vendors for specialized services:\n\n"
        "Cloud Migration Partner: Shortlisted vendor selection is appropriate. "
        "Ensure MSA agreements include SLA penalties for project delays.\n\n"
        "Security Audit Firm: The proposed firm has relevant credentials. "
        "Committee recommends two audit checkpoints rather than one.\n\n"
        "Training Provider: Approved. Ensure training materials are customized "
        "for organizational workflows rather than generic product training.\n\n"
        "4.3 Knowledge Transfer Plan\n\n"
        "The knowledge transfer timeline of 60 days is adequate. "
        "Documentation requirements are clearly specified.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT)

    page5.insert_text(pymupdf.Point(72, 600), "Resource Score: 91/100 — APPROVED",
                      fontsize=11, fontname="hebo", color=(0.2, 0.5, 0.2))

    # ---- Page 6: Conclusions and Next Steps ----
    page6 = doc.new_page(width=612, height=792)
    page6.insert_text(pymupdf.Point(72, 72), "SECTION 5: CONCLUSIONS AND NEXT STEPS",
                      fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    rect6 = pymupdf.Rect(72, 110, 540, 600)
    page6.insert_textbox(rect6,
        "5.1 Summary of Findings\n\n"
        "The Digital Infrastructure Modernization Initiative proposal has been thoroughly reviewed "
        "by the Strategic Planning Committee. The proposal demonstrates strong technical planning "
        "and team capability. The primary areas requiring revision are:\n\n"
        "1. Budget: Significant revision required (see Section 3)\n"
        "2. Application Migration Timeline: ERP downtime window must be planned\n"
        "3. Security Encryption Specifications: Detailed specs required for migration phase\n\n"
        "5.2 Required Actions Before Resubmission\n\n"
        "The proposal team must complete the following actions:\n\n"
        "ACTION 1 (High Priority): Revise budget to reflect realistic cost estimates. "
        "Budget must be approved by CFO before resubmission.\n\n"
        "ACTION 2 (Medium Priority): Update application migration plan to include "
        "ERP maintenance window. Coordinate with operations team.\n\n"
        "ACTION 3 (Medium Priority): Supplement security framework with detailed "
        "encryption specifications for the data migration phase.\n\n"
        "5.3 Resubmission Deadline\n\n"
        "Revised proposal must be submitted no later than April 15, 2025. "
        "Late submissions will be deferred to the next quarterly review cycle (July 2025).\n\n"
        "5.4 Contact Information\n\n"
        "For clarification on any feedback points, contact the committee secretariat at "
        "planning-committee@organization.internal or call extension 4721.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT)

    page6.insert_text(pymupdf.Point(72, 620), "Committee Chair: Margaret Holloway",
                      fontsize=11, fontname="hebo", color=(0, 0, 0))
    page6.insert_text(pymupdf.Point(72, 640), "Date: March 10, 2025",
                      fontsize=11, fontname="helv", color=(0, 0, 0))

    # Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    doc.save(OUTPUT_NAMED)
    doc.close()
    print(f'Initial file created: {OUTPUT_NAMED}')

    # GUI-ready startup: open in Evince at page 4 (page-index is 0-based, page 4 = index 3)
    launch_gui(f'evince --page-index=3 "{OUTPUT_NAMED}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0 at page 4')


create_initial()
