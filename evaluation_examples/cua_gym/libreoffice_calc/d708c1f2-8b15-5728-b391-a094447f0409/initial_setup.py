"""
Initial Setup: Set up Thunderbird with email from hr@company.com containing onboarding_checklist.odt attachment
Task ID: osworld_multi_apps_email_file_convert_002
Domain: multi_apps (Thunderbird + LibreOffice Writer + OS)

Initial state:
- Thunderbird Inbox has an email from hr@company.com with onboarding_checklist.odt attachment
- /home/user/documents/ directory exists but does NOT contain onboarding_checklist.odt
- Thunderbird is open showing the Inbox
"""

import os
import shlex
import subprocess
import time
import json
import mailbox
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import zipfile
import io
import base64

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_002'


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


def create_odt_bytes():
    """Create a minimal but realistic onboarding_checklist.odt as bytes (ODT is a zip archive)."""
    # ODT is a ZIP file containing XML files
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype (must be first, uncompressed)
        zf.writestr(zipfile.ZipInfo('mimetype'), 'application/vnd.oasis.opendocument.text',
                    compress_type=zipfile.ZIP_STORED)

        # meta.xml
        meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.3">
  <office:meta>
    <meta:initial-creator>HR Department</meta:initial-creator>
    <meta:creation-date>2025-01-15T09:00:00</meta:creation-date>
    <meta:document-statistic meta:word-count="120" meta:character-count="680"/>
  </office:meta>
</office:document-meta>'''
        zf.writestr('meta.xml', meta_xml)

        # settings.xml
        settings_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    office:version="1.3">
  <office:settings>
  </office:settings>
</office:document-settings>'''
        zf.writestr('settings.xml', settings_xml)

        # styles.xml
        styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:hyphenation-ladder-count="no-limit"/>
      <style:text-properties fo:font-family="Liberation Serif" fo:font-size="12pt" fo:language="en" fo:country="US"/>
    </style:default-style>
    <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
    <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph" style:next-style-name="Standard" style:class="text">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Heading_20_2" style:display-name="Heading 2" style:family="paragraph" style:next-style-name="Standard" style:class="text">
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="List_20_Bullet" style:display-name="List Bullet" style:family="paragraph">
      <style:paragraph-properties fo:margin-left="0.5in" fo:text-indent="-0.25in"/>
    </style:style>
  </office:styles>
  <office:automatic-styles/>
  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="Mpm1"/>
  </office:master-styles>
</office:document-styles>'''
        zf.writestr('styles.xml', styles_xml)

        # content.xml with realistic onboarding checklist
        content_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:automatic-styles/>
  <office:body>
    <office:text>
      <text:h text:style-name="Heading_20_1" text:outline-level="1">New Employee Onboarding Checklist</text:h>
      <text:p text:style-name="Standard">Welcome to Acme Corporation! Please complete the following items during your first week.</text:p>
      <text:p text:style-name="Standard">Employee Name: ___________________________</text:p>
      <text:p text:style-name="Standard">Start Date: ___________________________</text:p>
      <text:p text:style-name="Standard">Department: ___________________________</text:p>
      <text:p text:style-name="Standard">Manager: ___________________________</text:p>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Day 1 — Administrative Setup</text:h>
      <text:list>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Complete HR paperwork and tax forms (W-4, I-9)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Receive company ID badge from security desk (Building A, Room 101)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Set up company email account with IT support</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Configure VPN access on your workstation</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Review and sign the Employee Handbook acknowledgment form</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Attend orientation session at 10:00 AM in Conference Room B</text:p></text:list-item>
      </text:list>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Day 2-3 — System Access and Tools</text:h>
      <text:list>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Request access to internal project management system (Jira)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Set up Slack workspace and join relevant team channels</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Install required development tools (see IT Setup Guide)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Complete cybersecurity awareness training (online, approx. 2 hours)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Review code of conduct and data privacy policies</text:p></text:list-item>
      </text:list>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Week 1 — Team Integration</text:h>
      <text:list>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Schedule 1:1 meetings with all direct team members</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Attend weekly team standup (Monday and Thursday, 9:30 AM)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Review current sprint goals and backlog with your team lead</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Complete 30-day onboarding check-in form and return to HR</text:p></text:list-item>
      </text:list>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Benefits Enrollment</text:h>
      <text:p text:style-name="Standard">You have 30 days from your start date to enroll in benefits. Please contact benefits@company.com for questions.</text:p>
      <text:list>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Review health insurance options (Medical, Dental, Vision)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Set up 401(k) contribution with Fidelity (company matches up to 4%)</text:p></text:list-item>
        <text:list-item><text:p text:style-name="List_20_Bullet">[ ] Designate emergency contact in HR portal</text:p></text:list-item>
      </text:list>
      <text:p text:style-name="Standard">If you have any questions, please contact your HR Business Partner or email hr@company.com.</text:p>
      <text:p text:style-name="Standard">Human Resources Department — Acme Corporation</text:p>
      <text:p text:style-name="Standard">hr@company.com | (555) 867-5309</text:p>
    </office:text>
  </office:body>
</office:document-content>'''
        zf.writestr('content.xml', content_xml)

        # manifest.xml
        manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
    manifest:version="1.3">
  <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="settings.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    buf.seek(0)
    return buf.read()


