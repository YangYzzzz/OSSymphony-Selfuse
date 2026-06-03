"""
Initial Setup: Create a 4-page attorney-client privileged memo (unencrypted)
Task ID: pdf_legal_007
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_007'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/attorney_client_memo.pdf'

# Page dimensions (Letter size)
W, H = 612, 792
MARGIN_LEFT = 72
MARGIN_RIGHT = 540
MARGIN_TOP = 72
MARGIN_BOTTOM = 72


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


def add_header_footer(page, page_num, total_pages):
    """Add consistent header and footer to each page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, 50), pymupdf.Point(MARGIN_RIGHT, 50))
    shape.finish(color=(0.2, 0.2, 0.4), width=1.5)
    shape.commit()

    # Header text
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, 45),
        "MITCHELL, VASQUEZ & THORNTON LLP",
        fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.4)
    )
    page.insert_text(
        pymupdf.Point(400, 45),
        "PRIVILEGED & CONFIDENTIAL",
        fontsize=8, fontname="hebo", color=(0.7, 0.0, 0.0)
    )

    # Footer line
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(MARGIN_LEFT, H - 50), pymupdf.Point(MARGIN_RIGHT, H - 50))
    shape2.finish(color=(0.2, 0.2, 0.4), width=0.75)
    shape2.commit()

    # Footer text
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, H - 38),
        "ATTORNEY-CLIENT PRIVILEGED COMMUNICATION",
        fontsize=7, fontname="heit", color=(0.5, 0.5, 0.5)
    )
    page.insert_text(
        pymupdf.Point(MARGIN_RIGHT - 40, H - 38),
        f"Page {page_num} of {total_pages}",
        fontsize=7, fontname="helv", color=(0.5, 0.5, 0.5)
    )


