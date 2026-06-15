"""
Initial Setup: Create slide_creation_guide.odt document and quarterly review images
Task ID: osworld_multi_apps_media_doc_edit_006
Domain: multi_apps (LibreOffice Writer + Impress)

This script:
1. Creates /home/user/documents/slide_creation_guide.odt — instructions document
2. Creates /home/user/pictures/quarterly_review/ directory with 4 PNG images
3. Creates /home/user/presentations/ directory (empty, target for agent output)
4. Opens the .odt document and a new Impress window for the GUI agent
"""

import os
import shlex
import subprocess
import time

# Pillow & odf for image/document creation
from PIL import Image, ImageDraw, ImageFont
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import H, P, Span

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_doc_edit_006'

DOCUMENTS_DIR = f'{WORKDIR}/documents'
PICTURES_DIR = f'{WORKDIR}/pictures/quarterly_review'
PRESENTATIONS_DIR = f'{WORKDIR}/presentations'
ODT_FILE = f'{DOCUMENTS_DIR}/slide_creation_guide.odt'


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


def create_directories():
    """Create necessary directory structure."""
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(PICTURES_DIR, exist_ok=True)
    os.makedirs(PRESENTATIONS_DIR, exist_ok=True)
    print(f'Directories created: {DOCUMENTS_DIR}, {PICTURES_DIR}, {PRESENTATIONS_DIR}')


def create_guide_document():
    """Create the slide creation guide ODT document."""
    doc = OpenDocumentText()

    # Define heading style
    heading_style = Style(name="Heading1", family="paragraph")
    heading_style.addElement(ParagraphProperties(breakbefore="auto"))
    heading_style.addElement(TextProperties(fontsize="18pt", fontweight="bold"))
    doc.styles.addElement(heading_style)

    # Define body style
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(TextProperties(fontsize="12pt"))
    doc.styles.addElement(body_style)

    # Title heading
    h1 = H(outlinelevel=1)
    h1.addText("Quarterly Review Presentation — Slide Creation Guide")
    doc.text.addElement(h1)

    # Overview paragraph
    p1 = P(stylename="BodyText")
    p1.addText(
        "This document specifies the requirements for creating the Q4 Quarterly Review "
        "presentation in LibreOffice Impress. Follow the instructions below carefully."
    )
    doc.text.addElement(p1)

    # Section: Slide Layout
    h2 = H(outlinelevel=2)
    h2.addText("Slide Layout Specifications")
    doc.text.addElement(h2)

    p2 = P(stylename="BodyText")
    p2.addText(
        "Create a presentation file saved as: /home/user/presentations/quarterly_review.odp"
    )
    doc.text.addElement(p2)

    p3 = P(stylename="BodyText")
    p3.addText(
        "The presentation must contain exactly 4 slides. Each slide corresponds to one "
        "image file located in /home/user/pictures/quarterly_review/."
    )
    doc.text.addElement(p3)

    # Section: Per-slide instructions
    h3 = H(outlinelevel=2)
    h3.addText("Per-Slide Instructions")
    doc.text.addElement(h3)

    p4 = P(stylename="BodyText")
    p4.addText("For each image in /home/user/pictures/quarterly_review/, create one slide with:")
    doc.text.addElement(p4)

    p5 = P(stylename="BodyText")
    p5.addText(
        "1. The image placed on the slide filling approximately 80% of the slide area "
        "(centered horizontally, positioned in the upper portion of the slide)."
    )
    doc.text.addElement(p5)

    p6 = P(stylename="BodyText")
    p6.addText(
        "2. A text box below the image containing the filename WITHOUT its extension "
        "as the slide title text. For example, if the image is 'Q4_Revenue_Overview.png', "
        "the text box should read 'Q4_Revenue_Overview'."
    )
    doc.text.addElement(p6)

    p7 = P(stylename="BodyText")
    p7.addText(
        "3. The slides must follow the alphabetical order of the image filenames."
    )
    doc.text.addElement(p7)

    # Section: Image location
    h4 = H(outlinelevel=2)
    h4.addText("Image Files")
    doc.text.addElement(h4)

    p8 = P(stylename="BodyText")
    p8.addText(
        "Source images are located in: /home/user/pictures/quarterly_review/"
    )
    doc.text.addElement(p8)

    p9 = P(stylename="BodyText")
    p9.addText(
        "The directory contains the following PNG images (to be used in order):"
    )
    doc.text.addElement(p9)

    for img_name in [
        "Q4_Revenue_Overview.png",
        "Q4_Sales_Performance.png",
        "Q4_Customer_Satisfaction.png",
        "Q4_Product_Roadmap.png",
    ]:
        pi = P(stylename="BodyText")
        pi.addText(f"  - {img_name}")
        doc.text.addElement(pi)

    # Section: Output
    h5 = H(outlinelevel=2)
    h5.addText("Output Requirements")
    doc.text.addElement(h5)

    p10 = P(stylename="BodyText")
    p10.addText(
        "Save the completed presentation as: /home/user/presentations/quarterly_review.odp"
    )
    doc.text.addElement(p10)

    p11 = P(stylename="BodyText")
    p11.addText(
        "Ensure the file is in ODP format (LibreOffice Impress native format)."
    )
    doc.text.addElement(p11)

    doc.save(ODT_FILE)
    print(f'Guide document created: {ODT_FILE}')


