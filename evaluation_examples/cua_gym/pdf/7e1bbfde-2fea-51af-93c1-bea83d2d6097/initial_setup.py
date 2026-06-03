"""
Initial Setup: Create unencrypted 32-page employee handbook PDF
Task ID: pdf_mbc_004
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_004'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/employee_handbook.pdf'

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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Document structure: 32 pages of a realistic employee handbook
    # We'll create chapters with content spanning multiple pages

    A4_W, A4_H = 595, 842
    MARGIN = 72
    TEXT_W = A4_W - 2 * MARGIN
    BODY_TOP = MARGIN + 40
    BODY_BOTTOM = A4_H - MARGIN

    chapters = [
        {
            "title": "Welcome to Meridian Technologies",
            "sections": [
                ("About This Handbook", [
                    "This Employee Handbook has been prepared to inform you of Meridian Technologies' history, philosophy, employment practices, and policies, as well as the benefits provided to you as a valued employee.",
                    "No employee handbook can anticipate every circumstance or question. After reading the handbook, if you have questions, please talk with your manager or Human Resources. The policies described here are subject to change at the sole discretion of Meridian Technologies.",
                    "This handbook supersedes all previously issued editions. We ask that you keep it as a handy reference during your employment with us.",
                ]),
                ("Company History", [
                    "Meridian Technologies was founded in 2008 by Dr. Elena Vasquez and James Richardson in San Francisco, California. What started as a small consulting firm has grown into a global technology company with over 4,500 employees across 12 offices worldwide.",
                    "Our core mission remains unchanged: to develop innovative software solutions that empower businesses to operate more efficiently and sustainably. Today, our products serve over 15,000 enterprise customers in 45 countries.",
                    "Key milestones include our 2014 Series B funding of $85 million, our 2018 IPO on NASDAQ, and our 2022 acquisition of CloudBridge Analytics, which expanded our data platform capabilities significantly.",
                ]),
                ("Our Values", [
                    "Innovation First: We encourage creative thinking and are not afraid to challenge the status quo. Every team member is empowered to propose new ideas and approaches.",
                    "Integrity Always: We conduct our business with the highest ethical standards. Transparency, honesty, and accountability guide every decision we make.",
                    "Customer Obsession: Our customers' success is our success. We listen, adapt, and deliver solutions that genuinely solve their problems.",
                    "Collaborative Spirit: We believe the best outcomes arise from diverse teams working together. Inclusion and respect are non-negotiable.",
                    "Continuous Growth: We invest heavily in learning and development because our people are our greatest asset.",
                ]),
            ]
        },
        {
            "title": "Employment Policies",
            "sections": [
                ("Equal Employment Opportunity", [
                    "Meridian Technologies is an equal opportunity employer and does not discriminate against any employee or applicant for employment because of race, color, sex, age, national origin, religion, sexual orientation, gender identity, veteran status, disability, or any other federal, state, or local protected class.",
                    "This policy applies to all terms and conditions of employment, including recruiting, hiring, placement, promotion, termination, layoff, recall, transfer, leaves of absence, compensation, and training.",
                    "If you believe you have been subjected to any form of unlawful discrimination, submit a written complaint to the Director of Human Resources, Sarah Mitchell, at hr@meridiantech.com. All complaints will be investigated promptly and thoroughly.",
                ]),
                ("Employment Classification", [
                    "Each position at Meridian Technologies is designated as either exempt or non-exempt in accordance with the Fair Labor Standards Act (FLSA). Non-exempt employees are entitled to overtime pay under the specific provisions of federal and state laws.",
                    "Full-Time employees are those regularly scheduled to work 40 or more hours per week. Part-Time employees are those regularly scheduled to work fewer than 30 hours per week.",
                    "Temporary employees are hired for a pre-established period or for a specific project. Temporary employees may be full-time or part-time. They are not eligible for Meridian Technologies benefits unless required by law.",
                    "Independent contractors are not employees of Meridian Technologies and are not eligible for any benefits. The relationship is governed by the terms of the applicable contract.",
                ]),
                ("Probationary Period", [
                    "All new employees are subject to a 90-day probationary period. During this time, your supervisor will closely monitor your performance and provide feedback.",
                    "Successful completion of the probationary period does not guarantee continued employment for any specified period. Both Meridian Technologies and the employee retain the right to terminate the employment relationship at any time, with or without cause.",
                ]),
                ("Background Checks", [
                    "All offers of employment are contingent upon satisfactory results of a background check. Background checks may include verification of Social Security number, prior employment and education, review of criminal conviction records, and where applicable, credit history.",
                    "Any discrepancies or falsifications discovered during the background check process may result in the withdrawal of the offer or termination of employment.",
                ]),
            ]
        },
        {
            "title": "Compensation and Benefits",
            "sections": [
                ("Pay Schedule", [
                    "All employees are paid on a semi-monthly basis, on the 15th and the last business day of each month. If a pay date falls on a weekend or holiday, employees will be paid on the preceding business day.",
                    "Your pay stub is available electronically through the Meridian HR Portal at hr.meridiantech.com. Direct deposit is strongly encouraged and can be set up during your first week.",
                    "Overtime work by non-exempt employees must be approved in advance by their manager. Overtime pay is calculated at 1.5 times the regular hourly rate for hours worked beyond 40 in a workweek.",
                ]),
                ("Health Insurance", [
                    "Meridian Technologies offers comprehensive health insurance to all full-time employees, effective on the first day of the month following 30 days of employment. The company covers 85% of the premium for individual coverage and 70% for family coverage.",
                    "Plan options include: Meridian PPO Plan with a $500 individual deductible ($1,500 family), Meridian HMO Plan with $25 copays and no deductible, and the Meridian HSA-Compatible High Deductible Plan with a $2,800 individual deductible ($5,600 family).",
                    "Dental and vision coverage are also available. The dental plan covers preventive care at 100%, basic procedures at 80%, and major procedures at 50%. Vision coverage includes an annual exam and a $200 frame allowance.",
                ]),
                ("Retirement Plan", [
                    "The Meridian Technologies 401(k) Retirement Plan allows eligible employees to contribute pre-tax dollars up to the maximum allowed by law. The company matches 100% of employee contributions up to 4% of base salary, and 50% of contributions between 4% and 6%.",
                    "Employees are immediately vested in their own contributions. Company matching contributions vest over a 3-year schedule: 33% after year 1, 67% after year 2, and 100% after year 3.",
                    "A Roth 401(k) option is also available for employees who prefer after-tax contributions with tax-free withdrawals in retirement.",
                ]),
                ("Paid Time Off", [
                    "Full-time employees accrue Paid Time Off (PTO) based on years of service: 0-2 years: 15 days per year, 3-5 years: 20 days per year, 6-10 years: 25 days per year, and 10+ years: 30 days per year.",
                    "PTO may be used for vacation, personal days, or sick time. Unused PTO up to 10 days may be carried over to the following year. PTO in excess of the carryover limit will be forfeited on January 1st.",
                    "Meridian Technologies also observes 11 paid holidays per year: New Year's Day, Martin Luther King Jr. Day, Presidents' Day, Memorial Day, Independence Day, Labor Day, Columbus Day, Veterans Day, Thanksgiving Day, the day after Thanksgiving, and Christmas Day.",
                ]),
                ("Additional Benefits", [
                    "Life Insurance: The company provides basic life insurance at 2x annual salary at no cost to the employee. Supplemental life insurance is available for purchase.",
                    "Employee Assistance Program (EAP): Free, confidential counseling services for employees and their family members, covering mental health, financial planning, and legal guidance.",
                    "Tuition Reimbursement: Up to $8,000 per year for approved courses related to your current position or career development at Meridian Technologies.",
                    "Commuter Benefits: Pre-tax deductions for public transit passes and qualified parking expenses, up to IRS limits.",
                    "Wellness Program: $500 annual wellness stipend for gym memberships, fitness equipment, or wellness activities. Free flu shots and annual health screenings.",
                ]),
            ]
        },
        {
            "title": "Workplace Conduct",
            "sections": [
                ("Code of Conduct", [
                    "All employees are expected to conduct themselves in a professional manner at all times. This includes treating colleagues, customers, and business partners with respect and courtesy.",
                    "Employees must avoid conflicts of interest, or the appearance thereof, and should disclose any potential conflicts to their manager or the Ethics Committee.",
                    "The use of Meridian Technologies resources for personal gain or unauthorized purposes is strictly prohibited. This includes company equipment, software, proprietary information, and intellectual property.",
                ]),
                ("Anti-Harassment Policy", [
                    "Meridian Technologies is committed to maintaining a workplace free from harassment. Harassment based on any legally protected characteristic is strictly prohibited and will not be tolerated.",
                    "Harassment includes, but is not limited to: unwelcome verbal conduct such as epithets, derogatory comments, or slurs; visual conduct such as derogatory posters, cartoons, or drawings; physical conduct such as assault or unwelcome touching; and requests for sexual favors.",
                    "Any employee who experiences or witnesses harassment should report it immediately to their manager, Human Resources, or through the anonymous Ethics Hotline at 1-800-555-0199. All reports will be investigated promptly and confidentially.",
                    "Retaliation against any employee who reports harassment or participates in an investigation is strictly prohibited and will result in disciplinary action, up to and including termination.",
                ]),
                ("Attendance and Punctuality", [
                    "Regular attendance and punctuality are essential for the smooth operation of Meridian Technologies. Employees are expected to report to work as scheduled and on time.",
                    "If you are unable to report to work or will be late, you must notify your supervisor as early as possible, and no later than 30 minutes before your scheduled start time.",
                    "Excessive absenteeism or tardiness may result in disciplinary action. Three consecutive days of unexcused absence will be considered job abandonment and may result in termination.",
                ]),
                ("Dress Code", [
                    "Meridian Technologies maintains a business casual dress code. Employees are expected to present a clean, professional appearance appropriate for a business environment.",
                    "Engineering and non-client-facing teams may observe a more relaxed dress code, including jeans and company-branded attire. Client-facing roles should maintain business professional attire when meeting with external stakeholders.",
                    "On Fridays and during company events, casual dress is permitted. However, clothing with offensive graphics or language is never acceptable.",
                ]),
            ]
        },
        {
            "title": "Technology and Information Security",
            "sections": [
                ("Acceptable Use of Technology", [
                    "All Meridian Technologies computer systems, networks, and electronic communications are company property and should be used primarily for business purposes. Limited personal use is permitted provided it does not interfere with job performance.",
                    "Employees should have no expectation of privacy when using company systems. Meridian Technologies reserves the right to monitor, access, and disclose electronic communications and files at any time.",
                    "The installation of unauthorized software on company devices is prohibited. All software must be approved by the IT Department and properly licensed.",
                ]),
                ("Data Protection and Privacy", [
                    "All employees are responsible for protecting the confidentiality of company, customer, and employee data. This includes both digital and physical records.",
                    "Sensitive data must be encrypted when transmitted electronically and stored on secure, company-approved systems. USB drives and personal cloud storage should not be used for company data without explicit IT approval.",
                    "Employees must complete annual data protection training. Failure to comply with data protection policies may result in disciplinary action and potential legal liability.",
                ]),
                ("Password Policy", [
                    "Passwords must be at least 12 characters long and include a mix of uppercase letters, lowercase letters, numbers, and special characters. Passwords must be changed every 90 days.",
                    "Never share your password with anyone, including IT staff. IT will never ask for your password. If you suspect your password has been compromised, change it immediately and notify the IT Security team.",
                    "Multi-factor authentication (MFA) is required for all remote access, cloud services, and administrative accounts.",
                ]),
                ("Incident Reporting", [
                    "Any suspected security incident, data breach, or loss of company equipment must be reported immediately to the IT Security team at security@meridiantech.com or by calling the Security Operations Center at extension 5555.",
                    "Do not attempt to investigate or resolve security incidents on your own. Timely reporting enables the security team to contain threats and minimize damage.",
                    "All employees are required to complete annual cybersecurity awareness training, including phishing simulation exercises.",
                ]),
            ]
        },
        {
            "title": "Leave Policies",
            "sections": [
                ("Family and Medical Leave", [
                    "Eligible employees may take up to 12 weeks of unpaid, job-protected leave per year under the Family and Medical Leave Act (FMLA) for the birth or adoption of a child, to care for a spouse, child, or parent with a serious health condition, or for the employee's own serious health condition.",
                    "Meridian Technologies provides an additional benefit of 6 weeks of paid parental leave for the birth or adoption of a child. This paid leave runs concurrently with FMLA leave.",
                    "To request FMLA leave, contact Human Resources at least 30 days in advance when the leave is foreseeable. For unforeseeable events, notify HR as soon as practicable.",
                ]),
                ("Bereavement Leave", [
                    "Full-time employees are eligible for up to 5 days of paid bereavement leave for the death of an immediate family member (spouse, parent, child, sibling, grandparent, or grandchild).",
                    "Up to 3 days of paid bereavement leave may be taken for the death of an extended family member (aunt, uncle, cousin, in-law). Additional unpaid time may be approved by your manager.",
                ]),
                ("Jury Duty", [
                    "Meridian Technologies encourages employees to fulfill their civic duty. Employees summoned for jury duty will receive their full base pay for up to 10 business days per year.",
                    "If your jury service exceeds 10 days, additional time will be unpaid. However, your position will be protected throughout the duration of your service.",
                    "Employees must provide a copy of the jury summons to their manager and Human Resources as soon as it is received.",
                ]),
                ("Military Leave", [
                    "Employees who are members of the uniformed services are entitled to leave in accordance with the Uniformed Services Employment and Reemployment Rights Act (USERRA).",
                    "Meridian Technologies will pay the difference between military pay and base salary for up to 24 months. Benefits will continue during military leave of up to 12 months.",
                ]),
            ]
        },
        {
            "title": "Performance Management",
            "sections": [
                ("Performance Reviews", [
                    "Formal performance reviews are conducted twice per year: mid-year (June) and year-end (December). Reviews are based on goal achievement, competency demonstration, and alignment with company values.",
                    "Employees are expected to participate actively in the review process by completing a self-assessment, identifying development goals, and providing candid feedback on their experience.",
                    "Performance is rated on a 5-point scale: Exceptional (5), Exceeds Expectations (4), Meets Expectations (3), Needs Improvement (2), and Unsatisfactory (1). Ratings of 2 or below will trigger a Performance Improvement Plan.",
                ]),
                ("Performance Improvement Plans", [
                    "A Performance Improvement Plan (PIP) is a structured program designed to help an employee meet performance expectations. PIPs typically last 30-90 days and include specific, measurable goals.",
                    "During the PIP period, the employee will meet weekly with their manager to review progress. Successful completion of the PIP returns the employee to regular status. Failure to meet PIP goals may result in further disciplinary action, including termination.",
                ]),
                ("Promotions and Transfers", [
                    "Meridian Technologies encourages internal mobility and career advancement. Open positions are posted on the internal job board for at least 5 business days before external candidates are considered.",
                    "To be eligible for promotion or transfer, employees must have been in their current role for at least 12 months and have a performance rating of Meets Expectations or above.",
                    "The hiring manager, in consultation with HR, makes final decisions on internal transfers and promotions based on qualifications, performance history, and business needs.",
                ]),
            ]
        },
        {
            "title": "Safety and Emergency Procedures",
            "sections": [
                ("Workplace Safety", [
                    "Meridian Technologies is committed to providing a safe and healthy work environment. All employees must comply with all safety rules, procedures, and applicable OSHA regulations.",
                    "Report all workplace injuries, illnesses, or unsafe conditions to your manager and the Facilities team immediately, regardless of severity. Early reporting enables prompt treatment and helps prevent future incidents.",
                    "Safety Data Sheets (SDS) for any hazardous materials used on-site are available in the Facilities office and on the company intranet.",
                ]),
                ("Emergency Evacuation", [
                    "Emergency evacuation maps are posted at every exit and elevator lobby. Familiarize yourself with the primary and alternate evacuation routes from your work area.",
                    "When the fire alarm sounds, immediately proceed to the nearest exit. Use stairs, not elevators. Proceed to the designated assembly point in the parking lot and report to your floor warden.",
                    "Floor wardens are responsible for ensuring all personnel have evacuated their designated area. Employees with mobility limitations should proceed to the Area of Rescue Assistance and await emergency personnel.",
                ]),
                ("Active Threat Response", [
                    "In the event of an active threat situation, follow the Run-Hide-Fight protocol. If you can safely evacuate, do so immediately. If evacuation is not possible, find a secure location, lock and barricade the door, silence your phone, and remain quiet.",
                    "Call 911 when it is safe to do so. Provide your location, number of people in your area, and any information about the threat. Do not open the door until directed by law enforcement.",
                    "Annual active threat training is mandatory for all employees. Training sessions are scheduled quarterly and can be registered through the HR Portal.",
                ]),
            ]
        },
    ]

    # Page counter
    page_num = 0

    # --- Title Page ---
    page = doc.new_page(width=A4_W, height=A4_H)
    page_num += 1

    # Title page design
    shape = page.new_shape()
    # Blue header bar
    shape.draw_rect(pymupdf.Rect(0, 200, A4_W, 210))
    shape.finish(color=(0.13, 0.27, 0.53), fill=(0.13, 0.27, 0.53))
    shape.draw_rect(pymupdf.Rect(0, 480, A4_W, 490))
    shape.finish(color=(0.13, 0.27, 0.53), fill=(0.13, 0.27, 0.53))
    shape.commit()

    page.insert_text(pymupdf.Point(A4_W/2 - 180, 300), "EMPLOYEE HANDBOOK",
                     fontsize=32, fontname="hebo", color=(0.13, 0.27, 0.53))
    page.insert_text(pymupdf.Point(A4_W/2 - 120, 350), "Meridian Technologies",
                     fontsize=18, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(A4_W/2 - 60, 400), "Revised March 2024",
                     fontsize=12, fontname="helv", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(A4_W/2 - 80, 430), "Human Resources Department",
                     fontsize=11, fontname="helv", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(A4_W/2 - 50, 550), "CONFIDENTIAL",
                     fontsize=14, fontname="hebo", color=(0.7, 0.1, 0.1))
    page.insert_text(pymupdf.Point(72, 750), "Meridian Technologies, Inc.",
                     fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, 765), "1200 Innovation Drive, Suite 800, San Francisco, CA 94105",
                     fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Table of Contents Page ---
    page = doc.new_page(width=A4_W, height=A4_H)
    page_num += 1

    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 30), "TABLE OF CONTENTS",
                     fontsize=20, fontname="hebo", color=(0.13, 0.27, 0.53))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN, MARGIN + 40), pymupdf.Point(A4_W - MARGIN, MARGIN + 40))
    shape.finish(color=(0.13, 0.27, 0.53), width=1.5)
    shape.commit()

    toc_y = MARGIN + 70
    for i, chapter in enumerate(chapters):
        page.insert_text(pymupdf.Point(MARGIN, toc_y),
                         f"Chapter {i+1}: {chapter['title']}",
                         fontsize=12, fontname="hebo", color=(0.13, 0.27, 0.53))
        toc_y += 22
        for sec_title, _ in chapter['sections']:
            page.insert_text(pymupdf.Point(MARGIN + 20, toc_y),
                             sec_title, fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
            toc_y += 16
        toc_y += 6

    # --- Content Pages ---
    for ch_idx, chapter in enumerate(chapters):
        for sec_idx, (sec_title, paragraphs) in enumerate(chapter['sections']):
            # Determine if we need a new chapter heading page
            if sec_idx == 0:
                page = doc.new_page(width=A4_W, height=A4_H)
                page_num += 1
                # Chapter heading
                page.insert_text(pymupdf.Point(MARGIN, MARGIN + 30),
                                 f"Chapter {ch_idx + 1}",
                                 fontsize=14, fontname="helv", color=(0.5, 0.5, 0.5))
                page.insert_text(pymupdf.Point(MARGIN, MARGIN + 55),
                                 chapter['title'],
                                 fontsize=22, fontname="hebo", color=(0.13, 0.27, 0.53))
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(MARGIN, MARGIN + 65),
                                pymupdf.Point(A4_W - MARGIN, MARGIN + 65))
                shape.finish(color=(0.13, 0.27, 0.53), width=1)
                shape.commit()
                y_pos = MARGIN + 95
            else:
                page = doc.new_page(width=A4_W, height=A4_H)
                page_num += 1
                y_pos = MARGIN + 30

            # Section heading
            page.insert_text(pymupdf.Point(MARGIN, y_pos),
                             sec_title,
                             fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))
            y_pos += 25

            # Paragraphs
            for para in paragraphs:
                rect = pymupdf.Rect(MARGIN, y_pos, A4_W - MARGIN, BODY_BOTTOM - 40)
                excess = page.insert_textbox(rect, para,
                                             fontsize=10.5, fontname="helv",
                                             color=(0.15, 0.15, 0.15),
                                             align=pymupdf.TEXT_ALIGN_JUSTIFY)
                # Estimate lines used (rough: ~60 chars per line at 10.5pt in our width)
                chars_per_line = 80
                num_lines = max(1, len(para) // chars_per_line + 1)
                y_pos += num_lines * 14 + 10

                if y_pos > BODY_BOTTOM - 60:
                    # Add page number footer
                    page.insert_text(pymupdf.Point(A4_W/2 - 10, A4_H - 40),
                                     str(page_num), fontsize=9, fontname="helv",
                                     color=(0.5, 0.5, 0.5))
                    break

            # Add page number
            page.insert_text(pymupdf.Point(A4_W/2 - 10, A4_H - 40),
                             str(page_num), fontsize=9, fontname="helv",
                             color=(0.5, 0.5, 0.5))

    # Pad to exactly 32 pages with additional content if needed
    appendix_topics = [
        ("Appendix A: Organizational Chart",
         "The organizational chart below outlines the reporting structure at Meridian Technologies. The Executive Leadership Team consists of the CEO, CFO, CTO, COO, CHRO, and CLO. Each executive oversees multiple departments that are further divided into teams and workgroups."),
        ("Appendix B: Benefits Summary Table",
         "This appendix provides a comprehensive summary of all benefits available to Meridian Technologies employees, including eligibility requirements, coverage details, and enrollment deadlines."),
        ("Appendix C: Office Locations",
         "Meridian Technologies operates from the following locations: San Francisco HQ (1200 Innovation Drive), New York Office (350 5th Avenue, Suite 4500), London Office (25 Old Broad Street, EC2N 1HN), Singapore Office (1 Raffles Place, #44-01), and Sydney Office (200 George Street, Level 37)."),
        ("Appendix D: Glossary of Terms",
         "This glossary defines key terms used throughout the handbook, including COBRA, FMLA, FLSA, ADA, EEOC, OSHA, HIPAA, and other commonly referenced acronyms and their meanings in the context of employment law and company policy."),
        ("Appendix E: Acknowledgment Form",
         "By signing below, I acknowledge that I have received a copy of the Meridian Technologies Employee Handbook and understand that it is my responsibility to read and comply with the policies and procedures contained herein."),
        ("Appendix F: Contact Directory",
         "Human Resources: hr@meridiantech.com (ext. 2000), IT Help Desk: helpdesk@meridiantech.com (ext. 3000), Facilities: facilities@meridiantech.com (ext. 4000), Security Operations: security@meridiantech.com (ext. 5555), Ethics Hotline: 1-800-555-0199."),
        ("Appendix G: Remote Work Policy",
         "Effective January 2024, Meridian Technologies supports a hybrid work model. Employees may work remotely up to 3 days per week with manager approval. All remote work arrangements must be documented in the HR system and comply with the data security requirements outlined in Chapter 5."),
        ("Appendix H: Travel and Expense Policy",
         "All business travel must be pre-approved by a manager with budget authority. Airfare should be booked at least 14 days in advance when possible. Hotel accommodations are reimbursed up to $250 per night in domestic locations and actual cost for international travel. Meals are reimbursed up to $75 per day domestic and $100 per day international."),
        ("Appendix I: Intellectual Property Agreement",
         "All inventions, discoveries, software, designs, and creative works developed during employment or using company resources are the property of Meridian Technologies. Employees must disclose and assign all such intellectual property promptly. Pre-existing IP must be disclosed at the time of hire."),
        ("Appendix J: Social Media Guidelines",
         "Employees are welcome to use social media but must not disclose confidential company information, speak on behalf of Meridian Technologies without authorization, or post content that could damage the company's reputation. When in doubt, consult the Communications Department."),
    ]

    while page_num < 32:
        page = doc.new_page(width=A4_W, height=A4_H)
        page_num += 1

        idx = page_num - 23  # appendix index
        if 0 <= idx < len(appendix_topics):
            title, content = appendix_topics[idx]
        else:
            title = f"Notes"
            content = "This page is intentionally left for employee notes and personal reference."

        page.insert_text(pymupdf.Point(MARGIN, MARGIN + 30), title,
                         fontsize=16, fontname="hebo", color=(0.13, 0.27, 0.53))

        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN, MARGIN + 40),
                        pymupdf.Point(A4_W - MARGIN, MARGIN + 40))
        shape.finish(color=(0.8, 0.8, 0.8), width=0.5)
        shape.commit()

        rect = pymupdf.Rect(MARGIN, MARGIN + 55, A4_W - MARGIN, BODY_BOTTOM - 40)
        page.insert_textbox(rect, content,
                            fontsize=10.5, fontname="helv",
                            color=(0.15, 0.15, 0.15),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)

        page.insert_text(pymupdf.Point(A4_W/2 - 10, A4_H - 40),
                         str(page_num), fontsize=9, fontname="helv",
                         color=(0.5, 0.5, 0.5))

    # Set metadata
    doc.set_metadata({
        "title": "Employee Handbook - Meridian Technologies",
        "author": "Meridian Technologies HR Department",
        "subject": "Employee Policies and Procedures",
        "keywords": "employee, handbook, policies, Meridian Technologies",
        "creator": "Meridian Technologies",
        "producer": "Meridian Technologies HR",
    })

    # Build table of contents bookmarks
    toc_entries = []
    pg = 3  # content starts on page 3 (after title & TOC)
    for ch_idx, chapter in enumerate(chapters):
        toc_entries.append([1, f"Chapter {ch_idx+1}: {chapter['title']}", pg])
        for sec_idx, (sec_title, _) in enumerate(chapter['sections']):
            toc_entries.append([2, sec_title, pg + sec_idx])
        pg += len(chapter['sections'])
    doc.set_toc(toc_entries)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_num}')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
