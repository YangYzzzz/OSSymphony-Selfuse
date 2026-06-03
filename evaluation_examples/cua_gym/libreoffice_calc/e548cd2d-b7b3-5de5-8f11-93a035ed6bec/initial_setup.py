"""
Initial Setup: Save all open Chrome tabs as PDFs into /home/user/Documents/News-Archive
Task ID: osworld_multi_apps_bulk_pdf_save_004
Domain: chrome + os (multi-apps)

Creates:
  - 4 HTML news article files in /home/user/Documents/news_articles/
  - Empty /home/user/Documents/News-Archive directory
  - Launches Chrome with those 4 tabs open
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_004'
NEWS_DIR = f'{WORKDIR}/Documents/news_articles'
ARCHIVE_DIR = f'{WORKDIR}/Documents/News-Archive'

# Four realistic news article titles and content
ARTICLES = [
    {
        "title": "Global Climate Summit Reaches Historic Carbon Agreement",
        "filename": "article_climate.html",
        "outlet": "The Global Tribune",
        "author": "Amelia Hartwell",
        "date": "March 4, 2026",
        "content": """
        <p>World leaders gathering in Geneva have signed a landmark accord pledging to cut carbon
        emissions by 55 percent before 2035, marking the most ambitious climate commitment in history.
        The agreement, brokered after three days of intense negotiations, brings together 192 nations
        under a unified framework that includes binding targets and independent verification mechanisms.</p>
        <p>European Commission President Helena Voss called the accord "a turning point for civilization,"
        while US Climate Envoy James Rutherford said the deal was the product of years of scientific
        cooperation and diplomatic persistence. China, the world's largest emitter, agreed to peak its
        emissions by 2028 and achieve carbon neutrality by 2045.</p>
        <p>The accord includes a $400 billion global fund to help developing nations transition to
        renewable energy, a provision championed by the African Union and Pacific island states, who
        argued that wealthier countries bear the greatest historical responsibility for current atmospheric
        CO2 levels.</p>
        """
    },
    {
        "title": "Breakthrough in Quantum Computing Promises Faster Drug Discovery",
        "filename": "article_quantum.html",
        "outlet": "Science & Technology Daily",
        "author": "Dr. Rachel Kim",
        "date": "March 3, 2026",
        "content": """
        <p>Researchers at the Massachusetts Institute of Technology have demonstrated a 1,000-qubit
        quantum processor capable of simulating protein folding at molecular precision, a development
        that experts say could compress pharmaceutical research timelines from decades to years.</p>
        <p>The processor, named Helios-Q, achieved what the team describes as "fault-tolerant quantum
        supremacy" on a benchmark drug-target simulation — outperforming the world's most powerful
        classical supercomputer by a factor of 10 million on the specific task.</p>
        <p>"This changes the economics of drug discovery entirely," said lead researcher Professor
        Yuki Tanaka. "We can now model drug-receptor interactions with full quantum accuracy in hours
        instead of months." The team's findings were published in the journal Nature Quantum today.</p>
        <p>Major pharmaceutical companies including Novagen and BioSphere have already announced
        research partnerships to apply the technology to cancer therapeutics and antibiotic-resistant
        bacterial infections.</p>
        """
    },
    {
        "title": "Coastal Cities Adapt as Sea Level Rise Accelerates Along US East Seaboard",
        "filename": "article_sealevel.html",
        "outlet": "National Geographic News",
        "author": "Marcus Webb",
        "date": "March 2, 2026",
        "content": """
        <p>Satellite data released by NASA this week confirms that sea levels along the US Atlantic
        coast are rising at roughly twice the global average rate, with some areas around Miami,
        Norfolk, and New York experiencing annual increases exceeding 10 millimeters per year.</p>
        <p>In response, a coalition of twelve coastal municipalities has launched the Eastern Seaboard
        Resilience Initiative, a $28 billion investment program spanning managed coastal retreats,
        elevated roadways, living shoreline projects, and redesigned stormwater infrastructure.</p>
        <p>Norfolk, Virginia, long used as a case study for coastal flooding challenges, has already
        relocated more than 800 families from its lowest-lying neighborhoods under a voluntary buyout
        program that began in 2023. City planners say the approach has reduced emergency flood response
        costs by 40 percent compared to 2019 baseline levels.</p>
        <p>Scientists warn that without significant reductions in greenhouse gas emissions, many of
        the adaptation measures now underway will only delay the inevitable need for larger-scale
        managed retreats by the middle of the century.</p>
        """
    },
    {
        "title": "Remote Work Reshapes Urban Real Estate Markets Across North America",
        "filename": "article_remotework.html",
        "outlet": "Financial Review Weekly",
        "author": "Sandra Okonkwo",
        "date": "March 1, 2026",
        "content": """
        <p>A comprehensive new report from the Urban Land Institute reveals that sustained remote and
        hybrid work trends have fundamentally altered commercial and residential real estate patterns
        across North American cities, with downtown office vacancy rates averaging 22 percent nationally
        even as suburban and mid-size city residential markets experience unprecedented demand.</p>
        <p>Cities like Austin, Raleigh, and Boise have seen population growth rates three to five times
        the national average over the past five years, driven largely by workers who can now perform
        their jobs from anywhere with a reliable internet connection. Meanwhile, office landlords in
        San Francisco, Chicago, and Toronto are converting vacant towers to mixed residential use
        at an accelerating pace.</p>
        <p>"The 9-to-5 commute model served the industrial era, but knowledge workers have effectively
        voted with their feet," said ULI chief economist Patricia Sheldon. "We're witnessing the
        most rapid restructuring of urban geography since the post-war suburban boom."</p>
        <p>The report notes that transit ridership in major hubs remains 30 to 45 percent below
        pre-pandemic peaks, putting pressure on city budgets that historically relied on fare revenue
        and dense commercial property tax bases.</p>
        """
    },
]


def create_html_articles():
    """Create HTML files for 4 news articles in NEWS_DIR."""
    os.makedirs(NEWS_DIR, exist_ok=True)
    for article in ARTICLES:
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <style>
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #1a1a1a;
            line-height: 1.7;
            background: #ffffff;
        }}
        .outlet {{
            font-family: Arial, sans-serif;
            font-size: 13px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #c0392b;
            margin-bottom: 8px;
        }}
        h1 {{
            font-size: 2em;
            font-weight: bold;
            margin: 0 0 12px 0;
            line-height: 1.2;
        }}
        .byline {{
            font-family: Arial, sans-serif;
            font-size: 13px;
            color: #666;
            margin-bottom: 24px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 12px;
        }}
        p {{
            margin-bottom: 18px;
        }}
    </style>
</head>
<body>
    <div class="outlet">{article['outlet']}</div>
    <h1>{article['title']}</h1>
    <div class="byline">By {article['author']} &bull; {article['date']}</div>
    {article['content']}
</body>
</html>"""
        filepath = os.path.join(NEWS_DIR, article['filename'])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Created: {filepath}")


