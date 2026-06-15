"""
Initial Setup: Chrome with 4 legal document tabs open for PDF saving task
Task ID: osworld_multi_apps_bulk_pdf_save_006
Domain: chrome + os (multi-app)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_006'
LEGAL_DOCS_DIR = '/home/user/Documents/Legal-Docs'
HTML_DIR = '/home/user/Documents/legal_source_pages'

# Legal document page titles (these become the expected PDF filenames)
LEGAL_DOCUMENTS = [
    {
        "title": "Non-Disclosure Agreement Template",
        "filename": "nda_template.html",
        "content": """<!DOCTYPE html>
<html>
<head><title>Non-Disclosure Agreement Template</title></head>
<body>
<h1>Non-Disclosure Agreement (NDA)</h1>
<p>This Non-Disclosure Agreement ("Agreement") is entered into as of the date last signed below, between the parties identified herein.</p>

<h2>1. Definition of Confidential Information</h2>
<p>For purposes of this Agreement, "Confidential Information" shall include all information or data that has or could have commercial value or other utility in the business in which Disclosing Party is engaged.</p>

<h2>2. Obligations of Receiving Party</h2>
<p>The Receiving Party agrees to: (a) hold the Disclosing Party's Confidential Information in strict confidence; (b) not to disclose the Confidential Information to third parties without the prior written consent of the Disclosing Party; and (c) not to use any Confidential Information for any purpose except to evaluate and engage in discussions concerning a potential business relationship between the parties.</p>

<h2>3. Term</h2>
<p>The nondisclosure provisions of this Agreement shall survive the termination of this Agreement and Receiving Party's duty to hold Confidential Information in confidence shall remain in effect until the Confidential Information no longer qualifies as a trade secret or until Disclosing Party sends Receiving Party written notice releasing Receiving Party from this Agreement, whichever occurs first.</p>

<h2>4. Exclusions from Confidential Information</h2>
<p>Receiving Party's obligations under this Agreement do not extend to information that is: (a) publicly known at the time of disclosure or subsequently becomes publicly known through no fault of the Receiving Party; (b) discovered or created by the Receiving Party before disclosure by Disclosing Party; (c) learned by the Receiving Party through legitimate means other than from the Disclosing Party or Disclosing Party's representatives.</p>

<h2>5. Remedies</h2>
<p>Nothing in this Agreement is intended to limit any remedy of either party under applicable law. Receiving Party acknowledges that breach of this Agreement would cause irreparable harm to Disclosing Party and agrees that monetary damages may be inadequate.</p>

<p><strong>Disclosing Party Signature:</strong> _______________________</p>
<p><strong>Receiving Party Signature:</strong> _______________________</p>
<p><strong>Date:</strong> _______________________</p>
</body>
</html>"""
    },
    {
        "title": "Employment Contract Template",
        "filename": "employment_contract.html",
        "content": """<!DOCTYPE html>
<html>
<head><title>Employment Contract Template</title></head>
<body>
<h1>Employment Contract</h1>
<p>This Employment Contract ("Contract") is made and entered into as of [DATE], by and between [EMPLOYER NAME] ("Employer") and [EMPLOYEE NAME] ("Employee").</p>

<h2>1. Position and Duties</h2>
<p>Employer agrees to employ Employee as [JOB TITLE]. Employee's duties include but are not limited to performing all tasks assigned by the Employer that are consistent with the Employee's skills and experience.</p>

<h2>2. Compensation</h2>
<p>Employee shall receive a base salary of $[AMOUNT] per year, payable in accordance with Employer's standard payroll schedule. Employee shall also be eligible for performance-based bonuses at the discretion of management.</p>

<h2>3. Benefits</h2>
<p>Employee shall be entitled to all benefits generally available to employees in similar positions, including health insurance, dental insurance, vision insurance, and 401(k) retirement plan participation, subject to eligibility requirements.</p>

<h2>4. At-Will Employment</h2>
<p>Employee's employment with Employer is "at-will," meaning either party may terminate this Contract at any time, with or without cause, and with or without notice.</p>

<h2>5. Confidentiality</h2>
<p>Employee agrees to maintain the confidentiality of all proprietary and confidential information of Employer. This obligation shall survive termination of employment.</p>

<h2>6. Non-Compete Clause</h2>
<p>For a period of twelve (12) months following termination of employment, Employee agrees not to engage in any business activity that directly competes with Employer's business within a 50-mile radius.</p>

<p><strong>Employer Signature:</strong> _______________________</p>
<p><strong>Employee Signature:</strong> _______________________</p>
<p><strong>Date:</strong> _______________________</p>
</body>
</html>"""
    },
    {
        "title": "Service Level Agreement",
        "filename": "service_level_agreement.html",
        "content": """<!DOCTYPE html>
<html>
<head><title>Service Level Agreement</title></head>
<body>
<h1>Service Level Agreement (SLA)</h1>
<p>This Service Level Agreement ("SLA") is entered into between [SERVICE PROVIDER] ("Provider") and [CLIENT NAME] ("Client"), effective as of [DATE].</p>

<h2>1. Scope of Services</h2>
<p>Provider agrees to deliver the following services: cloud infrastructure management, 24/7 system monitoring, incident response, and technical support. All services shall be performed in accordance with industry best practices.</p>

