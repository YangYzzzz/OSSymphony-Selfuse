"""
Initial Setup: Create a LibreOffice Writer master document with 7 subdocuments, unprotected.
Task ID: writer_rm_087
Domain: libreoffice_writer

Uses only stdlib (zipfile, xml) to build ODF files — no odfpy dependency.
"""

import os
import shlex
import subprocess
import time
import zipfile
import hashlib
import base64
from xml.etree.ElementTree import Element, SubElement, tostring

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_087'
ODM_FILE = f'{WORKDIR}/{TASK_ID}.odm'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style':  'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'fo':     'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'xlink':  'http://www.w3.org/1999/xlink',
    'meta':   'urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
    'dc':     'http://purl.org/dc/elements/1.1/',
    'svg':    'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
    'manifest': 'urn:oasis:names:tc:opendocument:xmlns:manifest:1.0',
}


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


def make_odt_content(heading, paragraphs):
    """Build a minimal content.xml string for an ODF text document."""
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:automatic-styles/>
  <office:body>
    <office:text>
      <text:h text:outline-level="1">{heading}</text:h>
'''
    for p in paragraphs:
        xml += f'      <text:p>{p}</text:p>\n'
    xml += '''    </office:text>
  </office:body>
</office:document-content>'''
    return xml


def make_odt_styles():
    """Minimal styles.xml for ODF."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''


def make_meta():
    """Minimal meta.xml."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    office:version="1.3">
  <office:meta>
    <dc:title>Official Documentation</dc:title>
  </office:meta>
</office:document-meta>'''


def make_manifest(mimetype, extra_entries=None):
    """Build META-INF/manifest.xml."""
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
    manifest:version="1.3">
  <manifest:file-entry manifest:media-type="{mimetype}" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>
'''
    if extra_entries:
        for entry in extra_entries:
            xml += f'  <manifest:file-entry manifest:media-type="{entry[0]}" manifest:full-path="{entry[1]}"/>\n'
    xml += '</manifest:manifest>'
    return xml


def write_odf_zip(filepath, mimetype, content_xml, styles_xml=None, meta_xml=None, manifest_xml=None):
    """Write a minimal ODF ZIP package."""
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype MUST be first and uncompressed
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml or make_odt_styles())
        zf.writestr('meta.xml', meta_xml or make_meta())
        zf.writestr('META-INF/manifest.xml',
                     manifest_xml or make_manifest(mimetype))


def create_subdocuments():
    """Create 7 realistic subdocument .odt files."""
    subdocs = [
        ("Chapter1_Introduction.odt", "Chapter 1: Introduction",
         ["This document provides an overview of the Official Documentation project.",
          "The project aims to standardize all corporate documentation across departments.",
          "Last revised: March 2026 by Document Control Team."]),
        ("Chapter2_Policies.odt", "Chapter 2: Corporate Policies",
         ["All employees must adhere to the policies outlined in this section.",
          "Policy updates are reviewed quarterly by the compliance team.",
          "Effective date: January 1, 2026."]),
        ("Chapter3_Procedures.odt", "Chapter 3: Standard Operating Procedures",
         ["This chapter details the step-by-step procedures for common operations.",
          "Each procedure has been validated by the Quality Assurance department.",
          "Procedure templates are available on the internal portal."]),
        ("Chapter4_Guidelines.odt", "Chapter 4: Technical Guidelines",
         ["Technical guidelines cover software development, infrastructure, and security.",
          "All code must pass automated testing before deployment to production.",
          "Security audits are conducted bi-annually by the InfoSec team."]),
        ("Chapter5_Compliance.odt", "Chapter 5: Regulatory Compliance",
         ["This section addresses compliance with industry regulations and standards.",
          "Annual compliance training is mandatory for all staff members.",
          "Non-compliance incidents must be reported within 24 hours."]),
        ("Chapter6_Training.odt", "Chapter 6: Training Materials",
         ["Training resources are organized by department and skill level.",
          "New employee onboarding includes a 2-week training program.",
          "Advanced certification courses are available through our partner institutions."]),
        ("Chapter7_Appendices.odt", "Chapter 7: Appendices",
         ["Appendix A: Glossary of Terms",
          "Appendix B: Reference Documents and External Links",
          "Appendix C: Change Log and Version History"]),
    ]

    odt_mime = 'application/vnd.oasis.opendocument.text'
    filenames = []
    for filename, heading, paragraphs in subdocs:
        filepath = os.path.join(WORKDIR, filename)
        content = make_odt_content(heading, paragraphs)
        write_odf_zip(filepath, odt_mime, content)
        filenames.append(filename)
        print(f"  Created subdocument: {filepath}")

    return filenames


def make_master_content(subdoc_filenames, protected=False, password_hash=None):
    """Build content.xml for the master document with linked sections."""
    odm_mime = 'application/vnd.oasis.opendocument.text-master'

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    office:version="1.3">
  <office:automatic-styles/>
  <office:body>
    <office:text>
      <text:h text:outline-level="1">Official Documentation Master</text:h>
      <text:p>This master document links all official documentation chapters.</text:p>
'''

    for i, filename in enumerate(subdoc_filenames):
        section_name = f"LinkedSection{i+1}"
        prot_attrs = ''
        if protected and password_hash:
            prot_attrs = f' text:protected="true" text:protection-key="{password_hash}"'

        xml += f'''      <text:section text:name="{section_name}"{prot_attrs}>
        <text:section-source xlink:href="{filename}" xlink:type="simple" text:section-name=""/>
        <text:p>[Content from {filename}]</text:p>
      </text:section>
'''

    xml += '''    </office:text>
  </office:body>
</office:document-content>'''
    return xml


def main():
    # Step 1: Create subdocument files
    print("Creating subdocuments...")
    subdoc_filenames = create_subdocuments()

    # Step 2: Create unprotected master document
    print("Creating master document (unprotected)...")
    odm_mime = 'application/vnd.oasis.opendocument.text-master'
    content = make_master_content(subdoc_filenames, protected=False)
    write_odf_zip(ODM_FILE, odm_mime, content)

    # Step 3: Verify
    assert os.path.exists(ODM_FILE), f"Master document not found: {ODM_FILE}"
    print(f"Master document created: {ODM_FILE}")
    print(f"File size: {os.path.getsize(ODM_FILE)} bytes")

    # Verify no protection in the file
    with zipfile.ZipFile(ODM_FILE, 'r') as z:
        content_xml = z.read('content.xml').decode('utf-8')
        assert 'text:protected' not in content_xml, "ERROR: Protection found in initial file!"
        print("Verification: No protection attributes found (correct for initial state)")

    # Step 4: Open in LibreOffice Writer (master document mode)
    launch_gui(f'libreoffice --writer "{ODM_FILE}"', delay_sec=3.0)
    print("GUI_READY: launched LibreOffice Writer with DISPLAY=:0")


main()
