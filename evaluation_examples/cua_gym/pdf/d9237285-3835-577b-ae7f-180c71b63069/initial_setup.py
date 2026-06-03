"""
Initial Setup: Create a 25-page policy handbook PDF with no bookmarks
Task ID: pdf_pw_010
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_010'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/policy_handbook.pdf'

# Page dimensions (Letter size)
W, H = 612, 792
MARGIN = 72
TEXT_W = W - 2 * MARGIN


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


def add_header(page, title, is_section_header=False):
    """Add a header title to a page."""
    if is_section_header:
        page.insert_text(
            pymupdf.Point(MARGIN, 72),
            title,
            fontsize=22,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )
        # Underline
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN, 80), pymupdf.Point(W - MARGIN, 80))
        shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
        shape.commit()
        return 100
    else:
        page.insert_text(
            pymupdf.Point(MARGIN, 72),
            title,
            fontsize=14,
            fontname="hebo",
            color=(0.2, 0.2, 0.2),
        )
        return 95


def add_body_text(page, text, start_y=100):
    """Add body text to a page using a textbox."""
    rect = pymupdf.Rect(MARGIN, start_y, W - MARGIN, H - MARGIN)
    page.insert_textbox(
        rect,
        text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )


def add_page_number(page, num):
    """Add page number at bottom center."""
    page.insert_text(
        pymupdf.Point(W / 2 - 10, H - 40),
        str(num),
        fontsize=10,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ========== SECTION 1: Introduction (pages 1-2) ==========
    # Page 1
    p = doc.new_page(width=W, height=H)
    add_header(p, "Introduction", is_section_header=True)
    add_body_text(p, (
        "Welcome to the Meridian Technologies Employee Policy Handbook. This document serves as "
        "a comprehensive guide to the policies, procedures, and expectations that govern our workplace. "
        "Every employee is expected to read, understand, and comply with the guidelines outlined herein.\n\n"
        "Meridian Technologies was founded in 2008 with a mission to deliver innovative software solutions "
        "to enterprises worldwide. Over the past sixteen years, we have grown from a small startup of twelve "
        "people to a global organization with over 3,400 employees across fourteen offices in North America, "
        "Europe, and Asia-Pacific.\n\n"
        "Our core values -- Integrity, Innovation, Collaboration, and Excellence -- are the foundation of "
        "everything we do. These values guide our interactions with clients, partners, and each other. "
        "We believe that a respectful, inclusive, and transparent workplace is essential to achieving our "
        "business goals and fostering personal growth.\n\n"
        "This handbook is effective as of January 1, 2025 and supersedes all previous versions. Policies "
        "may be updated periodically; employees will be notified of material changes via email and the "
        "company intranet. Questions regarding any policy should be directed to your department manager "
        "or the Human Resources team at hr@meridiantech.com.\n\n"
        "By continuing your employment with Meridian Technologies, you acknowledge that you have received "
        "and reviewed this handbook and agree to abide by the policies contained within."
    ))
    add_page_number(p, 1)

    # Page 2
    p = doc.new_page(width=W, height=H)
    add_header(p, "Company Overview")
    add_body_text(p, (
        "Meridian Technologies operates in three primary business segments: Enterprise Cloud Services, "
        "Data Analytics Solutions, and Cybersecurity Products. Our flagship platform, MeridianCloud, "
        "serves over 2,200 enterprise customers globally, processing more than 15 billion transactions "
        "per month.\n\n"
        "Leadership Team:\n"
        "  - CEO: Dr. Amanda Richardson\n"
        "  - CTO: James Park\n"
        "  - CFO: Sarah Okonkwo\n"
        "  - VP of Engineering: Michael Torres\n"
        "  - VP of Human Resources: Lisa Chen\n"
        "  - VP of Sales: Robert Andersen\n\n"
        "Our headquarters is located at 4500 Innovation Drive, Austin, TX 78759. Regional offices include "
        "San Francisco, New York, London, Berlin, Singapore, and Sydney. The company is publicly traded "
        "on NASDAQ under the ticker symbol MRDN.\n\n"
        "Fiscal year 2024 highlights:\n"
        "  - Annual revenue: $892 million (up 18% year-over-year)\n"
        "  - Customer retention rate: 96.3%\n"
        "  - Employee satisfaction score: 4.2 out of 5.0\n"
        "  - R&D investment: $178 million (20% of revenue)"
    ))
    add_page_number(p, 2)

    # ========== SECTION 2: Code of Conduct (pages 3-7) ==========
    # Page 3
    p = doc.new_page(width=W, height=H)
    add_header(p, "Code of Conduct", is_section_header=True)
    add_body_text(p, (
        "All employees of Meridian Technologies are expected to conduct themselves with the highest "
        "standards of professionalism, ethics, and integrity. This Code of Conduct establishes the "
        "behavioral framework that supports our company values and ensures a positive work environment.\n\n"
        "1. Professional Behavior\n\n"
        "Employees must treat all colleagues, clients, vendors, and visitors with dignity and respect. "
        "Harassment, discrimination, bullying, or intimidation of any kind will not be tolerated. This "
        "includes but is not limited to behavior based on race, gender, age, religion, sexual orientation, "
        "disability, national origin, or any other protected characteristic.\n\n"
        "2. Conflict of Interest\n\n"
        "Employees must avoid situations where personal interests conflict, or appear to conflict, with "
        "the interests of the company. Any potential conflict of interest must be disclosed immediately "
        "to your direct supervisor and the Ethics Committee. Examples include:\n"
        "  - Holding a financial interest in a competitor or supplier\n"
        "  - Engaging in outside employment that interferes with job responsibilities\n"
        "  - Accepting gifts or entertainment valued above $150 from vendors or clients"
    ))
    add_page_number(p, 3)

    # Page 4
    p = doc.new_page(width=W, height=H)
    add_header(p, "Code of Conduct (continued)")
    add_body_text(p, (
        "3. Confidentiality and Data Protection\n\n"
        "Employees have a duty to protect confidential company information, trade secrets, and intellectual "
        "property. This obligation extends beyond the term of employment. Confidential information includes "
        "but is not limited to: source code, customer data, financial records, strategic plans, and "
        "proprietary algorithms.\n\n"
        "All employees must comply with the company's Information Security Policy (ISP-2024-003) and "
        "complete annual cybersecurity awareness training. Violations may result in disciplinary action "
        "up to and including termination, as well as potential legal consequences.\n\n"
        "4. Use of Company Resources\n\n"
        "Company equipment, software, networks, and facilities are provided for business purposes. Limited "
        "personal use is permitted provided it does not interfere with job performance, violate any policy, "
        "or consume excessive resources. Employees should have no expectation of privacy when using company "
        "systems, as the company reserves the right to monitor usage.\n\n"
        "5. Social Media and Public Statements\n\n"
        "Employees must exercise caution when using social media or making public statements that could "
        "be associated with Meridian Technologies. Do not disclose non-public information, disparage the "
        "company or colleagues, or represent personal opinions as company positions."
    ))
    add_page_number(p, 4)

    # Page 5
    p = doc.new_page(width=W, height=H)
    add_header(p, "Workplace Safety and Reporting")
    add_body_text(p, (
        "6. Workplace Violence Prevention\n\n"
        "Meridian Technologies maintains a zero-tolerance policy toward workplace violence. Any act or "
        "threat of physical violence, intimidation, or coercion is strictly prohibited. Employees who "
        "witness or experience threatening behavior must report it immediately to Security (ext. 5555) "
        "or their manager.\n\n"
        "7. Substance Abuse\n\n"
        "The use, possession, distribution, or sale of illegal drugs on company premises or during work "
        "hours is prohibited. Employees may not report to work under the influence of alcohol or illegal "
        "substances. Prescription medications that may impair performance must be reported to HR "
        "confidentially. The company offers an Employee Assistance Program (EAP) for those seeking help "
        "with substance abuse issues.\n\n"
        "8. Reporting Violations\n\n"
        "Employees are encouraged to report suspected violations of this Code of Conduct, company policies, "
        "or applicable laws through any of the following channels:\n"
        "  - Direct supervisor or department manager\n"
        "  - Human Resources (hr@meridiantech.com)\n"
        "  - Ethics Hotline: 1-800-555-0142 (anonymous, available 24/7)\n"
        "  - Online reporting portal: ethics.meridiantech.com\n\n"
        "Meridian Technologies prohibits retaliation against any employee who reports a concern in good faith."
    ))
    add_page_number(p, 5)

    # Page 6
    p = doc.new_page(width=W, height=H)
    add_header(p, "Disciplinary Procedures")
    add_body_text(p, (
        "9. Disciplinary Actions\n\n"
        "Violations of the Code of Conduct or company policies may result in disciplinary action. The "
        "severity of the response will be proportional to the nature and circumstances of the violation. "
        "Disciplinary measures may include:\n\n"
        "  Level 1: Verbal warning with documentation\n"
        "  Level 2: Written warning placed in personnel file\n"
        "  Level 3: Suspension without pay (duration determined by severity)\n"
        "  Level 4: Termination of employment\n\n"
        "Serious violations such as theft, fraud, harassment, or endangering others may result in immediate "
        "termination without progressive discipline. All disciplinary actions will be documented and "
        "maintained in the employee's personnel file.\n\n"
        "10. Appeals Process\n\n"
        "Employees who believe a disciplinary action was unjust may file an appeal within fifteen (15) "
        "business days of receiving the disciplinary notice. Appeals should be submitted in writing to "
        "the VP of Human Resources. An independent review panel consisting of one HR representative, "
        "one peer-level employee, and one senior manager will evaluate the appeal and issue a decision "
        "within thirty (30) business days. The panel's decision is final."
    ))
    add_page_number(p, 6)

    # Page 7
    p = doc.new_page(width=W, height=H)
    add_header(p, "Compliance and Ethics Training")
    add_body_text(p, (
        "11. Mandatory Training Requirements\n\n"
        "All employees must complete the following training programs within their first ninety (90) days "
        "of employment and annually thereafter:\n\n"
        "  - Code of Conduct Overview (2 hours)\n"
        "  - Anti-Harassment and Discrimination Prevention (3 hours)\n"
        "  - Cybersecurity Awareness (2 hours)\n"
        "  - Data Privacy and GDPR Compliance (1.5 hours)\n"
        "  - Workplace Safety Fundamentals (1 hour)\n\n"
        "Managers and team leads must additionally complete:\n"
        "  - Leadership Ethics Seminar (4 hours, annually)\n"
        "  - Inclusive Management Practices (3 hours, annually)\n\n"
        "Training records are maintained by the Learning and Development team. Failure to complete "
        "required training within the designated timeframe may result in temporary suspension of system "
        "access and potential disciplinary action.\n\n"
        "12. Acknowledgment\n\n"
        "Each employee must sign an acknowledgment form confirming receipt and understanding of this "
        "Code of Conduct. The signed acknowledgment will be retained in the employee's personnel file. "
        "New hires must submit the acknowledgment within their first week of employment."
    ))
    add_page_number(p, 7)

    # ========== SECTION 3: Leave Policy (pages 8-11) ==========
    # Page 8
    p = doc.new_page(width=W, height=H)
    add_header(p, "Leave Policy", is_section_header=True)
    add_body_text(p, (
        "Meridian Technologies provides a comprehensive leave program designed to support employees' "
        "work-life balance, health, and personal needs. All leave policies comply with applicable "
        "federal, state, and local laws.\n\n"
        "1. Paid Time Off (PTO)\n\n"
        "PTO accrual rates are based on years of service:\n\n"
        "  Years 0-2:   15 days per year (1.25 days/month)\n"
        "  Years 3-5:   20 days per year (1.67 days/month)\n"
        "  Years 6-10:  25 days per year (2.08 days/month)\n"
        "  Years 10+:   30 days per year (2.50 days/month)\n\n"
        "PTO may be used for vacation, personal business, or illness. Employees may carry over up to "
        "five (5) unused PTO days into the following calendar year. Unused PTO beyond the carryover "
        "limit will be forfeited on December 31st. PTO requests must be submitted through the HR portal "
        "at least two (2) weeks in advance for absences of three or more consecutive days.\n\n"
        "2. Sick Leave\n\n"
        "In addition to PTO, employees receive ten (10) days of dedicated sick leave per year. Sick leave "
        "may be used for personal illness, medical appointments, or caring for an immediate family member. "
        "A doctor's note is required for absences exceeding three (3) consecutive sick days."
    ))
    add_page_number(p, 8)

    # Page 9
    p = doc.new_page(width=W, height=H)
    add_header(p, "Family and Medical Leave")
    add_body_text(p, (
        "3. Family and Medical Leave Act (FMLA)\n\n"
        "Eligible employees may take up to twelve (12) weeks of unpaid, job-protected leave per year "
        "under FMLA for the following reasons:\n\n"
        "  - Birth and care of a newborn child\n"
        "  - Placement of a child for adoption or foster care\n"
        "  - Care for an immediate family member with a serious health condition\n"
        "  - Medical leave when unable to work due to a serious health condition\n\n"
        "To be eligible, employees must have worked for Meridian Technologies for at least twelve (12) "
        "months and have completed at least 1,250 hours of service in the twelve months preceding the "
        "leave request.\n\n"
        "4. Parental Leave\n\n"
        "Meridian Technologies provides sixteen (16) weeks of paid parental leave for the birth or "
        "adoption of a child. This benefit is available to all employees regardless of gender who have "
        "been employed for at least one (1) year. Parental leave must be taken within the first twelve "
        "(12) months following the birth or adoption. Employees may take the leave continuously or in "
        "increments of no less than one (1) week, subject to manager approval.\n\n"
        "5. Bereavement Leave\n\n"
        "Employees are entitled to five (5) days of paid bereavement leave for the death of an immediate "
        "family member (spouse, child, parent, sibling, grandparent) and three (3) days for extended "
        "family members."
    ))
    add_page_number(p, 9)

    # Page 10
    p = doc.new_page(width=W, height=H)
    add_header(p, "Additional Leave Types")
    add_body_text(p, (
        "6. Jury Duty\n\n"
        "Employees summoned for jury duty will receive their regular salary for up to ten (10) business "
        "days per calendar year. Employees must provide a copy of the summons to their manager and HR "
        "within two (2) business days of receipt. If jury service extends beyond ten days, additional "
        "leave will be unpaid unless otherwise required by law.\n\n"
        "7. Military Leave\n\n"
        "Meridian Technologies complies with the Uniformed Services Employment and Reemployment Rights "
        "Act (USERRA). Employees who serve in the uniformed services are entitled to leave and "
        "reemployment rights as provided by law. The company will pay the difference between military "
        "pay and regular salary for up to six (6) months of active duty per deployment.\n\n"
        "8. Sabbatical Leave\n\n"
        "Employees who have completed seven (7) consecutive years of service are eligible for a four-week "
        "paid sabbatical. Sabbaticals must be pre-approved by the department head and VP of Human "
        "Resources at least three (3) months in advance. Sabbatical leave may be used for personal "
        "development, travel, community service, or academic pursuits. Employees may take one sabbatical "
        "every seven years of service.\n\n"
        "9. Volunteer Time Off\n\n"
        "Employees receive sixteen (16) hours of paid volunteer time off per year to support approved "
        "charitable organizations. Requests must be submitted through the Community Engagement portal."
    ))
    add_page_number(p, 10)

    # Page 11
    p = doc.new_page(width=W, height=H)
    add_header(p, "Leave Administration")
    add_body_text(p, (
        "10. Leave Request Procedures\n\n"
        "All leave requests must be submitted through the MeridianPeople HR portal. The following "
        "guidelines apply:\n\n"
        "  - Planned absences (vacation, sabbatical): Submit at least 14 calendar days in advance\n"
        "  - Short-notice absences (sick, emergency): Notify your manager before your scheduled start time\n"
        "  - Extended leave (FMLA, parental): Submit request at least 30 days before anticipated start date\n"
        "  - Manager approval required for all planned absences of 3+ consecutive days\n\n"
        "11. Return to Work\n\n"
        "Employees returning from medical leave of five (5) or more consecutive days must provide a "
        "fitness-for-duty certification from their healthcare provider before resuming work. The company "
        "will make reasonable accommodations as required by the Americans with Disabilities Act (ADA).\n\n"
        "12. Leave Abuse\n\n"
        "Patterns of leave abuse, including but not limited to frequent Monday/Friday absences, "
        "unexplained absences, or failure to follow proper notification procedures, may result in "
        "disciplinary action. The company reserves the right to require medical documentation for any "
        "absence when a pattern of abuse is suspected."
    ))
    add_page_number(p, 11)

    # ========== SECTION 4: Benefits (pages 12-17) ==========
    # Page 12
    p = doc.new_page(width=W, height=H)
    add_header(p, "Benefits", is_section_header=True)
    add_body_text(p, (
        "Meridian Technologies offers a competitive benefits package designed to attract and retain "
        "top talent. Benefits are effective on the first day of the month following your hire date.\n\n"
        "1. Health Insurance\n\n"
        "The company offers three medical plan options through BlueCross BlueShield:\n\n"
        "  Plan A (PPO Premium): $125/month employee, $375/month family\n"
        "    - $500 individual deductible, $1,000 family deductible\n"
        "    - 90% in-network coverage after deductible\n"
        "    - $20 copay for primary care, $40 for specialists\n\n"
        "  Plan B (PPO Standard): $85/month employee, $255/month family\n"
        "    - $1,500 individual deductible, $3,000 family deductible\n"
        "    - 80% in-network coverage after deductible\n"
        "    - $30 copay for primary care, $60 for specialists\n\n"
        "  Plan C (HDHP with HSA): $45/month employee, $135/month family\n"
        "    - $3,000 individual deductible, $6,000 family deductible\n"
        "    - 80% coverage after deductible\n"
        "    - Company contributes $750/$1,500 annually to HSA"
    ))
    add_page_number(p, 12)

    # Page 13
    p = doc.new_page(width=W, height=H)
    add_header(p, "Dental, Vision, and Life Insurance")
    add_body_text(p, (
        "2. Dental Insurance\n\n"
        "Dental coverage is provided through Delta Dental at the following rates:\n"
        "  - Employee only: $22/month\n"
        "  - Employee + spouse: $44/month\n"
        "  - Employee + family: $66/month\n"
        "  - Preventive care covered at 100%, basic procedures at 80%, major procedures at 50%\n"
        "  - Annual maximum benefit: $2,000 per covered individual\n"
        "  - Orthodontia coverage (dependents under 19): 50% up to $2,500 lifetime maximum\n\n"
        "3. Vision Insurance\n\n"
        "Vision coverage is provided through VSP at the following rates:\n"
        "  - Employee only: $8/month\n"
        "  - Employee + family: $20/month\n"
        "  - Annual eye exam: $10 copay\n"
        "  - Frames allowance: $200 every 24 months\n"
        "  - Contact lens allowance: $150 annually\n\n"
        "4. Life and Disability Insurance\n\n"
        "Meridian Technologies provides the following at no cost to employees:\n"
        "  - Basic life insurance: 2x annual salary (up to $500,000)\n"
        "  - Accidental death and dismemberment (AD&D): 2x annual salary\n"
        "  - Short-term disability: 60% of salary for up to 26 weeks\n"
        "  - Long-term disability: 60% of salary after 26 weeks, up to age 65"
    ))
    add_page_number(p, 13)

    # Page 14
    p = doc.new_page(width=W, height=H)
    add_header(p, "Retirement and Financial Benefits")
    add_body_text(p, (
        "5. 401(k) Retirement Plan\n\n"
        "Employees are eligible to participate in the company's 401(k) plan from their date of hire. "
        "Key features include:\n\n"
        "  - Employee contributions: Up to IRS annual limit ($23,000 for 2025)\n"
        "  - Catch-up contributions: Additional $7,500 for employees age 50+\n"
        "  - Company match: 100% of first 4% + 50% of next 2% (maximum 5% match)\n"
        "  - Vesting schedule: Immediate vesting on employee contributions; company match vests\n"
        "    25% per year over four years\n"
        "  - Investment options: 22 mutual funds, 5 target-date funds, and company stock\n"
        "  - Roth 401(k) option available\n\n"
        "6. Employee Stock Purchase Plan (ESPP)\n\n"
        "Eligible employees may purchase company stock at a 15% discount through payroll deductions. "
        "Offering periods are six months (January-June, July-December). Maximum contribution is 10% of "
        "base salary or $25,000 per year, whichever is less.\n\n"
        "7. Tuition Reimbursement\n\n"
        "Full-time employees with at least one year of service may receive up to $8,000 per calendar "
        "year for job-related coursework at accredited institutions. A grade of B or higher (or equivalent) "
        "is required for reimbursement. Pre-approval from manager and HR is required."
    ))
    add_page_number(p, 14)

    # Page 15
    p = doc.new_page(width=W, height=H)
    add_header(p, "Wellness and Additional Benefits")
    add_body_text(p, (
        "8. Wellness Program\n\n"
        "Meridian Technologies is committed to employee well-being. Our comprehensive wellness program "
        "includes:\n\n"
        "  - On-site fitness center (Austin HQ) with personal training sessions\n"
        "  - Gym membership reimbursement: Up to $75/month for remote employees\n"
        "  - Annual biometric screening with $200 wellness incentive\n"
        "  - Mental health support: 12 free counseling sessions per year through EAP\n"
        "  - Meditation and mindfulness app subscription (Calm or Headspace)\n"
        "  - Quarterly wellness challenges with prizes\n"
        "  - Standing desks and ergonomic assessments for all office employees\n\n"
        "9. Commuter Benefits\n\n"
        "Employees may set aside up to $300/month pre-tax for qualified commuter expenses including "
        "public transit passes, vanpool fees, and qualified parking. The company provides free shuttle "
        "service from downtown Austin to the headquarters campus.\n\n"
        "10. Employee Assistance Program (EAP)\n\n"
        "The EAP provides confidential support for personal and work-related issues including:\n"
        "  - Stress management and mental health counseling\n"
        "  - Financial planning and debt management\n"
        "  - Legal consultation (30-minute sessions)\n"
        "  - Work-life balance resources\n"
        "  - Substance abuse referrals"
    ))
    add_page_number(p, 15)

    # Page 16
    p = doc.new_page(width=W, height=H)
    add_header(p, "Technology and Remote Work Benefits")
    add_body_text(p, (
        "11. Technology Allowance\n\n"
        "To support productivity, Meridian Technologies provides the following technology benefits:\n\n"
        "  - Company-issued laptop (refreshed every 3 years)\n"
        "  - Mobile phone stipend: $75/month\n"
        "  - Home office setup allowance: $1,500 one-time (remote employees)\n"
        "  - Annual technology refresh budget: $500 for peripherals and accessories\n"
        "  - Software licenses for approved productivity tools\n\n"
        "12. Remote Work Policy\n\n"
        "Meridian Technologies supports a hybrid work model. Policies vary by role and department:\n\n"
        "  - Fully remote: Available for approved positions with manager and VP approval\n"
        "  - Hybrid (3 days office, 2 days remote): Default for most positions\n"
        "  - On-site: Required for certain operational and laboratory roles\n\n"
        "Remote work expectations:\n"
        "  - Maintain a dedicated, professional workspace\n"
        "  - Be available during core hours (10:00 AM - 3:00 PM local time)\n"
        "  - Attend required in-person meetings and team events\n"
        "  - Ensure reliable internet connection (minimum 50 Mbps download)\n"
        "  - Comply with all information security policies when working remotely"
    ))
    add_page_number(p, 16)

    # Page 17
    p = doc.new_page(width=W, height=H)
    add_header(p, "Benefits Enrollment and Changes")
    add_body_text(p, (
        "13. Open Enrollment\n\n"
        "The annual open enrollment period runs from November 1 through November 30. During this period, "
        "employees may make changes to their benefit elections for the following plan year. Changes take "
        "effect January 1. Outside of open enrollment, changes may only be made within thirty (30) days "
        "of a qualifying life event.\n\n"
        "Qualifying life events include:\n"
        "  - Marriage or divorce\n"
        "  - Birth or adoption of a child\n"
        "  - Death of a dependent\n"
        "  - Loss of other health coverage\n"
        "  - Change in employment status of spouse/partner\n\n"
        "14. COBRA Continuation Coverage\n\n"
        "Upon termination of employment or reduction in hours that results in loss of coverage, "
        "employees and their dependents may elect to continue health, dental, and vision coverage "
        "under COBRA for up to eighteen (18) months (or thirty-six months for certain qualifying events). "
        "COBRA participants are responsible for the full premium plus a 2% administrative fee.\n\n"
        "15. Benefits Contact Information\n\n"
        "  Benefits Administration: benefits@meridiantech.com\n"
        "  Phone: (512) 555-0199 (Mon-Fri, 8:00 AM - 5:00 PM CT)\n"
        "  MeridianPeople Portal: people.meridiantech.com"
    ))
    add_page_number(p, 17)

    # ========== SECTION 5: Safety Guidelines (pages 18-21) ==========
    # Page 18
    p = doc.new_page(width=W, height=H)
    add_header(p, "Safety Guidelines", is_section_header=True)
    add_body_text(p, (
        "The safety and well-being of our employees is a top priority at Meridian Technologies. All "
        "employees share the responsibility of maintaining a safe working environment. This section "
        "outlines our safety policies, emergency procedures, and reporting requirements.\n\n"
        "1. General Safety Rules\n\n"
        "  - Report all unsafe conditions, near-misses, and injuries immediately to your supervisor\n"
        "  - Keep work areas clean, organized, and free from hazards\n"
        "  - Know the location of fire extinguishers, first aid kits, and emergency exits\n"
        "  - Do not block emergency exits, fire lanes, or electrical panels\n"
        "  - Follow all posted safety signs, labels, and instructions\n"
        "  - Use personal protective equipment (PPE) when required\n"
        "  - Report any malfunctioning equipment before use\n\n"
        "2. Emergency Evacuation Procedures\n\n"
        "Each facility has designated evacuation routes posted on every floor. In the event of an "
        "emergency requiring evacuation:\n\n"
        "  a. Remain calm and proceed to the nearest emergency exit\n"
        "  b. Do not use elevators\n"
        "  c. Assist colleagues with disabilities as needed\n"
        "  d. Proceed to the designated assembly point for your building\n"
        "  e. Report to your floor warden for a headcount\n"
        "  f. Do not re-enter the building until authorized by emergency personnel"
    ))
    add_page_number(p, 18)

    # Page 19
    p = doc.new_page(width=W, height=H)
    add_header(p, "Fire Safety and First Aid")
    add_body_text(p, (
        "3. Fire Safety\n\n"
        "Meridian Technologies conducts fire drills quarterly at all facilities. All employees must "
        "participate in scheduled drills. Key fire safety protocols:\n\n"
        "  - Fire extinguishers are inspected monthly and located every 75 feet\n"
        "  - Smoke detectors and sprinkler systems are tested semi-annually\n"
        "  - Fire suppression systems in server rooms use FM-200 clean agent\n"
        "  - Cooking appliances in break rooms have automatic fire suppression\n"
        "  - Candles, space heaters, and other open flame devices are prohibited\n\n"
        "RACE protocol for fire response:\n"
        "  R - Rescue anyone in immediate danger\n"
        "  A - Alarm: Pull the nearest fire alarm and call 911\n"
        "  C - Contain: Close doors and windows to slow fire spread\n"
        "  E - Evacuate or Extinguish (only if trained and fire is small)\n\n"
        "4. First Aid and Medical Emergencies\n\n"
        "First aid kits are located in break rooms, reception areas, and laboratories. At least two "
        "trained first aid responders are designated per floor during business hours. Automated External "
        "Defibrillators (AEDs) are located at main entrances and fitness center.\n\n"
        "For medical emergencies:\n"
        "  - Call 911 immediately\n"
        "  - Notify building security at ext. 5555\n"
        "  - Administer first aid only if trained to do so\n"
        "  - Stay with the injured person until help arrives"
    ))
    add_page_number(p, 19)

    # Page 20
    p = doc.new_page(width=W, height=H)
    add_header(p, "Ergonomics and Laboratory Safety")
    add_body_text(p, (
        "5. Ergonomic Safety\n\n"
        "Given the nature of our work, preventing repetitive strain injuries is essential. Guidelines:\n\n"
        "  - Position monitor at arm's length, top of screen at or slightly below eye level\n"
        "  - Keep wrists neutral when typing; use wrist rests as needed\n"
        "  - Feet should be flat on the floor or on a footrest\n"
        "  - Take a 5-minute break every hour to stretch and move\n"
        "  - Request an ergonomic assessment from Facilities (facilities@meridiantech.com)\n"
        "  - Standing desk users should alternate between sitting and standing every 30-60 minutes\n\n"
        "6. Laboratory and Hardware Lab Safety\n\n"
        "Employees working in hardware testing labs or R&D laboratories must:\n\n"
        "  - Complete laboratory safety training before access is granted\n"
        "  - Wear appropriate PPE (safety glasses, ESD wrist straps, gloves as needed)\n"
        "  - Follow all material handling and chemical storage procedures\n"
        "  - Never work alone in the lab during off-hours\n"
        "  - Keep Safety Data Sheets (SDS) accessible for all chemicals\n"
        "  - Report equipment malfunctions immediately to the Lab Manager\n"
        "  - Maintain clean workbenches and proper waste disposal\n\n"
        "7. Electrical Safety\n\n"
        "  - Only qualified electricians may perform electrical work\n"
        "  - Report frayed cords, damaged outlets, or sparking equipment immediately\n"
        "  - Do not overload power strips or daisy-chain extension cords\n"
        "  - Server room access requires badge authentication and ESD compliance"
    ))
    add_page_number(p, 20)

    # Page 21
    p = doc.new_page(width=W, height=H)
    add_header(p, "Incident Reporting and Safety Committees")
    add_body_text(p, (
        "8. Incident Reporting\n\n"
        "All workplace incidents, injuries, and near-misses must be reported within twenty-four (24) "
        "hours using the Incident Report Form available on the MeridianPeople portal. Reports should "
        "include:\n\n"
        "  - Date, time, and location of the incident\n"
        "  - Names of persons involved and witnesses\n"
        "  - Description of what happened\n"
        "  - Injuries sustained and first aid administered\n"
        "  - Contributing factors and suggested preventive measures\n\n"
        "The Environmental Health and Safety (EHS) team will investigate all reported incidents within "
        "five (5) business days and implement corrective actions as needed.\n\n"
        "9. Safety Committees\n\n"
        "Each facility has a Safety Committee comprising representatives from various departments. "
        "Committee responsibilities include:\n\n"
        "  - Conducting monthly safety inspections\n"
        "  - Reviewing incident reports and recommending improvements\n"
        "  - Organizing safety training and awareness campaigns\n"
        "  - Advising management on safety-related investments\n"
        "  - Ensuring compliance with OSHA regulations\n\n"
        "Safety Committee meetings are held on the first Wednesday of each month. Meeting minutes are "
        "published on the company intranet within one week.\n\n"
        "10. Workers' Compensation\n\n"
        "Employees who are injured on the job are covered by workers' compensation insurance. Report "
        "injuries immediately to your supervisor and HR to initiate a claim."
    ))
    add_page_number(p, 21)

    # ========== SECTION 6: Appendix (pages 22-25) ==========
    # Page 22
    p = doc.new_page(width=W, height=H)
    add_header(p, "Appendix", is_section_header=True)
    add_body_text(p, (
        "Appendix A: Key Contacts and Resources\n\n"
        "Human Resources Department\n"
        "  General Inquiries: hr@meridiantech.com | (512) 555-0100\n"
        "  Benefits: benefits@meridiantech.com | (512) 555-0199\n"
        "  Recruitment: careers@meridiantech.com | (512) 555-0150\n"
        "  VP of HR: Lisa Chen | lisa.chen@meridiantech.com\n\n"
        "Information Technology\n"
        "  IT Help Desk: helpdesk@meridiantech.com | ext. 4000\n"
        "  Security Incidents: security@meridiantech.com | ext. 4001\n"
        "  CTO: James Park | james.park@meridiantech.com\n\n"
        "Facilities Management\n"
        "  General: facilities@meridiantech.com | ext. 3000\n"
        "  Building Security: security@meridiantech.com | ext. 5555\n"
        "  Maintenance Requests: facilities.meridiantech.com/request\n\n"
        "Legal Department\n"
        "  General Counsel: legal@meridiantech.com | (512) 555-0175\n"
        "  Compliance: compliance@meridiantech.com | (512) 555-0176\n\n"
        "Ethics and Compliance\n"
        "  Ethics Hotline: 1-800-555-0142 (24/7, anonymous)\n"
        "  Online Portal: ethics.meridiantech.com\n"
        "  Ethics Committee Chair: Dr. Patricia Nguyen"
    ))
    add_page_number(p, 22)

    # Page 23
    p = doc.new_page(width=W, height=H)
    add_header(p, "Appendix B: Policy Reference Numbers")
    add_body_text(p, (
        "The following is a reference list of all company policies mentioned in this handbook, along "
        "with their document numbers for record-keeping purposes:\n\n"
        "  POL-HR-001    Employee Code of Conduct\n"
        "  POL-HR-002    Anti-Harassment Policy\n"
        "  POL-HR-003    Equal Employment Opportunity Policy\n"
        "  POL-HR-004    Paid Time Off Policy\n"
        "  POL-HR-005    Family and Medical Leave Policy\n"
        "  POL-HR-006    Remote Work Policy\n"
        "  POL-HR-007    Dress Code Policy\n"
        "  POL-HR-008    Performance Review Policy\n"
        "  POL-HR-009    Separation and Exit Policy\n"
        "  POL-HR-010    Employee Referral Program\n\n"
        "  POL-IT-001    Acceptable Use Policy\n"
        "  POL-IT-002    Password and Access Control Policy\n"
        "  POL-IT-003    Data Classification Policy\n"
        "  ISP-2024-003  Information Security Policy\n"
        "  POL-IT-005    BYOD (Bring Your Own Device) Policy\n"
        "  POL-IT-006    Incident Response Plan\n\n"
        "  POL-FIN-001   Travel and Expense Policy\n"
        "  POL-FIN-002   Procurement Policy\n"
        "  POL-FIN-003   Corporate Credit Card Policy\n\n"
        "  POL-SAF-001   Workplace Safety Policy\n"
        "  POL-SAF-002   Emergency Action Plan\n"
        "  POL-SAF-003   Laboratory Safety Policy\n"
        "  POL-SAF-004   Ergonomics Program"
    ))
    add_page_number(p, 23)

    # Page 24
    p = doc.new_page(width=W, height=H)
    add_header(p, "Appendix C: Acknowledgment Forms")
    add_body_text(p, (
        "EMPLOYEE HANDBOOK ACKNOWLEDGMENT\n\n"
        "I, _________________________, acknowledge that I have received and reviewed the Meridian "
        "Technologies Employee Policy Handbook (Effective January 1, 2025).\n\n"
        "I understand that:\n\n"
        "1. This handbook is not an employment contract and does not create contractual obligations.\n\n"
        "2. My employment with Meridian Technologies is at-will, meaning either party may terminate "
        "the employment relationship at any time, with or without cause or notice, subject to applicable "
        "law.\n\n"
        "3. The company reserves the right to modify, supplement, or rescind any policy or provision "
        "in this handbook at any time, with or without notice.\n\n"
        "4. I am responsible for reading, understanding, and complying with the policies in this handbook.\n\n"
        "5. I should direct any questions about these policies to my manager or the Human Resources "
        "department.\n\n\n"
        "Employee Name (Print): _________________________________\n\n"
        "Employee Signature: _____________________________________\n\n"
        "Date: ________________________________________________\n\n"
        "Employee ID: ___________________________________________\n\n"
        "Department: ____________________________________________\n\n"
        "Manager Name: __________________________________________"
    ))
    add_page_number(p, 24)

    # Page 25
    p = doc.new_page(width=W, height=H)
    add_header(p, "Appendix D: Revision History")
    add_body_text(p, (
        "This page documents all revisions made to the Employee Policy Handbook since its initial "
        "publication.\n\n"
        "Version    Date            Author              Description of Changes\n"
        "-------    ----------      ----------------    ----------------------------------\n"
        "1.0        2018-03-01      Emily Watson        Initial publication\n"
        "1.1        2018-09-15      Emily Watson        Updated PTO accrual rates\n"
        "1.2        2019-02-01      Mark Thompson       Added remote work policy section\n"
        "1.3        2019-07-20      Emily Watson        Updated health insurance plans\n"
        "2.0        2020-01-01      Lisa Chen           Major revision: COVID-19 policies,\n"
        "                                               expanded remote work guidelines\n"
        "2.1        2020-06-01      Lisa Chen           Added mental health resources\n"
        "2.2        2021-01-01      Lisa Chen           Updated 401(k) match percentages\n"
        "2.3        2021-08-15      Sarah Martinez      Revised safety guidelines for\n"
        "                                               hybrid workplace\n"
        "3.0        2022-01-01      Lisa Chen           Comprehensive review and update\n"
        "3.1        2022-06-01      David Kim           Added ESPP section\n"
        "3.2        2023-01-01      Lisa Chen           Updated salary bands and benefits\n"
        "3.3        2023-07-01      Lisa Chen           Revised parental leave policy\n"
        "4.0        2024-01-01      Lisa Chen           Major revision: new wellness\n"
        "                                               program, updated technology policy\n"
        "4.1        2024-07-15      Lisa Chen           Added sabbatical leave policy\n"
        "5.0        2025-01-01      Lisa Chen           Current version: comprehensive\n"
        "                                               update across all sections"
    ))
    add_page_number(p, 25)

    # Ensure NO bookmarks/TOC
    doc.set_toc([])

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
