"""
Initial Setup: Create a 10-page invoice bundle PDF with dollar amounts on pages 1-3.
Task ID: pdf_adv_014
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
TASK_ID = 'pdf_adv_014'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/invoice_bundle.pdf'

# Page dimensions (Letter)
W, H = 612, 792


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


def add_header_footer(page, page_num, total_pages, title="Meridian Financial Group"):
    """Add consistent header/footer to each page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 60), pymupdf.Point(W - 50, 60))
    shape.finish(color=(0.2, 0.2, 0.6), width=1.5)
    shape.commit()
    page.insert_text(pymupdf.Point(50, 50), title,
                     fontsize=10, fontname="hebo", color=(0.2, 0.2, 0.6))
    # Footer
    page.insert_text(pymupdf.Point(50, H - 30),
                     f"Page {page_num} of {total_pages}",
                     fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(W - 200, H - 30),
                     "Confidential - Internal Use Only",
                     fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))


def create_page1(doc):
    """Invoice Summary - Client: Oakridge Developments"""
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 1, 10)

    y = 90
    page.insert_text(pymupdf.Point(50, y), "INVOICE SUMMARY", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    page.insert_text(pymupdf.Point(50, y), "Client: Oakridge Developments LLC", fontsize=12, fontname="hebo")
    y += 18
    page.insert_text(pymupdf.Point(50, y), "Invoice Number: INV-2025-03847", fontsize=10, fontname="helv")
    y += 15
    page.insert_text(pymupdf.Point(50, y), "Date Issued: March 15, 2025", fontsize=10, fontname="helv")
    y += 15
    page.insert_text(pymupdf.Point(50, y), "Payment Due: April 14, 2025", fontsize=10, fontname="helv")

    # Table header
    y += 30
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(50, y - 12, W - 50, y + 6))
    shape.finish(color=(0.2, 0.2, 0.6), fill=(0.2, 0.2, 0.6))
    shape.commit()
    page.insert_text(pymupdf.Point(55, y), "Description", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page.insert_text(pymupdf.Point(300, y), "Qty", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page.insert_text(pymupdf.Point(370, y), "Unit Price", fontsize=10, fontname="hebo", color=(1, 1, 1))
    page.insert_text(pymupdf.Point(480, y), "Amount", fontsize=10, fontname="hebo", color=(1, 1, 1))

    # Line items with dollar amounts
    items = [
        ("Architectural Design Services", "1", "$12,500.00", "$12,500.00"),
        ("Structural Engineering Review", "1", "$8,750.00", "$8,750.00"),
        ("Site Survey and Assessment", "2", "$3,200.00", "$6,400.00"),
        ("Environmental Compliance Report", "1", "$4,875.50", "$4,875.50"),
        ("Project Management (Phase 1)", "1", "$15,000.00", "$15,000.00"),
        ("Material Cost Estimate", "1", "$2,340.75", "$2,340.75"),
    ]

    y += 20
    for i, (desc, qty, unit, amount) in enumerate(items):
        bg = (0.95, 0.95, 1.0) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(50, y - 12, W - 50, y + 6))
        shape.finish(fill=bg)
        shape.commit()
        page.insert_text(pymupdf.Point(55, y), desc, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(310, y), qty, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(370, y), unit, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(480, y), amount, fontsize=9, fontname="helv")
        y += 20

    # Totals
    y += 15
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(370, y - 5), pymupdf.Point(W - 50, y - 5))
    shape.finish(color=(0.2, 0.2, 0.6), width=1)
    shape.commit()
    page.insert_text(pymupdf.Point(370, y + 10), "Subtotal:", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(480, y + 10), "$49,866.25", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(370, y + 25), "Tax (8.25%):", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(480, y + 25), "$4,113.97", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(370, y + 45), "TOTAL DUE:", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(480, y + 45), "$53,980.22", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.4))

    return page


