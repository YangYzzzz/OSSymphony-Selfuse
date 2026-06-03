"""
Initial Setup: Create a 50-page ebook PDF with 5 bookmarks but no TOC page.
Task ID: pdf_gf1_037
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf1_037'
OUTPUT = f'{DOCUMENTS}/ebook.pdf'

# Bookmark structure: (title, start_page_0indexed)
BOOKMARKS = [
    ("Prologue", 0),
    ("Chapter 1", 7),
    ("Chapter 2", 19),
    ("Chapter 3", 32),
    ("Epilogue", 44),
]

# Realistic ebook content for each section
SECTION_CONTENT = {
    "Prologue": [
        "The morning light filtered through the curtains of the old Victorian house on Maple Street. Eleanor Blackwood stood at the kitchen window, watching the fog roll in from the harbor. She had lived in this coastal town for thirty-seven years, yet something about this particular autumn felt different.",
        "The letter had arrived three days ago, tucked inside a plain manila envelope with no return address. Its contents had shaken the foundations of everything she believed about her family's history. Now, as she sipped her Earl Grey tea, she knew there was no turning back.",
        "This is the story of how one woman's search for truth led her across continents, through centuries of family secrets, and ultimately to a discovery that would change not just her life, but the lives of everyone she loved.",
        "The harbor bells rang twice, signaling the arrival of the morning ferry. Eleanor set down her cup, gathered her coat, and stepped into the misty morning air. The journey was about to begin.",
        "She had always been curious about the locked room in the attic. Her grandmother had forbidden anyone from entering it, and after her passing, the key had seemingly vanished. But the letter mentioned a key hidden behind the third brick in the garden wall.",
        "Walking past the rose bushes her grandmother had planted decades ago, Eleanor counted the bricks methodically. Behind the third one from the left, her fingers found a cold metal object wrapped in oilcloth. The key was exactly where the letter said it would be.",
        "The discovery sent a chill down her spine that had nothing to do with the autumn air. Someone knew about the room. Someone had been watching, waiting, perhaps for years, for the right moment to reveal its existence.",
    ],
    "Chapter 1": [
        "The attic room was smaller than Eleanor had imagined. Dust motes danced in the pale light that seeped through a single, grimy window. Against the far wall stood an antique desk, its surface covered with stacks of leather-bound journals and yellowed correspondence.",
        "As Eleanor carefully opened the first journal, dated 1887, she recognized her great-grandmother's distinctive handwriting. Margaret Blackwood had been a prolific writer, it seemed, documenting everything from daily household affairs to elaborate botanical observations.",
        "But it was the entries from September 1892 that caught Eleanor's attention. Margaret wrote of a visitor, a man named Dr. Cornelius Ashworth, who arrived from London carrying a wooden case and speaking of an extraordinary discovery in the Egyptian desert.",
        "The discovery, according to Margaret's account, was nothing less than a complete manuscript written in an unknown language, found sealed inside a bronze cylinder within a previously undiscovered chamber beneath the Great Pyramid. Dr. Ashworth believed it predated all known writing systems by at least two thousand years.",
        "Eleanor spent the next several hours reading through the journals, her tea growing cold beside her. Each entry revealed another piece of a puzzle she was only beginning to comprehend. The manuscript had been brought to England in secret, studied by a small circle of scholars who called themselves the Meridian Society.",
        "Her great-grandmother had been more than a passive observer in these events. Margaret Blackwood, it turned out, was a gifted linguist who had been recruited by the Society to help decode the mysterious text. Her contributions to the translation effort were documented in meticulous detail.",
        "The implications were staggering. If the journals were accurate, Margaret had successfully translated portions of the manuscript, revealing knowledge that challenged the accepted understanding of ancient civilizations. Technology, agriculture, astronomy described with a sophistication that supposedly didn't exist for millennia after the manuscript's estimated date.",
        "Eleanor carefully photographed each page with her phone, then locked the room again. She needed to verify these claims before telling anyone. Her first stop would be the university library, where historical records of the Meridian Society might still exist.",
        "That evening, as rain drummed against the windows, Eleanor sat at her kitchen table with her laptop open. A preliminary search turned up scattered references to a Meridian Society active in Victorian England, described variously as a gentleman's club, a learned society, and in one conspiratorial blog post, a secret organization dedicated to suppressing ancient knowledge.",
        "She bookmarked everything and made a list of archives and libraries she would need to visit. The British Library, the Bodleian at Oxford, the private collection of the Royal Geographical Society. It was going to be a long journey, but Eleanor Blackwood was not the kind of woman who left mysteries unsolved.",
        "The phone rang, startling her from her research. It was her daughter, Catherine, calling from her flat in Edinburgh. After some small talk about the weather and Catherine's work at the museum, Eleanor found herself on the verge of mentioning the journals. She held back. Not yet. Not until she had more evidence.",
        "Sleep came fitfully that night. Eleanor dreamed of sand-colored corridors stretching endlessly underground, lit by torches that cast dancing shadows on walls covered in strange symbols. In the dream, she could almost read them.",
    ],
    "Chapter 2": [
        "Two weeks later, Eleanor found herself in the reading room of the British Library, surrounded by boxes of archived correspondence from the late Victorian period. The librarian, a helpful young woman named Priya, had located three separate collections that mentioned the Meridian Society.",
        "The most revealing was a set of letters between Sir Arthur Westlake, a prominent geologist, and his wife Lady Helena. Sir Arthur had been a founding member of the Meridian Society, and his letters home from various expeditions contained details that corroborated Margaret's journals.",
        "In a letter dated March 1893, Sir Arthur wrote: 'The cylinder manuscript has proven more remarkable than any of us dared hope. Mrs. Blackwood's translations suggest a civilization of extraordinary advancement. If this becomes public, it will overturn everything we think we know about human history.'",
        "Eleanor's hands trembled as she carefully turned the fragile pages. Here was independent confirmation of her great-grandmother's involvement. But there was more. Sir Arthur's later letters grew increasingly anxious, hinting at disagreements within the Society about what to do with their findings.",
        "A faction led by Dr. Ashworth wanted to publish everything and let the scientific community evaluate the evidence. Another group, led by Lord Pemberton, argued that the world was not ready for such revelations and that the manuscript should be secured indefinitely.",
        "The debate, Sir Arthur wrote, became bitter and personal. Accusations of forgery flew from one camp while the other accused their opponents of intellectual cowardice. The Society, which had operated harmoniously for decades, was tearing itself apart.",
        "Eleanor spent three days in the British Library, photographing documents and taking careful notes. She also found a membership roster from 1890, which listed twenty-three names, including Margaret Blackwood, one of only two women in the group.",
        "From London, Eleanor traveled to Oxford, where the Bodleian Library held papers donated by Lord Pemberton's descendants. These painted a very different picture of events. According to Pemberton's personal diary, the manuscript was not merely controversial but dangerous.",
        "Pemberton wrote of encoded instructions within the text, formulas and diagrams that, if interpreted correctly, could lead to technologies of immense power. He compared it to giving a child a loaded weapon. The world of the 1890s, already destabilized by rapid industrialization and imperial rivalries, could not be trusted with such knowledge.",
        "The parallel narratives fascinated Eleanor. Both sides believed they were acting in humanity's best interest. Both had compelling arguments. And somewhere in between, her great-grandmother had been quietly working on her translations, perhaps understanding both perspectives better than anyone.",
        "On her last evening in Oxford, Eleanor received an email from an address she didn't recognize. The subject line read simply: 'Regarding Margaret Blackwood's work.' The message was brief: 'Ms. Blackwood, your inquiries have not gone unnoticed. There are those who would prefer the past remain undisturbed. Consider this a friendly warning. A friend.'",
        "Eleanor stared at the screen for a long time. Then, rather than feeling afraid, she felt a surge of determination. Someone was watching. Someone knew what she was looking for. That meant there was still something to find.",
        "She booked a ticket to Cairo for the following week. If the cylinder had been found beneath the Great Pyramid, perhaps there were still traces to be discovered. Modern archaeological techniques had advanced considerably since the 1890s.",
    ],
    "Chapter 3": [
        "Cairo hit Eleanor like a warm wall of sound and color. The airport was chaos, beautiful chaos, and as her taxi wound through the city streets, she marveled at the juxtaposition of ancient and modern that defined this remarkable place.",
        "Her contact in Egypt was Dr. Amira Hassan, a professor of archaeology at the American University in Cairo. Eleanor had reached out through academic channels, framing her inquiry as genealogical research into her great-grandmother's Victorian-era travels.",
        "Dr. Hassan was a petite woman with sharp eyes and an infectious laugh. Over strong coffee in her university office, she listened to Eleanor's carefully edited version of events. When Eleanor mentioned the Meridian Society, Dr. Hassan's expression changed.",
        "'The Meridian Society,' she repeated slowly. 'I have heard this name before. My doctoral advisor, Professor Khalil, mentioned them once. He said they were responsible for the most significant archaeological cover-up of the nineteenth century.'",
        "Eleanor's heart raced. 'What did he mean by that?'",
        "'He died before he could tell me more,' Dr. Hassan said quietly. 'But he left me his research files. I never had reason to look through them until now. Shall we?'",
        "Professor Khalil's files were stored in a climate-controlled room in the university's archaeology department. Boxes upon boxes of notes, photographs, and documents, many in Arabic, some in French and English. It took Eleanor and Amira two full days to sort through them.",
        "What they found was extraordinary. Professor Khalil had spent decades tracking the movements of the Meridian Society's Egyptian expeditions. He had identified the exact location where the cylinder was reportedly found: a narrow passage beneath the Queen's Chamber of the Great Pyramid, sealed behind a block of limestone that had been replaced so perfectly it was virtually undetectable.",
        "More importantly, Khalil had found evidence suggesting that the passage had been reopened in 1952, during a period of political upheaval in Egypt when many archaeological sites were briefly unguarded. Someone had gone back. Whether they found anything new was unclear.",
        "Amira arranged for Eleanor to visit the Giza plateau with a special research permit. Standing before the Great Pyramid, Eleanor felt the weight of centuries pressing down on her. Somewhere inside that massive structure, her great-grandmother's story had begun.",
        "The visit itself was carefully supervised and limited to the public areas. But Eleanor noticed something that others might have missed: a small mark carved into the limestone at the entrance to the descending passage. It matched a symbol she had seen repeatedly in Margaret's journals.",
        "That evening, back at her hotel, Eleanor laid out all her evidence on the bed. The journals, the British Library documents, the Bodleian papers, Professor Khalil's research, and her own photographs. The pieces were coming together, forming a picture that was both thrilling and troubling.",
        "Her phone buzzed. A text from an unknown number: 'Leave Cairo. This is not a game.' Eleanor deleted the message and opened her laptop. She had work to do.",
    ],
    "Epilogue": [
        "Six months after her journey began, Eleanor Blackwood sat once again at her kitchen table in the house on Maple Street. The fog was rolling in from the harbor, just as it had on the morning she found the key.",
        "The manuscript, or rather, Margaret's complete translation of it, now resided in a secure vault at the British Museum, placed there with the cooperation of Dr. Hassan and a team of international scholars who had verified its authenticity. The announcement of its existence had indeed sent shockwaves through the academic world.",
        "But Eleanor had made a decision that her great-grandmother would have approved of. Rather than suppressing the knowledge or releasing it all at once, she had worked with the scholars to create a careful, staged program of publication. Each section of the translation would be released with full academic commentary and historical context.",
        "The first paper, published in Nature, had already generated more citations than any archaeology paper in the journal's history. Scientists and historians around the world were re-examining long-held assumptions about the development of ancient civilizations.",
        "Catherine had finally been told everything. She had cried, laughed, and then immediately begun planning an exhibition at her museum in Edinburgh. Mother and daughter had never been closer.",
        "The threatening messages had stopped after Eleanor went public. Whoever had been watching apparently decided that suppression was no longer viable. Eleanor suspected they were members of a modern incarnation of Lord Pemberton's faction, but she had no proof and, truthfully, no desire to pursue them.",
        "On quiet evenings, Eleanor sometimes climbed the stairs to the attic room. She would sit at Margaret's desk, running her fingers over the worn leather covers of the journals, and feel a connection across time to the remarkable woman who had first unlocked the secrets of the cylinder manuscript.",
        "The harbor bells rang twice, and Eleanor smiled. Another ferry arriving, another day beginning. The world was a little different now, a little more mysterious, a little more wonderful. And that, she thought, was exactly as it should be.",
        "Margaret Blackwood's final journal entry, dated December 24, 1901, read: 'Knowledge is neither good nor evil. It simply is. What matters is that we have the courage to seek it and the wisdom to share it. I hope that someday, someone will find these pages and carry the work forward.' Eleanor closed the journal gently. The work would indeed continue.",
    ],
}


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions
    WIDTH, HEIGHT = 595, 842  # A4
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 523
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 770
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

    # Track which section starts on which page
    section_start_pages = {}
    current_page_count = 0

    # Helper to create content pages for a section
    def add_section(title, paragraphs, target_page_count):
        nonlocal current_page_count
        section_start_pages[title] = current_page_count

        # First page of section: title + content
        page = doc.new_page(width=WIDTH, height=HEIGHT)
        current_page_count += 1

        # Section title
        y_pos = MARGIN_TOP + 40
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, y_pos),
            title,
            fontsize=24,
            fontname="tibo",
            color=(0.1, 0.1, 0.3),
        )

        # Decorative line under title
        shape = page.new_shape()
        shape.draw_line(
            pymupdf.Point(MARGIN_LEFT, y_pos + 10),
            pymupdf.Point(MARGIN_RIGHT, y_pos + 10),
        )
        shape.finish(color=(0.3, 0.3, 0.5), width=1.5)
        shape.commit()

        y_pos += 40
        para_idx = 0

        # Fill content
        while para_idx < len(paragraphs):
            if y_pos > MARGIN_BOTTOM - 30:
                # Need a new page
                page = doc.new_page(width=WIDTH, height=HEIGHT)
                current_page_count += 1
                y_pos = MARGIN_TOP

            # Insert paragraph text in a textbox
            text_rect = pymupdf.Rect(MARGIN_LEFT, y_pos, MARGIN_RIGHT, MARGIN_BOTTOM - 20)
            excess = page.insert_textbox(
                text_rect,
                paragraphs[para_idx],
                fontsize=11,
                fontname="tiro",
                color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

            # Estimate the height consumed (approximate)
            text_len = len(paragraphs[para_idx])
            chars_per_line = int(TEXT_WIDTH / (11 * 0.5))
            num_lines = max(1, (text_len // chars_per_line) + 1)
            line_height = 14
            consumed_height = num_lines * line_height + 12  # paragraph spacing

            y_pos += consumed_height
            para_idx += 1

        # Fill remaining pages for the section up to target count
        while current_page_count < target_page_count:
            page = doc.new_page(width=WIDTH, height=HEIGHT)
            current_page_count += 1
            # Add a subtle page continuation marker
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT, MARGIN_TOP),
                f"{title} (continued)",
                fontsize=9,
                fontname="heit",
                color=(0.5, 0.5, 0.5),
            )
            # Add some filler body text for realism
            filler_texts = [
                "The research continued to reveal fascinating connections between the ancient manuscript and modern scientific understanding. Each page of Margaret's translation opened new avenues of inquiry.",
                "Dr. Hassan's team documented every finding meticulously, creating a comprehensive record that would serve scholars for generations to come. The collaboration between institutions proved invaluable.",
                "The implications extended far beyond archaeology. Historians, linguists, and even physicists found relevance in the translated passages, suggesting an interconnected ancient knowledge system.",
                "Eleanor maintained detailed correspondence with researchers worldwide, building a network of scholars dedicated to understanding the full scope of the discovery.",
            ]
            y_pos = MARGIN_TOP + 20
            for ft in filler_texts:
                if y_pos > MARGIN_BOTTOM - 60:
                    break
                text_rect = pymupdf.Rect(MARGIN_LEFT, y_pos, MARGIN_RIGHT, y_pos + 100)
                page.insert_textbox(
                    text_rect, ft,
                    fontsize=11, fontname="tiro",
                    color=(0.1, 0.1, 0.1),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                y_pos += 80

    # Add page numbers at the bottom of each page (after all content is created)
    # First create sections with their target page counts
    # Bookmarks: Prologue=1, Ch1=8, Ch2=20, Ch3=33, Epilogue=45 (1-indexed)
    # So sections span: Prologue 1-7, Ch1 8-19, Ch2 20-32, Ch3 33-44, Epilogue 45-50

    section_targets = [
        ("Prologue", SECTION_CONTENT["Prologue"], 7),       # pages 1-7 (0-indexed: 0-6)
        ("Chapter 1", SECTION_CONTENT["Chapter 1"], 19),     # pages 8-19 (0-indexed: 7-18)
        ("Chapter 2", SECTION_CONTENT["Chapter 2"], 32),     # pages 20-32 (0-indexed: 19-31)
        ("Chapter 3", SECTION_CONTENT["Chapter 3"], 44),     # pages 33-44 (0-indexed: 32-43)
        ("Epilogue", SECTION_CONTENT["Epilogue"], 50),       # pages 45-50 (0-indexed: 44-49)
    ]

    for title, content, target in section_targets:
        add_section(title, content, target)

    # Add page numbers to all pages
    for i in range(doc.page_count):
        page = doc[i]
        page.insert_text(
            pymupdf.Point(WIDTH / 2 - 10, HEIGHT - 30),
            str(i + 1),
            fontsize=10,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

    # Set bookmarks/TOC (1-indexed page numbers)
    toc = [
        [1, "Prologue", 1],
        [1, "Chapter 1", 8],
        [1, "Chapter 2", 20],
        [1, "Chapter 3", 33],
        [1, "Epilogue", 45],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 50')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
