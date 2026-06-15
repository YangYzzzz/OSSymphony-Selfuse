"""
Initial Setup: Multi-app expense report task
Task ID: osworld_multi_apps_email_data_009
Domain: libreoffice_calc (multi-app: Thunderbird + Python + LibreOffice Calc)

Creates:
  - Thunderbird 'Expense Reports' IMAP folder with 3 emails,
    each carrying a realistic CSV attachment (10-15 rows).
  - Launch Thunderbird to make it visible.
"""

import base64
import email as email_lib
import email.mime.multipart
import email.mime.text
import email.mime.base
from email import encoders
import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_data_009'

# ---------------------------------------------------------------------------
# CSV attachment content (10-15 rows each, realistic business expense data)
# ---------------------------------------------------------------------------

ALICE_CSV = """date,category,amount
2025-01-03,Travel,245.50
2025-01-05,Meals,38.75
2025-01-07,Software,129.00
2025-01-08,Meals,52.40
2025-01-10,Office Supplies,87.20
2025-01-12,Travel,312.00
2025-01-14,Meals,44.90
2025-01-15,Training,450.00
2025-01-17,Travel,198.60
2025-01-20,Office Supplies,23.15
2025-01-22,Meals,61.30
2025-01-24,Software,59.99
"""

BOB_CSV = """date,category,amount
2025-01-04,Travel,180.00
2025-01-06,Meals,29.50
2025-01-09,Office Supplies,54.75
2025-01-11,Software,199.00
2025-01-13,Meals,67.20
2025-01-15,Travel,425.80
2025-01-16,Training,320.00
2025-01-18,Meals,41.60
2025-01-19,Office Supplies,18.90
2025-01-21,Travel,260.40
2025-01-23,Software,89.99
2025-01-25,Meals,55.00
2025-01-27,Office Supplies,31.40
"""

CAROL_CSV = """date,category,amount
2025-01-02,Travel,310.50
2025-01-05,Meals,47.80
2025-01-08,Training,275.00
2025-01-10,Software,149.00
2025-01-12,Meals,38.60
2025-01-14,Travel,195.30
2025-01-16,Office Supplies,62.45
2025-01-18,Meals,53.20
2025-01-21,Software,79.99
2025-01-22,Travel,410.00
2025-01-24,Office Supplies,44.80
2025-01-26,Meals,36.70
2025-01-28,Training,180.00
2025-01-30,Travel,228.90
"""

# ---------------------------------------------------------------------------
# Helper: build a MIME email with one CSV attachment
# ---------------------------------------------------------------------------

def build_email_with_csv(
    from_addr: str,
    to_addr: str,
    subject: str,
    body: str,
    csv_filename: str,
    csv_content: str,
    date_str: str,
    msg_id: str,
) -> str:
    """Return a raw RFC-2822 message string ready for mbox."""
    msg = email.mime.multipart.MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg['Date'] = date_str
    msg['Message-ID'] = msg_id

    # Text body
    msg.attach(email.mime.text.MIMEText(body, 'plain'))

    # CSV attachment
    part = email.mime.base.MIMEBase('text', 'csv')
    part.set_payload(csv_content.encode('utf-8'))
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment',
                    filename=csv_filename)
    msg.attach(part)

    return msg.as_string()


# ---------------------------------------------------------------------------
# Locate the Thunderbird profile directory
# ---------------------------------------------------------------------------

def find_thunderbird_profile() -> Path:
    """Return path to the first Thunderbird profile directory."""
    profiles_ini = Path(WORKDIR) / '.thunderbird' / 'profiles.ini'
    if not profiles_ini.exists():
        raise FileNotFoundError(
            f'Thunderbird profiles.ini not found at {profiles_ini}. '
            'Please ensure Thunderbird is installed and has been launched at least once.'
        )

    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(str(profiles_ini))

    for section in cfg.sections():
        if section.startswith('Profile'):
            is_relative = cfg.get(section, 'IsRelative', fallback='0')
            path_val = cfg.get(section, 'Path', fallback=None)
            if path_val:
                if is_relative == '1':
                    return Path(WORKDIR) / '.thunderbird' / path_val
                else:
                    return Path(path_val)

    raise RuntimeError('No Thunderbird profile found in profiles.ini')


# ---------------------------------------------------------------------------
# Create the 'Expense Reports' mbox folder with 3 emails
# ---------------------------------------------------------------------------

