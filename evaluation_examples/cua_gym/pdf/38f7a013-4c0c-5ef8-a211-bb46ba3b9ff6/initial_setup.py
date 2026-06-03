"""
Initial Setup: Create 18-page legal filing PDF without filing stamps
Task ID: pdf_pw_040
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_040'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/court_filing.pdf'

# Letter size in points
PAGE_W, PAGE_H = 612, 792

# Realistic legal document content for 18 pages
LEGAL_SECTIONS = [
    {
        "heading": "IN THE SUPERIOR COURT OF THE STATE OF COLUMBIA\nFOR THE COUNTY OF WESTBROOK",
        "body": (
            "GREENFIELD PROPERTIES LLC,\n"
            "                    Plaintiff,\n\n"
            "          v.\n\n"
            "MORRISON CONSTRUCTION INC.,\n"
            "                    Defendant.\n\n"
            "COMPLAINT FOR DAMAGES AND BREACH OF CONTRACT\n\n"
            "Plaintiff Greenfield Properties LLC ('Greenfield'), by and through its "
            "attorneys, Kessler, Hartman & Park LLP, hereby files this Complaint against "
            "Defendant Morrison Construction Inc. ('Morrison') and alleges as follows:"
        ),
    },
    {
        "heading": "I. PARTIES",
        "body": (
            "1. Plaintiff Greenfield Properties LLC is a limited liability company "
            "organized and existing under the laws of the State of Columbia, with its "
            "principal place of business at 4200 Meridian Boulevard, Suite 1200, "
            "Westbrook, Columbia 98401.\n\n"
            "2. Defendant Morrison Construction Inc. is a corporation organized and "
            "existing under the laws of the State of Columbia, with its principal place "
            "of business at 780 Industrial Park Drive, Westbrook, Columbia 98403.\n\n"
            "3. At all times relevant herein, Morrison held a general contractor's "
            "license (License No. GC-2019-04582) issued by the Columbia Department "
            "of Licensing and Regulation."
        ),
    },
    {
        "heading": "II. JURISDICTION AND VENUE",
        "body": (
            "4. This Court has jurisdiction over this matter pursuant to Columbia "
            "Revised Code Section 2.08.010 as the amount in controversy exceeds "
            "$75,000, exclusive of interest and costs.\n\n"
            "5. Venue is proper in Westbrook County Superior Court pursuant to "
            "Columbia Revised Code Section 4.12.025 because the events giving rise "
            "to this action occurred in Westbrook County and the Defendant maintains "
            "its principal office in Westbrook County.\n\n"
            "6. All conditions precedent to the filing of this action have been "
            "satisfied, waived, or otherwise excused."
        ),
    },
    {
        "heading": "III. FACTUAL BACKGROUND",
        "body": (
            "7. On or about March 15, 2024, Greenfield and Morrison entered into a "
            "written Construction Services Agreement ('the Agreement') for the "
            "renovation and expansion of the Meridian Commerce Center located at "
            "8900 Lakewood Avenue, Westbrook, Columbia 98402.\n\n"
            "8. The Agreement specified a total contract price of $4,275,000.00 for "
            "the complete renovation of floors 3 through 7 of the Meridian Commerce "
            "Center, including structural reinforcement, HVAC system replacement, "
            "electrical upgrades, and interior finish work.\n\n"
            "9. The Agreement established a substantial completion date of "
            "December 1, 2024, with final completion required by January 15, 2025.\n\n"
            "10. Greenfield made timely progress payments to Morrison totaling "
            "$3,412,500.00, representing 80% of the total contract price, in "
            "accordance with the payment schedule set forth in Exhibit A to the Agreement."
        ),
    },
    {
        "heading": "III. FACTUAL BACKGROUND (continued)",
        "body": (
            "11. Beginning in August 2024, Morrison failed to maintain adequate "
            "staffing levels at the project site. On multiple occasions, the number "
            "of workers present fell below the minimum required by the project schedule.\n\n"
            "12. On September 22, 2024, the Westbrook County Building Inspector "
            "issued a Notice of Violation (NOV-2024-1847) citing Morrison for failure "
            "to comply with fire suppression system installation requirements on the "
            "5th floor of the Meridian Commerce Center.\n\n"
            "13. Despite written notice from Greenfield dated October 3, 2024, "
            "demanding that Morrison cure the deficiencies within 30 days as required "
            "by Section 8.2 of the Agreement, Morrison failed to take corrective action.\n\n"
            "14. On November 15, 2024, Greenfield's independent structural engineer, "
            "Dr. Patricia Yamamoto, P.E., inspected the project site and identified "
            "significant deficiencies in the structural reinforcement work on floors "
            "4 and 5, documented in her report dated November 18, 2024."
        ),
    },
    {
        "heading": "III. FACTUAL BACKGROUND (continued)",
        "body": (
            "15. Dr. Yamamoto's report identified the following specific deficiencies:\n"
            "    a. Inadequate weld penetration on 23 of 48 steel beam connections;\n"
            "    b. Use of Grade 36 steel in locations requiring Grade 50 steel;\n"
            "    c. Missing shear connectors at 12 beam-to-column connections;\n"
            "    d. Improper torque values on 34 high-strength bolted connections.\n\n"
            "16. On December 5, 2024, Morrison abandoned the project site without "
            "notice, removing all equipment and personnel. Morrison has not returned "
            "to the site or communicated with Greenfield since that date.\n\n"
            "17. As of the date of Morrison's abandonment, the project was "
            "approximately 58% complete, with critical structural and mechanical "
            "systems work remaining unfinished.\n\n"
            "18. Greenfield engaged replacement contractor Atlas Building Group LLC "
            "to assess the remaining work. Atlas provided a completion estimate of "
            "$2,890,000.00, which includes $745,000.00 in remediation costs to "
            "correct Morrison's deficient work."
        ),
    },
    {
        "heading": "IV. FIRST CAUSE OF ACTION - BREACH OF CONTRACT",
        "body": (
            "19. Greenfield incorporates by reference paragraphs 1 through 18 "
            "as though fully set forth herein.\n\n"
            "20. The Agreement constitutes a valid and binding contract between "
            "Greenfield and Morrison.\n\n"
            "21. Greenfield performed all of its obligations under the Agreement, "
            "including timely payment of all progress payments due.\n\n"
            "22. Morrison breached the Agreement by:\n"
            "    a. Failing to complete construction work by the agreed-upon dates;\n"
            "    b. Performing deficient structural reinforcement work;\n"
            "    c. Failing to comply with building code requirements;\n"
            "    d. Abandoning the project without notice or justification;\n"
            "    e. Failing to cure deficiencies after written notice.\n\n"
            "23. As a direct and proximate result of Morrison's breach, Greenfield "
            "has suffered damages in an amount to be proven at trial, but not less "
            "than $3,027,500.00."
        ),
    },
    {
        "heading": "IV. FIRST CAUSE OF ACTION (continued) - DAMAGES CALCULATION",
        "body": (
            "24. Greenfield's damages include, but are not limited to:\n"
            "    a. Completion costs by replacement contractor:  $2,890,000.00\n"
            "    b. Less remaining contract balance:            ($  862,500.00)\n"
            "    c. Net additional completion costs:             $2,027,500.00\n"
            "    d. Lost rental income (6 months delay):        $  540,000.00\n"
            "    e. Additional architectural fees:               $   85,000.00\n"
            "    f. Additional inspection costs:                 $   47,500.00\n"
            "    g. Temporary relocation of existing tenants:    $  327,500.00\n"
            "    h. Total claimed damages:                      $3,027,500.00\n\n"
            "25. Greenfield reserves the right to amend the damages calculation "
            "as discovery proceeds and additional costs are identified."
        ),
    },
    {
        "heading": "V. SECOND CAUSE OF ACTION - NEGLIGENCE",
        "body": (
            "26. Greenfield incorporates by reference paragraphs 1 through 25 "
            "as though fully set forth herein.\n\n"
            "27. Morrison owed Greenfield a duty of care to perform the construction "
            "work in a workmanlike manner, in accordance with industry standards, "
            "applicable building codes, and the specifications set forth in the Agreement.\n\n"
            "28. Morrison breached its duty of care by performing deficient "
            "structural reinforcement work, failing to use specified materials, "
            "and failing to comply with applicable building codes.\n\n"
            "29. Morrison's negligence was a direct and proximate cause of "
            "Greenfield's damages as set forth above.\n\n"
            "30. Morrison's conduct was negligent per se in that it violated "
            "Columbia Building Code Section 1704.3 regarding special inspections "
            "of structural steel connections."
        ),
    },
    {
        "heading": "VI. THIRD CAUSE OF ACTION - BREACH OF IMPLIED WARRANTY",
        "body": (
            "31. Greenfield incorporates by reference paragraphs 1 through 30 "
            "as though fully set forth herein.\n\n"
            "32. Under Columbia law, Morrison impliedly warranted that its "
            "construction work would be performed in a workmanlike manner and "
            "would be suitable for the intended purpose.\n\n"
            "33. Morrison breached the implied warranty of workmanlike performance "
            "by performing deficient structural work, using substandard materials, "
            "and abandoning the project before completion.\n\n"
            "34. As a direct and proximate result of Morrison's breach of the "
            "implied warranty, Greenfield has been damaged in an amount to be "
            "proven at trial."
        ),
    },
    {
        "heading": "VII. FOURTH CAUSE OF ACTION - UNJUST ENRICHMENT",
        "body": (
            "35. Greenfield incorporates by reference paragraphs 1 through 34 "
            "as though fully set forth herein.\n\n"
            "36. Greenfield conferred a benefit upon Morrison by paying "
            "$3,412,500.00 in progress payments for construction work.\n\n"
            "37. Morrison was aware of and accepted the benefit of these payments.\n\n"
            "38. Morrison's retention of payments for work not performed, or "
            "performed deficiently, would be inequitable and unjust.\n\n"
            "39. Greenfield is entitled to restitution in an amount representing "
            "the difference between the payments made and the reasonable value "
            "of the work actually performed in a workmanlike manner, estimated "
            "at not less than $1,200,000.00."
        ),
    },
    {
        "heading": "VIII. FIFTH CAUSE OF ACTION - VIOLATION OF CONTRACTOR LICENSING ACT",
        "body": (
            "40. Greenfield incorporates by reference paragraphs 1 through 39 "
            "as though fully set forth herein.\n\n"
            "41. Columbia Revised Code Section 18.27.114 provides that a contractor "
            "who fails to substantially comply with licensing requirements or who "
            "performs deficient work shall be liable for damages, including "
            "attorney's fees and costs.\n\n"
            "42. Morrison violated the Contractor Licensing Act by:\n"
            "    a. Employing unlicensed subcontractors for structural steel work;\n"
            "    b. Failing to maintain required bonds and insurance;\n"
            "    c. Abandoning a project without proper notification;\n"
            "    d. Performing work that fails to meet minimum code requirements.\n\n"
            "43. Greenfield is entitled to treble damages under Section 18.27.114(4) "
            "of the Contractor Licensing Act."
        ),
    },
    {
        "heading": "IX. REQUEST FOR INJUNCTIVE RELIEF",
        "body": (
            "44. Greenfield incorporates by reference paragraphs 1 through 43 "
            "as though fully set forth herein.\n\n"
            "45. Greenfield has reason to believe that Morrison may dispose of, "
            "transfer, or encumber assets to avoid satisfaction of any judgment "
            "entered in this action.\n\n"
            "46. Morrison has recently transferred ownership of multiple pieces "
            "of construction equipment to related entities, as detailed in the "
            "Declaration of James Whitfield filed concurrently herewith.\n\n"
            "47. Greenfield will suffer irreparable harm if Morrison is permitted "
            "to dissipate its assets before judgment.\n\n"
            "48. Greenfield requests that this Court issue a temporary restraining "
            "order and preliminary injunction restraining Morrison from transferring, "
            "disposing of, or encumbering its assets pending resolution of this action."
        ),
    },
    {
        "heading": "X. PRAYER FOR RELIEF",
        "body": (
            "WHEREFORE, Plaintiff Greenfield Properties LLC prays for judgment "
            "against Defendant Morrison Construction Inc. as follows:\n\n"
            "1. For compensatory damages in an amount not less than $3,027,500.00;\n\n"
            "2. For treble damages under the Contractor Licensing Act;\n\n"
            "3. For restitution in an amount not less than $1,200,000.00;\n\n"
            "4. For temporary and permanent injunctive relief;\n\n"
            "5. For prejudgment interest at the statutory rate;\n\n"
            "6. For attorney's fees and costs as permitted by law;\n\n"
            "7. For such other and further relief as the Court deems just and equitable."
        ),
    },
    {
        "heading": "VERIFICATION",
        "body": (
            "I, Robert A. Greenfield, Managing Member of Greenfield Properties LLC, "
            "declare under penalty of perjury under the laws of the State of Columbia "
            "that the foregoing is true and correct to the best of my knowledge, "
            "information, and belief.\n\n"
            "Executed on March 28, 2026, in Westbrook, Columbia.\n\n\n"
            "___________________________________\n"
            "Robert A. Greenfield\n"
            "Managing Member\n"
            "Greenfield Properties LLC"
        ),
    },
    {
        "heading": "CERTIFICATE OF SERVICE",
        "body": (
            "I hereby certify that on March 28, 2026, I caused a true and correct "
            "copy of the foregoing COMPLAINT FOR DAMAGES AND BREACH OF CONTRACT to "
            "be served upon the following by the methods indicated:\n\n"
            "Morrison Construction Inc.\n"
            "c/o David L. Morrison, President\n"
            "780 Industrial Park Drive\n"
            "Westbrook, Columbia 98403\n"
            "    [ ] U.S. First Class Mail\n"
            "    [X] Certified Mail, Return Receipt Requested\n"
            "    [X] Personal Service by Process Server\n\n"
            "Henderson & Blake LLP\n"
            "Attorneys for Defendant\n"
            "1500 Columbia Tower, Suite 3400\n"
            "Westbrook, Columbia 98401\n"
            "    [X] Electronic Filing System\n"
            "    [X] Email: d.henderson@hendersonblake.com\n\n\n"
            "___________________________________\n"
            "Catherine S. Park, WSBA No. 38291\n"
            "Kessler, Hartman & Park LLP"
        ),
    },
    {
        "heading": "EXHIBIT LIST",
        "body": (
            "Exhibit A: Construction Services Agreement dated March 15, 2024\n\n"
            "Exhibit B: Payment Records and Progress Payment Schedule\n\n"
            "Exhibit C: Notice of Violation NOV-2024-1847 from Westbrook County "
            "Building Inspector\n\n"
            "Exhibit D: Written Notice to Cure dated October 3, 2024\n\n"
            "Exhibit E: Structural Engineering Report by Dr. Patricia Yamamoto, P.E., "
            "dated November 18, 2024\n\n"
            "Exhibit F: Atlas Building Group LLC Completion Estimate\n\n"
            "Exhibit G: Photographs of Project Site documenting deficiencies\n\n"
            "Exhibit H: Correspondence between Greenfield and Morrison\n\n"
            "Exhibit I: Declaration of James Whitfield regarding asset transfers"
        ),
    },
    {
        "heading": "ATTORNEY SIGNATURE",
        "body": (
            "Respectfully submitted,\n\n"
            "KESSLER, HARTMAN & PARK LLP\n\n\n"
            "___________________________________\n"
            "Catherine S. Park, WSBA No. 38291\n"
            "Michael T. Kessler, WSBA No. 24156\n"
            "4200 Meridian Boulevard, Suite 800\n"
            "Westbrook, Columbia 98401\n"
            "Telephone: (360) 555-0142\n"
            "Facsimile: (360) 555-0143\n"
            "Email: cpark@khplaw.com\n"
            "Email: mkessler@khplaw.com\n\n"
            "Attorneys for Plaintiff\n"
            "Greenfield Properties LLC"
        ),
    },
]


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

    for section in LEGAL_SECTIONS:
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        # Heading (bold, centered-ish at top)
        heading_y = 72
        for line in section["heading"].split("\n"):
            page.insert_text(
                pymupdf.Point(72, heading_y),
                line,
                fontsize=12,
                fontname="tibo",  # Times-Bold
                color=(0, 0, 0),
            )
            heading_y += 16

        # Body text in bounded rectangle below heading
        body_rect = pymupdf.Rect(72, heading_y + 12, 540, 740)
        page.insert_textbox(
            body_rect,
            section["body"],
            fontsize=11,
            fontname="tiro",  # Times-Roman
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {len(LEGAL_SECTIONS)}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
