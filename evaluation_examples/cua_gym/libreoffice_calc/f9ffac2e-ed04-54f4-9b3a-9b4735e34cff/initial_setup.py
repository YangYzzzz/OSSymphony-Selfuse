"""
Initial Setup: Extract Introduction from PDF to Google Doc
Task ID: osworld_multi_apps_pdf_to_gdocs_012
Domain: multi_apps (Chrome + PDF)

Creates:
  - employee_training_manual.pdf on the Desktop with multiple sections
  - Opens Chrome with Google Drive showing the hr_resources folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_012'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/employee_training_manual.pdf'


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


def create_pdf():
    """Create a realistic employee training manual PDF on the Desktop."""
    from fpdf import FPDF

    os.makedirs(DESKTOP, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # -----------------------------------------------------------------------
    # Cover Page
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 24)
    pdf.ln(40)
    pdf.cell(0, 12, 'Employee Training Manual', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.set_font('Helvetica', '', 14)
    pdf.ln(6)
    pdf.cell(0, 10, 'Acme Corporation - Human Resources Department', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 10, 'Version 3.2  |  Fiscal Year 2025', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.multi_cell(0, 7, (
        'This manual is intended for all new and existing employees of Acme Corporation. '
        'It outlines the standards, expectations, and developmental pathways that guide '
        'professional growth within our organization.'
    ), align='C')

    # -----------------------------------------------------------------------
    # Table of Contents
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Table of Contents', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)
    toc_items = [
        ('1.', 'Introduction', '3'),
        ('2.', 'Core Competencies', '5'),
        ('3.', 'Training Modules', '8'),
        ('4.', 'Assessment and Certification', '13'),
        ('5.', 'Resources and Support', '16'),
    ]
    pdf.set_font('Helvetica', '', 12)
    for num, title, page in toc_items:
        pdf.cell(10, 8, num)
        pdf.cell(150, 8, title)
        pdf.cell(0, 8, page, new_x='LMARGIN', new_y='NEXT')

    # -----------------------------------------------------------------------
    # Section 1: Introduction
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, '1. Introduction', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '1.1 Welcome to Acme Corporation', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Welcome to Acme Corporation. We are delighted to have you join our team and look forward '
        'to supporting your professional development. This training manual has been carefully '
        'designed to provide you with all the information you need to thrive in your new role '
        'and contribute meaningfully to our shared mission.\n\n'
        'Acme Corporation was founded in 1998 with a commitment to delivering exceptional value '
        'to clients across the technology, finance, and healthcare sectors. Over the past '
        'twenty-five years, we have grown from a small consulting firm to a global organization '
        'with over 4,500 employees in 18 countries. Our growth reflects our unwavering focus '
        'on talent development and operational excellence.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '1.2 Our Mission and Values', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Our mission is to empower organizations and individuals through innovative solutions '
        'and a culture of continuous learning. We believe that every employee is an integral '
        'part of our success, and we invest in your growth from day one.\n\n'
        'Our core values guide every interaction and decision we make:'
    ))
    pdf.ln(2)
    values = [
        ('Integrity:', 'We act with honesty and transparency in all we do.'),
        ('Excellence:', 'We hold ourselves to the highest standards of quality.'),
        ('Collaboration:', 'We achieve more together than we can individually.'),
        ('Innovation:', 'We encourage creative thinking and continuous improvement.'),
        ('Inclusion:', 'We celebrate diversity and foster a sense of belonging for all.'),
    ]
    pdf.set_font('Helvetica', '', 11)
    for bold_part, rest in values:
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(30, 6, bold_part)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 6, rest)
        pdf.ln(1)
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '1.3 Scope and Purpose of This Manual', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'This manual serves as both an onboarding guide for new employees and an ongoing '
        'reference for all staff. It covers five major areas:\n\n'
        '  - Introduction to Acme\'s culture, mission, and leadership structure\n'
        '  - Core competencies expected of every employee regardless of role\n'
        '  - Structured training modules organized by department and skill level\n'
        '  - Assessment criteria and certification pathways\n'
        '  - Resources and support channels available to employees\n\n'
        'Employees are expected to read and understand all sections relevant to their role. '
        'Managers are encouraged to use this manual as a coaching tool during regular '
        'one-on-one meetings and performance reviews.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '1.4 How to Use This Manual', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Each section of this manual is self-contained and can be read independently. '
        'We recommend new employees complete the manual sequentially during their first two '
        'weeks. Returning employees may consult specific sections as needed.\n\n'
        'Throughout the manual you will find:\n'
        '  - Key Definitions -- terminology specific to Acme\'s processes\n'
        '  - Quick Reference Boxes -- summaries of critical procedures\n'
        '  - Worked Examples -- illustrative scenarios from real workplace situations\n'
        '  - Self-Assessment Checklists -- tools to gauge your own readiness\n\n'
        'If you have questions that are not addressed in this manual, please contact the '
        'HR team at hr-support@acmecorp.com or visit your department\'s SharePoint portal.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '1.5 Organizational Structure', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Acme Corporation operates under a matrix organizational structure that balances '
        'functional expertise with cross-functional project delivery. The executive team '
        'consists of the Chief Executive Officer, Chief Operating Officer, Chief Financial '
        'Officer, Chief People Officer, and Chief Technology Officer.\n\n'
        'Each business unit is led by a Vice President who reports directly to the COO. '
        'Employees are typically aligned to one functional department (e.g., Engineering, '
        'Marketing, Finance) while simultaneously contributing to project teams that may '
        'span multiple departments.\n\n'
        'An up-to-date organizational chart is available on the company intranet at '
        'intranet.acmecorp.com/org-chart. New employees are encouraged to review the chart '
        'to understand reporting lines and identify key stakeholders relevant to their role.'
    ))

    # -----------------------------------------------------------------------
    # Section 2: Core Competencies
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, '2. Core Competencies', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '2.1 Communication', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Effective communication is fundamental to success at Acme. Employees are expected '
        'to write clearly and concisely, listen actively, and adapt their communication style '
        'to diverse audiences. This competency encompasses written communication (email, '
        'reports, documentation), verbal communication (meetings, presentations, one-on-ones), '
        'and non-verbal cues (body language, tone, active listening).\n\n'
        'New employees should complete the Business Writing Foundations module within their '
        'first 30 days and participate in at least one presentation skills workshop during '
        'their first quarter.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '2.2 Problem Solving and Critical Thinking', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Acme values employees who approach challenges with structured analytical thinking. '
        'The organization uses a five-step problem-solving framework:\n\n'
        '  Step 1: Define the problem clearly\n'
        '  Step 2: Gather relevant data and stakeholder input\n'
        '  Step 3: Generate and evaluate potential solutions\n'
        '  Step 4: Implement the chosen solution with an action plan\n'
        '  Step 5: Monitor outcomes and document lessons learned\n\n'
        'Employees are encouraged to apply this framework in both formal project settings '
        'and day-to-day operational challenges.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '2.3 Teamwork and Collaboration', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Collaboration is woven into Acme\'s DNA. Employees are expected to contribute '
        'constructively to team discussions, respect diverse perspectives, share knowledge '
        'proactively, and support colleagues during high-demand periods. Team performance '
        'is evaluated alongside individual performance in annual reviews.'
    ))

    # -----------------------------------------------------------------------
    # Section 3: Training Modules
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, '3. Training Modules', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '3.1 Onboarding Track (Weeks 1-4)', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'The onboarding track is designed to help new employees integrate quickly and '
        'confidently. It consists of six mandatory modules delivered through a combination '
        'of instructor-led sessions, e-learning, and shadowing opportunities:\n\n'
        '  Module 1: Company History and Culture (4 hours)\n'
        '  Module 2: IT Systems and Security Onboarding (6 hours)\n'
        '  Module 3: HR Policies and Benefits Overview (3 hours)\n'
        '  Module 4: Role-Specific Orientation (8 hours)\n'
        '  Module 5: Health and Safety Compliance (2 hours)\n'
        '  Module 6: Introduction to Acme\'s Project Management Methodology (5 hours)\n\n'
        'All six modules must be completed before the end of the fourth week. Completion '
        'is tracked automatically in the Learning Management System (LMS).'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '3.2 Continuous Development Track', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Beyond the onboarding period, employees are expected to complete a minimum of '
        '40 hours of professional development annually. Development activities may include:\n\n'
        '  - Internal workshops and lunch-and-learn sessions\n'
        '  - External conferences and industry seminars\n'
        '  - Online courses via LinkedIn Learning, Coursera, or Pluralsight\n'
        '  - Certification programs sponsored by the company\n'
        '  - Mentoring and coaching relationships\n\n'
        'All development activities must be logged in the LMS within 30 days of completion.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '3.3 Leadership Development Track', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Employees identified as high-potential leaders are invited to participate in '
        'Acme\'s Leadership Accelerator Program (LAP). The LAP is a 12-month cohort-based '
        'program that combines executive coaching, stretch assignments, peer learning '
        'circles, and a capstone business challenge. Nominations are accepted each January '
        'from direct managers and senior leaders.'
    ))

    # -----------------------------------------------------------------------
    # Section 4: Assessment
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, '4. Assessment and Certification', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '4.1 Competency Assessments', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Employees undergo formal competency assessments at the end of their first 90 days '
        'and annually thereafter as part of the Performance Review cycle. Assessments '
        'evaluate both technical skills (role-specific) and behavioral competencies '
        '(as outlined in Section 2). Scores are used to inform Individual Development '
        'Plans (IDPs) and succession planning discussions.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '4.2 Certifications', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Acme supports employees in obtaining industry-recognized certifications relevant '
        'to their role. The company will reimburse up to $3,000 per year for certification '
        'examination fees and preparatory course materials upon successful completion. '
        'Applications for reimbursement must be submitted through Workday within 60 days '
        'of passing the certification exam.'
    ))

    # -----------------------------------------------------------------------
    # Section 5: Resources
    # -----------------------------------------------------------------------
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, '5. Resources and Support', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '5.1 HR Support', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'The HR team is available to support employees with questions about benefits, '
        'payroll, leave policies, and workplace accommodations. HR Business Partners are '
        'assigned to each department and are your primary point of contact for employee '
        'relations matters. You can reach HR support at hr-support@acmecorp.com or by '
        'calling extension 5400 during business hours (Monday-Friday, 8:00 AM - 5:00 PM).'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '5.2 Employee Assistance Program', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'Acme provides access to a confidential Employee Assistance Program (EAP) through '
        'LifeWorks. The EAP offers free, short-term counseling and referral services for '
        'personal and work-related challenges including stress, mental health, financial '
        'concerns, and family issues. The service is available 24/7 at 1-800-555-0199 or '
        'online at lifeworks.acmecorp.com.'
    ))
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 9, '5.3 Technology Resources', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6, (
        'All employees receive access to Acme\'s standard technology stack upon joining. '
        'This includes Microsoft 365, Slack, Jira, Confluence, and Workday. IT support '
        'is available at the IT Help Desk (extension 5500) or via the ServiceNow portal '
        'at it.acmecorp.com/helpdesk. For urgent issues such as account lockouts or '
        'hardware failures, priority support is available 24/7.'
    ))

    pdf.output(PDF_PATH)
    print(f'PDF created: {PDF_PATH}')


def setup_initial():
    create_pdf()

    # Kill any existing Chrome instances to avoid conflicts
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    time.sleep(1.5)

    # Launch Chrome with Google Drive open -- the task starts here
    launch_gui(
        'google-chrome --no-sandbox --disable-gpu '
        '"https://drive.google.com/drive/my-drive"',
        delay_sec=3.0,
    )

    print('GUI_READY: launched Chrome with Google Drive (DISPLAY=:0)')
    print(f'Initial artifact: {PDF_PATH}')


setup_initial()
