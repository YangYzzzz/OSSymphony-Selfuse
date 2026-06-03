"""
Initial Setup: Create a 3-page client contact directory PDF with 24 phone numbers
Task ID: pdf_fin_057
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_057'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/client_contacts.pdf'

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
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792

    # Define 24 clients across 3 pages (8 per page)
    clients = [
        # Page 1: Clients 1-8
        [
            ("Sarah Chen", "Meridian Capital Partners", "sarah.chen@meridiancp.com", "(415) 892-3047", "2100 Market Street, San Francisco, CA 94114"),
            ("Marcus Johnson", "Apex Wealth Management", "m.johnson@apexwealth.com", "312-555-6781", "875 N Michigan Ave, Chicago, IL 60611"),
            ("Elena Rodriguez", "Pacific Coast Financial", "elena.r@pcfinancial.com", "650.443.8912", "400 Hamilton Ave, Palo Alto, CA 94301"),
            ("David Kim", "Sterling Investment Group", "dkim@sterlinginvest.com", "(212) 738-4521", "One World Trade Center, New York, NY 10007"),
            ("Rachel Thompson", "Crestview Capital", "rthompson@crestviewcap.com", "617-224-9033", "100 Federal Street, Boston, MA 02110"),
            ("James O'Brien", "Harbor Point Advisors", "jobrien@harborpoint.com", "(303) 557-8214", "1801 California St, Denver, CO 80202"),
            ("Priya Patel", "Quantum Financial Services", "ppatel@quantumfs.com", "408.331.7625", "2025 Gateway Place, San Jose, CA 95110"),
            ("William Foster", "Evergreen Asset Management", "wfoster@evergreen-am.com", "(202) 644-3189", "1700 K Street NW, Washington, DC 20006"),
        ],
        # Page 2: Clients 9-16
        [
            ("Lisa Chang", "Summit Ridge Partners", "lchang@summitridge.com", "206-873-4156", "1201 Third Ave, Seattle, WA 98101"),
            ("Robert Martinez", "Pinnacle Trust Group", "rmartinez@pinnacletrust.com", "(713) 429-8573", "1000 Louisiana St, Houston, TX 77002"),
            ("Amanda Wright", "Northstar Financial", "awright@northstarfin.com", "312.667.2948", "233 S Wacker Dr, Chicago, IL 60606"),
            ("Thomas Nakamura", "Bluewater Capital", "tnakamura@bluewatercap.com", "(415) 783-6102", "555 California St, San Francisco, CA 94104"),
            ("Catherine Brooks", "Ironwood Investments", "cbrooks@ironwoodinv.com", "949-558-3471", "3161 Michelson Dr, Irvine, CA 92612"),
            ("Michael Sullivan", "Granite Capital Advisors", "msullivan@granitecap.com", "(617) 332-7854", "225 Franklin St, Boston, MA 02110"),
            ("Diana Okafor", "Silverline Wealth", "dokafor@silverlinew.com", "404.219.6583", "191 Peachtree St NE, Atlanta, GA 30303"),
            ("Andrew Peterson", "Atlas Financial Group", "apeterson@atlasfg.com", "(972) 441-8267", "2200 Ross Ave, Dallas, TX 75201"),
        ],
        # Page 3: Clients 17-24
        [
            ("Jennifer Lee", "Sapphire Investment Partners", "jlee@sapphireip.com", "310-672-9418", "2049 Century Park E, Los Angeles, CA 90067"),
            ("Christopher Davis", "Monarch Advisory Services", "cdavis@monarchadv.com", "(305) 834-2176", "1450 Brickell Ave, Miami, FL 33131"),
            ("Stephanie Hoffman", "Ridgeline Capital", "shoffman@ridgelinecap.com", "503.287.4953", "111 SW 5th Ave, Portland, OR 97204"),
            ("Daniel Garcia", "Horizon Trust Management", "dgarcia@horizontm.com", "(480) 593-7128", "2398 E Camelback Rd, Phoenix, AZ 85016"),
            ("Maria Volkov", "Cornerstone Financial", "mvolkov@cornerstonefin.com", "612-448-3697", "225 S 6th St, Minneapolis, MN 55402"),
            ("Brian Taylor", "Keystone Wealth Partners", "btaylor@keystonewp.com", "(704) 261-5834", "201 S College St, Charlotte, NC 28244"),
            ("Natalie Chen", "Vanguard Point Advisors", "nchen@vanguardpoint.com", "858.734.2196", "4370 La Jolla Village Dr, San Diego, CA 92122"),
            ("Kevin O'Connor", "Liberty Financial Group", "koconnor@libertyfg.com", "(215) 887-4312", "1600 Market St, Philadelphia, PA 19103"),
        ],
    ]

    # Column layout
    col_x = {
        'name': 36,
        'company': 145,
        'email': 295,
        'phone': 430,
        'address': 430,
    }

    for page_idx, page_clients in enumerate(clients):
        page = doc.new_page(width=W, height=H)

        # Title
        page.insert_text(
            pymupdf.Point(36, 40),
            "MERIDIAN FINANCIAL GROUP",
            fontsize=16,
            fontname="hebo",
            color=(0.0, 0.15, 0.4),
        )
        page.insert_text(
            pymupdf.Point(36, 58),
            "Client Contact Directory — Confidential",
            fontsize=10,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(36, 65), pymupdf.Point(W - 36, 65))
        shape.finish(color=(0.0, 0.15, 0.4), width=1.5)
        shape.commit()

        # Column headers
        y_header = 85
        headers = [("Client Name", col_x['name']), ("Company", col_x['company']),
                    ("Email / Phone", col_x['email'])]
        for text, x in headers:
            page.insert_text(
                pymupdf.Point(x, y_header),
                text,
                fontsize=9,
                fontname="hebo",
                color=(0.0, 0.15, 0.4),
            )

        # Header underline
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(36, y_header + 5), pymupdf.Point(W - 36, y_header + 5))
        shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape2.commit()

        # Client entries
        y = y_header + 25
        for i, (name, company, email, phone, address) in enumerate(page_clients):
            # Alternating background
            if i % 2 == 0:
                shape3 = page.new_shape()
                shape3.draw_rect(pymupdf.Rect(36, y - 12, W - 36, y + 55))
                shape3.finish(fill=(0.96, 0.96, 0.98), color=None)
                shape3.commit()

            # Client name
            page.insert_text(pymupdf.Point(col_x['name'], y), name, fontsize=10, fontname="hebo", color=(0.1, 0.1, 0.1))
            # Company
            page.insert_text(pymupdf.Point(col_x['company'], y), company, fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
            # Email
            page.insert_text(pymupdf.Point(col_x['email'], y), email, fontsize=8, fontname="helv", color=(0.2, 0.2, 0.6))
            # Phone
            page.insert_text(pymupdf.Point(col_x['email'], y + 14), f"Tel: {phone}", fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))
            # Address
            page.insert_text(pymupdf.Point(col_x['name'], y + 28), address, fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))

            y += 80

        # Page footer
        page.insert_text(
            pymupdf.Point(36, H - 30),
            f"Page {page_idx + 1} of 3",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )
        page.insert_text(
            pymupdf.Point(W - 200, H - 30),
            "Confidential — Do Not Distribute",
            fontsize=7,
            fontname="heit",
            color=(0.6, 0.6, 0.6),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
