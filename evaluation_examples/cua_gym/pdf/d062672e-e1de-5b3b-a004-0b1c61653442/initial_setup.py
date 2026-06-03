"""
Initial Setup: Create a 30-page scanned deposition transcript (images only, no text layer)
Task ID: pdf_legal_011
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import textwrap

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_011'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/scanned_deposition.pdf'


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


# Realistic deposition transcript content for 30 pages
DEPOSITION_PAGES = []

# Page 1: Title page
DEPOSITION_PAGES.append("""
                    IN THE UNITED STATES DISTRICT COURT
                    FOR THE NORTHERN DISTRICT OF CALIFORNIA

    WESTFIELD COMMERCIAL PROPERTIES, LLC,
                    Plaintiff,

            v.                              Case No. 3:24-cv-01847-JST

    MERIDIAN CONSTRUCTION GROUP, INC.,
    and APEX ENGINEERING SOLUTIONS, INC.,
                    Defendants.

    ____________________________________________________________

                    DEPOSITION OF MICHAEL R. HARTWELL

                    Volume I

                    March 12, 2025

    Reported by:
    Jennifer A. Collins, CSR No. 12847
    Collins & Associates Court Reporters
    500 Market Street, Suite 1200
    San Francisco, California 94105
    (415) 555-2847
""")

# Page 2: Appearances
DEPOSITION_PAGES.append("""
                        APPEARANCES

    FOR THE PLAINTIFF:

        MORRISON & KESSLER LLP
        BY: DAVID A. MORRISON, ESQ.
            SARAH T. BLACKWELL, ESQ.
        1200 Pacific Avenue, 34th Floor
        San Francisco, California 94111
        (415) 555-8900
        dmorrison@morrisonkessler.com

    FOR DEFENDANT MERIDIAN CONSTRUCTION GROUP, INC.:

        CHEN, NAKAMURA & WELLS LLP
        BY: ROBERT J. CHEN, ESQ.
            PATRICIA L. NGUYEN, ESQ.
        600 Montgomery Street, Suite 2800
        San Francisco, California 94111
        (415) 555-3200
        rchen@cnwlaw.com

    FOR DEFENDANT APEX ENGINEERING SOLUTIONS, INC.:

        THE BRADSHAW FIRM
        BY: KATHERINE M. BRADSHAW, ESQ.
        100 Pine Street, Suite 1500
        San Francisco, California 94111
        (415) 555-7400
        kbradshaw@bradshawfirm.com

    ALSO PRESENT:    Thomas J. Whitfield, Corporate Representative
                     Meridian Construction Group, Inc.
""")

# Page 3: Beginning of testimony
DEPOSITION_PAGES.append("""
                                                          Page 3

 1       THE VIDEOGRAPHER:  We are now on the record.
 2  The time is 9:32 a.m.  Today is March 12, 2025.
 3  This is the video deposition of Michael R.
 4  Hartwell, in the matter of Westfield Commercial
 5  Properties, LLC versus Meridian Construction Group,
 6  Inc. and Apex Engineering Solutions, Inc., Case
 7  Number 3:24-cv-01847-JST, in the United States
 8  District Court for the Northern District of
 9  California.
10       Will the court reporter please swear in the
11  witness.
12       THE REPORTER:  Would you raise your right
13  hand, please.
14            MICHAEL R. HARTWELL,
15  having been first duly sworn, testified as follows:
16              EXAMINATION BY MR. MORRISON
17  Q.   Good morning, Mr. Hartwell.  Would you please
18       state your full name for the record?
19  A.   Michael Raymond Hartwell.
20  Q.   And what is your current address?
21  A.   1847 Elm Grove Drive, Palo Alto, California,
22       94301.
23  Q.   And your date of birth?
24  A.   September 14, 1971.
25  Q.   Mr. Hartwell, what is your current occupation?
""")

# Pages 4-30: Continued testimony
testimony_blocks = [
    # Page 4
    """
                                                          Page 4

 1  A.   I am the Senior Vice President of Development
 2       at Westfield Commercial Properties.
 3  Q.   How long have you held that position?
 4  A.   Since January of 2019.  So roughly six years
 5       now.
 6  Q.   And what are your primary responsibilities in
 7       that role?
 8  A.   I oversee all commercial development projects
 9       for the company's western region portfolio.
