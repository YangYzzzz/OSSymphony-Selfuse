"""
Initial Setup: Wine bottle label creation task
Task ID: writer_mt_036
Domain: libreoffice_writer

Creates:
1. A WineCatalog CSV data source with 24 records
2. A blank Writer document (pre-task state)
3. Opens LibreOffice Writer with the blank document
"""

import csv
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_036'
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

def create_wine_catalog_csv():
    """Create a WineCatalog CSV data source with 24 records."""
    csv_path = f'{WORKDIR}/WineCatalog.csv'
    records = [
        ["WineName", "Vintage", "Region", "Varietal", "Price"],
        ["Chateau Margaux", "2018", "Bordeaux", "Cabernet Sauvignon", "89.99"],
        ["Opus One", "2019", "Napa Valley", "Red Blend", "124.50"],
        ["Cloudy Bay", "2022", "Marlborough", "Sauvignon Blanc", "22.95"],
        ["Penfolds Grange", "2017", "Barossa Valley", "Shiraz", "175.00"],
        ["Tignanello", "2019", "Tuscany", "Sangiovese Blend", "95.00"],
        ["Clos du Mesnil", "2012", "Champagne", "Chardonnay", "310.00"],
        ["Ridge Monte Bello", "2018", "Santa Cruz Mountains", "Cabernet Sauvignon", "145.00"],
        ["Vega Sicilia Unico", "2011", "Ribera del Duero", "Tempranillo Blend", "285.00"],
        ["Domaine Leflaive Puligny", "2020", "Burgundy", "Chardonnay", "135.00"],
        ["Sassicaia", "2019", "Bolgheri", "Cabernet Sauvignon", "210.00"],
        ["Almaviva", "2020", "Maipo Valley", "Red Blend", "78.00"],
        ["Torbreck RunRig", "2018", "Barossa Valley", "Shiraz Viognier", "155.00"],
        ["Catena Zapata Malbec", "2020", "Mendoza", "Malbec", "42.50"],
        ["Kim Crawford", "2023", "Hawkes Bay", "Pinot Noir", "18.99"],
        ["Antinori Solaia", "2018", "Tuscany", "Cabernet Sauvignon", "198.00"],
        ["Beringer Private Reserve", "2019", "Napa Valley", "Cabernet Sauvignon", "165.00"],
        ["Trimbach Riesling", "2021", "Alsace", "Riesling", "34.50"],
        ["Guigal Cote Rotie", "2017", "Rhone Valley", "Syrah", "88.00"],
        ["Felton Road Block 5", "2021", "Central Otago", "Pinot Noir", "62.00"],
        ["Henschke Hill of Grace", "2016", "Eden Valley", "Shiraz", "450.00"],
        ["Dominus Estate", "2018", "Napa Valley", "Red Blend", "195.00"],
        ["Chateau Musar", "2015", "Bekaa Valley", "Red Blend", "38.00"],
        ["Yalumba The Signature", "2018", "Barossa Valley", "Cabernet Shiraz", "55.00"],
        ["Cakebread Cellars", "2021", "Napa Valley", "Chardonnay", "48.00"],
    ]
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(records)
    print(f'WineCatalog CSV created: {csv_path}')
    return csv_path

def create_initial_document():
    """Create a blank Writer document as the pre-task state."""
    from docx import Document
    from docx.shared import Inches

    doc = Document()

    # Set standard page size (Letter)
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)

    # Add a single empty paragraph (blank doc)
    doc.add_paragraph("")

    doc.save(OUTPUT)
    print(f'Initial document created: {OUTPUT}')

def main():
    create_wine_catalog_csv()
    create_initial_document()

    # Open LibreOffice Writer with the blank document
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')

main()