def create_page2(doc):
    """Payment History and Outstanding Balances"""
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 2, 10)

    y = 90
    page.insert_text(pymupdf.Point(50, y), "PAYMENT HISTORY & OUTSTANDING BALANCES",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 25
    page.insert_text(pymupdf.Point(50, y), "Account: Oakridge Developments LLC - ACC-90274",
                     fontsize=10, fontname="helv")

    # Payment history
    y += 30
    page.insert_text(pymupdf.Point(50, y), "Recent Payments:", fontsize=12, fontname="hebo")
    y += 20
    payments = [
        ("Feb 28, 2025", "INV-2025-03621", "Wire Transfer", "$22,450.00"),
        ("Feb 14, 2025", "INV-2025-03489", "Check #4872", "$8,900.00"),
        ("Jan 31, 2025", "INV-2025-03201", "Wire Transfer", "$35,675.50"),
        ("Jan 15, 2025", "INV-2024-02998", "ACH Payment", "$14,230.00"),
    ]
    for date, inv, method, amount in payments:
        page.insert_text(pymupdf.Point(60, y), f"{date}  |  {inv}  |  {method}  |  {amount}",
                         fontsize=9, fontname="helv")
        y += 16

    # Outstanding invoices
    y += 20
    page.insert_text(pymupdf.Point(50, y), "Outstanding Invoices:", fontsize=12, fontname="hebo")
    y += 20
    outstanding = [
        ("INV-2025-03847", "Mar 15, 2025", "Apr 14, 2025", "$53,980.22", "Current"),
        ("INV-2025-03755", "Mar 01, 2025", "Mar 31, 2025", "$18,425.00", "Overdue"),
    ]
    for inv, issued, due, amount, status in outstanding:
        color = (0.7, 0.0, 0.0) if status == "Overdue" else (0, 0, 0)
        page.insert_text(pymupdf.Point(60, y),
                         f"{inv}  |  Issued: {issued}  |  Due: {due}  |  {amount}  ({status})",
                         fontsize=9, fontname="helv", color=color)
        y += 16

    # Summary
    y += 25
    page.insert_text(pymupdf.Point(50, y), "Account Summary:", fontsize=12, fontname="hebo")
    y += 20
    page.insert_text(pymupdf.Point(60, y), "Total Outstanding: $72,405.22", fontsize=10, fontname="hebo")
    y += 16
    page.insert_text(pymupdf.Point(60, y), "30-Day Average Payment: $20,313.88", fontsize=10, fontname="helv")
    y += 16
    page.insert_text(pymupdf.Point(60, y), "Credit Limit: $150,000.00", fontsize=10, fontname="helv")
    y += 16
    page.insert_text(pymupdf.Point(60, y), "Available Credit: $77,594.78", fontsize=10, fontname="helv")

    return page


def create_page3(doc):
    """Expense Breakdown by Category"""
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 3, 10)

    y = 90
    page.insert_text(pymupdf.Point(50, y), "EXPENSE BREAKDOWN - Q1 2025",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    y += 30
    categories = [
        ("Professional Services", "$45,230.00"),
        ("Materials & Supplies", "$28,915.75"),
        ("Equipment Rental", "$12,680.00"),
        ("Travel & Accommodation", "$6,455.30"),
        ("Insurance & Permits", "$9,100.00"),
        ("Miscellaneous", "$3,247.50"),
    ]

    page.insert_text(pymupdf.Point(50, y), "Category", fontsize=11, fontname="hebo")
    page.insert_text(pymupdf.Point(350, y), "Amount", fontsize=11, fontname="hebo")
    y += 5
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, y), pymupdf.Point(W - 50, y))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()
    y += 18

    for cat, amount in categories:
        page.insert_text(pymupdf.Point(60, y), cat, fontsize=10, fontname="helv")
        page.insert_text(pymupdf.Point(360, y), amount, fontsize=10, fontname="helv")
        y += 18

    y += 10
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(300, y - 5), pymupdf.Point(W - 50, y - 5))
    shape.finish(color=(0.2, 0.2, 0.6), width=1.5)
    shape.commit()
    page.insert_text(pymupdf.Point(300, y + 10), "Total Q1 Expenses:", fontsize=11, fontname="hebo")
    page.insert_text(pymupdf.Point(360, y + 25), "$105,628.55", fontsize=12, fontname="hebo", color=(0.1, 0.1, 0.4))

    # Notes section
    y += 60
    page.insert_text(pymupdf.Point(50, y), "Notes:", fontsize=11, fontname="hebo")
    y += 18
    notes = [
        "- Professional services include $12,500.00 for architectural design",
        "- Equipment rental cost increased by $1,850.00 from Q4 2024",
        "- Travel expenses reduced by $2,100.00 compared to previous quarter",
        "- Insurance premium adjustment: $500.00 credit applied",
    ]
    for note in notes:
        page.insert_text(pymupdf.Point(60, y), note, fontsize=9, fontname="helv")
        y += 15

    return page


