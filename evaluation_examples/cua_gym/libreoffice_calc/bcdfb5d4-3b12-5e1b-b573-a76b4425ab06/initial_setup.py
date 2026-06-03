"""
Initial Setup: Create articles_project folder with .txt article files, open in VSCode
Task ID: osworld_multi_apps_vscode_concat_doc_004
Domain: multi_apps (VSCode + LibreOffice Writer)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_concat_doc_004'
DESKTOP = f'{WORKDIR}/Desktop'
PROJECT_DIR = f'{DESKTOP}/articles_project'


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
    # Create Desktop directory if needed
    os.makedirs(DESKTOP, exist_ok=True)
    # Create articles_project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Article 1: Technology trends
    article1 = """\
The Rise of Artificial Intelligence in Everyday Life

Artificial intelligence has transformed from a futuristic concept into a daily reality for millions
of people worldwide. From virtual assistants like Siri and Alexa to personalized content
recommendations on streaming platforms, AI is quietly reshaping how we interact with technology.

Machine learning algorithms now power fraud detection systems at major banks, helping identify
suspicious transactions within milliseconds. Healthcare providers are using AI-driven diagnostic
tools to detect early signs of diseases such as cancer with greater accuracy than traditional
methods allow.

The integration of AI in transportation is also accelerating. Autonomous vehicle technology
continues to advance, with companies conducting extensive trials on public roads. Meanwhile,
smart traffic management systems in cities like Singapore and Barcelona are reducing congestion
and lowering emissions through real-time data analysis.

As AI becomes more pervasive, discussions around ethics, privacy, and job displacement are
intensifying. Policymakers, technologists, and civil society groups are working together to
establish frameworks that ensure AI development benefits humanity as a whole.
"""

    # Article 2: Climate change and renewable energy
    article2 = """\
Renewable Energy: Powering a Sustainable Future

The global push toward renewable energy has gained unprecedented momentum over the past decade.
Solar panel installations have surged by over 400 percent since 2015, driven by falling costs
and supportive government policies across Europe, Asia, and the Americas.

Wind energy has emerged as one of the fastest-growing power sources globally. Offshore wind
farms off the coasts of Denmark, the United Kingdom, and China are generating electricity for
millions of households. Advances in turbine design have increased efficiency while reducing
maintenance costs.

Battery storage technology is addressing one of renewable energy's greatest challenges:
intermittency. Next-generation lithium-ion and solid-state batteries can now store surplus
energy from solar and wind installations for use during peak demand periods or cloudy,
calm weather conditions.

Developing nations are leapfrogging traditional fossil fuel infrastructure entirely, adopting
distributed solar microgrids to electrify rural communities that were previously off the grid.
This transition is not only reducing carbon emissions but also improving quality of life and
stimulating local economies.
"""

    # Article 3: Space exploration
    article3 = """\
The New Space Race: Private Companies and the Final Frontier

The 21st century has witnessed a dramatic shift in space exploration, with private companies
now playing a central role alongside government agencies. SpaceX, founded by Elon Musk in
2002, revolutionized the industry by developing reusable rocket technology that drastically
cut launch costs.

Blue Origin, founded by Amazon's Jeff Bezos, has focused on developing heavy-lift rockets
and reusable spacecraft designed for lunar exploration. Their New Glenn rocket completed its
first successful orbital mission, marking a significant milestone in commercial space access.

NASA's Artemis program aims to return humans to the Moon by the mid-2020s, with plans to
establish a sustainable lunar presence as a stepping stone for eventual Mars missions. The
program relies heavily on partnerships with commercial partners for rocket propulsion, life
support systems, and lunar landers.

Beyond the Moon, Mars remains the ultimate goal for many space enthusiasts and scientists.
Robotic missions have already mapped the Martian surface extensively, identified subsurface
water ice, and detected organic molecules. The findings lay the groundwork for eventual
human missions that could revolutionize our understanding of planetary science and life's
potential beyond Earth.
"""

    # Article 4: Digital health innovations
    article4 = """\
Digital Health: Transforming Patient Care in the 21st Century

The digital revolution is fundamentally changing how healthcare is delivered and experienced.
Telemedicine platforms experienced explosive growth during the COVID-19 pandemic and have
since become a standard component of healthcare delivery in many countries.

Wearable devices such as smartwatches and fitness trackers now monitor heart rate, blood
oxygen levels, sleep patterns, and even detect atrial fibrillation. This continuous stream
of health data is empowering individuals to take proactive steps in managing their wellbeing
and enabling physicians to monitor patients remotely.

Electronic health records have streamlined clinical workflows and improved care coordination
across providers. When a patient visits multiple specialists, their complete medical history
is accessible instantly, reducing duplicate testing and minimizing medication errors.

Genomic medicine is another frontier being transformed by digital technology. Advanced
sequencing tools and AI-powered analysis platforms are making personalized medicine a
reality, allowing treatments to be tailored to individual genetic profiles. This precision
approach is particularly promising in oncology, where targeted therapies have shown
significantly improved outcomes compared to conventional chemotherapy.
"""

    # Article 5: Urban development and smart cities
    article5 = """\
Smart Cities: Building Urban Environments for the Future

Urban populations are expected to reach 6.7 billion by 2050, placing enormous pressure on
city infrastructure, services, and resources. Smart city initiatives are emerging as a
critical strategy for managing this growth while improving quality of life for residents.

Sensor networks embedded throughout urban environments collect real-time data on traffic
flow, air quality, energy consumption, and waste management. City administrators use this
information to optimize services dynamically and plan future infrastructure investments
more effectively.

Barcelona's Superblock initiative has transformed city blocks by restricting through
traffic, reclaiming streets for pedestrians and cyclists, and creating green spaces.
The project has reduced noise pollution by 30 percent and particulate matter by 25 percent
in participating neighborhoods.

Singapore has emerged as a global leader in smart city development, implementing
integrated systems for housing, transportation, healthcare, and public safety. Their
Virtual Singapore 3D platform allows city planners to model and test urban interventions
before implementation, saving time and resources while minimizing disruption to residents.
"""

    # Write all article files
    articles = {
        'article1_ai_everyday.txt': article1,
        'article2_renewable_energy.txt': article2,
        'article3_space_exploration.txt': article3,
        'article4_digital_health.txt': article4,
        'article5_smart_cities.txt': article5,
    }

    for filename, content in articles.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    # Make sure articles_combined.docx does NOT exist in Desktop (negative constraint)
    combined_path = os.path.join(DESKTOP, 'articles_combined.docx')
    if os.path.exists(combined_path):
        os.remove(combined_path)
        print(f'Removed pre-existing: {combined_path}')

    print(f'Initial project folder created: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the articles_project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with articles_project folder (DISPLAY=:0)')


create_initial()
