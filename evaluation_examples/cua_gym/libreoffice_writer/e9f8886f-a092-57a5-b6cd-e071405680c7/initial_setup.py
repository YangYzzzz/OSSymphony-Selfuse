"""
Initial Setup: Create an ODT document with 3 embedded versions and today's edits.
Task ID: writer_lec_074
Domain: libreoffice_writer

Strategy:
1. Use UNO to create multiple ODT snapshots (v1, v2, v3, current)
2. Build the final ODT by embedding version snapshots as ZIP entries
3. Open the document in LibreOffice Writer GUI
"""

import os
import shlex
import subprocess
import time
import shutil
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_074'
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


def start_lo_and_connect():
    """Start LibreOffice in non-headless mode and connect via UNO bridge."""
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(3)

    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    lo_proc = subprocess.Popen(
        ['soffice', '--norestore', '--nologo',
         '--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager'],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(8)

    import uno
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext)

    ctx = None
    for i in range(15):
        try:
            ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            break
        except Exception:
            time.sleep(2)

    if ctx is None:
        raise RuntimeError("Cannot connect to LibreOffice")

    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    return lo_proc, desktop, ctx, smgr


def create_writer_doc(desktop, paragraphs, filepath):
    """Create a Writer document with given paragraphs and save as ODT."""
    import unohelper
    from com.sun.star.beans import PropertyValue

    p = PropertyValue()
    p.Name = "FilterName"
    p.Value = "writer8"

    doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
    text = doc.getText()
    cursor = text.createTextCursor()

    for style, content in paragraphs:
        cursor.setPropertyValue("ParaStyleName", style)
        text.insertString(cursor, content, False)
        text.insertControlCharacter(cursor, 0, False)  # PARAGRAPH_BREAK

    url = unohelper.systemPathToFileUrl(filepath)
    doc.storeToURL(url, (p,))
    doc.close(True)
    time.sleep(1)
    return filepath