def create_page1(doc):
    """Cover / Title page with memo header."""
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP + 20

    # Firm name
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "MITCHELL, VASQUEZ & THORNTON LLP",
                     fontsize=18, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 22
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Attorneys at Law",
                     fontsize=11, fontname="heit", color=(0.4, 0.4, 0.4))
    y += 14
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "1200 Market Street, Suite 3400 | Philadelphia, PA 19107",
                     fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    y += 12
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Tel: (215) 555-0142 | Fax: (215) 555-0143",
                     fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    # Divider
    y += 20
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, y), pymupdf.Point(MARGIN_RIGHT, y))
    shape.finish(color=(0.15, 0.15, 0.35), width=2)
    shape.commit()

    # Privileged banner
    y += 25
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "PRIVILEGED AND CONFIDENTIAL",
                     fontsize=13, fontname="hebo", color=(0.7, 0.0, 0.0))
    y += 16
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "ATTORNEY-CLIENT COMMUNICATION",
                     fontsize=13, fontname="hebo", color=(0.7, 0.0, 0.0))

    # Memo header block
    y += 35
    labels = ["MEMORANDUM", "", "TO:", "FROM:", "DATE:", "RE:", "FILE NO.:"]
    values = [
        "", "",
        "Rachel Whitfield, General Counsel\n     Meridian Healthcare Systems, Inc.",
        "David A. Mitchell, Esq.\n     Partner, Litigation Practice Group",
        "March 18, 2025",
        "Potential HIPAA Violation - Unauthorized Disclosure of Patient Records\n"
        "     at Meridian Regional Medical Center (Incident Ref: MHS-2025-0041)",
        "MHS-LIT-2025-0041"
    ]

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "MEMORANDUM",
                     fontsize=14, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 30

    field_pairs = [
        ("TO:", "Rachel Whitfield, General Counsel"),
        ("", "Meridian Healthcare Systems, Inc."),
        ("FROM:", "David A. Mitchell, Esq."),
        ("", "Partner, Litigation Practice Group"),
        ("DATE:", "March 18, 2025"),
        ("RE:", "Potential HIPAA Violation - Unauthorized Disclosure"),
        ("", "of Patient Records at Meridian Regional Medical Center"),
        ("", "(Incident Ref: MHS-2025-0041)"),
        ("FILE NO.:", "MHS-LIT-2025-0041"),
    ]

    for label, value in field_pairs:
        if label:
            page.insert_text(pymupdf.Point(MARGIN_LEFT, y), label,
                             fontsize=10, fontname="hebo", color=(0.0, 0.0, 0.0))
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 75, y), value,
                         fontsize=10, fontname="helv", color=(0.0, 0.0, 0.0))
        y += 15

    # Divider
    y += 10
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(MARGIN_LEFT, y), pymupdf.Point(MARGIN_RIGHT, y))
    shape2.finish(color=(0.0, 0.0, 0.0), width=1)
    shape2.commit()

    # Executive summary
    y += 20
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "I. EXECUTIVE SUMMARY",
                     fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 20

    summary = (
        "This memorandum analyzes the legal implications arising from the unauthorized "
        "disclosure of protected health information (PHI) involving approximately 2,340 "
        "patient records at Meridian Regional Medical Center. The incident, discovered on "
        "February 27, 2025, appears to have resulted from a misconfigured access control "
        "list on the facility's electronic health record (EHR) system, which permitted "
        "unauthorized personnel in the billing department to access clinical notes and "
        "diagnostic records outside the scope of their designated role-based permissions."
    )

    rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 120)
    page.insert_textbox(rect, summary, fontsize=10, fontname="helv",
                        color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 130

    summary2 = (
        "Based on our preliminary assessment, this incident triggers mandatory reporting "
        "obligations under 45 C.F.R. \u00a7 164.408 (notification to the Secretary of HHS) "
        "and 45 C.F.R. \u00a7 164.404 (individual notification). We recommend immediate "
        "engagement of a forensic IT consultant, completion of the required risk assessment "
        "under the Breach Notification Rule, and preparation of notification letters to "
        "affected individuals within the 60-day statutory window."
    )
    rect2 = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 100)
    page.insert_textbox(rect2, summary2, fontsize=10, fontname="helv",
                        color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    add_header_footer(page, 1, 4)
    return page


def create_page2(doc):
    """Factual background and timeline."""
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP + 10

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "II. FACTUAL BACKGROUND",
                     fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 22

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "A. Incident Discovery and Initial Response",
                     fontsize=11, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 18

    para1 = (
        "On February 27, 2025, Meridian's Information Security Officer, James Kowalski, "
        "identified anomalous access patterns during a routine audit of the Epic EHR system "
        "logs. Specifically, the audit revealed that fourteen (14) employees assigned to the "
        "billing and revenue cycle department had accessed clinical documentation modules "
        "including physician progress notes, radiology reports, and laboratory results "
        "for patients with whom they had no billing-related interaction."
    )
    rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 90)
    page.insert_textbox(rect, para1, fontsize=10, fontname="helv",
                        color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 100

    para2 = (
        "The investigation determined that on January 15, 2025, during a scheduled system "
        "update (Patch Version 2025.1.3), the access control list governing the billing "
        "department's role permissions was inadvertently modified. The change expanded the "
        "department's access rights from 'Billing Summary' and 'Insurance Verification' "
        "modules to include 'Clinical Notes,' 'Lab Results,' and 'Diagnostic Imaging Reports.' "
        "This misconfiguration persisted for approximately 43 days before detection."
    )
    rect2 = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 90)
    page.insert_textbox(rect2, para2, fontsize=10, fontname="helv",
                        color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 105

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "B. Scope of Exposure",
                     fontsize=11, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 18

    para3 = (
        "Our analysis of the access logs indicates the following exposure metrics:"
    )
    page.insert_textbox(pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 15), para3,
                        fontsize=10, fontname="helv", color=(0.0, 0.0, 0.0))
    y += 22

    bullets = [
        "Total unique patient records accessed: 2,340",
        "Total unauthorized access events logged: 8,712",
        "Employees with unauthorized access: 14 (billing department staff)",
        "Duration of exposure window: January 15 - February 27, 2025 (43 days)",
        "Types of PHI exposed: clinical notes, lab results, diagnostic imaging reports,",
        "  medication histories, and ICD-10/CPT diagnostic codes",
        "No evidence of external data exfiltration or download to removable media",
    ]
    for bullet in bullets:
        prefix = "    " if bullet.startswith("  ") else "  \u2022  "
        text = bullet.lstrip()
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 10, y), f"{prefix}{text}",
                         fontsize=9.5, fontname="helv", color=(0.0, 0.0, 0.0))
        y += 14

    y += 15
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "C. Timeline of Key Events",
                     fontsize=11, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 18

    timeline = [
        ("Jan 15, 2025", "System update Patch 2025.1.3 deployed; ACL misconfiguration introduced"),
        ("Jan 16-Feb 26", "Billing staff access clinical modules without authorization"),
        ("Feb 27, 2025", "ISO Kowalski detects anomalous access patterns in quarterly audit"),
        ("Feb 28, 2025", "Emergency remediation: ACL permissions reverted to baseline"),
        ("Mar 1, 2025", "Internal incident response team convened; outside counsel engaged"),
        ("Mar 5, 2025", "Forensic analysis of access logs initiated by CyberForge Analytics"),
        ("Mar 12, 2025", "Preliminary forensic report delivered; 2,340 affected records confirmed"),
    ]
    for date, event in timeline:
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 10, y), date,
                         fontsize=9, fontname="hebo", color=(0.0, 0.0, 0.0))
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 110, y), event,
                         fontsize=9, fontname="helv", color=(0.0, 0.0, 0.0))
        y += 14

    add_header_footer(page, 2, 4)
    return page


