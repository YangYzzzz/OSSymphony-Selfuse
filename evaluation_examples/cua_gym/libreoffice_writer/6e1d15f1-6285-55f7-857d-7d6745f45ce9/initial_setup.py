"""
Initial Setup: Mail merge holiday greeting letter
Task ID: writer_mt_032
Domain: libreoffice_writer

Creates:
  1. /home/user/Desktop/holiday_clients.csv  — 40-record client list
  2. /home/user/writer_mt_032.docx           — blank document
  3. Opens the blank document in LibreOffice Writer
"""

import csv
import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_032'
OUTPUT_DOCX = f'{WORKDIR}/{TASK_ID}.docx'
CSV_PATH = f'{WORKDIR}/Desktop/holiday_clients.csv'


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


# --- Client data (40 records) ---
CLIENTS = [
    ("Margaret Thompson", "Cascade Industries", "742 Elm Street", "Portland", "OR", "97201"),
    ("David Nakamura", "Pacific Ventures", "1085 Market Ave", "San Francisco", "CA", "94103"),
    ("Elena Rodriguez", "Sunrise Healthcare", "320 Oak Boulevard", "Austin", "TX", "78701"),
    ("James O'Brien", "Atlantic Partners", "55 Harbor Lane", "Boston", "MA", "02110"),
    ("Priya Sharma", "Summit Analytics", "1200 Pine Road", "Seattle", "WA", "98101"),
    ("Robert Chen", "Golden Gate Consulting", "890 Bay Street", "San Jose", "CA", "95112"),
    ("Sarah Mitchell", "Evergreen Solutions", "415 Maple Drive", "Denver", "CO", "80202"),
    ("Michael Okafor", "Lakeside Technologies", "2300 Lake Avenue", "Chicago", "IL", "60601"),
    ("Amanda Foster", "Horizon Media Group", "178 Sunset Blvd", "Los Angeles", "CA", "90028"),
    ("Thomas Klein", "Sterling Logistics", "650 River Road", "Minneapolis", "MN", "55401"),
    ("Lisa Patel", "Pinnacle Financial", "92 Wall Street", "New York", "NY", "10005"),
    ("Christopher Adams", "Blue Ridge Software", "1420 Mountain View", "Raleigh", "NC", "27601"),
    ("Jennifer Wu", "Coral Bay Imports", "330 Coastal Highway", "Miami", "FL", "33101"),
    ("Daniel Hernandez", "Redwood Manufacturing", "785 Industrial Parkway", "Sacramento", "CA", "95814"),
    ("Rachel Green", "Northern Star Marketing", "210 Birch Lane", "Minneapolis", "MN", "55402"),
    ("William Turner", "Ironclad Security", "500 Federal Plaza", "Washington", "DC", "20001"),
    ("Sophia Kim", "Orion Research Labs", "1100 Science Drive", "San Diego", "CA", "92101"),
    ("Andrew Collins", "Maple Leaf Hospitality", "88 Main Street", "Burlington", "VT", "05401"),
    ("Maria Santos", "Crescent Moon Designs", "445 Art District Way", "Santa Fe", "NM", "87501"),
    ("Kevin Murphy", "Trident Marine Services", "720 Dock Street", "Savannah", "GA", "31401"),
    ("Olivia Bennett", "Clearwater Energy", "360 Solar Avenue", "Phoenix", "AZ", "85001"),
    ("Patrick Walsh", "Emerald Isle Imports", "115 Commerce Boulevard", "Philadelphia", "PA", "19103"),
    ("Yuki Tanaka", "Sakura Tech Solutions", "2040 Innovation Way", "Austin", "TX", "78702"),
    ("Brian Larson", "Glacier Point Advisors", "530 Summit Road", "Salt Lake City", "UT", "84101"),
    ("Catherine Dubois", "Belle Epoch Interiors", "275 Design Center", "Nashville", "TN", "37201"),
    ("Marcus Williams", "Thunderbolt Sports", "800 Stadium Drive", "Atlanta", "GA", "30301"),
    ("Nadia Volkov", "Crystal Clear Optics", "145 Precision Lane", "Rochester", "NY", "14604"),
    ("George Papadopoulos", "Olympus Consulting", "910 Heritage Circle", "Tampa", "FL", "33602"),
    ("Isabel Moreno", "Terra Verde Organics", "420 Farm Road", "Portland", "OR", "97202"),
    ("Henry Chang", "Dragon Gate Enterprises", "1330 Commerce Street", "Houston", "TX", "77002"),
    ("Aisha Johnson", "Sahara Sun Travel", "250 Explorer Avenue", "Las Vegas", "NV", "89101"),
    ("Steven Park", "Han River Electronics", "675 Tech Park Drive", "San Jose", "CA", "95113"),
    ("Laura Fitzgerald", "Claddagh Publishing", "88 Library Square", "Dublin", "OH", "43017"),
    ("Ricardo Flores", "Condor Aerospace", "1500 Runway Boulevard", "Tucson", "AZ", "85701"),
    ("Emily Watson", "Heatherfield Textiles", "340 Mill Road", "Charlotte", "NC", "28201"),
    ("Raj Gupta", "Monsoon Technologies", "715 Gateway Center", "Dallas", "TX", "75201"),
    ("Claire Beaumont", "Chateau Wines LLC", "200 Vineyard Lane", "Napa", "CA", "94559"),
    ("Derek Howard", "Falcon Freight", "820 Logistics Way", "Memphis", "TN", "38103"),
    ("Monica Torres", "Sol y Luna Bakery", "155 Fiesta Street", "San Antonio", "TX", "78205"),
    ("Nathan Brooks", "Timber Creek Construction", "460 Builder Road", "Boise", "ID", "83702"),
]


def create_initial():
    # 1. Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    # 2. Write the CSV file
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ClientName', 'CompanyName', 'Address', 'City', 'State', 'Zip'])
        for client in CLIENTS:
            writer.writerow(client)
    print(f'CSV created: {CSV_PATH} ({len(CLIENTS)} records)')

    # 3. Create a blank document
    doc = Document()
    doc.save(OUTPUT_DOCX)
    print(f'Blank document created: {OUTPUT_DOCX}')

    # 4. Launch LibreOffice Writer with the blank document
    launch_gui(f'libreoffice --writer "{OUTPUT_DOCX}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
