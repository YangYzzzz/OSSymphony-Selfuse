"""
Initial Setup: Vendor Billing Audit - 7 monthly PDF invoices + empty audit_log template
Task ID: osworld_multi_apps_doc_pdf_calc_010
Domain: multi_apps (libreoffice_calc, libreoffice_writer, pdf)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_pdf_calc_010'
DESKTOP = f'{WORKDIR}/Desktop'
DOCUMENTS = f'{WORKDIR}/Documents'
INVOICES_DIR = f'{DESKTOP}/vendor_invoices'

# Invoice data: (month_label, invoice_date, units, unit_price, invoiced_subtotal, tax_rate_used, invoiced_tax, invoiced_total, has_error)
# Contractual formula: Total = Units x Unit_Price x 1.08 (8% tax)
# 3 invoices have errors: Feb (tax 10%), May (wrong units=144 instead of 130), Jun (tax 9%)
INVOICES = [
    # month, inv_date, true_units, unit_price, inv_units, inv_subtotal, inv_tax_rate, inv_tax, inv_total, error_desc
    ("January 2025",  "2025-01-15", 100, 45.00, 100, 4500.00, 0.08, 360.00, 4860.00, None),
    ("February 2025", "2025-02-14", 120, 45.00, 120, 5400.00, 0.10, 540.00, 5940.00, "Tax rate applied as 10% instead of contracted 8%"),
    ("March 2025",    "2025-03-18", 95,  45.00, 95,  4275.00, 0.08, 342.00, 4617.00, None),
    ("April 2025",    "2025-04-16", 110, 45.00, 110, 4950.00, 0.08, 396.00, 5346.00, None),
    ("May 2025",      "2025-05-14", 130, 45.00, 144, 6480.00, 0.08, 518.40, 6998.40, "Unit count invoiced as 144 instead of actual 130"),
    ("June 2025",     "2025-06-13", 85,  45.00, 85,  3825.00, 0.09, 344.25, 4169.25, "Tax rate applied as 9% instead of contracted 8%"),
    ("July 2025",     "2025-07-16", 115, 45.00, 115, 5175.00, 0.08, 414.00, 5589.00, None),
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


def create_pdf_invoice(filepath, month_label, inv_date, units, unit_price, subtotal, tax_rate, tax_amount, total, error_desc):
    """Create a PDF invoice using fpdf2."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    # Header
    pdf.set_font("Helvetica", "B", size=18)
    pdf.cell(0, 12, "TECHSUPPLY SOLUTIONS LTD.", ln=True, align="C")
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, "123 Industrial Park Ave, Singapore 456789", ln=True, align="C")
    pdf.cell(0, 8, "Tel: +65 6234 5678  |  billing@techsupply.sg", ln=True, align="C")
    pdf.ln(6)

    # Invoice title
    pdf.set_font("Helvetica", "B", size=14)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"TAX INVOICE - {month_label.upper()}", ln=True, align="C", fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Invoice details
    invoice_num = f"INV-2025-{['JAN','FEB','MAR','APR','MAY','JUN','JUL'][['January 2025','February 2025','March 2025','April 2025','May 2025','June 2025','July 2025'].index(month_label)]}"
    pdf.set_font("Helvetica", size=11)

    # Two-column info area
    col_w = 85
    pdf.set_font("Helvetica", "B", size=10)
    pdf.cell(col_w, 8, "BILL TO:", ln=False)
    pdf.cell(col_w, 8, "INVOICE DETAILS:", ln=True)

    pdf.set_font("Helvetica", size=10)
    pdf.cell(col_w, 7, "GlobalCorp International Pte Ltd", ln=False)
    pdf.cell(col_w, 7, f"Invoice Number: {invoice_num}", ln=True)
    pdf.cell(col_w, 7, "456 Corporate Tower, Level 12", ln=False)
    pdf.cell(col_w, 7, f"Invoice Date: {inv_date}", ln=True)
    pdf.cell(col_w, 7, "Singapore 789012", ln=False)
    pdf.cell(col_w, 7, "Payment Terms: Net 30 days", ln=True)
    pdf.ln(8)

    # Service description table header
    pdf.set_font("Helvetica", "B", size=10)
    pdf.set_fill_color(220, 220, 220)
    col_desc = 90
    col_qty = 25
    col_price = 35
    col_amount = 30

    pdf.cell(col_desc, 8, "Description", border=1, align="C", fill=True)
    pdf.cell(col_qty, 8, "Units", border=1, align="C", fill=True)
    pdf.cell(col_price, 8, "Unit Price (SGD)", border=1, align="C", fill=True)
    pdf.cell(col_amount, 8, "Amount (SGD)", border=1, align="C", fill=True)
    pdf.ln()

    # Service row
    pdf.set_font("Helvetica", size=10)
    pdf.cell(col_desc, 8, "IT Infrastructure Support Services", border=1)
    pdf.cell(col_qty, 8, str(units), border=1, align="C")
    pdf.cell(col_price, 8, f"{unit_price:.2f}", border=1, align="R")
    pdf.cell(col_amount, 8, f"{subtotal:.2f}", border=1, align="R")
    pdf.ln()

    pdf.ln(4)

    # Totals section (right-aligned)
    total_x = 120
    label_w = 45
    value_w = 25

    pdf.set_x(total_x)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(label_w, 8, "Subtotal:", align="R")
    pdf.cell(value_w, 8, f"SGD {subtotal:.2f}", align="R", border="B")
    pdf.ln()

    pdf.set_x(total_x)
    tax_pct = int(tax_rate * 100)
    pdf.cell(label_w, 8, f"Tax ({tax_pct}% GST):", align="R")
    pdf.cell(value_w, 8, f"SGD {tax_amount:.2f}", align="R", border="B")
    pdf.ln()

    pdf.set_x(total_x)
    pdf.set_font("Helvetica", "B", size=11)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(label_w, 9, "TOTAL:", align="R", fill=True)
    pdf.cell(value_w, 9, f"SGD {total:.2f}", align="R", fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln()

    pdf.ln(12)

    # Invoice line items breakdown
    pdf.set_font("Helvetica", "B", size=10)
    pdf.cell(0, 8, "Pricing Breakdown:", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 7, f"  Invoice_Date: {inv_date}", ln=True)
    pdf.cell(0, 7, f"  Units: {units}", ln=True)
    pdf.cell(0, 7, f"  Unit_Price: SGD {unit_price:.2f}", ln=True)
    pdf.cell(0, 7, f"  Subtotal: SGD {subtotal:.2f}  (Units x Unit_Price)", ln=True)
    pdf.cell(0, 7, f"  Tax_Rate: {tax_pct}%", ln=True)
    pdf.cell(0, 7, f"  Tax_Amount: SGD {tax_amount:.2f}", ln=True)
    pdf.cell(0, 7, f"  Total: SGD {total:.2f}", ln=True)

    pdf.ln(10)

    # Footer
    pdf.set_font("Helvetica", "I", size=9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "Payment by bank transfer to: TechSupply Solutions Ltd | DBS Bank | A/C: 023-456789-0", ln=True, align="C")
    pdf.cell(0, 7, "This is a computer-generated invoice. No signature required.", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    pdf.output(filepath)


def create_audit_log_template(filepath):
    """Create an empty audit_log.ods with just the column headers."""
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableCellProperties, TableColumnProperties
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf.text import P

    doc = OpenDocumentSpreadsheet()

    # Define header style
    header_style = Style(name="HeaderStyle", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold"))
    header_style.addElement(TableCellProperties(backgroundcolor="#DCE6F1"))
    doc.automaticstyles.addElement(header_style)

    # Normal cell style
    normal_style = Style(name="NormalCell", family="table-cell")
    doc.automaticstyles.addElement(normal_style)

    # Column style for wider columns
    wide_col_style = Style(name="WideCol", family="table-column")
    wide_col_style.addElement(TableColumnProperties(columnwidth="3.5cm"))
    doc.automaticstyles.addElement(wide_col_style)

    medium_col_style = Style(name="MedCol", family="table-column")
    medium_col_style.addElement(TableColumnProperties(columnwidth="2.8cm"))
    doc.automaticstyles.addElement(medium_col_style)

    table = Table(name="Audit Log")

    # Add column definitions
    headers = [
        "Invoice_Month", "Units", "Unit_Price",
        "Expected_Subtotal", "Invoiced_Subtotal",
        "Expected_Tax", "Invoiced_Tax",
        "Expected_Total", "Invoiced_Total",
        "Discrepancy_Amount", "Status"
    ]

    for _ in headers:
        table.addElement(TableColumn(stylename=medium_col_style))

    # Header row
    header_row = TableRow()
    for h in headers:
        tc = TableCell(valuetype="string", stylename=header_style)
        tc.addElement(P(text=h))
        header_row.addElement(tc)
    table.addElement(header_row)

    # 7 empty rows for agent to fill (Jan-Jul 2025)
    month_labels = [
        "January 2025", "February 2025", "March 2025", "April 2025",
        "May 2025", "June 2025", "July 2025"
    ]
    for month in month_labels:
        row = TableRow()
        # First cell: month name
        tc = TableCell(valuetype="string", stylename=normal_style)
        tc.addElement(P(text=month))
        row.addElement(tc)
        # Remaining cells empty
        for _ in range(len(headers) - 1):
            empty_tc = TableCell(stylename=normal_style)
            row.addElement(empty_tc)
        table.addElement(row)

    # Empty summary row
    summary_row = TableRow()
    tc = TableCell(valuetype="string", stylename=normal_style)
    tc.addElement(P(text="TOTAL"))
    summary_row.addElement(tc)
    for _ in range(len(headers) - 1):
        empty_tc = TableCell(stylename=normal_style)
        summary_row.addElement(empty_tc)
    table.addElement(summary_row)

    doc.spreadsheet.addElement(table)
    doc.save(filepath)


def create_initial():
    # Create directories
    os.makedirs(INVOICES_DIR, exist_ok=True)
    os.makedirs(DOCUMENTS, exist_ok=True)

    # Generate 7 PDF invoices
    month_codes = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL']
    for i, (month_label, inv_date, true_units, unit_price,
            inv_units, inv_subtotal, inv_tax_rate, inv_tax, inv_total, error_desc) in enumerate(INVOICES):
        code = month_codes[i]
        filename = f"Invoice_2025_{code}_TechSupply.pdf"
        filepath = os.path.join(INVOICES_DIR, filename)
        create_pdf_invoice(
            filepath, month_label, inv_date,
            inv_units, unit_price, inv_subtotal,
            inv_tax_rate, inv_tax, inv_total,
            error_desc
        )
        print(f"Created: {filepath}")

    # Create empty audit_log.ods template
    audit_log_path = f'{DESKTOP}/audit_log.ods'
    create_audit_log_template(audit_log_path)
    print(f"Created audit log template: {audit_log_path}")

    # GUI-ready startup: open vendor_invoices folder in Files and audit_log in Calc
    launch_gui(f'nautilus "{INVOICES_DIR}"', delay_sec=2.0)
    launch_gui(f'libreoffice --calc "{audit_log_path}"', delay_sec=3.0)
    print('GUI_READY: launched Nautilus file manager and LibreOffice Calc with DISPLAY=:0')


create_initial()
