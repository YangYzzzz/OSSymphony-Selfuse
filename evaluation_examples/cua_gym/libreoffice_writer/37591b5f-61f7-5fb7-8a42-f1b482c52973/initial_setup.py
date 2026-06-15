"""
Initial Setup: Create a LibreOffice Writer master document with 5 chapter subdocuments
and an Appendix_Data.odt file with wide tables (not yet inserted as subdocument).
Task ID: writer_rm_083
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

# ODF imports for creating .odt and .odm files
from odf.opendocument import OpenDocumentText
from odf.text import P, H, Section, SectionSource
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties, \
    TableCellProperties, PageLayout, PageLayoutProperties, MasterPage, SectionProperties
from odf.namespaces import XLINKNS, TEXTNS
from odf import text as odf_text

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_083'


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


def create_odt_chapter(filepath, title, paragraphs):
    """Create a simple .odt chapter document with portrait orientation."""
    doc = OpenDocumentText()

    # Create page layout (portrait)
    pl = PageLayout(name="PageLayout1")
    plp = PageLayoutProperties(
        pagewidth="8.5in",
        pageheight="11in",
        margintop="1in",
        marginbottom="1in",
        marginleft="1in",
        marginright="1in",
        printorientation="portrait"
    )
    pl.addElement(plp)
    doc.automaticstyles.addElement(pl)

    # Master page referencing the page layout
    mp = MasterPage(name="Standard", pagelayoutname="PageLayout1")
    doc.masterstyles.addElement(mp)

    # Heading style
    hs = Style(name="ChapterHeading", family="paragraph")
    hs.addElement(TextProperties(fontsize="18pt", fontweight="bold"))
    doc.styles.addElement(hs)

    # Body text style
    bs = Style(name="BodyText", family="paragraph")
    bs.addElement(TextProperties(fontsize="12pt"))
    bs.addElement(ParagraphProperties(marginbottom="0.15in"))
    doc.styles.addElement(bs)

    # Add heading
    h = H(outlinelevel=1, stylename="ChapterHeading")
    h.addText(title)
    doc.text.addElement(h)

    # Add paragraphs
    for para_text in paragraphs:
        p = P(stylename="BodyText")
        p.addText(para_text)
        doc.text.addElement(p)

    doc.save(filepath)
    print(f"Created: {filepath}")


def create_appendix_data(filepath):
    """Create Appendix_Data.odt with wide tables needing landscape orientation."""
    doc = OpenDocumentText()

    # Portrait page layout (initial state - NOT landscape yet)
    pl = PageLayout(name="PageLayout1")
    plp = PageLayoutProperties(
        pagewidth="8.5in",
        pageheight="11in",
        margintop="1in",
        marginbottom="1in",
        marginleft="1in",
        marginright="1in",
        printorientation="portrait"
    )
    pl.addElement(plp)
    doc.automaticstyles.addElement(pl)

    mp = MasterPage(name="Standard", pagelayoutname="PageLayout1")
    doc.masterstyles.addElement(mp)

    # Styles
    hs = Style(name="AppendixHeading", family="paragraph")
    hs.addElement(TextProperties(fontsize="16pt", fontweight="bold"))
    doc.styles.addElement(hs)

    bs = Style(name="BodyText", family="paragraph")
    bs.addElement(TextProperties(fontsize="11pt"))
    doc.styles.addElement(bs)

    # Table column style (wide)
    tcs = Style(name="WideCol", family="table-column")
    tcs.addElement(TableColumnProperties(columnwidth="1.2in"))
    doc.automaticstyles.addElement(tcs)

    # Table cell style
    tcells = Style(name="DataCell", family="table-cell")
    tcells.addElement(TableCellProperties(padding="0.05in", border="0.5pt solid #000000"))
    doc.automaticstyles.addElement(tcells)

    # Heading
    h = H(outlinelevel=1, stylename="AppendixHeading")
    h.addText("Appendix A: Quarterly Revenue Data by Region")
    doc.text.addElement(h)

    p = P(stylename="BodyText")
    p.addText("The following tables present comprehensive revenue data across all operating regions for fiscal year 2025. These wide-format tables require landscape orientation for optimal readability.")
    doc.text.addElement(p)

    # Table 1: Quarterly Revenue by Region (wide table)
    headers = ["Region", "Q1 Revenue", "Q1 Growth", "Q2 Revenue", "Q2 Growth",
               "Q3 Revenue", "Q3 Growth", "Q4 Revenue", "Q4 Growth", "Annual Total"]
    data_rows = [
        ["North America", "$12,450,000", "+8.2%", "$13,120,000", "+5.4%",
         "$14,890,000", "+13.5%", "$16,230,000", "+9.0%", "$56,690,000"],
        ["Europe", "$8,340,000", "+3.1%", "$9,120,000", "+9.4%",
         "$8,780,000", "-3.7%", "$10,450,000", "+19.0%", "$36,690,000"],
        ["Asia Pacific", "$6,780,000", "+15.3%", "$7,450,000", "+9.9%",
         "$8,120,000", "+9.0%", "$8,890,000", "+9.5%", "$31,240,000"],
        ["Latin America", "$3,210,000", "+6.7%", "$3,540,000", "+10.3%",
         "$3,890,000", "+9.9%", "$4,120,000", "+5.9%", "$14,760,000"],
        ["Middle East & Africa", "$2,180,000", "+12.1%", "$2,450,000", "+12.4%",
         "$2,670,000", "+9.0%", "$2,890,000", "+8.2%", "$10,190,000"],
    ]

    table1 = Table(name="RevenueByRegion")
    for _ in headers:
        tc = TableColumn(stylename="WideCol")
        table1.addElement(tc)

    # Header row
    hrow = TableRow()
    for htext in headers:
        cell = TableCell(stylename="DataCell")
        p = P()
        p.addText(htext)
        cell.addElement(p)
        hrow.addElement(cell)
    table1.addElement(hrow)

    # Data rows
    for row_data in data_rows:
        tr = TableRow()
        for val in row_data:
            cell = TableCell(stylename="DataCell")
            p = P()
            p.addText(val)
            cell.addElement(p)
            tr.addElement(cell)
        table1.addElement(tr)

    doc.text.addElement(table1)

    # Second paragraph
    p2 = P(stylename="BodyText")
    p2.addText("")
    doc.text.addElement(p2)

    p3 = P(stylename="BodyText")
    p3.addText("Table 2 below shows the detailed product category breakdown across all regions.")
    doc.text.addElement(p3)

    # Table 2: Product breakdown (also wide)
    headers2 = ["Product Line", "Units Sold", "Avg Price", "Total Revenue",
                "COGS", "Gross Margin", "Marketing Spend", "Net Contribution"]
    data_rows2 = [
        ["Enterprise Software", "2,340", "$45,200", "$105,768,000",
         "$31,730,400", "$74,037,600", "$12,450,000", "$61,587,600"],
        ["Cloud Services", "15,670", "$8,900", "$139,463,000",
         "$48,812,050", "$90,650,950", "$18,230,000", "$72,420,950"],
        ["Hardware Appliances", "890", "$125,000", "$111,250,000",
         "$66,750,000", "$44,500,000", "$8,900,000", "$35,600,000"],
        ["Professional Services", "4,520", "$12,300", "$55,596,000",
         "$33,357,600", "$22,238,400", "$4,120,000", "$18,118,400"],
        ["Training & Certification", "8,900", "$2,450", "$21,805,000",
         "$6,541,500", "$15,263,500", "$2,890,000", "$12,373,500"],
    ]

    table2 = Table(name="ProductBreakdown")
    for _ in headers2:
        tc = TableColumn(stylename="WideCol")
        table2.addElement(tc)

    hrow2 = TableRow()
    for htext in headers2:
        cell = TableCell(stylename="DataCell")
        p = P()
        p.addText(htext)
        cell.addElement(p)
        hrow2.addElement(cell)
    table2.addElement(hrow2)

    for row_data in data_rows2:
        tr = TableRow()
        for val in row_data:
            cell = TableCell(stylename="DataCell")
            p = P()
            p.addText(val)
            cell.addElement(p)
            tr.addElement(cell)
        table2.addElement(tr)

    doc.text.addElement(table2)

    doc.save(filepath)
    print(f"Created: {filepath}")


def create_master_document(filepath, subdoc_paths):
    """Create a master document (.odm) that references subdocuments.
    In ODF, a master document is essentially a .odt with text:section elements
    that link to external files. We save with .odm extension."""
    doc = OpenDocumentText()

    # Portrait page layout
    pl = PageLayout(name="PageLayout1")
    plp = PageLayoutProperties(
        pagewidth="8.5in",
        pageheight="11in",
        margintop="1in",
        marginbottom="1in",
        marginleft="1in",
        marginright="1in",
        printorientation="portrait"
    )
    pl.addElement(plp)
    doc.automaticstyles.addElement(pl)

    mp = MasterPage(name="Standard", pagelayoutname="PageLayout1")
    doc.masterstyles.addElement(mp)

    # Title style
    ts = Style(name="MasterTitle", family="paragraph")
    ts.addElement(TextProperties(fontsize="24pt", fontweight="bold"))
    ts.addElement(ParagraphProperties(textalign="center", marginbottom="0.3in"))
    doc.styles.addElement(ts)

    # Section style
    for i, subdoc_path in enumerate(subdoc_paths):
        sec_style = Style(name=f"SectionStyle{i+1}", family="section")
        sec_style.addElement(SectionProperties())
        doc.automaticstyles.addElement(sec_style)

    # Document title
    title = H(outlinelevel=1, stylename="MasterTitle")
    title.addText("Annual Strategic Report 2025")
    doc.text.addElement(title)

    subtitle = P()
    subtitle.addText("Consolidated Report — Global Operations Division")
    doc.text.addElement(subtitle)

    # Add sections linking to subdocuments
    for i, subdoc_path in enumerate(subdoc_paths):
        section_name = os.path.basename(subdoc_path).replace('.odt', '')
        sec = Section(
            name=section_name,
            stylename=f"SectionStyle{i+1}"
        )
        # Use text:section-source to link to subdocument (proper ODF way)
        src = SectionSource()
        src.setAttrNS(XLINKNS, 'href', subdoc_path)
        src.setAttrNS(XLINKNS, 'type', 'simple')
        sec.addElement(src)

        # Add a placeholder paragraph showing the link
        p = P()
        p.addText(f"[Subdocument: {os.path.basename(subdoc_path)}]")
        sec.addElement(p)

        doc.text.addElement(sec)

    doc.save(filepath)
    print(f"Created: {filepath}")


def create_initial():
    """Create all initial state files."""

    # Chapter 1: Executive Summary
    create_odt_chapter(
        f"{WORKDIR}/Chapter1_Executive_Summary.odt",
        "Chapter 1: Executive Summary",
        [
            "This report presents the consolidated findings from Global Operations Division's annual strategic review. The analysis covers financial performance, market positioning, operational efficiency, and strategic initiatives across all business units.",
            "Key highlights include a 12.3% year-over-year revenue growth, successful expansion into three new markets, and the completion of the digital transformation initiative that began in 2023.",
            "The board of directors has approved the recommended strategic priorities for the next fiscal year, including increased investment in artificial intelligence capabilities and sustainability programs.",
            "Revenue for the fiscal year reached $149.57 billion, surpassing targets by 4.2%. Operating margins improved to 23.8%, up from 21.5% in the previous year.",
            "Employee satisfaction scores reached an all-time high of 87%, driven by flexible work policies and enhanced professional development programs.",
        ]
    )

    # Chapter 2: Market Analysis
    create_odt_chapter(
        f"{WORKDIR}/Chapter2_Market_Analysis.odt",
        "Chapter 2: Market Analysis",
        [
            "The global technology market experienced significant shifts during fiscal year 2025, driven by accelerated adoption of cloud computing, artificial intelligence, and cybersecurity solutions.",
            "Our market share in the enterprise software segment grew from 18.4% to 21.7%, placing us in a strong second position behind the market leader. The cloud services division achieved the fastest growth at 34.2% year-over-year.",
            "Competitive analysis reveals that three key competitors have intensified their investment in AI-powered solutions, which aligns with our own strategic focus areas.",
            "Customer acquisition costs decreased by 15% due to improved marketing automation and brand recognition, while customer lifetime value increased by 22% through expanded service offerings.",
            "Emerging markets, particularly in Southeast Asia and Sub-Saharan Africa, showed the highest growth potential with compound annual growth rates exceeding 25%.",
        ]
    )

    # Chapter 3: Financial Performance
    create_odt_chapter(
        f"{WORKDIR}/Chapter3_Financial_Performance.odt",
        "Chapter 3: Financial Performance",
        [
            "Total revenue for fiscal year 2025 reached $149.57 billion, representing a 12.3% increase from the prior year. This growth was driven primarily by strong performance in cloud services and enterprise software segments.",
            "Operating expenses were carefully managed, resulting in an operating margin of 23.8%. Research and development spending increased to $18.2 billion, reflecting our commitment to innovation.",
            "Free cash flow generation remained robust at $42.3 billion, enabling continued investment in strategic acquisitions and shareholder returns through dividends and share buybacks.",
            "The balance sheet remains strong with total assets of $312.8 billion and a debt-to-equity ratio of 0.45, well within our target range of 0.3 to 0.6.",
            "Capital expenditures totaled $28.5 billion, primarily directed toward data center expansion, manufacturing facility upgrades, and technology infrastructure modernization.",
            "Foreign currency fluctuations had a net negative impact of approximately $2.1 billion on reported revenues, though hedging strategies mitigated an estimated additional $800 million in exposure.",
        ]
    )

    # Chapter 4: Strategic Initiatives
    create_odt_chapter(
        f"{WORKDIR}/Chapter4_Strategic_Initiatives.odt",
        "Chapter 4: Strategic Initiatives",
        [
            "The digital transformation program, launched in 2023, reached full deployment across all business units by Q3 2025. The initiative has delivered cumulative cost savings of $3.8 billion and improved operational efficiency by 28%.",
            "Our sustainability program achieved carbon neutrality in Scope 1 and Scope 2 emissions ahead of the 2026 target. The renewable energy portfolio now covers 94% of global operations.",
            "Strategic acquisitions completed during the year include DataVault Analytics ($4.2 billion) and SecureNet Technologies ($2.8 billion), strengthening our data analytics and cybersecurity capabilities.",
            "The workforce development initiative trained over 45,000 employees in AI and machine learning skills, positioning the company for the next wave of technology innovation.",
            "Partnership agreements with three leading universities established research collaboration programs focused on quantum computing, advanced materials, and biotechnology applications.",
        ]
    )

    # Chapter 5: Future Outlook
    create_odt_chapter(
        f"{WORKDIR}/Chapter5_Future_Outlook.odt",
        "Chapter 5: Future Outlook",
        [
            "Looking ahead to fiscal year 2026, we project revenue growth of 10-13%, driven by continued momentum in cloud services, the full-year contribution of recent acquisitions, and expansion into new market segments.",
            "Key strategic priorities include launching three new AI-powered product lines, expanding the partner ecosystem by 40%, and achieving full Scope 3 carbon neutrality by year-end.",
            "The board has approved a capital investment program of $32 billion for the coming year, with emphasis on next-generation data centers, semiconductor design capabilities, and quantum computing research.",
            "Risk factors under active monitoring include evolving regulatory landscapes in key markets, potential macroeconomic headwinds, and intensifying competition in the AI space.",
            "Management remains confident in the company's strategic positioning and expects continued value creation for shareholders through disciplined execution of our growth strategy.",
        ]
    )

    # Appendix_Data.odt — wide tables, portrait initially (needs landscape)
    create_appendix_data(f"{WORKDIR}/Appendix_Data.odt")

    # Create master document referencing the 5 chapters (NOT the appendix yet)
    subdoc_paths = [
        f"{WORKDIR}/Chapter1_Executive_Summary.odt",
        f"{WORKDIR}/Chapter2_Market_Analysis.odt",
        f"{WORKDIR}/Chapter3_Financial_Performance.odt",
        f"{WORKDIR}/Chapter4_Strategic_Initiatives.odt",
        f"{WORKDIR}/Chapter5_Future_Outlook.odt",
    ]
    create_master_document(f"{WORKDIR}/Report_Master.odm", subdoc_paths)

    # Open the master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{WORKDIR}/Report_Master.odm"', delay_sec=3.0)
    print("GUI_READY: launched LibreOffice Writer with Report_Master.odm on DISPLAY=:0")


create_initial()
