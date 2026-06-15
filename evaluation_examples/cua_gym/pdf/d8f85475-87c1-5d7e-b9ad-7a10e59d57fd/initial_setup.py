"""
Initial Setup: Create ~25 PDF files across ~/Documents/ subdirectories, 4 of which are password-protected.
Task ID: pdf_cross_098
Domain: pdf

Creates:
  ~/Documents/ — directory structure with ~25 PDF files across subdirectories
  ~/scripts/   — directory (empty, agent must create check_encryption.py here)

4 of the PDFs are password-protected (encrypted).

The agent must:
1. Write ~/scripts/check_encryption.py that scans all PDFs in ~/Documents/ recursively
2. Create ~/Documents/encryption_report.csv with columns:
   filepath, encrypted (yes/no), page_count, file_size_kb
3. Sort by encrypted status (encrypted first), then by filename
4. Run the script

Opens a file manager or terminal for the GUI agent to start with.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

import pikepdf

DOCUMENTS_DIR = '/home/user/Documents'
SCRIPTS_DIR = '/home/user/scripts'

A4_W, A4_H = 595, 842


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


def create_simple_pdf(filepath, title, body_text, num_pages=1):
    """Create a simple unencrypted PDF with given content."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    doc = pymupdf.open()
    for page_num in range(num_pages):
        page = doc.new_page(width=A4_W, height=A4_H)
        page.insert_text(
            pymupdf.Point(72, 72),
            title,
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0),
        )
        page.insert_text(
            pymupdf.Point(72, 110),
            f"Page {page_num + 1} of {num_pages}",
            fontsize=10,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )
        rect = pymupdf.Rect(72, 140, 523, 770)
        page.insert_textbox(
            rect,
            body_text + f"\n\nPDF_MARKER_{os.path.basename(filepath).replace('.pdf', '')}_PAGE{page_num+1}",
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )
    doc.save(filepath)
    doc.close()


def create_encrypted_pdf(filepath, title, body_text, password, num_pages=1):
    """Create a PDF and then encrypt it with pikepdf."""
    # First create unencrypted version
    tmp_path = filepath + ".tmp_plain.pdf"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    doc = pymupdf.open()
    for page_num in range(num_pages):
        page = doc.new_page(width=A4_W, height=A4_H)
        page.insert_text(
            pymupdf.Point(72, 72),
            title,
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0),
        )
        page.insert_text(
            pymupdf.Point(72, 110),
            f"Page {page_num + 1} of {num_pages}",
            fontsize=10,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )
        rect = pymupdf.Rect(72, 140, 523, 770)
        page.insert_textbox(
            rect,
            body_text + f"\n\nENCRYPTED_PDF_MARKER_{os.path.basename(filepath).replace('.pdf', '')}_PAGE{page_num+1}",
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )
    doc.save(tmp_path)
    doc.close()

    # Encrypt with pikepdf
    pdf = pikepdf.open(tmp_path)
    pdf.save(
        filepath,
        encryption=pikepdf.Encryption(
            owner=password + "_owner",
            user=password,
            R=4,
        ),
    )
    pdf.close()
    os.remove(tmp_path)


