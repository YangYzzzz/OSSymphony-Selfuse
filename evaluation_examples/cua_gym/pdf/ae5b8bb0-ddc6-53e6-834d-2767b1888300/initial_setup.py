"""
Initial Setup: Create purchase_order.pdf (2-page purchase order document)
Task ID: pdf_cross_077
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_077'
OUTPUT = f'{WORKDIR}/purchase_order.pdf'


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
    # Ensure Documents directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import HexColor, black, grey
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    # Build the PDF using reportlab
    tmp_path = OUTPUT + '.tmp.pdf'

    doc_rl = SimpleDocTemplate(
        tmp_path,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    styles = getSampleStyleSheet()
    story = []

    # --- Page 1: Purchase Order Header + Line Items ---
    title_style = ParagraphStyle(
        'POTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=HexColor('#003366'),
        spaceAfter=14,
    )
    heading2_style = ParagraphStyle(
        'POHeading2',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#003366'),
        spaceAfter=6,
        fontName='Helvetica-Bold',
    )
    normal_style = ParagraphStyle(
        'PONormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
    )

    story.append(Paragraph("PURCHASE ORDER", title_style))
    story.append(Paragraph("Meridian Tech Solutions, Inc.", heading2_style))
    story.append(Paragraph("4821 Innovation Blvd, Suite 300, San Jose, CA 95110", normal_style))
    story.append(Paragraph("Tel: (408) 555-0192  |  Email: procurement@meridiantech.com", normal_style))
    story.append(Spacer(1, 10))

    # PO details table
    po_details = [
        ["Purchase Order #:", "PO-2025-00342", "Date:", "March 14, 2025"],
        ["Vendor:", "DataStream Components Ltd.", "Terms:", "Net 30"],
        ["Ship To:", "Meridian Tech — Receiving Dock", "Ship Via:", "FedEx Ground"],
        ["Requested By:", "Elena Vasquez", "Dept:", "Engineering"],
    ]
    po_tbl = Table(po_details, colWidths=[130, 160, 80, 140])
    po_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#EEF3FA'), HexColor('#FFFFFF')]),
        ('BOX', (0, 0), (-1, -1), 0.5, grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, grey),
    ]))
    story.append(po_tbl)
    story.append(Spacer(1, 16))

    story.append(Paragraph("ORDER DETAILS", heading2_style))

    # Line items table
    line_items = [
        ["#", "Item Description", "Part No.", "Qty", "Unit Price", "Total"],
        ["1", "Industrial Ethernet Switch 24-Port", "DS-SW-24G", "3", "$489.00", "$1,467.00"],
        ["2", "SFP+ Transceiver Module 10GBase-SR", "DS-SFP-10G", "12", "$78.50", "$942.00"],
        ["3", "Rack-Mount Cable Management Panel 1U", "DS-CMP-1U", "5", "$34.00", "$170.00"],
        ["4", "Cat6A Shielded Patch Cable 3ft (10-pack)", "DS-CAT6A-3", "8", "$62.00", "$496.00"],
        ["5", "19\" Equipment Rack 42U Open Frame", "DS-RACK-42", "2", "$875.00", "$1,750.00"],
        ["6", "KVM Switch 8-Port USB/HDMI", "DS-KVM-8H", "2", "$310.00", "$620.00"],
        ["7", "UPS 1500VA Tower APC", "DS-UPS-15T", "4", "$295.00", "$1,180.00"],
        ["8", "Fiber Optic Patch Panel 24-Port LC", "DS-FPP-24L", "3", "$145.00", "$435.00"],
    ]
    items_tbl = Table(line_items, colWidths=[22, 185, 90, 35, 70, 68])
    items_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F5F8FC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(items_tbl)
    story.append(Spacer(1, 10))

    # Totals sub-table
    totals_data = [
        ["", "Subtotal:", "$7,060.00"],
        ["", "Tax (8.75%):", "$617.75"],
        ["", "Shipping & Handling:", "$185.00"],
        ["", "TOTAL:", "$7,862.75"],
    ]
    totals_tbl = Table(totals_data, colWidths=[330, 120, 70])
    totals_tbl.setStyle(TableStyle([
        ('FONTNAME', (1, 0), (1, -2), 'Helvetica'),
        ('FONTNAME', (1, 3), (-1, 3), 'Helvetica-Bold'),
        ('FONTNAME', (2, 3), (2, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('LINEABOVE', (1, 3), (-1, 3), 1, black),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(totals_tbl)

    # Page break to page 2
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    # --- Page 2: Vendor Info, Terms & Conditions, Approval Section ---
    story.append(Paragraph("VENDOR INFORMATION", heading2_style))
    story.append(Spacer(1, 6))

    vendor_data = [
        ["Vendor Name:", "DataStream Components Ltd."],
        ["Address:", "9200 Semiconductor Way, Austin, TX 78744"],
        ["Contact:", "Michael R. Thompson"],
        ["Phone:", "(512) 555-0278"],
        ["Email:", "sales@datastreamcomp.com"],
        ["Account #:", "MRDNTECH-007"],
    ]
    vendor_tbl = Table(vendor_data, colWidths=[120, 340])
    vendor_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#EEF3FA'), HexColor('#FFFFFF')]),
        ('BOX', (0, 0), (-1, -1), 0.5, grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, grey),
    ]))
    story.append(vendor_tbl)
    story.append(Spacer(1, 16))

    story.append(Paragraph("TERMS AND CONDITIONS", heading2_style))
    terms = [
        "1. Acceptance: This purchase order constitutes a binding agreement between Meridian Tech Solutions, Inc. "
        "('Buyer') and the vendor ('Seller'). Seller's acceptance or commencement of performance constitutes "
        "acceptance of all terms herein.",
        "2. Delivery: All items must be delivered to the designated ship-to address within the agreed timeframe. "
        "Time is of the essence. Buyer reserves the right to cancel if delivery is delayed beyond 10 business days.",
        "3. Inspection & Rejection: Buyer reserves the right to inspect all goods upon delivery. Non-conforming goods "
        "will be returned at Seller's expense within 15 days of receipt.",
        "4. Invoicing: Seller shall invoice per the terms stated on this PO. Buyer is not responsible for costs not "
        "expressly authorized in writing. All invoices must reference this PO number.",
        "5. Warranty: Seller warrants that all goods are free from defects in material and workmanship for a period "
        "of twelve (12) months from delivery date.",
        "6. Confidentiality: The terms of this purchase order are confidential. Seller shall not disclose the pricing "
        "or specifications to any third party without written consent from Buyer.",
        "7. Governing Law: This PO shall be governed by the laws of the State of California.",
    ]
    for term in terms:
        story.append(Paragraph(term, normal_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 20))
    story.append(Paragraph("AUTHORIZATION", heading2_style))
    story.append(Spacer(1, 8))

    auth_data = [
        ["Requested By:", "Elena Vasquez", "Date:", "March 14, 2025"],
        ["Dept. Manager:", "Raymond Okafor", "Date:", ""],
        ["Finance Approval:", "", "Date:", ""],
        ["VP Operations:", "", "Date:", ""],
    ]
    auth_tbl = Table(auth_data, colWidths=[130, 160, 50, 140])
    auth_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.5, grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, grey),
        ('LINEBELOW', (1, 0), (1, -1), 0.5, black),
        ('LINEBELOW', (3, 0), (3, -1), 0.5, black),
    ]))
    story.append(auth_tbl)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "This purchase order is subject to the standard terms and conditions of Meridian Tech Solutions, Inc. "
        "Unauthorized modifications to this document are prohibited.",
        normal_style
    ))

    doc_rl.build(story)

    # Verify tmp file created correctly (check file size > 0)
    tmp_size = os.path.getsize(tmp_path)
    print(f'Temp PDF created, size={tmp_size} bytes')

    # Move to final location
    import shutil
    shutil.move(tmp_path, OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open purchase_order.pdf in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
