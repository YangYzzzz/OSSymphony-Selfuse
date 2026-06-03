"""
Initial Setup: Process emails with CSV attachments in Thunderbird Receipts folder
Task ID: osworld_multi_apps_email_file_convert_008
Domain: multi_apps (Thunderbird + Python scripting + LibreOffice Calc)

This script:
1. Creates a local Thunderbird mail folder 'Receipts' with 5 emails, each containing a CSV attachment
2. Ensures /home/user/receipts/ directory does NOT exist (so the agent can create it)
3. Opens Thunderbird with the Receipts folder visible
"""

import os
import shlex
import subprocess
import time
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mailbox
import io
import csv

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_008'


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


def create_csv_content(rows_data):
    """Create CSV content as bytes."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['date', 'vendor', 'amount'])
    for row in rows_data:
        writer.writerow(row)
    return output.getvalue().encode('utf-8')


def create_email_with_attachment(from_addr, to_addr, subject, body, csv_filename, csv_content, date_str):
    """Create a MIME email with a CSV attachment."""
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg['Date'] = date_str
    msg['Message-ID'] = f'<{hash(subject) % 10**10}@receipts.example.com>'

    # Email body
    msg.attach(MIMEText(body, 'plain'))

    # CSV attachment
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_content)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{csv_filename}"')
    msg.attach(part)

    return msg


def setup_thunderbird_receipts_folder():
    """
    Create a Thunderbird 'Receipts' mail folder with 5 emails.
    Uses Thunderbird's mbox format in the default profile.
    """
    # Find Thunderbird profile directory
    tb_profiles_base = os.path.expanduser('~/.thunderbird')

    if not os.path.exists(tb_profiles_base):
        os.makedirs(tb_profiles_base, exist_ok=True)

    # Find profile directory
    profile_dir = None
    profiles_ini = os.path.join(tb_profiles_base, 'profiles.ini')

    if os.path.exists(profiles_ini):
        with open(profiles_ini, 'r') as f:
            content = f.read()
        # Parse profiles.ini to find profile path
        import configparser
        config = configparser.ConfigParser()
        config.read(profiles_ini)
        for section in config.sections():
            if section.startswith('Profile'):
                path_val = config.get(section, 'Path', fallback=None)
                is_relative = config.get(section, 'IsRelative', fallback='0')
                if path_val:
                    if is_relative == '1':
                        profile_dir = os.path.join(tb_profiles_base, path_val)
                    else:
                        profile_dir = path_val
                    break

    if not profile_dir or not os.path.exists(profile_dir):
        # Create a default profile
        profile_dir = os.path.join(tb_profiles_base, 'default.profile')
        os.makedirs(profile_dir, exist_ok=True)
        with open(profiles_ini, 'w') as f:
            f.write('[General]\nStartWithLastProfile=1\n\n[Profile0]\nName=default\nIsRelative=1\nPath=default.profile\nDefault=1\n')

    # Mail directory within profile
    mail_dir = os.path.join(profile_dir, 'Mail', 'Local Folders')
    os.makedirs(mail_dir, exist_ok=True)

    # Email data: 5 senders with CSV data
    emails_data = [
        {
            'from': 'billing@techsupplies.com',
            'from_name': 'Tech Supplies Billing',
            'date': 'Mon, 03 Feb 2025 10:15:23 +0000',
            'subject': 'Receipt - February 2025 Tech Supplies Order',
            'body': 'Please find attached your receipt for your recent purchase from Tech Supplies.',
            'csv_filename': 'receipt_feb_techsupplies.csv',
            'csv_rows': [
                ['2025-02-03', 'Tech Supplies Inc', '245.99'],
                ['2025-02-03', 'Tech Supplies Inc', '89.50'],
                ['2025-02-03', 'Tech Supplies Inc', '34.75'],
            ]
        },
        {
            'from': 'orders@officepro.net',
            'from_name': 'Office Pro Orders',
            'date': 'Wed, 12 Feb 2025 14:30:00 +0000',
            'subject': 'Your Office Pro Purchase Receipt',
            'body': 'Thank you for shopping at Office Pro. Your receipt is attached.',
            'csv_filename': 'officepro_purchase_receipt.csv',
            'csv_rows': [
                ['2025-02-12', 'Office Pro Network', '127.80'],
                ['2025-02-12', 'Office Pro Network', '56.40'],
                ['2025-02-12', 'Office Pro Network', '199.99'],
                ['2025-02-12', 'Office Pro Network', '23.15'],
                ['2025-02-12', 'Office Pro Network', '44.60'],
            ]
        },
        {
            'from': 'receipts@cloudservices.io',
            'from_name': 'Cloud Services Receipts',
            'date': 'Thu, 20 Feb 2025 09:00:00 +0000',
            'subject': 'Cloud Services Monthly Invoice Receipt',
            'body': 'Attached is your monthly cloud services receipt.',
            'csv_filename': 'cloud_services_receipt.csv',
            'csv_rows': [
                ['2025-02-20', 'Cloud Services IO', '350.00'],
                ['2025-02-20', 'Cloud Services IO', '75.00'],
                ['2025-02-20', 'Cloud Services IO', '125.50'],
                ['2025-02-20', 'Cloud Services IO', '45.00'],
            ]
        },
        {
            'from': 'noreply@printshop.com',
            'from_name': 'Print Shop',
            'date': 'Fri, 21 Feb 2025 16:45:00 +0000',
            'subject': 'Print Shop Order Confirmation Receipt',
            'body': 'Your print order receipt is enclosed.',
            'csv_filename': 'printshop_order.csv',
            'csv_rows': [
                ['2025-02-21', 'The Print Shop', '88.25'],
                ['2025-02-21', 'The Print Shop', '142.00'],
                ['2025-02-21', 'The Print Shop', '67.30'],
                ['2025-02-21', 'The Print Shop', '29.99'],
                ['2025-02-21', 'The Print Shop', '215.60'],
                ['2025-02-21', 'The Print Shop', '55.00'],
                ['2025-02-21', 'The Print Shop', '38.75'],
            ]
        },
        {
            'from': 'invoices@designstudio.co',
            'from_name': 'Design Studio',
            'date': 'Mon, 24 Feb 2025 11:20:00 +0000',
            'subject': 'Design Studio Invoice Receipt - Project Alpha',
            'body': 'Please find your invoice receipt for Project Alpha.',
            'csv_filename': 'design_studio_invoice.csv',
            'csv_rows': [
                ['2025-02-24', 'Design Studio Co', '500.00'],
                ['2025-02-24', 'Design Studio Co', '250.00'],
                ['2025-02-24', 'Design Studio Co', '175.00'],
                ['2025-02-24', 'Design Studio Co', '85.50'],
            ]
        },
    ]

    # Create the Receipts mbox file
    receipts_mbox_path = os.path.join(mail_dir, 'Receipts')

    # Build mbox content
    mbox_content = ''
    for edata in emails_data:
        csv_content = create_csv_content(edata['csv_rows'])
        msg = create_email_with_attachment(
            from_addr=f"{edata['from_name']} <{edata['from']}>",
            to_addr='user@localhost',
            subject=edata['subject'],
            body=edata['body'],
            csv_filename=edata['csv_filename'],
            csv_content=csv_content,
            date_str=edata['date']
        )
        msg_str = msg.as_string()
        # mbox format: each message starts with "From " line
        mbox_content += f"From {edata['from']} {edata['date']}\n"
        mbox_content += msg_str
        mbox_content += '\n'

    with open(receipts_mbox_path, 'w') as f:
        f.write(mbox_content)

    # Create empty .msf index file for the mbox (Thunderbird summary file)
    msf_path = receipts_mbox_path + '.msf'
    if not os.path.exists(msf_path):
        with open(msf_path, 'w') as f:
            f.write('// <!-- <mdb:mork:z v="1.4"/> -->\n')

    print(f'Thunderbird Receipts mbox created: {receipts_mbox_path}')
    print(f'  Contains {len(emails_data)} emails with CSV attachments')

    return profile_dir, mail_dir


def cleanup_existing_receipts_dir():
    """Remove any existing receipts directory to ensure clean start state."""
    receipts_dir = os.path.join(WORKDIR, 'receipts')
    if os.path.exists(receipts_dir):
        import shutil
        shutil.rmtree(receipts_dir)
        print(f'Removed existing receipts directory: {receipts_dir}')


def create_initial():
    # 1. Clean up any previous receipts work directory
    cleanup_existing_receipts_dir()

    # 2. Set up Thunderbird with Receipts folder
    profile_dir, mail_dir = setup_thunderbird_receipts_folder()

    print(f'Setup complete:')
    print(f'  Thunderbird profile: {profile_dir}')
    print(f'  Mail directory: {mail_dir}')
    print(f'  Receipts folder with 5 emails (each has a CSV attachment)')
    print(f'  /home/user/receipts/ does NOT exist (agent must create it)')

    # 3. GUI-ready startup: open Thunderbird
    # Kill any existing Thunderbird instances first
    subprocess.run(['pkill', '-f', 'thunderbird'], capture_output=True)
    time.sleep(1.0)

    launch_gui('thunderbird', delay_sec=3.0)
    print('GUI_READY: launched Thunderbird with DISPLAY=:0')


create_initial()