def create_pages_4_to_10(doc):
    """Pages 4-10: Various supporting content without dollar amounts in $X,XXX.XX format on pages 4-10"""

    # Page 4: Project Timeline
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 4, 10)
    y = 90
    page.insert_text(pymupdf.Point(50, y), "PROJECT TIMELINE - OAKRIDGE PLAZA",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    milestones = [
        ("Phase 1: Design & Planning", "Jan 6 - Feb 28, 2025", "Completed"),
        ("Phase 2: Permitting", "Mar 1 - Mar 31, 2025", "In Progress"),
        ("Phase 3: Site Preparation", "Apr 1 - Apr 30, 2025", "Pending"),
        ("Phase 4: Foundation Work", "May 1 - Jun 30, 2025", "Pending"),
        ("Phase 5: Structural Build", "Jul 1 - Oct 31, 2025", "Pending"),
        ("Phase 6: Interior Finishing", "Nov 1, 2025 - Jan 31, 2026", "Pending"),
        ("Phase 7: Final Inspection", "Feb 1 - Feb 28, 2026", "Pending"),
    ]
    for milestone, dates, status in milestones:
        color = (0, 0.5, 0) if status == "Completed" else (0.8, 0.5, 0) if status == "In Progress" else (0.4, 0.4, 0.4)
        page.insert_text(pymupdf.Point(60, y), f"{milestone}", fontsize=10, fontname="hebo")
        page.insert_text(pymupdf.Point(300, y), dates, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(480, y), status, fontsize=9, fontname="hebo", color=color)
        y += 22

    # Page 5: Team Directory
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 5, 10)
    y = 90
    page.insert_text(pymupdf.Point(50, y), "PROJECT TEAM DIRECTORY",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    team = [
        ("Sarah Chen", "Lead Architect", "sarah.chen@meridianfg.com", "ext. 4201"),
        ("Marcus Johnson", "Project Manager", "m.johnson@meridianfg.com", "ext. 4105"),
        ("Elena Vasquez", "Structural Engineer", "e.vasquez@meridianfg.com", "ext. 4312"),
        ("David Kim", "Environmental Specialist", "d.kim@meridianfg.com", "ext. 4418"),
        ("Rachel Thompson", "Cost Estimator", "r.thompson@meridianfg.com", "ext. 4207"),
        ("James O'Brien", "Site Supervisor", "j.obrien@meridianfg.com", "ext. 4156"),
        ("Aisha Patel", "Quality Assurance", "a.patel@meridianfg.com", "ext. 4333"),
        ("Robert Hernandez", "Client Liaison", "r.hernandez@meridianfg.com", "ext. 4089"),
    ]
    for name, role, email, ext in team:
        page.insert_text(pymupdf.Point(60, y), name, fontsize=10, fontname="hebo")
        page.insert_text(pymupdf.Point(200, y), role, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(370, y), email, fontsize=8, fontname="helv", color=(0, 0, 0.7))
        page.insert_text(pymupdf.Point(530, y), ext, fontsize=8, fontname="helv")
        y += 20

    # Page 6: Scope of Work
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 6, 10)
    y = 90
    page.insert_text(pymupdf.Point(50, y), "SCOPE OF WORK",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 25
    paragraphs = [
        "The Oakridge Plaza project encompasses the design, permitting, and construction of a",
        "mixed-use commercial development spanning approximately 45,000 square feet. The project",
        "includes ground-level retail space, second-floor office suites, and a rooftop terrace area.",
        "",
        "Key deliverables include comprehensive architectural drawings, structural engineering",
        "specifications, environmental impact assessments, and construction management services",
        "through project completion. All work shall comply with local building codes and the",
        "approved site development plan filed with the City Planning Commission (ref: SDP-2024-1847).",
        "",
        "The contractor shall maintain weekly progress reports and participate in bi-weekly",
        "stakeholder meetings. Any change orders require written approval from both the project",
        "manager and the client representative within five business days of submission.",
    ]
    for line in paragraphs:
        if line:
            page.insert_text(pymupdf.Point(60, y), line, fontsize=10, fontname="helv")
        y += 15

    # Page 7: Risk Assessment
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 7, 10)
    y = 90
    page.insert_text(pymupdf.Point(50, y), "RISK ASSESSMENT MATRIX",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    risks = [
        ("Weather Delays", "Medium", "High", "Schedule buffer of 15 business days included"),
        ("Material Price Volatility", "High", "Medium", "Fixed-price contracts with key suppliers"),
        ("Permit Delays", "Low", "High", "Pre-application meetings completed"),
        ("Labor Shortages", "Medium", "Medium", "Relationships with 3 subcontractor pools"),
        ("Design Changes", "Medium", "High", "Change order process with 5-day approval window"),
        ("Site Conditions", "Low", "Medium", "Phase 1 geotechnical survey completed"),
    ]
    page.insert_text(pymupdf.Point(60, y), "Risk", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(220, y), "Likelihood", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(310, y), "Impact", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(380, y), "Mitigation", fontsize=10, fontname="hebo")
    y += 18
    for risk, likelihood, impact, mitigation in risks:
        page.insert_text(pymupdf.Point(60, y), risk, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(230, y), likelihood, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(320, y), impact, fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(385, y), mitigation, fontsize=8, fontname="helv")
        y += 18

    # Page 8: Quality Standards
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 8, 10)
    y = 90
    page.insert_text(pymupdf.Point(50, y), "QUALITY ASSURANCE STANDARDS",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    standards = [
        "1. All architectural drawings shall conform to AIA Document E202 standards.",
        "2. Structural calculations must be verified by a licensed PE in the state of operation.",
        "3. Materials testing shall follow ASTM International specifications.",
        "4. Concrete mix designs require laboratory approval prior to placement.",
        "5. Steel fabrication tolerances per AISC Code of Standard Practice.",
        "6. Electrical installations per NEC 2023 Edition requirements.",
        "7. Plumbing systems per IPC 2021 with local amendments.",
        "8. HVAC systems designed to ASHRAE 90.1 energy efficiency standards.",
        "9. Fire protection per NFPA 13 sprinkler system requirements.",
        "10. Accessibility compliance with ADA 2010 Standards for Accessible Design.",
    ]
    for std in standards:
        page.insert_text(pymupdf.Point(60, y), std, fontsize=10, fontname="helv")
        y += 20

    # Page 9: Communication Protocol
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 9, 10)
    y = 90
    page.insert_text(pymupdf.Point(50, y), "COMMUNICATION PROTOCOL",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    content = [
        "Primary Contact: Marcus Johnson, Project Manager",
        "Email: m.johnson@meridianfg.com | Phone: (555) 847-2910",
        "",
        "Meeting Schedule:",
        "  - Weekly team standup: Mondays at 9:00 AM (Conference Room 4B)",
        "  - Bi-weekly client review: Thursdays at 2:00 PM (via Zoom)",
        "  - Monthly executive briefing: First Friday at 10:00 AM",
        "",
        "Reporting Requirements:",
        "  - Daily construction logs submitted by 5:00 PM",
        "  - Weekly progress photos uploaded to shared drive by Friday noon",
        "  - Monthly cost reports due by the 5th of following month",
        "  - Change order requests within 48 hours of discovery",
        "",
        "Emergency Contact Chain:",
        "  1. Site Supervisor: James O'Brien - (555) 847-2915",
        "  2. Project Manager: Marcus Johnson - (555) 847-2910",
        "  3. Director of Operations: Patricia Wells - (555) 847-2900",
    ]
    for line in content:
        if line:
            page.insert_text(pymupdf.Point(60, y), line, fontsize=10, fontname="helv")
        y += 15

    # Page 10: Terms and Conditions
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 10, 10)
    y = 90
    page.insert_text(pymupdf.Point(50, y), "TERMS AND CONDITIONS",
                     fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    terms = [
        "1. PAYMENT TERMS: Net 30 days from date of invoice. Late payments subject to",
        "   a finance charge of one and one-half percent per month on the unpaid balance.",
        "",
        "2. WARRANTY: All work performed shall be warranted for a period of twelve months",
        "   from the date of substantial completion against defects in workmanship.",
        "",
        "3. INSURANCE: Contractor shall maintain comprehensive general liability insurance",
        "   with minimum coverage as specified in the master services agreement.",
        "",
        "4. INDEMNIFICATION: Each party agrees to indemnify and hold harmless the other",
        "   party from claims arising from its own negligent acts or omissions.",
        "",
        "5. DISPUTE RESOLUTION: Any disputes shall first be submitted to mediation before",
        "   proceeding to binding arbitration under the rules of the American Arbitration",
        "   Association. Venue shall be in the county where the project is located.",
        "",
        "6. TERMINATION: Either party may terminate this agreement with thirty days written",
        "   notice. Client shall pay for all work completed through the termination date.",
        "",
        "7. FORCE MAJEURE: Neither party shall be liable for delays caused by events beyond",
        "   reasonable control including natural disasters, pandemics, or government actions.",
    ]
    for line in terms:
        if line:
            page.insert_text(pymupdf.Point(60, y), line, fontsize=9, fontname="helv")
        y += 14


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    create_page1(doc)
    create_page2(doc)
    create_page3(doc)
    create_pages_4_to_10(doc)

    # Set metadata
    doc.set_metadata({
        "title": "Invoice Bundle - Oakridge Developments",
        "author": "Meridian Financial Group",
        "subject": "Q1 2025 Invoice Package",
        "creator": "Meridian Billing System",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 10')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
