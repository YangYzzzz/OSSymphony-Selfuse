"""
Initial Setup: Create a 35-page insurance policy PDF with multiple occurrences of 'liability'
Task ID: pdf_fm_023
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_023'
DOC_DIR = f'{WORKDIR}/Documents/legal'
OUTPUT = f'{DOC_DIR}/insurance_policy.pdf'

# Page dimensions (Letter size)
PAGE_W, PAGE_H = 612, 792

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

def add_page_text(doc, title, body_paragraphs, page_num):
    """Add a page with title and body text."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Page header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 50), pymupdf.Point(PAGE_W - 50, 50))
    shape.finish(color=(0.2, 0.2, 0.5), width=1.5)
    shape.commit()

    # Header text
    page.insert_text(
        pymupdf.Point(50, 45),
        "COMPREHENSIVE INSURANCE POLICY  |  Policy No. INS-2024-78432",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Title
    page.insert_text(
        pymupdf.Point(50, 80),
        title,
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.3),
    )

    # Body text
    y_pos = 110
    for para in body_paragraphs:
        rect = pymupdf.Rect(50, y_pos, PAGE_W - 50, PAGE_H - 60)
        excess = page.insert_textbox(
            rect,
            para,
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )
        # Estimate how much vertical space was used
        lines_approx = len(para) / 80  # rough chars per line
        y_pos += lines_approx * 13 + 15
        if y_pos > PAGE_H - 80:
            break

    # Footer
    page.insert_text(
        pymupdf.Point(50, PAGE_H - 40),
        f"Page {page_num}",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )
    page.insert_text(
        pymupdf.Point(PAGE_W - 250, PAGE_H - 40),
        "Meridian National Insurance Group",
        fontsize=8,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )
    return page