def create_quarterly_images():
    """Create 4 realistic-looking quarterly review PNG images."""
    slide_w, slide_h = 1920, 1080

    image_specs = [
        {
            "filename": "Q4_Revenue_Overview.png",
            "title": "Q4 Revenue Overview",
            "subtitle": "Total Revenue: $4.2M | Growth: +18% YoY",
            "bg_color": (15, 52, 96),       # dark blue
            "accent_color": (52, 152, 219),  # blue
            "bar_values": [320, 380, 410, 420],
            "bar_labels": ["Oct", "Nov", "Dec", "Total"],
        },
        {
            "filename": "Q4_Sales_Performance.png",
            "title": "Q4 Sales Performance",
            "subtitle": "Units Sold: 12,847 | Target Achieved: 103%",
            "bg_color": (22, 60, 36),        # dark green
            "accent_color": (39, 174, 96),   # green
            "bar_values": [280, 360, 340, 390],
            "bar_labels": ["Oct", "Nov", "Dec", "Avg"],
        },
        {
            "filename": "Q4_Customer_Satisfaction.png",
            "title": "Q4 Customer Satisfaction",
            "subtitle": "NPS Score: 72 | CSAT: 4.6/5.0",
            "bg_color": (60, 30, 80),        # dark purple
            "accent_color": (155, 89, 182),  # purple
            "bar_values": [350, 400, 420, 440],
            "bar_labels": ["Oct", "Nov", "Dec", "Q4"],
        },
        {
            "filename": "Q4_Product_Roadmap.png",
            "title": "Q4 Product Roadmap",
            "subtitle": "Features Launched: 14 | Bug Fixes: 63",
            "bg_color": (80, 40, 10),        # dark orange
            "accent_color": (230, 126, 34),  # orange
            "bar_values": [200, 300, 410, 380],
            "bar_labels": ["Oct", "Nov", "Dec", "Avg"],
        },
    ]

    for spec in image_specs:
        img = Image.new("RGB", (slide_w, slide_h), color=spec["bg_color"])
        draw = ImageDraw.Draw(img)

        # Draw a header bar
        draw.rectangle([(0, 0), (slide_w, 120)], fill=spec["accent_color"])

        # Title text
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
            font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            font_val = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except (IOError, OSError):
            font_title = ImageFont.load_default()
            font_sub = font_label = font_val = font_title

        draw.text((60, 20), spec["title"], fill=(255, 255, 255), font=font_title)
        draw.text((60, 150), spec["subtitle"], fill=(200, 200, 200), font=font_sub)

        # Draw a simple bar chart
        chart_x, chart_y = 200, 280
        chart_h, chart_w_total = 500, 1500
        bar_count = len(spec["bar_values"])
        bar_width = 200
        bar_gap = (chart_w_total - bar_width * bar_count) // (bar_count + 1)
        max_val = max(spec["bar_values"])

        # Chart background
        draw.rectangle(
            [(chart_x - 20, chart_y - 20),
             (chart_x + chart_w_total + 20, chart_y + chart_h + 60)],
            fill=(255, 255, 255, 30),
            outline=spec["accent_color"],
        )

        for i, (val, label) in enumerate(zip(spec["bar_values"], spec["bar_labels"])):
            bx = chart_x + bar_gap + i * (bar_width + bar_gap)
            bar_h = int((val / max_val) * chart_h)
            by_top = chart_y + chart_h - bar_h

            # Draw bar
            draw.rectangle(
                [(bx, by_top), (bx + bar_width, chart_y + chart_h)],
                fill=spec["accent_color"],
            )
            # Value label above bar
            draw.text(
                (bx + bar_width // 2 - 20, by_top - 50),
                str(val),
                fill=(255, 255, 255),
                font=font_val,
            )
            # Month label below bar
            draw.text(
                (bx + bar_width // 2 - 20, chart_y + chart_h + 10),
                label,
                fill=(200, 200, 200),
                font=font_label,
            )

        # Footer line
        draw.line([(0, slide_h - 60), (slide_w, slide_h - 60)], fill=spec["accent_color"], width=3)
        draw.text((60, slide_h - 50), "Confidential — Q4 2024 Internal Report", fill=(150, 150, 150), font=font_label)

        out_path = os.path.join(PICTURES_DIR, spec["filename"])
        img.save(out_path)
        print(f'Image created: {out_path}')


def main():
    create_directories()
    create_quarterly_images()
    create_guide_document()

    # GUI-ready startup: open the guide document so the agent can read it
    # The agent needs to read the guide then create the presentation
    launch_gui(f'libreoffice --writer "{ODT_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with slide_creation_guide.odt (DISPLAY=:0)')


main()
