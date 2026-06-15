"""
Initial Setup: Create a Writer .odt document with 8 saved versions in version history.
Task ID: writer_lec_082
Domain: libreoffice_writer
"""

import os
import subprocess
import shlex
import shutil
import time
import zipfile
import io
from lxml import etree
from datetime import datetime, timedelta

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_082'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


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


def run_cmd(cmd: str, timeout: int = 60):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip()


def create_initial():
    # Kill any existing LibreOffice instances
    run_cmd("pkill -f soffice || true")
    time.sleep(2)

    env = os.environ.copy()
    env["DISPLAY"] = ":0"

    # Step 1: Create a text file with the document content
    txt_path = f'{WORKDIR}/_temp_content.txt'
    with open(txt_path, 'w') as f:
        f.write("""Quarterly Financial Analysis Report

Prepared by: Elena Vasquez, Senior Financial Analyst
Department: Corporate Finance & Strategy
Date: March 15, 2025

1. Executive Summary

This report provides a comprehensive analysis of the company's financial performance for Q4 2024 and a forward-looking assessment for Q1 2025. Revenue grew by 12.3% year-over-year, driven primarily by expansion in the Asia-Pacific region and the successful launch of three new product lines. Operating margins improved by 2.1 percentage points to 18.7%, reflecting ongoing cost optimization initiatives.

2. Revenue Analysis

Total revenue for Q4 2024 reached $47.8 million, exceeding our internal forecast of $45.2 million by 5.8%. The breakdown by region is as follows:

North America: $19.2M (40.2%) - Up 8.1% YoY
Europe/Middle East: $12.4M (25.9%) - Up 6.7% YoY
Asia-Pacific: $11.8M (24.7%) - Up 28.4% YoY
Latin America: $4.4M (9.2%) - Up 11.2% YoY

3. Cost Structure and Margins

Cost of goods sold decreased to 52.3% of revenue from 54.8% in the prior year quarter. This improvement was primarily driven by renegotiated supplier contracts and increased manufacturing efficiency at our Shenzhen facility. SG&A expenses remained flat at $6.2 million despite the revenue growth, demonstrating effective cost discipline across the organization.

4. Cash Flow and Balance Sheet

Operating cash flow was $8.9 million for the quarter, representing a conversion rate of 94.2% of EBITDA. Capital expenditures totaled $3.1 million, primarily allocated to the new R&D center in Austin, Texas. Free cash flow of $5.8 million enabled a $2.0 million debt repayment and $1.5 million in share buybacks.

5. Outlook and Recommendations

Based on current pipeline visibility and market conditions, we project Q1 2025 revenue of $49.5-51.0 million. Key risks include potential tariff increases on imported components and currency headwinds in the Euro zone. We recommend accelerating the hedging program and increasing inventory buffers for critical supply chain components.
""")

    # Step 2: Convert to .odt using LibreOffice headless
    result = subprocess.run(
        ['libreoffice', '--headless', '--convert-to', 'odt', '--outdir', WORKDIR, txt_path],
        capture_output=True, text=True, timeout=60, env=env,
    )
    print(f"Conversion output: {result.stdout}")
    if result.stderr:
        print(f"Conversion stderr: {result.stderr}")

    temp_odt = f'{WORKDIR}/_temp_content.odt'
    if not os.path.exists(temp_odt):
        print("ERROR: Conversion to .odt failed!")
        return

    shutil.copy(temp_odt, OUTPUT)

    # Step 3: Add 8 versions to the .odt by manipulating the ZIP structure
    add_versions_to_odt(OUTPUT, num_versions=8)

    # Cleanup temp files
    os.remove(txt_path)
    if os.path.exists(temp_odt):
        os.remove(temp_odt)

    size = os.path.getsize(OUTPUT)
    print(f"Initial file created: {OUTPUT} ({size} bytes)")

    # Kill headless LO before GUI launch
    run_cmd("pkill -f 'soffice.*headless' || true")
    time.sleep(2)

    # Step 4: Open in LibreOffice Writer GUI for the agent
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


