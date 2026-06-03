"""
Initial Setup: Thunderbird Projects folder with 9 emails for export task
Task ID: osworld_multi_apps_email_file_convert_005
Domain: multi_apps (Thunderbird + terminal)

Creates a Thunderbird Local Folders 'Projects' folder with 9 emails,
4 of which contain 'deadline' in their body/subject.
The agent must export these emails as .eml files and find the deadline ones.
"""

import os
import shlex
import subprocess
import time
import glob

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_005'
PROFILE_DIR = '/home/user/.thunderbird/wtkk3c2w.default-release'
MAIL_DIR = f'{PROFILE_DIR}/Mail/Local Folders'


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


def build_mbox_message(msg_id, from_addr, to_addr, subject, date_str, body):
    """Build a single mbox-format email message."""
    # mbox format: starts with "From " line (note: no colon)
    from_line = f"From {from_addr} {date_str}\n"
    headers = (
        f"Message-ID: <{msg_id}@projects.local>\n"
        f"From: {from_addr}\n"
        f"To: {to_addr}\n"
        f"Subject: {subject}\n"
        f"Date: {date_str}\n"
        f"MIME-Version: 1.0\n"
        f"Content-Type: text/plain; charset=UTF-8\n"
        f"Content-Transfer-Encoding: 7bit\n"
        f"\n"
    )
    # Ensure no line starts with "From " (mbox quoting) — escape if needed
    quoted_body = "\n".join(
        (">" + line if line.startswith("From ") else line)
        for line in body.splitlines()
    )
    return from_line + headers + quoted_body + "\n\n"


