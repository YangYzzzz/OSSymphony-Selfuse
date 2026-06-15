"""
Initial Setup: Merge PDFs - insert appendix after page 5 of main document
Task ID: pdf_gf1_023
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_023'
DOCS_DIR = f'{WORKDIR}/Documents'

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

def create_main_document():
    """Create a 10-page technical report PDF."""
    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    margin = 72
    content_width = W - 2 * margin

    # Page 1: Title page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 200), "Advanced Network Infrastructure",
                     fontsize=24, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(margin, 240), "Technical Assessment Report",
                     fontsize=20, fontname="helv", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(margin, 300), "Prepared by: Meridian Systems Engineering",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(margin, 320), "Date: March 15, 2025",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(margin, 340), "Document Reference: MSE-2025-NET-0471",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(margin, 360), "Classification: Internal Use Only",
                     fontsize=12, fontname="hebo", color=(0.6, 0.1, 0.1))

    # Page 2: Table of Contents
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "Table of Contents",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    toc_items = [
        "1. Executive Summary .......................... 3",
        "2. Current Infrastructure Overview ............ 4",
        "3. Performance Analysis ....................... 5",
        "4. Security Assessment ........................ 6",
        "5. Capacity Planning .......................... 7",
        "6. Recommendations ............................ 8",
        "7. Implementation Timeline .................... 9",
        "8. Budget Estimates ........................... 10",
    ]
    y = 110
    for item in toc_items:
        page.insert_text(pymupdf.Point(margin, y), item,
                         fontsize=12, fontname="helv", color=(0, 0, 0))
        y += 22

    # Page 3: Executive Summary
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "1. Executive Summary",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 400),
        "This report presents a comprehensive assessment of the corporate network infrastructure "
        "at Meridian Systems. Over the past quarter, our engineering team conducted detailed "
        "analyses of network performance, security posture, and capacity utilization across all "
        "regional data centers. Key findings indicate that the current backbone operates at 73% "
        "average utilization during peak hours, with latency spikes observed in the Asia-Pacific "
        "region reaching 145ms. The security audit identified 12 medium-severity vulnerabilities "
        "in the perimeter firewall configuration and 3 high-severity issues in the VPN gateway "
        "authentication module. We recommend a phased upgrade approach starting with the core "
        "switching fabric, followed by WAN optimization and security hardening measures. The "
        "estimated budget for the complete infrastructure modernization is $2.4M over 18 months.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 4: Current Infrastructure Overview
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "2. Current Infrastructure Overview",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 500),
        "The existing network infrastructure comprises three primary data centers located in "
        "San Jose (US-West), Chicago (US-Central), and Frankfurt (EU-Central). Each facility "
        "houses redundant core switches (Cisco Nexus 9500 series) with 40GbE uplinks to the "
        "WAN backbone. The access layer consists of 847 Catalyst 9300 switches serving "
        "approximately 12,400 endpoint devices across 23 office locations.\n\n"
        "The WAN connectivity is provided through a hybrid MPLS/SD-WAN architecture with "
        "primary circuits from AT&T (500 Mbps per site) and backup Internet links from Comcast "
        "and Lumen Technologies. The SD-WAN overlay (Cisco Viptela) manages traffic steering "
        "across 156 branch office connections.\n\n"
        "Current monitoring is performed through a centralized Nagios XI deployment with 4,200 "
        "active service checks. The NOC team operates on a 24/7 rotation with an average "
        "incident response time of 14 minutes for P1 events.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 5: Performance Analysis
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "3. Performance Analysis",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 500),
        "Network performance metrics collected over the Q4 2024 period reveal several areas "
        "of concern. The core backbone averaged 73% utilization during business hours (08:00-"
        "18:00 local time), with peaks reaching 91% on the San Jose-Chicago link during the "
        "monthly financial close process.\n\n"
        "Latency measurements across regions:\n"
        "  - US-West to US-Central: 28ms average (acceptable)\n"
        "  - US-West to EU-Central: 142ms average (marginal)\n"
        "  - US-Central to EU-Central: 89ms average (acceptable)\n"
        "  - US-West to AP-Southeast: 198ms average (exceeds SLA)\n"
        "  - Intra-campus (all sites): 2.1ms average (excellent)\n\n"
        "Packet loss rates remained below 0.01% on all MPLS circuits but reached 0.3% on "
        "several Internet-based SD-WAN tunnels during congestion events. The QoS policies "
        "successfully prioritized voice and video traffic, maintaining MOS scores above 4.1 "
        "for all unified communications sessions.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 6: Security Assessment
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "4. Security Assessment",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 500),
        "The security audit conducted in January 2025 identified a total of 15 vulnerabilities "
        "across the network infrastructure. Three items were classified as high severity:\n\n"
        "  1. CVE-2024-20356: Cisco IOS XE Web UI privilege escalation (CVSS 8.6)\n"
        "     Affected devices: 12 Catalyst 9300 switches running IOS XE 17.6.x\n"
        "     Remediation: Upgrade to IOS XE 17.9.4 (scheduled for Feb 2025)\n\n"
        "  2. Expired SSL certificates on 3 VPN concentrators\n"
        "     Risk: Man-in-the-middle attacks on remote access VPN sessions\n"
        "     Remediation: Certificate renewal completed on Jan 22, 2025\n\n"
        "  3. Default SNMP community strings on 47 legacy devices\n"
        "     Risk: Unauthorized read/write access to device configurations\n"
        "     Remediation: SNMPv3 migration in progress (67% complete)\n\n"
        "The perimeter firewall (Palo Alto PA-5260) rule base contains 2,847 rules, of which "
        "312 are identified as redundant or shadowed. A firewall policy optimization project "
        "is recommended to reduce the attack surface.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 7: Capacity Planning
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "5. Capacity Planning",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 500),
        "Based on the current growth trajectory of 18% year-over-year increase in network "
        "traffic, the existing infrastructure will reach capacity limits within 14 months. The "
        "following capacity upgrades are recommended:\n\n"
        "Core Network:\n"
        "  - Upgrade backbone links from 40GbE to 100GbE (Q2 2025)\n"
        "  - Add redundant core switches at Chicago DC (Q3 2025)\n"
        "  - Deploy spine-leaf architecture at San Jose DC (Q4 2025)\n\n"
        "WAN Connectivity:\n"
        "  - Increase MPLS circuit bandwidth to 1 Gbps at top 10 sites\n"
        "  - Deploy dedicated Internet DIA circuits for cloud traffic\n"
        "  - Implement Zscaler Internet Access for SaaS optimization\n\n"
        "Wireless Infrastructure:\n"
        "  - Upgrade to Wi-Fi 6E (802.11ax) at headquarters and 5 largest offices\n"
        "  - Deploy IoT-dedicated SSIDs with micro-segmentation\n"
        "  - Add 240 additional access points across 8 growing office locations",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 8: Recommendations
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "6. Recommendations",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 500),
        "Based on our comprehensive analysis, we recommend the following strategic initiatives:\n\n"
        "Priority 1 (Immediate - within 30 days):\n"
        "  - Patch all high-severity vulnerabilities (3 items)\n"
        "  - Complete SNMPv3 migration on remaining 33% of devices\n"
        "  - Renew all expiring SSL/TLS certificates\n\n"
        "Priority 2 (Short-term - Q2 2025):\n"
        "  - Begin backbone upgrade to 100GbE\n"
        "  - Optimize firewall rule base (remove 312 redundant rules)\n"
        "  - Deploy network automation (Ansible + Terraform)\n\n"
        "Priority 3 (Medium-term - Q3-Q4 2025):\n"
        "  - Implement spine-leaf architecture at primary DC\n"
        "  - Deploy Zscaler for cloud traffic optimization\n"
        "  - Upgrade wireless infrastructure to Wi-Fi 6E\n\n"
        "Priority 4 (Long-term - 2026):\n"
        "  - Evaluate 400GbE for inter-DC backbone\n"
        "  - Implement AIOps for predictive network management\n"
        "  - Complete zero-trust network architecture rollout",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 9: Implementation Timeline
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "7. Implementation Timeline",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 500),
        "The proposed implementation follows a phased approach over 18 months:\n\n"
        "Phase 1: Foundation (April - June 2025)\n"
        "  - Security remediation and compliance hardening\n"
        "  - Network automation framework deployment\n"
        "  - Monitoring system upgrade (Nagios XI to Datadog)\n"
        "  Duration: 12 weeks | Team: 4 network engineers\n\n"
        "Phase 2: Core Upgrade (July - September 2025)\n"
        "  - Backbone 100GbE migration (weekend maintenance windows)\n"
        "  - Chicago DC redundancy build-out\n"
        "  - WAN circuit upgrades at priority sites\n"
        "  Duration: 14 weeks | Team: 6 network engineers + vendor support\n\n"
        "Phase 3: Optimization (October 2025 - March 2026)\n"
        "  - Spine-leaf deployment at San Jose DC\n"
        "  - Wi-Fi 6E rollout across offices\n"
        "  - Cloud connectivity optimization\n"
        "  - Zero-trust architecture pilot\n"
        "  Duration: 24 weeks | Team: 8 network engineers\n\n"
        "Total project duration: 52 weeks (with 4-week buffer)",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 10: Budget Estimates
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "8. Budget Estimates",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(margin, 100, W - margin, 500),
        "The total estimated investment for the network modernization program is $2,415,000 "
        "distributed across the following categories:\n\n"
        "Hardware:\n"
        "  - Core switches (Nexus 9500 upgrades): $485,000\n"
        "  - 100GbE optics and cabling: $127,000\n"
        "  - Wi-Fi 6E access points (240 units): $192,000\n"
        "  - Wireless controllers: $68,000\n"
        "  Hardware subtotal: $872,000\n\n"
        "Software & Licensing:\n"
        "  - SD-WAN license renewals (3-year): $234,000\n"
        "  - Zscaler Internet Access (annual): $156,000\n"
        "  - Datadog monitoring (annual): $89,000\n"
        "  - Network automation tools: $45,000\n"
        "  Software subtotal: $524,000\n\n"
        "Services:\n"
        "  - Professional services (vendor): $380,000\n"
        "  - Internal labor (overtime/backfill): $285,000\n"
        "  - Training and certification: $54,000\n"
        "  Services subtotal: $719,000\n\n"
        "Contingency (15%): $300,000\n"
        "Grand Total: $2,415,000",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    doc.save(f'{DOCS_DIR}/main_document.pdf')
    doc.close()
    print(f'Created main_document.pdf with {10} pages')

def create_appendix():
    """Create a 4-page appendix PDF with supporting data tables."""
    doc = pymupdf.open()
    W, H = 612, 792
    margin = 72

    # Page 1: Appendix Title + Bandwidth Utilization Table
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "Appendix: Supporting Data Tables",
                     fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(margin, 110), "Table A-1: Monthly Bandwidth Utilization (Gbps)",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    table_data = [
        ["Month", "SJ-CHI", "SJ-FRA", "CHI-FRA", "Peak %"],
        ["Jul 2024", "28.4", "18.7", "15.2", "71%"],
        ["Aug 2024", "30.1", "19.3", "16.0", "75%"],
        ["Sep 2024", "32.8", "20.5", "16.8", "82%"],
        ["Oct 2024", "29.6", "19.1", "15.9", "74%"],
        ["Nov 2024", "34.2", "21.8", "17.5", "86%"],
        ["Dec 2024", "36.5", "22.4", "18.1", "91%"],
    ]
    y = 140
    for i, row in enumerate(table_data):
        x = margin
        font = "hebo" if i == 0 else "helv"
        for val in row:
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=font, color=(0, 0, 0))
            x += 95
        y += 18

    page.insert_text(pymupdf.Point(margin, y + 20), "Table A-2: Latency Measurements (ms) - P50/P95/P99",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    latency_data = [
        ["Route", "P50", "P95", "P99"],
        ["US-West <-> US-Central", "28", "45", "67"],
        ["US-West <-> EU-Central", "142", "178", "215"],
        ["US-Central <-> EU-Central", "89", "112", "138"],
        ["US-West <-> AP-Southeast", "198", "245", "312"],
        ["Intra-campus (avg)", "2.1", "5.8", "11.2"],
    ]
    y = y + 50
    for i, row in enumerate(latency_data):
        x = margin
        font = "hebo" if i == 0 else "helv"
        for val in row:
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=font, color=(0, 0, 0))
            x += 130
        y += 18

    # Page 2: Device Inventory
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "Table A-3: Network Device Inventory Summary",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    inventory = [
        ["Device Type", "Model", "Count", "Avg Age", "Status"],
        ["Core Switch", "Nexus 9500", "6", "3.2 yr", "Active"],
        ["Dist Switch", "Nexus 5600", "24", "4.1 yr", "Active"],
        ["Access Switch", "Cat 9300", "847", "2.8 yr", "Active"],
        ["Router", "ASR 1001-X", "18", "3.7 yr", "Active"],
        ["Firewall", "PA-5260", "4", "2.1 yr", "Active"],
        ["Firewall", "PA-850", "46", "3.5 yr", "Active"],
        ["VPN Gateway", "ASA 5545-X", "8", "5.2 yr", "EOL Soon"],
        ["WLC", "C9800-40", "6", "1.8 yr", "Active"],
        ["Access Point", "AP C9120AXI", "1,847", "2.4 yr", "Active"],
        ["Load Balancer", "F5 i4800", "4", "2.9 yr", "Active"],
    ]
    y = 100
    for i, row in enumerate(inventory):
        x = margin
        font = "hebo" if i == 0 else "helv"
        col_widths = [100, 100, 55, 65, 75]
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=font, color=(0, 0, 0))
            x += col_widths[j]
        y += 18

    page.insert_text(pymupdf.Point(margin, y + 20), "Table A-4: Circuit Inventory",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    circuits = [
        ["Circuit ID", "Provider", "Type", "Bandwidth", "MRC"],
        ["MPLS-SJ-001", "AT&T", "MPLS", "500 Mbps", "$4,200"],
        ["MPLS-CHI-001", "AT&T", "MPLS", "500 Mbps", "$3,800"],
        ["MPLS-FRA-001", "Deutsche Telekom", "MPLS", "200 Mbps", "$5,100"],
        ["DIA-SJ-001", "Comcast", "DIA", "1 Gbps", "$1,200"],
        ["DIA-CHI-001", "Lumen", "DIA", "1 Gbps", "$1,100"],
        ["VPN-BRANCH", "Various", "IPSec VPN", "100 Mbps", "$890/site"],
    ]
    y = y + 50
    for i, row in enumerate(circuits):
        x = margin
        font = "hebo" if i == 0 else "helv"
        col_widths = [95, 110, 70, 80, 75]
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=font, color=(0, 0, 0))
            x += col_widths[j]
        y += 18

    # Page 3: Vulnerability Details
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "Table A-5: Vulnerability Assessment Results",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    vulns = [
        ["ID", "Severity", "CVSS", "Description", "Status"],
        ["V-001", "High", "8.6", "IOS XE Web UI priv escalation", "Open"],
        ["V-002", "High", "7.8", "Expired VPN SSL certificates", "Remediated"],
        ["V-003", "High", "7.5", "Default SNMP community strings", "In Progress"],
        ["V-004", "Medium", "6.2", "Outdated NTP configuration", "Open"],
        ["V-005", "Medium", "5.9", "Weak SSH key exchange algos", "Open"],
        ["V-006", "Medium", "5.7", "Unencrypted syslog transport", "Open"],
        ["V-007", "Medium", "5.5", "Missing BPDU guard on access", "Open"],
        ["V-008", "Medium", "5.3", "ARP inspection not enabled", "Open"],
        ["V-009", "Medium", "5.1", "TACACS+ fallback to local", "Open"],
        ["V-010", "Medium", "4.8", "Redundant firewall rules", "Open"],
        ["V-011", "Low", "3.5", "Banner message non-compliant", "Open"],
        ["V-012", "Low", "3.2", "DNS resolver misconfiguration", "Open"],
        ["V-013", "Low", "2.8", "Unused VLAN interfaces up", "Open"],
        ["V-014", "Low", "2.5", "Missing interface descriptions", "Open"],
        ["V-015", "Low", "2.1", "Console timeout > 10 min", "Open"],
    ]
    y = 100
    col_widths = [50, 65, 45, 230, 80]
    for i, row in enumerate(vulns):
        x = margin
        font = "hebo" if i == 0 else "helv"
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(x, y), val, fontsize=9, fontname=font, color=(0, 0, 0))
            x += col_widths[j]
        y += 16

    # Page 4: Cost Breakdown Details
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin, 72), "Table A-6: Detailed Cost Breakdown by Phase",
                     fontsize=13, fontname="hebo", color=(0, 0, 0))
    costs = [
        ["Phase", "Category", "Item", "Cost"],
        ["Phase 1", "Security", "IOS XE patches (labor)", "$18,000"],
        ["Phase 1", "Security", "SNMPv3 migration (labor)", "$24,000"],
        ["Phase 1", "Software", "Datadog deployment", "$89,000"],
        ["Phase 1", "Services", "Automation framework", "$45,000"],
        ["Phase 2", "Hardware", "Nexus 9500 line cards", "$485,000"],
        ["Phase 2", "Hardware", "100GbE optics + cabling", "$127,000"],
        ["Phase 2", "Services", "Vendor installation", "$180,000"],
        ["Phase 2", "Software", "SD-WAN renewals", "$234,000"],
        ["Phase 3", "Hardware", "Wi-Fi 6E APs (240)", "$192,000"],
        ["Phase 3", "Hardware", "Wireless controllers", "$68,000"],
        ["Phase 3", "Software", "Zscaler (annual)", "$156,000"],
        ["Phase 3", "Services", "Pro services", "$200,000"],
        ["Phase 3", "Services", "Training", "$54,000"],
        ["All", "Buffer", "Contingency (15%)", "$300,000"],
    ]
    y = 100
    col_widths = [70, 80, 210, 80]
    for i, row in enumerate(costs):
        x = margin
        font = "hebo" if i == 0 else "helv"
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=font, color=(0, 0, 0))
            x += col_widths[j]
        y += 18

    page.insert_text(pymupdf.Point(margin, y + 30),
                     "Note: All costs are estimates based on current vendor pricing as of Q1 2025.",
                     fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(margin, y + 45),
                     "Actual costs may vary by +/- 10% depending on negotiated discounts and scope changes.",
                     fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))

    doc.save(f'{DOCS_DIR}/appendix.pdf')
    doc.close()
    print(f'Created appendix.pdf with {4} pages')


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Create source PDFs
    create_main_document()
    create_appendix()

    # Verify page counts
    main_doc = pymupdf.open(f'{DOCS_DIR}/main_document.pdf')
    app_doc = pymupdf.open(f'{DOCS_DIR}/appendix.pdf')
    print(f'main_document.pdf: {len(main_doc)} pages')
    print(f'appendix.pdf: {len(app_doc)} pages')
    main_doc.close()
    app_doc.close()

    # Do NOT create document_with_appendix.pdf - that is the task for the agent

    # Open file manager to show Documents folder
    launch_gui(f'nautilus "{DOCS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus with DISPLAY=:0')


main()
