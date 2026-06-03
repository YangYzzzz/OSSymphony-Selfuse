"""
Initial Setup: Redact emails and encrypt legal deposition PDF
Task ID: pdf_pw_006
Domain: pdf
"""

import os
import re
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_006'
OUTPUT_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{OUTPUT_DIR}/depositions_batch.pdf'


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


# Email addresses to scatter throughout the document
EMAILS = [
    "john.doe@example.com",
    "witness3@lawfirm.org",
    "sarah.martinez@globalcorp.net",
    "m.thompson@legalaid.org",
    "r.chen@deposervices.com",
    "karen.white@courtreporter.org",
    "jbrown@litigationteam.com",
    "a.patel@fordhamlaw.edu",
    "l.garcia@stateattorney.gov",
    "witness7@lawfirm.org",
    "d.kim@forensicaccounting.com",
    "p.nguyen@insuranceclaims.net",
    "c.robinson@deposervices.com",
    "h.jackson@legalaid.org",
    "f.williams@globalcorp.net",
    "t.moore@courtreporter.org",
    "e.taylor@litigationteam.com",
    "b.anderson@stateattorney.gov",
    "witness12@lawfirm.org",
    "n.wright@forensicaccounting.com",
]

# Deposition content organized by page themes
DEPOSITION_SECTIONS = [
    # Section 1: Case header and intro (pages 1-3)
    {
        "title": "IN THE SUPERIOR COURT OF THE STATE OF CALIFORNIA\nCOUNTY OF LOS ANGELES",
        "pages": [
            (
                "Case No. 2025-CV-04781\n\n"
                "GREENFIELD PROPERTIES, LLC,\n    Plaintiff,\n\nvs.\n\n"
                "PACIFIC RIM DEVELOPMENT GROUP, INC.,\n    Defendant.\n\n"
                "DEPOSITION OF MARCUS ANDREW THOMPSON\n"
                "Volume I\n\n"
                "Taken on behalf of Plaintiff\n"
                "Wednesday, January 15, 2025\n\n"
                "Reported by: Karen White, CSR No. 12847\n"
                f"Email: {EMAILS[5]}\n\n"
                "APPEARANCES:\n\n"
                "For Plaintiff GREENFIELD PROPERTIES, LLC:\n"
                "    MARTINEZ & CHEN, LLP\n"
                "    By: Sarah L. Martinez, Esq.\n"
                f"    Email: {EMAILS[2]}\n"
                "    555 South Grand Avenue, Suite 2800\n"
                "    Los Angeles, California 90071\n"
            ),
            (
                "For Defendant PACIFIC RIM DEVELOPMENT GROUP, INC.:\n"
                "    THOMPSON BROWN ASSOCIATES\n"
                "    By: James R. Brown, Esq.\n"
                f"    Email: {EMAILS[6]}\n"
                "    1200 Wilshire Boulevard, Suite 1500\n"
                "    Los Angeles, California 90017\n\n"
                "Also Present:\n"
                "    Dr. Raymond Chen, Expert Witness\n"
                f"    Email: {EMAILS[4]}\n"
                "    Forensic Accounting Division\n\n"
                "    Amita Patel, Paralegal\n"
                f"    Email: {EMAILS[7]}\n\n"
                "THE VIDEOGRAPHER: We are now on the record. Today's date is\n"
                "January 15, 2025. The time is approximately 9:02 a.m. We are\n"
                "at the offices of Martinez & Chen, LLP, located at 555 South\n"
                "Grand Avenue, Suite 2800, Los Angeles, California.\n"
            ),
            (
                "EXAMINATION BY MS. MARTINEZ:\n\n"
                "Q.  Good morning, Mr. Thompson. Could you please state your\n"
                "    full name for the record?\n"
                "A.  Marcus Andrew Thompson.\n\n"
                "Q.  And what is your current position?\n"
                "A.  I am the Chief Financial Officer of Pacific Rim\n"
                "    Development Group, Incorporated.\n\n"
                "Q.  How long have you held that position?\n"
                "A.  Since March of 2019. About six years now.\n\n"
                "Q.  Prior to joining Pacific Rim, where were you employed?\n"
                "A.  I was a Senior Vice President at Meridian Capital Partners\n"
                "    from 2014 to 2019.\n\n"
                "Q.  Mr. Thompson, I'm going to show you what has been marked\n"
                "    as Plaintiff's Exhibit 1. Do you recognize this document?\n"
                "A.  Yes. This appears to be an internal email I sent on\n"
                f"    September 3, 2024, from my email {EMAILS[0]} to several\n"
                "    members of the development team.\n"
            ),
        ]
    },
    # Section 2: Financial testimony (pages 4-8)
    {
        "title": "CONTINUED EXAMINATION - FINANCIAL RECORDS",
        "pages": [
            (
                "Q.  Mr. Thompson, directing your attention to Exhibit 3, can\n"
                "    you identify the figures in the column marked 'Projected\n"
                "    Revenue'?\n"
                "A.  Yes. These are the quarterly revenue projections that were\n"
                "    prepared by our accounting department in June 2024.\n\n"
                "Q.  And what were those projections based on?\n"
                "A.  They were based on committed lease agreements and letters\n"
                "    of intent that we had received as of May 31, 2024.\n\n"
                "Q.  The total projected revenue for Q3 2024 was $4.7 million.\n"
                "    Is that correct?\n"
                "A.  That is what the document shows, yes.\n\n"
                "Q.  And the actual revenue for Q3 2024 was $2.1 million?\n"
                "A.  I believe that is approximately correct.\n\n"
                "Q.  So there was a shortfall of approximately $2.6 million?\n"
                "A.  The numbers speak for themselves.\n\n"
                "    MR. BROWN: Objection. Calls for a legal conclusion.\n"
                "    MS. MARTINEZ: I'm asking about the arithmetic.\n"
                "    THE WITNESS: Yes, the difference would be approximately\n"
                "    $2.6 million.\n"
            ),
            (
                "Q.  Did you communicate this shortfall to the board of\n"
                "    directors?\n"
                "A.  I sent a memorandum to the board on October 8, 2024.\n\n"
                "Q.  Was that communication sent via email?\n"
                f"A.  Yes, I sent it from {EMAILS[0]} to the full board\n"
                "    distribution list.\n\n"
                "Q.  And did you receive any responses?\n"
                "A.  Several board members responded. I recall receiving\n"
                f"    emails from {EMAILS[10]} regarding the\n"
                "    forensic audit implications and from\n"
                f"    {EMAILS[11]} about the insurance coverage\n"
                "    questions.\n\n"
                "Q.  Let me direct your attention to Exhibit 5. Is this the\n"
                "    email chain you are referring to?\n"
                "A.  Yes, this appears to be a portion of that thread.\n\n"
                "    (Whereupon, a brief recess was taken from\n"
                "    10:45 a.m. to 11:00 a.m.)\n"
            ),
            (
                "Q.  Mr. Thompson, before the break we were discussing the\n"
                "    revenue shortfall. I'd like to now turn to the\n"
                "    construction cost overruns. Are you familiar with the\n"
                "    construction budget for the Oceanview Towers project?\n"
                "A.  Yes, I oversaw the financial aspects of that project.\n\n"
                "Q.  What was the original approved construction budget?\n"
                "A.  The board approved a budget of $38.5 million in\n"
                "    February 2023.\n\n"
                "Q.  And what was the final construction cost?\n"
                "A.  The project came in at approximately $47.2 million.\n\n"
                "Q.  That represents a cost overrun of approximately\n"
                "    $8.7 million, or about 22.6 percent. Is that accurate?\n"
                "A.  Your arithmetic appears correct.\n\n"
                "Q.  Were there change orders that contributed to these\n"
                "    overruns?\n"
                "A.  Yes, there were seventeen change orders over the course\n"
                "    of the project.\n"
            ),
            (
                "Q.  Who authorized these change orders?\n"
                "A.  Change orders under $250,000 could be approved by the\n"
                "    project manager. Those exceeding that threshold required\n"
                "    approval from the development committee.\n\n"
                "Q.  How many of the seventeen change orders exceeded\n"
                "    $250,000?\n"
                "A.  I believe seven of them did.\n\n"
                "Q.  And were all seven approved by the development\n"
                "    committee?\n"
                "A.  To my knowledge, yes. The approvals should be documented\n"
                "    in the committee minutes. Ms. Garcia from the State\n"
                f"    Attorney's office, reachable at {EMAILS[8]},\n"
                "    has requested copies of those minutes as well.\n\n"
                "Q.  Let's look at Change Order No. 12, which is Exhibit 7.\n"
                "    This change order was for $1.2 million for foundation\n"
                "    remediation. Can you explain what happened?\n"
                "A.  During excavation, the geotechnical engineers discovered\n"
                "    soil conditions that differed from the original survey.\n"
                "    Additional foundation work was required.\n"
            ),
            (
                "Q.  Was a new geotechnical survey conducted?\n"
                "A.  Yes. The original survey had been performed by GeoTech\n"
                "    Associates in 2022. A supplemental survey was performed\n"
                "    by Consolidated Soils Engineering in August 2023.\n\n"
                "Q.  And who bore the cost of the supplemental survey?\n"
                "A.  Pacific Rim absorbed that cost. It was approximately\n"
                "    $85,000.\n\n"
                "Q.  Did Pacific Rim pursue any claims against GeoTech\n"
                "    Associates for the original survey?\n"
                "A.  I am aware that our legal team evaluated potential claims.\n"
                "    I was not directly involved in those discussions.\n\n"
                "    MR. BROWN: And to the extent those discussions involved\n"
                "    attorney-client communications, I would instruct the\n"
                "    witness not to answer.\n"
                "    MS. MARTINEZ: Understood. I'm not asking about the\n"
                "    substance of legal advice.\n\n"
                "Q.  Were there other significant change orders you recall?\n"
                "A.  Change Order No. 15 for the upgraded HVAC system was\n"
                "    approximately $890,000. That one I remember clearly.\n"
            ),
        ]
    },
    # Section 3: Witness testimony (pages 9-14)
    {
        "title": "CONTINUED EXAMINATION - WITNESS COMMUNICATIONS",
        "pages": [
            (
                "Q.  Mr. Thompson, I'd like to discuss the communications\n"
                "    between Pacific Rim and its investors in 2024. Were\n"
                "    quarterly investor reports prepared?\n"
                "A.  Yes, we prepared and distributed quarterly investor\n"
                "    reports as required under the partnership agreement.\n\n"
                "Q.  Who was responsible for preparing those reports?\n"
                "A.  My office prepared the financial sections. The\n"
                "    development updates were prepared by the project\n"
                "    management team.\n\n"
                "Q.  Were these reports reviewed before distribution?\n"
                "A.  Yes, they were reviewed by our legal counsel and the\n"
                "    compliance department.\n\n"
                "Q.  I'm showing you Exhibit 9, which is the Q2 2024\n"
                "    investor report. On page 4, it states that the\n"
                "    Oceanview Towers project was 'on budget and on\n"
                "    schedule.' Was that accurate as of June 30, 2024?\n"
                "A.  At that point, we had not yet received the updated\n"
                "    cost projections from the general contractor.\n"
            ),
            (
                "Q.  When did you receive those updated projections?\n"
                "A.  I believe we received the revised cost estimate on\n"
                "    July 22, 2024.\n\n"
                "Q.  So approximately three weeks after the Q2 report was\n"
                "    issued?\n"
                "A.  That sounds about right.\n\n"
                "Q.  Did you issue a correction or supplement to the Q2\n"
                "    report?\n"
                "A.  No, we addressed the updated figures in the Q3 report.\n\n"
                "Q.  In the interim, were any investors informed of the\n"
                "    budget revisions?\n"
                "A.  I know that our investor relations team had\n"
                "    conversations with several of the larger institutional\n"
                "    investors.\n\n"
                "Q.  Do you know which investors were contacted?\n"
                "A.  I don't have a complete list. I know that Meridian\n"
                "    Capital and Westfield Partners were among them.\n"
                f"    Our contact at Westfield, witness number 3 at {EMAILS[1]},\n"
                "    can confirm the timeline of those discussions.\n"
            ),
            (
                "Q.  Were these conversations documented?\n"
                "A.  I would expect there to be call logs and follow-up\n"
                "    emails, but I was not a party to all of those\n"
                "    communications.\n\n"
                "Q.  Let's look at Exhibit 10. This is an email dated\n"
                "    August 5, 2024, from you to the investor relations\n"
                "    team. The subject line is 'Talking Points for Investor\n"
                "    Calls.' Did you write this email?\n"
                "A.  Yes.\n\n"
                "Q.  In this email, you wrote, and I quote, 'It is critical\n"
                "    that we frame the cost adjustments as a strategic\n"
                "    investment in quality rather than an overrun.' Did you\n"
                "    write that?\n"
                "A.  I did.\n\n"
                "Q.  What did you mean by 'frame'?\n"
                "A.  I meant that we should provide context for the\n"
                "    additional costs. The foundation remediation and HVAC\n"
                "    upgrades genuinely improved the quality and value of\n"
                "    the property.\n\n"
                "    MR. BROWN: Objection. The document speaks for itself.\n"
                "    THE WITNESS: I was simply trying to ensure our\n"
                "    communications were accurate and complete.\n"
            ),
            (
                "Q.  Mr. Thompson, let's turn to the tenant leasing process.\n"
                "    When did leasing efforts begin for Oceanview Towers?\n"
                "A.  We engaged a leasing broker, Coastal Commercial Real\n"
                "    Estate, in January 2024.\n\n"
                "Q.  And who at Coastal was your primary contact?\n"
                "A.  Christine Robinson was our account manager.\n\n"
                "Q.  How frequently did you communicate with Ms. Robinson?\n"
                "A.  Initially, we had weekly calls. As leasing activity\n"
                "    picked up, it became more frequent. Ms. Robinson\n"
                f"    communicated primarily via email at {EMAILS[12]}.\n\n"
                "Q.  How many leases were executed as of September 30, 2024?\n"
                "A.  I believe we had executed four commercial leases\n"
                "    representing approximately 40,000 square feet.\n\n"
                "Q.  And the building has approximately 180,000 square feet\n"
                "    of leasable space?\n"
                "A.  That is correct.\n\n"
                "Q.  So as of September 30, the building was approximately\n"
                "    22 percent leased?\n"
                "A.  Approximately, yes.\n"
            ),
            (
                "Q.  What was the projected leasing rate at that point in\n"
                "    the original pro forma?\n"
                "A.  The original projection anticipated approximately\n"
                "    65 percent occupancy by September 2024.\n\n"
                "Q.  So the actual leasing was significantly behind\n"
                "    projections?\n"
                "A.  The market conditions had changed significantly from\n"
                "    when those projections were made. Interest rates had\n"
                "    risen, and several potential tenants had delayed their\n"
                "    expansion plans.\n\n"
                "Q.  Did you communicate this leasing shortfall to the\n"
                "    investors?\n"
                "A.  It was reflected in the Q3 2024 investor report.\n\n"
                "Q.  But not before then?\n"
                "A.  The Q2 report included a general discussion of market\n"
                "    conditions.\n\n"
                "    MR. BROWN: I'll object to the characterization. The Q2\n"
                "    report speaks for itself.\n\n"
                "Q.  Fair enough. Let me ask it this way: Between July 1\n"
                "    and September 30, 2024, did you have any direct\n"
                "    communications with investors about the leasing pace?\n"
                "A.  I may have had some informal conversations, but I\n"
                "    don't recall the specifics.\n"
            ),
            (
                "Q.  Let's discuss your compensation and any financial\n"
                "    interest you have in the Oceanview Towers project.\n"
                "A.  I receive a base salary and a performance bonus tied\n"
                "    to company-wide metrics.\n\n"
                "Q.  Do you have any equity interest in Pacific Rim?\n"
                "A.  I hold a 3.5 percent equity stake.\n\n"
                "Q.  Is any portion of your compensation tied directly to\n"
                "    the Oceanview Towers project?\n"
                "A.  There is a project completion bonus that is contingent\n"
                "    on achieving certain milestones.\n\n"
                "Q.  What are those milestones?\n"
                "A.  Certificate of occupancy, achievement of 75 percent\n"
                "    occupancy, and debt service coverage ratio of 1.25\n"
                "    or better.\n\n"
                "Q.  What is the potential amount of that bonus?\n"
                "A.  Up to $500,000.\n\n"
                "Q.  Have any of those milestones been achieved?\n"
                "A.  We received the certificate of occupancy in\n"
                "    November 2024. The other two milestones have not\n"
                "    yet been achieved.\n"
            ),
        ]
    },
    # Section 4: Expert analysis (pages 15-20)
    {
        "title": "CONTINUED EXAMINATION - EXPERT ANALYSIS AND DOCUMENTS",
        "pages": [
            (
                "Q.  Mr. Thompson, I'd like to ask about the forensic\n"
                "    accounting analysis that was conducted. Are you aware\n"
                "    that Greenfield Properties retained a forensic\n"
                "    accountant?\n"
                "A.  I became aware of that, yes.\n\n"
                "Q.  Have you reviewed the forensic accounting report?\n"
                "    MR. BROWN: Objection. Work product.\n"
                "    MS. MARTINEZ: I'm not asking about work product. I'm\n"
                "    asking whether Mr. Thompson has seen a non-privileged\n"
                "    report that has been produced in discovery.\n"
                "    MR. BROWN: Subject to that limitation, you may answer.\n"
                "A.  I have reviewed portions of it, yes.\n\n"
                "Q.  The report was prepared by Dr. David Kim of Forensic\n"
                "    Analytics Group. Is that correct?\n"
                f"A.  I believe so. Dr. Kim's contact is {EMAILS[10]}.\n\n"
                "Q.  The report identifies several instances where project\n"
                "    costs were reclassified between budget categories.\n"
                "    Were you aware of those reclassifications?\n"
                "A.  Some of them, yes. Reclassifications are a normal\n"
                "    part of project accounting.\n"
            ),
            (
                "Q.  The report specifically identifies a transfer of\n"
                "    $1.4 million from the 'Contingency' line item to\n"
                "    'General Conditions' in August 2024. Do you recall\n"
                "    that transfer?\n"
                "A.  I would need to review the specific transaction. We\n"
                "    had numerous line-item adjustments throughout the\n"
                "    project.\n\n"
                "Q.  Would you agree that transferring funds from\n"
                "    contingency to general conditions could mask a budget\n"
                "    overrun?\n"
                "    MR. BROWN: Objection. Calls for speculation and a legal\n"
                "    conclusion.\n"
                "A.  I disagree with that characterization. Contingency\n"
                "    funds are specifically set aside to address\n"
                "    unanticipated costs.\n\n"
                "Q.  But the contingency line was fully depleted by\n"
                "    September 2024, correct?\n"
                "A.  I believe that is accurate.\n\n"
                "Q.  And at that point, additional costs had to be\n"
                "    funded from other sources?\n"
                "A.  The company authorized additional capital contributions\n"
                "    to cover the remaining costs.\n"
            ),
            (
                "Q.  How were those additional capital contributions funded?\n"
                "A.  Primarily through a supplemental capital call to the\n"
                "    existing investors.\n\n"
                "Q.  What was the amount of the supplemental capital call?\n"
                "A.  $5.8 million.\n\n"
                "Q.  Were all investors able to meet the capital call?\n"
                "A.  I understand that some of the smaller investors had\n"
                "    difficulty meeting the call. Our investor relations\n"
                f"    team, particularly Helen Jackson at {EMAILS[13]},\n"
                "    worked with each investor individually.\n\n"
                "Q.  Did any investors default on the capital call?\n"
                "A.  I believe two investors were unable to meet the full\n"
                "    amount within the specified timeframe.\n\n"
                "Q.  What were the consequences of those defaults under\n"
                "    the partnership agreement?\n"
                "    MR. BROWN: Objection. Calls for a legal interpretation.\n"
                "    MS. MARTINEZ: I'm asking about what actually happened,\n"
                "    not for a legal opinion.\n"
                "A.  The defaulting investors' interests were diluted in\n"
                "    accordance with the partnership agreement provisions.\n"
            ),
            (
                "Q.  Let's discuss the marketing materials that were used\n"
                "    to attract tenants. Who was responsible for preparing\n"
                "    those materials?\n"
                "A.  The marketing materials were prepared by our in-house\n"
                "    marketing team in coordination with Coastal Commercial\n"
                "    Real Estate.\n\n"
                "Q.  I'm showing you Exhibit 14. This is a marketing\n"
                "    brochure for Oceanview Towers. On page 2, it states\n"
                "    that the building offers 'Class A office space with\n"
                "    panoramic ocean views from all floors.' Is that\n"
                "    accurate?\n"
                "A.  The building is a Class A property. Most floors have\n"
                "    ocean views, although the lower floors have partial\n"
                "    views.\n\n"
                "Q.  So the statement 'panoramic ocean views from all\n"
                "    floors' is not entirely accurate?\n"
                "A.  It could be more precise, I suppose.\n\n"
                "Q.  Were you involved in approving these marketing\n"
                "    materials?\n"
                "A.  I reviewed the financial projections included in the\n"
                "    materials. I did not review the descriptive marketing\n"
                "    language.\n"
            ),
            (
                "Q.  Turning to the environmental compliance issues. Were\n"
                "    there any environmental concerns raised during\n"
                "    construction?\n"
                "A.  There was a minor issue with stormwater management\n"
                "    that was identified by the county inspector.\n\n"
                "Q.  When was that identified?\n"
                "A.  I believe it was in March 2024.\n\n"
                "Q.  Was a notice of violation issued?\n"
                "A.  Yes, a notice was issued and we corrected the\n"
                "    condition within 30 days.\n\n"
                "Q.  Were any fines assessed?\n"
                "A.  There was a nominal fine of $15,000.\n\n"
                "Q.  Was the fine disclosed to investors?\n"
                "A.  I believe it was mentioned in the Q1 2024 quarterly\n"
                "    report. Our environmental consultant, Frank Williams,\n"
                f"    can be contacted at {EMAILS[14]} to verify the\n"
                "    remediation timeline.\n\n"
                "Q.  Were there any other environmental issues?\n"
                "A.  Not to my knowledge.\n"
            ),
            (
                "    MS. MARTINEZ: I'd like to mark this as Exhibit 15.\n\n"
                "    (Whereupon, Plaintiff's Exhibit 15 was\n"
                "    marked for identification.)\n\n"
                "Q.  Mr. Thompson, Exhibit 15 is an email chain between\n"
                "    you and several Pacific Rim executives dated\n"
                "    October 15, 2024. The subject is 'Investor\n"
                "    Communication Strategy.' Do you see that?\n"
                "A.  Yes.\n\n"
                "Q.  In this email, you wrote to the team including\n"
                f"    {EMAILS[15]} and {EMAILS[16]}, stating:\n"
                "    'We need to carefully manage the narrative around\n"
                "    the Q3 numbers.' What did you mean by that?\n"
                "A.  I meant that we needed to provide appropriate context\n"
                "    for the financial results. The numbers alone, without\n"
                "    context, could be misleading.\n\n"
                "Q.  Misleading in what way?\n"
                "A.  The Q3 numbers reflected one-time charges and timing\n"
                "    differences that would normalize in future quarters.\n"
                "    Presenting raw numbers without that context could\n"
                "    cause unnecessary alarm among investors.\n"
            ),
        ]
    },
    # Section 5: Additional testimony (pages 21-28)
    {
        "title": "CONTINUED EXAMINATION - ADDITIONAL TESTIMONY",
        "pages": [
            (
                "Q.  Let's return to the construction timeline. You\n"
                "    mentioned earlier that there were seventeen change\n"
                "    orders. I'd like to focus on Change Order No. 3.\n"
                "    This was for the upgraded lobby design. Correct?\n"
                "A.  I believe so, yes.\n\n"
                "Q.  The original lobby design was budgeted at $420,000?\n"
                "A.  That sounds correct.\n\n"
                "Q.  And the upgraded design came in at $780,000?\n"
                "A.  I would need to confirm the exact figure, but that\n"
                "    sounds approximately right.\n\n"
                "Q.  Who requested the lobby upgrade?\n"
                "A.  It was a collective decision by the development\n"
                "    committee. The leasing broker had advised that a\n"
                "    more impressive lobby would help attract premium\n"
                "    tenants.\n\n"
                "Q.  Was there a cost-benefit analysis performed?\n"
                "A.  The leasing broker provided an opinion that the\n"
                "    upgraded lobby could support rental rates approximately\n"
                "    $2 per square foot higher. Over the ten-year\n"
                "    projection, that would more than offset the\n"
                "    additional cost.\n"
            ),
            (
                "Q.  Did that analysis prove accurate?\n"
                "A.  It's too early to tell definitively. We are achieving\n"
                "    rental rates consistent with Class A properties in\n"
                "    the area.\n\n"
                "Q.  But occupancy is well below projections, as we\n"
                "    discussed earlier.\n"
                "    MR. BROWN: Objection. Asked and answered.\n"
                "    MS. MARTINEZ: I'll move on.\n\n"
                "Q.  Mr. Thompson, were you involved in selecting the\n"
                "    general contractor for the Oceanview Towers project?\n"
                "A.  I participated in the selection committee, yes.\n\n"
                "Q.  How many bids were received?\n"
                "A.  I believe we received five bids.\n\n"
                "Q.  And the contract was awarded to Pacifica Construction\n"
                "    Group?\n"
                "A.  That is correct.\n\n"
                "Q.  Was Pacifica's bid the lowest?\n"
                "A.  No, I believe they were the second-lowest bidder.\n\n"
                "Q.  Why was a higher bid selected?\n"
                "A.  Pacifica had more experience with similar coastal\n"
                "    developments and had better references.\n"
            ),
            (
                "Q.  Did any member of the selection committee have a\n"
                "    pre-existing relationship with Pacifica Construction?\n"
                "A.  I'm not aware of any conflicts that were not\n"
                "    disclosed.\n\n"
                "Q.  Were conflict-of-interest disclosures required?\n"
                "A.  Yes, all selection committee members were required to\n"
                "    complete a disclosure form.\n\n"
                "Q.  Did you complete a disclosure form?\n"
                "A.  Yes.\n\n"
                "Q.  And you disclosed no conflicts?\n"
                "A.  That is correct. I had no prior relationship with\n"
                "    Pacifica or any of its principals.\n\n"
                "Q.  Mr. Thompson, I have here records showing that you\n"
                "    attended a golf event hosted by Pacifica's CEO in\n"
                "    May 2022. Is that accurate?\n"
                "A.  I attended many industry events. I may have attended\n"
                "    that event, but it was a large industry gathering,\n"
                "    not a private meeting.\n\n"
                "    MR. BROWN: For the record, attending an industry\n"
                "    event does not constitute a conflict of interest.\n"
            ),
            (
                "    MS. MARTINEZ: Let's take a short break.\n\n"
                "    (Whereupon, a luncheon recess was taken from\n"
                "    12:15 p.m. to 1:30 p.m.)\n\n"
                "    MS. MARTINEZ: Back on the record.\n\n"
                "Q.  Mr. Thompson, I'd like to ask about the property\n"
                "    insurance for Oceanview Towers. Who was the insurance\n"
                "    broker?\n"
                "A.  We used Pacific West Insurance Brokers.\n\n"
                "Q.  And the carrier?\n"
                "A.  The primary carrier is National Fidelity Insurance\n"
                "    Company.\n\n"
                "Q.  What is the total insured value?\n"
                "A.  The building is insured for replacement cost, which\n"
                "    I believe is approximately $52 million.\n\n"
                "Q.  Does the policy include business interruption\n"
                "    coverage?\n"
                "A.  Yes, it does.\n\n"
                "Q.  For how long?\n"
                "A.  I believe the business interruption period is\n"
                "    18 months.\n"
            ),
            (
                "Q.  Has any insurance claim been filed in connection\n"
                "    with the matters we've been discussing today?\n"
                "    MR. BROWN: Objection. Vague as to 'matters.'\n"
                "    MS. MARTINEZ: I'll rephrase.\n\n"
                "Q.  Has Pacific Rim filed any insurance claims related\n"
                "    to the Oceanview Towers project?\n"
                "A.  Yes, there was a claim filed for water damage that\n"
                "    occurred during construction. I believe the contact\n"
                f"    for claims was {EMAILS[11]} at the\n"
                "    insurance adjusters' office.\n\n"
                "Q.  When did the water damage occur?\n"
                "A.  During a storm in November 2023, before the building\n"
                "    envelope was fully sealed.\n\n"
                "Q.  What was the amount of the claim?\n"
                "A.  The claim was for approximately $340,000.\n\n"
                "Q.  Was the claim paid?\n"
                "A.  Yes, the carrier paid the claim minus the $50,000\n"
                "    deductible.\n\n"
                "Q.  Were there any other insurance claims?\n"
                "A.  Not to my recollection.\n"
            ),
            (
                "Q.  Mr. Thompson, I'd like to discuss the relationship\n"
                "    between Pacific Rim and Greenfield Properties. When\n"
                "    did Greenfield first invest in Pacific Rim?\n"
                "A.  Greenfield was one of the original investors in the\n"
                "    Oceanview Towers fund, which was formed in\n"
                "    December 2022.\n\n"
                "Q.  What was Greenfield's initial investment?\n"
                "A.  $3.2 million, representing a 12 percent limited\n"
                "    partnership interest.\n\n"
                "Q.  And Greenfield participated in the supplemental\n"
                "    capital call?\n"
                "A.  Yes, Greenfield contributed its pro rata share.\n\n"
                "Q.  Which was approximately $696,000?\n"
                "A.  I believe that is approximately correct.\n\n"
                "Q.  At any point, did Greenfield express concerns about\n"
                "    the management of the project?\n"
                "A.  I recall some inquiries from Greenfield's\n"
                "    representatives, but I would characterize them as\n"
                "    routine investor inquiries.\n\n"
                "Q.  When did those inquiries become more than routine?\n"
                "A.  I'm not sure I agree with that characterization.\n"
            ),
            (
                "Q.  Let me show you Exhibit 18. This is a letter from\n"
                "    Greenfield's counsel to Pacific Rim dated\n"
                "    November 12, 2024. Have you seen this letter?\n"
                "A.  Yes.\n\n"
                "Q.  This letter requests a full accounting of all project\n"
                "    expenditures. Did Pacific Rim comply with this\n"
                "    request?\n"
                "A.  We provided the information that we were required to\n"
                "    provide under the partnership agreement.\n\n"
                "Q.  Did you provide a full accounting as requested?\n"
                "A.  We provided the quarterly financial statements,\n"
                "    capital account statements, and K-1 tax documents.\n\n"
                "Q.  But not a detailed line-item accounting of project\n"
                "    expenditures?\n"
                "A.  The partnership agreement does not require that level\n"
                "    of detail to be provided to limited partners.\n\n"
                "    MR. BROWN: And for the record, that issue is the\n"
                "    subject of a pending motion.\n"
                "    MS. MARTINEZ: Noted.\n\n"
                "Q.  Were there communications between Brenda Anderson at\n"
                f"    {EMAILS[17]} and your legal team regarding\n"
                "    the scope of required disclosures?\n"
                "A.  I believe there were some exchanges, yes.\n"
            ),
            (
                "Q.  Mr. Thompson, are you aware of any instances where\n"
                "    Pacific Rim provided inaccurate information to\n"
                "    investors?\n"
                "A.  No. To my knowledge, all information provided to\n"
                "    investors was accurate.\n\n"
                "Q.  Even the Q2 report stating the project was 'on budget\n"
                "    and on schedule'?\n"
                "    MR. BROWN: Objection. Asked and answered.\n"
                "A.  As I explained earlier, that statement was accurate\n"
                "    as of the date it was made, based on the information\n"
                "    available at that time.\n\n"
                "Q.  But within three weeks, you learned that statement\n"
                "    was no longer accurate.\n"
                "    MR. BROWN: Objection. Mischaracterizes the testimony.\n"
                "A.  We learned of revised cost projections. Whether that\n"
                "    means the earlier statement was inaccurate is a\n"
                "    matter of perspective and timing.\n\n"
                "Q.  Did Pacific Rim have a duty to update investors when\n"
                "    it learned of material changes?\n"
                "    MR. BROWN: Objection. Calls for a legal conclusion.\n"
                "    MS. MARTINEZ: I'll rephrase.\n"
            ),
        ]
    },
    # Section 6: Closing pages (pages 29-35)
    {
        "title": "CONTINUED EXAMINATION - CLOSING TESTIMONY",
        "pages": [
            (
                "Q.  Mr. Thompson, what steps has Pacific Rim taken to\n"
                "    address the leasing shortfall?\n"
                "A.  We have engaged additional leasing brokers. We have\n"
                "    offered tenant improvement allowances. We have also\n"
                "    adjusted asking rents on certain floors to be more\n"
                "    competitive.\n\n"
                "Q.  By how much have rents been adjusted?\n"
                "A.  On the lower floors, we reduced asking rents by\n"
                "    approximately 8 to 12 percent.\n\n"
                "Q.  Does that reduction affect the financial projections\n"
                "    that were provided to investors?\n"
                "A.  The updated projections were included in the Q3 2024\n"
                "    investor report.\n\n"
                f"Q.  Our witness at {EMAILS[18]} provided\n"
                "    testimony that investor communications were delayed.\n"
                "    Do you dispute that characterization?\n"
                "A.  I dispute the characterization of 'delayed.' We\n"
                "    communicated on the schedule provided in the\n"
                "    partnership agreement.\n"
            ),
            (
                "Q.  What is the current occupancy rate of Oceanview\n"
                "    Towers?\n"
                "A.  As of the end of December 2024, we are at\n"
                "    approximately 38 percent occupancy.\n\n"
                "Q.  And the breakeven occupancy rate for debt service\n"
                "    is approximately 55 percent. Is that correct?\n"
                "A.  I believe that is approximately correct.\n\n"
                "Q.  So the building is currently operating below the\n"
                "    breakeven point?\n"
                "A.  Yes, that is the current situation. However, we\n"
                "    have several leases in advanced negotiation.\n\n"
                "Q.  How much additional space is under negotiation?\n"
                "A.  Approximately 35,000 square feet across three\n"
                "    prospective tenants.\n\n"
                "Q.  If all three leases are executed, what would the\n"
                "    occupancy rate be?\n"
                "A.  Approximately 57 percent.\n\n"
                "Q.  Just above breakeven.\n"
                "A.  Yes, and we would expect continued leasing activity\n"
                "    throughout 2025.\n"
            ),
            (
                "Q.  Mr. Thompson, have there been any discussions about\n"
                "    selling the property?\n"
                "A.  There have been preliminary inquiries, but no formal\n"
                "    decision to market the property.\n\n"
                "Q.  Who made those inquiries?\n"
                "A.  I'm not at liberty to disclose the identities of\n"
                "    parties who have made confidential inquiries.\n\n"
                "Q.  Has the board discussed a potential sale?\n"
                "A.  The board regularly evaluates all strategic options.\n"
                "    I'm not going to characterize specific board\n"
                "    discussions. Our board secretary, Natalie Wright\n"
                f"    at {EMAILS[19]}, maintains those minutes.\n\n"
                "Q.  Were any formal offers received?\n"
                "A.  I'm not aware of any formal written offers.\n\n"
                "Q.  Have any verbal offers been communicated?\n"
                "    MR. BROWN: Objection. Relevance.\n"
                "    MS. MARTINEZ: It goes to damages.\n"
                "    MR. BROWN: You may answer.\n"
                "A.  I'm not aware of any specific verbal offers that\n"
                "    would constitute binding proposals.\n"
            ),
            (
                "Q.  Let's discuss the current financial situation.\n"
                "    What is the outstanding mortgage balance on\n"
                "    Oceanview Towers?\n"
                "A.  Approximately $28.5 million.\n\n"
                "Q.  And the lender?\n"
                "A.  First Pacific National Bank.\n\n"
                "Q.  Is the loan current?\n"
                "A.  Yes, all payments are current.\n\n"
                "Q.  Are there any covenant violations?\n"
                "A.  There was a technical violation of the debt service\n"
                "    coverage ratio covenant in Q3 2024, which was waived\n"
                "    by the lender.\n\n"
                "Q.  What were the terms of that waiver?\n"
                "A.  The lender agreed to waive the covenant through\n"
                "    June 30, 2025, subject to certain conditions.\n\n"
                "Q.  What conditions?\n"
                "A.  The primary condition was that the DSCR must reach\n"
                "    1.10 or better by June 30, 2025.\n\n"
                "Q.  Is Pacific Rim on track to meet that condition?\n"
                "A.  If the pending leases are executed, we should be\n"
                "    close to that threshold.\n"
            ),
            (
                "    MS. MARTINEZ: I have just a few more questions.\n\n"
                "Q.  Mr. Thompson, to your knowledge, has any director,\n"
                "    officer, or employee of Pacific Rim engaged in any\n"
                "    conduct that you believe to be fraudulent,\n"
                "    dishonest, or in violation of law?\n"
                "    MR. BROWN: Objection. Vague, overbroad, calls for\n"
                "    a legal conclusion.\n"
                "A.  No.\n\n"
                "Q.  Do you believe the financial information provided to\n"
                "    investors was materially accurate?\n"
                "    MR. BROWN: Same objections.\n"
                "A.  Yes, I do.\n\n"
                "Q.  Is there anything you would have done differently\n"
                "    with respect to investor communications?\n"
                "    MR. BROWN: Objection. Calls for speculation.\n"
                "A.  In hindsight, we could have provided more frequent\n"
                "    updates between quarterly reports. I believe our\n"
                "    communications were adequate, but there is always\n"
                "    room for improvement.\n\n"
                "    MS. MARTINEZ: I have no further questions at this\n"
                "    time. I reserve the right to recall this witness.\n"
            ),
            (
                "EXAMINATION BY MR. BROWN:\n\n"
                "Q.  Mr. Thompson, Ms. Martinez asked you about the\n"
                "    Q2 2024 investor report. Is it true that the\n"
                "    information in that report was accurate as of the\n"
                "    date it was prepared?\n"
                "A.  Yes.\n\n"
                "Q.  And the cost overruns that were subsequently\n"
                "    identified were not known at the time of the Q2\n"
                "    report?\n"
                "A.  That is correct.\n\n"
                "Q.  Is it standard industry practice to address updated\n"
                "    financial information in the next quarterly report?\n"
                "A.  Yes, that is standard practice in the industry.\n\n"
                "Q.  Were the construction cost overruns caused by any\n"
                "    wrongdoing by Pacific Rim?\n"
                "    MS. MARTINEZ: Objection. Leading.\n"
                "    MR. BROWN: It's my witness.\n"
                "A.  No. The cost overruns were caused by unforeseen\n"
                "    soil conditions, material price increases, and\n"
                "    design improvements.\n\n"
                "    MR. BROWN: No further questions.\n"
            ),
            (
                "    MS. MARTINEZ: Brief redirect.\n\n"
                "REDIRECT EXAMINATION BY MS. MARTINEZ:\n\n"
                "Q.  Mr. Thompson, you testified that the cost overruns\n"
                "    were caused by unforeseen soil conditions and other\n"
                "    factors. But seven of the seventeen change orders\n"
                "    exceeded $250,000 and were discretionary upgrades,\n"
                "    correct?\n"
                "    MR. BROWN: Objection. Mischaracterizes.\n"
                "A.  Some of the change orders involved upgrades, and\n"
                "    some were necessitated by site conditions. I would\n"
                "    need to review each individually to categorize\n"
                "    them.\n\n"
                "    MS. MARTINEZ: That's all I have. Thank you.\n\n"
                "    MR. BROWN: Nothing further.\n\n"
                "    THE VIDEOGRAPHER: We are now off the record. The\n"
                "    time is 3:47 p.m.\n\n"
                "    (Whereupon, the deposition was concluded at\n"
                "    3:47 p.m.)\n"
            ),
        ]
    },
]


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    page_num = 0
    for section in DEPOSITION_SECTIONS:
        for page_text in section["pages"]:
            page = doc.new_page(width=612, height=792)  # Letter size

            # Header
            header_y = 50
            page.insert_text(
                pymupdf.Point(72, header_y),
                "GREENFIELD PROPERTIES, LLC v. PACIFIC RIM DEVELOPMENT GROUP, INC.",
                fontsize=8,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )

            # Page number
            page.insert_text(
                pymupdf.Point(540, header_y),
                f"Page {page_num + 1}",
                fontsize=8,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )

            # Separator line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 55), pymupdf.Point(540, 55))
            shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
            shape.commit()

            # Body text
            rect = pymupdf.Rect(72, 65, 540, 750)
            page.insert_textbox(
                rect,
                page_text,
                fontsize=10,
                fontname="cour",  # Courier for deposition transcript look
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

            # Footer
            page.insert_text(
                pymupdf.Point(200, 775),
                "DEPOSITION OF MARCUS ANDREW THOMPSON - VOLUME I",
                fontsize=7,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

            page_num += 1

    # Set metadata
    doc.set_metadata({
        "title": "Deposition of Marcus Andrew Thompson - Volume I",
        "author": "Court Reporter Karen White, CSR No. 12847",
        "subject": "Greenfield Properties, LLC v. Pacific Rim Development Group, Inc.",
        "keywords": "deposition, legal, transcript, Oceanview Towers",
        "creator": "Legal Transcription Services",
        "producer": "PyMuPDF",
    })

    # Set table of contents
    toc = [
        [1, "Case Information and Appearances", 1],
        [1, "Examination by Ms. Martinez", 3],
        [2, "Financial Records", 4],
        [2, "Witness Communications", 9],
        [2, "Expert Analysis and Documents", 15],
        [2, "Additional Testimony", 21],
        [1, "Closing Testimony", 29],
        [1, "Examination by Mr. Brown", 34],
        [1, "Redirect Examination", 35],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_num}')

    # Verify emails are present
    doc = pymupdf.open(OUTPUT)
    all_text = ""
    for p in doc:
        all_text += p.get_text("text")
    doc.close()

    import re
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found_emails = re.findall(email_pattern, all_text)
    print(f'Emails found in document: {len(found_emails)}')
    for e in found_emails:
        print(f'  - {e}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
