"""
Initial Setup: Chrome open with 5 job posting tabs; Postings folder does NOT exist.
Task ID: osworld_multi_apps_bulk_pdf_save_008
Domain: chrome + os (multi-app)

This script:
1. Kills any running Chrome instances
2. Clears old Chrome session state so we can pre-load tabs
3. Creates /home/user/Documents/Job-Applications/ (but NOT the Postings subfolder)
4. Launches Chrome with 5 job-posting HTML pages opened as tabs
5. Leaves Chrome running (DISPLAY=:0) with all tabs visible
"""

import os
import shlex
import subprocess
import time
import json
import shutil

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_008'

# Job postings: (job_title, source_site, fake_url)
JOB_POSTINGS = [
    {
        "title": "Senior Software Engineer",
        "company": "Google",
        "location": "Mountain View, CA (Hybrid)",
        "source": "LinkedIn",
        "url": "https://www.linkedin.com/jobs/view/senior-software-engineer-google",
        "salary": "$180,000 - $250,000/yr",
        "description": (
            "Join Google's Core Infrastructure team as a Senior Software Engineer. "
            "You will design, build, and maintain the systems that power Google's global services. "
            "Requirements: 5+ years of experience in distributed systems, proficiency in C++/Go/Java, "
            "strong understanding of algorithms and data structures."
        ),
        "posted": "2 days ago",
        "applicants": "342 applicants",
    },
    {
        "title": "Data Scientist",
        "company": "Spotify",
        "location": "New York, NY (Remote OK)",
        "source": "Indeed",
        "url": "https://www.indeed.com/viewjob?jk=data-scientist-spotify-nyc",
        "salary": "$130,000 - $160,000/yr",
        "description": (
            "Spotify is looking for a Data Scientist to join our Personalization team. "
            "You will build and evaluate machine learning models that power our recommendation engine. "
            "Requirements: MS/PhD in Statistics or CS, 3+ years of ML experience, Python/SQL expertise."
        ),
        "posted": "1 day ago",
        "applicants": "218 applicants",
    },
    {
        "title": "Product Manager",
        "company": "Stripe",
        "location": "San Francisco, CA",
        "source": "Stripe Careers",
        "url": "https://stripe.com/jobs/listing/product-manager-payments",
        "salary": "$170,000 - $230,000/yr",
        "description": (
            "Drive product strategy and roadmap for Stripe's Payments platform. "
            "Collaborate with engineering, design, and business teams to ship features that "
            "make financial infrastructure accessible to businesses globally. "
            "Requirements: 4+ years of PM experience in fintech or developer tools."
        ),
        "posted": "3 days ago",
        "applicants": "127 applicants",
    },
    {
        "title": "UX Designer",
        "company": "Airbnb",
        "location": "San Francisco, CA (Hybrid)",
        "source": "LinkedIn",
        "url": "https://www.linkedin.com/jobs/view/ux-designer-airbnb-sf",
        "salary": "$120,000 - $155,000/yr",
        "description": (
            "Airbnb's Design team is seeking a UX Designer to reimagine travel experiences. "
            "You will conduct user research, create wireframes and prototypes, and partner with "
            "product and engineering to deliver intuitive interfaces. "
            "Requirements: 3+ years UX design experience, proficiency in Figma, portfolio required."
        ),
        "posted": "4 days ago",
        "applicants": "89 applicants",
    },
    {
        "title": "DevOps Engineer",
        "company": "Netflix",
        "location": "Los Gatos, CA (On-site)",
        "source": "Netflix Jobs",
        "url": "https://jobs.netflix.com/jobs/devops-engineer-cloud-infrastructure",
        "salary": "$160,000 - $220,000/yr",
        "description": (
            "Netflix is hiring a DevOps Engineer to scale our cloud infrastructure for 270M+ subscribers. "
            "You will automate deployments, maintain CI/CD pipelines, and improve system reliability. "
            "Requirements: 4+ years in DevOps/SRE, expertise in AWS/GCP, Kubernetes, Terraform."
        ),
        "posted": "5 days ago",
        "applicants": "456 applicants",
    },
]

HTML_DIR = f'{WORKDIR}/job_posting_pages'


