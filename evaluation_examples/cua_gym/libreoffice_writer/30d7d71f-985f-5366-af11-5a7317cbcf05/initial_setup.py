"""
Initial Setup: Create a 4-page document with three footnotes
Task ID: writer_bs_009
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
import tempfile

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_009'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'


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
    """
    Build a .docx with 3 footnotes across 4 pages using raw OOXML.
    python-docx does not support footnotes natively, so we build
    the document from scratch using XML templates.
    """

    # --- XML Templates ---
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>
  <Override PartName="/word/endnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''

    rels_root = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    rels_word = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes" Target="endnotes.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>'''

    settings_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:defaultTabStop w:val="720"/>
</w:settings>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="character" w:styleId="FootnoteReference">
    <w:name w:val="footnote reference"/>
    <w:rPr><w:vertAlign w:val="superscript"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="FootnoteText">
    <w:name w:val="footnote text"/>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="character" w:styleId="EndnoteReference">
    <w:name w:val="endnote reference"/>
    <w:rPr><w:vertAlign w:val="superscript"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="EndnoteText">
    <w:name w:val="endnote text"/>
    <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
</w:styles>'''

    # Build body paragraphs with page breaks and footnote references
    # Page 1 content with footnote 1
    page1 = '''
    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
      <w:r><w:t>Global Economic Outlook Report 2024</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">The global economy experienced significant shifts in 2023, with emerging markets showing resilience despite ongoing geopolitical tensions. According to recent data, global GDP growth reached 3.1% in the fiscal year, surpassing initial estimates by major financial institutions.</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
      <w:r><w:t>1. Overview of Global Growth Trends</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">Developing nations contributed disproportionately to global output in 2023. Sub-Saharan Africa recorded a growth rate of 4.2%, while South Asia maintained momentum at 5.8%. These regions benefited from improved trade connectivity and targeted investment in infrastructure development. The manufacturing sector in particular saw a resurgence, driven by supply chain diversification strategies adopted after the pandemic disruptions of previous years.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">International lending institutions have increased their support for sustainable development projects. Total development financing reached $412 billion in 2023</w:t></w:r>
      <w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="1"/></w:r>
      <w:r><w:t xml:space="preserve">, marking a 15% increase over the previous year. This growth in funding has been particularly notable in renewable energy and digital infrastructure sectors.</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">Trade volumes recovered strongly, with merchandise trade growing by 3.5% year-over-year. Services trade showed even stronger performance, expanding by 4.8% as international travel and tourism rebounded to near pre-pandemic levels.</w:t></w:r></w:p>'''

    # Page break + Page 2 with footnote 2
    page2 = '''
    <w:p><w:r><w:br w:type="page"/></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
      <w:r><w:t>2. Regional Performance Analysis</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">The Asia-Pacific region maintained its position as the fastest-growing economic zone, contributing approximately 60% of global growth. China's economy grew by 5.2%, supported by domestic consumption and targeted fiscal stimulus measures. Japan showed unexpected strength with a 1.9% expansion, its best performance in the current cycle.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">European economies presented a mixed picture. Northern European nations demonstrated steady growth averaging 2.1%, while southern economies continued their gradual recovery. The European Central Bank's monetary policy adjustments played a crucial role in stabilizing financial markets across the continent.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">Consumer purchasing power across OECD nations improved by 2.3% on average</w:t></w:r>
      <w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="2"/></w:r>
      <w:r><w:t xml:space="preserve">, reflecting the combined effect of wage growth outpacing inflation in many developed economies. This improvement was most pronounced in the technology and healthcare sectors.</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">Latin American economies showed divergent trends. Brazil and Mexico recorded solid growth above 3%, while Argentina and Venezuela continued to face macroeconomic challenges including high inflation and currency depreciation.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">The Middle East and North Africa region benefited from stabilized energy prices, with oil-exporting nations channeling revenues into economic diversification programs. The UAE and Saudi Arabia led ambitious infrastructure and tourism development initiatives.</w:t></w:r></w:p>'''

    # Page break + Page 3 with footnote 3
    page3 = '''
    <w:p><w:r><w:br w:type="page"/></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
      <w:r><w:t>3. Sectoral Analysis and Employment Trends</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">The technology sector continued to drive innovation and employment growth globally. Artificial intelligence and machine learning applications expanded across industries, creating an estimated 2.4 million new jobs in 2023 alone. Cloud computing services grew by 22%, reflecting accelerated digital transformation across both public and private sectors.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">The global unemployment rate fell to 5.1%, the lowest level recorded since comprehensive tracking began. Youth unemployment, however, remained elevated in several regions, particularly in North Africa and Southern Europe where rates exceeded 25%.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">Agricultural output increased by 1.8%, driven by improved yields in grain-producing regions and adoption of precision farming technologies. Climate-related disruptions affected production in parts of East Africa and Central America, highlighting the ongoing vulnerability of food systems to environmental change.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">The detailed statistical breakdown reveals significant variations across income groups and geographic regions</w:t></w:r>
      <w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="3"/></w:r>
      <w:r><w:t xml:space="preserve">. Low-income countries showed the highest growth potential but also the greatest volatility, with standard deviations in quarterly GDP figures nearly three times those of high-income economies.</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">Manufacturing output globally expanded by 3.2%, with particular strength in semiconductor production, electric vehicle manufacturing, and pharmaceutical production. The reshoring trend accelerated, with major economies investing in domestic production capabilities for critical technologies.</w:t></w:r></w:p>'''

    # Page break + Page 4
    page4 = '''
    <w:p><w:r><w:br w:type="page"/></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
      <w:r><w:t>4. Policy Recommendations and Future Outlook</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t xml:space="preserve">Based on the analysis presented in the preceding sections, several key policy recommendations emerge for governments and international organizations seeking to sustain and accelerate economic growth while addressing persistent structural challenges.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">First, continued investment in digital infrastructure is essential. Countries that prioritized broadband connectivity and digital skills training showed measurably stronger economic performance. The digital divide between high-income and low-income nations represents both a challenge and an opportunity for targeted development assistance.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">Second, climate-resilient development strategies must be integrated into national economic planning. The estimated cost of climate adaptation for developing nations exceeds $300 billion annually, requiring innovative financing mechanisms and strengthened international cooperation.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">Third, labor market policies need to evolve to address the rapidly changing nature of work. Investment in reskilling programs, portable benefits systems, and flexible labor regulations will be crucial for maintaining social cohesion during the ongoing technological transition.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">Looking ahead to 2025 and beyond, the global economic outlook remains cautiously optimistic. Consensus forecasts project global growth of 3.3% in 2025, with developing economies expected to outpace advanced economies by approximately 2 percentage points. However, significant downside risks persist, including geopolitical tensions, potential financial market corrections, and the uncertain pace of technological disruption across traditional industries.</w:t></w:r></w:p>
    <w:p><w:r><w:t xml:space="preserve">The international community must work collaboratively to address these challenges while capitalizing on the opportunities presented by technological innovation, demographic shifts, and the growing commitment to sustainable development goals.</w:t></w:r></w:p>'''

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {page1}
    {page2}
    {page3}
    {page4}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"
               w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    # Footnotes part: includes separator footnotes (id 0, -1) + our 3 footnotes
    footnotes_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:footnotes xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:footnote w:type="separator" w:id="-1">
    <w:p><w:r><w:separator/></w:r></w:p>
  </w:footnote>
  <w:footnote w:type="continuationSeparator" w:id="0">
    <w:p><w:r><w:continuationSeparator/></w:r></w:p>
  </w:footnote>
  <w:footnote w:id="1">
    <w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:t xml:space="preserve"> Source: World Bank, 2022</w:t></w:r>
    </w:p>
  </w:footnote>
  <w:footnote w:id="2">
    <w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:t xml:space="preserve"> Adjusted for inflation</w:t></w:r>
    </w:p>
  </w:footnote>
  <w:footnote w:id="3">
    <w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:t xml:space="preserve"> See Appendix B for full data</w:t></w:r>
    </w:p>
  </w:footnote>
</w:footnotes>'''

    # Empty endnotes part (required for well-formed docx)
    endnotes_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:endnotes xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:endnote w:type="separator" w:id="-1">
    <w:p><w:r><w:separator/></w:r></w:p>
  </w:endnote>
  <w:endnote w:type="continuationSeparator" w:id="0">
    <w:p><w:r><w:continuationSeparator/></w:r></w:p>
  </w:endnote>
</w:endnotes>'''

    # Build the docx as a zip file
    tmpdir = tempfile.mkdtemp()
    docx_path = OUTPUT

    try:
        with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('[Content_Types].xml', content_types)
            zf.writestr('_rels/.rels', rels_root)
            zf.writestr('word/_rels/document.xml.rels', rels_word)
            zf.writestr('word/document.xml', document_xml)
            zf.writestr('word/styles.xml', styles_xml)
            zf.writestr('word/footnotes.xml', footnotes_xml)
            zf.writestr('word/endnotes.xml', endnotes_xml)
            zf.writestr('word/settings.xml', settings_xml)

        print(f'Initial file created: {docx_path}')
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # GUI-ready: open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{docx_path}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
