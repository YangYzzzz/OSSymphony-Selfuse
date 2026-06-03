"""
Initial Setup: Compile memoir chapters into EPUB using Chrome-researched tool
Task ID: osworld_multi_apps_misc_073
Domain: multi_apps (OS + Chrome)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_073'
MEMOIR_DIR = '/home/user/Documents/Memoir/A_Life_Lived'


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
    # Create the memoir directory structure
    os.makedirs(MEMOIR_DIR, exist_ok=True)

    # --- prologue.txt ---
    prologue_content = """A Life Lived
Prologue

My mother used to say that a life without stories is a life half-lived. I never understood what she meant until the day I found her old journals tucked beneath the floorboards of our childhood home in Asheville, North Carolina. The journals — seven of them, bound in cracked leather and smelling faintly of cedar — contained stories I had never heard, of a woman I thought I knew entirely.

This memoir is my attempt to reconcile the mother I remembered with the woman she truly was. It is a story of immigration and identity, of secrets kept out of love, and of the long road toward understanding that begins only when we are finally willing to listen.

My name is Eleanor Marsh, and I have lived eighty-two years on this earth. I have buried a husband, raised three children, and worked as a schoolteacher for thirty-seven years. I have laughed more than I have wept, though not by as wide a margin as I once believed. And I have spent the last decade trying to put words to a life that, even now, surprises me with its twists and unexpected grace.

These pages are for my grandchildren, who know me only as the woman who bakes apple pie on Sundays and insists on watching the evening news without interruption. They deserve to know the rest.
"""

    # --- chapter_01.txt ---
    chapter_01_content = """Chapter One: The House on Magnolia Street

I was born in the summer of 1942, in a narrow white house on Magnolia Street in Asheville. The house had a green tin roof that sang in the rain and a front porch wide enough to hold the entire neighborhood on warm evenings, which it often did.

My father, Raymond Holloway, worked at the textile mill on the edge of town. He was a quiet man of medium build, with hands that could fix almost anything and a laugh that erupted suddenly, like a car backfiring. My mother, Ida — born Ida Vasquez in Guadalajara, Mexico — had come north with her own mother in 1935, following a cousin who had already established herself in the laundry business. Ida had married Raymond within a year of arriving, a fact that my grandmother never fully forgave, though she loved Raymond in her way.

The neighborhood was a patchwork of mill workers, small shopkeepers, and one retired schoolteacher named Mr. Pickett who kept bees and gave honey to anyone who would listen to his theories about the Civil War. We children ranged freely across the block from morning until the streetlights came on, and in those years before air conditioning, the whole street seemed to breathe together — screen doors banging, radios playing through open windows, the smell of supper drifting over the hedgerows.

I was the second of four children. My older brother, James, was the serious one, always with a book in hand. My younger sister, Vera, arrived when I was five, all lungs and determination. And then there was Thomas, born when I was nine, whose easy smile could defuse any argument and who grew up to become an electrician in Charlotte.

We were, by the standards of the time and place, ordinary. And for a long while, I was proud of that ordinariness. It felt like stability, like bedrock. I did not yet understand how much was hidden beneath.
"""

    # --- chapter_02.txt ---
    chapter_02_content = """Chapter Two: Learning and Leaving

The woman who changed my life was named Margaret Tilson, and she taught seventh-grade English at Vance Junior High School. She was tall, angular, and possessed of an alarming directness that terrified most of her students. She terrified me too, but I also wanted, desperately, to impress her.

It was Mrs. Tilson who told me, one afternoon in 1955 when I was thirteen, that I wrote with unusual clarity for my age and that I should consider it seriously. "Clarity is a form of courage," she said, handing back my essay on the causes of World War Two with a large A at the top and seven corrections in red ink beneath it. I did not know, then, that this was the highest praise she gave. I kept that essay for forty years.

High school was the era of Elvis and bobby socks and the particular anguish of being neither fully child nor adult. I edited the school newspaper for two years, wrote a column called "Plain Talk" that got me into mild trouble twice for opinions deemed unbecoming, and fell in and out of love with a boy named David Merritt who later became a dentist in Knoxville. I was accepted to the University of North Carolina at Chapel Hill in the spring of 1960, the first in my family to attend a four-year college.

The day I left for Chapel Hill, my mother walked me to the Greyhound station carrying a paper bag with two ham sandwiches and a boiled egg. At the bus, she held my face in her hands and said, in Spanish, which she used only when she meant something with her whole self: "Remember where you come from. And then go wherever you must."

I have turned those words over in my mind for sixty years.
"""

    # --- chapter_03.txt ---
    chapter_03_content = """Chapter Three: Marriage, Teaching, and the Years That Blur

