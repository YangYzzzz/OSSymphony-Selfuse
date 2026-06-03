"""
Initial Setup: Create a 12-page technical whitepaper PDF with no headers/footers.
Task ID: pdf_pw_017
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
TASK_ID = 'pdf_pw_017'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/whitepaper.pdf'

# Letter size in points
PAGE_W, PAGE_H = 612, 792

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
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Content for a 12-page technical whitepaper about edge computing
    pages_content = [
        # Page 1 - Title page
        {
            "title": "Edge Computing Architecture for Industrial IoT",
            "subtitle": "A Technical Whitepaper",
            "body": (
                "Prepared by the Advanced Research Division\n"
                "Revision 3.2 - March 2025\n\n"
                "This document presents a comprehensive analysis of edge computing\n"
                "architectures optimized for industrial Internet of Things deployments.\n"
                "It covers network topology design, latency optimization strategies,\n"
                "and fault-tolerant processing frameworks suitable for manufacturing\n"
                "environments with strict real-time requirements."
            ),
        },
        # Page 2 - Executive Summary
        {
            "title": "1. Executive Summary",
            "body": (
                "The proliferation of connected sensors and actuators in modern manufacturing\n"
                "facilities has created unprecedented demands on data processing infrastructure.\n"
                "Traditional cloud-centric architectures introduce latency that is incompatible\n"
                "with real-time control loops operating at sub-millisecond intervals.\n\n"
                "This whitepaper proposes a three-tier edge computing architecture that reduces\n"
                "end-to-end processing latency by 94% compared to conventional cloud pipelines.\n"
                "Field testing across 17 manufacturing sites demonstrated consistent round-trip\n"
                "times below 2.3 milliseconds for critical control signals.\n\n"
                "Key findings include:\n"
                "- Device-level inference reduces upstream bandwidth by 73%\n"
                "- Hierarchical caching achieves 99.97% data availability during network partitions\n"
                "- Federated model updates converge 4.2x faster than centralized retraining\n"
                "- Total cost of ownership decreases by 31% over a 5-year deployment horizon"
            ),
        },
        # Page 3 - Introduction
        {
            "title": "2. Introduction",
            "body": (
                "Industrial automation has evolved from isolated programmable logic controllers\n"
                "to interconnected cyber-physical systems spanning entire production lines.\n"
                "The International Data Corporation estimates that by 2026, over 41.6 billion\n"
                "IoT devices will generate 79.4 zettabytes of data annually.\n\n"
                "Processing this data at the network edge, rather than transmitting it to remote\n"
                "data centers, offers significant advantages in latency, bandwidth efficiency,\n"
                "and operational resilience. However, edge deployments face unique constraints:\n\n"
                "- Limited computational resources at field-level nodes\n"
                "- Harsh environmental conditions (temperature, vibration, electromagnetic interference)\n"
                "- Stringent safety and regulatory requirements (IEC 61508, ISO 13849)\n"
                "- Integration with legacy OT protocols (Modbus, PROFINET, EtherCAT)\n\n"
                "This paper addresses these challenges through a modular architecture that\n"
                "balances processing locality with centralized orchestration capabilities."
            ),
        },
        # Page 4 - Architecture Overview
        {
            "title": "3. Architecture Overview",
            "body": (
                "The proposed architecture consists of three processing tiers:\n\n"
                "Tier 1 - Device Edge: Microcontroller-based nodes co-located with sensors and\n"
                "actuators. These perform signal conditioning, anomaly detection using lightweight\n"
                "neural networks (typically 50-200KB models), and protocol translation. Average\n"
                "processing latency at this tier is 0.3 milliseconds.\n\n"
                "Tier 2 - Near Edge: Industrial-grade compute nodes deployed per production cell\n"
                "or assembly line segment. Equipped with GPU accelerators, these nodes handle\n"
                "computer vision inspection, predictive maintenance inference, and local\n"
                "orchestration. Typical configurations include NVIDIA Jetson AGX Orin modules\n"
                "with 64GB unified memory.\n\n"
                "Tier 3 - Far Edge: Rack-mounted servers in on-premises data rooms providing\n"
                "model training, historical analytics, and coordination with cloud services.\n"
                "These maintain local replicas of cloud databases for offline operation."
            ),
        },
        # Page 5 - Network Topology
        {
            "title": "4. Network Topology Design",
            "body": (
                "The network fabric interconnecting the three tiers employs a redundant mesh\n"
                "topology with deterministic latency guarantees based on IEEE 802.1 Time-Sensitive\n"
                "Networking (TSN) standards.\n\n"
                "4.1 Tier 1 Connectivity\n"
                "Device edge nodes communicate via EtherCAT (cycle time 125 microseconds) for\n"
                "real-time control traffic and MQTT-SN over 802.15.4e for telemetry data.\n"
                "Each production cell supports up to 256 device nodes with automatic topology\n"
                "discovery using LLDP extensions.\n\n"
                "4.2 Tier 1 to Tier 2 Uplinks\n"
                "Dual 10GbE connections with 802.1Qbv scheduled traffic provide guaranteed\n"
                "bandwidth for time-critical streams. Non-critical traffic uses best-effort\n"
                "queues with weighted fair scheduling.\n\n"
                "4.3 Tier 2 to Tier 3 Backbone\n"
                "25GbE spine-leaf fabric with ECMP routing ensures no single point of failure.\n"
                "BGP-based micro-segmentation isolates safety-critical traffic from general\n"
                "enterprise communication."
            ),
        },
        # Page 6 - Latency Optimization
        {
            "title": "5. Latency Optimization Strategies",
            "body": (
                "Achieving sub-millisecond processing requires optimization across the full\n"
                "software stack, from kernel scheduling to application-level batching.\n\n"
                "5.1 Real-Time Operating System Configuration\n"
                "Tier 1 and Tier 2 nodes run PREEMPT_RT patched Linux kernels with isolated\n"
                "CPU cores dedicated to control tasks. IRQ affinity is configured to prevent\n"
                "interrupt storms from disrupting real-time threads.\n\n"
                "5.2 Zero-Copy Data Paths\n"
                "Shared memory regions mapped between sensor drivers and inference engines\n"
                "eliminate unnecessary data copies. DPDK-accelerated network interfaces bypass\n"
                "the kernel networking stack for inter-node communication.\n\n"
                "5.3 Model Optimization\n"
                "Neural network models are quantized to INT8 precision using calibration\n"
                "datasets from production environments. TensorRT optimization reduces inference\n"
                "time by 3.7x on average compared to FP32 execution. Pruning removes 40-60%\n"
                "of parameters with less than 0.2% accuracy degradation."
            ),
        },
        # Page 7 - Fault Tolerance
        {
            "title": "6. Fault Tolerance Framework",
            "body": (
                "Industrial deployments require continuous operation despite hardware failures,\n"
                "network disruptions, and software faults. The architecture implements multiple\n"
                "resilience mechanisms:\n\n"
                "6.1 Redundant Processing Paths\n"
                "Safety-critical inference tasks run simultaneously on primary and standby\n"
                "Tier 2 nodes. A voting mechanism compares outputs and triggers failover within\n"
                "500 microseconds if discrepancies are detected.\n\n"
                "6.2 Hierarchical Data Caching\n"
                "Each tier maintains a local time-series cache with configurable retention:\n"
                "- Tier 1: 10-minute rolling buffer in SRAM (128KB per node)\n"
                "- Tier 2: 24-hour cache in NVMe storage (2TB per cell controller)\n"
                "- Tier 3: 90-day archive with compression (achieving 12:1 ratios)\n\n"
                "During network partitions, cached data ensures continuous operation. Upon\n"
                "reconnection, a conflict resolution protocol based on vector clocks merges\n"
                "divergent state without data loss."
            ),
        },
        # Page 8 - Security Considerations
        {
            "title": "7. Security Considerations",
            "body": (
                "Edge computing expands the attack surface compared to centralized architectures.\n"
                "The security framework addresses threats at each tier:\n\n"
                "7.1 Device Authentication\n"
                "Tier 1 nodes use hardware-based attestation via TPM 2.0 modules. Device\n"
                "certificates are provisioned through an automated enrollment protocol that\n"
                "verifies firmware integrity before granting network access.\n\n"
                "7.2 Encrypted Communication\n"
                "All inter-tier traffic is encrypted using TLS 1.3 with mutual authentication.\n"
                "Pre-shared keys are rotated every 24 hours through a key distribution service\n"
                "running on Tier 3 infrastructure.\n\n"
                "7.3 Model Integrity\n"
                "Machine learning models deployed to edge nodes are cryptographically signed.\n"
                "Runtime verification ensures models have not been tampered with during transit\n"
                "or storage. Anomalous model outputs trigger automatic rollback to the previous\n"
                "verified version."
            ),
        },
        # Page 9 - Performance Benchmarks
        {
            "title": "8. Performance Benchmarks",
            "body": (
                "Comprehensive benchmarks were conducted across 17 manufacturing sites spanning\n"
                "automotive assembly, semiconductor fabrication, and food processing industries.\n\n"
                "8.1 Latency Measurements\n"
                "End-to-end processing latency (sensor input to actuator output):\n"
                "- P50 latency: 1.1 ms   (cloud baseline: 18.4 ms)\n"
                "- P95 latency: 1.8 ms   (cloud baseline: 42.7 ms)\n"
                "- P99 latency: 2.3 ms   (cloud baseline: 127.3 ms)\n"
                "- Maximum observed: 4.1 ms (cloud baseline: 892 ms)\n\n"
                "8.2 Throughput Analysis\n"
                "Aggregate data processing throughput per Tier 2 node:\n"
                "- Inference: 12,400 frames/second at 640x480 resolution\n"
                "- Time-series anomaly detection: 1.2 million samples/second\n"
                "- Protocol translation: 85,000 messages/second (Modbus to OPC-UA)\n\n"
                "8.3 Availability\n"
                "Measured system availability over 12-month deployment: 99.9994%\n"
                "Mean time to recovery after Tier 2 node failure: 480 milliseconds"
            ),
        },
        # Page 10 - Deployment Case Study
        {
            "title": "9. Deployment Case Study: Automotive Assembly",
            "body": (
                "A major European automotive manufacturer deployed the edge architecture across\n"
                "three assembly plants with a combined 847 robotic welding stations.\n\n"
                "9.1 Pre-Deployment Baseline\n"
                "Prior to edge deployment, quality inspection relied on end-of-line testing\n"
                "with a 3.2% defect escape rate. Weld quality data was uploaded to cloud\n"
                "servers every 15 minutes, preventing real-time corrective action.\n\n"
                "9.2 Edge-Enabled Improvements\n"
                "After deploying Tier 1 vision nodes at each welding station and Tier 2\n"
                "controllers per assembly cell:\n"
                "- Defect escape rate reduced to 0.08% (97.5% improvement)\n"
                "- Weld parameter adjustments applied within 2 ms of defect detection\n"
                "- Cloud bandwidth consumption reduced by 89%\n"
                "- Annual savings estimated at EUR 14.3 million across three plants\n\n"
                "9.3 Lessons Learned\n"
                "Initial deployment challenges included electromagnetic interference from\n"
                "welding arcs affecting Tier 1 node communications. Shielded enclosures and\n"
                "redundant wireless backup channels resolved reliability issues."
            ),
        },
        # Page 11 - Future Directions
        {
            "title": "10. Future Directions",
            "body": (
                "Several emerging technologies will enhance edge computing capabilities:\n\n"
                "10.1 Neuromorphic Processing\n"
                "Spiking neural network accelerators such as Intel Loihi 2 and IBM NorthPole\n"
                "offer order-of-magnitude improvements in energy efficiency for event-driven\n"
                "sensor processing. Preliminary testing shows 15x reduction in power consumption\n"
                "for vibration analysis workloads.\n\n"
                "10.2 6G Network Integration\n"
                "Sixth-generation wireless networks promise sub-100 microsecond air interface\n"
                "latency with native support for deterministic communication. This could enable\n"
                "wireless replacement of wired Tier 1 connections in applications where physical\n"
                "cabling is impractical.\n\n"
                "10.3 Digital Twin Synchronization\n"
                "Real-time synchronization between physical edge nodes and cloud-hosted digital\n"
                "twins will enable predictive simulation of equipment failures up to 72 hours\n"
                "before occurrence, based on multi-physics models continuously calibrated with\n"
                "live sensor data."
            ),
        },
        # Page 12 - Conclusion and References
        {
            "title": "11. Conclusion",
            "body": (
                "This whitepaper has demonstrated that a three-tier edge computing architecture\n"
                "can deliver the latency, throughput, and reliability required for industrial\n"
                "IoT applications. Field deployments across diverse manufacturing environments\n"
                "validate the approach with consistent sub-2.3ms processing times and 99.9994%\n"
                "system availability.\n\n"
                "The modular design allows organizations to adopt the architecture incrementally,\n"
                "starting with Tier 2 deployment for immediate latency benefits and expanding\n"
                "to device-level intelligence as use cases mature.\n\n"
                "References\n\n"
                "[1] Shi, W. et al. Edge Computing: Vision and Challenges. IEEE IoT Journal, 2016.\n"
                "[2] Satyanarayanan, M. The Emergence of Edge Computing. Computer, 50(1), 2017.\n"
                "[3] Khan, W.Z. et al. Edge Computing: A Survey. Future Generation Computer\n"
                "    Systems, Vol. 97, pp. 219-235, 2019.\n"
                "[4] IEEE 802.1 Time-Sensitive Networking Task Group. TSN Standards, 2023.\n"
                "[5] IEC 62443. Industrial Communication Networks - Security, Ed. 4.0, 2024.\n"
                "[6] NIST SP 800-183. Networks of Things. National Institute of Standards, 2024."
            ),
        },
    ]

    for i, page_data in enumerate(pages_content):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        if i == 0:
            # Title page - centered layout using textboxes
            title_rect = pymupdf.Rect(72, 220, 540, 280)
            page.insert_textbox(
                title_rect,
                page_data["title"],
                fontsize=20,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            subtitle_rect = pymupdf.Rect(72, 290, 540, 330)
            page.insert_textbox(
                subtitle_rect,
                page_data["subtitle"],
                fontsize=16,
                fontname="heit",
                color=(0.3, 0.3, 0.3),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            body_rect = pymupdf.Rect(100, 380, 512, 700)
            page.insert_textbox(
                body_rect,
                page_data["body"],
                fontsize=11,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
        else:
            # Content pages - standard layout with margins
            # Title at y=72 (well below the empty top margin area y<50)
            page.insert_text(
                pymupdf.Point(72, 80),
                page_data["title"],
                fontsize=16,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            # Separator line below title
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 90), pymupdf.Point(540, 90))
            shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
            shape.commit()

            # Body text
            body_rect = pymupdf.Rect(72, 105, 540, 745)
            page.insert_textbox(
                body_rect,
                page_data["body"],
                fontsize=10.5,
                fontname="helv",
                color=(0.15, 0.15, 0.15),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
