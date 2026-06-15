"""
Initial Setup: Create customer_list.pdf with 4 pages of customer records containing phone numbers
Task ID: pdf_gf1_008
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
OUTPUT = f'{WORKDIR}/customer_list.pdf'


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
    os.makedirs(WORKDIR, exist_ok=True)

    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    doc = SimpleDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Title'],
        fontSize=18, textColor=HexColor("#1a3c6e"), spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontSize=10, textColor=HexColor("#555555"), spaceAfter=16,
    )
    section_style = ParagraphStyle(
        'SectionHead', parent=styles['Heading2'],
        fontSize=13, textColor=HexColor("#1a3c6e"), spaceBefore=10, spaceAfter=6,
    )
    cell_style = ParagraphStyle(
        'CellStyle', parent=styles['Normal'], fontSize=9, leading=12,
    )

    def P(text):
        return Paragraph(text, cell_style)

    # Customer data spread across 4 pages, ~5 per page = 20 phone numbers
    customers = [
        # Page 1 - West Region
        ("WR-1001", "Sarah Chen", "742 Oakwood Drive, Portland, OR 97205", "(503) 284-7193", "sarah.chen@westmail.com"),
        ("WR-1002", "Marcus Rivera", "1588 Sunset Blvd, San Francisco, CA 94122", "(415) 763-0482", "m.rivera@baylink.net"),
        ("WR-1003", "Emily Johansson", "209 Pine Ridge Court, Seattle, WA 98103", "(206) 551-3847", "ejohansson@cascademail.com"),
        ("WR-1004", "David Nakamura", "4310 Harbor View Lane, San Diego, CA 92109", "(619) 437-2918", "d.nakamura@coastnet.com"),
        ("WR-1005", "Angela Foster", "876 Redwood Circle, Eugene, OR 97401", "(541) 682-5034", "afoster@greenpine.org"),
        # Page 2 - East Region
        ("ER-2001", "Robert Kowalski", "155 Beacon Street, Boston, MA 02116", "(617) 329-8456", "rkowalski@hubmail.com"),
        ("ER-2002", "Priya Sharma", "2843 Liberty Avenue, Philadelphia, PA 19130", "(215) 764-1093", "p.sharma@libertynet.com"),
        ("ER-2003", "James O'Brien", "901 Magnolia Terrace, Charlotte, NC 28203", "(704) 518-6372", "jobrien@southmail.net"),
        ("ER-2004", "Lisa Martinelli", "417 Atlantic Way, Miami, FL 33139", "(305) 842-7519", "lmartinelli@suncoast.com"),
        ("ER-2005", "Christopher Hayes", "3620 Chestnut Hill Road, Newark, NJ 07102", "(973) 206-4831", "c.hayes@gardenstate.net"),
        # Page 3 - Central Region
        ("CR-3001", "Michelle Tanaka", "1245 Prairie Wind Drive, Chicago, IL 60614", "(312) 478-9205", "mtanaka@windymail.com"),
        ("CR-3002", "William Okafor", "5678 Lakeside Boulevard, Minneapolis, MN 55401", "(612) 935-1748", "wokafor@northlake.org"),
        ("CR-3003", "Jennifer Morales", "320 Elm Street, Dallas, TX 75201", "(214) 603-8294", "jmorales@lonestar.net"),
        ("CR-3004", "Andrew Petrov", "899 Summit Avenue, Denver, CO 80202", "(303) 741-5620", "apetrov@milehi.com"),
        ("CR-3005", "Samantha Wu", "2100 Riverbank Lane, Kansas City, MO 64108", "(816) 254-3867", "swu@heartland.com"),
        # Page 4 - South Region
        ("SR-4001", "Daniel Gutierrez", "1776 Peachtree Road NE, Atlanta, GA 30309", "(404) 873-2146", "dgutierrez@peachnet.com"),
        ("SR-4002", "Rachel Adebayo", "543 Magnolia Street, Nashville, TN 37203", "(615) 492-7583", "radebayo@musiccity.net"),
        ("SR-4003", "Thomas Becker", "2901 Canal Street, New Orleans, LA 70119", "(504) 316-8075", "tbecker@crescentmail.com"),
        ("SR-4004", "Olivia Patel", "684 Bayshore Drive, Houston, TX 77058", "(713) 540-2698", "opatel@spacecity.org"),
        ("SR-4005", "Kevin Fitzgerald", "1350 King Street, Charleston, SC 29401", "(843) 627-4910", "kfitzgerald@lowcountry.net"),
    ]

    story = []

    # Document header
    story.append(Paragraph("Meridian Solutions Inc.", title_style))
    story.append(Paragraph("Customer Directory  |  Confidential  |  Last Updated: March 2026", subtitle_style))

    regions = [
        ("West Region Accounts", customers[0:5]),
        ("East Region Accounts", customers[5:10]),
        ("Central Region Accounts", customers[10:15]),
        ("South Region Accounts", customers[15:20]),
    ]

    header_color = HexColor("#1a3c6e")
    header_text_color = HexColor("#ffffff")
    alt_row_color = HexColor("#f0f4fa")

    for idx, (region_name, region_customers) in enumerate(regions):
        if idx > 0:
            story.append(PageBreak())
            story.append(Paragraph("Meridian Solutions Inc.", title_style))
            story.append(Paragraph(
                "Customer Directory  |  Confidential  |  Last Updated: March 2026",
                subtitle_style
            ))

        story.append(Paragraph(region_name, section_style))
        story.append(Spacer(1, 4))

        table_data = [
            [P("<b>ID</b>"), P("<b>Customer Name</b>"), P("<b>Address</b>"),
             P("<b>Phone</b>"), P("<b>Email</b>")],
        ]
        for cid, name, addr, phone, email in region_customers:
            table_data.append([P(cid), P(name), P(addr), P(phone), P(email)])

        col_widths = [55, 105, 195, 95, 160]
        t = Table(table_data, colWidths=col_widths, repeatRows=1)

        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), header_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), header_text_color),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        # Alternate row colors
        for row_idx in range(1, len(table_data)):
            if row_idx % 2 == 0:
                style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), alt_row_color))

        t.setStyle(TableStyle(style_cmds))
        story.append(t)

        story.append(Spacer(1, 14))
        story.append(Paragraph(
            f"<i>Total accounts in {region_name.replace(' Accounts', '')}: "
            f"{len(region_customers)}</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9,
                           textColor=HexColor("#888888")),
        ))

    doc.build(story)
    print(f'Initial file created: {OUTPUT}')

    # Open in evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
