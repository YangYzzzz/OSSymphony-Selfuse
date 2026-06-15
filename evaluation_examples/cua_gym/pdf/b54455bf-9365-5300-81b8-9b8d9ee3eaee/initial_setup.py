"""
Initial Setup: Create a 10-page motion to compel PDF for legal task
Task ID: pdf_legal_074
Domain: pdf
"""

import os
import shlex
import subprocess
import time

# reportlab imports
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether
)
from reportlab.lib.colors import black

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_074'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/motion_compel.pdf'


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

    styles = getSampleStyleSheet()

    # Custom styles for legal document
    caption_style = ParagraphStyle(
        'Caption', parent=styles['Normal'],
        fontSize=12, leading=14, alignment=TA_CENTER,
        spaceAfter=6, fontName='Times-Roman'
    )
    caption_bold = ParagraphStyle(
        'CaptionBold', parent=styles['Normal'],
        fontSize=12, leading=14, alignment=TA_CENTER,
        spaceAfter=6, fontName='Times-Bold'
    )
    heading_style = ParagraphStyle(
        'LegalHeading', parent=styles['Normal'],
        fontSize=12, leading=14, alignment=TA_CENTER,
        spaceBefore=12, spaceAfter=12, fontName='Times-Bold'
    )
    body_style = ParagraphStyle(
        'LegalBody', parent=styles['Normal'],
        fontSize=12, leading=16, alignment=TA_JUSTIFY,
        firstLineIndent=36, spaceAfter=8, fontName='Times-Roman'
    )
    numbered_style = ParagraphStyle(
        'Numbered', parent=styles['Normal'],
        fontSize=12, leading=16, alignment=TA_JUSTIFY,
        leftIndent=36, spaceAfter=8, fontName='Times-Roman'
    )
    subheading_style = ParagraphStyle(
        'SubHeading', parent=styles['Normal'],
        fontSize=12, leading=14, alignment=TA_LEFT,
        spaceBefore=12, spaceAfter=8, fontName='Times-Bold'
    )

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    story = []

    # ===== PAGE 1: Caption / Cover =====
    story.append(Spacer(1, 12))
    story.append(Paragraph("IN THE UNITED STATES DISTRICT COURT", caption_bold))
    story.append(Paragraph("FOR THE NORTHERN DISTRICT OF CALIFORNIA", caption_bold))
    story.append(Paragraph("SAN FRANCISCO DIVISION", caption_bold))
    story.append(Spacer(1, 24))

    # Parties table
    caption_data = [
        [Paragraph("TECHVISION SYSTEMS, INC.,<br/>a Delaware corporation,", caption_style),
         '', ''],
        [Paragraph("Plaintiff,", caption_style), '', ''],
        ['', '', ''],
        [Paragraph("v.", caption_style),
         '',
         Paragraph("Case No. 3:23-cv-04817-WHO<br/><br/>"
                    "<b>PLAINTIFF'S MOTION TO COMPEL<br/>"
                    "DISCOVERY RESPONSES FROM<br/>"
                    "DEFENDANT DATACORE ANALYTICS</b>", caption_style)],
        ['', '', ''],
        [Paragraph("DATACORE ANALYTICS, LLC,<br/>a California limited liability company,", caption_style),
         '', ''],
        [Paragraph("Defendant.", caption_style), '', ''],
    ]
    caption_table = Table(caption_data, colWidths=[2.8 * inch, 0.3 * inch, 3.4 * inch])
    caption_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEAFTER', (0, 0), (0, -1), 1, black),
    ]))
    story.append(caption_table)
    story.append(Spacer(1, 24))

    story.append(Paragraph(
        "Date: March 25, 2024&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "Time: 2:00 p.m.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "Courtroom: 2, 17th Floor", body_style
    ))
    story.append(Paragraph(
        "Judge: Honorable William H. Orrick", body_style
    ))

    story.append(PageBreak())

    # ===== PAGE 2: Table of Contents =====
    story.append(Paragraph("TABLE OF CONTENTS", heading_style))
    story.append(Spacer(1, 12))

    toc_items = [
        ("I.", "INTRODUCTION", "1"),
        ("II.", "FACTUAL BACKGROUND", "2"),
        ("III.", "DISCOVERY REQUESTS AT ISSUE", "3"),
        ("IV.", "MEET AND CONFER EFFORTS", "5"),
        ("V.", "LEGAL STANDARD", "6"),
        ("VI.", "ARGUMENT", "7"),
        ("", "A. Defendant's Objections Lack Merit", "7"),
        ("", "B. The Requested Documents Are Directly Relevant", "8"),
        ("", "C. Defendant's Burden Claims Are Unsupported", "9"),
        ("VII.", "CONCLUSION", "10"),
    ]
    for num, title, page in toc_items:
        line = f"{num} {title}" if num else f"&nbsp;&nbsp;&nbsp;&nbsp;{title}"
        story.append(Paragraph(
            f"{line} {'.' * (60 - len(title))} {page}",
            ParagraphStyle('TOC', parent=body_style, firstLineIndent=0, fontName='Times-Roman')
        ))

    story.append(PageBreak())

    # ===== PAGE 3: Introduction =====
    story.append(Paragraph("I. INTRODUCTION", heading_style))
    story.append(Paragraph(
        "Plaintiff TechVision Systems, Inc. (\"TechVision\" or \"Plaintiff\") respectfully moves this "
        "Court for an order compelling Defendant DataCore Analytics, LLC (\"DataCore\" or \"Defendant\") "
        "to provide full and complete responses to Plaintiff's First Set of Requests for Production of "
        "Documents (\"RFPs\") and Plaintiff's First Set of Interrogatories. Despite multiple good-faith "
        "efforts to resolve these disputes informally, Defendant continues to withhold responsive "
        "documents and provide evasive answers to straightforward interrogatories.",
        body_style
    ))
    story.append(Paragraph(
        "This action arises from Defendant's systematic misappropriation of Plaintiff's proprietary "
        "machine learning algorithms and trade secrets. TechVision developed its NeuralEdge platform "
        "over a period of seven years at a cost exceeding $47 million in research and development. "
        "In 2022, three senior engineers—Dr. James Liu, Priya Sharma, and Michael Torres—departed "
        "TechVision and joined DataCore within a span of four months, bringing with them intimate "
        "knowledge of TechVision's proprietary technology.",
        body_style
    ))
    story.append(Paragraph(
        "Within six months of these departures, DataCore launched its \"CoreML Pro\" product, which "
        "bears striking similarities to TechVision's NeuralEdge platform in architecture, "
        "functionality, and even specific algorithm implementations. The discovery sought in this "
        "motion goes to the heart of Plaintiff's claims and is essential to proving that Defendant "
        "used Plaintiff's trade secrets to develop CoreML Pro.",
        body_style
    ))

    story.append(PageBreak())

    # ===== PAGE 4: Factual Background =====
    story.append(Paragraph("II. FACTUAL BACKGROUND", heading_style))
    story.append(Paragraph(
        "TechVision is a leading artificial intelligence company headquartered in San Francisco, "
        "California. Founded in 2015 by Dr. Emily Watson and Robert Nakamura, TechVision has "
        "developed cutting-edge machine learning solutions for enterprise clients across the "
        "financial services, healthcare, and telecommunications industries.",
        body_style
    ))
    story.append(Paragraph(
        "The NeuralEdge platform, TechVision's flagship product, incorporates proprietary neural "
        "network architectures, custom optimization algorithms, and a unique data preprocessing "
        "pipeline that collectively enable superior performance on complex classification and "
        "prediction tasks. The platform processes over 2.3 billion transactions daily for clients "
        "including Goldman Sachs, UnitedHealth Group, and AT&T.",
        body_style
    ))
    story.append(Paragraph(
        "Dr. James Liu served as TechVision's Chief Technology Officer from 2017 to 2022. During "
        "his tenure, Dr. Liu had unrestricted access to all proprietary source code, algorithm "
        "specifications, and technical documentation related to NeuralEdge. Priya Sharma served "
        "as Senior Machine Learning Engineer and was the lead architect of NeuralEdge's optimization "
        "module. Michael Torres served as Principal Software Engineer responsible for the platform's "
        "data pipeline infrastructure.",
        body_style
    ))
    story.append(Paragraph(
        "On September 15, 2022, Dr. Liu submitted his resignation, effective October 15, 2022. "
        "On October 3, 2022, Priya Sharma submitted her resignation, effective November 1, 2022. "
        "On November 28, 2022, Michael Torres submitted his resignation, effective December 20, 2022. "
        "Each of these individuals had signed confidentiality and non-disclosure agreements with "
        "TechVision that remain in effect.",
        body_style
    ))
    story.append(Paragraph(
        "DataCore Analytics was founded in 2019 and had been a relatively small player in the "
        "machine learning space until its rapid expansion beginning in early 2023. Following the "
        "hiring of Dr. Liu, Sharma, and Torres, DataCore announced the development of CoreML Pro "
        "in March 2023 and released a beta version in August 2023.",
        body_style
    ))

    story.append(PageBreak())

    # ===== PAGE 5: Discovery Requests at Issue =====
    story.append(Paragraph("III. DISCOVERY REQUESTS AT ISSUE", heading_style))
    story.append(Paragraph(
        "Plaintiff served its First Set of Requests for Production on November 15, 2023. "
        "Defendant served its responses on December 20, 2023, consisting largely of boilerplate "
        "objections and producing only 127 pages of documents—primarily publicly available marketing "
        "materials. The specific requests at issue are:",
        body_style
    ))
    story.append(Spacer(1, 8))

    requests = [
        ("<b>RFP No. 7:</b> All documents relating to the development of CoreML Pro, including "
         "but not limited to design documents, architecture specifications, source code repositories, "
         "commit histories, and internal presentations."),
        ("<b>RFP No. 12:</b> All communications between Dr. James Liu, Priya Sharma, and/or "
         "Michael Torres regarding TechVision, NeuralEdge, or any technology derived from or "
         "similar to TechVision's products."),
        ("<b>RFP No. 15:</b> All documents relating to DataCore's evaluation, comparison, or "
         "analysis of TechVision's NeuralEdge platform or any competitor product with similar "
         "functionality."),
        ("<b>RFP No. 18:</b> All onboarding materials, training documents, and access credentials "
         "provided to Dr. Liu, Sharma, and Torres upon their commencement of employment at DataCore."),
        ("<b>Interrogatory No. 4:</b> Identify all persons who contributed to the design, "
         "development, testing, or deployment of CoreML Pro's neural network architecture."),
        ("<b>Interrogatory No. 8:</b> Describe in detail the timeline and process by which "
         "CoreML Pro was conceptualized, designed, developed, and brought to market."),
    ]
    for req in requests:
        story.append(Paragraph(req, numbered_style))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ===== PAGE 6: Meet and Confer =====
    story.append(Paragraph("IV. MEET AND CONFER EFFORTS", heading_style))
    story.append(Paragraph(
        "Plaintiff's counsel has engaged in extensive meet-and-confer efforts with Defendant's "
        "counsel in a good-faith attempt to resolve these discovery disputes without Court "
        "intervention. The following summarizes these efforts:",
        body_style
    ))
    story.append(Paragraph(
        "On January 8, 2024, Plaintiff's counsel sent a detailed eight-page meet-and-confer letter "
        "to Defendant's counsel, Amanda Richardson of Morrison & Foerster LLP, identifying the "
        "deficiencies in Defendant's discovery responses and requesting supplemental responses "
        "within 14 days.",
        body_style
    ))
    story.append(Paragraph(
        "On January 25, 2024, Defendant's counsel responded with a three-page letter maintaining "
        "all objections and offering to produce only a limited subset of documents responsive to "
        "RFP No. 18.",
        body_style
    ))
    story.append(Paragraph(
        "On February 5, 2024, counsel for both parties participated in a telephonic meet-and-confer "
        "conference lasting approximately two hours. During this conference, Plaintiff narrowed "
        "certain requests and proposed reasonable search protocols, but Defendant refused to withdraw "
        "its blanket objections to RFP Nos. 7, 12, and 15.",
        body_style
    ))
    story.append(Paragraph(
        "On February 20, 2024, a second telephonic conference was held, during which Defendant "
        "agreed to supplement its response to Interrogatory No. 8 but continued to refuse meaningful "
        "production responsive to the document requests.",
        body_style
    ))
    story.append(Paragraph(
        "On March 5, 2024, Defendant served supplemental responses that failed to address any of "
        "the substantive deficiencies identified by Plaintiff. Accordingly, the parties have reached "
        "an impasse, and judicial intervention is now necessary.",
        body_style
    ))

    story.append(PageBreak())

    # ===== PAGE 7: Legal Standard =====
    story.append(Paragraph("V. LEGAL STANDARD", heading_style))
    story.append(Paragraph(
        "Federal Rule of Civil Procedure 26(b)(1) provides that parties may obtain discovery "
        "regarding any nonprivileged matter that is relevant to any party's claim or defense and "
        "proportional to the needs of the case. The scope of relevance under Rule 26(b)(1) is "
        "broad, and \"[r]elevant information need not be admissible at the trial if the discovery "
        "appears reasonably calculated to lead to the discovery of admissible evidence.\"",
        body_style
    ))
    story.append(Paragraph(
        "Under Rule 37(a), a party may move for an order compelling disclosure or discovery if "
        "a party fails to respond to interrogatories under Rule 33 or fails to produce documents "
        "as requested under Rule 34. The party resisting discovery bears the burden of showing "
        "that the discovery is improper. <i>Blankenship v. Hearst Corp.</i>, 519 F.2d 418, 429 "
        "(9th Cir. 1975).",
        body_style
    ))
    story.append(Paragraph(
        "Courts in this District have consistently held that boilerplate objections, without "
        "particularized factual support, are insufficient to resist production. <i>Burlington "
        "Northern & Santa Fe Ry. Co. v. U.S. Dist. Court</i>, 408 F.3d 1142, 1149 (9th Cir. 2005). "
        "\"General and conclusory objections to relevance are inadequate and tantamount to not "
        "making any objection at all.\" <i>Doe v. Trump</i>, 329 F.R.D. 262, 270 (W.D. Wash. 2018).",
        body_style
    ))

    story.append(PageBreak())

    # ===== PAGE 8-9: Argument =====
    story.append(Paragraph("VI. ARGUMENT", heading_style))
    story.append(Paragraph("A. Defendant's Objections Lack Merit", subheading_style))
    story.append(Paragraph(
        "Defendant has interposed a litany of boilerplate objections to virtually every discovery "
        "request, including objections based on relevance, overbreadth, undue burden, and "
        "proportionality. None of these objections withstand scrutiny.",
        body_style
    ))
    story.append(Paragraph(
        "First, Defendant's relevance objections fail because each of the discovery requests "
        "directly targets information concerning the development of CoreML Pro and the activities "
        "of the former TechVision employees at DataCore. This information is plainly relevant to "
        "Plaintiff's claims for trade secret misappropriation under both the Defend Trade Secrets "
        "Act, 18 U.S.C. § 1836, and the California Uniform Trade Secrets Act, Cal. Civ. Code "
        "§ 3426 et seq.",
        body_style
    ))
    story.append(Paragraph(
        "Second, Defendant's overbreadth objections are meritless. Plaintiff has already narrowed "
        "its requests during the meet-and-confer process, proposing specific search terms, date "
        "ranges (January 2022 through the present), and custodians (limited to Dr. Liu, Sharma, "
        "Torres, and their direct supervisors at DataCore). These limitations render the requests "
        "appropriately tailored.",
        body_style
    ))
    story.append(Paragraph(
        "Third, Defendant's proportionality objections ignore the substantial amount in controversy. "
        "TechVision invested over $47 million in developing NeuralEdge and has suffered estimated "
        "damages exceeding $85 million. The discovery sought is proportional to these stakes and "
        "to the complexity of the technology at issue.",
        body_style
    ))

    story.append(PageBreak())

    story.append(Paragraph("B. The Requested Documents Are Directly Relevant", subheading_style))
    story.append(Paragraph(
        "The documents sought in RFP Nos. 7, 12, 15, and 18 are essential to proving Plaintiff's "
        "claims. RFP No. 7 seeks the development history of CoreML Pro, which will reveal whether "
        "DataCore incorporated TechVision's trade secrets into its competing product. Without access "
        "to CoreML Pro's source code, design documents, and commit histories, Plaintiff cannot "
        "perform the technical comparison necessary to establish misappropriation.",
        body_style
    ))
    story.append(Paragraph(
        "RFP No. 12 seeks communications that may reveal whether the former TechVision employees "
        "discussed or shared TechVision's proprietary information after joining DataCore. Courts "
        "routinely compel production of such communications in trade secret cases. See <i>Waymo LLC "
        "v. Uber Technologies, Inc.</i>, No. 17-cv-00939 (N.D. Cal. 2017) (compelling production "
        "of communications between former employees regarding trade secrets).",
        body_style
    ))
    story.append(Paragraph(
        "RFP No. 15 seeks competitive analysis documents that would demonstrate DataCore's "
        "knowledge of and interest in TechVision's technology. Such documents are highly probative "
        "of intent and knowledge, both of which are relevant to Plaintiff's willful misappropriation "
        "claim and request for exemplary damages.",
        body_style
    ))

    story.append(Paragraph("C. Defendant's Burden Claims Are Unsupported", subheading_style))
    story.append(Paragraph(
        "Defendant asserts without substantiation that compliance with Plaintiff's discovery requests "
        "would impose an \"undue burden.\" However, Defendant has failed to provide any affidavit, "
        "declaration, or other evidence quantifying the alleged burden. A party claiming undue burden "
        "must provide specific, detailed information demonstrating that compliance would be unduly "
        "burdensome. <i>Convertino v. U.S. Dep't of Justice</i>, 795 F. Supp. 2d 1, 7 (D.D.C. 2011).",
        body_style
    ))
    story.append(Paragraph(
        "Moreover, DataCore is a well-funded technology company that recently completed a $200 million "
        "Series D funding round. It employs over 500 employees and maintains sophisticated document "
        "management and communication systems. The notion that it cannot perform reasonable document "
        "searches and produce responsive materials strains credulity.",
        body_style
    ))

    story.append(PageBreak())

    # ===== PAGE 10: Conclusion =====
    story.append(Paragraph("VII. CONCLUSION", heading_style))
    story.append(Paragraph(
        "For the foregoing reasons, Plaintiff TechVision Systems, Inc. respectfully requests that "
        "this Court enter an order:",
        body_style
    ))
    story.append(Spacer(1, 8))
    conclusions = [
        "1. Compelling Defendant to provide full and complete responses to RFP Nos. 7, 12, 15, "
        "and 18 within 14 days of the Court's order;",
        "2. Compelling Defendant to provide a complete and verified response to Interrogatories "
        "Nos. 4 and 8 within 14 days of the Court's order;",
        "3. Awarding Plaintiff its reasonable attorneys' fees and costs incurred in bringing this "
        "motion pursuant to Federal Rule of Civil Procedure 37(a)(5); and",
        "4. Granting such other and further relief as this Court deems just and proper.",
    ]
    for c in conclusions:
        story.append(Paragraph(c, numbered_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 24))
    story.append(Paragraph("Respectfully submitted,", body_style))
    story.append(Spacer(1, 36))
    story.append(Paragraph("WILSON, CHEN & ASSOCIATES LLP", ParagraphStyle(
        'Firm', parent=body_style, firstLineIndent=0, fontName='Times-Bold'
    )))
    story.append(Spacer(1, 8))
    story.append(Paragraph("By: _____________________________", ParagraphStyle(
        'SigLine', parent=body_style, firstLineIndent=0
    )))
    story.append(Paragraph("Sarah Chen, Esq.", ParagraphStyle(
        'Attorney', parent=body_style, firstLineIndent=0, fontName='Times-Bold'
    )))
    story.append(Paragraph("Bar No. 123456", ParagraphStyle(
        'BarNo', parent=body_style, firstLineIndent=0
    )))
    story.append(Paragraph("100 Montgomery Street, Suite 2400", ParagraphStyle(
        'Addr', parent=body_style, firstLineIndent=0
    )))
    story.append(Paragraph("San Francisco, California 94104", ParagraphStyle(
        'Addr2', parent=body_style, firstLineIndent=0
    )))
    story.append(Paragraph("Telephone: (415) 555-0142", ParagraphStyle(
        'Phone', parent=body_style, firstLineIndent=0
    )))
    story.append(Paragraph("Email: schen@wilsonchenlaw.com", ParagraphStyle(
        'Email', parent=body_style, firstLineIndent=0
    )))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<i>Attorneys for Plaintiff TechVision Systems, Inc.</i>", ParagraphStyle(
        'AttFor', parent=body_style, firstLineIndent=0
    )))

    doc.build(story)
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