def create_projects_mbox():
    """Create the Projects mbox file with 9 emails, 4 containing 'deadline'."""
    os.makedirs(MAIL_DIR, exist_ok=True)

    # Define 9 emails: first 4 contain 'deadline', last 5 do not
    emails = [
        # Emails WITH 'deadline' (4 total)
        {
            "msg_id": "proj001",
            "from": "alice.morgan@techcorp.com",
            "to": "user@projects.local",
            "subject": "Q3 Project Deadline Reminder",
            "date": "Mon, 15 Jan 2025 09:00:00 +0000",
            "body": (
                "Hi team,\n\n"
                "Just a reminder that the Q3 project deadline is approaching.\n"
                "Please submit all deliverables by January 31st, 2025.\n\n"
                "The deadline for the main milestone is firm — no extensions.\n\n"
                "Best regards,\nAlice Morgan\nProject Lead"
            ),
        },
        {
            "msg_id": "proj002",
            "from": "brian.lee@techcorp.com",
            "to": "user@projects.local",
            "subject": "Website Redesign - Status Update",
            "date": "Tue, 16 Jan 2025 14:30:00 +0000",
            "body": (
                "Hi,\n\n"
                "Quick update on the website redesign project.\n"
                "The deadline for wireframe completion is January 20th.\n"
                "Our contractor has confirmed they can meet the deadline.\n\n"
                "Please review the attached mockups and provide feedback before EOD.\n\n"
                "Thanks,\nBrian Lee\nUI/UX Team"
            ),
        },
        {
            "msg_id": "proj003",
            "from": "carol.chen@techcorp.com",
            "to": "user@projects.local",
            "subject": "Budget Approval Required",
            "date": "Wed, 17 Jan 2025 11:15:00 +0000",
            "body": (
                "Hello,\n\n"
                "The budget proposal for Project Alpha requires your approval.\n"
                "We have a hard deadline of January 22nd to submit to finance.\n\n"
                "Total requested: $45,000 for Q1 activities.\n"
                "Missing this deadline will delay the project by 6 weeks.\n\n"
                "Please review and sign off ASAP.\n\n"
                "Regards,\nCarol Chen\nFinance Coordinator"
            ),
        },
        {
            "msg_id": "proj004",
            "from": "david.kim@techcorp.com",
            "to": "user@projects.local",
            "subject": "Code Review Assignments",
            "date": "Thu, 18 Jan 2025 16:45:00 +0000",
            "body": (
                "Team,\n\n"
                "Please see your code review assignments below.\n"
                "All reviews must be completed before the release deadline.\n"
                "The release deadline is January 25th at midnight.\n\n"
                "- Module A: Assigned to David Kim\n"
                "- Module B: Assigned to Sarah Walsh\n"
                "- Module C: Assigned to James Park\n\n"
                "Submit your review comments in JIRA.\n\n"
                "David Kim\nTech Lead"
            ),
        },
        # Emails WITHOUT 'deadline' (5 total)
        {
            "msg_id": "proj005",
            "from": "emily.wang@techcorp.com",
            "to": "user@projects.local",
            "subject": "Team Lunch Next Friday",
            "date": "Fri, 19 Jan 2025 10:00:00 +0000",
            "body": (
                "Hi everyone,\n\n"
                "We're planning a team lunch next Friday at noon.\n"
                "Proposed venue: The Green Garden Restaurant on 5th Ave.\n\n"
                "Please RSVP by Wednesday so we can make a reservation.\n"
                "Looking forward to seeing everyone!\n\n"
                "Cheers,\nEmily Wang\nOffice Manager"
            ),
        },
        {
            "msg_id": "proj006",
            "from": "frank.ozzy@techcorp.com",
            "to": "user@projects.local",
            "subject": "New Tool License Available",
            "date": "Mon, 22 Jan 2025 08:30:00 +0000",
            "body": (
                "Hello,\n\n"
                "We have acquired 5 new licenses for the project management tool Asana.\n"
                "Please reply if you need access and I will assign one to you.\n\n"
                "The tool includes features for task tracking, collaboration, and reporting.\n"
                "Training session will be scheduled next week.\n\n"
                "Best,\nFrank Ozzy\nIT Manager"
            ),
        },
        {
            "msg_id": "proj007",
            "from": "grace.liu@techcorp.com",
            "to": "user@projects.local",
            "subject": "Project Alpha - Kickoff Meeting Notes",
            "date": "Tue, 23 Jan 2025 13:00:00 +0000",
            "body": (
                "Hi team,\n\n"
                "Here are the notes from today's kickoff meeting for Project Alpha.\n\n"
                "Attendees: Grace Liu, Frank Ozzy, David Kim, Carol Chen\n\n"
                "Key decisions:\n"
                "1. Technology stack: React + Node.js\n"
                "2. Sprint duration: 2 weeks\n"
                "3. Daily standups at 9 AM\n"
                "4. GitHub for version control\n\n"
                "Next meeting: February 5th, 2025\n\n"
                "Grace Liu\nScrum Master"
            ),
        },
        {
            "msg_id": "proj008",
            "from": "henry.park@techcorp.com",
            "to": "user@projects.local",
            "subject": "Server Maintenance Window",
            "date": "Wed, 24 Jan 2025 07:00:00 +0000",
            "body": (
                "All,\n\n"
                "We will be performing scheduled server maintenance this Saturday.\n"
                "Maintenance window: Saturday January 27th, 2 AM - 6 AM UTC.\n\n"
                "During this time, the development environment will be unavailable.\n"
                "Please plan your work accordingly.\n\n"
                "Contact the IT support team if you have questions.\n\n"
                "Henry Park\nSystems Administrator"
            ),
        },
        {
            "msg_id": "proj009",
            "from": "iris.north@techcorp.com",
            "to": "user@projects.local",
            "subject": "Client Presentation Slides Ready",
            "date": "Thu, 25 Jan 2025 15:30:00 +0000",
            "body": (
                "Hi,\n\n"
                "The slides for the client presentation on February 3rd are ready.\n"
                "You can find them in the shared drive under /Presentations/Q1-2025/.\n\n"
                "Total: 22 slides covering product overview, technical architecture, and pricing.\n"
                "Please review and send any feedback by Monday.\n\n"
                "Looking forward to a successful presentation!\n\n"
                "Best,\nIris North\nSales Engineer"
            ),
        },
    ]

    # Build the mbox content
    mbox_content = ""
    for email in emails:
        mbox_content += build_mbox_message(
            msg_id=email["msg_id"],
            from_addr=email["from"],
            to_addr=email["to"],
            subject=email["subject"],
            date_str=email["date"],
            body=email["body"],
        )

    projects_mbox_path = f'{MAIL_DIR}/Projects'
    with open(projects_mbox_path, 'w', encoding='utf-8') as f:
        f.write(mbox_content)
    print(f'Created Projects mbox: {projects_mbox_path}')

    # Create the .msf index file (empty summary file — Thunderbird will rebuild)
    with open(f'{projects_mbox_path}.msf', 'w') as f:
        f.write('')
    print(f'Created Projects.msf index file')

    # Create Inbox and Trash mbox files (required for Local Folders structure)
    for folder_name in ['Inbox', 'Trash']:
        folder_path = f'{MAIL_DIR}/{folder_name}'
        if not os.path.exists(folder_path):
            with open(folder_path, 'w') as f:
                f.write('')
            with open(f'{folder_path}.msf', 'w') as f:
                f.write('')
    print('Created Inbox and Trash folders')

    return projects_mbox_path


