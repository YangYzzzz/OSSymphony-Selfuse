"""
Initial Setup: Create a master document with 5 subdocuments
Task ID: writer_rm_053
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
from io import BytesIO

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_053'

# Subdocument file names
SUBDOCS = ['Chapter1.odt', 'Chapter2.odt', 'Chapter3.odt', 'Appendix_A.odt', 'Appendix_C.odt']

# Master document output
MASTER_OUTPUT = f'{WORKDIR}/Report_Master.odm'


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


def create_odt(filepath, title, body_paragraphs):
    """Create a minimal .odt file with given title and body text."""
    # ODT is a ZIP with specific XML structure
    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
 <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:version="1.2" manifest:full-path="/"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
</manifest:manifest>'''

    body_paras = ''
    for p in body_paragraphs:
        body_paras += f'  <text:p text:style-name="Standard">{p}</text:p>\n'

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  office:version="1.2">
 <office:automatic-styles>
  <style:style style:name="Heading1" style:family="paragraph">
   <style:paragraph-properties fo:font-size="18pt" fo:font-weight="bold"/>
  </style:style>
 </office:automatic-styles>
 <office:body>
  <office:text>
   <text:p text:style-name="Heading1">{title}</text:p>
{body_paras}  </office:text>
 </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  office:version="1.2">
 <office:styles>
  <style:style style:name="Standard" style:family="paragraph">
   <style:paragraph-properties fo:margin-top="0.2cm" fo:margin-bottom="0.2cm"/>
   <style:text-properties fo:font-size="12pt"/>
  </style:style>
 </office:styles>
</office:document-styles>'''

    mimetype = 'application/vnd.oasis.opendocument.text'

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and stored uncompressed
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)


def create_odm(filepath, subdoc_filenames):
    """Create a master document (.odm) that links the given subdocuments."""
    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
 <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text-master" manifest:version="1.2" manifest:full-path="/"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
 <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
</manifest:manifest>'''

    # Build section elements for each subdocument
    sections = ''
    for fname in subdoc_filenames:
        section_name = fname.replace('.odt', '')
        sections += f'''   <text:section text:style-name="SectDefault" text:name="{section_name}" text:protected="false">
    <text:section-source xlink:href="{fname}" xlink:type="simple"/>
   </text:section>
'''

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  office:version="1.2">
 <office:automatic-styles>
  <style:style style:name="SectDefault" style:family="section"/>
 </office:automatic-styles>
 <office:body>
  <office:text>
   <text:p text:style-name="Standard">Annual Report - Master Document</text:p>
{sections}  </office:text>
 </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  office:version="1.2">
 <office:styles>
  <style:style style:name="Standard" style:family="paragraph">
   <style:paragraph-properties fo:margin-top="0.2cm" fo:margin-bottom="0.2cm"/>
   <style:text-properties fo:font-size="12pt"/>
  </style:style>
 </office:styles>
</office:document-styles>'''

    mimetype = 'application/vnd.oasis.opendocument.text-master'

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)


def create_initial():
    # Create all 5 subdocument .odt files with realistic content
    subdoc_content = {
        'Chapter1.odt': (
            'Chapter 1: Executive Summary',
            [
                'The fiscal year 2025 marked a significant turning point for Meridian Technologies.',
                'Revenue increased by 18.3% compared to the previous year, reaching $142.7 million.',
                'Our expansion into the Asia-Pacific market contributed $23.4 million in new revenue streams.',
                'Employee headcount grew from 847 to 1,024, with the majority of new hires in engineering and sales.',
                'Key partnerships with Horizon Systems and ClearPath Analytics drove innovation in our core product line.',
            ]
        ),
        'Chapter2.odt': (
            'Chapter 2: Financial Performance',
            [
                'Total revenue for FY2025 was $142.7 million, an increase of $22.1 million over FY2024.',
                'Operating expenses rose to $98.3 million, primarily due to new R&D investments of $31.2 million.',
                'Net income reached $28.9 million, representing a net margin of 20.3%.',
                'Cash reserves stood at $67.5 million by the end of Q4, providing ample runway for planned expansions.',
                'The board approved a quarterly dividend of $0.35 per share, up from $0.28 the prior year.',
            ]
        ),
        'Chapter3.odt': (
            'Chapter 3: Strategic Outlook',
            [
                'In 2026, we plan to launch the Meridian CloudSync platform, targeting enterprise customers.',
                'We anticipate capital expenditures of approximately $15 million for data center upgrades.',
                'A new office in Singapore will serve as our regional headquarters for Asia-Pacific operations.',
                'Projected revenue growth for FY2026 is between 12% and 16%, driven by SaaS subscription models.',
                'We are actively exploring acquisition opportunities in the cybersecurity and AI analytics sectors.',
            ]
        ),
        'Appendix_A.odt': (
            'Appendix A: Quarterly Revenue Breakdown',
            [
                'Q1 2025: $31.2 million (North America: $19.8M, Europe: $7.1M, APAC: $4.3M)',
                'Q2 2025: $34.8 million (North America: $21.5M, Europe: $8.2M, APAC: $5.1M)',
                'Q3 2025: $37.1 million (North America: $22.3M, Europe: $8.9M, APAC: $5.9M)',
                'Q4 2025: $39.6 million (North America: $23.7M, Europe: $9.5M, APAC: $6.4M)',
                'Year-over-year growth was strongest in APAC at 34.2%, followed by Europe at 21.7%.',
            ]
        ),
        'Appendix_C.odt': (
            'Appendix C: Employee Satisfaction Survey Results',
            [
                'Survey conducted in November 2025 with an 87% response rate across all departments.',
                'Overall satisfaction score: 4.2 out of 5.0, up from 3.9 in the prior year.',
                'Top positive factors: flexible work arrangements (4.6), team collaboration (4.4), compensation (4.1).',
                'Areas for improvement: career development pathways (3.5), internal communication tools (3.3).',
                'Voluntary attrition decreased to 8.7% from 12.1%, attributed to improved benefits and remote work policies.',
            ]
        ),
    }

    for fname, (title, paras) in subdoc_content.items():
        filepath = os.path.join(WORKDIR, fname)
        create_odt(filepath, title, paras)
        print(f'Created subdocument: {filepath}')

    # Create master document linking all 5 subdocuments
    create_odm(MASTER_OUTPUT, SUBDOCS)
    print(f'Master document created: {MASTER_OUTPUT}')

    # GUI-ready startup: open the master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{MASTER_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
