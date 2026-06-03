"""
Initial Setup: Create a 14-page partnership agreement PDF with 12 defined terms.
Task ID: pdf_legal_037
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_037'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/partnership_agreement.pdf'

# Page dimensions
W, H = 612, 792  # US Letter


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def add_page_text(doc, text_content, start_y=72, font="helv", fontsize=11,
                  bold_font="hebo", title=None, title_size=14):
    """Add text content across pages. Returns (current_page, current_y)."""
    page = doc[-1] if doc.page_count > 0 else doc.new_page(width=W, height=H)
    y = start_y
    left_margin = 72
    right_margin = W - 72
    line_height = fontsize * 1.4
    bottom_margin = H - 72

    if title:
        page.insert_text(pymupdf.Point(left_margin, y), title,
                         fontsize=title_size, fontname=bold_font, color=(0, 0, 0))
        y += title_size * 2

    for para in text_content:
        # Check if we need a new page
        if y + line_height > bottom_margin:
            page = doc.new_page(width=W, height=H)
            y = 72

        # Use textbox for paragraph wrapping
        rect = pymupdf.Rect(left_margin, y, right_margin, bottom_margin)
        fontname = bold_font if para.startswith("ARTICLE") or para.startswith("Section") else font
        fs = fontsize + 1 if para.startswith("ARTICLE") else fontsize

        excess = page.insert_textbox(rect, para, fontsize=fs, fontname=fontname,
                                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

        # Estimate how many lines this paragraph took
        chars_per_line = int((right_margin - left_margin) / (fs * 0.5))
        if chars_per_line < 1:
            chars_per_line = 1
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * (fs * 1.4) + 8

        # If text overflowed, continue on new pages
        while excess < 0:
            page = doc.new_page(width=W, height=H)
            y = 72
            rect = pymupdf.Rect(left_margin, y, right_margin, bottom_margin)
            excess = page.insert_textbox(rect, "", fontsize=fs, fontname=fontname,
                                         color=(0, 0, 0))
            y += 20

    return page, y


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()
    left = 72
    right = W - 72
    text_width = right - left

    # ===== PAGE 1: Title Page =====
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(left, 120), "GENERAL PARTNERSHIP AGREEMENT",
                     fontsize=22, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(left, 160), "of",
                     fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(left, 190), "PACIFIC NORTHWEST VENTURES",
                     fontsize=18, fontname="hebo", color=(0, 0, 0.4))

    page.insert_text(pymupdf.Point(left, 260), "Effective Date: January 15, 2025",
                     fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(left, 280), "State of Washington",
                     fontsize=12, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(left, 340),
                     "CONFIDENTIAL - FOR AUTHORIZED PARTIES ONLY",
                     fontsize=10, fontname="hebo", color=(0.6, 0, 0))

    # ===== PAGE 2: Parties and Recitals with Defined Terms 1-4 =====
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(left, y), "PARTNERSHIP AGREEMENT",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 30

    paras = [
        'This General Partnership Agreement (hereinafter referred to as "the Agreement") is entered into and made effective as of the 15th day of January, 2025, by and between the following parties:',
        '',
        'Westfield Capital Group, LLC, a limited liability company organized and existing under the laws of the State of Washington, with its principal office located at 1200 Pacific Avenue, Suite 400, Seattle, Washington 98101 (hereinafter referred to as "the Managing Partner");',
        '',
        'and',
        '',
        'Cascade Investment Holdings, Inc., a corporation organized and existing under the laws of the State of Oregon, with its principal office located at 900 Morrison Street, Suite 1500, Portland, Oregon 97205 (hereinafter referred to as "the Limited Partner");',
        '',
        'and',
        '',
        'Evergreen Strategic Advisors, a sole proprietorship owned and operated by Margaret Thornton, with its principal office located at 450 Bellevue Way NE, Suite 200, Bellevue, Washington 98004 (hereinafter referred to as "the Advisory Partner");',
        '',
        'The Managing Partner, the Limited Partner, and the Advisory Partner are collectively referred to throughout this document as (hereinafter referred to as "the Partners") and individually as a "Partner."',
        '',
        'RECITALS',
        '',
        'WHEREAS, the Partners desire to form a general partnership under the laws of the State of Washington for the purpose of engaging in real estate development, property management, and investment advisory services;',
        '',
        'WHEREAS, the Partners have agreed to contribute capital, services, and expertise to the partnership in the proportions and manner described herein;',
        '',
        'WHEREAS, the Partners wish to define their respective rights, duties, obligations, and liabilities with respect to the partnership and to each other;',
        '',
        'NOW, THEREFORE, in consideration of the mutual promises, covenants, and agreements contained herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Partners agree as follows:',
    ]

    for para in paras:
        if not para:
            y += 8
            continue
        if para in ("RECITALS",):
            page.insert_text(pymupdf.Point(left, y), para,
                             fontsize=13, fontname="hebo", color=(0, 0, 0))
            y += 22
            continue
        rect = pymupdf.Rect(left, y, right, H - 72)
        excess = page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== PAGE 3-4: Article I - Formation and Name (Defined Terms 5-6) =====
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE I - FORMATION AND NAME",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art1_paras = [
        'Section 1.1 Formation. The Partners hereby form a general partnership pursuant to the provisions of the Revised Uniform Partnership Act of the State of Washington, Chapter 25.05 of the Revised Code of Washington, and upon the terms and conditions set forth in this Agreement.',
        '',
        'Section 1.2 Name. The business of the partnership shall be conducted under the name "Pacific Northwest Ventures" (hereinafter referred to as "the Partnership") or such other name as the Partners may unanimously agree upon from time to time. The Partnership shall file all necessary assumed business name certificates and registrations as required by applicable law.',
        '',
        'Section 1.3 Principal Office. The principal office of the Partnership shall be located at 1200 Pacific Avenue, Suite 500, Seattle, Washington 98101 (hereinafter referred to as "the Principal Office"), or at such other location as the Partners may designate by unanimous written consent. The Partnership may maintain additional offices at such other places as the Partners may determine.',
        '',
        'Section 1.4 Term. The Partnership shall commence on the date first written above and shall continue for an initial period of fifteen (15) years, unless earlier dissolved in accordance with the provisions of Article X of this Agreement, or extended by mutual written agreement of the Partners.',
        '',
        'Section 1.5 Registered Agent. The registered agent for service of process for the Partnership in the State of Washington shall be Thompson Legal Services, Inc., located at 800 Fifth Avenue, Suite 3200, Seattle, Washington 98104. The Managing Partner shall have the authority to change the registered agent upon written notice to all Partners.',
    ]

    for para in art1_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        bold = para.startswith("Section")
        fn = "hebo" if bold else "helv"
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE II - Purpose (Defined Term 7) =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE II - PURPOSE AND BUSINESS",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art2_paras = [
        'Section 2.1 Purpose. The purpose of the Partnership shall be to engage in real estate development, property acquisition, property management, investment advisory services, and any other lawful business activities as may be approved by the unanimous consent of the Partners. The scope of activities permitted under this Agreement shall collectively be known as (hereinafter referred to as "the Business Activities") and shall include, without limitation:',
        '',
        '(a) The acquisition, development, management, leasing, and disposition of real property located in the Pacific Northwest region, including but not limited to the states of Washington, Oregon, and Idaho;',
        '',
        '(b) The provision of investment advisory and consulting services to third-party clients in connection with real estate transactions and portfolio management;',
        '',
        '(c) The formation and management of joint ventures, syndications, and other investment vehicles related to real estate;',
        '',
        '(d) The borrowing of funds, the execution and delivery of promissory notes, bonds, debentures, and other evidence of indebtedness, and the securing of same by mortgage, pledge, or other lien on Partnership assets;',
        '',
        '(e) Any and all other activities incidental or ancillary to the foregoing purposes.',
        '',
        'Section 2.2 Limitations. The Partnership shall not engage in any business activity that is not substantially related to the Business Activities without the prior unanimous written consent of all Partners. The Partnership shall not make any investment that would cause the Partnership to be classified as an investment company under the Investment Company Act of 1940, as amended.',
    ]

    for para in art2_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE III - Capital Contributions (Defined Terms 8-9) =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE III - CAPITAL CONTRIBUTIONS",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art3_paras = [
        'Section 3.1 Initial Contributions. Each Partner shall make an initial capital contribution to the Partnership as set forth below. The aggregate of all initial capital contributions shall constitute (hereinafter referred to as "the Initial Capital") of the Partnership:',
        '',
        '(a) The Managing Partner shall contribute the sum of Two Million Five Hundred Thousand Dollars ($2,500,000.00) in cash, to be deposited into the Partnership bank account within thirty (30) days of the effective date of this Agreement;',
        '',
        '(b) The Limited Partner shall contribute the sum of One Million Seven Hundred Fifty Thousand Dollars ($1,750,000.00) in cash and real property valued at Seven Hundred Fifty Thousand Dollars ($750,000.00), consisting of a commercial parcel located at 2200 NW Vaughn Street, Portland, Oregon 97210, as appraised by an independent certified appraiser selected by the Partners;',
        '',
        '(c) The Advisory Partner shall contribute professional services valued at Five Hundred Thousand Dollars ($500,000.00), consisting of strategic advisory services, client relationship management, and business development expertise, to be rendered over the initial two-year period of the Partnership.',
        '',
        'Section 3.2 Additional Contributions. No Partner shall be required to make any additional capital contributions beyond those specified in Section 3.1 unless unanimously agreed upon by all Partners. Any additional capital contributions shall be documented in a written amendment to this Agreement.',
        '',
        'Section 3.3 Capital Accounts. The Partnership shall maintain a separate capital account for each Partner. Each Partner\'s capital account shall be credited with such Partner\'s capital contributions and share of Partnership profits, and shall be debited with such Partner\'s share of Partnership losses and distributions. The books and records reflecting the capital accounts shall be maintained at the Principal Office and collectively constitute (hereinafter referred to as "the Capital Records").',
        '',
        'Section 3.4 Interest on Capital. No interest shall be paid on any capital contribution or on any balance in any Partner\'s capital account, unless otherwise agreed in writing by all Partners.',
        '',
        'Section 3.5 Return of Capital. No Partner shall have the right to withdraw or demand the return of such Partner\'s capital contribution, or any portion thereof, except upon dissolution of the Partnership or with the unanimous written consent of all Partners.',
    ]

    for para in art3_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE IV - Profit and Loss Allocation =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE IV - ALLOCATION OF PROFITS AND LOSSES",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art4_paras = [
        'Section 4.1 Allocation. The net profits and net losses of the Partnership for each fiscal year shall be allocated among the Partners in the following proportions:',
        '',
        '(a) The Managing Partner: Forty-five percent (45%);',
        '(b) The Limited Partner: Forty percent (40%);',
        '(c) The Advisory Partner: Fifteen percent (15%).',
        '',
        'Section 4.2 Special Allocations. Notwithstanding Section 4.1, the Partners may agree by unanimous written consent to make special allocations of income, gain, loss, deduction, or credit items among the Partners in a manner different from the general allocation percentages, provided that such special allocations have substantial economic effect within the meaning of Section 704(b) of the Internal Revenue Code.',
        '',
        'Section 4.3 Tax Allocations. Tax items shall be allocated in accordance with the principles of Section 704(c) of the Internal Revenue Code to the extent applicable. The Partnership shall maintain records sufficient to enable the allocation of all items of income, gain, loss, deduction, and credit in compliance with applicable federal and state tax laws.',
        '',
        'Section 4.4 Distribution Policy. The net profits available for distribution, after setting aside reasonable reserves for operating expenses, capital expenditures, and contingencies as determined by the Managing Partner with the approval of the Advisory Partner, shall be distributed to the Partners in accordance with their profit-sharing percentages on a quarterly basis, within forty-five (45) days following the close of each fiscal quarter. Such distributable amounts shall collectively constitute (hereinafter referred to as "the Quarterly Distributions").',
    ]

    for para in art4_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE V - Management (Defined Term 10) =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE V - MANAGEMENT AND OPERATIONS",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art5_paras = [
        'Section 5.1 Management Authority. The day-to-day management and operations of the Partnership shall be vested in the Managing Partner, who shall have the authority to make decisions regarding ordinary business matters without the prior consent of the other Partners, subject to the limitations set forth in Section 5.3 below.',
        '',
        'Section 5.2 Advisory Role. The Advisory Partner shall serve as a strategic advisor to the Partnership and shall be responsible for identifying new business opportunities, maintaining client relationships, and providing guidance on investment strategy. The Advisory Partner shall report to the Managing Partner and the Limited Partner on a quarterly basis regarding advisory activities and opportunities.',
        '',
        'Section 5.3 Major Decisions. The following actions shall require the unanimous written consent of all Partners, and shall collectively be known as (hereinafter referred to as "the Reserved Matters"):',
        '',
        '(a) The acquisition or disposition of any asset with a value exceeding Five Hundred Thousand Dollars ($500,000.00);',
        '(b) The incurrence of any indebtedness exceeding Two Hundred Fifty Thousand Dollars ($250,000.00);',
        '(c) The entry into any lease with annual payments exceeding One Hundred Thousand Dollars ($100,000.00);',
        '(d) The admission of any new Partner or the modification of any Partner\'s interest;',
        '(e) The amendment of this Agreement;',
        '(f) The merger, consolidation, or dissolution of the Partnership;',
        '(g) The commencement or settlement of any litigation involving claims exceeding One Hundred Thousand Dollars ($100,000.00);',
        '(h) The establishment of any employee benefit plan or compensation arrangement.',
        '',
        'Section 5.4 Meetings. The Partners shall hold regular meetings at least once per calendar quarter to review the financial performance and operations of the Partnership. Special meetings may be called by any Partner upon five (5) business days\' prior written notice to all other Partners.',
        '',
        'Section 5.5 Voting. Except as otherwise provided in this Agreement, all decisions requiring Partner approval shall be made by majority vote, with each Partner having one vote regardless of the Partner\'s percentage interest in the Partnership.',
    ]

    for para in art5_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE VI - Books and Records =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE VI - BOOKS, RECORDS, AND ACCOUNTING",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art6_paras = [
        'Section 6.1 Books and Records. The Managing Partner shall maintain, or cause to be maintained, full, complete, and accurate books of account and other records of the Partnership at the Principal Office. Such books and records shall include, but not be limited to:',
        '',
        '(a) A current list of the full name and last known business, residence, or mailing address of each Partner;',
        '(b) A copy of this Agreement and all amendments thereto;',
        '(c) Copies of the Partnership\'s federal, state, and local income tax returns for the three (3) most recent fiscal years;',
        '(d) Copies of all financial statements for the three (3) most recent fiscal years;',
        '(e) The Capital Records as defined in Section 3.3.',
        '',
        'Section 6.2 Fiscal Year. The fiscal year of the Partnership shall be the calendar year, ending December 31 of each year.',
        '',
        'Section 6.3 Accounting Method. The Partnership shall use the accrual method of accounting for both financial reporting and tax purposes, unless otherwise determined by the Managing Partner with the consent of a majority of the Partners.',
        '',
        'Section 6.4 Annual Audit. The Partnership\'s financial statements shall be audited annually by an independent certified public accounting firm selected by the Managing Partner. The audited financial statements shall be delivered to each Partner within ninety (90) days following the close of each fiscal year.',
        '',
        'Section 6.5 Tax Returns. The Managing Partner shall cause the Partnership\'s tax returns to be prepared and filed in a timely manner. Schedule K-1 or equivalent tax reporting documents shall be provided to each Partner within seventy-five (75) days following the close of each fiscal year.',
    ]

    for para in art6_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE VII - Transfer of Interests (Defined Term 11) =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE VII - TRANSFER OF PARTNERSHIP INTERESTS",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art7_paras = [
        'Section 7.1 Restrictions on Transfer. No Partner may sell, assign, transfer, pledge, hypothecate, or otherwise dispose of or encumber all or any portion of such Partner\'s interest in the Partnership without the prior unanimous written consent of all other Partners and compliance with the conditions specified in this Article VII. Any such permitted sale, assignment, or transfer shall be subject to the right of first refusal set forth herein (hereinafter referred to as "the Transfer Restrictions").',
        '',
        'Section 7.2 Right of First Refusal. Before any Partner may transfer all or any portion of such Partner\'s interest to any third party, the transferring Partner must first offer the interest to the remaining Partners on the same terms and conditions as the proposed third-party transfer. The remaining Partners shall have thirty (30) days from receipt of written notice to exercise their right of first refusal, on a pro rata basis in proportion to their respective interests in the Partnership.',
        '',
        'Section 7.3 Permitted Transfers. Notwithstanding the foregoing, a Partner may transfer all or any portion of such Partner\'s interest without the consent of the other Partners to: (a) a revocable living trust established for the benefit of the transferring Partner and/or the transferring Partner\'s immediate family members; (b) a corporation, limited liability company, or other entity wholly owned by the transferring Partner; or (c) the transferring Partner\'s spouse, children, or grandchildren, provided that the transferee agrees in writing to be bound by all terms and conditions of this Agreement.',
        '',
        'Section 7.4 Effect of Transfer. Any permitted transfer of a Partner\'s interest shall not dissolve or terminate the Partnership. The transferee shall succeed to the transferring Partner\'s rights and obligations under this Agreement to the extent of the transferred interest.',
    ]

    for para in art7_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE VIII - Indemnification =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE VIII - INDEMNIFICATION AND LIABILITY",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art8_paras = [
        'Section 8.1 Indemnification. The Partnership shall indemnify, defend, and hold harmless each Partner and such Partner\'s officers, directors, employees, agents, and affiliates from and against any and all claims, demands, losses, damages, liabilities, costs, and expenses (including reasonable attorneys\' fees and court costs) arising out of or relating to the business, operations, or affairs of the Partnership, except to the extent that such claims, demands, losses, damages, liabilities, costs, and expenses result from the willful misconduct, gross negligence, or breach of fiduciary duty by the Partner seeking indemnification.',
        '',
        'Section 8.2 Limitation of Liability. No Partner shall be personally liable for any debts, obligations, or liabilities of the Partnership in excess of such Partner\'s capital contribution and share of undistributed profits, except as otherwise required by applicable law or as a result of such Partner\'s willful misconduct, gross negligence, or fraud.',
        '',
        'Section 8.3 Insurance. The Partnership shall obtain and maintain comprehensive general liability insurance, professional liability insurance, directors and officers liability insurance, and such other insurance coverages as the Managing Partner deems necessary or appropriate, in amounts adequate to protect the interests of the Partnership and the Partners.',
    ]

    for para in art8_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE IX - Non-Competition (Defined Term 12) =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE IX - NON-COMPETITION AND CONFIDENTIALITY",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art9_paras = [
        'Section 9.1 Non-Competition. During the term of this Agreement and for a period of two (2) years following the withdrawal or removal of any Partner from the Partnership, each Partner agrees not to directly or indirectly engage in, own, manage, operate, control, or participate in any business that competes with the Business Activities within a radius of one hundred (100) miles of the Principal Office or any other office maintained by the Partnership.',
        '',
        'Section 9.2 Confidentiality. Each Partner acknowledges that, in the course of the Partnership\'s business, the Partners will have access to and become acquainted with confidential and proprietary information belonging to the Partnership, including but not limited to business plans, financial projections, client lists, investment strategies, proprietary software, trade secrets, and other proprietary information. All such information shall collectively constitute (hereinafter referred to as "the Confidential Information") and each Partner agrees to hold such information in strict confidence and not to disclose, publish, or otherwise reveal any of the Confidential Information to any third party during or after the term of this Agreement, except as required by law or as authorized by the unanimous written consent of the Partners.',
        '',
        'Section 9.3 Non-Solicitation. During the term of this Agreement and for a period of one (1) year following the withdrawal or removal of any Partner from the Partnership, each Partner agrees not to directly or indirectly solicit any client, customer, vendor, or employee of the Partnership for the purpose of diverting business from the Partnership or inducing any employee to terminate their employment with the Partnership.',
        '',
        'Section 9.4 Remedies. Each Partner acknowledges and agrees that any breach of the covenants contained in this Article IX would cause irreparable harm to the Partnership and the other Partners, and that monetary damages would be an insufficient remedy. Accordingly, in addition to any other remedies available at law or in equity, the Partnership and the non-breaching Partners shall be entitled to seek injunctive relief, specific performance, or other equitable remedies to enforce the provisions of this Article IX.',
    ]

    for para in art9_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE X - Dissolution =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE X - DISSOLUTION AND WINDING UP",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art10_paras = [
        'Section 10.1 Events of Dissolution. The Partnership shall be dissolved upon the occurrence of any of the following events: (a) the unanimous written agreement of all Partners to dissolve the Partnership; (b) the expiration of the term of the Partnership as specified in Section 1.4; (c) the entry of a decree of judicial dissolution under applicable law; (d) the death, disability, bankruptcy, or insolvency of any Partner, unless the remaining Partners unanimously agree to continue the Partnership within ninety (90) days of such event; or (e) any event that makes it unlawful to carry on the business of the Partnership.',
        '',
        'Section 10.2 Winding Up. Upon dissolution, the Managing Partner (or, if the Managing Partner is unable or unwilling to act, such other Partner as may be designated by the remaining Partners) shall proceed to wind up the affairs of the Partnership. The winding-up process shall include the following steps, in the order of priority set forth below:',
        '',
        '(a) The collection and liquidation of all Partnership assets at the best prices obtainable;',
        '(b) The payment of all Partnership debts and obligations to third-party creditors;',
        '(c) The setting aside of any reserves that the person winding up the Partnership deems reasonably necessary for any contingent or unforeseen liabilities or obligations of the Partnership;',
        '(d) The repayment of any loans or advances made by any Partner to the Partnership;',
        '(e) The return of each Partner\'s capital contribution, to the extent of the positive balance in such Partner\'s capital account;',
        '(f) The distribution of any remaining assets among the Partners in accordance with their profit-sharing percentages.',
        '',
        'Section 10.3 Accounting Upon Dissolution. Within one hundred twenty (120) days following the dissolution of the Partnership, the Managing Partner shall provide to each Partner a full and accurate accounting of the assets, liabilities, and capital accounts of the Partnership as of the date of dissolution.',
    ]

    for para in art10_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== ARTICLE XI - General Provisions =====
    if y > H - 150:
        page = doc.new_page(width=W, height=H)
        y = 72
    page.insert_text(pymupdf.Point(left, y), "ARTICLE XI - GENERAL PROVISIONS",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 28

    art11_paras = [
        'Section 11.1 Entire Agreement. This Agreement, together with all exhibits, schedules, and amendments hereto, constitutes the entire agreement among the Partners with respect to the subject matter hereof and supersedes all prior agreements, understandings, negotiations, and discussions, whether oral or written, relating to such subject matter.',
        '',
        'Section 11.2 Amendments. This Agreement may be amended, modified, or supplemented only by a written instrument executed by all Partners. No waiver of any provision of this Agreement shall be effective unless set forth in a written instrument signed by the Partner or Partners waiving such provision.',
        '',
        'Section 11.3 Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Washington, without giving effect to the principles of conflicts of law thereof.',
        '',
        'Section 11.4 Dispute Resolution. Any dispute, controversy, or claim arising out of or relating to this Agreement, or the breach, termination, or invalidity thereof, shall first be submitted to mediation in accordance with the mediation rules of the American Arbitration Association. If mediation fails to resolve the dispute within sixty (60) days, the dispute shall be submitted to binding arbitration in Seattle, Washington, in accordance with the Commercial Arbitration Rules of the American Arbitration Association.',
        '',
        'Section 11.5 Severability. If any provision of this Agreement is held to be invalid, illegal, or unenforceable in any respect, such invalidity, illegality, or unenforceability shall not affect any other provision of this Agreement, and this Agreement shall be construed as if such invalid, illegal, or unenforceable provision had never been contained herein.',
        '',
        'Section 11.6 Notices. All notices, requests, demands, and other communications required or permitted under this Agreement shall be in writing and shall be deemed to have been duly given when delivered in person, sent by certified mail (return receipt requested, postage prepaid), sent by overnight courier service, or transmitted by email (with confirmation of receipt) to the addresses set forth above or to such other address as any Partner may designate by notice to the other Partners.',
        '',
        'Section 11.7 Counterparts. This Agreement may be executed in two or more counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument.',
        '',
        'Section 11.8 Headings. The section headings contained in this Agreement are for reference purposes only and shall not affect the meaning or interpretation of this Agreement.',
        '',
        'Section 11.9 Waiver. The failure of any Partner to insist upon the strict performance of any provision of this Agreement shall not be construed as a waiver of any subsequent default of the same or similar nature.',
    ]

    for para in art11_paras:
        if not para:
            y += 6
            continue
        if y > H - 100:
            page = doc.new_page(width=W, height=H)
            y = 72
        rect = pymupdf.Rect(left, y, right, H - 72)
        page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        chars_per_line = int(text_width / (11 * 0.5))
        num_lines = max(1, (len(para) + chars_per_line - 1) // chars_per_line)
        y += num_lines * 15.4 + 6
        if y > H - 90:
            page = doc.new_page(width=W, height=H)
            y = 72

    # ===== SIGNATURE PAGE =====
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(left, y), "SIGNATURE PAGE",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 30

    page.insert_textbox(pymupdf.Rect(left, y, right, y + 40),
                        "IN WITNESS WHEREOF, the Partners have executed this General Partnership Agreement as of the date first written above.",
                        fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 60

    signatures = [
        ("WESTFIELD CAPITAL GROUP, LLC", "Managing Partner", "Robert J. Westfield", "Chief Executive Officer"),
        ("CASCADE INVESTMENT HOLDINGS, INC.", "Limited Partner", "Diana L. Cascade", "President"),
        ("EVERGREEN STRATEGIC ADVISORS", "Advisory Partner", "Margaret Thornton", "Principal"),
    ]

    for company, role, name, title in signatures:
        page.insert_text(pymupdf.Point(left, y), company,
                         fontsize=11, fontname="hebo", color=(0, 0, 0))
        y += 18
        page.insert_text(pymupdf.Point(left, y), f"({role})",
                         fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 30

        # Signature line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(left, y), pymupdf.Point(left + 250, y))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()
        y += 5
        page.insert_text(pymupdf.Point(left, y), f"By: {name}",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15
        page.insert_text(pymupdf.Point(left, y), f"Title: {title}",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15
        page.insert_text(pymupdf.Point(left, y), "Date: January 15, 2025",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 40

    # Pad to 14 pages if needed
    while doc.page_count < 14:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(left, 72),
                         f"[This page intentionally left blank - Page {doc.page_count}]",
                         fontsize=10, fontname="helv", color=(0.5, 0.5, 0.5))

    # Add page numbers to all pages
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(pymupdf.Point(W / 2 - 10, H - 40),
                       f"- {i + 1} -",
                       fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {pymupdf.open(OUTPUT).page_count}')

    # Verify defined terms
    doc = pymupdf.open(OUTPUT)
    full_text = ""
    for p in doc:
        full_text += p.get_text("text")
    doc.close()

    import re
    terms = re.findall(r'hereinafter referred to as\s+"([^"]+)"', full_text)
    print(f'Found {len(terms)} defined terms: {terms}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