def create_page3(doc):
    """Legal analysis."""
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP + 10

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "III. LEGAL ANALYSIS",
                     fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 22

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "A. HIPAA Breach Determination Under the Breach Notification Rule",
                     fontsize=11, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 18

    para1 = (
        "Under the HIPAA Breach Notification Rule (45 C.F.R. \u00a7\u00a7 164.400-414), a "
        "'breach' is defined as the acquisition, access, use, or disclosure of PHI in a "
        "manner not permitted under the Privacy Rule that compromises the security or "
        "privacy of the PHI. The Rule establishes a presumption that any impermissible "
        "use or disclosure constitutes a breach unless the covered entity demonstrates "
        "through a four-factor risk assessment that there is a low probability the PHI "
        "has been compromised."
    )
    rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 90)
    page.insert_textbox(rect, para1, fontsize=10, fontname="helv",
                        color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 100

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Four-Factor Risk Assessment:",
                     fontsize=10, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 18

    factors = [
        ("1. Nature and extent of PHI involved:",
         "The exposed data includes clinical notes, lab results, diagnostic codes, and "
         "medication histories. This constitutes highly sensitive PHI including mental health "
         "records, substance abuse treatment notes, and HIV testing results for certain patients. "
         "Risk Level: HIGH."),
        ("2. Identity of unauthorized persons:",
         "The fourteen billing employees are workforce members subject to confidentiality "
         "agreements and HIPAA training. While not external actors, their access exceeded "
         "authorized scope. Risk Level: MODERATE."),
        ("3. Whether PHI was actually acquired or viewed:",
         "Access logs confirm that clinical notes were opened and viewed on 8,712 occasions. "
         "Seven employees accessed records of patients known to them personally (co-workers "
         "and family members). Risk Level: HIGH."),
        ("4. Extent of mitigation:",
         "ACL was corrected within 24 hours of discovery. All fourteen employees have been "
         "interviewed and signed supplemental confidentiality acknowledgments. No evidence "
         "of data exfiltration. However, 43-day exposure window limits mitigation effectiveness. "
         "Risk Level: MODERATE-HIGH."),
    ]

    for title, body in factors:
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 10, y), title,
                         fontsize=9.5, fontname="hebo", color=(0.0, 0.0, 0.0))
        y += 14
        rect_f = pymupdf.Rect(MARGIN_LEFT + 20, y, MARGIN_RIGHT, y + 55)
        page.insert_textbox(rect_f, body, fontsize=9, fontname="helv",
                            color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 62

    y += 5
    conclusion = (
        "Based on the totality of these factors, it is our legal opinion that the presumption "
        "of breach has NOT been rebutted. Accordingly, this incident constitutes a reportable "
        "breach under the Breach Notification Rule, triggering notification obligations to "
        "affected individuals, HHS, and potentially the media (given the >500 individual threshold)."
    )
    rect_c = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 65)
    page.insert_textbox(rect_c, conclusion, fontsize=10, fontname="hebo",
                        color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    add_header_footer(page, 3, 4)
    return page


def create_page4(doc):
    """Recommendations and signature."""
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP + 10

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "IV. RECOMMENDATIONS",
                     fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 22

    para_intro = (
        "In light of the foregoing analysis, we recommend that Meridian Healthcare Systems "
        "take the following immediate and near-term actions:"
    )
    rect_i = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 30)
    page.insert_textbox(rect_i, para_intro, fontsize=10, fontname="helv",
                        color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 38

    recommendations = [
        ("1. Breach Notification to HHS (Deadline: April 28, 2025)",
         "File the breach report with the HHS Office for Civil Rights via the online breach "
         "reporting portal within 60 days of discovery (by April 28, 2025). The report must "
         "include the nature of the breach, types of PHI involved, and remediation steps taken."),
        ("2. Individual Notification (Deadline: April 28, 2025)",
         "Prepare and mail notification letters to all 2,340 affected individuals via first-class "
         "mail. Letters must describe the breach, types of information involved, steps individuals "
         "should take, and contact information for Meridian's designated privacy officer."),
        ("3. Media Notification",
         "Because the breach affects more than 500 individuals in a single state, notification to "
         "prominent media outlets serving the relevant jurisdiction is required under "
         "45 C.F.R. \u00a7 164.406."),
        ("4. Workforce Sanctions",
         "Review the access patterns of the fourteen identified employees and determine appropriate "
         "sanctions under Meridian's existing HIPAA Sanctions Policy (HR-POL-2023-017). "
         "Disciplinary actions should be proportionate and consistently applied."),
        ("5. Technical Remediation",
         "Engage CyberForge Analytics to conduct a comprehensive review of all role-based access "
         "controls across the Epic EHR platform. Implement automated monitoring alerts for "
         "permission changes exceeding predefined thresholds."),
        ("6. Credit Monitoring Services",
         "Offer complimentary credit monitoring and identity theft protection services to all "
         "affected individuals for a minimum of 24 months, consistent with industry best practices "
         "and OCR enforcement expectations."),
    ]

    for title, body in recommendations:
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 10, y), title,
                         fontsize=10, fontname="hebo", color=(0.0, 0.0, 0.0))
        y += 16
        rect_r = pymupdf.Rect(MARGIN_LEFT + 20, y, MARGIN_RIGHT, y + 48)
        page.insert_textbox(rect_r, body, fontsize=9.5, fontname="helv",
                            color=(0.0, 0.0, 0.0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 55

    # Signature block
    y += 15
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, y), pymupdf.Point(MARGIN_RIGHT, y))
    shape.finish(color=(0.0, 0.0, 0.0), width=0.5)
    shape.commit()
    y += 18

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Respectfully submitted,",
                     fontsize=10, fontname="heit", color=(0.0, 0.0, 0.0))
    y += 30
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "David A. Mitchell, Esq.",
                     fontsize=10, fontname="hebo", color=(0.0, 0.0, 0.0))
    y += 14
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Partner, Litigation Practice Group",
                     fontsize=9, fontname="helv", color=(0.0, 0.0, 0.0))
    y += 12
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Mitchell, Vasquez & Thornton LLP",
                     fontsize=9, fontname="helv", color=(0.0, 0.0, 0.0))
    y += 12
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Direct: (215) 555-0187 | david.mitchell@mvtlaw.com",
                     fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    y += 25
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "cc:  Thomas Reeves, Chief Compliance Officer",
                     fontsize=9, fontname="helv", color=(0.0, 0.0, 0.0))
    y += 12
    page.insert_text(pymupdf.Point(MARGIN_LEFT + 25, y),
                     "Sandra Liu, VP of Information Technology",
                     fontsize=9, fontname="helv", color=(0.0, 0.0, 0.0))
    y += 12
    page.insert_text(pymupdf.Point(MARGIN_LEFT + 25, y),
                     "James Kowalski, Information Security Officer",
                     fontsize=9, fontname="helv", color=(0.0, 0.0, 0.0))

    add_header_footer(page, 4, 4)
    return page


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    create_page1(doc)
    create_page2(doc)
    create_page3(doc)
    create_page4(doc)

    # Set metadata
    doc.set_metadata({
        "title": "Attorney-Client Privileged Memorandum - MHS-LIT-2025-0041",
        "author": "David A. Mitchell, Esq.",
        "subject": "HIPAA Breach Analysis - Meridian Healthcare Systems",
        "keywords": "privileged, confidential, attorney-client, HIPAA, breach",
        "creator": "Mitchell, Vasquez & Thornton LLP",
        "producer": "Legal Document System",
    })

    # Set TOC / bookmarks
    toc = [
        [1, "I. Executive Summary", 1],
        [1, "II. Factual Background", 2],
        [2, "A. Incident Discovery and Initial Response", 2],
        [2, "B. Scope of Exposure", 2],
        [2, "C. Timeline of Key Events", 2],
        [1, "III. Legal Analysis", 3],
        [1, "IV. Recommendations", 4],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
