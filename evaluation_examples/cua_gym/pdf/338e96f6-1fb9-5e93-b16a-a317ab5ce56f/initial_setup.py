"""
Initial Setup: Create batch PDF processing environment
Task ID: pdf_gf3_020
Domain: pdf

Creates:
- /home/user/incoming/ with 12 vendor PDF documents (with images and text)
- /home/user/templates/disclaimer.pdf (1-page standard disclaimer)
- /home/user/processed/ (empty directory)
- /home/user/scripts/ (empty directory - script to be created by agent)
- Opens file manager to /home/user/ for GUI readiness
"""

import os
import shlex
import subprocess
import time
import pymupdf
from PIL import Image
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_020'

INCOMING_DIR = f'{WORKDIR}/incoming'
TEMPLATES_DIR = f'{WORKDIR}/templates'
PROCESSED_DIR = f'{WORKDIR}/processed'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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


def create_sample_image(width=200, height=150, color=(70, 130, 180)):
    """Create a simple colored image with some variation for PDF embedding."""
    img = Image.new('RGB', (width, height), color)
    # Add some variation
    pixels = img.load()
    for x in range(0, width, 10):
        for y in range(0, height, 10):
            r = min(255, color[0] + (x * 3) % 60)
            g = min(255, color[1] + (y * 2) % 40)
            b = min(255, color[2] + ((x + y) * 2) % 50)
            for dx in range(min(5, width - x)):
                for dy in range(min(5, height - y)):
                    pixels[x + dx, y + dy] = (r, g, b)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.read()


def create_vendor_pdf(filepath, vendor_name, doc_type, pages, content_lines, image_color):
    """Create a realistic vendor PDF document with text and images."""
    doc = pymupdf.open()

    for page_num in range(pages):
        page = doc.new_page(width=612, height=792)  # Letter size

        # Header
        page.insert_text(
            pymupdf.Point(72, 50),
            vendor_name,
            fontsize=18,
            fontname="hebo",
            color=(0, 0, 0.5),
        )

        # Document type subtitle
        page.insert_text(
            pymupdf.Point(72, 75),
            f"{doc_type} - Page {page_num + 1} of {pages}",
            fontsize=10,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Horizontal line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 85), pymupdf.Point(540, 85))
        shape.finish(color=(0, 0, 0.5), width=1)
        shape.commit()

        # Insert an image on the first page
        if page_num == 0:
            img_data = create_sample_image(250, 180, image_color)
            img_rect = pymupdf.Rect(330, 120, 540, 280)
            page.insert_image(img_rect, stream=img_data)

        # Body content
        y_pos = 120
        for i, line in enumerate(content_lines):
            if page_num > 0:
                line = f"[Continued] {line} (section {page_num + 1})"
            if y_pos > 720:
                break
            page.insert_text(
                pymupdf.Point(72, y_pos),
                line,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
            )
            y_pos += 18

        # Footer
        page.insert_text(
            pymupdf.Point(72, 760),
            f"Confidential - {vendor_name} | Document ID: VND-2025-{hash(vendor_name) % 9000 + 1000}",
            fontsize=8,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )

    # Set metadata
    doc.set_metadata({
        "title": f"{vendor_name} - {doc_type}",
        "author": vendor_name,
        "subject": doc_type,
        "creator": "Vendor Portal",
    })

    doc.save(filepath)
    doc.close()