10       That includes site acquisition, project
11       planning, contractor selection, and
12       construction oversight for properties in
13       California, Oregon, Washington, and Nevada.
14  Q.   How many projects have you overseen in that
15       capacity?
16  A.   Approximately thirty-five to forty projects
17       since I started.  Some are still ongoing.
18  Q.   Now, I'd like to direct your attention to
19       the Bayshore Commerce Center project.  Are
20       you familiar with that project?
21  A.   Yes, very much so.  That was one of our
22       flagship developments.
23  Q.   Can you describe the project for the record?
24  A.   The Bayshore Commerce Center is a mixed-use
25       commercial development located at 2400 Bayshore
""",
    # Page 5
    """
                                                          Page 5

 1       Boulevard in South San Francisco.  It was
 2       designed to be a 450,000-square-foot complex
 3       comprising office space, retail outlets, and a
 4       parking structure.  The total project budget
 5       was approximately $187 million.
 6  Q.   When did the project commence?
 7  A.   We broke ground in March of 2023.  The
 8       original completion date was set for September
 9       2024.
10  Q.   And who was the general contractor for the
11       project?
12  A.   Meridian Construction Group.  They were
13       awarded the contract following a competitive
14       bidding process in late 2022.
15  Q.   Was Apex Engineering Solutions involved in the
16       project as well?
17  A.   Yes.  Apex was the structural engineering firm
18       retained by Meridian as a subcontractor for
19       the steel and concrete work on the main office
20       tower.
21  Q.   Let me show you what has been marked as
22       Exhibit 1.
23            MR. CHEN:  May I see that, please?
24            MR. MORRISON:  Of course.
25            (Exhibit 1 was marked for identification.)
""",
    # Page 6
    """
                                                          Page 6

 1  Q.   (BY MR. MORRISON)  Mr. Hartwell, do you
 2       recognize Exhibit 1?
 3  A.   Yes.  This is the Master Construction
 4       Agreement between Westfield and Meridian,
 5       dated November 15, 2022.
 6  Q.   And is this your signature on page 34?
 7  A.   Yes, it is.
 8  Q.   Now, directing your attention to Section 4.2
 9       of the agreement, can you read that section
10       for the record?
11  A.   Section 4.2 reads: "Contractor shall complete
12       all work in accordance with the project
13       schedule attached hereto as Exhibit A and shall
14       notify Owner in writing within five business
15       days of any anticipated delay exceeding ten
16       calendar days."
17  Q.   Did Meridian comply with this provision?
18            MR. CHEN:  Objection.  Calls for a legal
19       conclusion.  You may answer.
20  A.   No.  In my experience, they did not comply
21       with this provision on multiple occasions.
22  Q.   Can you give me a specific example?
23  A.   The first significant delay occurred in June
24       of 2023.  We discovered that the foundation
25       work for Building C was approximately three
""",
    # Page 7
    """
                                                          Page 7

 1       weeks behind schedule.  We were not notified
 2       by Meridian until I personally visited the
 3       site and observed the delay myself.
 4  Q.   What happened when you discovered this delay?
 5  A.   I immediately called a meeting with James
 6       Thornton, the project manager for Meridian.
 7       He acknowledged the delay but attributed it to
 8       unexpected soil conditions that required
 9       additional excavation.
10  Q.   Did you find that explanation satisfactory?
11  A.   Not entirely.  The geotechnical report that we
12       had commissioned prior to construction had
13       identified potential soil instability in that
14       area.  It was in the project documentation that
15       Meridian received during the bidding process.
16  Q.   So the soil conditions were known before
17       construction began?
18  A.   That is correct.  The geotechnical report,
19       prepared by Pacific Geological Associates in
20       August 2022, specifically noted elevated
21       moisture content and clay composition in the
22       Building C footprint area.  It recommended
23       deep foundation pilings rather than standard
24       spread footings.
25  Q.   Did Meridian follow that recommendation?
""",
    # Page 8
    """
                                                          Page 8

 1  A.   No.  And that is actually one of the central
 2       issues in this case.  Meridian initially used
 3       spread footings for Building C, which was
 4       contrary to the geotechnical recommendations.
 5       When the settlement occurred, they had to
 6       retrofit the entire foundation with micro-piles
 7       at an additional cost of approximately $4.2
 8       million.
 9  Q.   Who bore that cost?
