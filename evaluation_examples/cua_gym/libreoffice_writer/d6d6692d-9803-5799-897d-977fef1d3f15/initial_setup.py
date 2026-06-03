"""
Initial Setup: RL Papers from cs.LG March 2024 - LibreOffice Writer task
Task ID: osworld_multi_apps_hf_papers_writer_009
Domain: libreoffice_writer

Creates rl_papers.odt with only the heading 'Reinforcement Learning Papers - cs.LG March 2024'.
Opens Chrome (for the agent to navigate to arxiv.org) and LibreOffice Writer with the file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_009'
OUTPUT = f'{WORKDIR}/rl_papers.odt'


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
    # Use odfpy to create an ODT file with only a heading
    try:
        from odf.opendocument import OpenDocumentText
        from odf.style import Style, TextProperties, ParagraphProperties
        from odf.text import H, P
        from odf import teletype

        doc = OpenDocumentText()

        # Create heading style
        h1style = Style(name="Heading 1", family="paragraph")
        h1style.addElement(TextProperties(attributes={
            'fo:font-size': '18pt',
            'fo:font-weight': 'bold',
        }))
        doc.styles.addElement(h1style)

        # Add heading
        heading = H(outlinelevel=1, stylename="Heading 1")
        heading.addText("Reinforcement Learning Papers - cs.LG March 2024")
        doc.text.addElement(heading)

        doc.save(OUTPUT)
        print(f"Initial ODT file created: {OUTPUT}")

    except ImportError:
        # Fallback: create a minimal ODT using zipfile (ODT is a zip containing XML)
        import zipfile
        import io

        mimetype_content = b"application/vnd.oasis.opendocument.text"

        manifest_content = """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
 <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.text"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="settings.xml" manifest:media-type="text/xml"/>
</manifest:manifest>"""

        content_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="P1" style:family="paragraph" style:parent-style-name="Heading_20_1">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:h text:outline-level="1" text:style-name="P1">Reinforcement Learning Papers - cs.LG March 2024</text:h>
    </office:text>
  </office:body>
</office:document-content>"""

        styles_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph" style:class="text">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
  </office:styles>
</office:document-styles>"""

        meta_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    office:version="1.2">
  <office:meta/>
</office:document-meta>"""

        settings_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    office:version="1.2">
  <office:settings/>
</office:document-settings>"""

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            # mimetype must be first and uncompressed
            zf.writestr(zipfile.ZipInfo('mimetype'), mimetype_content)
            zf.writestr('META-INF/manifest.xml', manifest_content)
            zf.writestr('content.xml', content_xml)
            zf.writestr('styles.xml', styles_xml)
            zf.writestr('meta.xml', meta_xml)
            zf.writestr('settings.xml', settings_xml)

        with open(OUTPUT, 'wb') as f:
            f.write(buf.getvalue())

        print(f"Initial ODT file created (fallback method): {OUTPUT}")

    # Launch Chrome first (agent needs to navigate to arxiv.org)
    launch_gui('google-chrome --new-window "https://arxiv.org/list/cs.LG/2024-03"', delay_sec=3.0)

    # Launch LibreOffice Writer with the ODT file
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome and LibreOffice Writer with DISPLAY=:0')


create_initial()
