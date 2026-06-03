"""
Initial Setup: Create travel essay txt files and open Chrome with conversion tool docs
Task ID: osworld_multi_apps_misc_074
Domain: os / multi_apps
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_074'
ESSAYS_DIR = f'{WORKDIR}/Documents/Essays/Travel_Chronicles'


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
    # Create directory structure
    os.makedirs(ESSAYS_DIR, exist_ok=True)

    # Create realistic travel essay txt files
    rome_content = """Rome: The Eternal City

The morning light filtered through the shutters of my tiny apartment near the Trastevere neighborhood, casting long golden rays across the worn terracotta tiles. I had arrived in Rome three days earlier, still jet-lagged and overwhelmed by the sheer density of history embedded in every cobblestone.

My first morning walk took me past the Pantheon, its massive dome rising impossibly above the narrow medieval streets surrounding it. Built nearly two thousand years ago, it remains the best-preserved ancient building in Rome — a testament to Roman engineering that would not be matched for centuries. I stood in the square outside, coffee in hand, watching tourists from a dozen countries photograph its columned facade, each trying to capture something that simply cannot be reduced to a single image.

The food markets near Campo de' Fiori offered a sensory explosion: crimson tomatoes stacked in pyramids, glossy purple eggplants, artichokes with their layered armor, and fresh pasta in shapes I had never seen back home. An elderly vendor pressed a small piece of aged pecorino into my hand without asking — a gift, I realized, and an invitation to linger.

I spent an afternoon in the Borghese Gallery, restricted to timed entry to protect the masterworks inside. Bernini's sculptures stopped me cold. The marble of Daphne's fingers, transforming into laurel leaves as Apollo grasps her, seemed to breathe. No photograph I had seen prepared me for the actual experience of standing a meter away from something so impossibly alive.

On my last evening, I walked the length of the old Appian Way as dusk settled over the Roman countryside. The original basalt paving stones, worn smooth by two millennia of feet and wheels, clicked under my shoes as the cypresses turned black against a violet sky. Rome is not merely a city; it is a palimpsest — layer upon layer of human ambition, beauty, and failure, compressed into a living place.
"""

    tokyo_content = """Tokyo: Infinite City

There is a particular quality of light in Tokyo at six in the morning that I have not encountered anywhere else — a pale, diffuse glow that seems to emerge from the city itself rather than from the sky above. I discovered this standing outside a 7-Eleven in Shimokitazawa, clutching a steaming can of canned coffee, watching the neighborhood wake up with quiet efficiency.

Tokyo operates on a frequency that initially seems overwhelming but gradually reveals itself as deeply ordered. The trains run with a precision that makes European rail networks seem amateurish — delays of more than a minute are announced apologetically over the intercom. The subway map, with its web of colored lines, looked impenetrable on the first day and felt intuitive by the third.

The Tsukiji outer market, even years after the main wholesale operations moved to Toyosu, remains a revelation. Vendors have been perfecting their specialties for generations — one stall selling only tamagoyaki, the rolled egg omelet, has been operated by the same family for four decades. I ate three different versions in a single morning and could detect distinct differences in sweetness, texture, and technique.

In the evening, I took the train to Yanaka, one of the few Tokyo neighborhoods that survived both the 1923 earthquake and the Second World War essentially intact. Walking its narrow lanes felt like passing through a gap in time — wooden houses with sliding paper screens, small temples tucked between the buildings, a cemetery populated by the city's ancestors. Yet the sounds of the present were never far: a delivery truck navigating the narrow alley, a television murmuring inside a house, children calling to each other.

The contradiction at the heart of Tokyo is that a city of fourteen million people can feel both relentlessly urban and deeply intimate simultaneously. The izakaya where I ate my last meal had six seats at the counter. The chef prepared each dish with the same careful attention he would give a meal for twelve. This refusal to compromise based on scale may be the most Japanese thing I encountered.
"""

    nyc_content = """New York City: The Perpetual Present

New York City exists only in the present tense. Unlike Rome, which is perpetually haunted by its past, or Tokyo, which maintains a careful negotiation between continuity and transformation, New York seems constitutionally incapable of nostalgia. Buildings that stood for a century are demolished in a weekend. Neighborhoods that defined an era are remade within a decade. The city's energy comes precisely from this refusal to preserve.

I arrived at JFK on a Tuesday morning in October, when the city was at its most seductive — cool air, sharp light, the trees in Central Park turning gold and amber. By the time I reached Manhattan by AirTrain and subway, the sensory overload had already begun: the particular smell of the subway, warm and metallic; the percussion of construction on every other block; the simultaneous conversations in what seemed like a dozen languages.

The High Line, the elevated park built on a former freight rail line through the West Side, offered an unusual perspective on the city's layers. Walking above the street, I could see into the upper floors of Chelsea galleries, over the rooftops of the Meatpacking District, across to New Jersey and the Hudson. The park itself has become a symbol of a certain kind of urban transformation — adaptive reuse, the conversion of industrial infrastructure into public space — that has made it both celebrated and criticized.

