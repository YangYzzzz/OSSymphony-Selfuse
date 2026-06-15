"""
Initial Setup: anthology.odt multi-author document in Documents folder
Task ID: osworld_multi_apps_book_splitting_nav_012
Domain: libreoffice_writer (ODT)

Creates:
  - /home/user/Documents/anthology.odt: a multi-author anthology document
  - /home/user/Desktop/anthology_split/ directory

The anthology.odt contains works from 5 authors, each with 3-6 chapters.
Author sections are separated by bold author names.
No TOC, no bookmarks, no heading styles — those must be added by the agent.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import (
    Style, TextProperties, ParagraphProperties, ListLevelProperties
)
from odf.text import (
    P, H, Span, LineBreak, List, ListItem
)
from odf import style as odfstyle

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_splitting_nav_012'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
ANTHOLOGY_FILE = f'{DOCUMENTS_DIR}/anthology.odt'
SPLIT_DIR = f'{WORKDIR}/Desktop/anthology_split'


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


# --- Author/Chapter data ---
AUTHORS = [
    {
        "name": "Elena Rivera",
        "surname": "Rivera",
        "bio": "Elena Rivera is an acclaimed novelist known for her vivid portrayals of Latin American life.",
        "chapters": [
            {
                "title": "The Crimson Market",
                "sections": [
                    ("Morning Hours", [
                        "The market opened before dawn, when the sky above Mexico City still held its midnight indigo. Elena Vasquez arrived first, as she always did, hauling her cart laden with dried chiles and fresh herbs.",
                        "The vendors arranged themselves with practiced efficiency. Each stall claimed its customary territory, a silent agreement maintained across generations of commerce.",
                        "By the time the sun crested the eastern ridge, over three hundred vendors had established their positions, transforming the empty plaza into a vibrant labyrinth of color and scent.",
                    ]),
                    ("The Bargaining", [
                        "Prices were never fixed at the crimson market. Everything was negotiated through an elaborate dance of offers and counter-offers, anchored by long-standing relationships.",
                        "Señora Montoya, who sold the finest avocados in the city, refused to deal with strangers until they had visited her stall at least three times.",
                        "Her logic was sound: the best customers were those who understood patience.",
                    ]),
                    ("Evening Gathering", [
                        "As dusk fell, the vendors began the slow work of dismantling their stalls. But no one left immediately. The evening gathering was as important as the commerce itself.",
                        "Stories were shared, disputes mediated, marriages arranged. The crimson market was a living institution, its traditions stretching back centuries.",
                    ]),
                ],
            },
            {
                "title": "Daughters of the Drought",
                "sections": [
                    ("The Dry Season", [
                        "Three years without rain had transformed the valley into a testament of endurance. The women of Oaxahuala adapted, as women always do, finding water in unexpected places.",
                        "Lucia Reyes led the daily pilgrimage to the spring, a three-hour walk each way. The younger women complained; the older ones remembered worse.",
                    ]),
                    ("New Methods", [
                        "A young engineer named Sofía Díaz arrived in the village with blueprints for a cistern system. The village elders were skeptical; the women were not.",
                        "Within two weeks, they had organized work teams, collected building materials, and begun excavation. The cisterns were complete before the engineer expected.",
                    ]),
                ],
            },
            {
                "title": "The Night Letters",
                "sections": [
                    ("First Correspondence", [
                        "The letters began arriving in October, tucked under the door of the village post office before sunrise. No return address, but the handwriting was unmistakably feminine.",
                        "The postmistress, Carmela, held each one up to the light before distributing them. She never read them, but she catalogued their arrival in her private ledger.",
                    ]),
                    ("Revelations", [
                        "By December, nearly every family in San Cristóbal had received at least one letter. The contents varied widely — confessions, declarations, warnings, and in one case, a detailed map of the valley's hidden springs.",
                        "The village priest called a meeting to discuss the matter. Only the women attended.",
                    ]),
                    ("Resolution", [
                        "The final letter arrived on Christmas Eve. Unlike the others, it was addressed to the whole village, not to any individual family.",
                        "It contained a single paragraph: a reminder that the mountains held the memory of everything that had transpired in the valley, and that memory was the only true inheritance.",
                    ]),
                ],
            },
        ],
    },
    {
        "name": "Kenji Nakamura",
        "surname": "Nakamura",
        "bio": "Kenji Nakamura writes literary fiction exploring identity, memory, and the Japanese diaspora experience.",
        "chapters": [
            {
                "title": "The Paper Garden",
                "sections": [
                    ("Folds and Memory", [
                        "His grandmother had taught him origami before she taught him to read. The cranes came first — always the cranes — then the mountains, the boats, the impossible geometries of the orchid.",
                        "Takeshi Mori kept a box of his grandmother's completed pieces under his bed in Seattle, wrapped in silk purchased at the market in Kyoto where she had spent her working years.",
                    ]),
                    ("The Seattle Years", [
                        "America had its own paper, he discovered. Thick and uncooperative, it resisted the precise folds that Japanese paper accepted willingly. He learned to compensate with stronger pressure.",
                        "His coworkers at the architecture firm were fascinated by his lunch-hour practice. They brought him their business cards, which he transformed into tiny foxes and returned without explanation.",
                    ]),
                    ("Return", [
                        "Twenty years after leaving Nagoya, Takeshi returned for his grandmother's hundredth birthday. The house was smaller than he remembered, or perhaps he had simply grown.",
                        "His grandmother sat in her garden, folding. Her fingers moved with the same precision they always had, despite the arthritis that had bent them at unfamiliar angles.",
                    ]),
                ],
            },
            {
                "title": "Between Two Rivers",
                "sections": [
                    ("Departure", [
                        "The ship left Yokohama Harbor on a Tuesday morning in April 1923. Hiroshi Nakamura stood at the railing and watched Japan recede until it was indistinguishable from the horizon.",
                        "He carried one suitcase, containing three changes of clothes, his father's pocket watch, and a dictionary of English idioms that he had memorized but not yet understood.",
                    ]),
                    ("San Francisco", [
                        "The city bewildered him with its noise and its colors. Everything moved at a pace that seemed designed to exclude the careful, the deliberate, the thoughtful.",
                        "He found work in a laundry in the Western Addition, alongside men who had also crossed oceans and were learning, as he was, to navigate the peculiar grammar of American ambition.",
                    ]),
                    ("Roots", [
                        "By 1930, Hiroshi had saved enough to open his own business, a small restaurant serving food that bore only a passing resemblance to Japanese cuisine.",
                        "He had learned that Americans did not want authenticity. They wanted the idea of a thing. He provided the idea of Japan: clean, efficient, mysterious, contained.",
                    ]),
                ],
            },
            {
                "title": "Silence and Ceremony",
                "sections": [
                    ("The Tea Room", [
                        "Yuki built her tea room in the corner of the garage, converting the space over a period of three years. Her husband thought it was a hobby; her daughter understood it was something else.",
                        "The construction followed strict protocols: the proportions of the tatami mats, the placement of the alcove, the height of the ceiling. Every measurement carried historical weight.",
                    ]),
                    ("Students", [
                        "She began teaching in her third year, accepting students on the recommendation of existing students only. The waiting list grew to fourteen months.",
                        "Her curriculum was unusual. She spent the first six months teaching silence — not the absence of sound, but the presence of attention.",
                    ]),
                    ("The Last Lesson", [
                        "The afternoon light fell through the paper screens in the way that had always moved her, casting a diffuse gold that softened all edges.",
                        "Her oldest student, a woman named Patricia Clearwater, was preparing to teach her own first class. This was the final lesson: receiving is not enough; the tradition continues only through giving.",
                    ]),
                ],
            },
            {
                "title": "The Architect's Dream",
                "sections": [
                    ("First Sketches", [
                        "The commission came in November, a museum of Japanese-American history to be built on Bainbridge Island. Hideo Tanaka spent three weeks refusing it.",
                        "The problem was not technical. The problem was that he did not know how to build a container for grief without making the grief itself the subject.",
                    ]),
                    ("The Design", [
                        "The solution came at 3am, in the manner that solutions to such problems always come: unexpectedly, in a form that seemed obvious in retrospect.",
                        "He would not build a monument. He would build a threshold — a place where one could stand between past and present, not forced to choose.",
                    ]),
                ],
            },
        ],
    },
    {
        "name": "Amara Okafor",
        "surname": "Okafor",
        "bio": "Amara Okafor is a Nigerian-British author whose work spans magical realism and contemporary fiction.",
        "chapters": [
            {
                "title": "The Weaver's House",
                "sections": [
                    ("Thread and Pattern", [
                        "In the compound of the Okafor family, three generations of women had worked the same loom. The pattern they wove was not static; it evolved with each generation, incorporating new colors and motifs while maintaining the essential geometry established by the great-grandmother.",
                        "Adaeze, the youngest, had learned the craft reluctantly. She had wanted to study law in Lagos. Her grandmother had said: study law, but learn the loom first. The law can wait; the loom does not wait.",
                    ]),
                    ("New Colors", [
                        "Adaeze returned from the market with synthetic dyes in colors that had no names in the local tradition. Her grandmother examined them with the same attention she gave everything: complete, nonjudgmental, curious.",
                        "They added two new colors to the pattern that year. Adaeze recorded them in the family notebook, where every adaptation had been noted since 1887.",
                    ]),
                ],
            },
            {
                "title": "Rain Oracle",
                "sections": [
                    ("The Prediction", [
                        "The rain oracle had not been consulted in forty years. The younger generation considered the practice superstition; the older generation considered it science they did not yet have the instruments to measure.",
                        "When the drought reached its sixth month, the village council voted 7-4 to consult the oracle. The four dissenters recorded their objections but agreed to participate.",
                    ]),
                    ("The Consultation", [
                        "Old Chinwe, the oracle's keeper, had assumed she would die without performing the ceremony again. She had kept the instruments clean and properly stored, out of professional habit rather than expectation.",
                        "The ceremony required three days. On the first day, Chinwe walked the boundary of the village, touching each tree that stood on the perimeter. On the second day, she did not speak. On the third day, she consulted the bones.",
                    ]),
                    ("The Answer", [
                        "The bones indicated rain within forty days, approaching from the southeast. Chinwe communicated this through a designated interpreter, maintaining the protocol established by her great-grandmother.",
                        "The rains came on the thirty-eighth day. The four council members who had objected said nothing. The seven who had voted for consultation also said nothing. That silence too was part of the protocol.",
                    ]),
                ],
            },
            {
                "title": "The London Flat",
                "sections": [
                    ("Arrival", [
                        "The flat in Peckham was smaller than anything Obiageli had imagined during her three months of planning. She had done the mathematics: 380 square feet, divided among herself, a bed, a desk, and the academic ambitions that had brought her across the Atlantic.",
                        "She found, to her surprise, that she was not lonely. The city provided a kind of anonymity that felt not like isolation but like freedom — the freedom of not being expected to be anything in particular.",
                    ]),
                    ("The University", [
                        "Her fellow students treated her with the particular brand of liberal guilt that made her feel simultaneously seen and unseen. They wanted her presence to signify something; she wanted to study medieval manuscripts.",
                        "Her supervisor, Professor Adeyemi, was Nigerian-British and had spent thirty years learning not to be a symbol. He taught her this as part of her academic training.",
                    ]),
                    ("Home", [
                        "After five years in London, Obiageli could not have said whether she lived in England or merely stayed there. Home remained where the air smelled right and the light fell at the angle her body had learned to expect.",
                        "She began writing at night, in Igbo, which surprised her. She had not expected the language to be so available, so ready to receive what she had to say.",
                    ]),
                ],
            },
            {
                "title": "Market Women",
                "sections": [
                    ("The Cooperative", [
                        "The women's cooperative had been meeting on the first Thursday of every month since 1974. The founding members were all dead; their daughters and granddaughters maintained the organization with modifications that preserved the essential structure while adapting it to current needs.",
                        "Membership required attendance at four consecutive meetings, a small annual fee, and the willingness to lend and borrow. The last requirement was the most difficult; many women had been raised to believe that needing help was a form of weakness.",
                    ]),
                    ("Trade Routes", [
                        "The cooperative's most innovative project was the transport network. By pooling resources, the members had purchased three vehicles that served twenty-seven villages along the eastern road.",
                        "The network had not been planned; it had grown organically from individual arrangements until its structure became visible. This, the founder's daughter often said, was how all important things were built.",
                    ]),
                ],
            },
            {
                "title": "Grandmother's Recipes",
                "sections": [
                    ("The Notebook", [
                        "The notebook was written in three languages: Igbo, Yoruba, and a functional English developed for practical purposes. The recipes were not measurements but proportions, and the proportions were expressed in relationships rather than numbers.",
                        "To make the pepper soup, the notebook said, use enough pepper to make your hands warm when you stir, and enough water to cover your reflection.",
                    ]),
                    ("Transmission", [
                        "Ngozi had been trying to recreate her grandmother's egusi soup for eleven years. Every version was good; none was right. The grandmother had died before Ngozi understood what questions to ask.",
                        "She had interviewed thirty women in the village, collecting variations. The variations clarified the range; they did not identify the specific preparation her grandmother had used.",
                    ]),
                    ("Discovery", [
                        "The answer came from an unexpected source: her grandmother's sister, aged ninety-one and living in a village Ngozi had not known existed.",
                        "The secret was not a technique or an ingredient. The secret was the intention. Her grandmother had cooked always for a specific number of people with a specific appetite, and the soup knew this.",
                    ]),
                ],
            },
        ],
    },
    {
        "name": "Dmitri Petrov",
        "surname": "Petrov",
        "bio": "Dmitri Petrov is a Russian-American novelist whose works explore the Soviet experience and its aftermath.",
        "chapters": [
            {
                "title": "The Leningrad Notebooks",
                "sections": [
                    ("Winter 1942", [
                        "The notebooks were kept in the inner pocket of a coat that had belonged to three men: a professor of mathematics, his son, and his son's colleague, all of them dead by the time the war ended.",
                        "The current keeper, a woman named Irina Sorokina, had found the coat in the rubble of a building on Nevsky Prospekt. She read the notebooks only after the siege was lifted, when she had the luxury of time.",
                    ]),
                    ("The Mathematics of Survival", [
                        "The professor had written in a precise hand that remained legible even as the entries grew shorter and the dates more irregular. He had been documenting, with mathematical precision, the calories available to each family member.",
                        "His calculations were unsparing: projected survival time, probability of liberation, expected deficit. He had not allowed himself sentimentality. The numbers were the numbers.",
                    ]),
                    ("After", [
                        "Irina eventually donated the notebooks to the State Historical Archive, where they were catalogued and stored. Fifty years later, a researcher discovered them.",
                        "The researcher, a young woman named Masha Krasnova, published a paper that included the professor's calculations alongside her own analysis of survival rates during the siege. The data matched, almost perfectly.",
                    ]),
                ],
            },
            {
                "title": "The Factory Town",
                "sections": [
                    ("Novgorodsk", [
                        "The factory had been producing ball bearings since 1927. The men who built it had believed they were constructing the future; their grandchildren, who still worked its floors, had different opinions about what it represented.",
                        "Pavel Ivanovich had worked at the factory for thirty-two years. He knew the machinery as he knew his own body — its rhythms, its complaints, its silences that signified problems before any instrument could detect them.",
                    ]),
                    ("Perestroika", [
                        "The changes came in stages, like spring thaw: first a loosening, then a flood. The factory director called meetings every Friday to explain the new policies, each meeting slightly contradicting the previous one.",
                        "Pavel listened and said nothing. He had learned early that the most important information was communicated not in what was said but in what was omitted.",
                    ]),
                    ("Closure", [
                        "The factory closed in 1994. Pavel received three months' severance and a letter signed by someone he had never met, thanking him for his years of service.",
                        "He sat in the letter for a long time. He had not expected gratitude. The sentiment felt like a foreign language: technically comprehensible, emotionally untranslatable.",
                    ]),
                ],
            },
            {
                "title": "The Dissident's Wife",
                "sections": [
                    ("The Arrest", [
                        "They came at 4am, which was the traditional hour. Natasha had been waiting for this arrival for three years; the wait had been a form of preparation that she had not fully understood until the moment itself.",
                        "Her husband was calm. This surprised her, though it should not have — he had always been calm in crises, reserving his anxiety for the ordinary accumulations of daily life.",
                    ]),
                    ("The Letters", [
                        "She was permitted to send one letter per month. She had learned to write in two registers simultaneously: the official surface, which described domestic matters and expressed appropriate sentiments, and the encoded level, which contained the actual information.",
                        "Alexei read both registers with equal attention. His replies, when they arrived, were in the same double voice.",
                    ]),
                    ("Release", [
                        "He was released on a Wednesday in March, thinner and slower but otherwise recognizably himself. She had been preparing for his return for six months, anticipating adjustments.",
                        "The first adjustment required was her own. She had become accustomed to making decisions alone. The relearning of consultation took longer than either of them had expected.",
                    ]),
                ],
            },
        ],
    },
    {
        "name": "Isabelle Delacroix",
        "surname": "Delacroix",
        "bio": "Isabelle Delacroix is a Belgian author celebrated for her psychological novels and lush European landscapes.",
        "chapters": [
            {
                "title": "The Bruges Convent",
                "sections": [
                    ("Arrival", [
                        "Sister Marie-Claire arrived at the convent in November, when the canals were freezing at their edges and the brick buildings gathered the grey light into themselves.",
                        "She had chosen this particular community for reasons she did not fully understand and would not examine too closely. The abbess, who had seen this kind of arrival before, gave her six months before asking questions.",
                    ]),
                    ("The Library", [
                        "The convent library held eleven thousand volumes, many of them manuscripts that predated the printing press. Sister Marie-Claire was assigned to cataloguing them, a task projected to require fourteen years.",
                        "She found this prospect not daunting but consoling. The manuscripts would not change. The task would not be completed in her lifetime. This was a form of stability that the secular world had not offered.",
                    ]),
                    ("The Question", [
                        "In her third year, the abbess asked the question she had promised to defer. Sister Marie-Claire answered it honestly, which took three hours.",
                        "The abbess listened without interruption. When Marie-Claire finished, the abbess said: the answer you have given is the answer you needed to give. Whether it is the complete answer is for you to determine.",
                    ]),
                ],
            },
            {
                "title": "The Antwerp Dealer",
                "sections": [
                    ("The Gallery", [
                        "Henri Vermeersch had been dealing in art for forty years, specializing in seventeenth-century Flemish masters. His gallery on Meir Street was small by deliberate design; he believed that cramped spaces encouraged attention.",
                        "The painting arrived on a Tuesday, wrapped in brown paper and carried by a man who would not give his name. Henri paid without asking questions, which was one of his professional rules.",
                    ]),
                    ("Authentication", [
                        "The authentication process took four months. Three experts were consulted; each provided a different opinion. The fourth expert, whom Henri had been saving, provided a fourth.",
                        "He kept the painting in his personal office, where he could examine it during the slow hours of the afternoon. He was increasingly convinced that the painting knew what it was, regardless of what the experts concluded.",
                    ]),
                    ("The Decision", [
                        "In the end, Henri declined to sell. This decision surprised everyone, including himself. The financial value was significant; the personal value, which he could not have quantified, was larger.",
                        "He had the painting hung in his home, in the room that received the best morning light. Every morning, before his coffee, he stood before it for exactly five minutes. This became a practice he would maintain until he died.",
                    ]),
                ],
            },
            {
                "title": "The Brussels Letters",
                "sections": [
                    ("Archive", [
                        "The letters had been held in the family archive since 1918, unopened because no one had felt authorized to open them. The youngest grandchild, a historian named Claire Dupont, finally obtained the family's permission.",
                        "There were 847 letters, arranged by date and tied with the original ribbon. The ribbon was blue and had survived a century better than the paper it contained.",
                    ]),
                    ("Reading", [
                        "The letters were in French, Flemish, and German, in proportions that reflected the political transitions of the era they documented. The grandmother had code-switched as a matter of survival.",
                        "Claire read them chronologically, which was not how they had been written; they existed in a different time, the time of their composition, which was parallel to rather than sequential with each other.",
                    ]),
                    ("Publication", [
                        "The published edition appeared three years after Claire began her reading. She had translated the non-French letters and written an introduction of forty pages.",
                        "The introduction was, her colleagues said, the best thing she had written. She was not surprised; the grandmother had been a better writer than any of her descendants, and proximity to that excellence had raised everyone.",
                    ]),
                ],
            },
            {
                "title": "The Ghent Garden",
                "sections": [
                    ("Spring", [
                        "The garden had been in the family for six generations, each adding or removing elements according to its aesthetic convictions. The result was not coherent in any classical sense; it was coherent in the way that families are coherent, through the accumulation of contradictions.",
                        "Mathilde Vandenberghe spent every summer there from childhood, absorbing its particular logic without being able to articulate it.",
                    ]),
                    ("Inheritance", [
                        "When her parents died, Mathilde inherited the garden along with the house and the obligation to decide what to do with both. She was a professor of contemporary literature in Amsterdam with no intention of returning to Ghent.",
                        "She made no decision for three years. She paid a gardener and visited twice annually, in spring and autumn, to check that nothing had been lost.",
                    ]),
                    ("Resolution", [
                        "The resolution came, as resolutions often do, from an unexpected direction. A neighbor offered to buy the house but not the garden, wanting to preserve it as a shared green space.",
                        "Mathilde accepted. She kept legal ownership and visiting rights, relinquishing maintenance responsibility. The garden continued without her daily attention, which was, she eventually understood, exactly what the garden had always been doing.",
                    ]),
                ],
            },
        ],
    },
]


def create_anthology_odt():
    """Create anthology.odt in /home/user/Documents/ with all 5 authors and chapters.
    Content is formatted with bold author names separating sections. No heading styles,
    TOC, or bookmarks - those are what the agent must add.
    """
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    doc = OpenDocumentText()

    # Define styles
    # Normal paragraph style
    normal_style = Style(name="Text Body", family="paragraph")
    normal_style.addElement(ParagraphProperties(marginbottom="0.2cm", margintop="0.2cm"))
    normal_style.addElement(TextProperties(fontsize="12pt", fontfamily="Times New Roman"))
    doc.styles.addElement(normal_style)

    # Bold style for inline spans (author names, chapter labels)
    bold_style = Style(name="Bold Text", family="text")
    bold_style.addElement(TextProperties(fontweight="bold", fontsize="14pt"))
    doc.styles.addElement(bold_style)

    # Chapter label style (bold, slightly larger)
    chapter_style = Style(name="Chapter Label", family="text")
    chapter_style.addElement(TextProperties(fontweight="bold", fontsize="13pt"))
    doc.styles.addElement(chapter_style)

    # Section label style (bold)
    section_style = Style(name="Section Label", family="text")
    section_style.addElement(TextProperties(fontweight="bold", fontsize="12pt"))
    doc.styles.addElement(section_style)

    def add_paragraph(text, bold=False, para_style="Text Body"):
        """Add a paragraph with given text to the document."""
        p = P(stylename=para_style)
        if bold:
            span = Span(stylename="Bold Text")
            span.addText(text)
            p.addElement(span)
        else:
            p.addText(text)
        doc.text.addElement(p)
        return p

    def add_empty_paragraph():
        """Add an empty paragraph for spacing."""
        p = P(stylename="Text Body")
        p.addText("")
        doc.text.addElement(p)

    # Title page
    title_p = P(stylename="Text Body")
    title_span = Span(stylename="Bold Text")
    title_span.addText("ANTHOLOGY: Voices from Five Continents")
    title_p.addElement(title_span)
    doc.text.addElement(title_p)

    add_empty_paragraph()

    subtitle_p = P(stylename="Text Body")
    subtitle_p.addText("A collection of literary works from five contemporary authors, each exploring themes of memory, identity, and belonging across diverse cultural landscapes.")
    doc.text.addElement(subtitle_p)

    add_empty_paragraph()
    add_empty_paragraph()

    # Write each author section
    for author_data in AUTHORS:
        # Author separator: bold author name
        add_empty_paragraph()
        author_p = P(stylename="Text Body")
        author_span = Span(stylename="Bold Text")
        author_span.addText(f"*** {author_data['name'].upper()} ***")
        author_p.addElement(author_span)
        doc.text.addElement(author_p)

        add_empty_paragraph()

        # Author bio
        bio_p = P(stylename="Text Body")
        bio_p.addText(author_data["bio"])
        doc.text.addElement(bio_p)

        add_empty_paragraph()

        # Write each chapter
        for chap_num, chapter in enumerate(author_data["chapters"], 1):
            # Chapter title (bold label — agent must convert to Heading 1)
            chap_p = P(stylename="Text Body")
            chap_span = Span(stylename="Chapter Label")
            chap_span.addText(f"Chapter {chap_num}: {chapter['title']}")
            chap_p.addElement(chap_span)
            doc.text.addElement(chap_p)

            add_empty_paragraph()

            # Write each section
            for section_name, paragraphs in chapter["sections"]:
                # Section title (bold — agent must convert to Heading 2)
                sec_p = P(stylename="Text Body")
                sec_span = Span(stylename="Section Label")
                sec_span.addText(section_name)
                sec_p.addElement(sec_span)
                doc.text.addElement(sec_p)

                add_empty_paragraph()

                # Section body paragraphs
                for para_text in paragraphs:
                    body_p = P(stylename="Text Body")
                    body_p.addText(para_text)
                    doc.text.addElement(body_p)

                add_empty_paragraph()

            add_empty_paragraph()

    doc.save(ANTHOLOGY_FILE)
    print(f"Anthology file created: {ANTHOLOGY_FILE}")


def create_split_directory():
    """Create the Desktop/anthology_split/ directory."""
    os.makedirs(SPLIT_DIR, exist_ok=True)
    print(f"Split directory created: {SPLIT_DIR}")


def main():
    # 1. Create anthology.odt in Documents
    create_anthology_odt()

    # 2. Create Desktop/anthology_split/ directory
    create_split_directory()

    # 3. Launch LibreOffice Writer with the anthology file
    launch_gui(f'libreoffice --writer "{ANTHOLOGY_FILE}"', delay_sec=2.0)
    print("GUI_READY: launched LibreOffice Writer with anthology.odt (DISPLAY=:0)")


main()
