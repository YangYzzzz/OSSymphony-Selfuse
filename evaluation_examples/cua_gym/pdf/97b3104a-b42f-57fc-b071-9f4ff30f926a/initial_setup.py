"""
Initial Setup: Create over_stamped.pdf with mixed annotation types for stamp-removal task.
Task ID: pdf_adv_195
Domain: pdf

Creates ~/Documents/over_stamped.pdf with 8 pages containing:
  - 12 Stamp annotations (distributed across pages)
  - 5 Highlight annotations
  - 3 Text (sticky note) annotations
  - 2 Link annotations

The agent must remove ONLY the Stamp annotations while preserving all others,
and save the result as ~/Documents/no_stamps.pdf.

Opens the file in Evince for the GUI agent to work with.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = "/home/user/Documents"
OUTPUT = f"{WORKDIR}/over_stamped.pdf"
PAGE_W, PAGE_H = 595, 842  # A4


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


def create_page_content(doc, page_num, title, body_paragraphs):
    """Add a page with realistic document content."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Page header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 55), pymupdf.Point(545, 55))
    shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
    shape.commit()

    # Title
    page.insert_text(
        pymupdf.Point(50, 45),
        title,
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Body text
    y = 80
    for para in body_paragraphs:
        rect = pymupdf.Rect(50, y, 545, y + 100)
        excess = page.insert_textbox(
            rect,
            para,
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )
        y += 110

    # Footer with page number
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 10, PAGE_H - 30),
        f"Page {page_num}",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    return page