10  A.   Meridian billed Westfield for the remediation
11       work, claiming it was a change order resulting
12       from unforeseen site conditions.  We disputed
13       that characterization.
14  Q.   Let me show you Exhibit 2.
15            (Exhibit 2 was marked for identification.)
16  Q.   (BY MR. MORRISON)  Do you recognize this
17       document?
18  A.   Yes.  This is the Change Order Request
19       submitted by Meridian, dated July 28, 2023,
20       for the Building C foundation remediation.
21       The total amount requested was $4,247,800.
22  Q.   And what was Westfield's response?
23  A.   We rejected the change order on August 12,
24       2023, on the grounds that the soil conditions
25       were documented in the pre-construction
""",
    # Page 9
    """
                                                          Page 9

 1       geotechnical report and that Meridian's
 2       failure to follow the foundation
 3       recommendations constituted a deviation from
 4       the approved construction documents.
 5  Q.   How did Meridian respond to that rejection?
 6  A.   They threatened to stop work on the project
 7       if we didn't approve the change order.  We
 8       received a letter from their attorney, Mr.
 9       Chen's firm, on August 20, 2023, indicating
10       that Meridian would exercise its right to
11       suspend work under Section 7.3 of the
12       contract.
13  Q.   Did Meridian actually suspend work?
14  A.   Not entirely.  They reduced their workforce on
15       site from approximately 180 workers to about
16       60.  They continued work on Buildings A and B
17       but effectively stopped all work on Building C
18       and the parking structure.
19  Q.   For how long did this reduced workforce
20       situation continue?
21  A.   From approximately late August through mid-
22       October 2023.  So about seven weeks.
23  Q.   What was the impact of that slowdown?
24  A.   It was devastating to the project timeline.
25       We estimated that the seven-week slowdown
""",
    # Page 10
    """
                                                         Page 10

 1       resulted in an overall project delay of
 2       approximately four months, because the
 3       Building C and parking structure work was on
 4       the critical path.
 5  Q.   Can you explain what you mean by "critical
 6       path"?
 7  A.   In project management, the critical path is
 8       the longest sequence of dependent tasks that
 9       determines the minimum project duration.  If
10       any task on the critical path is delayed, the
11       entire project completion date is pushed back
12       by the same amount.  Building C's foundation
13       work had to be completed before the steel
14       erection could begin, which had to be done
15       before the exterior cladding, and so on.
16  Q.   Were there financial consequences to Westfield
17       as a result of this delay?
18  A.   Yes, significant consequences.  First, we had
19       pre-leasing agreements with three anchor
20       tenants -- Pacific Digital Solutions, Hartwick
21       Medical Group, and Cascade Ventures -- that
22       included occupancy date commitments.  When it
23       became clear we would miss those dates, we had
24       to renegotiate the leases.  Pacific Digital
25       ultimately received a rent concession of $2.1
""",
    # Page 11
    """
                                                         Page 11

 1       million over the first three years of their
 2       lease.  Hartwick Medical Group withdrew entirely
 3       and leased space at a competing development in
 4       Millbrae.  Cascade Ventures negotiated a
 5       15 percent reduction in their base rent.
 6  Q.   What was the total financial impact to
 7       Westfield from these lease modifications?
 8  A.   Our finance team calculated the total impact
 9       at approximately $8.3 million in lost or
10       reduced revenue over the initial lease terms.
11  Q.   Were there other financial consequences?
12  A.   Yes.  We incurred additional carrying costs
13       on our construction loan.  The project was
14       financed through a $140 million construction
15       facility with First Pacific Bank.  The
16       additional four months of interest expense
17       amounted to approximately $3.7 million.
18  Q.   Any other damages?
19  A.   We also had to retain a separate construction
20       management firm, Kensington Project Services,
21       to provide additional oversight after we lost
22       confidence in Meridian's ability to manage the
23       project effectively.  That engagement cost
24       approximately $1.8 million through project
25       completion.
""",
    # Page 12
    """
                                                         Page 12

 1  Q.   Let's talk about Apex Engineering Solutions
 2       and their role in the project.  When did you
 3       first become aware of issues with Apex's work?
 4  A.   In September 2023, our independent structural
 5       inspector, Dr. Raymond Patel from Structural
 6       Integrity Associates, identified anomalies in
 7       the steel connections on the third and fourth
 8       floors of Building A.
 9  Q.   What kind of anomalies?
10  A.   The inspection revealed that approximately
11       15 percent of the moment-frame connections on
12       those floors had incomplete penetration welds.
13       In layman's terms, the welds that were supposed
14       to create a rigid connection between the beams
15       and columns were deficient.
16  Q.   Was this a safety concern?
17  A.   Absolutely.  Dr. Patel's preliminary
18       assessment indicated that the deficient
19       connections could compromise the building's
20       seismic resistance.  Given that we're in a
21       high seismic zone here in the Bay Area, this
22       was an extremely serious finding.
23            MS. BRADSHAW:  Objection.  Lack of
24       foundation.  The witness is not a structural
25       engineer.
""",
    # Page 13
    """
                                                         Page 13

 1            MR. MORRISON:  He's testifying to what he
 2       was told by the structural inspector.
 3            MS. BRADSHAW:  Noted.
 4  Q.   (BY MR. MORRISON)  What steps did Westfield
 5       take in response to Dr. Patel's findings?
 6  A.   We immediately issued a stop-work order for
 7       all steel erection on Building A pending a
 8       comprehensive inspection.  We also notified
 9       Meridian and Apex in writing and demanded an