def create_initial():
    # =====================================================
    # Document content definitions for each version state
    # =====================================================

    base_content = [
        ("Heading 1", "Quarterly Marketing Strategy Report"),
        ("Default Paragraph Style", "Prepared by: Elena Rodriguez, VP of Marketing"),
        ("Default Paragraph Style", "Date: March 15, 2025"),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Executive Summary"),
        ("Default Paragraph Style",
         "This report outlines our marketing strategy for Q2 2025, focusing on digital "
         "transformation initiatives and brand awareness campaigns. Our primary objective "
         "is to increase market penetration in the enterprise software segment by 15% "
         "while maintaining our current customer retention rate of 92%."),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Market Analysis"),
        ("Default Paragraph Style",
         "The enterprise software market continues to grow at an annual rate of 11.3%, "
         "driven primarily by cloud adoption and remote work infrastructure demands. "
         "Key competitors include Salesforce, Microsoft, and SAP, each holding significant "
         "market share in overlapping verticals."),
        ("Default Paragraph Style", ""),
        ("Default Paragraph Style",
         "Our analysis of customer feedback data from the past two quarters reveals that "
         "product integration capabilities and API documentation quality are the top two "
         "factors influencing purchase decisions among enterprise buyers."),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Campaign Strategy"),
        ("Default Paragraph Style",
         "We propose a three-pronged approach to our Q2 campaigns: content marketing "
         "through thought leadership articles, targeted LinkedIn advertising for "
         "decision-makers, and a series of webinars showcasing our integration capabilities."),
        ("Default Paragraph Style", ""),
        ("Default Paragraph Style",
         "The allocated budget for these initiatives is $425,000, distributed across "
         "digital advertising ($180,000), content production ($120,000), and event "
         "management ($125,000)."),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Timeline and Milestones"),
        ("Default Paragraph Style",
         "Phase 1 (April 1-30): Launch content marketing campaign and begin LinkedIn "
         "ad targeting. Expected reach: 50,000 impressions."),
        ("Default Paragraph Style",
         "Phase 2 (May 1-31): Execute webinar series with guest speakers from partner "
         "companies. Target attendance: 500 registrations per webinar."),
        ("Default Paragraph Style",
         "Phase 3 (June 1-30): Analyze results, optimize underperforming channels, "
         "and prepare Q3 strategy recommendations."),
    ]

    # Version 2 adds budget allocation details
    v2_addition = [
        ("Heading 2", "Budget Allocation Details"),
        ("Default Paragraph Style",
         "The digital advertising budget of $180,000 will be split between LinkedIn Ads "
         "(60%), Google Ads (25%), and industry-specific platforms (15%). Content production "
         "costs include freelance writer fees, graphic design, and video production for "
         "the webinar series."),
        ("Default Paragraph Style", ""),
    ]

    # Version 3 adds risk assessment
    v3_addition = [
        ("Heading 2", "Risk Assessment"),
        ("Default Paragraph Style",
         "Primary risks include competitor response to our campaigns, potential budget "
         "overruns in content production, and lower-than-expected webinar attendance rates. "
         "Mitigation strategies are outlined below for each identified risk."),
        ("Default Paragraph Style", ""),
    ]

    # Current state has modified paragraphs (today's edits)
    current_content = [
        ("Heading 1", "Quarterly Marketing Strategy Report"),
        ("Default Paragraph Style", "Prepared by: Elena Rodriguez, VP of Marketing"),
        ("Default Paragraph Style", "Date: March 15, 2025"),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Executive Summary"),
        # MODIFIED: 15% -> 20%, 92% -> 94%, added partnerships
        ("Default Paragraph Style",
         "This report outlines our marketing strategy for Q2 2025, focusing on digital "
         "transformation initiatives, brand awareness campaigns, and strategic partnerships "
         "with industry leaders. Our primary objective is to increase market penetration in "
         "the enterprise software segment by 20% while maintaining our current customer "
         "retention rate of 94%."),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Market Analysis"),
        ("Default Paragraph Style",
         "The enterprise software market continues to grow at an annual rate of 11.3%, "
         "driven primarily by cloud adoption and remote work infrastructure demands. "
         "Key competitors include Salesforce, Microsoft, and SAP, each holding significant "
         "market share in overlapping verticals."),
        ("Default Paragraph Style", ""),
        ("Default Paragraph Style",
         "Our analysis of customer feedback data from the past two quarters reveals that "
         "product integration capabilities and API documentation quality are the top two "
         "factors influencing purchase decisions among enterprise buyers."),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Campaign Strategy"),
        # MODIFIED: three->four pronged, added Twitter + referral
        ("Default Paragraph Style",
         "We propose a four-pronged approach to our Q2 campaigns: content marketing "
         "through thought leadership articles, targeted LinkedIn and Twitter advertising "
         "for decision-makers, a series of webinars showcasing our integration capabilities, "
         "and a new partner referral program launching in mid-April."),
        ("Default Paragraph Style", ""),
        # MODIFIED: $425k->$510k, restructured
        ("Default Paragraph Style",
         "The revised budget for these initiatives is $510,000, distributed across "
         "digital advertising ($200,000), content production ($140,000), event management "
         "($120,000), and partner program ($50,000)."),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Timeline and Milestones"),
        ("Default Paragraph Style",
         "Phase 1 (April 1-30): Launch content marketing campaign and begin LinkedIn "
         "ad targeting. Expected reach: 50,000 impressions."),
        ("Default Paragraph Style",
         "Phase 2 (May 1-31): Execute webinar series with guest speakers from partner "
         "companies. Target attendance: 500 registrations per webinar."),
        ("Default Paragraph Style",
         "Phase 3 (June 1-30): Analyze results, optimize underperforming channels, "
         "and prepare Q3 strategy recommendations."),
        ("Heading 2", "Budget Allocation Details"),
        ("Default Paragraph Style",
         "The digital advertising budget of $180,000 will be split between LinkedIn Ads "
         "(60%), Google Ads (25%), and industry-specific platforms (15%). Content production "
         "costs include freelance writer fees, graphic design, and video production for "
         "the webinar series."),
        ("Default Paragraph Style", ""),
        ("Heading 2", "Risk Assessment"),
        ("Default Paragraph Style",
         "Primary risks include competitor response to our campaigns, potential budget "
         "overruns in content production, and lower-than-expected webinar attendance rates. "
         "Mitigation strategies are outlined below for each identified risk."),
        ("Default Paragraph Style", ""),
    ]

    # =====================================================
    # Step 1: Start LO and create all version snapshots
    # =====================================================
    lo_proc, desktop, ctx, smgr = start_lo_and_connect()

    v1_content = list(base_content)
    v2_content = list(base_content) + list(v2_addition)
    v3_content = list(base_content) + list(v2_addition) + list(v3_addition)

    print("Creating version snapshots...")
    create_writer_doc(desktop, v1_content, "/tmp/v1.odt")
    print("  Version 1 snapshot saved")
    create_writer_doc(desktop, v2_content, "/tmp/v2.odt")
    print("  Version 2 snapshot saved")
    create_writer_doc(desktop, v3_content, "/tmp/v3.odt")
    print("  Version 3 snapshot saved")
    create_writer_doc(desktop, current_content, "/tmp/current.odt")
    print("  Current state saved")

    # Close LO
    try:
        desktop.terminate()
    except Exception:
        pass
    time.sleep(2)
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(3)

    # =====================================================
    # Step 2: Build final ODT with embedded versions
    # =====================================================
    print("\nBuilding final ODT with embedded versions...")

    # Read version snapshots
    with open("/tmp/v1.odt", "rb") as f:
        v1_bytes = f.read()
    with open("/tmp/v2.odt", "rb") as f:
        v2_bytes = f.read()
    with open("/tmp/v3.odt", "rb") as f:
        v3_bytes = f.read()

    # VersionList.xml
    version_list_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<VL:version-list xmlns:VL="http://openoffice.org/2001/versions-list" xmlns:dc="http://purl.org/dc/elements/1.1/">
 <VL:version-entry VL:title="Version1" VL:comment="Initial draft - March 10" VL:creator="Elena Rodriguez" dc:date-time="2025-03-10T09:30:00">
 </VL:version-entry>
 <VL:version-entry VL:title="Version2" VL:comment="Added budget details - March 12" VL:creator="Elena Rodriguez" dc:date-time="2025-03-12T14:15:00">
 </VL:version-entry>
 <VL:version-entry VL:title="Version3" VL:comment="Pre-editing session snapshot - March 15 morning" VL:creator="Elena Rodriguez" dc:date-time="2025-03-15T08:00:00">
 </VL:version-entry>
