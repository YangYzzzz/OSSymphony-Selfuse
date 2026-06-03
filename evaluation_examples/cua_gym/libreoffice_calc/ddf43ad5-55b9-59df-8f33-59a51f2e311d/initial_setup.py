"""
Initial Setup: Multi-app email + LibreOffice Calc evaluation ranking task
Task ID: osworld_multi_apps_email_data_012
Domain: libreoffice_calc (multi-app: Thunderbird + LibreOffice Calc + Python)

Sets up Thunderbird with an 'Evaluations' folder containing 4 emails, each
with a plain-text attachment of performance scores. The agent must:
  1. Download attachments to /home/user/evaluations/
  2. Write a Python script to parse and rank the evaluators
  3. Save rankings.csv and open in LibreOffice Calc with formatting + RANK formula
  4. Reply to the top-ranked evaluator's email
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_data_012'

# Thunderbird profile path (typical OSWorld path)
TB_PROFILE_BASE = os.path.expanduser('~/.thunderbird')

# Evaluator data — 4 evaluators, 5 criteria each (scores 1-5)
EVALUATORS = [
    {
        'name': 'Dr. Emily Watson',
        'email': 'emily.watson@university.edu',
        'filename': 'evaluation_emily_watson.txt',
        'subject': 'Performance Evaluation - Q1 2025',
        'scores': {
            'Communication Skills': 5,
            'Technical Knowledge': 4,
            'Problem Solving': 5,
            'Teamwork': 4,
            'Leadership': 5,
        },
    },
    {
        'name': 'Prof. Marcus Chen',
        'email': 'marcus.chen@institute.org',
        'filename': 'evaluation_marcus_chen.txt',
        'subject': 'Performance Evaluation - Q1 2025',
        'scores': {
            'Communication Skills': 4,
            'Technical Knowledge': 3,
            'Problem Solving': 4,
            'Teamwork': 3,
            'Leadership': 4,
        },
    },
    {
        'name': 'Dr. Sarah Rivera',
        'email': 'sarah.rivera@research.edu',
        'filename': 'evaluation_sarah_rivera.txt',
        'subject': 'Performance Evaluation - Q1 2025',
        'scores': {
            'Communication Skills': 5,
            'Technical Knowledge': 5,
            'Problem Solving': 4,
            'Teamwork': 5,
            'Leadership': 5,
        },
    },
    {
        'name': 'James O\'Brien',
        'email': 'james.obrien@consulting.com',
        'filename': 'evaluation_james_obrien.txt',
        'subject': 'Performance Evaluation - Q1 2025',
        'scores': {
            'Communication Skills': 3,
            'Technical Knowledge': 4,
            'Problem Solving': 3,
            'Teamwork': 4,
            'Leadership': 3,
        },
    },
]


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def find_thunderbird_profile():
    """Find the default Thunderbird profile directory."""
    if not os.path.isdir(TB_PROFILE_BASE):
        return None
    profiles_ini = os.path.join(TB_PROFILE_BASE, 'profiles.ini')
    if not os.path.isfile(profiles_ini):
        return None
    # Parse profiles.ini to find default profile
    import configparser
    config = configparser.ConfigParser()
    config.read(profiles_ini)
    for section in config.sections():
        if 'Path' in config[section]:
            path = config[section]['Path']
            is_relative = config[section].get('IsRelative', '0') == '1'
            if is_relative:
                full_path = os.path.join(TB_PROFILE_BASE, path)
            else:
                full_path = path
            if os.path.isdir(full_path):
                return full_path
    return None


def create_mbox_email(evaluator, date_offset_days=0):
    """
    Create a properly formatted mbox email entry with an attached .txt file.
    The attachment contains performance scores.
    """
    import base64
    import email
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    name = evaluator['name']
    sender_email = evaluator['email']
    filename = evaluator['filename']
    subject = evaluator['subject']
    scores = evaluator['scores']

    # Build the attachment content
    lines = []
    for criterion, score in scores.items():
        lines.append(f'{criterion}: {score}')
    attachment_content = '\n'.join(lines) + '\n'

    # Email body text
    body_text = (
        f"Dear Evaluation Committee,\n\n"
        f"Please find attached my performance evaluation scores for Q1 2025.\n"
        f"I have carefully assessed each criterion based on the provided rubric.\n\n"
        f"Best regards,\n"
        f"{name}\n"
    )

    # Build MIME message
    msg = MIMEMultipart()
    msg['From'] = f'{name} <{sender_email}>'
    msg['To'] = 'evaluation.committee@company.com'
    msg['Subject'] = f'{subject}'

    # Offset dates so emails appear on different days
    from datetime import datetime, timedelta
    base_date = datetime(2025, 3, 10, 9, 0, 0) + timedelta(days=date_offset_days)
    date_str = base_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
    msg['Date'] = date_str

    # Attach body
    msg.attach(MIMEText(body_text, 'plain'))

    # Attach scores file
    att = MIMEBase('text', 'plain')
    att.set_payload(attachment_content.encode('utf-8'))
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(att)

    # Format as mbox entry
    mbox_from_line = f"From {sender_email} {base_date.strftime('%a %b %d %H:%M:%S %Y')}"
    return mbox_from_line + '\n' + msg.as_string() + '\n'


def setup_thunderbird_evaluations_folder(profile_dir):
    """
    Create an 'Evaluations' folder in Thunderbird's Local Folders with 4 emails.
    """
    # Local Folders path in Thunderbird
    local_folders_path = os.path.join(profile_dir, 'Mail', 'Local Folders')
    os.makedirs(local_folders_path, exist_ok=True)

    # Create the Evaluations mbox file
    evaluations_mbox = os.path.join(local_folders_path, 'Evaluations')
    evaluations_msf = os.path.join(local_folders_path, 'Evaluations.msf')

    # Write all 4 emails into the mbox file
    mbox_content = ''
    for i, evaluator in enumerate(EVALUATORS):
        mbox_content += create_mbox_email(evaluator, date_offset_days=i)

    with open(evaluations_mbox, 'w', encoding='utf-8') as f:
        f.write(mbox_content)

    # Create a minimal .msf index file (Thunderbird will regenerate it on startup)
    # Just create empty or minimal to signal folder exists
    if not os.path.isfile(evaluations_msf):
        with open(evaluations_msf, 'w') as f:
            f.write('# Netscape folder cache\n')

    print(f'Created Evaluations mbox at: {evaluations_mbox}')
    print(f'Mbox size: {os.path.getsize(evaluations_mbox)} bytes')


def ensure_no_evaluations_dir():
    """Ensure /home/user/evaluations/ does NOT exist — agent must create it."""
    eval_dir = os.path.join(WORKDIR, 'evaluations')
    if os.path.exists(eval_dir):
        shutil.rmtree(eval_dir)
        print(f'Removed pre-existing evaluations directory: {eval_dir}')


def create_initial():
    print('=== Setting up initial environment for task: osworld_multi_apps_email_data_012 ===')

    # 1. Ensure evaluations directory does NOT exist (agent must download and create it)
    ensure_no_evaluations_dir()

    # 2. Find or initialize Thunderbird profile
    profile_dir = find_thunderbird_profile()
    if profile_dir is None:
        print('Thunderbird profile not found. Launching Thunderbird briefly to create profile...')
        # Launch and kill to create default profile
        launch_gui('thunderbird', delay_sec=5.0)
        subprocess.run(['pkill', '-f', 'thunderbird'], capture_output=True)
        time.sleep(2)
        profile_dir = find_thunderbird_profile()

    if profile_dir is None:
        # Fallback: create profile directory manually
        fallback = os.path.join(TB_PROFILE_BASE, 'default.default')
        os.makedirs(fallback, exist_ok=True)
        profile_dir = fallback
        print(f'Using fallback profile dir: {profile_dir}')

    print(f'Using Thunderbird profile: {profile_dir}')

    # 3. Set up Evaluations folder with 4 emails
    setup_thunderbird_evaluations_folder(profile_dir)

    # 4. Remove any existing .msf cache files so Thunderbird rebuilds the index
    local_folders = os.path.join(profile_dir, 'Mail', 'Local Folders')
    msf_path = os.path.join(local_folders, 'Evaluations.msf')
    if os.path.isfile(msf_path):
        os.remove(msf_path)
        print(f'Removed stale .msf cache: {msf_path}')

    print('Initial environment setup complete.')
    print(f'  - Thunderbird Evaluations folder: 4 emails with .txt attachments')
    print(f'  - /home/user/evaluations/ does NOT exist (agent must create)')
    print()

    # 5. GUI-ready startup: open Thunderbird
    print('Launching Thunderbird...')
    launch_gui('thunderbird', delay_sec=3.0)
    print('GUI_READY: Thunderbird launched with DISPLAY=:0')


create_initial()