# Document content for 8 pages
PAGES_CONTENT = [
    (
        "Executive Summary — Q3 Financial Review",
        [
            "This report presents the consolidated financial results for the third quarter ending "
            "September 30, 2024. Overall performance exceeded analyst expectations with revenue "
            "growth of 12.4% year-over-year, driven primarily by strong adoption in the enterprise "
            "segment and expansion into new geographic markets.",
            "Operating expenses were well-managed, rising only 6.1% against a backdrop of elevated "
            "inflation. EBITDA margin expanded by 180 basis points to 28.3%, reflecting improved "
            "operational efficiency and favorable product mix.",
            "Cash and cash equivalents stood at $847M at quarter-end, providing ample liquidity "
            "for both organic growth initiatives and potential strategic acquisitions.",
        ],
    ),
    (
        "Section 1: Revenue Analysis",
        [
            "Total net revenue for Q3 2024 reached $2.34 billion, compared to $2.08 billion in "
            "the prior year period. The Enterprise segment contributed $1.42 billion (61% of total), "
            "while SMB accounted for $0.67 billion and Consumer for $0.25 billion.",
            "Geographic breakdown reveals continued strong performance in North America ($1.56B), "
            "with accelerating growth in EMEA ($0.48B, +22% YoY) and APAC ($0.30B, +34% YoY). "
            "Latin America remains a developing opportunity with $0.10B in quarterly revenue.",
            "Recurring subscription revenue now represents 78% of total revenue, up from 71% in "
            "Q3 2023, demonstrating successful execution of the company's platform transition "
            "strategy and improved revenue predictability.",
        ],
    ),
    (
        "Section 2: Cost Structure and Margins",
        [
            "Cost of goods sold totaled $612M, representing a gross margin of 73.8%, an improvement "
            "of 140 basis points versus Q3 2023. This improvement reflects favorable product mix "
            "shift toward higher-margin software licenses and professional services.",
            "Research and development expenses were $342M (14.6% of revenue), reflecting continued "
            "investment in next-generation platform capabilities. Sales and marketing spend of "
            "$468M (20.0% of revenue) was disciplined, with customer acquisition costs declining "
            "8% on a per-unit basis.",
            "General and administrative expenses came in at $211M, inclusive of $24M in one-time "
            "restructuring charges related to the consolidation of two regional offices. Excluding "
            "these charges, G&A as a percentage of revenue improved by 60 basis points.",
        ],
    ),
    (
        "Section 3: Balance Sheet and Liquidity",
        [
            "Total assets as of September 30, 2024 were $14.7 billion, including $847M in cash "
            "and short-term investments. Accounts receivable of $1.23B reflects DSO of 48 days, "
            "consistent with historical seasonality and collection patterns.",
            "The company's $1.5B revolving credit facility remains fully undrawn, providing "
            "substantial financial flexibility. Total debt of $2.1B carries a weighted average "
            "interest rate of 4.2% and a weighted average maturity of 5.8 years.",
            "Shareholders' equity increased to $8.4B, driven by net income of $412M partially "
            "offset by $185M in share repurchases under the ongoing $500M buyback program "
            "authorized in January 2024.",
        ],
    ),
    (
        "Section 4: Operational Highlights",
        [
            "Customer count grew to 47,200 enterprise clients and 312,000 SMB clients as of "
            "quarter-end, representing net additions of 1,850 and 8,400 respectively. Annual "
            "contract value per enterprise customer reached $301K, up 7% year-over-year.",
            "Net Revenue Retention rate remained strong at 118%, as existing customers continued "
            "to expand their platform usage and add new modules. Gross retention improved to 93%, "
            "reflecting success of customer success initiatives launched in H1 2024.",
            "Product usage metrics show encouraging engagement trends, with monthly active users "
            "growing 24% YoY to 2.8M. API call volume reached 18.4B in the quarter, up 41% YoY, "
            "demonstrating deep product integration within customer workflows.",
        ],
    ),
    (
        "Section 5: Strategic Initiatives",
        [
            "The company completed the acquisition of DataSync Technologies for $340M in August "
            "2024, adding approximately 850 enterprise customers and key data integration "
            "capabilities that complement the existing analytics platform.",
            "Partnership ecosystem expansion continues with 12 new certified integration partners "
            "added in Q3, bringing the total to 387. These partnerships drove 23% of new bookings "
            "in the quarter, up from 18% in Q2 2024.",
            "The AI-powered product suite, launched in March 2024, has been adopted by 8,200 "
            "enterprise customers as of quarter-end. Early data indicates 15-20% productivity "
            "improvements reported by survey respondents, supporting premium pricing.",
        ],
    ),
    (
        "Section 6: Outlook and Guidance",
        [
            "Based on Q3 performance and current business momentum, management is raising full-year "
            "2024 guidance. Revenue is now expected in the range of $9.10B to $9.20B, compared to "
            "prior guidance of $8.95B to $9.10B. Non-GAAP operating margin guidance increases to "
            "27.5%-28.0% from the prior range of 26.5%-27.5%.",
            "For Q4 2024, revenue is expected in the range of $2.52B to $2.56B. Non-GAAP EPS is "
            "expected to be $1.52 to $1.56 per diluted share, reflecting normal Q4 seasonality "
            "and continued investment in go-to-market capacity.",
            "Free cash flow generation for full-year 2024 is now expected to be in the range of "
            "$2.1B to $2.2B, driven by strong operating performance and disciplined working capital "
            "management. Capital expenditure guidance remains unchanged at $280M.",
        ],
    ),
    (
        "Appendix: Risk Factors and Forward-Looking Statements",
        [
            "This report contains forward-looking statements within the meaning of Section 27A of "
            "the Securities Act of 1933 and Section 21E of the Securities Exchange Act of 1934. "
            "These statements involve known and unknown risks, uncertainties, and other factors "
            "that may cause actual results to differ materially from those expressed or implied.",
            "Key risk factors include: macroeconomic conditions and their impact on technology "
            "spending, competitive pressures from established and emerging vendors, cybersecurity "
            "threats and data privacy regulatory changes, integration risks associated with recent "
            "acquisitions, and geopolitical developments affecting international operations.",
            "Past performance is not indicative of future results. Investors are cautioned not to "
            "place undue reliance on these forward-looking statements. The company undertakes no "
            "obligation to update or revise any forward-looking statements except as required by "
            "applicable securities laws.",
        ],
    ),
]

# Stamp types available in PyMuPDF (stamp=N parameter):
# 0=Approved, 1=AsIs, 2=Confidential, 3=Departmental, 4=Experimental,
# 5=Expired, 6=Final, 7=ForComment, 8=ForPublicRelease, 9=NotApproved,
# 10=NotForPublicRelease, 11=Sold, 12=TopSecret, 13=Draft
STAMP_PLACEMENTS = [
    # (page_idx, rect_x0, rect_y0, rect_x1, rect_y1, stamp_type)
    (0, 350, 100, 540, 145, 2),   # Page 1: Confidential
    (0, 350, 160, 540, 205, 12),  # Page 1: TopSecret
    (1, 60, 65, 250, 110, 7),     # Page 2: ForComment
    (1, 350, 65, 540, 110, 9),    # Page 2: NotApproved
    (2, 60, 65, 250, 110, 0),     # Page 3: Approved
    (3, 350, 65, 540, 110, 6),    # Page 4: Final
    (3, 60, 750, 250, 795, 5),    # Page 4: Expired
    (4, 350, 65, 540, 110, 13),   # Page 5: Draft
    (5, 60, 65, 250, 110, 4),     # Page 6: Experimental
    (5, 350, 750, 540, 795, 1),   # Page 6: AsIs
    (6, 60, 65, 250, 110, 11),    # Page 7: Sold
    (7, 350, 65, 540, 110, 3),    # Page 8: Departmental
]

