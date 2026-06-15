"""
Initial Setup: Create a 5-page legal declaration PDF without line numbers
Task ID: pdf_legal_047
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_047'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/declaration.pdf'

# Letter size in points
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

def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Case Caption and beginning of declaration ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Court header
    page.insert_text(pymupdf.Point(72, 60), "SUPERIOR COURT OF THE STATE OF CALIFORNIA", fontsize=11, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 76), "COUNTY OF LOS ANGELES", fontsize=11, fontname="hebo")

    # Case caption box
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    y = 120
    lines_p1 = [
        ("JENNIFER MARTINEZ, an individual,", "tiro", 11),
        ("", "tiro", 11),
        ("                    Plaintiff,", "tiit", 11),
        ("", "tiro", 11),
        ("        vs.                                                      Case No. 24STCV-08712", "tiro", 11),
        ("", "tiro", 11),
        ("GREENFIELD PROPERTY MANAGEMENT,", "tiro", 11),
        ("LLC, a California limited liability", "tiro", 11),
        ("company; and DOES 1 through 50,", "tiro", 11),
        ("inclusive,", "tiro", 11),
        ("", "tiro", 11),
        ("                    Defendants.", "tiit", 11),
        ("", "tiro", 11),
    ]
    for text, font, size in lines_p1:
        if text:
            page.insert_text(pymupdf.Point(72, y), text, fontsize=size, fontname=font)
        y += 18

    # Separator
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()
    y += 25

    # Declaration title
    page.insert_text(pymupdf.Point(150, y), "DECLARATION OF JENNIFER MARTINEZ", fontsize=12, fontname="hebo")
    y += 25
    page.insert_text(pymupdf.Point(130, y), "IN SUPPORT OF MOTION FOR SUMMARY JUDGMENT", fontsize=11, fontname="hebo")
    y += 30

    # Body text start
    body_lines_p1 = [
        "I, Jennifer Martinez, declare as follows:",
        "",
        "1.  I am the Plaintiff in the above-captioned action. I have personal",
        "knowledge of the facts stated herein, and if called as a witness, I could",
        "and would testify competently thereto.",
        "",
        "2.  I am a resident of the City of Los Angeles, County of Los Angeles,",
        "State of California. I have resided at 1847 Wilshire Boulevard, Apartment",
        "312, Los Angeles, California 90057, since March 15, 2021.",
        "",
        "3.  On or about June 1, 2023, I entered into a written residential lease",
        "agreement with Greenfield Property Management, LLC (hereinafter",
        "\"Greenfield\") for the rental of the above-described premises. A true and",
        "correct copy of the lease agreement is attached hereto as Exhibit A.",
    ]
    for line in body_lines_p1:
        if line:
            page.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="tiro")
        y += 16

    # --- Page 2: Continued declaration ---
    page2 = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    body_lines_p2 = [
        "4.  The monthly rent under the lease agreement was $2,450.00 per month,",
        "due on the first day of each calendar month. I have consistently paid my",
        "rent on time throughout the entirety of my tenancy, as evidenced by the",
        "bank statements attached hereto as Exhibit B.",
        "",
        "5.  Beginning in approximately September 2023, I began to notice",
        "significant water damage in the bathroom ceiling of my apartment. The",
        "plaster was bubbling and discolored, and there was a persistent musty",
        "odor consistent with mold growth.",
        "",
        "6.  On September 15, 2023, I submitted a written maintenance request to",
        "Greenfield's online tenant portal, describing the water damage and",
        "requesting immediate inspection and repair. A screenshot of this request",
        "is attached hereto as Exhibit C.",
        "",
        "7.  Despite my initial request, no maintenance personnel visited my",
        "apartment until October 3, 2023, a period of eighteen (18) days. When",
        "the maintenance worker, identified as Robert Tran, did arrive, he",
        "inspected the ceiling for approximately five minutes and stated that it",
        "was \"just cosmetic\" and did not require repair.",
        "",
        "8.  I followed up with two additional written requests on October 10,",
        "2023, and October 25, 2023, each time providing photographs documenting",
        "the worsening condition. Copies of these communications and photographs",
        "are attached hereto as Exhibit D.",
        "",
        "9.  On November 12, 2023, I hired an independent licensed contractor,",
        "David Park of Park Building Inspections, to assess the condition of my",
        "apartment. Mr. Park's report, attached hereto as Exhibit E, identified",
        "the following deficiencies:",
        "",
        "    a.  Active water intrusion from the unit above, originating from a",
        "        failed shower pan seal;",
        "",
        "    b.  Aspergillus mold growth covering approximately 4.5 square feet",
        "        of the bathroom ceiling;",
        "",
        "    c.  Structural damage to the ceiling joists, rated as requiring",
        "        immediate remediation.",
        "",
        "10. The cost of Mr. Park's inspection was $875.00, which I paid out of",
        "pocket. A receipt is attached hereto as Exhibit F.",
    ]
    for line in body_lines_p2:
        if line:
            page2.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="tiro")
        y += 16

    # --- Page 3: More declaration ---
    page3 = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    body_lines_p3 = [
        "11. On November 20, 2023, I sent a formal demand letter via certified",
        "mail to Greenfield's registered agent, Global Business Services, Inc.,",
        "at 500 South Grand Avenue, Suite 2100, Los Angeles, California 90071.",
        "The letter demanded that Greenfield remediate the mold and water damage",
        "within thirty (30) days. A copy of the letter and certified mail receipt",
        "are attached hereto as Exhibit G.",
        "",
        "12. Greenfield responded by letter dated December 5, 2023, in which it",
        "acknowledged receipt of my demand but stated that it believed the damage",
        "was caused by my \"improper ventilation habits\" and denied responsibility.",
        "A copy of Greenfield's response is attached hereto as Exhibit H.",
        "",
        "13. As a direct result of the mold exposure, I began experiencing",
        "respiratory symptoms in approximately October 2023, including persistent",
        "coughing, wheezing, and shortness of breath. I had no history of",
        "respiratory illness prior to this time.",
        "",
        "14. On January 8, 2024, I was seen by Dr. Alicia Nguyen, M.D., a",
        "board-certified pulmonologist at UCLA Medical Center. Dr. Nguyen",
        "diagnosed me with allergic bronchopulmonary aspergillosis, which she",
        "attributed to chronic mold exposure in my residence. Dr. Nguyen's",
        "medical report is attached hereto as Exhibit I.",
        "",
        "15. Dr. Nguyen prescribed a course of oral corticosteroids and an",
        "inhaled bronchodilator. I have incurred medical expenses totaling",
        "$4,327.50 to date in connection with the treatment of this condition.",
        "Copies of medical bills are attached hereto as Exhibit J.",
        "",
        "16. As a result of my respiratory condition, I was unable to perform",
        "my duties as a registered nurse at Cedars-Sinai Medical Center for a",
        "total of fourteen (14) workdays between January and March 2024. My",
        "base pay rate is $52.00 per hour, and I work twelve-hour shifts. My",
        "total lost wages during this period amount to $8,736.00. A letter from",
        "my employer confirming my absence is attached hereto as Exhibit K.",
        "",
        "17. On February 1, 2024, the Los Angeles County Department of Public",
        "Health conducted an inspection of my apartment following a complaint I",
        "filed on January 15, 2024. The inspector, Maria Santos, confirmed the",
        "presence of visible mold and issued a notice of violation to Greenfield.",
        "A copy of the inspection report and notice is attached as Exhibit L.",
        "",
        "18. Despite the notice of violation, Greenfield did not commence any",
        "remediation work until March 18, 2024, more than six months after my",
        "initial complaint.",
    ]
    for line in body_lines_p3:
        if line:
            page3.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="tiro")
        y += 16

    # --- Page 4: More declaration ---
    page4 = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    body_lines_p4 = [
        "19. The remediation work performed by Greenfield's contractor, Quick",
        "Fix Maintenance, Inc., was completed on April 5, 2024. However, Mr.",
        "Park conducted a follow-up inspection on April 20, 2024, and determined",
        "that the remediation was incomplete. Specifically, Mr. Park found that:",
        "",
        "    a.  The mold had been painted over rather than properly removed;",
        "",
        "    b.  The failed shower pan seal in the unit above had not been",
        "        replaced, meaning water intrusion was likely to recur;",
        "",
        "    c.  No air quality testing had been performed to verify that",
        "        airborne mold spore levels had returned to safe levels.",
        "",
        "Mr. Park's follow-up report is attached hereto as Exhibit M.",
        "",
        "20. Due to the continuing habitability issues, I was forced to vacate",
        "my apartment on May 1, 2024, and relocate to temporary housing at the",
        "Oakwood Apartments at 3636 Barham Boulevard, Los Angeles, California",
        "90068, at a monthly rate of $3,200.00. I have incurred relocation",
        "expenses of $2,150.00 for moving services and $1,500.00 in security",
        "deposit for the temporary unit.",
        "",
        "21. I continued to pay rent on the Wilshire Boulevard apartment through",
        "May 2024 in the amount of $2,450.00, as I had not yet been released",
        "from the lease. I consider this amount to have been paid under protest",
        "and seek its recovery in this action.",
        "",
        "22. In total, I have suffered the following damages as a direct and",
        "proximate result of Greenfield's failure to maintain habitable",
        "conditions:",
        "",
        "    a.  Medical expenses:                          $4,327.50",
        "    b.  Lost wages:                                $8,736.00",
        "    c.  Inspection costs:                          $1,750.00",
        "    d.  Relocation expenses:                       $3,650.00",
        "    e.  Excess rent (temporary housing premium):   $2,250.00",
        "    f.  Rent paid under protest (May 2024):        $2,450.00",
        "    g.  Emotional distress damages:               $25,000.00",
        "",
        "    TOTAL:                                        $48,163.50",
        "",
        "23. The emotional distress I have suffered includes anxiety, difficulty",
        "sleeping, and significant stress related to the health impacts of mold",
        "exposure and the uncertainty of my housing situation. I began seeing a",
        "licensed therapist, Dr. Sarah Kim, Ph.D., on February 15, 2024, and",
        "continue to attend weekly sessions. Dr. Kim's letter regarding my",
        "treatment is attached hereto as Exhibit N.",
    ]
    for line in body_lines_p4:
        if line:
            page4.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="tiro")
        y += 16

    # --- Page 5: Conclusion and signature ---
    page5 = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    body_lines_p5 = [
        "24. At no time during my tenancy did I engage in any conduct that would",
        "have caused or contributed to the water damage or mold growth in my",
        "apartment. I maintained the premises in a clean and sanitary condition",
        "and regularly used the exhaust fan while showering, as recommended by",
        "the building management.",
        "",
        "25. I have reviewed the terms of the lease agreement and find no",
        "provision that would shift responsibility for structural water damage",
        "or mold remediation to the tenant. To the contrary, Section 14.2 of",
        "the lease expressly states that the landlord shall maintain the",
        "structural elements of the building in good repair.",
        "",
        "26. I am informed and believe that Greenfield was aware of recurring",
        "plumbing issues in the building prior to my complaint. According to",
        "maintenance records obtained through discovery, at least three other",
        "units in the building experienced similar water intrusion issues between",
        "2021 and 2023, and Greenfield failed to address the root cause.",
        "",
        "27. I declare under penalty of perjury under the laws of the State of",
        "California that the foregoing is true and correct.",
        "",
        "",
        "Executed on August 12, 2024, at Los Angeles, California.",
        "",
        "",
        "",
        "",
        "                              _________________________________",
        "                              Jennifer Martinez",
        "                              Declarant",
    ]
    for line in body_lines_p5:
        if line:
            page5.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="tiro")
        y += 16

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
