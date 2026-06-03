"""
Initial Setup: Archive emails from Thunderbird Sent folder task
Task ID: osworld_multi_apps_email_file_convert_004
Domain: multi_apps (Thunderbird + OS)

Creates:
- Thunderbird Local Folders account with 12 realistic sent emails in Sent folder
- Opens Thunderbird showing the Sent folder
"""

import os
import shlex
import subprocess
import time
import textwrap

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_004'
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


def create_mbox_email(from_addr, to_addr, subject, date, message_id, body):
    """Create a single email in mbox format."""
    # mbox From_ line (envelope from)
    from_line = f'From {from_addr} {date}\n'
    headers = (
        f'From: {from_addr}\n'
        f'To: {to_addr}\n'
        f'Subject: {subject}\n'
        f'Date: {date}\n'
        f'Message-ID: <{message_id}>\n'
        f'MIME-Version: 1.0\n'
        f'Content-Type: text/plain; charset=UTF-8\n'
        f'X-Mozilla-Status: 0001\n'
        f'X-Mozilla-Status2: 00000000\n'
        f'\n'
    )
    return from_line + headers + body + '\n'


def create_sent_mbox():
    """Create the Sent mbox file with 12 realistic emails."""
    emails = [
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'sarah.chen@clientco.com',
            'subject': 'Q3 Performance Report - Action Items',
            'date': 'Mon, 15 Jan 2024 09:23:45 +0800',
            'message_id': 'msg001.2024.techcorp',
            'body': textwrap.dedent("""\
                Hi Sarah,

                Please find below the action items from our Q3 performance review:

                1. Update the sales dashboard with December figures by Jan 20
                2. Schedule the team retrospective for week of Jan 22
                3. Submit budget forecasts for Q4 planning

                The overall numbers look strong - revenue up 18% year-over-year.
                Let me know if you have any questions.

                Best regards,
                Alex Morgan
                Senior Manager, TechCorp
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'marcus.johnson@partner.org',
            'subject': 'Re: Partnership Agreement - Final Review',
            'date': 'Tue, 16 Jan 2024 14:05:22 +0800',
            'message_id': 'msg002.2024.techcorp',
            'body': textwrap.dedent("""\
                Hi Marcus,

                Thank you for sending over the revised partnership agreement.
                I've reviewed all the clauses and have a few minor suggestions:

                Section 4.2: Adjust the revenue sharing to 60/40 (currently 55/45)
                Section 7.1: Extend the exclusivity period to 18 months
                Appendix B: Update the technical specifications to v2.3

                Overall the document looks solid. Let's schedule a call this week
                to finalize the remaining points.

                Best,
                Alex
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'engineering-team@techcorp.com',
            'subject': 'Sprint Planning - Week 3 Kickoff',
            'date': 'Wed, 17 Jan 2024 08:30:00 +0800',
            'message_id': 'msg003.2024.techcorp',
            'body': textwrap.dedent("""\
                Team,

                Reminder for our sprint planning session today at 10:00 AM in Conference Room B.

                Agenda:
                - Review previous sprint velocity (avg 42 story points)
                - Prioritize backlog items for Sprint 12
                - Assign tickets to team members
                - Discuss the API gateway refactoring proposal

                Please come prepared with your capacity estimates for the next two weeks.
                David has updated the Jira board with the new epics.

                See you there,
                Alex
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'hr@techcorp.com',
            'subject': 'Leave Request - February 5-9',
            'date': 'Thu, 18 Jan 2024 11:15:33 +0800',
            'message_id': 'msg004.2024.techcorp',
            'body': textwrap.dedent("""\
                Hi HR Team,

                I would like to request annual leave for the following dates:
                February 5-9, 2024 (5 working days)

                Reason: Family vacation

                I have ensured my team is fully briefed and David Chen will be
                the acting manager during my absence. All critical deliverables
                are on track before my departure.

                Please confirm approval at your earliest convenience.

                Thank you,
                Alex Morgan
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'vendor.support@cloudservices.io',
            'subject': 'Support Ticket #TB-48291 - Database Performance Issue',
            'date': 'Fri, 19 Jan 2024 16:42:18 +0800',
            'message_id': 'msg005.2024.techcorp',
            'body': textwrap.dedent("""\
                Dear CloudServices Support,

                Following up on ticket #TB-48291 regarding the database performance
                degradation observed last week.

                As requested, I'm attaching the query execution logs from January 15-17.
                The slowdowns predominantly occur during the 6-8 PM peak hours when
                concurrent connections exceed 450.

                Our DBA suggests this may be related to the index fragmentation issue
                mentioned in your January release notes. Has the hotfix been deployed
                to our instance?

                Please advise on next steps and estimated resolution time.

                Regards,
                Alex Morgan
                TechCorp Infrastructure Team
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'board@techcorp.com',
            'subject': 'Monthly Executive Summary - January 2024',
            'date': 'Mon, 22 Jan 2024 09:00:00 +0800',
            'message_id': 'msg006.2024.techcorp',
            'body': textwrap.dedent("""\
                Board Members,

                Please find attached the January 2024 Executive Summary.

                Key Highlights:
                - Revenue: $2.4M (Target: $2.1M, +14.3% above target)
                - New Customers: 47 (Target: 40, +17.5% above target)
                - Customer Retention Rate: 94.2%
                - Employee Headcount: 234 (Net +8 from December)

                Notable Achievements:
                - Launched new analytics platform (Product Team)
                - Completed ISO 27001 certification audit
                - Secured $500K contract with RegionalBank Corp

                Risks & Concerns:
                - Supply chain delays affecting hardware division
                - Increased competition in APAC market requires strategy review

                Full report available in the executive portal.

                Respectfully,
                Alex Morgan
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'lisa.park@techcorp.com',
            'subject': 'Re: Marketing Campaign Approval - Spring 2024',
            'date': 'Tue, 23 Jan 2024 13:28:55 +0800',
            'message_id': 'msg007.2024.techcorp',
            'body': textwrap.dedent("""\
                Lisa,

                The Spring 2024 campaign proposal looks excellent. I'm approving
                the budget allocation of $85,000 for the following channels:

                - Digital advertising (Google/LinkedIn): $40,000
                - Content marketing & SEO: $20,000
                - Trade show presence (TechSummit April): $15,000
                - Email campaign automation: $10,000

                Please coordinate with the design team to finalize creative assets
                by February 15. The campaign should go live on March 1.

                One request: please include A/B testing for the landing page
                to optimize conversion rates.

                Approved,
                Alex Morgan
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'it.security@techcorp.com',
            'subject': 'Security Audit Findings - Response Plan',
            'date': 'Wed, 24 Jan 2024 10:55:44 +0800',
            'message_id': 'msg008.2024.techcorp',
            'body': textwrap.dedent("""\
                IT Security Team,

                Following the security audit report received January 22, I want to
                outline our remediation priorities:

                Critical (Resolve by Feb 1):
                - Patch CVE-2024-0842 on production servers (3 affected hosts)
                - Enable MFA for all admin accounts

                High (Resolve by Feb 15):
                - Update TLS certificates expiring in March
                - Review and restrict S3 bucket public access policies

                Medium (Resolve by Mar 1):
                - Implement network segmentation for dev/staging environments
                - Complete SOC 2 Type II evidence collection

                Please assign owners and provide weekly status updates.

                Alex Morgan
                Chief Technology Officer
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'new.hire@techcorp.com',
            'subject': 'Welcome to TechCorp - Onboarding Resources',
            'date': 'Thu, 25 Jan 2024 08:15:00 +0800',
            'message_id': 'msg009.2024.techcorp',
            'body': textwrap.dedent("""\
                Welcome to TechCorp!

                On behalf of the entire team, I'm delighted to welcome you aboard.
                Here are some resources to help you get started:

                First Week Checklist:
                - Complete HR onboarding paperwork (HR portal: hr.techcorp.internal)
                - Set up your development environment (IT wiki: confluence.techcorp.internal)
                - Meet with your buddy: Jennifer Walsh (jennifer.walsh@techcorp.com)
                - Attend the Tuesday all-hands meeting at 2 PM

                Your access credentials will be sent by IT within the next hour.
                Don't hesitate to reach out if you have any questions.

                Looking forward to working with you!

                Best,
                Alex Morgan
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'finance@techcorp.com',
            'subject': 'Budget Reallocation Request - Q1 2024',
            'date': 'Fri, 26 Jan 2024 15:33:27 +0800',
            'message_id': 'msg010.2024.techcorp',
            'body': textwrap.dedent("""\
                Finance Team,

                I am requesting a budget reallocation for Q1 2024:

                From: Infrastructure Reserve Fund ($120,000)
                To:
                  - Cloud infrastructure scaling: $75,000
                  - Security tooling licenses: $25,000
                  - Training & development: $20,000

                Justification: The unexpected 35% increase in platform traffic
                requires immediate infrastructure investment to maintain our
                99.9% SLA commitments. The current over-provisioning costs
                are offset by reduced incident response time.

                Please process this by January 31 to avoid billing delays.

                Thank you,
                Alex Morgan
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'client.success@techcorp.com',
            'subject': 'Enterprise Client Feedback - Follow-up Actions',
            'date': 'Mon, 29 Jan 2024 09:45:12 +0800',
            'message_id': 'msg011.2024.techcorp',
            'body': textwrap.dedent("""\
                Customer Success Team,

                Following last week's NPS survey, we received important feedback
                from our enterprise clients. Here's what needs immediate attention:

                MegaCorp (NPS Score: 6 - Detractor):
                - Main complaint: API response times during peak hours
                - Action: Schedule technical review with their IT team by Feb 2
                - Owner: David Chen

                GlobalFinance (NPS Score: 9 - Promoter):
                - Requested feature: bulk export functionality
                - Add to Q2 roadmap with high priority
                - Owner: Product Team

                NationalRetail (NPS Score: 7 - Passive):
                - Integration documentation needs updating
                - Assign technical writer to refresh docs by Feb 10
                - Owner: Jennifer Walsh

                Please ensure all owners are notified and timelines are tracked
                in our CRM system.

                Alex
            """)
        },
        {
            'from_addr': 'alex.morgan@techcorp.com',
            'to_addr': 'all-staff@techcorp.com',
            'subject': 'Company Town Hall - February 2024 Invitation',
            'date': 'Tue, 30 Jan 2024 11:00:00 +0800',
            'message_id': 'msg012.2024.techcorp',
            'body': textwrap.dedent("""\
                All TechCorp Staff,

                You are cordially invited to our Q1 2024 Company Town Hall.

                Date: Thursday, February 8, 2024
                Time: 3:00 PM - 4:30 PM
                Location: Main Auditorium (Building A) + Live Stream

                Agenda:
                1. Company Performance Review - Q4 2023 Results
                2. 2024 Vision and Strategic Priorities
                3. Product Roadmap Highlights
                4. Team Recognition Awards
                5. Q&A Session

                This is a great opportunity to hear about our direction and
                ask questions directly to the leadership team. All employees
                are encouraged to attend.

                Calendar invite has been sent to all staff. Please RSVP
                by February 1 if attending in-person for catering purposes.

                See you there!

                Alex Morgan
                CEO, TechCorp
            """)
        },
    ]

    mbox_content = ''
    for email in emails:
        mbox_content += create_mbox_email(**email)

    return mbox_content


def setup_thunderbird_local_account():
    """Set up Thunderbird local folders with Sent mbox."""
    # Create Local Folders directory structure
    os.makedirs(MAIL_DIR, exist_ok=True)

    # Create Sent mbox file
    sent_mbox_path = os.path.join(MAIL_DIR, 'Sent')
    mbox_content = create_sent_mbox()
    with open(sent_mbox_path, 'w', encoding='utf-8') as f:
        f.write(mbox_content)
    print(f'Created Sent mbox: {sent_mbox_path}')

    # Create Sent.msf (mail summary file - empty marker for Thunderbird)
    sent_msf_path = os.path.join(MAIL_DIR, 'Sent.msf')
    with open(sent_msf_path, 'wb') as f:
        # Write minimal MSF header
        f.write(b'// <!-- <mdb:mork:z v="1.4"/> -->\n')
    print(f'Created Sent.msf: {sent_msf_path}')

    # Update prefs.js to configure local folders account
    prefs_path = f'{PROFILE_DIR}/prefs.js'
    with open(prefs_path, 'r') as f:
        prefs_content = f.read()

    # Add local folders account configuration if not already present
    local_account_prefs = """
user_pref("mail.account.account1.identities", "id1");
user_pref("mail.account.account1.server", "server1");
user_pref("mail.accountmanager.accounts", "account1");
user_pref("mail.accountmanager.localfoldersserver", "server1");
user_pref("mail.identity.id1.fullName", "Alex Morgan");
user_pref("mail.identity.id1.useremail", "alex.morgan@techcorp.com");
user_pref("mail.identity.id1.valid", true);
user_pref("mail.server.server1.directory-rel", "[ProfD]Mail/Local Folders");
user_pref("mail.server.server1.hostname", "Local Folders");
user_pref("mail.server.server1.name", "Local Folders");
user_pref("mail.server.server1.type", "none");
user_pref("mail.server.server1.userName", "nobody");
"""

    if 'mail.account.account1' not in prefs_content:
        with open(prefs_path, 'a') as f:
            f.write(local_account_prefs)
        print('Updated prefs.js with local folders account')
    else:
        print('prefs.js already has local account configuration')


def create_initial():
    """Main setup function."""
    # Ensure no leftover sent_backup or backup_log
    sent_backup = f'{WORKDIR}/sent_backup'
    backup_log = f'{WORKDIR}/backup_log.txt'
    if os.path.exists(sent_backup):
        import shutil
        shutil.rmtree(sent_backup)
        print(f'Removed existing {sent_backup}')
    if os.path.exists(backup_log):
        os.remove(backup_log)
        print(f'Removed existing {backup_log}')

    # Set up Thunderbird local folders account with 12 sent emails
    setup_thunderbird_local_account()

    print(f'Initial state prepared: 12 emails in Thunderbird Sent folder')
    print(f'Mail directory: {MAIL_DIR}')

    # GUI-ready startup: open Thunderbird
    # Kill any running Thunderbird instances first to avoid lock conflicts
    subprocess.run(['pkill', '-f', 'thunderbird'], capture_output=True)
    time.sleep(2.0)

    # Remove profile lock if any
    lock_file = f'{PROFILE_DIR}/lock'
    if os.path.exists(lock_file):
        os.remove(lock_file)

    parent_lock = f'{PROFILE_DIR}/.parentlock'
    if os.path.exists(parent_lock):
        os.remove(parent_lock)

    # Launch Thunderbird
    launch_gui('thunderbird', delay_sec=3.0)
    print('GUI_READY: launched Thunderbird with DISPLAY=:0')


create_initial()
