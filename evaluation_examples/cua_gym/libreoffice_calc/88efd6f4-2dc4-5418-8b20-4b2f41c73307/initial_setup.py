"""
Initial Setup: Create a 15-page PDF archive with realistic content for verification task.
Task ID: pdf_gf1_038
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_038'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/archive.pdf'


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
    # Install dependencies
    subprocess.run(['pip3', 'install', 'PyMuPDF', 'pikepdf'], capture_output=True)

    import pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)

    # Remove any pre-existing check file (must NOT exist for the task)
    check_file = f'{DOCS_DIR}/archive_check.txt'
    if os.path.exists(check_file):
        os.remove(check_file)

    # Create a realistic 15-page PDF simulating a merged company archive document
    doc = pymupdf.open()

    # Page dimensions
    W, H = 595, 842  # A4

    # --- Page 1: Cover Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(150, 200), "MERIDIAN TECHNOLOGIES", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(180, 260), "Document Archive", fontsize=20, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(170, 320), "Consolidated Records 2019-2024", fontsize=14, fontname="heit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(200, 400), "Classification: Internal", fontsize=11, fontname="helv", color=(0.5, 0.1, 0.1))
    page.insert_text(pymupdf.Point(200, 430), "Archive ID: MRD-2024-0738", fontsize=11, fontname="cour", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(200, 460), "Generated: March 15, 2024", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 500), pymupdf.Point(523, 500))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()

    # --- Page 2: Table of Contents ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    toc_items = [
        ("1. Executive Summary", 3),
        ("2. Q1 2024 Financial Overview", 4),
        ("3. Q2 2024 Financial Overview", 5),
        ("4. Engineering Department Report", 6),
        ("5. Marketing Campaign Results", 7),
        ("6. Human Resources Update", 8),
        ("7. Product Development Roadmap", 9),
        ("8. Customer Satisfaction Survey", 10),
        ("9. IT Infrastructure Audit", 11),
        ("10. Legal Compliance Review", 12),
        ("11. Supply Chain Analysis", 13),
        ("12. Board Meeting Minutes - Jan 2024", 14),
        ("13. Appendix: Supporting Data", 15),
    ]
    y = 120
    for title, pg in toc_items:
        page.insert_text(pymupdf.Point(90, y), title, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(460, y), f"Page {pg}", fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 24

    # --- Page 3: Executive Summary ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    summary_text = (
        "Meridian Technologies demonstrated strong performance across all business units in the "
        "first half of fiscal year 2024. Total revenue reached $47.3 million, representing a 12% "
        "year-over-year increase driven primarily by expansion in the enterprise software segment. "
        "Operating margins improved to 18.4%, up from 15.7% in the prior year period, reflecting "
        "disciplined cost management and favorable product mix shifts. Key highlights include the "
        "successful launch of the Meridian CloudSync platform, which attracted 340 enterprise "
        "customers within its first quarter. The engineering team expanded to 186 members with "
        "strategic hires in machine learning and distributed systems. Customer satisfaction scores "
        "reached an all-time high of 4.6 out of 5.0 across all product lines. Looking ahead, the "
        "company remains positioned for continued growth with a robust pipeline of $23.8 million "
        "in contracted recurring revenue."
    )
    rect = pymupdf.Rect(72, 110, 523, 500)
    page.insert_textbox(rect, summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 4: Q1 Financial ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2. Q1 2024 Financial Overview", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    fin_data = [
        ("Revenue", "$23,145,000"),
        ("Cost of Goods Sold", "$12,890,000"),
        ("Gross Profit", "$10,255,000"),
        ("Operating Expenses", "$5,870,000"),
        ("EBITDA", "$4,385,000"),
        ("Net Income", "$3,210,000"),
        ("Earnings Per Share", "$1.42"),
        ("Cash & Equivalents", "$18,650,000"),
    ]
    y = 120
    for label, value in fin_data:
        page.insert_text(pymupdf.Point(90, y), label, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(350, y), value, fontsize=11, fontname="cour", color=(0.1, 0.3, 0.1))
        y += 28

    # --- Page 5: Q2 Financial ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "3. Q2 2024 Financial Overview", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    fin_data_q2 = [
        ("Revenue", "$24,180,000"),
        ("Cost of Goods Sold", "$13,240,000"),
        ("Gross Profit", "$10,940,000"),
        ("Operating Expenses", "$5,920,000"),
        ("EBITDA", "$5,020,000"),
        ("Net Income", "$3,670,000"),
        ("Earnings Per Share", "$1.63"),
        ("Cash & Equivalents", "$21,340,000"),
    ]
    y = 120
    for label, value in fin_data_q2:
        page.insert_text(pymupdf.Point(90, y), label, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(350, y), value, fontsize=11, fontname="cour", color=(0.1, 0.3, 0.1))
        y += 28

    # --- Page 6: Engineering ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4. Engineering Department Report", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    eng_text = (
        "The engineering department expanded from 152 to 186 team members during H1 2024. "
        "Key accomplishments include: completion of the CloudSync v2.0 architecture migration, "
        "achieving 99.97% uptime SLA across all production services, reducing average deployment "
        "time from 45 minutes to 12 minutes through CI/CD pipeline improvements, and establishing "
        "a dedicated ML ops team of 8 engineers focused on predictive analytics features. Technical "
        "debt reduction efforts resulted in a 34% decrease in critical bug reports compared to H2 2023. "
        "The team shipped 47 feature releases across 3 product lines."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, eng_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 7: Marketing ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "5. Marketing Campaign Results", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    mkt_text = (
        "Marketing initiatives in H1 2024 generated 2,847 qualified leads, a 28% increase over "
        "the same period last year. The digital marketing budget of $1.2 million delivered a 4.3x "
        "return on ad spend. Key campaigns included the 'Transform Your Workflow' brand awareness "
        "series (reaching 12.4 million impressions), the CloudSync launch campaign (conversion rate "
        "of 3.8%), and the annual TechForward conference sponsorship which generated 412 direct "
        "enterprise contacts. Social media following grew by 45% across all platforms, with LinkedIn "
        "emerging as the highest-performing channel for B2B engagement."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, mkt_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 8: HR ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "6. Human Resources Update", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    hr_text = (
        "Total headcount reached 412 employees across 6 offices. Employee satisfaction survey "
        "results showed 87% overall satisfaction, with notable improvements in work-life balance "
        "(+9 points) and career development opportunities (+7 points). Voluntary turnover decreased "
        "to 8.3% from 11.2% in the prior year. Benefits enhancements included expanded parental "
        "leave (now 16 weeks), a new wellness stipend of $1,500/year, and tuition reimbursement "
        "up to $8,000 annually. Diversity hiring initiatives resulted in 43% of new hires from "
        "underrepresented groups, exceeding the 35% target."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, hr_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 9: Product Development ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "7. Product Development Roadmap", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    prod_text = (
        "The product roadmap for H2 2024 includes three major releases: CloudSync v3.0 featuring "
        "real-time collaboration tools (target: September), DataBridge Enterprise with advanced ETL "
        "capabilities (target: October), and the Meridian Analytics Dashboard v2.0 with predictive "
        "modeling features (target: November). Investment in R&D totaled $6.8 million in H1, "
        "representing 14.4% of revenue. Patent applications filed: 7 (3 approved, 4 pending). "
        "The beta testing program expanded to include 85 enterprise partners providing structured "
        "feedback on pre-release features."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, prod_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 10: Customer Satisfaction ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "8. Customer Satisfaction Survey", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    csat_text = (
        "The semi-annual customer satisfaction survey received 1,247 responses (62% response rate). "
        "Overall satisfaction: 4.6/5.0 (up from 4.3). Net Promoter Score: 67 (up from 58). "
        "Highest-rated areas: product reliability (4.8/5.0), customer support responsiveness "
        "(4.7/5.0), and onboarding experience (4.5/5.0). Areas identified for improvement: "
        "documentation quality (3.9/5.0), API developer experience (4.0/5.0), and reporting "
        "customization options (3.8/5.0). Action plans have been established for each improvement "
        "area with quarterly milestones."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, csat_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 11: IT Infrastructure ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "9. IT Infrastructure Audit", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    it_text = (
        "The annual IT infrastructure audit was completed in May 2024. Key findings: production "
        "environment uptime averaged 99.97% across all regions. Security assessment identified "
        "zero critical vulnerabilities and 3 medium-severity items (all remediated within 14 days). "
        "Cloud infrastructure costs were reduced by 22% through reserved instance optimization and "
        "right-sizing. Disaster recovery testing confirmed RTO of 4 hours and RPO of 1 hour across "
        "all tier-1 services. Network latency between primary and secondary data centers averaged "
        "12ms, within the 15ms SLA requirement."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, it_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 12: Legal Compliance ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "10. Legal Compliance Review", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    legal_text = (
        "The compliance review confirmed adherence to all applicable regulations including SOC 2 "
        "Type II certification (renewed April 2024), GDPR compliance across EU operations, CCPA "
        "compliance for California customers, and HIPAA compliance for healthcare sector clients. "
        "No regulatory actions or fines were incurred during the review period. Data processing "
        "agreements were updated with 234 vendors. Privacy impact assessments completed for all "
        "new product features prior to launch. Employee compliance training completion rate: 98.5%."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, legal_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 13: Supply Chain ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "11. Supply Chain Analysis", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    sc_text = (
        "Supply chain operations maintained strong performance with 97.2% on-time delivery rate "
        "for hardware components. Vendor diversification strategy reduced single-source dependency "
        "from 34% to 18% of critical components. Inventory optimization through demand forecasting "
        "models reduced carrying costs by $420,000 annually. New vendor qualification process was "
        "implemented, with 12 new suppliers onboarded and 4 underperforming suppliers replaced. "
        "Sustainability initiatives included 100% renewable energy procurement for logistics "
        "operations and a 15% reduction in packaging waste."
    )
    rect = pymupdf.Rect(72, 110, 523, 450)
    page.insert_textbox(rect, sc_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 14: Board Minutes ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "12. Board Meeting Minutes - January 2024", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    board_text = (
        "Board of Directors Meeting - January 18, 2024\n"
        "Attendees: C. Nakamura (Chair), R. Okonkwo, L. Petrov, A. Gutierrez, S. Ahluwalia, "
        "M. Fernandez, T. Worthington\n\n"
        "Agenda items discussed:\n"
        "1. Approval of Q4 2023 financial statements - unanimously approved\n"
        "2. FY2024 budget allocation - approved with amendment to increase R&D by $800K\n"
        "3. Strategic acquisition candidate review - tabled for February meeting\n"
        "4. CEO performance review - satisfactory with merit increase approved\n"
        "5. Cybersecurity insurance renewal - approved at $2.4M annual premium\n"
        "6. ESG reporting framework adoption - approved GRI Standards implementation\n\n"
        "Next meeting: February 22, 2024"
    )
    rect = pymupdf.Rect(72, 110, 523, 600)
    page.insert_textbox(rect, board_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 15: Appendix ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "13. Appendix: Supporting Data", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    app_text = (
        "This appendix contains supplementary data referenced throughout the archive document.\n\n"
        "A. Revenue Breakdown by Product Line:\n"
        "   - CloudSync: $18,420,000 (39%)\n"
        "   - DataBridge: $14,280,000 (30%)\n"
        "   - Analytics Dashboard: $8,745,000 (18.5%)\n"
        "   - Professional Services: $5,880,000 (12.5%)\n\n"
        "B. Geographic Revenue Distribution:\n"
        "   - North America: 62%\n"
        "   - Europe: 24%\n"
        "   - Asia-Pacific: 11%\n"
        "   - Rest of World: 3%\n\n"
        "C. Employee Distribution by Department:\n"
        "   - Engineering: 186\n"
        "   - Sales & Marketing: 94\n"
        "   - Operations: 58\n"
        "   - Customer Support: 42\n"
        "   - Administration: 32\n\n"
        "End of Archive Document"
    )
    rect = pymupdf.Rect(72, 110, 523, 750)
    page.insert_textbox(rect, app_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Set document metadata to simulate a merged archive
    doc.set_metadata({
        "title": "Meridian Technologies - Document Archive 2024",
        "author": "Meridian Technologies Inc.",
        "subject": "Consolidated Records 2019-2024",
        "keywords": "archive, financial, engineering, compliance",
        "creator": "Meridian DocMerge v3.1",
        "producer": "PDF Merger Pro 2.8",
    })

    # Add a Table of Contents (bookmarks)
    toc = [
        [1, "Cover Page", 1],
        [1, "Table of Contents", 2],
        [1, "Executive Summary", 3],
        [1, "Q1 2024 Financial Overview", 4],
        [1, "Q2 2024 Financial Overview", 5],
        [1, "Engineering Department Report", 6],
        [1, "Marketing Campaign Results", 7],
        [1, "Human Resources Update", 8],
        [1, "Product Development Roadmap", 9],
        [1, "Customer Satisfaction Survey", 10],
        [1, "IT Infrastructure Audit", 11],
        [1, "Legal Compliance Review", 12],
        [1, "Supply Chain Analysis", 13],
        [1, "Board Meeting Minutes", 14],
        [1, "Appendix: Supporting Data", 15],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 15')

    # Ensure archive_check.txt does NOT exist
    check_file = f'{DOCS_DIR}/archive_check.txt'
    if os.path.exists(check_file):
        os.remove(check_file)
        print(f'Removed pre-existing check file: {check_file}')

    # GUI-ready: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
