"""
Initial Setup: Create a 25-page corporate governance PDF with 18 email addresses
Task ID: pdf_legal_041
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf


WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_041'
OUTPUT_DIR = f'{WORKDIR}/legal/corp'
OUTPUT = f'{OUTPUT_DIR}/governance_docs.pdf'


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


# 18 email addresses to scatter across 25 pages
EMAILS = [
    "j.anderson@nexacorp.com",
    "sarah.chen@nexacorp.com",
    "m.rodriguez@nexacorp.com",
    "david.kim@nexacorp.com",
    "l.thompson@nexacorp.com",
    "r.patel@nexacorp.com",
    "compliance@nexacorp.com",
    "board.secretary@nexacorp.com",
    "a.williams@nexacorp.com",
    "k.nakamura@nexacorp.com",
    "e.okonkwo@nexacorp.com",
    "p.martinez@nexacorp.com",
    "investor.relations@nexacorp.com",
    "legal.affairs@nexacorp.com",
    "c.dubois@nexacorp.com",
    "h.schmidt@nexacorp.com",
    "governance@nexacorp.com",
    "t.brooks@nexacorp.com",
]

# Corporate governance document content — 25 pages of realistic legal text
PAGES = [
    # Page 1: Title page
    {
        "title": "NEXACORP INDUSTRIES, INC.",
        "subtitle": "Corporate Governance Guidelines",
        "body": (
            "Adopted by the Board of Directors\n"
            "Effective Date: January 15, 2025\n"
            "Last Amended: March 1, 2025\n\n"
            "Prepared by the Office of the Corporate Secretary\n"
            f"Contact: {EMAILS[7]}\n\n"
            "CONFIDENTIAL — FOR INTERNAL DISTRIBUTION ONLY\n\n"
            "NexaCorp Industries, Inc.\n"
            "1200 Innovation Drive, Suite 4500\n"
            "San Francisco, CA 94105\n"
            "United States of America"
        ),
    },
    # Page 2: Table of Contents
    {
        "title": "TABLE OF CONTENTS",
        "body": (
            "1. Role of the Board of Directors .......................... 3\n"
            "2. Board Composition and Qualifications ................... 4\n"
            "3. Director Independence Standards ........................ 5\n"
            "4. Board Leadership Structure ............................. 6\n"
            "5. Board Meetings and Attendance .......................... 7\n"
            "6. Board Committees ...................................... 8\n"
            "7. Audit Committee Charter ............................... 9\n"
            "8. Compensation Committee Charter ........................ 10\n"
            "9. Nominating and Governance Committee ................... 11\n"
            "10. Risk Oversight Framework ............................. 12\n"
            "11. Code of Business Conduct and Ethics .................. 14\n"
            "12. Related Party Transactions Policy .................... 16\n"
            "13. Insider Trading Policy ............................... 17\n"
            "14. Director Compensation ................................ 18\n"
            "15. Stock Ownership Guidelines ........................... 19\n"
            "16. Succession Planning .................................. 20\n"
            "17. Shareholder Engagement ............................... 21\n"
            "18. Environmental, Social, and Governance (ESG) .......... 22\n"
            "19. Whistleblower Protection ............................. 23\n"
            "20. Annual Review and Amendments ......................... 24\n"
            "Appendix A: Board Member Directory ....................... 25\n"
        ),
    },
    # Page 3: Role of the Board
    {
        "title": "1. ROLE OF THE BOARD OF DIRECTORS",
        "body": (
            "The Board of Directors of NexaCorp Industries, Inc. (the 'Company') is elected by "
            "stockholders to oversee management and to ensure that the long-term interests of "
            "stockholders are being served. The Board is responsible for the overall governance of "
            "the Company, including strategic direction, risk oversight, and management accountability.\n\n"
            "The Board shall:\n\n"
            "(a) Review and approve the Company's strategic plan and annual operating budget;\n"
            "(b) Select, evaluate, and compensate the Chief Executive Officer;\n"
            "(c) Oversee succession planning for senior management positions;\n"
            "(d) Review and approve major corporate actions and transactions;\n"
            "(e) Monitor the Company's financial performance and integrity of financial reporting;\n"
            "(f) Ensure compliance with applicable laws and regulations;\n"
            "(g) Oversee the Company's risk management framework.\n\n"
            f"For questions regarding Board responsibilities, contact the General Counsel, "
            f"James Anderson, at {EMAILS[0]}."
        ),
    },
    # Page 4: Board Composition
    {
        "title": "2. BOARD COMPOSITION AND QUALIFICATIONS",
        "body": (
            "The Board shall consist of not fewer than seven (7) and not more than thirteen (13) "
            "members, as determined by the Board from time to time. A majority of the Board shall "
            "consist of independent directors as defined by the applicable listing standards of the "
            "New York Stock Exchange and Securities and Exchange Commission rules.\n\n"
            "Director Qualifications:\n\n"
            "The Nominating and Governance Committee is responsible for identifying and recommending "
            "director candidates. In evaluating candidates, the Committee shall consider:\n\n"
            "- Professional experience and expertise relevant to the Company's business\n"
            "- Integrity and highest ethical standards\n"
            "- Sound business judgment\n"
            "- Diversity of background, experience, and perspective\n"
            "- Ability to devote sufficient time and attention to Board duties\n"
            "- Independence from management and the Company\n\n"
            f"Nominations may be submitted to Sarah Chen, Chief Human Resources Officer, "
            f"at {EMAILS[1]}."
        ),
    },
    # Page 5: Independence Standards
    {
        "title": "3. DIRECTOR INDEPENDENCE STANDARDS",
        "body": (
            "The Board has adopted categorical standards to assist in determining director "
            "independence. A director shall be considered independent if the Board affirmatively "
            "determines that the director has no material relationship with the Company.\n\n"
            "A director shall NOT be considered independent if:\n\n"
            "(i) The director is, or has been within the last three years, an employee of the "
            "Company, or an immediate family member is, or has been within the last three years, "
            "an executive officer of the Company;\n\n"
            "(ii) The director has received, or has an immediate family member who has received, "
            "during any twelve-month period within the last three years, more than $120,000 in "
            "direct compensation from the Company;\n\n"
            "(iii) The director is a current partner or employee of a firm that is the Company's "
            "internal or external auditor;\n\n"
            "(iv) The director is, or has been within the last three years, employed as an "
            "executive officer of another company where any of the present executive officers of "
            "NexaCorp serves or served on that company's compensation committee.\n\n"
            "The Board shall annually review all commercial, charitable, consulting, family, and "
            "other relationships of each director."
        ),
    },
    # Page 6: Board Leadership
    {
        "title": "4. BOARD LEADERSHIP STRUCTURE",
        "body": (
            "The Board shall annually evaluate its leadership structure and determine whether to "
            "combine or separate the roles of Chairman of the Board and Chief Executive Officer.\n\n"
            "If the Chairman is not an independent director, the Board shall appoint a Lead "
            "Independent Director with the following responsibilities:\n\n"
            "- Preside at all meetings of the Board at which the Chairman is not present;\n"
            "- Call meetings of the independent directors;\n"
            "- Serve as principal liaison between the Chairman and the independent directors;\n"
            "- Approve information sent to the Board;\n"
            "- Approve meeting agendas and schedules;\n"
            "- Be available for consultation and direct communication with major shareholders;\n"
            "- Perform such other duties as the Board may determine from time to time.\n\n"
            f"The current Lead Independent Director is Dr. Maria Rodriguez. She can be reached "
            f"at {EMAILS[2]} for any governance-related inquiries."
        ),
    },
    # Page 7: Board Meetings
    {
        "title": "5. BOARD MEETINGS AND ATTENDANCE",
        "body": (
            "Regular Meetings: The Board shall hold no fewer than four (4) regular meetings per "
            "year. Additional special meetings may be called by the Chairman, Lead Independent "
            "Director, or upon the written request of any two directors.\n\n"
            "Attendance: Each director is expected to attend at least 75% of all Board and "
            "assigned committee meetings during each fiscal year. A director who fails to meet "
            "this attendance requirement shall receive written notice from the Nominating and "
            "Governance Committee.\n\n"
            "Executive Sessions: The independent directors shall meet in executive session without "
            "management present at each regularly scheduled Board meeting. The Lead Independent "
            "Director shall preside at these sessions.\n\n"
            "Meeting Materials: Directors shall receive meeting materials at least five (5) "
            "business days in advance of regular meetings. Emergency materials may be distributed "
            "with shorter notice with the approval of the Chairman or Lead Independent Director.\n\n"
            f"Meeting logistics are coordinated by David Kim, Executive Assistant to the Board, "
            f"at {EMAILS[3]}."
        ),
    },
    # Page 8: Board Committees
    {
        "title": "6. BOARD COMMITTEES",
        "body": (
            "The Board has established the following standing committees:\n\n"
            "1. Audit Committee\n"
            "2. Compensation Committee\n"
            "3. Nominating and Corporate Governance Committee\n"
            "4. Risk Committee\n"
            "5. Technology and Innovation Committee\n\n"
            "Each committee shall operate under a written charter approved by the Board. "
            "Committee charters shall be reviewed annually and updated as necessary.\n\n"
            "Committee Composition Requirements:\n\n"
            "- Each standing committee shall consist of at least three (3) independent directors\n"
            "- Committee members and chairs are appointed annually by the Board\n"
            "- The Audit Committee must include at least one 'financial expert' as defined by SEC rules\n"
            "- No director may serve on more than three standing committees simultaneously\n\n"
            f"For committee assignment inquiries, contact Lisa Thompson, Deputy Corporate Secretary, "
            f"at {EMAILS[4]}."
        ),
    },
    # Page 9: Audit Committee
    {
        "title": "7. AUDIT COMMITTEE CHARTER",
        "body": (
            "Purpose: The Audit Committee assists the Board in fulfilling its oversight "
            "responsibilities with respect to:\n\n"
            "(a) The integrity of the Company's financial statements;\n"
            "(b) The Company's compliance with legal and regulatory requirements;\n"
            "(c) The qualifications, independence, and performance of the Company's independent "
            "auditor;\n"
            "(d) The performance of the Company's internal audit function;\n"
            "(e) The Company's systems of internal controls and disclosure controls.\n\n"
            "Membership: The Audit Committee shall consist of not fewer than three (3) members of "
            "the Board, all of whom shall be independent and financially literate. At least one "
            "member shall qualify as an 'audit committee financial expert.'\n\n"
            "Authority: The Audit Committee has sole authority to:\n"
            "- Appoint, compensate, and oversee the independent auditor\n"
            "- Pre-approve all audit and non-audit services\n"
            "- Retain independent counsel, accountants, or other advisors\n\n"
            f"The Audit Committee Chair is Raj Patel. Submit audit concerns to {EMAILS[5]}."
        ),
    },
    # Page 10: Compensation Committee
    {
        "title": "8. COMPENSATION COMMITTEE CHARTER",
        "body": (
            "Purpose: The Compensation Committee is responsible for overseeing the Company's "
            "compensation philosophy, policies, and programs, including:\n\n"
            "(a) Setting compensation for the CEO and other executive officers;\n"
            "(b) Reviewing and approving equity-based compensation plans;\n"
            "(c) Overseeing executive succession planning;\n"
            "(d) Producing the annual Compensation Committee Report for the proxy statement;\n"
            "(e) Reviewing and approving employment agreements, severance arrangements, and "
            "change-in-control agreements for executive officers.\n\n"
            "Compensation Philosophy:\n\n"
            "The Company's executive compensation program is designed to:\n"
            "- Attract, retain, and motivate talented executives\n"
            "- Align executive interests with stockholder interests\n"
            "- Provide competitive total compensation\n"
            "- Reward both short-term performance and long-term value creation\n"
            "- Discourage excessive risk-taking\n\n"
            f"The Compliance Department can be reached at {EMAILS[6]} for any compensation "
            f"policy questions."
        ),
    },
    # Page 11: Nominating and Governance Committee
    {
        "title": "9. NOMINATING AND CORPORATE GOVERNANCE COMMITTEE",
        "body": (
            "Purpose: The Nominating and Corporate Governance Committee is responsible for:\n\n"
            "(a) Identifying, recruiting, and recommending qualified candidates for Board membership;\n"
            "(b) Recommending the composition and structure of Board committees;\n"
            "(c) Developing and recommending corporate governance guidelines;\n"
            "(d) Overseeing annual Board and committee self-evaluations;\n"
            "(e) Reviewing director independence on an annual basis;\n"
            "(f) Monitoring developments in corporate governance best practices.\n\n"
            "Director Selection Process:\n\n"
            "The Committee evaluates potential candidates from multiple sources including:\n"
            "- Recommendations from current directors and management\n"
            "- Professional search firms\n"
            "- Stockholder nominations submitted in accordance with the Company's bylaws\n\n"
            "The Committee values diversity in its broadest sense and seeks candidates who "
            "bring a variety of complementary skills, backgrounds, and perspectives to the Board.\n\n"
            f"Director nominations and governance inquiries should be directed to Angela Williams "
            f"at {EMAILS[8]}."
        ),
    },
    # Page 12: Risk Oversight (part 1)
    {
        "title": "10. RISK OVERSIGHT FRAMEWORK",
        "body": (
            "The Board is responsible for overseeing the Company's enterprise risk management "
            "program. While the Board has overall responsibility for risk oversight, certain "
            "committees have been delegated specific risk categories:\n\n"
            "Audit Committee: Financial reporting risks, internal controls, cybersecurity risks\n"
            "Compensation Committee: Compensation-related risks\n"
            "Risk Committee: Operational, strategic, and regulatory risks\n"
            "Technology Committee: Technology and innovation risks\n\n"
            "Risk Identification and Assessment:\n\n"
            "Management shall maintain a comprehensive risk register that identifies, assesses, "
            "and prioritizes risks across the following categories:\n\n"
            "1. Strategic Risks: Market conditions, competitive landscape, M&A integration\n"
            "2. Financial Risks: Credit, liquidity, foreign exchange, interest rate\n"
            "3. Operational Risks: Supply chain, talent, IT infrastructure, business continuity\n"
            "4. Compliance Risks: Regulatory changes, data privacy, anti-corruption\n"
            "5. Reputational Risks: Brand integrity, ESG performance, media relations\n\n"
            f"Risk assessment reports should be submitted to Kenji Nakamura, Chief Risk Officer, "
            f"at {EMAILS[9]}."
        ),
    },
    # Page 13: Risk Oversight (part 2)
    {
        "title": "10. RISK OVERSIGHT FRAMEWORK (continued)",
        "body": (
            "Risk Reporting:\n\n"
            "The Chief Risk Officer shall provide quarterly reports to the Risk Committee "
            "covering:\n\n"
            "- Summary of top enterprise risks and trends\n"
            "- Status of risk mitigation efforts\n"
            "- Emerging risks and potential impact assessments\n"
            "- Key risk indicators and dashboards\n"
            "- Incident reports and lessons learned\n\n"
            "Cybersecurity Risk Oversight:\n\n"
            "Given the increasing threat landscape, the Board recognizes cybersecurity as a "
            "critical enterprise risk. The Audit Committee shall receive quarterly briefings "
            "from the Chief Information Security Officer on:\n\n"
            "- Cybersecurity program maturity assessment\n"
            "- Threat intelligence and incident response activities\n"
            "- Data protection and privacy compliance status\n"
            "- Third-party vendor risk management\n"
            "- Employee security awareness training metrics\n\n"
            "The full Board shall receive an annual comprehensive cybersecurity risk assessment."
        ),
    },
    # Page 14: Code of Conduct (part 1)
    {
        "title": "11. CODE OF BUSINESS CONDUCT AND ETHICS",
        "body": (
            "All directors, officers, and employees are required to comply with the Company's "
            "Code of Business Conduct and Ethics. The Code addresses, among other matters:\n\n"
            "Conflicts of Interest:\n"
            "Directors and officers must avoid any situation that creates or appears to create "
            "a conflict between personal interests and the interests of the Company. Any actual "
            "or potential conflict must be promptly disclosed to the General Counsel.\n\n"
            "Corporate Opportunities:\n"
            "Directors and officers may not take personal advantage of business opportunities "
            "that are discovered through the use of Company property, information, or position.\n\n"
            "Confidentiality:\n"
            "Directors and officers must maintain the confidentiality of non-public information "
            "about the Company and its business partners, except when disclosure is authorized "
            "or legally required.\n\n"
            "Fair Dealing:\n"
            "All employees shall deal fairly with customers, suppliers, competitors, and "
            "colleagues. No one should take unfair advantage through manipulation, concealment, "
            "abuse of privileged information, or misrepresentation.\n\n"
            f"Ethics-related inquiries may be directed to Emeka Okonkwo at {EMAILS[10]}."
        ),
    },
    # Page 15: Code of Conduct (part 2)
    {
        "title": "11. CODE OF BUSINESS CONDUCT AND ETHICS (continued)",
        "body": (
            "Anti-Corruption and Anti-Bribery:\n\n"
            "The Company is committed to complying with all applicable anti-corruption laws, "
            "including the U.S. Foreign Corrupt Practices Act (FCPA) and the UK Bribery Act. "
            "No director, officer, or employee shall:\n\n"
            "- Offer, promise, or provide anything of value to any government official, "
            "political party, or candidate for political office to obtain or retain business "
            "or secure an improper advantage;\n"
            "- Accept bribes, kickbacks, or other corrupt payments;\n"
            "- Use third parties to channel improper payments.\n\n"
            "Political Activities and Contributions:\n\n"
            "The Company does not make contributions to political candidates, parties, or "
            "campaigns. Employees are free to participate in the political process on their "
            "own time and at their own expense. The Company maintains a Political Action "
            "Committee (PAC) that is funded solely by voluntary employee contributions.\n\n"
            "Protection of Company Assets:\n\n"
            "All employees are responsible for protecting Company assets and ensuring their "
            "efficient use. Company assets include physical property, intellectual property, "
            "confidential information, and technology resources."
        ),
    },
    # Page 16: Related Party Transactions
    {
        "title": "12. RELATED PARTY TRANSACTIONS POLICY",
        "body": (
            "The Audit Committee is responsible for reviewing and approving or ratifying all "
            "related party transactions. A 'related party transaction' is any transaction, "
            "arrangement, or relationship in which:\n\n"
            "(a) The Company is a participant;\n"
            "(b) The amount involved exceeds $120,000; and\n"
            "(c) A related person has a direct or indirect material interest.\n\n"
            "Related persons include:\n"
            "- Directors, director nominees, and executive officers\n"
            "- Beneficial owners of more than 5% of the Company's common stock\n"
            "- Immediate family members of the above\n"
            "- Entities in which the above have a significant interest\n\n"
            "Review Standards:\n\n"
            "In evaluating a related party transaction, the Audit Committee shall consider:\n"
            "- Whether the transaction is on terms comparable to those obtainable in an "
            "arm's-length transaction with an unrelated third party\n"
            "- The related person's interest in the transaction\n"
            "- The purpose of, and potential benefits to the Company from, the transaction\n"
            "- The impact on the director's independence, if applicable\n\n"
            f"Related party transaction disclosures should be sent to Patricia Martinez, "
            f"VP of Internal Audit, at {EMAILS[11]}."
        ),
    },
    # Page 17: Insider Trading
    {
        "title": "13. INSIDER TRADING POLICY",
        "body": (
            "All directors, officers, and employees who have access to material non-public "
            "information about the Company are prohibited from trading in the Company's "
            "securities or tipping others.\n\n"
            "Trading Blackout Periods:\n\n"
            "Directors and designated insiders are subject to quarterly trading blackout periods "
            "beginning fourteen (14) calendar days before the end of each fiscal quarter and "
            "ending two (2) full trading days after the public release of quarterly earnings.\n\n"
            "Pre-Clearance Requirements:\n\n"
            "All Section 16 officers and directors must pre-clear all transactions in Company "
            "securities with the General Counsel or Deputy General Counsel. Pre-clearance "
            "requests should be submitted at least two (2) business days before the proposed "
            "transaction date.\n\n"
            "10b5-1 Trading Plans:\n\n"
            "Directors and officers are encouraged to adopt written trading plans that comply "
            "with SEC Rule 10b5-1 to facilitate orderly trading during open trading windows. "
            "All 10b5-1 plans must be pre-approved by the General Counsel.\n\n"
            f"For pre-clearance requests and insider trading policy questions, contact the "
            f"Investor Relations team at {EMAILS[12]}."
        ),
    },
    # Page 18: Director Compensation
    {
        "title": "14. DIRECTOR COMPENSATION",
        "body": (
            "Non-employee directors receive compensation for their Board service as follows:\n\n"
            "Annual Cash Retainer: $85,000\n"
            "Annual Equity Award: $150,000 (in restricted stock units)\n"
            "Lead Independent Director: Additional $30,000 annual retainer\n\n"
            "Committee Chair Retainers:\n"
            "  Audit Committee Chair: $25,000\n"
            "  Compensation Committee Chair: $20,000\n"
            "  Nominating and Governance Committee Chair: $15,000\n"
            "  Risk Committee Chair: $20,000\n"
            "  Technology and Innovation Committee Chair: $15,000\n\n"
            "Committee Member Retainers:\n"
            "  Audit Committee Member: $12,500\n"
            "  Compensation Committee Member: $10,000\n"
            "  Other Committee Member: $7,500\n\n"
            "Meeting Fees:\n"
            "  Board meetings beyond eight (8) per year: $2,000 per meeting\n"
            "  Committee meetings beyond six (6) per year: $1,500 per meeting\n\n"
            "Directors who are employees of the Company receive no additional compensation "
            "for their Board service.\n\n"
            f"Compensation inquiries: contact the Legal Affairs team at {EMAILS[13]}."
        ),
    },
    # Page 19: Stock Ownership Guidelines
    {
        "title": "15. STOCK OWNERSHIP GUIDELINES",
        "body": (
            "To align the interests of directors and executive officers with those of "
            "stockholders, the Board has adopted the following stock ownership guidelines:\n\n"
            "Directors:\n"
            "  Required Ownership: 5x annual cash retainer (currently $425,000)\n"
            "  Compliance Period: Five (5) years from date of appointment\n\n"
            "Executive Officers:\n"
            "  CEO: 6x base salary\n"
            "  Executive Vice Presidents: 3x base salary\n"
            "  Senior Vice Presidents: 2x base salary\n"
            "  Vice Presidents: 1x base salary\n"
            "  Compliance Period: Five (5) years from appointment to position\n\n"
            "Qualifying Holdings:\n"
            "- Shares owned directly or jointly with spouse\n"
            "- Shares held in trust for the benefit of the director/officer or family members\n"
            "- Unvested restricted stock and restricted stock units\n"
            "- Shares held through Company benefit plans (e.g., 401(k), ESPP)\n\n"
            "Stock options (vested or unvested) and unearned performance share units do not "
            "count toward meeting the ownership guidelines.\n\n"
            f"Stock ownership compliance tracking: contact Claire Dubois at {EMAILS[14]}."
        ),
    },
    # Page 20: Succession Planning
    {
        "title": "16. SUCCESSION PLANNING",
        "body": (
            "The Board recognizes the importance of effective leadership succession planning "
            "to ensure continuity and long-term success. The Board shall:\n\n"
            "(a) Review and evaluate the CEO succession plan at least annually in executive "
            "session;\n"
            "(b) Ensure that emergency succession procedures are in place for the CEO and "
            "other key senior executives;\n"
            "(c) Review the development plans for high-potential senior leaders;\n"
            "(d) Consider both internal and external candidates for CEO succession;\n"
            "(e) Oversee management's succession planning for other critical leadership roles.\n\n"
            "Emergency Succession:\n\n"
            "In the event of an unexpected vacancy in the CEO position, the Board has "
            "designated the following emergency succession order:\n"
            "1. Chief Operating Officer\n"
            "2. Chief Financial Officer\n"
            "3. General Counsel\n\n"
            "The designated successor shall serve as interim CEO until the Board completes "
            "its search for a permanent CEO.\n\n"
            f"Succession planning communications: contact Hans Schmidt, SVP Talent Management, "
            f"at {EMAILS[15]}."
        ),
    },
    # Page 21: Shareholder Engagement
    {
        "title": "17. SHAREHOLDER ENGAGEMENT",
        "body": (
            "The Board is committed to meaningful engagement with stockholders and values "
            "their input on governance, compensation, and strategy matters.\n\n"
            "Engagement Program:\n\n"
            "The Company maintains an active shareholder engagement program that includes:\n"
            "- Annual meeting presentations and Q&A sessions\n"
            "- Off-season governance roadshows with institutional investors\n"
            "- Regular communication through investor letters and webcasts\n"
            "- Prompt response to shareholder inquiries and proposals\n\n"
            "Communications with the Board:\n\n"
            "Stockholders may communicate directly with the Board, the Lead Independent "
            "Director, or any individual director by writing to:\n\n"
            "Board of Directors\n"
            "c/o Corporate Secretary\n"
            "NexaCorp Industries, Inc.\n"
            "1200 Innovation Drive, Suite 4500\n"
            "San Francisco, CA 94105\n\n"
            f"Electronic communications may be sent to the Corporate Governance team at "
            f"{EMAILS[16]}.\n\n"
            "All communications will be reviewed by the Corporate Secretary and forwarded "
            "to the appropriate director(s) unless they are deemed frivolous or otherwise "
            "not appropriate for Board review."
        ),
    },
    # Page 22: ESG
    {
        "title": "18. ENVIRONMENTAL, SOCIAL, AND GOVERNANCE (ESG)",
        "body": (
            "NexaCorp is committed to integrating environmental, social, and governance "
            "considerations into its business strategy and operations.\n\n"
            "Environmental Stewardship:\n"
            "- Carbon neutrality target by 2030 for Scope 1 and 2 emissions\n"
            "- 50% reduction in Scope 3 emissions by 2035\n"
            "- 100% renewable energy for all facilities by 2028\n"
            "- Zero waste to landfill by 2027\n\n"
            "Social Responsibility:\n"
            "- Diversity, Equity, and Inclusion (DEI) targets for all management levels\n"
            "- Living wage commitment for all employees and contracted workers\n"
            "- Community investment program ($10M annual target)\n"
            "- Supply chain human rights due diligence program\n\n"
            "Governance Excellence:\n"
            "- Board diversity: minimum 40% gender diverse; minimum 25% racially/ethnically diverse\n"
            "- Annual board and committee self-evaluations\n"
            "- Clawback policy for executive incentive compensation\n"
            "- Proxy access for qualifying shareholders\n\n"
            "The Technology and Innovation Committee provides oversight of ESG-related "
            "technology initiatives and data privacy matters."
        ),
    },
    # Page 23: Whistleblower Protection
    {
        "title": "19. WHISTLEBLOWER PROTECTION",
        "body": (
            "The Company encourages employees, officers, and directors to report suspected "
            "violations of law, regulation, or Company policy without fear of retaliation.\n\n"
            "Reporting Channels:\n\n"
            "1. Direct Supervisor or Department Manager\n"
            "2. Human Resources Department\n"
            "3. General Counsel or Legal Department\n"
            "4. Ethics Hotline: 1-800-555-ETHX (3849) — available 24/7, anonymous\n"
            "5. Online reporting portal: ethics.nexacorp.com\n\n"
            "Anti-Retaliation Policy:\n\n"
            "The Company strictly prohibits retaliation against any person who, in good faith:\n"
            "- Reports a suspected violation through any of the above channels\n"
            "- Participates in an investigation of a reported violation\n"
            "- Refuses to participate in activities believed to be illegal\n\n"
            "Retaliation includes termination, demotion, suspension, threats, harassment, "
            "or any other adverse action taken against a person for reporting a concern.\n\n"
            "Any person who believes they have been subjected to retaliation should immediately "
            f"report the matter to Terrence Brooks, VP of Ethics and Compliance, at {EMAILS[17]}."
        ),
    },
    # Page 24: Annual Review
    {
        "title": "20. ANNUAL REVIEW AND AMENDMENTS",
        "body": (
            "The Nominating and Corporate Governance Committee shall review these Corporate "
            "Governance Guidelines annually and recommend any proposed changes to the Board "
            "for approval.\n\n"
            "Amendment Process:\n\n"
            "These Guidelines may be amended by the Board at any time upon recommendation "
            "of the Nominating and Corporate Governance Committee. Amendments shall be "
            "disclosed to stockholders in accordance with applicable SEC and NYSE requirements.\n\n"
            "Annual Board Self-Evaluation:\n\n"
            "The Board shall conduct an annual self-evaluation to assess:\n"
            "- Overall Board effectiveness and performance\n"
            "- Quality of Board discussions and decision-making\n"
            "- Adequacy of information provided to the Board\n"
            "- Board composition, diversity, and skills matrix\n"
            "- Committee structure and effectiveness\n"
            "- Board-management dynamics and communication\n\n"
            "The evaluation process shall be overseen by the Nominating and Corporate "
            "Governance Committee, which may engage an independent third-party facilitator.\n\n"
            "Effective Date: These Corporate Governance Guidelines were adopted by the Board "
            "of Directors on January 15, 2025, and last amended on March 1, 2025."
        ),
    },
    # Page 25: Appendix - Board Member Directory
    {
        "title": "APPENDIX A: BOARD MEMBER DIRECTORY",
        "body": (
            "Current Board Members (as of March 2025):\n\n"
            "1. James Anderson, Chairman & CEO\n"
            "   Phone: (415) 555-0101\n\n"
            "2. Dr. Maria Rodriguez, Lead Independent Director\n"
            "   Phone: (415) 555-0102\n\n"
            "3. Raj Patel, Audit Committee Chair\n"
            "   Phone: (415) 555-0103\n\n"
            "4. Angela Williams, Nominating Committee Chair\n"
            "   Phone: (415) 555-0104\n\n"
            "5. Kenji Nakamura, Risk Committee Chair\n"
            "   Phone: (415) 555-0105\n\n"
            "6. Dr. Priya Sharma, Technology Committee Chair\n"
            "   Phone: (415) 555-0106\n\n"
            "7. Robert Chang, Compensation Committee Chair\n"
            "   Phone: (415) 555-0107\n\n"
            "8. Eleanor Washington, Director\n"
            "   Phone: (415) 555-0108\n\n"
            "9. Michael O'Brien, Director\n"
            "   Phone: (415) 555-0109\n\n"
            "10. Fatima Al-Rashid, Director\n"
            "   Phone: (415) 555-0110\n\n"
            "11. Thomas Eriksson, Director\n"
            "   Phone: (415) 555-0111\n\n"
            "For individual director email addresses, please contact the\n"
            "Corporate Secretary's office."
        ),
    },
]

def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    for i, page_data in enumerate(PAGES):
        page = doc.new_page(width=612, height=792)  # Letter size

        y = 72  # top margin

        # Draw title
        title = page_data.get("title", "")
        if title:
            fontname = "hebo"
            fontsize = 18 if i == 0 else 14
            page.insert_text(
                pymupdf.Point(72, y + fontsize),
                title,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0),
            )
            y += fontsize + 20

        # Draw subtitle if present
        subtitle = page_data.get("subtitle", "")
        if subtitle:
            page.insert_text(
                pymupdf.Point(72, y + 14),
                subtitle,
                fontsize=14,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
            )
            y += 30

        # Draw body text
        body = page_data.get("body", "")
        if body:
            rect = pymupdf.Rect(72, y, 540, 740)
            page.insert_textbox(
                rect,
                body,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

        # Page number at bottom
        if i > 0:
            page.insert_text(
                pymupdf.Point(296, 770),
                str(i + 1),
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

    # Set metadata
    doc.set_metadata({
        "title": "NexaCorp Industries - Corporate Governance Guidelines",
        "author": "NexaCorp Corporate Secretary",
        "subject": "Corporate Governance",
        "keywords": "governance, board, directors, NexaCorp",
        "creator": "NexaCorp Legal Department",
    })

    # Add table of contents bookmarks
    toc = [
        [1, "Title Page", 1],
        [1, "Table of Contents", 2],
        [1, "1. Role of the Board of Directors", 3],
        [1, "2. Board Composition and Qualifications", 4],
        [1, "3. Director Independence Standards", 5],
        [1, "4. Board Leadership Structure", 6],
        [1, "5. Board Meetings and Attendance", 7],
        [1, "6. Board Committees", 8],
        [1, "7. Audit Committee Charter", 9],
        [1, "8. Compensation Committee Charter", 10],
        [1, "9. Nominating and Governance Committee", 11],
        [1, "10. Risk Oversight Framework", 12],
        [1, "11. Code of Business Conduct and Ethics", 14],
        [1, "12. Related Party Transactions Policy", 16],
        [1, "13. Insider Trading Policy", 17],
        [1, "14. Director Compensation", 18],
        [1, "15. Stock Ownership Guidelines", 19],
        [1, "16. Succession Planning", 20],
        [1, "17. Shareholder Engagement", 21],
        [1, "18. ESG", 22],
        [1, "19. Whistleblower Protection", 23],
        [1, "20. Annual Review and Amendments", 24],
        [1, "Appendix A: Board Member Directory", 25],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify email count
    doc2 = pymupdf.open(OUTPUT)
    import re
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    all_emails = []
    for p in range(doc2.page_count):
        text = doc2[p].get_text()
        found = email_pattern.findall(text)
        all_emails.extend(found)
    doc2.close()
    print(f'Total pages: 25, Total email addresses found: {len(all_emails)}')
    for e in all_emails:
        print(f'  - {e}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