10       explanation and a remediation plan.
11  Q.   What was Apex's response?
12  A.   Apex's project engineer, Steven Nakamura,
13       initially disputed the findings.  He claimed
14       that the welds met the minimum requirements
15       under the applicable building code.  However,
16       when we retained a third-party testing firm,
17       Bay Area Metallurgical Testing, to conduct
18       ultrasonic testing of the welds, the results
19       confirmed Dr. Patel's findings and actually
20       showed the problem was more widespread than
21       initially thought.
22  Q.   How much more widespread?
23  A.   The ultrasonic testing revealed that
24       approximately 22 percent of all moment-frame
25       connections across Buildings A and B had
""",
    # Page 14
    """
                                                         Page 14

 1       deficient welds.  That represented roughly 340
 2       connections out of a total of approximately
 3       1,550 moment-frame connections.
 4  Q.   What was the remediation plan?
 5  A.   After considerable back and forth, it was
 6       agreed that all deficient connections would
 7       need to be repaired.  This involved grinding
 8       out the existing welds and re-welding them to
 9       specification.  The work had to be done under
10       continuous third-party inspection, which added
11       significant cost and time.
12  Q.   What was the cost of the welding remediation?
13  A.   The total cost for the weld repairs, including
14       the third-party inspection, was approximately
15       $6.8 million.
16  Q.   Who paid for that?
17  A.   Meridian initially covered the cost but has
18       been seeking reimbursement from Westfield as
19       part of their counterclaim.  Apex has taken
20       the position that they are not responsible
21       because they claim their welders followed
22       Meridian's instructions and the approved
23       fabrication drawings.
24  Q.   Let's take a short break.  It's about 10:45.
25            THE VIDEOGRAPHER:  We are going off the
""",
    # Page 15
    """
                                                         Page 15

 1       record.  The time is 10:47 a.m.
 2            (Recess taken from 10:47 a.m. to
 3             11:03 a.m.)
 4            THE VIDEOGRAPHER:  We are back on the
 5       record.  The time is 11:03 a.m.
 6  Q.   (BY MR. MORRISON)  Mr. Hartwell, before the
 7       break we were discussing the welding defects.
 8       I'd like to now turn to the issue of the
 9       Building B envelope problems.  Can you describe
10       what happened?
11  A.   Yes.  In January 2024, shortly after the
12       Building B exterior curtain wall was
13       substantially complete, we began experiencing
14       water infiltration during rainstorms.  The
15       water was entering at multiple locations on the
16       north and west facades, primarily around the
17       window assemblies and at the floor slab edges.
18  Q.   How was this discovered?
19  A.   The tenant improvement contractor for Pacific
20       Digital Solutions reported water staining on
21       the interior drywall on the sixth floor.  When
22       we investigated, we found evidence of water
23       intrusion on floors four through eight.
24  Q.   What was the cause of the water infiltration?
25  A.   Our building envelope consultant, Weathertight
""",
    # Page 16
    """
                                                         Page 16

 1       Associates, conducted a thorough investigation
 2       over a three-week period.  They performed water
 3       testing using ASTM E1105 methodology and found
 4       multiple deficiencies.  The primary issues were
 5       improper sealant application at the curtain
 6       wall mullion joints, missing or improperly
 7       installed flashing at the floor slab edges, and
 8       defective gaskets in approximately 30 percent
 9       of the window assemblies.
10  Q.   Who was responsible for the curtain wall
11       installation?
12  A.   The curtain wall was installed by Pacific
13       Glazing Systems, a subcontractor to Meridian.
14       However, I should note that Apex Engineering
15       was responsible for the structural attachment
16       design of the curtain wall anchorage system.
17       Weathertight Associates found that some of the
18       water intrusion was related to inadequate
19       thermal breaks in the anchorage details, which
20       was an Apex design issue.
21  Q.   What was the cost to remediate the building
22       envelope issues?
23  A.   The total cost for the envelope repairs was
24       $3.4 million.  That included removal and
25       replacement of sealants, installation of
""",
    # Page 17
    """
                                                         Page 17

 1       additional flashing, replacement of defective
 2       window gaskets, and repair of interior damage
 3       from the water intrusion.
 4  Q.   Were there additional consequential damages?
 5  A.   Yes.  The envelope remediation delayed Pacific
 6       Digital Solutions' occupancy by an additional
 7       two months beyond the already-delayed schedule.
 8       This triggered a liquidated damages clause in
 9       their lease, resulting in a credit of $450,000