def create_disclaimer_pdf():
    """Create a standard 1-page disclaimer document."""
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)

    # Title
    page.insert_text(
        pymupdf.Point(200, 80),
        "STANDARD DISCLAIMER",
        fontsize=20,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    disclaimer_text = [
        "This document has been processed by the Compliance Department of Meridian",
        "Global Holdings, Inc. The information contained herein has been reviewed",
        "and verified in accordance with our standard operating procedures.",
        "",
        "TERMS AND CONDITIONS:",
        "",
        "1. All vendor documents are subject to the terms outlined in the Master",
        "   Services Agreement (MSA) dated January 15, 2024.",
        "",
        "2. The recipient acknowledges that all pricing information, technical",
        "   specifications, and proprietary data remain confidential.",
        "",
        "3. This document may not be reproduced, distributed, or disclosed to",
        "   third parties without prior written consent from Meridian Global",
        "   Holdings, Inc.",
        "",
        "4. Any discrepancies between this document and the original vendor",
        "   submission should be reported to compliance@meridian-global.com",
        "   within five (5) business days of receipt.",
        "",
        "5. Meridian Global Holdings, Inc. reserves the right to modify these",
        "   terms at any time with thirty (30) days written notice to the vendor.",
        "",
        "6. All financial transactions referenced in vendor documents are subject",
        "   to audit by internal and external auditors as required by applicable",
        "   law and regulation.",
        "",
        "",
        "Document Classification: INTERNAL USE ONLY",
        "Compliance Version: 4.2.1",
        "Last Updated: March 2025",
    ]

    y_pos = 130
    for line in disclaimer_text:
        if line.startswith("TERMS") or line.startswith("Document Classification"):
            fontname = "hebo"
            fontsize = 11
        elif line and line[0].isdigit():
            fontname = "helv"
            fontsize = 10
        else:
            fontname = "helv"
            fontsize = 10
        page.insert_text(
            pymupdf.Point(72, y_pos),
            line,
            fontsize=fontsize,
            fontname=fontname,
            color=(0, 0, 0),
        )
        y_pos += 16

    # Footer
    page.insert_text(
        pymupdf.Point(150, 750),
        "Meridian Global Holdings, Inc. - Compliance Department",
        fontsize=9,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    doc.set_metadata({
        "title": "Standard Disclaimer",
        "author": "Meridian Global Holdings Compliance",
        "subject": "Vendor Document Disclaimer",
        "creator": "Compliance Department",
    })

    disclaimer_path = f'{TEMPLATES_DIR}/disclaimer.pdf'
    doc.save(disclaimer_path)
    doc.close()
    print(f'Created disclaimer: {disclaimer_path}')


def create_initial():
    # Create directories
    for d in [INCOMING_DIR, TEMPLATES_DIR, PROCESSED_DIR, SCRIPTS_DIR]:
        os.makedirs(d, exist_ok=True)

    # Define 12 vendor documents with varied content
    vendors = [
        {
            "filename": "acme_supply_invoice_Q1.pdf",
            "vendor": "Acme Industrial Supply Co.",
            "doc_type": "Invoice - Q1 2025",
            "pages": 3,
            "color": (70, 130, 180),
            "content": [
                "Invoice Number: INV-2025-0341",
                "Date: January 15, 2025",
                "Payment Terms: Net 30",
                "",
                "Item Description                    Qty    Unit Price    Total",
                "Industrial Grade Bearings (SKU-4421)  500   $12.50    $6,250.00",
                "Hydraulic Fluid 5-Gal (HF-200)       120    $34.75    $4,170.00",
                "Stainless Steel Bolts M10 (SS-M10)   2000    $0.85    $1,700.00",
                "Conveyor Belt Section 24in (CB-24)     15   $245.00    $3,675.00",
                "Safety Valve Assembly (SVA-100)         8   $189.99    $1,519.92",
                "",
                "Subtotal: $17,314.92",
                "Tax (8.25%): $1,428.48",
                "Shipping: $450.00",
                "Total Due: $19,193.40",
            ],
        },
        {
            "filename": "nexgen_tech_proposal.pdf",
            "vendor": "NexGen Technologies Inc.",
            "doc_type": "Technical Proposal",
            "pages": 4,
            "color": (46, 139, 87),
            "content": [
                "Project: Enterprise Network Infrastructure Upgrade",
                "Proposal Reference: NXT-PROP-2025-0087",
                "Prepared for: Meridian Global Holdings",
                "",
                "Executive Summary:",
                "NexGen Technologies proposes a comprehensive network infrastructure",
                "upgrade designed to support Meridian's growing operational demands.",
                "The solution includes redundant fiber backbone, SD-WAN deployment",
                "across 14 branch offices, and next-gen firewall integration.",
                "",
                "Project Timeline: 16 weeks from contract execution",
                "Total Investment: $487,500",
                "Annual Maintenance: $52,000",
                "",
                "Key Deliverables:",
                "- Core switch replacement (Cisco Catalyst 9500 series)",
                "- SD-WAN deployment across all branch locations",
                "- Firewall migration to Palo Alto PA-5200 series",
                "- Network monitoring dashboard implementation",
            ],
        },
        {
            "filename": "greenfield_materials_cert.pdf",
            "vendor": "Greenfield Materials Corp.",
            "doc_type": "Material Certification",
            "pages": 2,
            "color": (34, 139, 34),
            "content": [
                "Certificate of Material Compliance",
                "Certificate No: GMC-CERT-2025-0192",
                "Date of Issue: February 3, 2025",
                "",
                "This certifies that the following materials meet all applicable",
                "ASTM, ISO, and industry specifications as listed below:",
                "",
                "Material: Recycled HDPE Pellets Grade A",
                "Lot Number: RP-2025-0341-A",
                "Quantity: 25,000 kg",
                "Melt Flow Index: 7.2 g/10min (ASTM D1238)",
                "Density: 0.955 g/cm3 (ASTM D792)",
                "Tensile Strength: 28.5 MPa (ASTM D638)",
                "Impact Resistance: 45 J/m (ASTM D256)",
                "",
                "Testing Laboratory: SGS North America",
                "Test Date: January 28, 2025",
            ],
        },
        {
            "filename": "horizon_logistics_contract.pdf",
            "vendor": "Horizon Logistics Partners",
            "doc_type": "Service Contract",
            "pages": 5,
            "color": (178, 34, 34),
            "content": [
                "MASTER LOGISTICS SERVICE AGREEMENT",
                "Contract ID: HLP-MSA-2025-0044",
                "Effective Date: March 1, 2025",
                "Expiration: February 28, 2026",
                "",
                "PARTIES:",
                "Provider: Horizon Logistics Partners, LLC",
                "Client: Meridian Global Holdings, Inc.",
                "",
                "SCOPE OF SERVICES:",
                "Horizon Logistics shall provide full-service warehousing,",
                "distribution, and last-mile delivery for all Meridian product",
                "lines across the continental United States.",
                "",
                "Monthly Base Fee: $78,500",
                "Per-Unit Handling: $2.35",
                "Expedited Shipping Surcharge: 15% above standard rates",
                "SLA: 99.2% on-time delivery",
            ],
        },
        {
            "filename": "pinnacle_consulting_report.pdf",
            "vendor": "Pinnacle Strategic Consulting",
            "doc_type": "Market Analysis Report",
            "pages": 3,
            "color": (128, 0, 128),
            "content": [
                "MARKET ANALYSIS: Q4 2024 - Industrial Equipment Sector",
                "Report ID: PSC-MAR-2024-Q4",
                "Prepared: January 2025",
                "",
                "Key Findings:",
                "1. Global industrial equipment market grew 6.8% YoY to $892B",
                "2. North American market share increased to 31.4%",
                "3. Automation segment outperformed with 12.3% growth",
                "4. Supply chain disruptions decreased by 23% vs Q3",
                "",
                "Recommendations:",
                "- Expand automation product line by Q2 2025",
                "- Target Southeast Asian markets for growth",
                "- Invest in AI-driven predictive maintenance solutions",
                "- Consolidate vendor relationships to reduce costs 8-12%",
                "",
                "Competitive Landscape:",
                "Top 5 competitors analyzed with SWOT matrices attached.",
            ],
        },
        {
            "filename": "sterling_pharma_msds.pdf",
            "vendor": "Sterling Pharmaceutical LLC",
            "doc_type": "Material Safety Data Sheet",
            "pages": 2,
            "color": (255, 140, 0),
            "content": [
                "MATERIAL SAFETY DATA SHEET (MSDS)",
                "Product: Industrial Cleaning Compound IPA-500",
                "SDS Number: SPC-SDS-2025-0012",
                "Revision Date: January 10, 2025",
                "",
                "SECTION 1 - IDENTIFICATION",
                "Product Name: IPA-500 Industrial Cleaning Compound",
                "Manufacturer: Sterling Pharmaceutical LLC",
                "Emergency Phone: 1-800-555-0199",
                "",
                "SECTION 2 - HAZARD IDENTIFICATION",
                "Classification: Flammable Liquid Category 2",
                "Signal Word: DANGER",
                "Hazard Statements: H225 Highly flammable liquid and vapour",
                "",
                "SECTION 3 - COMPOSITION",
                "Isopropyl Alcohol (CAS 67-63-0): 70%",
                "Purified Water: 28%",
                "Surfactant Blend: 2%",
            ],
        },
        {
            "filename": "bluewave_energy_audit.pdf",
            "vendor": "BlueWave Energy Solutions",
            "doc_type": "Energy Audit Report",
            "pages": 4,
            "color": (0, 100, 200),
            "content": [
                "COMPREHENSIVE ENERGY AUDIT REPORT",
                "Facility: Meridian Global - Building A (HQ)",
                "Audit Date: December 2024",
                "Report Number: BWE-AUD-2024-0089",
                "",
                "Current Energy Consumption:",
                "Annual Electricity: 4,850,000 kWh ($582,000)",
                "Annual Natural Gas: 180,000 therms ($198,000)",
                "Total Annual Energy Cost: $780,000",
                "",
                "Recommended Improvements:",
                "1. LED Retrofit (ROI: 2.1 years) - Save $45,000/yr",
                "2. HVAC Optimization (ROI: 3.4 years) - Save $67,000/yr",
                "3. Solar Panel Installation (ROI: 5.8 years) - Save $92,000/yr",
                "4. Building Envelope Sealing (ROI: 1.8 years) - Save $23,000/yr",
                "",
                "Total Potential Savings: $227,000/year (29% reduction)",
            ],
        },
        {
            "filename": "atlas_freight_waybill.pdf",
            "vendor": "Atlas Freight International",
            "doc_type": "Commercial Waybill",
            "pages": 1,
            "color": (139, 69, 19),
            "content": [
                "COMMERCIAL WAYBILL / BILL OF LADING",
                "Waybill Number: AFI-WB-2025-00234",
                "Date: February 18, 2025",
                "",
                "Shipper: Meridian Global Holdings",
                "Consignee: Meridian Distribution Center - East",
                "Origin: Los Angeles, CA (Port of Long Beach)",
                "Destination: Newark, NJ",
                "",
                "Cargo Description:",
                "40x Pallets - Industrial Equipment Components",
                "Total Weight: 18,500 kg",
                "Container: AFIU2345678 (40ft HC)",
                "",
                "Freight Charges: $4,850.00",
                "Insurance: $290.00",
                "Documentation Fee: $75.00",
                "Total: $5,215.00",
                "",
                "Estimated Transit: 5-7 business days",
                "Carrier: Pacific Coast Shipping Lines",
            ],
        },
        {
            "filename": "vertex_security_assessment.pdf",
            "vendor": "Vertex Cybersecurity Group",
            "doc_type": "Security Assessment",
            "pages": 3,
            "color": (220, 20, 60),
            "content": [
                "CYBERSECURITY VULNERABILITY ASSESSMENT",
                "Client: Meridian Global Holdings, Inc.",
                "Assessment Period: January 6-17, 2025",
                "Report Classification: CONFIDENTIAL",
                "",
                "Executive Summary:",
                "Vertex conducted a comprehensive security assessment covering",
                "external perimeter, internal network, and cloud infrastructure.",
                "",
                "Findings Summary:",
                "Critical Vulnerabilities: 2",
                "High Vulnerabilities: 7",
                "Medium Vulnerabilities: 15",
                "Low Vulnerabilities: 23",
                "",
                "Top Priority Remediation:",
                "1. Patch Exchange Server CVE-2024-xxxx (CRITICAL)",
                "2. Update firewall rules for DMZ segment (HIGH)",
                "3. Enable MFA for all admin accounts (HIGH)",
                "4. Rotate expired SSL certificates (HIGH)",
            ],
        },
        {
            "filename": "oakridge_compliance_review.pdf",
            "vendor": "Oakridge Regulatory Advisors",
            "doc_type": "Compliance Review",
            "pages": 2,
            "color": (85, 107, 47),
            "content": [
                "REGULATORY COMPLIANCE REVIEW",
                "Client: Meridian Global Holdings",
                "Review Period: Q4 2024",
                "Report ID: ORA-CR-2024-Q4-0031",
                "",
                "Compliance Status by Category:",
                "Environmental (EPA): COMPLIANT",
                "Workplace Safety (OSHA): COMPLIANT - 2 minor findings",
                "Financial Reporting (SEC): COMPLIANT",
                "Data Privacy (GDPR/CCPA): PARTIAL - 3 action items",
                "Export Controls (EAR): COMPLIANT",
                "",
                "Action Items Required:",
                "1. Update data retention policy by March 31, 2025",
                "2. Complete CCPA consumer request portal upgrade",
                "3. Conduct annual data mapping exercise for EU operations",
                "",
                "Next Review Scheduled: April 2025",
            ],
        },
        {
            "filename": "cascade_maintenance_schedule.pdf",
            "vendor": "Cascade Industrial Maintenance",
            "doc_type": "Preventive Maintenance Schedule",
            "pages": 2,
            "color": (100, 149, 237),
            "content": [
                "PREVENTIVE MAINTENANCE SCHEDULE - 2025",
                "Facility: Meridian Global - Manufacturing Plant B",
                "Contract: CIM-PMS-2025-0018",
                "",
                "Monthly Maintenance Tasks:",
                "- HVAC filter replacement and coil cleaning",
                "- Fire suppression system inspection",
                "- Emergency lighting and exit sign check",
                "- Compressed air system leak detection",
                "",
                "Quarterly Maintenance Tasks:",
                "- Electrical panel thermal imaging",
                "- Roof drainage system inspection",
                "- Loading dock equipment service",
                "- Generator load bank testing",
                "",
                "Annual Maintenance Tasks:",
                "- Full elevator inspection and certification",
                "- Fire alarm system recertification",
                "- Backflow preventer testing",
                "- Structural assessment of mezzanine areas",
            ],
        },
        {
            "filename": "riverstone_training_materials.pdf",
            "vendor": "Riverstone Professional Development",
            "doc_type": "Training Catalog - Spring 2025",
            "pages": 3,
            "color": (147, 112, 219),
            "content": [
                "CORPORATE TRAINING CATALOG - SPRING 2025",
                "Customized for: Meridian Global Holdings",
                "Proposal: RPD-CAT-2025-SP",
                "",
                "Available Programs:",
                "",
                "1. Leadership Excellence Workshop (2 days)",
                "   Capacity: 25 | Cost: $8,500 per session",
                "   Dates Available: March 15-16, April 22-23",
                "",
                "2. Project Management Professional (PMP) Prep (5 days)",
                "   Capacity: 20 | Cost: $12,000 per session",
                "   Dates Available: March 3-7, May 12-16",
                "",
                "3. Data Analytics for Business Leaders (3 days)",
                "   Capacity: 15 | Cost: $9,750 per session",
                "   Dates Available: April 7-9, June 2-4",
                "",
                "4. Workplace Safety Certification (1 day)",
                "   Capacity: 40 | Cost: $3,200 per session",
                "   Dates Available: Monthly - First Monday",
            ],
        },
    ]

    # Create all 12 vendor PDFs
    for v in vendors:
        filepath = f'{INCOMING_DIR}/{v["filename"]}'
        create_vendor_pdf(filepath, v["vendor"], v["doc_type"],
                         v["pages"], v["content"], v["color"])
        print(f'Created: {filepath}')

    # Create disclaimer PDF
    create_disclaimer_pdf()

    # Verify
    files = os.listdir(INCOMING_DIR)
    print(f'\nTotal files in incoming/: {len(files)}')
    print(f'processed/ is empty: {len(os.listdir(PROCESSED_DIR)) == 0}')
    print(f'scripts/ is empty: {len(os.listdir(SCRIPTS_DIR)) == 0}')
    print(f'disclaimer exists: {os.path.exists(f"{TEMPLATES_DIR}/disclaimer.pdf")}')

    # GUI-ready startup: open file manager to /home/user
    launch_gui(f'nautilus "{WORKDIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
