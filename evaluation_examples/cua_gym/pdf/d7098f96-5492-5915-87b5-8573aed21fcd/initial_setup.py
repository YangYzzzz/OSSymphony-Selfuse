"""
Initial Setup: Create a 150-page trial binder PDF with no bookmarks
Task ID: pdf_legal_026
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_026'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/trial_binder.pdf'

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
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    MARGIN = 72  # 1 inch
    TEXT_WIDTH = W - 2 * MARGIN

    # --- Section definitions for a realistic trial binder ---
    sections = [
        # (title, start_page_0indexed, end_page_0indexed_exclusive, subsections)
        ("PLEADINGS", 0, 29, [
            ("COMPLAINT", 0, 14,
             "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK\n\n"
             "GREENFIELD TECHNOLOGIES, INC.,\nPlaintiff,\n\nvs.\n\n"
             "NEXGEN SOLUTIONS GROUP, LLC,\nDefendant.\n\n"
             "Case No. 2024-CV-03847\n\n"
             "COMPLAINT FOR PATENT INFRINGEMENT,\nBREACH OF CONTRACT, AND MISAPPROPRIATION\nOF TRADE SECRETS\n\n"
             "Plaintiff Greenfield Technologies, Inc. (\"Greenfield\" or \"Plaintiff\"), by and through its "
             "undersigned attorneys, hereby files this Complaint against Nexgen Solutions Group, LLC "
             "(\"Nexgen\" or \"Defendant\") and alleges as follows:\n\n"
             "NATURE OF THE ACTION\n\n"
             "1. This is an action for patent infringement under 35 U.S.C. Section 271, breach of contract, "
             "and misappropriation of trade secrets under the Defend Trade Secrets Act, 18 U.S.C. Section 1836, "
             "arising from Defendant's unauthorized use of Plaintiff's proprietary cloud computing technology "
             "and related intellectual property.\n\n"
             "2. Plaintiff Greenfield is a Delaware corporation with its principal place of business at "
             "450 Innovation Drive, Suite 1200, New York, New York 10013. Greenfield is a leading provider "
             "of enterprise cloud infrastructure solutions, holding over forty-seven (47) patents related to "
             "distributed computing architectures, data synchronization protocols, and automated scaling "
             "technologies.\n\n"
             "3. Defendant Nexgen is a limited liability company organized under the laws of the State of "
             "California, with its principal place of business at 8800 Technology Boulevard, San Jose, "
             "California 95134. Upon information and belief, Nexgen develops and markets competing cloud "
             "computing products that incorporate Greenfield's patented technologies without authorization.\n\n"
             "JURISDICTION AND VENUE\n\n"
             "4. This Court has subject matter jurisdiction under 28 U.S.C. Section 1331 (federal question) "
             "and 28 U.S.C. Section 1338(a) (patent jurisdiction).\n\n"
             "5. This Court has personal jurisdiction over Defendant because Nexgen conducts substantial "
             "business within this judicial district, maintains offices at 125 Broadway, New York, New York "
             "10006, and has committed acts of infringement within this district.\n\n"
             "FACTUAL BACKGROUND\n\n"
             "6. Greenfield was founded in 2008 by Dr. Margaret Chen and Dr. Robert Yamamoto, both former "
             "researchers at MIT's Computer Science and Artificial Intelligence Laboratory. Since its founding, "
             "Greenfield has invested over $340 million in research and development of its proprietary cloud "
             "computing technologies.\n\n"
             "7. In March 2019, Greenfield and Nexgen entered into a Technology Licensing Agreement (the "
             "\"License Agreement\") pursuant to which Greenfield granted Nexgen a limited, non-exclusive "
             "license to use certain Greenfield APIs for integration purposes only. The License Agreement "
             "expressly prohibited Nexgen from reverse engineering, decompiling, or otherwise attempting to "
             "derive the source code of Greenfield's proprietary software.\n\n"
             "8. Beginning in approximately January 2023, Greenfield discovered that Nexgen had launched a "
             "new product line called \"CloudSync Pro\" that incorporated technology substantially identical "
             "to Greenfield's patented distributed synchronization protocol, described in U.S. Patent No. "
             "10,847,293 (the \"'293 Patent\").\n\n"
             "COUNT I - PATENT INFRINGEMENT\n\n"
             "9. Greenfield repeats and re-alleges each of the foregoing allegations as if fully set forth "
             "herein.\n\n"
             "10. Greenfield is the owner by assignment of the '293 Patent, entitled \"System and Method for "
             "Distributed Data Synchronization in Multi-Tenant Cloud Environments,\" which was duly and legally "
             "issued on November 10, 2020.\n\n"
             "COUNT II - BREACH OF CONTRACT\n\n"
             "15. Greenfield repeats and re-alleges each of the foregoing allegations.\n\n"
             "16. The License Agreement constitutes a valid and binding contract between Greenfield and Nexgen. "
             "Nexgen has materially breached the License Agreement by, inter alia, reverse engineering "
             "Greenfield's proprietary software and using derived technology in competing products.\n\n"
             "COUNT III - TRADE SECRET MISAPPROPRIATION\n\n"
             "20. Greenfield repeats and re-alleges each of the foregoing allegations.\n\n"
             "21. Greenfield's proprietary algorithms, source code, and technical specifications constitute "
             "trade secrets under the Defend Trade Secrets Act.\n\n"
             "PRAYER FOR RELIEF\n\n"
             "WHEREFORE, Plaintiff respectfully requests that this Court enter judgment in its favor and "
             "against Defendant as follows:\n\n"
             "a) A permanent injunction restraining Defendant from further infringement;\n"
             "b) An award of compensatory damages in an amount to be determined at trial;\n"
             "c) An award of treble damages for willful infringement;\n"
             "d) An award of attorneys' fees and costs;\n"
             "e) Such other and further relief as the Court deems just and proper.\n\n"
             "Respectfully submitted,\n\n"
             "HARRISON & BLACKWELL LLP\n"
             "By: /s/ Victoria A. Harrison\n"
             "Victoria A. Harrison, Esq.\n"
             "Senior Partner\n"
             "One Liberty Plaza, 38th Floor\n"
             "New York, NY 10006\n"
             "Tel: (212) 555-4200\n"
             "Dated: March 15, 2024"),
            ("ANSWER AND AFFIRMATIVE DEFENSES", 14, 29,
             "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK\n\n"
             "GREENFIELD TECHNOLOGIES, INC.,\nPlaintiff,\n\nvs.\n\n"
             "NEXGEN SOLUTIONS GROUP, LLC,\nDefendant.\n\n"
             "Case No. 2024-CV-03847\n\n"
             "ANSWER AND AFFIRMATIVE DEFENSES\n\n"
             "Defendant Nexgen Solutions Group, LLC (\"Nexgen\" or \"Defendant\"), by and through its "
             "undersigned attorneys, responds to the Complaint filed by Plaintiff Greenfield Technologies, "
             "Inc. (\"Greenfield\" or \"Plaintiff\") as follows:\n\n"
             "GENERAL DENIAL\n\n"
             "1. Nexgen denies each and every allegation contained in the Complaint except as expressly "
             "admitted herein.\n\n"
             "RESPONSE TO SPECIFIC ALLEGATIONS\n\n"
             "2. Nexgen admits the allegations in Paragraph 1 to the extent they describe the general nature "
             "of Plaintiff's claims. Nexgen denies that it has engaged in any unlawful conduct.\n\n"
             "3. Nexgen admits that Greenfield is a Delaware corporation. Nexgen lacks knowledge or information "
             "sufficient to form a belief as to Greenfield's characterization of itself as a \"leading provider\" "
             "and therefore denies the same.\n\n"
             "4. Nexgen admits it is organized under California law with its principal place of business in "
             "San Jose, California. Nexgen denies that its products incorporate any of Greenfield's patented "
             "technologies without authorization.\n\n"
             "AFFIRMATIVE DEFENSES\n\n"
             "FIRST AFFIRMATIVE DEFENSE - Non-Infringement\n\n"
             "5. Nexgen's CloudSync Pro product was independently developed by Nexgen's engineering team over "
             "a period of thirty-six months, beginning in March 2020, well before any exposure to the specific "
             "Greenfield technologies at issue.\n\n"
             "SECOND AFFIRMATIVE DEFENSE - Invalidity\n\n"
             "8. Upon information and belief, the '293 Patent is invalid for failure to satisfy one or more "
             "conditions of patentability under 35 U.S.C. Sections 101, 102, 103, and/or 112.\n\n"
             "THIRD AFFIRMATIVE DEFENSE - License\n\n"
             "11. To the extent any Nexgen product utilizes technology covered by the '293 Patent, such use "
             "is authorized under the License Agreement between the parties.\n\n"
             "FOURTH AFFIRMATIVE DEFENSE - Unclean Hands\n\n"
             "14. Greenfield's claims are barred by the doctrine of unclean hands. Upon information and belief, "
             "Greenfield engaged in inequitable conduct before the United States Patent and Trademark Office.\n\n"
             "COUNTERCLAIMS\n\n"
             "17. Nexgen hereby asserts the following counterclaims against Greenfield.\n\n"
             "COUNT I - DECLARATORY JUDGMENT OF NON-INFRINGEMENT\n\n"
             "18. An actual justiciable controversy exists between Nexgen and Greenfield.\n\n"
             "COUNT II - DECLARATORY JUDGMENT OF INVALIDITY\n\n"
             "22. The '293 Patent is invalid as anticipated by prior art, including published research by "
             "Dr. James Patterson at Stanford University (2017) and U.S. Patent No. 9,412,567 to Kowalski.\n\n"
             "PRAYER FOR RELIEF\n\n"
             "WHEREFORE, Defendant respectfully requests that the Court:\n"
             "a) Dismiss all claims asserted by Plaintiff;\n"
             "b) Enter judgment declaring the '293 Patent invalid;\n"
             "c) Enter judgment declaring Nexgen does not infringe;\n"
             "d) Award Nexgen its reasonable attorneys' fees;\n"
             "e) Grant such other relief as the Court deems appropriate.\n\n"
             "Respectfully submitted,\n\n"
             "MARTINEZ, CHEN & ASSOCIATES\n"
             "By: /s/ David R. Martinez\n"
             "David R. Martinez, Esq.\n"
             "525 Market Street, Suite 3100\n"
             "San Francisco, CA 94105\n"
             "Tel: (415) 555-8900\n"
             "Dated: April 29, 2024"),
        ]),
        ("DISCOVERY", 29, 79, [
            ("INTERROGATORIES", 29, 44,
             "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK\n\n"
             "GREENFIELD TECHNOLOGIES, INC.,\nPlaintiff,\n\nvs.\n\n"
             "NEXGEN SOLUTIONS GROUP, LLC,\nDefendant.\n\n"
             "Case No. 2024-CV-03847\n\n"
             "PLAINTIFF'S FIRST SET OF INTERROGATORIES\nTO DEFENDANT\n\n"
             "Pursuant to Federal Rules of Civil Procedure Rule 33, Plaintiff Greenfield Technologies, Inc. "
             "hereby propounds the following Interrogatories upon Defendant Nexgen Solutions Group, LLC.\n\n"
             "DEFINITIONS AND INSTRUCTIONS\n\n"
             "1. \"Document\" means any writing, recording, or compilation of data or information.\n\n"
             "2. \"Communication\" means every manner of exchange of information.\n\n"
             "3. \"You\" or \"Your\" refers to Defendant Nexgen Solutions Group, LLC.\n\n"
             "INTERROGATORIES\n\n"
             "INTERROGATORY NO. 1:\n"
             "Identify each person who participated in the design, development, testing, or deployment "
             "of the CloudSync Pro product, including their full name, job title, dates of employment, "
             "and specific role in the product's development.\n\n"
             "INTERROGATORY NO. 2:\n"
             "For each person identified in response to Interrogatory No. 1, state whether that person "
             "had access to any Greenfield proprietary information, and if so, describe the nature and "
             "extent of such access.\n\n"
             "INTERROGATORY NO. 3:\n"
             "Describe in detail the development timeline for CloudSync Pro, including all milestones, "
             "design reviews, code commits, and releases from inception through the present date.\n\n"
             "INTERROGATORY NO. 4:\n"
             "Identify all documents, source code repositories, and technical specifications that relate "
             "to the distributed synchronization functionality of CloudSync Pro.\n\n"
             "INTERROGATORY NO. 5:\n"
             "State the total revenue generated by CloudSync Pro from its initial release through the "
             "present date, broken down by calendar quarter.\n\n"
             "INTERROGATORY NO. 6:\n"
             "Identify all third-party libraries, open-source components, or licensed technologies "
             "incorporated into CloudSync Pro.\n\n"
             "INTERROGATORY NO. 7:\n"
             "Describe all communications between any Nexgen employee and any Greenfield employee or "
             "contractor regarding cloud synchronization technology.\n\n"
             "INTERROGATORY NO. 8:\n"
             "State whether Nexgen conducted any analysis or comparison of CloudSync Pro's functionality "
             "against Greenfield's patented technology.\n\n"
             "Dated: June 15, 2024\n\n"
             "HARRISON & BLACKWELL LLP\n"
             "By: /s/ Victoria A. Harrison"),
            ("DEPOSITIONS", 44, 79,
             "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK\n\n"
             "GREENFIELD TECHNOLOGIES, INC.,\nPlaintiff,\n\nvs.\n\n"
             "NEXGEN SOLUTIONS GROUP, LLC,\nDefendant.\n\n"
             "Case No. 2024-CV-03847\n\n"
             "DEPOSITION OF JAMES THORNTON\n"
             "Vice President of Engineering, Nexgen Solutions Group, LLC\n\n"
             "Taken on behalf of the Plaintiff\n"
             "August 12, 2024\n"
             "9:00 a.m.\n\n"
             "Location: Offices of Harrison & Blackwell LLP\n"
             "One Liberty Plaza, 38th Floor\n"
             "New York, New York 10006\n\n"
             "Court Reporter: Patricia M. Sullivan, RPR, CSR\n\n"
             "APPEARANCES:\n\n"
             "For the Plaintiff:\n"
             "  Victoria A. Harrison, Esq.\n"
             "  Thomas J. Blackwell, Esq.\n"
             "  HARRISON & BLACKWELL LLP\n\n"
             "For the Defendant:\n"
             "  David R. Martinez, Esq.\n"
             "  Sarah K. Tanaka, Esq.\n"
             "  MARTINEZ, CHEN & ASSOCIATES\n\n"
             "EXAMINATION BY MS. HARRISON:\n\n"
             "Q. Good morning, Mr. Thornton. Could you state your full name for the record?\n"
             "A. James William Thornton.\n\n"
             "Q. And your current position?\n"
             "A. I'm the Vice President of Engineering at Nexgen Solutions Group.\n\n"
             "Q. How long have you held that position?\n"
             "A. Since September 2021. Before that, I was Senior Director of Platform Engineering.\n\n"
             "Q. Mr. Thornton, are you familiar with the product known as CloudSync Pro?\n"
             "A. Yes, very familiar. I oversaw its development from the beginning.\n\n"
             "Q. When did development begin on CloudSync Pro?\n"
             "A. The formal project was approved in March 2020. We had some preliminary research before "
             "that, but the official kickoff was March 2020.\n\n"
             "Q. Were you aware of Greenfield's distributed synchronization technology before development "
             "started?\n\n"
             "MR. MARTINEZ: Objection. Vague as to what you mean by \"aware of.\"\n\n"
             "MS. HARRISON: I'll rephrase.\n\n"
             "Q. Had you personally reviewed any Greenfield technical documentation regarding their "
             "synchronization protocol prior to March 2020?\n"
             "A. I had reviewed publicly available documentation, yes. Greenfield's API documentation "
             "is publicly available on their developer portal.\n\n"
             "Q. Did you review any documentation that was not publicly available?\n"
             "A. Not to my knowledge, no.\n\n"
             "Q. Let me show you what has been marked as Exhibit 14. Do you recognize this document?\n"
             "A. It appears to be an internal technical design document.\n\n"
             "Q. And whose internal document is it?\n"
             "A. It's a Nexgen document. It looks like an early architecture proposal for CloudSync Pro.\n\n"
             "Q. Does this document reference Greenfield's '293 Patent?\n\n"
             "MR. MARTINEZ: Objection. The document speaks for itself.\n\n"
             "A. I see a reference to the patent in the prior art section, yes.\n\n"
             "Q. So your engineering team was aware of the '293 Patent during development?\n"
             "A. We were aware of it as prior art, yes. That doesn't mean we copied it.\n\n"
             "[Deposition continues...]"),
        ]),
        ("MOTIONS", 79, 149, [
            ("MOTION IN LIMINE", 79, 94,
             "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK\n\n"
             "GREENFIELD TECHNOLOGIES, INC.,\nPlaintiff,\n\nvs.\n\n"
             "NEXGEN SOLUTIONS GROUP, LLC,\nDefendant.\n\n"
             "Case No. 2024-CV-03847\n\n"
             "PLAINTIFF'S MOTION IN LIMINE NO. 1\nTO EXCLUDE EVIDENCE OF SUBSEQUENT REMEDIAL MEASURES\n\n"
             "Plaintiff Greenfield Technologies, Inc. respectfully moves this Court for an order in limine "
             "excluding all evidence, testimony, and argument regarding any modifications, updates, or changes "
             "made by Defendant to its CloudSync Pro product after the filing of this lawsuit.\n\n"
             "MEMORANDUM OF LAW IN SUPPORT\n\n"
             "I. INTRODUCTION\n\n"
             "Defendant Nexgen Solutions Group, LLC has indicated its intention to introduce evidence that it "
             "modified certain aspects of the CloudSync Pro product after this litigation commenced. Such "
             "evidence is inadmissible under Federal Rule of Evidence 407, which bars evidence of subsequent "
             "remedial measures to prove negligence, culpable conduct, product defect, or need for a warning.\n\n"
             "II. LEGAL STANDARD\n\n"
             "Federal Rule of Evidence 407 provides:\n\n"
             "\"When measures are taken that would have made an earlier injury or harm less likely to occur, "
             "evidence of the subsequent measures is not admissible to prove: negligence; culpable conduct; "
             "a defect in a product or its design; or a need for a warning or instruction.\"\n\n"
             "The Advisory Committee Notes to Rule 407 explain that the rule is grounded in two policy "
             "considerations: (1) the conduct is not necessarily an admission of fault, and (2) the public "
             "policy of encouraging corrective action should not be discouraged.\n\n"
             "III. ARGUMENT\n\n"
             "A. The Modifications Constitute Subsequent Remedial Measures\n\n"
             "Following the filing of this Complaint on March 15, 2024, Nexgen released version 3.2 of "
             "CloudSync Pro on May 1, 2024, which replaced the synchronization algorithm at issue with an "
             "alternative implementation. This modification is precisely the type of subsequent remedial "
             "measure that Rule 407 is designed to exclude.\n\n"
             "B. The Prejudicial Effect Substantially Outweighs Any Probative Value\n\n"
             "Even if the Court were to find that Rule 407 does not strictly apply, the evidence should be "
             "excluded under Federal Rule of Evidence 403 because its probative value is substantially "
             "outweighed by the danger of unfair prejudice and confusion of the issues.\n\n"
             "IV. CONCLUSION\n\n"
             "For the foregoing reasons, Plaintiff respectfully requests that this Court grant this Motion "
             "in Limine and exclude all evidence of Defendant's post-litigation modifications to CloudSync Pro.\n\n"
             "Respectfully submitted,\n\n"
             "HARRISON & BLACKWELL LLP\n"
             "By: /s/ Victoria A. Harrison\n"
             "Dated: October 1, 2024"),
            ("MOTION FOR SUMMARY JUDGMENT", 94, 149,
             "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK\n\n"
             "GREENFIELD TECHNOLOGIES, INC.,\nPlaintiff,\n\nvs.\n\n"
             "NEXGEN SOLUTIONS GROUP, LLC,\nDefendant.\n\n"
             "Case No. 2024-CV-03847\n\n"
             "PLAINTIFF'S MOTION FOR SUMMARY JUDGMENT\n\n"
             "Plaintiff Greenfield Technologies, Inc. (\"Greenfield\") respectfully moves this Court, pursuant "
             "to Federal Rule of Civil Procedure 56, for summary judgment on Counts I (Patent Infringement) "
             "and II (Breach of Contract) of its Complaint.\n\n"
             "STATEMENT OF UNDISPUTED MATERIAL FACTS\n\n"
             "1. Greenfield is the owner by assignment of U.S. Patent No. 10,847,293 (\"the '293 Patent\"), "
             "entitled \"System and Method for Distributed Data Synchronization in Multi-Tenant Cloud "
             "Environments.\" (Ex. A, Patent Certificate).\n\n"
             "2. The '293 Patent was filed on April 12, 2018, and issued on November 10, 2020. "
             "(Ex. A).\n\n"
             "3. In March 2019, Greenfield and Nexgen entered into a Technology Licensing Agreement "
             "(\"License Agreement\"). (Ex. B, License Agreement).\n\n"
             "4. Section 4.2 of the License Agreement provides: \"Licensee shall not reverse engineer, "
             "decompile, disassemble, or otherwise attempt to derive the source code of Licensor's "
             "proprietary software.\" (Ex. B, Section 4.2).\n\n"
             "5. Nexgen's CloudSync Pro product was released in January 2023. (Ex. C, Product Announcement).\n\n"
             "6. Dr. Patricia Huang, Greenfield's Chief Technology Officer, analyzed CloudSync Pro and "
             "concluded that its synchronization protocol implements each element of Claims 1, 7, and 12 "
             "of the '293 Patent. (Ex. D, Huang Declaration, Paragraphs 15-42).\n\n"
             "7. Nexgen's own internal design document (Exhibit 14 from the Thornton Deposition) references "
             "the '293 Patent in its \"Prior Art\" section and describes the CloudSync Pro architecture using "
             "terminology identical to the patent claims. (Ex. E, Thornton Depo. Tr. at 87:14-89:22).\n\n"
             "ARGUMENT\n\n"
             "I. LEGAL STANDARD\n\n"
             "Summary judgment is appropriate when \"there is no genuine dispute as to any material fact and "
             "the movant is entitled to judgment as a matter of law.\" Fed. R. Civ. P. 56(a).\n\n"
             "II. GREENFIELD IS ENTITLED TO SUMMARY JUDGMENT ON COUNT I\n\n"
             "A. Claim Construction\n\n"
             "The Court has already construed the disputed claim terms in its Markman Order dated August 30, "
             "2024. Under the Court's construction, the key term \"distributed synchronization protocol\" "
             "means \"a method for coordinating data updates across multiple geographically separated servers "
             "in real time.\"\n\n"
             "B. Infringement Analysis\n\n"
             "Applying the Court's claim construction to the undisputed facts, CloudSync Pro literally "
             "infringes Claims 1, 7, and 12 of the '293 Patent.\n\n"
             "III. GREENFIELD IS ENTITLED TO SUMMARY JUDGMENT ON COUNT II\n\n"
             "The undisputed evidence demonstrates that Nexgen breached Section 4.2 of the License Agreement.\n\n"
             "CONCLUSION\n\n"
             "For the foregoing reasons, Greenfield respectfully requests that this Court grant summary "
             "judgment in Greenfield's favor on Counts I and II.\n\n"
             "Respectfully submitted,\n\n"
             "HARRISON & BLACKWELL LLP\n"
             "By: /s/ Victoria A. Harrison\n"
             "Dated: November 15, 2024"),
        ]),
    ]

    # Helper to add text to a page with word wrap
    def add_page_text(page, text, y_start=72):
        """Add text to a page using textbox insertion."""
        rect = pymupdf.Rect(MARGIN, y_start, W - MARGIN, H - MARGIN)
        page.insert_textbox(
            rect,
            text,
            fontsize=11,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    def add_section_header(page, title, y_pos=72):
        """Add a bold section header."""
        page.insert_text(
            pymupdf.Point(MARGIN, y_pos + 16),
            title,
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0),
        )

    def add_page_number(page, num):
        """Add page number at bottom center."""
        page.insert_text(
            pymupdf.Point(W / 2 - 10, H - 36),
            str(num),
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # Generate 150 pages
    total_pages = 150

    for pg_idx in range(total_pages):
        page = doc.new_page(width=W, height=H)
        add_page_number(page, pg_idx + 1)

        # Determine which section and subsection this page belongs to
        content_added = False
        for section_title, sec_start, sec_end, subsections in sections:
            if sec_start <= pg_idx < sec_end:
                for sub_title, sub_start, sub_end, sub_text in subsections:
                    if sub_start <= pg_idx < sub_end:
                        if pg_idx == sub_start:
                            # First page of subsection: add header and beginning of text
                            add_section_header(page, sub_title, y_pos=72)
                            # Split text into chunks for pages
                            lines = sub_text.split('\n')
                            # Estimate ~45 lines per page
                            lines_per_page = 42
                            page_offset = pg_idx - sub_start
                            start_line = page_offset * lines_per_page
                            end_line = start_line + lines_per_page
                            chunk = '\n'.join(lines[start_line:end_line])
                            if chunk.strip():
                                add_page_text(page, chunk, y_start=100)
                        else:
                            # Continuation page
                            lines = sub_text.split('\n')
                            lines_per_page = 45
                            page_offset = pg_idx - sub_start
                            start_line = page_offset * lines_per_page
                            end_line = start_line + lines_per_page
                            chunk = '\n'.join(lines[start_line:end_line])
                            if chunk.strip():
                                add_page_text(page, chunk, y_start=72)
                            else:
                                # Filler continuation text
                                filler_texts = [
                                    f"{sub_title} - Continued\n\n"
                                    f"[Page {pg_idx + 1} of {sub_end - sub_start} in this section]\n\n"
                                    f"Case No. 2024-CV-03847\n"
                                    f"Greenfield Technologies, Inc. v. Nexgen Solutions Group, LLC\n\n"
                                    f"{'=' * 50}\n\n",
                                ]
                                add_page_text(page, filler_texts[0], y_start=72)
                        content_added = True
                        break
                if not content_added:
                    # Page in section but between subsections
                    add_page_text(page, f"{section_title}\n\n[Continued - Page {pg_idx + 1}]\n\n"
                                  f"Case No. 2024-CV-03847", y_start=72)
                    content_added = True
                break

        if not content_added:
            # Pages beyond the defined sections (pages 150)
            add_page_text(page, f"EXHIBITS AND APPENDICES\n\n"
                          f"[Page {pg_idx + 1}]\n\n"
                          f"Case No. 2024-CV-03847\n"
                          f"Greenfield Technologies, Inc. v. Nexgen Solutions Group, LLC\n\n"
                          f"{'=' * 50}\n\n"
                          f"Additional supporting materials and exhibits referenced in the "
                          f"foregoing pleadings, discovery materials, and motions.", y_start=72)

    # Ensure NO bookmarks exist
    doc.set_toc([])

    # Set metadata
    doc.set_metadata({
        "title": "Trial Binder - Greenfield Technologies v. Nexgen Solutions Group",
        "author": "Harrison & Blackwell LLP",
        "subject": "Case No. 2024-CV-03847",
        "keywords": "trial binder, patent infringement, breach of contract, trade secrets",
        "creator": "Legal Document Management System",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {total_pages}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
