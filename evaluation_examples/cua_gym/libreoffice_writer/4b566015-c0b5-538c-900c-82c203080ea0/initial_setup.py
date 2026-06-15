"""
Initial Setup: Master document with stale subdocuments
Task ID: writer_rm_056
Domain: libreoffice_writer

Creates 8 chapter .odt files and a Book_Master.odm master document.
Chapters 2, 5, 7 have updated content in the .odt files but the master
document shows stale/old content for those chapters.
"""

import os
import shlex
import subprocess
import time
import zipfile
import io

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_056'
MASTER_FILE = f'{WORKDIR}/Book_Master.odm'

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


# ── Chapter content definitions ──

CHAPTER_TITLES = {
    1: "The Foundation of Modern Architecture",
    2: "Materials and Structural Engineering",
    3: "Urban Planning and City Design",
    4: "Sustainable Building Practices",
    5: "Interior Design Philosophy",
    6: "Historical Preservation Methods",
    7: "Digital Tools in Architecture",
    8: "Future Trends in Construction",
}

# Current (updated) content for each chapter
CHAPTER_CONTENT_CURRENT = {
    1: [
        "Modern architecture emerged in the early 20th century as a rejection of ornate historical styles.",
        "Pioneers like Le Corbusier, Ludwig Mies van der Rohe, and Frank Lloyd Wright championed functional design that celebrated clean lines and open spaces.",
        "The Bauhaus movement, founded in 1919 by Walter Gropius in Weimar, Germany, became the intellectual cradle of modernist thought.",
        "By the 1950s, the International Style had spread across continents, transforming skylines from New York to Tokyo.",
    ],
    2: [
        "Reinforced concrete revolutionized construction by combining the compressive strength of concrete with the tensile strength of steel reinforcement bars.",
        "Cross-laminated timber (CLT) has emerged as a sustainable alternative to steel framing, offering comparable strength with a significantly lower carbon footprint.",
        "Advanced composite materials, including carbon fiber reinforced polymers, are now being integrated into high-performance building facades.",
        "The development of self-healing concrete using bacteria that produce limestone represents a breakthrough in material longevity and maintenance reduction.",
    ],
    3: [
        "Effective urban planning balances residential, commercial, and recreational zones to create livable communities that serve diverse populations.",
        "Transit-oriented development concentrates mixed-use areas around public transportation hubs, reducing car dependency and promoting walkability.",
        "Green infrastructure, including bioswales, rain gardens, and permeable pavements, manages stormwater while enhancing urban biodiversity.",
        "The 15-minute city concept proposes that all essential services should be accessible within a short walk or bike ride from any residence.",
    ],
    4: [
        "Net-zero energy buildings generate as much renewable energy as they consume annually through a combination of solar panels, geothermal systems, and energy-efficient design.",
        "Passive house standards require airtight construction with continuous insulation, dramatically reducing heating and cooling energy demands by up to 90 percent.",
        "Life-cycle assessment (LCA) evaluates the total environmental impact of building materials from extraction through manufacturing, use, and eventual disposal.",
        "Biophilic design integrates natural elements such as living walls, natural ventilation, and daylight harvesting to improve occupant health and productivity.",
    ],
    5: [
        "Contemporary interior design embraces minimalism as a guiding philosophy, prioritizing intentional simplicity and functional beauty.",
        "The integration of smart home technology has transformed interior spaces, with automated lighting, climate control, and voice-activated systems becoming standard features.",
        "Biophilic interior elements, including indoor gardens, natural wood finishes, and water features, create spaces that reconnect occupants with nature.",
        "Adaptive reuse of industrial spaces has given rise to the modern loft aesthetic, combining exposed structural elements with refined residential comfort.",
    ],
    6: [
        "Historical preservation maintains the cultural identity of communities by protecting buildings and sites of architectural significance.",
        "The Secretary of the Interior's Standards for Rehabilitation provide a framework for updating historic structures while preserving their character-defining features.",
        "Adaptive reuse transforms obsolete buildings into functional modern spaces, balancing preservation with contemporary needs.",
        "Digital documentation techniques, including photogrammetry and 3D laser scanning, create precise records of historical structures for future generations.",
    ],
    7: [
        "Building Information Modeling (BIM) enables architects to create comprehensive digital representations that integrate structural, mechanical, and electrical systems in a single coordinated model.",
        "Parametric design software such as Grasshopper and Dynamo allows architects to explore complex geometries through algorithmic manipulation of design variables.",
        "Virtual reality walkthroughs now allow clients and stakeholders to experience proposed designs at full scale before any physical construction begins.",
        "Artificial intelligence tools are being deployed for generative design, energy optimization, and automated code compliance checking.",
    ],
    8: [
        "3D printing technology enables the rapid fabrication of building components and even entire structures using concrete, recycled plastics, and bio-based materials.",
        "Modular and prefabricated construction methods are reducing project timelines by up to 50 percent while improving quality control in factory settings.",
        "Robotic construction systems, including autonomous bricklaying and welding robots, address labor shortages while increasing precision and safety on job sites.",
        "Responsive architecture incorporates kinetic facades, adaptive shading systems, and shape-memory materials that react dynamically to environmental conditions.",
    ],
}