<h2>2. Service Availability</h2>
<p>Provider guarantees system uptime of 99.9% ("Uptime Guarantee"), measured on a monthly basis. Scheduled maintenance windows of up to 4 hours per month are excluded from uptime calculations and will be communicated 48 hours in advance.</p>

<h2>3. Response Times</h2>
<p>Incident response times are classified as follows:</p>
<ul>
<li><strong>Critical (P1):</strong> Response within 15 minutes, resolution within 4 hours</li>
<li><strong>High (P2):</strong> Response within 1 hour, resolution within 8 hours</li>
<li><strong>Medium (P3):</strong> Response within 4 hours, resolution within 24 hours</li>
<li><strong>Low (P4):</strong> Response within 8 hours, resolution within 72 hours</li>
</ul>

<h2>4. Service Credits</h2>
<p>In the event Provider fails to meet the Uptime Guarantee, Client shall receive service credits calculated as follows: 10% credit for uptime between 99.0%-99.9%; 25% credit for uptime between 95.0%-99.0%; 50% credit for uptime below 95.0%.</p>

<h2>5. Measurement and Reporting</h2>
<p>Provider shall provide monthly performance reports detailing uptime statistics, incident summaries, and any SLA breaches. Reports will be delivered within 5 business days of month-end.</p>

<h2>6. Term and Termination</h2>
<p>This SLA shall remain in effect for one (1) year from the effective date and shall automatically renew unless terminated by either party with 30 days written notice.</p>

<p><strong>Provider Signature:</strong> _______________________</p>
<p><strong>Client Signature:</strong> _______________________</p>
<p><strong>Date:</strong> _______________________</p>
</body>
</html>"""
    },
    {
        "title": "Privacy Policy Template",
        "filename": "privacy_policy.html",
        "content": """<!DOCTYPE html>
<html>
<head><title>Privacy Policy Template</title></head>
<body>
<h1>Privacy Policy</h1>
<p>Last Updated: [DATE]</p>
<p>[COMPANY NAME] ("we," "us," or "our") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our services.</p>

<h2>1. Information We Collect</h2>
<p>We may collect information about you in a variety of ways. The information we may collect includes:</p>
<ul>
<li><strong>Personal Data:</strong> Personally identifiable information, such as your name, email address, phone number, and demographic information.</li>
<li><strong>Derivative Data:</strong> Information our servers automatically collect when you access our services, such as your IP address, browser type, referring/exit pages, and operating system.</li>
<li><strong>Financial Data:</strong> Financial information, such as data related to your payment method, collected when you purchase our services.</li>
</ul>

<h2>2. Use of Your Information</h2>
<p>Having accurate information about you permits us to provide you with a smooth, efficient, and customized experience. We may use information collected about you to: create and manage your account; process transactions; send administrative information; fulfill and manage purchases; generate statistical and research data.</p>

<h2>3. Disclosure of Your Information</h2>
<p>We may share information we have collected about you in certain situations. Your information may be disclosed as follows:</p>
<ul>
<li><strong>By Law or to Protect Rights:</strong> If we believe the release of information about you is necessary to respond to legal process.</li>
<li><strong>Business Transfers:</strong> We may share or transfer your information in connection with, or during negotiations of, any merger, sale of company assets, or acquisition.</li>
</ul>

<h2>4. Security of Your Information</h2>
<p>We use administrative, technical, and physical security measures to help protect your personal information. While we have taken reasonable steps to secure the personal information you provide, please be aware that no security measures are perfect or impenetrable.</p>

<h2>5. Contact Us</h2>
<p>If you have questions or comments about this Privacy Policy, please contact us at: [CONTACT EMAIL]</p>
</body>
</html>"""
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
    # 1. Create the Legal-Docs target directory (empty - no PDFs yet)
    os.makedirs(LEGAL_DOCS_DIR, exist_ok=True)
    print(f'Created directory: {LEGAL_DOCS_DIR}')

    # 2. Create source HTML directory
    os.makedirs(HTML_DIR, exist_ok=True)

    # 3. Write all legal document HTML files
    html_paths = []
    for doc in LEGAL_DOCUMENTS:
        html_path = os.path.join(HTML_DIR, doc['filename'])
        with open(html_path, 'w') as f:
            f.write(doc['content'])
        html_paths.append(html_path)
        print(f'Created HTML: {html_path}')

    # 4. Kill any running Chrome instances so we can start fresh
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(2)

    # 5. Launch Chrome with all 4 legal document tabs open
    # Use remote debugging port so tabs are visible and manageable
    # Build the command with all URLs
    urls = [f'file://{p}' for p in html_paths]
    url_args = ' '.join(f'"{u}"' for u in urls)

    chrome_cmd = (
        f'google-chrome '
        f'--no-first-run '
        f'--disable-default-apps '
        f'--no-default-browser-check '
        f'--remote-debugging-port=1337 '
        f'{url_args}'
    )

    launch_gui(chrome_cmd, delay_sec=3.0)
    print('GUI_READY: Chrome launched with 4 legal document tabs open')
    print(f'Tabs:')
    for doc in LEGAL_DOCUMENTS:
        print(f'  - {doc["title"]}')
    print(f'Target directory (empty): {LEGAL_DOCS_DIR}')


create_initial()
