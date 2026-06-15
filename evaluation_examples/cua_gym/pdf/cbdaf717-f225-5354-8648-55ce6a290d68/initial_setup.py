"""
Initial Setup: Create a 30-page trust document with bookmarks but no custom open action.
Task ID: pdf_legal_082
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_082'
DOC_DIR = f'{WORKDIR}/legal/estate'
OUTPUT = f'{DOC_DIR}/trust_document.pdf'


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
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Trust document content ---
    # Page dimensions: US Letter
    W, H = 612, 792
    LEFT_MARGIN = 72
    RIGHT_MARGIN = 540
    TOP_START = 72

    # Document structure
    sections = [
        ("ARTICLE I: ESTABLISHMENT OF TRUST", [
            "Section 1.1 Creation of Trust",
            "This Revocable Living Trust Agreement (the \"Trust\") is entered into on "
            "March 15, 2024, by and between MARGARET ELIZABETH THORNTON (hereinafter "
            "referred to as \"Grantor\" or \"Trustee\"), residing at 4782 Ridgewood Drive, "
            "Greenwich, Connecticut 06830.",
            "",
            "The Grantor hereby transfers and delivers to the Trustee the property described "
            "in Schedule A attached hereto, to be held, administered, and distributed in "
            "accordance with the terms and conditions set forth in this Trust Agreement.",
            "",
            "Section 1.2 Name of Trust",
            "This Trust shall be known as the \"Margaret Elizabeth Thornton Revocable Living "
            "Trust dated March 15, 2024\" (the \"Trust\").",
            "",
            "Section 1.3 Revocability",
            "During the lifetime of the Grantor, this Trust shall be revocable in whole or "
            "in part by the Grantor. The Grantor reserves the right to amend, modify, or "
            "revoke this Trust at any time during the Grantor's lifetime by a written "
            "instrument delivered to the Trustee.",
        ]),
        ("ARTICLE II: TRUST PROPERTY", [
            "Section 2.1 Initial Trust Property",
            "The Grantor hereby transfers to the Trustee the property listed in Schedule A, "
            "which is attached hereto and incorporated by reference. The Trustee agrees to "
            "hold, manage, invest, and distribute the Trust Property in accordance with the "
            "terms of this Agreement.",
            "",
            "Section 2.2 Additional Contributions",
            "The Grantor may at any time transfer additional property to the Trust by deed, "
            "assignment, or other appropriate method of transfer. Any additional property so "
            "transferred shall become part of the Trust Property and shall be subject to "
            "all the terms and conditions of this Agreement.",
            "",
            "Section 2.3 Acceptance by Trustee",
            "The Trustee hereby accepts the Trust Property and agrees to hold the same in "
            "trust, subject to the terms and conditions herein set forth.",
        ]),
        ("ARTICLE III: ADMINISTRATION DURING GRANTOR'S LIFETIME", [
            "Section 3.1 Distributions to Grantor",
            "During the lifetime of the Grantor, the Trustee shall pay to or apply for the "
            "benefit of the Grantor such amounts of income and principal as the Grantor may "
            "from time to time request in writing. The Trustee shall also distribute to the "
            "Grantor all net income of the Trust at least quarterly.",
            "",
            "Section 3.2 Incapacity of Grantor",
            "If the Grantor becomes incapacitated, as determined by two licensed physicians, "
            "the Trustee shall use the Trust income and principal for the Grantor's health, "
            "education, maintenance, and support. The Trustee shall consider the Grantor's "
            "accustomed manner of living and any other resources available to the Grantor.",
            "",
            "Section 3.3 Investment Authority",
            "The Trustee shall have full authority to invest and reinvest the Trust Property "
            "in any form of property or investment, including but not limited to stocks, "
            "bonds, mutual funds, real estate, certificates of deposit, and money market "
            "accounts, as the Trustee deems appropriate.",
        ]),
        ("ARTICLE IV: DISTRIBUTION UPON GRANTOR'S DEATH", [
            "Section 4.1 Payment of Debts and Expenses",
            "Upon the death of the Grantor, the Trustee shall pay from the Trust Property "
            "all legally enforceable debts of the Grantor, funeral expenses, and costs of "
            "administration of the Grantor's estate, to the extent such debts and expenses "
            "are not paid from other sources.",
            "",
            "Section 4.2 Specific Bequests",
            "The Trustee shall distribute the following specific bequests:\n"
            "  (a) To JONATHAN DAVID THORNTON, the Grantor's son: the real property "
            "located at 891 Maple Court, Darien, Connecticut 06820, together with all "
            "furnishings and personal property therein.\n"
            "  (b) To ELIZABETH ANNE THORNTON-RICHARDS, the Grantor's daughter: the sum "
            "of Five Hundred Thousand Dollars ($500,000.00) from the Trust principal.\n"
            "  (c) To WILLIAM CHARLES THORNTON, the Grantor's son: the Grantor's interest "
            "in Thornton Family Holdings, LLC.",
            "",
            "Section 4.3 Residuary Distribution",
            "After payment of all debts, expenses, and specific bequests, the Trustee shall "
            "distribute the remaining Trust Property (the \"Residuary Trust Property\") in "
            "equal shares to the Grantor's surviving children, per stirpes.",
        ]),
        ("ARTICLE V: TRUSTEE PROVISIONS", [
            "Section 5.1 Successor Trustee",
            "If the Grantor ceases to serve as Trustee for any reason, JONATHAN DAVID "
            "THORNTON shall serve as Successor Trustee. If Jonathan David Thornton is "
            "unable or unwilling to serve, FIRST NATIONAL BANK OF CONNECTICUT shall serve "
            "as Successor Trustee.",
            "",
            "Section 5.2 Powers of Trustee",
            "The Trustee shall have all powers granted under the Connecticut Uniform Trust "
            "Code, including but not limited to the power to:\n"
            "  (a) Sell, exchange, or dispose of Trust property;\n"
            "  (b) Borrow money and mortgage or pledge Trust property;\n"
            "  (c) Employ attorneys, accountants, and other advisors;\n"
            "  (d) Make distributions in cash or in kind;\n"
            "  (e) Execute and deliver all instruments necessary to carry out the terms "
            "of this Trust.",
            "",
            "Section 5.3 Compensation of Trustee",
            "Any individual serving as Trustee shall be entitled to reasonable compensation "
            "for services rendered. Any corporate Trustee shall be compensated in accordance "
            "with its published fee schedule in effect at the time of service.",
            "",
            "Section 5.4 Trustee Liability",
            "No Trustee shall be liable for any loss or depreciation in value of the Trust "
            "Property unless such loss or depreciation was caused by the Trustee's willful "
            "misconduct, gross negligence, or breach of fiduciary duty.",
        ]),
        ("ARTICLE VI: TRUST FOR MINOR BENEFICIARIES", [
            "Section 6.1 Trust for Minors",
            "Any property distributable to a beneficiary who has not attained the age of "
            "twenty-five (25) years shall be held in a separate trust for that beneficiary "
            "(a \"Minor's Trust\"). The Trustee shall manage and invest the Minor's Trust "
            "property and distribute income and principal as necessary for the beneficiary's "
            "health, education, maintenance, and support.",
            "",
            "Section 6.2 Distribution of Minor's Trust",
            "The Trustee shall distribute the remaining balance of the Minor's Trust to the "
            "beneficiary upon attaining the age of twenty-five (25) years. If the beneficiary "
            "dies before attaining such age, the remaining balance shall be distributed to "
            "the beneficiary's then-living descendants, per stirpes, or if none, to the "
            "Grantor's remaining beneficiaries.",
            "",
            "Section 6.3 Education Distributions",
            "The Trustee is authorized to make distributions from the Minor's Trust for "
            "tuition, room, board, books, and other reasonable expenses incurred in "
            "connection with the beneficiary's education at any accredited institution.",
        ]),
        ("ARTICLE VII: SPENDTHRIFT PROVISIONS", [
            "Section 7.1 Spendthrift Clause",
            "No interest in the income or principal of any trust created under this Agreement "
            "shall be voluntarily or involuntarily alienated, or subject to the claims of "
            "creditors of any beneficiary, prior to distribution. This provision shall not "
            "limit the exercise of any power of appointment.",
            "",
            "Section 7.2 Protection from Creditors",
            "The interest of any beneficiary in the Trust shall not be subject to attachment, "
            "garnishment, execution, or any other legal process by any creditor of such "
            "beneficiary. The Trustee shall not make any distribution to or for the benefit "
            "of a beneficiary if such distribution would be subject to the claims of the "
            "beneficiary's creditors.",
        ]),
        ("ARTICLE VIII: TAX PROVISIONS", [
            "Section 8.1 Tax Elections",
            "The Trustee is authorized to make any tax elections permitted under applicable "
            "federal, state, or local tax laws, including but not limited to elections "
            "regarding the treatment of administration expenses, the valuation date for "
            "estate tax purposes, and the allocation of generation-skipping transfer tax "
            "exemptions.",
            "",
            "Section 8.2 Generation-Skipping Transfer Tax",
            "The Trustee shall allocate the Grantor's available GST exemption to transfers "
            "under this Trust to the extent necessary to minimize generation-skipping "
            "transfer taxes. The Trustee may create separate trusts for GST-exempt and "
            "non-exempt property if doing so would be advantageous.",
            "",
            "Section 8.3 Income Tax Reporting",
            "During the Grantor's lifetime, the Trust shall be treated as a grantor trust "
            "for federal income tax purposes. All income, deductions, and credits of the "
            "Trust shall be reported on the Grantor's personal income tax return.",
        ]),
        ("ARTICLE IX: GENERAL PROVISIONS", [
            "Section 9.1 Governing Law",
            "This Trust Agreement shall be governed by and construed in accordance with "
            "the laws of the State of Connecticut, without regard to conflicts of law "
            "principles.",
            "",
            "Section 9.2 Severability",
            "If any provision of this Trust Agreement is held to be invalid or unenforceable, "
            "the remaining provisions shall continue in full force and effect.",
            "",
            "Section 9.3 Entire Agreement",
            "This Trust Agreement, together with all schedules and amendments, constitutes "
            "the entire agreement between the parties with respect to the subject matter "
            "hereof and supersedes all prior negotiations, representations, and agreements.",
            "",
            "Section 9.4 Headings",
            "The headings used in this Trust Agreement are for convenience of reference only "
            "and shall not affect the interpretation of any provision.",
            "",
            "Section 9.5 No Contest Clause",
            "If any beneficiary under this Trust directly or indirectly contests or attacks "
            "this Trust or any of its provisions, any share or interest in the Trust given "
            "to that contesting beneficiary shall be revoked and such share shall be "
            "distributed as if the contesting beneficiary had predeceased the Grantor.",
        ]),
        ("ARTICLE X: EXECUTION", [
            "Section 10.1 Signatures",
            "IN WITNESS WHEREOF, the Grantor and Trustee have executed this Revocable "
            "Living Trust Agreement as of the date first written above.",
            "",
            "",
            "______________________________",
            "MARGARET ELIZABETH THORNTON",
            "Grantor and Trustee",
            "",
            "",
            "STATE OF CONNECTICUT",
            "COUNTY OF FAIRFIELD",
            "",
            "On this 15th day of March, 2024, before me, the undersigned notary public, "
            "personally appeared MARGARET ELIZABETH THORNTON, known to me (or proved to "
            "me on the basis of satisfactory evidence) to be the person whose name is "
            "subscribed to the within instrument and acknowledged to me that she executed "
            "the same in her authorized capacity, and that by her signature on the "
            "instrument the person, or the entity upon behalf of which the person acted, "
            "executed the instrument.",
            "",
            "______________________________",
            "Notary Public",
            "My Commission Expires: ___________",
        ]),
        ("SCHEDULE A: TRUST PROPERTY", [
            "The following property is hereby transferred to and shall constitute the "
            "initial Trust Property of the Margaret Elizabeth Thornton Revocable Living "
            "Trust dated March 15, 2024:",
            "",
            "1. REAL PROPERTY:",
            "   (a) Residence at 4782 Ridgewood Drive, Greenwich, CT 06830",
            "       (Fair Market Value: $2,850,000)",
            "   (b) Vacation home at 156 Ocean Bluff Road, Kennebunkport, ME 04046",
            "       (Fair Market Value: $1,200,000)",
            "   (c) Investment property at 2340 Commerce Park, Stamford, CT 06901",
            "       (Fair Market Value: $3,500,000)",
            "",
            "2. FINANCIAL ACCOUNTS:",
            "   (a) First National Bank of Connecticut, Account #XXXX-7891",
            "       (Approximate Balance: $425,000)",
            "   (b) Schwab Brokerage Account #XXXX-4562",
            "       (Approximate Value: $1,850,000)",
            "   (c) Fidelity IRA Account #XXXX-3378 (as designated beneficiary)",
            "       (Approximate Value: $780,000)",
            "   (d) Vanguard Municipal Bond Fund #XXXX-9012",
            "       (Approximate Value: $650,000)",
            "",
            "3. BUSINESS INTERESTS:",
            "   (a) 60% membership interest in Thornton Family Holdings, LLC",
            "       (Estimated Value: $4,200,000)",
            "   (b) 25% limited partnership interest in Greenwich Real Estate Partners, LP",
            "       (Estimated Value: $1,100,000)",
            "",
            "4. PERSONAL PROPERTY:",
            "   (a) Antique furniture collection (appraised value: $175,000)",
            "   (b) Fine art collection (appraised value: $320,000)",
            "   (c) Jewelry (appraised value: $95,000)",
            "   (d) 2023 Mercedes-Benz S-Class (VIN: WDDUG8CB7PA123456)",
            "   (e) 2022 BMW X5 (VIN: 5UXCR6C04N9K78901)",
            "",
            "5. LIFE INSURANCE POLICIES:",
            "   (a) MetLife Policy #LF-2019-445678 (Face Value: $1,000,000)",
            "   (b) Northwestern Mutual Policy #NW-2021-889012 (Face Value: $500,000)",
            "",
            "TOTAL ESTIMATED TRUST PROPERTY VALUE: $18,645,000",
        ]),
        ("SCHEDULE B: BENEFICIARY DESIGNATIONS", [
            "Primary Beneficiaries (upon Grantor's death):",
            "",
            "1. JONATHAN DAVID THORNTON (Son)",
            "   Date of Birth: June 12, 1978",
            "   Address: 891 Maple Court, Darien, CT 06820",
            "   Share: One-third (1/3) of Residuary Trust Property",
            "",
            "2. ELIZABETH ANNE THORNTON-RICHARDS (Daughter)",
            "   Date of Birth: September 3, 1981",
            "   Address: 2567 Park Avenue, Apt 14B, New York, NY 10035",
            "   Share: One-third (1/3) of Residuary Trust Property",
            "",
            "3. WILLIAM CHARLES THORNTON (Son)",
            "   Date of Birth: January 28, 1985",
            "   Address: 445 Beacon Street, Boston, MA 02115",
            "   Share: One-third (1/3) of Residuary Trust Property",
            "",
            "Contingent Beneficiaries:",
            "",
            "If any primary beneficiary predeceases the Grantor, such beneficiary's share "
            "shall pass to such beneficiary's then-living descendants, per stirpes. If a "
            "primary beneficiary has no living descendants, such share shall be distributed "
            "equally among the remaining primary beneficiaries or their descendants.",
            "",
            "Charitable Beneficiary (if all primary and contingent beneficiaries predecease "
            "the Grantor):",
            "   Greenwich Community Foundation",
            "   One Lafayette Court, Greenwich, CT 06830",
            "   Purpose: To establish the Thornton Family Scholarship Fund",
        ]),
    ]

    # Build pages
    page_num = 0
    toc_entries = []

    # Title page (page 0)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 200), "REVOCABLE LIVING TRUST AGREEMENT",
                     fontsize=22, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 240), "OF",
                     fontsize=16, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 270), "MARGARET ELIZABETH THORNTON",
                     fontsize=20, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 320), "Dated: March 15, 2024",
                     fontsize=14, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 370), "Prepared by:",
                     fontsize=12, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 390), "Harrison, Mitchell & Associates, LLP",
                     fontsize=12, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 410), "Attorneys at Law",
                     fontsize=12, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 430), "275 Greenwich Avenue, Suite 400",
                     fontsize=12, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 450), "Greenwich, Connecticut 06830",
                     fontsize=12, fontname="tiro", color=(0, 0, 0))
    page_num += 1

    # Table of Contents page (page 1)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(LEFT_MARGIN, 72), "TABLE OF CONTENTS",
                     fontsize=16, fontname="tibo", color=(0, 0, 0))
    y_pos = 110
    for i, (title, _) in enumerate(sections):
        page.insert_text(pymupdf.Point(LEFT_MARGIN, y_pos),
                         f"{title}", fontsize=10, fontname="tiro", color=(0, 0, 0))
        y_pos += 18
        if y_pos > H - 72:
            break
    page_num += 1

    # Content pages
    for section_idx, (title, paragraphs) in enumerate(sections):
        # Each article starts on a new page
        page = doc.new_page(width=W, height=H)
        page_num += 1
        toc_entries.append([1, title, page_num])

        # Title
        page.insert_text(pymupdf.Point(LEFT_MARGIN, TOP_START),
                         title, fontsize=14, fontname="tibo", color=(0, 0, 0))

        # Draw a separator line under the title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(LEFT_MARGIN, TOP_START + 8),
                        pymupdf.Point(RIGHT_MARGIN, TOP_START + 8))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()

        y_pos = TOP_START + 30
        text_rect = pymupdf.Rect(LEFT_MARGIN, y_pos, RIGHT_MARGIN, H - 72)

        full_text = "\n".join(paragraphs)
        rc = page.insert_textbox(text_rect, full_text, fontsize=11,
                                  fontname="tiro", color=(0, 0, 0),
                                  align=pymupdf.TEXT_ALIGN_JUSTIFY)
        # rc < 0 means all text fit; rc > 0 means overflow (but insert_textbox
        # does not return the excess text itself, so we just note it)

    # Pad to exactly 30 pages if needed
    while doc.page_count < 30:
        page = doc.new_page(width=W, height=H)
        pg = doc.page_count
        page.insert_text(pymupdf.Point(LEFT_MARGIN, TOP_START),
                         f"[This page intentionally left blank]",
                         fontsize=11, fontname="tiit", color=(0.5, 0.5, 0.5))

    # If we have more than 30 pages, trim to 30
    while doc.page_count > 30:
        doc.delete_page(doc.page_count - 1)

    # Add page numbers to all pages (footer)
    for i in range(doc.page_count):
        pg = doc[i]
        pg.insert_text(pymupdf.Point(W / 2 - 10, H - 36),
                        f"- {i + 1} -", fontsize=9, fontname="tiro",
                        color=(0.4, 0.4, 0.4))

    # Set table of contents / bookmarks
    doc.set_toc(toc_entries)

    # Do NOT set any custom open action or page mode - the task is to add these
    doc.save(OUTPUT)
    doc.close()

    print(f"Initial file created: {OUTPUT}")
    print(f"Pages: 30, Bookmarks: {len(toc_entries)}")

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched evince with DISPLAY=:0")


create_initial()