def create_all_pdfs():
    import shutil
    # Clean slate: remove existing Documents dir and scripts dir to ensure
    # the environment is reproducible with exactly the PDFs we create.
    if os.path.isdir(DOCUMENTS_DIR):
        shutil.rmtree(DOCUMENTS_DIR)
    if os.path.isdir(SCRIPTS_DIR):
        shutil.rmtree(SCRIPTS_DIR)
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # --- Subdirectory: reports ---
    reports_dir = os.path.join(DOCUMENTS_DIR, 'reports')
    create_simple_pdf(
        os.path.join(reports_dir, 'annual_report_2023.pdf'),
        'Annual Report 2023',
        'This document summarizes the annual performance metrics for the fiscal year 2023.\n'
        'Revenue grew by 12% compared to the previous year. Operating costs were reduced by 5%.',
        num_pages=3,
    )
    create_simple_pdf(
        os.path.join(reports_dir, 'quarterly_summary_q1.pdf'),
        'Q1 Quarterly Summary',
        'First quarter results show strong growth in all product segments.\n'
        'Customer acquisition increased by 18% year-over-year.',
        num_pages=2,
    )
    create_simple_pdf(
        os.path.join(reports_dir, 'quarterly_summary_q2.pdf'),
        'Q2 Quarterly Summary',
        'Second quarter results demonstrate continued momentum.\n'
        'New product launches contributed to 22% revenue increase.',
        num_pages=2,
    )
    create_simple_pdf(
        os.path.join(reports_dir, 'market_analysis.pdf'),
        'Market Analysis Report',
        'Comprehensive analysis of current market trends and competitive landscape.\n'
        'Identified three key growth opportunities in emerging markets.',
        num_pages=4,
    )

    # --- Subdirectory: reports/confidential (2 encrypted) ---
    conf_dir = os.path.join(reports_dir, 'confidential')
    create_encrypted_pdf(
        os.path.join(conf_dir, 'financial_projections_2024.pdf'),
        'Financial Projections 2024 (CONFIDENTIAL)',
        'Confidential financial projections for fiscal year 2024.\n'
        'Internal use only. Do not distribute.',
        password='FinProj2024!',
        num_pages=5,
    )
    create_encrypted_pdf(
        os.path.join(conf_dir, 'merger_proposal.pdf'),
        'Merger Proposal (CONFIDENTIAL)',
        'Confidential merger and acquisition proposal document.\n'
        'Strictly confidential. Authorized personnel only.',
        password='MergerConf!',
        num_pages=3,
    )

    # --- Subdirectory: contracts ---
    contracts_dir = os.path.join(DOCUMENTS_DIR, 'contracts')
    create_simple_pdf(
        os.path.join(contracts_dir, 'service_agreement_2023.pdf'),
        'Service Agreement 2023',
        'This service agreement is entered into by and between the parties.\n'
        'Terms and conditions apply as outlined in Schedule A.',
        num_pages=6,
    )
    create_simple_pdf(
        os.path.join(contracts_dir, 'vendor_contract_acme.pdf'),
        'Vendor Contract - ACME Corp',
        'Vendor supply agreement with ACME Corporation.\n'
        'Effective January 2023, renewable annually.',
        num_pages=4,
    )
    create_simple_pdf(
        os.path.join(contracts_dir, 'nda_template.pdf'),
        'Non-Disclosure Agreement Template',
        'Standard NDA template for use with partners and vendors.\n'
        'Legal review required before execution.',
        num_pages=2,
    )
    create_simple_pdf(
        os.path.join(contracts_dir, 'employee_handbook.pdf'),
        'Employee Handbook',
        'Company policies, procedures, and guidelines for all employees.\n'
        'Updated for fiscal year 2023-2024.',
        num_pages=8,
    )

    # --- Subdirectory: contracts/signed (1 encrypted) ---
    signed_dir = os.path.join(contracts_dir, 'signed')
    create_encrypted_pdf(
        os.path.join(signed_dir, 'signed_partnership_agreement.pdf'),
        'Signed Partnership Agreement (PROTECTED)',
        'Executed partnership agreement with digital signatures.\n'
        'Password protected to preserve integrity of signatures.',
        password='SignedDoc2023!',
        num_pages=7,
    )
    create_simple_pdf(
        os.path.join(signed_dir, 'signed_nda_techcorp.pdf'),
        'Signed NDA - TechCorp',
        'Executed non-disclosure agreement with TechCorp Inc.\n'
        'Signed by both parties on March 15, 2023.',
        num_pages=3,
    )

    # --- Subdirectory: presentations ---
    presentations_dir = os.path.join(DOCUMENTS_DIR, 'presentations')
    create_simple_pdf(
        os.path.join(presentations_dir, 'product_launch_slides.pdf'),
        'Product Launch Presentation',
        'Slides for the Q3 product launch event.\n'
        'Audience: investors, partners, and press.',
        num_pages=12,
    )
    create_simple_pdf(
        os.path.join(presentations_dir, 'investor_deck_2023.pdf'),
        'Investor Deck 2023',
        'Annual investor presentation covering company performance and strategy.\n'
        'Prepared for the Annual General Meeting.',
        num_pages=20,
    )
    create_simple_pdf(
        os.path.join(presentations_dir, 'team_training_slides.pdf'),
        'Team Training Materials',
        'Training slides for new employee onboarding program.\n'
        'Module 1: Company Overview and Culture.',
        num_pages=15,
    )

    # --- Subdirectory: invoices ---
    invoices_dir = os.path.join(DOCUMENTS_DIR, 'invoices')
    create_simple_pdf(
        os.path.join(invoices_dir, 'invoice_2023_001.pdf'),
        'Invoice #2023-001',
        'Invoice for professional services rendered in January 2023.\n'
        'Amount due: $12,500.00. Payment terms: Net 30.',
        num_pages=1,
    )
    create_simple_pdf(
        os.path.join(invoices_dir, 'invoice_2023_002.pdf'),
        'Invoice #2023-002',
        'Invoice for consulting services rendered in February 2023.\n'
        'Amount due: $8,750.00. Payment terms: Net 30.',
        num_pages=1,
    )
    create_simple_pdf(
        os.path.join(invoices_dir, 'invoice_2023_003.pdf'),
        'Invoice #2023-003',
        'Invoice for software licensing fees for Q1 2023.\n'
        'Amount due: $45,000.00. Payment terms: Net 15.',
        num_pages=2,
    )
    create_simple_pdf(
        os.path.join(invoices_dir, 'invoice_2023_004.pdf'),
        'Invoice #2023-004',
        'Invoice for hardware procurement and installation.\n'
        'Amount due: $23,400.00. Payment terms: Net 30.',
        num_pages=1,
    )
    create_simple_pdf(
        os.path.join(invoices_dir, 'invoice_2023_005.pdf'),
        'Invoice #2023-005',
        'Invoice for marketing campaign services Q2 2023.\n'
        'Amount due: $18,200.00. Payment terms: Net 30.',
        num_pages=1,
    )

    # --- Root Documents directory (top-level PDFs) ---
    create_simple_pdf(
        os.path.join(DOCUMENTS_DIR, 'company_overview.pdf'),
        'Company Overview',
        'Executive summary of the company mission, vision, and values.\n'
        'Prepared for external distribution.',
        num_pages=2,
    )
    create_simple_pdf(
        os.path.join(DOCUMENTS_DIR, 'project_roadmap_2024.pdf'),
        'Project Roadmap 2024',
        'Strategic roadmap outlining key projects and milestones for 2024.\n'
        'Department heads should review and provide feedback.',
        num_pages=3,
    )
    create_simple_pdf(
        os.path.join(DOCUMENTS_DIR, 'meeting_minutes_jan2024.pdf'),
        'Meeting Minutes - January 2024',
        'Minutes from the board meeting held on January 10, 2024.\n'
        'Attendees: 12 board members and 3 executives.',
        num_pages=2,
    )

    # --- 4th encrypted PDF in presentations ---
    create_encrypted_pdf(
        os.path.join(presentations_dir, 'board_presentation_confidential.pdf'),
        'Board Presentation (CONFIDENTIAL)',
        'Confidential presentation for board members only.\n'
        'Contains sensitive strategic and financial information.',
        password='Board2024Conf!',
        num_pages=18,
    )

    print(f"Created PDF structure in {DOCUMENTS_DIR}")


def verify_setup():
    """Verify that PDFs were created correctly."""
    import glob

    pdf_files = glob.glob(os.path.join(DOCUMENTS_DIR, '**', '*.pdf'), recursive=True)
    total = len(pdf_files)
    encrypted_count = 0

    for pdf_path in pdf_files:
        try:
            doc = pymupdf.open(pdf_path)
            if doc.is_encrypted:
                encrypted_count += 1
            doc.close()
        except Exception:
            encrypted_count += 1  # Can't open = likely encrypted

    print(f"Verified: {total} PDF files created, {encrypted_count} encrypted")
    assert total >= 20, f"Expected >= 20 PDFs, found {total}"
    assert encrypted_count == 4, f"Expected 4 encrypted PDFs, found {encrypted_count}"
    print("Setup verification PASSED")


create_all_pdfs()
verify_setup()

# Open a terminal for the GUI agent to work in
launch_gui('bash -c "DISPLAY=:0 gnome-terminal -- bash"', delay_sec=2.0)
print("GUI_READY: launched terminal with DISPLAY=:0")
