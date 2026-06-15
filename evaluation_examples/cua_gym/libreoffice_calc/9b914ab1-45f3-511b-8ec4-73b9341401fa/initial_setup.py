"""
Initial Setup: novel_draft.odt - 8-chapter novel draft with plain text (no headings, no TOC, no bookmarks)
Task ID: osworld_multi_apps_book_splitting_nav_007
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, Span

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_splitting_nav_007'
OUTPUT = f'{WORKDIR}/novel_draft.odt'


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
    doc = OpenDocumentText()

    # Define a plain body text style (no heading style)
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(ParagraphProperties(margintop="0.2cm", marginbottom="0.2cm"))
    body_style.addElement(TextProperties(fontsize="12pt", fontfamily="Liberation Serif"))
    doc.automaticstyles.addElement(body_style)

    def add_paragraph(text, style_name="BodyText"):
        p = P(stylename=style_name)
        p.addText(text)
        doc.text.addElement(p)
        return p

    # Chapter data: titles and content paragraphs
    chapters = [
        {
            "title": "Chapter 1: The Forgotten Shore",
            "paragraphs": [
                "The tide had receded further than anyone could remember, leaving behind a vast expanse of grey sand dotted with stranded jellyfish and rusted anchors. Elena Marsh stood at the edge of the waterline, her boots sinking slightly into the wet sand, staring out at the horizon where the sea had retreated.",
                "She had arrived in the coastal village of Halverton three days ago, ostensibly to write her dissertation on tidal patterns, but the real reason was buried somewhere deeper — a memory she couldn't shake, a photograph she'd found tucked inside her mother's journal.",
                "The photograph showed two children standing on this very shore. One of them was undeniably her mother at perhaps eight years old. The other child — a boy with dark eyes and an unsettling smile — was someone Elena had never seen before.",
                "Behind the children, barely visible through the sea mist, stood a structure that no longer existed: a lighthouse. The old fishermen at the harbor pub spoke about it in hushed tones, as if the mere mention might summon something unwelcome.",
                "Elena pulled her coat tighter against the wind and turned back toward the village. She needed to find the local archives. She needed to understand what had happened to the lighthouse, and more importantly, what had happened to the boy in the photograph.",
                "The village of Halverton had a way of keeping secrets, she was beginning to realize. The locals were friendly enough on the surface, but there was a reticence beneath their warmth, a practiced evasiveness she had encountered everywhere she turned.",
                "Even old Thomas Greer, the harbormaster who had taken a shine to her, changed the subject whenever the lighthouse came up. He would busy himself with rope or nets, his weathered hands moving with sudden purpose, his eyes fixed on anything but her face.",
                "She made a mental note to visit the library first thing in the morning. Whatever the photograph revealed, whatever mystery it pointed to, she was determined to unravel it before the week was out.",
            ]
        },
        {
            "title": "Chapter 2: The Archive Room",
            "paragraphs": [
                "The Halverton public library occupied a converted Victorian customs house at the edge of the market square. Its stone walls were thick with ivy, and the heavy oak door creaked on its hinges when Elena pushed it open the following morning.",
                "The librarian, a lean woman in her sixties named Margaret Thorpe, looked up from behind a stack of cataloging cards and peered at Elena over her reading glasses. Her expression was neither welcoming nor hostile — merely assessing.",
                "Elena explained that she was a researcher studying the history of the coastline and asked to see any records related to the old lighthouse structure. Margaret's expression didn't change, but her hands went still for just a moment before she rose from her chair.",
                "The archive room was at the back of the building, down a narrow hallway lined with framed maps. Margaret unlocked the door with a key she kept on a chain around her neck and stepped aside to let Elena enter.",
                "The room smelled of old paper and something faintly metallic. Filing cabinets lined two walls, and a long oak table ran down the center. Margaret gestured toward the cabinets on the left.",
                "'Maritime records from 1880 to 1970 are in those four cabinets,' she said. 'Anything more recent is on the computer terminal in the main hall. You'll need to sign the access register.' She set a worn leather-bound book on the table.",
                "Elena signed her name and affiliation, noting that hers was the first entry in over two months. The last visitor had been someone named D. Carver, who had listed their purpose simply as 'family research.'",
                "She spent the next four hours working through the files. The lighthouse had been built in 1887, decommissioned in 1952, and demolished in 1961. But it was the gap between 1943 and 1952 that drew her attention. Those nine years were nearly absent from the records — just a handful of sparse maintenance logs and one cryptic inspection report.",
                "The inspection report, dated September 1951, referenced an 'incident of significant concern' and recommended that the structure be closed to all non-essential personnel pending further investigation. The report was signed by a Superintendent H. Arlen, but the accompanying documentation had been removed.",
            ]
        },
        {
            "title": "Chapter 3: The Name in the Ledger",
            "paragraphs": [
                "Elena returned to the library the next morning with a thermos of coffee and the photograph tucked inside her notebook. She had spent the previous evening comparing the faces in the picture to the names in the maritime logs, looking for anything that might connect the dots.",
                "She found it in an old crew ledger from 1943. Among the names of lighthouse keepers and assistants, one entry stood out: Samuel Carver, age 10, listed as 'keeper's ward.' The handwriting was cramped and hurried, as if added as an afterthought.",
                "Samuel Carver. The same surname as D. Carver, the researcher who had visited the archive two months earlier. Elena's pulse quickened. She photographed the entry with her phone and sat back in her chair, thinking.",
                "Her mother's name — before she married Elena's father — had been Ruth Halverton. She had never spoken much about her childhood, deflecting questions with a smile and a change of subject. Elena had assumed she simply found the past painful. Now she wondered if there was something more specific she had been avoiding.",
                "The boy in the photograph might be Samuel Carver. If so, he would be in his eighties now, assuming he was still alive. D. Carver might be a descendant — a child or grandchild — looking for the same answers Elena was.",
                "She asked Margaret if there was any way to find out more about the Carver family. The librarian's response was careful, almost choreographed.",
                "'The Carvers left Halverton some time ago,' Margaret said. 'I believe there was a daughter — Diane. She works at the university in Merswick, I think. In the history department, if I recall correctly.'",
                "Elena wrote down the name. Merswick was forty minutes up the coast. She could be there and back in an afternoon. But first, she wanted to see what else the archive had to offer.",
            ]
        },
        {
            "title": "Chapter 4: The Lighthouse Keeper's Daughter",
            "paragraphs": [
                "Diane Carver was not what Elena had expected. She was perhaps forty-five, with close-cropped silver hair and a directness that was almost startling. She had agreed to meet Elena in her office at the university without hesitation — almost, Elena thought, as if she had been expecting the call.",
                "The office was small and cluttered with books and maps. A framed print of a coastal survey hung on one wall, and beside it, a photograph of a lighthouse. Not the Halverton lighthouse — this one was taller, painted in red and white stripes.",
                "'My grandfather was Samuel Carver,' Diane said, without preamble, before Elena had fully settled into her chair. 'He was a ward of the Halverton lighthouse keeper from 1941 to 1951. His parents were killed in a bombing raid, and the keeper, a man named George Marsh, took him in.'",
                "Elena looked up sharply. Marsh. Her own family name.",
                "'George Marsh,' she said carefully. 'Do you know if he had children?'",
                "Diane studied her for a moment. 'He had a daughter,' she said. 'Ruth. She would have been about Samuel's age.' She paused. 'You have the same surname. Is that a coincidence?'",
                "Elena placed the photograph on the desk between them. Diane stared at it for a long moment, then reached out and turned it over. On the back, in faded pencil, was written: Ruth and Sam, 1949.",
                "Neither woman spoke for a while. Outside, students moved between buildings in the weak autumn sunshine, their voices carrying faintly through the glass.",
                "'He never talked about that time,' Diane said finally. 'Not once, in all the years I knew him. He lived until he was eighty-three, and he never mentioned Halverton or the lighthouse or Ruth Marsh. Not to me, not to my father, not to anyone, as far as I know.'",
            ]
        },
        {
            "title": "Chapter 5: What the Keeper Knew",
            "paragraphs": [
                "The question of what had happened in the lighthouse between 1943 and 1952 drove Elena back to the archive with renewed urgency. She requested the maintenance logs again and went through them page by page, looking for anything she had missed.",
                "She found it on the third day of searching: a single folded sheet tucked inside the back cover of a logbook from 1948. It was a personal letter, written in a careful hand she now recognized as her grandfather's.",
                "The letter was addressed to no one in particular. It was dated March 14, 1950, and it began: 'I write this not knowing if it will ever be found, or if finding it will do any good. But I cannot carry it alone any longer.'",
                "George Marsh had discovered, in the winter of 1947, that the lighthouse was being used as a transfer point for something. He did not know exactly what — he had only seen shapes in the darkness, boats that came and went without lights, men who did not meet his eyes when they passed him on the path.",
                "He had reported his suspicions to the local constabulary and been told, politely but firmly, to keep to his duties and not concern himself with matters above his station. Two months later, he had received a visit from a man who introduced himself only as a government official and who made it clear, with quiet precision, that certain activities were protected and that George's continued health and the wellbeing of his family depended on his discretion.",
                "George had kept silent. He had done what the man asked. He had watched and said nothing and written nothing down — until this letter, this single act of private defiance, tucked inside a logbook that he perhaps hoped would outlast him.",
                "'I do not know what they carried,' the letter concluded. 'I do not know who they answered to. But I know that two men died in connection with it, and that their deaths were called accidents, and that I said nothing. That is what I have to live with. That is what I leave behind me.'",
                "Elena sat very still for a long time after she finished reading. Outside, the wind had picked up, and she could hear it moving around the corners of the old building, finding the gaps, seeking a way in.",
            ]
        },
        {
            "title": "Chapter 6: The Second Photograph",
            "paragraphs": [
                "Diane Carver drove down to Halverton the following weekend. She brought with her a small cardboard box that had been sitting in her attic since her grandfather's death, unopened because no one had known what to do with it.",
                "They spread the contents across Elena's kitchen table. There were letters, a few small objects — a pocket watch, a brass button, a glass marble — and, at the bottom, three photographs.",
                "The first showed a group of men in heavy coats standing on a dock. Elena didn't recognize anyone.",
                "The second showed Samuel Carver as a young man, perhaps twenty, standing outside a building that Elena couldn't identify. He was thinner than in the childhood photograph, and his expression was guarded, watchful.",
                "The third photograph stopped them both cold. It showed the interior of the lighthouse, and it had clearly been taken without the subjects' knowledge. In the foreground, barely in focus, were two men in dark clothing handling a large crate. In the background, watching from a doorway, was a young woman.",
                "Elena recognized her immediately. It was her mother, Ruth — perhaps nineteen or twenty years old, her face pale and very still.",
                "Diane turned the photograph over. Nothing was written on the back.",
                "'She knew,' Diane said.",
                "Elena nodded. She didn't trust herself to speak.",
                "'My grandfather knew too,' Diane said. 'They both knew, and neither of them ever said a word about it. They carried this for their entire lives.'",
                "Elena thought about her mother's deflections, her careful silences, the way she had always steered conversations away from her childhood with such practiced ease. She thought about what it must have been like to watch something happen and be powerless to stop it, and then to carry that watching with you for decades.",
            ]
        },
        {
            "title": "Chapter 7: The Last Keeper",
            "paragraphs": [
                "They found Thomas Greer on the harbor wall the next morning, mending nets with the methodical patience of a man who has been doing the same task for forty years. He looked up when they approached and set down his work with a sigh that seemed to come from somewhere deep and old.",
                "'I thought it would be one of you eventually,' he said. He did not seem surprised to see Diane.",
                "He had been twelve years old in 1951, the son of one of the fishermen who used the harbor. He had seen the boats coming in late at night, had seen the men unloading the crates. He had once crept close enough to hear voices — two men arguing in low, fierce tones about timing and risk and someone who 'wouldn't stay quiet much longer.'",
                "Three weeks later, one of the men he had seen was found drowned in the harbor. It was ruled an accident. Thomas had told his father what he had seen and heard. His father had gone very pale and told him never to repeat it to anyone.",
                "'Your grandfather,' Thomas said, looking at Elena, 'was a good man in an impossible position. He tried to protect the children in his care. That was why he never pushed back harder than he did — because he was afraid of what they might do to Ruth. And to the Carver boy.'",
                "Elena asked him what had been in the crates. Thomas was quiet for a long moment, watching a gull circle overhead.",
                "'Weapons,' he said finally. 'Post-war surplus, mostly. Being sold off-books to buyers abroad. It went on for years, from what I could piece together later. There were people in the local government involved, people in London too. It was the kind of thing that got buried very thoroughly.'",
                "'Did anyone ever investigate?' Diane asked.",
                "'Someone tried,' Thomas said. 'In the mid-1970s, a journalist. He published one article and then the inquiry went quiet. The journalist moved away. The paper ran a retraction.' He picked up his nets again. 'That's how it works, sometimes. Things get buried. People move on. The sea keeps coming in.'",
            ]
        },
        {
            "title": "Chapter 8: The Tide Returns",
            "paragraphs": [
                "Elena spent her final days in Halverton writing. Not her dissertation — that felt remote now, almost irrelevant — but something else: a careful, documented account of everything she had found and everything she had been told.",
                "Diane was helping her. They worked from opposite ends of Elena's rented kitchen table, cross-referencing documents, verifying dates, tracking down secondary sources. It was slow work, but it had a clarity and purpose that made the hours pass without notice.",
                "They were not naive about what this meant. Whatever had happened in the lighthouse had been successfully suppressed for over sixty years. The people most directly involved were dead. The paper trail had been carefully thinned. What they had was fragmentary — compelling, but not yet sufficient.",
                "But it was a beginning. And it was a beginning that neither of their families had been able to make, bound as they were by fear and complicity and the particular kind of silence that settles over people who have seen something they cannot report.",
                "On her last evening in Halverton, Elena walked back down to the shore. The tide was coming in now, covering the grey sand in slow, dark waves. The horizon was clear, the sky a deep copper at the edges where the sun had set.",
                "She thought about her mother, young and frightened in a lighthouse doorway, watching something she had no power to stop. She thought about George Marsh, writing his letter in secret and hiding it in a logbook, hoping that someone, someday, would find it.",
                "She thought about the weight of things that go unsaid. How they accumulate. How they shape a person's life from the inside without ever being named.",
                "The waves came in and covered her footprints. She stood and watched until it was fully dark, and then she turned and walked back toward the lights of the village.",
                "She had work to do. The story was not finished. But for the first time in a long time, she felt that she was moving in the right direction — not away from something, but toward it.",
            ]
        },
    ]

    # Add each chapter to the document with plain text (NO heading styles)
    for ch in chapters:
        # Chapter title as plain text (NOT a heading style)
        add_paragraph(ch["title"])

        # Chapter body paragraphs
        for para_text in ch["paragraphs"]:
            add_paragraph(para_text)

        # Add blank paragraph between chapters for spacing
        add_paragraph("")

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
