"""
Initial Setup: 20-page book document with mirrored layout, no headers configured.
Task ID: writer_fs_060
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_060'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


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
    from odf.opendocument import OpenDocumentText
    from odf.style import (
        Style, PageLayoutProperties, MasterPage, PageLayout,
        ParagraphProperties, TextProperties, HeaderFooterProperties
    )
    from odf.text import P, Span, H
    from odf import text as odftext

    doc = OpenDocumentText()

    # --- Page Layout with mirrored margins (for book printing) ---
    pl = PageLayout(name="pm1")
    pl.addElement(PageLayoutProperties(
        pagewidth="8.5in",
        pageheight="11in",
        marginleft="1.2in",
        marginright="0.8in",
        margintop="1in",
        marginbottom="1in",
        writingmode="lr-tb"
    ))
    # Set mirror margins via attributes on the page layout properties
    # Set mirrored layout mode via direct XML attribute
    plp = pl.getElementsByType(PageLayoutProperties)[0]
    ns_style = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
    plp.setAttrNS(ns_style, 'layout-mode', 'mirrored')
    doc.automaticstyles.addElement(pl)

    # --- Master Page referencing our page layout (no headers) ---
    mp = MasterPage(name="Standard", pagelayoutname="pm1")
    doc.masterstyles.addElement(mp)

    # --- Paragraph styles ---
    # Body text style
    body_style = Style(name="BookBody", family="paragraph")
    body_style.addElement(ParagraphProperties(
        margintop="0in",
        marginbottom="0.08in",
        textalign="justify"
    ))
    body_style.addElement(TextProperties(
        fontsize="12pt",
        fontname="Liberation Serif"
    ))
    doc.styles.addElement(body_style)

    # Chapter heading style
    chapter_style = Style(name="ChapterHeading", family="paragraph")
    chapter_style.addElement(ParagraphProperties(
        margintop="0.5in",
        marginbottom="0.3in",
        textalign="center",
        breakbefore="page"
    ))
    chapter_style.addElement(TextProperties(
        fontsize="24pt",
        fontweight="bold",
        fontname="Liberation Sans"
    ))
    doc.styles.addElement(chapter_style)

    # --- Book content across ~20 pages ---
    chapters = [
        {
            "title": "Chapter 1: The Beginning",
            "paragraphs": [
                "In the early morning light of a crisp autumn day, the small town of Millbrook began to stir. "
                "The cobblestone streets, still damp from the overnight rain, reflected the amber glow of the "
                "street lamps that had yet to be extinguished. Margaret Thornton pulled her woolen shawl tighter "
                "around her shoulders as she stepped onto the front porch of her Victorian-era home.",

                "The garden, once her mother's pride, had been allowed to grow somewhat wild over the past two "
                "seasons. Roses climbed the wrought-iron fence with an abandon that would have horrified the "
                "elder Mrs. Thornton, but Margaret found their unruly beauty oddly comforting. Each morning she "
                "paused here, taking in the scent of dew-kissed petals before beginning her walk to the office.",

                "As the town librarian, Margaret held a position of quiet importance in Millbrook. The library, "
                "a stately brick building on the corner of Main and Oak streets, had been the heart of the "
                "community for over a century. Its shelves housed not only books but also the collective memory "
                "of three generations of townsfolk. Margaret knew every shelf, every corner, and most of the "
                "stories that the walls themselves could tell.",

                "That particular Tuesday in October would prove to be different from all the others. A letter "
                "had arrived in the morning post — not an ordinary letter, but one bearing the seal of the "
                "National Historical Society. Margaret's hands trembled slightly as she turned the envelope over. "
                "She had written to them months ago, almost on a whim, about a collection of documents she had "
                "discovered in the library's basement archives.",
            ]
        },
        {
            "title": "Chapter 2: The Discovery",
            "paragraphs": [
                "The basement of the Millbrook Library was a labyrinth of forgotten knowledge. Shelves stretched "
                "from floor to ceiling, packed with yellowing newspapers, leather-bound ledgers, and boxes of "
                "correspondence dating back to the town's founding in 1847. It was in one of these boxes that "
                "Margaret had made her discovery.",

                "Hidden beneath a stack of property deeds and tax records from the 1890s, she had found a bundle "
                "of letters tied with a faded blue ribbon. The handwriting was elegant, the ink barely legible "
                "after more than a century. But as Margaret carefully transcribed each letter, a remarkable story "
                "emerged — one that would rewrite the history of not just Millbrook, but the entire region.",

                "The letters were written by Elizabeth Fairfax, the wife of the town's first mayor, to her sister "
                "in Boston. In them, she described in vivid detail the establishment of an underground railroad "
                "station that operated from beneath the very building that would later become the library. The "
                "passages were hidden behind false walls in the cellar, and Elizabeth served as the primary "
                "coordinator for the entire operation.",

                "Margaret spent three weeks verifying the authenticity of the letters. She cross-referenced dates "
                "with known historical events, checked the paper composition with a specialist at the state "
                "university, and traced the genealogy of the Fairfax family through census records. Everything "
                "checked out. The letters were genuine, and the story they told was extraordinary.",

                "Now, the National Historical Society had responded to her inquiry. Margaret sat at her desk, "
                "the morning light streaming through the tall windows, and carefully opened the envelope. The "
                "letter inside was brief but its implications were enormous: they wanted to send a team of "
                "historians to Millbrook to examine the documents and, if they confirmed her findings, to begin "
                "an archaeological survey of the library's basement.",
            ]
        },
        {
            "title": "Chapter 3: Preparations",
            "paragraphs": [
                "The news of the Historical Society's interest spread through Millbrook like wildfire. Within "
                "days, Margaret found herself at the center of a whirlwind of activity. The town council called "
                "an emergency session. The local newspaper, the Millbrook Gazette, ran a front-page story. And "
                "the phone in the library rang incessantly with calls from curious residents and ambitious "
                "journalists.",

                "Margaret handled the attention with characteristic grace, though she privately confessed to her "
                "friend Sarah that the sudden spotlight made her uncomfortable. She was a scholar at heart, "
                "happiest when surrounded by books and silence. The prospect of television cameras in her "
                "library filled her with a mixture of pride and dread.",

                "The preparations for the Historical Society's visit consumed every waking hour. The basement "
                "needed to be made accessible — decades of accumulated debris had to be carefully cataloged and "
                "removed. Margaret insisted that nothing be discarded; every scrap of paper, every forgotten "
                "artifact, might hold clues that would help the historians in their work.",

                "Thomas Reynolds, the town's retired contractor, volunteered to shore up the basement's aging "
                "support beams. His granddaughter, a structural engineering student at MIT, came down for a "
                "weekend to help assess the integrity of the foundation. Together, they determined that while "
                "the building was sound, certain areas of the basement would need reinforcement before any "
                "serious excavation could begin.",

                "As the days passed, Margaret began to notice something curious. Several prominent citizens "
                "seemed unusually interested in the project — not in the historical discovery itself, but in "
                "certain specific details. Town councilman Harold Pemberton, whose family had been in Millbrook "
                "for five generations, asked Margaret repeatedly about which walls had been identified as "
                "potentially concealing hidden passages.",
            ]
        },
        {
            "title": "Chapter 4: The Arrival",
            "paragraphs": [
                "On the morning of November fifteenth, a silver sedan pulled into the library's parking lot. "
                "Dr. Catherine Webb, the lead historian from the National Historical Society, stepped out and "
                "surveyed the building with an appraising eye. She was accompanied by two colleagues: Dr. James "
                "Okafor, a specialist in antebellum American history, and Dr. Mei-Lin Zhang, an archaeologist "
                "with extensive experience in historic building surveys.",

                "Margaret greeted them at the front door, her heart beating faster than she would have liked. "
                "The documents she had found were safely stored in acid-free archival sleeves, arranged "
                "chronologically in a climate-controlled cabinet she had purchased with her own savings. She "
                "had spent weeks preparing a detailed index of each letter, cross-referenced with the historical "
                "context she had been able to establish.",

                "Dr. Webb's eyes widened as she examined the first letter. She held it up to the light, studying "
                "the watermark, then carefully turned it over to examine the wax seal on the envelope. Without "
                "a word, she pulled a jeweler's loupe from her pocket and bent closer. After several minutes "
                "of silent examination, she looked up at Margaret with an expression that blended amazement "
                "with professional caution.",

                "The team spent three days examining the letters and the basement. They mapped the foundation "
                "walls, took core samples from the mortar, and used ground-penetrating radar to scan for "
                "hollow spaces behind the stone walls. On the evening of the second day, the radar revealed "
                "what appeared to be a chamber behind the northeast wall — exactly where Elizabeth Fairfax's "
                "letters had described a hidden passage.",

                "The excitement in the library was palpable. Even the most skeptical members of the team "
                "could not deny the significance of what the radar had shown. Dr. Okafor, who had initially "
                "been reserved in his enthusiasm, was now poring over Margaret's transcriptions with undisguised "
                "fascination, making copious notes in his leather-bound journal.",
            ]
        },
        {
            "title": "Chapter 5: The Revelation",
            "paragraphs": [
                "The breakthrough came on a cold Saturday morning in late November. With the town council's "
                "permission and under the careful supervision of Dr. Zhang, a section of the northeast basement "
                "wall was carefully dismantled, stone by stone. Behind it, exactly as Elizabeth Fairfax had "
                "described one hundred and seventy years earlier, lay a narrow passage leading into darkness.",

                "Margaret was the first civilian to enter the hidden chamber. The air was cool and still, "
                "carrying the faint scent of old earth and ancient timber. The passage was low — she had to "
                "duck to avoid the rough-hewn ceiling beams — but it opened after about twenty feet into a "
                "room roughly twelve feet square. Against one wall stood a wooden bench, its surface worn "
                "smooth by countless hands. Above it, carved into the stone, were words that made Margaret's "
                "breath catch in her throat.",

                "The inscription read: 'Freedom's Gate — May all who pass through find their way to liberty.' "
                "Below it, someone had carved a series of dates, beginning with March 1852 and ending with "
                "September 1863. Each date, Margaret would later determine, corresponded to a documented "
                "movement along the underground railroad in the region.",

                "The discovery made national news. Within a week, Millbrook was featured in every major "
                "newspaper and on three network news broadcasts. The library, once a quiet refuge for readers "
                "and researchers, became a destination for historians, tourists, and descendants of those who "
                "had traveled the underground railroad. Margaret found herself giving tours, answering "
                "questions from documentary filmmakers, and fielding offers from publishers eager to tell "
                "the story.",

                "But amid all the excitement and recognition, Margaret never lost sight of what mattered most. "
                "The hidden chamber beneath the library was more than a historical curiosity — it was a "
                "testament to the courage of ordinary people who had risked everything for the cause of human "
                "freedom. And it was Margaret Thornton, the quiet librarian of Millbrook, who had given their "
                "story back to the world.",
            ]
        },
    ]

    # Write chapters — first chapter without page break
    for i, chapter in enumerate(chapters):
        if i == 0:
            # First chapter heading without page break
            first_heading_style = Style(name="FirstChapterHeading", family="paragraph")
            first_heading_style.addElement(ParagraphProperties(
                margintop="0.5in",
                marginbottom="0.3in",
                textalign="center"
            ))
            first_heading_style.addElement(TextProperties(
                fontsize="24pt",
                fontweight="bold",
                fontname="Liberation Sans"
            ))
            doc.styles.addElement(first_heading_style)
            heading = P(stylename=first_heading_style)
        else:
            heading = P(stylename=chapter_style)
        heading.addText(chapter["title"])
        doc.text.addElement(heading)

        for para_text in chapter["paragraphs"]:
            p = P(stylename=body_style)
            p.addText(para_text)
            doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
