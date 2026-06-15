"""
Initial Setup: Create master document with subdocuments for cross-reference task
Task ID: writer_rm_058
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_058'

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


def create_chapter2_odt():
    """Create Chapter2.odt with Table 2.1: Experimental Parameters (captioned)."""
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H, Span, SequenceDecls, SequenceDecl, Sequence, TableOfContentSource
    from odf.table import Table, TableRow, TableCell, TableColumn
    from odf.style import Style, TextProperties, ParagraphProperties, TableProperties, TableColumnProperties, TableCellProperties

    doc = OpenDocumentText()

    # --- Styles ---
    # Heading style
    h1_style = Style(name="Heading1", family="paragraph")
    h1_style.addElement(TextProperties(attributes={
        'fontsize': '18pt', 'fontweight': 'bold',
        'fontname': 'Liberation Sans'
    }))
    h1_style.addElement(ParagraphProperties(attributes={'margintop': '0.4in', 'marginbottom': '0.2in'}))
    doc.styles.addElement(h1_style)

    # Body text style
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(TextProperties(attributes={
        'fontsize': '12pt', 'fontname': 'Liberation Serif'
    }))
    body_style.addElement(ParagraphProperties(attributes={
        'margintop': '0.05in', 'marginbottom': '0.05in'
    }))
    doc.styles.addElement(body_style)

    # Caption style
    caption_style = Style(name="TableCaption", family="paragraph")
    caption_style.addElement(TextProperties(attributes={
        'fontsize': '10pt', 'fontweight': 'bold',
        'fontname': 'Liberation Serif'
    }))
    caption_style.addElement(ParagraphProperties(attributes={
        'margintop': '0.1in', 'marginbottom': '0.1in'
    }))
    doc.styles.addElement(caption_style)

    # Table style
    table_style = Style(name="DataTable", family="table")
    table_style.addElement(TableProperties(attributes={'width': '6in', 'align': 'margins'}))
    doc.automaticstyles.addElement(table_style)

    col_style = Style(name="DataTable.Col", family="table-column")
    col_style.addElement(TableColumnProperties(attributes={'columnwidth': '2in'}))
    doc.automaticstyles.addElement(col_style)

    cell_style = Style(name="DataTable.Cell", family="table-cell")
    cell_style.addElement(TableCellProperties(attributes={
        'padding': '0.04in',
        'borderright': '0.5pt solid #000000',
        'borderbottom': '0.5pt solid #000000',
        'borderleft': '0.5pt solid #000000',
        'bordertop': '0.5pt solid #000000'
    }))
    doc.automaticstyles.addElement(cell_style)

    header_cell_style = Style(name="DataTable.HeaderCell", family="table-cell")
    header_cell_style.addElement(TableCellProperties(attributes={
        'padding': '0.04in',
        'borderright': '0.5pt solid #000000',
        'borderbottom': '0.5pt solid #000000',
        'borderleft': '0.5pt solid #000000',
        'bordertop': '0.5pt solid #000000',
        'backgroundcolor': '#c0c0c0'
    }))
    doc.automaticstyles.addElement(header_cell_style)

    bold_style = Style(name="BoldText", family="text")
    bold_style.addElement(TextProperties(attributes={'fontweight': 'bold'}))
    doc.automaticstyles.addElement(bold_style)

    # --- Sequence declarations for table numbering ---
    seq_decls = SequenceDecls()
    seq_decl = SequenceDecl(attributes={
        'displayoutlinelevel': '0',
        'name': 'Table'
    })
    seq_decls.addElement(seq_decl)
    doc.text.addElement(seq_decls)

    # --- Chapter 2 Content ---
    # Chapter heading
    heading = H(outlinelevel=1, stylename=h1_style)
    heading.addText("Chapter 2: Experimental Methodology")
    doc.text.addElement(heading)

    # Introduction paragraphs
    p1 = P(stylename=body_style)
    p1.addText("This chapter describes the experimental methodology used in the study of thermodynamic properties of novel polymer composites. The research was conducted at the Advanced Materials Laboratory at Stanford University during the 2024-2025 academic year.")
    doc.text.addElement(p1)

    p2 = P(stylename=body_style)
    p2.addText("The experimental design followed a factorial approach, varying temperature, pressure, and composition ratios across multiple trials. Each trial was repeated three times to ensure statistical significance of the results.")
    doc.text.addElement(p2)

    # Section heading
    h2 = H(outlinelevel=2, stylename=h1_style)
    h2.addText("2.1 Experimental Setup")
    doc.text.addElement(h2)

    p3 = P(stylename=body_style)
    p3.addText("The experimental apparatus consisted of a high-precision calorimeter (TA Instruments Q2000), a hydraulic press capable of generating pressures up to 500 MPa, and a custom-designed mixing chamber with real-time viscosity monitoring.")
    doc.text.addElement(p3)

    p4 = P(stylename=body_style)
    p4.addText("The following table summarizes the key experimental parameters used across all trial runs.")
    doc.text.addElement(p4)

    # --- Table 2.1 Caption with sequence field (bookmark for cross-ref) ---
    caption_p = P(stylename=caption_style)
    caption_p.addText("Table ")
    # Add sequence number
    seq = Sequence(attributes={'name': 'Table', 'formula': 'ooow:Table+1'})
    seq.addText("2.1")
    caption_p.addElement(seq)
    caption_p.addText(": Experimental Parameters")
    doc.text.addElement(caption_p)

    # Add a bookmark around the caption for cross-referencing
    from odf.text import BookmarkStart, BookmarkEnd
    # We'll use a reference mark instead for proper cross-referencing
    from odf.text import ReferenceMark, ReferenceMarkStart, ReferenceMarkEnd

    # Actually, let's add the reference mark in a separate paragraph approach
    # We need to rebuild the caption with a reference mark

    # --- Data Table ---
    table = Table(name="Table_2_1", stylename=table_style)

    # Columns
    for i in range(3):
        table.addElement(TableColumn(stylename=col_style))

    # Header row
    headers = ["Parameter", "Value", "Unit"]
    header_row = TableRow()
    for h_text in headers:
        cell = TableCell(stylename=header_cell_style)
        p = P()
        span = Span(stylename=bold_style)
        span.addText(h_text)
        p.addElement(span)
        cell.addElement(p)
        header_row.addElement(cell)
    table.addElement(header_row)

    # Data rows - realistic experimental parameters
    data = [
        ["Temperature Range", "25 - 350", "°C"],
        ["Pressure", "0.1 - 500", "MPa"],
        ["Heating Rate", "10", "°C/min"],
        ["Sample Mass", "15.0 ± 0.5", "mg"],
        ["Atmosphere", "N₂ (99.999%)", "—"],
        ["Flow Rate", "50", "mL/min"],
        ["Polymer Concentration", "5 - 40", "wt%"],
        ["Mixing Speed", "200 - 800", "RPM"],
        ["Equilibration Time", "30", "min"],
        ["Number of Cycles", "3", "per sample"],
    ]

    for row_data in data:
        row = TableRow()
        for val in row_data:
            cell = TableCell(stylename=cell_style)
            p = P()
            p.addText(val)
            cell.addElement(p)
            row.addElement(cell)
        table.addElement(row)

    doc.text.addElement(table)

    # Post-table text
    p5 = P(stylename=body_style)
    p5.addText("All measurements were performed using calibrated instruments with NIST-traceable standards. The uncertainty values reported represent the expanded uncertainty with a coverage factor of k=2, corresponding to a 95% confidence interval.")
    doc.text.addElement(p5)

    p6 = P(stylename=body_style)
    p6.addText("The polymer samples were sourced from Sigma-Aldrich (>99% purity) and used without further purification. Composite samples were prepared by melt-mixing in a Brabender twin-screw extruder at 280°C for 10 minutes.")
    doc.text.addElement(p6)

    # Now add a reference mark around the caption text for cross-referencing
    # We need to manipulate the XML directly to add a reference mark to the caption
    # ODF cross-references use text:reference-mark-start/end or text:bookmark-start/end

    # Add bookmark to the caption paragraph using low-level XML
    from lxml import etree
    TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

    # Find the caption paragraph and add bookmark
    body = doc.text
    for child in body.childNodes:
        if hasattr(child, 'getAttribute') and child.getAttribute('stylename') == 'TableCaption':
            # This is our caption paragraph - add reference mark
            elem = child
            # Add reference-mark-start at beginning
            ref_start = etree.SubElement(
                elem.qname[1] if hasattr(elem, 'qname') else elem,
                '{%s}reference-mark-start' % TEXT_NS
            )
            ref_start.set('{%s}name' % TEXT_NS, 'Table 2.1: Experimental Parameters')
            break

    # Save
    filepath = os.path.join(WORKDIR, 'Chapter2.odt')
    doc.save(filepath)
    print(f'Created: {filepath}')
    return filepath


def create_chapter2_odt_v2():
    """Create Chapter2.odt using raw XML for proper bookmark/reference-mark support."""
    import zipfile
    from io import BytesIO

    content_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    office:version="1.3">
  <office:automatic-styles>
    <style:style style:name="TableStyle" style:family="table">
      <style:table-properties style:width="6in" table:align="margins"/>
    </style:style>
    <style:style style:name="ColStyle" style:family="table-column">
      <style:table-column-properties style:column-width="2in"/>
    </style:style>
    <style:style style:name="CellStyle" style:family="table-cell">
      <style:table-cell-properties fo:padding="0.04in"
          fo:border="0.5pt solid #000000"/>
    </style:style>
    <style:style style:name="HeaderCellStyle" style:family="table-cell">
      <style:table-cell-properties fo:padding="0.04in"
          fo:border="0.5pt solid #000000"
          fo:background-color="#c0c0c0"/>
    </style:style>
    <style:style style:name="Bold" style:family="text">
      <style:text-properties fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="CaptionStyle" style:family="paragraph">
      <style:text-properties fo:font-size="10pt" fo:font-weight="bold"/>
      <style:paragraph-properties fo:margin-top="0.1in" fo:margin-bottom="0.1in"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:sequence-decls>
        <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
      </text:sequence-decls>

      <text:h text:outline-level="1">Chapter 2: Experimental Methodology</text:h>

      <text:p>This chapter describes the experimental methodology used in the study of thermodynamic properties of novel polymer composites. The research was conducted at the Advanced Materials Laboratory at Stanford University during the 2024-2025 academic year.</text:p>

      <text:p>The experimental design followed a factorial approach, varying temperature, pressure, and composition ratios across multiple trials. Each trial was repeated three times to ensure statistical significance of the results.</text:p>

      <text:h text:outline-level="2">2.1 Experimental Setup</text:h>

      <text:p>The experimental apparatus consisted of a high-precision calorimeter (TA Instruments Q2000), a hydraulic press capable of generating pressures up to 500 MPa, and a custom-designed mixing chamber with real-time viscosity monitoring.</text:p>

      <text:p>The following table summarizes the key experimental parameters used across all trial runs.</text:p>

      <text:p text:style-name="CaptionStyle"><text:bookmark-start text:name="Ref_Table_2_1"/>Table <text:sequence text:name="Table" text:formula="ooow:Table+1">2.1</text:sequence>: Experimental Parameters<text:bookmark-end text:name="Ref_Table_2_1"/></text:p>

      <table:table table:name="Table_2_1" table:style-name="TableStyle">
        <table:table-column table:style-name="ColStyle" table:number-columns-repeated="3"/>
        <table:table-row>
          <table:table-cell table:style-name="HeaderCellStyle"><text:p><text:span text:style-name="Bold">Parameter</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="HeaderCellStyle"><text:p><text:span text:style-name="Bold">Value</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="HeaderCellStyle"><text:p><text:span text:style-name="Bold">Unit</text:span></text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Temperature Range</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>25 - 350</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>°C</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Pressure</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>0.1 - 500</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>MPa</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Heating Rate</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>10</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>°C/min</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Sample Mass</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>15.0 ± 0.5</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>mg</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Atmosphere</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>N2 (99.999%)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>-</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Flow Rate</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>50</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>mL/min</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Polymer Concentration</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>5 - 40</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>wt%</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Mixing Speed</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>200 - 800</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>RPM</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Equilibration Time</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>30</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>min</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellStyle"><text:p>Number of Cycles</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>3</text:p></table:table-cell>
          <table:table-cell table:style-name="CellStyle"><text:p>per sample</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p>All measurements were performed using calibrated instruments with NIST-traceable standards. The uncertainty values reported represent the expanded uncertainty with a coverage factor of k=2, corresponding to a 95% confidence interval.</text:p>

      <text:p>The polymer samples were sourced from Sigma-Aldrich (purity greater than 99%) and used without further purification. Composite samples were prepared by melt-mixing in a Brabender twin-screw extruder at 280 degrees Celsius for 10 minutes.</text:p>

    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    office:version="1.3">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0in" fo:margin-bottom="0.08in"/>
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.3">
  <office:meta>
    <meta:generator>CUA-Gym/1.0</meta:generator>
  </office:meta>
</office:document-meta>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>
</manifest:manifest>'''

    filepath = os.path.join(WORKDIR, 'Chapter2.odt')
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text')
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    print(f'Created: {filepath}')
    return filepath


def create_chapter3_odt():
    """Create Chapter3.odt with placeholder [reference needed]."""
    import zipfile

    content_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:automatic-styles/>
  <office:body>
    <office:text>

      <text:h text:outline-level="1">Chapter 3: Results and Discussion</text:h>

      <text:p>This chapter presents the results obtained from the experimental procedures described in the previous chapter and provides a detailed discussion of their implications for polymer composite design.</text:p>

      <text:h text:outline-level="2">3.1 Thermal Analysis Results</text:h>

      <text:p>The differential scanning calorimetry (DSC) measurements revealed distinct thermal transitions for each composite formulation. The glass transition temperature (Tg) showed a systematic increase with filler content, consistent with restricted chain mobility at the polymer-filler interface.</text:p>

      <text:p>As shown in [reference needed], the parameters were carefully controlled to ensure reproducibility across all experimental runs. The temperature and pressure ranges were selected based on preliminary screening experiments conducted in the first phase of the study.</text:p>

      <text:p>The thermal decomposition onset temperature was determined using thermogravimetric analysis (TGA) at a heating rate matching the DSC conditions. All composites exhibited improved thermal stability compared to the neat polymer, with the 25 wt% formulation showing the highest decomposition onset at 412 degrees Celsius.</text:p>

      <text:h text:outline-level="2">3.2 Mechanical Properties</text:h>

      <text:p>Tensile testing was performed according to ASTM D638 standard procedures. The elastic modulus increased monotonically with filler loading, reaching a maximum of 4.8 GPa at 40 wt% concentration. However, the elongation at break decreased significantly above 30 wt%, indicating a transition from ductile to brittle failure mode.</text:p>

      <text:p>Dynamic mechanical analysis (DMA) confirmed the trends observed in static tensile testing. The storage modulus at room temperature showed excellent agreement with the static elastic modulus values, validating the consistency of the two measurement techniques.</text:p>

      <text:h text:outline-level="2">3.3 Microstructural Characterization</text:h>

      <text:p>Scanning electron microscopy (SEM) images of fracture surfaces revealed good dispersion of filler particles in the polymer matrix at concentrations up to 30 wt%. Above this threshold, particle agglomeration was observed, which correlates with the reduction in mechanical performance noted in Section 3.2.</text:p>

      <text:p>X-ray diffraction (XRD) analysis confirmed that the crystal structure of the filler was preserved during the melt-mixing process. No new crystalline phases were detected, suggesting that the polymer-filler interaction is primarily physical rather than chemical in nature.</text:p>

    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    office:version="1.3">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0in" fo:margin-bottom="0.08in"/>
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.3">
  <office:meta>
    <meta:generator>CUA-Gym/1.0</meta:generator>
  </office:meta>
</office:document-meta>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>
</manifest:manifest>'''

    filepath = os.path.join(WORKDIR, 'Chapter3.odt')
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text')
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    print(f'Created: {filepath}')
    return filepath


def create_master_odm():
    """Create Science_Report_Master.odm that links Chapter2.odt and Chapter3.odt."""
    import zipfile

    content_xml = '''<?xml version="1.0" encoding="UTF-8"?>
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

      <text:h text:outline-level="1">Science Report: Thermodynamic Properties of Novel Polymer Composites</text:h>

      <text:p>This master document compiles all chapters of the research report on the thermodynamic and mechanical properties of polymer-filler composite materials.</text:p>

      <text:section text:name="Chapter2Section" text:protected="false">
        <text:section-source xlink:href="Chapter2.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>

      <text:section text:name="Chapter3Section" text:protected="false">
        <text:section-source xlink:href="Chapter3.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>

    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    office:version="1.3">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0in" fo:margin-bottom="0.08in"/>
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.3">
  <office:meta>
    <meta:generator>CUA-Gym/1.0</meta:generator>
  </office:meta>
</office:document-meta>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text-master" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>
</manifest:manifest>'''

    filepath = os.path.join(WORKDIR, 'Science_Report_Master.odm')
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text-master')
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    print(f'Created: {filepath}')
    return filepath


def main():
    # Install odfpy if not present
    subprocess.run(['pip3', 'install', 'odfpy'], capture_output=True)

    # Create subdocuments
    create_chapter2_odt_v2()
    create_chapter3_odt()

    # Create master document
    create_master_odm()

    # Verify all files exist
    for fname in ['Chapter2.odt', 'Chapter3.odt', 'Science_Report_Master.odm']:
        fpath = os.path.join(WORKDIR, fname)
        assert os.path.exists(fpath), f'Missing: {fpath}'
        size = os.path.getsize(fpath)
        print(f'  {fname}: {size} bytes')

    # Open the master document in LibreOffice Writer for the GUI agent
    launch_gui(f'libreoffice --writer "{WORKDIR}/Science_Report_Master.odm"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with Science_Report_Master.odm on DISPLAY=:0')


main()
