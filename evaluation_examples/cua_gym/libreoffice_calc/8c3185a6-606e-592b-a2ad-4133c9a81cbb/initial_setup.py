"""
Initial Setup: PDF to Google Doc extraction task
Task ID: osworld_multi_apps_pdf_to_gdocs_007
Domain: multi_apps (PDF + Chrome/Google Drive)

Creates:
  - company_strategy.pdf on Desktop with multiple strategic planning sections
  - Chrome opened to Google Drive (pre-signed-in state is available in the VM image)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_007'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/company_strategy.pdf'


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


def create_strategy_pdf():
    """Create company_strategy.pdf on the Desktop with multiple sections."""
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos
    except ImportError:
        subprocess.run(['pip3', 'install', 'fpdf2'], check=True, capture_output=True)
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos

    def mcell(pdf, text, h=6):
        """multi_cell that resets x to left margin after printing (fpdf2 bug workaround)."""
        pdf.multi_cell(0, h, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Page 1: Cover Page ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 22)
    pdf.ln(30)
    pdf.cell(0, 12, 'TechVision Inc.', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Company Strategy 2025-2027', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'Confidential - Internal Use Only', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 7, 'Prepared by: Strategy and Planning Team', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 7, 'Last Updated: March 2025', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # --- Page 2: Table of Contents ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Table of Contents', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    for item in [
        '1. Executive Summary',
        '2. Product Roadmap',
        '3. Market Analysis',
        '4. Financial Projections',
        '5. Operational Plan',
    ]:
        pdf.cell(0, 8, item, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- Page 3: Executive Summary ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '1. Executive Summary', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'TechVision Inc. has experienced significant growth over the past fiscal year, '
        'achieving a 34% increase in annual recurring revenue and expanding our customer '
        'base to over 2,400 enterprise clients globally. This strategic document outlines '
        'our three-year roadmap to solidify our market position and achieve our ambitious '
        'growth targets.')
    pdf.ln(3)
    mcell(pdf,
        'Our strategy is built on four core pillars: product innovation, market expansion, '
        'operational excellence, and talent development. By executing on all four fronts '
        'simultaneously, we aim to triple our market share in the enterprise SaaS segment '
        'by 2027.')
    pdf.ln(3)
    mcell(pdf,
        'Key highlights include the launch of our AI-powered analytics suite (Q2 2025), '
        'expansion into the Asia-Pacific market (Q3 2025), and a strategic partnership '
        'with CloudScale Systems to enhance our infrastructure capabilities.')

    # --- Page 4: Product Roadmap Part 1 ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '2. Product Roadmap', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Vision Statement', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'Our product vision is to become the leading intelligent work platform for '
        'enterprise teams, enabling seamless collaboration, automation, and data-driven '
        'decision making at scale. We will achieve this by building deeply integrated '
        'AI capabilities into every layer of our platform.')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Q1-Q2 2025: Foundation and AI Integration', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    for item in [
        'Launch TechVision AI Assistant v1.0 with natural language query support',
        'Release redesigned dashboard with customizable widget framework',
        'Implement SSO integration for enterprise identity providers',
        'Deploy advanced role-based access control (RBAC) with granular permissions',
        'Complete migration to microservices architecture for improved scalability',
        'Achieve SOC 2 Type II certification for enterprise compliance requirements',
    ]:
        mcell(pdf, '- ' + item)
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Q3-Q4 2025: Market Expansion Features', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    for item in [
        'Launch multi-language support (Japanese, Korean, Portuguese, German)',
        'Release mobile applications for iOS and Android platforms',
        'Introduce TechVision Marketplace for third-party integrations and extensions',
        'Deploy predictive analytics module with ML-powered forecasting',
        'Launch TechVision API v3.0 with GraphQL support and enhanced documentation',
        'Implement real-time collaborative editing for all document types',
    ]:
        mcell(pdf, '- ' + item)

    # --- Page 5: Product Roadmap Part 2 ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '2026: Enterprise Scale and Intelligence', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    for item in [
        'Launch TechVision Intelligence Suite with automated workflow optimization',
        'Release enterprise data governance and compliance monitoring tools',
        'Deploy industry-specific solution packages (Healthcare, Finance, Retail)',
        'Introduce AI-powered customer success prediction and intervention tools',
        'Launch TechVision Academy for customer training and certification programs',
        'Complete integration with all major ERP systems (SAP, Oracle, Dynamics)',
    ]:
        mcell(pdf, '- ' + item)
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, '2027: Platform Maturity and Ecosystem Growth', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    for item in [
        'Achieve feature parity across all deployment models (cloud, hybrid, on-premise)',
        'Launch TechVision Partner Network with 500+ certified implementation partners',
        'Deploy next-generation AI reasoning engine for complex workflow automation',
        'Introduce cross-organizational data sharing with privacy-preserving protocols',
        'Launch TechVision Insights: industry benchmarking and competitive intelligence',
        'Complete global data residency compliance for 40+ countries',
    ]:
        mcell(pdf, '- ' + item)
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Key Product Metrics and Success Criteria', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf, 'Success will be measured against the following KPIs:')
    for m in [
        'Net Promoter Score (NPS): Target 65+ by end of 2025 (current: 48)',
        'Feature Adoption Rate: 70% of enterprise customers using AI features by Q4 2025',
        'Time-to-Value: Reduce onboarding from 45 days to 14 days by mid-2025',
        'Platform Uptime: Maintain 99.99% availability SLA across all regions',
        'API Response Time: less than 100ms P95 for all core API endpoints',
    ]:
        mcell(pdf, '- ' + m)

    # --- Page 6: Market Analysis ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '3. Market Analysis', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Total Addressable Market', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'The global enterprise work management software market is valued at $47.8 billion '
        'in 2024 and projected to grow at a CAGR of 12.3% through 2028, reaching $75.2 billion. '
        'TechVision currently holds approximately 0.8% market share with significant headroom '
        'for expansion.')
    pdf.ln(3)
    mcell(pdf,
        'Our serviceable addressable market (SAM) focuses on mid-to-large enterprises '
        '(500-50,000 employees) with complex workflow needs, valued at $18.3 billion. '
        'Within this segment, we target organizations undergoing digital transformation '
        'initiatives, representing a SAM of $6.7 billion.')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Competitive Landscape', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    for comp in [
        'WorkStream Pro: Market leader with 18% share; strong in project management',
        'CollabSuite Enterprise: 12% share; dominant in communication-first workflows',
        'ProcessMax: 9% share; specialist in manufacturing and supply chain',
        'FlowOS: Emerging competitor; AI-native architecture, 3% share',
        'TechVision: 0.8% share; differentiated by deep AI integration and open API',
    ]:
        mcell(pdf, '- ' + comp)
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Target Customer Segments', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'Primary: Technology companies (500-5000 employees) seeking to streamline '
        'engineering and product workflows. Current penetration: 24% of addressable accounts.')
    pdf.ln(2)
    mcell(pdf,
        'Secondary: Financial services firms requiring compliance-grade audit trails '
        'and process documentation. Current penetration: 12% of addressable accounts.')
    pdf.ln(2)
    mcell(pdf,
        'Tertiary: Healthcare organizations modernizing administrative workflows while '
        'maintaining HIPAA compliance. Current penetration: 7% of addressable accounts.')

    # --- Page 7: Financial Projections ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '4. Financial Projections', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Revenue Forecast', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'Based on our pipeline analysis and historical growth patterns, we project the '
        'following revenue trajectory:')
    pdf.ln(2)
    for f in ['FY2025: $48.5M ARR (+42% YoY)', 'FY2026: $78.3M ARR (+62% YoY)', 'FY2027: $134.7M ARR (+72% YoY)']:
        pdf.cell(0, 7, f, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    mcell(pdf,
        'Key assumptions: Average contract value increases from $18,400 to $24,700 '
        'as we move upmarket; net revenue retention improves from 112% to 128%; '
        'new logo acquisition accelerates from 380 to 620 per quarter by end of 2025.')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Cost Structure', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    for c in [
        'R&D Investment: 28% of revenue in 2025, decreasing to 22% as we achieve scale',
        'Sales & Marketing: 38% of revenue in 2025 to fund growth initiatives',
        'General & Administrative: 12% of revenue, declining with scale efficiencies',
        'Cost of Revenue: 18% of revenue, improving with infrastructure optimization',
    ]:
        mcell(pdf, '- ' + c)
    pdf.ln(2)
    pdf.cell(0, 7, 'EBITDA margin path: -15% in 2025, -3% in 2026, +12% in 2027',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Investment Requirements', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'To execute this strategy, we are seeking $35M in Series C funding with the '
        'following allocation:')
    for inv in [
        'Product & Engineering: $14M (40%) for hiring 85 additional engineers',
        'Sales & Marketing: $10.5M (30%) for market expansion and brand building',
        'International Expansion: $7M (20%) for APAC and EMEA regional offices',
        'Infrastructure: $3.5M (10%) for capacity expansion and reliability improvements',
    ]:
        mcell(pdf, '- ' + inv)

    # --- Page 8: Operational Plan ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '5. Operational Plan', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'Our operational plan focuses on building the organizational capabilities needed '
        'to support our growth targets. Key initiatives include:')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 7, 'Talent Strategy', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'Grow headcount from 247 to 420 employees by end of 2025, with particular emphasis '
        'on senior engineering talent and enterprise sales professionals with domain expertise '
        'in our target verticals.')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 7, 'Infrastructure Scaling', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'Migrate from single-region to multi-region active-active deployment by Q2 2025, '
        'enabling sub-100ms latency for all major markets and eliminating single points of '
        'failure in our production stack.')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 7, 'Customer Success', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    mcell(pdf,
        'Expand customer success team from 18 to 45 FTEs, implement proactive health scoring '
        'for all accounts over $50K ARR, and launch dedicated enterprise support tiers with '
        '4-hour SLA response times.')

    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)
    pdf.output(PDF_PATH)
    print(f'Created: {PDF_PATH}')
    print(f'Size: {os.path.getsize(PDF_PATH)} bytes')


def main():
    create_strategy_pdf()

    # GUI-ready startup: Open Chrome pointing to Google Drive
    # Chrome is pre-configured with Google account in the VM image
    launch_gui('google-chrome --new-window "https://drive.google.com"', delay_sec=3.0)
    print('GUI_READY: launched Chrome with Google Drive open (DISPLAY=:0)')


main()
