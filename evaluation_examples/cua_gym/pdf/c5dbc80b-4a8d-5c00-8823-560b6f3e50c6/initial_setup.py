"""
Initial Setup: Create a 12-page corporate bylaws PDF with no bookmarks
Task ID: pdf_legal_055
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_055'
DIR_PATH = f'{WORKDIR}/legal/corp'
OUTPUT = f'{DIR_PATH}/bylaws.pdf'

# Page dimensions (Letter size)
WIDTH, HEIGHT = 612, 792
MARGIN_LEFT = 72
MARGIN_RIGHT = 540
MARGIN_TOP = 72
MARGIN_BOTTOM = 720
LINE_HEIGHT = 16
HEADING_SIZE = 16
SUBHEADING_SIZE = 13
BODY_SIZE = 11


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


def add_text(page, y, text, fontname="helv", fontsize=11, color=(0, 0, 0)):
    """Insert text and return new y position."""
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), text,
                     fontsize=fontsize, fontname=fontname, color=color)
    return y + fontsize + 4


def add_paragraph(page, y, text, fontname="helv", fontsize=11, indent=0):
    """Insert a wrapped paragraph in a textbox and return new y position."""
    rect = pymupdf.Rect(MARGIN_LEFT + indent, y, MARGIN_RIGHT, MARGIN_BOTTOM)
    excess = page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                                  align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Estimate lines used
    text_width = MARGIN_RIGHT - MARGIN_LEFT - indent
    chars_per_line = max(1, int(text_width / (fontsize * 0.5)))
    lines = max(1, len(text) // chars_per_line + 1)
    return y + lines * (fontsize + 3) + 6


def create_initial():
    os.makedirs(DIR_PATH, exist_ok=True)
    doc = pymupdf.open()

    # ==================== PAGE 1: Article I - Name ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP

    # Title
    page.insert_text(pymupdf.Point(180, y), "CORPORATE BYLAWS",
                     fontsize=22, fontname="hebo", color=(0, 0, 0.4))
    y += 30
    page.insert_text(pymupdf.Point(160, y), "Westfield Holdings Corporation",
                     fontsize=14, fontname="tibo", color=(0, 0, 0.3))
    y += 20

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, y), pymupdf.Point(MARGIN_RIGHT, y))
    shape.finish(color=(0, 0, 0.3), width=1.5)
    shape.commit()
    y += 20

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Adopted: March 15, 2024",
                     fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))
    y += 14
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y), "Last Amended: January 8, 2025",
                     fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))
    y += 30

    y = add_text(page, y, "ARTICLE I - NAME", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The name of this corporation shall be Westfield Holdings Corporation "
        "(hereinafter referred to as the \"Corporation\"), a corporation organized and "
        "existing under the laws of the State of Delaware, United States of America. "
        "The Corporation may conduct its business under such trade names or assumed "
        "names as the Board of Directors may from time to time authorize."
    ))
    y += 8
    y = add_paragraph(page, y, (
        "The principal office of the Corporation shall be located at 4200 Westfield "
        "Boulevard, Suite 800, Wilmington, Delaware 19801. The Corporation may also "
        "maintain offices at such other places, both within and outside the State of "
        "Delaware, as the Board of Directors may from time to time determine or as the "
        "business of the Corporation may require."
    ))
    y += 8
    y = add_paragraph(page, y, (
        "The registered agent of the Corporation in the State of Delaware shall be "
        "National Registered Agents, Inc., or such other agent as may be designated "
        "by resolution of the Board of Directors from time to time. The Corporation "
        "shall maintain a registered office in the State of Delaware as required by law."
    ))
    y += 8
    y = add_paragraph(page, y, (
        "The fiscal year of the Corporation shall begin on January 1 and end on "
        "December 31 of each calendar year, unless otherwise fixed by resolution of "
        "the Board of Directors."
    ))

    # ==================== PAGE 2: Article II - Purpose ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE II - PURPOSE", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The purpose of the Corporation is to engage in any lawful act or activity "
        "for which corporations may be organized under the General Corporation Law of "
        "the State of Delaware, including but not limited to the following:"
    ))
    y += 4
    purposes = [
        "(a) To acquire, own, develop, manage, lease, sell, and otherwise deal in real property, personal property, and mixed property of every kind and description;",
        "(b) To engage in the business of investment management, financial advisory services, and wealth management for institutional and individual clients;",
        "(c) To provide consulting services in the areas of corporate strategy, mergers and acquisitions, restructuring, and capital markets;",
        "(d) To invest in, acquire, hold, and dispose of securities, equity interests, partnership interests, and other financial instruments;",
        "(e) To borrow money and issue evidences of indebtedness, and to secure the same by mortgage, pledge, or other lien on the Corporation's assets;",
        "(f) To enter into joint ventures, partnerships, and other collaborative arrangements with domestic and foreign entities;",
        "(g) To do and perform all acts and things necessary, suitable, or proper for the accomplishment of the purposes herein set forth.",
    ]
    for p in purposes:
        y = add_paragraph(page, y, p, indent=20)
        y += 2

    y += 8
    y = add_paragraph(page, y, (
        "The Corporation shall have perpetual existence unless dissolved in accordance "
        "with applicable law and the provisions of these Bylaws."
    ))

    # ==================== PAGE 3: Article III - Members ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE III - MEMBERS", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The Corporation shall have members as defined in this Article. Membership "
        "in the Corporation shall be governed by the provisions set forth below and "
        "any additional policies adopted by the Board of Directors."
    ))
    y += 8

    y = add_text(page, y, "Section 3.1 - Eligibility", fontname="tibo", fontsize=SUBHEADING_SIZE)
    y += 6
    y = add_paragraph(page, y, (
        "Any natural person who is at least eighteen (18) years of age and who meets "
        "the qualifications established by the Board of Directors shall be eligible "
        "for membership in the Corporation. Membership applications shall be submitted "
        "in writing to the Secretary of the Corporation and shall be reviewed by the "
        "Membership Committee within thirty (30) days of receipt."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The following categories of membership shall be recognized: (i) Regular Members, "
        "who shall have full voting rights and be entitled to all benefits of membership; "
        "(ii) Associate Members, who shall have limited voting rights as determined by the "
        "Board; and (iii) Honorary Members, who shall be nominated by the Board in "
        "recognition of distinguished service to the Corporation."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Each applicant for Regular Membership shall demonstrate a minimum of three (3) "
        "years of professional experience in a field related to the Corporation's "
        "purposes, or hold a professional certification recognized by the Board. "
        "The Membership Committee may waive these requirements upon a two-thirds (2/3) "
        "vote of its members."
    ))

    # ==================== PAGE 4: Section 3.2 - Voting ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "Section 3.2 - Voting", fontname="tibo", fontsize=SUBHEADING_SIZE)
    y += 6
    y = add_paragraph(page, y, (
        "Each Regular Member in good standing shall be entitled to one (1) vote on each "
        "matter submitted to a vote of the members. Associate Members shall be entitled "
        "to vote only on matters specifically designated by the Board of Directors. "
        "Honorary Members shall have no voting rights."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Voting may be conducted in person at any duly called meeting of the members, "
        "by written ballot submitted by mail or electronic transmission, or by proxy "
        "executed in writing by the member or by the member's duly authorized agent. "
        "No proxy shall be valid after eleven (11) months from the date of its execution, "
        "unless otherwise provided in the proxy."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "A quorum for the transaction of business at any meeting of the members shall "
        "consist of not less than twenty-five percent (25%) of the Regular Members "
        "entitled to vote, represented in person or by proxy. If a quorum is not present, "
        "the meeting may be adjourned to a date not less than ten (10) nor more than "
        "thirty (30) days thereafter."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Unless otherwise required by law or these Bylaws, the affirmative vote of a "
        "majority of the members present and voting at a meeting at which a quorum is "
        "present shall be the act of the members. The following actions shall require "
        "the affirmative vote of two-thirds (2/3) of the members present and voting: "
        "(a) amendment of the Articles of Incorporation; (b) dissolution of the "
        "Corporation; (c) merger or consolidation with another entity; and (d) sale "
        "of substantially all of the Corporation's assets."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Cumulative voting shall not be permitted for the election of Directors. "
        "Each member entitled to vote shall cast one vote per Director seat to be "
        "filled. The candidates receiving the highest number of votes, up to the "
        "number of seats to be filled, shall be elected."
    ))

    # ==================== PAGE 5: Article IV - Directors ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE IV - DIRECTORS", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The business and affairs of the Corporation shall be managed by or under the "
        "direction of the Board of Directors. The Board shall exercise all powers of "
        "the Corporation except as otherwise provided by law, the Articles of "
        "Incorporation, or these Bylaws."
    ))
    y += 8
    y = add_text(page, y, "Section 4.1 - Number", fontname="tibo", fontsize=SUBHEADING_SIZE)
    y += 6
    y = add_paragraph(page, y, (
        "The Board of Directors shall consist of not fewer than seven (7) nor more than "
        "fifteen (15) directors. The exact number of directors shall be fixed from time "
        "to time by resolution of the Board, provided that no decrease in the number of "
        "directors shall shorten the term of any incumbent director."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "At least two-thirds (2/3) of the directors shall be independent directors, "
        "as defined by applicable securities regulations and the Corporation's Corporate "
        "Governance Guidelines. An independent director is one who has no material "
        "relationship with the Corporation, directly or as a partner, shareholder, or "
        "officer of an organization that has a relationship with the Corporation."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Board shall include at least one director with expertise in financial "
        "accounting or auditing (the \"Financial Expert\"), and at least one director "
        "with experience in the Corporation's primary industry sector. The Nominating "
        "and Governance Committee shall consider diversity of background, experience, "
        "and perspective when recommending candidates for election to the Board."
    ))

    # ==================== PAGE 6: Section 4.2 - Election ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "Section 4.2 - Election", fontname="tibo", fontsize=SUBHEADING_SIZE)
    y += 6
    y = add_paragraph(page, y, (
        "Directors shall be elected at the annual meeting of members by a plurality of "
        "the votes cast. Each director shall serve for a term of three (3) years, with "
        "the Board divided into three classes of approximately equal size, so that the "
        "term of one class expires each year (a \"classified board\" or \"staggered board\")."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Nominations for election to the Board of Directors may be made by: (a) the "
        "Nominating and Governance Committee; (b) any Regular Member in good standing "
        "who has submitted a written nomination at least sixty (60) days prior to the "
        "annual meeting; or (c) the Board of Directors itself. All nominees must consent "
        "in writing to serve if elected."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Each nominee shall complete and submit a Director Qualification Questionnaire, "
        "disclosing any potential conflicts of interest, other board memberships, "
        "financial interests in competitors, and any pending legal proceedings. The "
        "Nominating and Governance Committee shall review all questionnaires and make "
        "its recommendation to the full Board."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "In the event of a vacancy on the Board arising from death, resignation, "
        "removal, or an increase in the number of directors, the remaining directors "
        "may fill the vacancy by a majority vote. A director elected to fill a vacancy "
        "shall serve for the remainder of the term of the class to which the director "
        "has been assigned."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "No individual who has attained the age of seventy-five (75) years shall be "
        "eligible for election or re-election to the Board. Directors who reach this "
        "age during their term shall complete the remainder of their term but shall "
        "not stand for re-election."
    ))

    # ==================== PAGE 7: Section 4.3 - Removal ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "Section 4.3 - Removal", fontname="tibo", fontsize=SUBHEADING_SIZE)
    y += 6
    y = add_paragraph(page, y, (
        "Any director may be removed from office, with or without cause, by the "
        "affirmative vote of two-thirds (2/3) of the members entitled to vote at a "
        "special meeting called for that purpose. Written notice of such meeting, "
        "stating the purpose thereof, shall be delivered to all members at least "
        "twenty (20) days prior to the date of the meeting."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Board of Directors may also declare vacant the office of a director who "
        "has been declared of unsound mind by a court order, who has been convicted of "
        "a felony, or who has failed to attend three (3) consecutive regular meetings "
        "of the Board without good cause. The affected director shall be given written "
        "notice and an opportunity to be heard before the Board takes such action."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "A director may resign at any time by delivering written notice to the "
        "Chairperson of the Board or to the Secretary of the Corporation. Such "
        "resignation shall take effect at the time specified in the notice, or if "
        "no time is specified, upon delivery of the notice. Acceptance of such "
        "resignation shall not be necessary to make it effective."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "In the event that removal proceedings are initiated against a director, the "
        "director under consideration for removal shall recuse themselves from any "
        "Board vote or discussion relating to the removal. The Corporation shall bear "
        "all costs associated with the removal proceedings, including reasonable "
        "attorney's fees for the Corporation's legal counsel."
    ))

    # ==================== PAGE 8: Article V - Officers ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE V - OFFICERS", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The officers of the Corporation shall be a Chairperson of the Board, a Chief "
        "Executive Officer, a President, one or more Vice Presidents, a Secretary, a "
        "Treasurer, and such other officers as the Board of Directors may from time to "
        "time appoint. Any two or more offices may be held by the same person, except "
        "that the offices of President and Secretary shall not be held simultaneously "
        "by the same individual."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Officers shall be elected by the Board of Directors at its first meeting "
        "following the annual meeting of members and shall serve at the pleasure of "
        "the Board. The compensation of all officers shall be fixed by the Board upon "
        "recommendation of the Compensation Committee."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Chairperson of the Board shall preside at all meetings of the Board and "
        "of the members, and shall perform such other duties as may be assigned by the "
        "Board. The Chief Executive Officer shall be the principal executive officer of "
        "the Corporation and shall have general supervision and control of the business "
        "and affairs of the Corporation, subject to the direction of the Board."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Secretary shall keep the minutes of all meetings of the Board and of the "
        "members, shall maintain the corporate records and the seal of the Corporation, "
        "and shall give all notices required by law or these Bylaws. The Treasurer shall "
        "have custody of all corporate funds and securities and shall keep accurate books "
        "and accounts of all receipts and disbursements."
    ))

    # ==================== PAGE 9: Article VI - Committees ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE VI - COMMITTEES", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The Board of Directors may establish one or more committees, each consisting "
        "of two or more directors, to serve at the pleasure of the Board. Standing "
        "committees of the Board shall include: the Executive Committee, the Audit "
        "Committee, the Compensation Committee, and the Nominating and Governance "
        "Committee."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Audit Committee shall consist of not fewer than three (3) independent "
        "directors, at least one of whom shall be the Financial Expert. The Audit "
        "Committee shall oversee the Corporation's financial reporting processes, "
        "internal controls, and compliance with applicable laws and regulations. "
        "It shall also be responsible for the appointment, compensation, and oversight "
        "of the Corporation's independent auditor."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Compensation Committee shall consist of not fewer than three (3) "
        "independent directors and shall be responsible for reviewing and approving "
        "the compensation of the Corporation's executive officers, administering "
        "equity-based compensation plans, and preparing the annual compensation "
        "report for inclusion in the Corporation's proxy statement."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Each committee shall keep regular minutes of its proceedings and shall "
        "report its actions to the Board at the next regular Board meeting. No "
        "committee shall have the authority to amend the Articles of Incorporation, "
        "adopt or amend these Bylaws, fill vacancies on the Board, or declare dividends."
    ))

    # ==================== PAGE 10: Article VII - Meetings ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE VII - MEETINGS", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The annual meeting of the members shall be held on the third Tuesday of "
        "April of each year at such time and place as may be designated by the Board "
        "of Directors. If the day fixed for the annual meeting falls on a legal holiday, "
        "the meeting shall be held on the next succeeding business day."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Special meetings of the members may be called by the Chairperson of the Board, "
        "the Chief Executive Officer, or by a majority of the Board of Directors. "
        "Special meetings may also be called upon the written request of not less than "
        "ten percent (10%) of the Regular Members entitled to vote."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Regular meetings of the Board of Directors shall be held at least quarterly, "
        "at such times and places as the Board may determine. Special meetings of the "
        "Board may be called by the Chairperson or by any three (3) directors upon at "
        "least forty-eight (48) hours' notice."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Members of the Board or any committee may participate in a meeting by means "
        "of conference telephone, video conference, or similar communications equipment "
        "by means of which all persons participating in the meeting can hear each other "
        "at the same time. Such participation shall constitute presence in person at "
        "the meeting."
    ))

    # ==================== PAGE 11: Article VIII - Indemnification ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE VIII - INDEMNIFICATION", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "The Corporation shall indemnify any person who was or is a party, or is "
        "threatened to be made a party, to any threatened, pending, or completed "
        "action, suit, or proceeding, whether civil, criminal, administrative, or "
        "investigative, by reason of the fact that such person is or was a director, "
        "officer, employee, or agent of the Corporation, to the fullest extent "
        "permitted by the General Corporation Law of the State of Delaware."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Corporation shall advance expenses incurred by a director or officer in "
        "defending any action, suit, or proceeding upon receipt of an undertaking by "
        "or on behalf of such person to repay such amount if it shall ultimately be "
        "determined that such person is not entitled to be indemnified by the Corporation."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The Corporation may purchase and maintain insurance on behalf of any person "
        "who is or was a director, officer, employee, or agent of the Corporation "
        "against any liability asserted against such person and incurred by such person "
        "in any such capacity. The Board shall review the Corporation's directors' and "
        "officers' liability insurance coverage on an annual basis."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "The indemnification and advancement of expenses provided by this Article "
        "shall not be deemed exclusive of any other rights to which a person may be "
        "entitled under any agreement, vote of members or directors, or otherwise, "
        "both as to action in an official capacity and as to action in another capacity "
        "while holding such office."
    ))

    # ==================== PAGE 12: Article IX - Amendments ====================
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    y = MARGIN_TOP
    y = add_text(page, y, "ARTICLE IX - AMENDMENTS AND GENERAL PROVISIONS", fontname="hebo", fontsize=HEADING_SIZE)
    y += 8
    y = add_paragraph(page, y, (
        "These Bylaws may be altered, amended, or repealed, and new Bylaws may be "
        "adopted, by the affirmative vote of two-thirds (2/3) of the members present "
        "and voting at any regular or special meeting of the members at which a quorum "
        "is present. The Board of Directors shall also have the power to alter, amend, "
        "or repeal these Bylaws or adopt new Bylaws by the affirmative vote of a "
        "majority of the entire Board, subject to the right of the members to change "
        "or repeal such action."
    ))
    y += 4
    y = add_paragraph(page, y, (
        "Proposed amendments to these Bylaws shall be submitted in writing to the "
        "Secretary at least thirty (30) days prior to the meeting at which they are "
        "to be considered. The Secretary shall include the proposed amendments in the "
        "notice of such meeting sent to all members."
    ))
    y += 8

    y = add_text(page, y, "Severability", fontname="tibo", fontsize=SUBHEADING_SIZE)
    y += 6
    y = add_paragraph(page, y, (
        "If any provision of these Bylaws is held to be invalid, illegal, or "
        "unenforceable, the remaining provisions shall continue in full force and "
        "effect. The invalid, illegal, or unenforceable provision shall be modified "
        "to the minimum extent necessary to make it valid, legal, and enforceable."
    ))
    y += 8

    y = add_text(page, y, "Governing Law", fontname="tibo", fontsize=SUBHEADING_SIZE)
    y += 6
    y = add_paragraph(page, y, (
        "These Bylaws and the rights and obligations of the Corporation, its directors, "
        "officers, and members shall be governed by and construed in accordance with "
        "the laws of the State of Delaware, without regard to conflict of law principles."
    ))
    y += 16

    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "CERTIFIED AS TRUE AND CORRECT:",
                     fontsize=11, fontname="hebo")
    y += 20
    # Signature line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, y), pymupdf.Point(300, y))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    y += 14
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "Victoria R. Pemberton, Corporate Secretary",
                     fontsize=10, fontname="tiit")
    y += 14
    page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                     "Date: January 8, 2025",
                     fontsize=10, fontname="tiit")

    # Verify NO bookmarks
    doc.set_toc([])

    # Add page numbers to all pages
    for i, pg in enumerate(doc):
        pg.insert_text(
            pymupdf.Point(WIDTH / 2 - 10, HEIGHT - 30),
            str(i + 1),
            fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5)
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 12')

    # Verify
    verify_doc = pymupdf.open(OUTPUT)
    print(f'Verified page count: {verify_doc.page_count}')
    print(f'Verified TOC entries: {len(verify_doc.get_toc())}')
    verify_doc.close()

    # GUI-ready startup: open the bylaws in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
