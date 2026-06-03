"""
Initial Setup: Extract 'Background and Context' section from grant_proposal.pdf
and save as Google Doc in Google Drive.
Task ID: osworld_multi_apps_pdf_to_gdocs_011
Domain: multi_apps (PDF + Chrome/Google Drive)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_011'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/grant_proposal.pdf'


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


def create_grant_proposal_pdf():
    """Create a realistic grant proposal PDF on the Desktop."""
    try:
        from fpdf import FPDF
    except ImportError:
        subprocess.run(['pip3', 'install', 'fpdf2'], check=True)
        from fpdf import FPDF

    os.makedirs(DESKTOP, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, 'Grant Proposal: Community Health Innovation Initiative', ln=True, align='C')
    pdf.ln(5)

    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, 'Submitted to: National Foundation for Health Research', ln=True, align='C')
    pdf.cell(0, 8, 'Submitted by: Riverside Community Health Center', ln=True, align='C')
    pdf.cell(0, 8, 'Date: March 2025', ln=True, align='C')
    pdf.ln(8)

    # Background and Context section
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '1. Background and Context', ln=True)
    pdf.ln(2)

    pdf.set_font('Helvetica', '', 11)
    background_text = (
        "The Riverside Community Health Center has served the greater metropolitan area for over 25 years, "
        "providing essential medical services to underserved and low-income populations. Despite significant "
        "advances in healthcare technology and treatment protocols, many residents in our service area continue "
        "to face barriers to accessing timely, quality healthcare."
    )
    pdf.multi_cell(0, 7, background_text)
    pdf.ln(4)

    context_text = (
        "Recent epidemiological data from the county health department indicates that chronic diseases such as "
        "diabetes, hypertension, and cardiovascular conditions disproportionately affect residents in ZIP codes "
        "94701, 94702, and 94703, where our primary service area is concentrated. The prevalence rate of Type 2 "
        "diabetes in these communities is 18.3%, nearly double the state average of 9.7%. Furthermore, emergency "
        "room utilization for preventable conditions has increased by 34% over the past three years, suggesting "
        "significant gaps in primary care access and preventive health education."
    )
    pdf.multi_cell(0, 7, context_text)
    pdf.ln(4)

    context_text2 = (
        "The COVID-19 pandemic further exacerbated these health disparities, with our community experiencing "
        "hospitalization rates 2.4 times higher than the regional average. Many community members lost health "
        "insurance coverage during the economic disruption, with our uninsured patient population growing from "
        "23% to 41% between 2020 and 2022. While coverage rates have partially recovered, an estimated 28% of "
        "our patients remain uninsured or underinsured as of the most recent census data."
    )
    pdf.multi_cell(0, 7, context_text2)
    pdf.ln(4)

    context_text3 = (
        "In response to these challenges, Riverside Community Health Center proposes to implement a comprehensive "
        "Community Health Innovation Initiative that leverages telehealth technology, community health workers, "
        "and data-driven care coordination to address chronic disease management and preventive care gaps. This "
        "initiative builds upon our existing partnerships with local schools, faith-based organizations, and "
        "social service agencies to create a robust network of community support."
    )
    pdf.multi_cell(0, 7, context_text3)
    pdf.ln(8)

    # Objectives section
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '2. Objectives', ln=True)
    pdf.ln(2)

    pdf.set_font('Helvetica', '', 11)
    objectives_text = (
        "The primary objectives of this initiative are to reduce preventable emergency room visits by 25% within "
        "two years, increase chronic disease screening rates to 85% of eligible patients, and train 15 community "
        "health workers to serve as cultural liaisons and care navigators within our target communities."
    )
    pdf.multi_cell(0, 7, objectives_text)
    pdf.ln(4)

    obj_list = [
        "Objective 1: Establish a telehealth platform serving 500+ patients monthly by Year 1.",
        "Objective 2: Deploy community health worker program across 5 neighborhood sites.",
        "Objective 3: Implement chronic disease registry for tracking and follow-up care.",
        "Objective 4: Achieve 30% reduction in uncontrolled hypertension rates by Year 2.",
        "Objective 5: Partner with 10 community organizations to expand outreach efforts."
    ]
    for obj in obj_list:
        pdf.multi_cell(0, 7, f"  {obj}")
        pdf.ln(2)
    pdf.ln(4)

    # Budget section
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '3. Budget', ln=True)
    pdf.ln(2)

    pdf.set_font('Helvetica', '', 11)
    budget_text = (
        "The total budget request for this two-year initiative is $487,500. The budget breakdown is as follows:"
    )
    pdf.multi_cell(0, 7, budget_text)
    pdf.ln(3)

    budget_items = [
        ("Personnel (60%)", "$292,500", "Program director, 15 community health workers, data analyst"),
        ("Technology & Equipment (20%)", "$97,500", "Telehealth platform, tablets, connectivity"),
        ("Training & Education (10%)", "$48,750", "Staff training, curriculum development, materials"),
        ("Evaluation & Reporting (5%)", "$24,375", "External evaluator, data collection, reporting"),
        ("Indirect Costs (5%)", "$24,375", "Administrative overhead at 5% rate"),
    ]

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(60, 8, 'Category', border=1)
    pdf.cell(35, 8, 'Amount', border=1)
    pdf.cell(0, 8, 'Description', border=1, ln=True)
    pdf.set_font('Helvetica', '', 10)
    for category, amount, description in budget_items:
        pdf.cell(60, 8, category, border=1)
        pdf.cell(35, 8, amount, border=1)
        pdf.cell(0, 8, description, border=1, ln=True)
    pdf.ln(6)

    # Evaluation Plan section
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '4. Evaluation Plan', ln=True)
    pdf.ln(2)

    pdf.set_font('Helvetica', '', 11)
    eval_text = (
        "The evaluation framework will employ a mixed-methods approach combining quantitative health outcome "
        "metrics with qualitative patient and community feedback. An independent external evaluator from the "
        "University of California School of Public Health will oversee all evaluation activities."
    )
    pdf.multi_cell(0, 7, eval_text)
    pdf.ln(4)

    eval_text2 = (
        "Key performance indicators include: monthly telehealth visit volumes, chronic disease screening "
        "completion rates, emergency department utilization rates, patient satisfaction scores (target: >4.2/5.0), "
        "community health worker caseload and outcomes, and health literacy assessment pre/post scores. "
        "Quarterly progress reports will be submitted to the funding agency, with a comprehensive mid-project "
        "evaluation at the 12-month mark and a final evaluation report at project completion."
    )
    pdf.multi_cell(0, 7, eval_text2)
    pdf.ln(4)

    eval_text3 = (
        "Data collection tools include electronic health record extraction, standardized patient surveys, "
        "community health worker activity logs, and focus groups with community members. All evaluation "
        "activities will comply with IRB-approved protocols for human subjects research."
    )
    pdf.multi_cell(0, 7, eval_text3)

    pdf.output(PDF_PATH)
    print(f'Grant proposal PDF created: {PDF_PATH}')


def setup_chrome_google_drive():
    """Set up Chrome to be open with Google Drive showing the grant_applications folder."""
    # Kill any existing Chrome instances to ensure clean state
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    time.sleep(2)

    # Launch Chrome with Google Drive opened
    # The VM is pre-configured with Google account sign-in
    launch_gui(
        'google-chrome --remote-debugging-port=1337 --no-first-run '
        '"https://drive.google.com/drive/folders/" ',
        delay_sec=3.0
    )
    print('Chrome launched with Google Drive')


def create_initial():
    """Main setup function."""
    # Step 1: Create the grant proposal PDF on Desktop
    create_grant_proposal_pdf()

    # Step 2: Launch Chrome with Google Drive
    setup_chrome_google_drive()

    print('GUI_READY: Chrome opened with Google Drive, grant_proposal.pdf on Desktop')


create_initial()
