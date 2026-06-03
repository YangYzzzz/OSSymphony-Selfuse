"""
Initial Setup: Build a comprehensive product catalog document from a large Calc dataset.
Task ID: osworld_multi_apps_doc_calc_to_writer_011
Domain: libreoffice_writer (multi-app: LibreOffice Calc source file)

Creates:
  - /home/user/Desktop/products.ods  (source data file with 40 products across 5 categories)
  - Launches LibreOffice Calc with products.ods open
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_calc_to_writer_011'
ODS_FILE = f'{DESKTOP}/products.ods'


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
    import subprocess as sp
    # Install odfpy if not present
    sp.run(['pip3', 'install', 'odfpy', '-q'], capture_output=True)

    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    from odf.style import Style, TableCellProperties, TextProperties
    from odf.number import Number

    os.makedirs(DESKTOP, exist_ok=True)
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = OpenDocumentSpreadsheet()

    # Define header style
    header_style = Style(name="HeaderStyle", family="table-cell")
    header_style.addElement(TableCellProperties(backgroundcolor="#4472C4"))
    header_style.addElement(TextProperties(fontweight="bold", color="#FFFFFF"))
    doc.styles.addElement(header_style)

    sheet = Table(name="Products")
    doc.spreadsheet.addElement(sheet)

    # Define columns: Product_ID, Name, Category, Description, Unit_Price, Stock_Count
    headers = ['Product_ID', 'Name', 'Category', 'Description', 'Unit_Price', 'Stock_Count']

    def make_cell(value, val_type='string', style=None):
        if val_type == 'float':
            tc = TableCell(valuetype='float', value=str(value))
        else:
            tc = TableCell(valuetype='string')
        p = P(text=str(value))
        tc.addElement(p)
        return tc

    # Header row
    header_row = TableRow()
    for h in headers:
        header_row.addElement(make_cell(h))
    sheet.addElement(header_row)

    # Product data - 40 products across 5 categories
    # Electronics (10), Clothing (8), Food (7), Books (8), Home_Goods (7)
    products = [
        # Electronics (10)
        ('E001', 'UltraView 4K Monitor', 'Electronics',
         '27-inch IPS display, 144Hz refresh rate, HDR400 support, USB-C connectivity', 349.99, 42),
        ('E002', 'ProSound Wireless Headphones', 'Electronics',
         'Active noise cancellation, 30-hour battery life, foldable design, Bluetooth 5.2', 189.99, 78),
        ('E003', 'SwiftType Mechanical Keyboard', 'Electronics',
         'Tenkeyless layout, Cherry MX Red switches, RGB backlight, N-key rollover', 129.99, 55),
        ('E004', 'PrecisionTrack Mouse', 'Electronics',
         'Ergonomic design, 16000 DPI optical sensor, 7 programmable buttons, 2.4GHz wireless', 79.99, 93),
        ('E005', 'PowerBank Ultra 20000', 'Electronics',
         '20000mAh capacity, 65W PD fast charging, dual USB-A + USB-C ports, LCD display', 59.99, 120),
        ('E006', 'SmartHome Hub Pro', 'Electronics',
         'Supports Zigbee/Z-Wave/WiFi protocols, voice assistant compatible, 50-device limit', 149.99, 31),
        ('E007', 'WebCam 4K Pro', 'Electronics',
         '4K 30fps or 1080p 60fps, auto-focus, built-in ring light, privacy shutter', 109.99, 64),
        ('E008', 'PortaCharge 65W GaN', 'Electronics',
         'GaN technology, 3-port USB charger, foldable plug, international voltage support', 49.99, 200),
        ('E009', 'SoundBar Connect 2.1', 'Electronics',
         '120W total output, built-in subwoofer, Bluetooth/HDMI ARC/optical inputs, wall-mount kit', 229.99, 28),
        ('E010', 'TabletStand Pro Adjustable', 'Electronics',
         'Aluminum construction, 360-degree rotation, fits 7-13 inch devices, non-slip base', 39.99, 150),

        # Clothing (8)
        ('C001', 'Alpine Trek Jacket', 'Clothing',
         'Waterproof Gore-Tex shell, 3-in-1 design, removable fleece liner, 5 pockets', 245.00, 35),
        ('C002', 'CoreFlex Training Tee', 'Clothing',
         'Moisture-wicking polyester blend, flat-lock seams, anti-odor treatment, slim fit', 38.50, 110),
        ('C003', 'UrbanComfort Chinos', 'Clothing',
         'Stretch cotton-twill fabric, tapered fit, hidden coin pocket, available in 6 colors', 75.00, 88),
        ('C004', 'WoolBlend Business Socks 3pk', 'Clothing',
         'Merino wool blend, reinforced heel and toe, cushioned sole, crew length', 22.99, 245),
        ('C005', 'Summit Fleece Pullover', 'Clothing',
         '100% recycled polyester fleece, kangaroo pocket, half-zip design, anti-pill finish', 89.95, 62),
        ('C006', 'TechWeave Running Shorts', 'Clothing',
         '4-inch inseam, built-in liner, reflective trim, zip pocket, quick-dry fabric', 44.50, 95),
        ('C007', 'CloudStep Casual Sneakers', 'Clothing',
         'Memory foam insole, canvas upper, rubber sole, machine washable, unisex sizing', 68.00, 77),
        ('C008', 'ThermalBase Layer Set', 'Clothing',
         'Long-sleeve top + leggings set, brushed inner fleece, 4-way stretch, odor-resistant', 55.00, 53),

        # Food (7)
        ('F001', 'Artisan Dark Chocolate Collection', 'Food',
         'Assorted 70-90% cacao truffles, 12-piece gift box, single-origin beans, vegan-friendly', 28.50, 180),
        ('F002', 'Himalayan Pink Salt Grinder', 'Food',
         '200g premium coarse salt, refillable ceramic grinder, sustainably sourced', 12.99, 320),
        ('F003', 'Cold-Brew Coffee Concentrate', 'Food',
         '32oz bottle, single-origin Colombian beans, low acidity, makes 8-10 servings, refrigerate', 18.75, 95),
        ('F004', 'Organic Green Tea Sampler', 'Food',
         '40-bag assortment, 8 varieties including Sencha/Matcha/Gyokuro, USDA organic certified', 24.00, 140),
        ('F005', 'Truffle & Sea Salt Popcorn', 'Food',
         '6oz gourmet popcorn, real black truffle oil, non-GMO kernels, gluten-free, resealable bag', 9.99, 210),
        ('F006', 'Aged Balsamic Vinegar 12yr', 'Food',
         '250ml bottle, DOP certified Modena origin, 12-year aged, rich and complex flavor profile', 34.95, 60),
        ('F007', 'Raw Wildflower Honey 500g', 'Food',
         'Unfiltered and unpasteurized, mixed wildflower pollen, glass jar, local farm sourced', 15.50, 175),

        # Books (8)
        ('B001', 'The Art of Systems Thinking', 'Books',
         'Hardcover, 380 pages, explores mental models and feedback loops, bestseller edition', 32.00, 88),
        ('B002', 'Python Machine Learning 4th Ed', 'Books',
         'Paperback, 780 pages, covers scikit-learn/TensorFlow/PyTorch, practical examples throughout', 55.00, 42),
        ('B003', 'Financial Freedom Blueprint', 'Books',
         'Hardcover, 295 pages, personal finance and investment strategies, revised and updated', 27.50, 110),
        ('B004', 'Digital Photography Masterclass', 'Books',
         'Full-color paperback, 420 pages, covers composition/lighting/post-processing, 1200+ photos', 48.00, 35),
        ('B005', 'The Mediterranean Diet Cookbook', 'Books',
         'Hardcover, 336 pages, 150+ recipes, full-color photography, nutritional info per serving', 38.00, 75),
        ('B006', 'Leadership in the Digital Age', 'Books',
         'Paperback, 260 pages, case studies from Fortune 500 companies, includes workbook exercises', 29.95, 60),
        ('B007', 'Urban Gardening Handbook', 'Books',
         'Spiral-bound, 180 pages, covers balcony/rooftop/indoor growing, seasonal planting guides', 22.00, 92),
        ('B008', 'Mindfulness and Productivity', 'Books',
         'Paperback, 215 pages, evidence-based techniques, daily practice templates, audio companion', 19.99, 130),

        # Home_Goods (7)
        ('H001', 'BambooLux Cutting Board Set', 'Home_Goods',
         '3-piece nested set, organic bamboo, juice grooves, non-slip feet, antimicrobial surface', 45.00, 67),
        ('H002', 'Nordic Ceramic Mug Set 4pc', 'Home_Goods',
         '400ml capacity each, dishwasher safe, matte glaze finish, Scandinavian minimalist design', 52.00, 83),
        ('H003', 'EcoWeave Linen Throw Blanket', 'Home_Goods',
         '130x170cm, 100% stonewashed linen, herringbone pattern, machine washable, 8 color options', 79.00, 44),
        ('H004', 'AromaStone Essential Oil Diffuser', 'Home_Goods',
         '300ml ultrasonic diffuser, 7-color LED, timer function, auto shut-off, covers 400 sq ft', 38.50, 120),
        ('H005', 'SteelCore Stackable Organizer 5pk', 'Home_Goods',
         'Powder-coated steel bins, interlocking design, pantry/closet/office use, includes labels', 34.99, 98),
        ('H006', 'PlantPod Self-Watering Planters Set', 'Home_Goods',
         '3-piece glazed ceramic, reservoir system, drainage holes, fits 4-6 inch root balls, indoor', 42.00, 55),
        ('H007', 'VelvetTouch Bath Towel Set 6pc', 'Home_Goods',
         '600 GSM Egyptian cotton, 2 bath/2 hand/2 face towels, quick-dry weave, hotel collection', 89.99, 38),
    ]

    for prod in products:
        row = TableRow()
        pid, name, cat, desc, price, stock = prod
        row.addElement(make_cell(pid))
        row.addElement(make_cell(name))
        row.addElement(make_cell(cat))
        row.addElement(make_cell(desc))
        row.addElement(make_cell(price, 'float'))
        row.addElement(make_cell(stock, 'float'))
        sheet.addElement(row)

    doc.save(ODS_FILE)
    print(f'Initial file created: {ODS_FILE}')

    # GUI-ready startup: open products.ods in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{ODS_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Calc with products.ods, DISPLAY=:0')


create_initial()