</VL:version-list>'''

    # Start with current.odt, add version entries
    shutil.copy("/tmp/current.odt", OUTPUT)

    # Read existing manifest.xml
    with zipfile.ZipFile(OUTPUT, 'r') as zin:
        manifest = zin.read("META-INF/manifest.xml").decode("utf-8")

    # Add version entries to manifest
    version_manifest_entries = '''
 <manifest:file-entry manifest:media-type="" manifest:full-path="Versions/VersionList.xml"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Versions/Version1"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Versions/Version2"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Versions/Version3"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Versions/"/>'''
    manifest_updated = manifest.replace(
        "</manifest:manifest>",
        version_manifest_entries + "\n</manifest:manifest>"
    )

    # Rebuild ZIP with versions
    temp_path = "/tmp/final_with_versions.odt"
    with zipfile.ZipFile(OUTPUT, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w') as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "mimetype":
                    # mimetype MUST be first entry and stored uncompressed
                    zout.writestr(item, data, compress_type=zipfile.ZIP_STORED)
                elif item.filename == "META-INF/manifest.xml":
                    zout.writestr(item, manifest_updated.encode("utf-8"),
                                  compress_type=zipfile.ZIP_DEFLATED)
                else:
                    zout.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED)

            # Add version entries
            zout.writestr("Versions/VersionList.xml", version_list_xml,
                          compress_type=zipfile.ZIP_DEFLATED)
            zout.writestr("Versions/Version1", v1_bytes,
                          compress_type=zipfile.ZIP_DEFLATED)
            zout.writestr("Versions/Version2", v2_bytes,
                          compress_type=zipfile.ZIP_DEFLATED)
            zout.writestr("Versions/Version3", v3_bytes,
                          compress_type=zipfile.ZIP_DEFLATED)

    shutil.move(temp_path, OUTPUT)

    # Clean up temp files
    for f in ["/tmp/v1.odt", "/tmp/v2.odt", "/tmp/v3.odt", "/tmp/current.odt"]:
        if os.path.exists(f):
            os.remove(f)

    # Verify
    size = os.path.getsize(OUTPUT)
    print(f"Final ODT created: {OUTPUT} ({size} bytes)")

    with zipfile.ZipFile(OUTPUT, 'r') as z:
        version_entries = [e for e in z.namelist() if 'Version' in e]
        print(f"Version entries in ZIP: {version_entries}")

    # =====================================================
    # Step 3: Open in LibreOffice Writer GUI
    # =====================================================
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
