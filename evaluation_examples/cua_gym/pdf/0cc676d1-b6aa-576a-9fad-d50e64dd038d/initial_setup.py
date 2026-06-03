"""
Initial Setup: PDF QA Pipeline Environment
Task ID: pdf_gf3_032
Domain: pdf
Creates 20 PDFs with varying quality in /home/user/qa/incoming/,
a rules.json config, and empty passed/failed directories.
"""

import json
import os
import shlex
import subprocess
import time

import pymupdf
import pikepdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_032'

QA_DIR = f'{WORKDIR}/qa'
INCOMING = f'{QA_DIR}/incoming'
PASSED = f'{QA_DIR}/passed'
FAILED = f'{QA_DIR}/failed'
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


def create_pdf(filepath, num_pages, title=None, author=None, bookmarks=None, add_javascript=False):
    """Create a PDF with specified properties."""
    doc = pymupdf.open()

    for i in range(num_pages):
        page = doc.new_page(width=595, height=842)
        # Add content to each page
        page.insert_text(
            pymupdf.Point(72, 72),
            f"Page {i + 1}",
            fontsize=24,
            fontname="hebo",
            color=(0, 0, 0),
        )
        page.insert_text(
            pymupdf.Point(72, 110),
            f"Document: {os.path.basename(filepath)}",
            fontsize=12,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )
        # Add some body text
        rect = pymupdf.Rect(72, 150, 523, 770)
        body_text = (
            f"This is the content of page {i + 1}. "
            "The document contains structured information relevant to "
            "quality assurance testing procedures. Each section covers "
            "different aspects of the validation framework including "
            "compliance checks, metadata verification, and structural "
            "integrity assessments. The pipeline must validate each "
            "document against the configured rule set before processing."
        )
        page.insert_textbox(rect, body_text, fontsize=11, fontname="helv")

    # Set metadata
    metadata = {}
    if title:
        metadata["title"] = title
    if author:
        metadata["author"] = author
    if metadata:
        doc.set_metadata(metadata)

    # Set bookmarks/TOC
    if bookmarks:
        toc = []
        for bm in bookmarks:
            page_num = min(bm.get("page", 1), num_pages)
            toc.append([1, bm["title"], page_num])
        doc.set_toc(toc)

    doc.save(filepath)
    doc.close()

    # Add JavaScript if requested (makes PDF fail no_javascript rule)
    if add_javascript:
        pdf = pikepdf.open(filepath, allow_overwriting_input=True)
        js_code = "app.alert('This document contains JavaScript');"
        js_action = pikepdf.Dictionary(
            S=pikepdf.Name.JavaScript,
            JS=js_code,
        )
        js_name_tree = pikepdf.Dictionary(
            Names=pikepdf.Array([pikepdf.String("TestJS"), pdf.make_indirect(js_action)])
        )
        pdf.Root[pikepdf.Name.Names] = pdf.make_indirect(
            pikepdf.Dictionary(JavaScript=pdf.make_indirect(js_name_tree))
        )
        pdf.save(filepath)
        pdf.close()