def create_initial():
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- COVER PAGE (Page 1) ----
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(150, 200), "MERIDIAN NATIONAL", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(140, 240), "INSURANCE GROUP", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(130, 310), "Comprehensive Insurance Policy", fontsize=18, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(180, 370), "Policy Number: INS-2024-78432", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(180, 390), "Effective Date: March 1, 2024", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(180, 410), "Expiration Date: February 28, 2025", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(180, 440), "Policyholder: Westbrook Manufacturing, Inc.", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(180, 460), "Agent: Patricia Navarro, CLU, ChFC", fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(150, 550), "CONFIDENTIAL - FOR POLICYHOLDER USE ONLY", fontsize=10, fontname="hebo", color=(0.6, 0.1, 0.1))

    # The actual insurance policy content with 'liability' appearing naturally
    # Each entry: (title, [paragraphs])
    sections = [
        # Page 2 - Table of Contents
        ("TABLE OF CONTENTS", [
            "Section I: Definitions and General Provisions .......................... 3\n"
            "Section II: General Liability Coverage ................................ 5\n"
            "Section III: Product Liability Insurance .............................. 8\n"
            "Section IV: Professional Liability Protection ........................ 11\n"
            "Section V: Property Coverage and Endorsements ........................ 14\n"
            "Section VI: Workers' Compensation and Employer's Liability ........... 17\n"
            "Section VII: Commercial Auto Liability ............................... 20\n"
            "Section VIII: Umbrella Liability Coverage ............................ 23\n"
            "Section IX: Cyber Liability and Data Breach Response ................. 26\n"
            "Section X: Environmental Liability .................................. 29\n"
            "Section XI: Claims Procedures and Dispute Resolution ................. 31\n"
            "Section XII: Exclusions, Conditions, and Endorsements ................ 33\n",
        ]),
        # Page 3 - Definitions
        ("SECTION I: DEFINITIONS AND GENERAL PROVISIONS", [
            "1.1 DEFINITIONS. For the purposes of this policy, the following terms shall have the meanings set forth below unless the context clearly indicates otherwise.",
            "\"Bodily Injury\" means physical injury, sickness, or disease sustained by a person, including death resulting from any of these at any time. This definition extends to mental anguish or emotional distress when arising from bodily injury as defined herein.",
            "\"Claim\" means a written demand for monetary damages or equitable relief arising from an occurrence. A claim includes any civil proceeding, arbitration demand, or regulatory action that alleges liability on the part of the insured.",
            "\"Coverage Territory\" means the United States of America, its territories and possessions, Puerto Rico, and Canada. International liability coverage may apply where endorsed separately.",
            "\"Insured\" means the Named Insured and any person or organization qualifying as an insured under the terms of this policy. Additional insureds may be added by endorsement. The liability of the insurer extends only to covered events.",
            "\"Occurrence\" means an accident, including continuous or repeated exposure to substantially the same general harmful conditions, that results in bodily injury or property damage. Each occurrence may give rise to a separate liability assessment under this policy.",
        ]),
        # Page 4 - More Definitions
        ("SECTION I: DEFINITIONS (CONTINUED)", [
            "\"Personal Injury\" means injury other than bodily injury arising out of false arrest, detention, imprisonment, malicious prosecution, wrongful eviction, invasion of privacy, or defamation. Personal injury liability is subject to the terms and conditions of this policy.",
            "\"Pollutant\" means any solid, liquid, gaseous, or thermal irritant or contaminant. Environmental liability related to pollutants is covered under Section X of this policy.",
            "\"Property Damage\" means physical injury to tangible property, including resulting loss of use of that property, or loss of use of tangible property that is not physically injured. The insurer's liability for property damage is subject to the limits stated in the Declarations.",
            "\"Suit\" means a civil proceeding in which monetary damages or equitable relief to which this insurance applies are alleged. Suit includes arbitration proceedings and any other alternative dispute resolution proceeding in which such relief is sought. The insurer has the right and duty to defend any suit seeking damages that may trigger liability under this policy.",
            "1.2 GENERAL PROVISIONS. This policy is a contract of indemnity whereby the insurer agrees to pay on behalf of the insured all sums that the insured becomes legally obligated to pay as damages because of liability imposed by law or assumed under contract, subject to all terms, conditions, and limitations of this policy.",
            "1.3 POLICY PERIOD AND TERRITORY. Coverage applies to occurrences taking place within the policy period and within the coverage territory. The insurer's liability shall not exceed the limits of insurance stated in the Declarations, regardless of the number of insureds, claims, or claimants.",
        ]),
        # Page 5 - General Liability
        ("SECTION II: GENERAL LIABILITY COVERAGE", [
            "2.1 INSURING AGREEMENT. The insurer will pay those sums that the insured becomes legally obligated to pay as damages because of bodily injury or property damage to which this liability coverage applies. General liability insurance provides foundational protection for business operations.",
            "The insurer has the right and duty to defend the insured against any suit seeking damages for bodily injury or property damage. The liability to defend ends when the applicable limit of insurance has been exhausted by payment of judgments or settlements.",
            "2.2 COVERAGE A: BODILY INJURY AND PROPERTY DAMAGE LIABILITY. This insurance applies to bodily injury and property damage only if the injury or damage is caused by an occurrence that takes place in the coverage territory during the policy period.",
            "The general liability coverage responds to claims arising from the insured's premises, operations, products, and completed operations. The per-occurrence limit of liability for Coverage A is $2,000,000 with a general aggregate limit of $5,000,000.",
            "2.3 COVERAGE B: PERSONAL AND ADVERTISING INJURY LIABILITY. This liability coverage applies to personal and advertising injury caused by an offense arising out of the insured's business operations. The limit of liability for Coverage B is $1,000,000 per occurrence.",
            "Personal and advertising injury liability does not apply to injury arising out of willful violation of a penal statute or ordinance committed by or with the consent of the insured, nor to any liability assumed under contract except as permitted by this policy.",
        ]),
        # Page 6 - General Liability Continued
        ("SECTION II: GENERAL LIABILITY (CONTINUED)", [
            "2.4 MEDICAL PAYMENTS COVERAGE. The insurer will pay medical expenses for bodily injury caused by an accident on premises the insured owns or rents, or because of the insured's operations. Medical payments coverage does not constitute an admission of liability.",
            "The medical expense limit is $10,000 per person. This coverage applies regardless of fault and is intended to provide immediate relief for minor injuries without requiring the claimant to establish the insured's liability.",
            "2.5 SUPPLEMENTARY PAYMENTS. In addition to the limits of liability, the insurer will pay: (a) all expenses incurred by the insurer in the investigation, defense, and settlement of any claim or suit; (b) premiums on bonds required in any suit defended by the insurer; (c) reasonable expenses incurred by the insured at the insurer's request.",
            "The insurer's liability for supplementary payments is in addition to the applicable limits of insurance. These payments do not reduce the available limits of liability under this policy.",
            "2.6 AGGREGATE LIMITS. The general aggregate limit is the most the insurer will pay for the sum of all damages under Coverage A and Coverage B and for medical expenses. The products-completed operations aggregate limit governs liability arising from the insured's products and completed operations.",
            "When the aggregate limit of liability is exhausted, the insurer has no further obligation to pay damages or defend any additional suits. The insured is responsible for any liability in excess of the policy limits.",
        ]),
        # Page 7 - General Liability Exclusions
        ("SECTION II: GENERAL LIABILITY EXCLUSIONS", [
            "2.7 EXCLUSIONS. This liability coverage does not apply to: (a) expected or intended injury from the standpoint of the insured; (b) contractual liability except where the insured has assumed liability in an insured contract; (c) liquor liability for insureds in the business of manufacturing, distributing, selling, or serving alcoholic beverages.",
            "Additional exclusions to general liability coverage include: (d) workers' compensation and similar laws; (e) employer's liability, which is addressed separately in Section VI; (f) pollution liability, addressed in Section X; (g) aircraft, auto, or watercraft liability, except as provided in Section VII.",
            "Professional services liability is excluded from general liability coverage and is instead covered under Section IV of this policy. The insured should review all applicable liability sections to ensure comprehensive understanding of coverage.",
            "War, terrorism, and nuclear hazard exclusions apply across all liability sections of this policy. The insurer assumes no liability for losses arising directly or indirectly from these excluded perils.",
            "The liability exclusions set forth in this section apply to all coverages under Section II unless specifically modified by endorsement. Any conflict between an exclusion and an endorsement shall be resolved in favor of the endorsement.",
        ]),
        # Page 8 - Product Liability
        ("SECTION III: PRODUCT LIABILITY INSURANCE", [
            "3.1 PRODUCTS-COMPLETED OPERATIONS LIABILITY. This section covers the insured's liability for bodily injury and property damage arising from the insured's products or completed operations. Product liability protection is essential for manufacturing enterprises.",
            "The products-completed operations hazard includes all bodily injury and property damage occurring away from premises owned by or rented to the insured and arising out of the insured's product or work. Product liability extends to goods distributed, sold, or handled by the insured.",
            "3.2 PRODUCT LIABILITY LIMITS. The products-completed operations aggregate limit of liability is $3,000,000. This limit applies separately from the general aggregate. Each occurrence involving product liability is subject to the per-occurrence limit of $2,000,000.",
            "Product liability coverage includes the cost of defense, which is paid in addition to the liability limits. The insurer will provide experienced product liability defense counsel at no additional cost to the insured.",
            "3.3 PRODUCT RECALL. This policy provides limited product recall liability coverage. In the event the insured's product is found to be defective, the insurer will reimburse reasonable recall expenses up to $500,000 per recall event. Product recall liability is subject to a $25,000 deductible.",
            "The insured must notify the insurer within 48 hours of becoming aware of any product defect that may give rise to product liability claims. Failure to provide timely notice may prejudice the insurer's ability to manage the liability exposure.",
        ]),
        # Page 9 - Product Liability Continued
        ("SECTION III: PRODUCT LIABILITY (CONTINUED)", [
            "3.4 VENDOR'S LIABILITY. When required by contract, vendors selling the insured's products may be included as additional insureds for product liability purposes. Vendor liability coverage applies only to bodily injury or property damage arising from the insured's products.",
            "The vendor's liability protection does not extend to: (a) products that have been materially altered by the vendor; (b) liability arising from the vendor's own acts or omissions; (c) product liability claims unrelated to the insured's products.",
            "3.5 COMPLETED OPERATIONS LIABILITY. Completed operations liability coverage applies to bodily injury or property damage arising from the insured's work after it has been completed or abandoned. This liability coverage is triggered when the work is performed for others.",
            "The completed operations liability period begins when the insured's work is completed at the job site or when the insured has abandoned the work. Ongoing operations at the job site are covered under the general liability provisions of Section II.",
            "3.6 PRODUCT LIABILITY ENDORSEMENTS. The following endorsements are available to modify product liability coverage: (a) extended product liability for international distribution; (b) component parts liability endorsement; (c) sistership liability exclusion modification.",
            "Each product liability endorsement may be added for an additional premium. The insured should consult with their agent regarding the specific liability exposures of their product lines to ensure adequate coverage.",
        ]),
        # Page 10 - Product Liability Claims
        ("SECTION III: PRODUCT LIABILITY CLAIMS PROCEDURES", [
            "3.7 REPORTING PRODUCT LIABILITY CLAIMS. Upon receiving notice of any product liability claim, the insured must promptly forward to the insurer every demand, notice, summons, or other process received. Timely reporting of product liability claims is essential.",
            "The insured shall cooperate fully with the insurer in the investigation, settlement, and defense of any product liability claim. The insurer reserves the right to settle any product liability claim within the applicable limits of liability without the consent of the insured.",
            "3.8 PRODUCT LIABILITY DEFENSE. The insurer has the right to appoint defense counsel for all product liability claims. The insured may request specific counsel, subject to the insurer's approval. All defense costs for product liability claims are paid in addition to the limits of liability.",
            "In multi-party product liability litigation, the insurer will coordinate defense efforts with other potentially liable parties and their insurers. The insured's liability share will be determined through contribution and indemnification agreements.",
            "3.9 PRODUCT LIABILITY RESERVES. The insurer will establish appropriate reserves for each product liability claim. Reserve amounts reflect the insurer's assessment of potential liability exposure and defense costs.",
        ]),
        # Page 11 - Professional Liability
        ("SECTION IV: PROFESSIONAL LIABILITY PROTECTION", [
            "4.1 PROFESSIONAL LIABILITY INSURING AGREEMENT. The insurer agrees to pay on behalf of the insured all sums arising from claims of professional negligence, errors, or omissions. Professional liability coverage is written on a claims-made basis.",
            "Professional liability, also known as errors and omissions liability, responds to claims alleging failure to render professional services or negligent acts in the performance of professional duties. This liability coverage is distinct from general liability.",
            "4.2 PROFESSIONAL LIABILITY LIMITS. The per-claim limit of professional liability is $1,000,000 with an annual aggregate limit of $3,000,000. The professional liability deductible is $10,000 per claim, applicable to both damages and defense costs.",
            "Professional liability coverage includes defense costs within the limit of liability, unlike general liability where defense is provided in addition to limits. This distinction is important for managing the insured's professional liability exposure.",
            "4.3 PROFESSIONAL LIABILITY RETROACTIVE DATE. The retroactive date for professional liability coverage is January 1, 2020. Claims arising from professional acts or omissions occurring before this date are excluded from coverage. The professional liability coverage period extends through the policy expiration date.",
            "Extended reporting periods are available for professional liability coverage. Upon termination of the policy, the insured may purchase an extended reporting period of 12, 24, or 36 months for an additional premium of 75%, 125%, or 175% of the expiring professional liability premium.",
        ]),
        # Page 12 - Professional Liability Continued
        ("SECTION IV: PROFESSIONAL LIABILITY (CONTINUED)", [
            "4.4 PROFESSIONAL LIABILITY EXCLUSIONS. Professional liability coverage does not apply to: (a) claims arising from dishonest, fraudulent, criminal, or malicious acts; (b) liability for bodily injury or property damage, which is covered under general liability; (c) claims arising from prior known circumstances.",
            "Contractual professional liability is excluded unless the contract was executed in the ordinary course of the insured's professional practice. The professional liability section does not cover liability assumed under hold harmless agreements.",
            "4.5 TECHNOLOGY PROFESSIONAL LIABILITY. For insureds providing technology services, this section extends professional liability coverage to include: (a) failure of technology products to perform; (b) security breaches arising from professional services; (c) unintentional infringement of intellectual property rights.",
            "Technology professional liability has a separate sub-limit of $500,000 per claim, which is part of and not in addition to the overall professional liability limit. The technology liability sub-limit reflects the specialized nature of technology exposures.",
            "4.6 PROFESSIONAL LIABILITY CLAIMS MANAGEMENT. The insurer shall have the right to investigate, negotiate, and settle any professional liability claim. The insured's consent to settlement is required for claims exceeding $100,000, but such consent shall not be unreasonably withheld.",
        ]),
        # Page 13 - Professional Liability Management
        ("SECTION IV: PROFESSIONAL LIABILITY MANAGEMENT", [
            "4.7 RISK MANAGEMENT. The insurer provides professional liability risk management resources including: (a) contract review services to identify potential liability exposures; (b) continuing education programs on professional liability topics; (c) industry-specific liability alerts.",
            "Participation in professional liability risk management programs may qualify the insured for premium credits of up to 10%. The insurer's risk management recommendations do not constitute legal advice and do not reduce the insurer's liability under this policy.",
            "4.8 DISCIPLINARY PROCEEDINGS. Professional liability coverage extends to disciplinary proceedings brought by a regulatory body against the insured for professional conduct. The liability coverage for disciplinary proceedings has a sub-limit of $100,000 per proceeding.",
            "The insured must notify the insurer within 30 days of receiving notice of any disciplinary proceeding. Professional liability defense counsel will be provided for covered disciplinary matters.",
            "4.9 VICARIOUS PROFESSIONAL LIABILITY. The insured is covered for vicarious professional liability arising from the professional acts or omissions of employees, independent contractors, and subcontractors performing professional services on behalf of the insured.",
        ]),
        # Page 14 - Property Coverage
        ("SECTION V: PROPERTY COVERAGE AND ENDORSEMENTS", [
            "5.1 COMMERCIAL PROPERTY COVERAGE. This section provides protection for the insured's real and personal property against direct physical loss or damage. Property coverage is subject to the perils, conditions, and exclusions stated herein.",
            "The covered property includes: (a) buildings at scheduled locations; (b) business personal property; (c) property of others in the insured's care, custody, or control. The insurer's liability for property of others is limited to the declared value.",
            "5.2 PROPERTY VALUATION. Buildings are insured at replacement cost without deduction for depreciation. Business personal property is insured at actual cash value unless the replacement cost endorsement applies. Property valuation does not affect the insurer's liability limits.",
            "The insured is required to maintain insurance to at least 80% of the replacement cost of covered property. Failure to meet this requirement may result in a coinsurance penalty, reducing the insurer's liability for partial losses.",
            "5.3 BUSINESS INCOME COVERAGE. The insurer will pay the actual loss of business income sustained during the period of restoration following a covered property loss. Business income liability is limited to 12 months of actual demonstrated loss.",
            "Extra expense coverage provides reimbursement for reasonable costs to minimize the suspension of business operations. The combined limit of liability for business income and extra expense is $1,000,000 per occurrence.",
        ]),
        # Page 15 - Property Continued
        ("SECTION V: PROPERTY COVERAGE (CONTINUED)", [
            "5.4 PROPERTY DEDUCTIBLES. The standard property deductible is $5,000 per occurrence. Higher deductibles of $10,000, $25,000, or $50,000 are available for reduced premiums. Wind and hail losses are subject to a separate 2% deductible based on the building value.",
            "The deductible applies per occurrence for property losses. Earthquake and flood deductibles apply separately and are stated on the Declarations page. The insurer's liability is reduced by the applicable deductible amount.",
            "5.5 INLAND MARINE COVERAGE. Scheduled equipment and property in transit are covered under inland marine provisions. The insurer's liability for inland marine losses is limited to the scheduled value of each item. Pairs and sets coverage applies.",
            "Contractors' equipment is covered on a replacement cost basis for losses occurring within the coverage territory. The inland marine liability limit must be updated annually to reflect current replacement costs.",
            "5.6 EQUIPMENT BREAKDOWN. The insurer covers direct physical loss arising from equipment breakdown of covered equipment. Equipment breakdown liability includes the cost of repair or replacement and resulting business income loss.",
            "The equipment breakdown limit of liability is $2,000,000 per occurrence. Hazardous substances contamination resulting from equipment breakdown has a sub-limit of liability of $250,000 per occurrence.",
        ]),
        # Page 16 - Property Exclusions
        ("SECTION V: PROPERTY EXCLUSIONS AND CONDITIONS", [
            "5.7 PROPERTY EXCLUSIONS. Property coverage does not apply to: (a) accounts, bills, currency, money, or securities; (b) animals unless specifically scheduled; (c) automobiles held for sale; (d) bridges, roadways, and pavements; (e) property in transit except as covered by inland marine.",
            "Additional property exclusions include: (f) wear and tear; (g) rust, corrosion, or gradual deterioration; (h) mechanical breakdown not covered under equipment breakdown; (i) settling, cracking, or expansion of buildings. The insurer's liability does not extend to these excluded causes of loss.",
            "5.8 PROTECTIVE SAFEGUARDS. The insured warrants the following protective safeguards are maintained: automatic sprinkler system (P-1), automatic fire alarm (P-2), security service (P-3). Failure to maintain required safeguards may void the insurer's liability for related losses.",
            "5.9 VACANCY CONDITION. If a building is vacant for more than 60 consecutive days, the insurer's liability is reduced by 15% and coverage for vandalism, sprinkler leakage, and glass breakage is suspended entirely.",
            "5.10 ORDINANCE OR LAW COVERAGE. The insurer provides coverage for increased costs arising from enforcement of building codes following a covered property loss. The liability for ordinance or law coverage is $500,000 per occurrence.",
        ]),
        # Page 17 - Workers Comp
        ("SECTION VI: WORKERS' COMPENSATION AND EMPLOYER'S LIABILITY", [
            "6.1 WORKERS' COMPENSATION INSURING AGREEMENT. The insurer will pay promptly all compensation and other benefits required by the workers' compensation law of the states listed on the Declarations. Workers' compensation is a statutory liability independent of fault.",
            "6.2 EMPLOYER'S LIABILITY INSURING AGREEMENT. The insurer will pay all sums the insured legally must pay as damages because of bodily injury to an employee arising out of and in the course of employment. Employer's liability coverage complements workers' compensation by covering claims not governed by statute.",
            "Employer's liability limits: $500,000 each accident, $500,000 disease (each employee), $500,000 disease (policy limit). The employer's liability coverage applies to claims brought by employees outside of the workers' compensation system.",
            "6.3 STOP GAP LIABILITY. In monopolistic state fund states, stop gap employer's liability coverage fills the gap between the state fund and the insured's liability exposure. Stop gap liability limits mirror the employer's liability limits.",
            "6.4 VOLUNTARY COMPENSATION. The insurer agrees to pay benefits that would be payable under workers' compensation law to employees not otherwise covered by statute. Voluntary compensation liability applies to officers, partners, and sole proprietors who have elected exclusion.",
            "The insurer's liability for voluntary compensation is limited to benefits that would be payable if the workers' compensation law applied. This coverage does not create any liability beyond statutory benefits.",
        ]),
        # Page 18 - Workers Comp Continued
        ("SECTION VI: WORKERS' COMPENSATION (CONTINUED)", [
            "6.5 OTHER STATES COVERAGE. Workers' compensation and employer's liability coverage extends to states not listed on the Declarations if the insured begins operations in those states during the policy period. The insured must notify the insurer within 30 days.",
            "6.6 EXPERIENCE MODIFICATION. The insured's workers' compensation premium is modified by the experience modification factor assigned by the applicable rating bureau. Current experience modification factor: 0.92 (indicating better than average loss experience).",
            "6.7 SAFETY AND LOSS CONTROL. The insurer provides safety and loss control services including workplace inspections, safety program development, and OSHA compliance assistance. These services reduce the insured's liability exposure over time.",
            "Participation in the insurer's safety dividend program may result in a return premium of up to 5% of the workers' compensation premium. Safety dividends reflect the insured's commitment to reducing employer's liability claims.",
            "6.8 SUBROGATION. The insurer retains the right of subrogation against third parties whose negligence caused a workers' compensation or employer's liability claim. The insured must cooperate with all subrogation efforts.",
        ]),
        # Page 19 - Workers Comp Exclusions
        ("SECTION VI: EMPLOYER'S LIABILITY EXCLUSIONS", [
            "6.9 EMPLOYER'S LIABILITY EXCLUSIONS. The employer's liability coverage does not apply to: (a) liability assumed under contract; (b) punitive damages arising from employee injury; (c) liability arising from employment practices, which is covered under a separate EPLI policy.",
            "Additional employer's liability exclusions: (d) bodily injury to any person employed in violation of law; (e) liability for discrimination claims; (f) intentional injury directed by the insured. These exclusions apply to employer's liability coverage only.",
            "6.10 DUAL CAPACITY LIABILITY. The employer's liability section does not cover claims brought by employees under a dual capacity theory where the insured acts in a capacity other than employer. Dual capacity liability may be covered under general liability or product liability sections.",
            "6.11 THIRD-PARTY-OVER ACTIONS. Employer's liability coverage responds to third-party-over actions where an injured employee sues a third party who then seeks contribution or indemnification from the insured employer. The employer's liability limits apply to such claims.",
            "6.12 OCCUPATIONAL DISEASE LIABILITY. The insurer covers employer's liability claims arising from occupational diseases contracted by employees during the policy period. Long-latency occupational disease liability is subject to the disease policy limit.",
        ]),
        # Page 20 - Auto Liability
        ("SECTION VII: COMMERCIAL AUTO LIABILITY", [
            "7.1 AUTO LIABILITY INSURING AGREEMENT. The insurer will pay all sums the insured legally must pay as damages because of bodily injury or property damage caused by an auto accident. Commercial auto liability coverage applies to owned, hired, and non-owned automobiles.",
            "7.2 AUTO LIABILITY LIMITS. The combined single limit of auto liability is $1,000,000 per accident. This limit applies to the sum of bodily injury and property damage liability arising from any one auto accident.",
            "Split limits are available as an alternative: $500,000 per person bodily injury liability, $1,000,000 per accident bodily injury liability, and $250,000 property damage liability per accident.",
            "7.3 HIRED AUTO LIABILITY. The insurer covers the insured's liability for bodily injury or property damage arising from the use of hired automobiles. Hired auto liability applies to vehicles rented, leased, or borrowed for business purposes.",
            "7.4 NON-OWNED AUTO LIABILITY. This coverage applies to the insured's liability arising from the use of non-owned automobiles by employees in the course of business. Non-owned auto liability does not cover the vehicle itself.",
            "7.5 UNINSURED/UNDERINSURED MOTORIST COVERAGE. Where required by law, the insurer provides uninsured and underinsured motorist coverage. The UM/UIM liability limit matches the bodily injury liability limit.",
        ]),
        # Page 21 - Auto Continued
        ("SECTION VII: COMMERCIAL AUTO (CONTINUED)", [
            "7.6 AUTO PHYSICAL DAMAGE. Comprehensive and collision coverage applies to scheduled owned automobiles. The insurer's liability for physical damage is limited to the lesser of the actual cash value or the cost to repair or replace the vehicle.",
            "Comprehensive coverage deductible: $500 per vehicle. Collision coverage deductible: $1,000 per vehicle. Glass breakage may be included under comprehensive or subject to a separate deductible. The insurer's liability excludes wear and tear.",
            "7.7 MOTOR CARRIER ENDORSEMENT. For insureds operating as motor carriers, the MCS-90 endorsement provides mandatory liability coverage. Motor carrier liability meets the minimum financial responsibility requirements of the Federal Motor Carrier Safety Administration.",
            "The MCS-90 endorsement liability limit is $1,000,000 for general freight. Hazardous materials transportation requires higher limits of liability as specified by federal regulation.",
            "7.8 FLEET MANAGEMENT. The insurer provides fleet management resources including driver qualification reviews, vehicle maintenance program recommendations, and fleet safety training. These services help reduce auto liability exposure.",
            "An annual fleet safety audit may qualify the insured for auto liability premium credits of up to 10%. Fleet management recommendations are advisory and do not alter the insurer's liability under this policy.",
        ]),
        # Page 22 - Auto Exclusions
        ("SECTION VII: AUTO LIABILITY EXCLUSIONS", [
            "7.9 AUTO LIABILITY EXCLUSIONS. Coverage does not apply to: (a) expected or intended injury; (b) contractual liability; (c) workers' compensation; (d) employee indemnification and employer's liability; (e) fellow employee claims.",
            "Additional auto liability exclusions: (f) care, custody, or control of property other than the insured vehicle; (g) handling of property before loading or after unloading; (h) movement of property by mechanical device not attached to the vehicle.",
            "The auto liability exclusions for completed operations and products liability refer the insured to Sections II and III for applicable coverage. Auto liability and general liability work together to provide comprehensive protection.",
            "7.10 DRIVE OTHER CAR COVERAGE. Named individuals may receive drive other car liability coverage under this policy. This endorsement extends auto liability protection to vehicles driven by the named individual for personal use.",
            "7.11 GARAGEKEEPERS LIABILITY. For insureds with garage operations, garagekeepers liability coverage protects against damage to customers' vehicles in the insured's care. The garagekeepers liability limit is $500,000 per location.",
        ]),
        # Page 23 - Umbrella
        ("SECTION VIII: UMBRELLA LIABILITY COVERAGE", [
            "8.1 UMBRELLA LIABILITY INSURING AGREEMENT. The insurer will pay on behalf of the insured the ultimate net loss in excess of the retained limit arising from an occurrence. Umbrella liability provides catastrophic protection above underlying liability policies.",
            "The umbrella liability coverage applies in excess of: (a) general liability; (b) auto liability; (c) employer's liability. The umbrella follows form to the underlying liability coverage with certain broader provisions as stated herein.",
            "8.2 UMBRELLA LIABILITY LIMITS. The per-occurrence limit of umbrella liability is $10,000,000. The annual aggregate limit of umbrella liability is $10,000,000. These limits apply in addition to the underlying liability limits.",
            "The self-insured retention under the umbrella liability is $10,000 per occurrence for claims not covered by underlying liability insurance but covered by the umbrella. The SIR acts as a deductible for drop-down liability coverage.",
            "8.3 DROP-DOWN LIABILITY. If underlying liability limits are exhausted by prior losses during the policy period, the umbrella provides drop-down liability coverage subject to the self-insured retention. Drop-down liability is a critical benefit of umbrella coverage.",
            "The umbrella liability policy does not provide drop-down coverage for claims excluded by the underlying liability policies due to policy terms other than limits. The umbrella liability follows the exclusion structure of the underlying liability policies.",
        ]),
        # Page 24 - Umbrella Continued
        ("SECTION VIII: UMBRELLA LIABILITY (CONTINUED)", [
            "8.4 UMBRELLA LIABILITY COVERAGE FEATURES. The umbrella liability coverage provides broader coverage than the underlying liability policies in certain respects: (a) worldwide coverage territory; (b) personal injury coverage including disparagement; (c) advertising liability with fewer restrictions.",
            "The umbrella liability policy also provides: (d) liquor liability coverage where the underlying excludes it (subject to SIR); (e) non-owned watercraft liability for vessels up to 52 feet; (f) liability coverage for foreign operations not covered by the underlying CGL.",
            "8.5 UMBRELLA LIABILITY EXCLUSIONS. The umbrella does not cover: (a) workers' compensation or similar statutory liability; (b) contractual liability not covered by the underlying; (c) professional liability, which has its own excess provisions; (d) pollution liability, except as covered under Section X.",
            "Nuclear liability, war, and terrorism exclusions apply to the umbrella as they do to the underlying liability policies. The umbrella liability does not drop down to cover losses specifically excluded by policy terms.",
            "8.6 UNDERLYING INSURANCE REQUIREMENTS. The insured must maintain the underlying liability insurance at the limits specified in the umbrella liability schedule. Failure to maintain underlying limits may result in the insured bearing the liability gap.",
        ]),
        # Page 25 - Umbrella Defense
        ("SECTION VIII: UMBRELLA LIABILITY DEFENSE", [
            "8.7 UMBRELLA DEFENSE OBLIGATIONS. The insurer has no duty to defend until the underlying liability limits are exhausted. Once the underlying limits are exhausted, the umbrella insurer assumes the defense of the insured. Defense costs under the umbrella liability are paid in addition to the limits.",
            "For claims where the umbrella provides drop-down liability coverage (not covered by underlying policies), the insurer will defend from the outset, subject to the self-insured retention. The duty to defend is broader than the duty to indemnify under the umbrella liability.",
            "8.8 COORDINATION WITH UNDERLYING LIABILITY. The umbrella insurer will cooperate with the underlying liability insurer in the investigation and defense of claims. Where multiple liability policies respond to a single occurrence, the insurers will coordinate to avoid conflicts.",
            "The umbrella liability insurer has the right to associate in the defense of any claim that may involve the umbrella. Early involvement of the umbrella liability insurer helps ensure consistent defense strategy.",
            "8.9 UMBRELLA CLAIMS REPORTING. The insured must notify the umbrella liability insurer of any claim that may reasonably be expected to involve the umbrella. Failure to provide notice of a potentially excess liability claim does not invalidate coverage unless the insurer is materially prejudiced.",
        ]),
        # Page 26 - Cyber Liability
        ("SECTION IX: CYBER LIABILITY AND DATA BREACH RESPONSE", [
            "9.1 CYBER LIABILITY INSURING AGREEMENT. The insurer agrees to pay on behalf of the insured all sums arising from claims related to data breaches, network security failures, and technology errors. Cyber liability is a critical coverage for modern business operations.",
            "Cyber liability coverage is written on a claims-made and reported basis. The retroactive date for cyber liability coverage is the same as the policy inception date unless otherwise stated. Each cyber liability claim is subject to the terms herein.",
            "9.2 CYBER LIABILITY LIMITS. The per-claim limit of cyber liability is $2,000,000. The annual aggregate limit of cyber liability is $5,000,000. Defense costs are included within the cyber liability limits, not in addition to them.",
            "The cyber liability deductible is $25,000 per claim. Regulatory defense costs have a separate sub-limit of liability of $500,000 within the overall cyber liability limit.",
            "9.3 FIRST-PARTY CYBER COVERAGE. The insurer covers the insured's own losses resulting from a cyber event: (a) data restoration costs; (b) business interruption losses; (c) cyber extortion payments; (d) crisis management expenses. First-party cyber liability is subject to separate sub-limits.",
            "Data restoration liability limit: $1,000,000 per event. Business interruption liability limit: $1,500,000 per event with a 12-hour waiting period. Cyber extortion liability limit: $500,000 per event.",
        ]),
        # Page 27 - Cyber Continued
        ("SECTION IX: CYBER LIABILITY (CONTINUED)", [
            "9.4 THIRD-PARTY CYBER LIABILITY. This coverage responds to claims by third parties alleging: (a) unauthorized access to personal data; (b) failure to protect confidential information; (c) transmission of malicious code; (d) denial of service. Third-party cyber liability is the core of this coverage section.",
            "Privacy regulatory proceedings are covered under cyber liability with a sub-limit of $500,000. The insurer will provide experienced cyber liability defense counsel for regulatory matters.",
            "9.5 DATA BREACH RESPONSE SERVICES. Upon discovery of a data breach, the insurer provides: (a) forensic investigation services; (b) notification services to affected individuals; (c) credit monitoring for affected parties; (d) public relations and crisis communications. Breach response liability costs are advanced by the insurer.",
            "The liability for breach response services is $2,000,000 per event. The insurer maintains a panel of pre-approved breach response vendors. The insured must use panel vendors to ensure coverage; use of non-panel vendors requires prior approval.",
            "9.6 CYBER LIABILITY EXCLUSIONS. Cyber coverage does not apply to: (a) prior known breaches; (b) intentional or criminal acts; (c) contractual liability not arising from privacy obligations; (d) bodily injury or physical property damage; (e) intellectual property infringement other than privacy.",
        ]),
        # Page 28 - Cyber Additional
        ("SECTION IX: CYBER LIABILITY ADDITIONAL PROVISIONS", [
            "9.7 SOCIAL ENGINEERING COVERAGE. The insurer provides limited coverage for losses arising from social engineering fraud, including phishing and business email compromise. Social engineering liability limit: $250,000 per event with a $10,000 deductible.",
            "Verification procedures are required for social engineering coverage to apply. The insured must maintain documented callback verification procedures for all financial transactions exceeding $25,000. Failure to follow verification procedures voids the social engineering liability coverage.",
            "9.8 MEDIA LIABILITY. Cyber coverage extends to claims arising from the insured's online media activities: (a) defamation; (b) invasion of privacy; (c) copyright infringement in digital content. Media liability sub-limit: $500,000 per claim.",
            "9.9 REGULATORY FINES AND PENALTIES. Where insurable by law, the cyber liability coverage extends to fines and penalties imposed by regulatory authorities for data protection violations. GDPR and CCPA fines are covered subject to the regulatory liability sub-limit.",
            "9.10 CYBER RISK MANAGEMENT. The insurer provides cyber risk management resources including vulnerability assessments, employee training programs, and incident response planning. Active participation in cyber risk management may reduce cyber liability premiums by up to 15%.",
        ]),
        # Page 29 - Environmental Liability
        ("SECTION X: ENVIRONMENTAL LIABILITY", [
            "10.1 ENVIRONMENTAL LIABILITY INSURING AGREEMENT. The insurer agrees to pay on behalf of the insured all sums arising from claims of pollution conditions on, under, or migrating from covered locations. Environmental liability coverage is essential for manufacturing and industrial operations.",
            "Environmental liability coverage is written on a claims-made basis with a retroactive date of January 1, 2020. The insurer's liability for pre-existing pollution conditions known to the insured is excluded.",
            "10.2 ENVIRONMENTAL LIABILITY LIMITS. The per-claim limit of environmental liability is $2,000,000. The annual aggregate limit of environmental liability is $5,000,000. Defense costs are included within the environmental liability limits.",
            "10.3 COVERED POLLUTION CONDITIONS. Environmental liability applies to: (a) new pollution conditions discovered during the policy period; (b) pre-existing unknown pollution conditions; (c) third-party pollution conditions migrating onto the insured's property.",
            "10.4 ENVIRONMENTAL CLEANUP COSTS. The insurer covers reasonable and necessary cleanup costs incurred to remediate pollution conditions at covered locations. Environmental cleanup liability includes costs mandated by governmental authorities.",
            "The insurer's liability for voluntary cleanup costs is limited to costs that the insurer has pre-approved. The insured must obtain the insurer's consent before initiating voluntary remediation to ensure coverage under the environmental liability section.",
        ]),
        # Page 30 - Environmental Continued
        ("SECTION X: ENVIRONMENTAL LIABILITY (CONTINUED)", [
            "10.5 TRANSPORTATION ENVIRONMENTAL LIABILITY. Coverage extends to pollution conditions arising during the transportation of materials to or from covered locations. Transportation environmental liability applies to sudden and accidental releases only.",
            "10.6 NON-OWNED DISPOSAL SITE LIABILITY. The insurer covers the insured's liability for pollution conditions at non-owned disposal sites to which the insured sent waste. Non-owned site environmental liability is subject to a $1,000,000 sub-limit.",
            "10.7 ENVIRONMENTAL LIABILITY EXCLUSIONS. Environmental coverage does not apply to: (a) known pre-existing conditions; (b) asbestos or lead paint liability; (c) nuclear materials; (d) intentional discharge of pollutants. These environmental liability exclusions apply regardless of negligence.",
            "10.8 ENVIRONMENTAL COMPLIANCE. The insurer provides environmental compliance assistance including regulatory tracking, permit review, and compliance auditing. Proactive environmental compliance reduces the insured's environmental liability exposure.",
            "10.9 MOLD LIABILITY. Limited coverage for mold remediation is provided within the environmental liability section. Mold liability sub-limit: $250,000 per occurrence. The insured must maintain proper ventilation and moisture control to preserve mold liability coverage.",
        ]),
        # Page 31 - Claims Procedures
        ("SECTION XI: CLAIMS PROCEDURES AND DISPUTE RESOLUTION", [
            "11.1 NOTICE OF OCCURRENCE. The insured must provide notice to the insurer as soon as practicable of any occurrence that may result in a claim under this policy. Notice must include the nature of the occurrence, the identity of potential claimants, and an estimate of potential liability.",
            "Written notice of occurrence should be sent to: Meridian National Insurance Group, Claims Division, P.O. Box 9847, Hartford, CT 06152. Electronic notice may be submitted through the insurer's online portal at www.meridian-national.com/claims.",
            "11.2 NOTICE OF CLAIM OR SUIT. The insured must immediately forward to the insurer every demand, notice, summons, or other process received regarding any potential liability under this policy. Failure to provide timely notice of a claim may result in denial of coverage.",
            "11.3 ASSISTANCE AND COOPERATION. The insured must cooperate with the insurer in the investigation, settlement, and defense of any claim or suit. The insured shall attend hearings, depositions, and trials when requested. The duty to cooperate applies to all liability sections.",
            "The insured shall not voluntarily make any payment, assume any obligation, or incur any expense without the insurer's prior written consent. Unauthorized payments or admissions of liability may void coverage under this policy.",
            "11.4 EXAMINATION UNDER OATH. The insurer may require the insured to submit to examination under oath regarding any matter relating to a claim. The insured must comply with such request and produce all relevant documents.",
        ]),
        # Page 32 - Dispute Resolution
        ("SECTION XI: DISPUTE RESOLUTION (CONTINUED)", [
            "11.5 APPRAISAL. If the insured and insurer disagree on the amount of loss under the property sections, either party may demand appraisal. Each party selects an appraiser, and the two appraisers select an umpire. The appraisal process does not address liability coverage disputes.",
            "11.6 ARBITRATION. Disputes regarding the interpretation of this policy or the determination of liability may be submitted to binding arbitration. Each party selects one arbitrator, and the two arbitrators select a third. The arbitration is conducted under the rules of the American Arbitration Association.",
            "11.7 LEGAL ACTIONS AGAINST THE INSURER. No action shall be brought against the insurer unless the insured has fully complied with all terms of this policy and the action is commenced within two years after the date of the occurrence giving rise to liability.",
            "11.8 SUBROGATION. The insurer may require the insured to assign all rights of recovery against third parties for any payment made under this policy. The insured must cooperate with the insurer's subrogation efforts. Subrogation applies to all liability and property sections.",
            "11.9 SETTLEMENT AUTHORITY. The insurer has the right to settle any claim or suit within the applicable limit of liability. For claims under the professional liability section, the insurer will consult with the insured before settling. The insured's consent to settlement is not required for general liability or auto liability claims.",
        ]),
        # Page 33 - Exclusions and Conditions
        ("SECTION XII: EXCLUSIONS, CONDITIONS, AND ENDORSEMENTS", [
            "12.1 GENERAL EXCLUSIONS. In addition to the exclusions stated in each liability section, this policy does not cover: (a) war, military action, insurrection, or rebellion; (b) nuclear reaction, radiation, or contamination; (c) intentional acts of the insured.",
            "Terrorism liability exclusion: Acts of terrorism as defined by the Terrorism Risk Insurance Act are excluded unless the insured has elected to purchase terrorism liability coverage for an additional premium.",
            "12.2 CONDITIONS APPLICABLE TO ALL COVERAGES. (a) Entire Agreement: This policy, including all endorsements and the Declarations, constitutes the entire agreement between the parties. (b) Policy Period: Coverage applies only to occurrences during the policy period. (c) Cancellation: Either party may cancel by providing 30 days written notice.",
            "12.3 DUTIES IN THE EVENT OF LOSS. The insured must: (a) protect property from further damage; (b) cooperate in the investigation; (c) submit to examination under oath; (d) provide signed, sworn proof of loss within 60 days. Failure to perform these duties may void the insurer's liability.",
            "12.4 OTHER INSURANCE. When other valid insurance exists, this policy shall be excess over such other insurance. The insurer's liability is limited to the amount by which the applicable limit exceeds the total of other collectible insurance.",
            "12.5 TRANSFER OF RIGHTS AND DUTIES. The insured may not transfer rights or duties under this policy without the written consent of the insurer. The policy is personal to the Named Insured. Any purported transfer without consent does not bind the insurer and creates no liability obligation.",
        ]),
        # Page 34 - Endorsements
        ("SECTION XII: ENDORSEMENTS AND SCHEDULES", [
            "12.6 ATTACHED ENDORSEMENTS. The following endorsements are attached to and form part of this policy: (a) Additional Insured Endorsement - Scheduled Organizations; (b) Waiver of Subrogation Endorsement; (c) Primary and Non-Contributory Endorsement; (d) Per Project Aggregate Endorsement.",
            "Each endorsement modifies the liability terms as stated therein. In the event of conflict between an endorsement and the policy form, the endorsement controls. The insurer's liability is governed by the endorsement provisions.",
            "12.7 SCHEDULE OF LOCATIONS. Covered locations for property and environmental liability coverage: (a) 4520 Industrial Boulevard, Springfield, IL 62701 - Main Manufacturing Plant; (b) 1280 Commerce Drive, Springfield, IL 62704 - Warehouse and Distribution Center; (c) 890 Technology Park, Decatur, IL 62521 - Research Facility.",
            "12.8 SCHEDULE OF LIABILITY LIMITS SUMMARY. General Liability: $2M/$5M aggregate. Product Liability: $2M/$3M aggregate. Professional Liability: $1M/$3M aggregate. Auto Liability: $1M CSL. Umbrella Liability: $10M/$10M aggregate. Cyber Liability: $2M/$5M aggregate. Environmental Liability: $2M/$5M aggregate.",
            "12.9 PREMIUM SUMMARY. Total annual premium: $187,450. Payment terms: quarterly installments. Premium is subject to annual audit. The insured's premium obligation is independent of any liability determination.",
        ]),
        # Page 35 - Signature Page
        ("SIGNATURE AND ATTESTATION", [
            "IN WITNESS WHEREOF, the insurer has caused this policy to be signed by its authorized officers at its home office in Hartford, Connecticut, effective as of March 1, 2024.",
            "MERIDIAN NATIONAL INSURANCE GROUP\n\nJames R. Whitfield, President and CEO\nDate: February 15, 2024\n\nEleanor M. Castellano, Senior Vice President, Underwriting\nDate: February 15, 2024\n\nRobert K. Tanaka, Chief Underwriting Officer\nDate: February 15, 2024",
            "POLICYHOLDER ACKNOWLEDGMENT\n\nThe undersigned acknowledges receipt of this policy and agrees that all representations made in the application for insurance are accurate and complete. The policyholder acknowledges reviewing all liability terms, conditions, and exclusions.",
            "WESTBROOK MANUFACTURING, INC.\n\nDavid A. Westbrook, Chief Executive Officer\nDate: February 20, 2024\n\nMaria C. Rodriguez, Chief Financial Officer\nDate: February 20, 2024",
            "This policy provides comprehensive liability and property protection. For questions about coverage, liability limits, or claims procedures, contact your agent Patricia Navarro at (217) 555-0134 or pnavarro@meridianins.com.",
            "IMPORTANT: This policy document is intended for the sole use of the named insured and authorized representatives. Reproduction or distribution of this document may violate confidentiality provisions. All liability determinations under this policy are subject to the terms, conditions, and exclusions stated herein.",
        ]),
    ]

    for i, (title, paragraphs) in enumerate(sections, 2):
        add_page_text(doc, title, paragraphs, i)

    # Set metadata
    doc.set_metadata({
        "title": "Comprehensive Insurance Policy - INS-2024-78432",
        "author": "Meridian National Insurance Group",
        "subject": "Commercial Insurance Policy",
        "keywords": "insurance, liability, coverage, policy",
        "creator": "Meridian National Insurance Group",
        "producer": "Meridian Policy Management System",
    })

    # Add Table of Contents bookmarks
    toc = [
        [1, "Cover Page", 1],
        [1, "Table of Contents", 2],
        [1, "Section I: Definitions and General Provisions", 3],
        [1, "Section II: General Liability Coverage", 5],
        [1, "Section III: Product Liability Insurance", 8],
        [1, "Section IV: Professional Liability Protection", 11],
        [1, "Section V: Property Coverage and Endorsements", 14],
        [1, "Section VI: Workers' Compensation and Employer's Liability", 17],
        [1, "Section VII: Commercial Auto Liability", 20],
        [1, "Section VIII: Umbrella Liability Coverage", 23],
        [1, "Section IX: Cyber Liability and Data Breach Response", 26],
        [1, "Section X: Environmental Liability", 29],
        [1, "Section XI: Claims Procedures and Dispute Resolution", 31],
        [1, "Section XII: Exclusions, Conditions, and Endorsements", 33],
        [1, "Signature and Attestation", 35],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()

    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {pymupdf.open(OUTPUT).page_count}')

    # Count occurrences of 'liability' for reference
    d = pymupdf.open(OUTPUT)
    count = 0
    for pg in d:
        count += len(pg.search_for("liability"))
    d.close()
    print(f"Occurrences of 'liability': {count}")

    # Launch Evince to open the PDF
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