def create_archive_dir():
    """Create empty News-Archive directory."""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    # Ensure it is empty
    for item in os.listdir(ARCHIVE_DIR):
        item_path = os.path.join(ARCHIVE_DIR, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
    print(f"Archive directory ready (empty): {ARCHIVE_DIR}")


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


def launch_chrome_with_tabs():
    """Kill any existing Chrome, then launch with 4 news article tabs."""
    # Kill existing Chrome instances
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(2)

    # Build file:// URLs for each article
    tab_urls = [
        f"file://{NEWS_DIR}/{article['filename']}"
        for article in ARTICLES
    ]

    # Launch Chrome with remote debugging port and all tabs
    tabs_arg = ' '.join(f'"{url}"' for url in tab_urls)
    chrome_cmd = (
        f'google-chrome --remote-debugging-port=1337 '
        f'--no-first-run --no-default-browser-check '
        f'{tabs_arg}'
    )
    launch_gui(chrome_cmd, delay_sec=3.0)

    # Start socat bridge so CDP is accessible on port 9222
    subprocess.Popen(
        shlex.split('socat tcp-listen:9222,fork tcp:localhost:1337'),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.0)
    print('GUI_READY: Chrome launched with 4 news article tabs and CDP bridge on port 9222')


def main():
    create_html_articles()
    create_archive_dir()
    launch_chrome_with_tabs()
    print(f'Initial setup complete.')
    print(f'  News articles: {NEWS_DIR}')
    print(f'  Archive dir (empty): {ARCHIVE_DIR}')
    print(f'  Chrome tabs: {len(ARTICLES)} articles open')


main()
