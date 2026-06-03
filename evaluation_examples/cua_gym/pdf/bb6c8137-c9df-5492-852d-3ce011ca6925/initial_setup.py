"""
Initial Setup: Create accounting policy PDF v2 with 18 pages
Task ID: pdf_fin_077
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_077'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/accounting_policy_v2.pdf'


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
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Document structure - 18 pages of accounting policy content
    sections = [
        # Page 1: Title page
        {
            "title": "Greenfield Industries, Inc.",
            "subtitle": "Corporate Accounting Policy Manual",
            "body": (
                "Version 2.0\n\n"
                "Effective Date: March 15, 2022\n\n"
                "Approved by: Victoria Hargrove, Chief Financial Officer\n"
                "Reviewed by: Internal Audit Committee\n\n"
                "Classification: Internal Use Only\n\n"
                "Document Control Number: FIN-POL-2022-003\n\n"
                "This manual establishes the accounting policies, procedures, and internal "
                "controls governing the financial reporting activities of Greenfield Industries, Inc. "
                "and all subsidiary entities. All finance department personnel are required to comply "
                "with the standards set forth herein."
            ),
        },
        # Page 2: Table of Contents
        {
            "title": "Table of Contents",
            "body": (
                "1. General Accounting Principles .......................... 3\n"
                "2. Revenue Recognition Policy ............................ 4\n"
                "3. Accounts Receivable Management ........................ 5\n"
                "4. Inventory Valuation Methods ........................... 6\n"
                "5. Fixed Asset Capitalization ............................. 7\n"
                "6. Depreciation and Amortization ......................... 8\n"
                "7. Accounts Payable Procedures ........................... 9\n"
                "8. Accrued Liabilities and Provisions ................... 10\n"
                "9. Intercompany Transactions ............................ 11\n"
                "10. Foreign Currency Translation ........................ 12\n"
                "11. Lease Accounting (ASC 842) .......................... 13\n"
                "12. Income Tax Provisions ............................... 14\n"
                "13. Equity and Share-Based Compensation ................. 15\n"
                "14. Financial Close Procedures .......................... 16\n"
                "15. Internal Controls and Compliance .................... 17\n"
                "16. Appendix: Chart of Accounts Summary ................. 18\n"
            ),
        },
        # Page 3
        {
            "title": "1. General Accounting Principles",
            "body": (
                "1.1 Basis of Preparation\n\n"
                "All financial statements shall be prepared in accordance with U.S. Generally Accepted "
                "Accounting Principles (GAAP) as codified by the Financial Accounting Standards Board "
                "(FASB). The Company follows the accrual basis of accounting.\n\n"
                "1.2 Fiscal Year\n\n"
                "The fiscal year runs from January 1 through December 31. Quarterly reporting periods "
                "end on March 31, June 30, September 30, and December 31.\n\n"
                "1.3 Materiality Threshold\n\n"
                "Individual transactions exceeding $25,000 require separate disclosure review. "
                "Cumulative adjustments affecting net income by more than 2% of pre-tax earnings "
                "must be reported to the Audit Committee within 5 business days.\n\n"
                "1.4 Consistency Principle\n\n"
                "Accounting methods, once adopted, shall be applied consistently across reporting "
                "periods. Any change in accounting policy requires written approval from the CFO "
                "and disclosure in the notes to financial statements."
            ),
        },
        # Page 4
        {
            "title": "2. Revenue Recognition Policy",
            "body": (
                "2.1 Overview\n\n"
                "Revenue is recognized in accordance with ASC 606, Revenue from Contracts with "
                "Customers. The five-step model is applied to all customer contracts:\n\n"
                "  Step 1: Identify the contract\n"
                "  Step 2: Identify performance obligations\n"
                "  Step 3: Determine the transaction price\n"
                "  Step 4: Allocate the price to obligations\n"
                "  Step 5: Recognize revenue as obligations are satisfied\n\n"
                "2.2 Product Revenue\n\n"
                "Revenue from product sales is recognized at the point of transfer of control to the "
                "customer, typically upon shipment (FOB shipping point) or delivery (FOB destination) "
                "as specified in the contract terms.\n\n"
                "2.3 Service Revenue\n\n"
                "Service revenue is recognized over time using the input method (cost-to-cost) for "
                "long-term contracts exceeding $500,000 and over time using the output method for "
                "recurring maintenance agreements. Revenue for contracts under $50,000 may be "
                "recognized at a point in time upon completion."
            ),
        },
        # Page 5
        {
            "title": "3. Accounts Receivable Management",
            "body": (
                "3.1 Credit Terms\n\n"
                "Standard payment terms are Net 30 days from invoice date. Extended terms of "
                "Net 45 or Net 60 require approval from the Director of Credit and Collections.\n\n"
                "3.2 Allowance for Doubtful Accounts\n\n"
                "The allowance is calculated using the current expected credit loss (CECL) model "
                "as required by ASC 326. The aging schedule is:\n\n"
                "  Current (0-30 days):      0.5% estimated loss rate\n"
                "  31-60 days past due:       2.0% estimated loss rate\n"
                "  61-90 days past due:       8.0% estimated loss rate\n"
                "  91-120 days past due:     25.0% estimated loss rate\n"
                "  Over 120 days past due:   60.0% estimated loss rate\n\n"
                "3.3 Write-Off Procedures\n\n"
                "Accounts are written off after 180 days past due and all collection efforts have "
                "been exhausted. Write-offs exceeding $10,000 require Controller approval. "
                "Write-offs exceeding $50,000 require CFO approval."
            ),
        },
        # Page 6
        {
            "title": "4. Inventory Valuation Methods",
            "body": (
                "4.1 Valuation Basis\n\n"
                "Inventory is valued at the lower of cost or net realizable value (NRV) in "
                "accordance with ASC 330.\n\n"
                "4.2 Cost Flow Assumption\n\n"
                "The Company uses the weighted average cost method for raw materials and "
                "work-in-progress. Finished goods are valued using standard costing with "
                "quarterly variance analysis.\n\n"
                "4.3 Inventory Categories and Targets\n\n"
                "  Raw Materials:        Target turnover 8x per year\n"
                "  Work-in-Progress:     Target turnover 12x per year\n"
                "  Finished Goods:       Target turnover 6x per year\n"
                "  Spare Parts/MRO:      Reviewed semi-annually for obsolescence\n\n"
                "4.4 Obsolescence Reserve\n\n"
                "Inventory items with no movement for 12 months are reserved at 50%. Items "
                "with no movement for 24 months are reserved at 100%. The reserve is reviewed "
                "quarterly by the Operations Controller."
            ),
        },
        # Page 7
        {
            "title": "5. Fixed Asset Capitalization",
            "body": (
                "5.1 Capitalization Threshold\n\n"
                "Assets with a useful life exceeding one year and a cost exceeding $5,000 shall "
                "be capitalized. Items below this threshold are expensed in the period acquired.\n\n"
                "5.2 Asset Categories\n\n"
                "  Land:                  Not depreciated\n"
                "  Buildings:             Useful life 30-40 years\n"
                "  Machinery & Equipment: Useful life 5-15 years\n"
                "  Vehicles:              Useful life 3-7 years\n"
                "  Computer Equipment:    Useful life 3-5 years\n"
                "  Furniture & Fixtures:  Useful life 5-10 years\n"
                "  Leasehold Improvements: Lesser of useful life or lease term\n\n"
                "5.3 Capital Projects\n\n"
                "Projects exceeding $100,000 require a Capital Expenditure Request (CER) form "
                "approved by the VP of Finance. Projects exceeding $500,000 require Board approval. "
                "Interest costs are capitalized during the construction period for qualifying assets."
            ),
        },
        # Page 8
        {
            "title": "6. Depreciation and Amortization",
            "body": (
                "6.1 Depreciation Methods\n\n"
                "Straight-line depreciation is the standard method for all asset classes unless "
                "an alternative method better reflects the pattern of economic benefit consumption.\n\n"
                "6.2 Salvage Value\n\n"
                "A salvage value of 5% of original cost is assumed for machinery and equipment. "
                "Computer equipment and vehicles assume zero salvage value. Salvage estimates "
                "are reviewed annually.\n\n"
                "6.3 Impairment Testing\n\n"
                "Long-lived assets are tested for impairment whenever events or changes in "
                "circumstances indicate the carrying amount may not be recoverable (ASC 360). "
                "Triggering events include:\n\n"
                "  - Significant decrease in market price\n"
                "  - Adverse change in business climate\n"
                "  - Accumulation of costs significantly above original expectation\n"
                "  - Operating losses or cash flow declines\n\n"
                "6.4 Intangible Assets\n\n"
                "Definite-lived intangibles are amortized over their estimated useful lives. "
                "Goodwill and indefinite-lived intangibles are tested annually for impairment."
            ),
        },
        # Page 9
        {
            "title": "7. Accounts Payable Procedures",
            "body": (
                "7.1 Invoice Processing\n\n"
                "All vendor invoices must be matched against an approved purchase order and "
                "receiving report (three-way match) before payment processing.\n\n"
                "7.2 Payment Terms\n\n"
                "Standard payment terms negotiated with vendors:\n\n"
                "  2/10 Net 30:    Take 2% discount if paid within 10 days\n"
                "  Net 30:         Standard terms\n"
                "  Net 45:         For strategic suppliers with volume agreements\n"
                "  Net 60:         Requires VP Finance approval\n\n"
                "7.3 Payment Approval Matrix\n\n"
                "  Up to $5,000:          Department Manager\n"
                "  $5,001 - $25,000:      Director level\n"
                "  $25,001 - $100,000:    VP level\n"
                "  $100,001 - $500,000:   CFO\n"
                "  Over $500,000:         CEO + CFO joint approval\n\n"
                "7.4 Vendor Setup\n\n"
                "New vendors require a completed W-9, credit reference check, and approval "
                "by the Procurement Department before being added to the vendor master file."
            ),
        },
        # Page 10
        {
            "title": "8. Accrued Liabilities and Provisions",
            "body": (
                "8.1 Month-End Accruals\n\n"
                "All known liabilities must be accrued at each month-end close regardless of "
                "whether an invoice has been received. Common accruals include:\n\n"
                "  - Employee wages and benefits (earned but unpaid)\n"
                "  - Utilities and telecommunications\n"
                "  - Professional fees (audit, legal, consulting)\n"
                "  - Interest on outstanding debt\n"
                "  - Property and sales taxes\n\n"
                "8.2 Provision Recognition\n\n"
                "Provisions are recognized when: (a) there is a present obligation from a past "
                "event, (b) an outflow of resources is probable, and (c) a reliable estimate "
                "can be made. The best estimate of the expenditure is recorded.\n\n"
                "8.3 Warranty Provisions\n\n"
                "Product warranty provisions are calculated at 2.5% of trailing twelve-month "
                "revenue for the Industrial Products segment and 1.8% for the Consumer Products "
                "segment, adjusted quarterly based on actual claim experience."
            ),
        },
        # Page 11
        {
            "title": "9. Intercompany Transactions",
            "body": (
                "9.1 Transfer Pricing\n\n"
                "All intercompany transactions must be conducted at arm's length in compliance "
                "with IRC Section 482 and OECD Transfer Pricing Guidelines. The Company uses "
                "the Comparable Uncontrolled Price (CUP) method as the primary approach.\n\n"
                "9.2 Intercompany Elimination\n\n"
                "All intercompany balances and transactions are eliminated in consolidation. "
                "The Corporate Accounting team maintains the intercompany elimination matrix "
                "and reconciles balances monthly.\n\n"
                "9.3 Intercompany Settlement\n\n"
                "Intercompany invoices are settled quarterly via netting. Outstanding balances "
                "exceeding $1,000,000 for more than 90 days require escalation to the "
                "International Tax Director.\n\n"
                "9.4 Documentation Requirements\n\n"
                "Each intercompany transaction must be supported by a written agreement, "
                "transfer pricing study (updated annually), and contemporaneous documentation "
                "of the economic substance of the arrangement."
            ),
        },
        # Page 12
        {
            "title": "10. Foreign Currency Translation",
            "body": (
                "10.1 Functional Currency Determination\n\n"
                "Each subsidiary's functional currency is determined based on the primary "
                "economic environment in which it operates (ASC 830). Current designations:\n\n"
                "  Greenfield Europe GmbH:        EUR\n"
                "  Greenfield Asia Pacific Ltd:    SGD\n"
                "  Greenfield Canada Inc:          CAD\n"
                "  Greenfield UK Ltd:              GBP\n"
                "  Greenfield Japan KK:            JPY\n\n"
                "10.2 Translation Method\n\n"
                "Assets and liabilities are translated at the closing rate. Income statement "
                "items are translated at the average rate for the period. Translation adjustments "
                "are recorded in Other Comprehensive Income (OCI).\n\n"
                "10.3 Transaction Gains and Losses\n\n"
                "Foreign currency transaction gains and losses are recorded in the income "
                "statement under 'Other Income/Expense.' Hedging gains and losses on designated "
                "hedges are recorded in OCI until the hedged item affects earnings."
            ),
        },
        # Page 13
        {
            "title": "11. Lease Accounting (ASC 842)",
            "body": (
                "11.1 Scope\n\n"
                "All contracts that convey the right to control the use of an identified asset "
                "for a period of time in exchange for consideration are within scope. Short-term "
                "leases (12 months or less) may elect the practical expedient for off-balance "
                "sheet treatment.\n\n"
                "11.2 Classification\n\n"
                "Leases are classified as either finance leases or operating leases based on "
                "the criteria in ASC 842-10-25-2. The Company's current lease portfolio:\n\n"
                "  Operating Leases:     87 active leases ($42.3M total obligation)\n"
                "  Finance Leases:       12 active leases ($18.7M total obligation)\n\n"
                "11.3 Measurement\n\n"
                "Right-of-use assets and lease liabilities are measured at the present value "
                "of remaining lease payments. The incremental borrowing rate (currently 5.25% "
                "for USD obligations) is used when the implicit rate is not determinable.\n\n"
                "11.4 Reassessment\n\n"
                "Lease terms are reassessed upon modification, exercise of renewal options, "
                "or triggering events. The Treasury team updates the IBR quarterly."
            ),
        },
        # Page 14
        {
            "title": "12. Income Tax Provisions",
            "body": (
                "12.1 Current Tax Provision\n\n"
                "The current income tax provision is calculated based on estimated taxable "
                "income for the period, applying enacted tax rates for each jurisdiction.\n\n"
                "12.2 Deferred Tax Assets and Liabilities\n\n"
                "Deferred taxes are recognized for temporary differences between financial "
                "reporting and tax bases of assets and liabilities (ASC 740). Significant "
                "deferred tax items include:\n\n"
                "  Deferred Tax Assets:\n"
                "    - Net operating loss carryforwards: $3.2M\n"
                "    - Allowance for doubtful accounts: $890K\n"
                "    - Accrued compensation: $1.4M\n"
                "    - Lease liabilities: $15.1M\n\n"
                "  Deferred Tax Liabilities:\n"
                "    - Depreciation differences: $8.6M\n"
                "    - Right-of-use assets: $14.8M\n"
                "    - Prepaid expenses: $420K\n\n"
                "12.3 Valuation Allowance\n\n"
                "A valuation allowance is established when it is more likely than not that "
                "some or all of the deferred tax asset will not be realized."
            ),
        },
        # Page 15
        {
            "title": "13. Equity and Share-Based Compensation",
            "body": (
                "13.1 Common Stock\n\n"
                "The Company has 50,000,000 authorized shares of common stock with a par "
                "value of $0.01 per share. As of the latest balance sheet date, 32,450,000 "
                "shares are issued and outstanding.\n\n"
                "13.2 Treasury Stock\n\n"
                "Treasury stock is accounted for using the cost method. The Company holds "
                "1,200,000 shares in treasury at an average cost of $28.50 per share.\n\n"
                "13.3 Stock Option Plans\n\n"
                "The 2020 Equity Incentive Plan authorizes 3,000,000 shares for issuance. "
                "Stock options vest over 4 years (25% cliff at year 1, monthly thereafter) "
                "and expire after 10 years. Fair value is estimated using the Black-Scholes "
                "model at grant date.\n\n"
                "13.4 Restricted Stock Units (RSUs)\n\n"
                "RSUs vest over 3 years (33.3% annually). Compensation expense is recognized "
                "ratably over the vesting period based on the grant-date fair value. Forfeiture "
                "rates are estimated at 8% annually for non-executive employees."
            ),
        },
        # Page 16
        {
            "title": "14. Financial Close Procedures",
            "body": (
                "14.1 Close Calendar\n\n"
                "  Business Day 1:    Sub-ledger closes (AP, AR, Payroll)\n"
                "  Business Day 2:    Journal entries and accruals posted\n"
                "  Business Day 3:    Intercompany eliminations processed\n"
                "  Business Day 4:    Account reconciliations completed\n"
                "  Business Day 5:    Management review and sign-off\n"
                "  Business Day 6:    Financial package distributed\n\n"
                "14.2 Journal Entry Controls\n\n"
                "All manual journal entries require supporting documentation and dual "
                "approval. Entries exceeding $100,000 require Controller review. "
                "Recurring entries are automated through the ERP system.\n\n"
                "14.3 Account Reconciliations\n\n"
                "All balance sheet accounts must be reconciled monthly. High-risk accounts "
                "(cash, receivables, inventory, debt) are reconciled by Business Day 3. "
                "All reconciliations must be reviewed by a supervisor within 5 business days.\n\n"
                "14.4 Variance Analysis\n\n"
                "Budget-to-actual variances exceeding 10% or $50,000 (whichever is less) "
                "require written explanation from the responsible department head."
            ),
        },
        # Page 17
        {
            "title": "15. Internal Controls and Compliance",
            "body": (
                "15.1 Control Framework\n\n"
                "The Company's internal control structure is based on the COSO 2013 Internal "
                "Control Integrated Framework. Controls are designed to provide reasonable "
                "assurance regarding the reliability of financial reporting.\n\n"
                "15.2 Segregation of Duties\n\n"
                "Key incompatible duties that must be segregated:\n\n"
                "  - Authorization vs. custody of assets\n"
                "  - Recording vs. custody of assets\n"
                "  - Authorization vs. recording of transactions\n"
                "  - IT access administration vs. transaction processing\n\n"
                "15.3 SOX Compliance\n\n"
                "As a publicly traded company, Greenfield Industries maintains compliance "
                "with Sarbanes-Oxley Act Sections 302 and 404. Key controls are tested "
                "annually by Internal Audit and the external audit team.\n\n"
                "15.4 Whistleblower Policy\n\n"
                "Employees may report accounting irregularities through the anonymous ethics "
                "hotline (1-800-555-ETHICS) or via the online portal. All reports are "
                "investigated by the Audit Committee within 30 days."
            ),
        },
        # Page 18
        {
            "title": "16. Appendix: Chart of Accounts Summary",
            "body": (
                "Account Range     Category              Description\n"
                "1000-1999         Assets                Current and non-current assets\n"
                "2000-2999         Liabilities           Current and long-term liabilities\n"
                "3000-3999         Equity                Stockholders' equity accounts\n"
                "4000-4999         Revenue               Sales and other revenue\n"
                "5000-5999         Cost of Goods Sold    Direct costs of production\n"
                "6000-6999         Operating Expenses    SGA and administrative costs\n"
                "7000-7999         Other Income/Expense  Non-operating items\n"
                "8000-8999         Tax Provisions        Income tax accounts\n"
                "9000-9999         Statistical           Non-financial tracking\n\n"
                "Key Account Details:\n\n"
                "  1010  Cash - Operating Account (JPMorgan Chase)\n"
                "  1020  Cash - Payroll Account (Bank of America)\n"
                "  1030  Cash - Money Market (Goldman Sachs)\n"
                "  1100  Accounts Receivable - Trade\n"
                "  1150  Allowance for Doubtful Accounts\n"
                "  1200  Inventory - Raw Materials\n"
                "  1210  Inventory - Work in Progress\n"
                "  1220  Inventory - Finished Goods\n"
                "  1300  Prepaid Expenses\n"
                "  1500  Property, Plant & Equipment\n"
                "  1550  Accumulated Depreciation\n\n"
                "Document End - Greenfield Industries Accounting Policy v2.0"
            ),
        },
    ]

    for i, section in enumerate(sections):
        page = doc.new_page(width=612, height=792)  # Letter size

        y = 72  # top margin

        # Title
        if i == 0:
            # Title page - centered, larger font
            page.insert_text(
                pymupdf.Point(306, y),
                section["title"],
                fontsize=22,
                fontname="hebo",
                color=(0, 0, 0.4),
            )
            y += 40
            if "subtitle" in section:
                page.insert_text(
                    pymupdf.Point(72, y),
                    section["subtitle"],
                    fontsize=18,
                    fontname="hebo",
                    color=(0, 0, 0.4),
                )
                y += 50
        else:
            # Section title
            page.insert_text(
                pymupdf.Point(72, y),
                section["title"],
                fontsize=16,
                fontname="hebo",
                color=(0, 0, 0.3),
            )
            # Underline
            title_width = pymupdf.get_text_length(section["title"], fontname="hebo", fontsize=16)
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y + 4), pymupdf.Point(72 + title_width, y + 4))
            shape.finish(color=(0, 0, 0.3), width=1)
            shape.commit()
            y += 30

        # Body text in a textbox
        rect = pymupdf.Rect(72, y, 540, 740)
        page.insert_textbox(
            rect,
            section["body"],
            fontsize=10.5,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number footer
        page.insert_text(
            pymupdf.Point(296, 770),
            str(i + 1),
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
