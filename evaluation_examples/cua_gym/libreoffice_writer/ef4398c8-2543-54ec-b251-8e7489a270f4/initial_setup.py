"""
Initial Setup: api_response.odt with JSON array of 10 API log entries (unsorted)
Task ID: osworld_multi_apps_json_reformat_writer_007
Domain: libreoffice_writer

Creates /home/user/Documents/api_response.odt with a JSON array of 10 API log entries.
The entries are unsorted (NOT sorted by response_time_ms).
The file contains plain text JSON - no table, no header note.
"""

import os
import shlex
import subprocess
import time

try:
    from odf.opendocument import OpenDocumentText
    from odf.text import P
    from odf.style import Style, TextProperties, ParagraphProperties
except ImportError:
    import subprocess as _sp
    _sp.run(["pip3", "install", "odfpy"], check=True)
    from odf.opendocument import OpenDocumentText
    from odf.text import P
    from odf.style import Style, TextProperties, ParagraphProperties

WORKDIR = '/home/user'
DOCS_DIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_007'
OUTPUT = f'{DOCS_DIR}/api_response.odt'


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
    # Ensure Documents directory exists
    os.makedirs(DOCS_DIR, exist_ok=True)

    # JSON array of 10 API log entries - UNSORTED (random order by response_time_ms)
    # Response times range from 45ms to 2300ms
    json_content = """[
  {
    "timestamp": "2025-03-15T08:12:34Z",
    "endpoint": "/api/v1/users",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": 185
  },
  {
    "timestamp": "2025-03-15T08:14:02Z",
    "endpoint": "/api/v1/orders",
    "method": "POST",
    "status_code": 201,
    "response_time_ms": 980
  },
  {
    "timestamp": "2025-03-15T08:15:47Z",
    "endpoint": "/api/v1/products",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": 45
  },
  {
    "timestamp": "2025-03-15T08:17:10Z",
    "endpoint": "/api/v1/auth/login",
    "method": "POST",
    "status_code": 200,
    "response_time_ms": 2300
  },
  {
    "timestamp": "2025-03-15T08:19:33Z",
    "endpoint": "/api/v1/inventory",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": 310
  },
  {
    "timestamp": "2025-03-15T08:21:55Z",
    "endpoint": "/api/v1/reports/monthly",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": 1850
  },
  {
    "timestamp": "2025-03-15T08:23:14Z",
    "endpoint": "/api/v1/users/profile",
    "method": "PUT",
    "status_code": 200,
    "response_time_ms": 120
  },
  {
    "timestamp": "2025-03-15T08:25:40Z",
    "endpoint": "/api/v1/notifications",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": 640
  },
  {
    "timestamp": "2025-03-15T08:27:08Z",
    "endpoint": "/api/v1/payments",
    "method": "POST",
    "status_code": 201,
    "response_time_ms": 490
  },
  {
    "timestamp": "2025-03-15T08:29:22Z",
    "endpoint": "/api/v1/analytics/dashboard",
    "method": "GET",
    "status_code": 200,
    "response_time_ms": 220
  }
]"""

    # Create ODT document with the JSON as plain text
    doc = OpenDocumentText()

    # Add a default paragraph style
    para_style = Style(name="DefaultParagraph", family="paragraph")
    para_style.addElement(ParagraphProperties(breakbefore="auto"))
    doc.automaticstyles.addElement(para_style)

    # Add JSON content as a single paragraph
    para = P(stylename="DefaultParagraph")
    para.addText(json_content)
    doc.text.addElement(para)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
