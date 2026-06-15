"""
Initial Setup: Create a 12-page marketing brochure PDF and a company logo PNG.
Task ID: pdf_gf2_005
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_005'
BROCHURE_PATH = f'{WORKDIR}/marketing/brochure.pdf'
LOGO_PATH = f'{WORKDIR}/assets/logo.png'


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


def create_logo():
    """Create a 300x100 company logo PNG using Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    os.makedirs(f'{WORKDIR}/assets', exist_ok=True)

    img = Image.new('RGBA', (300, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a rounded rectangle background
    draw.rounded_rectangle([(5, 5), (295, 95)], radius=15, fill=(0, 82, 136, 255))

    # Draw a stylized "V" icon on the left
    draw.polygon([(20, 25), (50, 75), (80, 25)], fill=(255, 200, 50, 255))
    draw.polygon([(30, 25), (50, 65), (70, 25)], fill=(0, 82, 136, 255))

    # Company name text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except (IOError, OSError):
        font = ImageFont.load_default()

    draw.text((90, 22), "Vertex", fill=(255, 255, 255, 255), font=font)

    try:
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except (IOError, OSError):
        font_small = ImageFont.load_default()

    draw.text((90, 58), "Digital Solutions", fill=(200, 220, 240, 255), font=font_small)

    img.save(LOGO_PATH)
    print(f'Logo created: {LOGO_PATH}')


def create_brochure():
    """Create a 12-page marketing brochure PDF with realistic content."""
    os.makedirs(f'{WORKDIR}/marketing', exist_ok=True)

    doc = pymupdf.open()
    W, H = 595, 842  # A4

    pages_content = [
        {
            "title": "Vertex Digital Solutions",
            "subtitle": "Transforming Business Through Technology",
            "body": (
                "At Vertex Digital Solutions, we empower organizations to thrive in the digital age. "
                "Founded in 2018, we have partnered with over 350 enterprises across North America and "
                "Europe to deliver cutting-edge digital transformation strategies.\n\n"
                "Our team of 120+ specialists brings deep expertise in cloud architecture, data analytics, "
                "cybersecurity, and AI-driven automation. We don't just implement technology — we build "
                "lasting partnerships that drive measurable business outcomes."
            ),
        },
        {
            "title": "Our Services",
            "subtitle": "Comprehensive Digital Transformation",
            "body": (
                "Cloud Infrastructure & Migration\n"
                "We design and implement scalable cloud architectures on AWS, Azure, and Google Cloud. "
                "Our migration framework has achieved 99.7% uptime across all client deployments.\n\n"
                "Data Analytics & Business Intelligence\n"
                "Turn raw data into strategic insights. Our analytics platform processes over 2.4 billion "
                "data points daily for clients in finance, healthcare, and retail.\n\n"
                "Cybersecurity Solutions\n"
                "Protect your digital assets with our comprehensive security suite, including threat detection, "
                "compliance management, and incident response services."
            ),
        },
        {
            "title": "AI & Automation",
            "subtitle": "Intelligent Process Optimization",
            "body": (
                "Machine Learning Operations (MLOps)\n"
                "Deploy and manage ML models at scale with our end-to-end MLOps pipeline. Average model "
                "deployment time reduced from 6 weeks to 3 days.\n\n"
                "Robotic Process Automation\n"
                "Automate repetitive business processes with our RPA solutions. Clients report an average "
                "68% reduction in manual processing time and 94% accuracy improvement.\n\n"
                "Natural Language Processing\n"
                "Build intelligent document processing systems, chatbots, and sentiment analysis tools "
                "powered by state-of-the-art NLP models."
            ),
        },
        {
            "title": "Case Study: Meridian Healthcare",
            "subtitle": "Digital Transformation in Healthcare",
            "body": (
                "Challenge:\n"
                "Meridian Healthcare Group, operating 45 clinics across the Northeast, struggled with "
                "fragmented patient data systems and manual appointment scheduling.\n\n"
                "Solution:\n"
                "Vertex implemented a unified cloud-based patient management platform with AI-powered "
                "scheduling optimization and real-time analytics dashboards.\n\n"
                "Results:\n"
                "• 42% reduction in patient wait times\n"
                "• 89% improvement in data accessibility across clinics\n"
                "• $2.3M annual savings in administrative costs\n"
                "• Patient satisfaction scores increased from 72% to 91%"
            ),
        },
        {
            "title": "Case Study: Atlas Financial Group",
            "subtitle": "Securing Financial Infrastructure",
            "body": (
                "Challenge:\n"
                "Atlas Financial Group needed to modernize its legacy trading platform while maintaining "
                "strict regulatory compliance across 12 jurisdictions.\n\n"
                "Solution:\n"
                "Vertex designed a microservices-based trading architecture with real-time compliance "
                "monitoring, encrypted data pipelines, and automated regulatory reporting.\n\n"
                "Results:\n"
                "• Transaction processing speed improved by 340%\n"
                "• Zero compliance violations in 18 months post-deployment\n"
                "• $4.7M saved in annual compliance audit costs\n"
                "• System uptime of 99.99% achieved consistently"
            ),
        },
        {
            "title": "Industry Expertise",
            "subtitle": "Deep Domain Knowledge Across Sectors",
            "body": (
                "Financial Services\n"
                "Trading platforms, risk management, regulatory compliance, and fraud detection systems "
                "for banks, insurance companies, and investment firms.\n\n"
                "Healthcare & Life Sciences\n"
                "Electronic health records, telemedicine platforms, clinical trial data management, "
                "and HIPAA-compliant cloud infrastructure.\n\n"
                "Retail & E-commerce\n"
                "Personalization engines, inventory optimization, omnichannel experience platforms, "
                "and demand forecasting systems.\n\n"
                "Manufacturing\n"
                "IoT-enabled predictive maintenance, supply chain optimization, quality control automation, "
                "and digital twin implementation."
            ),
        },
        {
            "title": "Technology Partners",
            "subtitle": "Best-in-Class Technology Ecosystem",
            "body": (
                "We maintain premier partnerships with leading technology providers to ensure our "
                "clients benefit from the most advanced and reliable solutions available.\n\n"
                "Cloud Partners: AWS Advanced Consulting Partner, Microsoft Gold Partner, "
                "Google Cloud Premier Partner\n\n"
                "Data & AI: Databricks, Snowflake, Confluent, DataRobot\n\n"
                "Security: CrowdStrike, Palo Alto Networks, Okta, HashiCorp\n\n"
                "DevOps: GitLab, Docker, Kubernetes, Terraform\n\n"
                "Each partnership is backed by certified specialists who continuously update their "
                "expertise through ongoing training and certification programs."
            ),
        },
        {
            "title": "Our Methodology",
            "subtitle": "The Vertex Transformation Framework",
            "body": (
                "Phase 1: Discovery & Assessment (2-4 weeks)\n"
                "Comprehensive analysis of current systems, processes, and organizational readiness. "
                "Stakeholder interviews, technical audits, and gap analysis.\n\n"
                "Phase 2: Strategy & Architecture (3-6 weeks)\n"
                "Solution design, technology selection, roadmap development, and ROI modeling. "
                "Deliverables include detailed architecture diagrams and implementation plans.\n\n"
                "Phase 3: Implementation & Integration (8-16 weeks)\n"
                "Agile development sprints, continuous integration/delivery, and iterative testing. "
                "Weekly stakeholder updates and demo sessions.\n\n"
                "Phase 4: Optimization & Support (Ongoing)\n"
                "Performance monitoring, continuous improvement, and 24/7 technical support. "
                "Quarterly business reviews and technology roadmap updates."
            ),
        },
        {
            "title": "Client Testimonials",
            "subtitle": "What Our Partners Say",
            "body": (
                '"Vertex transformed our entire digital infrastructure in under six months. Their team\'s '
                'technical expertise and project management were exceptional."\n'
                "— Sarah Chen, CTO, Meridian Healthcare Group\n\n"
                '"The cybersecurity solution Vertex implemented gave us confidence to expand into new '
                'markets. Their compliance framework saved us millions in potential regulatory fines."\n'
                "— David Rodriguez, CISO, Atlas Financial Group\n\n"
                '"Working with Vertex felt like having an extension of our own team. They understood our '
                'business challenges and delivered solutions that exceeded our expectations."\n'
                "— Priya Sharma, VP Engineering, NovaTech Industries\n\n"
                '"The AI-powered analytics platform Vertex built has become the backbone of our '
                'decision-making process. Data-driven insights have increased our revenue by 23%."\n'
                "— Marcus Johnson, Director of Analytics, Pacific Retail Holdings"
            ),
        },
        {
            "title": "Awards & Recognition",
            "subtitle": "Industry Leadership",
            "body": (
                "2025 Gartner Magic Quadrant — Leader in Digital Transformation Services\n\n"
                "2024 Forrester Wave — Strong Performer in Cloud Migration Services\n\n"
                "2024 Deloitte Technology Fast 500 — Ranked #127\n\n"
                "2023 Stevie Award — Gold Winner for Innovation in Technology Services\n\n"
                "2023 Inc. 5000 — Fastest Growing Private Companies (#312)\n\n"
                "ISO 27001 Certified — Information Security Management\n\n"
                "SOC 2 Type II Compliant — Service Organization Controls\n\n"
                "Our commitment to excellence is reflected in our 97% client retention rate "
                "and an average NPS score of 82 across all service lines."
            ),
        },
        {
            "title": "Global Presence",
            "subtitle": "Offices Worldwide",
            "body": (
                "North America\n"
                "• New York City (Headquarters) — 450 Park Avenue, Suite 2200\n"
                "• San Francisco — 101 California Street, Suite 1500\n"
                "• Toronto — 100 King Street West, Suite 3400\n"
                "• Chicago — 233 South Wacker Drive, Suite 4800\n\n"
                "Europe\n"
                "• London — 30 St Mary Axe, Level 12\n"
                "• Berlin — Friedrichstraße 68, 4th Floor\n"
                "• Amsterdam — Keizersgracht 391, 3rd Floor\n\n"
                "Asia-Pacific\n"
                "• Singapore — One Raffles Quay, North Tower, Level 35\n"
                "• Sydney — 200 George Street, Level 17\n\n"
                "With teams across 9 offices and remote specialists in 15 countries, we deliver "
                "seamless service regardless of your geographic footprint."
            ),
        },
        {
            "title": "Get Started Today",
            "subtitle": "Partner With Vertex Digital Solutions",
            "body": (
                "Ready to accelerate your digital transformation journey? Our team is here to help "
                "you navigate the complexities of modern technology and unlock new business value.\n\n"
                "Schedule a Free Consultation\n"
                "Contact our solutions architects for a no-obligation assessment of your current "
                "technology landscape and transformation opportunities.\n\n"
                "Email: partnerships@vertexdigital.com\n"
                "Phone: +1 (212) 555-0147\n"
                "Web: www.vertexdigitalsolutions.com\n\n"
                "Follow Us\n"
                "LinkedIn: /company/vertex-digital-solutions\n"
                "Twitter: @VertexDigital\n\n"
                "© 2025 Vertex Digital Solutions. All rights reserved.\n"
                "Privacy Policy | Terms of Service | Cookie Policy"
            ),
        },
    ]

    for i, content in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        # Header bar
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, W, 80))
        shape.finish(fill=(0, 0.322, 0.533), color=(0, 0.322, 0.533))  # Dark blue
        shape.commit()

        # Title in header
        page.insert_text(
            pymupdf.Point(50, 50),
            content["title"],
            fontsize=22,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Subtitle
        page.insert_text(
            pymupdf.Point(50, 110),
            content["subtitle"],
            fontsize=14,
            fontname="heit",
            color=(0, 0.322, 0.533),
        )

        # Divider line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(50, 125), pymupdf.Point(545, 125))
        shape2.finish(color=(0.78, 0.62, 0.19), width=2)
        shape2.commit()

        # Body text
        body_rect = pymupdf.Rect(50, 145, 545, 790)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Footer
        footer_text = f"Vertex Digital Solutions  |  Confidential  |  Page {i + 1} of 12"
        page.insert_text(
            pymupdf.Point(50, 820),
            footer_text,
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(BROCHURE_PATH)
    doc.close()
    print(f'Brochure created: {BROCHURE_PATH} (12 pages)')


def main():
    create_logo()
    create_brochure()

    # Open the brochure in Evince for the agent
    launch_gui(f'evince "{BROCHURE_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


main()