I spent a long afternoon in the New York Public Library on Fifth Avenue, sitting in the Rose Main Reading Room beneath its ornate ceiling. The room, restored to its 1911 condition, was full of people working on laptops, reading newspapers, filling out forms. The coexistence of Beaux-Arts grandeur and everyday practicality seemed to me essentially New York: monumental ambition deployed in service of the ordinary.

The city reveals itself differently at different hours. At midnight in the East Village, the streets were as busy as a Tuesday afternoon in any other city. At four in the morning, walking back from a late concert in Brooklyn, I found the streets emptied except for delivery trucks and the occasional insomniac. For a moment, the city felt navigable, even intimate. Then the first subway train of the morning rumbled past, and the perpetual present reasserted itself.
"""

    cape_town_content = """Cape Town: Mountains and Ocean

Cape Town is the only city I have visited where the landscape consistently overwhelms the human-built environment. This is not to diminish the city's considerable architectural and cultural achievements — it is to acknowledge that Table Mountain, with its flat summit and sheer faces, and the two oceans converging at the Cape of Good Hope, create a context that simply cannot be ignored or backgrounded.

I arrived in late January, the height of the Southern Hemisphere summer, when the southeasterly wind known as the Cape Doctor blows with a frequency and force that clears the air of everything and sends tablecloths and umbrellas airborne in outdoor cafes. The mountain behind the city was visible from everywhere, its distinctive profile serving as a constant compass point.

The Bo-Kaap neighborhood, with its brightly painted houses on the slopes above the central city, told a compressed version of Cape Town's layered history. The neighborhood was originally settled by enslaved people and free Muslims brought from Southeast Asia, Indonesia, and elsewhere in the Indian Ocean world during the seventeenth and eighteenth centuries. Their descendants created a distinct Cape Malay culture, its architecture and cuisine inseparable from the history of forced migration and gradual liberation.

I spent a day on the Cape Peninsula, driving the coastal road south past Hout Bay to the Cape Point Nature Reserve. The landscape shifted from suburban to wild within twenty minutes — fynbos scrubland, rocky beaches, the cold Atlantic crashing against headlands. At the reserve's southwestern tip, I stood at the continent's edge and watched a colony of African penguins waddling through the heath, absurdly out of place and entirely at home.

The Boulders Beach penguin colony, a few kilometers north on the False Bay side of the peninsula, offered a different kind of encounter: African penguins nesting among granite boulders while tourists photographed them from designated boardwalks. The penguins appeared entirely indifferent to the attention. I found this indifference — the simple confidence of animals that belong exactly where they are — more moving than I expected.

Cape Town's contradictions are not subtle. Extraordinary natural beauty exists in proximity to some of the most severe inequality on Earth. The informal settlements visible from the highway into the city center, home to hundreds of thousands, exist in direct sight of the wine farms and beach houses of the southern suburbs. To visit Cape Town honestly requires holding these contradictions without resolving them.
"""

    # Write essay files
    Path(os.path.join(ESSAYS_DIR, 'rome.txt')).write_text(rome_content, encoding='utf-8')
    Path(os.path.join(ESSAYS_DIR, 'tokyo.txt')).write_text(tokyo_content, encoding='utf-8')
    Path(os.path.join(ESSAYS_DIR, 'nyc.txt')).write_text(nyc_content, encoding='utf-8')
    Path(os.path.join(ESSAYS_DIR, 'cape_town.txt')).write_text(cape_town_content, encoding='utf-8')

    print(f'Created directory: {ESSAYS_DIR}')
    print(f'Created: rome.txt, tokyo.txt, nyc.txt, cape_town.txt')

    # Verify files exist
    for fname in ['rome.txt', 'tokyo.txt', 'nyc.txt', 'cape_town.txt']:
        fpath = os.path.join(ESSAYS_DIR, fname)
        assert os.path.isfile(fpath), f'Missing: {fpath}'
        print(f'  OK: {fname} ({os.path.getsize(fpath)} bytes)')

    # ---- GUI-ready startup ----
    # 1. Open Nautilus file manager showing the Travel_Chronicles folder
    launch_gui(f'nautilus "{ESSAYS_DIR}"', delay_sec=2.0)

    # 2. Open Chrome with tabs showing EPUB conversion tool documentation
    # Calibre is a well-known ebook conversion tool available on Linux
    # Also show pandoc documentation as an alternative
    launch_gui(
        'google-chrome '
        '"https://calibre-ebook.com/download_linux" '
        '"https://pandoc.org/MANUAL.html#epub-extensions" '
        '"https://manual.calibre-ebook.com/generated/en/ebook-convert.html"',
        delay_sec=3.0,
    )

    print('GUI_READY: launched Nautilus and Chrome with DISPLAY=:0')


create_initial()
