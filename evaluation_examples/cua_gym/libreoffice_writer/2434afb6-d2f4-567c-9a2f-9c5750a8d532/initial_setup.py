"""
Initial Setup: Create five separate ODT policy documents with heading structure.
Task ID: writer_rm_064
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_064'


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


def create_odt(filepath, title, sections):
    """Create an ODT file with Heading 1 title and Heading 2 sections with body text."""
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H
    from odf.style import Style, TextProperties, ParagraphProperties

    doc = OpenDocumentText()

    # Add the main title as Heading 1
    h1 = H(outlinelevel=1, text=title)
    doc.text.addElement(h1)

    # Add each section
    for section_title, paragraphs in sections:
        h2 = H(outlinelevel=2, text=section_title)
        doc.text.addElement(h2)
        for para_text in paragraphs:
            p = P(text=para_text)
            doc.text.addElement(p)

    doc.save(filepath)
    print(f"Created: {filepath}")


def create_initial():
    # --- HR_Policies.odt ---
    create_odt(
        f"{WORKDIR}/HR_Policies.odt",
        "Human Resources Policies",
        [
            ("Recruitment and Hiring", [
                "All open positions must be posted internally for a minimum of five business days before external advertising begins. The hiring manager is responsible for creating a detailed job description that includes required qualifications, preferred skills, and salary range.",
                "Interview panels must consist of at least three members, including one representative from Human Resources. All candidates must complete a standardized assessment relevant to the position."
            ]),
            ("Employee Benefits", [
                "Full-time employees are eligible for health insurance coverage beginning on the first day of the month following their start date. The company offers three plan options: Basic, Standard, and Premium.",
                "Retirement contributions are matched up to 6% of annual salary. Employees become fully vested after three years of continuous service with the organization."
            ]),
            ("Leave and Attendance", [
                "Employees accrue 15 days of paid time off per year during their first three years of employment. After three years, accrual increases to 20 days per year.",
                "Sick leave is provided at a rate of 10 days per calendar year and does not carry over. Extended medical leave follows the provisions outlined in the Family and Medical Leave Act."
            ]),
            ("Performance Management", [
                "Annual performance reviews are conducted in December. Managers must complete written evaluations using the standardized review template and discuss results with each direct report.",
                "Performance improvement plans are initiated when an employee receives an overall rating below expectations for two consecutive review periods."
            ]),
        ]
    )

    # --- IT_Policies.odt ---
    create_odt(
        f"{WORKDIR}/IT_Policies.odt",
        "Information Technology Policies",
        [
            ("Acceptable Use Policy", [
                "Company-provided computing resources are intended primarily for business use. Limited personal use is permitted provided it does not interfere with job performance or violate any other company policy.",
                "Users must not attempt to bypass network security controls, install unauthorized software, or access systems or data for which they have not been granted permission."
            ]),
            ("Data Security", [
                "All sensitive data must be encrypted both in transit and at rest using AES-256 or equivalent encryption standards. Portable storage devices containing company data must use full-disk encryption.",
                "Access to production databases requires multi-factor authentication and must be logged. Database access reviews are conducted quarterly by the Information Security team."
            ]),
            ("Password Requirements", [
                "Passwords must be a minimum of 12 characters and include at least one uppercase letter, one lowercase letter, one digit, and one special character. Passwords expire every 90 days.",
                "Password reuse is prohibited for the last 12 passwords. Account lockout occurs after five consecutive failed login attempts."
            ]),
            ("Incident Response", [
                "All security incidents must be reported to the IT Security team within one hour of discovery. The incident response coordinator will assess severity and activate the appropriate response protocol.",
                "Post-incident reviews are mandatory for all Severity 1 and Severity 2 incidents. Findings and corrective actions must be documented within five business days."
            ]),
        ]
    )

    # --- Finance_Policies.odt ---
    create_odt(
        f"{WORKDIR}/Finance_Policies.odt",
        "Finance Department Policies",
        [
            ("Expense Reporting", [
                "All business expenses must be submitted within 30 calendar days of the transaction date. Receipts are required for any individual expense exceeding $25.00.",
                "Travel expenses must be pre-approved by the department manager for amounts under $2,000 and by the VP of Finance for amounts exceeding that threshold."
            ]),
            ("Procurement and Purchasing", [
                "Purchase orders are required for all goods and services exceeding $500. Purchases over $10,000 require three competitive bids and approval from the Chief Financial Officer.",
                "Preferred vendor agreements must be reviewed annually. New vendor onboarding requires completion of the Vendor Qualification Form and a credit reference check."
            ]),
            ("Budget Management", [
                "Department budgets are prepared annually during the fourth quarter planning cycle. Monthly variance reports must be submitted by the 10th business day of the following month.",
                "Budget transfers between line items up to $5,000 may be approved by the department head. Transfers exceeding $5,000 require Finance Committee approval."
            ]),
            ("Audit and Compliance", [
                "Internal audits are conducted on a rotating schedule, with each department reviewed at least once every two years. Audit findings must receive a management response within 30 days.",
                "The company undergoes an annual external audit by an independent accounting firm. All departments must cooperate fully and provide requested documentation within the specified deadlines."
            ]),
        ]
    )

    # --- Safety_Policies.odt ---
    create_odt(
        f"{WORKDIR}/Safety_Policies.odt",
        "Workplace Safety Policies",
        [
            ("General Safety Guidelines", [
                "All employees must complete safety orientation training within their first week of employment. Refresher training is required annually for all personnel.",
                "Personal protective equipment must be worn in designated areas at all times. The company provides required PPE at no cost to employees."
            ]),
            ("Emergency Procedures", [
                "Evacuation drills are conducted quarterly. All employees must know the location of the nearest two emergency exits and the designated assembly point for their work area.",
                "First aid kits are maintained on each floor and inspected monthly. At least two employees per floor must hold current first aid and CPR certifications."
            ]),
            ("Hazard Reporting", [
                "Employees must report unsafe conditions or near-miss incidents to their supervisor or the Safety Officer within 24 hours. Anonymous reports may be submitted through the safety hotline.",
                "The Safety Committee meets monthly to review reported hazards and incidents. Corrective actions are tracked to completion and verified by the Safety Officer."
            ]),
            ("Ergonomics", [
                "Workstation assessments are available to all employees upon request. The company provides adjustable chairs, monitor stands, and keyboard trays as standard equipment.",
                "Employees who spend more than six hours per day at a computer workstation must take a 10-minute break every two hours to reduce the risk of repetitive strain injuries."
            ]),
        ]
    )

    # --- Ethics_Policies.odt ---
    create_odt(
        f"{WORKDIR}/Ethics_Policies.odt",
        "Code of Ethics and Conduct",
        [
            ("Conflict of Interest", [
                "Employees must disclose any personal, financial, or familial relationships that could create a conflict of interest with their job responsibilities. Disclosures are reviewed by the Ethics Committee.",
                "Board members and senior executives must complete an annual conflict of interest questionnaire. Any identified conflicts must be managed through recusal or divestiture as determined by the Board."
            ]),
            ("Anti-Corruption and Bribery", [
                "The company strictly prohibits the giving or receiving of bribes, kickbacks, or other improper payments. This policy applies to all employees, contractors, and third-party agents.",
                "Gifts from vendors or clients exceeding $50 in value must be reported to the Compliance Officer. Entertainment expenses involving government officials require prior written approval."
            ]),
            ("Whistleblower Protection", [
                "Employees who report suspected violations of law or company policy in good faith are protected from retaliation. Reports may be made to a supervisor, the Ethics Hotline, or the General Counsel.",
                "All reports are investigated confidentially. The company prohibits any adverse employment action against individuals who cooperate with internal or external investigations."
            ]),
            ("Confidentiality and Non-Disclosure", [
                "Proprietary information, trade secrets, and confidential business data must not be disclosed to unauthorized parties during or after employment. All employees sign a confidentiality agreement upon hire.",
                "Electronic transmission of confidential documents must use approved secure channels. Physical documents classified as confidential must be stored in locked cabinets when not in active use."
            ]),
        ]
    )

    print("All 5 policy ODT files created successfully.")

    # Open LibreOffice Writer so the user has a starting point
    # Open the file manager showing /home/user so they can see all files
    launch_gui('libreoffice --writer', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
