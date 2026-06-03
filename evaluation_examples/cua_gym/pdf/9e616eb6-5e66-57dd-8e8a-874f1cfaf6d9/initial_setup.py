"""
Initial Setup: Create two product brochure PDFs (v1 and v2) with different images
for an image comparison task.
Task ID: pdf_cr_065
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import struct
import zlib

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'pdf_cr_065'
V1_PATH = f'{DESKTOP}/brochure_v1.pdf'
V2_PATH = f'{DESKTOP}/brochure_v2.pdf'


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


def make_png_bytes(width, height, r, g, b):
    """Create a minimal PNG image in memory with a solid color."""
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(chunk) & 0xFFFFFFFF)
        return struct.pack('>I', len(data)) + chunk + crc

    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)

    raw_data = b''
    for _ in range(height):
        raw_data += b'\x00' + bytes([r, g, b]) * width
    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)
    iend = make_chunk(b'IEND', b'')

    return signature + ihdr + idat + iend


def create_brochures():
    import pymupdf

    os.makedirs(DESKTOP, exist_ok=True)

    # ===== Create brochure_v1.pdf (4 pages) =====
    doc1 = pymupdf.open()

    # Page 1: Cover - 2 images (logo + hero)
    p1 = doc1.new_page(width=595, height=842)
    p1.insert_text(pymupdf.Point(72, 60), "TechVista Pro", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    p1.insert_text(pymupdf.Point(72, 90), "Product Brochure 2025", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))

    logo_png = make_png_bytes(120, 60, 30, 80, 160)  # blue logo
    p1.insert_image(pymupdf.Rect(72, 110, 192, 170), stream=logo_png)

    hero_png = make_png_bytes(450, 250, 40, 120, 200)  # hero image
    p1.insert_image(pymupdf.Rect(72, 200, 522, 450), stream=hero_png)

    p1.insert_textbox(pymupdf.Rect(72, 480, 522, 600),
        "TechVista Pro is the next generation of enterprise productivity software. "
        "Designed for teams that demand high performance and seamless collaboration.",
        fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))

    # Page 2: Features - 3 images (feature icons)
    p2 = doc1.new_page(width=595, height=842)
    p2.insert_text(pymupdf.Point(72, 60), "Key Features", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.5))

    feat1_png = make_png_bytes(100, 100, 60, 180, 75)   # green icon
    feat2_png = make_png_bytes(100, 100, 200, 60, 60)   # red icon
    feat3_png = make_png_bytes(100, 100, 180, 140, 50)   # orange icon
    p2.insert_image(pymupdf.Rect(72, 100, 172, 200), stream=feat1_png)
    p2.insert_text(pymupdf.Point(190, 155), "Real-Time Analytics Dashboard", fontsize=12, fontname="hebo")

    p2.insert_image(pymupdf.Rect(72, 240, 172, 340), stream=feat2_png)
    p2.insert_text(pymupdf.Point(190, 295), "Advanced Security Protocol", fontsize=12, fontname="hebo")

    p2.insert_image(pymupdf.Rect(72, 380, 172, 480), stream=feat3_png)
    p2.insert_text(pymupdf.Point(190, 435), "Seamless Cloud Integration", fontsize=12, fontname="hebo")

    p2.insert_textbox(pymupdf.Rect(72, 520, 522, 700),
        "Our platform integrates with over 200 enterprise tools including Salesforce, "
        "Slack, Jira, and Microsoft 365. The analytics engine processes data in real-time "
        "with sub-second latency, providing actionable insights.",
        fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Page 3: Pricing - 1 image (pricing table graphic)
    p3 = doc1.new_page(width=595, height=842)
    p3.insert_text(pymupdf.Point(72, 60), "Pricing Plans", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.5))

    pricing_png = make_png_bytes(400, 200, 230, 230, 240)  # light gray pricing graphic
    p3.insert_image(pymupdf.Rect(97, 100, 497, 300), stream=pricing_png)

    p3.insert_textbox(pymupdf.Rect(72, 340, 522, 600),
        "Starter Plan: $29/month per user\n"
        "Professional Plan: $79/month per user\n"
        "Enterprise Plan: Custom pricing\n\n"
        "All plans include 24/7 support, 99.9% uptime SLA, and unlimited storage. "
        "Enterprise customers receive dedicated account management and custom integrations.",
        fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))

    # Page 4: Contact - 2 images (team photo + QR code)
    p4 = doc1.new_page(width=595, height=842)
    p4.insert_text(pymupdf.Point(72, 60), "Contact Us", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.5))

    team_png = make_png_bytes(400, 180, 100, 130, 170)  # team photo placeholder
    p4.insert_image(pymupdf.Rect(97, 100, 497, 280), stream=team_png)

    qr_png = make_png_bytes(80, 80, 20, 20, 20)  # QR code placeholder
    p4.insert_image(pymupdf.Rect(257, 320, 337, 400), stream=qr_png)

    p4.insert_textbox(pymupdf.Rect(72, 430, 522, 600),
        "TechVista Inc.\n"
        "1200 Innovation Drive, Suite 400\n"
        "San Francisco, CA 94107\n\n"
        "Email: sales@techvista.com\n"
        "Phone: +1 (415) 555-0192\n"
        "Web: www.techvista.com",
        fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))

    doc1.save(V1_PATH)
    doc1.close()
    print(f'Created: {V1_PATH}')

    # ===== Create brochure_v2.pdf (4 pages) =====
    # Differences from v1:
    #   Page 1: hero image REPLACED (different dimensions: 450x200 instead of 450x250)
    #   Page 2: feat3 REMOVED, one NEW image added (collaboration icon) = net same count but 1 removed + 1 added
    #            Actually let's do: remove feat2, add 2 new images = +1 net on page 2
    #   Page 3: pricing image REPLACED with different dimensions (400x180 vs 400x200), add 1 new badge image
    #   Page 4: QR code REMOVED
    # Summary: v1 = 2+3+1+2 = 8 images, v2 = 2+3+2+1 = 8 images
    # Let me recalculate for a clearer diff:
    #   v1: p1=2, p2=3, p3=1, p4=2 => total 8
    #   v2: p1=2(hero replaced diff size), p2=2(feat2 removed), p3=2(pricing replaced + badge added), p4=1(qr removed) => total 7
    # Added: 1 (badge on p3), Removed: 2 (feat2 on p2, qr on p4), Changed: 1 (hero on p1 - diff dimensions), pricing replaced diff dim = changed
    # Let me simplify:
    #   v2: p1=2, p2=2, p3=2, p4=1 => total 7
    #   Per-page: p1 same count(2=2) hero diff dim => 1 changed; p2 (3 vs 2) => 1 removed;
    #             p3 (1 vs 2) => 1 added, pricing diff dim => 1 changed; p4 (2 vs 1) => 1 removed

    doc2 = pymupdf.open()

    # Page 1: Cover - 2 images (logo same + hero REPLACED with different dimensions)
    p1 = doc2.new_page(width=595, height=842)
    p1.insert_text(pymupdf.Point(72, 60), "TechVista Pro", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    p1.insert_text(pymupdf.Point(72, 90), "Product Brochure 2025 - Updated", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))

    p1.insert_image(pymupdf.Rect(72, 110, 192, 170), stream=logo_png)  # same logo

    hero_v2_png = make_png_bytes(450, 200, 50, 100, 180)  # different size hero
    p1.insert_image(pymupdf.Rect(72, 200, 522, 400), stream=hero_v2_png)

    p1.insert_textbox(pymupdf.Rect(72, 430, 522, 600),
        "TechVista Pro is the next generation of enterprise productivity software. "
        "Now with AI-powered workflows and enhanced collaboration features.",
        fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))

    # Page 2: Features - 2 images (feat1 + feat3 only, feat2 removed)
    p2 = doc2.new_page(width=595, height=842)
    p2.insert_text(pymupdf.Point(72, 60), "Key Features", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.5))

    p2.insert_image(pymupdf.Rect(72, 100, 172, 200), stream=feat1_png)  # same green icon
    p2.insert_text(pymupdf.Point(190, 155), "Real-Time Analytics Dashboard", fontsize=12, fontname="hebo")

    p2.insert_image(pymupdf.Rect(72, 240, 172, 340), stream=feat3_png)  # same orange icon (moved up)
    p2.insert_text(pymupdf.Point(190, 295), "Seamless Cloud Integration", fontsize=12, fontname="hebo")

    p2.insert_textbox(pymupdf.Rect(72, 400, 522, 600),
        "Our platform integrates with over 200 enterprise tools. The analytics engine "
        "processes data in real-time with sub-second latency.",
        fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Page 3: Pricing - 2 images (pricing REPLACED with different dimensions + NEW badge)
    p3 = doc2.new_page(width=595, height=842)
    p3.insert_text(pymupdf.Point(72, 60), "Pricing Plans", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.5))

    pricing_v2_png = make_png_bytes(400, 180, 220, 225, 235)  # different size pricing graphic
    p3.insert_image(pymupdf.Rect(97, 100, 497, 280), stream=pricing_v2_png)

    badge_png = make_png_bytes(80, 80, 255, 200, 50)  # NEW gold badge
    p3.insert_image(pymupdf.Rect(440, 290, 520, 370), stream=badge_png)

    p3.insert_textbox(pymupdf.Rect(72, 390, 522, 600),
        "Starter Plan: $29/month per user\n"
        "Professional Plan: $79/month per user\n"
        "Enterprise Plan: Custom pricing\n\n"
        "All plans include 24/7 support, 99.9% uptime SLA, and unlimited storage.",
        fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))

    # Page 4: Contact - 1 image (team photo only, QR removed)
    p4 = doc2.new_page(width=595, height=842)
    p4.insert_text(pymupdf.Point(72, 60), "Contact Us", fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.5))

    p4.insert_image(pymupdf.Rect(97, 100, 497, 280), stream=team_png)  # same team photo

    p4.insert_textbox(pymupdf.Rect(72, 320, 522, 500),
        "TechVista Inc.\n"
        "1200 Innovation Drive, Suite 400\n"
        "San Francisco, CA 94107\n\n"
        "Email: sales@techvista.com\n"
        "Phone: +1 (415) 555-0192\n"
        "Web: www.techvista.com",
        fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))

    doc2.save(V2_PATH)
    doc2.close()
    print(f'Created: {V2_PATH}')

    # Ensure image_diff.txt does NOT exist (that's the task output)
    diff_path = f'{DESKTOP}/image_diff.txt'
    if os.path.exists(diff_path):
        os.remove(diff_path)
        print(f'Removed pre-existing: {diff_path}')

    # Open both PDFs for the agent
    launch_gui(f'evince "{V1_PATH}"', delay_sec=2.0)
    launch_gui(f'evince "{V2_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched evince for both brochure PDFs with DISPLAY=:0')


create_brochures()
