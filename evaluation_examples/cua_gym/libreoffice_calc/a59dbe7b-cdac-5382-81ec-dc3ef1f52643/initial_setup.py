"""
Initial Setup: Bangkok Street Food Markets Research Task
Task ID: osworld_multi_apps_web_location_009
Domain: libreoffice_calc (multi-app with Chrome)

Creates asia_markets.ods on the Desktop with 4 existing entries for
non-Bangkok Asian cities. The agent will search for Bangkok markets
and add 6 new rows.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_location_009'
OUTPUT = f'{WORKDIR}/asia_markets.ods'


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
    # Install odfpy if needed
    subprocess.run(
        ['pip3', 'install', 'odfpy', '--quiet'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableColumnProperties, TableRowProperties
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf.text import P

    doc = OpenDocumentSpreadsheet()

    # Define styles
    header_style = Style(name="HeaderStyle", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(header_style)

    table = Table(name="Sheet1")

    # Column widths
    for _ in range(7):
        col = TableColumn()
        table.addElement(col)

    # Header row
    headers = ['Name', 'City', 'Country', 'Area', 'Opening_Hours', 'Specialty_Food', 'Source_URL']
    header_row = TableRow()
    for h in headers:
        cell = TableCell(valuetype="string", stylename="HeaderStyle")
        cell.addElement(P(text=h))
        header_row.addElement(cell)
    table.addElement(header_row)

    # 4 existing entries for non-Bangkok Asian cities
    data = [
        [
            'Tsukiji Outer Market',
            'Tokyo',
            'Japan',
            'Chuo City',
            '5AM-2PM daily',
            'Fresh sushi, tamagoyaki, seafood bowls',
            'https://www.timeout.com/tokyo/restaurants/tsukiji-outer-market'
        ],
        [
            'Gwangjang Market',
            'Seoul',
            'South Korea',
            'Jongno-gu',
            '9AM-11PM daily',
            'Bindaetteok, mayak gimbap, raw beef yukhoe',
            'https://www.lonelyplanet.com/south-korea/seoul/attractions/gwangjang-market'
        ],
        [
            'Maxwell Food Centre',
            'Singapore',
            'Singapore',
            'Chinatown, Outram',
            '8AM-10PM daily',
            'Hainanese chicken rice, char kway teow, laksa',
            'https://www.visitsingapore.com/dining-drinks/local-dishes/maxwell-food-centre'
        ],
        [
            'Temple Street Night Market',
            'Hong Kong',
            'China',
            'Yau Ma Tei, Kowloon',
            '4PM-11PM daily',
            'Stinky tofu, curry fishballs, egg waffles',
            'https://www.discoverhongkong.com/us/shop/where-to-shop/street-markets/temple-street-night-market.jsp'
        ],
    ]

    for row_data in data:
        row = TableRow()
        for val in row_data:
            cell = TableCell(valuetype="string")
            cell.addElement(P(text=str(val)))
            row.addElement(cell)
        table.addElement(row)

    doc.spreadsheet.addElement(table)

    # Ensure Desktop directory exists
    os.makedirs(WORKDIR, exist_ok=True)
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open Chrome and LibreOffice Calc
    # First open Chrome so agent can search
    launch_gui('google-chrome', delay_sec=2.0)
    # Then open the initial ODS file in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')


create_initial()
