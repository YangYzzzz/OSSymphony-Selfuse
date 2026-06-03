"""
Initial Setup: Chrome open with 3 financial article tabs; Research directory exists (empty)
Task ID: osworld_multi_apps_bulk_pdf_save_003
Domain: chrome + os (multi-app)

Initial state:
  - /home/user/Documents/Finance/Research/ exists (no PDFs)
  - 3 HTML financial article files in /home/user/Documents/Finance/
  - Chrome opened with 3 tabs loading those articles
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
FINANCE_DIR = '/home/user/Documents/Finance'
RESEARCH_DIR = '/home/user/Documents/Finance/Research'

# The 3 article page titles (Chrome will use the <title> tag as the page title)
ARTICLES = [
    {
        "filename": "article_buffett_principles.html",
        "title": "Warren Buffett's Top Investment Principles for 2025",
        "content": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Warren Buffett's Top Investment Principles for 2025</title>
</head>
<body>
<h1>Warren Buffett's Top Investment Principles for 2025</h1>
<p>By Financial Times Staff | March 4, 2025</p>
<p>
Warren Buffett, the legendary chairman and CEO of Berkshire Hathaway, has long been regarded
as one of the greatest investors of all time. His approach to value investing has generated
extraordinary returns over more than six decades. Here are his most important investment
principles for navigating markets in 2025.
</p>
<h2>1. Invest in What You Understand</h2>
<p>
Buffett has always emphasized the importance of staying within your "circle of competence."
Only invest in businesses whose products, services, and economics you can clearly understand.
This reduces the risk of making costly mistakes based on misunderstanding.
</p>
<h2>2. Focus on Long-Term Value</h2>
<p>
Buffett famously said, "Our favorite holding period is forever." Rather than chasing
short-term price movements, he looks for companies with durable competitive advantages
that will compound value over decades.
</p>
<h2>3. Be Fearful When Others Are Greedy</h2>
<p>
Market sentiment often drives prices far away from intrinsic value. Buffett's contrarian
approach means buying during periods of widespread pessimism and being cautious when
euphoria grips the market.
</p>
<h2>4. Margin of Safety</h2>
<p>
Always pay significantly less than a business is worth. This principle, borrowed from
Benjamin Graham, provides a buffer against errors in analysis and unexpected adversity.
</p>
<h2>5. Quality Over Price</h2>
<p>
"It's far better to buy a wonderful company at a fair price than a fair company at a
wonderful price." Buffett evolved from Graham's strict value approach to prioritize
business quality, exemplified by investments like Coca-Cola and Apple.
</p>
<footer>
<p>© 2025 Financial Times. All rights reserved.</p>
</footer>
</body>
</html>
"""
    },
    {
        "filename": "article_bond_yields.html",
        "title": "Understanding Bond Yields and Market Volatility",
        "content": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Understanding Bond Yields and Market Volatility</title>
</head>
<body>
<h1>Understanding Bond Yields and Market Volatility</h1>
<p>By Investors Daily | February 28, 2025</p>
<p>
The relationship between bond yields and equity market volatility is one of the most
important dynamics for modern investors to understand. As central banks navigate
post-pandemic monetary policy, these relationships have become increasingly complex.
</p>
<h2>What Are Bond Yields?</h2>
<p>
A bond yield represents the return an investor receives from holding a bond until maturity.
The 10-year U.S. Treasury yield is widely considered the benchmark risk-free rate, serving
as a reference point for pricing virtually all other financial assets.
</p>
<h2>The Yield Curve and Its Signals</h2>
<p>
When short-term yields rise above long-term yields, the yield curve "inverts." Historically,
this has preceded recessions with a 12-to-18 month lag. In 2024, the curve began re-steepening,
signaling a potential normalization of monetary conditions.
</p>
<h2>Bond Yields and Stock Valuations</h2>
<p>
Higher bond yields increase the discount rate used in stock valuation models, which reduces
the present value of future earnings. This is why technology stocks — which derive most of
their value from distant future cash flows — are particularly sensitive to yield movements.
</p>
<h2>Managing Volatility in Your Portfolio</h2>
<p>
Investors can manage yield-driven volatility by maintaining a mix of short and long-duration
bonds, using Treasury Inflation-Protected Securities (TIPS), and considering alternative
assets that have historically low correlation with interest rate movements.
</p>
<h2>Current Outlook for 2025</h2>
<p>
With the Federal Reserve holding rates steady at 4.25-4.50%, markets are pricing in 2-3
potential cuts through 2025. This creates a nuanced environment where bond duration risk
is modest but equity valuations remain elevated relative to historical norms.
</p>
<footer>
<p>© 2025 Investors Daily. All rights reserved.</p>
</footer>
</body>
</html>
"""
    },
    {
        "filename": "article_diversification.html",
        "title": "Diversification Strategies for Long-Term Wealth Building",
        "content": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Diversification Strategies for Long-Term Wealth Building</title>
</head>
<body>
<h1>Diversification Strategies for Long-Term Wealth Building</h1>
<p>By Wealth Management Review | March 1, 2025</p>
<p>
Diversification is the only "free lunch" in investing — a way to reduce risk without
necessarily sacrificing returns. As markets become more interconnected, building a
truly diversified portfolio requires thinking beyond traditional asset classes.
</p>
<h2>Core Principles of Diversification</h2>
<p>
Effective diversification means spreading investments across assets that don't move
together. When one asset falls, others may rise or remain stable, smoothing out the
overall portfolio performance over time.
</p>
<h2>Geographic Diversification</h2>
<p>
U.S. stocks represent roughly 60% of global market capitalization. Allocating to
international developed markets (Europe, Japan, Australia) and emerging markets
(India, Brazil, Southeast Asia) reduces concentration risk and captures different
growth cycles.
</p>
<h2>Asset Class Diversification</h2>
<p>
A well-diversified portfolio typically includes:
</p>
<ul>
<li><strong>Equities (50-70%):</strong> Domestic and international stocks</li>
<li><strong>Fixed Income (20-30%):</strong> Government and corporate bonds</li>
<li><strong>Real Assets (5-15%):</strong> REITs, commodities, infrastructure</li>
<li><strong>Alternatives (0-10%):</strong> Private equity, hedge funds, or cash</li>
</ul>
<h2>Sector Diversification</h2>
<p>
Within equities, avoid over-concentration in any single sector. Technology has outperformed
for over a decade, but cycles turn. Maintaining exposure to healthcare, consumer staples,
energy, and financials provides balance through different economic conditions.
</p>
<h2>Rebalancing Strategy</h2>
<p>
Portfolio drift occurs naturally as different assets grow at different rates. Annual
rebalancing back to target allocations forces investors to systematically buy low and
sell high, improving long-term risk-adjusted returns.
</p>
<footer>
<p>© 2025 Wealth Management Review. All rights reserved.</p>
</footer>
</body>
</html>
"""
    }
]


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
    # 1. Create directories
    os.makedirs(FINANCE_DIR, exist_ok=True)
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    print(f"Created directories: {FINANCE_DIR}, {RESEARCH_DIR}")

    # 2. Create HTML article files
    for article in ARTICLES:
        html_path = os.path.join(FINANCE_DIR, article["filename"])
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(article["content"])
        print(f"Created article: {html_path}")

    # 3. Verify Research dir is empty (no PDFs pre-existing)
    existing_pdfs = [f for f in os.listdir(RESEARCH_DIR) if f.endswith('.pdf')]
    if existing_pdfs:
        for pdf in existing_pdfs:
            os.remove(os.path.join(RESEARCH_DIR, pdf))
            print(f"Removed pre-existing PDF: {pdf}")

    print("Initial state created successfully.")
    print(f"Research directory is empty: {os.listdir(RESEARCH_DIR)}")

    # 4. Kill any existing Chrome instances before launching fresh
    subprocess.run(
        ["pkill", "-f", "google-chrome"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2.0)

    # 5. Launch Chrome with the 3 article tabs
    # Build URLs for all 3 articles
    article_urls = " ".join(
        f'"file://{FINANCE_DIR}/{a["filename"]}"' for a in ARTICLES
    )
    chrome_cmd = (
        f'google-chrome --new-window {article_urls}'
    )
    launch_gui(chrome_cmd, delay_sec=3.0)
    print(f"GUI_READY: launched Chrome with 3 financial article tabs (DISPLAY=:0)")
    print(f"Tabs:")
    for a in ARTICLES:
        print(f"  - {a['title']} (file://{FINANCE_DIR}/{a['filename']})")


create_initial()
