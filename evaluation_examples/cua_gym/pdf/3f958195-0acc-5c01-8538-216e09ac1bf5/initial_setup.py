"""
Initial Setup: Create a 40-page employee handbook PDF with no bookmarks
Task ID: pdf_ro_015
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_015'
OUTPUT = f'{WORKDIR}/Documents/handbook.pdf'

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
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    MARGIN = 72  # 1 inch

    # Chapter structure: (title, start_page_0indexed, content_sections)
    chapters = [
        ("Introduction", 0, [
            "Welcome to Meridian Technologies",
            "This employee handbook serves as a comprehensive guide to our company's policies, "
            "procedures, and workplace expectations. At Meridian Technologies, we believe that a "
            "well-informed team is the foundation of our success.",
            "Our mission is to deliver innovative software solutions that transform how businesses "
            "operate in the digital age. Founded in 2008 by Dr. Elena Vasquez and James Thornton, "
            "Meridian has grown from a small startup in Austin, Texas to a global enterprise with "
            "offices in twelve countries.",
            "This handbook covers everything you need to know about working at Meridian, from our "
            "core values and code of conduct to benefits enrollment and career development pathways.",
        ]),
        ("Chapter 1: Policies", 4, [
            "Employment Policies and Guidelines",
            "1.1 Equal Employment Opportunity\n"
            "Meridian Technologies is committed to providing equal employment opportunities to all "
            "employees and applicants. We do not discriminate based on race, color, religion, sex, "
            "national origin, age, disability, or any other protected status.",
            "1.2 Code of Conduct\n"
            "All employees are expected to maintain the highest standards of professional behavior. "
            "This includes treating colleagues with respect, maintaining confidentiality of company "
            "information, and avoiding conflicts of interest.",
            "1.3 Attendance and Punctuality\n"
            "Regular attendance is essential to the smooth operation of our business. Employees are "
            "expected to report to work on time and to notify their supervisor as early as possible "
            "if they will be absent or late.",
            "1.4 Remote Work Policy\n"
            "Meridian offers flexible remote work arrangements for eligible positions. Employees may "
            "work remotely up to three days per week with manager approval. Remote workers must "
            "maintain a dedicated workspace and be available during core business hours (10:00 AM - 3:00 PM).",
            "1.5 Dress Code\n"
            "Our dress code is business casual for in-office days. Client-facing meetings may require "
            "business professional attire. Engineering teams enjoy a relaxed dress code on Fridays.",
        ]),
        ("Chapter 2: Procedures", 14, [
            "Operational Procedures",
            "2.1 Onboarding Process\n"
            "New employees will complete a structured onboarding program during their first two weeks. "
            "This includes orientation sessions, IT setup, security training, and introductions to key "
            "team members and stakeholders.",
            "2.2 Performance Review Cycle\n"
            "Performance reviews are conducted semi-annually in June and December. Employees complete "
            "a self-assessment, and managers provide written evaluations using our competency framework. "
            "Goals for the next review period are set collaboratively.",
            "2.3 Expense Reimbursement\n"
            "Business expenses must be submitted through the ExpenseTrack portal within 30 days of "
            "the expense date. Receipts are required for all expenses over $25. Manager approval is "
            "needed for expenses exceeding $500. Reimbursements are processed within two pay cycles.",
            "2.4 Travel Authorization\n"
            "All business travel requires pre-approval from your department head. Travel requests must "
            "be submitted at least two weeks in advance through the TravelDesk system. Preferred vendors "
            "should be used for flights and hotels when available.",
            "2.5 Incident Reporting\n"
            "Workplace incidents, safety concerns, and near-misses must be reported immediately to your "
            "supervisor and the Safety Office. Use the online incident reporting form within 24 hours "
            "of the event. All reports are kept confidential.",
            "2.6 IT Support Requests\n"
            "For technical issues, submit a ticket through the ServiceNow portal or call the IT Help Desk "
            "at extension 4500. Priority levels range from P1 (critical system outage) to P4 (general "
            "inquiries). Response times vary by priority level.",
        ]),
        ("Chapter 3: Resources", 24, [
            "Employee Resources and Benefits",
            "3.1 Health and Wellness Benefits\n"
            "Meridian offers comprehensive health insurance plans through BlueCross BlueShield. Options "
            "include HMO, PPO, and High-Deductible Health Plans with HSA contributions. Dental and vision "
            "coverage is included in all plans. Open enrollment occurs annually in November.",
            "3.2 Retirement Plans\n"
            "Employees are eligible for our 401(k) plan after 90 days of employment. Meridian matches "
            "100% of contributions up to 4% of salary and 50% of the next 2%. Vesting follows a "
            "three-year graduated schedule.",
            "3.3 Professional Development\n"
            "Each employee receives an annual learning budget of $3,000 for conferences, courses, and "
            "certifications. Tuition reimbursement of up to $5,250 per year is available for degree "
            "programs related to your role.",
            "3.4 Employee Assistance Program\n"
            "Our EAP provides free, confidential counseling services for personal and work-related "
            "concerns. Services include mental health support, financial planning, legal consultation, "
            "and work-life balance resources. Contact the EAP at 1-800-555-0199.",
            "3.5 Paid Time Off\n"
            "Full-time employees accrue PTO based on years of service:\n"
            "  - Years 0-2: 15 days per year\n"
            "  - Years 3-5: 20 days per year\n"
            "  - Years 6-10: 25 days per year\n"
            "  - Years 10+: 30 days per year\n"
            "Additionally, Meridian observes 11 paid holidays per year.",
            "3.6 Parental Leave\n"
            "Primary caregivers receive 16 weeks of fully paid parental leave. Secondary caregivers "
            "receive 6 weeks of fully paid leave. Adoption and surrogacy are covered under the same policy.",
        ]),
        ("Appendix", 34, [
            "Appendix: Forms, Templates, and Quick Reference",
            "A.1 Key Contacts Directory\n"
            "Human Resources: hr@meridiantech.com | Ext. 2100\n"
            "IT Help Desk: helpdesk@meridiantech.com | Ext. 4500\n"
            "Facilities: facilities@meridiantech.com | Ext. 3200\n"
            "Safety Office: safety@meridiantech.com | Ext. 3800\n"
            "Legal Department: legal@meridiantech.com | Ext. 5100",
            "A.2 Acronyms and Definitions\n"
            "EAP - Employee Assistance Program\n"
            "HSA - Health Savings Account\n"
            "PTO - Paid Time Off\n"
            "SLA - Service Level Agreement\n"
            "HRIS - Human Resources Information System\n"
            "KPI - Key Performance Indicator",
            "A.3 Office Locations\n"
            "Headquarters: 4200 Innovation Drive, Austin, TX 78759\n"
            "East Coast Office: 350 Park Avenue, Suite 1200, New York, NY 10022\n"
            "West Coast Office: 2800 Sand Hill Road, Menlo Park, CA 94025\n"
            "European Office: Friedrichstrasse 68, 10117 Berlin, Germany\n"
            "Asia Pacific Office: 1 Raffles Place, #38-01, Singapore 048616",
            "A.4 Revision History\n"
            "Version 1.0 - January 2020: Initial publication\n"
            "Version 1.1 - March 2021: Updated remote work policy\n"
            "Version 2.0 - January 2023: Major revision, added DEI section\n"
            "Version 2.1 - September 2024: Updated benefits information\n"
            "Version 2.2 - January 2025: Current edition",
        ]),
    ]

    # Generate all 40 pages
    for page_idx in range(40):
        page = doc.new_page(width=W, height=H)

        # Determine which chapter this page belongs to
        current_chapter = None
        for i, (title, start, _) in enumerate(chapters):
            if page_idx >= start:
                current_chapter = i

        chapter_title, chapter_start, sections = chapters[current_chapter]
        page_in_chapter = page_idx - chapter_start

        # Header line
        page.insert_text(
            pymupdf.Point(MARGIN, 40),
            "Meridian Technologies - Employee Handbook",
            fontsize=8,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )
        # Header rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN, 48), pymupdf.Point(W - MARGIN, 48))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

        # Footer with page number
        page.insert_text(
            pymupdf.Point(W / 2 - 10, H - 36),
            str(page_idx + 1),
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        y = 80  # starting y position for content

        if page_in_chapter == 0:
            # Chapter title page
            page.insert_text(
                pymupdf.Point(MARGIN, y + 30),
                chapter_title,
                fontsize=24,
                fontname="hebo",
                color=(0.0, 0.2, 0.4),
            )
            y += 70

            # Decorative line under title
            shape2 = page.new_shape()
            shape2.draw_line(pymupdf.Point(MARGIN, y), pymupdf.Point(W / 2, y))
            shape2.finish(color=(0.0, 0.3, 0.6), width=2)
            shape2.commit()
            y += 30

            # First section content on title page
            if len(sections) > 0:
                for si, section in enumerate(sections[:2]):
                    if si == 0:
                        # Subtitle
                        page.insert_text(
                            pymupdf.Point(MARGIN, y),
                            section,
                            fontsize=14,
                            fontname="hebo",
                            color=(0.1, 0.1, 0.1),
                        )
                        y += 30
                    else:
                        rect = pymupdf.Rect(MARGIN, y, W - MARGIN, H - 60)
                        excess = page.insert_textbox(
                            rect, section,
                            fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY,
                        )
                        y += 80
        else:
            # Content pages - fill with section text or continuation text
            section_idx = min(page_in_chapter, len(sections) - 1)

            # Section heading if applicable
            if page_in_chapter < len(sections):
                section_text = sections[section_idx]
                if '\n' in section_text:
                    heading, body = section_text.split('\n', 1)
                    page.insert_text(
                        pymupdf.Point(MARGIN, y),
                        heading,
                        fontsize=13,
                        fontname="hebo",
                        color=(0.0, 0.2, 0.4),
                    )
                    y += 25
                    rect = pymupdf.Rect(MARGIN, y, W - MARGIN, H - 80)
                    page.insert_textbox(
                        rect, body,
                        fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1),
                        align=pymupdf.TEXT_ALIGN_LEFT,
                    )
                else:
                    page.insert_text(
                        pymupdf.Point(MARGIN, y),
                        section_text,
                        fontsize=13,
                        fontname="hebo",
                        color=(0.0, 0.2, 0.4),
                    )
                    y += 25

            # Fill remaining space with continuation content
            filler_paragraphs = [
                "Meridian Technologies continues to invest in employee growth and development. "
                "Our leadership team regularly reviews policies to ensure they remain competitive "
                "and aligned with industry best practices.",
                "Employees are encouraged to provide feedback on company policies through the "
                "annual employee survey and the suggestion portal on the intranet. All feedback "
                "is reviewed by the HR Policy Committee quarterly.",
                "For questions about any policy or procedure described in this handbook, please "
                "contact your HR Business Partner or the HR Service Center during business hours.",
                "Meridian's commitment to workplace excellence extends to all aspects of the "
                "employee experience, from initial onboarding through retirement planning.",
                "Our diversity and inclusion initiatives have been recognized by several "
                "industry organizations, reflecting our dedication to creating a welcoming "
                "workplace for all employees regardless of background.",
            ]

            for fi, para in enumerate(filler_paragraphs):
                if y > H - 120:
                    break
                rect = pymupdf.Rect(MARGIN, y, W - MARGIN, y + 80)
                page.insert_textbox(
                    rect, para,
                    fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                y += 85

    # Verify: NO bookmarks in initial file
    assert doc.get_toc() == [], "Initial file should have no bookmarks"

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 40')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
