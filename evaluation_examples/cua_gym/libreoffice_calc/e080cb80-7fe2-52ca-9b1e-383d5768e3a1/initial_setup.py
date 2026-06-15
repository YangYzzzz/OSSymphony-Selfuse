"""
Initial Setup: Backup and Report Shell Script Task
Task ID: osworld_multi_apps_code_batch_terminal_011
Domain: os

Creates /home/user/documents/important/ with 3 subdirectories and 18 total files.
Also creates /home/user/scripts/ directory (empty, where agent will create the script).
Opens a terminal so the agent can write and test the shell script.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_batch_terminal_011'
DOCS_DIR = f'{WORKDIR}/documents/important'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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
    # Create scripts directory (where agent will write the script)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    print(f'Created: {SCRIPTS_DIR}')

    # Create the important documents directory structure
    # Subdirectory 1: finance (6 files)
    finance_dir = os.path.join(DOCS_DIR, 'finance')
    os.makedirs(finance_dir, exist_ok=True)

    finance_files = {
        'q1_budget.txt': (
            'Q1 2025 Budget Report\n'
            'Department: Engineering\n'
            'Allocated: $450,000\n'
            'Spent: $387,250\n'
            'Remaining: $62,750\n'
            'Status: Under budget\n'
            'Reviewed by: Sarah Chen, CFO\n'
        ),
        'q2_forecast.txt': (
            'Q2 2025 Financial Forecast\n'
            'Revenue Projection: $1,250,000\n'
            'Operating Expenses: $890,000\n'
            'Net Income Estimate: $360,000\n'
            'Growth Rate: 12.5%\n'
            'Market Conditions: Favorable\n'
        ),
        'vendor_contracts.csv': (
            'Vendor,Contract Value,Start Date,End Date,Status\n'
            'TechSupply Co,85000,2025-01-01,2025-12-31,Active\n'
            'CloudServices Inc,120000,2025-03-01,2026-02-28,Active\n'
            'DataAnalytics Ltd,45000,2025-02-01,2025-07-31,Active\n'
            'Marketing Pro,32000,2025-01-15,2025-06-15,Active\n'
        ),
        'expense_report_jan.txt': (
            'January 2025 Expense Report\n'
            'Employee: Marcus Johnson\n'
            'Department: Sales\n'
            'Travel: $2,340.50\n'
            'Meals: $485.20\n'
            'Equipment: $1,200.00\n'
            'Total: $4,025.70\n'
            'Approved by: Director of Finance\n'
        ),
        'annual_audit.txt': (
            'Annual Audit Summary 2024\n'
            'Auditor: PricewaterhouseCoopers\n'
            'Audit Period: Jan 2024 - Dec 2024\n'
            'Total Revenue: $4,850,000\n'
            'Total Expenses: $3,920,000\n'
            'Net Profit: $930,000\n'
            'Tax Liability: $279,000\n'
            'Compliance Status: Fully compliant\n'
            'Next Review: Q3 2025\n'
        ),
        'tax_documents.txt': (
            'Tax Filing Summary 2024\n'
            'Entity: Acme Corporation LLC\n'
            'EIN: 45-1234567\n'
            'Filing Status: Corporation\n'
            'Fiscal Year: January - December 2024\n'
            'Gross Revenue: $4,850,000\n'
            'Deductions: $3,650,000\n'
            'Taxable Income: $1,200,000\n'
            'Federal Tax Rate: 21%\n'
            'Tax Filed: March 15, 2025\n'
        ),
    }

    for filename, content in finance_files.items():
        filepath = os.path.join(finance_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'  Created: {filepath}')

    # Subdirectory 2: projects (7 files)
    projects_dir = os.path.join(DOCS_DIR, 'projects')
    os.makedirs(projects_dir, exist_ok=True)

    projects_files = {
        'project_alpha_plan.txt': (
            'Project Alpha - Implementation Plan\n'
            'Project Manager: Elena Rodriguez\n'
            'Start Date: 2025-02-01\n'
            'Target Completion: 2025-08-31\n'
            'Budget: $750,000\n'
            '\n'
            'Milestones:\n'
            '  M1: Requirements gathering (Feb 2025)\n'
            '  M2: Architecture design (Mar 2025)\n'
            '  M3: Development phase 1 (Apr-May 2025)\n'
            '  M4: Testing and QA (Jun-Jul 2025)\n'
            '  M5: Deployment and launch (Aug 2025)\n'
            '\n'
            'Team: 8 engineers, 2 designers, 1 PM\n'
        ),
        'project_beta_status.txt': (
            'Project Beta - Status Update\n'
            'Project Manager: James Wilson\n'
            'Current Phase: Development\n'
            'Completion: 65%\n'
            'On Schedule: Yes\n'
            '\n'
            'Completed Tasks:\n'
            '  - Database schema design\n'
            '  - API endpoint development\n'
            '  - Authentication module\n'
            '\n'
            'Pending Tasks:\n'
            '  - Frontend integration\n'
            '  - Performance testing\n'
            '  - Security audit\n'
        ),
        'client_requirements.txt': (
            'Client Requirements Document\n'
            'Client: GlobalTech Industries\n'
            'Contact: David Park, CTO\n'
            'Date: 2025-01-20\n'
            '\n'
            'Functional Requirements:\n'
            '  1. Real-time data processing pipeline\n'
            '  2. Multi-tenant architecture support\n'
            '  3. REST API with OAuth 2.0\n'
            '  4. Dashboard with analytics\n'
            '  5. Export to CSV/PDF/Excel\n'
            '\n'
            'Non-Functional Requirements:\n'
            '  - 99.9% uptime SLA\n'
            '  - < 200ms API response time\n'
            '  - GDPR compliant data handling\n'
        ),
        'tech_specs.md': (
            '# Technical Specifications\n\n'
            '## System Architecture\n\n'
            '### Backend\n'
            '- Framework: Python FastAPI 0.100+\n'
            '- Database: PostgreSQL 15\n'
            '- Cache: Redis 7.0\n'
            '- Message Queue: RabbitMQ 3.12\n\n'
            '### Frontend\n'
            '- Framework: React 18\n'
            '- State Management: Redux Toolkit\n'
            '- UI Library: Material UI v5\n\n'
            '### Infrastructure\n'
            '- Container: Docker + Kubernetes\n'
            '- CI/CD: GitHub Actions\n'
            '- Cloud: AWS (us-east-1)\n'
            '- CDN: CloudFront\n'
        ),
        'meeting_notes_2025_02.txt': (
            'Meeting Notes - Project Sync\n'
            'Date: February 10, 2025\n'
            'Attendees: Elena Rodriguez, James Wilson, Sarah Chen, David Park\n'
            '\n'
            'Agenda Items:\n'
            '1. Sprint review - completed 23/25 story points\n'
            '2. Blocker: Third-party API rate limits\n'
            '3. Decision: Implement local caching layer\n'
            '4. Timeline adjustment: 2-week buffer added\n'
            '\n'
            'Action Items:\n'
            '  - James: Implement Redis caching by Feb 20\n'
            '  - Elena: Update project timeline in Jira\n'
            '  - Sarah: Review Q2 budget allocation\n'
            '\n'
            'Next Meeting: February 24, 2025\n'
        ),
        'risk_assessment.txt': (
            'Risk Assessment Report\n'
            'Project: Alpha & Beta Combined\n'
            'Assessment Date: 2025-01-28\n'
            '\n'
            'High Risk:\n'
            '  R1: Third-party API dependency (Probability: Medium, Impact: High)\n'
            '  R2: Key personnel availability (Probability: Low, Impact: High)\n'
            '\n'
            'Medium Risk:\n'
            '  R3: Scope creep from client changes (Probability: High, Impact: Medium)\n'
            '  R4: Performance targets at scale (Probability: Medium, Impact: Medium)\n'
            '\n'
            'Mitigation Strategies:\n'
            '  R1: Implement fallback providers\n'
            '  R2: Cross-train team members\n'
            '  R3: Strict change control process\n'
            '  R4: Load testing at 2x expected traffic\n'
        ),
        'deliverables_checklist.txt': (
            'Deliverables Checklist\n'
            'Project Alpha - Final Delivery\n'
            '\n'
            '[x] Source code repository (GitHub)\n'
            '[x] API documentation (Swagger/OpenAPI)\n'
            '[x] Database migration scripts\n'
            '[x] Docker containerization\n'
            '[x] Unit test suite (95% coverage)\n'
            '[x] Integration test suite\n'
            '[ ] Performance test report\n'
            '[ ] Security audit report\n'
            '[ ] User manual\n'
            '[ ] Deployment runbook\n'
            '\n'
            'Completion: 60%\n'
        ),
    }

    for filename, content in projects_files.items():
        filepath = os.path.join(projects_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'  Created: {filepath}')

    # Subdirectory 3: hr (5 files)
    hr_dir = os.path.join(DOCS_DIR, 'hr')
    os.makedirs(hr_dir, exist_ok=True)

    hr_files = {
        'employee_roster.csv': (
            'EmployeeID,Name,Department,Position,Salary,StartDate,Status\n'
            'E001,Sarah Chen,Finance,CFO,185000,2019-03-01,Active\n'
            'E002,Marcus Johnson,Sales,Director,145000,2020-07-15,Active\n'
            'E003,Elena Rodriguez,Engineering,Project Manager,125000,2021-01-10,Active\n'
            'E004,James Wilson,Engineering,Lead Developer,115000,2020-11-01,Active\n'
            'E005,Priya Patel,Marketing,Marketing Manager,98000,2022-02-14,Active\n'
            'E006,David Kim,Engineering,Senior Developer,108000,2021-06-01,Active\n'
            'E007,Laura Thompson,HR,HR Director,118000,2019-09-01,Active\n'
            'E008,Robert Zhang,Engineering,DevOps Engineer,112000,2022-08-01,Active\n'
        ),
        'performance_reviews_2024.txt': (
            'Performance Review Summary 2024\n'
            'Reviewed by: Laura Thompson, HR Director\n'
            '\n'
            'Outstanding (5/5):\n'
            '  - Sarah Chen: Led successful financial restructuring\n'
            '  - James Wilson: Delivered Project Beta 3 weeks early\n'
            '\n'
            'Exceeds Expectations (4/5):\n'
            '  - Elena Rodriguez: Managed 3 concurrent projects\n'
            '  - David Kim: Improved system performance by 40%\n'
            '  - Robert Zhang: Zero downtime deployments all year\n'
            '\n'
            'Meets Expectations (3/5):\n'
            '  - Marcus Johnson: Hit 92% of sales targets\n'
            '  - Priya Patel: Successful product launch campaign\n'
            '\n'
            'Overall Team Score: 4.1/5.0\n'
        ),
        'hiring_plan_2025.txt': (
            'Hiring Plan 2025\n'
            'Approved by: CEO - Michael Anderson\n'
            'Budget: $2,400,000 (combined salaries)\n'
            '\n'
            'Q1 Openings:\n'
            '  - 2x Backend Engineers (Python/FastAPI)\n'
            '  - 1x Data Engineer\n'
            '\n'
            'Q2 Openings:\n'
            '  - 1x Frontend Engineer (React)\n'
            '  - 1x QA Engineer\n'
            '  - 1x Product Manager\n'
            '\n'
            'Q3 Openings:\n'
            '  - 1x Security Engineer\n'
            '  - 1x Technical Writer\n'
            '\n'
            'Total Headcount Increase: 8\n'
            'Projected Year-End Headcount: 45\n'
        ),
        'training_schedule.txt': (
            'Employee Training Schedule 2025\n'
            '\n'
            'Mandatory Training:\n'
            '  - Security Awareness: All staff (Jan 15, 2025)\n'
            '  - Data Privacy (GDPR): All staff (Jan 22, 2025)\n'
            '  - Workplace Safety: All staff (Feb 5, 2025)\n'
            '\n'
            'Technical Training:\n'
            '  - Kubernetes Advanced: Engineering team (Mar 10-14, 2025)\n'
            '  - AWS Solutions Architect: DevOps team (Apr 7-11, 2025)\n'
            '  - Python FastAPI Workshop: Backend devs (Feb 19-20, 2025)\n'
            '\n'
            'Leadership Training:\n'
            '  - Management Essentials: Team leads (May 12-16, 2025)\n'
            '  - Strategic Planning: Directors (Jun 9-10, 2025)\n'
            '\n'
            'Total Training Hours per Employee: 40\n'
        ),
        'benefits_summary.txt': (
            'Employee Benefits Summary 2025\n'
            '\n'
            'Health Insurance:\n'
            '  - Medical: 100% company-paid for employee, 80% for dependents\n'
            '  - Dental: 90% company-paid\n'
            '  - Vision: 85% company-paid\n'
            '\n'
            'Retirement:\n'
            '  - 401(k) with 4% company match\n'
            '  - Vesting period: 2 years\n'
            '\n'
            'Time Off:\n'
            '  - PTO: 20 days/year (increases to 25 after 3 years)\n'
            '  - Sick Leave: 10 days/year\n'
            '  - Holidays: 11 federal holidays\n'
            '  - Parental Leave: 16 weeks paid\n'
            '\n'
            'Other Benefits:\n'
            '  - $5,000 annual learning budget\n'
            '  - Remote work: 2 days/week\n'
            '  - Stock options for senior staff\n'
        ),
    }

    for filename, content in hr_files.items():
        filepath = os.path.join(hr_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'  Created: {filepath}')

    # Verify file count
    total_files = 0
    for root, dirs, files in os.walk(DOCS_DIR):
        total_files += len(files)
    print(f'\nTotal files in {DOCS_DIR}: {total_files}')
    assert total_files == 18, f'Expected 18 files, got {total_files}'

    # Open terminal for the agent to write the script
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

    print(f'\nInitial state created successfully:')
    print(f'  Documents: {DOCS_DIR}')
    print(f'    - finance/ (6 files)')
    print(f'    - projects/ (7 files)')
    print(f'    - hr/ (5 files)')
    print(f'  Scripts dir: {SCRIPTS_DIR}')


create_initial()
