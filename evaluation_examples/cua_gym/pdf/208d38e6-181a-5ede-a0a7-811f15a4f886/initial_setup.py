"""
Initial Setup: Create a 4-page product price list PDF with $49.99 appearing 8 times.
Task ID: pdf_ro_027
Domain: pdf
"""

import os
import shlex
import subprocess
import time

# Install PyMuPDF on VM if not present
subprocess.run(["pip3", "install", "PyMuPDF"], capture_output=True)

import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_027'
MARKETING_DIR = f'{WORKDIR}/marketing'
OUTPUT = f'{MARKETING_DIR}/price_list.pdf'


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
    os.makedirs(MARKETING_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Cover / Featured Products ---
    page1 = doc.new_page(width=612, height=792)  # Letter size
    # Header
    page1.insert_text(pymupdf.Point(72, 50), "TechVista Electronics", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page1.insert_text(pymupdf.Point(72, 75), "Spring 2026 Price List", fontsize=16, fontname="heit", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 90), pymupdf.Point(540, 90))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()

    # Product 1
    page1.insert_text(pymupdf.Point(72, 130), "Wireless Bluetooth Earbuds Pro", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 150), "Premium noise-canceling earbuds with 24-hour battery life.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page1.insert_text(pymupdf.Point(72, 168), "Active Noise Cancellation | IPX5 Water Resistant | Touch Controls", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(72, 188), "Price: $49.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page1.insert_text(pymupdf.Point(72, 206), "SKU: TVE-BT-2026-001", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 2
    page1.insert_text(pymupdf.Point(72, 250), "Smart LED Desk Lamp", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 270), "Adjustable brightness and color temperature for optimal workspace lighting.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page1.insert_text(pymupdf.Point(72, 288), "5 Color Modes | USB Charging Port | Memory Function", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(72, 308), "Price: $34.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page1.insert_text(pymupdf.Point(72, 326), "SKU: TVE-LED-2026-015", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 3
    page1.insert_text(pymupdf.Point(72, 370), "USB-C Fast Charging Cable (6ft)", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 390), "Braided nylon cable with 100W power delivery support.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page1.insert_text(pymupdf.Point(72, 408), "100W PD | USB 3.2 Gen 2 | Reinforced Connectors", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(72, 428), "Price: $49.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page1.insert_text(pymupdf.Point(72, 446), "SKU: TVE-CB-2026-042", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 4
    page1.insert_text(pymupdf.Point(72, 490), "Portable Bluetooth Speaker", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 510), "Compact waterproof speaker with deep bass and 360-degree sound.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page1.insert_text(pymupdf.Point(72, 528), "IPX7 Waterproof | 12-hour Playback | TWS Pairing", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(72, 548), "Price: $29.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page1.insert_text(pymupdf.Point(72, 566), "SKU: TVE-SPK-2026-008", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Footer
    page1.insert_text(pymupdf.Point(72, 750), "Page 1 of 4  |  Prices valid through June 30, 2026  |  TechVista Electronics Inc.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 2: Accessories ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 50), "Accessories & Peripherals", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 65), pymupdf.Point(540, 65))
    shape2.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape2.commit()

    # Product 5
    page2.insert_text(pymupdf.Point(72, 100), "Ergonomic Wireless Mouse", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 120), "Sculpted design reduces wrist strain during extended use.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page2.insert_text(pymupdf.Point(72, 138), "2400 DPI | Silent Clicks | Rechargeable Li-ion", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page2.insert_text(pymupdf.Point(72, 158), "Price: $49.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page2.insert_text(pymupdf.Point(72, 176), "SKU: TVE-MS-2026-027", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 6
    page2.insert_text(pymupdf.Point(72, 220), "Mechanical Keyboard (TKL)", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 240), "Hot-swappable switches with per-key RGB backlighting.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page2.insert_text(pymupdf.Point(72, 258), "Cherry MX Compatible | PBT Keycaps | N-Key Rollover", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page2.insert_text(pymupdf.Point(72, 278), "Price: $79.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page2.insert_text(pymupdf.Point(72, 296), "SKU: TVE-KB-2026-033", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 7
    page2.insert_text(pymupdf.Point(72, 340), "USB Webcam HD 1080p", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 360), "Auto-focus webcam with built-in noise-reducing dual microphone.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page2.insert_text(pymupdf.Point(72, 378), "1080p/30fps | Auto Light Correction | Privacy Shutter", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page2.insert_text(pymupdf.Point(72, 398), "Price: $49.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page2.insert_text(pymupdf.Point(72, 416), "SKU: TVE-WC-2026-051", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 8
    page2.insert_text(pymupdf.Point(72, 460), "Laptop Stand (Aluminum)", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, 480), "Adjustable height laptop riser with ventilated design for cooling.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page2.insert_text(pymupdf.Point(72, 498), "6-Level Height | Foldable Design | Anti-Slip Pads", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page2.insert_text(pymupdf.Point(72, 518), "Price: $24.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page2.insert_text(pymupdf.Point(72, 536), "SKU: TVE-LS-2026-019", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    page2.insert_text(pymupdf.Point(72, 750), "Page 2 of 4  |  Prices valid through June 30, 2026  |  TechVista Electronics Inc.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 3: Smart Home ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 50), "Smart Home Devices", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 65), pymupdf.Point(540, 65))
    shape3.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape3.commit()

    # Product 9
    page3.insert_text(pymupdf.Point(72, 100), "Smart Wi-Fi Plug (2-Pack)", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(72, 120), "Voice-controlled outlets compatible with Alexa, Google Home, and HomeKit.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(72, 138), "Energy Monitoring | Scheduling | Away Mode", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(72, 158), "Price: $19.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page3.insert_text(pymupdf.Point(72, 176), "SKU: TVE-SH-2026-005", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 10
    page3.insert_text(pymupdf.Point(72, 220), "Indoor Security Camera", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(72, 240), "Pan-and-tilt camera with night vision and two-way audio.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(72, 258), "2K Resolution | 360-Degree View | Motion Detection", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(72, 278), "Price: $49.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page3.insert_text(pymupdf.Point(72, 296), "SKU: TVE-SC-2026-064", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 11
    page3.insert_text(pymupdf.Point(72, 340), "Smart LED Light Bulb (4-Pack)", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(72, 360), "RGBW bulbs with app control and music sync capability.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(72, 378), "16 Million Colors | Scene Modes | Voice Control", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(72, 398), "Price: $49.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page3.insert_text(pymupdf.Point(72, 416), "SKU: TVE-LB-2026-038", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Product 12
    page3.insert_text(pymupdf.Point(72, 460), "Smart Door Lock (Keyless)", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(72, 480), "Fingerprint and PIN code entry with remote access via smartphone.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page3.insert_text(pymupdf.Point(72, 498), "Fingerprint Sensor | Auto-Lock | Activity Log", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page3.insert_text(pymupdf.Point(72, 518), "Price: $129.99", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page3.insert_text(pymupdf.Point(72, 536), "SKU: TVE-DL-2026-072", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    page3.insert_text(pymupdf.Point(72, 750), "Page 3 of 4  |  Prices valid through June 30, 2026  |  TechVista Electronics Inc.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 4: Bundles & Special Offers ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 50), "Bundles & Special Offers", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 65), pymupdf.Point(540, 65))
    shape4.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape4.commit()

    # Bundle 1
    page4.insert_text(pymupdf.Point(72, 100), "Work From Home Starter Kit", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 120), "Includes webcam, wireless mouse, and laptop stand.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(72, 138), "3 Items | Save 15% | Free Shipping", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page4.insert_text(pymupdf.Point(72, 158), "Bundle Price: $89.99 (Individual items total: $124.97)", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page4.insert_text(pymupdf.Point(72, 176), "SKU: TVE-BDL-2026-B01", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Bundle 2
    page4.insert_text(pymupdf.Point(72, 220), "Smart Home Essential Pack", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 240), "Includes 2x smart plugs, 4x LED bulbs, and security camera.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(72, 258), "7 Items | Save 20% | Free Installation Guide", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    page4.insert_text(pymupdf.Point(72, 278), "Bundle Price: $99.99 (Individual items total: $119.97)", fontsize=12, fontname="hebo", color=(0.0, 0.0, 0.0))
    page4.insert_text(pymupdf.Point(72, 296), "SKU: TVE-BDL-2026-B02", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Additional note with $49.99 appearances
    page4.insert_text(pymupdf.Point(72, 350), "Individual Product Quick Reference", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))

    page4.insert_text(pymupdf.Point(72, 380), "The following items are available at $49.99 each:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(90, 400), "- Wireless Bluetooth Earbuds Pro (TVE-BT-2026-001)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(90, 418), "- USB-C Fast Charging Cable 6ft (TVE-CB-2026-042)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(90, 436), "- Ergonomic Wireless Mouse (TVE-MS-2026-027)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(90, 454), "- USB Webcam HD 1080p (TVE-WC-2026-051)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(90, 472), "- Indoor Security Camera (TVE-SC-2026-064)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(90, 490), "- Smart LED Light Bulb 4-Pack (TVE-LB-2026-038)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    # Ordering info
    page4.insert_text(pymupdf.Point(72, 540), "How to Order", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    page4.insert_text(pymupdf.Point(72, 562), "Online: www.techvista-electronics.com", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(72, 580), "Phone: 1-800-TECHVISTA (1-800-832-4847)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(72, 598), "Email: orders@techvista-electronics.com", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page4.insert_text(pymupdf.Point(72, 622), "Most popular price point: $49.99 - see items above.", fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))
    page4.insert_text(pymupdf.Point(72, 640), "Bulk pricing available for orders of 10+ units. Contact sales for details.", fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))

    page4.insert_text(pymupdf.Point(72, 750), "Page 4 of 4  |  Prices valid through June 30, 2026  |  TechVista Electronics Inc.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify $49.99 count
    doc = pymupdf.open(OUTPUT)
    count = 0
    for page in doc:
        instances = page.search_for("$49.99")
        count += len(instances)
    doc.close()
    print(f'Verified: $49.99 appears {count} times across all pages')

    # Launch in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
