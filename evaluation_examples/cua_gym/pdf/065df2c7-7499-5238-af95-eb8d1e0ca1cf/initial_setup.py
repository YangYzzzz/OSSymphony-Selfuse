"""
Initial Setup: Create a smart city infrastructure proposal PDF with metadata.
Task ID: pdf_mbc_011
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_011'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/project_proposal.pdf'

LETTER_W, LETTER_H = 612, 792  # Letter size in points


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Remove properties.txt if it exists (initial must NOT have it)
    props_path = f'{DOCS_DIR}/properties.txt'
    if os.path.exists(props_path):
        os.remove(props_path)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(150, 250), "Smart City Infrastructure", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(220, 290), "Proposal", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(180, 360), "Prepared by: Urban Planning Dept", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(210, 390), "Date: March 15, 2025", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(160, 430), "Revision: 2.1 | Classification: Internal", fontsize=11, fontname="heit", color=(0.5, 0.5, 0.5))
    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(100, 310), pymupdf.Point(512, 310))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.5))
    summary_text = (
        "This proposal outlines a comprehensive plan to deploy smart city infrastructure across "
        "the metropolitan area over a 36-month period. The initiative encompasses IoT sensor networks, "
        "intelligent traffic management systems, environmental monitoring stations, and a centralized "
        "data analytics platform. The estimated budget for Phase 1 is $14.2 million, with projected "
        "annual savings of $3.8 million in operational costs once fully deployed.\n\n"
        "Key objectives include reducing traffic congestion by 25%, improving emergency response times "
        "by 40%, and achieving real-time environmental monitoring across 95% of the urban core. The "
        "project will leverage existing fiber optic infrastructure and 5G networks to minimize "
        "deployment costs while maximizing data throughput.\n\n"
        "Stakeholder engagement sessions conducted between January and February 2025 indicate strong "
        "community support, with 78% of surveyed residents favoring the initiative. The city council "
        "has allocated preliminary funding of $5.6 million for the first fiscal quarter."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Project Scope ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "2. Project Scope", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.5))
    scope_text = (
        "2.1 IoT Sensor Network\n\n"
        "The deployment will include 3,500 multi-purpose sensors distributed across 12 districts. "
        "Each sensor node integrates air quality monitoring (PM2.5, NO2, O3), temperature and humidity "
        "sensors, acoustic level detectors, and pedestrian/vehicle counting modules. Communication "
        "relies on LoRaWAN gateways with 5G fallback for critical data streams.\n\n"
        "2.2 Traffic Management System\n\n"
        "Adaptive signal controllers will replace legacy timing systems at 240 intersections. These "
        "controllers use real-time camera feeds processed through edge computing nodes to dynamically "
        "adjust signal phases. Vehicle-to-infrastructure (V2I) communication will be piloted at 50 "
        "intersections along the Highway 101 corridor.\n\n"
        "2.3 Environmental Monitoring\n\n"
        "Fifteen fixed monitoring stations and 30 mobile units will track air quality, noise levels, "
        "and water quality in real time. Data feeds into the central analytics platform and triggers "
        "automated alerts when thresholds are exceeded."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), scope_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 4: Technical Architecture ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "3. Technical Architecture", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.5))
    arch_text = (
        "The system architecture follows a three-tier model:\n\n"
        "Edge Layer: Local processing at sensor nodes and intersection controllers. Each edge node "
        "runs a lightweight analytics engine capable of real-time anomaly detection without cloud "
        "dependency. Expected latency: <50ms for critical alerts.\n\n"
        "Network Layer: LoRaWAN for low-bandwidth sensor data (up to 50 kbps), 5G NR for high-bandwidth "
        "video and V2I communications (up to 1 Gbps). Redundant fiber backbone connects all district "
        "hubs with 99.99% uptime SLA.\n\n"
        "Cloud Layer: Hosted on a hybrid cloud (Azure + on-premise data center at City Hall). "
        "The analytics platform processes approximately 2.4 TB of data per day, utilizing Apache Kafka "
        "for stream ingestion, Spark for batch analytics, and a PostgreSQL/TimescaleDB cluster for "
        "time-series storage.\n\n"
        "Security: End-to-end TLS 1.3 encryption, mutual authentication for all IoT devices, and "
        "a zero-trust network architecture with microsegmentation."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), arch_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 5: Budget & Timeline ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "4. Budget & Timeline", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.5))
    budget_text = (
        "Phase 1 (Months 1-12): Core Infrastructure Deployment\n"
        "  - IoT sensor procurement and installation: $4,200,000\n"
        "  - Traffic controller upgrades (80 intersections): $2,800,000\n"
        "  - Network infrastructure (LoRaWAN gateways, 5G nodes): $3,100,000\n"
        "  - Cloud platform setup and integration: $1,500,000\n"
        "  - Project management and contingency: $2,600,000\n"
        "  Phase 1 Total: $14,200,000\n\n"
        "Phase 2 (Months 13-24): Expansion & Optimization\n"
        "  - Additional sensor deployment (2,000 units): $3,600,000\n"
        "  - Remaining intersection upgrades (160): $5,100,000\n"
        "  - Advanced analytics modules: $2,200,000\n"
        "  - Community engagement platforms: $800,000\n"
        "  Phase 2 Total: $11,700,000\n\n"
        "Phase 3 (Months 25-36): Full Operation & V2I Pilot\n"
        "  - V2I pilot deployment: $3,400,000\n"
        "  - System optimization and scaling: $1,800,000\n"
        "  - Training and documentation: $600,000\n"
        "  Phase 3 Total: $5,800,000\n\n"
        "Grand Total: $31,700,000"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), budget_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 6: Risk Assessment ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "5. Risk Assessment", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.5))
    risk_text = (
        "5.1 Technical Risks\n\n"
        "Sensor failure rate: Estimated at 2-3% annually based on manufacturer data. Mitigation: "
        "redundant sensors in critical zones, 24-month warranty, and predictive maintenance algorithm.\n\n"
        "Network congestion: Peak data volumes may exceed initial capacity estimates. Mitigation: "
        "dynamic bandwidth allocation, edge computing offloading, and phased deployment to spread load.\n\n"
        "5.2 Financial Risks\n\n"
        "Cost overruns: Hardware procurement costs may fluctuate due to global supply chain conditions. "
        "Mitigation: 15% contingency budget, multi-vendor sourcing strategy, and phased procurement.\n\n"
        "5.3 Operational Risks\n\n"
        "Public resistance: Privacy concerns related to surveillance-capable sensors. Mitigation: "
        "strict data anonymization policies, public advisory board, and transparent data usage reports "
        "published quarterly.\n\n"
        "Cybersecurity incidents: IoT devices present expanded attack surface. Mitigation: dedicated "
        "SOC monitoring, automated patch management, and regular penetration testing."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), risk_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 7: Implementation Team ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "6. Implementation Team", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.5))
    team_text = (
        "Project Director: Dr. Elena Vasquez, Chief Technology Officer\n"
        "  - 15 years experience in municipal technology projects\n"
        "  - Led the citywide fiber optic deployment (2019-2021)\n\n"
        "Technical Lead: Marcus Chen, Senior Infrastructure Architect\n"
        "  - IoT systems specialist with deployments in 3 smart city projects\n"
        "  - AWS/Azure certified solutions architect\n\n"
        "Operations Manager: Priya Sharma, Director of Urban Services\n"
        "  - Oversees 340 field technicians across 12 districts\n"
        "  - Background in traffic engineering and logistics\n\n"
        "Data Science Lead: Dr. James Okafor, Principal Data Scientist\n"
        "  - PhD in Machine Learning from MIT\n"
        "  - Published 28 papers on urban analytics\n\n"
        "Security Architect: Sarah Lindgren, CISO\n"
        "  - Former NSA cybersecurity analyst\n"
        "  - Certified CISSP, CISM, and CEH\n\n"
        "Community Liaison: David Tanaka, Public Affairs Director\n"
        "  - 10 years in government communications\n"
        "  - Managed stakeholder engagement for transit expansion project"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), team_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 8: Conclusion & Next Steps ---
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    page.insert_text(pymupdf.Point(72, 72), "7. Conclusion & Next Steps", fontsize=20, fontname="hebo", color=(0.1, 0.2, 0.5))
    conclusion_text = (
        "The Smart City Infrastructure initiative represents a transformative investment in the "
        "metropolitan area's future. By integrating IoT sensors, adaptive traffic management, and "
        "advanced data analytics, the city will achieve measurable improvements in livability, "
        "sustainability, and operational efficiency.\n\n"
        "Immediate Next Steps:\n\n"
        "1. City council vote on Phase 1 funding (April 2025)\n"
        "2. Release RFP for IoT sensor procurement (May 2025)\n"
        "3. Finalize vendor selection and contracts (July 2025)\n"
        "4. Begin pilot installation in District 7 (September 2025)\n"
        "5. First public progress report (December 2025)\n\n"
        "We recommend scheduling a detailed technical briefing with the council's technology "
        "subcommittee to review the architecture specifications and address any remaining questions "
        "before the funding vote.\n\n"
        "For questions or additional information, please contact:\n"
        "Dr. Elena Vasquez, CTO\n"
        "Email: e.vasquez@cityplanning.gov\n"
        "Phone: (555) 234-8901\n\n"
        "Urban Planning Department\n"
        "City Hall, Suite 420\n"
        "Metropolitan Area, ST 10001"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 720), conclusion_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Set metadata
    doc.set_metadata({
        "title": "Smart City Infrastructure Proposal",
        "author": "Urban Planning Dept",
        "subject": "Infrastructure",
        "keywords": "smart city, IoT, sensors",
        "creator": "LibreOffice Writer",
        "producer": "LibreOffice 7.5",
        "creationDate": "D:20250315100000+00'00'",
        "modDate": "D:20250315143000+00'00'",
    })

    # Set TOC/bookmarks
    toc = [
        [1, "Executive Summary", 2],
        [1, "Project Scope", 3],
        [1, "Technical Architecture", 4],
        [1, "Budget & Timeline", 5],
        [1, "Risk Assessment", 6],
        [1, "Implementation Team", 7],
        [1, "Conclusion & Next Steps", 8],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