def create_job_posting_html(posting):
    """Create a realistic job posting HTML page."""
    title = posting['title']
    company = posting['company']
    location = posting['location']
    source = posting['source']
    salary = posting['salary']
    description = posting['description']
    posted = posting['posted']
    applicants = posting['applicants']
    tab_title = f"{title} at {company}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{tab_title}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #f3f2ee;
      margin: 0;
      padding: 0;
    }}
    .navbar {{
      background: #0a66c2;
      color: white;
      padding: 12px 24px;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .container {{
      max-width: 860px;
      margin: 32px auto;
      background: white;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12);
      padding: 32px 36px;
    }}
    h1 {{
      font-size: 26px;
      font-weight: 700;
      color: #191919;
      margin: 0 0 6px 0;
    }}
    .company-info {{
      font-size: 16px;
      color: #191919;
      margin-bottom: 4px;
    }}
    .meta {{
      font-size: 14px;
      color: #666;
      margin-bottom: 18px;
    }}
    .salary-badge {{
      display: inline-block;
      background: #e8f5e9;
      color: #2e7d32;
      border: 1px solid #a5d6a7;
      border-radius: 4px;
      padding: 4px 12px;
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 18px;
    }}
    .apply-btn {{
      display: inline-block;
      background: #0a66c2;
      color: white;
      border: none;
      border-radius: 24px;
      padding: 10px 28px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      margin-bottom: 28px;
      text-decoration: none;
    }}
    .section-title {{
      font-size: 18px;
      font-weight: 700;
      color: #191919;
      margin-bottom: 10px;
      border-bottom: 1px solid #e0e0e0;
      padding-bottom: 6px;
    }}
    .description {{
      font-size: 15px;
      color: #333;
      line-height: 1.7;
      margin-bottom: 24px;
    }}
    .tag {{
      display: inline-block;
      background: #f0f0f0;
      color: #555;
      border-radius: 4px;
      padding: 3px 10px;
      font-size: 13px;
      margin: 3px 3px 3px 0;
    }}
    .source-label {{
      font-size: 13px;
      color: #999;
      margin-top: 20px;
    }}
  </style>
</head>
<body>
  <div class="navbar">{source}</div>
  <div class="container">
    <h1>{title}</h1>
    <div class="company-info">{company} &middot; {location}</div>
    <div class="meta">{posted} &middot; {applicants}</div>
    <div class="salary-badge">{salary}</div>
    <br/>
    <a class="apply-btn" href="#">Apply Now</a>
    <div class="section-title">About the Role</div>
    <div class="description">{description}</div>
    <div class="section-title">Skills</div>
    <div>
      <span class="tag">Python</span>
      <span class="tag">SQL</span>
      <span class="tag">Cloud</span>
      <span class="tag">Agile</span>
      <span class="tag">Communication</span>
    </div>
    <div class="source-label">Posted on {source}</div>
  </div>
</body>
</html>
"""
    return html


def setup_initial():
    # ---- 1. Kill any running Chrome ----
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    time.sleep(2)

    # ---- 2. Create job posting HTML pages ----
    os.makedirs(HTML_DIR, exist_ok=True)
    html_files = []
    for posting in JOB_POSTINGS:
        fname = f"{posting['title'].replace(' ', '_').replace('/', '_')}_{posting['company']}.html"
        fpath = os.path.join(HTML_DIR, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(create_job_posting_html(posting))
        html_files.append(fpath)
        print(f"Created: {fpath}")

    # ---- 3. Create Job-Applications dir (but NOT Postings subfolder) ----
    job_apps_dir = f'{WORKDIR}/Documents/Job-Applications'
    os.makedirs(job_apps_dir, exist_ok=True)
    # Explicitly ensure Postings subfolder does NOT exist
    postings_dir = os.path.join(job_apps_dir, 'Postings')
    if os.path.exists(postings_dir):
        shutil.rmtree(postings_dir)
    print(f"Created: {job_apps_dir} (Postings subfolder not created)")

    # ---- 4. Pre-configure Chrome session to open these URLs ----
    # Write a first-run sentinel config so Chrome doesn't show welcome dialogs
    chrome_dir = os.path.expanduser('~/.config/google-chrome')
    os.makedirs(chrome_dir, exist_ok=True)

    # Clear any old "Last Session" / "Last Tabs" so Chrome won't restore stale state
    default_dir = os.path.join(chrome_dir, 'Default')
    os.makedirs(default_dir, exist_ok=True)
    for stale_file in ['Last Session', 'Last Tabs', 'Current Session', 'Current Tabs']:
        stale_path = os.path.join(default_dir, stale_file)
        if os.path.exists(stale_path):
            os.remove(stale_path)

    # ---- 5. Launch Chrome with all 5 job posting tabs ----
    env = os.environ.copy()
    env['DISPLAY'] = ':0'

    # Build file:// URLs for local HTML files
    file_urls = [f'file://{p}' for p in html_files]

    chrome_cmd = [
        'google-chrome',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-default-apps',
        '--disable-sync',
        '--remote-debugging-port=1337',
    ] + file_urls

    subprocess.Popen(
        chrome_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(3)

    # Also launch socat bridge so CDP is accessible on port 9222
    subprocess.Popen(
        ['socat', 'tcp-listen:9222,fork,reuseaddr', 'tcp:localhost:1337'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)

    print('GUI_READY: Chrome launched with 5 job posting tabs (DISPLAY=:0)')
    print(f'Tabs opened:')
    for p in JOB_POSTINGS:
        print(f'  - {p["title"]} at {p["company"]}')


setup_initial()