# Old/stale content for chapters 2, 5, 7 (what the master doc will show)
CHAPTER_CONTENT_STALE = {
    2: [
        "Concrete and steel have been the primary materials in modern construction for over a century.",
        "Wood-frame construction remains popular for residential buildings in many regions due to its cost-effectiveness.",
        "New composite materials are being explored for potential use in building applications.",
    ],
    5: [
        "Interior design focuses on creating functional and aesthetically pleasing indoor environments.",
        "Color theory and spatial planning are fundamental skills for any interior designer.",
        "Furniture selection and arrangement play a key role in defining the character of a room.",
    ],
    7: [
        "Computer-aided design (CAD) software has replaced hand drafting in most architectural firms.",
        "3D rendering tools help architects visualize their designs before construction begins.",
        "Digital collaboration platforms enable teams to work together across geographic boundaries.",
    ],
}

STALE_CHAPTERS = {2, 5, 7}


def create_odt_file(filepath, title, paragraphs):
    """Create an .odt file using raw ODF XML in a ZIP archive."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and uncompressed
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text',
                     compress_type=zipfile.ZIP_STORED)

        manifest = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2"
                       manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''
        zf.writestr('META-INF/manifest.xml', manifest)

        # Build content paragraphs
        para_xml = ''
        for p in paragraphs:
            escaped = p.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            para_xml += f'    <text:p text:style-name="Standard">{escaped}</text:p>\n'

        title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        content = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="Standard" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0.2cm" fo:margin-bottom="0.2cm"/>
    </style:style>
    <style:style style:name="Heading1" style:family="paragraph">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
      <style:paragraph-properties fo:margin-top="0.5cm" fo:margin-bottom="0.3cm"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
    <text:p text:style-name="Heading1">{title_escaped}</text:p>
{para_xml}    </office:text>
  </office:body>
</office:document-content>'''
        zf.writestr('content.xml', content)

        styles = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''
        zf.writestr('styles.xml', styles)

    with open(filepath, 'wb') as f:
        f.write(buf.getvalue())


def create_master_document(filepath, chapter_files, stale_chapters, current_content, stale_content, titles):
    """
    Create an .odm master document with section links to chapter files.
    For stale chapters, the embedded/cached text in the section shows old content.
    For up-to-date chapters, the embedded text matches the .odt file content.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype - MUST be first entry and stored uncompressed
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text-master',
                     compress_type=zipfile.ZIP_STORED)

        manifest = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2"
                       manifest:media-type="application/vnd.oasis.opendocument.text-master"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''
        zf.writestr('META-INF/manifest.xml', manifest)

        # Build sections with linked subdocuments
        sections_xml = ''
        for ch_num in sorted(chapter_files.keys()):
            ch_file = chapter_files[ch_num]
            section_name = f'Chapter{ch_num}'
            title = titles[ch_num]

            # Determine which content to embed (cached text in master)
            if ch_num in stale_chapters:
                paragraphs = stale_content[ch_num]
            else:
                paragraphs = current_content[ch_num]

            # Build paragraph XML for the cached content in the section
            para_xml = ''
            title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            para_xml += f'        <text:p text:style-name="Heading1">{title_escaped}</text:p>\n'
            for p in paragraphs:
                escaped = p.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                para_xml += f'        <text:p text:style-name="Standard">{escaped}</text:p>\n'

            sections_xml += f'''
      <text:section text:style-name="SectDefault" text:name="{section_name}"
                    text:protected="false">
        <text:section-source xlink:href="{ch_file}"
                             xmlns:xlink="http://www.w3.org/1999/xlink"
                             text:section-name=""
                             text:filter-name="writer8"/>
{para_xml}      </text:section>
'''

        content = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="Standard" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0.2cm" fo:margin-bottom="0.2cm"/>
    </style:style>
    <style:style style:name="Heading1" style:family="paragraph">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
      <style:paragraph-properties fo:margin-top="0.5cm" fo:margin-bottom="0.3cm"/>
    </style:style>
    <style:style style:name="SectDefault" style:family="section"/>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:p text:style-name="Heading1">Architecture: A Comprehensive Study</text:p>
      <text:p text:style-name="Standard">This master document compiles all chapters of the architecture textbook.</text:p>
{sections_xml}
    </office:text>
  </office:body>
</office:document-content>'''
        zf.writestr('content.xml', content)

        styles = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''
        zf.writestr('styles.xml', styles)

    with open(filepath, 'wb') as f:
        f.write(buf.getvalue())


def create_initial():
    # Step 1: Create all 8 chapter .odt files with CURRENT content
    chapter_files = {}
    for ch_num in range(1, 9):
        filename = f'Chapter{ch_num}.odt'
        filepath = f'{WORKDIR}/{filename}'
        create_odt_file(
            filepath,
            CHAPTER_TITLES[ch_num],
            CHAPTER_CONTENT_CURRENT[ch_num],
        )
        chapter_files[ch_num] = filename
        print(f'Created {filepath}')

    # Step 2: Create master document with stale content for chapters 2, 5, 7
    create_master_document(
        MASTER_FILE,
        chapter_files,
        STALE_CHAPTERS,
        CHAPTER_CONTENT_CURRENT,
        CHAPTER_CONTENT_STALE,
        CHAPTER_TITLES,
    )
    print(f'Created master document: {MASTER_FILE}')

    # Step 3: Open the master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{MASTER_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with Book_Master.odm on DISPLAY=:0')


create_initial()
