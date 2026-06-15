"""
Initial Setup: Create report.html for VSCode folding task
Task ID: vscode_edit_077
Domain: vs_code
Description: Creates ~/Desktop/report.html (180 lines, 5 section elements)
             and opens it in VSCode. All sections are visible (unfolded).
             Section positions: header (10-30), summary (32-60),
             details (62-110), charts (112-155), footer (157-180).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'vscode_edit_077'
OUTPUT = f'{DESKTOP}/report.html'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # Lines 1-9: DOCTYPE and head
    # Line 10: <section id="header">
    # Line 30: </section>  [closes header]
    # Line 31: blank
    # Line 32: <section id="summary">
    # Line 60: </section>  [closes summary]
    # Line 61: blank
    # Line 62: <section id="details">
    # Line 110: </section> [closes details]
    # Line 111: blank
    # Line 112: <section id="charts">
    # Line 155: </section> [closes charts]
    # Line 156: blank
    # Line 157: <section id="footer">
    # Line 180: </section> [closes footer]

    lines = []

    # Lines 1-9: HTML boilerplate
    lines.append('<!DOCTYPE html>')                              # 1
    lines.append('<html lang="en">')                            # 2
    lines.append('<head>')                                      # 3
    lines.append('    <meta charset="UTF-8">')                  # 4
    lines.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">') # 5
    lines.append('    <title>Quarterly Business Report - Q1 2025</title>') # 6
    lines.append('    <link rel="stylesheet" href="styles.css">') # 7
    lines.append('</head>')                                     # 8
    lines.append('<body>')                                      # 9

    # Line 10: <section id="header">  — 21 lines (10-30)
    lines.append('<section id="header">')                       # 10
    lines.append('    <header class="page-header">')            # 11
    lines.append('        <div class="company-logo">')          # 12
    lines.append('            <img src="assets/logo.png" alt="Acme Corp Logo" />') # 13
    lines.append('        </div>')                              # 14
    lines.append('        <div class="report-title">')          # 15
    lines.append('            <h1>Quarterly Business Report</h1>') # 16
    lines.append('            <h2>Q1 2025 — January through March</h2>') # 17
    lines.append('        </div>')                              # 18
    lines.append('        <div class="report-meta">')           # 19
    lines.append('            <p>Prepared by: Strategic Analytics Division</p>') # 20
    lines.append('            <p>Report Date: April 10, 2025</p>') # 21
    lines.append('            <p>Classification: Internal Use Only</p>') # 22
    lines.append('            <p>Version: 2.1 (Final)</p>')     # 23
    lines.append('            <p>Distribution: Executive Team, Department Heads</p>') # 24
    lines.append('            <p>Next Review: July 15, 2025</p>') # 25
    lines.append('        </div>')                              # 26
    lines.append('        <nav class="report-nav">')            # 27
    lines.append('            <a href="#summary">Summary</a> | <a href="#details">Details</a> | <a href="#charts">Charts</a>') # 28
    lines.append('        </nav>')                              # 29
    # Line 30: </section> closes the header section
    lines.append('</section>')                                  # 30
    assert len(lines) == 30, f"Expected 30 lines after header section, got {len(lines)}"

    # Line 31: blank separator
    lines.append('')                                            # 31

    # Line 32: <section id="summary">  — 29 lines (32-60)
    lines.append('<section id="summary">')                      # 32
    lines.append('    <div class="section-header">')            # 33
    lines.append('        <h2>Executive Summary</h2>')          # 34
    lines.append('        <p class="subtitle">High-level overview of Q1 2025 performance</p>') # 35
    lines.append('    </div>')                                  # 36
    lines.append('    <div class="summary-content">')           # 37
    lines.append('        <p>')                                 # 38
    lines.append('            The first quarter of 2025 demonstrated strong revenue growth across all') # 39
    lines.append('            major business units. Total revenue reached $4.7 million, a 12% increase') # 40
    lines.append('            compared to Q1 2024. Operating expenses were held at $3.1 million,') # 41
    lines.append('            resulting in an operating margin of 34%.') # 42
    lines.append('        </p>')                                # 43
    lines.append('        <p>')                                 # 44
    lines.append('            Key highlights: successful launch of the CloudSync Pro product line,') # 45
    lines.append('            contributing $420,000 in new revenue; expansion into Southeast Asian') # 46
    lines.append('            market, adding 87 enterprise customers at $28,000 average contract value.') # 47
    lines.append('        </p>')                                # 48
    lines.append('    </div>')                                  # 49
    lines.append('    <div class="summary-kpis">')              # 50
    lines.append('        <div class="kpi-card">')              # 51
    lines.append('            <span class="kpi-label">Total Revenue</span>') # 52
    lines.append('            <span class="kpi-value">$4.7M</span>') # 53
    lines.append('            <span class="kpi-delta positive">+12% YoY</span>') # 54
    lines.append('        </div>')                              # 55
    lines.append('        <div class="kpi-card">')              # 56
    lines.append('            <span class="kpi-label">New Customers</span>') # 57
    lines.append('            <span class="kpi-value">214</span>') # 58
    lines.append('            <span class="kpi-delta positive">+31% YoY</span>') # 59
    lines.append('</section>')                                  # 60
    assert len(lines) == 60, f"Expected 60 lines after summary section, got {len(lines)}"

    # Line 61: blank separator
    lines.append('')                                            # 61

    # Line 62: <section id="details">  — 49 lines (62-110)
    lines.append('<section id="details">')                      # 62
    lines.append('    <div class="section-header">')            # 63
    lines.append('        <h2>Detailed Performance Analysis</h2>') # 64
    lines.append('        <p class="subtitle">Department-by-department breakdown for Q1 2025</p>') # 65
    lines.append('    </div>')                                  # 66
    lines.append('    <div class="department-section">')        # 67
    lines.append('        <h3>Engineering &amp; Product</h3>') # 68
    lines.append('        <p>The Engineering team shipped 3 major releases and 14 minor updates.')  # 69
    lines.append('           CloudSync Pro launched on schedule. Technical debt reduction led to')  # 70
    lines.append('           22% faster build times and 15% fewer production incidents.</p>')       # 71
    lines.append('        <table class="data-table">')          # 72
    lines.append('            <thead>')                         # 73
    lines.append('                <tr><th>Metric</th><th>Q1 2025</th><th>Q4 2024</th><th>Change</th></tr>') # 74
    lines.append('            </thead>')                        # 75
    lines.append('            <tbody>')                         # 76
    lines.append('                <tr><td>Major releases</td><td>3</td><td>2</td><td>+50%</td></tr>') # 77
    lines.append('                <tr><td>Bug fix PRs</td><td>147</td><td>138</td><td>+6.5%</td></tr>') # 78
    lines.append('                <tr><td>Uptime SLA</td><td>99.97%</td><td>99.91%</td><td>+0.06pp</td></tr>') # 79
    lines.append('                <tr><td>Deploy time</td><td>8 min</td><td>12 min</td><td>-33%</td></tr>') # 80
    lines.append('            </tbody>')                        # 81
    lines.append('        </table>')                            # 82
    lines.append('    </div>')                                  # 83
    lines.append('    <div class="department-section">')        # 84
    lines.append('        <h3>Sales &amp; Business Development</h3>') # 85
    lines.append('        <p>Sales exceeded quarterly targets by 18%, closing 214 new accounts.')   # 86
    lines.append('           Southeast Asia expansion campaign generated 87 new accounts at')       # 87
    lines.append('           an average contract value of $28,000.</p>')                            # 88
    lines.append('        <table class="data-table">')          # 89
    lines.append('            <thead>')                         # 90
    lines.append('                <tr><th>Region</th><th>New Accounts</th><th>ARR Added</th><th>Win Rate</th></tr>') # 91
    lines.append('            </thead>')                        # 92
    lines.append('            <tbody>')                         # 93
    lines.append('                <tr><td>North America</td><td>89</td><td>$1,240,000</td><td>42%</td></tr>') # 94
    lines.append('                <tr><td>Europe</td><td>38</td><td>$620,000</td><td>37%</td></tr>') # 95
    lines.append('                <tr><td>Southeast Asia</td><td>87</td><td>$2,436,000</td><td>51%</td></tr>') # 96
    lines.append('            </tbody>')                        # 97
    lines.append('        </table>')                            # 98
    lines.append('    </div>')                                  # 99
    lines.append('    <div class="department-section">')        # 100
    lines.append('        <h3>Customer Success</h3>')           # 101
    lines.append('        <p>Customer Success managed 1,048 active accounts. Net Promoter Score: 62.') # 102
    lines.append('           Churn rate reduced to 1.8% versus industry average of 2.4%.</p>')     # 103
    lines.append('        <ul>')                                # 104
    lines.append('            <li>Average ticket resolution: 4.2 hours (was 7.0 hours)</li>') # 105
    lines.append('            <li>CSAT score: 4.6 / 5.0 (was 4.3 / 5.0)</li>') # 106
    lines.append('            <li>3 enterprise accounts upgraded to Platinum tier</li>') # 107
    lines.append('            <li>0 critical P0 incidents reported in Q1 2025</li>') # 108
    lines.append('        </ul>')                               # 109
    lines.append('</section>')                                  # 110
    assert len(lines) == 110, f"Expected 110 lines after details section, got {len(lines)}"

    # Line 111: blank separator
    lines.append('')                                            # 111

    # Line 112: <section id="charts">  — 44 lines (112-155)
    lines.append('<section id="charts">')                       # 112
    lines.append('    <div class="section-header">')            # 113
    lines.append('        <h2>Data Visualizations</h2>')        # 114
    lines.append('        <p class="subtitle">Charts and graphs for Q1 2025 performance metrics</p>') # 115
    lines.append('    </div>')                                  # 116
    lines.append('    <div class="chart-grid">')                # 117
    lines.append('        <figure class="chart-item">')         # 118
    lines.append('            <img src="charts/revenue_trend.png" alt="Monthly Revenue Trend Q1 2025" />') # 119
    lines.append('            <figcaption>Figure 1: Monthly Revenue Trend (Jan-Mar 2025)</figcaption>') # 120
    lines.append('        </figure>')                           # 121
    lines.append('        <figure class="chart-item">')         # 122
    lines.append('            <img src="charts/customer_acq.png" alt="Customer Acquisition by Region" />') # 123
    lines.append('            <figcaption>Figure 2: New Customer Acquisition by Region</figcaption>') # 124
    lines.append('        </figure>')                           # 125
    lines.append('        <figure class="chart-item">')         # 126
    lines.append('            <img src="charts/nps_trend.png" alt="NPS Score Over Time" />') # 127
    lines.append('            <figcaption>Figure 3: Net Promoter Score — Rolling 12-Month</figcaption>') # 128
    lines.append('        </figure>')                           # 129
    lines.append('        <figure class="chart-item">')         # 130
    lines.append('            <img src="charts/opex_breakdown.png" alt="Operating Expense Breakdown" />') # 131
    lines.append('            <figcaption>Figure 4: Operating Expense Breakdown by Category</figcaption>') # 132
    lines.append('        </figure>')                           # 133
    lines.append('        <figure class="chart-item">')         # 134
    lines.append('            <img src="charts/headcount.png" alt="Headcount Growth" />') # 135
    lines.append('            <figcaption>Figure 5: Headcount Growth Q4 2023 - Q1 2025</figcaption>') # 136
    lines.append('        </figure>')                           # 137
    lines.append('        <figure class="chart-item">')         # 138
    lines.append('            <img src="charts/product_rev.png" alt="Revenue by Product Line" />') # 139
    lines.append('            <figcaption>Figure 6: Revenue Contribution by Product Line</figcaption>') # 140
    lines.append('        </figure>')                           # 141
    lines.append('    </div>')                                  # 142
    lines.append('    <div class="chart-notes">')               # 143
    lines.append('        <h3>Notes on Data Sources</h3>')      # 144
    lines.append('        <p>All revenue figures are reported in USD under ASC 606 standards.')    # 145
    lines.append('           Customer counts reflect active paid subscriptions as of March 31.</p>') # 146
    lines.append('        <p>NPS data is collected via quarterly survey (41% response rate).</p>') # 147
    lines.append('        <p>Charts generated using internal analytics tooling v3.2.</p>') # 148
    lines.append('        <p>Raw data available from Finance: finance@acmecorp.example.com</p>') # 149
    lines.append('        <p>Headcount data sourced from HR system as of March 31, 2025.</p>') # 150
    lines.append('        <p>All percentages rounded to nearest 0.1 percentage point.</p>') # 151
    lines.append('        <p>Prior period figures restated for comparability where noted.</p>') # 152
    lines.append('        <p>Currency conversion rates as of March 31, 2025 (USD/EUR: 1.082).</p>') # 153
    lines.append('        <p>Forecast data excluded from this version per policy.</p>') # 154
    lines.append('</section>')                                  # 155
    assert len(lines) == 155, f"Expected 155 lines after charts section, got {len(lines)}"

    # Line 156: blank separator
    lines.append('')                                            # 156

    # Line 157: <section id="footer">  — 24 lines (157-180)
    lines.append('<section id="footer">')                       # 157
    lines.append('    <footer class="page-footer">')            # 158
    lines.append('        <div class="footer-content">')        # 159
    lines.append('            <p class="disclaimer">')          # 160
    lines.append('                This report is confidential and intended solely for internal use') # 161
    lines.append('                by Acme Corp employees and authorized contractors. Unauthorized') # 162
    lines.append('                distribution is strictly prohibited under company policy.')       # 163
    lines.append('            </p>')                            # 164
    lines.append('            <p>For questions, contact Strategic Analytics: analytics@acmecorp.example.com</p>') # 165
    lines.append('            <p>Phone extension: 4421 | Office: Building B, Room 312</p>') # 166
    lines.append('        </div>')                              # 167
    lines.append('        <div class="footer-signatures">')     # 168
    lines.append('            <div class="signature-block">')   # 169
    lines.append('                <p>Approved by: Sarah Chen, VP of Analytics</p>') # 170
    lines.append('                <p>Reviewed by: Marcus Johnson, CFO</p>') # 171
    lines.append('                <p>Date: April 10, 2025</p>') # 172
    lines.append('            </div>')                          # 173
    lines.append('        </div>')                              # 174
    lines.append('        <div class="footer-meta">')           # 175
    lines.append('            <p>Document ID: QBR-2025-Q1-v2.1</p>') # 176
    lines.append('            <p>Generated: 2025-04-10T09:15:00Z</p>') # 177
    lines.append('        </div>')                              # 178
    lines.append('    </footer>')                               # 179
    lines.append('</section>')                                  # 180
    assert len(lines) == 180, f"Expected 180 lines after footer section, got {len(lines)}"

    # Closing HTML tags (not counted in section lines, but needed for valid HTML)
    lines.append('')                                            # 181
    lines.append('</body>')                                     # 182
    lines.append('</html>')                                     # 183

    html_content = '\n'.join(lines) + '\n'

    with open(OUTPUT, 'w') as f:
        f.write(html_content)

    # Verify line count
    actual_lines = html_content.count('\n')
    print(f'Initial file created: {OUTPUT} ({actual_lines} lines written)')

    # Verify section positions
    all_lines = html_content.split('\n')
    for i, line in enumerate(all_lines, 1):
        if '<section' in line or ('</section>' in line and '</section>' == line.strip()):
            print(f'  Line {i}: {line.strip()[:70]}')

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with report.html using DISPLAY=:0')


create_initial()