def setup_thunderbird_email():
    """Set up a Thunderbird local mail account with the test email containing the attachment."""

    # Find or create the Thunderbird profile directory
    thunderbird_base = os.path.expanduser('~/.thunderbird')

    # List existing profiles
    profiles_ini = os.path.join(thunderbird_base, 'profiles.ini')
    profile_dir = None

    if os.path.exists(profiles_ini):
        with open(profiles_ini, 'r') as f:
            content = f.read()
        # Find profile path
        for line in content.split('\n'):
            if line.startswith('Path='):
                candidate = line.split('=', 1)[1].strip()
                if not os.path.isabs(candidate):
                    candidate = os.path.join(thunderbird_base, candidate)
                if os.path.isdir(candidate):
                    profile_dir = candidate
                    break

    if not profile_dir:
        # Create a new profile
        import glob
        dirs = glob.glob(os.path.join(thunderbird_base, '*.default*'))
        if dirs:
            profile_dir = dirs[0]

    if not profile_dir or not os.path.isdir(profile_dir):
        print(f"Warning: Could not find Thunderbird profile at {thunderbird_base}")
        print("Will attempt to create mail structure directly...")
        # Try common profile names
        for name in ['default', 'default-release', 'default-esr']:
            candidate = os.path.join(thunderbird_base, f'xxxxx.{name}')
            if os.path.isdir(candidate):
                profile_dir = candidate
                break

    # Create the ODT file bytes
    odt_bytes = create_odt_bytes()

    # Encode attachment as base64
    odt_b64 = base64.b64encode(odt_bytes).decode('ascii')

    # Build MIME message for the email
    msg = MIMEMultipart()
    msg['From'] = 'hr@company.com'
    msg['To'] = 'user@localhost'
    msg['Subject'] = 'Welcome! Your Onboarding Checklist'
    msg['Date'] = 'Mon, 15 Jan 2025 09:00:00 +0000'
    msg['Message-ID'] = '<onboarding-001@company.com>'

    # Email body
    body_text = """Dear New Employee,

Welcome to Acme Corporation! We are thrilled to have you join our team.

Please find attached your New Employee Onboarding Checklist. This document outlines the steps you need to complete during your first week with us.

Please save the document and open it with LibreOffice Writer to review all the items on the checklist.

If you have any questions about the onboarding process, please do not hesitate to reach out to us.

Best regards,

Human Resources Department
Acme Corporation
hr@company.com
(555) 867-5309
"""
    msg.attach(MIMEText(body_text, 'plain'))

    # Attach the ODT file
    part = MIMEBase('application', 'vnd.oasis.opendocument.text')
    part.set_payload(odt_bytes)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='onboarding_checklist.odt')
    msg.attach(part)

    # Convert to mbox format string
    mbox_entry = msg.as_string()

    if profile_dir and os.path.isdir(profile_dir):
        # Look for Mail/Local Folders directory in profile
        mail_dir = os.path.join(profile_dir, 'Mail', 'Local Folders')
        if not os.path.exists(mail_dir):
            os.makedirs(mail_dir, exist_ok=True)

        inbox_path = os.path.join(mail_dir, 'Inbox')

        # Write the email to the Inbox mbox file
        with open(inbox_path, 'a') as f:
            f.write(f'From hr@company.com Mon Jan 15 09:00:00 2025\n')
            f.write(mbox_entry)
            f.write('\n\n')

        # Remove the index file to force Thunderbird to re-read the mbox
        inbox_msf = inbox_path + '.msf'
        if os.path.exists(inbox_msf):
            os.remove(inbox_msf)

        print(f"Email added to Thunderbird inbox at: {inbox_path}")
    else:
        # Fallback: create the mail structure from scratch
        print(f"Profile dir not found or invalid: {profile_dir}")
        print("Setting up Thunderbird mail structure...")

        # We'll use a different approach - create a local mbox directly
        # and configure Thunderbird to use it
        os.makedirs(thunderbird_base, exist_ok=True)

        # Create a simple profile
        new_profile_dir = os.path.join(thunderbird_base, 'default-profile.default')
        os.makedirs(new_profile_dir, exist_ok=True)

        mail_dir = os.path.join(new_profile_dir, 'Mail', 'Local Folders')
        os.makedirs(mail_dir, exist_ok=True)

        inbox_path = os.path.join(mail_dir, 'Inbox')
        with open(inbox_path, 'a') as f:
            f.write(f'From hr@company.com Mon Jan 15 09:00:00 2025\n')
            f.write(mbox_entry)
            f.write('\n\n')

        # Create profiles.ini
        profiles_ini_content = f"""[General]
StartWithLastProfile=1
Version=2

[Profile0]
Name=default
IsRelative=1
Path=default-profile.default
Default=1
"""
        with open(profiles_ini, 'w') as f:
            f.write(profiles_ini_content)

        print(f"Created new Thunderbird profile with email at: {inbox_path}")

    return True


