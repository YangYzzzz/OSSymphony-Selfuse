"""
Initial Setup: Create PDF visual regression testing environment
Task ID: pdf_gf3_049
Domain: pdf (libreoffice_calc listed but this is a pdf/scripting task)

Creates:
- /home/user/test/golden.pdf (10 pages, reference)
- /home/user/test/candidate.pdf (10 pages, 3 pages with intentional visual differences)
- /home/user/scripts/ directory (empty, agent must create pdf_regression.py)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_049'

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


def create_pdfs():
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    # Ensure directories exist
    os.makedirs(f'{WORKDIR}/test', exist_ok=True)
    os.makedirs(f'{WORKDIR}/scripts', exist_ok=True)

    # --- Page content definitions ---
    # 10 pages of realistic content for a "release notes" document
    page_contents = [
        {
            "title": "Release Notes v3.2.0",
            "subtitle": "PDF Processing Library",
            "body": "This document contains the release notes for version 3.2.0 of the Meridian PDF Processing Library. This major update includes performance improvements, new API endpoints, and critical bug fixes identified during the Q4 2025 testing cycle.",
            "footer": "Meridian Software Inc. - Confidential",
        },
        {
            "title": "Executive Summary",
            "subtitle": "",
            "body": "Version 3.2.0 delivers a 40% improvement in rendering speed for documents exceeding 500 pages. Memory consumption has been reduced by 25% through optimized buffer management. The new batch processing API supports concurrent document handling with configurable thread pools. Security patches address three CVEs identified in the encryption module.",
            "footer": "Page 2 of 10",
        },
        {
            "title": "New Features",
            "subtitle": "Batch Processing API",
            "body": "The BatchProcessor class now supports parallel document conversion with automatic load balancing. Configuration options include max_threads (default: 4), timeout_seconds (default: 300), and retry_count (default: 2). The API integrates with existing logging frameworks through the standard observer pattern. Output formats supported: PDF/A-1b, PDF/A-2b, PDF/X-4.",
            "footer": "Page 3 of 10",
        },
        {
            "title": "Performance Benchmarks",
            "subtitle": "Rendering Engine v3.2",
            "body": "Test Environment: Ubuntu 22.04 LTS, 32GB RAM, Intel Xeon E5-2680\n\nSingle Document (100 pages):\n  v3.1.0: 4.2 seconds\n  v3.2.0: 2.5 seconds (-40%)\n\nBatch Processing (50 documents):\n  v3.1.0: 210 seconds (sequential)\n  v3.2.0: 58 seconds (8 threads)\n\nMemory Peak:\n  v3.1.0: 1.8 GB\n  v3.2.0: 1.35 GB (-25%)",
            "footer": "Page 4 of 10",
        },
        {
            "title": "API Changes",
            "subtitle": "Breaking Changes",
            "body": "1. RenderContext.initialize() now requires an explicit Configuration object.\n2. The deprecated PdfWriter.write_legacy() method has been removed.\n3. Font embedding defaults changed from subset to full for PDF/A compliance.\n4. Minimum Python version raised from 3.8 to 3.10.\n5. The encryption module now uses AES-256 by default (was AES-128).",
            "footer": "Page 5 of 10",
        },
        {
            "title": "Bug Fixes",
            "subtitle": "Critical and High Priority",
            "body": "MERID-4521: Fixed memory leak in incremental save operations affecting documents with >1000 annotations.\nMERID-4498: Resolved incorrect glyph mapping for CJK fonts when subsetting is enabled.\nMERID-4467: Fixed race condition in concurrent page rendering that caused intermittent blank output.\nMERID-4445: Corrected CropBox calculation for rotated pages with non-standard MediaBox origins.\nMERID-4430: Fixed XMP metadata corruption when saving PDF/A-2b documents with custom namespaces.",
            "footer": "Page 6 of 10",
        },
        {
            "title": "Security Updates",
            "subtitle": "CVE Patches",
            "body": "CVE-2025-3847 (High): Buffer overflow in JBIG2 decoder when processing malformed streams. Fixed by adding bounds checking in the decoding pipeline.\n\nCVE-2025-3621 (Medium): Information disclosure through uninitialized memory in font parsing. Resolved by zero-initializing all font descriptor buffers.\n\nCVE-2025-3590 (Low): Denial of service via deeply nested object references. Added configurable recursion depth limit (default: 100).",
            "footer": "Page 7 of 10",
        },
        {
            "title": "Migration Guide",
            "subtitle": "Upgrading from v3.1.x",
            "body": "Step 1: Update dependency to meridian-pdf>=3.2.0 in requirements.txt\nStep 2: Replace PdfWriter.write_legacy() calls with PdfWriter.save()\nStep 3: Create Configuration objects for all RenderContext instances\nStep 4: Review font embedding settings if targeting PDF/A\nStep 5: Test encryption workflows with AES-256 default\nStep 6: Update thread pool settings for batch processing\nStep 7: Run the compatibility checker: python -m meridian.compat_check",
            "footer": "Page 8 of 10",
        },
        {
            "title": "Known Issues",
            "subtitle": "v3.2.0 Limitations",
            "body": "1. OpenType variable fonts are not fully supported in the subsetting engine. Workaround: convert to static instances before embedding.\n2. PDF/A-3 validation may produce false positives for documents with embedded file attachments larger than 100MB.\n3. The batch processor does not yet support mixed page orientations within a single job. This will be addressed in v3.2.1.\n4. ARM64 builds on macOS may show 5-10% lower performance compared to x86_64 due to SIMD optimization gaps.",
            "footer": "Page 9 of 10",
        },
        {
            "title": "Acknowledgments",
            "subtitle": "Contributors to v3.2.0",
            "body": "Core Team: Sarah Chen (Lead), Marcus Johnson, Priya Patel, Thomas Weber\nSecurity: Elena Rodriguez, James Kim\nQA: Aisha Mohammed, David Park, Lisa Tanaka\nDocumentation: Michael Brown, Yuki Sato\n\nSpecial thanks to the 47 community contributors who submitted bug reports and feature requests through our GitHub repository. Your feedback drives the quality of each release.\n\nNext Release: v3.3.0 scheduled for Q2 2026",
            "footer": "Page 10 of 10",
        },
    ]

    # Pages that will differ in candidate (0-indexed): pages 2, 5, 8
    diff_pages = {2, 5, 8}

    # --- Create golden.pdf ---
    golden_doc = pymupdf.open()
    for i, content in enumerate(page_contents):
        page = golden_doc.new_page(width=595, height=842)  # A4

        # Title
        page.insert_text(
            pymupdf.Point(72, 60),
            content["title"],
            fontsize=22,
            fontname="hebo",
            color=(0.0, 0.2, 0.5),
        )

        # Subtitle
        if content["subtitle"]:
            page.insert_text(
                pymupdf.Point(72, 88),
                content["subtitle"],
                fontsize=14,
                fontname="heit",
                color=(0.3, 0.3, 0.3),
            )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 100), pymupdf.Point(523, 100))
        shape.finish(color=(0.0, 0.2, 0.5), width=1.5)
        shape.commit()

        # Body text
        body_rect = pymupdf.Rect(72, 120, 523, 760)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=0,  # LEFT
        )

        # Footer
        page.insert_text(
            pymupdf.Point(72, 810),
            content["footer"],
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Page border
        shape2 = page.new_shape()
        shape2.draw_rect(pymupdf.Rect(50, 30, 545, 825))
        shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape2.commit()

    golden_path = f'{WORKDIR}/test/golden.pdf'
    golden_doc.save(golden_path)
    golden_doc.close()
    print(f'Created: {golden_path}')

    # --- Create candidate.pdf (copy golden, then modify 3 pages) ---
    import shutil
    candidate_path = f'{WORKDIR}/test/candidate.pdf'
    shutil.copy(golden_path, candidate_path)

    cand_doc = pymupdf.open(candidate_path)

    # --- Page 2 (index 2): Large red banner across page ---
    page2 = cand_doc[2]
    shape_p2 = page2.new_shape()
    shape_p2.draw_rect(pymupdf.Rect(50, 100, 545, 300))
    shape_p2.finish(color=(0.8, 0.0, 0.0), fill=(1.0, 0.85, 0.85), width=3)
    shape_p2.commit()
    page2.insert_text(
        pymupdf.Point(120, 180),
        "DRAFT - REVIEW REQUIRED",
        fontsize=36,
        fontname="hebo",
        color=(0.8, 0.0, 0.0),
    )
    page2.insert_text(
        pymupdf.Point(100, 230),
        "This page is under active review by the QA team.",
        fontsize=16,
        fontname="helv",
        color=(0.5, 0.0, 0.0),
    )
    page2.insert_text(
        pymupdf.Point(100, 260),
        "Do not distribute until approval is granted.",
        fontsize=16,
        fontname="helv",
        color=(0.5, 0.0, 0.0),
    )

    # --- Page 5 (index 5): Large watermark and colored overlay ---
    page5 = cand_doc[5]
    shape_p5 = page5.new_shape()
    shape_p5.draw_rect(pymupdf.Rect(50, 150, 545, 500))
    shape_p5.finish(color=(1.0, 0.0, 0.0), fill=(1.0, 0.9, 0.9), width=3)
    shape_p5.commit()
    page5.insert_text(
        pymupdf.Point(80, 250),
        "UNDER REVIEW",
        fontsize=52,
        fontname="hebo",
        color=(0.9, 0.2, 0.2),
        rotate=0,
    )
    page5.insert_text(
        pymupdf.Point(80, 320),
        "Security team review pending for CVE patches.",
        fontsize=16,
        fontname="helv",
        color=(0.6, 0.0, 0.0),
    )
    page5.insert_text(
        pymupdf.Point(80, 360),
        "Expected completion date: 2026-04-15",
        fontsize=16,
        fontname="helv",
        color=(0.6, 0.0, 0.0),
    )
    page5.insert_text(
        pymupdf.Point(80, 400),
        "Contact: Elena Rodriguez (security@meridian.io)",
        fontsize=16,
        fontname="helv",
        color=(0.6, 0.0, 0.0),
    )

    # --- Page 8 (index 8): Large yellow highlight box with updated content ---
    page8 = cand_doc[8]
    shape_p8 = page8.new_shape()
    shape_p8.draw_rect(pymupdf.Rect(50, 130, 545, 380))
    shape_p8.finish(color=(0.8, 0.6, 0.0), fill=(1.0, 1.0, 0.7), width=3)
    shape_p8.commit()
    page8.insert_text(
        pymupdf.Point(70, 170),
        "** REVISION NOTICE **",
        fontsize=28,
        fontname="hebo",
        color=(0.6, 0.3, 0.0),
    )
    page8.insert_text(
        pymupdf.Point(70, 210),
        "Limitations list revised per QA feedback on 2026-03-28.",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.2, 0.0),
    )
    page8.insert_text(
        pymupdf.Point(70, 240),
        "Items 2 and 4 have been updated with new workarounds.",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.2, 0.0),
    )
    page8.insert_text(
        pymupdf.Point(70, 270),
        "ARM64 performance gap reduced to 3-5% in latest builds.",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.2, 0.0),
    )

    cand_doc.save(candidate_path, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    cand_doc.close()
    print(f'Created: {candidate_path} (pages 3, 6, 9 have visual differences)')

    print(f'\nEnvironment ready:')
    print(f'  {WORKDIR}/test/golden.pdf     - 10 page reference PDF')
    print(f'  {WORKDIR}/test/candidate.pdf  - 10 page candidate with 3 diff pages')
    print(f'  {WORKDIR}/scripts/            - empty (agent creates pdf_regression.py)')


create_pdfs()

# GUI-ready: open a text editor for creating the script and file manager
try:
    launch_gui(f'nautilus "{WORKDIR}/test"', delay_sec=2.0)
except Exception:
    pass
try:
    launch_gui(f'gedit "{WORKDIR}/scripts/"', delay_sec=1.0)
except Exception:
    pass
print('GUI_READY: launched file manager and editor with DISPLAY=:0')
