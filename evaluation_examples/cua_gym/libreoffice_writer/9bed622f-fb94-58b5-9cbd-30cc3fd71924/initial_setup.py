"""
Initial Setup: Network scan results document with duplicate MAC addresses
Task ID: osworld_writer_dedup_010
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_dedup_010'
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


def create_initial():
    # 117 unique MAC addresses — realistic device inventory for a mid-size office network
    unique_macs = [
        "00:1A:2B:3C:4D:5E",
        "AA:BB:CC:DD:EE:FF",
        "08:00:27:AB:CD:EF",
        "00:50:56:C0:00:01",
        "52:54:00:12:34:56",
        "B8:27:EB:01:23:45",
        "DC:A6:32:67:89:AB",
        "00:0C:29:4F:6A:12",
        "00:1B:21:E3:07:44",
        "3C:A9:F4:28:BC:01",
        "F4:EC:38:AA:11:22",
        "A4:C3:F0:77:88:99",
        "00:26:B9:C0:D1:E2",
        "74:DA:38:F3:04:15",
        "E8:40:F2:1C:2D:3E",
        "00:23:14:5A:6B:7C",
        "FC:FB:FB:01:A2:B3",
        "D0:50:99:C4:D5:E6",
        "1C:1B:0D:F7:08:19",
        "44:8A:5B:2A:3B:4C",
        "78:E4:00:5D:6E:7F",
        "00:09:6B:80:91:A2",
        "00:13:77:B3:C4:D5",
        "34:97:F6:E6:F7:08",
        "70:85:C2:19:2A:3B",
        "20:F4:1B:4C:5D:6E",
        "00:1C:42:7F:80:91",
        "5C:CF:7F:A2:B3:C4",
        "00:0D:3A:D5:E6:F7",
        "EC:FA:BC:08:19:2A",
        "00:1D:09:3B:4C:5D",
        "BC:EE:7B:6E:7F:80",
        "00:0F:EA:91:A2:B3",
        "28:CD:C1:C4:D5:E6",
        "7C:2F:80:F7:08:19",
        "AC:3C:0B:2A:3B:4C",
        "00:1A:79:5D:6E:7F",
        "64:70:02:80:91:A2",
        "CC:F9:54:B3:C4:D5",
        "84:0D:8E:E6:F7:08",
        "00:1E:4C:19:2A:3B",
        "A8:51:AB:4C:5D:6E",
        "18:31:BF:7F:80:91",
        "00:60:97:A2:B3:C4",
        "B4:FB:E4:D5:E6:F7",
        "00:24:1D:08:19:2A",
        "60:F8:1D:3B:4C:5D",
        "98:90:96:6E:7F:80",
        "40:B0:34:91:A2:B3",
        "14:5A:05:C4:D5:E6",
        "3C:97:0E:F7:08:19",
        "00:11:22:2A:3B:4C",
        "7E:05:15:5D:6E:7F",
        "88:36:6C:80:91:A2",
        "2C:4D:54:B3:C4:D5",
        "C8:D7:19:E6:F7:08",
        "00:17:F2:19:2A:3B",
        "54:26:96:4C:5D:6E",
        "EC:88:8F:7F:80:91",
        "AC:DE:48:A2:B3:C4",
        "50:7A:55:D5:E6:F7",
        "00:1B:77:08:19:2A",
        "6C:40:08:3B:4C:5D",
        "F0:18:98:6E:7F:80",
        "24:77:03:91:A2:B3",
        "D8:FE:E3:C4:D5:E6",
        "00:15:5D:F7:08:19",
        "48:51:B7:2A:3B:4C",
        "90:B1:1C:5D:6E:7F",
        "0C:8B:FD:80:91:A2",
        "58:B0:35:B3:C4:D5",
        "E4:F8:9C:E6:F7:08",
        "00:12:17:19:2A:3B",
        "4C:74:03:4C:5D:6E",
        "A0:99:9B:7F:80:91",
        "30:F9:ED:A2:B3:C4",
        "8C:EC:4B:D5:E6:F7",
        "00:1F:F3:08:19:2A",
        "68:A8:6D:3B:4C:5D",
        "B0:D5:CC:6E:7F:80",
        "1C:AF:F7:91:A2:B3",
        "D4:01:29:C4:D5:E6",
        "00:21:70:F7:08:19",
        "38:C9:86:2A:3B:4C",
        "94:DE:80:5D:6E:7F",
        "2C:DB:07:80:91:A2",
        "70:F3:95:B3:C4:D5",
        "00:22:48:E6:F7:08",
        "BC:5F:F4:19:2A:3B",
        "E0:CB:4E:4C:5D:6E",
        "48:D7:05:7F:80:91",
        "AC:7B:A1:A2:B3:C4",
        "00:25:B3:D5:E6:F7",
        "64:D1:54:08:19:2A",
        "28:EF:01:3B:4C:5D",
        "80:CE:62:6E:7F:80",
        "3C:07:71:91:A2:B3",
        "00:27:0E:C4:D5:E6",
        "5C:51:4F:F7:08:19",
        "C4:6A:B7:2A:3B:4C",
        "10:02:B5:5D:6E:7F",
        "6C:B7:F4:80:91:A2",
        "A4:77:33:B3:C4:D5",
        "00:90:27:E6:F7:08",
        "D8:B3:77:19:2A:3B",
        "54:EE:75:4C:5D:6E",
        "18:65:90:7F:80:91",
        "FC:3F:DB:A2:B3:C4",
        "08:3A:88:D5:E6:F7",
        "44:D8:84:08:19:2A",
        "9C:B6:D0:3B:4C:5D",
        "60:D9:C7:6E:7F:80",
        "34:36:3B:91:A2:B3",
    ]

    # Three scan passes — simulate scanner detecting all devices three times
    # Pass 1: sequential order
    pass1 = list(unique_macs)
    # Pass 2: slightly shuffled order (simulates real scanner re-discovery)
    pass2 = unique_macs[11:] + unique_macs[:11]
    # Pass 3: another shuffle pattern
    pass3 = unique_macs[23:] + unique_macs[:23]

    # Interleaved scan results (all three passes combined, ~351 lines)
    all_macs = pass1 + pass2 + pass3

    doc = Document()

    for mac in all_macs:
        doc.add_paragraph(mac)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines: {len(all_macs)} ({len(unique_macs)} unique * 3 passes)')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
