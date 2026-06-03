"""
Initial Setup: Create a 14-page insurance policy PDF for annotation task.
Task ID: pdf_legal_075
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_075'
PDF_DIR = f'{WORKDIR}/legal/insurance'
OUTPUT = f'{PDF_DIR}/policy_review.pdf'


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


# Insurance policy content for 14 pages
POLICY_SECTIONS = [
    # Page 1: Title / Cover page
    {
        "title": "COMPREHENSIVE GENERAL LIABILITY INSURANCE POLICY",
        "content": [
            "Policy Number: CGL-2025-487291",
            "Effective Date: January 1, 2025",
            "Expiration Date: December 31, 2025",
            "",
            "Named Insured: Meridian Technology Solutions, Inc.",
            "Principal Address: 4500 Commerce Parkway, Suite 300, Austin, TX 78731",
            "",
            "Insurance Company: Continental Assurance Group",
            "Home Office: 200 Financial Center Drive, Hartford, CT 06103",
            "",
            "Agent: Katherine M. Davenport, Licensed Agent #TX-48291",
            "Agency: Pinnacle Risk Management Services",
            "",
            "Premium Amount: $47,850.00 per annum",
            "Payment Schedule: Quarterly installments of $11,962.50",
            "",
            "THIS POLICY IS ISSUED IN CONSIDERATION OF THE APPLICATION AND PREMIUM STATED HEREIN.",
            "PLEASE READ THIS POLICY CAREFULLY.",
        ]
    },
    # Page 2: Declarations
    {
        "title": "DECLARATIONS PAGE",
        "content": [
            "SECTION I - DECLARATIONS",
            "",
            "Item 1. Named Insured and Mailing Address:",
            "   Meridian Technology Solutions, Inc.",
            "   4500 Commerce Parkway, Suite 300, Austin, TX 78731",
            "",
            "Item 2. Policy Period: From 01/01/2025 to 12/31/2025 at 12:01 A.M. standard time",
            "   at the Named Insured's mailing address.",
            "",
            "Item 3. Limits of Insurance:",
            "   General Aggregate Limit (other than Products-Completed Operations): $4,000,000",
            "   Products-Completed Operations Aggregate Limit: $2,000,000",
            "   Personal and Advertising Injury Limit (each occurrence): $1,000,000",
            "   Each Occurrence Limit: $1,000,000",
            "   Damage to Premises Rented to You (each occurrence): $300,000",
            "   Medical Expense Limit (any one person): $10,000",
            "",
            "Item 4. Retroactive Date: January 1, 2020",
            "",
            "Item 5. Business Description: Technology consulting, software development,",
            "   systems integration, and related professional services.",
            "",
            "Item 6. Premium Computation:",
            "   Classification    Code    Premium Base    Rate    Advance Premium",
            "   Tech Consulting   91583   $12,500,000     0.245   $30,625.00",
            "   Software Dev      91584   $8,200,000      0.210   $17,225.00",
            "   Total Advance Premium:                            $47,850.00",
        ]
    },
    # Page 3: Liability Coverage (KEY PAGE for annotation)
    {
        "title": "SECTION II - LIABILITY COVERAGE",
        "content": [
            "The Company agrees to pay on behalf of the Insured all sums which the Insured shall",
            "become legally obligated to pay as damages because of bodily injury or property damage",
            "to which this insurance applies, caused by an occurrence, provided that the applicable",
            "limit of the Company's liability has not been exhausted by payment of judgments or",
            "settlements. The Company shall have the right and duty to defend any suit against the",
            "Insured seeking damages on account of such bodily injury or property damage, even if",
            "any of the allegations of the suit are groundless, false, or fraudulent.",
            "",
            "A. Coverage Trigger and Scope of Protection",
            "",
            "This policy provides occurrence-based coverage for claims arising from incidents that",
            "take place during the policy period, regardless of when the claim is formally reported,",
            "subject to the provisions and conditions set forth herein. Coverage extends to the Named",
            "Insured, its officers, directors, shareholders, and employees while acting within the",
            "scope of their duties for the Named Insured.",
            "",
            "B. Supplementary Payments",
            "",
            "In addition to the limits of liability, the Company will pay:",
            "   1. All expenses incurred by the Company in the investigation, negotiation,",
            "      and defense of any claim or suit.",
            "   2. Premiums on appeal bonds and bonds to release attachments up to the",
            "      applicable limit of liability.",
            "   3. Reasonable expenses incurred by the Insured at the Company's request.",
            "   4. Court costs and prejudgment interest awarded against the Insured.",
            "   5. Post-judgment interest on that portion of any judgment within limits.",
        ]
    },
    # Page 4: Exclusions
    {
        "title": "SECTION III - EXCLUSIONS",
        "content": [
            "This insurance does not apply to:",
            "",
            "A. Expected or Intended Injury",
            "   Bodily injury or property damage expected or intended from the standpoint of the",
            "   Insured. This exclusion does not apply to bodily injury resulting from the use of",
            "   reasonable force to protect persons or property.",
            "",
            "B. Contractual Liability",
            "   Bodily injury or property damage for which the Insured is obligated to pay damages",
            "   by reason of the assumption of liability in a contract or agreement, except for",
            "   liability assumed under an insured contract as defined in Section VII.",
            "",
            "C. Liquor Liability",
            "   Bodily injury or property damage arising out of the selling, serving, or furnishing",
            "   of any alcoholic beverage by the Named Insured in the business of manufacturing,",
            "   distributing, selling, serving, or furnishing alcoholic beverages.",
            "",
            "D. Workers' Compensation and Similar Laws",
            "   Any obligation of the Insured under workers' compensation, disability benefits,",
            "   or unemployment compensation law, or any similar law.",
            "",
            "E. Employer's Liability",
            "   Bodily injury to an employee of the Insured arising out of and in the course of",
            "   employment by the Insured, except liability assumed under a sidetrack agreement.",
            "",
            "F. Pollution",
            "   Bodily injury or property damage arising out of the actual, alleged, or threatened",
            "   discharge, dispersal, seepage, migration, release, or escape of pollutants.",
        ]
    },
    # Page 5: Exclusions continued
    {
        "title": "SECTION III - EXCLUSIONS (Continued)",
        "content": [
            "G. Aircraft, Auto, or Watercraft",
            "   Bodily injury or property damage arising out of the ownership, maintenance,",
            "   operation, use, loading, or unloading of any aircraft, auto, or watercraft",
            "   owned, operated, rented, or loaned to any Insured.",
            "",
            "H. Mobile Equipment",
            "   Bodily injury or property damage arising out of the transportation of mobile",
            "   equipment by an auto owned, operated, rented, or loaned to any Insured.",
            "",
            "I. War and Terrorism",
            "   Bodily injury or property damage due to war, invasion, civil war, rebellion,",
            "   revolution, or any act of terrorism as defined by applicable federal law.",
            "",
            "J. Professional Services",
            "   Bodily injury or property damage arising out of the rendering of or failure to",
            "   render professional services. This exclusion applies to technology consulting",
            "   errors and omissions, which are covered under a separate E&O policy.",
            "",
            "K. Damage to Your Product",
            "   Property damage to your product arising out of it or any part of it.",
            "",
            "L. Damage to Your Work",
            "   Property damage to your work arising out of it or any part of it and included",
            "   in the products-completed operations hazard.",
            "",
            "M. Cyber and Data Breach",
            "   Any liability arising from unauthorized access to, or breach of, electronic",
            "   data or computer systems. Cyber coverage is provided under a separate policy.",
        ]
    },
    # Page 6: Conditions
    {
        "title": "SECTION IV - CONDITIONS",
        "content": [
            "A. Duties in the Event of Occurrence, Offense, Claim, or Suit",
            "",
            "   1. The Named Insured must see to it that the Company is notified as soon as",
            "      practicable of an occurrence or an offense which may result in a claim.",
            "   2. To the extent possible, notice should include:",
            "      a. How, when, and where the occurrence or offense took place;",
            "      b. The names and addresses of any injured persons and witnesses; and",
            "      c. The nature and location of any injury or damage arising from the event.",
            "   3. If a claim is made or suit is brought against any Insured, the Named Insured",
            "      must immediately record the specifics of the claim or suit and the date",
            "      received, and notify the Company as soon as practicable.",
            "",
            "B. Legal Action Against the Company",
            "",
            "   No person or organization has a right under this Coverage Part to join the",
            "   Company as a party or otherwise bring the Company into a suit against the",
            "   Insured, or to sue the Company on this Coverage Part unless all terms have",
            "   been fully complied with.",
            "",
            "C. Other Insurance",
            "",
            "   If other valid and collectible insurance is available to the Insured for a loss",
            "   covered under this Coverage Part, the insurance provided by this Coverage Part",
            "   shall be excess over any other valid and collectible insurance available to the",
            "   Insured, whether primary, excess, contingent, or on any other basis.",
        ]
    },
    # Page 7: Conditions continued
    {
        "title": "SECTION IV - CONDITIONS (Continued)",
        "content": [
            "D. Premium Audit",
            "",
            "   The Company shall be permitted to examine and audit all records of the Named",
            "   Insured that relate to this Coverage Part at any time during the policy period",
            "   and up to three years after the final termination date. The Named Insured shall",
            "   make records available at reasonable times at the Named Insured's offices.",
            "",
            "   If the audit reveals that the advance premium is less than the actual earned",
            "   premium, the Named Insured shall pay the additional premium due. If the advance",
            "   premium exceeds the earned premium, the Company will return the excess to the",
            "   Named Insured, subject to a minimum retained premium of $5,000.",
            "",
            "E. Representations",
            "",
            "   By accepting this policy, the Named Insured agrees that the statements in the",
            "   application are accurate and complete. Any misrepresentation or concealment of",
            "   material facts may void this policy from inception.",
            "",
            "F. Separation of Insureds",
            "",
            "   Except with respect to the limits of insurance and any rights or duties",
            "   specifically assigned to the Named Insured, this insurance applies as if each",
            "   Named Insured were the only Named Insured and separately to each Insured",
            "   against whom claim is made or suit is brought.",
            "",
            "G. Transfer of Rights Against Others to the Company",
            "",
            "   If the Insured has rights to recover all or part of any payment made under this",
            "   Coverage Part, those rights are transferred to the Company. The Insured shall do",
            "   everything necessary to secure such rights and shall do nothing to impair them.",
        ]
    },
    # Page 8: Definitions
    {
        "title": "SECTION V - DEFINITIONS",
        "content": [
            "As used in this policy:",
            "",
            "\"Bodily Injury\" means bodily injury, sickness, or disease sustained by a person,",
            "including death resulting from any of these at any time.",
            "",
            "\"Coverage Territory\" means the United States of America (including its territories",
            "and possessions), Puerto Rico, and Canada. Coverage also extends to international",
            "waters and airspace, provided the claim is made in the Coverage Territory.",
            "",
            "\"Impaired Property\" means tangible property, other than your product or your work,",
            "that cannot be used or is less useful because it incorporates your product or your",
            "work that is known or thought to be defective, deficient, inadequate, or dangerous.",
            "",
            "\"Insured Contract\" means:",
            "   a. A contract for a lease of premises;",
            "   b. A sidetrack agreement;",
            "   c. Any easement or license agreement;",
            "   d. An obligation required by ordinance to indemnify a municipality;",
            "   e. An elevator maintenance agreement; or",
            "   f. That part of any other contract pertaining to the Named Insured's business.",
            "",
            "\"Loading or Unloading\" means the handling of property after it is moved from the",
            "place where it is accepted for movement into or onto an aircraft, watercraft, or",
            "auto, and until it is moved from the aircraft, watercraft, or auto to the place",
            "where it is finally delivered.",
            "",
            "\"Occurrence\" means an accident, including continuous or repeated exposure to",
            "substantially the same general harmful conditions.",
        ]
    },
    # Page 9: Definitions continued
    {
        "title": "SECTION V - DEFINITIONS (Continued)",
        "content": [
            "\"Personal and Advertising Injury\" means injury, including consequential bodily",
            "injury, arising out of one or more of the following offenses:",
            "   a. False arrest, detention, or imprisonment;",
            "   b. Malicious prosecution;",
            "   c. The wrongful eviction from, or wrongful entry into, a room, dwelling,",
            "      or premises that a person occupies;",
            "   d. Oral or written publication of material that slanders or libels a person",
            "      or organization, or disparages their goods, products, or services;",
            "   e. Oral or written publication of material that violates a person's right",
            "      of privacy;",
            "   f. The use of another's advertising idea in your advertisement; or",
            "   g. Infringing upon another's copyright, trade dress, or slogan.",
            "",
            "\"Pollutants\" means any solid, liquid, gaseous, or thermal irritant or contaminant,",
            "including smoke, vapor, soot, fumes, acids, alkalis, chemicals, and waste.",
            "",
            "\"Products-Completed Operations Hazard\" includes all bodily injury and property",
            "damage occurring away from premises owned or rented by the Named Insured and",
            "arising out of the Named Insured's product or work.",
            "",
            "\"Property Damage\" means:",
            "   a. Physical injury to tangible property, including all resulting loss of use of",
            "      that property. All such loss of use shall be deemed to occur at the time of",
            "      the physical injury that caused it; or",
            "   b. Loss of use of tangible property that is not physically injured. All such",
            "      loss of use shall be deemed to occur at the time of the occurrence that",
            "      caused it.",
        ]
    },
    # Page 10: Endorsements
    {
        "title": "ENDORSEMENT NO. 1 - ADDITIONAL INSURED",
        "content": [
            "ADDITIONAL INSURED - MANAGERS OR LESSORS OF PREMISES",
            "",
            "This endorsement modifies insurance provided under the Commercial General",
            "Liability Coverage Part.",
            "",
            "Schedule of Additional Insureds:",
            "",
            "   1. Apex Commercial Properties, LLC",
            "      4500 Commerce Parkway, Austin, TX 78731",
            "      Interest: Lessor of premises occupied by Named Insured",
            "",
            "   2. Metropolitan Office Trust",
            "      1200 Congress Avenue, Suite 800, Austin, TX 78701",
            "      Interest: Building management company",
            "",
            "   3. Greater Austin Technology Council",
            "      901 West Riverside Drive, Austin, TX 78704",
            "      Interest: Event venue host for industry conferences",
            "",
            "The person or organization shown in the schedule is an Additional Insured only",
            "with respect to liability arising out of the ownership, maintenance, or use of",
            "that part of the premises leased to the Named Insured.",
            "",
            "The insurance afforded to the Additional Insured does not apply to any occurrence",
            "which takes place after the Named Insured ceases to be a tenant in that premises.",
            "",
            "Coverage for the Additional Insured is limited to the lesser of:",
            "   a. The limits of liability shown in the Declarations; or",
            "   b. The limits required by the written contract or agreement.",
        ]
    },
    # Page 11: Endorsement 2
    {
        "title": "ENDORSEMENT NO. 2 - WAIVER OF SUBROGATION",
        "content": [
            "WAIVER OF TRANSFER OF RIGHTS OF RECOVERY AGAINST OTHERS TO THE COMPANY",
            "",
            "This endorsement modifies insurance provided under the Commercial General",
            "Liability Coverage Part.",
            "",
            "The following is added to Section IV - Conditions:",
            "",
            "Transfer of Rights Against Others to the Company - Waiver",
            "",
            "We waive any right of recovery we may have against the person or organization",
            "shown in the Schedule below because of payments we make for injury or damage",
            "arising out of the Named Insured's ongoing operations or your work done under",
            "a contract with that person or organization and included in the products-completed",
            "operations hazard.",
            "",
            "Schedule:",
            "",
            "   1. Apex Commercial Properties, LLC",
            "      Effective: 01/01/2025 - 12/31/2025",
            "      Per Lease Agreement dated November 15, 2024",
            "",
            "   2. DataStream Analytics, Inc.",
            "      Effective: 01/01/2025 - 12/31/2025",
            "      Per Master Services Agreement dated September 3, 2024",
            "",
            "   3. Federal Systems Integration Corp.",
            "      Effective: 03/01/2025 - 12/31/2025",
            "      Per Subcontractor Agreement dated February 12, 2025",
            "",
            "This waiver applies only to the person or organization shown in the Schedule",
            "and only for operations or work specified in the applicable agreement.",
        ]
    },
    # Page 12: Endorsement 3
    {
        "title": "ENDORSEMENT NO. 3 - AMENDED AGGREGATE LIMITS",
        "content": [
            "DESIGNATED LOCATION(S) GENERAL AGGREGATE LIMIT",
            "",
            "This endorsement modifies insurance provided under the Commercial General",
            "Liability Coverage Part.",
            "",
            "Schedule:",
            "   Designated Location: 4500 Commerce Parkway, Suite 300, Austin, TX 78731",
            "   Designated Location General Aggregate Limit: $4,000,000",
            "",
            "A. For all sums which the Insured becomes legally obligated to pay as damages",
            "   caused by occurrences under Section II - Liability Coverage, and for all",
            "   medical expenses under Section II arising from occurrences at the designated",
            "   location, a separate Designated Location General Aggregate Limit applies.",
            "",
            "B. The Designated Location General Aggregate Limit is the most the Company",
            "   will pay for the sum of all damages under Section II, except damages included",
            "   in the Products-Completed Operations Aggregate Limit.",
            "",
            "C. Any payments made under Section II for damages or medical expenses shall",
            "   reduce the Designated Location General Aggregate Limit for that location.",
            "   They shall not reduce any other Designated Location General Aggregate Limit",
            "   or the General Aggregate Limit under the Declarations.",
            "",
            "D. The limits shown in the Declarations for Each Occurrence, Damage to Premises",
            "   Rented to You, and Medical Expense continue to apply. However, instead of",
            "   being subject to the General Aggregate Limit in the Declarations, these limits",
            "   will be subject to the Designated Location General Aggregate Limit.",
        ]
    },
    # Page 13: Claims History
    {
        "title": "SCHEDULE OF PRIOR CLAIMS AND LOSSES",
        "content": [
            "The following is a summary of claims and losses reported during the prior",
            "policy period (January 1, 2024 to December 31, 2024):",
            "",
            "Claim #1:",
            "   Date of Loss: March 14, 2024",
            "   Claimant: Riverside Medical Center",
            "   Nature: Property damage - water leak from server room",
            "   Status: Closed",
            "   Paid: $23,450.00 (property damage repair)",
            "   Reserved: $0.00",
            "",
            "Claim #2:",
            "   Date of Loss: July 8, 2024",
            "   Claimant: Patricia Gonzalez (visitor)",
            "   Nature: Bodily injury - slip and fall in lobby",
            "   Status: Closed",
            "   Paid: $8,750.00 (medical expenses and settlement)",
            "   Reserved: $0.00",
            "",
            "Claim #3:",
            "   Date of Loss: October 22, 2024",
            "   Claimant: TechBridge Solutions, LLC",
            "   Nature: Property damage - software deployment error",
            "   Status: Open - under investigation",
            "   Paid: $0.00",
            "   Reserved: $175,000.00",
            "",
            "Total Incurred Losses (2024): $207,200.00",
            "Current Loss Ratio: 4.33%",
        ]
    },
    # Page 14: Signatures
    {
        "title": "EXECUTION AND ATTESTATION",
        "content": [
            "IN WITNESS WHEREOF, the Company has caused this policy to be executed and",
            "attested as of the effective date stated in the Declarations.",
            "",
            "",
            "CONTINENTAL ASSURANCE GROUP",
            "",
            "",
            "______________________________________",
            "Robert A. Whitfield",
            "President and Chief Executive Officer",
            "",
            "",
            "______________________________________",
            "Sandra L. Morrison, CPCU, ARM",
            "Vice President, Commercial Lines Underwriting",
            "",
            "",
            "______________________________________",
            "James T. O'Brien",
            "Secretary",
            "",
            "",
            "Countersigned by:",
            "",
            "______________________________________",
            "Katherine M. Davenport",
            "Licensed Agent #TX-48291",
            "Pinnacle Risk Management Services",
            "Date: December 20, 2024",
            "",
            "",
            "This policy contains 14 pages including Declarations, Coverage Forms,",
            "and Endorsements. All pages are integral parts of this policy.",
        ]
    },
]


def create_initial():
    os.makedirs(PDF_DIR, exist_ok=True)

    doc = pymupdf.open()

    for i, section in enumerate(POLICY_SECTIONS):
        # Use letter size for US legal documents
        page = doc.new_page(width=612, height=792)

        # Page header
        page.insert_text(
            pymupdf.Point(72, 40),
            "Continental Assurance Group - Policy CGL-2025-487291",
            fontsize=8,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )
        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 48), pymupdf.Point(540, 48))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

        # Section title
        page.insert_text(
            pymupdf.Point(72, 75),
            section["title"],
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0.4),
        )

        # Content - starting at y=100 to fill the region around (72,100)-(540,200) on page 3
        y_pos = 100
        for line in section["content"]:
            if y_pos > 740:
                break
            if line == "":
                y_pos += 8
                continue
            # Use textbox for long lines to auto-wrap
            rect = pymupdf.Rect(72, y_pos, 540, y_pos + 14)
            page.insert_textbox(
                rect,
                line,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            y_pos += 14

        # Page footer
        page.insert_text(
            pymupdf.Point(280, 770),
            f"Page {i + 1} of 14",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )
        # Footer line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 755), pymupdf.Point(540, 755))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince on page 3 for the agent
    launch_gui(f'evince --page-index=3 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
