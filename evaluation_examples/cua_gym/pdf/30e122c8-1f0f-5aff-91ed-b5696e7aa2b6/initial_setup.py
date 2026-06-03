"""
Initial Setup: Create a policy document PDF with specific metadata dates.
Task ID: pdf_mbc_021
Domain: pdf
"""

import os
import shlex
import subprocess
import time

import pymupdf
import pikepdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_021'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/policy_doc.pdf'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    # --- Build a realistic policy document PDF ---
    doc = pymupdf.open()

    # Page 1: Title page
    page = doc.new_page(width=612, height=792)
    page.insert_text(
        pymupdf.Point(72, 120),
        "Meridian Financial Group",
        fontsize=24,
        fontname="hebo",
        color=(0.0, 0.15, 0.4),
    )
    page.insert_text(
        pymupdf.Point(72, 160),
        "Data Protection & Privacy Policy",
        fontsize=20,
        fontname="hebo",
        color=(0.0, 0.15, 0.4),
    )
    page.insert_text(
        pymupdf.Point(72, 200),
        "Document Reference: MFG-POL-2023-017",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 220),
        "Effective Date: March 1, 2023",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 240),
        "Classification: Internal Use Only",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 270), pymupdf.Point(540, 270))
    shape.finish(color=(0.0, 0.15, 0.4), width=2)
    shape.commit()

    # Table of contents on title page
    toc_items = [
        "1. Purpose and Scope",
        "2. Definitions",
        "3. Data Collection Principles",
        "4. Data Processing and Storage",
        "5. Third-Party Data Sharing",
        "6. Data Subject Rights",
        "7. Incident Response Procedures",
        "8. Compliance and Enforcement",
    ]
    y = 310
    page.insert_text(pymupdf.Point(72, y), "Table of Contents", fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 30
    for item in toc_items:
        page.insert_text(pymupdf.Point(90, y), item, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 20

    # Page 2: Purpose and Scope + Definitions
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 72), "1. Purpose and Scope", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))

    purpose_text = (
        "This Data Protection and Privacy Policy establishes the framework by which Meridian Financial Group "
        "collects, processes, stores, and disposes of personal and sensitive data. This policy applies to all "
        "employees, contractors, and third-party partners who access, handle, or manage data on behalf of "
        "Meridian Financial Group.\n\n"
        "The scope encompasses all forms of data, whether in digital or physical format, across all business "
        "units including Wealth Management, Corporate Banking, Retail Services, and Insurance Products. "
        "Compliance with this policy is mandatory and subject to periodic audit by the Internal Compliance team."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 95, 540, 280),
        purpose_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page2.insert_text(pymupdf.Point(72, 300), "2. Definitions", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))
    definitions_text = (
        "Personal Data: Any information relating to an identified or identifiable natural person, including "
        "but not limited to name, identification number, location data, and online identifiers.\n\n"
        "Sensitive Data: A subset of personal data that includes financial account numbers, social security "
        "numbers, health information, biometric data, and trade secrets.\n\n"
        "Data Controller: The entity (Meridian Financial Group) that determines the purposes and means of "
        "processing personal data.\n\n"
        "Data Processor: Any natural or legal person who processes data on behalf of the Data Controller, "
        "including cloud service providers, analytics vendors, and outsourced operations."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 323, 540, 560),
        definitions_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 3: Data Collection + Processing
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 72), "3. Data Collection Principles", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))
    collection_text = (
        "All data collection activities must adhere to the following principles:\n\n"
        "a) Lawfulness: Data shall only be collected when there is a legitimate legal basis, such as consent, "
        "contractual necessity, or regulatory obligation.\n\n"
        "b) Purpose Limitation: Data collected for a specific purpose shall not be further processed in a "
        "manner incompatible with that purpose without additional consent.\n\n"
        "c) Data Minimization: Only the minimum amount of data necessary for the stated purpose shall be "
        "collected. Excessive data collection is strictly prohibited.\n\n"
        "d) Accuracy: Reasonable steps must be taken to ensure personal data is accurate and kept up to date. "
        "Inaccurate data must be rectified or erased without delay."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 95, 540, 370),
        collection_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page3.insert_text(pymupdf.Point(72, 390), "4. Data Processing and Storage", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))
    processing_text = (
        "All data processing operations must be documented in the company's Data Processing Register. "
        "Data shall be stored in approved systems only, with encryption at rest using AES-256 or equivalent. "
        "Access controls must follow the principle of least privilege, and all access events are logged for "
        "a minimum retention period of 24 months.\n\n"
        "Data retention periods are determined by the Legal and Compliance department in accordance with "
        "applicable regulations. Upon expiry of the retention period, data must be securely destroyed using "
        "approved methods (digital: cryptographic erasure; physical: cross-cut shredding)."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 413, 540, 600),
        processing_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 4: Third-Party + Rights + Incident Response + Compliance
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 72), "5. Third-Party Data Sharing", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))
    sharing_text = (
        "Data sharing with third parties requires prior approval from the Data Protection Officer (DPO). "
        "All third-party data processors must execute a Data Processing Agreement (DPA) that includes "
        "appropriate technical and organizational safeguards. Cross-border data transfers are permitted only "
        "to jurisdictions deemed adequate or under approved transfer mechanisms such as Standard Contractual "
        "Clauses (SCCs) or Binding Corporate Rules (BCRs)."
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 95, 540, 230),
        sharing_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page4.insert_text(pymupdf.Point(72, 250), "6. Data Subject Rights", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))
    rights_text = (
        "Meridian Financial Group recognizes and facilitates the following data subject rights: right of "
        "access, right to rectification, right to erasure, right to restrict processing, right to data "
        "portability, and right to object. Requests must be acknowledged within 48 hours and fulfilled "
        "within 30 calendar days. The Privacy Operations team handles all subject access requests."
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 273, 540, 390),
        rights_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page4.insert_text(pymupdf.Point(72, 410), "7. Incident Response Procedures", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))
    incident_text = (
        "Any suspected or confirmed data breach must be reported to the Security Operations Center (SOC) "
        "within one hour of discovery. The Incident Response Team will assess severity, contain the breach, "
        "and notify affected individuals and regulatory authorities as required. A post-incident review "
        "must be completed within 14 days to identify root causes and implement corrective measures."
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 433, 540, 550),
        incident_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page4.insert_text(pymupdf.Point(72, 570), "8. Compliance and Enforcement", fontsize=16, fontname="hebo", color=(0.0, 0.15, 0.4))
    compliance_text = (
        "Violation of this policy may result in disciplinary action up to and including termination of "
        "employment or contract. The Internal Audit department conducts annual reviews of compliance with "
        "this policy. All employees must complete mandatory data protection training upon onboarding and "
        "annually thereafter. Questions regarding this policy should be directed to the Data Protection "
        "Officer at dpo@meridianfinancial.com."
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 593, 540, 740),
        compliance_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Set TOC
    doc.set_toc([
        [1, "Purpose and Scope", 2],
        [1, "Definitions", 2],
        [1, "Data Collection Principles", 3],
        [1, "Data Processing and Storage", 3],
        [1, "Third-Party Data Sharing", 4],
        [1, "Data Subject Rights", 4],
        [1, "Incident Response Procedures", 4],
        [1, "Compliance and Enforcement", 4],
    ])

    # Set metadata with original dates
    doc.set_metadata({
        "title": "Data Protection & Privacy Policy",
        "author": "Meridian Financial Group",
        "subject": "Data Protection Policy",
        "keywords": "data protection, privacy, policy, compliance",
        "creator": "Meridian Legal Department",
        "producer": "Meridian Document Management System",
        "creationDate": "D:20230301",
        "modDate": "D:20230301",
    })

    doc.save(OUTPUT)
    doc.close()

    # Verify and re-set metadata with pikepdf to ensure Info dict dates are correct
    pdf = pikepdf.open(OUTPUT, allow_overwriting_input=True)
    pdf.docinfo[pikepdf.Name.CreationDate] = pikepdf.String("D:20230301")
    pdf.docinfo[pikepdf.Name.ModDate] = pikepdf.String("D:20230301")
    pdf.save(OUTPUT)

    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
