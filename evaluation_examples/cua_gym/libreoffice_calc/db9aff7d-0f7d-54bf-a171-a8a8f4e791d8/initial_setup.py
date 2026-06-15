"""
Initial Setup: Archive Thunderbird 'Client Contracts' emails to .eml files and process with LibreOffice Calc
Task ID: osworld_multi_apps_email_file_convert_007
Domain: libreoffice_calc (multi-app: Thunderbird + Python + LibreOffice Calc)

This script sets up:
1. Thunderbird profile with 'Client Contracts' folder containing 6 realistic emails (some with attachments)
2. Opens Thunderbird so the agent can see the email client
"""

import os
import shlex
import subprocess
import time
import textwrap

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_007'


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


def run_cmd(cmd, check=True):
    """Run a shell command."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"  STDOUT: {result.stdout}")
        print(f"  STDERR: {result.stderr}")
    return result


def create_email_mbox():
    """Create Thunderbird profile with Client Contracts folder containing 6 realistic emails."""

    # Find or create Thunderbird profile directory
    tb_dir = f"{WORKDIR}/.thunderbird"
    os.makedirs(tb_dir, exist_ok=True)

    # Create a default profile
    profiles_ini = f"{tb_dir}/profiles.ini"
    profile_name = "default.setup"
    profile_dir = f"{tb_dir}/{profile_name}"
    os.makedirs(profile_dir, exist_ok=True)

    # Write profiles.ini
    with open(profiles_ini, 'w') as f:
        f.write(f"""[General]
StartWithLastProfile=1