10       to Pacific Digital.  Additionally, the interior
11       damage to the tenant improvement work that had
12       already been completed cost approximately
13       $780,000 to repair.
14  Q.   I'd like to show you Exhibit 7.
15            (Exhibit 7 was marked for identification.)
16  Q.   (BY MR. MORRISON)  Can you identify this
17       document?
18  A.   This is a summary spreadsheet prepared by our
19       project controls team showing the cumulative
20       cost overruns and delay damages as of December
21       31, 2024.
22  Q.   Can you walk us through the major categories?
23  A.   Certainly.  The spreadsheet shows the
24       following categories of damages.  Foundation
25       remediation for Building C: $4,247,800.  Steel
""",
    # Page 18
    """
                                                         Page 18

 1       connection welding repairs: $6,800,000.
 2       Building envelope remediation: $3,400,000.
 3       Interior damage repairs: $780,000.  Additional
 4       construction management: $1,800,000.
 5       Additional construction loan interest:
 6       $3,700,000.  Tenant lease concessions and
 7       credits: $10,850,000.  Lost rental income
 8       during extended construction: $2,400,000.
 9       Third-party inspection and testing:
10       $1,200,000.  The total shown on the
11       spreadsheet is $35,177,800.
12  Q.   Is that the total amount of damages Westfield
13       is claiming in this action?
14  A.   That figure represents the direct and
15       consequential damages.  I understand that our
16       legal team has also included a claim for loss
17       of anticipated profits from the delayed
18       operations, but I don't know the exact amount
19       of that claim.
20            MR. CHEN:  We'll reserve our objection to
21       the admissibility of this exhibit and the
22       damage calculations at trial.
23  Q.   (BY MR. MORRISON)  Mr. Hartwell, did Meridian
24       ever acknowledge responsibility for any of
25       these delays or defects?
""",
    # Page 19
    """
                                                         Page 19

 1  A.   Not formally.  In informal discussions,
 2       James Thornton, the Meridian project manager,
 3       acknowledged to me on at least two occasions
 4       that the project had experienced significant
 5       management challenges.  But in their formal
 6       correspondence, Meridian has consistently
 7       taken the position that the delays and cost
 8       overruns were caused by design changes
 9       initiated by Westfield and unforeseen site
10       conditions.
11  Q.   Were there design changes initiated by
12       Westfield?
13  A.   There were some minor design modifications,
14       yes.  But nothing that would account for the
15       magnitude of the delays and cost overruns we
16       experienced.
17  Q.   Can you describe the design changes?
18  A.   There were three formal change orders initiated
19       by Westfield.  The first was a modification to
20       the lobby finishes in Building A to upgrade
21       from standard granite to custom marble.  That
22       was a $340,000 change.  The second was an
23       addition of a fitness center on the ground
24       floor of Building B, which was approximately
25       $890,000.  The third was a reconfiguration of
""",
    # Page 20
    """
                                                         Page 20

 1       the parking structure entrance to improve
 2       traffic flow, at a cost of approximately
 3       $225,000.  So the total Westfield-initiated
 4       changes were about $1.455 million, which is
 5       less than one percent of the total project
 6       budget.
 7  Q.   Did any of these changes affect the critical
 8       path of the project?
 9  A.   No.  All three changes were on non-critical
10       path activities and were scheduled to be
11       performed concurrently with other work.  The
12       lobby finish change didn't even begin until
13       the building was substantially enclosed, and
14       the fitness center addition was incorporated
15       into the tenant improvement phase.
16  Q.   Let me ask you about the project schedule
17       more broadly.  You mentioned the original
18       completion date was September 2024.  When was
19       the project actually completed?
20  A.   Building A received its temporary certificate
21       of occupancy on February 14, 2025.  Building B
22       received its TCO on January 28, 2025.
23       Building C is still not complete as of today.
24       The current estimated completion date for
25       Building C is June 2025.
""",
    # Page 21
    """
                                                         Page 21

 1  Q.   So the project is approximately 17 to 21
 2       months behind schedule?
 3  A.   For Building C, yes, approximately 21 months
 4       behind the original schedule.  Buildings A and
 5       B are approximately 17 months behind.
 6  Q.   I'd like to turn now to the communications
 7       between Westfield and Meridian during the
 8       course of the project.  How frequently did you
 9       communicate with Meridian's team?
