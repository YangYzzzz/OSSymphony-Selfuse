"""
Initial Setup: Create 18-page legal demand package PDF
Task ID: pdf_legal_092
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_092'
DIR = f'{WORKDIR}/legal/demand'
OUTPUT = f'{DIR}/demand_package.pdf'


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
    os.makedirs(DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page dimensions ---
    W, H = 612, 792  # US Letter

    # Content for an 18-page demand package
    pages_content = [
        # Page 1: Cover / Title Page
        {
            "title": "DEMAND PACKAGE",
            "subtitle": "Prepared on Behalf of Elena Vasquez-Rodriguez",
            "body": (
                "Date: March 14, 2025\n\n"
                "Prepared by:\n"
                "Martinez & Chen, LLP\n"
                "Attorneys at Law\n"
                "4200 Westfield Boulevard, Suite 1100\n"
                "Sacramento, CA 95814\n"
                "Tel: (916) 555-0187\n\n"
                "Submitted to:\n"
                "Pacific Coast Insurance Group\n"
                "Claims Department\n"
                "Attn: Karen Whitfield, Senior Claims Adjuster\n"
                "Claim No.: PCI-2024-88471\n"
                "Policy No.: APC-7739201\n"
                "Date of Loss: September 3, 2024"
            ),
        },
        # Page 2: Table of Contents
        {
            "title": "TABLE OF CONTENTS",
            "body": (
                "I.    Introduction and Summary of Claim ........................... 3\n"
                "II.   Factual Background .......................................... 4\n"
                "III.  Liability Analysis ........................................... 5\n"
                "IV.   Medical Treatment Summary ................................... 6\n"
                "V.    Emergency Room Treatment .................................... 7\n"
                "VI.   Orthopedic Consultation ..................................... 8\n"
                "VII.  Physical Therapy Records .................................... 9\n"
                "VIII. Pain Management Treatment ................................... 10\n"
                "IX.   Diagnostic Imaging Results .................................. 11\n"
                "X.    Lost Wages and Economic Damages ............................. 12\n"
                "XI.   Non-Economic Damages Analysis ............................... 13\n"
                "XII.  Future Medical Expenses ..................................... 14\n"
                "XIII. Property Damage ............................................. 15\n"
                "XIV.  Comparable Verdicts and Settlements ......................... 16\n"
                "XV.   Demand Amount ............................................... 17\n"
                "XVI.  Conclusion .................................................. 18\n"
            ),
        },
        # Page 3: Introduction
        {
            "title": "I. INTRODUCTION AND SUMMARY OF CLAIM",
            "body": (
                "This demand package is submitted on behalf of Elena Vasquez-Rodriguez "
                "('Claimant') for injuries sustained in a motor vehicle collision that "
                "occurred on September 3, 2024, at the intersection of Folsom Boulevard "
                "and 65th Street in Sacramento, California.\n\n"
                "On the date of the incident, the Claimant was traveling westbound on "
                "Folsom Boulevard when the insured, Derek Marshall, failed to observe a "
                "red traffic signal and struck the Claimant's vehicle on the driver's "
                "side at approximately 40 miles per hour. The Sacramento Police Department "
                "responded to the scene and issued a citation to Mr. Marshall for running "
                "a red light (CVC Section 21453(a)).\n\n"
                "As a direct result of this collision, Ms. Vasquez-Rodriguez suffered "
                "significant injuries including a herniated disc at L4-L5, cervical "
                "strain, left shoulder rotator cuff tear, and multiple contusions. She "
                "has undergone extensive medical treatment over the past six months and "
                "continues to require ongoing care.\n\n"
                "The total medical expenses incurred to date are $87,342.18. Lost wages "
                "total $34,560.00. This demand seeks full compensation for all economic "
                "and non-economic damages sustained by the Claimant."
            ),
        },
        # Page 4: Factual Background
        {
            "title": "II. FACTUAL BACKGROUND",
            "body": (
                "On September 3, 2024, at approximately 5:47 PM, Elena Vasquez-Rodriguez "
                "was driving her 2021 Honda Accord westbound on Folsom Boulevard. She had "
                "departed from her workplace at Regional Medical Center, where she is "
                "employed as a Registered Nurse in the Intensive Care Unit.\n\n"
                "As Ms. Vasquez-Rodriguez entered the intersection at 65th Street with a "
                "green traffic signal, Derek Marshall, operating a 2019 Ford F-150, ran "
                "the red light while traveling northbound on 65th Street. Mr. Marshall's "
                "vehicle collided with the driver's side of Ms. Vasquez-Rodriguez's "
                "vehicle at an estimated speed of 40 mph.\n\n"
                "The collision caused severe damage to the Claimant's vehicle. The airbags "
                "deployed and Ms. Vasquez-Rodriguez was trapped in the vehicle until "
                "Sacramento Fire Department personnel extracted her using hydraulic rescue "
                "tools. She was transported via ambulance to UC Davis Medical Center.\n\n"
                "Witness statements from three independent bystanders confirm that "
                "Mr. Marshall ran the red light. Traffic camera footage obtained from the "
                "City of Sacramento corroborates these accounts. The police report "
                "(Report No. SPD-2024-09-45872) documents Mr. Marshall's admission that "
                "he was 'checking his phone' at the time of the collision."
            ),
        },
        # Page 5: Liability
        {
            "title": "III. LIABILITY ANALYSIS",
            "body": (
                "Liability in this matter rests solely with the insured, Derek Marshall. "
                "The evidence establishes the following:\n\n"
                "1. Traffic Signal Violation: Mr. Marshall ran a red light in violation "
                "of California Vehicle Code Section 21453(a). This constitutes negligence "
                "per se under Evidence Code Section 669.\n\n"
                "2. Distracted Driving: Mr. Marshall admitted to Sacramento Police "
                "officers that he was using his cellular telephone at the time of the "
                "collision, in violation of CVC Section 23123.5.\n\n"
                "3. Witness Corroboration: Three independent witnesses -- Maria Santos, "
                "Thomas Blackwell, and Jennifer Okonkwo -- all provided statements "
                "confirming that Mr. Marshall's vehicle entered the intersection against "
                "a red signal.\n\n"
                "4. Traffic Camera Evidence: Surveillance footage from the intersection "
                "camera clearly shows Mr. Marshall's vehicle proceeding through the red "
                "light at full speed without any attempt to brake.\n\n"
                "5. Police Citation: Officer James Reeves of the Sacramento Police "
                "Department issued Citation No. T-892471 to Mr. Marshall for failure to "
                "stop at a red signal.\n\n"
                "Based on the foregoing, Pacific Coast Insurance Group's insured bears "
                "100% liability for this collision and the resulting damages."
            ),
        },
        # Page 6: Medical Treatment Summary
        {
            "title": "IV. MEDICAL TREATMENT SUMMARY",
            "body": (
                "The following is a comprehensive summary of all medical treatment "
                "received by Ms. Vasquez-Rodriguez as a result of the September 3, 2024 "
                "collision:\n\n"
                "Date         Provider                    Treatment           Cost\n"
                "09/03/2024   UC Davis Medical Center      ER/Trauma           $18,742.00\n"
                "09/05/2024   Sacramento Radiology Group   MRI - Lumbar        $3,200.00\n"
                "09/05/2024   Sacramento Radiology Group   MRI - Cervical      $3,200.00\n"
                "09/08/2024   Dr. Richard Yamamoto         Ortho Consult       $475.00\n"
                "09/10/2024   Sacramento Radiology Group   MRI - L Shoulder    $3,400.00\n"
                "09/15/2024   Dr. Yamamoto                 Follow-up           $275.00\n"
                "09/20/2024   Peak Performance PT          Eval + Treatment    $350.00\n"
                "10/2024-     Peak Performance PT          36 PT Sessions      $12,600.00\n"
                "  03/2025\n"
                "10/01/2024   Dr. Susan Park               Pain Mgmt Consult   $550.00\n"
                "10/15/2024   Dr. Park                     Epidural Injection  $4,800.00\n"
                "11/12/2024   Dr. Park                     Epidural Injection  $4,800.00\n"
                "12/10/2024   Dr. Park                     Epidural Injection  $4,800.00\n"
                "01/15/2025   Dr. Yamamoto                 Surgical Consult    $475.00\n"
                "02/03/2025   UC Davis Medical Center      Arthroscopic Surg   $28,450.00\n"
                "02/10/2025   Dr. Yamamoto                 Post-Op Follow-up   $275.00\n"
                "03/01/2025   Peak Performance PT          Post-Op PT (6 ses)  $2,100.00\n\n"
                "TOTAL MEDICAL EXPENSES TO DATE: $87,342.18\n"
                "(Includes $1,149.18 in prescription medications not listed above)"
            ),
        },
        # Page 7: ER Treatment
        {
            "title": "V. EMERGENCY ROOM TREATMENT",
            "body": (
                "Ms. Vasquez-Rodriguez was transported to UC Davis Medical Center by "
                "Sacramento Fire Department Medic Unit 7 on September 3, 2024. She "
                "arrived at the Emergency Department at 6:12 PM.\n\n"
                "Upon arrival, the trauma team performed the following assessments:\n"
                "- Full trauma survey per ATLS protocol\n"
                "- CT scan of head, cervical spine, chest, abdomen, and pelvis\n"
                "- X-rays of left shoulder, lumbar spine, and left hip\n"
                "- Complete blood count, metabolic panel, urinalysis\n\n"
                "Initial findings included:\n"
                "- Acute cervical strain with muscle spasm\n"
                "- Left shoulder contusion with limited range of motion\n"
                "- Lower back pain with radiculopathy to left lower extremity\n"
                "- Multiple contusions to left arm, left leg, and torso\n"
                "- Laceration to left forearm (3 cm, closed with 5 sutures)\n\n"
                "Ms. Vasquez-Rodriguez was administered IV morphine for pain management, "
                "a cervical collar was applied, and she was placed on spinal precautions. "
                "CT scans were negative for fractures or internal bleeding. She was "
                "discharged at 11:48 PM with prescriptions for hydrocodone 5/325mg, "
                "cyclobenzaprine 10mg, and naproxen 500mg, along with instructions for "
                "orthopedic and radiology follow-up within one week.\n\n"
                "Total ER charges: $18,742.00"
            ),
        },
        # Page 8: Orthopedic Consultation
        {
            "title": "VI. ORTHOPEDIC CONSULTATION",
            "body": (
                "Dr. Richard Yamamoto, Board-Certified Orthopedic Surgeon at Sacramento "
                "Orthopedic Associates, evaluated Ms. Vasquez-Rodriguez on September 8, "
                "2024.\n\n"
                "Physical Examination Findings:\n"
                "- Cervical spine: Decreased ROM in all planes, significant paraspinal "
                "muscle tenderness bilaterally, positive Spurling's test on left\n"
                "- Left shoulder: Positive Neer's impingement sign, positive Hawkins test, "
                "decreased abduction (95 degrees vs. normal 180), pain with overhead "
                "reaching\n"
                "- Lumbar spine: Positive straight leg raise at 40 degrees on left, "
                "decreased forward flexion, palpable muscle spasm L3-S1\n\n"
                "MRI Results (September 5 and 10, 2024):\n"
                "- Cervical MRI: C5-C6 disc bulge with mild foraminal stenosis, "
                "paravertebral soft tissue edema\n"
                "- Lumbar MRI: L4-L5 posterior disc herniation with left-sided foraminal "
                "extension compressing the L5 nerve root\n"
                "- Left Shoulder MRI: Partial-thickness articular surface tear of the "
                "supraspinatus tendon (approximately 50% thickness), mild subacromial "
                "bursitis, labral fraying\n\n"
                "Dr. Yamamoto's treatment plan recommended:\n"
                "1. Physical therapy 3x/week for 12 weeks\n"
                "2. Pain management referral for epidural steroid injections\n"
                "3. Re-evaluation at 3 months to assess surgical candidacy for shoulder\n"
                "4. Activity restrictions: No lifting >10 lbs, no overhead work"
            ),
        },
        # Page 9: Physical Therapy
        {
            "title": "VII. PHYSICAL THERAPY RECORDS",
            "body": (
                "Ms. Vasquez-Rodriguez commenced physical therapy at Peak Performance "
                "Physical Therapy on September 20, 2024, under the direction of "
                "Dr. Amanda Torres, DPT.\n\n"
                "Initial Evaluation (09/20/2024):\n"
                "- Cervical ROM: Flexion 30/50 deg, Extension 20/60 deg, "
                "Lateral flexion 25/45 deg bilaterally\n"
                "- Lumbar ROM: Flexion 40/60 deg, Extension 10/25 deg\n"
                "- Left shoulder ROM: Flexion 110/180 deg, Abduction 95/180 deg\n"
                "- Pain levels: Cervical 7/10, Lumbar 8/10, Left Shoulder 6/10\n"
                "- Functional limitations: Unable to perform nursing duties, difficulty "
                "with ADLs including dressing, driving, and household tasks\n\n"
                "Treatment Protocol:\n"
                "- Manual therapy: Soft tissue mobilization, joint mobilization\n"
                "- Therapeutic exercises: Core stabilization, rotator cuff strengthening\n"
                "- Modalities: Electrical stimulation, ultrasound, ice/heat\n"
                "- Frequency: 3 sessions per week for 12 weeks\n\n"
                "Progress at 12 Weeks (12/13/2024):\n"
                "- Cervical ROM: Improved to 40/50 deg flexion, 40/60 deg extension\n"
                "- Lumbar ROM: Improved to 50/60 deg flexion, 18/25 deg extension\n"
                "- Left shoulder ROM: Improved to 140/180 deg flexion, 120/180 abduction\n"
                "- Pain levels: Cervical 4/10, Lumbar 5/10, Left Shoulder 5/10\n"
                "- Patient continued to report significant functional limitations\n\n"
                "Total PT charges (36 sessions + 6 post-op): $14,700.00"
            ),
        },
        # Page 10: Pain Management
        {
            "title": "VIII. PAIN MANAGEMENT TREATMENT",
            "body": (
                "Dr. Susan Park, Board-Certified Pain Management Specialist at Capitol "
                "Pain & Spine Center, evaluated Ms. Vasquez-Rodriguez on October 1, 2024.\n\n"
                "Dr. Park diagnosed:\n"
                "1. Lumbar radiculopathy secondary to L4-L5 disc herniation\n"
                "2. Cervical facet syndrome at C5-C6\n"
                "3. Chronic pain syndrome\n\n"
                "Treatment Provided:\n\n"
                "Injection #1 (10/15/2024): Left L4-L5 transforaminal epidural steroid "
                "injection under fluoroscopic guidance. Patient reported 40% pain "
                "reduction lasting approximately 3 weeks.\n\n"
                "Injection #2 (11/12/2024): Left L4-L5 transforaminal epidural steroid "
                "injection. Patient reported 50% pain reduction lasting approximately "
                "4 weeks.\n\n"
                "Injection #3 (12/10/2024): Left L4-L5 transforaminal epidural steroid "
                "injection. Patient reported 35% pain reduction lasting approximately "
                "2.5 weeks. Diminishing returns noted.\n\n"
                "Dr. Park's Assessment:\n"
                "The decreasing efficacy of the epidural injections suggests that "
                "Ms. Vasquez-Rodriguez may require surgical intervention for the lumbar "
                "disc herniation. Dr. Park prescribed gabapentin 300mg TID for "
                "neuropathic pain and recommended continued physical therapy.\n\n"
                "Total Pain Management charges: $15,950.00\n"
                "(Includes consultation, three injections, and follow-up visits)"
            ),
        },
        # Page 11: Diagnostic Imaging
        {
            "title": "IX. DIAGNOSTIC IMAGING RESULTS",
            "body": (
                "The following diagnostic imaging studies were performed at Sacramento "
                "Radiology Group and UC Davis Medical Center:\n\n"
                "1. CT Scan - Head (09/03/2024)\n"
                "   Findings: No acute intracranial pathology. No fractures identified.\n\n"
                "2. CT Scan - Cervical Spine (09/03/2024)\n"
                "   Findings: No fracture or subluxation. Mild disc space narrowing at "
                "C5-C6. Prevertebral soft tissue swelling.\n\n"
                "3. X-Ray - Left Shoulder (09/03/2024)\n"
                "   Findings: No fracture or dislocation. Soft tissue swelling noted.\n\n"
                "4. MRI - Cervical Spine (09/05/2024)\n"
                "   Findings: C5-C6 broad-based disc bulge with mild bilateral foraminal "
                "stenosis. Paravertebral muscle edema consistent with acute strain.\n\n"
                "5. MRI - Lumbar Spine (09/05/2024)\n"
                "   Findings: L4-L5 posterior disc herniation, 6mm protrusion with "
                "left-sided foraminal extension. Left L5 nerve root compression. Mild "
                "facet hypertrophy at L3-L4 and L5-S1.\n\n"
                "6. MRI - Left Shoulder (09/10/2024)\n"
                "   Findings: Partial-thickness articular surface tear of the supraspinatus "
                "tendon, approximately 50% thickness involvement. Mild subacromial "
                "bursitis. Superior labral fraying. Moderate joint effusion.\n\n"
                "Total Diagnostic Imaging charges: $9,800.00"
            ),
        },
        # Page 12: Lost Wages
        {
            "title": "X. LOST WAGES AND ECONOMIC DAMAGES",
            "body": (
                "Ms. Vasquez-Rodriguez is employed as a Registered Nurse in the Intensive "
                "Care Unit at Regional Medical Center in Sacramento, California. She has "
                "been continuously employed at this facility since June 2019.\n\n"
                "Compensation Details:\n"
                "- Base hourly rate: $52.00/hour\n"
                "- Average weekly hours: 36 (three 12-hour shifts)\n"
                "- Average weekly gross pay: $1,872.00\n"
                "- Shift differential (nights/weekends): ~$180/week average\n"
                "- Average weekly gross with differential: $2,052.00\n\n"
                "Period of Disability:\n"
                "- Total disability: 09/03/2024 - 11/15/2024 (10.5 weeks)\n"
                "- Partial disability: 11/16/2024 - 02/03/2025 (11.5 weeks, working "
                "reduced 24 hrs/week at modified duty)\n"
                "- Surgical recovery: 02/03/2025 - 03/14/2025 (5.5 weeks)\n\n"
                "Lost Wages Calculation:\n"
                "Total disability: 10.5 weeks x $2,052.00 = $21,546.00\n"
                "Partial disability: 11.5 weeks x ($2,052.00 - $1,368.00) = $7,866.00\n"
                "Surgical recovery: 5.5 weeks x $1,872.00 = $10,296.00\n"
                "Subtotal lost wages: $39,708.00\n"
                "Less: Short-term disability payments received: ($5,148.00)\n\n"
                "NET LOST WAGES: $34,560.00\n\n"
                "Documentation attached: Employer verification letter, pay stubs "
                "(June-August 2024), disability payment records."
            ),
        },
        # Page 13: Non-Economic Damages
        {
            "title": "XI. NON-ECONOMIC DAMAGES ANALYSIS",
            "body": (
                "Ms. Vasquez-Rodriguez has suffered significant non-economic damages "
                "as a result of the collision caused by the insured:\n\n"
                "Physical Pain and Suffering:\n"
                "Ms. Vasquez-Rodriguez has endured six months of persistent pain in her "
                "neck, lower back, and left shoulder. She has undergone three epidural "
                "steroid injections, 42 physical therapy sessions, and arthroscopic "
                "shoulder surgery. Despite treatment, she continues to experience daily "
                "pain rated at 4-6/10.\n\n"
                "Emotional Distress:\n"
                "Since the collision, Ms. Vasquez-Rodriguez has experienced anxiety while "
                "driving, difficulty sleeping due to pain, and depression related to her "
                "inability to perform her normal activities. She has been prescribed "
                "sertraline 50mg by her primary care physician.\n\n"
                "Loss of Enjoyment of Life:\n"
                "Prior to the accident, Ms. Vasquez-Rodriguez was an active individual "
                "who enjoyed hiking, swimming, and playing soccer in a recreational "
                "league. She has been unable to participate in any of these activities "
                "since the collision. She also struggles with basic household tasks "
                "including cleaning, cooking, and caring for her two children ages 8 "
                "and 11.\n\n"
                "Impact on Daily Living:\n"
                "- Cannot lift her children or carry groceries\n"
                "- Requires assistance with household chores\n"
                "- Cannot sit or stand for prolonged periods\n"
                "- Sleep disruption averaging 4-5 hours per night\n"
                "- Unable to drive for more than 20 minutes without pain"
            ),
        },
        # Page 14: Future Medical Expenses
        {
            "title": "XII. FUTURE MEDICAL EXPENSES",
            "body": (
                "Based on the medical opinions of Dr. Yamamoto and Dr. Park, "
                "Ms. Vasquez-Rodriguez will require the following future medical "
                "treatment:\n\n"
                "1. Lumbar Disc Surgery (Microdiscectomy)\n"
                "   Given the failure of conservative treatment, Dr. Yamamoto has "
                "recommended surgical intervention for the L4-L5 herniation.\n"
                "   Estimated cost: $45,000 - $65,000\n\n"
                "2. Post-Surgical Physical Therapy\n"
                "   12 weeks of PT following lumbar surgery\n"
                "   Estimated cost: $4,200\n\n"
                "3. Ongoing Pain Management\n"
                "   Annual pain management visits and potential facet joint injections "
                "for cervical spine\n"
                "   Estimated annual cost: $3,500 - $5,000 for 5 years = $17,500 - $25,000\n\n"
                "4. Continued Physical Therapy (Maintenance)\n"
                "   Monthly maintenance sessions for 2 years\n"
                "   Estimated cost: $8,400\n\n"
                "5. Future Shoulder Revision Surgery (Possible)\n"
                "   If current repair fails, full rotator cuff reconstruction may be "
                "needed\n"
                "   Estimated cost: $35,000 - $50,000 (50% probability per Dr. Yamamoto)\n\n"
                "ESTIMATED FUTURE MEDICAL COSTS:\n"
                "Low estimate: $75,100\n"
                "High estimate: $152,600\n"
                "Midpoint: $113,850"
            ),
        },
        # Page 15: Property Damage
        {
            "title": "XIII. PROPERTY DAMAGE",
            "body": (
                "Ms. Vasquez-Rodriguez's 2021 Honda Accord (VIN: 1HGCV1F34MA028847) "
                "sustained severe damage in the collision.\n\n"
                "Vehicle Information:\n"
                "- Year/Make/Model: 2021 Honda Accord Sport 1.5T\n"
                "- Mileage at time of loss: 38,472\n"
                "- Pre-accident fair market value: $27,800\n"
                "- Financing: Honda Financial Services, balance $18,200\n\n"
                "Damage Assessment:\n"
                "The vehicle was inspected by Pacific Coast Insurance Group's appraiser "
                "on September 10, 2024. The vehicle was determined to be a total loss. "
                "Primary damage areas included:\n"
                "- Driver's side doors (front and rear) crushed\n"
                "- Driver's side B-pillar deformed\n"
                "- Left front wheel and suspension assembly destroyed\n"
                "- Frame damage to left side rail\n"
                "- All airbags deployed (driver, passenger, side curtain, side torso)\n\n"
                "Settlement:\n"
                "Total loss value: $27,800.00\n"
                "Less salvage value: ($2,100.00)\n"
                "Net property damage payment: $25,700.00\n\n"
                "Additional property damage:\n"
                "- Personal items in vehicle: $1,240.00\n"
                "  (Laptop computer, nursing textbooks, gym bag with contents)\n"
                "- Rental vehicle (28 days): $1,680.00\n\n"
                "TOTAL PROPERTY DAMAGE: $28,620.00\n"
                "(Property damage has been separately resolved; included for context)"
            ),
        },
        # Page 16: Comparable Verdicts
        {
            "title": "XIV. COMPARABLE VERDICTS AND SETTLEMENTS",
            "body": (
                "The following verdicts and settlements from Sacramento County and "
                "surrounding jurisdictions support the valuation of this claim:\n\n"
                "1. Martinez v. Thompson (2024) - Sacramento County Superior Court\n"
                "   Intersection collision, disc herniation, shoulder tear\n"
                "   Verdict: $485,000 (past medicals: $92,000)\n\n"
                "2. Williams v. Patel (2023) - Sacramento County Superior Court\n"
                "   Red-light collision, lumbar disc herniation requiring surgery\n"
                "   Settlement: $425,000 (past medicals: $78,000)\n\n"
                "3. Johnson v. Rivera (2024) - Placer County Superior Court\n"
                "   T-bone collision, cervical/lumbar injuries, shoulder surgery\n"
                "   Verdict: $612,000 (past medicals: $105,000)\n\n"
                "4. Chen v. Blackstone (2023) - Yolo County Superior Court\n"
                "   Intersection collision, L4-L5 herniation, epidural injections\n"
                "   Settlement: $375,000 (past medicals: $68,000)\n\n"
                "5. Okafor v. Hansen (2024) - Sacramento County Superior Court\n"
                "   Rear-end collision, disc herniation, rotator cuff tear, surgery\n"
                "   Mediation settlement: $525,000 (past medicals: $96,000)\n\n"
                "Average comparable value: $484,400\n"
                "Ms. Vasquez-Rodriguez's claim falls squarely within this range given "
                "the severity of her injuries, the clear liability, and the substantial "
                "medical treatment required."
            ),
        },
        # Page 17: Demand Amount
        {
            "title": "XV. DEMAND AMOUNT",
            "body": (
                "Based on the foregoing analysis, we present the following demand:\n\n"
                "ECONOMIC DAMAGES:\n"
                "Past medical expenses:                    $87,342.18\n"
                "Past lost wages:                          $34,560.00\n"
                "Future medical expenses (midpoint):      $113,850.00\n"
                "Future lost earning capacity:              $24,000.00\n"
                "                                        ____________\n"
                "Total Economic Damages:                  $259,752.18\n\n"
                "NON-ECONOMIC DAMAGES:\n"
                "Physical pain and suffering:             $125,000.00\n"
                "Emotional distress:                       $50,000.00\n"
                "Loss of enjoyment of life:                $65,000.00\n"
                "                                        ____________\n"
                "Total Non-Economic Damages:              $240,000.00\n\n"
                "                                        ============\n"
                "TOTAL DEMAND:                            $499,752.18\n\n"
                "This demand is open for thirty (30) days from the date of this letter. "
                "We are prepared to negotiate in good faith and believe that mediation "
                "would be an appropriate forum for resolution.\n\n"
                "Please direct all correspondence to the undersigned."
            ),
        },
        # Page 18: Conclusion
        {
            "title": "XVI. CONCLUSION",
            "body": (
                "This demand package demonstrates that Elena Vasquez-Rodriguez has "
                "suffered severe and life-altering injuries as a direct result of "
                "Derek Marshall's negligence. The evidence of liability is overwhelming, "
                "and the damages are well-documented and supported by medical records, "
                "employer verification, and expert opinions.\n\n"
                "Ms. Vasquez-Rodriguez, a dedicated healthcare professional and mother "
                "of two, has been forced to endure months of pain, multiple invasive "
                "procedures, and significant disruption to her personal and professional "
                "life. She faces the prospect of additional surgery and years of ongoing "
                "treatment.\n\n"
                "We urge Pacific Coast Insurance Group to evaluate this claim fairly and "
                "promptly. The demand of $499,752.18 is reasonable and well within the "
                "range of comparable cases in this jurisdiction.\n\n"
                "We look forward to your timely response.\n\n"
                "Respectfully submitted,\n\n\n"
                "___________________________\n"
                "Ricardo Martinez, Esq.\n"
                "Martinez & Chen, LLP\n"
                "4200 Westfield Boulevard, Suite 1100\n"
                "Sacramento, CA 95814\n"
                "Tel: (916) 555-0187\n"
                "Fax: (916) 555-0188\n"
                "Email: rmartinez@martinezchen.com\n\n"
                "California State Bar No. 287451"
            ),
        },
    ]

    # Build each page
    for i, pc in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        # Title
        y = 72
        if i == 0:
            # Cover page: centered title, larger
            page.insert_text(
                pymupdf.Point(W / 2 - 100, y + 40),
                pc["title"],
                fontsize=22,
                fontname="hebo",
                color=(0, 0, 0),
            )
            y = 160
            # Subtitle
            if "subtitle" in pc:
                page.insert_text(
                    pymupdf.Point(72, y),
                    pc["subtitle"],
                    fontsize=14,
                    fontname="tiit",
                    color=(0.2, 0.2, 0.2),
                )
                y += 40
        else:
            # Section title
            page.insert_text(
                pymupdf.Point(72, y),
                pc["title"],
                fontsize=14,
                fontname="hebo",
                color=(0, 0, 0),
            )
            # Underline
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y + 4), pymupdf.Point(540, y + 4))
            shape.finish(color=(0, 0, 0), width=0.5)
            shape.commit()
            y += 28

        # Body text
        body_rect = pymupdf.Rect(72, y, 540, H - 60)
        page.insert_textbox(
            body_rect,
            pc["body"],
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number (skip cover page)
        if i > 0:
            page.insert_text(
                pymupdf.Point(W / 2 - 5, H - 36),
                str(i + 1),
                fontsize=9,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 18')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
