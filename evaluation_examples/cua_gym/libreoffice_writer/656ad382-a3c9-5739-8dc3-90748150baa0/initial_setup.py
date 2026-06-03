"""
Initial Setup: Master document with 6 chapter subdocuments, each with footnotes restarting at 1.
Task ID: writer_rm_082
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_082'
MASTER_FILE = f'{WORKDIR}/History_Book_Master.odm'

# Namespace map for ODF
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'svg': 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'meta': 'urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
    'number': 'urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'manifest': 'urn:oasis:names:tc:opendocument:xmlns:manifest:1.0',
}

# Chapter content and footnotes
CHAPTERS = [
    {
        'title': 'Chapter 1: The Dawn of Civilization',
        'paragraphs': [
            'The earliest civilizations emerged in the fertile river valleys of Mesopotamia around 3500 BCE.',
            'Agriculture transformed nomadic tribes into settled communities, enabling the development of complex social structures.',
            'The invention of writing in Sumer around 3200 BCE marked a pivotal moment in human history.',
            'Trade routes between city-states facilitated cultural exchange and economic growth across the region.',
            'Religious institutions played a central role in governance, with temple complexes serving as administrative centers.',
        ],
        'footnotes': [
            'Kramer, S.N., "The Sumerians: Their History, Culture, and Character," University of Chicago Press, 1963.',
            'Diamond, J., "Guns, Germs, and Steel: The Fates of Human Societies," W.W. Norton, 1997, pp. 85-92.',
            'Schmandt-Besserat, D., "Before Writing: From Counting to Cuneiform," University of Texas Press, 1992.',
            'Algaze, G., "The Uruk World System," University of Chicago Press, 2005, pp. 45-67.',
            'Van De Mieroop, M., "The Ancient Mesopotamian City," Oxford University Press, 1997.',
        ],
    },
    {
        'title': 'Chapter 2: Classical Antiquity',
        'paragraphs': [
            'The Greek city-states developed the foundations of Western democratic thought during the 5th century BCE.',
            'Athens under Pericles experienced an unprecedented golden age of art, philosophy, and political innovation.',
            'The Persian Wars united the fractious Greek poleis against a common threat from the east.',
            'Alexander the Great\'s conquests spread Hellenistic culture from Egypt to the borders of India.',
            'Roman engineering achievements, including aqueducts and roads, transformed the Mediterranean landscape.',
            'The Roman Republic\'s transition to an empire under Augustus reshaped governance for centuries.',
            'Greco-Roman philosophical traditions, from Socrates to Seneca, continue to influence modern thought.',
            'The decline of Rome in the 5th century CE marked the end of classical antiquity in the West.',
        ],
        'footnotes': [
            'Hansen, M.H., "The Athenian Democracy in the Age of Demosthenes," University of Oklahoma Press, 1999.',
            'Kagan, D., "Pericles of Athens and the Birth of Democracy," Free Press, 1991, pp. 120-145.',
            'Holland, T., "Persian Fire: The First World Empire and the Battle for the West," Doubleday, 2005.',
            'Green, P., "Alexander of Macedon, 356-323 B.C.," University of California Press, 1991.',
            'Laurence, R., "The Roads of Roman Italy," Routledge, 1999, pp. 55-78.',
            'Goldsworthy, A., "Augustus: First Emperor of Rome," Yale University Press, 2014.',
            'Long, A.A., "Hellenistic Philosophy," University of California Press, 1986.',
            'Heather, P., "The Fall of the Roman Empire," Oxford University Press, 2006, pp. 301-340.',
        ],
    },
    {
        'title': 'Chapter 3: The Medieval World',
        'paragraphs': [
            'The feudal system organized medieval European society into hierarchical relationships of obligation and protection.',
            'Monastic communities preserved classical learning through centuries of political instability.',
            'The Crusades brought European powers into sustained contact with the Islamic world.',
            'Gothic cathedral construction represented both artistic achievement and communal devotion.',
            'The Black Death of 1347-1351 decimated European populations and transformed social structures.',
            'Medieval universities at Bologna, Paris, and Oxford established enduring models of higher education.',
        ],
        'footnotes': [
            'Bloch, M., "Feudal Society," University of Chicago Press, 1961, vol. 1, pp. 145-175.',
            'Lawrence, C.H., "Medieval Monasticism," Longman, 2001, pp. 88-112.',
            'Tyerman, C., "God\'s War: A New History of the Crusades," Harvard University Press, 2006.',
            'Scott, R.A., "The Gothic Enterprise: A Guide to Understanding the Medieval Cathedral," University of California Press, 2003.',
            'Ziegler, P., "The Black Death," Harper Perennial, 2009, pp. 220-248.',
            'Haskins, C.H., "The Rise of Universities," Cornell University Press, 1957.',
            'Wickham, C., "The Inheritance of Rome: Illuminating the Dark Ages," Penguin, 2009, pp. 55-80.',
        ],
    },
    {
        'title': 'Chapter 4: Renaissance and Reformation',
        'paragraphs': [
            'The Italian Renaissance sparked a cultural rebirth that redefined European art, science, and philosophy.',
            'Patronage networks in Florence, particularly under the Medici family, fueled artistic innovation.',
            'Gutenberg\'s printing press, developed around 1440, revolutionized the dissemination of knowledge.',
            'Martin Luther\'s Ninety-Five Theses of 1517 challenged papal authority and fractured Western Christianity.',
            'The Counter-Reformation strengthened Catholic institutions while addressing internal corruption.',
            'Scientific inquiry during this period laid groundwork for the later Scientific Revolution.',
        ],
        'footnotes': [
            'Burckhardt, J., "The Civilization of the Renaissance in Italy," Penguin Classics, 2004.',
            'Strathern, P., "The Medici: Power, Money, and Ambition in the Italian Renaissance," Pegasus, 2016, pp. 67-95.',
            'Eisenstein, E., "The Printing Revolution in Early Modern Europe," Cambridge University Press, 2005.',
            'MacCulloch, D., "The Reformation: A History," Viking, 2003, pp. 110-155.',
            'O\'Malley, J.W., "Trent: What Happened at the Council," Harvard University Press, 2013.',
        ],
    },
    {
        'title': 'Chapter 5: The Age of Revolutions',
        'paragraphs': [
            'The Enlightenment provided intellectual foundations for political upheaval across the Atlantic world.',
            'The American Revolution of 1776 established a republic based on principles of liberty and self-governance.',
            'The French Revolution of 1789 violently dismantled the ancien regime and inspired movements worldwide.',
            'The Haitian Revolution represented the first successful large-scale slave revolt in modern history.',
            'Napoleon Bonaparte\'s campaigns reshaped European borders and spread revolutionary ideals by force.',
            'The Industrial Revolution transformed economic production and created new social classes.',
            'Latin American independence movements drew on Enlightenment ideals to challenge colonial rule.',
        ],
        'footnotes': [
            'Israel, J., "Radical Enlightenment: Philosophy and the Making of Modernity," Oxford University Press, 2001.',
            'Wood, G.S., "The Radicalism of the American Revolution," Vintage, 1993, pp. 189-225.',
            'Schama, S., "Citizens: A Chronicle of the French Revolution," Vintage, 1990.',
            'Dubois, L., "Avengers of the New World: The Story of the Haitian Revolution," Harvard University Press, 2004, pp. 78-102.',
            'Roberts, A., "Napoleon: A Life," Viking, 2014.',
            'Mokyr, J., "The Enlightened Economy: An Economic History of Britain," Yale University Press, 2009, pp. 280-315.',
        ],
    },
    {
        'title': 'Chapter 6: The Modern Era',
        'paragraphs': [
            'The two World Wars of the 20th century reshaped global power structures and international relations.',
            'Decolonization movements after 1945 transformed the political map of Africa and Asia.',
            'The Cold War divided the world into competing ideological blocs for nearly half a century.',
            'The digital revolution, beginning in the late 20th century, has transformed communication and commerce.',
            'Globalization has connected economies and cultures while generating new forms of inequality.',
            'Climate change has emerged as the defining challenge of the 21st century.',
        ],
        'footnotes': [
            'Keegan, J., "The First World War," Vintage, 2000, pp. 3-28.',
            'Beevor, A., "The Second World War," Little, Brown, 2012.',
            'Springhall, J., "Decolonization since 1945," Palgrave Macmillan, 2001, pp. 45-68.',
            'Gaddis, J.L., "The Cold War: A New History," Penguin, 2005.',
            'Isaacson, W., "The Innovators: How a Group of Hackers, Geniuses, and Geeks Created the Digital Revolution," Simon & Schuster, 2014, pp. 310-350.',
            'Stiglitz, J., "Globalization and Its Discontents Revisited," W.W. Norton, 2017.',
            'Kolbert, E., "Under a White Sky: The Nature of the Future," Crown, 2021, pp. 88-115.',
            'Mann, M., "The New Climate War," PublicAffairs, 2021.',
        ],
    },
]

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


def create_odt_chapter(filepath, chapter_data, restart_footnotes=True):
    """Create an ODT file for a chapter with footnotes that restart numbering at 1."""

    # Build content.xml
    content_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    office:version="1.3">
  <office:automatic-styles>
    <style:style style:name="Heading1" style:family="paragraph" style:parent-style-name="Heading_20_1">
      <style:paragraph-properties fo:margin-top="0.5cm" fo:margin-bottom="0.3cm"/>
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="BodyText" style:family="paragraph">
      <style:paragraph-properties fo:margin-bottom="0.3cm"/>
      <style:text-properties fo:font-size="12pt"/>
    </style:style>
    <style:style style:name="FootnoteAnchor" style:family="text">
      <style:text-properties style:text-position="super 58%"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:sequence-decls>
        <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Text"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Figure"/>
      </text:sequence-decls>
'''

    # Add title
    content_xml += f'      <text:h text:style-name="Heading1" text:outline-level="1">{chapter_data["title"]}</text:h>\n'

    # Add paragraphs with footnotes
    fn_idx = 0
    for i, para_text in enumerate(chapter_data['paragraphs']):
        content_xml += f'      <text:p text:style-name="BodyText">{para_text}'
        # Add a footnote at the end of paragraphs that have them
        if fn_idx < len(chapter_data['footnotes']):
            fn_text = chapter_data['footnotes'][fn_idx]
            fn_num = fn_idx + 1  # Always restart from 1
            content_xml += f'''<text:note text:id="ftn{fn_num}" text:note-class="footnote">
          <text:note-citation>{fn_num}</text:note-citation>
          <text:note-body>
            <text:p text:style-name="BodyText">{fn_text}</text:p>
          </text:note-body>
        </text:note>'''
            fn_idx += 1
        content_xml += '</text:p>\n'

    # Add any remaining footnotes to the last paragraph's continuation
    while fn_idx < len(chapter_data['footnotes']):
        fn_text = chapter_data['footnotes'][fn_idx]
        fn_num = fn_idx + 1
        content_xml += f'''      <text:p text:style-name="BodyText">Additional scholarly references support these findings.<text:note text:id="ftn{fn_num}" text:note-class="footnote">
          <text:note-citation>{fn_num}</text:note-citation>
          <text:note-body>
            <text:p text:style-name="BodyText">{fn_text}</text:p>
          </text:note-body>
        </text:note></text:p>\n'''
        fn_idx += 1

    content_xml += '''    </office:text>
  </office:body>
</office:document-content>'''

    # Build styles.xml with footnote configuration
    # restart_footnotes=True means per-document restart (default for each subdocument)
    fn_config = 'text:start-value="0"' if restart_footnotes else ''
    styles_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:styles>
    <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph"
                 style:class="text">
      <style:paragraph-properties fo:margin-top="0.5cm" fo:margin-bottom="0.3cm"/>
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
    <style:style style:name="Footnote" style:family="paragraph" style:class="extra"/>
    <text:notes-configuration text:note-class="footnote"
        text:citation-style-name="FootnoteAnchor"
        text:citation-body-style-name="FootnoteAnchor"
        style:num-format="1"
        text:start-numbering-at="document"
        {fn_config}/>
  </office:styles>
  <office:automatic-styles>
    <style:page-layout style:name="pm1">
      <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm"
          fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm"/>
    </style:page-layout>
  </office:automatic-styles>
  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="pm1"/>
  </office:master-styles>
</office:document-styles>'''

    # Build META-INF/manifest.xml
    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.3">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    office:version="1.3">
  <office:meta>
    <dc:title></dc:title>
  </office:meta>
</office:document-meta>'''

    mimetype = 'application/vnd.oasis.opendocument.text'

    # Create ODF zip
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and uncompressed
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    print(f'Created: {filepath}')


def create_master_document(master_path, chapter_paths):
    """Create an ODM master document that links to chapter subdocuments."""

    # Build content.xml with text:section elements pointing to subdocuments
    sections_xml = ''
    for i, ch_path in enumerate(chapter_paths):
        ch_name = os.path.basename(ch_path)
        sections_xml += f'''      <text:section text:style-name="SectLink{i+1}" text:name="Section{i+1}">
        <text:section-source xlink:href="{ch_name}" text:section-name="" text:filter-name="writer8"/>
      </text:section>
'''

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    office:version="1.3">
  <office:automatic-styles>
    <style:style style:name="SectLink1" style:family="section"/>
    <style:style style:name="SectLink2" style:family="section"/>
    <style:style style:name="SectLink3" style:family="section"/>
    <style:style style:name="SectLink4" style:family="section"/>
    <style:style style:name="SectLink5" style:family="section"/>
    <style:style style:name="SectLink6" style:family="section"/>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:sequence-decls>
        <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Text"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Figure"/>
      </text:sequence-decls>
{sections_xml}    </office:text>
  </office:body>
</office:document-content>'''

    # Footnote configuration: each chapter restarts numbering (per-chapter = per-page or per-document in subdocuments)
    # The initial state has footnotes restarting per chapter
    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:styles>
    <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
    <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph"
                 style:class="text">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <text:notes-configuration text:note-class="footnote"
        style:num-format="1"
        text:start-numbering-at="document"
        text:start-value="0"/>
  </office:styles>
  <office:automatic-styles>
    <style:page-layout style:name="pm1">
      <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm"
          fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm"/>
    </style:page-layout>
  </office:automatic-styles>
  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="pm1"/>
  </office:master-styles>
</office:document-styles>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.3">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text-master"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    office:version="1.3">
  <office:meta>
    <dc:title>A Comprehensive History of World Civilizations</dc:title>
  </office:meta>
</office:document-meta>'''

    mimetype = 'application/vnd.oasis.opendocument.text-master'

    with zipfile.ZipFile(master_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    print(f'Created master document: {master_path}')


def create_initial():
    # Create chapter files
    chapter_paths = []
    for i, chapter in enumerate(CHAPTERS):
        ch_path = f'{WORKDIR}/Chapter{i+1}.odt'
        create_odt_chapter(ch_path, chapter, restart_footnotes=True)
        chapter_paths.append(ch_path)

    # Create master document
    create_master_document(MASTER_FILE, chapter_paths)

    # Launch master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{MASTER_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with History_Book_Master.odm on DISPLAY=:0')


create_initial()
