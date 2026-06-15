"""
Initial Setup: Create two versions of a financial policy document for comparison
Task ID: pdf_fin_013
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_013'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT_V1 = f'{FINANCE_DIR}/policy_v1.pdf'
OUTPUT_V2 = f'{FINANCE_DIR}/policy_v2.pdf'

# Page layout constants
PAGE_W, PAGE_H = 612, 792  # Letter size
MARGIN_L, MARGIN_R = 72, 72
MARGIN_T, MARGIN_B = 72, 72
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

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


# ---------------------------------------------------------------------------
# Define the 8 text changes between v1 and v2
# Each change: (page_index_0based, description, v1_text, v2_text)
# ---------------------------------------------------------------------------
CHANGES = [
    # Change 1: Page 2 - updated approval threshold
    (1, "Expense approval threshold",
     "All expense claims exceeding $5,000 require prior written approval from the department head and must be submitted within 30 calendar days of the expenditure.",
     "All expense claims exceeding $10,000 require prior written approval from the department head and the CFO, and must be submitted within 15 business days of the expenditure."),
    # Change 2: Page 4 - travel policy update
    (3, "Travel reimbursement rate",
     "Domestic travel reimbursement shall be processed at a flat per-diem rate of $275 per day, inclusive of meals and incidental expenses.",
     "Domestic travel reimbursement shall be processed at a tiered per-diem rate of $325 per day for Tier 1 cities and $250 per day for all other locations, inclusive of meals and incidental expenses."),
    # Change 3: Page 5 - vendor payment terms
    (4, "Vendor payment terms",
     "Vendor invoices shall be settled within a net-60 payment cycle unless otherwise negotiated in the master service agreement.",
     "Vendor invoices shall be settled within a net-45 payment cycle. Exceptions require documented approval from the Procurement Director."),
    # Change 4: Page 7 - audit frequency
    (6, "Internal audit frequency",
     "Internal financial audits shall be conducted on a biannual basis, with the audit committee reviewing findings within 45 days of completion.",
     "Internal financial audits shall be conducted on a quarterly basis, with the audit committee reviewing findings within 30 days of completion."),
    # Change 5: Page 9 - capital expenditure limit
    (8, "Capital expenditure authorization",
     "Capital expenditure proposals below $50,000 may be authorized by the divisional vice president without board approval.",
     "Capital expenditure proposals below $25,000 may be authorized by the divisional vice president. Amounts between $25,000 and $100,000 require CFO co-authorization."),
    # Change 6: Page 11 - data retention period
    (10, "Financial records retention",
     "All financial records, including transaction logs and supporting documentation, must be retained for a minimum period of five years from the fiscal year-end.",
     "All financial records, including transaction logs and supporting documentation, must be retained for a minimum period of seven years from the fiscal year-end, in accordance with updated regulatory requirements."),
    # Change 7: Page 13 - whistleblower clause
    (12, "Whistleblower protection",
     "Employees who report suspected financial misconduct in good faith shall be protected from retaliation under the company's existing grievance policy.",
     "Employees who report suspected financial misconduct in good faith shall be protected from retaliation under the enhanced Whistleblower Protection Program, which includes anonymous reporting channels and independent investigation oversight."),
    # Change 8: Page 14 - penalty clause
    (13, "Non-compliance penalties",
     "Violations of this financial policy may result in disciplinary action, up to and including termination of employment.",
     "Violations of this financial policy may result in disciplinary action, including suspension without pay, termination of employment, and referral to external regulatory authorities where applicable."),
]


# Section titles for each page (15 pages for v1, 16 for v2)
SECTION_TITLES = [
    "1. Introduction and Purpose",
    "2. Expense Management and Approval",
    "3. Procurement and Purchasing Guidelines",
    "4. Travel and Entertainment Policy",
    "5. Vendor and Supplier Payments",
    "6. Revenue Recognition Standards",
    "7. Internal Audit and Compliance",
    "8. Budget Planning and Forecasting",
    "9. Capital Expenditure Authorization",
    "10. Tax Compliance and Reporting",
    "11. Records Retention and Data Governance",
    "12. Risk Management Framework",
    "13. Ethics and Whistleblower Provisions",
    "14. Enforcement and Penalties",
    "15. Appendix: Approval Matrix and Forms",
]

EXTRA_SECTION_V2 = "16. Environmental, Social, and Governance (ESG) Reporting Requirements"

# Base paragraph content for pages that don't have changes
BASE_PARAGRAPHS = {
    0: [
        "This Financial Policy Manual establishes the comprehensive framework governing all financial operations, transactions, and reporting activities within Meridian Global Holdings, Inc. and its subsidiaries.",
        "The policies outlined herein are effective as of January 1, 2025, and supersede all previously issued financial policy documents. All employees, contractors, and authorized agents are bound by these provisions.",
        "The Finance Department, under the direction of the Chief Financial Officer, is responsible for the interpretation, implementation, and periodic review of these policies. Questions regarding applicability should be directed to the Corporate Finance Office.",
        "This manual has been reviewed and approved by the Board of Directors and the Audit Committee. Amendments require formal board resolution and will be communicated to all stakeholders within 30 days of adoption.",
    ],
    2: [
        "All procurement activities must adhere to the competitive bidding process established by the Procurement Office. Purchases exceeding $15,000 require a minimum of three qualified vendor quotations.",
        "Sole-source procurement is permitted only when documented justification demonstrates that no reasonable alternative exists. Such requests must be approved by the Chief Procurement Officer.",
        "Purchase orders must be issued prior to the delivery of goods or services. Retroactive purchase orders are prohibited except in documented emergency situations as defined in Appendix B.",
        "The Procurement Office maintains a qualified vendor registry. All new vendors must complete the onboarding process, including financial due diligence and compliance verification, before any purchase orders are issued.",
    ],
    5: [
        "Revenue shall be recognized in accordance with ASC 606 and applicable international financial reporting standards. The five-step model must be consistently applied across all business segments.",
        "Contract modifications that create new performance obligations must be evaluated for standalone selling prices and allocated accordingly. The Revenue Accounting team maintains detailed guidance for complex arrangements.",
        "Variable consideration, including volume discounts, rebates, and performance bonuses, must be estimated using the expected value or most likely amount method, depending on the nature of the arrangement.",
        "Quarterly revenue recognition reviews are conducted by the Financial Reporting team in coordination with the external auditors to ensure ongoing compliance with evolving accounting standards.",
    ],
    7: [
        "Annual budgets must be submitted by each department no later than October 15 for the upcoming fiscal year. The budget cycle includes three review rounds with Finance Business Partners.",
        "Mid-year budget revisions are permitted under the rolling forecast framework. Material variances exceeding 10% of the approved budget must be documented and approved by the Finance Committee.",
        "Capital budgets are developed separately from operating budgets and follow the Capital Expenditure Authorization process outlined in Section 9 of this manual.",
        "Budget performance is reported monthly to department heads and quarterly to the executive leadership team. Variance analysis must include root cause identification and corrective action plans.",
    ],
    9: [
        "The Corporate Tax Department is responsible for ensuring compliance with all federal, state, local, and international tax obligations. Tax positions must be documented in accordance with ASC 740.",
        "Transfer pricing policies are maintained for all intercompany transactions and are reviewed annually to ensure arm's-length compliance. Documentation must meet the requirements of OECD guidelines.",
        "Sales and use tax exemption certificates must be maintained for all applicable transactions. The Tax Department conducts semi-annual reviews of exemption certificate validity.",
        "Tax planning strategies must be reviewed and approved by the Chief Tax Officer and external tax counsel. Aggressive tax positions require formal evaluation of technical merits and risk assessment.",
    ],
    11: [
        "The Enterprise Risk Management framework integrates financial, operational, and strategic risk assessment into a unified governance structure overseen by the Risk Committee.",
        "Each business unit is responsible for maintaining a risk register that identifies, categorizes, and prioritizes risks using the standardized probability-impact matrix defined in Appendix D.",
        "Financial risk exposures, including foreign currency, interest rate, and credit risks, are managed through approved hedging strategies and counterparty risk limits established by the Treasury Department.",
        "Quarterly risk assessments are presented to the Audit Committee. Material risk events must be reported to the Chief Risk Officer within 24 hours of identification.",
    ],
    14: [
        "This appendix provides standardized forms and approval matrices referenced throughout this Financial Policy Manual.",
        "Form FP-001: Expense Reimbursement Request (available on the Finance intranet portal)",
        "Form FP-002: Capital Expenditure Proposal (requires three levels of authorization for amounts exceeding $100,000)",
        "Form FP-003: Vendor Onboarding Checklist (includes due diligence requirements and compliance certification)",
        "Form FP-004: Budget Variance Exception Request (must be accompanied by corrective action plan)",
        "The approval matrix below summarizes authorization levels by transaction type and dollar threshold. Refer to individual policy sections for detailed requirements.",
    ],
}


def get_page_paragraphs(page_idx, version='v1'):
    """Get paragraphs for a given page. Substitutes changed text for v2."""
    # Check if this page has a change
    for change_page, _desc, v1_text, v2_text in CHANGES:
        if change_page == page_idx:
            # Build paragraphs with the changed text embedded
            if version == 'v1':
                changed_para = v1_text
            else:
                changed_para = v2_text
            # Return base content + the specific changed paragraph
            if page_idx in BASE_PARAGRAPHS:
                paras = list(BASE_PARAGRAPHS[page_idx])
                paras.insert(1, changed_para)
                return paras
            else:
                return [
                    f"This section addresses key aspects of {SECTION_TITLES[page_idx].split('. ', 1)[1].lower()} as they relate to the overall financial governance framework of Meridian Global Holdings.",
                    changed_para,
                    "The provisions outlined above are subject to periodic review by the Finance Committee and may be amended through the standard policy update process described in Section 1.",
                    "Compliance with these requirements is mandatory for all organizational units. Exceptions must be formally requested and documented in accordance with the established waiver process.",
                ]
    # No change on this page - use base paragraphs or generate generic content
    if page_idx in BASE_PARAGRAPHS:
        return BASE_PARAGRAPHS[page_idx]
    else:
        title_text = SECTION_TITLES[page_idx].split('. ', 1)[1] if page_idx < len(SECTION_TITLES) else "Additional Provisions"
        return [
            f"This section establishes the policies and procedures governing {title_text.lower()} within Meridian Global Holdings, Inc.",
            f"The {title_text.lower()} framework has been designed to align with industry best practices and applicable regulatory requirements. All organizational units must comply with the standards set forth herein.",
            "Implementation of these provisions is overseen by the designated policy owners in coordination with the Finance Department. Regular training and communication ensures consistent application across the enterprise.",
            "Any deviations from the established procedures must be documented, justified, and approved through the formal exception request process. The Compliance Office maintains records of all granted exceptions.",
        ]


def build_policy_pdf(output_path, version='v1'):
    """Build a multi-page financial policy PDF."""
    doc = pymupdf.open()

    num_pages = 15 if version == 'v1' else 16
    titles = list(SECTION_TITLES)
    if version == 'v2':
        titles.append(EXTRA_SECTION_V2)

    for page_idx in range(num_pages):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        y = MARGIN_T

        # Document header on page 1
        if page_idx == 0:
            page.insert_text(
                pymupdf.Point(MARGIN_L, y),
                "MERIDIAN GLOBAL HOLDINGS, INC.",
                fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.4)
            )
            y += 28
            page.insert_text(
                pymupdf.Point(MARGIN_L, y),
                "Financial Policy Manual",
                fontsize=14, fontname="hebo", color=(0.1, 0.15, 0.4)
            )
            y += 22
            ver_label = "Version 1.0 - January 2025" if version == 'v1' else "Version 2.0 - March 2025"
            page.insert_text(
                pymupdf.Point(MARGIN_L, y),
                ver_label,
                fontsize=10, fontname="heit", color=(0.4, 0.4, 0.4)
            )
            y += 20
            # Separator line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(PAGE_W - MARGIN_R, y))
            shape.finish(color=(0.2, 0.2, 0.6), width=1.5)
            shape.commit()
            y += 20

        # Section title
        title = titles[page_idx]
        page.insert_text(
            pymupdf.Point(MARGIN_L, y),
            title,
            fontsize=14, fontname="hebo", color=(0.15, 0.2, 0.45)
        )
        y += 24

        # Separator under title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(PAGE_W - MARGIN_R, y))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        y += 16

        # Page content
        if page_idx == num_pages - 1 and version == 'v2' and page_idx == 15:
            # Extra ESG section for v2
            paragraphs = [
                "In alignment with evolving regulatory expectations and stakeholder demands, Meridian Global Holdings is committed to transparent Environmental, Social, and Governance (ESG) reporting.",
                "Beginning in fiscal year 2026, all business units must report ESG metrics on a quarterly basis using the standardized framework developed by the Sustainability Office.",
                "Financial disclosures related to climate risk, workforce diversity, and governance practices shall be integrated into the annual report and filed in accordance with SEC climate disclosure rules.",
                "The ESG Steering Committee, chaired by the Chief Sustainability Officer, is responsible for establishing reporting standards, reviewing submissions, and ensuring data integrity across all reporting entities.",
            ]
        else:
            paragraphs = get_page_paragraphs(page_idx, version)

        for para in paragraphs:
            rect = pymupdf.Rect(MARGIN_L, y, PAGE_W - MARGIN_R, PAGE_H - MARGIN_B - 30)
            excess = page.insert_textbox(
                rect, para,
                fontsize=10.5, fontname="helv", color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
            # Estimate used height (approximate: ~14 pts per line, ~80 chars per line)
            lines_needed = max(1, len(para) // 75 + 1)
            y += lines_needed * 14 + 10

            if y > PAGE_H - MARGIN_B - 50:
                break

        # Footer
        page.insert_text(
            pymupdf.Point(MARGIN_L, PAGE_H - 36),
            "Meridian Global Holdings - Confidential",
            fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5)
        )
        page.insert_text(
            pymupdf.Point(PAGE_W - MARGIN_R - 60, PAGE_H - 36),
            f"Page {page_idx + 1} of {num_pages}",
            fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5)
        )

    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path} ({num_pages} pages)")


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    # Build both policy versions
    build_policy_pdf(OUTPUT_V1, version='v1')
    build_policy_pdf(OUTPUT_V2, version='v2')

    # Do NOT create comparison report - that's the agent's task

    # Open v1 in Evince for the agent
    launch_gui(f'evince "{OUTPUT_V1}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with policy_v1.pdf on DISPLAY=:0')


create_initial()
