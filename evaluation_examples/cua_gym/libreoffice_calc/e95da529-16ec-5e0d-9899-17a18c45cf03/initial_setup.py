"""
Initial Setup: Inventory PDF and Reorder Levels ODS
Task ID: pdf_cross_045
Domain: libreoffice_calc (cross-domain with PDF)

Creates:
  - ~/Documents/inventory_count.pdf: 2-page PDF with 30 inventory items and current stock quantities
  - ~/Documents/reorder_levels.ods: Calc file with Item Code, Item Name, Reorder Level for 30 items
    (NO Current Stock or Reorder Needed column — agent must add these from PDF data)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_045'

# -----------------------------------------------------------------------
# 30 inventory items: (item_code, item_name, reorder_level, current_stock)
# 12 items will have current_stock < reorder_level
# -----------------------------------------------------------------------
ITEMS = [
    ('ITM-001', 'Wireless Keyboard',       50,  35),   # BELOW (needs reorder)
    ('ITM-002', 'USB-C Hub',               30,  42),
    ('ITM-003', 'Monitor Stand',           20,  18),   # BELOW
    ('ITM-004', 'Mechanical Keyboard',     40,  55),
    ('ITM-005', 'Laptop Cooling Pad',      25,  12),   # BELOW
    ('ITM-006', 'HDMI Cable 2m',           100, 130),
    ('ITM-007', 'Wireless Mouse',          60,  45),   # BELOW
    ('ITM-008', 'Desk Lamp LED',           35,  50),
    ('ITM-009', 'Monitor 24inch',          15,  8),    # BELOW
    ('ITM-010', 'Ergonomic Chair',         10,  14),
    ('ITM-011', 'Webcam 1080p',            30,  22),   # BELOW
    ('ITM-012', 'USB Flash Drive 64GB',    80,  95),
    ('ITM-013', 'Laptop Backpack',         25,  30),
    ('ITM-014', 'Standing Desk',           8,   5),    # BELOW
    ('ITM-015', 'Cable Organizer Set',     50,  60),
    ('ITM-016', 'Noise Cancelling Headph', 20,  11),   # BELOW
    ('ITM-017', 'Portable SSD 1TB',        15,  20),
    ('ITM-018', 'Smart Power Strip',       40,  28),   # BELOW
    ('ITM-019', 'Screen Cleaning Kit',     70,  85),
    ('ITM-020', 'Wrist Rest Pad',          45,  33),   # BELOW
    ('ITM-021', 'Document Scanner',        10,  13),
    ('ITM-022', 'Ethernet Cable 5m',       60,  75),
    ('ITM-023', 'Laptop Lock',             30,  38),
    ('ITM-024', 'Mouse Pad XL',            40,  27),   # BELOW
    ('ITM-025', 'USB-A Hub 4-Port',        55,  70),
    ('ITM-026', 'Privacy Screen Filter',   20,  25),
    ('ITM-027', 'Trackball Mouse',         15,  9),    # BELOW
    ('ITM-028', 'Mini Projector',          8,   10),
    ('ITM-029', 'Keyboard Wrist Rest',     35,  42),
    ('ITM-030', 'Laptop Docking Station',  12,  16),
]

# Verify 12 items below reorder level
below = [(code, name, rl, cs) for (code, name, rl, cs) in ITEMS if cs < rl]
assert len(below) == 12, f"Expected 12 below-reorder items, got {len(below)}"


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


def create_inventory_pdf():
    """Create a 2-page PDF listing 30 items with current stock quantities."""
    import pymupdf

    pdf_path = f'{WORKDIR}/inventory_count.pdf'
    doc = pymupdf.open()

    # Page 1: items 1-15
    def add_page(doc, items_slice, page_num):
        page = doc.new_page(width=595, height=842)

        # Title
        page.insert_text(pymupdf.Point(72, 55),
                         "INVENTORY COUNT REPORT",
                         fontsize=18, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(72, 78),
                         f"Date: 2025-06-15   Page {page_num} of 2   Warehouse: Main Distribution Center",
                         fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

        # Draw header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 90), pymupdf.Point(523, 90))
        shape.finish(color=(0, 0, 0), width=1)
        shape.commit()

        # Column headers
        headers_y = 108
        page.insert_text(pymupdf.Point(72,  headers_y), "Item Code", fontsize=10, fontname="hebo")
        page.insert_text(pymupdf.Point(155, headers_y), "Item Name",  fontsize=10, fontname="hebo")
        page.insert_text(pymupdf.Point(370, headers_y), "Unit",       fontsize=10, fontname="hebo")
        page.insert_text(pymupdf.Point(430, headers_y), "Current Stock", fontsize=10, fontname="hebo")

        # Underline headers
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 114), pymupdf.Point(523, 114))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()

        # Rows
        row_y = 132
        for idx, (code, name, rl, stock) in enumerate(items_slice):
            bg = (0.95, 0.95, 0.95) if idx % 2 == 0 else (1, 1, 1)
            # Row background
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(72, row_y - 12, 523, row_y + 4))
            shape.finish(fill=bg, color=None, width=0)
            shape.commit()

            page.insert_text(pymupdf.Point(72,  row_y), code,       fontsize=10, fontname="helv")
            page.insert_text(pymupdf.Point(155, row_y), name,       fontsize=10, fontname="helv")
            page.insert_text(pymupdf.Point(370, row_y), "pcs",      fontsize=10, fontname="helv")
            page.insert_text(pymupdf.Point(455, row_y), str(stock), fontsize=10, fontname="helv")
            row_y += 20

        # Footer
        page.insert_text(pymupdf.Point(72, 810),
                         "Counted by: Warehouse Team  |  Verified by: Inventory Manager",
                         fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    add_page(doc, ITEMS[:15], 1)
    add_page(doc, ITEMS[15:], 2)

    doc.save(pdf_path)
    doc.close()
    print(f'PDF created: {pdf_path}')


def create_reorder_ods():
    """Create an ODS spreadsheet with Item Code, Item Name, Reorder Level (NO Current Stock column)."""
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableCellProperties, TableColumnProperties
    from odf.text import P
    from odf.table import Table, TableRow, TableCell, TableColumn

    ods_path = f'{WORKDIR}/reorder_levels.ods'
    doc_ods = OpenDocumentSpreadsheet()

    # --- Define styles ---
    # Header style
    header_style = Style(name="header_style", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold"))
    header_style.addElement(TableCellProperties(backgroundcolor="#4472C4"))
    doc_ods.styles.addElement(header_style)

    # Data style
    data_style = Style(name="data_style", family="table-cell")
    doc_ods.styles.addElement(data_style)

    # Column widths
    col_style_code  = Style(name="col_code",  family="table-column")
    col_style_code.addElement(TableColumnProperties(columnwidth="3cm"))
    doc_ods.automaticstyles.addElement(col_style_code)

    col_style_name  = Style(name="col_name",  family="table-column")
    col_style_name.addElement(TableColumnProperties(columnwidth="6cm"))
    doc_ods.automaticstyles.addElement(col_style_name)

    col_style_level = Style(name="col_level", family="table-column")
    col_style_level.addElement(TableColumnProperties(columnwidth="3.5cm"))
    doc_ods.automaticstyles.addElement(col_style_level)

    # --- Create sheet ---
    sheet = Table(name="Reorder Levels")
    sheet.addElement(TableColumn(stylename=col_style_code))
    sheet.addElement(TableColumn(stylename=col_style_name))
    sheet.addElement(TableColumn(stylename=col_style_level))

    def make_cell(value, style=None):
        tc = TableCell()
        if style:
            tc.setAttribute("stylename", style)
        tc.addElement(P(text=str(value)))
        return tc

    # Header row
    hrow = TableRow()
    hrow.addElement(make_cell("Item Code",    "header_style"))
    hrow.addElement(make_cell("Item Name",    "header_style"))
    hrow.addElement(make_cell("Reorder Level","header_style"))
    sheet.addElement(hrow)

    # Data rows (NO Current Stock, NO Reorder Needed)
    for (code, name, rl, stock) in ITEMS:
        drow = TableRow()
        drow.addElement(make_cell(code,    "data_style"))
        drow.addElement(make_cell(name,    "data_style"))
        drow.addElement(make_cell(str(rl), "data_style"))
        sheet.addElement(drow)

    doc_ods.spreadsheet.addElement(sheet)
    doc_ods.save(ods_path)
    print(f'ODS created: {ods_path}')


def main():
    os.makedirs(WORKDIR, exist_ok=True)

    create_inventory_pdf()
    create_reorder_ods()

    # GUI: open the ODS in LibreOffice Calc (agent works primarily in Calc)
    ods_path = f'{WORKDIR}/reorder_levels.ods'
    launch_gui(f'libreoffice --calc "{ods_path}"', delay_sec=3.0)
    # Also open the PDF so agent can view it
    pdf_path = f'{WORKDIR}/inventory_count.pdf'
    launch_gui(f'evince "{pdf_path}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc and Evince with DISPLAY=:0')


main()