def configure_thunderbird_prefs():
    """Add Local Folders account configuration to Thunderbird prefs.js."""
    prefs_path = f'{PROFILE_DIR}/prefs.js'

    # Read existing prefs
    with open(prefs_path, 'r') as f:
        content = f.read()

    # Only add if not already configured
    if 'mail.account.account1' in content:
        print('Thunderbird accounts already configured, skipping prefs update')
        return

    # Local Folders account configuration for Thunderbird
    # account1 = local folders pseudo-account
    # server1 = local folders mail store
    local_folders_prefs = f"""
user_pref("mail.account.account1.server", "server1");
user_pref("mail.account.account1.identities", "id1");
user_pref("mail.accountmanager.accounts", "account1");
user_pref("mail.accountmanager.localfoldersserver", "server1");
user_pref("mail.identity.id1.fullName", "User");
user_pref("mail.identity.id1.smtpServer", "");
user_pref("mail.identity.id1.useremail", "user@projects.local");
user_pref("mail.server.server1.directory-rel", "[ProfD]Mail/Local Folders");
user_pref("mail.server.server1.hostname", "Local Folders");
user_pref("mail.server.server1.login_at_startup", false);
user_pref("mail.server.server1.name", "Local Folders");
user_pref("mail.server.server1.type", "none");
user_pref("mail.server.server1.userName", "nobody");
"""

    # Append new prefs before the end
    content = content.rstrip() + "\n" + local_folders_prefs.strip() + "\n"
    with open(prefs_path, 'w') as f:
        f.write(content)
    print(f'Updated Thunderbird prefs.js with Local Folders account')


def create_initial():
    print(f'=== Initial Setup: {TASK_ID} ===')

    # 1. Create the Projects mbox in Thunderbird Local Folders
    projects_mbox = create_projects_mbox()

    # 2. Configure Thunderbird to recognize the Local Folders account
    configure_thunderbird_prefs()

    # 3. Verify the mbox was created with content
    size = os.path.getsize(projects_mbox)
    print(f'Projects mbox size: {size} bytes')
    assert size > 1000, f'Projects mbox too small: {size} bytes'

    # 4. Verify backup directory does NOT exist (agent must create it)
    backup_dir = f'{WORKDIR}/projects_email_backup'
    if os.path.exists(backup_dir):
        import shutil
        shutil.rmtree(backup_dir)
        print(f'Removed pre-existing backup dir: {backup_dir}')

    # 5. Verify deadline_emails.txt does NOT exist (agent must create it)
    deadline_file = f'{WORKDIR}/deadline_emails.txt'
    if os.path.exists(deadline_file):
        os.remove(deadline_file)
        print(f'Removed pre-existing deadline_emails.txt')

    # 6. Kill any running Thunderbird instance before launching fresh
    subprocess.run(['pkill', '-f', 'thunderbird'], capture_output=True)
    time.sleep(2.0)

    # 7. Launch Thunderbird to show the Projects folder
    launch_gui('thunderbird', delay_sec=3.0)
    print('GUI_READY: launched Thunderbird with DISPLAY=:0')

    print(f'=== Setup complete ===')
    print(f'  Projects mbox: {projects_mbox} (9 emails, 4 with deadline)')
    print(f'  Backup dir: {backup_dir} (does not exist - agent must create)')
    print(f'  Deadline file: {deadline_file} (does not exist - agent must create)')


create_initial()