10  A.   During the active construction phase, we had
11       weekly on-site progress meetings.  I typically
12       attended every other week, with my project
13       manager, Elena Rodriguez, attending the
14       alternate weeks.  In addition to the formal
15       meetings, there were numerous phone calls and
16       emails on a daily basis.
17  Q.   Who were your primary points of contact at
18       Meridian?
19  A.   James Thornton was the project manager and my
20       primary day-to-day contact.  His supervisor,
21       Vice President of Operations Marcus Williams,
22       would get involved when there were disputes or
23       escalations.  I also had some direct contact
24       with the company's CEO, Richard Meridian, on
25       two or three occasions when things got
""",
    # Page 22
    """
                                                         Page 22

 1       particularly contentious.
 2  Q.   You mentioned Elena Rodriguez.  What is her
 3       role?
 4  A.   Elena is the Senior Project Manager at
 5       Westfield.  She was responsible for the
 6       day-to-day oversight of the Bayshore project.
 7       She reported directly to me.
 8  Q.   Is Ms. Rodriguez still employed by Westfield?
 9  A.   Yes, she is.
10  Q.   Will she be available for deposition?
11            MR. MORRISON:  We've already designated
12       Ms. Rodriguez as a witness.  Her deposition is
13       scheduled for next week.
14            MR. CHEN:  Thank you.
15  Q.   (BY MR. MORRISON)  Mr. Hartwell, I'd like to
16       show you Exhibit 12.
17            (Exhibit 12 was marked for identification.)
18  Q.   Do you recognize this document?
19  A.   Yes.  This is an email chain between myself
20       and Marcus Williams from October 2023,
21       regarding the workforce reduction and the
22       disputed change order for the Building C
23       foundation work.
24  Q.   Can you read the highlighted portion of your
25       email dated October 3, 2023?
""",
    # Page 23
    """
                                                         Page 23

 1  A.   My email states: "Marcus, I want to be direct
 2       about the situation.  Westfield cannot accept
 3       the current pace of work.  The reduction in
 4       workforce is causing cascading delays across
 5       all project phases.  If Meridian does not
 6       restore full staffing within ten business days,
 7       we will have no choice but to issue a notice
 8       of default under Section 14.1 of the Master
 9       Construction Agreement.  I strongly urge us to
10       schedule a meeting to resolve the change order
11       dispute before it escalates further."
12  Q.   And what was Mr. Williams' response?
13  A.   He responded the same day, stating -- and I'm
14       paraphrasing -- that Meridian was experiencing
15       cash flow difficulties due to Westfield's
16       refusal to pay the change order, and that the
17       workforce reduction was a necessary business
18       decision.  He also suggested that we engage in
19       mediation, as provided for in Section 15 of
20       the contract.
21  Q.   Did the parties engage in mediation?
22  A.   We attempted mediation in November 2023 with
23       retired Judge William Henderson as the
24       mediator.  Unfortunately, the mediation was
25       unsuccessful.  The parties were too far apart
""",
    # Page 24
    """
                                                         Page 24

 1       on the fundamental issues.  Meridian wanted
 2       full payment of the $4.2 million change order
 3       plus additional compensation for what they
 4       termed "acceleration costs."  Westfield's
 5       position was that Meridian owed us damages
 6       for the delays and defective work.
 7  Q.   After the mediation failed, what happened?
 8  A.   We issued a formal notice of default on
 9       December 15, 2023, giving Meridian 30 days to
10       cure the defaults identified in the notice.
11       Those defaults included the failure to
12       maintain adequate workforce levels, the
13       foundation deficiencies, the welding defects,
14       and the failure to comply with the project
15       schedule.
16  Q.   Did Meridian cure the defaults?
17  A.   Partially.  They restored workforce levels
18       in early January 2024, but the foundation and
19       welding issues required ongoing remediation
20       that took several more months to complete.
21       And of course, the building envelope problems
22       emerged shortly after that.
23  Q.   At any point did Westfield consider
24       terminating Meridian's contract?
25  A.   Yes.  We seriously considered it in early
""",
    # Page 25
    """
                                                         Page 25

 1       2024.  However, after consulting with our
 2       legal team and our construction consultant,
 3       we concluded that terminating Meridian and
 4       bringing in a new general contractor at that
 5       stage would have caused even greater delays
 6       and costs.  The project was approximately
 7       65 percent complete at that point, and the
 8       learning curve for a new contractor, combined
 9       with the mobilization time, would likely have