def add_versions_to_odt(odt_path, num_versions=8):
    """Add version entries into an .odt file by manipulating its ZIP structure.

    ODF version history is stored as:
    - VersionList.xml at the root of the ZIP
    - Versions/VersionN.xml files containing content snapshots
    - Entries in META-INF/manifest.xml
    """
    version_comments = [
        "Initial draft - outline and structure",
        "Added executive summary section",
        "Revenue analysis data updated with Q4 figures",
        "Cost structure section revised per CFO feedback",
        "Cash flow analysis added",
        "Outlook section draft completed",
        "Incorporated review comments from department heads",
        "Final version - ready for board presentation",
    ]

    # Version dates spanning several months (Sep 2024 - Mar 2025)
    base_date = datetime(2024, 9, 15, 9, 0, 0)
    version_dates = []
    for i in range(num_versions):
        d = base_date + timedelta(days=i * 14 + i * 3)
        version_dates.append(d)

    # Read the existing odt content
    original_data = {}
    with zipfile.ZipFile(odt_path, 'r') as zin:
        for item in zin.namelist():
            original_data[item] = zin.read(item)

    content_xml = original_data.get('content.xml', b'')

    # Build VersionList.xml
    OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    FRAMEWORK_NS = "urn:oasis:names:tc:opendocument:xmlns:framework:1.0"
    DC_NS = "http://purl.org/dc/elements/1.1/"

    nsmap = {
        'office': OFFICE_NS,
        'framework': FRAMEWORK_NS,
        'dc': DC_NS,
    }

    root = etree.Element(f'{{{OFFICE_NS}}}document-versions', nsmap=nsmap)
    root.set(f'{{{OFFICE_NS}}}version', '1.0')

    for i in range(num_versions):
        ver = etree.SubElement(root, f'{{{FRAMEWORK_NS}}}version-entry')
        ver.set(f'{{{FRAMEWORK_NS}}}title', f'Version{i+1}')
        ver.set(f'{{{FRAMEWORK_NS}}}comment', version_comments[i])
        ver.set(f'{{{FRAMEWORK_NS}}}creator', 'Elena Vasquez')
        dt = version_dates[i]
        ver.set(f'{{{DC_NS}}}date-time', dt.strftime('%Y-%m-%dT%H:%M:%S'))

    version_list_xml = (
        b'<?xml version="1.0" encoding="UTF-8"?>\n'
        + etree.tostring(root, encoding='unicode', pretty_print=True).encode('utf-8')
    )

    # Update manifest to include version entries
    MANIFEST_NS = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
    manifest_xml = original_data.get('META-INF/manifest.xml', b'')
    updated_manifest = None
    if manifest_xml:
        manifest_tree = etree.fromstring(manifest_xml)
        # Add Versions/ directory entry
        dir_entry = etree.SubElement(manifest_tree, f'{{{MANIFEST_NS}}}file-entry')
        dir_entry.set(f'{{{MANIFEST_NS}}}full-path', 'Versions/')
        dir_entry.set(f'{{{MANIFEST_NS}}}media-type', '')
        # Add each version file entry
        for i in range(num_versions):
            entry = etree.SubElement(manifest_tree, f'{{{MANIFEST_NS}}}file-entry')
            entry.set(f'{{{MANIFEST_NS}}}full-path', f'Versions/Version{i+1}.xml')
            entry.set(f'{{{MANIFEST_NS}}}media-type', 'text/xml')
        updated_manifest = (
            b'<?xml version="1.0" encoding="UTF-8"?>\n'
            + etree.tostring(manifest_tree, encoding='unicode', pretty_print=True).encode('utf-8')
        )

    # Create the new ZIP
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        # mimetype must be first and uncompressed
        if 'mimetype' in original_data:
            zout.writestr('mimetype', original_data['mimetype'], compress_type=zipfile.ZIP_STORED)

        for name, data in original_data.items():
            if name == 'mimetype':
                continue
            if name == 'META-INF/manifest.xml' and updated_manifest:
                zout.writestr(name, updated_manifest)
            else:
                zout.writestr(name, data)

        # Add VersionList.xml
        zout.writestr('VersionList.xml', version_list_xml)

        # Add version content files
        for i in range(num_versions):
            zout.writestr(f'Versions/Version{i+1}.xml', content_xml)

    with open(odt_path, 'wb') as f:
        f.write(buf.getvalue())

    print(f"Added {num_versions} versions to {odt_path}")


create_initial()
