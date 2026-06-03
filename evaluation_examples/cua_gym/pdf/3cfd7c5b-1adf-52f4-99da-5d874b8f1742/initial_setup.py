"""
Initial Setup: Create a 30-page technical manual PDF without page numbers.
Task ID: pdf_gf3_007
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_007'
DOCS_DIR = f'{WORKDIR}/documents'
OUTPUT = f'{DOCS_DIR}/manual.pdf'


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


# Chapter/section structure for a realistic technical manual
MANUAL_STRUCTURE = [
    # (chapter_title, sections)
    ("Introduction", [
        ("Purpose and Scope",
         "This manual provides comprehensive guidance for configuring and operating the AeroVista 3200 "
         "industrial monitoring platform. It covers hardware installation, software configuration, network "
         "integration, and routine maintenance procedures. The target audience includes field engineers, "
         "system administrators, and technical support personnel responsible for deploying and maintaining "
         "monitoring infrastructure across distributed facility networks."),
        ("System Overview",
         "The AeroVista 3200 is a modular environmental monitoring system designed for industrial and "
         "commercial facilities. It supports up to 256 sensor nodes per controller unit, with real-time "
         "data aggregation, threshold-based alerting, and historical trend analysis. The platform integrates "
         "with existing building management systems via BACnet, Modbus, and REST API protocols. Key components "
         "include the central processing unit (CPU-3200), sensor gateway modules (SGM-100), and the web-based "
         "dashboard interface (WebUI v4.2)."),
        ("Safety Precautions",
         "Before installing or servicing any component of the AeroVista 3200 system, ensure all power sources "
         "are disconnected and locked out according to your facility's LOTO procedures. The CPU-3200 unit "
         "operates at 24VDC but internal components may retain residual charge for up to 60 seconds after "
         "power disconnection. Always wear appropriate ESD protection when handling circuit boards and sensor "
         "modules. Refer to OSHA guidelines 29 CFR 1910.147 for detailed lockout/tagout requirements."),
    ]),
    ("Hardware Installation", [
        ("Unpacking and Inspection",
         "Upon receiving the AeroVista 3200 shipment, verify the contents against the packing list included "
         "in the shipping documentation. Each standard deployment kit includes one CPU-3200 controller, four "
         "SGM-100 gateway modules, one power supply unit (PSU-350), mounting hardware, and a CAT6 patch cable "
         "kit. Inspect all components for visible damage. Document any discrepancies using Form HW-INS-001 "
         "and contact AeroVista Technical Support within 48 hours of delivery for warranty claims."),
        ("Mounting the Controller Unit",
         "The CPU-3200 controller requires a standard 19-inch rack mount with a minimum depth of 450mm. "
         "Ensure adequate ventilation clearance of at least 50mm on all sides. The unit occupies 2U of rack "
         "space and weighs 4.8 kg. Secure the controller using the included M6 cage nuts and mounting screws. "
         "Route power cables through the rear cable management channel. The ambient operating temperature "
         "range is 0 to 45 degrees Celsius with humidity between 10 and 90 percent non-condensing."),
        ("Connecting Sensor Gateways",
         "Each SGM-100 gateway module supports up to 64 wireless sensor nodes within a 200-meter line-of-sight "
         "range. Connect gateway modules to the CPU-3200 using the provided CAT6 cables through the RJ45 ports "
         "labeled GW1 through GW4 on the rear panel. The gateway modules support Power over Ethernet (PoE+) "
         "and draw a maximum of 25.5 watts per module. LED indicators on each gateway show connection status: "
         "solid green indicates active communication, amber indicates standby, and red indicates a fault condition."),
        ("Power Supply Configuration",
         "The PSU-350 supports input voltages from 100 to 240 VAC at 50/60 Hz. Connect the AC input using "
         "the included IEC C13 power cord. The PSU delivers 24VDC at up to 14.6 amps across four independently "
         "fused output channels. Each channel is protected by a 4-amp fast-blow fuse accessible from the front "
         "panel. For redundant power configurations, a secondary PSU-350 can be installed in the adjacent rack "
         "slot and connected via the DC bus jumper cable (sold separately as accessory ACC-PWR-DUP)."),
    ]),
    ("Software Configuration", [
        ("Initial Boot Sequence",
         "After completing hardware installation, apply power to the CPU-3200 by toggling the rear power switch. "
         "The initial boot sequence takes approximately 90 seconds. During first boot, the system performs a "
         "hardware self-test, initializes the operating environment, and generates default configuration files. "
         "The front panel LCD displays boot progress. Upon completion, the system displays its assigned IP "
         "address. The default network configuration uses DHCP. If no DHCP server is available, the system "
         "falls back to the static IP address 192.168.1.100 with subnet mask 255.255.255.0."),
        ("Accessing the Web Interface",
         "Open a web browser and navigate to the IP address displayed on the front panel LCD. The WebUI "
         "supports Chrome 90+, Firefox 88+, and Edge 90+. The default login credentials are username 'admin' "
         "and password 'AV3200-Setup'. You will be prompted to change the default password upon first login. "
         "The password must be at least 12 characters and include uppercase, lowercase, numeric, and special "
         "characters. After authentication, the main dashboard displays real-time sensor data, system health "
         "indicators, and recent alert notifications."),
        ("Network Configuration",
         "Navigate to Settings > Network to configure the system's network parameters. The CPU-3200 supports "
         "dual Ethernet interfaces (ETH0 and ETH1) for network redundancy. ETH0 is designated for management "
         "traffic and ETH1 for sensor data. Configure static IP addresses, subnet masks, default gateways, "
         "and DNS servers for each interface. VLAN tagging (802.1Q) is supported on both interfaces. For "
         "integration with enterprise networks, configure the RADIUS authentication settings under Settings > "
         "Security > Authentication. The system supports RADIUS, LDAP, and local authentication modes."),
        ("Sensor Enrollment",
         "To add sensor nodes to the monitoring network, navigate to Devices > Enrollment. Place each sensor "
         "in pairing mode by pressing and holding the reset button for 3 seconds until the LED flashes blue. "
         "Click 'Scan for Devices' in the WebUI. Discovered sensors appear in the enrollment queue with their "
         "MAC address and signal strength. Select sensors to enroll and assign them to zones and groups. Each "
         "sensor can be configured with custom polling intervals ranging from 1 second to 24 hours, threshold "
         "values for alerting, and descriptive labels for identification in reports and dashboards."),
    ]),
    ("Alert Configuration", [
        ("Threshold-Based Alerts",
         "The AeroVista 3200 supports configurable threshold alerts on all measured parameters. Navigate to "
         "Alerts > Thresholds to define alert rules. Each rule specifies a sensor parameter, comparison "
         "operator (greater than, less than, equal to, or range), threshold value, and severity level "
         "(informational, warning, critical, or emergency). Alerts can be configured with hysteresis values "
         "to prevent rapid toggling when measurements oscillate near the threshold boundary. The recommended "
         "hysteresis setting is 5 percent of the threshold value for temperature sensors and 2 percent for "
         "humidity sensors."),
        ("Notification Channels",
         "Configure alert notification delivery under Alerts > Notifications. The system supports email (SMTP), "
         "SMS (via integrated GSM modem or API gateway), SNMP traps (v2c and v3), webhook callbacks, and "
         "integration with popular incident management platforms including PagerDuty, Opsgenie, and ServiceNow. "
         "Each notification channel can be associated with specific alert severity levels and time-of-day "
         "schedules. For example, informational alerts might only generate email notifications during business "
         "hours, while critical alerts trigger SMS and PagerDuty escalations around the clock."),
        ("Escalation Policies",
         "Define escalation policies under Alerts > Escalation to ensure critical alerts receive timely "
         "attention. An escalation policy specifies a sequence of notification actions triggered at increasing "
         "time intervals if an alert remains unacknowledged. For example, a critical temperature alert might "
         "first notify the on-duty engineer via SMS, then escalate to the shift supervisor after 15 minutes, "
         "and finally page the facility manager after 30 minutes. Escalation policies can be assigned to "
         "individual sensors, sensor groups, or entire zones."),
    ]),
    ("Data Management", [
        ("Historical Data Storage",
         "The CPU-3200 includes a 2TB solid-state drive for local data storage. At default polling intervals, "
         "this provides approximately 5 years of historical data for a fully populated system with 256 sensors. "
         "Data is stored in a time-series database optimized for fast retrieval and aggregation. The system "
         "automatically compresses data older than 90 days using lossy downsampling, retaining hourly averages "
         "instead of raw per-second readings. To preserve full-resolution historical data, configure an external "
         "data export target under Settings > Data Management > Export."),
        ("Report Generation",
         "The WebUI includes a built-in report generator accessible from Reports > Create New. Standard report "
         "templates include Daily Summary, Weekly Trend Analysis, Monthly Compliance, and Annual Performance "
         "Review. Custom reports can be created using the drag-and-drop report builder with available widgets "
         "including line charts, bar charts, heat maps, data tables, and statistical summaries. Reports can "
         "be scheduled for automatic generation and distribution via email. Supported export formats include "
         "PDF, CSV, and Excel (XLSX)."),
        ("Backup and Recovery",
         "Configure automated system backups under Settings > Backup. The system supports full and incremental "
         "backups to local USB storage, network file shares (SMB/CIFS, NFS), and cloud storage (Amazon S3, "
         "Azure Blob Storage). Full backups include system configuration, sensor calibration data, user "
         "accounts, alert rules, and historical measurement data. Incremental backups capture only changes "
         "since the last full backup. The recommended backup schedule is daily incremental with weekly full "
         "backups. Test backup restoration quarterly using the recovery wizard under Settings > Backup > Restore."),
    ]),
    ("Maintenance Procedures", [
        ("Routine Inspections",
         "Perform visual inspections of all system components on a monthly basis. Check LED status indicators "
         "on the CPU-3200, PSU-350, and all SGM-100 gateway modules. Verify that cooling fans are operational "
         "and air filters are clean. Inspect cable connections for signs of damage or loosening. Record "
         "inspection findings in the maintenance log accessible from the WebUI under System > Maintenance Log. "
         "Replace air filters every 6 months or more frequently in dusty environments. Order replacement "
         "filters using part number ACC-FLT-200."),
        ("Firmware Updates",
         "AeroVista releases firmware updates quarterly to address security vulnerabilities, improve "
         "performance, and add new features. Check for available updates under System > Firmware > Check for "
         "Updates. The update process takes approximately 10 minutes during which the system is temporarily "
         "offline. Schedule firmware updates during planned maintenance windows. Always create a full system "
         "backup before applying firmware updates. If an update fails, the system automatically rolls back to "
         "the previous firmware version. Release notes for each firmware version are available on the AeroVista "
         "customer support portal."),
        ("Sensor Calibration",
         "Sensor nodes require periodic calibration to maintain measurement accuracy. The recommended "
         "calibration interval is 12 months for temperature and humidity sensors, and 6 months for air quality "
         "sensors. Calibration can be performed in-situ using the built-in calibration wizard under Devices > "
         "Calibration, or sensors can be returned to AeroVista for factory calibration. In-situ calibration "
         "requires a certified reference instrument traceable to NIST standards. Record calibration results "
         "and certificates in the calibration management system under Devices > Calibration > Records."),
    ]),
    ("Troubleshooting", [
        ("Common Error Codes",
         "The AeroVista 3200 displays diagnostic error codes on the front panel LCD and in the WebUI under "
         "System > Diagnostics. Error code E001 indicates a power supply fault; check fuse integrity and "
         "input voltage. E002 indicates a gateway communication timeout; verify cable connections and network "
         "configuration. E003 indicates a sensor enrollment failure; ensure the sensor is in pairing mode and "
         "within range. E004 indicates a storage subsystem error; check SSD health under System > Storage. "
         "E005 indicates a thermal warning; verify cooling fan operation and ambient temperature."),
        ("Network Connectivity Issues",
         "If the WebUI is unreachable, first verify the system's IP address on the front panel LCD. Confirm "
         "that your workstation is on the same subnet or that appropriate routing is configured. Check Ethernet "
         "link status LEDs on both the CPU-3200 and the connected network switch. If using DHCP, verify that "
         "the DHCP server is operational and has available addresses in its pool. For VLAN configurations, "
         "ensure the switch port is configured with the correct VLAN assignment. Use the built-in network "
         "diagnostic tools accessible via the serial console: 'diag network ping <ip>' and 'diag network trace <ip>'."),
        ("Sensor Data Anomalies",
         "If sensor readings appear inaccurate or erratic, first check the sensor's battery level under "
         "Devices > Sensor Status. Low battery voltage can cause intermittent communication failures and "
         "measurement drift. Verify the sensor's signal strength indicator; values below -80 dBm may result "
         "in data loss. Check for sources of radio frequency interference near the sensor or gateway. If the "
         "sensor has not been calibrated within the recommended interval, perform a calibration procedure. "
         "As a last resort, perform a factory reset on the sensor by pressing and holding the reset button "
         "for 10 seconds, then re-enroll the sensor in the system."),
    ]),
    ("Appendices", [
        ("Technical Specifications",
         "CPU-3200 Controller: Dimensions 483 x 88 x 450 mm (2U rack mount), Weight 4.8 kg, Power 24VDC "
         "at 3.2A typical, Operating temperature 0 to 45 degrees C, Storage temperature -20 to 70 degrees C, "
         "Humidity 10 to 90 percent non-condensing, Network interfaces 2x Gigabit Ethernet (RJ45), Gateway "
         "ports 4x RJ45 (PoE+), Serial console 1x RS-232 (DB9), USB 2x USB 3.0 Type-A, Storage 2TB NVMe SSD, "
         "Processor ARM Cortex-A72 quad-core at 1.8 GHz, Memory 8 GB DDR4, Display 2.4 inch LCD 320x240 pixels."),
        ("Regulatory Compliance",
         "The AeroVista 3200 system is certified for compliance with the following standards and regulations: "
         "FCC Part 15 Class A (United States), CE Marking (European Union), IC (Canada), VCCI Class A (Japan), "
         "RoHS Directive 2011/65/EU, WEEE Directive 2012/19/EU, UL 61010-1 (Safety), IEC 61326-1 (EMC), "
         "IEEE 802.3af/at (PoE/PoE+), BACnet BTL Listed (Building Automation), ISO 9001:2015 (Quality "
         "Management), ISO 27001:2013 (Information Security). Certificates of compliance are available "
         "upon request from AeroVista regulatory affairs department."),
        ("Warranty Information",
         "The AeroVista 3200 system is covered by a standard 3-year limited warranty from the date of purchase. "
         "The warranty covers defects in materials and workmanship under normal use conditions. Sensor nodes "
         "carry a separate 2-year warranty. The warranty does not cover damage resulting from improper "
         "installation, unauthorized modification, exposure to conditions beyond published specifications, "
         "or normal wear of consumable components such as batteries and air filters. Extended warranty options "
         "of 5 and 7 years are available for purchase within 90 days of the original system delivery date. "
         "Contact AeroVista Sales for pricing and terms."),
    ]),
]


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page_width, page_height = 612, 792  # US Letter

    content_left = 72
    content_right = page_width - 72
    content_top = 72
    content_width = content_right - content_left

    page_index = 0

    # --- Title Page (Page 1) ---
    page = doc.new_page(width=page_width, height=page_height)
    page_index += 1

    # Title
    page.insert_text(
        pymupdf.Point(page_width / 2 - 180, 250),
        "AeroVista 3200",
        fontsize=32,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )
    page.insert_text(
        pymupdf.Point(page_width / 2 - 200, 300),
        "Technical Operations Manual",
        fontsize=24,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(content_left, 330), pymupdf.Point(content_right, 330))
    shape.finish(color=(0.6, 0.6, 0.6), width=1.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(page_width / 2 - 80, 380),
        "Version 4.2.1",
        fontsize=14,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(page_width / 2 - 100, 410),
        "Release Date: March 2025",
        fontsize=12,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(page_width / 2 - 120, 450),
        "AeroVista Industrial Systems",
        fontsize=12,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(page_width / 2 - 100, 470),
        "Confidential - Internal Use",
        fontsize=10,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    # --- Table of Contents (Page 2) ---
    page = doc.new_page(width=page_width, height=page_height)
    page_index += 1

    page.insert_text(
        pymupdf.Point(content_left, content_top + 30),
        "Table of Contents",
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    y_pos = content_top + 70
    chapter_num = 1
    # We'll fill in approximate page references
    content_page = 3  # Content starts on page 3
    for chapter_title, sections in MANUAL_STRUCTURE:
        page.insert_text(
            pymupdf.Point(content_left, y_pos),
            f"Chapter {chapter_num}: {chapter_title}",
            fontsize=12,
            fontname="hebo",
            color=(0, 0, 0),
        )
        y_pos += 20
        for section_title, _ in sections:
            page.insert_text(
                pymupdf.Point(content_left + 24, y_pos),
                f"{chapter_num}.{sections.index((section_title, _)) + 1}  {section_title}",
                fontsize=10,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
            )
            y_pos += 16
        y_pos += 8
        chapter_num += 1

    # --- Content Pages (Pages 3-30) ---
    # We have 28 pages to fill with 8 chapters of content
    chapter_num = 0
    for chapter_title, sections in MANUAL_STRUCTURE:
        chapter_num += 1

        # Chapter title page
        page = doc.new_page(width=page_width, height=page_height)
        page_index += 1

        # Chapter heading
        page.insert_text(
            pymupdf.Point(content_left, content_top + 40),
            f"Chapter {chapter_num}",
            fontsize=14,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )
        page.insert_text(
            pymupdf.Point(content_left, content_top + 70),
            chapter_title,
            fontsize=22,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )

        # Horizontal rule under chapter title
        shape = page.new_shape()
        shape.draw_line(
            pymupdf.Point(content_left, content_top + 80),
            pymupdf.Point(content_right, content_top + 80),
        )
        shape.finish(color=(0.6, 0.6, 0.6), width=1)
        shape.commit()

        y_pos = content_top + 110

        for sec_idx, (section_title, section_text) in enumerate(sections):
            # Check if we need a new page for this section
            if y_pos > page_height - 150:
                page = doc.new_page(width=page_width, height=page_height)
                page_index += 1
                y_pos = content_top + 30

            # Section heading
            page.insert_text(
                pymupdf.Point(content_left, y_pos),
                f"{chapter_num}.{sec_idx + 1}  {section_title}",
                fontsize=14,
                fontname="hebo",
                color=(0.15, 0.15, 0.35),
            )
            y_pos += 25

            # Section body text - use textbox for wrapping
            text_rect = pymupdf.Rect(content_left, y_pos, content_right, page_height - 72)
            excess = page.insert_textbox(
                text_rect,
                section_text,
                fontsize=11,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

            # insert_textbox returns remaining space (negative = overflow)
            # Estimate vertical space used based on available rect height and remaining
            available_height = text_rect.height
            if excess >= 0:
                # Text fit; used space = available - remaining
                used = available_height - excess
            else:
                # Text overflowed; used all available space
                used = available_height
            y_pos += used + 20

    # Pad to exactly 30 pages if we have fewer
    while doc.page_count < 30:
        page = doc.new_page(width=page_width, height=page_height)
        # Add a "Notes" or continuation placeholder
        page.insert_text(
            pymupdf.Point(content_left, content_top + 30),
            "Notes",
            fontsize=16,
            fontname="hebo",
            color=(0.3, 0.3, 0.3),
        )
        # Add some ruled lines for notes
        shape = page.new_shape()
        for line_y in range(content_top + 70, page_height - 100, 30):
            shape.draw_line(
                pymupdf.Point(content_left, line_y),
                pymupdf.Point(content_right, line_y),
            )
        shape.finish(color=(0.85, 0.85, 0.85), width=0.5)
        shape.commit()

    # If we have more than 30 pages, trim to 30
    while doc.page_count > 30:
        doc.delete_page(doc.page_count - 1)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {doc.page_count}')
    doc.close()

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