10       added another six to eight months to the
11       schedule.
12  Q.   So Westfield chose to continue with Meridian?
13  A.   Yes, but with significantly enhanced oversight
14       and monitoring.  That's when we brought in
15       Kensington Project Services as an independent
16       construction manager.  We also required
17       Meridian to submit weekly progress reports with
18       detailed scheduling updates, which they had not
19       been providing consistently.
20  Q.   How would you characterize the working
21       relationship between Westfield and Meridian
22       after the notice of default?
23  A.   It was professional but strained.  Both sides
24       had lawyers involved in most communications.
25       The weekly meetings became more formal, with
""",
    # Page 26
    """
                                                         Page 26

 1       attorneys present on both sides.  It wasn't
 2       the collaborative relationship we had hoped
 3       for at the outset of the project.
 4            MR. MORRISON:  I'd like to take a lunch
 5       break at this point.  We can resume at 1:00.
 6            MR. CHEN:  That's fine.
 7            THE VIDEOGRAPHER:  We are going off the
 8       record.  The time is 12:18 p.m.
 9            (Lunch recess taken from 12:18 p.m. to
10             1:07 p.m.)
11            THE VIDEOGRAPHER:  We are back on the
12       record.  The time is 1:07 p.m.
13  Q.   (BY MR. MORRISON)  Good afternoon, Mr.
14       Hartwell.  I'd like to now discuss the
15       current status of the project and Westfield's
16       ongoing damages.  What is the current status
17       of the Bayshore Commerce Center?
18  A.   As I mentioned, Buildings A and B have
19       received their temporary certificates of
20       occupancy.  Pacific Digital Solutions has
21       moved into their space in Building B as of
22       last month.  Cascade Ventures is currently
23       completing their tenant improvements in
24       Building A and expects to move in by April.
25       Building C remains under construction with
""",
    # Page 27
    """
                                                         Page 27

 1       an estimated completion date of June 2025.
 2  Q.   Has Westfield been able to lease the remaining
 3       space in Buildings A and B?
 4  A.   We have leased approximately 78 percent of the
 5       available space.  However, I should note that
 6       the delays significantly impacted our leasing
 7       efforts.  Several prospective tenants who were
 8       in advanced negotiations during the original
 9       construction timeline chose to lease space
10       elsewhere when it became clear that our project
11       would be substantially delayed.
12  Q.   Can you quantify the impact on leasing?
13  A.   Our original pro forma projected that we would
14       be 95 percent leased within six months of
15       completion.  Based on our current trajectory,
16       we don't expect to reach that level until mid-
17       2026 at the earliest.  The carrying cost of
18       the unleased space, including debt service,
19       property taxes, and operating expenses, is
20       approximately $180,000 per month.
21  Q.   Are there any outstanding disputes with
22       Meridian regarding final payment?
23  A.   Yes.  Meridian has submitted its application
24       for final payment in the amount of $12.3
25       million for work completed on Buildings A and
""",
    # Page 28
    """
                                                         Page 28

 1       B.  Westfield is withholding that payment
 2       pending resolution of the disputes and has
 3       applied backcharges totaling $8.7 million
 4       against the amount owed.  The net amount in
 5       dispute is therefore approximately $21 million
 6       -- the $12.3 million Meridian claims we owe
 7       them, plus the $8.7 million we claim they owe
 8       us.
 9            MR. CHEN:  I want to note for the record
10       that Meridian disputes the characterization
11       of the backcharges and will address those in
12       detail during Mr. Thornton's deposition.
13            MR. MORRISON:  Understood.
14  Q.   (BY MR. MORRISON)  Mr. Hartwell, one final
15       area.  Have you personally had any
16       conversations with Richard Meridian, the CEO
17       of Meridian Construction Group, about
18       resolving this dispute?
19  A.   Yes.  I spoke with Richard on two occasions.
20       The first was in October 2023, during the
21       workforce reduction issue.  He was cordial but
22       firm that Meridian needed the change order
23       payment to maintain cash flow.  The second
24       conversation was in February 2024, after the
25       building envelope problems were discovered.
""",
    # Page 29
    """
                                                         Page 29

 1       That conversation was less cordial.  He
 2       accused Westfield of nickel-and-diming
 3       Meridian and said that we were responsible for
 4       many of the project's problems because of what
 5       he called "constantly changing requirements."
 6       I disagreed with that characterization.
 7  Q.   Is there anything else you'd like to add
 8       regarding the issues we've discussed today?
 9  A.   I would just say that the Bayshore Commerce
