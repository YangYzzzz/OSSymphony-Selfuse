"""
Initial Setup: Multi-app task — Extract email tables and consolidate into spreadsheet
Task ID: osworld_multi_apps_email_data_011
Domain: libreoffice_calc + thunderbird (multi-app)

Creates:
  1. /home/user/sales_consolidated.ods — Calc file with headers only, no data
  2. Thunderbird 'Monthly Reports' folder with 3 emails from regional managers,
     each containing an HTML table with sales data
  3. Opens both LibreOffice Calc and Thunderbird in GUI-ready state
"""

import os
import shlex
import subprocess
import time
import mailbox
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_data_011'
OUTPUT_ODS = f'{WORKDIR}/sales_consolidated.ods'

# Sales data that will be IN the emails (agent needs to extract manually)
# Region, Q1, Q2, Q3, Q4
NORTH_DATA = ('North', 124500, 138200, 151900, 167300)
SOUTH_DATA = ('South', 98300, 105700, 112400, 119800)
EAST_DATA  = ('East',  143600, 157200, 168900, 182500)


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


def build_email_html(sender_name: str, region: str, q1: int, q2: int, q3: int, q4: int) -> str:
    """Build an HTML email body with an inline table of quarterly sales data."""
    return f"""<html>
<body>
<p>Hi Team,</p>
<p>Please find below the quarterly sales figures for the <strong>{region} Region</strong> for the current fiscal year.</p>
<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; font-family: Arial, sans-serif;">
  <thead>
    <tr style="background-color: #4472C4; color: white;">
      <th>Region</th>
      <th>Q1</th>
      <th>Q2</th>
      <th>Q3</th>
      <th>Q4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{region}</td>
      <td>{q1:,}</td>
      <td>{q2:,}</td>
      <td>{q3:,}</td>
      <td>{q4:,}</td>
    </tr>
  </tbody>
</table>
<p>Please let me know if you need any clarification on these numbers.</p>
<p>Best regards,<br>{sender_name}<br>Regional Sales Manager, {region} Region</p>
</body>
</html>"""


def build_email_text(sender_name: str, region: str, q1: int, q2: int, q3: int, q4: int) -> str:
    """Build a plain-text fallback for the email."""
    return f"""Hi Team,

Please find below the quarterly sales figures for the {region} Region:

Region  | Q1      | Q2      | Q3      | Q4
{region:<7} | {q1:<7,} | {q2:<7,} | {q3:<7,} | {q4:<7,}

Please let me know if you need any clarification.

Best regards,
{sender_name}
Regional Sales Manager, {region} Region
"""


def create_mime_email(sender: str, sender_name: str, subject: str,
                      region: str, q1: int, q2: int, q3: int, q4: int,
                      date_str: str) -> email.message.Message:
    """Construct a multipart MIME email message."""
    msg = MIMEMultipart('alternative')
    msg['From'] = f'{sender_name} <{sender}>'
    msg['To'] = 'sales-team@company.com'
    msg['Subject'] = subject
    msg['Date'] = date_str
    msg['Message-ID'] = f'<{region.lower()}-q-report-2025@company.com>'

    # Plain text part
    text_part = MIMEText(
        build_email_text(sender_name, region, q1, q2, q3, q4),
        'plain', 'utf-8'
    )
    # HTML part
    html_part = MIMEText(
        build_email_html(sender_name, region, q1, q2, q3, q4),
        'html', 'utf-8'
    )

    msg.attach(text_part)
    msg.attach(html_part)
    return msg