def setup_thunderbird_folder():
    profile_dir = find_thunderbird_profile()
    print(f'Thunderbird profile: {profile_dir}')

    # Mail/Local Folders (fallback for pure IMAP setups we also try ImapMail)
    mail_dirs = [
        profile_dir / 'Mail' / 'Local Folders',
    ]
    # Try to find an existing account mail dir
    mail_base = profile_dir / 'Mail'
    if mail_base.exists():
        for sub in mail_base.iterdir():
            if sub.is_dir():
                mail_dirs.append(sub)
    imap_base = profile_dir / 'ImapMail'
    if imap_base.exists():
        for sub in imap_base.iterdir():
            if sub.is_dir():
                mail_dirs.append(sub)

    # Use the first existing dir, or create Local Folders
    target_mail_dir = None
    for d in mail_dirs:
        if d.exists():
            target_mail_dir = d
            break
    if target_mail_dir is None:
        target_mail_dir = profile_dir / 'Mail' / 'Local Folders'
        target_mail_dir.mkdir(parents=True, exist_ok=True)

    print(f'Using mail dir: {target_mail_dir}')

    # Build 3 emails
    emails_cfg = [
        {
            'from': 'alice@co.com',
            'subject': 'January Expense Report',
            'body': (
                'Hi,\n\nPlease find attached my expense report for January 2025.\n\n'
                'Total expenses: $1,702.79\n\nBest regards,\nAlice'
            ),
            'csv_name': 'alice.csv',
            'csv_content': ALICE_CSV,
            'date': 'Mon, 03 Feb 2025 09:14:00 +0000',
            'msg_id': '<alice-exp-jan-2025@co.com>',
        },
        {
            'from': 'bob@co.com',
            'subject': 'Expense Report - January 2025',
            'body': (
                'Hello,\n\nAttached is my expense report for January.\n\n'
                'Total: $1,773.54\n\nThanks,\nBob'
            ),
            'csv_name': 'bob.csv',
            'csv_content': BOB_CSV,
            'date': 'Tue, 04 Feb 2025 10:22:00 +0000',
            'msg_id': '<bob-exp-jan-2025@co.com>',
        },
        {
            'from': 'carol@co.com',
            'subject': 'My Expense Report for January',
            'body': (
                'Hi team,\n\nHere is my expense report CSV for January 2025.\n\n'
                'Total: $2,112.24\n\nCheers,\nCarol'
            ),
            'csv_name': 'carol.csv',
            'csv_content': CAROL_CSV,
            'date': 'Wed, 05 Feb 2025 08:45:00 +0000',
            'msg_id': '<carol-exp-jan-2025@co.com>',
        },
    ]

    # Build mbox content
    mbox_lines = []
    for cfg_item in emails_cfg:
        raw = build_email_with_csv(
            from_addr=cfg_item['from'],
            to_addr='user@localhost',
            subject=cfg_item['subject'],
            body=cfg_item['body'],
            csv_filename=cfg_item['csv_name'],
            csv_content=cfg_item['csv_content'],
            date_str=cfg_item['date'],
            msg_id=cfg_item['msg_id'],
        )
        # mbox separator line (From_ line)
        from_line = f"From {cfg_item['from']} {cfg_item['date']}"
        mbox_lines.append(from_line)
        mbox_lines.append(raw)
        mbox_lines.append('')  # blank line between messages

    mbox_content = '\n'.join(mbox_lines)

    # Write mbox file
    mbox_path = target_mail_dir / 'Expense Reports'
    mbox_path.write_text(mbox_content, encoding='utf-8')
    print(f'mbox file written: {mbox_path}')

    # Remove stale msf index so Thunderbird re-reads the mbox
    msf_path = target_mail_dir / 'Expense Reports.msf'
    if msf_path.exists():
        msf_path.unlink()
        print(f'Removed stale index: {msf_path}')

    return target_mail_dir


# ---------------------------------------------------------------------------
# GUI helper
# ---------------------------------------------------------------------------

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app non-blocking, using DISPLAY=:0."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def create_initial():
    # 1. Set up Thunderbird folder with emails
    setup_thunderbird_folder()
    print('Thunderbird Expense Reports folder populated.')

    # 2. Ensure expected directories do NOT pre-exist
    #    (agent must create /home/user/expenses/ and /home/user/scripts/)
    for d in [f'{WORKDIR}/expenses', f'{WORKDIR}/scripts']:
        p = Path(d)
        if p.exists() and p.is_dir():
            # Only remove if empty (don't clobber existing user data)
            try:
                p.rmdir()
                print(f'Removed empty dir: {d}')
            except OSError:
                # Not empty — leave it alone; agent will work within it
                print(f'Directory not empty, leaving: {d}')

    # 3. Launch Thunderbird (with the Expense Reports folder visible)
    launch_gui('thunderbird', delay_sec=3.0)
    print('GUI_READY: Thunderbird launched with DISPLAY=:0')


create_initial()