I met Gordon Marsh at a faculty mixer in September of 1966. I was twenty-four, newly hired to teach third grade at Brewer Elementary School, and wearing a blue dress I had bought specifically for the occasion. Gordon was thirty-one, a history teacher at the high school, divorced once and careful about it, with dark eyes and a habit of listening that I had not often encountered in men.

We married in June of 1967 in a small ceremony at St. Luke's Episcopal Church. My mother wore lavender and cried continuously from the processional to the final photograph. My father shook Gordon's hand for a very long time without saying anything, which was his way of expressing approval.

The years that followed were, in the way of most good lives, simultaneously ordinary and irreplaceable. We rented a house on Spruce Street, then bought a small one on Walnut. Gordon coached track in the afternoons and wrote a local history column for the newspaper on weekends. I taught third grade, then fourth, then looped back to third again. We had three children in seven years: David in 1969, Caroline in 1971, and Robert in 1976.

There were bad stretches — the year Gordon lost his father and went quiet for months; the miscarriage between Caroline and Robert that we never spoke of at the time and should have; the decade when money was consistently too tight and we both worked second jobs without complaining out loud about it. But there were also the beach vacations in Wrightsville Beach, the tomato garden that produced more than we could ever eat, the Sunday mornings with coffee and the newspaper that remain, even now, among the most vivid memories I carry.

I did not know, until I was in my late forties, that my mother had kept journals for most of her adult life. I did not know what was in them. I was not yet ready to find out.
"""

    # --- epilogue.txt ---
    epilogue_content = """Epilogue: What the Journals Said

My mother died in 1998, at eighty-three, in the same house on Magnolia Street where she had raised four children. Gordon and I drove up from Asheville for the last weeks, and I sat with her through many of those nights, holding her hand and listening to her breathe. She did not say much at the end. She had never been a woman who believed in unnecessary speech.

It was the following spring, during the clearing of the house, that I found the journals. They were wrapped in brown paper and tied with kitchen string, and they were under the floorboards in her bedroom, beneath a loose plank I had never noticed in all my years of living there.

I brought them home and did not open them for three months.

What I found, when I finally did, was a woman both familiar and utterly surprising. My mother had written in a mixture of Spanish and English, switching between languages depending, it seemed, on which offered her the better word. She wrote about leaving Mexico with a grief so precise it made me catch my breath. She wrote about my father — with love, yes, but also with a candor about his limitations that she had never permitted herself aloud. She wrote about us children with a tenderness so fierce it felt almost painful to read.

And she wrote about herself — her own desires, regrets, and private convictions — with the freedom that comes only when you believe no one will ever read your words.

I am finishing this memoir in my eighty-second year, in a house full of grandchildren's drawings and the smell of coffee and the noise of a life that has been, by any measure, more than I deserved. I am not a woman who arrived at wisdom gracefully. I resisted understanding at every available turn and required decades to learn what perhaps should have been obvious.

But I learned it. And I write it down now — for David and Caroline and Robert, for the grandchildren who know me mainly as the woman on the porch, for whoever might one day want to know what one ordinary life contained — because my mother was right.

A life without stories is a life half-lived.

And this one is fully, wholly, stubbornly mine.
"""

    # Write all the text files
    files_content = {
        'prologue.txt': prologue_content,
        'chapter_01.txt': chapter_01_content,
        'chapter_02.txt': chapter_02_content,
        'chapter_03.txt': chapter_03_content,
        'epilogue.txt': epilogue_content,
    }

    for filename, content in files_content.items():
        filepath = os.path.join(MEMOIR_DIR, filename)
        Path(filepath).write_text(content, encoding='utf-8')
        print(f'Created: {filepath}')

    print(f'\nAll memoir text files created in: {MEMOIR_DIR}')
    print('Directory contents:')
    for f in sorted(os.listdir(MEMOIR_DIR)):
        print(f'  {f}')

    # GUI-ready startup
    # 1. Open Chrome with GitHub tabs showing epub creation utilities
    launch_gui(
        'google-chrome --new-window '
        '"https://github.com/aerkalov/ebooklib" '
        '"https://github.com/yihong0618/bilingual_book_maker" '
        '"https://github.com/pandoc/pandoc"',
        delay_sec=3.0
    )

    # 2. Open Nautilus file manager showing the memoir directory
    launch_gui(f'nautilus "{MEMOIR_DIR}"', delay_sec=1.5)

    print('GUI_READY: launched Chrome with GitHub epub tabs and Nautilus file manager with DISPLAY=:0')


create_initial()
