"""
Initial Setup: Create a 30-page employee benefits handbook PDF with no bookmarks.
Task ID: pdf_fin_059
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_059'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/benefits_handbook.pdf'

# Page dimensions (Letter size)
W, H = 612, 792
MARGIN = 72
TEXT_W = W - 2 * MARGIN

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


# Section content for 30 pages of a realistic employee benefits handbook
SECTIONS = [
    # Health Insurance section (pages 1-9)
    {"title": "Health Insurance Overview", "body": (
        "Meridian Technologies is committed to providing comprehensive health insurance coverage "
        "for all eligible employees and their dependents. Our health insurance program is designed "
        "to help you and your family access quality healthcare while managing out-of-pocket costs.\n\n"
        "Eligibility begins on the first day of the month following 30 days of continuous employment. "
        "Full-time employees working 30 or more hours per week are eligible for all health plans. "
        "Part-time employees working 20-29 hours per week may enroll in the basic medical plan.\n\n"
        "Open enrollment occurs annually during the month of November, with coverage changes "
        "effective January 1st. Qualifying life events such as marriage, birth of a child, or "
        "loss of other coverage allow mid-year enrollment changes within 30 days of the event.\n\n"
        "The company contributes 80% of the premium for employee-only coverage and 65% for "
        "dependent coverage across all plan tiers. Premium contributions are deducted pre-tax "
        "from your bi-weekly paycheck."
    )},
    {"title": "Medical Plan Options", "body": (
        "Meridian Technologies offers three medical plan options to meet varying healthcare needs:\n\n"
        "PPO Preferred Plan: This plan provides the broadest network of physicians and hospitals. "
        "Annual deductible is $500 individual / $1,000 family. In-network copays are $25 for "
        "primary care and $50 for specialists. Out-of-network coverage is available at 60% after "
        "a separate $1,500 deductible. Maximum out-of-pocket is $4,000 individual / $8,000 family.\n\n"
        "PPO Standard Plan: A mid-range option with a $1,000 individual / $2,000 family deductible. "
        "In-network copays are $35 for primary care and $65 for specialists. Prescription drug "
        "coverage includes $10 generic / $35 preferred brand / $60 non-preferred brand copays. "
        "Maximum out-of-pocket is $6,000 individual / $12,000 family.\n\n"
        "High Deductible Health Plan (HDHP): Paired with a Health Savings Account (HSA), this plan "
        "has a $2,800 individual / $5,600 family deductible. The company contributes $750 annually "
        "to your HSA. After the deductible is met, the plan covers 80% of eligible expenses. "
        "Maximum out-of-pocket is $7,050 individual / $14,100 family."
    )},
    {"title": "In-Network Provider Directory", "body": (
        "Our PPO network includes over 850,000 healthcare providers nationwide through the BlueCross "
        "BlueShield national network. To find in-network providers, visit the benefits portal at "
        "benefits.meridiantech.com or call Member Services at 1-800-555-0142.\n\n"
        "When selecting a primary care physician (PCP), consider providers within 25 miles of your "
        "home or workplace for convenience. While a PCP referral is not required for specialist "
        "visits under our PPO plans, coordinating care through your PCP ensures better health outcomes.\n\n"
        "Telehealth services are available 24/7 through MDLive at no additional cost for PPO Preferred "
        "and PPO Standard members. HDHP members pay the standard office visit rate until their "
        "deductible is met. Telehealth visits cover non-emergency medical conditions, behavioral "
        "health consultations, and dermatology evaluations."
    )},
    {"title": "Prescription Drug Coverage", "body": (
        "All medical plans include integrated prescription drug coverage administered by OptumRx. "
        "Medications are classified into four tiers:\n\n"
        "Tier 1 - Generic: $10 copay (retail 30-day) / $25 copay (mail order 90-day)\n"
        "Tier 2 - Preferred Brand: $35 copay (retail) / $87.50 copay (mail order)\n"
        "Tier 3 - Non-Preferred Brand: $60 copay (retail) / $150 copay (mail order)\n"
        "Tier 4 - Specialty: 25% coinsurance up to $250 per fill\n\n"
        "Prior authorization is required for certain medications including specialty drugs, "
        "compound medications, and select brand-name drugs when generic equivalents are available. "
        "Step therapy protocols apply to specific drug classes.\n\n"
        "The formulary is updated quarterly. Employees will receive 60-day notice of any formulary "
        "changes affecting their current prescriptions. Transition supply provisions allow a one-time "
        "30-day fill of non-formulary medications during plan transitions."
    )},
    {"title": "Dental Plan - PPO Option", "body": (
        "The Dental PPO plan through Delta Dental provides coverage for preventive, basic, and major "
        "dental services. This plan allows you to visit any licensed dentist, with higher benefit "
        "levels when using in-network Delta Dental Premier or PPO providers.\n\n"
        "Preventive Services (covered at 100% in-network):\n"
        "- Oral examinations (two per calendar year)\n"
        "- Cleanings / prophylaxis (two per calendar year)\n"
        "- Bitewing X-rays (one set per calendar year)\n"
        "- Full mouth X-rays (one set per 36 months)\n"
        "- Fluoride treatment (one per calendar year, age 18 and under)\n\n"
        "Basic Services (covered at 80% after deductible):\n"
        "- Fillings (amalgam and composite)\n"
        "- Simple extractions\n"
        "- Root canal therapy\n"
        "- Periodontal scaling and root planing\n\n"
        "Annual maximum benefit: $2,000 per person. Calendar year deductible: $50 individual / "
        "$150 family. The deductible is waived for preventive services."
    )},
    {"title": "Dental Plan - DHMO Option", "body": (
        "The Dental DHMO (Dental Health Maintenance Organization) plan offers lower out-of-pocket "
        "costs in exchange for using a designated network of dental providers. Each member must "
        "select a primary care dentist from the DHMO network.\n\n"
        "There are no annual deductibles or annual maximum benefit limits under the DHMO plan. "
        "Copayments are fixed and listed in the Schedule of Benefits:\n\n"
        "Office Visit: $0\n"
        "Preventive Cleaning: $0\n"
        "Composite Filling (1 surface): $25\n"
        "Composite Filling (2 surfaces): $40\n"
        "Root Canal (anterior): $95\n"
        "Root Canal (molar): $175\n"
        "Crown (porcelain fused to metal): $250\n"
        "Extraction (simple): $15\n"
        "Extraction (surgical): $75\n\n"
        "Orthodontic coverage is included for dependent children under age 19, with a $1,500 "
        "lifetime maximum copay. Adult orthodontics is available at a 25% discount off usual fees."
    )},
    {"title": "Orthodontic Benefits", "body": (
        "Orthodontic benefits are available under both the Dental PPO and Dental DHMO plans, "
        "subject to different terms and conditions.\n\n"
        "Dental PPO Orthodontic Coverage:\n"
        "- Available for dependent children under age 19\n"
        "- Lifetime maximum benefit: $1,500\n"
        "- Plan pays 50% of covered charges after deductible\n"
        "- Pre-treatment estimate required for treatment plans exceeding $500\n\n"
        "Dental DHMO Orthodontic Coverage:\n"
        "- Available for dependent children under age 19\n"
        "- Fixed copayment schedule (no lifetime maximum)\n"
        "- Must use designated orthodontic providers within the DHMO network\n\n"
        "Adult orthodontic treatment (age 19+) is not covered under the Dental PPO plan. "
        "DHMO members age 19+ may access orthodontic services at a 25% discount through "
        "network providers. Invisalign and similar clear aligner treatments are covered at "
        "the same rate as traditional braces when deemed medically necessary."
    )},
    {"title": "Vision Plan Benefits", "body": (
        "The Vision Plan through VSP (Vision Service Plan) covers routine eye examinations, "
        "corrective lenses, and frames or contact lenses.\n\n"
        "Eye Examination: One comprehensive exam per calendar year, $15 copay with in-network "
        "provider. Exam includes dilation, refraction, and assessment of eye health.\n\n"
        "Lenses (one pair per calendar year):\n"
        "- Single vision: covered in full after $25 copay\n"
        "- Bifocal: covered in full after $25 copay\n"
        "- Trifocal: covered in full after $25 copay\n"
        "- Progressive: $55 copay + covered in full\n\n"
        "Frames: $180 allowance every other calendar year with participating providers. "
        "20% discount on amounts exceeding the allowance.\n\n"
        "Contact Lenses (in lieu of glasses): $150 allowance per calendar year for contacts "
        "and contact lens fitting/evaluation. Elective contact lenses receive the full allowance. "
        "Medically necessary contact lenses are covered in full."
    )},
    {"title": "Vision Plan - Additional Benefits", "body": (
        "Beyond standard vision coverage, our VSP plan includes several enhanced benefits:\n\n"
        "Laser Vision Correction: VSP members receive an average of 15% off the regular price "
        "or 5% off a promotional offer for LASIK or PRK from contracted facilities. A pre-procedure "
        "consultation is covered at no additional cost.\n\n"
        "TruHearing Discount: VSP members and their families can access discounted hearing aids "
        "starting at $599 per aid through TruHearing. This includes a comprehensive hearing exam, "
        "fitting, and three follow-up visits.\n\n"
        "Diabetic Eyecare Plus Program: Members diagnosed with Type 1 or Type 2 diabetes are "
        "eligible for additional services including retinal screening annually and up to four "
        "additional office visits per year for diabetes-related eye conditions.\n\n"
        "Safety Eyewear: Employees in designated safety-sensitive roles receive a $150 annual "
        "allowance for prescription safety glasses meeting ANSI Z87.1 standards. Contact the "
        "Safety Office for eligibility determination."
    )},
    # Retirement section (pages 10-19)
    {"title": "Retirement Benefits Overview", "body": (
        "Meridian Technologies provides a robust retirement benefits package to help employees "
        "build long-term financial security. Our retirement program includes both defined "
        "contribution and defined benefit components.\n\n"
        "Retirement plan participation is voluntary for the 401(k) plan, while eligible employees "
        "are automatically enrolled in the defined benefit pension plan after meeting service "
        "requirements. Both plans are designed to work together to provide comprehensive "
        "retirement income.\n\n"
        "Financial planning resources are available through Fidelity Investments, our retirement "
        "plan administrator. Employees may schedule one-on-one consultations with a financial "
        "advisor at no cost. Online planning tools and educational webinars are available at "
        "netbenefits.fidelity.com.\n\n"
        "The company reviews retirement benefit offerings annually and adjusts contribution "
        "rates and plan features based on market conditions and regulatory requirements."
    )},
    {"title": "401(k) Plan - Enrollment and Contributions", "body": (
        "The Meridian Technologies 401(k) Savings Plan allows eligible employees to save for "
        "retirement on a tax-advantaged basis. Key plan features:\n\n"
        "Eligibility: All employees age 21 or older with at least 90 days of service.\n\n"
        "Auto-Enrollment: New hires are automatically enrolled at a 4% pre-tax contribution "
        "rate with annual 1% auto-escalation up to 10%. Employees may opt out or change their "
        "contribution rate at any time through the Fidelity portal.\n\n"
        "Contribution Limits (2025):\n"
        "- Employee elective deferrals: $23,500\n"
        "- Catch-up contributions (age 50+): additional $7,500\n"
        "- Super catch-up (ages 60-63): additional $11,250\n"
        "- Combined employee + employer limit: $70,000\n\n"
        "Contribution Types:\n"
        "- Pre-tax: Reduces current taxable income; taxed upon withdrawal\n"
        "- Roth (after-tax): No current tax benefit; qualified withdrawals are tax-free\n"
        "- After-tax (non-Roth): For mega backdoor Roth conversions (if applicable)\n\n"
        "Employees may change contribution rates and Roth/pre-tax elections at any time."
    )},
    {"title": "401(k) Plan - Employer Match and Vesting", "body": (
        "Employer Matching Contributions:\n"
        "Meridian Technologies matches 100% of the first 4% of eligible compensation contributed "
        "by the employee, plus 50% of the next 2% contributed. This means an employee contributing "
        "6% of pay receives a 5% employer match.\n\n"
        "Example for an employee earning $100,000 annually:\n"
        "Employee contributes 6% = $6,000\n"
        "Employer matches first 4% (100%) = $4,000\n"
        "Employer matches next 2% (50%) = $1,000\n"
        "Total employer match = $5,000 (effective 5% of salary)\n\n"
        "Vesting Schedule for Employer Contributions:\n"
        "- Year 1: 0%\n"
        "- Year 2: 25%\n"
        "- Year 3: 50%\n"
        "- Year 4: 75%\n"
        "- Year 5+: 100%\n\n"
        "Employee contributions are always 100% vested. Vesting service is calculated from date "
        "of hire and includes periods of leave and rehire."
    )},
    {"title": "401(k) Plan - Investment Options", "body": (
        "The plan offers a diversified lineup of investment options across major asset classes:\n\n"
        "Target Date Funds (Vanguard Target Retirement Series):\n"
        "Funds ranging from Target Retirement 2025 through Target Retirement 2070. These funds "
        "automatically adjust their asset allocation as you approach retirement.\n\n"
        "Index Funds:\n"
        "- Vanguard 500 Index Fund (VFIAX) - Large Cap US Equity\n"
        "- Vanguard Mid-Cap Index Fund (VIMAX) - Mid Cap US Equity\n"
        "- Vanguard Small-Cap Index Fund (VSMAX) - Small Cap US Equity\n"
        "- Vanguard Total International Stock Index (VTIAX) - International Equity\n"
        "- Vanguard Total Bond Market Index (VBTLX) - US Fixed Income\n\n"
        "Actively Managed Funds:\n"
        "- Fidelity Contrafund (FCNTX) - Large Cap Growth\n"
        "- T. Rowe Price Blue Chip Growth (TRBCX) - Large Cap Growth\n"
        "- PIMCO Total Return (PTTRX) - Intermediate Bond\n\n"
        "Self-Directed Brokerage: Available through Fidelity BrokerageLink for employees seeking "
        "access to a broader range of investments. A $50 annual fee applies."
    )},
    {"title": "401(k) Plan - Loans and Hardship Withdrawals", "body": (
        "Plan Loans:\n"
        "Participants may borrow from their 401(k) account under the following terms:\n"
        "- Minimum loan amount: $1,000\n"
        "- Maximum loan amount: lesser of 50% of vested balance or $50,000\n"
        "- Maximum of two outstanding loans at any time\n"
        "- General purpose loans: repayment period up to 5 years\n"
        "- Primary residence loans: repayment period up to 15 years\n"
        "- Interest rate: Prime rate + 1% at time of origination\n"
        "- $75 loan origination fee\n\n"
        "Repayment is made through payroll deduction. Missed payments may result in the "
        "outstanding balance being treated as a taxable distribution.\n\n"
        "Hardship Withdrawals:\n"
        "Available for immediate and heavy financial need, including:\n"
        "- Medical expenses not covered by insurance\n"
        "- Purchase of primary residence\n"
        "- Tuition and related educational fees\n"
        "- Prevention of eviction or mortgage foreclosure\n"
        "- Funeral and burial expenses\n"
        "- Repair of damage to primary residence qualifying as a casualty loss\n\n"
        "Hardship withdrawals are subject to income tax and a 10% early withdrawal penalty "
        "if under age 59-1/2."
    )},
    {"title": "Pension Plan - Eligibility and Benefits", "body": (
        "The Meridian Technologies Defined Benefit Pension Plan provides a guaranteed monthly "
        "retirement income based on your years of service and final average compensation.\n\n"
        "Eligibility:\n"
        "- All full-time employees hired before January 1, 2020\n"
        "- Minimum 5 years of vesting service required\n"
        "- Normal retirement age: 65\n"
        "- Early retirement: age 55 with 10 years of service\n\n"
        "Benefit Formula:\n"
        "Monthly Pension = 1.5% x Final Average Compensation x Years of Credited Service\n\n"
        "Final Average Compensation is calculated as the average of your highest consecutive "
        "60 months of eligible compensation within the last 120 months of service.\n\n"
        "Example Calculation:\n"
        "Employee with 25 years of service and $120,000 final average compensation:\n"
        "Monthly Pension = 1.5% x $120,000 x 25 = $45,000 annually ($3,750/month)\n\n"
        "The pension benefit is payable as a single life annuity, joint and survivor annuity "
        "(50%, 75%, or 100%), or a 10-year certain and life annuity."
    )},
    {"title": "Pension Plan - Vesting and Service Credits", "body": (
        "Vesting:\n"
        "The pension plan uses a 5-year cliff vesting schedule. Participants with fewer than "
        "5 years of vesting service are 0% vested. Upon completing 5 years, participants become "
        "100% vested in their accrued benefit.\n\n"
        "Vesting service includes all periods of employment with Meridian Technologies, including:\n"
        "- Active employment\n"
        "- Approved leaves of absence (up to 12 months)\n"
        "- Military leave under USERRA\n"
        "- Periods of disability receiving company-sponsored LTD benefits\n\n"
        "Breaks in Service:\n"
        "A break in service occurs when an employee completes fewer than 501 hours in a plan "
        "year. If consecutive breaks in service equal or exceed prior vesting service (and the "
        "participant was not yet vested), prior service may be forfeited under the rule of parity.\n\n"
        "Service Credit Purchases:\n"
        "Employees who previously worked for companies acquired by Meridian Technologies may "
        "be eligible to purchase up to 5 years of prior service credit. Contact HR Benefits "
        "for eligibility and cost calculations."
    )},
    {"title": "Pension Plan - Early Retirement and Distributions", "body": (
        "Early Retirement:\n"
        "Participants who have reached age 55 with at least 10 years of service may elect early "
        "retirement. The benefit is calculated using the standard formula, then reduced by 5% "
        "for each year before age 65 (up to a maximum 50% reduction).\n\n"
        "Early Retirement Reduction Example:\n"
        "Age at retirement: 60 (5 years before normal retirement)\n"
        "Reduction: 5% x 5 = 25%\n"
        "If full pension at 65 would be $3,750/month, early retirement pension = $2,812.50/month\n\n"
        "Deferred Vested Benefit:\n"
        "Participants who leave the company after vesting but before retirement eligibility may "
        "commence benefits at age 65, or elect a reduced benefit starting at age 55.\n\n"
        "Lump Sum Option:\n"
        "At retirement or termination, vested participants may elect a lump sum distribution "
        "in lieu of monthly annuity payments. The lump sum is calculated using IRS-prescribed "
        "mortality tables and interest rates. This option may be rolled over to an IRA or "
        "another qualified plan to defer taxation."
    )},
    {"title": "Supplemental Retirement Accounts", "body": (
        "In addition to the 401(k) and pension plans, Meridian Technologies offers supplemental "
        "retirement savings vehicles for eligible employees.\n\n"
        "Nonqualified Deferred Compensation Plan (NQDC):\n"
        "Available to employees with base compensation exceeding $155,000 annually. The NQDC "
        "plan allows participants to defer up to 50% of base salary and up to 100% of bonus "
        "compensation beyond the IRS limits applicable to the 401(k) plan.\n\n"
        "Key features:\n"
        "- Investment options mirror the 401(k) fund lineup\n"
        "- Distribution elections made at time of deferral (in-service date or separation)\n"
        "- Lump sum or installment payment options (2-15 years)\n"
        "- Company match: 25% of first 6% deferred (subject to vesting)\n\n"
        "457(b) Plan:\n"
        "A select group of management and highly compensated employees may also participate "
        "in a governmental 457(b) plan, allowing additional pre-tax deferrals of up to $23,500 "
        "(2025 limit). This is separate from and in addition to 401(k) limits.\n\n"
        "IMPORTANT: NQDC plan assets are subject to the claims of company creditors in the "
        "event of bankruptcy. Consult a financial advisor before making deferral elections."
    )},
    {"title": "Retirement Planning Resources", "body": (
        "Meridian Technologies partners with Fidelity Investments to provide comprehensive "
        "retirement planning support to all employees.\n\n"
        "Online Tools (netbenefits.fidelity.com):\n"
        "- Retirement income calculator\n"
        "- Social Security benefit estimator\n"
        "- Investment analysis and portfolio review\n"
        "- Beneficiary management\n"
        "- Required Minimum Distribution calculator\n\n"
        "Financial Wellness Program:\n"
        "- Monthly educational webinars on retirement and investment topics\n"
        "- Annual retirement readiness assessment\n"
        "- Access to Fidelity financial planners (phone and video consultations)\n"
        "- Pre-retirement planning workshops for employees age 50+\n\n"
        "One-on-One Financial Planning:\n"
        "Employees may schedule up to three complimentary sessions per year with a Certified "
        "Financial Planner through Fidelity. Topics include retirement income planning, Social "
        "Security optimization, tax-efficient withdrawal strategies, and estate planning basics.\n\n"
        "Contact Fidelity at 1-800-555-0198 or visit the HR Benefits office for assistance."
    )},
    # Leave Policies section (pages 20-30)
    {"title": "Leave Policies Overview", "body": (
        "Meridian Technologies recognizes that employees need time away from work for personal "
        "needs, family obligations, and health-related reasons. Our comprehensive leave policies "
        "are designed to support work-life balance while maintaining operational efficiency.\n\n"
        "All leave types described in this section are administered by the HR Benefits team in "
        "coordination with the employee's direct manager. Leave requests should be submitted "
        "through the Workday HR portal at least 14 calendar days in advance when foreseeable.\n\n"
        "Meridian Technologies complies with all applicable federal, state, and local leave laws. "
        "Where company policy provides greater benefits than legally required, the more generous "
        "provision applies. Employees in states with additional leave protections (California, "
        "New York, Washington, etc.) may be entitled to benefits exceeding those listed here.\n\n"
        "Leave policies are reviewed annually and updated as needed. Employees will be notified "
        "of any material changes at least 30 days before the effective date."
    )},
    {"title": "Paid Time Off (PTO) Program", "body": (
        "Meridian Technologies provides a consolidated Paid Time Off (PTO) program that combines "
        "vacation, personal, and sick time into a single flexible bank of paid days.\n\n"
        "PTO Accrual Rates (based on years of service):\n"
        "Years 0-2: 15 days (120 hours) per year, accruing at 4.62 hours per bi-weekly pay period\n"
        "Years 3-5: 20 days (160 hours) per year, accruing at 6.15 hours per bi-weekly pay period\n"
        "Years 6-10: 25 days (200 hours) per year, accruing at 7.69 hours per bi-weekly pay period\n"
        "Years 11+: 30 days (240 hours) per year, accruing at 9.23 hours per bi-weekly pay period\n\n"
        "Carryover Policy:\n"
        "Employees may carry over up to 40 hours of unused PTO into the next calendar year. "
        "Excess hours above 40 will be forfeited on January 1st. Employees are encouraged to "
        "use their PTO throughout the year.\n\n"
        "PTO Payout at Separation:\n"
        "Upon voluntary or involuntary separation, accrued but unused PTO will be paid out in "
        "the final paycheck at the employee's current base rate of pay, up to a maximum of "
        "the current year's accrual amount."
    )},
    {"title": "PTO Scheduling and Blackout Periods", "body": (
        "PTO Scheduling Guidelines:\n"
        "- Requests for 3 or more consecutive days should be submitted at least 14 days in advance\n"
        "- Requests for 1-2 days should be submitted at least 3 business days in advance\n"
        "- Manager approval is required for all PTO requests\n"
        "- Managers should respond to PTO requests within 2 business days\n"
        "- Scheduling conflicts are resolved based on seniority within the same department\n\n"
        "Blackout Periods:\n"
        "Certain departments may designate blackout periods during peak business cycles when "
        "PTO is restricted or limited. Common blackout periods include:\n"
        "- Finance Department: Month-end close (last 3 business days of each month)\n"
        "- IT Department: System migration windows (as announced)\n"
        "- Sales Department: Quarter-end (last week of March, June, September, December)\n"
        "- All departments: Annual inventory (typically first week of January)\n\n"
        "Unplanned Absences:\n"
        "Employees who are unable to report to work due to illness or emergency should notify "
        "their manager before their scheduled start time. Three consecutive days of unplanned "
        "absence may require a physician's note upon return."
    )},
    {"title": "Company Holidays", "body": (
        "Meridian Technologies observes the following paid holidays for all eligible employees:\n\n"
        "Fixed Holidays (10 days):\n"
        "1. New Year's Day - January 1\n"
        "2. Martin Luther King Jr. Day - Third Monday in January\n"
        "3. Presidents' Day - Third Monday in February\n"
        "4. Memorial Day - Last Monday in May\n"
        "5. Juneteenth - June 19\n"
        "6. Independence Day - July 4\n"
        "7. Labor Day - First Monday in September\n"
        "8. Thanksgiving Day - Fourth Thursday in November\n"
        "9. Day After Thanksgiving - Fourth Friday in November\n"
        "10. Christmas Day - December 25\n\n"
        "Floating Holidays (2 days):\n"
        "Each employee receives two floating holidays per calendar year, which may be used for "
        "religious observances, cultural celebrations, or personal occasions. Floating holidays "
        "must be used within the calendar year and do not carry over.\n\n"
        "When a fixed holiday falls on a Saturday, it is observed on the preceding Friday. "
        "When a holiday falls on a Sunday, it is observed on the following Monday."
    )},
    {"title": "Family and Medical Leave Act (FMLA)", "body": (
        "In compliance with the Family and Medical Leave Act of 1993, Meridian Technologies "
        "provides eligible employees up to 12 weeks of unpaid, job-protected leave per 12-month "
        "period for qualifying reasons.\n\n"
        "Eligibility Requirements:\n"
        "- Employed for at least 12 months (need not be consecutive)\n"
        "- Worked at least 1,250 hours during the 12 months preceding the leave\n"
        "- Work at a location where the company employs 50 or more employees within 75 miles\n\n"
        "Qualifying Reasons for FMLA Leave:\n"
        "1. Birth and care of a newborn child\n"
        "2. Placement of a child for adoption or foster care\n"
        "3. Care for an immediate family member with a serious health condition\n"
        "4. Medical leave when unable to work due to a serious health condition\n"
        "5. Qualifying exigency arising from a family member's military service\n\n"
        "Military Caregiver Leave:\n"
        "Eligible employees may take up to 26 weeks of leave in a single 12-month period to "
        "care for a covered servicemember with a serious injury or illness."
    )},
    {"title": "FMLA - Leave Administration", "body": (
        "Requesting FMLA Leave:\n"
        "Employees must provide 30 days' advance notice when the need for leave is foreseeable. "
        "When leave is unforeseeable, employees must provide notice as soon as practicable, "
        "generally within one to two business days.\n\n"
        "Medical Certification:\n"
        "The company requires a completed Certification of Health Care Provider form (DOL Form "
        "WH-380-E for employee's own condition or WH-380-F for family member) within 15 calendar "
        "days of the leave request. Failure to provide adequate certification may result in "
        "denial or delay of FMLA leave.\n\n"
        "Intermittent Leave:\n"
        "FMLA leave may be taken intermittently or on a reduced schedule when medically necessary. "
        "Employees on intermittent leave must follow the company's normal absence reporting "
        "procedures and make reasonable efforts to schedule treatment outside of business hours.\n\n"
        "Benefits During FMLA Leave:\n"
        "- Health insurance continues on the same terms as active employment\n"
        "- Employee must continue paying their share of premiums\n"
        "- PTO does not accrue during unpaid FMLA leave\n"
        "- 401(k) contributions are suspended during unpaid leave"
    )},
    {"title": "FMLA - Reinstatement and Return to Work", "body": (
        "Job Reinstatement:\n"
        "Upon return from FMLA leave, employees are entitled to be restored to the same position "
        "or an equivalent position with equivalent pay, benefits, and working conditions.\n\n"
        "An equivalent position must have:\n"
        "- Substantially similar duties, responsibilities, and status\n"
        "- Same pay and benefits\n"
        "- Same or geographically proximate work location\n"
        "- Same shift or schedule\n\n"
        "Return to Work Requirements:\n"
        "Employees returning from FMLA leave for their own serious health condition must provide "
        "a fitness-for-duty certification from their healthcare provider before returning to work. "
        "The certification must address the employee's ability to perform the essential functions "
        "of their position.\n\n"
        "Key Employee Exception:\n"
        "Salaried employees in the highest-paid 10% of the workforce may be denied reinstatement "
        "if restoration would cause substantial and grievous economic injury to company operations. "
        "Affected employees will be notified of their key employee status when leave is requested.\n\n"
        "Failure to Return:\n"
        "Employees who do not return to work at the end of FMLA leave may be required to repay "
        "the company's share of health insurance premiums paid during the leave period."
    )},
    {"title": "Parental Leave Policy", "body": (
        "Meridian Technologies provides paid parental leave to support employees welcoming a new "
        "child through birth, adoption, or foster placement.\n\n"
        "Paid Parental Leave Benefits:\n"
        "- Birth parents: 16 weeks at 100% base pay\n"
        "- Non-birth parents (spouse/partner): 8 weeks at 100% base pay\n"
        "- Adoptive parents: 12 weeks at 100% base pay\n"
        "- Foster parents: 6 weeks at 100% base pay\n\n"
        "Eligibility:\n"
        "- Full-time employees with at least 6 months of continuous service\n"
        "- Part-time employees with at least 12 months of service (prorated benefit)\n\n"
        "Parental leave must commence within 12 months of the birth, adoption, or placement. "
        "Leave may be taken in a single continuous block or, with manager approval, in two "
        "separate blocks within the 12-month period.\n\n"
        "Parental leave runs concurrently with FMLA leave where applicable. If paid parental "
        "leave is exhausted, employees may use PTO or request unpaid FMLA leave for the "
        "remainder of the 12-week FMLA entitlement."
    )},
    {"title": "Parental Leave - Additional Support", "body": (
        "Gradual Return Program:\n"
        "Employees returning from parental leave of 8 weeks or more may participate in the "
        "gradual return program. This allows a reduced schedule (minimum 60% of normal hours) "
        "at full pay for up to 4 weeks following the end of parental leave.\n\n"
        "Lactation Support:\n"
        "Meridian Technologies provides dedicated lactation rooms at all office locations with "
        "50 or more employees. Rooms are equipped with hospital-grade breast pumps, refrigerators, "
        "and comfortable seating. Nursing parents are provided reasonable break time for "
        "expressing milk for up to one year after the child's birth.\n\n"
        "Childcare Resources:\n"
        "- Dependent Care Flexible Spending Account (DCFSA): Pre-tax contributions up to $5,000/year\n"
        "- Backup childcare: 15 days per year through Bright Horizons at $25/day\n"
        "- Childcare referral service through LifeWorks EAP\n\n"
        "Fertility and Adoption Assistance:\n"
        "- Fertility treatment coverage: up to $25,000 lifetime maximum\n"
        "- Adoption assistance: up to $10,000 per adoption for legal fees, court costs, and "
        "agency fees\n"
        "- Surrogacy support: up to $15,000 for agency and legal fees"
    )},
    {"title": "Other Leave Types", "body": (
        "Bereavement Leave:\n"
        "- Immediate family (spouse, child, parent, sibling): 5 paid days\n"
        "- Extended family (grandparent, in-law, aunt/uncle): 3 paid days\n"
        "- Close friend or colleague: 1 paid day\n"
        "- Additional unpaid leave may be granted with manager approval\n\n"
        "Jury Duty:\n"
        "Employees called for jury duty receive full pay for up to 10 days per calendar year. "
        "Beyond 10 days, the company will pay the difference between jury duty compensation and "
        "regular pay. Employees must provide a copy of the jury summons to HR.\n\n"
        "Voting Leave:\n"
        "Up to 2 hours of paid time off to vote in federal, state, and local elections when "
        "polling hours do not allow sufficient time outside of working hours.\n\n"
        "Military Leave:\n"
        "In compliance with USERRA, employees called to active duty or training receive unpaid "
        "leave with full reinstatement rights. The company will pay the difference between "
        "military pay and base salary for up to 12 months of active duty.\n\n"
        "Personal Leave of Absence:\n"
        "After exhausting all PTO, employees may request an unpaid personal leave of up to 30 "
        "days. Approval is at the discretion of the department head and HR."
    )},
    {"title": "Leave Policy Administration and Compliance", "body": (
        "Record Keeping:\n"
        "All leave requests, approvals, and related documentation are maintained in the Workday "
        "HR system. Employees are responsible for submitting leave requests promptly and providing "
        "required documentation within specified timeframes.\n\n"
        "Anti-Retaliation:\n"
        "Meridian Technologies strictly prohibits retaliation against any employee for requesting "
        "or taking leave under any company policy or applicable law. Any employee who believes "
        "they have experienced retaliation should report it immediately to HR or the Ethics Hotline "
        "at 1-800-555-0177.\n\n"
        "Fraud Prevention:\n"
        "Employees who provide false or misleading information in connection with a leave request "
        "may be subject to disciplinary action up to and including termination. The company "
        "reserves the right to require additional documentation or certification to verify "
        "leave eligibility.\n\n"
        "Questions and Assistance:\n"
        "For questions about leave policies, eligibility, or administration, contact:\n"
        "- HR Benefits Team: benefits@meridiantech.com\n"
        "- HR Service Center: 1-800-555-0134 (Monday-Friday, 8am-6pm ET)\n"
        "- Workday HR Portal: hr.meridiantech.com\n\n"
        "This handbook is provided for informational purposes and does not constitute a contract "
        "of employment. Meridian Technologies reserves the right to modify or discontinue any "
        "benefit program at any time."
    )},
]


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    for i, section in enumerate(SECTIONS):
        page = doc.new_page(width=W, height=H)

        y = MARGIN

        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN, y + 30), pymupdf.Point(W - MARGIN, y + 30))
        shape.finish(color=(0.2, 0.3, 0.5), width=1.5)
        shape.commit()

        # Section title
        page.insert_text(
            pymupdf.Point(MARGIN, y + 20),
            section["title"],
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.2, 0.4),
        )

        y += 50

        # Page indicator (top right)
        page.insert_text(
            pymupdf.Point(W - MARGIN - 60, MARGIN - 10),
            f"Page {i + 1}",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Body text in a textbox
        text_rect = pymupdf.Rect(MARGIN, y, W - MARGIN, H - MARGIN - 30)
        page.insert_textbox(
            text_rect,
            section["body"],
            fontsize=10.5,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Footer
        page.insert_text(
            pymupdf.Point(MARGIN, H - MARGIN + 10),
            "Meridian Technologies - Employee Benefits Handbook - Confidential",
            fontsize=8,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )
        page.insert_text(
            pymupdf.Point(W - MARGIN - 20, H - MARGIN + 10),
            str(i + 1),
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # Ensure NO bookmarks
    doc.set_toc([])

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {len(SECTIONS)}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