# Highlight placements: (page_idx, search_text)
# Using substrings that appear in the content
HIGHLIGHT_TEXTS = [
    (0, "12.4%"),          # Page 1: revenue growth percentage
    (1, "78% of total"),   # Page 2: recurring revenue
    (2, "73.8%"),          # Page 3: gross margin
    (3, "4.2%"),           # Page 4: interest rate
    (6, "23% of new"),     # Page 7: partnerships
]

# Text (sticky note) annotation placements: (page_idx, x, y, content)
NOTE_PLACEMENTS = [
    (0, 50, 200, "Review: confirm revenue growth figures match audited statements"),
    (3, 50, 200, "Action required: verify debt maturity schedule with treasury team"),
    (7, 50, 200, "Legal: update risk factors section before final publication"),
]

# Link placements: (page_idx, link_rect, uri)
LINK_PLACEMENTS = [
    (
        1,
        pymupdf.Rect(50, 300, 280, 315),
        "https://investor.example.com/q3-2024-revenue-detail",
    ),
    (
        4,
        pymupdf.Rect(50, 300, 300, 315),
        "https://investor.example.com/q3-2024-customer-metrics",
    ),
]


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # Create all 8 pages with content
    pages = []
    for i, (title, paras) in enumerate(PAGES_CONTENT):
        p = create_page_content(doc, i + 1, title, paras)
        pages.append(p)

    # Add 12 Stamp annotations
    for page_idx, x0, y0, x1, y1, stamp_type in STAMP_PLACEMENTS:
        page = doc[page_idx]
        stamp_rect = pymupdf.Rect(x0, y0, x1, y1)
        annot = page.add_stamp_annot(stamp_rect, stamp=stamp_type)
        annot.update()

    # Add 5 Highlight annotations
    for page_idx, search_text in HIGHLIGHT_TEXTS:
        page = doc[page_idx]
        instances = page.search_for(search_text)
        if instances:
            annot = page.add_highlight_annot(instances[0])
            annot.set_colors(stroke=(1, 1, 0))  # yellow highlight
            annot.update()
        else:
            # Fallback: highlight a region if text search fails
            fallback_rect = pymupdf.Rect(50, 75, 250, 90)
            annot = page.add_highlight_annot(fallback_rect)
            annot.set_colors(stroke=(1, 1, 0))
            annot.update()

    # Add 3 Text (sticky note) annotations
    for page_idx, x, y, content in NOTE_PLACEMENTS:
        page = doc[page_idx]
        annot = page.add_text_annot(
            pymupdf.Point(x, y),
            content,
            icon="Note",
        )
        annot.set_colors(stroke=(1, 0.8, 0))
        annot.update()

    # Add 2 Link annotations
    for page_idx, link_rect, uri in LINK_PLACEMENTS:
        page = doc[page_idx]
        page.insert_link({
            "kind": pymupdf.LINK_URI,
            "from": link_rect,
            "uri": uri,
        })
        # Add visible underlined text for the link
        page.insert_text(
            pymupdf.Point(link_rect.x0, link_rect.y1 - 2),
            "→ See detailed breakdown",
            fontsize=9,
            fontname="helv",
            color=(0, 0, 0.8),
        )

    # Verify counts before saving
    total_stamps = sum(
        sum(1 for a in doc[i].annots() if a.type[1] == "Stamp")
        for i in range(doc.page_count)
    )
    total_highlights = sum(
        sum(1 for a in doc[i].annots() if a.type[1] == "Highlight")
        for i in range(doc.page_count)
    )
    total_notes = sum(
        sum(1 for a in doc[i].annots() if a.type[1] == "Text")
        for i in range(doc.page_count)
    )
    total_links = sum(len(doc[i].get_links()) for i in range(doc.page_count))

    assert doc.page_count == 8, f"Expected 8 pages, got {doc.page_count}"
    assert total_stamps == 12, f"Expected 12 stamps, got {total_stamps}"
    assert total_highlights == 5, f"Expected 5 highlights, got {total_highlights}"
    assert total_notes == 3, f"Expected 3 notes, got {total_notes}"
    assert total_links == 2, f"Expected 2 links, got {total_links}"

    doc.save(OUTPUT)
    doc.close()

    print(f"Initial file created: {OUTPUT}")
    print(f"  Pages: 8")
    print(f"  Stamp annotations: {total_stamps}")
    print(f"  Highlight annotations: {total_highlights}")
    print(f"  Text (note) annotations: {total_notes}")
    print(f"  Links: {total_links}")

    # Launch GUI — open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_initial()
