"""
Initial Setup: Invoice automation template with bookmarks and JSON config
Task ID: writer_gf4_047
Domain: libreoffice_writer
"""

import json
import os
import shlex
import subprocess
import time
import zipfile
import tempfile
import shutil
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_gf4_047'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'
JSON_CONFIG = f'{WORKDIR}/invoice_config.json'


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


def create_invoice_config():
    """Create the JSON configuration file with invoice data."""
    config = {
        "InvoiceNumber": "INV-2025-0384",
        "ClientName": "Greenleaf Consulting Partners",
        "ClientAddress": "742 Innovation Boulevard, Suite 300, Portland, OR 97205",
        "LineItems": [
            {"description": "Website Redesign - UX Research & Wireframing", "amount": 3200.00},
            {"description": "Frontend Development (React Components)", "amount": 5800.00},
            {"description": "Backend API Integration & Testing", "amount": 4500.00},
            {"description": "Performance Optimization & CDN Setup", "amount": 1750.00},
            {"description": "Documentation & Knowledge Transfer Sessions", "amount": 950.00}
        ],
        "TaxRate": 0.085,
        "PaymentTerms": "Net 30",
        "Notes": "Thank you for your continued partnership. Payment via wire transfer preferred."
    }
    with open(JSON_CONFIG, 'w') as f:
        json.dump(config, f, indent=2)
    print(f'Invoice config created: {JSON_CONFIG}')


