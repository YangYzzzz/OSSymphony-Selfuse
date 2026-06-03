"""
Initial Setup: Create a 40-page court record PDF with no watermark or encryption.
Task ID: pdf_legal_095
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_095'
OUTPUT_DIR = f'{WORKDIR}/legal/sealed'
OUTPUT = f'{OUTPUT_DIR}/court_record.pdf'


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
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions: US Letter
    W, H = 612, 792

    # Court case metadata
    case_number = "2024-CV-03847"
    case_title = "State of California v. Meridian Technologies, Inc."
    court_name = "SUPERIOR COURT OF CALIFORNIA, COUNTY OF LOS ANGELES"
    judge_name = "Hon. Patricia M. Nakamura"
    plaintiff_counsel = "Rebecca L. Torres, Esq., Office of the Attorney General"
    defendant_counsel = "David K. Whitfield, Esq., Whitfield & Associates LLP"
    filing_date = "March 15, 2024"

    # Helper to add page header/footer
    def add_header_footer(page, page_num):
        # Header line
        page.insert_text(pymupdf.Point(72, 36), court_name, fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        page.insert_text(pymupdf.Point(72, 48), f"Case No. {case_number}", fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 54), pymupdf.Point(W - 72, 54))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()
        # Footer
        page.insert_text(pymupdf.Point(72, H - 30), "SEALED COURT RECORD - CONFIDENTIAL", fontsize=7, fontname="heit", color=(0.4, 0.4, 0.4))
        page.insert_text(pymupdf.Point(W - 120, H - 30), f"Page {page_num} of 40", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # ---- Page 1: Title / Cover Page ----
    page = doc.new_page(width=W, height=H)
    add_header_footer(page, 1)
    y = 120
    page.insert_text(pymupdf.Point(W/2 - 180, y), court_name, fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 40
    page.insert_text(pymupdf.Point(W/2 - 100, y), f"Case No. {case_number}", fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 50
    page.insert_text(pymupdf.Point(72, y), case_title, fontsize=16, fontname="tibo", color=(0, 0, 0))
    y += 40
    page.insert_text(pymupdf.Point(72, y), "SEALED COURT RECORD", fontsize=18, fontname="hebo", color=(0.5, 0, 0))
    y += 50
    info_lines = [
        f"Filed: {filing_date}",
        f"Presiding Judge: {judge_name}",
        f"Plaintiff's Counsel: {plaintiff_counsel}",
        f"Defendant's Counsel: {defendant_counsel}",
        "",
        "This document contains sealed proceedings and is not available for public inspection.",
        "Unauthorized disclosure may result in contempt of court.",
    ]
    for line in info_lines:
        page.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 18

    # ---- Pages 2-3: Table of Contents ----
    toc_entries = [
        ("I.", "Complaint and Initial Filing", 4),
        ("II.", "Defendant's Answer and Counterclaims", 7),
        ("III.", "Discovery Proceedings", 10),
        ("IV.", "Deposition of Sarah M. Chen, CFO", 13),
        ("V.", "Deposition of Robert J. Alvarez, VP Engineering", 16),
        ("VI.", "Expert Witness Report - Dr. Emily Park, Forensic Accounting", 19),
        ("VII.", "Expert Witness Report - Dr. James Liu, Data Security", 22),
        ("VIII.", "Motions and Rulings", 25),
        ("IX.", "Settlement Conference Notes", 28),
        ("X.", "Judicial Findings of Fact", 31),
        ("XI.", "Conclusions of Law", 34),
        ("XII.", "Final Order and Judgment", 37),
        ("XIII.", "Appendix: Exhibits Index", 39),
    ]
    for toc_page_num in [2, 3]:
        page = doc.new_page(width=W, height=H)
        add_header_footer(page, toc_page_num)
        y = 80
        if toc_page_num == 2:
            page.insert_text(pymupdf.Point(72, y), "TABLE OF CONTENTS", fontsize=14, fontname="hebo", color=(0, 0, 0))
            y += 30
            entries = toc_entries[:7]
        else:
            entries = toc_entries[7:]
        for num, title, pg in entries:
            page.insert_text(pymupdf.Point(72, y), f"{num}  {title}", fontsize=11, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(W - 100, y), str(pg), fontsize=11, fontname="helv", color=(0, 0, 0))
            y += 22

    # ---- Content generation helpers ----
    section_content = {
        "Complaint and Initial Filing": [
            "COMES NOW the Plaintiff, the People of the State of California, by and through the Office "
            "of the Attorney General, and files this Complaint against Defendant Meridian Technologies, Inc., "
            "alleging violations of California Business and Professions Code Sections 17200-17210 and "
            "California Civil Code Section 1750 et seq.",
            "",
            "PARTIES",
            "",
            "1. Plaintiff is the People of the State of California, represented by the Attorney General "
            "pursuant to Business and Professions Code Section 17204.",
            "",
            "2. Defendant Meridian Technologies, Inc. (hereinafter 'Meridian') is a Delaware corporation "
            "with its principal place of business at 4500 Innovation Drive, Suite 800, San Jose, California "
            "95134. Meridian is registered to do business in California and maintains offices in Los Angeles, "
            "San Francisco, and San Diego.",
            "",
            "JURISDICTION AND VENUE",
            "",
            "3. This Court has jurisdiction over this matter pursuant to California Code of Civil Procedure "
            "Section 410.10. Venue is proper in Los Angeles County pursuant to Code of Civil Procedure "
            "Section 395.5, as Defendant conducts substantial business activities in this county.",
            "",
            "FACTUAL ALLEGATIONS",
            "",
            "4. From January 2021 through December 2023, Meridian marketed and sold its 'SecureVault Pro' "
            "software product to approximately 12,500 California consumers and 340 business entities.",
            "",
            "5. Meridian represented that SecureVault Pro provided 'military-grade AES-256 encryption' for "
            "consumer data. Internal documents obtained during investigation reveal that the software utilized "
            "a deprecated DES encryption algorithm for data-at-rest, with AES-256 applied only to data in transit.",
            "",
            "6. Meridian's Chief Technology Officer, Mark R. Sullivan, was informed of this discrepancy via "
            "internal memorandum dated April 3, 2022 (Exhibit A-7), yet authorized continued marketing of the "
            "product without correction.",
            "",
            "7. As a direct result of Meridian's misrepresentations, consumers suffered actual damages estimated "
            "at $4.2 million, including costs of alternative security solutions, credit monitoring services, "
            "and business losses attributable to three documented data breaches affecting Meridian customers.",
        ],
        "Defendant's Answer and Counterclaims": [
            "DEFENDANT'S ANSWER TO COMPLAINT",
            "",
            "Defendant Meridian Technologies, Inc., by and through its attorneys, Whitfield & Associates LLP, "
            "hereby answers the Complaint as follows:",
            "",
            "FIRST DEFENSE",
            "",
            "8. The Complaint fails to state facts sufficient to constitute a cause of action against Defendant.",
            "",
            "SECOND DEFENSE",
            "",
            "9. Defendant denies each and every allegation of the Complaint except as specifically admitted herein.",
            "",
            "SPECIFIC RESPONSES",
            "",
            "10. Responding to Paragraph 4: Defendant admits that it marketed SecureVault Pro in California "
            "during the stated period. Defendant states that total California sales were approximately 11,800 "
            "individual licenses and 285 enterprise licenses, and denies the figures stated in the Complaint.",
            "",
            "11. Responding to Paragraph 5: Defendant denies that its marketing materials were misleading. "
            "The term 'military-grade encryption' is an industry-standard marketing phrase and was not "
            "intended as a specific technical specification. Defendant further states that its hybrid encryption "
            "approach (AES-256 for transit, DES for at-rest storage) met or exceeded industry standards for "
            "the product's price point at the time of sale.",
            "",
            "12. Responding to Paragraph 6: Defendant admits that an internal memorandum was circulated on "
            "the date specified. Defendant denies that the memorandum recommended discontinuation of marketing "
            "and states that the memorandum proposed a phased upgrade plan, which was subsequently implemented.",
            "",
            "COUNTERCLAIM",
            "",
            "13. Defendant counterclaims that the Attorney General's investigation caused irreparable harm to "
            "Defendant's business reputation, resulting in loss of $8.7 million in projected Q4 2023 revenue "
            "and the cancellation of three pending enterprise contracts valued at $2.1 million.",
        ],
        "Discovery Proceedings": [
            "DISCOVERY ORDER AND PROCEEDINGS",
            "",
            "Pursuant to the Court's Order dated May 1, 2024, the following discovery schedule is established:",
            "",
            "DOCUMENT PRODUCTION",
            "",
            "14. Defendant shall produce all internal communications, memoranda, and technical documentation "
            "relating to SecureVault Pro's encryption implementation from January 2020 through December 2023.",
            "",
            "15. The following document categories were produced and reviewed:",
            "    a. Internal email correspondence: 14,327 documents (Bates Nos. MER-001 through MER-14327)",
            "    b. Technical specifications: 89 documents (Bates Nos. MER-TS-001 through MER-TS-089)",
            "    c. Marketing materials: 234 documents (Bates Nos. MER-MK-001 through MER-MK-234)",
            "    d. Board meeting minutes: 12 documents (Bates Nos. MER-BM-001 through MER-BM-012)",
            "    e. Customer complaints: 1,847 records (Bates Nos. MER-CC-001 through MER-CC-1847)",
            "",
            "INTERROGATORIES",
            "",
            "16. Plaintiff served 25 interrogatories on Defendant. Defendant responded, with objections noted "
            "to Interrogatories 8, 12, 15, and 22. The Court sustained objections to Interrogatories 8 and 22, "
            "and overruled objections to Interrogatories 12 and 15.",
            "",
            "17. Key findings from discovery include:",
            "    a. Email from CTO Mark Sullivan to CEO Diana Reeves dated April 5, 2022, stating: "
            "'We need to accelerate the AES migration but current timeline is 18 months minimum.'",
            "    b. Engineering ticket #SEC-4471 documenting a known vulnerability in the DES implementation, "
            "filed June 12, 2022, with status 'deferred - resource constraints.'",
            "    c. Customer complaint analysis showing 847 complaints specifically mentioning encryption "
            "performance between March 2022 and November 2023.",
        ],
        "Deposition Transcript": [
            "DEPOSITION TRANSCRIPT",
            "",
            "Q: Please state your name and position for the record.",
            "A: My name is Sarah M. Chen. I serve as Chief Financial Officer of Meridian Technologies.",
            "",
            "Q: How long have you held that position?",
            "A: Since August 2019. Prior to that, I was VP of Finance from 2016 to 2019.",
            "",
            "Q: Ms. Chen, are you familiar with the revenue figures for SecureVault Pro?",
            "A: Yes. SecureVault Pro generated $47.3 million in total revenue from Q1 2021 through Q4 2023.",
            "",
            "Q: What was the breakdown by customer segment?",
            "A: Approximately 62% from enterprise clients and 38% from individual consumers. Enterprise "
            "contracts ranged from $15,000 to $450,000 annually, while consumer licenses were $79.99 per year.",
            "",
            "Q: Were you aware of any technical concerns about the encryption implementation?",
            "A: I was made aware in Q2 2022 that the engineering team had identified a need to upgrade "
            "certain encryption components. This was presented to me in the context of a budget request "
            "for $3.2 million to fund the migration project.",
            "",
            "Q: Did you approve that budget request?",
            "A: I recommended a phased approach. We approved $1.8 million for Phase 1, covering the "
            "enterprise product line, with Phase 2 for consumer products contingent on Q3 revenue targets.",
            "",
            "Q: Were Q3 revenue targets met?",
            "A: No. Q3 2022 revenue came in at $11.2 million against a target of $13.5 million, primarily "
            "due to increased competition from CloudShield and DataFortress entering our market segment.",
            "",
            "Q: So Phase 2 was not funded?",
            "A: Not immediately. Phase 2 was eventually approved in February 2023 and completed in "
            "September 2023.",
        ],
        "Expert Witness Report": [
            "EXPERT WITNESS REPORT",
            "",
            "Prepared by: Dr. Emily Park, CPA, CFF",
            "Forensic Accounting Specialist",
            "Park & Associates Consulting Group",
            "",
            "QUALIFICATIONS",
            "",
            "I have been retained by Plaintiff's counsel to provide expert analysis on the financial damages "
            "resulting from Defendant's alleged misrepresentations. I hold a Ph.D. in Accounting from Stanford "
            "University, am a Certified Public Accountant (California License #AC-78432), and hold the "
            "Certified in Financial Forensics credential from the AICPA.",
            "",
            "METHODOLOGY",
            "",
            "My analysis employed three complementary approaches:",
            "1. Direct consumer harm calculation based on price differential analysis",
            "2. Consequential damages assessment from documented security incidents",
            "3. Cost of remediation analysis for affected customers",
            "",
            "FINDINGS",
            "",
            "Consumer Price Differential: Based on competitive market analysis, the fair market value of "
            "software providing DES-level encryption (as actually delivered) would be approximately $34.99 "
            "per year, compared to the $79.99 charged. This represents a $45.00 per-license overcharge, "
            "totaling $531,000 across 11,800 individual California licenses.",
            "",
            "Enterprise Damages: Enterprise clients paid an average premium of 35% for advertised AES-256 "
            "encryption. Aggregate overpayment is estimated at $2.84 million across 285 enterprise contracts.",
            "",
            "Data Breach Costs: Three documented breaches (February 2023 incident affecting 2,400 users; "
            "June 2023 incident affecting 890 users; October 2023 incident affecting 4,100 users) resulted "
            "in quantifiable costs of $834,000 in credit monitoring, $290,000 in identity theft losses, "
            "and $1.47 million in business interruption costs.",
            "",
            "TOTAL ESTIMATED DAMAGES: $5,965,000",
        ],
        "Motions and Rulings": [
            "MOTIONS AND COURT RULINGS",
            "",
            "MOTION TO DISMISS (Filed June 15, 2024)",
            "",
            "Defendant moved to dismiss Counts II and III of the Complaint under Code of Civil Procedure "
            "Section 430.10(e), arguing that the Consumer Legal Remedies Act claims are time-barred under "
            "the three-year statute of limitations.",
            "",
            "RULING: Motion DENIED. The Court finds that the discovery rule applies, as consumers could not "
            "reasonably have discovered the encryption discrepancy without specialized technical knowledge. "
            "The limitations period commenced, at earliest, when the first data breach was publicly reported "
            "in February 2023.",
            "",
            "MOTION FOR CLASS CERTIFICATION (Filed August 8, 2024)",
            "",
            "Plaintiff moved for class certification of all California purchasers of SecureVault Pro.",
            "",
            "RULING: Motion GRANTED IN PART. The Court certifies a class of individual California consumers "
            "who purchased SecureVault Pro between January 2021 and September 2023 (when the encryption "
            "upgrade was completed). The Court declines to certify enterprise purchasers as a class due to "
            "material differences in contract terms and negotiated warranties.",
            "",
            "MOTION TO COMPEL (Filed September 20, 2024)",
            "",
            "Plaintiff moved to compel production of Defendant's internal security audit reports.",
            "",
            "RULING: Motion GRANTED. Defendant's assertion of work product privilege is overruled as the "
            "reports were prepared in the ordinary course of business, not in anticipation of litigation.",
        ],
        "Settlement Conference": [
            "SETTLEMENT CONFERENCE NOTES",
            "",
            "Date: November 5, 2024",
            "Location: Chambers of Hon. Patricia M. Nakamura",
            "Present: All counsel of record; Diana Reeves (CEO, Meridian); Deputy AG Thomas Okafor",
            "",
            "CONFIDENTIAL - SETTLEMENT DISCUSSIONS",
            "",
            "1. The Court convened the parties for a mandatory settlement conference pursuant to Local Rule 3.25.",
            "",
            "2. Plaintiff presented a demand of $12.5 million in restitution and civil penalties, plus "
            "injunctive relief requiring Meridian to:",
            "   a. Implement AES-256 encryption across all product lines within 90 days",
            "   b. Retain an independent security auditor for 24 months",
            "   c. Provide free credit monitoring to all affected California customers for 36 months",
            "",
            "3. Defendant countered with an offer of $3.8 million in total payments, asserting that:",
            "   a. The encryption upgrade was already completed in September 2023",
            "   b. No systemic data breach was caused by the encryption implementation",
            "   c. Market conditions, not technical deficiencies, drove customer complaints",
            "",
            "4. After two rounds of mediated negotiation, the Court proposed a framework of $7.5 million "
            "in consumer restitution, $2.0 million in civil penalties, and modified injunctive terms.",
            "",
            "5. Defendant requested 14 days to consult with its Board of Directors.",
            "",
            "6. Conference adjourned at 4:47 PM. Next conference scheduled for November 19, 2024.",
        ],
        "Judicial Findings": [
            "JUDICIAL FINDINGS OF FACT",
            "",
            "Having considered all evidence presented, testimony of witnesses, expert reports, and arguments "
            "of counsel, the Court makes the following findings of fact:",
            "",
            "1. Meridian Technologies, Inc. sold SecureVault Pro software to California consumers and "
            "businesses from January 2021 through December 2023, generating $47.3 million in total revenue.",
            "",
            "2. Meridian's marketing materials, including its website, product packaging, and sales "
            "presentations, consistently represented that SecureVault Pro utilized 'military-grade AES-256 "
            "encryption' for all data protection functions.",
            "",
            "3. In fact, SecureVault Pro used AES-256 encryption only for data in transit. Data at rest "
            "was protected using the older DES algorithm, which provides substantially lower security.",
            "",
            "4. Meridian's CTO, Mark Sullivan, was informed of this discrepancy no later than April 3, 2022, "
            "via internal memorandum from Senior Engineer Lisa Huang (Exhibit A-7).",
            "",
            "5. Despite this knowledge, Meridian continued to market SecureVault Pro with unchanged encryption "
            "claims for an additional 17 months, until the AES-256 migration was completed in September 2023.",
            "",
            "6. The Court finds that Meridian's conduct constitutes unfair business practices under Business "
            "and Professions Code Section 17200 and deceptive advertising under Section 17500.",
            "",
            "7. Three data breaches affecting Meridian customers in 2023 were facilitated, in part, by "
            "the weaker DES encryption used for data at rest. The Court accepts Dr. Emily Park's damage "
            "estimate of $5,965,000 as supported by credible evidence.",
            "",
            "8. The Court finds that Meridian's conduct was willful and not the result of mere negligence, "
            "based on the April 2022 memorandum and subsequent decision to continue existing marketing.",
        ],
        "Conclusions of Law": [
            "CONCLUSIONS OF LAW",
            "",
            "Based on the foregoing Findings of Fact, the Court reaches the following Conclusions of Law:",
            "",
            "1. UNFAIR COMPETITION (Bus. & Prof. Code Section 17200): Meridian's practice of marketing "
            "SecureVault Pro as providing AES-256 encryption when it actually used DES for at-rest data "
            "constitutes an 'unfair' and 'fraudulent' business practice within the meaning of Section 17200.",
            "",
            "2. FALSE ADVERTISING (Bus. & Prof. Code Section 17500): Meridian's marketing claims regarding "
            "'military-grade AES-256 encryption' were false and misleading in a material respect, in violation "
            "of Section 17500.",
            "",
            "3. CONSUMER LEGAL REMEDIES ACT (Civ. Code Section 1770(a)(5) and (a)(7)): Meridian's conduct "
            "constitutes a representation that goods have characteristics and benefits they do not have, "
            "and a representation that goods are of a particular standard or quality when they are not.",
            "",
            "4. STANDING: The People of the State of California have standing to bring this action under "
            "Business and Professions Code Section 17204 and Civil Code Section 1781.",
            "",
            "5. DAMAGES: Plaintiff has established damages by a preponderance of the evidence. The Court "
            "awards restitution of $5,965,000 to affected consumers through a claims process to be "
            "administered as set forth in the Final Order.",
            "",
            "6. CIVIL PENALTIES: Under Business and Professions Code Section 17206, the Court imposes "
            "civil penalties of $2,500 per violation. Given the Court's finding of 12,085 affected "
            "California transactions, total civil penalties are assessed at $2,500,000, accounting for "
            "the Court's discretion under the statutory maximum.",
            "",
            "7. INJUNCTIVE RELIEF: The Court finds that injunctive relief is necessary and appropriate "
            "to prevent future violations.",
        ],
        "Final Order": [
            "FINAL ORDER AND JUDGMENT",
            "",
            "IT IS HEREBY ORDERED, ADJUDGED, AND DECREED as follows:",
            "",
            "1. RESTITUTION: Defendant Meridian Technologies, Inc. shall pay restitution in the amount of "
            "$5,965,000 to a Court-supervised restitution fund within 60 days of this Order.",
            "",
            "2. CIVIL PENALTIES: Defendant shall pay civil penalties in the amount of $2,500,000 to the "
            "State of California within 60 days of this Order.",
            "",
            "3. INJUNCTIVE RELIEF: Defendant is permanently enjoined from:",
            "   a. Making any representation regarding encryption standards unless such representation "
            "is accurate and verifiable at the time of publication;",
            "   b. Marketing any security product without annual third-party security audits;",
            "   c. Failing to disclose known security vulnerabilities to affected customers within 30 "
            "days of discovery.",
            "",
            "4. COMPLIANCE MONITORING: Defendant shall retain an independent security auditor, approved by "
            "the Court, to conduct quarterly security assessments for a period of 36 months from the date "
            "of this Order. Reports shall be filed with the Court under seal.",
            "",
            "5. CREDIT MONITORING: Defendant shall provide identity theft protection and credit monitoring "
            "services to all affected California customers for a period of 36 months at no cost.",
            "",
            "6. CLAIMS PROCESS: The Court appoints retired Judge Harold S. Yamamoto as Claims Administrator. "
            "The Claims Administrator shall develop and implement a streamlined process for affected consumers "
            "to submit claims against the restitution fund.",
            "",
            "7. REPORTING: Defendant shall file quarterly compliance reports with this Court for a period "
            "of 36 months, detailing its compliance with each provision of this Order.",
            "",
            "8. COSTS: Defendant shall pay Plaintiff's costs of suit in the amount of $387,500.",
            "",
            "SO ORDERED this 15th day of December 2024.",
            "",
            "______________________________",
            "Hon. Patricia M. Nakamura",
            "Judge of the Superior Court",
        ],
        "Exhibits Index": [
            "APPENDIX: EXHIBITS INDEX",
            "",
            "Exhibit A-1: SecureVault Pro Product Brochure (2021 Edition)",
            "Exhibit A-2: SecureVault Pro Website Screenshots (archived January 2022)",
            "Exhibit A-3: SecureVault Pro Technical Specification Sheet (Version 3.2)",
            "Exhibit A-4: Enterprise Sales Presentation (Q3 2021)",
            "Exhibit A-5: Email: Sullivan to Engineering Team re: Encryption Roadmap (Jan 15, 2022)",
            "Exhibit A-6: Engineering Ticket #SEC-4471: DES Vulnerability Report",
            "Exhibit A-7: Internal Memorandum: Huang to Sullivan re: Encryption Discrepancy (Apr 3, 2022)",
            "Exhibit A-8: Email: Sullivan to Reeves re: Encryption Migration Timeline (Apr 5, 2022)",
            "Exhibit A-9: Board Meeting Minutes (May 2022)",
            "Exhibit A-10: Phase 1 Migration Budget Approval (Q3 2022)",
            "Exhibit A-11: Phase 2 Migration Budget Approval (Feb 2023)",
            "Exhibit A-12: Data Breach Incident Report - February 2023",
            "Exhibit A-13: Data Breach Incident Report - June 2023",
            "Exhibit A-14: Data Breach Incident Report - October 2023",
            "Exhibit A-15: Customer Complaint Summary Report (Mar 2022 - Nov 2023)",
            "Exhibit B-1: Expert Report of Dr. Emily Park, CPA, CFF",
            "Exhibit B-2: Expert Report of Dr. James Liu, Ph.D., CISSP",
            "Exhibit B-3: Expert Report of Dr. Michael Torres, Economic Damages",
            "Exhibit C-1: Deposition Transcript - Sarah M. Chen, CFO",
            "Exhibit C-2: Deposition Transcript - Robert J. Alvarez, VP Engineering",
            "Exhibit C-3: Deposition Transcript - Mark R. Sullivan, CTO",
            "Exhibit C-4: Deposition Transcript - Lisa Huang, Senior Engineer",
            "Exhibit C-5: Deposition Transcript - Diana Reeves, CEO",
            "Exhibit D-1: Third-Party Security Audit Report (Norton CyberSec, 2023)",
            "Exhibit D-2: Competitive Encryption Standard Analysis",
            "Exhibit D-3: Industry Standard Reference Guide (NIST SP 800-175B)",
        ],
    }

    # Sections to page mapping
    sections = [
        ("I. COMPLAINT AND INITIAL FILING", "Complaint and Initial Filing", 4, 6),
        ("II. DEFENDANT'S ANSWER AND COUNTERCLAIMS", "Defendant's Answer and Counterclaims", 7, 9),
        ("III. DISCOVERY PROCEEDINGS", "Discovery Proceedings", 10, 12),
        ("IV. DEPOSITION OF SARAH M. CHEN, CFO", "Deposition Transcript", 13, 15),
        ("V. DEPOSITION OF ROBERT J. ALVAREZ, VP ENGINEERING", "Deposition Transcript", 16, 18),
        ("VI. EXPERT WITNESS REPORT - DR. EMILY PARK", "Expert Witness Report", 19, 21),
        ("VII. EXPERT WITNESS REPORT - DR. JAMES LIU", "Expert Witness Report", 22, 24),
        ("VIII. MOTIONS AND RULINGS", "Motions and Rulings", 25, 27),
        ("IX. SETTLEMENT CONFERENCE NOTES", "Settlement Conference", 28, 30),
        ("X. JUDICIAL FINDINGS OF FACT", "Judicial Findings", 31, 33),
        ("XI. CONCLUSIONS OF LAW", "Conclusions of Law", 34, 36),
        ("XII. FINAL ORDER AND JUDGMENT", "Final Order", 37, 38),
        ("XIII. APPENDIX: EXHIBITS INDEX", "Exhibits Index", 39, 40),
    ]

    for section_title, content_key, start_pg, end_pg in sections:
        content_lines = section_content[content_key]
        for pg_num in range(start_pg, end_pg + 1):
            page = doc.new_page(width=W, height=H)
            add_header_footer(page, pg_num)
            y = 80

            if pg_num == start_pg:
                # Section heading
                page.insert_text(pymupdf.Point(72, y), section_title, fontsize=13, fontname="hebo", color=(0, 0, 0))
                y += 30
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, y - 8), pymupdf.Point(W - 72, y - 8))
                shape.finish(color=(0, 0, 0), width=1)
                shape.commit()
                y += 10

            # Insert content lines with wrapping
            rect = pymupdf.Rect(72, y, W - 72, H - 60)
            # Calculate which portion of content to show on this page within the section
            page_offset = pg_num - start_pg
            total_pages = end_pg - start_pg + 1
            lines_per_page = len(content_lines) // total_pages + 1
            start_line = page_offset * lines_per_page
            end_line = min(start_line + lines_per_page, len(content_lines))
            page_text = "\n".join(content_lines[start_line:end_line])

            if page_text.strip():
                page.insert_textbox(rect, page_text, fontsize=10.5, fontname="helv",
                                    color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    doc.save(OUTPUT)
    doc.close()
    print(f"Initial file created: {OUTPUT}")
    print(f"Page count: 40")

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