def create_initial():
    """Create the initial state for the task."""

    # 1. Ensure /home/user/documents/ directory exists (but without the ODT file)
    documents_dir = os.path.join(WORKDIR, 'documents')
    os.makedirs(documents_dir, exist_ok=True)
    print(f"Created documents directory: {documents_dir}")

    # 2. Ensure the ODT file is NOT in /home/user/documents/ (negative constraint)
    odt_in_docs = os.path.join(documents_dir, 'onboarding_checklist.odt')
    if os.path.exists(odt_in_docs):
        os.remove(odt_in_docs)
        print(f"Removed pre-existing file: {odt_in_docs}")

    # 3. Also ensure it's not in the home directory (task is to save from email)
    odt_in_home = os.path.join(WORKDIR, 'onboarding_checklist.odt')
    if os.path.exists(odt_in_home):
        os.remove(odt_in_home)
        print(f"Removed pre-existing file from home: {odt_in_home}")

    # 4. Set up Thunderbird email with the attachment
    setup_thunderbird_email()

    # 5. Launch Thunderbird to show the inbox
    print("Launching Thunderbird...")
    launch_gui('thunderbird', delay_sec=3.0)

    print(f"\nInitial state created successfully.")
    print(f"- Thunderbird inbox has email from hr@company.com with onboarding_checklist.odt")
    print(f"- /home/user/documents/ exists but does NOT contain onboarding_checklist.odt")
    print(f"- Thunderbird is launching (DISPLAY=:0)")
    print('GUI_READY: launched Thunderbird with DISPLAY=:0')


create_initial()