def create_initial():
    # Create directory structure
    for d in [QA_DIR, INCOMING, PASSED, FAILED, SCRIPTS_DIR]:
        os.makedirs(d, exist_ok=True)

    # Create rules.json
    rules = {
        "min_pages": 3,
        "required_bookmarks": ["Chapter 1"],
        "max_size_mb": 10,
        "required_metadata": ["Title", "Author"],
        "no_javascript": True
    }
    rules_path = f'{QA_DIR}/rules.json'
    with open(rules_path, 'w') as f:
        json.dump(rules, f, indent=2)
    print(f'Rules file created: {rules_path}')

    # Define 20 PDFs with varying quality
    # Some will pass all rules, some will fail various rules
    pdf_specs = [
        # --- PASSING PDFs (meet all criteria) ---
        {
            "name": "annual_report_2024.pdf",
            "pages": 5,
            "title": "Annual Report 2024",
            "author": "Meridian Corp Finance Team",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 3}],
        },
        {
            "name": "employee_handbook_v3.pdf",
            "pages": 8,
            "title": "Employee Handbook Version 3",
            "author": "HR Department",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 4}, {"title": "Chapter 3", "page": 6}],
        },
        {
            "name": "project_charter_phoenix.pdf",
            "pages": 4,
            "title": "Project Phoenix Charter",
            "author": "Sarah Chen",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 3}],
        },
        {
            "name": "safety_guidelines_2025.pdf",
            "pages": 6,
            "title": "Workplace Safety Guidelines 2025",
            "author": "Compliance Division",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 3}, {"title": "Chapter 3", "page": 5}],
        },
        {
            "name": "vendor_agreement_template.pdf",
            "pages": 3,
            "title": "Vendor Agreement Template",
            "author": "Legal Department",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 2}],
        },
        {
            "name": "training_materials_q1.pdf",
            "pages": 7,
            "title": "Q1 Training Materials",
            "author": "Learning & Development",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 4}],
        },
        {
            "name": "data_governance_policy.pdf",
            "pages": 5,
            "title": "Data Governance Policy",
            "author": "IT Security Team",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 3}],
        },
        {
            "name": "quarterly_review_q4.pdf",
            "pages": 4,
            "title": "Q4 Quarterly Review",
            "author": "Marcus Johnson",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 3}],
        },
        {
            "name": "compliance_audit_2024.pdf",
            "pages": 6,
            "title": "Compliance Audit Report 2024",
            "author": "External Auditors LLC",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 4}],
        },
        {
            "name": "strategic_plan_2025.pdf",
            "pages": 5,
            "title": "Strategic Plan 2025-2027",
            "author": "Executive Leadership",
            "bookmarks": [{"title": "Chapter 1", "page": 1}, {"title": "Chapter 2", "page": 3}],
        },
        # --- FAILING PDFs (various rule violations) ---
        # Fail: too few pages (< 3)
        {
            "name": "quick_memo_parking.pdf",
            "pages": 1,
            "title": "Parking Memo",
            "author": "Facilities",
            "bookmarks": [{"title": "Chapter 1", "page": 1}],
        },
        {
            "name": "one_pager_summary.pdf",
            "pages": 2,
            "title": "Executive Summary",
            "author": "Strategy Team",
            "bookmarks": [{"title": "Chapter 1", "page": 1}],
        },
        # Fail: missing required bookmark "Chapter 1"
        {
            "name": "design_spec_aurora.pdf",
            "pages": 5,
            "title": "Aurora Design Specification",
            "author": "Engineering Team",
            "bookmarks": [{"title": "Introduction", "page": 1}, {"title": "Architecture", "page": 3}],
        },
        {
            "name": "meeting_notes_march.pdf",
            "pages": 4,
            "title": "March Board Meeting Notes",
            "author": "Corporate Secretary",
            "bookmarks": [],  # no bookmarks at all
        },
        # Fail: missing metadata (no Title)
        {
            "name": "draft_proposal_unsigned.pdf",
            "pages": 4,
            "title": None,
            "author": "Procurement",
            "bookmarks": [{"title": "Chapter 1", "page": 1}],
        },
        # Fail: missing metadata (no Author)
        {
            "name": "technical_bulletin_007.pdf",
            "pages": 3,
            "title": "Technical Bulletin #007",
            "author": None,
            "bookmarks": [{"title": "Chapter 1", "page": 1}],
        },
        # Fail: missing both Title and Author
        {
            "name": "unlabeled_scan_batch3.pdf",
            "pages": 5,
            "title": None,
            "author": None,
            "bookmarks": [{"title": "Chapter 1", "page": 1}],
        },
        # Fail: too few pages AND missing bookmark
        {
            "name": "cover_letter_draft.pdf",
            "pages": 1,
            "title": "Cover Letter Draft",
            "author": "Recruiting",
            "bookmarks": [{"title": "Overview", "page": 1}],
        },
        # Fail: contains JavaScript
        {
            "name": "interactive_form_legacy.pdf",
            "pages": 4,
            "title": "Legacy Interactive Form",
            "author": "IT Department",
            "bookmarks": [{"title": "Chapter 1", "page": 1}],
            "javascript": True,
        },
        # Fail: missing metadata + missing bookmark
        {
            "name": "temp_report_unreviewed.pdf",
            "pages": 3,
            "title": None,
            "author": None,
            "bookmarks": [{"title": "Section A", "page": 1}],
        },
    ]

    for spec in pdf_specs:
        filepath = f'{INCOMING}/{spec["name"]}'
        create_pdf(
            filepath,
            num_pages=spec["pages"],
            title=spec.get("title"),
            author=spec.get("author"),
            bookmarks=spec.get("bookmarks"),
            add_javascript=spec.get("javascript", False),
        )
        print(f'Created: {filepath}')

    print(f'\nAll 20 PDFs created in {INCOMING}')
    print(f'Rules: {rules_path}')
    print(f'Directories ready: {PASSED}, {FAILED}')

    # GUI-ready: open a terminal for the agent to work in
    launch_gui('bash -c "cd /home/user && exec bash"', delay_sec=0.5)
    # Open file manager to show the qa directory
    launch_gui(f'nautilus "{QA_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')


create_initial()
