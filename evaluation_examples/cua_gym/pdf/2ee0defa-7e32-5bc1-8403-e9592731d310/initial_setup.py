"""
Initial Setup: Create 85-page audit document bundle for Bates numbering task
Task ID: pdf_fin_007
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_007'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/audit_docs.pdf'


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


# Realistic audit document content for 85 pages
AUDIT_SECTIONS = [
    {
        "title": "INDEPENDENT AUDITOR'S REPORT",
        "pages": 3,
        "content": [
            "To the Board of Directors and Shareholders of Meridian Holdings Inc.\n\n"
            "Opinion\n\n"
            "We have audited the accompanying consolidated financial statements of Meridian Holdings Inc. "
            "and its subsidiaries, which comprise the consolidated balance sheet as of December 31, 2025, "
            "and the related consolidated statements of comprehensive income, changes in stockholders' equity, "
            "and cash flows for the year then ended, and the related notes to the consolidated financial statements.\n\n"
            "In our opinion, the consolidated financial statements referred to above present fairly, in all material "
            "respects, the financial position of Meridian Holdings Inc. and its subsidiaries as of December 31, 2025, "
            "and the results of their operations and their cash flows for the year then ended in accordance with "
            "accounting principles generally accepted in the United States of America.",

            "Basis for Opinion\n\n"
            "We conducted our audit in accordance with auditing standards generally accepted in the United States "
            "of America (GAAS) and in accordance with the auditing standards of the Public Company Accounting "
            "Oversight Board (PCAOB). Our responsibilities under those standards are further described in the "
            "Auditor's Responsibilities for the Audit of the Consolidated Financial Statements section of our report. "
            "We are required to be independent of Meridian Holdings Inc. and to meet our other ethical responsibilities "
            "in accordance with the relevant ethical requirements relating to our audit.\n\n"
            "We believe that the audit evidence we have obtained is sufficient and appropriate to provide a basis "
            "for our audit opinion.",

            "Responsibilities of Management for the Financial Statements\n\n"
            "Management is responsible for the preparation and fair presentation of the consolidated financial "
            "statements in accordance with accounting principles generally accepted in the United States of America, "
            "and for the design, implementation, and maintenance of internal control relevant to the preparation and "
            "fair presentation of consolidated financial statements that are free from material misstatement, "
            "whether due to fraud or error.\n\n"
            "Grant Thornton LLP\nChicago, Illinois\nMarch 15, 2026",
        ],
    },
    {
        "title": "CONSOLIDATED BALANCE SHEET",
        "pages": 4,
        "content": [
            "Meridian Holdings Inc.\nConsolidated Balance Sheet\nAs of December 31, 2025\n(In thousands)\n\n"
            "ASSETS\n\n"
            "Current Assets:\n"
            "  Cash and cash equivalents          $  42,318\n"
            "  Short-term investments                 15,640\n"
            "  Accounts receivable, net               28,752\n"
            "  Inventories                            19,423\n"
            "  Prepaid expenses                        3,891\n"
            "  Other current assets                    2,156\n"
            "    Total current assets                112,180\n\n"
            "Non-current Assets:\n"
            "  Property, plant and equipment, net     87,643\n"
            "  Goodwill                               54,218\n"
            "  Intangible assets, net                 31,475\n"
            "  Operating lease right-of-use assets    22,910\n"
            "  Long-term investments                  18,330\n"
            "  Other non-current assets                6,752\n"
            "    Total non-current assets            221,328\n\n"
            "TOTAL ASSETS                           $333,508",

            "LIABILITIES AND STOCKHOLDERS' EQUITY\n\n"
            "Current Liabilities:\n"
            "  Accounts payable                    $  17,892\n"
            "  Accrued expenses                       12,431\n"
            "  Current portion of long-term debt       8,500\n"
            "  Current operating lease liabilities     5,218\n"
            "  Income taxes payable                    3,674\n"
            "  Other current liabilities               4,110\n"
            "    Total current liabilities            51,825\n\n"
            "Non-current Liabilities:\n"
            "  Long-term debt, net                    72,340\n"
            "  Operating lease liabilities, non-current 18,692\n"
            "  Deferred tax liabilities               11,485\n"
            "  Other long-term liabilities              5,830\n"
            "    Total non-current liabilities       108,347\n\n"
            "Total Liabilities                       160,172",

            "Stockholders' Equity:\n"
            "  Common stock, $0.01 par value;\n"
            "    500,000,000 shares authorized;\n"
            "    142,385,000 shares issued\n"
            "    and outstanding                   $    1,424\n"
            "  Additional paid-in capital             89,752\n"
            "  Retained earnings                      85,218\n"
            "  Accumulated other comprehensive\n"
            "    loss                                 (3,058)\n"
            "    Total stockholders' equity          173,336\n\n"
            "TOTAL LIABILITIES AND\n"
            "STOCKHOLDERS' EQUITY                   $333,508\n\n"
            "See accompanying notes to consolidated financial statements.",

            "Meridian Holdings Inc.\nConsolidated Balance Sheet (Comparative)\nAs of December 31, 2024\n(In thousands)\n\n"
            "ASSETS\n\n"
            "Current Assets:\n"
            "  Cash and cash equivalents          $  38,912\n"
            "  Short-term investments                 12,150\n"
            "  Accounts receivable, net               25,418\n"
            "  Inventories                            17,862\n"
            "  Prepaid expenses                        3,425\n"
            "    Total current assets                 97,767\n\n"
            "Non-current Assets:\n"
            "  Property, plant and equipment, net     82,310\n"
            "  Goodwill                               54,218\n"
            "  Intangible assets, net                 35,692\n"
            "    Total non-current assets            198,710\n\n"
            "TOTAL ASSETS                           $296,477",
        ],
    },
    {
        "title": "CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME",
        "pages": 3,
        "content": [
            "Meridian Holdings Inc.\nConsolidated Statement of Comprehensive Income\n"
            "For the Year Ended December 31, 2025\n(In thousands, except per share data)\n\n"
            "Net revenues                           $287,432\n"
            "Cost of revenues                       (168,915)\n"
            "  Gross profit                          118,517\n\n"
            "Operating expenses:\n"
            "  Research and development               (24,318)\n"
            "  Selling, general and administrative    (52,640)\n"
            "  Depreciation and amortization          (14,275)\n"
            "  Restructuring charges                   (2,180)\n"
            "    Total operating expenses             (93,413)\n\n"
            "Operating income                         25,104",

            "Other income (expense):\n"
            "  Interest income                         1,842\n"
            "  Interest expense                       (4,318)\n"
            "  Foreign exchange gain (loss)              (523)\n"
            "  Other income, net                          418\n"
            "    Total other expense, net              (2,581)\n\n"
            "Income before income taxes               22,523\n"
            "Income tax expense                        (5,631)\n"
            "Net income                             $ 16,892\n\n"
            "Other comprehensive income (loss):\n"
            "  Foreign currency translation adj.         (842)\n"
            "  Unrealized gain on investments              315\n"
            "  Comprehensive income                  $ 16,365",

            "Earnings per share:\n"
            "  Basic                                 $   0.12\n"
            "  Diluted                               $   0.12\n\n"
            "Weighted average shares outstanding:\n"
            "  Basic                            142,128,000\n"
            "  Diluted                          144,518,000\n\n"
            "See accompanying notes to consolidated financial statements.",
        ],
    },
    {
        "title": "CONSOLIDATED STATEMENT OF CASH FLOWS",
        "pages": 3,
        "content": [
            "Meridian Holdings Inc.\nConsolidated Statement of Cash Flows\n"
            "For the Year Ended December 31, 2025\n(In thousands)\n\n"
            "Cash flows from operating activities:\n"
            "  Net income                            $ 16,892\n"
            "  Adjustments to reconcile net income to\n"
            "  net cash provided by operating activities:\n"
            "    Depreciation and amortization         14,275\n"
            "    Stock-based compensation               4,832\n"
            "    Deferred income taxes                  1,218\n"
            "    Provision for doubtful accounts          875\n"
            "    Changes in operating assets and liabilities:\n"
            "      Accounts receivable                 (3,334)\n"
            "      Inventories                         (1,561)\n"
            "      Accounts payable                     2,418\n"
            "      Accrued expenses                     1,852\n"
            "  Net cash provided by operating activities 37,467",

            "Cash flows from investing activities:\n"
            "  Purchases of property and equipment   $(19,608)\n"
            "  Purchases of short-term investments     (8,490)\n"
            "  Maturities of short-term investments     5,000\n"
            "  Acquisitions, net of cash acquired           -\n"
            "  Other investing activities                (425)\n"
            "  Net cash used in investing activities  (23,523)\n\n"
            "Cash flows from financing activities:\n"
            "  Repayment of long-term debt            $(6,250)\n"
            "  Proceeds from stock option exercises      2,104\n"
            "  Dividends paid                          (5,692)\n"
            "  Treasury stock repurchased                (700)\n"
            "  Net cash used in financing activities  (10,538)",

            "Net increase in cash and cash equivalents   3,406\n"
            "Cash and cash equivalents, beginning of year 38,912\n"
            "Cash and cash equivalents, end of year    $ 42,318\n\n"
            "Supplemental disclosures:\n"
            "  Cash paid for income taxes             $  4,413\n"
            "  Cash paid for interest                 $  4,125\n\n"
            "Non-cash investing and financing activities:\n"
            "  Operating lease right-of-use assets      5,218\n"
            "  Capital expenditures in accounts payable  1,340\n\n"
            "See accompanying notes to consolidated financial statements.",
        ],
    },
    {
        "title": "NOTES TO CONSOLIDATED FINANCIAL STATEMENTS",
        "pages": 42,
        "content": None,  # Will be generated programmatically
    },
    {
        "title": "SCHEDULE OF INVESTMENTS",
        "pages": 8,
        "content": None,
    },
    {
        "title": "INTERNAL CONTROL ASSESSMENT",
        "pages": 10,
        "content": None,
    },
    {
        "title": "SUPPLEMENTARY INFORMATION",
        "pages": 6,
        "content": None,
    },
    {
        "title": "MANAGEMENT LETTER",
        "pages": 6,
        "content": None,
    },
]

# Notes content generator
NOTES_CONTENT = [
    "Note 1 - Organization and Summary of Significant Accounting Policies\n\n"
    "Meridian Holdings Inc. (the 'Company') is a diversified technology and manufacturing corporation "
    "headquartered in Chicago, Illinois. The Company operates through three reportable segments: "
    "Technology Solutions, Industrial Products, and Professional Services.\n\n"
    "Basis of Presentation: The consolidated financial statements include the accounts of Meridian "
    "Holdings Inc. and all subsidiaries in which the Company has a controlling financial interest. "
    "All intercompany balances and transactions have been eliminated in consolidation.",

    "Revenue Recognition: The Company recognizes revenue when control of promised goods or services "
    "is transferred to customers, in an amount that reflects the consideration expected to be entitled "
    "to in exchange for those goods or services. Revenue is recognized in accordance with ASC 606.\n\n"
    "Technology Solutions segment revenue is primarily derived from software licensing, cloud services, "
    "and technology consulting. Software licenses are recognized at a point in time when the license is "
    "delivered. Cloud services revenue is recognized over the subscription period.",

    "Inventory Valuation: Inventories are stated at the lower of cost or net realizable value. Cost is "
    "determined on a first-in, first-out (FIFO) basis for finished goods and raw materials. Work-in-process "
    "includes direct materials, direct labor, and applicable manufacturing overhead.\n\n"
    "As of December 31, 2025, inventory balances were:\n"
    "  Raw materials              $ 6,142\n"
    "  Work-in-process              4,871\n"
    "  Finished goods               8,410\n"
    "    Total inventories        $19,423",

    "Note 2 - Accounts Receivable\n\n"
    "Accounts receivable consisted of the following (in thousands):\n"
    "  Trade receivables           $30,418\n"
    "  Less: Allowance for\n"
    "    doubtful accounts          (1,666)\n"
    "  Net accounts receivable     $28,752\n\n"
    "The Company's allowance for doubtful accounts is based on management's assessment of "
    "the collectability of specific customer accounts and the aging of the accounts receivable.",

    "Note 3 - Property, Plant and Equipment\n\n"
    "Property, plant and equipment consisted of (in thousands):\n"
    "  Land                        $  8,420\n"
    "  Buildings and improvements     42,318\n"
    "  Machinery and equipment        65,742\n"
    "  Furniture and fixtures          8,915\n"
    "  Computer equipment             14,823\n"
    "  Vehicles                        3,240\n"
    "  Construction in progress         5,180\n"
    "    Total                       148,638\n"
    "  Less: Accumulated depreciation (60,995)\n"
    "  Net PP&E                     $ 87,643",

    "Note 4 - Goodwill and Intangible Assets\n\n"
    "The changes in goodwill by segment for 2025 were (in thousands):\n\n"
    "                   Technology  Industrial  Professional   Total\n"
    "Balance, 1/1/25    $28,410     $16,830      $8,978     $54,218\n"
    "Acquisitions             -           -           -           -\n"
    "Impairment               -           -           -           -\n"
    "Balance, 12/31/25  $28,410     $16,830      $8,978     $54,218\n\n"
    "The Company performed its annual goodwill impairment test as of October 1, 2025. "
    "No impairment was identified for any reporting unit.",

    "Note 5 - Debt Obligations\n\n"
    "Long-term debt consisted of (in thousands):\n"
    "  Senior secured credit facility,\n"
    "    variable rate (SOFR + 1.75%),\n"
    "    maturing June 2029              $35,000\n"
    "  Senior unsecured notes, 4.25%,\n"
    "    maturing March 2030              30,000\n"
    "  Equipment financing, various rates,\n"
    "    maturing 2026-2028               15,840\n"
    "    Total long-term debt             80,840\n"
    "  Less: Current portion              (8,500)\n"
    "  Long-term debt, net               $72,340",

    "Note 6 - Income Taxes\n\n"
    "The provision for income taxes consisted of (in thousands):\n"
    "  Current:\n"
    "    Federal                          $ 3,215\n"
    "    State and local                    1,198\n"
    "      Total current                    4,413\n"
    "  Deferred:\n"
    "    Federal                              895\n"
    "    State and local                      323\n"
    "      Total deferred                   1,218\n"
    "  Total income tax expense           $ 5,631\n\n"
    "Effective tax rate: 25.0%\n"
    "Statutory federal rate: 21.0%",

    "Note 7 - Leases\n\n"
    "The Company leases office space, manufacturing facilities, and equipment under "
    "operating and finance leases. Operating lease costs totaled $7,842 thousand for the "
    "year ended December 31, 2025.\n\n"
    "Right-of-use assets and lease liabilities:\n"
    "  Operating lease ROU assets          $22,910\n"
    "  Current operating lease liabilities   5,218\n"
    "  Non-current operating lease liabilities 18,692\n\n"
    "Weighted-average remaining lease term:  6.8 years\n"
    "Weighted-average discount rate:         4.2%",

    "Note 8 - Stock-Based Compensation\n\n"
    "The Company maintains the 2020 Equity Incentive Plan under which stock options, "
    "restricted stock units (RSUs), and performance share units (PSUs) may be granted.\n\n"
    "Stock-based compensation expense (in thousands):\n"
    "  Stock options                       $ 1,218\n"
    "  Restricted stock units                2,814\n"
    "  Performance share units                 800\n"
    "    Total                             $ 4,832\n\n"
    "As of December 31, 2025, total unrecognized stock-based compensation was $12,415 thousand.",

    "Note 9 - Segment Information\n\n"
    "The Company reports three segments:\n\n"
    "Revenue by segment (in thousands):\n"
    "  Technology Solutions               $142,718\n"
    "  Industrial Products                  98,214\n"
    "  Professional Services                46,500\n"
    "    Total revenues                   $287,432\n\n"
    "Operating income by segment:\n"
    "  Technology Solutions               $ 18,453\n"
    "  Industrial Products                  10,824\n"
    "  Professional Services                 5,312\n"
    "  Corporate and unallocated            (9,485)\n"
    "    Total operating income           $ 25,104",

    "Note 10 - Commitments and Contingencies\n\n"
    "The Company is involved in various legal proceedings arising in the ordinary course of business. "
    "Management believes that the resolution of these matters will not have a material adverse effect "
    "on the Company's financial position or results of operations.\n\n"
    "Purchase Commitments: As of December 31, 2025, the Company had non-cancelable purchase "
    "commitments totaling approximately $18,500 thousand, primarily for raw materials and components.\n\n"
    "Environmental Matters: The Company has accrued $2,150 thousand for estimated environmental "
    "remediation costs related to a former manufacturing site in Detroit, Michigan.",

    "Note 11 - Related Party Transactions\n\n"
    "During 2025, the Company entered into the following transactions with related parties:\n\n"
    "  Consulting services from Apex Advisory Group\n"
    "  (affiliated through a board member):           $1,240\n\n"
    "  Office lease from Meridian Real Estate Trust\n"
    "  (common ownership):                            $3,680\n\n"
    "All related party transactions were conducted at arm's length and on terms comparable "
    "to those available from unaffiliated third parties.",

    "Note 12 - Subsequent Events\n\n"
    "The Company has evaluated subsequent events through March 15, 2026, the date the "
    "consolidated financial statements were available to be issued.\n\n"
    "On January 22, 2026, the Company completed the acquisition of DataStream Analytics Inc. "
    "for approximately $28,500 thousand in cash. DataStream is a cloud analytics provider that "
    "will be integrated into the Technology Solutions segment.\n\n"
    "On February 10, 2026, the Board of Directors declared a quarterly dividend of $0.10 per share, "
    "payable on March 28, 2026 to shareholders of record as of March 14, 2026.",
]

INVESTMENT_CONTENT = [
    "Schedule of Investments\nAs of December 31, 2025\n(In thousands)\n\n"
    "SHORT-TERM INVESTMENTS\n\n"
    "U.S. Treasury Securities:\n"
    "  U.S. Treasury Note, 4.125%, 03/15/2026    $ 3,200\n"
    "  U.S. Treasury Note, 3.875%, 06/30/2026      2,800\n"
    "  U.S. Treasury Bill, 04/24/2026               2,140\n\n"
    "Corporate Bonds:\n"
    "  Apple Inc., 3.45%, 05/06/2026                1,500\n"
    "  Microsoft Corp., 3.30%, 02/06/2027           1,800\n"
    "  Johnson & Johnson, 3.40%, 01/15/2026         1,200\n"
    "  Procter & Gamble, 3.55%, 03/05/2026          1,000\n"
    "  Alphabet Inc., 3.375%, 02/25/2026            2,000\n"
    "    Total short-term investments             $15,640",

    "LONG-TERM INVESTMENTS\n\n"
    "Equity Securities:\n"
    "  Vanguard S&P 500 ETF (VOO)                $ 5,200\n"
    "  iShares Core U.S. Aggregate Bond ETF (AGG)  3,800\n"
    "  Schwab International Equity ETF (SCHF)      2,100\n\n"
    "Corporate Bonds (Held-to-Maturity):\n"
    "  Amazon.com Inc., 4.05%, 12/01/2028          2,500\n"
    "  Bank of America, 4.25%, 10/22/2029          1,730\n"
    "  Berkshire Hathaway, 3.85%, 03/15/2028       1,500\n"
    "  Coca-Cola Co., 3.45%, 09/01/2028            1,500\n"
    "    Total long-term investments              $18,330",

    "FAIR VALUE MEASUREMENTS\n\n"
    "The following table presents the Company's financial instruments measured at fair value\n"
    "on a recurring basis, categorized by level of the fair value hierarchy:\n\n"
    "                              Level 1    Level 2    Level 3    Total\n"
    "U.S. Treasury Securities     $ 8,140          -          -   $ 8,140\n"
    "Corporate Bonds                     -   $15,230          -    15,230\n"
    "Equity Securities             11,100          -          -    11,100\n"
    "  Total                      $19,240   $15,230          -   $34,470\n\n"
    "Transfers between levels: None during 2025.",

    "INVESTMENT INCOME AND GAINS/LOSSES\n\n"
    "For the Year Ended December 31, 2025 (in thousands):\n\n"
    "  Interest income from investments            $ 1,842\n"
    "  Dividend income                                 418\n"
    "  Net realized gains on sales                     215\n"
    "  Net unrealized gains on equity securities        315\n"
    "    Total investment income                    $ 2,790\n\n"
    "Maturity Schedule of Debt Securities:\n"
    "  Due within 1 year                           $ 8,140\n"
    "  Due in 1-3 years                              7,500\n"
    "  Due in 3-5 years                              5,730\n"
    "    Total debt securities                     $21,370",
]

INTERNAL_CONTROL_CONTENT = [
    "REPORT ON INTERNAL CONTROL OVER FINANCIAL REPORTING\n\n"
    "Management's Report on Internal Control\n\n"
    "The management of Meridian Holdings Inc. is responsible for establishing and maintaining "
    "adequate internal control over financial reporting. Internal control over financial reporting "
    "is a process designed by, or under the supervision of, the Company's principal executive and "
    "principal financial officers to provide reasonable assurance regarding the reliability of "
    "financial reporting and the preparation of financial statements for external purposes in "
    "accordance with generally accepted accounting principles.",

    "Assessment of Internal Control\n\n"
    "Management assessed the effectiveness of the Company's internal control over financial "
    "reporting as of December 31, 2025, based on the criteria established in Internal Control - "
    "Integrated Framework (2013) issued by the Committee of Sponsoring Organizations of the "
    "Treadway Commission (COSO).\n\n"
    "Based on this assessment, management has concluded that the Company's internal control "
    "over financial reporting was effective as of December 31, 2025.",

    "Key Control Activities Tested\n\n"
    "1. Revenue Recognition Controls\n"
    "   - Automated contract review and approval workflow\n"
    "   - Segregation of duties between sales and accounting\n"
    "   - Monthly revenue reconciliation procedures\n"
    "   - Quarterly revenue cut-off testing\n\n"
    "2. Financial Close Process Controls\n"
    "   - Standardized journal entry approval process\n"
    "   - Monthly account reconciliation procedures\n"
    "   - Management review of significant estimates\n"
    "   - Intercompany elimination procedures",

    "3. IT General Controls\n"
    "   - Access management and user provisioning\n"
    "   - Change management for financial systems\n"
    "   - Data backup and recovery procedures\n"
    "   - Security monitoring and incident response\n\n"
    "4. Procurement and Disbursement Controls\n"
    "   - Purchase order approval limits\n"
    "   - Three-way matching (PO, receipt, invoice)\n"
    "   - Vendor master file maintenance\n"
    "   - Segregation of duties in payment processing",

    "Deficiencies and Remediation\n\n"
    "During the assessment period, no material weaknesses were identified. The following "
    "significant deficiency was identified and remediated:\n\n"
    "SD-2025-01: Inventory Count Procedures\n"
    "  Nature: Inconsistent application of cycle count procedures at the\n"
    "          Portland manufacturing facility during Q2 2025.\n"
    "  Impact: Potential for minor inventory discrepancies.\n"
    "  Remediation: Enhanced training program implemented in Q3 2025;\n"
    "               additional supervisory oversight established.\n"
    "  Status: Remediated as of September 30, 2025.",
]

SUPPLEMENTARY_CONTENT = [
    "SUPPLEMENTARY INFORMATION\n\n"
    "Quarterly Financial Data (Unaudited)\n(In thousands, except per share data)\n\n"
    "                          Q1 2025    Q2 2025    Q3 2025    Q4 2025\n"
    "Revenue                   $68,412    $71,843    $72,518    $74,659\n"
    "Gross profit               28,124     29,642     29,918     30,833\n"
    "Net income                  3,842      4,218      4,312      4,520\n"
    "EPS - basic                $ 0.03     $ 0.03     $ 0.03     $ 0.03\n"
    "EPS - diluted              $ 0.03     $ 0.03     $ 0.03     $ 0.03",

    "Five-Year Financial Summary\n(In thousands)\n\n"
    "                    2025       2024       2023       2022       2021\n"
    "Revenue          $287,432   $265,218   $248,910   $232,415   $218,752\n"
    "Operating income   25,104     22,318     19,842     17,125     15,480\n"
    "Net income         16,892     15,218     13,412     11,842     10,518\n"
    "Total assets      333,508    296,477    278,215    261,830    245,612\n"
    "Long-term debt     72,340     78,590     82,140     85,000     88,250\n"
    "Dividends/share  $   0.40   $   0.38   $   0.36   $   0.34   $   0.32",

    "Revenue by Geographic Region\n(In thousands)\n\n"
    "                        2025       2024       % Change\n"
    "North America        $198,412   $185,218      +7.1%\n"
    "Europe                 52,318     46,842     +11.7%\n"
    "Asia-Pacific           28,410     25,842      +9.9%\n"
    "Rest of World           8,292      7,316     +13.3%\n"
    "  Total              $287,432   $265,218      +8.4%",
]

MANAGEMENT_LETTER_CONTENT = [
    "MANAGEMENT LETTER\n\n"
    "March 15, 2026\n\n"
    "Board of Directors\nMeridian Holdings Inc.\n"
    "200 South Wacker Drive, Suite 3500\nChicago, IL 60606\n\n"
    "Dear Members of the Board:\n\n"
    "In planning and performing our audit of the financial statements of Meridian Holdings Inc. "
    "for the year ended December 31, 2025, we considered the Company's internal control over "
    "financial reporting as a basis for designing audit procedures. The following observations "
    "and recommendations are offered for management's consideration.",

    "OBSERVATION 1: Accounts Receivable Aging\n\n"
    "During our testing, we noted that approximately $2.3 million (7.5%) of trade receivables "
    "were past due by more than 90 days as of December 31, 2025, compared to $1.8 million (7.1%) "
    "in the prior year.\n\n"
    "Recommendation: We recommend that management enhance collection procedures for aged "
    "receivables and consider more frequent credit reviews for customers with deteriorating "
    "payment patterns.\n\n"
    "Management Response: Management acknowledges this observation and has implemented enhanced "
    "collection procedures effective January 2026, including automated reminder systems.",

    "OBSERVATION 2: IT Security Improvements\n\n"
    "While the Company maintains adequate IT security controls, we identified opportunities "
    "to further strengthen the cybersecurity posture:\n\n"
    "  a) Multi-factor authentication should be extended to all administrative accounts\n"
    "  b) Periodic penetration testing frequency should increase to quarterly\n"
    "  c) Employee security awareness training completion should be tracked more rigorously\n\n"
    "Management Response: Management has budgeted $1.2 million for cybersecurity enhancements "
    "in fiscal year 2026, including the items noted above.",

    "OBSERVATION 3: Lease Accounting Compliance\n\n"
    "The Company has made significant progress in implementing ASC 842 lease accounting. "
    "We recommend continued investment in lease management software to handle the growing "
    "portfolio of operating and finance leases across all business segments.\n\n"
    "We appreciate the cooperation and assistance of the management team during our audit.\n\n"
    "Sincerely,\n\n"
    "Grant Thornton LLP\n"
    "Chicago, Illinois",
]


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    page_count = 0

    for section in AUDIT_SECTIONS:
        title = section["title"]
        target_pages = section["pages"]

        # Determine content for this section
        if section["content"] is not None:
            contents = section["content"]
        elif title == "NOTES TO CONSOLIDATED FINANCIAL STATEMENTS":
            contents = NOTES_CONTENT
        elif title == "SCHEDULE OF INVESTMENTS":
            contents = INVESTMENT_CONTENT
        elif title == "INTERNAL CONTROL ASSESSMENT":
            contents = INTERNAL_CONTROL_CONTENT
        elif title == "SUPPLEMENTARY INFORMATION":
            contents = SUPPLEMENTARY_CONTENT
        elif title == "MANAGEMENT LETTER":
            contents = MANAGEMENT_LETTER_CONTENT
        else:
            contents = [f"{title}\n\nContent for this section."]

        # Distribute content across target pages
        pages_created = 0
        content_idx = 0

        while pages_created < target_pages:
            page = doc.new_page(width=612, height=792)  # Letter size
            page_count += 1

            # Header
            page.insert_text(
                pymupdf.Point(72, 50),
                "MERIDIAN HOLDINGS INC.",
                fontsize=8,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )
            page.insert_text(
                pymupdf.Point(72, 62),
                title,
                fontsize=8,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )

            # Separator line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 68), pymupdf.Point(540, 68))
            shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
            shape.commit()

            # Body content
            if content_idx < len(contents):
                text = contents[content_idx]
                content_idx += 1
            else:
                # Generate filler content for remaining pages
                text = self_generate_filler(title, pages_created, target_pages)

            rect = pymupdf.Rect(72, 80, 540, 740)
            page.insert_textbox(
                rect,
                text,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

            # Footer line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 750), pymupdf.Point(540, 750))
            shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
            shape.commit()

            # Page number footer (centered)
            page.insert_text(
                pymupdf.Point(290, 770),
                str(page_count),
                fontsize=8,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )

            pages_created += 1

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_count}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


def self_generate_filler(section_title, page_idx, total_pages):
    """Generate realistic filler content for remaining pages in a section."""
    fillers = {
        "NOTES TO CONSOLIDATED FINANCIAL STATEMENTS": [
            "Note (continued)\n\n"
            "The Company evaluates its financial instruments at fair value on a recurring basis. "
            "Level 1 inputs are quoted prices in active markets. Level 2 inputs include quoted prices "
            "for similar instruments, interest rates, and credit spreads. Level 3 inputs are unobservable "
            "inputs based on the Company's assumptions.\n\n"
            "The Company's derivative instruments are primarily used to hedge foreign currency exposure "
            "related to forecasted intercompany transactions. The notional amount of outstanding foreign "
            "currency forward contracts was $12,840 thousand as of December 31, 2025.\n\n"
            "Concentration Risk: Financial instruments that potentially subject the Company to concentrations "
            "of credit risk consist primarily of cash equivalents, short-term investments, and accounts "
            "receivable. The Company maintains its cash deposits with high-quality financial institutions "
            "and limits concentration of credit risk.",

            "Revenue Disaggregation (continued)\n\n"
            "The following table disaggregates revenue by major product/service category:\n\n"
            "  Software licensing            $  68,412\n"
            "  Cloud and SaaS services          42,318\n"
            "  Technology consulting             31,988\n"
            "  Industrial equipment              52,418\n"
            "  Maintenance and spare parts       45,796\n"
            "  Professional consulting           28,500\n"
            "  Training and education            18,000\n"
            "    Total revenue                 $287,432\n\n"
            "Remaining performance obligations as of December 31, 2025: $98,400 thousand\n"
            "Expected to be recognized within 1 year: 68%\n"
            "Expected to be recognized in 1-3 years: 32%",

            "Business Combinations and Acquisitions\n\n"
            "On August 15, 2024, the Company acquired NovaTech Solutions, a provider of enterprise "
            "resource planning (ERP) software, for $42,500 thousand in cash.\n\n"
            "Purchase price allocation (in thousands):\n"
            "  Cash and equivalents              $ 3,218\n"
            "  Accounts receivable                  5,412\n"
            "  Technology assets                   12,800\n"
            "  Customer relationships              15,400\n"
            "  Goodwill                            14,218\n"
            "  Other assets                         2,452\n"
            "  Assumed liabilities                (11,000)\n"
            "    Total purchase price             $42,500",

            "Pension and Post-Retirement Benefits\n\n"
            "The Company sponsors a defined benefit pension plan covering substantially all employees "
            "hired before January 1, 2015. The plan was frozen to new participants effective that date.\n\n"
            "Components of net periodic pension cost:\n"
            "  Service cost                       $    812\n"
            "  Interest cost                         2,418\n"
            "  Expected return on plan assets        (3,125)\n"
            "  Amortization of prior service cost       165\n"
            "  Recognized actuarial loss                 480\n"
            "    Net periodic pension cost         $    750\n\n"
            "Projected benefit obligation           $58,420\n"
            "Fair value of plan assets               52,180\n"
            "  Funded status (underfunded)          $(6,240)",
        ],
        "SCHEDULE OF INVESTMENTS": [
            "Investment Portfolio Details (continued)\n\n"
            "Municipal Bonds:\n"
            "  State of Illinois GO, 3.85%, 2028       $ 1,200\n"
            "  City of Chicago Rev, 4.10%, 2029            850\n"
            "  Cook County GO, 3.75%, 2027                 650\n\n"
            "Money Market Funds:\n"
            "  Vanguard Prime Money Market                3,218\n"
            "  Fidelity Government Money Market           2,450\n\n"
            "Investment Policy: The Company's investment policy limits exposure to any single "
            "issuer (other than U.S. government securities) to 5% of total portfolio value. "
            "Maximum portfolio duration is 3 years for short-term investments.",
        ],
        "INTERNAL CONTROL ASSESSMENT": [
            "Testing Methodology and Scope\n\n"
            "The internal control assessment covered the following key processes:\n\n"
            "  Process                        Controls Tested    Deficiencies Found\n"
            "  Revenue cycle                        42                  0\n"
            "  Procurement/Payables                 38                  0\n"
            "  Payroll and HR                       25                  0\n"
            "  Treasury and investments             18                  0\n"
            "  Financial reporting/close            35                  1\n"
            "  IT general controls                  28                  0\n"
            "  Tax compliance                       15                  0\n"
            "    Total                             201                  1\n\n"
            "Sampling methodology: Statistical sampling with 95% confidence level, using a "
            "tolerable deviation rate of 5% for key controls.",
        ],
        "SUPPLEMENTARY INFORMATION": [
            "Employee and Compensation Data\n\n"
            "Headcount by segment as of December 31, 2025:\n"
            "  Technology Solutions         1,842\n"
            "  Industrial Products          1,215\n"
            "  Professional Services          628\n"
            "  Corporate                       315\n"
            "    Total employees             4,000\n\n"
            "Average compensation and benefits per employee: $87,500\n"
            "Total compensation and benefits expense: $350,000 thousand\n"
            "Voluntary turnover rate: 12.8% (industry average: 15.2%)",
        ],
        "MANAGEMENT LETTER": [
            "OBSERVATION 4: Tax Compliance Enhancements\n\n"
            "We recommend that the Company evaluate its transfer pricing documentation "
            "to ensure compliance with recent OECD guidelines and local tax authority requirements "
            "in all jurisdictions where the Company operates.\n\n"
            "Management Response: The Company has engaged an external tax advisory firm to conduct "
            "a comprehensive transfer pricing study, expected to be completed by Q2 2026.\n\n"
            "We wish to express our appreciation for the courtesy extended to us during our "
            "engagement and look forward to continued service.\n\n"
            "This communication is intended solely for the information and use of the Board of "
            "Directors, Audit Committee, and management of Meridian Holdings Inc.",
        ],
    }

    section_fillers = fillers.get(section_title, [])
    if section_fillers:
        return section_fillers[page_idx % len(section_fillers)]

    return (
        f"{section_title} (continued)\n\n"
        f"Additional supporting documentation and schedules for the audit period ended "
        f"December 31, 2025. This section contains supplementary details, cross-references, "
        f"and supporting calculations for the figures presented in the primary financial statements.\n\n"
        f"All amounts are presented in thousands of U.S. dollars unless otherwise stated. "
        f"Figures have been rounded to the nearest thousand."
    )


create_initial()
