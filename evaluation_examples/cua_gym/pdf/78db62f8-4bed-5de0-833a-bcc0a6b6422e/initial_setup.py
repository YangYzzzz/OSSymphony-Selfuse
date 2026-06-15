"""
Initial Setup: Create a 350-page appellate record PDF
Task ID: pdf_legal_062
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_062'
LEGAL_DIR = f'{WORKDIR}/legal/appellate'
OUTPUT = f'{LEGAL_DIR}/record.pdf'

# Page size: US Letter
W, H = 612, 792

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

# Realistic legal section content for an appellate record
SECTIONS = [
    ("COVER PAGE", [
        "IN THE UNITED STATES COURT OF APPEALS",
        "FOR THE NINTH CIRCUIT",
        "",
        "Case No. 2025-CV-04817",
        "",
        "WESTFIELD COMMERCIAL PROPERTIES, LLC,",
        "    Plaintiff-Appellant,",
        "",
        "v.",
        "",
        "MERIDIAN INSURANCE GROUP, INC.,",
        "    Defendant-Appellee.",
        "",
        "APPELLATE RECORD",
        "",
        "Appeal from the United States District Court",
        "for the Central District of California",
        "The Honorable Patricia K. Yamamoto, District Judge",
        "Case No. 8:23-cv-01492-PKY",
        "",
        "Volume I of I",
        "",
        "Prepared by the Clerk of the Court",
    ]),
    ("TABLE OF CONTENTS", [
        "TABLE OF CONTENTS",
        "",
        "Docket Entries ..................................... 1",
        "Complaint .......................................... 8",
        "Answer and Affirmative Defenses ................... 32",
        "Motion for Summary Judgment ....................... 58",
        "Opposition to Motion for Summary Judgment ......... 89",
        "Reply in Support of Summary Judgment .............. 118",
        "Order Granting Summary Judgment ................... 135",
        "Notice of Appeal ................................... 148",
        "Exhibits A through M ............................... 155",
        "Deposition of Robert Langford ..................... 210",
        "Deposition of Sandra Whitfield .................... 248",
        "Expert Report - Dr. James Thornton ................ 290",
        "Trial Transcript Excerpts ......................... 320",
    ]),
    ("DOCKET ENTRIES", [
        "UNITED STATES DISTRICT COURT",
        "CENTRAL DISTRICT OF CALIFORNIA",
        "",
        "Case No. 8:23-cv-01492-PKY",
        "Westfield Commercial Properties, LLC v. Meridian Insurance Group, Inc.",
        "",
        "DOCKET ENTRIES",
        "",
        "Date Filed    No.    Description",
        "----------    ---    -----------",
        "06/12/2023     1     COMPLAINT filed by Westfield Commercial Properties, LLC",
        "                     against Meridian Insurance Group, Inc. Filing fee $402.00",
        "                     paid. (Attachments: #1 Civil Cover Sheet, #2 Summons)",
        "06/15/2023     2     SUMMONS issued as to Meridian Insurance Group, Inc.",
        "07/01/2023     3     RETURN OF SERVICE executed. Meridian Insurance Group, Inc.",
        "                     served on 06/28/2023.",
        "07/22/2023     4     ANSWER to Complaint filed by Meridian Insurance Group, Inc.",
        "                     with Affirmative Defenses.",
        "08/10/2023     5     SCHEDULING ORDER: Discovery due by 02/15/2024.",
        "                     Dispositive motions due 03/15/2024. Pretrial conference",
        "                     set for 05/01/2024 at 10:00 AM.",
        "09/05/2023     6     NOTICE of Deposition of Robert Langford on 10/12/2023.",
        "09/08/2023     7     NOTICE of Deposition of Sandra Whitfield on 10/19/2023.",
    ]),
    ("COMPLAINT", [
        "COLE, HENDERSON & PARK LLP",
        "Margaret A. Cole (SBN 198452)",
        "David R. Henderson (SBN 213876)",
        "2100 Pacific Avenue, Suite 3400",
        "Los Angeles, California 90067",
        "Telephone: (310) 555-0142",
        "Facsimile: (310) 555-0143",
        "Email: mcole@colehendersonpark.com",
        "",
        "Attorneys for Plaintiff",
        "WESTFIELD COMMERCIAL PROPERTIES, LLC",
        "",
        "UNITED STATES DISTRICT COURT",
        "CENTRAL DISTRICT OF CALIFORNIA",
        "",
        "WESTFIELD COMMERCIAL PROPERTIES, LLC,",
        "a California limited liability company,",
        "    Plaintiff,",
        "v.",
        "MERIDIAN INSURANCE GROUP, INC.,",
        "a Delaware corporation,",
        "    Defendant.",
        "",
        "COMPLAINT FOR BREACH OF CONTRACT AND",
        "DECLARATORY RELIEF",
        "",
        "Plaintiff Westfield Commercial Properties, LLC ('Westfield') alleges as follows:",
        "",
        "NATURE OF THE ACTION",
        "",
        "1. This action arises from Defendant Meridian Insurance Group, Inc.'s",
        "('Meridian') wrongful denial of Plaintiff's insurance claim under Commercial",
        "Property Insurance Policy No. CPP-2022-08471, covering Westfield's commercial",
        "property located at 4500 Harbor Boulevard, Costa Mesa, California 92626.",
    ]),
    ("COMPLAINT - PARTIES AND JURISDICTION", [
        "PARTIES",
        "",
        "2. Plaintiff Westfield Commercial Properties, LLC is a California limited",
        "liability company with its principal place of business at 1800 Century Park",
        "East, Suite 600, Los Angeles, California 90067.",
        "",
        "3. Defendant Meridian Insurance Group, Inc. is a Delaware corporation with",
        "its principal place of business at 500 Park Avenue, New York, New York 10022.",
        "Meridian is authorized to transact insurance business in the State of California.",
        "",
        "JURISDICTION AND VENUE",
        "",
        "4. This Court has subject matter jurisdiction under 28 U.S.C. Section 1332",
        "because there is complete diversity of citizenship between the parties and the",
        "amount in controversy exceeds $75,000, exclusive of interest and costs.",
        "",
        "5. Venue is proper in this district under 28 U.S.C. Section 1391(b) because",
        "a substantial part of the events giving rise to the claims occurred in this",
        "district, the insured property is located in this district, and the insurance",
        "policy was issued and delivered in this district.",
        "",
        "FACTUAL ALLEGATIONS",
        "",
        "6. On or about March 15, 2022, Westfield procured from Meridian a Commercial",
        "Property Insurance Policy, Policy No. CPP-2022-08471 (the 'Policy'), which",
        "provided coverage for Westfield's commercial property located at 4500 Harbor",
        "Boulevard, Costa Mesa, California 92626 (the 'Property').",
    ]),
    ("COMPLAINT - FACTUAL ALLEGATIONS", [
        "7. The Policy provided all-risk coverage with a policy limit of $12,500,000",
        "and a deductible of $25,000 for covered losses occurring during the policy",
        "period of March 15, 2022 through March 15, 2023.",
        "",
        "8. On November 4, 2022, the Property sustained significant water damage",
        "caused by the failure of the building's fire suppression sprinkler system.",
        "The sprinkler head on the fourth floor malfunctioned, resulting in continuous",
        "water discharge for approximately 14 hours before it was discovered and the",
        "water supply was shut off.",
        "",
        "9. The water damage affected floors two through four of the five-story",
        "commercial building, causing extensive damage to:",
        "    a. Interior walls, flooring, and ceiling materials;",
        "    b. Electrical systems and wiring;",
        "    c. HVAC equipment and ductwork;",
        "    d. Tenant improvements and fixtures;",
        "    e. Common area furnishings and equipment; and",
        "    f. Personal property of multiple commercial tenants.",
        "",
        "10. Westfield promptly reported the loss to Meridian on November 4, 2022,",
        "and submitted a formal proof of loss on December 20, 2022, in the amount",
        "of $8,743,216.50.",
        "",
        "11. On February 10, 2023, Meridian issued a letter denying coverage for the",
        "claimed loss, asserting that the damage was caused by 'wear and tear' and",
        "'lack of maintenance' of the sprinkler system, which Meridian contended were",
        "excluded under the Policy.",
    ]),
    ("ANSWER AND AFFIRMATIVE DEFENSES", [
        "BAKER, POWELL & ASSOCIATES LLP",
        "Thomas J. Baker (SBN 187653)",
        "Rachel S. Powell (SBN 224891)",
        "700 Wilshire Boulevard, Suite 2800",
        "Los Angeles, California 90017",
        "Telephone: (213) 555-0288",
        "Facsimile: (213) 555-0289",
        "",
        "Attorneys for Defendant",
        "MERIDIAN INSURANCE GROUP, INC.",
        "",
        "ANSWER AND AFFIRMATIVE DEFENSES",
        "",
        "Defendant Meridian Insurance Group, Inc. ('Meridian'), by and through",
        "its attorneys of record, hereby answers the Complaint as follows:",
        "",
        "FIRST DEFENSE",
        "",
        "The Complaint fails to state a claim upon which relief can be granted.",
        "",
        "SECOND DEFENSE",
        "",
        "1. Meridian admits the allegations contained in Paragraph 1 of the Complaint",
        "to the extent that it characterizes the nature of the action, but denies any",
        "allegation that it wrongfully denied Plaintiff's claim.",
        "",
        "2. Meridian admits the allegations in Paragraphs 2 and 3.",
        "",
        "3. Meridian admits the allegations in Paragraphs 4 and 5 regarding",
        "jurisdiction and venue.",
    ]),
    ("MOTION FOR SUMMARY JUDGMENT", [
        "MEMORANDUM OF POINTS AND AUTHORITIES IN SUPPORT OF",
        "DEFENDANT'S MOTION FOR SUMMARY JUDGMENT",
        "",
        "I. INTRODUCTION",
        "",
        "Defendant Meridian Insurance Group, Inc. ('Meridian') respectfully moves",
        "this Court for summary judgment on all claims asserted in the Complaint",
        "filed by Plaintiff Westfield Commercial Properties, LLC ('Westfield').",
        "",
        "The undisputed evidence demonstrates that the water damage to Westfield's",
        "property was caused by long-standing neglect of the fire suppression system,",
        "a condition expressly excluded from coverage under the Policy's maintenance",
        "exclusion provision. Westfield's own maintenance records confirm that no",
        "inspection or servicing of the sprinkler system had been performed for over",
        "three years preceding the loss, in direct violation of both the Policy terms",
        "and applicable building codes.",
        "",
        "II. STATEMENT OF UNDISPUTED MATERIAL FACTS",
        "",
        "1. On March 15, 2022, Meridian issued Commercial Property Insurance",
        "Policy No. CPP-2022-08471 to Westfield. (Baker Decl., Ex. A.)",
        "",
        "2. Section IV.B.3 of the Policy excludes coverage for 'loss or damage",
        "caused directly or indirectly by... deterioration, wear and tear,",
        "inherent vice, latent defect, mechanical breakdown, or lack of",
        "maintenance.' (Baker Decl., Ex. A at 42.)",
    ]),
    ("OPPOSITION TO MOTION FOR SUMMARY JUDGMENT", [
        "MEMORANDUM OF POINTS AND AUTHORITIES IN OPPOSITION TO",
        "DEFENDANT'S MOTION FOR SUMMARY JUDGMENT",
        "",
        "I. INTRODUCTION",
        "",
        "Plaintiff Westfield Commercial Properties, LLC ('Westfield') respectfully",
        "opposes Defendant Meridian Insurance Group, Inc.'s ('Meridian') Motion for",
        "Summary Judgment. Genuine disputes of material fact preclude summary judgment.",
        "",
        "The evidence demonstrates that the sprinkler system failure was caused by a",
        "manufacturing defect in the sprinkler head, not by any lack of maintenance.",
        "Westfield's expert, Dr. James Thornton, a licensed mechanical engineer with",
        "over 25 years of experience in fire suppression systems, has opined that the",
        "failure was attributable to a metallurgical defect in the sprinkler head",
        "assembly that caused premature corrosion and eventual failure under normal",
        "operating conditions.",
        "",
        "II. DISPUTED MATERIAL FACTS",
        "",
        "1. Meridian claims that the sprinkler system failure was caused by lack of",
        "maintenance. (Defendant's Fact No. 7.) This fact is disputed. Dr. Thornton's",
        "expert report concludes that the failure was caused by a manufacturing defect",
        "in the Model TX-4400 sprinkler head produced by National Fire Protection",
        "Systems, Inc. (Thornton Report at 18-22.)",
    ]),
    ("ORDER GRANTING SUMMARY JUDGMENT", [
        "UNITED STATES DISTRICT COURT",
        "CENTRAL DISTRICT OF CALIFORNIA",
        "",
        "Case No. 8:23-cv-01492-PKY",
        "",
        "ORDER GRANTING DEFENDANT'S MOTION FOR SUMMARY JUDGMENT",
        "",
        "Before the Court is Defendant Meridian Insurance Group, Inc.'s ('Meridian')",
        "Motion for Summary Judgment. The Court has reviewed the moving, opposing,",
        "and reply papers, as well as the evidence submitted by both parties.",
        "",
        "For the reasons stated below, the Motion is GRANTED.",
        "",
        "I. BACKGROUND",
        "",
        "This action arises from a dispute over insurance coverage for water damage",
        "to commercial property. Plaintiff Westfield Commercial Properties, LLC",
        "('Westfield') held a commercial property insurance policy issued by Meridian",
        "covering property at 4500 Harbor Boulevard, Costa Mesa, California.",
        "",
        "On November 4, 2022, the property sustained water damage when a sprinkler",
        "head on the fourth floor failed, releasing water for approximately 14 hours.",
        "Westfield submitted a claim for $8,743,216.50 in damages. Meridian denied",
        "the claim, citing the Policy's maintenance exclusion.",
        "",
        "II. LEGAL STANDARD",
        "",
        "Summary judgment is appropriate when 'there is no genuine dispute as to any",
        "material fact and the movant is entitled to judgment as a matter of law.'",
        "Fed. R. Civ. P. 56(a).",
    ]),
    ("NOTICE OF APPEAL", [
        "COLE, HENDERSON & PARK LLP",
        "Margaret A. Cole (SBN 198452)",
        "David R. Henderson (SBN 213876)",
        "2100 Pacific Avenue, Suite 3400",
        "Los Angeles, California 90067",
        "",
        "NOTICE OF APPEAL",
        "",
        "Notice is hereby given that Plaintiff Westfield Commercial Properties, LLC,",
        "hereby appeals to the United States Court of Appeals for the Ninth Circuit",
        "from the Order Granting Summary Judgment entered in this action on",
        "June 14, 2024, and from the Final Judgment entered on June 14, 2024.",
        "",
        "Dated: July 10, 2024",
        "",
        "COLE, HENDERSON & PARK LLP",
        "",
        "By: /s/ Margaret A. Cole",
        "    Margaret A. Cole",
        "    Attorneys for Plaintiff-Appellant",
        "    Westfield Commercial Properties, LLC",
    ]),
    ("EXHIBIT A - INSURANCE POLICY EXCERPTS", [
        "EXHIBIT A",
        "",
        "COMMERCIAL PROPERTY INSURANCE POLICY",
        "Policy No. CPP-2022-08471",
        "",
        "MERIDIAN INSURANCE GROUP, INC.",
        "",
        "Named Insured: Westfield Commercial Properties, LLC",
        "Policy Period: March 15, 2022 to March 15, 2023",
        "Coverage Amount: $12,500,000",
        "Deductible: $25,000",
        "",
        "SECTION I - PROPERTY COVERED",
        "",
        "This policy covers direct physical loss of or damage to Covered Property",
        "at the premises described in the Declarations, caused by or resulting from",
        "any Covered Cause of Loss.",
        "",
        "SECTION II - COVERED CAUSES OF LOSS",
        "",
        "When the Special Causes of Loss form applies, Covered Causes of Loss means",
        "direct physical loss unless the loss is excluded or limited in this policy.",
        "",
        "SECTION III - EXCLUSIONS",
        "",
        "A. The following exclusions apply to all coverage under this policy:",
        "   1. Earth Movement",
        "   2. Governmental Action",
        "   3. Nuclear Hazard",
    ]),
    ("EXHIBIT B - MAINTENANCE RECORDS", [
        "EXHIBIT B",
        "",
        "WESTFIELD COMMERCIAL PROPERTIES",
        "PROPERTY MAINTENANCE LOG",
        "4500 Harbor Boulevard, Costa Mesa, CA 92626",
        "",
        "Date        System          Service Performed           Technician",
        "----------  --------------  -------------------------   ----------",
        "01/15/2020  HVAC            Annual inspection           R. Torres",
        "02/20/2020  Elevator        Annual safety certification J. Kim",
        "03/10/2020  Fire Alarm      Annual test and inspection  M. Santos",
        "03/10/2020  Sprinkler       Annual flow test            M. Santos",
        "05/22/2020  Plumbing        Water heater replacement    D. Nguyen",
        "07/15/2020  Electrical      Panel upgrade, 3rd floor    A. Patel",
        "09/30/2020  HVAC            Filter replacement          R. Torres",
        "01/12/2021  HVAC            Annual inspection           R. Torres",
        "02/18/2021  Elevator        Annual safety certification J. Kim",
        "03/08/2021  Fire Alarm      Annual test and inspection  M. Santos",
        "[NOTE: No sprinkler inspection recorded for 2021 or 2022]",
        "06/14/2021  Plumbing        Restroom fixture repair     D. Nguyen",
        "08/22/2021  Electrical      Emergency lighting test     A. Patel",
        "01/10/2022  HVAC            Annual inspection           R. Torres",
        "02/15/2022  Elevator        Annual safety certification J. Kim",
        "03/12/2022  Fire Alarm      Annual test and inspection  M. Santos",
        "11/04/2022  Sprinkler       EMERGENCY - System failure  Fire Dept.",
    ]),
    ("DEPOSITION EXCERPT - ROBERT LANGFORD", [
        "DEPOSITION OF ROBERT LANGFORD",
        "",
        "October 12, 2023",
        "",
        "EXAMINATION BY MS. POWELL:",
        "",
        "Q.  Mr. Langford, what is your position at Westfield Commercial Properties?",
        "A.  I am the Director of Facilities Management. I've held that position",
        "    since January 2019.",
        "",
        "Q.  What are your responsibilities in that role?",
        "A.  I oversee all building maintenance, vendor relationships, and capital",
        "    improvement projects for Westfield's commercial properties in Southern",
        "    California.",
        "",
        "Q.  How many properties do you manage?",
        "A.  Currently, seven properties.",
        "",
        "Q.  Including the property at 4500 Harbor Boulevard?",
        "A.  Yes.",
        "",
        "Q.  Can you describe the maintenance protocol for fire suppression systems",
        "    at the Harbor Boulevard property?",
        "A.  The sprinkler system is supposed to be inspected annually. We contract",
        "    with licensed fire protection companies to perform those inspections.",
        "",
        "Q.  When was the last sprinkler inspection before the November 2022 incident?",
        "A.  Based on our records, March 2020.",
    ]),
    ("DEPOSITION EXCERPT - SANDRA WHITFIELD", [
        "DEPOSITION OF SANDRA WHITFIELD",
        "",
        "October 19, 2023",
        "",
        "EXAMINATION BY MR. HENDERSON:",
        "",
        "Q.  Ms. Whitfield, please state your position and employer.",
        "A.  I am a Senior Claims Examiner with Meridian Insurance Group. I've been",
        "    with the company for twelve years.",
        "",
        "Q.  Were you assigned to handle the Westfield claim?",
        "A.  Yes, I was the lead examiner on that claim.",
        "",
        "Q.  When did you first receive the claim?",
        "A.  The initial notice came in on November 4, 2022. The formal proof of loss",
        "    was received on December 20, 2022.",
        "",
        "Q.  What steps did you take to investigate the claim?",
        "A.  I reviewed the policy terms, arranged for an independent adjuster to",
        "    inspect the property, obtained the building maintenance records, and",
        "    retained a consulting engineer to evaluate the cause of the sprinkler",
        "    failure.",
        "",
        "Q.  Who was the consulting engineer?",
        "A.  Dr. Harold Pemberton from Structural Engineering Associates.",
    ]),
    ("EXPERT REPORT - DR. JAMES THORNTON", [
        "EXPERT REPORT OF DR. JAMES THORNTON, P.E.",
        "",
        "Prepared for: Cole, Henderson & Park LLP",
        "Date: January 15, 2024",
        "",
        "I. QUALIFICATIONS",
        "",
        "I am a licensed Professional Engineer (Mechanical) in the states of",
        "California, New York, and Texas. I hold a Ph.D. in Mechanical Engineering",
        "from Stanford University and an M.S. in Materials Science from MIT. I have",
        "over 25 years of experience in fire protection engineering, with a focus",
        "on automatic sprinkler systems.",
        "",
        "II. SCOPE OF ENGAGEMENT",
        "",
        "I was retained by Cole, Henderson & Park LLP on behalf of Westfield",
        "Commercial Properties, LLC to investigate the cause of the sprinkler",
        "system failure that occurred on November 4, 2022, at the commercial",
        "building located at 4500 Harbor Boulevard, Costa Mesa, California.",
        "",
        "III. INVESTIGATION",
        "",
        "I conducted a site inspection on September 8, 2023. During my inspection,",
        "I examined the failed sprinkler head, the surrounding piping, and the",
        "overall condition of the fire suppression system on the fourth floor.",
    ]),
]

# Additional filler sections to reach 350 pages
EXHIBIT_LETTERS = list("CDEFGHIJKLM")
EXHIBIT_TITLES = [
    "BUILDING INSPECTION REPORT",
    "CONTRACTOR REPAIR ESTIMATES",
    "TENANT CORRESPONDENCE",
    "PHOTOGRAPHIC EVIDENCE INDEX",
    "ENGINEERING DIAGRAMS",
    "INDEPENDENT ADJUSTER REPORT",
    "FINANCIAL LOSS DOCUMENTATION",
    "BUILDING CODE COMPLIANCE RECORDS",
    "MANUFACTURER SPECIFICATIONS - TX-4400",
    "INSURANCE CLAIM CORRESPONDENCE",
    "COURT HEARING TRANSCRIPTS",
]


def create_exhibit_content(letter, title):
    """Generate filler exhibit content."""
    return [
        f"EXHIBIT {letter}",
        "",
        title,
        "",
        f"[Contents of Exhibit {letter} follow]",
        "",
    ]


def add_legal_body_text():
    """Return generic legal body text lines to fill pages."""
    return [
        "The foregoing evidence demonstrates that the insured property sustained",
        "direct physical loss within the meaning of the Policy. The water damage",
        "to the building's interior systems, tenant improvements, and common areas",
        "constitutes a covered cause of loss under the all-risk provisions of the",
        "Policy.",
        "",
        "California courts have consistently held that an insurer bears the burden",
        "of proving the applicability of an exclusion. See Aydin Corp. v. First",
        "State Ins. Co., 18 Cal.4th 1183 (1998); MacKinnon v. Truck Ins. Exchange,",
        "31 Cal.4th 635 (2003). Where an insurer relies on a maintenance exclusion,",
        "the insurer must demonstrate that the loss was proximately caused by lack",
        "of maintenance, rather than by an intervening cause such as a manufacturing",
        "defect.",
        "",
        "The evidence in this case establishes a genuine dispute regarding the",
        "proximate cause of the sprinkler head failure. While Defendant's expert",
        "opines that the failure was attributable to corrosion caused by lack of",
        "maintenance, Plaintiff's expert has identified specific metallurgical",
        "defects in the sprinkler head assembly that are consistent with a",
        "manufacturing defect in the Model TX-4400 sprinkler head.",
        "",
        "Furthermore, the maintenance records demonstrate that Westfield maintained",
        "a comprehensive building maintenance program. The gap in sprinkler",
        "inspections between March 2020 and November 2022, while acknowledged,",
        "occurred during the COVID-19 pandemic when many routine inspections were",
        "deferred across the commercial real estate industry. This deferral was",
        "consistent with guidance issued by the California State Fire Marshal.",
    ]


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Margins
    LEFT = 72
    TOP = 72
    RIGHT = 540  # 612 - 72
    BOTTOM = 720  # 792 - 72
    LINE_HEIGHT = 14

    pages_created = 0

    def new_page():
        nonlocal pages_created
        page = doc.new_page(width=W, height=H)
        pages_created += 1
        return page

    def write_section(lines):
        """Write lines of text, creating new pages as needed."""
        nonlocal pages_created
        page = new_page()
        y = TOP

        for line in lines:
            if y + LINE_HEIGHT > BOTTOM:
                page = new_page()
                y = TOP

            if line == "":
                y += LINE_HEIGHT * 0.7
                continue

            # Detect headings (all caps lines)
            is_heading = (line == line.upper() and len(line) > 3 and line[0].isalpha())

            fontname = "hebo" if is_heading else "tiro"
            fontsize = 12 if is_heading else 11

            page.insert_text(
                pymupdf.Point(LEFT, y),
                line,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0),
            )
            y += LINE_HEIGHT

    # Write main sections
    for title, content in SECTIONS:
        write_section(content)

    # Write exhibit sections with filler to reach 350 pages
    for letter, etitle in zip(EXHIBIT_LETTERS, EXHIBIT_TITLES):
        exhibit_lines = create_exhibit_content(letter, etitle)
        # Add substantial body text to each exhibit
        for _ in range(8):
            exhibit_lines.extend(add_legal_body_text())
        write_section(exhibit_lines)

    # Fill remaining pages to reach 350
    filler_sections = [
        "TRIAL TRANSCRIPT EXCERPTS",
        "SUPPLEMENTAL DECLARATIONS",
        "REPLY DECLARATIONS",
        "PROPOSED FINDINGS OF FACT",
        "PROPOSED CONCLUSIONS OF LAW",
        "JUDGMENT",
        "POST-JUDGMENT MOTIONS",
        "STIPULATIONS",
        "DISCOVERY RESPONSES",
        "SUPPLEMENTAL EXPERT REPORTS",
    ]

    section_idx = 0
    while pages_created < 350:
        stitle = filler_sections[section_idx % len(filler_sections)]
        section_idx += 1
        lines = [
            stitle,
            "",
            f"Case No. 8:23-cv-01492-PKY",
            f"Westfield Commercial Properties, LLC v. Meridian Insurance Group, Inc.",
            "",
        ]
        # Add enough body text to fill several pages
        for _ in range(12):
            lines.extend(add_legal_body_text())
        write_section(lines)

    # Trim to exactly 350 pages if we overshot
    while doc.page_count > 350:
        doc.delete_page(doc.page_count - 1)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 350')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
