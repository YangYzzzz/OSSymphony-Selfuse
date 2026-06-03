"""
Initial Setup: Create legal case files for PDF portfolio bundling task
Task ID: pdf_aw_012
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_012'
CASE_DIR = f'{WORKDIR}/legal/case_files'


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


def create_pdf(filepath, title, body_lines):
    """Create a simple single-page PDF with title and body text."""
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page.insert_text(
        pymupdf.Point(72, 72),
        title,
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0.4),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 85), pymupdf.Point(540, 85))
    shape.finish(color=(0, 0, 0.4), width=1.5)
    shape.commit()

    # Body text
    y = 110
    for line in body_lines:
        if y > 740:
            break
        page.insert_text(
            pymupdf.Point(72, y),
            line,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
        )
        y += 16

    doc.save(filepath)
    doc.close()


def create_initial():
    os.makedirs(CASE_DIR, exist_ok=True)

    # --- Pleadings (3 files) ---

    create_pdf(
        f'{CASE_DIR}/plea_complaint.pdf',
        'COMPLAINT FOR DAMAGES - Case No. 2025-CV-04817',
        [
            'IN THE SUPERIOR COURT OF THE STATE OF CALIFORNIA',
            'COUNTY OF LOS ANGELES',
            '',
            'GREENFIELD TECHNOLOGIES, INC.,          Plaintiff,',
            'vs.',
            'NEXUS INDUSTRIAL SOLUTIONS, LLC,        Defendant.',
            '',
            'Case No. 2025-CV-04817',
            'Filed: January 14, 2025',
            '',
            'COMES NOW Plaintiff Greenfield Technologies, Inc., by and through its',
            'attorneys of record, Martinez & Calloway LLP, and for its Complaint',
            'against Defendant Nexus Industrial Solutions, LLC, states as follows:',
            '',
            'PARTIES',
            '1. Plaintiff Greenfield Technologies, Inc. ("Greenfield") is a Delaware',
            '   corporation with its principal place of business at 2400 Wilshire Blvd,',
            '   Suite 1500, Los Angeles, California 90010.',
            '',
            '2. Defendant Nexus Industrial Solutions, LLC ("Nexus") is a Nevada limited',
            '   liability company registered to do business in California, with offices',
            '   at 8700 Commerce Drive, Henderson, Nevada 89015.',
            '',
            'FACTUAL ALLEGATIONS',
            '3. On or about March 12, 2024, Greenfield and Nexus entered into a Supply',
            '   Agreement (the "Agreement") for the provision of specialized industrial',
            '   filtration components valued at approximately $2,350,000.',
            '',
            '4. Nexus delivered components that failed to meet the specifications outlined',
            '   in Exhibit A of the Agreement, resulting in production line failures at',
            '   Greenfield\'s San Bernardino manufacturing facility.',
            '',
            '5. The defective components caused direct damages of $847,000 in production',
            '   losses and $312,000 in emergency procurement costs from alternative',
            '   suppliers.',
            '',
            'PRAYER FOR RELIEF',
            'WHEREFORE, Plaintiff respectfully requests that this Court:',
            'a) Award compensatory damages in excess of $1,159,000;',
            'b) Award consequential damages as proven at trial;',
            'c) Award attorneys\' fees and costs of suit;',
            'd) Grant such other relief as this Court deems just and proper.',
        ]
    )

    create_pdf(
        f'{CASE_DIR}/plea_answer.pdf',
        'ANSWER TO COMPLAINT - Case No. 2025-CV-04817',
        [
            'IN THE SUPERIOR COURT OF THE STATE OF CALIFORNIA',
            'COUNTY OF LOS ANGELES',
            '',
            'GREENFIELD TECHNOLOGIES, INC.,          Plaintiff,',
            'vs.',
            'NEXUS INDUSTRIAL SOLUTIONS, LLC,        Defendant.',
            '',
            'Case No. 2025-CV-04817',
            'Filed: February 28, 2025',
            '',
            'Defendant Nexus Industrial Solutions, LLC, by its attorneys, Sterling &',
            'Whitfield PC, hereby answers the Complaint as follows:',
            '',
            'FIRST DEFENSE',
            'The Complaint fails to state a claim upon which relief can be granted.',
            '',
            'SECOND DEFENSE - RESPONSES TO ALLEGATIONS',
            '1. Admitted that Greenfield is a Delaware corporation. Denied that Greenfield',
            '   suffered damages as alleged.',
            '',
            '2. Admitted that Nexus is a Nevada LLC. Denied as to all remaining',
            '   allegations in Paragraph 2.',
            '',
            '3. Admitted that the parties entered into a Supply Agreement. Denied that',
            '   the Agreement value was $2,350,000; the true contract value was $1,975,000.',
            '',
            '4. Denied. The components delivered met or exceeded all specifications.',
            '   Any production failures were caused by Plaintiff\'s own improper',
            '   installation and maintenance procedures.',
            '',
            '5. Denied. Plaintiff\'s claimed damages are speculative and unsupported.',
            '',
            'AFFIRMATIVE DEFENSES',
            '6. Comparative/Contributory Negligence: Plaintiff\'s damages, if any, were',
            '   caused by its own negligence in installation and operation.',
            '',
            '7. Failure to Mitigate: Plaintiff failed to take reasonable steps to',
            '   mitigate its alleged damages.',
            '',
            'WHEREFORE, Defendant requests dismissal with prejudice and attorneys\' fees.',
        ]
    )

    create_pdf(
        f'{CASE_DIR}/plea_motion.pdf',
        'MOTION FOR SUMMARY JUDGMENT - Case No. 2025-CV-04817',
        [
            'IN THE SUPERIOR COURT OF THE STATE OF CALIFORNIA',
            'COUNTY OF LOS ANGELES',
            '',
            'GREENFIELD TECHNOLOGIES, INC.,          Plaintiff,',
            'vs.',
            'NEXUS INDUSTRIAL SOLUTIONS, LLC,        Defendant.',
            '',
            'Case No. 2025-CV-04817',
            'Filed: June 15, 2025',
            'Hearing: August 4, 2025 at 9:00 AM, Department 12',
            '',
            'NOTICE OF MOTION AND MOTION FOR PARTIAL SUMMARY JUDGMENT',
            '',
            'TO ALL PARTIES AND THEIR ATTORNEYS OF RECORD:',
            '',
            'PLEASE TAKE NOTICE that on August 4, 2025, at 9:00 a.m., in Department',
            '12 of the above-entitled Court, Defendant Nexus Industrial Solutions, LLC',
            'will move this Court for an order granting partial summary judgment on',
            'Plaintiff\'s claim for consequential damages.',
            '',
            'MEMORANDUM OF POINTS AND AUTHORITIES',
            '',
            'I. INTRODUCTION',
            'This motion seeks partial summary judgment on the ground that the Supply',
            'Agreement between the parties contains a valid limitation of liability',
            'clause (Section 12.3) that expressly excludes consequential damages.',
            '',
            'II. UNDISPUTED MATERIAL FACTS',
            '1. Section 12.3 of the Agreement states: "In no event shall either party',
            '   be liable for indirect, incidental, or consequential damages."',
            '2. Both parties were represented by counsel during negotiation.',
            '3. The limitation clause was not modified by any subsequent amendment.',
            '',
            'III. ARGUMENT',
            'Under California law, contractual limitation of liability provisions are',
            'enforceable when freely negotiated between sophisticated commercial parties.',
            'See Markborough California Inc. v. Superior Court (1991) 227 Cal.App.3d 705.',
        ]
    )

    # --- Evidence (5 files) ---

    create_pdf(
        f'{CASE_DIR}/evid_photo_01.pdf',
        'EXHIBIT E-1: Photographic Evidence - Damaged Filtration Units',
        [
            'Case No. 2025-CV-04817',
            'Exhibit E-1 of 5',
            'Photographer: James Kowalski, P.E.',
            'Date Taken: April 3, 2024',
            'Location: Greenfield Manufacturing Facility, San Bernardino, CA',
            '',
            '[PHOTOGRAPH PLACEHOLDER]',
            '',
            'Description: Front view of filtration unit assembly line showing',
            'Unit #FU-2024-017 with visible crack along the primary housing seam.',
            'The crack extends approximately 14 inches from the upper flange to',
            'the mid-section coupling joint.',
            '',
            'Note: Unit was in operation for 47 days before failure was detected',
            'during routine quality inspection by Greenfield staff.',
            '',
            'Chain of Custody:',
            '  - April 3, 2024: Photographed in situ by J. Kowalski',
            '  - April 5, 2024: Unit removed and stored in evidence locker #B-14',
            '  - April 10, 2024: Inspected by independent expert Dr. Rajan Mehta',
            '  - May 2, 2024: Digital copies provided to counsel',
            '',
            'AUTHENTICATED BY:',
            'James Kowalski, P.E.',
            'License No. CE-48291',
            'Date: April 3, 2024',
        ]
    )

    create_pdf(
        f'{CASE_DIR}/evid_photo_02.pdf',
        'EXHIBIT E-2: Photographic Evidence - Manufacturing Defect Close-up',
        [
            'Case No. 2025-CV-04817',
            'Exhibit E-2 of 5',
            'Photographer: James Kowalski, P.E.',
            'Date Taken: April 3, 2024',
            'Location: Greenfield Manufacturing Facility, San Bernardino, CA',
            '',
            '[PHOTOGRAPH PLACEHOLDER]',
            '',
            'Description: Close-up macro photograph of the fracture surface on',
            'filtration unit #FU-2024-017. The fracture pattern shows characteristic',
            'signs of material fatigue consistent with substandard alloy composition.',
            '',
            'Magnification: 10x optical',
            'Camera: Nikon D850 with Nikkor 105mm f/2.8 Macro lens',
            'Lighting: Ring flash, 45-degree incident angle',
            '',
            'Technical Analysis Notes:',
            '  - Grain structure visible at fracture surface indicates cold-working',
            '    deficiency in the base material',
            '  - Porosity measurements: 3.2% (specification max: 1.5%)',
            '  - Material hardness: 42 HRC (specification: 48-52 HRC)',
            '',
            'AUTHENTICATED BY:',
            'James Kowalski, P.E.',
            'License No. CE-48291',
            'Date: April 3, 2024',
        ]
    )

    create_pdf(
        f'{CASE_DIR}/evid_transcript.pdf',
        'DEPOSITION TRANSCRIPT - David Chen, Quality Manager',
        [
            'Case No. 2025-CV-04817',
            'DEPOSITION OF DAVID CHEN',
            'Date: May 20, 2025',
            'Location: Martinez & Calloway LLP, 633 W. 5th Street, Los Angeles',
            'Court Reporter: Sandra L. Thompson, CSR No. 12847',
            '',
            'EXAMINATION BY MS. CALLOWAY:',
            '',
            'Q: Please state your name and title for the record.',
            'A: David Chen, Quality Assurance Manager at Nexus Industrial Solutions.',
            '',
            'Q: How long have you held that position?',
            'A: Since September 2021, approximately three and a half years.',
            '',
            'Q: Were you responsible for quality control on the filtration units',
            '   shipped to Greenfield Technologies in March 2024?',
            'A: Yes, I oversaw the final inspection process.',
            '',
            'Q: What testing protocols were followed for those units?',
            'A: We performed standard dimensional checks, pressure testing at',
            '   1.5x operating pressure, and visual inspection.',
            '',
            'Q: Did you perform metallurgical analysis on the component alloys?',
            'A: No, we relied on the material certificates from our supplier.',
            '',
            'Q: Are you aware that independent testing found the alloy composition',
            '   did not meet the agreed specifications?',
            'A: I became aware of that after the complaint was filed.',
            '',
            'Q: Would metallurgical testing have detected this deficiency?',
            'A: Objection noted. Yes, it likely would have.',
            '',
            '--- PAGE BREAK ---',
            '',
            'Q: How many units from that production run were shipped?',
            'A: Twenty-four units total, across three shipments.',
        ]
    )

    create_pdf(
        f'{CASE_DIR}/evid_report.pdf',
        'EXPERT REPORT - Dr. Rajan Mehta, Metallurgical Engineering',
        [
            'Case No. 2025-CV-04817',
            'INDEPENDENT EXPERT REPORT',
            '',
            'Expert: Dr. Rajan Mehta, Ph.D., P.E.',
            'Affiliation: Stanford Materials Science Laboratory',
            'Date: July 8, 2025',
            '',
            'I. QUALIFICATIONS',
            'Dr. Mehta holds a Ph.D. in Materials Science from MIT and has 22 years',
            'of experience in failure analysis of industrial components. He has served',
            'as an expert witness in over 40 cases involving materials defects.',
            '',
            'II. MATERIALS EXAMINED',
            '  - Fractured filtration unit #FU-2024-017',
            '  - Material certificates from Nexus supplier (Changzhou Metal Works)',
            '  - Supply Agreement specifications (Exhibit A)',
            '  - Production records from Nexus (Bates No. NEX-000142 through NEX-000387)',
            '',
            'III. FINDINGS',
            '',
            'A. Alloy Composition Analysis',
            '   Specification: ASTM A351 Grade CF8M (316 SS equivalent)',
            '   Actual: Non-standard austenitic alloy with:',
            '     - Chromium: 14.2% (spec: 18-21%)',
            '     - Nickel: 7.8% (spec: 9-12%)',
            '     - Molybdenum: 1.1% (spec: 2-3%)',
            '',
            'B. Mechanical Properties',
            '   Tensile Strength: 485 MPa (spec min: 515 MPa)',
            '   Yield Strength: 195 MPa (spec min: 205 MPa)',
            '   Elongation: 28% (spec min: 30%)',
            '',
            'IV. CONCLUSIONS',
            '1. The filtration units were manufactured from substandard alloy.',
            '2. The material deficiency directly caused premature fatigue failure.',
            '3. Standard quality testing (metallurgical analysis) would have detected',
            '   this deficiency prior to shipment.',
            '',
            'V. OPINION',
            'It is my professional opinion, to a reasonable degree of engineering',
            'certainty, that the component failures were caused by material defects',
            'originating in the manufacturing process, not by improper installation.',
        ]
    )

    create_pdf(
        f'{CASE_DIR}/evid_diagram.pdf',
        'EXHIBIT E-5: Engineering Diagram - Failure Mode Analysis',
        [
            'Case No. 2025-CV-04817',
            'Exhibit E-5',
            'Prepared by: Dr. Rajan Mehta, Ph.D., P.E.',
            'Date: July 8, 2025',
            '',
            'FAILURE MODE ANALYSIS DIAGRAM',
            '',
            'Component: Primary Filtration Housing Assembly',
            'Part No: FH-200-SS316',
            '',
            '  +--------------------------------------------------+',
            '  |                UPPER FLANGE                       |',
            '  |    [Bolt Circle: 12x M16 @ 45mm PCD 320mm]       |',
            '  +=======================///========================+',
            '  |                   ///  CRACK PROPAGATION PATH     |',
            '  |                ///                                 |',
            '  |             ///    STRESS CONCENTRATION            |',
            '  |          ///       ZONE (see Detail A)             |',
            '  |       ///                                          |',
            '  |    ///                                             |',
            '  +==///=============================================+',
            '  |  COUPLING JOINT                                   |',
            '  +--------------------------------------------------+',
            '  |                LOWER SECTION                      |',
            '  +--------------------------------------------------+',
            '',
            'Legend:',
            '  /// = Fracture path (14 inches, upper flange to coupling)',
            '  Detail A: Porosity cluster at weld heat-affected zone',
            '',
            'Operating Conditions at Failure:',
            '  - Internal Pressure: 185 psi (rated: 250 psi)',
            '  - Temperature: 165 deg F (rated: 200 deg F)',
            '  - Cycles at failure: ~112,000 (expected life: >500,000)',
        ]
    )

    # Verify all files created
    files = os.listdir(CASE_DIR)
    print(f'Created {len(files)} files in {CASE_DIR}:')
    for f in sorted(files):
        size = os.path.getsize(os.path.join(CASE_DIR, f))
        print(f'  {f} ({size} bytes)')

    # Verify no bundle exists
    bundle_path = f'{WORKDIR}/legal/case_bundle.pdf'
    if os.path.exists(bundle_path):
        os.remove(bundle_path)
        print(f'Removed pre-existing bundle: {bundle_path}')

    # GUI-ready: open file manager showing case_files directory
    launch_gui(f'nautilus "{CASE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
