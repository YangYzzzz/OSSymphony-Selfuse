"""
Initial Setup: Insert subdocuments into master document
Task ID: writer_rm_069
Domain: libreoffice_writer

Creates:
- 6 chapter ODT files (Ch1.odt - Ch6.odt) with content
- 3 new ODT files (Preface.odt, Midword.odt, Afterword.odt) on disk
- A master document (Anthology_Master.odm) linking only Ch1-Ch6
- Opens the master document in LibreOffice Writer
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_069'


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


def create_odt_file(filepath, title, body_paragraphs):
    """Create an ODT file with given title and body paragraphs using odfpy."""
    from odf.opendocument import OpenDocumentText
    from odf import text as odftext
    from odf.style import Style, TextProperties, ParagraphProperties

    doc = OpenDocumentText()

    # Define a heading style
    h_style = Style(name="HeadingStyle", family="paragraph")
    h_style.addElement(TextProperties(fontsize="18pt", fontweight="bold"))
    h_style.addElement(ParagraphProperties(margintop="0.3in", marginbottom="0.15in"))
    doc.styles.addElement(h_style)

    # Define a body text style
    body_style = Style(name="BodyStyle", family="paragraph")
    body_style.addElement(TextProperties(fontsize="12pt"))
    body_style.addElement(ParagraphProperties(margintop="0.05in", marginbottom="0.05in"))
    doc.styles.addElement(body_style)

    # Add heading
    heading = odftext.H(outlinelevel=1, stylename=h_style, text=title)
    doc.text.addElement(heading)

    # Add body paragraphs
    for para_text in body_paragraphs:
        p = odftext.P(stylename=body_style, text=para_text)
        doc.text.addElement(p)

    doc.save(filepath)


def create_master_document(filepath, subdoc_names):
    """Create an ODM master document linking to subdocuments using odfpy."""
    from odf.opendocument import OpenDocumentTextMaster
    from odf import text as odftext
    from odf.namespaces import XLINKNS, TEXTNS

    master = OpenDocumentTextMaster()

    for name in subdoc_names:
        sec_name = name.replace('.odt', '')
        sec = odftext.Section(name=sec_name)
        src = odftext.SectionSource()
        src.setAttrNS(XLINKNS, 'href', f'../{name}')
        src.setAttrNS(XLINKNS, 'type', 'simple')
        src.setAttrNS(TEXTNS, 'filter-name', 'writer8')
        src.setAttrNS(TEXTNS, 'section-name', sec_name)
        sec.addElement(src)
        master.text.addElement(sec)

    master.save(filepath)


def create_initial():
    # Chapter content - realistic anthology content
    chapters = {
        'Ch1.odt': {
            'title': 'Chapter 1: The Dawn of Discovery',
            'paragraphs': [
                'Dr. Elena Vasquez stood at the edge of the observation deck, her breath fogging in the cold morning air. The telescope array stretched before her like a field of metallic sunflowers, each dish tilted toward a different quadrant of the sky.',
                'For seventeen years she had worked at the Atacama Radio Observatory, cataloging signals from distant stars. Most were noise - the cosmic static of hydrogen clouds and spinning pulsars. But three nights ago, something different had appeared in the data.',
                'The signal repeated every 4.7 hours with mathematical precision. Its frequency shifted in patterns that defied natural explanation. Elena had checked and rechecked her instruments, run calibration sequences, and consulted with colleagues in Chile and Japan.',
                'Now she sat in her office, staring at the printout taped to her wall. The pattern was unmistakable: a prime number sequence embedded in the carrier wave.',
            ]
        },
        'Ch2.odt': {
            'title': 'Chapter 2: Echoes Across the Void',
            'paragraphs': [
                'Commander James Okafor reviewed the mission briefing for the third time that morning. The International Space Agency had fast-tracked Project Lighthouse after the Atacama discovery, and his crew of six would be the first to attempt contact.',
                'The ship, christened Meridian, was a marvel of engineering - ion propulsion, rotating habitat ring, and a communications array powerful enough to reach the signal source in the Tau Ceti system.',
                'Lieutenant Sarah Kim ran diagnostics on the navigation computer while Dr. Raj Patel calibrated the medical bay. In the cargo hold, engineer Marco Benedetti secured the last of the supplies.',
                'Okafor floated to the observation port and looked at Earth one final time. The blue marble hung in darkness, impossibly fragile. He thought of his daughter Amara, who had drawn him a picture of the ship with crayons.',
            ]
        },
        'Ch3.odt': {
            'title': 'Chapter 3: The Language of Light',
            'paragraphs': [
                'Dr. Mei-Lin Chen had spent her career studying the mathematics of communication. As the lead linguist aboard Meridian, her task was to decode any messages they might receive.',
                'She had developed what she called the "Rosetta Framework" - a system for finding universal mathematical structures in alien signals. It started with prime numbers and geometric constants, then built upward through increasingly complex concepts.',
                'During the third month of the voyage, the signal changed. The prime sequence gave way to something more complex: a series of mathematical proofs, each building on the last.',
                'Mei-Lin worked around the clock, mapping the new patterns. By the end of the week, she had a breakthrough: the signal was not just mathematics. It was a teaching sequence, designed to build a shared vocabulary between species.',
            ]
        },
        'Ch4.odt': {
            'title': 'Chapter 4: First Contact',
            'paragraphs': [
                'The Tau Ceti system came into view after fourteen months of travel. Three rocky planets orbited the star, and the signal originated from the second - a world slightly larger than Earth with a thick atmosphere of nitrogen and carbon dioxide.',
                'Okafor ordered the ship into orbit while Kim mapped the surface. Vast structures covered the northern continent - geometric patterns visible from space, too regular to be natural formations.',
                'Mei-Lin continued her analysis of the signal, which had grown increasingly complex as they approached. She was now able to identify what appeared to be a greeting protocol.',
                'The crew gathered in the command module as Okafor opened the communications channel. For a long moment, there was only static. Then, a response came - not in radio waves, but in a beam of modulated light that painted patterns across Meridian\'s hull.',
            ]
        },
        'Ch5.odt': {
            'title': 'Chapter 5: The Garden of Minds',
            'paragraphs': [
                'What they found on the planet\'s surface defied every expectation. The structures were not buildings in any conventional sense - they were living networks of crystalline material that pulsed with bioluminescent light.',
                'Dr. Patel took atmospheric readings while Benedetti set up the base camp. The air was breathable with supplemental oxygen, and the temperature was a comfortable eighteen degrees Celsius.',
                'The beings who had sent the signal were not what anyone had imagined. They existed as distributed consciousness across the crystal networks - a single mind spanning an entire continent, yet capable of manifesting localized awareness.',
                'Through Mei-Lin\'s framework, a dialogue began. The entity, which they came to call the Architect, had been broadcasting for over two thousand years, waiting for a species to reach the technological threshold to respond.',
            ]
        },
        'Ch6.odt': {
            'title': 'Chapter 6: The Return',
            'paragraphs': [
                'The journey home took thirteen months. In the cargo hold, sealed in a specially designed containment unit, was a gift from the Architect: a crystal seed that contained a compressed library of knowledge spanning millions of years.',
                'Okafor spent his evenings writing reports, trying to find words adequate to describe what they had experienced. Every draft felt insufficient. How do you explain to humanity that it is not alone in the universe?',
                'Kim maintained the ship\'s systems with quiet efficiency, while Mei-Lin continued her work on the translation framework. Each day she unlocked new layers of meaning in the crystal\'s data.',
                'As Earth grew larger in the viewport, Okafor assembled the crew one last time. They had left as explorers and returned as ambassadors. The world they were returning to would never be the same.',
            ]
        },
    }

    # New subdocuments that should exist on disk but NOT be in the master document
    new_docs = {
        'Preface.odt': {
            'title': 'Preface: A Note from the Editor',
            'paragraphs': [
                'This anthology represents one of the most ambitious collaborative fiction projects undertaken in the twenty-first century. Twelve authors from nine countries contributed their visions of humanity\'s first encounter with extraterrestrial intelligence.',
                'The chapters were written independently, yet a remarkable coherence emerged - perhaps reflecting our shared hopes and anxieties about what lies beyond our small corner of the cosmos.',
                'I wish to thank the contributors for their patience during the editorial process, and the readers for joining us on this journey into the unknown.',
                '-- Dr. Isabelle Moreau, Editor, Geneva, 2025',
            ]
        },
        'Midword.odt': {
            'title': 'Interlude: Reflections at the Halfway Point',
            'paragraphs': [
                'Between departure and arrival lies the vast emptiness of interstellar space. It is here, in the silence between stars, that the crew of Meridian confronted the weight of their mission.',
                'This interlude collects personal journal entries, recorded messages to family, and informal conversations captured during the voyage. They reveal the human dimension of an enterprise often described in purely scientific terms.',
                'What strikes the reader most is the ordinariness of their concerns: birthdays missed, favorite foods craved, the particular quality of sunlight on a spring morning.',
                'These are not heroes in the traditional sense. They are people - brilliant, flawed, homesick, and brave - carried forward by curiosity and the stubborn belief that the universe has something to teach us.',
            ]
        },
        'Afterword.odt': {
            'title': 'Afterword: What Comes Next',
            'paragraphs': [
                'The events described in these chapters are fiction, but the questions they raise are profoundly real. As our instruments grow more sensitive and our reach extends further into space, the probability of detecting signs of intelligent life increases with each passing decade.',
                'The SETI Institute, the Breakthrough Listen project, and numerous academic programs continue to scan the skies. The James Webb Space Telescope has already identified promising biosignatures in the atmospheres of several exoplanets.',
                'When contact comes - and many scientists believe it is a matter of when, not if - we will need more than technology to navigate the encounter. We will need imagination, empathy, and the kind of moral courage displayed by the fictional crew of Meridian.',
                'This anthology is, in its own small way, a preparation for that moment. -- Professor Adrian Holt, Department of Astrobiology, Cambridge University, 2025',
            ]
        },
    }

    # Create chapter files
    for filename, content in chapters.items():
        filepath = os.path.join(WORKDIR, filename)
        create_odt_file(filepath, content['title'], content['paragraphs'])
        print(f'Created: {filepath}')

    # Create new subdocument files (on disk but NOT linked in master)
    for filename, content in new_docs.items():
        filepath = os.path.join(WORKDIR, filename)
        create_odt_file(filepath, content['title'], content['paragraphs'])
        print(f'Created: {filepath}')

    # Create master document with only the 6 chapters
    master_path = os.path.join(WORKDIR, 'Anthology_Master.odm')
    chapter_files = ['Ch1.odt', 'Ch2.odt', 'Ch3.odt', 'Ch4.odt', 'Ch5.odt', 'Ch6.odt']
    create_master_document(master_path, chapter_files)
    print(f'Created master document: {master_path}')

    # Open the master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{master_path}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