[Profile0]
Name=default
IsRelative=1
Path={profile_name}
Default=1
""")

    # Create Local Folders Mail directory
    mail_dir = f"{profile_dir}/Mail/Local Folders"
    os.makedirs(mail_dir, exist_ok=True)

    # Define 6 realistic client contract emails
    emails = [
        {
            "message_id": "msg001@nexuscorp.com",
            "from": "Victoria Sterling <v.sterling@nexuscorp.com>",
            "to": "contracts@ourlegalteam.com",
            "date": "Mon, 06 Jan 2025 09:15:00 +0000",
            "subject": "Service Agreement - NexusCorp Q1 2025",
            "body": textwrap.dedent("""\
                Dear Contracts Team,

                Please find attached the signed service agreement for NexusCorp Q1 2025.
                The contract covers consulting services from January through March 2025,
                with a total value of $125,000.

                Please review and confirm receipt at your earliest convenience.

                Best regards,
                Victoria Sterling
                VP of Operations, NexusCorp
            """),
            "has_attachment": True,
            "attachment_name": "NexusCorp_Q1_2025_Service_Agreement.pdf",
        },
        {
            "message_id": "msg002@alphadynamics.net",
            "from": "Marcus Webb <m.webb@alphadynamics.net>",
            "to": "contracts@ourlegalteam.com",
            "date": "Wed, 15 Jan 2025 14:30:00 +0000",
            "subject": "Software License Contract - AlphaDynamics",
            "body": textwrap.dedent("""\
                Hello,

                Attached is the executed software license contract for AlphaDynamics.
                This covers 50 enterprise seats of our analytics platform for calendar year 2025.
                Annual license fee: $89,500.

                Please note the renewal clause in Section 7.3.

                Regards,
                Marcus Webb
                Procurement Director, AlphaDynamics
            """),
            "has_attachment": True,
            "attachment_name": "AlphaDynamics_Software_License_2025.pdf",
        },
        {
            "message_id": "msg003@brightwave.io",
            "from": "Sophia Hartmann <s.hartmann@brightwave.io>",
            "to": "contracts@ourlegalteam.com",
            "date": "Fri, 24 Jan 2025 11:00:00 +0000",
            "subject": "Re: Amendment to Consulting Agreement",
            "body": textwrap.dedent("""\
                Hi,

                Following our discussion on January 22nd, please find the amendment
                to our consulting agreement. Key changes include:
                - Extended project timeline to April 30, 2025
                - Revised payment schedule (milestone-based)
                - Added IP ownership clause (Section 12)

                The amended total project value is now $210,000.

                Thank you,
                Sophia Hartmann
                Legal Counsel, BrightWave Technologies
            """),
            "has_attachment": False,
            "attachment_name": None,
        },
        {
            "message_id": "msg004@peaklogistics.com",
            "from": "Daniel Okafor <d.okafor@peaklogistics.com>",
            "to": "contracts@ourlegalteam.com",
            "date": "Tue, 04 Feb 2025 16:45:00 +0000",
            "subject": "Logistics Partnership Contract 2025-2026",
            "body": textwrap.dedent("""\
                Good afternoon,

                Please review and execute the attached partnership contract for our
                two-year logistics collaboration. This contract governs the distribution
                agreement effective March 1, 2025 through February 28, 2027.

                Contract value: $340,000 per annum.
                Payment terms: Net 30.

                We look forward to a successful partnership.

                Best,
                Daniel Okafor
                CEO, Peak Logistics Group
            """),
            "has_attachment": True,
            "attachment_name": "Peak_Logistics_Partnership_Contract_2025-2026.docx",
        },
        {
            "message_id": "msg005@stellarmedical.org",
            "from": "Priya Nair <p.nair@stellarmedical.org>",
            "to": "contracts@ourlegalteam.com",
            "date": "Mon, 10 Feb 2025 08:20:00 +0000",
            "subject": "Healthcare Data Processing Agreement",
            "body": textwrap.dedent("""\
                Dear Legal Team,

                Attached please find the fully executed HIPAA-compliant data processing
                agreement between Stellar Medical Group and your organization.

                This agreement covers the processing of anonymized patient analytics
                data for research purposes, effective immediately through December 31, 2025.

                Please ensure compliance with Article 28 provisions.

                Sincerely,
                Priya Nair
                Chief Compliance Officer, Stellar Medical Group
            """),
            "has_attachment": True,
            "attachment_name": "Stellar_Medical_Data_Processing_Agreement.pdf",
        },
        {
            "message_id": "msg006@zenithcapital.co",
            "from": "Oliver Chen <o.chen@zenithcapital.co>",
            "to": "contracts@ourlegalteam.com",
            "date": "Thu, 20 Feb 2025 10:00:00 +0000",
            "subject": "Investment Advisory Services Contract",
            "body": textwrap.dedent("""\
                Hello,

                Thank you for your patience during negotiations. Enclosed is the
                finalized investment advisory services contract for Zenith Capital Partners.

                Services include: quarterly portfolio review, risk assessment reporting,
                and regulatory compliance advisory. Contract term: 18 months.
                Retainer: $15,000/month.

                Please return one signed copy at your earliest convenience.

                Kind regards,
                Oliver Chen
                Managing Partner, Zenith Capital Partners
            """),
            "has_attachment": False,
            "attachment_name": None,
        },
    ]

    # Build the mbox file for 'Client Contracts' folder
    mbox_path = f"{mail_dir}/Client Contracts"
    with open(mbox_path, 'w') as mbox:
        for email in emails:
            # Write mbox From_ line (separator)
            mbox.write(f"From MAILER-DAEMON {email['date']}\n")
            # Write headers
            mbox.write(f"Message-ID: <{email['message_id']}>\n")
            mbox.write(f"From: {email['from']}\n")
            mbox.write(f"To: {email['to']}\n")
            mbox.write(f"Date: {email['date']}\n")
            mbox.write(f"Subject: {email['subject']}\n")
            mbox.write("MIME-Version: 1.0\n")

            if email['has_attachment']:
                boundary = f"==============={email['message_id'].replace('@', '').replace('.', '')}=="
                mbox.write(f'Content-Type: multipart/mixed; boundary="{boundary}"\n')
                mbox.write("\n")
                mbox.write(f"--{boundary}\n")
                mbox.write("Content-Type: text/plain; charset=utf-8\n")
                mbox.write("Content-Transfer-Encoding: 8bit\n")
                mbox.write("\n")
                mbox.write(email['body'])
                mbox.write("\n")
                mbox.write(f"--{boundary}\n")
                mbox.write(f'Content-Type: application/octet-stream; name="{email["attachment_name"]}"\n')
                mbox.write("Content-Transfer-Encoding: base64\n")
                mbox.write(f'Content-Disposition: attachment; filename="{email["attachment_name"]}"\n')
                mbox.write("\n")
                # Minimal base64 placeholder for the attachment
                mbox.write("JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmoKPDwvTGVuZ3RoIDMgMCBSL0ZpbHRlci9GbGF0ZURl\n")
                mbox.write("Y29kZT4+CnN0cmVhbQp4nCvkMlAwUDC1NNUzMlcwslAwslIwtVAwNAcAGzUFCgplbmRzdHJlYW0K\n")
                mbox.write("\n")
                mbox.write(f"--{boundary}--\n")
            else:
                mbox.write("Content-Type: text/plain; charset=utf-8\n")
                mbox.write("Content-Transfer-Encoding: 8bit\n")
                mbox.write("\n")
                mbox.write(email['body'])
                mbox.write("\n")

            # Empty line between messages
            mbox.write("\n")

    print(f"Created mbox with 6 emails: {mbox_path}")

    # Create the .msf index file (required by Thunderbird to recognize the folder)
    msf_path = f"{mail_dir}/Client Contracts.msf"
    with open(msf_path, 'w') as f:
        f.write("// <!-- <mdb:mork:z v=\"1.4\"/> -->\n")
        f.write("< <(a=c)> // (f=iso-8859-1))\n")
        f.write("  (B8=Client Contracts)(4=Subject)(2=From)(3=Date)\n")
        f.write("  (5=To)(6=Message-ID)(7=Size)(9=Flags)(A=Priority)\n")
        f.write("  (82=numMsgs)(83=numNewMsgs)(84=folderSize)\n")
        f.write("  (85=expungedBytes)(86=folderDate)(87=highWaterKey)\n")
        f.write("  (88=totalMsgsInDB)(89=msgsWithInvalidDBValues)\n")
        f.write(">\n")

    print(f"Created MSF index: {msf_path}")

    # Create prefs.js for the Thunderbird profile
    prefs_path = f"{profile_dir}/prefs.js"
    with open(prefs_path, 'w') as f:
        f.write('// Mozilla User Preferences\n')
        f.write('/* Do not edit this file.\n')
        f.write(' *\n')
        f.write(' * If you make changes to this file while the application is running,\n')
        f.write(' * the changes will be overwritten when the application exits.\n')
        f.write(' *\n')
        f.write(' * To make a change to preferences, you can either:\n')
        f.write(' * - modify it via the UI (e.g. via about:config in the browser); or\n')
        f.write(' * - set it within a user.js file in your profile.\n')
        f.write(' */\n')
        f.write('\n')
        f.write('user_pref("mail.account.account1.identities", "id1");\n')
        f.write('user_pref("mail.account.account1.server", "server1");\n')
        f.write('user_pref("mail.accountmanager.accounts", "account1");\n')
        f.write('user_pref("mail.accountmanager.defaultaccount", "account1");\n')
        f.write('user_pref("mail.identity.id1.fullName", "Contracts Team");\n')
        f.write('user_pref("mail.identity.id1.useremail", "contracts@ourlegalteam.com");\n')
        f.write('user_pref("mail.identity.id1.valid", true);\n')
        f.write('user_pref("mail.server.server1.directory-rel", "[ProfD]Mail/Local Folders");\n')
        f.write('user_pref("mail.server.server1.hostname", "Local Folders");\n')
        f.write('user_pref("mail.server.server1.name", "Local Folders");\n')
        f.write('user_pref("mail.server.server1.type", "none");\n')
        f.write('user_pref("mail.server.server1.userName", "nobody");\n')
        f.write('user_pref("mail.startup.enabledMailCheckOnce", true);\n')
        f.write('user_pref("mailnews.start_page.enabled", false);\n')

    print(f"Created Thunderbird prefs: {prefs_path}")

    # Update installs.ini to point to our new profile (override existing Locked profile)
    installs_ini_path = f"{tb_dir}/installs.ini"
    if os.path.exists(installs_ini_path):
        with open(installs_ini_path, 'r') as f:
            content = f.read()
        # Find the section and update Default/Locked
        import re
        # Replace Default=<anything> with our profile
        content = re.sub(r'^Default=.*$', f'Default={profile_name}', content, flags=re.MULTILINE)
        # Remove Locked line to allow our profile to load
        content = re.sub(r'^Locked=.*\n?', '', content, flags=re.MULTILINE)
        with open(installs_ini_path, 'w') as f:
            f.write(content)
        print(f"Updated installs.ini to use profile: {profile_name}")

    return profile_dir


def create_initial():
    print("Setting up initial environment for osworld_multi_apps_email_file_convert_007")

    # Ensure contracts_backup does NOT exist (task requires agent to create it)
    backup_dir = f"{WORKDIR}/contracts_backup"
    if os.path.exists(backup_dir):
        import shutil
        shutil.rmtree(backup_dir)
        print(f"Removed pre-existing: {backup_dir}")

    # Ensure scripts directory does NOT have the parse script (agent creates it)
    script_path = f"{WORKDIR}/scripts/parse_contracts_eml.py"
    if os.path.exists(script_path):
        os.remove(script_path)
        print(f"Removed pre-existing: {script_path}")

    # Create Thunderbird profile with Client Contracts emails
    profile_dir = create_email_mbox()
    print(f"Thunderbird profile ready: {profile_dir}")

    # GUI-ready startup: Open Thunderbird with the configured profile
    launch_gui(f'thunderbird --profile "{profile_dir}"', delay_sec=3.0)
    print('GUI_READY: launched Thunderbird with Client Contracts folder with DISPLAY=:0')


create_initial()