10       Center was supposed to be Westfield's premier
11       development in the Bay Area market.  We
12       invested enormous resources in planning and
13       design to make it a landmark project.  The
14       construction deficiencies and delays have not
15       only cost us tens of millions of dollars but
16       have also damaged our reputation in the market
17       and with our tenants and investors.  It has
18       been deeply disappointing.
19            MR. MORRISON:  I have no further questions
20       at this time.  I'll reserve the right to
21       examine further after defendants' questioning.
22            MR. CHEN:  I'd like to begin my
23       examination.  We'll try to be efficient.
24            MS. BRADSHAW:  I'll reserve my questions
25       until after Mr. Chen.
""",
    # Page 30
    """
                                                         Page 30

 1            EXAMINATION BY MR. CHEN
 2  Q.   Good afternoon, Mr. Hartwell.  I have some
 3       questions on behalf of Meridian Construction
 4       Group.
 5  A.   Good afternoon.
 6  Q.   You testified earlier that the geotechnical
 7       report identified potential soil issues in the
 8       Building C area.  Isn't it true that the report
 9       also noted that the conditions were "within
10       acceptable parameters for standard foundation
11       design"?
12  A.   I believe the report stated that the conditions
13       could be managed with either standard or deep
14       foundation methods, but recommended deep
15       foundations as the more conservative approach.
16  Q.   So it's fair to say that standard foundations
17       were an option considered in the report?
18            MR. MORRISON:  Objection.  Mischaracterizes
19       the document.  The report recommended deep
20       foundations.
21  Q.   (BY MR. CHEN)  You can answer.
22  A.   The report discussed both options but
23       recommended deep foundations.  Standard
24       foundations were mentioned as feasible only
25       under certain conditions that, as it turned
""",
]

for block in testimony_blocks:
    DEPOSITION_PAGES.append(block)


def create_initial():
    """Create a 30-page scanned deposition PDF with images only (no text layer)."""
    from PIL import Image, ImageDraw, ImageFont
    import pymupdf

    os.makedirs(LEGAL_DIR, exist_ok=True)

    # Page dimensions for Letter size at 200 DPI
    DPI = 200
    PAGE_W = int(8.5 * DPI)   # 1700
    PAGE_H = int(11.0 * DPI)  # 2200

    # Try to find a monospace or serif font
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
        '/usr/share/fonts/truetype/freefont/FreeMono.ttf',
    ]
    font_path = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break

    if font_path:
        body_font = ImageFont.truetype(font_path, 18)
    else:
        body_font = ImageFont.load_default()

    # Create the PDF from rendered page images
    doc = pymupdf.open()

    for page_idx, page_text in enumerate(DEPOSITION_PAGES):
        # Create image for this page
        img = Image.new('RGB', (PAGE_W, PAGE_H), color=(252, 250, 245))
        draw = ImageDraw.Draw(img)

        # Add slight "scan" artifacts - a faint border shadow
        for i in range(5):
            shade = 220 - i * 10
            draw.rectangle([i, i, PAGE_W - 1 - i, PAGE_H - 1 - i],
                           outline=(shade, shade, shade))

        # Render text line by line
        lines = page_text.strip().split('\n')
        y = 80
        line_height = 28

        for line in lines:
            if y + line_height > PAGE_H - 80:
                break
            draw.text((100, y), line, fill=(25, 25, 30), font=body_font)
            y += line_height

        # Add subtle scan noise/specks
        import random
        random.seed(42 + page_idx)
        for _ in range(30):
            x = random.randint(0, PAGE_W - 1)
            sy = random.randint(0, PAGE_H - 1)
            size = random.randint(1, 3)
            shade = random.randint(180, 220)
            draw.ellipse([x, sy, x + size, sy + size], fill=(shade, shade, shade))

        # Save image to bytes
        import io
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Insert image as a full page in the PDF (no text layer)
        # Letter size in points: 612 x 792
        page = doc.new_page(width=612, height=792)
        page.insert_image(
            pymupdf.Rect(0, 0, 612, 792),
            stream=img_bytes.read()
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Pages: {len(DEPOSITION_PAGES)}')

    # Verify no text layer
    doc = pymupdf.open(OUTPUT)
    text = doc[2].get_text('text').strip()
    doc.close()
    print(f'Text layer check (page 3): "{text[:50]}..." (should be empty)')
    if text == '':
        print('PASS: No text layer detected - image-only PDF confirmed')
    else:
        print(f'WARNING: Text layer detected with {len(text)} chars')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
