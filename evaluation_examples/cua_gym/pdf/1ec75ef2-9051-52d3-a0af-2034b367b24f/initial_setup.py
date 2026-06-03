"""
Initial Setup: Create a 45-page manual PDF with no page numbers.
Task ID: pdf_ro_012
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_012'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/manual.pdf'

# Page dimensions: Letter size
PAGE_W = 612
PAGE_H = 792

# Chapter structure for a realistic technical manual
CHAPTERS = [
    ("Introduction to Network Administration", [
        "This manual provides a comprehensive guide to network administration for "
        "enterprise environments. It covers essential topics including network topology "
        "design, security configuration, monitoring, and troubleshooting procedures.",
        "Network administrators play a critical role in maintaining the reliability and "
        "security of organizational IT infrastructure. The principles outlined in this "
        "manual are based on industry best practices and years of operational experience.",
        "Throughout this manual, you will find practical examples, configuration templates, "
        "and step-by-step procedures that can be adapted to your specific environment.",
    ]),
    ("Network Topology and Architecture", [
        "A well-designed network topology is the foundation of reliable infrastructure. "
        "This chapter covers the primary topologies used in enterprise environments: "
        "star, mesh, hybrid, and spine-leaf architectures.",
        "When selecting a topology, consider factors such as scalability requirements, "
        "fault tolerance needs, budget constraints, and the physical layout of your "
        "facilities. Each topology has distinct advantages and trade-offs.",
        "The spine-leaf architecture has become the standard for modern data centers, "
        "providing consistent latency, easy scalability, and simplified management. "
        "A typical spine-leaf design uses two tiers of switches with full mesh connectivity.",
    ]),
    ("IP Address Management", [
        "Effective IP address management (IPAM) is essential for maintaining an organized "
        "and efficient network. This chapter covers subnet planning, DHCP configuration, "
        "and DNS integration strategies.",
        "For enterprise networks, the recommended practice is to use RFC 1918 private "
        "address ranges: 10.0.0.0/8 for large organizations, 172.16.0.0/12 for medium "
        "deployments, and 192.168.0.0/16 for smaller networks.",
        "DHCP servers should be configured with appropriate lease times based on device "
        "types. Workstations typically use 8-hour leases, while servers and infrastructure "
        "devices should use static reservations.",
    ]),
    ("VLAN Configuration", [
        "Virtual LANs provide logical segmentation of network traffic, improving security "
        "and performance. This chapter details VLAN planning, trunk configuration, and "
        "inter-VLAN routing procedures.",
        "A standard VLAN assignment scheme includes: VLAN 10 for management, VLAN 20 for "
        "servers, VLAN 30 for workstations, VLAN 40 for VoIP, VLAN 50 for guest access, "
        "and VLAN 99 for native/untagged traffic.",
        "Inter-VLAN routing can be implemented using a Layer 3 switch or a router-on-a-stick "
        "configuration. Layer 3 switching is preferred for high-performance environments.",
    ]),
    ("Firewall and Security Policies", [
        "Network security begins with a well-configured firewall. This chapter covers "
        "firewall rule design, zone-based security, and intrusion prevention systems.",
        "The principle of least privilege should guide all firewall rules. Start with a "
        "default-deny policy and explicitly allow only necessary traffic. Document every "
        "rule with a business justification and review date.",
        "Zone-based firewall configurations typically define these zones: TRUST (internal), "
        "UNTRUST (internet), DMZ (public-facing servers), and GUEST (visitor access). "
        "Traffic policies between zones must be carefully controlled.",
    ]),
    ("Wireless Network Deployment", [
        "Enterprise wireless networks require careful planning for coverage, capacity, and "
        "security. This chapter covers site surveys, access point placement, and wireless "
        "security configuration.",
        "Conduct a thorough RF site survey before deploying access points. Measure signal "
        "strength, noise levels, and interference sources. Target a minimum signal strength "
        "of -67 dBm for voice applications and -70 dBm for data.",
        "WPA3-Enterprise with 802.1X authentication is the recommended security standard. "
        "Configure RADIUS integration for centralized authentication and use certificate-based "
        "authentication where possible.",
    ]),
    ("Network Monitoring and Alerting", [
        "Proactive network monitoring enables early detection of issues before they impact "
        "users. This chapter covers SNMP configuration, syslog management, and alerting "
        "thresholds.",
        "Deploy monitoring using a combination of SNMP polling, NetFlow analysis, and "
        "synthetic monitoring. Key metrics to track include bandwidth utilization, packet "
        "loss, latency, and device CPU/memory usage.",
        "Configure alerting thresholds based on historical baselines. Typical thresholds: "
        "interface utilization above 80%, packet loss above 0.1%, latency above 50ms for "
        "LAN and 100ms for WAN links.",
    ]),
    ("Backup and Disaster Recovery", [
        "A robust backup and disaster recovery plan ensures business continuity during "
        "outages. This chapter covers configuration backup procedures, redundancy design, "
        "and failover testing.",
        "Network device configurations should be backed up daily using automated scripts. "
        "Store backups in at least two geographically separated locations. Use version "
        "control to track configuration changes over time.",
        "Disaster recovery testing should be conducted quarterly. Document recovery time "
        "objectives (RTO) and recovery point objectives (RPO) for each critical system. "
        "The target RTO for core network services is typically under 4 hours.",
    ]),
    ("VPN and Remote Access", [
        "Secure remote access is essential for distributed workforces. This chapter covers "
        "IPSec VPN, SSL VPN, and Zero Trust Network Access (ZTNA) implementations.",
        "Site-to-site VPN tunnels should use IKEv2 with AES-256-GCM encryption and "
        "SHA-384 integrity. Configure dead peer detection (DPD) with 30-second intervals "
        "and establish redundant tunnels for critical links.",
        "For remote user access, SSL VPN provides a flexible solution that works through "
        "most firewalls. Enforce multi-factor authentication and device posture checks "
        "before granting network access.",
    ]),
    ("Quality of Service (QoS)", [
        "Quality of Service policies ensure critical applications receive adequate bandwidth "
        "and priority. This chapter covers QoS classification, marking, queuing, and "
        "policing configurations.",
        "Classify traffic at the network edge using DSCP markings. Standard markings include: "
        "EF (46) for voice, AF41 (34) for video conferencing, AF21 (18) for critical data, "
        "and CS1 (8) for bulk/scavenger traffic.",
        "Apply strict priority queuing for real-time traffic (voice and video) with a bandwidth "
        "limit of 33% of link capacity. Use weighted fair queuing for remaining traffic classes.",
    ]),
    ("Network Automation", [
        "Network automation reduces manual errors and improves operational efficiency. "
        "This chapter covers automation tools, scripting practices, and configuration "
        "management frameworks.",
        "Ansible is the recommended tool for network configuration management. Create "
        "playbooks for common tasks: device provisioning, OS upgrades, configuration "
        "compliance checks, and backup collection.",
        "Python scripting with libraries such as Netmiko, NAPALM, and Nornir enables "
        "custom automation solutions. Maintain scripts in version control and include "
        "error handling, logging, and rollback capabilities.",
    ]),
    ("Troubleshooting Methodology", [
        "Systematic troubleshooting is essential for efficient problem resolution. This "
        "chapter presents a structured approach to diagnosing and resolving network issues.",
        "Follow the OSI model bottom-up approach: verify physical connectivity (Layer 1), "
        "check data link integrity (Layer 2), confirm IP addressing and routing (Layer 3), "
        "test transport connectivity (Layer 4), and validate application behavior (Layer 7).",
        "Document all troubleshooting steps and outcomes. Maintain a knowledge base of "
        "resolved issues with root causes and solutions. This information accelerates "
        "future troubleshooting and helps identify recurring problems.",
    ]),
    ("Compliance and Documentation", [
        "Maintaining accurate network documentation and compliance records is a regulatory "
        "requirement in many industries. This chapter covers documentation standards and "
        "audit preparation.",
        "Essential documentation includes: network diagrams (logical and physical), IP "
        "address inventories, device configuration archives, change management logs, and "
        "incident response procedures.",
        "Schedule regular compliance audits against frameworks such as NIST 800-53, ISO "
        "27001, or PCI DSS depending on your industry requirements. Automate compliance "
        "checks where possible to maintain continuous compliance.",
    ]),
    ("Appendix: Reference Tables", [
        "This appendix contains reference tables for common network administration tasks "
        "including port numbers, subnet masks, cable specifications, and protocol identifiers.",
        "Common TCP ports: SSH (22), HTTP (80), HTTPS (443), DNS (53), SMTP (25), "
        "IMAP (143), LDAP (389), RDP (3389), MySQL (3306), PostgreSQL (5432).",
        "Common subnet masks: /24 (255.255.255.0, 254 hosts), /25 (255.255.255.128, "
        "126 hosts), /26 (255.255.255.192, 62 hosts), /27 (255.255.255.224, 30 hosts), "
        "/28 (255.255.255.240, 14 hosts), /29 (255.255.255.248, 6 hosts).",
    ]),
    ("Appendix: Glossary", [
        "ACL - Access Control List: A set of rules that filter network traffic based on "
        "source, destination, protocol, and port criteria.",
        "BGP - Border Gateway Protocol: The routing protocol used to exchange routing "
        "information between autonomous systems on the internet.",
        "CIDR - Classless Inter-Domain Routing: A method for allocating IP addresses that "
        "replaces the older classful addressing system.",
        "DHCP - Dynamic Host Configuration Protocol: A protocol that automatically assigns "
        "IP addresses and network configuration to devices.",
        "EIGRP - Enhanced Interior Gateway Routing Protocol: A Cisco proprietary routing "
        "protocol that uses a composite metric based on bandwidth and delay.",
        "FHRP - First Hop Redundancy Protocol: Protocols like HSRP, VRRP, and GLBP that "
        "provide default gateway redundancy.",
    ]),
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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # We need 45 pages spread across 15 chapters
    # Each chapter gets 3 pages (15 * 3 = 45)
    page_num = 0
    for ch_idx, (title, paragraphs) in enumerate(CHAPTERS):
        chapter_num = ch_idx + 1

        # --- Page 1 of chapter: title page ---
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_num += 1

        # Chapter title
        if ch_idx < 13:
            heading = f"Chapter {chapter_num}: {title}"
        else:
            heading = title

        page.insert_text(
            pymupdf.Point(72, 72),
            heading,
            fontsize=18,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Horizontal rule under title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
        shape.finish(color=(0.3, 0.3, 0.3), width=1)
        shape.commit()

        # First paragraph
        if len(paragraphs) > 0:
            rect = pymupdf.Rect(72, 110, 540, 400)
            page.insert_textbox(
                rect,
                paragraphs[0],
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # Second paragraph
        if len(paragraphs) > 1:
            rect = pymupdf.Rect(72, 420, 540, 720)
            page.insert_textbox(
                rect,
                paragraphs[1],
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # --- Page 2 of chapter ---
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_num += 1

        # Continuation header
        page.insert_text(
            pymupdf.Point(72, 50),
            f"{title} (continued)",
            fontsize=10,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )

        # More content
        if len(paragraphs) > 2:
            rect = pymupdf.Rect(72, 80, 540, 380)
            page.insert_textbox(
                rect,
                paragraphs[2],
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # Additional filler content for realism
        rect = pymupdf.Rect(72, 400, 540, 720)
        filler = (
            f"For additional details on {title.lower()}, refer to the vendor-specific "
            f"documentation and the organization's internal knowledge base. Regular training "
            f"sessions are recommended to keep the team updated on the latest best practices "
            f"and emerging technologies in this area. Documentation should be reviewed and "
            f"updated at least quarterly to ensure accuracy."
        )
        page.insert_textbox(
            rect,
            filler,
            fontsize=11,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # --- Page 3 of chapter ---
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_num += 1

        page.insert_text(
            pymupdf.Point(72, 50),
            f"{title} (continued)",
            fontsize=10,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )

        # Summary / key takeaways section
        page.insert_text(
            pymupdf.Point(72, 85),
            "Key Takeaways",
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0),
        )

        takeaways = [
            f"1. Understand the core principles of {title.lower()} before implementing changes.",
            f"2. Always test configurations in a lab environment before deploying to production.",
            f"3. Document all changes and maintain a rollback plan for critical modifications.",
            f"4. Review and update procedures regularly to align with evolving requirements.",
        ]
        y_pos = 115
        for ta in takeaways:
            rect = pymupdf.Rect(90, y_pos, 540, y_pos + 60)
            page.insert_textbox(
                rect,
                ta,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
            )
            y_pos += 55

        # Notes section
        page.insert_text(
            pymupdf.Point(72, y_pos + 30),
            "Notes",
            fontsize=12,
            fontname="hebo",
            color=(0.2, 0.2, 0.2),
        )
        rect = pymupdf.Rect(72, y_pos + 50, 540, 720)
        page.insert_textbox(
            rect,
            "Use this section to record environment-specific configurations, exceptions, "
            "and implementation notes relevant to your organization's deployment.",
            fontsize=10,
            fontname="heit",
            color=(0.3, 0.3, 0.3),
        )

    assert doc.page_count == 45, f"Expected 45 pages, got {doc.page_count}"

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 45')

    # Open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
