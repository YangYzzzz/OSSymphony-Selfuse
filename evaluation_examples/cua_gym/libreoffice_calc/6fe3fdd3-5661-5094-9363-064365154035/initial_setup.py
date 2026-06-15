"""
Initial Setup: VSCode meeting_notes project with date-named .txt files
Task ID: osworld_multi_apps_vscode_concat_doc_006
Domain: multi_apps (VSCode + LibreOffice Writer)

Creates:
  - /home/user/Desktop/meeting_notes/ folder with date-named .txt files
  - Opens VSCode with the meeting_notes folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
MEETING_NOTES_DIR = f'{DESKTOP}/meeting_notes'

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
    # Create Desktop and meeting_notes directory
    os.makedirs(MEETING_NOTES_DIR, exist_ok=True)

    # Realistic meeting note files sorted by date (oldest to newest)
    meeting_files = {
        '2024-01-10.txt': (
            "Attendees: Sarah Chen, Marcus Johnson, Linda Park, David Kim\n\n"
            "Topics Discussed:\n"
            "1. Q1 project roadmap review\n"
            "   - Engineering team to finalize API design by end of January\n"
            "   - Marketing team to prepare campaign materials for February launch\n"
            "2. Budget allocation for Q1\n"
            "   - Total budget approved: $120,000\n"
            "   - Engineering: $70,000 | Marketing: $30,000 | Operations: $20,000\n"
            "3. Hiring plan update\n"
            "   - Two senior engineer positions to be posted this week\n"
            "   - Interviews expected to start February 5th\n\n"
            "Action Items:\n"
            "- Sarah: Draft API specification document (due Jan 17)\n"
            "- Marcus: Finalize campaign brief (due Jan 20)\n"
            "- Linda: Post job listings (due Jan 12)\n\n"
            "Next Meeting: January 17, 2024"
        ),
        '2024-01-17.txt': (
            "Attendees: Sarah Chen, Marcus Johnson, Linda Park, Robert Nguyen\n\n"
            "Topics Discussed:\n"
            "1. API specification review\n"
            "   - Draft reviewed and approved with minor revisions\n"
            "   - Version 1.0 to be shared with frontend team by Jan 22\n"
            "2. New hire interviews update\n"
            "   - 12 applications received for senior engineer positions\n"
            "   - First round interviews scheduled for Jan 29-31\n"
            "3. Product roadmap adjustments\n"
            "   - Mobile app feature pushed to Q2 due to resource constraints\n"
            "   - Web dashboard prioritized for Q1 delivery\n\n"
            "Action Items:\n"
            "- Sarah: Share API v1.0 with frontend team (due Jan 22)\n"
            "- Robert: Coordinate interview panels (due Jan 25)\n"
            "- Marcus: Update campaign timeline (due Jan 24)\n\n"
            "Next Meeting: January 24, 2024"
        ),
        '2024-01-24.txt': (
            "Attendees: Sarah Chen, Marcus Johnson, David Kim, Robert Nguyen, Emily Torres\n\n"
            "Topics Discussed:\n"
            "1. Frontend integration progress\n"
            "   - Frontend team has reviewed API spec, questions addressed\n"
            "   - Integration timeline: 3 weeks starting Feb 1\n"
            "2. Campaign materials review\n"
            "   - First draft of landing page reviewed - approved with feedback\n"
            "   - Social media content calendar shared and approved\n"
            "3. Q1 milestone tracking setup\n"
            "   - Emily introduced new project tracking board in Jira\n"
            "   - All team leads to update their tasks by Friday\n\n"
            "Action Items:\n"
            "- David: Begin frontend integration Feb 1 (ongoing)\n"
            "- Marcus: Finalize landing page based on feedback (due Jan 31)\n"
            "- Emily: Send Jira training invite to all team leads (due Jan 26)\n\n"
            "Next Meeting: February 7, 2024"
        ),
        '2024-02-07.txt': (
            "Attendees: Sarah Chen, Marcus Johnson, David Kim, Emily Torres, Linda Park\n\n"
            "Topics Discussed:\n"
            "1. Frontend integration status check\n"
            "   - Core API connections completed, authentication module in progress\n"
            "   - On track for Feb 22 integration milestone\n"
            "2. Senior engineer hires finalized\n"
            "   - Two candidates selected: offer letters sent Feb 5\n"
            "   - Start dates: March 4 and March 11\n"
            "3. February marketing push\n"
            "   - Landing page live as of Feb 6 - 1,200 unique visitors in first day\n"
            "   - Email campaign launched to 45,000 subscribers\n"
            "4. Risk review\n"
            "   - Server capacity may be insufficient at launch - DevOps investigating\n\n"
            "Action Items:\n"
            "- David: Complete auth module (due Feb 14)\n"
            "- Marcus: Compile first-week marketing metrics (due Feb 14)\n"
            "- Sarah: Review DevOps capacity report (due Feb 10)\n\n"
            "Next Meeting: February 14, 2024"
        ),
        '2024-02-14.txt': (
            "Attendees: Sarah Chen, Marcus Johnson, David Kim, Emily Torres, James Park\n\n"
            "Topics Discussed:\n"
            "1. Authentication module completion\n"
            "   - OAuth2 integration done, unit tests passing\n"
            "   - Awaiting QA sign-off before merge to main branch\n"
            "2. Marketing metrics week 1\n"
            "   - Landing page: 8,400 unique visitors total\n"
            "   - Email open rate: 24.3% (industry avg: 18%)\n"
            "   - Sign-up conversions: 312\n"
            "3. Infrastructure scale-up plan\n"
            "   - James (DevOps) presented 3-tier auto-scaling plan\n"
            "   - Budget for infrastructure: additional $15,000 approved\n"
            "4. Valentine's Day promotional campaign results\n"
            "   - 15% discount code used 287 times\n"
            "   - Revenue impact: $34,500\n\n"
            "Action Items:\n"
            "- David: Merge auth module after QA approval (due Feb 17)\n"
            "- James: Implement auto-scaling configuration (due Feb 21)\n"
            "- Emily: Update Q1 milestone tracker (due Feb 16)\n\n"
            "Next Meeting: February 21, 2024"
        ),
        '2024-02-21.txt': (
            "Attendees: Sarah Chen, Marcus Johnson, David Kim, James Park, Emily Torres\n\n"
            "Topics Discussed:\n"
            "1. Integration milestone completion\n"
            "   - All planned API integrations completed on schedule\n"
            "   - Final end-to-end testing starting Feb 23\n"
            "2. Infrastructure auto-scaling deployed\n"
            "   - Auto-scaling tested under simulated 5x load - performed well\n"
            "   - Monitoring dashboards live in Grafana\n"
            "3. Launch readiness review\n"
            "   - Feature freeze set for Feb 28\n"
            "   - Production deployment scheduled for March 5\n"
            "   - All teams confirmed ready for launch window\n"
            "4. New engineers onboarding plan\n"
            "   - Onboarding schedule prepared for March 4 and March 11 starters\n"
            "   - Buddy system assigned: David for Hire 1, Emily for Hire 2\n\n"
            "Action Items:\n"
            "- Sarah: Prepare launch communications draft (due Feb 28)\n"
            "- James: Final infrastructure checklist (due Feb 27)\n"
            "- Marcus: Prepare press release draft (due Feb 26)\n\n"
            "Next Meeting: February 28, 2024"
        ),
    }

    # Write all meeting note files
    for filename, content in meeting_files.items():
        filepath = os.path.join(MEETING_NOTES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Created: {filepath}')

    print(f'Meeting notes directory created: {MEETING_NOTES_DIR}')

    # Ensure no meeting_minutes.docx exists on Desktop (task output should not pre-exist)
    minutes_path = f'{DESKTOP}/meeting_minutes.docx'
    if os.path.exists(minutes_path):
        os.remove(minutes_path)
        print(f'Removed pre-existing: {minutes_path}')

    # GUI-ready startup: open VSCode with the meeting_notes folder
    launch_gui(f'code "{MEETING_NOTES_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with meeting_notes folder (DISPLAY=:0)')

create_initial()
