"""
Initial Setup: Create a 20-page product catalog PDF with embedded images on pages 5-8.
Task ID: pdf_mbc_080
Domain: pdf
"""

import os
import shlex
import subprocess
import time

# Use pymupdf (PyMuPDF)
import pymupdf
from PIL import Image
import io
import random

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_080'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/product_catalog.pdf'

# Page dimensions (A4)
W, H = 595, 842


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


def create_product_image(width, height, product_name, color_rgb, seed):
    """Create a simple product image using Pillow."""
    random.seed(seed)
    img = Image.new('RGB', (width, height), color_rgb)
    # Draw some geometric patterns to make images distinguishable
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)

    # Draw border
    draw.rectangle([2, 2, width - 3, height - 3], outline=(255, 255, 255), width=3)

    # Draw some shapes inside
    for _ in range(5):
        x1 = random.randint(10, width - 40)
        y1 = random.randint(10, height - 40)
        x2 = x1 + random.randint(20, 60)
        y2 = y1 + random.randint(20, 60)
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(255, 255, 255))

    # Add product name text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, height - 30), product_name, fill=(255, 255, 255), font=font)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def create_catalog():
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # Define product images for pages 5-8
    # Page 5: 2 images, Page 6: 3 images, Page 7: 2 images, Page 8: 1 image
    product_images = {
        4: [  # page index 4 = page 5
            {"name": "Wireless Headphones XR-500", "color": (45, 85, 130), "w": 280, "h": 200, "seed": 101},
            {"name": "Bluetooth Speaker BT-200", "color": (130, 55, 45), "w": 260, "h": 180, "seed": 102},
        ],
        5: [  # page index 5 = page 6
            {"name": "Smart Watch Pro S7", "color": (40, 110, 70), "w": 240, "h": 240, "seed": 201},
            {"name": "Fitness Tracker FT-100", "color": (100, 50, 120), "w": 260, "h": 190, "seed": 202},
            {"name": "Digital Pedometer DP-50", "color": (50, 90, 110), "w": 220, "h": 170, "seed": 203},
        ],
        6: [  # page index 6 = page 7
            {"name": "Laptop Stand LS-300", "color": (90, 75, 45), "w": 300, "h": 220, "seed": 301},
            {"name": "USB-C Hub UH-7in1", "color": (60, 60, 100), "w": 250, "h": 180, "seed": 302},
        ],
        7: [  # page index 7 = page 8
            {"name": "Mechanical Keyboard MK-88", "color": (110, 40, 65), "w": 320, "h": 200, "seed": 401},
        ],
    }

    # Page content for the catalog
    page_titles = [
        "TechVault Pro — 2025 Product Catalog",          # page 1 - cover
        "Table of Contents",                               # page 2
        "About TechVault Pro",                             # page 3
        "Our Quality Promise",                             # page 4
        "Audio & Entertainment",                           # page 5 - images
        "Wearable Technology",                             # page 6 - images
        "Workspace Accessories",                           # page 7 - images
        "Keyboards & Input Devices",                       # page 8 - images
        "Networking Solutions",                            # page 9
        "Storage & Memory",                                # page 10
        "Cables & Adapters",                               # page 11
        "Power & Charging",                                # page 12
        "Mobile Accessories",                              # page 13
        "Gaming Peripherals",                              # page 14
        "Smart Home Devices",                              # page 15
        "Customer Testimonials",                           # page 16
        "Warranty Information",                            # page 17
        "Shipping & Returns Policy",                       # page 18
        "Frequently Asked Questions",                      # page 19
        "Contact Us & Order Information",                  # page 20
    ]

    body_texts = {
        0: "Welcome to the TechVault Pro 2025 Product Catalog. We are proud to present our comprehensive range of technology products designed for professionals and enthusiasts alike. Browse through our carefully curated selection of cutting-edge devices and accessories.",
        1: "1. About TechVault Pro .................. 3\n2. Our Quality Promise .................. 4\n3. Audio & Entertainment ................ 5\n4. Wearable Technology .................. 6\n5. Workspace Accessories ................ 7\n6. Keyboards & Input Devices ............ 8\n7. Networking Solutions ................. 9\n8. Storage & Memory .................... 10\n9. Cables & Adapters ................... 11\n10. Power & Charging ................... 12\n11. Mobile Accessories ................. 13\n12. Gaming Peripherals ................. 14\n13. Smart Home Devices ................. 15\n14. Customer Testimonials .............. 16\n15. Warranty Information ............... 17\n16. Shipping & Returns ................. 18\n17. FAQ ................................ 19\n18. Contact Us ......................... 20",
        2: "Founded in 2018, TechVault Pro has been at the forefront of consumer electronics distribution. Our team of technology experts meticulously tests and selects each product in our catalog. With partnerships spanning over 200 manufacturers worldwide, we bring the best technology directly to your doorstep.\n\nOur headquarters in San Francisco houses a state-of-the-art testing facility where every product undergoes rigorous quality assessments before being added to our catalog.",
        3: "At TechVault Pro, quality is not just a buzzword — it is our core principle. Every product in this catalog has passed our 12-point quality inspection process:\n\n• Material durability testing\n• Electrical safety certification\n• Performance benchmarking\n• Ergonomic assessment\n• Environmental compliance verification\n• User experience evaluation\n• Packaging integrity check\n• Long-term reliability simulation\n• Compatibility testing across platforms\n• Customer satisfaction prediction scoring\n• Return rate historical analysis\n• Price-to-value ratio optimization",
        4: "Discover our premium audio and entertainment lineup. From noise-cancelling headphones to portable speakers, we have curated the finest selection for audiophiles and casual listeners. Each product in this category delivers exceptional sound quality with modern design aesthetics.",
        5: "Step into the future with our wearable technology collection. Track your fitness goals, stay connected on the go, and monitor your health metrics with precision engineering. Our wearables combine style with functionality for the modern professional.",
        6: "Transform your workspace with our range of ergonomic accessories. Designed to boost productivity and comfort, these essential workspace tools help you create the ideal setup whether you work from home or in the office.",
        7: "Experience the tactile perfection of our keyboard and input device selection. From mechanical switches to wireless ergonomic designs, find the perfect typing companion for work and play.",
        8: "Build a robust network infrastructure with our enterprise-grade and consumer networking solutions. Fast, reliable, and secure connectivity for homes and businesses of all sizes.",
        9: "Expand your storage capacity with our range of SSDs, HDDs, NAS devices, and memory cards. Fast read/write speeds and reliable data protection for all your digital assets.",
        10: "Connect everything seamlessly with our extensive cable and adapter collection. USB-C, HDMI, DisplayPort, Thunderbolt — we have every connection type you need, built to last.",
        11: "Keep your devices charged and ready with our power solutions. From fast-charging wall adapters to high-capacity power banks, never run out of battery again.",
        12: "Protect, mount, and enhance your mobile devices with our curated selection of phone and tablet accessories. Cases, stands, car mounts, and screen protectors from top brands.",
        13: "Level up your gaming experience with professional-grade peripherals. High-DPI mice, responsive controllers, immersive headsets, and streaming equipment for competitive gamers.",
        14: "Make your home smarter with our IoT device collection. Smart lights, thermostats, security cameras, and voice assistants that integrate seamlessly with your existing ecosystem.",
        15: "Don't just take our word for it — hear from our satisfied customers:\n\n\"TechVault Pro's product quality is unmatched. I have ordered from them six times and every product exceeded my expectations.\" — Maria Gonzalez, Portland, OR\n\n\"The customer service team went above and beyond to help me find the right setup for my home office.\" — David Kim, Austin, TX\n\n\"Fast shipping, great prices, and products that actually match the descriptions. Highly recommended!\" — Rachel Thompson, Denver, CO",
        16: "All TechVault Pro products come with our comprehensive warranty coverage:\n\n• 30-day money-back guarantee on all items\n• 1-year manufacturer warranty (standard)\n• 2-year extended warranty available for select products\n• Free technical support via phone, email, and chat\n• Accidental damage protection plans available",
        17: "Shipping: Free standard shipping on orders over $50. Express (2-day) shipping available for $9.99. Same-day delivery available in select metro areas.\n\nReturns: Hassle-free returns within 30 days of purchase. Items must be in original packaging. Defective items replaced at no additional cost. Refunds processed within 5-7 business days.",
        18: "Q: Do you ship internationally?\nA: Yes, we ship to over 40 countries worldwide.\n\nQ: Can I track my order?\nA: Absolutely. You will receive a tracking number via email once your order ships.\n\nQ: Do you offer bulk pricing?\nA: Yes, for orders of 10+ units. Contact our sales team.\n\nQ: What payment methods do you accept?\nA: We accept all major credit cards, PayPal, Apple Pay, and Google Pay.",
        19: "TechVault Pro Inc.\n1200 Market Street, Suite 450\nSan Francisco, CA 94103\n\nPhone: (415) 555-0187\nEmail: orders@techvaultpro.com\nWebsite: www.techvaultpro.com\n\nBusiness Hours:\nMonday — Friday: 8:00 AM — 8:00 PM PST\nSaturday: 9:00 AM — 5:00 PM PST\nSunday: Closed\n\nOrder Online: www.techvaultpro.com/shop",
    }

    for page_idx in range(20):
        page = doc.new_page(width=W, height=H)

        # Header
        if page_idx == 0:
            # Cover page
            page.insert_text(pymupdf.Point(72, 200), "TechVault Pro", fontsize=36, fontname="hebo", color=(0.1, 0.2, 0.5))
            page.insert_text(pymupdf.Point(72, 260), "2025 Product Catalog", fontsize=24, fontname="helv", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(72, 320), "Premium Technology Solutions", fontsize=14, fontname="heit", color=(0.4, 0.4, 0.4))
            # Decorative line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 280), pymupdf.Point(523, 280))
            shape.finish(color=(0.1, 0.2, 0.5), width=2)
            shape.commit()
        else:
            # Title
            page.insert_text(pymupdf.Point(72, 60), page_titles[page_idx], fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
            # Separator
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(523, 70))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()

            # Body text
            body = body_texts.get(page_idx, "")
            if body:
                rect = pymupdf.Rect(72, 90, 523, 700)
                page.insert_textbox(rect, body, fontsize=10, fontname="helv", color=(0.15, 0.15, 0.15))

            # Insert images for pages 5-8 (indices 4-7)
            if page_idx in product_images:
                imgs = product_images[page_idx]
                # Position images below the text area
                y_start = 400 if page_idx != 7 else 300  # page 8 has just 1 image, give more space
                x_positions = [72, 310]  # two-column layout
                y_pos = y_start

                for i, img_info in enumerate(imgs):
                    img_data = create_product_image(
                        img_info["w"], img_info["h"],
                        img_info["name"], img_info["color"],
                        img_info["seed"]
                    )
                    # Place images: 2 per row
                    col = i % 2
                    row = i // 2
                    x = x_positions[col]
                    y = y_start + row * 220

                    # Scale to fit within page
                    img_rect = pymupdf.Rect(x, y, x + 210, y + 160)
                    page.insert_image(img_rect, stream=img_data)

                    # Image caption
                    page.insert_text(
                        pymupdf.Point(x, y + 175),
                        img_info["name"],
                        fontsize=8, fontname="hebo", color=(0.2, 0.2, 0.2)
                    )

        # Footer with page number (except cover)
        if page_idx > 0:
            page.insert_text(
                pymupdf.Point(280, 820),
                f"— {page_idx + 1} —",
                fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5)
            )

    # Set metadata
    doc.set_metadata({
        "title": "TechVault Pro 2025 Product Catalog",
        "author": "TechVault Pro Marketing Department",
        "subject": "Product Catalog",
        "keywords": "electronics, technology, catalog, products, 2025",
        "creator": "TechVault Pro",
        "producer": "PyMuPDF",
    })

    # Add table of contents / bookmarks
    toc = [
        [1, "Cover", 1],
        [1, "Table of Contents", 2],
        [1, "About TechVault Pro", 3],
        [1, "Our Quality Promise", 4],
        [1, "Audio & Entertainment", 5],
        [1, "Wearable Technology", 6],
        [1, "Workspace Accessories", 7],
        [1, "Keyboards & Input Devices", 8],
        [1, "Networking Solutions", 9],
        [1, "Storage & Memory", 10],
        [1, "Cables & Adapters", 11],
        [1, "Power & Charging", 12],
        [1, "Mobile Accessories", 13],
        [1, "Gaming Peripherals", 14],
        [1, "Smart Home Devices", 15],
        [1, "Customer Testimonials", 16],
        [1, "Warranty Information", 17],
        [1, "Shipping & Returns Policy", 18],
        [1, "Frequently Asked Questions", 19],
        [1, "Contact Us & Order Information", 20],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify image counts
    verify_doc = pymupdf.open(OUTPUT)
    for pi in [4, 5, 6, 7]:
        imgs = verify_doc[pi].get_images()
        print(f'  Page {pi+1}: {len(imgs)} images')
    print(f'  Total pages: {verify_doc.page_count}')
    verify_doc.close()

    # GUI-ready: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_catalog()
