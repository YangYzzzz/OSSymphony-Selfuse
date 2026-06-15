"""
Initial Setup: Create a 200-page court transcript PDF with no headers
Task ID: pdf_legal_080
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_080'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/transcript.pdf'

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


# Realistic court transcript content segments
WITNESS_NAMES = [
    "Rachel Anderson", "Detective Michael Torres", "Dr. Emily Sato",
    "Officer David Park", "Sarah Mitchell", "James Thornton",
    "Maria Gonzalez", "Robert Chen", "Linda Whitfield", "Kevin O'Brien",
    "Patricia Nguyen", "Thomas Blackwell", "Angela Foster",
    "Christopher Reed", "Diane Martinez",
]

ATTORNEYS = {
    "prosecution": "Ms. Katherine Wells, Assistant District Attorney",
    "defense": "Mr. Brian Hartley, Defense Counsel",
}

JUDGE = "The Honorable Judge Patricia Reeves"

# Pre-built transcript line templates for realism
EXAMINATION_LINES = [
    ("Q", "Could you please state your full name for the record?"),
    ("A", "My name is {witness}."),
    ("Q", "And what is your occupation?"),
    ("A", "I am a {occupation}."),
    ("Q", "How long have you been in that position?"),
    ("A", "Approximately {years} years."),
    ("Q", "Can you describe for the jury what you observed on the evening of March 14th, 2024?"),
    ("A", "Yes. I was at the intersection of Oak Street and Main Boulevard at approximately 8:45 PM when I noticed a dark-colored sedan parked near the northwest corner of the parking lot."),
    ("Q", "What drew your attention to that vehicle?"),
    ("A", "The headlights were on, and the engine appeared to be running, but no one was visible inside at first glance."),
    ("Q", "What happened next?"),
    ("A", "I continued walking along the sidewalk when I heard what sounded like raised voices coming from the direction of the convenience store."),
    ("Q", "Could you make out what was being said?"),
    ("A", "Not the exact words, but the tone was aggressive and confrontational."),
    ("Q", "And then what did you do?"),
    ("A", "I stopped and looked toward the store entrance. That's when I saw two individuals exit the front door quickly."),
    ("Q", "Can you describe these individuals?"),
    ("A", "One was a male, approximately six feet tall, wearing a dark hoodie and jeans. The other was shorter, maybe five-seven, wearing a gray jacket."),
    ("Q", "Did you see their faces?"),
    ("A", "I saw the taller individual's face briefly when he passed under the streetlight. The shorter one had a baseball cap pulled low."),
    ("Q", "What happened after they exited the store?"),
    ("A", "They moved quickly to the sedan I mentioned earlier. The taller one got in the driver's seat and the other went to the passenger side."),
    ("Q", "Did the vehicle leave at that point?"),
    ("A", "Yes, it pulled out of the lot rapidly, heading south on Main Boulevard. The tires screeched as it turned."),
    ("Q", "Did you call the police?"),
    ("A", "I did. I called 911 immediately from my cell phone."),
    ("Q", "Approximately what time was that call placed?"),
    ("A", "Around 8:52 PM, according to my phone records."),
    ("Q", "Did you provide a description of the vehicle to the dispatcher?"),
    ("A", "Yes, I described it as a dark blue or black four-door sedan, possibly a Honda or Toyota, mid-2010s model."),
    ("Q", "Did you notice a license plate number?"),
    ("A", "I caught a partial plate. It started with 7-K-B, but I couldn't read the remaining characters in the dim light."),
]

OBJECTION_EXCHANGES = [
    ("MR. HARTLEY", "Objection, Your Honor. Leading the witness."),
    ("THE COURT", "Sustained. Rephrase the question, Counsel."),
    ("MS. WELLS", "Of course, Your Honor."),
]

OBJECTION_EXCHANGES_2 = [
    ("MR. HARTLEY", "Objection. Calls for speculation."),
    ("THE COURT", "Overruled. The witness may answer based on their personal observation."),
]

SIDEBAR_EXCHANGE = [
    ("THE COURT", "Let's take a brief recess. We'll reconvene in fifteen minutes."),
    ("THE CLERK", "All rise."),
    ("", "(Recess taken at {time}; proceedings resumed at {time2}.)"),
    ("THE CLERK", "Court is back in session. Please be seated."),
    ("THE COURT", "Counsel, you may continue."),
]

OCCUPATIONS = [
    "registered nurse at Mercy General Hospital",
    "retail manager at GreenMart on Oak Street",
    "forensic analyst with the State Crime Lab",
    "patrol officer with the Metropolitan Police Department",
    "licensed clinical psychologist",
    "automotive mechanic at Precision Auto Works",
    "high school English teacher at Westfield Academy",
    "financial analyst at Baxter & Associates",
    "paramedic with County Emergency Services",
    "security guard at Ridgeview Shopping Center",
    "software engineer at TechCore Solutions",
    "administrative assistant at City Hall",
    "pharmacist at Walton's Pharmacy",
    "construction foreman for Apex Building Group",
    "freelance photographer",
]

CROSS_EXAM_LINES = [
    ("Q", "Now, you mentioned you were approximately how far from the store entrance?"),
    ("A", "I would estimate about forty to fifty feet."),
    ("Q", "And it was dark outside, correct?"),
    ("A", "It was evening, yes, but there were streetlights in the area."),
    ("Q", "Streetlights that cast shadows and create uneven lighting, would you agree?"),
    ("A", "There was adequate lighting where I was standing."),
    ("Q", "But you couldn't read the full license plate, could you?"),
    ("A", "No, I only got a partial."),
    ("Q", "So is it fair to say the lighting conditions were not ideal for identification purposes?"),
    ("A", "The lighting was sufficient for me to see what I described."),
    ("Q", "You testified you saw the taller individual's face 'briefly.' How long would you estimate that glimpse lasted?"),
    ("A", "Perhaps two to three seconds as he walked under the light."),
    ("Q", "Two to three seconds. And from forty to fifty feet away. In the dark."),
    ("A", "Under a streetlight, yes."),
    ("Q", "Have you ever met my client before that evening?"),
    ("A", "No, I had not."),
    ("Q", "And you were asked to identify someone from a photo lineup roughly three weeks after the incident, correct?"),
    ("A", "That is correct."),
    ("Q", "No further questions, Your Honor."),
]

RECESS_TIMES = [
    ("10:32 AM", "10:48 AM"), ("11:15 AM", "11:30 AM"),
    ("12:05 PM", "1:30 PM"), ("2:22 PM", "2:38 PM"),
    ("3:10 PM", "3:25 PM"), ("3:55 PM", "4:10 PM"),
]


def build_transcript_page_text(page_num):
    """Generate realistic transcript text for a given page number."""
    import random
    random.seed(page_num * 42 + 7)

    lines = []
    line_num = 1

    # Page reference in transcript format
    if page_num == 0:
        # Title page
        lines.append("")
        lines.append("IN THE SUPERIOR COURT OF THE STATE OF COLUMBIA")
        lines.append("FOR THE COUNTY OF WESTFIELD")
        lines.append("")
        lines.append("THE PEOPLE OF THE STATE OF COLUMBIA,")
        lines.append("          Plaintiff,")
        lines.append("")
        lines.append("     vs.                          Case No. 2024-CR-4567")
        lines.append("")
        lines.append("DEREK JAMES ANDERSON,")
        lines.append("          Defendant.")
        lines.append("")
        lines.append("_" * 52)
        lines.append("")
        lines.append("OFFICIAL TRANSCRIPT OF PROCEEDINGS")
        lines.append("JURY TRIAL - DAY {0}".format((page_num // 40) + 1))
        lines.append("")
        lines.append("BEFORE: {0}".format(JUDGE))
        lines.append("")
        lines.append("APPEARANCES:")
        lines.append("  For the People:   {0}".format(ATTORNEYS["prosecution"]))
        lines.append("  For the Defendant: {0}".format(ATTORNEYS["defense"]))
        lines.append("")
        lines.append("Court Reporter: Janet L. Morrison, CSR No. 12847")
        lines.append("Date: March 25, 2024")
        lines.append("Volume I of V")
        return "\n".join(lines)

    # Regular transcript pages
    witness_idx = (page_num - 1) // 14 % len(WITNESS_NAMES)
    witness = WITNESS_NAMES[witness_idx]
    occupation = OCCUPATIONS[witness_idx % len(OCCUPATIONS)]

    # Determine section of examination
    section_in_witness = (page_num - 1) % 14

    if section_in_witness == 0:
        # Start of new witness examination
        lines.append(f"{line_num:>4}    {JUDGE.upper()}: Call your next witness, Counsel.")
        line_num += 1
        lines.append(f"{line_num:>4}    MS. WELLS: The People call {witness}.")
        line_num += 1
        lines.append(f"{line_num:>4}    THE CLERK: Please raise your right hand. Do you")
        line_num += 1
        lines.append(f"{line_num:>4}  solemnly swear that the testimony you are about to")
        line_num += 1
        lines.append(f"{line_num:>4}  give in this matter shall be the truth, the whole")
        line_num += 1
        lines.append(f"{line_num:>4}  truth, and nothing but the truth, so help you God?")
        line_num += 1
        lines.append(f"{line_num:>4}    THE WITNESS: I do.")
        line_num += 1
        lines.append(f"{line_num:>4}    THE CLERK: Please be seated and state your full")
        line_num += 1
        lines.append(f"{line_num:>4}  name for the record.")
        line_num += 1
        lines.append(f"{line_num:>4}")
        line_num += 1
        lines.append(f"{line_num:>4}         DIRECT EXAMINATION BY MS. WELLS")
        line_num += 1
        lines.append(f"{line_num:>4}")
        line_num += 1

        for speaker, text in EXAMINATION_LINES[:6]:
            t = text.format(witness=witness, occupation=occupation, years=random.randint(3, 22))
            lines.append(f"{line_num:>4}    {speaker}  {t}")
            line_num += 1

    elif section_in_witness < 5:
        # Continuing direct examination
        start = 6 + (section_in_witness - 1) * 7
        end = min(start + 7, len(EXAMINATION_LINES))
        exam_slice = EXAMINATION_LINES[start:end]

        for speaker, text in exam_slice:
            t = text.format(witness=witness, occupation=occupation, years=random.randint(3, 22))
            wrapped = [t[i:i+60] for i in range(0, len(t), 60)]
            for j, chunk in enumerate(wrapped):
                if j == 0:
                    lines.append(f"{line_num:>4}    {speaker}  {chunk}")
                else:
                    lines.append(f"{line_num:>4}  {chunk}")
                line_num += 1

        # Add an objection on some pages
        if section_in_witness == 3:
            lines.append(f"{line_num:>4}")
            line_num += 1
            for speaker, text in OBJECTION_EXCHANGES:
                lines.append(f"{line_num:>4}    {speaker}: {text}")
                line_num += 1

    elif section_in_witness < 8:
        # More direct examination content
        lines.append(f"{line_num:>4}    Q  Now, turning your attention to the events that")
        line_num += 1
        lines.append(f"{line_num:>4}  followed, can you describe what you observed next?")
        line_num += 1

        filler_responses = [
            "I saw the defendant approach the counter where the clerk was standing.",
            "There was a brief verbal exchange that I could not fully hear from my position.",
            "The store alarm went off approximately thirty seconds later.",
            "I immediately moved to a safer location behind a parked vehicle.",
            "Other bystanders were also reacting to the commotion at that point.",
            "I maintained visual contact with the entrance of the establishment.",
            "Emergency vehicles arrived within approximately seven to eight minutes.",
            "Officers secured the perimeter and began taking statements from witnesses.",
            "I provided my initial statement to Officer Park at approximately 9:15 PM.",
            "I was asked to remain available for follow-up questioning the next day.",
            "During the incident I noticed the taller suspect was carrying a dark backpack.",
            "The shorter individual appeared to be giving directions to the taller one.",
            "I observed that the store clerk appeared visibly shaken after the suspects departed.",
            "Several other customers were inside the store at the time of the incident.",
        ]
        random.shuffle(filler_responses)

        for resp in filler_responses[:6]:
            lines.append(f"{line_num:>4}    A  {resp}")
            line_num += 1
            lines.append(f"{line_num:>4}    Q  And what happened after that?")
            line_num += 1

        if section_in_witness == 6:
            for speaker, text in OBJECTION_EXCHANGES_2:
                lines.append(f"{line_num:>4}    {speaker}: {text}")
                line_num += 1

    elif section_in_witness < 10:
        # Cross-examination
        if section_in_witness == 8:
            lines.append(f"{line_num:>4}    MS. WELLS: No further questions for this witness,")
            line_num += 1
            lines.append(f"{line_num:>4}  Your Honor.")
            line_num += 1
            lines.append(f"{line_num:>4}    THE COURT: Mr. Hartley, cross-examination?")
            line_num += 1
            lines.append(f"{line_num:>4}    MR. HARTLEY: Thank you, Your Honor.")
            line_num += 1
            lines.append(f"{line_num:>4}")
            line_num += 1
            lines.append(f"{line_num:>4}         CROSS-EXAMINATION BY MR. HARTLEY")
            line_num += 1
            lines.append(f"{line_num:>4}")
            line_num += 1

        start = 0 if section_in_witness == 8 else 9
        end = min(start + 9, len(CROSS_EXAM_LINES))
        for speaker, text in CROSS_EXAM_LINES[start:end]:
            wrapped = [text[i:i+58] for i in range(0, len(text), 58)]
            for j, chunk in enumerate(wrapped):
                if j == 0:
                    lines.append(f"{line_num:>4}    {speaker}  {chunk}")
                else:
                    lines.append(f"{line_num:>4}  {chunk}")
                line_num += 1

    elif section_in_witness == 10:
        # Recess
        recess_idx = (page_num // 14) % len(RECESS_TIMES)
        t1, t2 = RECESS_TIMES[recess_idx]
        for speaker, text in SIDEBAR_EXCHANGE:
            t = text.format(time=t1, time2=t2)
            if speaker:
                lines.append(f"{line_num:>4}    {speaker}: {t}")
            else:
                lines.append(f"{line_num:>4}    {t}")
            line_num += 1

    else:
        # Redirect or procedural
        lines.append(f"{line_num:>4}    THE COURT: Any redirect, Ms. Wells?")
        line_num += 1
        redirect_qs = [
            ("Q", "Just a few questions on redirect, {witness}. You mentioned the streetlight. How close was it to where the suspect walked?"),
            ("A", "The light was directly overhead, perhaps ten feet above. He walked right through the pool of light."),
            ("Q", "And your vision - do you wear corrective lenses?"),
            ("A", "I do wear glasses for reading, but my distance vision is 20/20."),
            ("Q", "On the night in question, were you wearing your glasses?"),
            ("A", "I was not wearing them, no. As I said, I don't need them for distance."),
            ("Q", "Thank you. Nothing further, Your Honor."),
        ]
        for speaker, text in redirect_qs:
            t = text.format(witness=witness)
            wrapped = [t[i:i+58] for i in range(0, len(t), 58)]
            for j, chunk in enumerate(wrapped):
                if j == 0:
                    lines.append(f"{line_num:>4}    {speaker}  {chunk}")
                else:
                    lines.append(f"{line_num:>4}  {chunk}")
                line_num += 1

        lines.append(f"{line_num:>4}    THE COURT: The witness is excused. Thank you,")
        line_num += 1
        lines.append(f"{line_num:>4}  {witness}.")
        line_num += 1

    return "\n".join(lines)


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    for page_num in range(200):
        page = doc.new_page(width=612, height=792)  # Letter size

        text_content = build_transcript_page_text(page_num)

        # Insert transcript text
        text_rect = pymupdf.Rect(72, 72, 540, 740)
        page.insert_textbox(
            text_rect,
            text_content,
            fontsize=10,
            fontname="cour",  # Courier - standard for transcripts
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(290, 770),
            str(page_num + 1),
            fontsize=9,
            fontname="cour",
            color=(0, 0, 0),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