def create_odt_template():
    """Create an ODT invoice template with text bookmarks for macro filling."""
    # We'll build the ODT using odfpy
    from odf.opendocument import OpenDocumentText
    from odf.text import P, Span, BookmarkStart, BookmarkEnd, H
    from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties, TableCellProperties, TableProperties
    from odf.table import Table, TableColumn, TableRow, TableCell

    doc = OpenDocumentText()

    # --- Styles ---
    # Title style
    title_style = Style(name="InvoiceTitle", family="paragraph")
    title_style.addElement(ParagraphProperties(textalign="center", marginbottom="0.3in"))
    title_style.addElement(TextProperties(fontsize="24pt", fontweight="bold", color="#1a3c6e"))
    doc.automaticstyles.addElement(title_style)

    # Subtitle style
    sub_style = Style(name="SubInfo", family="paragraph")
    sub_style.addElement(ParagraphProperties(textalign="center", marginbottom="0.1in"))
    sub_style.addElement(TextProperties(fontsize="11pt", color="#555555"))
    doc.automaticstyles.addElement(sub_style)

    # Section header style
    sec_style = Style(name="SectionHead", family="paragraph")
    sec_style.addElement(ParagraphProperties(marginbottom="0.1in", margintop="0.25in"))
    sec_style.addElement(TextProperties(fontsize="13pt", fontweight="bold", color="#1a3c6e"))
    doc.automaticstyles.addElement(sec_style)

    # Normal text style
    norm_style = Style(name="NormalField", family="paragraph")
    norm_style.addElement(ParagraphProperties(marginbottom="0.08in"))
    norm_style.addElement(TextProperties(fontsize="11pt"))
    doc.automaticstyles.addElement(norm_style)

    # Bookmark placeholder style (gray italic)
    bm_text_style = Style(name="BookmarkPlaceholder", family="text")
    bm_text_style.addElement(TextProperties(fontsize="11pt", fontstyle="italic", color="#999999"))
    doc.automaticstyles.addElement(bm_text_style)

    # Table styles
    table_style = Style(name="InvoiceTable", family="table")
    table_style.addElement(TableProperties(width="6.5in", align="margins"))
    doc.automaticstyles.addElement(table_style)

    col_desc_style = Style(name="ColDesc", family="table-column")
    col_desc_style.addElement(TableColumnProperties(columnwidth="4.5in"))
    doc.automaticstyles.addElement(col_desc_style)

    col_amt_style = Style(name="ColAmt", family="table-column")
    col_amt_style.addElement(TableColumnProperties(columnwidth="2.0in"))
    doc.automaticstyles.addElement(col_amt_style)

    header_cell_style = Style(name="HeaderCell", family="table-cell")
    header_cell_style.addElement(TableCellProperties(
        padding="0.05in", backgroundcolor="#1a3c6e",
        borderbottom="1pt solid #1a3c6e"))
    doc.automaticstyles.addElement(header_cell_style)

    data_cell_style = Style(name="DataCell", family="table-cell")
    data_cell_style.addElement(TableCellProperties(
        padding="0.05in",
        borderbottom="0.5pt solid #cccccc"))
    doc.automaticstyles.addElement(data_cell_style)

    header_text_style = Style(name="HeaderText", family="text")
    header_text_style.addElement(TextProperties(fontsize="11pt", fontweight="bold", color="#ffffff"))
    doc.automaticstyles.addElement(header_text_style)

    # Bold label style
    label_style = Style(name="FieldLabel", family="text")
    label_style.addElement(TextProperties(fontsize="11pt", fontweight="bold"))
    doc.automaticstyles.addElement(label_style)

    # Right-align style for amounts
    right_style = Style(name="RightAlign", family="paragraph")
    right_style.addElement(ParagraphProperties(textalign="end"))
    right_style.addElement(TextProperties(fontsize="11pt"))
    doc.automaticstyles.addElement(right_style)

    # Totals bold style
    totals_bold_style = Style(name="TotalsBold", family="text")
    totals_bold_style.addElement(TextProperties(fontsize="12pt", fontweight="bold", color="#1a3c6e"))
    doc.automaticstyles.addElement(totals_bold_style)

    def add_bookmark_field(parent_element, bookmark_name, placeholder_text):
        """Add a bookmark with placeholder text to a paragraph."""
        bm_start = BookmarkStart(name=bookmark_name)
        parent_element.addElement(bm_start)
        span = Span(stylename="BookmarkPlaceholder")
        span.addText(placeholder_text)
        parent_element.addElement(span)
        bm_end = BookmarkEnd(name=bookmark_name)
        parent_element.addElement(bm_end)

    # === Document Content ===

    # Company header
    company_p = P(stylename="InvoiceTitle")
    company_p.addText("INVOICE")
    doc.text.addElement(company_p)

    # Freelancer info
    info_p = P(stylename="SubInfo")
    info_p.addText("Elena Vasquez | Freelance Software Developer")
    doc.text.addElement(info_p)

    info_p2 = P(stylename="SubInfo")
    info_p2.addText("elena.vasquez@devstudio.io | (503) 555-0147")
    doc.text.addElement(info_p2)

    info_p3 = P(stylename="SubInfo")
    info_p3.addText("1024 Cedar Lane, Portland, OR 97201")
    doc.text.addElement(info_p3)

    # Separator
    sep_p = P(stylename="NormalField")
    sep_p.addText("─" * 60)
    doc.text.addElement(sep_p)

    # Invoice details section
    sec1 = P(stylename="SectionHead")
    sec1.addText("Invoice Details")
    doc.text.addElement(sec1)

    # Invoice Number field
    inv_num_p = P(stylename="NormalField")
    label_span = Span(stylename="FieldLabel")
    label_span.addText("Invoice Number: ")
    inv_num_p.addElement(label_span)
    add_bookmark_field(inv_num_p, "InvoiceNumber", "[invoice number]")
    doc.text.addElement(inv_num_p)

    # Invoice Date field
    inv_date_p = P(stylename="NormalField")
    label_span2 = Span(stylename="FieldLabel")
    label_span2.addText("Invoice Date: ")
    inv_date_p.addElement(label_span2)
    add_bookmark_field(inv_date_p, "InvoiceDate", "[date]")
    doc.text.addElement(inv_date_p)

    # Client section
    sec2 = P(stylename="SectionHead")
    sec2.addText("Bill To")
    doc.text.addElement(sec2)

    client_p = P(stylename="NormalField")
    label_span3 = Span(stylename="FieldLabel")
    label_span3.addText("Client: ")
    client_p.addElement(label_span3)
    add_bookmark_field(client_p, "ClientName", "[client name]")
    doc.text.addElement(client_p)

    # Line Items section
    sec3 = P(stylename="SectionHead")
    sec3.addText("Line Items")
    doc.text.addElement(sec3)

    # Line items table
    table = Table(name="LineItems", stylename="InvoiceTable")
    table.addElement(TableColumn(stylename="ColDesc"))
    table.addElement(TableColumn(stylename="ColAmt"))

    # Table header row
    header_row = TableRow()
    hc1 = TableCell(stylename="HeaderCell")
    hp1 = P()
    hs1 = Span(stylename="HeaderText")
    hs1.addText("Description")
    hp1.addElement(hs1)
    hc1.addElement(hp1)
    header_row.addElement(hc1)

    hc2 = TableCell(stylename="HeaderCell")
    hp2 = P(stylename="RightAlign")
    hs2 = Span(stylename="HeaderText")
    hs2.addText("Amount")
    hp2.addElement(hs2)
    hc2.addElement(hp2)
    header_row.addElement(hc2)
    table.addElement(header_row)

    # Line item rows with bookmarks (1-5)
    for i in range(1, 6):
        row = TableRow()
        # Description cell
        desc_cell = TableCell(stylename="DataCell")
        desc_p = P(stylename="NormalField")
        add_bookmark_field(desc_p, f"LineItem{i}Desc", f"[line item {i} description]")
        desc_cell.addElement(desc_p)
        row.addElement(desc_cell)

        # Amount cell
        amt_cell = TableCell(stylename="DataCell")
        amt_p = P(stylename="RightAlign")
        add_bookmark_field(amt_p, f"LineItem{i}Amt", f"[amount]")
        amt_cell.addElement(amt_p)
        row.addElement(amt_cell)

        table.addElement(row)

    doc.text.addElement(table)

    # Separator
    sep_p2 = P(stylename="NormalField")
    sep_p2.addText("")
    doc.text.addElement(sep_p2)

    # Totals section
    sec4 = P(stylename="SectionHead")
    sec4.addText("Summary")
    doc.text.addElement(sec4)

    # SubTotal
    sub_p = P(stylename="NormalField")
    sub_label = Span(stylename="FieldLabel")
    sub_label.addText("Subtotal: ")
    sub_p.addElement(sub_label)
    add_bookmark_field(sub_p, "SubTotal", "[subtotal]")
    doc.text.addElement(sub_p)

    # Tax Rate
    tax_rate_p = P(stylename="NormalField")
    tax_rate_label = Span(stylename="FieldLabel")
    tax_rate_label.addText("Tax Rate: ")
    tax_rate_p.addElement(tax_rate_label)
    add_bookmark_field(tax_rate_p, "TaxRate", "[tax rate]")
    doc.text.addElement(tax_rate_p)

    # Tax Amount
    tax_amt_p = P(stylename="NormalField")
    tax_amt_label = Span(stylename="FieldLabel")
    tax_amt_label.addText("Tax Amount: ")
    tax_amt_p.addElement(tax_amt_label)
    add_bookmark_field(tax_amt_p, "TaxAmount", "[tax amount]")
    doc.text.addElement(tax_amt_p)

    # Grand Total
    grand_p = P(stylename="NormalField")
    grand_label = Span(stylename="TotalsBold")
    grand_label.addText("Grand Total: ")
    grand_p.addElement(grand_label)
    add_bookmark_field(grand_p, "GrandTotal", "[grand total]")
    doc.text.addElement(grand_p)

    # Separator
    sep_p3 = P(stylename="NormalField")
    sep_p3.addText("─" * 60)
    doc.text.addElement(sep_p3)

    # Payment terms
    terms_p = P(stylename="NormalField")
    terms_label = Span(stylename="FieldLabel")
    terms_label.addText("Payment Terms: ")
    terms_p.addElement(terms_label)
    terms_p.addText("Net 30")
    doc.text.addElement(terms_p)

    # Notes
    notes_p = P(stylename="NormalField")
    notes_label = Span(stylename="FieldLabel")
    notes_label.addText("Notes: ")
    notes_p.addElement(notes_label)
    notes_p.addText("Thank you for your business.")
    doc.text.addElement(notes_p)

    doc.save(OUTPUT)
    print(f'Invoice template created: {OUTPUT}')


def create_initial():
    create_invoice_config()
    create_odt_template()

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