def setup_thunderbird_emails():
    """
    Creates a local mbox file in Thunderbird's profile Mail/Local Folders/
    named 'Monthly Reports' and inserts 3 regional-manager emails.
    Also registers the folder in Thunderbird's pref file if needed.
    """
    import glob as globmod

    # Locate Thunderbird profile directory
    tb_profiles_dir = os.path.expanduser('~/.thunderbird')
    profile_dirs = globmod.glob(os.path.join(tb_profiles_dir, '*.default*'))
    if not profile_dirs:
        # Create a minimal profile if none exists
        profile_path = os.path.join(tb_profiles_dir, 'default.default-release')
        os.makedirs(profile_path, exist_ok=True)
    else:
        profile_path = profile_dirs[0]

    local_folders_dir = os.path.join(profile_path, 'Mail', 'Local Folders')
    os.makedirs(local_folders_dir, exist_ok=True)

    mbox_path = os.path.join(local_folders_dir, 'Monthly Reports')

    # Remove existing mbox if present to ensure idempotency
    if os.path.exists(mbox_path):
        os.remove(mbox_path)
    msf_path = mbox_path + '.msf'
    if os.path.exists(msf_path):
        os.remove(msf_path)

    # Define the 3 regional emails
    emails_to_create = [
        {
            'sender': 'north@company.com',
            'sender_name': 'Alexandra Winters',
            'subject': 'Q1-Q4 Sales Report — North Region',
            'region': 'North',
            'q1': NORTH_DATA[1],
            'q2': NORTH_DATA[2],
            'q3': NORTH_DATA[3],
            'q4': NORTH_DATA[4],
            'date_str': 'Mon, 03 Feb 2025 09:15:00 +0000',
        },
        {
            'sender': 'south@company.com',
            'sender_name': 'Marcus Delgado',
            'subject': 'Q1-Q4 Sales Report — South Region',
            'region': 'South',
            'q1': SOUTH_DATA[1],
            'q2': SOUTH_DATA[2],
            'q3': SOUTH_DATA[3],
            'q4': SOUTH_DATA[4],
            'date_str': 'Mon, 03 Feb 2025 10:22:00 +0000',
        },
        {
            'sender': 'east@company.com',
            'sender_name': 'Priya Nair',
            'subject': 'Q1-Q4 Sales Report — East Region',
            'region': 'East',
            'q1': EAST_DATA[1],
            'q2': EAST_DATA[2],
            'q3': EAST_DATA[3],
            'q4': EAST_DATA[4],
            'date_str': 'Mon, 03 Feb 2025 11:08:00 +0000',
        },
    ]

    # Write messages to mbox
    with open(mbox_path, 'w', encoding='utf-8') as mbox_file:
        for edata in emails_to_create:
            msg = create_mime_email(
                sender=edata['sender'],
                sender_name=edata['sender_name'],
                subject=edata['subject'],
                region=edata['region'],
                q1=edata['q1'],
                q2=edata['q2'],
                q3=edata['q3'],
                q4=edata['q4'],
                date_str=edata['date_str'],
            )
            # mbox format: each message starts with "From " line
            mbox_file.write(f"From {edata['sender']} {edata['date_str']}\n")
            mbox_file.write(msg.as_string())
            mbox_file.write('\n\n')

    print(f'Thunderbird mbox created: {mbox_path}')
    print(f'  3 emails written to Monthly Reports folder')
    return mbox_path, local_folders_dir


def create_initial_ods():
    """
    Create the initial sales_consolidated.ods with headers only.
    We create it as an .xlsx first, then use LibreOffice headless to convert to .ods.
    The initial file must NOT contain data rows 2-4, SUM formulas, or a bar chart.
    """
    import openpyxl

    xlsx_tmp = f'{WORKDIR}/{TASK_ID}_tmp.xlsx'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Sales Data'

    # Headers in row 1 — these match the email table columns
    headers = ['Region', 'Q1', 'Q2', 'Q3', 'Q4']
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)

    # Rows 2-4 intentionally empty (agent must fill from emails)
    # Row 5 intentionally empty (agent must add SUM formulas)
    # No chart (agent must create)

    wb.save(xlsx_tmp)
    print(f'Temporary xlsx created: {xlsx_tmp}')

    # Convert to .ods using LibreOffice headless
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    result = subprocess.run(
        ['libreoffice', '--headless', '--convert-to', 'ods',
         '--outdir', WORKDIR, xlsx_tmp],
        capture_output=True, text=True, env=env, timeout=60
    )
    print(f'LibreOffice conversion stdout: {result.stdout}')
    print(f'LibreOffice conversion stderr: {result.stderr}')

    # LibreOffice converts <name>_tmp.xlsx -> <name>_tmp.ods
    ods_tmp = f'{WORKDIR}/{TASK_ID}_tmp.ods'
    if os.path.exists(ods_tmp):
        os.rename(ods_tmp, OUTPUT_ODS)
        print(f'ODS file created: {OUTPUT_ODS}')
    else:
        # Fallback: just keep the xlsx under the ods name
        print(f'WARNING: LibreOffice conversion failed; keeping xlsx as ods fallback')
        os.rename(xlsx_tmp, OUTPUT_ODS)

    # Clean up temp xlsx if still exists
    if os.path.exists(xlsx_tmp):
        os.remove(xlsx_tmp)

    return OUTPUT_ODS


def create_initial():
    # 1. Create the spreadsheet with headers only
    ods_path = create_initial_ods()

    # 2. Set up Thunderbird emails
    mbox_path, local_folders_dir = setup_thunderbird_emails()

    print(f'\nInitial environment ready:')
    print(f'  Spreadsheet: {ods_path}')
    print(f'  Email mbox:  {mbox_path}')

    # 3. Launch Thunderbird first (so it registers the mbox on first run)
    launch_gui('thunderbird', delay_sec=4.0)

    # 4. Launch LibreOffice Calc with the initial spreadsheet
    launch_gui(f'libreoffice --calc "{ods_path}"', delay_sec=2.0)

    print('GUI_READY: launched Thunderbird and LibreOffice Calc with DISPLAY=:0')


create_initial()
