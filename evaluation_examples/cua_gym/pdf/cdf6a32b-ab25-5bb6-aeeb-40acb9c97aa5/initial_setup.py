"""
Initial Setup: Create a scanned multi-page will PDF (8 pages, image-only, no text layer)
Task ID: pdf_legal_061
Domain: pdf
"""

import os
import shlex
import subprocess
import time

# We use reportlab to create text on a canvas, then render each page as an image
# with PyMuPDF, then reassemble as image-only PDF (no text layer) to simulate a scan.
try:
    import pymupdf
except ImportError:
    import fitz as pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import random
import math

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_061'
ESTATE_DIR = f'{WORKDIR}/legal/estate'
OUTPUT = f'{ESTATE_DIR}/will_scan.pdf'

# Page dimensions for Letter size scan at 200 DPI
DPI = 200
PAGE_W_PT, PAGE_H_PT = 612, 792  # Letter in points
IMG_W = int(PAGE_W_PT * DPI / 72)  # ~1700 px
IMG_H = int(PAGE_H_PT * DPI / 72)  # ~2200 px

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


def get_font(size, bold=False, italic=False):
    """Try to get a font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    ]
    if bold:
        preferred = [p for p in font_paths if 'Bold' in p]
        fallback = font_paths
    else:
        preferred = [p for p in font_paths if 'Bold' not in p and 'Italic' not in p]
        fallback = font_paths

    for path in preferred + fallback:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def add_scan_noise(img):
    """Add realistic scan artifacts: slight rotation, noise, edge darkening."""
    # Slight random rotation (simulating scanner misalignment)
    angle = random.uniform(-0.3, 0.3)
    img = img.rotate(angle, fillcolor=(255, 255, 255), expand=False)

    # Add subtle noise
    import numpy as np
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, 3, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)

    # Slight blur to simulate scan
    img = img.filter(ImageFilter.GaussianBlur(radius=0.4))

    return img


def draw_text_block(draw, text_lines, x, y, font, line_spacing=1.4, color=(20, 20, 20)):
    """Draw multiple lines of text, return the y position after the last line."""
    for line in text_lines:
        draw.text((x, y), line, fill=color, font=font)
        y += int(font.size * line_spacing)
    return y


def draw_handwritten_text(draw, text, x, y, size=22, color=(10, 10, 80)):
    """Simulate handwritten text with slight irregularity."""
    # Use a different font or just offset characters slightly
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    font = None
    for p in font_paths:
        if os.path.exists(p):
            try:
                font = ImageFont.truetype(p, size)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()

    cur_x = x
    for ch in text:
        # Add slight random offset per character to simulate handwriting
        offset_y = random.randint(-1, 1)
        draw.text((cur_x, y + offset_y), ch, fill=color, font=font)
        bbox = font.getbbox(ch)
        cur_x += bbox[2] - bbox[0] + random.randint(-1, 1)
    return y + int(size * 1.5)


def create_page_image(page_num):
    """Create a single page of the will as a PIL Image (simulating a scan)."""
    img = Image.new('RGB', (IMG_W, IMG_H), (252, 250, 245))  # Slightly off-white like scanned paper
    draw = ImageDraw.Draw(img)

    # Margins
    mx, my = 170, 140  # Left margin, top margin
    max_x = IMG_W - 170
    content_w = max_x - mx

    font_title = get_font(32, bold=True)
    font_heading = get_font(24, bold=True)
    font_body = get_font(19)
    font_body_bold = get_font(19, bold=True)
    font_small = get_font(15)
    font_page = get_font(14)

    y = my

    if page_num == 0:
        # PAGE 1: Title page and opening declarations
        # Centered title
        title = "LAST WILL AND TESTAMENT"
        bbox = font_title.getbbox(title)
        tw = bbox[2] - bbox[0]
        draw.text(((IMG_W - tw) // 2, y), title, fill=(10, 10, 10), font=font_title)
        y += 70

        subtitle = "OF"
        bbox = font_heading.getbbox(subtitle)
        sw = bbox[2] - bbox[0]
        draw.text(((IMG_W - sw) // 2, y), subtitle, fill=(10, 10, 10), font=font_heading)
        y += 50

        name = "MARGARET ELEANOR WHITFIELD"
        bbox = font_heading.getbbox(name)
        nw = bbox[2] - bbox[0]
        draw.text(((IMG_W - nw) // 2, y), name, fill=(10, 10, 10), font=font_heading)
        y += 80

        # Horizontal rule
        draw.line([(mx, y), (max_x, y)], fill=(60, 60, 60), width=2)
        y += 40

        body_lines = [
            "I, Margaret Eleanor Whitfield, of 4217 Chestnut Hill Lane, Fairfax,",
            "Virginia 22030, being of sound mind and disposing memory, do hereby",
            "declare this instrument to be my Last Will and Testament, revoking",
            "all previous wills and codicils heretofore made by me.",
            "",
            "ARTICLE I - DECLARATIONS",
            "",
            "Section 1.01. I am currently married to Robert James Whitfield.",
            "All references to \"my husband\" in this Will are references to",
            "Robert James Whitfield.",
            "",
            "Section 1.02. I have three (3) children, namely:",
            "   (a) Katherine Anne Whitfield, born June 14, 1985;",
            "   (b) Thomas Robert Whitfield, born September 22, 1988;",
            "   (c) Elizabeth Grace Whitfield-Chen, born March 3, 1992.",
            "",
            "Section 1.03. I have two (2) grandchildren, namely:",
            "   (a) Oliver James Chen, born November 8, 2018;",
            "   (b) Sophie Marie Chen, born April 21, 2021.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.45)

    elif page_num == 1:
        # PAGE 2: Article II - Debts and Expenses, Article III - Specific Bequests
        heading = "ARTICLE II - PAYMENT OF DEBTS AND EXPENSES"
        draw.text((mx, y), heading, fill=(10, 10, 10), font=font_heading)
        y += 50

        body_lines = [
            "Section 2.01. I direct my Personal Representative to pay all of my",
            "legally enforceable debts, funeral expenses, costs of last illness,",
            "and expenses of administration of my estate from the assets of my",
            "residuary estate as soon as practicable after my death.",
            "",
            "Section 2.02. All estate, inheritance, succession, and other death",
            "taxes imposed by reason of my death shall be paid from the residuary",
            "estate without apportionment.",
            "",
            "",
            "ARTICLE III - SPECIFIC BEQUESTS",
            "",
            "Section 3.01. Personal Property Bequests:",
            "",
            "   (a) To my daughter Katherine Anne Whitfield, I bequeath my",
            "       antique pearl necklace and matching earrings, the Steinway",
            "       grand piano currently located in my residence, and all",
            "       original artwork hanging in the living room and study.",
            "",
            "   (b) To my son Thomas Robert Whitfield, I bequeath my collection",
            "       of first-edition books, the 1967 Chevrolet Corvette stored",
            "       at 892 Maple Drive Storage Unit #14, and all woodworking",
            "       tools and equipment in the basement workshop.",
            "",
            "   (c) To my daughter Elizabeth Grace Whitfield-Chen, I bequeath",
            "       my grandmother's china set (Royal Albert, 12 place settings),",
            "       all jewelry not otherwise specifically bequeathed herein,",
            "       and the contents of my safe deposit box at First National",
            "       Bank, Box #2847.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.40)

    elif page_num == 2:
        # PAGE 3: More bequests + handwritten marginal note
        heading = "ARTICLE III - SPECIFIC BEQUESTS (Continued)"
        draw.text((mx, y), heading, fill=(10, 10, 10), font=font_heading)
        y += 50

        body_lines = [
            "Section 3.02. Monetary Bequests:",
            "",
            "   (a) To my sister, Dorothy Louise Patterson, the sum of Fifty",
            "       Thousand Dollars ($50,000.00).",
            "",
            "   (b) To my longtime friend and colleague, Dr. Patricia Ann",
            "       Sullivan, the sum of Twenty-Five Thousand Dollars ($25,000.00).",
            "",
            "   (c) To the Fairfax County Public Library Foundation, the sum",
            "       of Fifteen Thousand Dollars ($15,000.00) to be used for",
            "       the acquisition of children's literature.",
            "",
            "   (d) To St. Andrew's Episcopal Church, Fairfax, Virginia, the",
            "       sum of Ten Thousand Dollars ($10,000.00) for the organ",
            "       restoration fund.",
            "",
            "Section 3.03. Real Property Bequests:",
            "",
            "   (a) The vacation property located at 17 Oceanview Drive,",
            "       Rehoboth Beach, Delaware 19971, I bequeath to my husband",
            "       Robert James Whitfield for his lifetime, with remainder",
            "       to my children in equal shares.",
            "",
            "   (b) The rental property located at 2305 Columbia Pike,",
            "       Arlington, Virginia 22204, I bequeath to my three",
            "       children in equal shares, to be held as tenants in common.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.40)

        # Handwritten marginal note (simulating testator's annotation)
        y_note = 520
        draw_handwritten_text(draw, "Initialed: MEW", max_x - 300, y_note, size=20, color=(15, 15, 90))
        draw_handwritten_text(draw, "03/15/2024", max_x - 280, y_note + 30, size=18, color=(15, 15, 90))

    elif page_num == 3:
        # PAGE 4: Article IV - Residuary Estate
        heading = "ARTICLE IV - RESIDUARY ESTATE"
        draw.text((mx, y), heading, fill=(10, 10, 10), font=font_heading)
        y += 50

        body_lines = [
            "Section 4.01. I give, devise, and bequeath all the rest, residue,",
            "and remainder of my estate, whether real, personal, or mixed, of",
            "whatsoever kind and wheresoever situated, which I may own or have",
            "the right to dispose of at the time of my death (my \"residuary",
            "estate\") to my husband, Robert James Whitfield, if he survives me",
            "by thirty (30) days.",
            "",
            "Section 4.02. If my husband does not survive me by thirty (30) days,",
            "I give, devise, and bequeath my residuary estate in equal shares to",
            "my surviving children, per stirpes.",
            "",
            "Section 4.03. If none of my children survive me, my residuary",
            "estate shall be distributed to my grandchildren in equal shares,",
            "per stirpes, provided they have attained the age of twenty-five",
            "(25) years. Any share passing to a grandchild under the age of",
            "twenty-five (25) years shall be held in trust as provided in",
            "Article V of this Will.",
            "",
            "",
            "ARTICLE V - TRUST PROVISIONS",
            "",
            "Section 5.01. Any property held in trust under this Article shall",
            "be managed and administered by the Trustee appointed herein for",
            "the benefit of the designated beneficiary until such beneficiary",
            "attains the age of twenty-five (25) years.",
            "",
            "Section 5.02. The Trustee shall apply so much of the net income",
            "and principal as the Trustee deems advisable for the health,",
            "education, maintenance, and support of the beneficiary, taking",
            "into consideration other resources available to the beneficiary.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.38)

    elif page_num == 4:
        # PAGE 5: Trust provisions continued + Article VI
        heading = "ARTICLE V - TRUST PROVISIONS (Continued)"
        draw.text((mx, y), heading, fill=(10, 10, 10), font=font_heading)
        y += 50

        body_lines = [
            "Section 5.03. Upon the beneficiary attaining the age of twenty-five",
            "(25) years, the Trustee shall distribute the remaining trust assets,",
            "including any accumulated income, to the beneficiary outright and",
            "free of trust.",
            "",
            "Section 5.04. If a beneficiary dies before full distribution of",
            "the trust, the remaining trust assets shall be distributed to the",
            "beneficiary's then-living descendants, per stirpes, or if none,",
            "to my then-living descendants, per stirpes.",
            "",
            "",
            "ARTICLE VI - APPOINTMENT OF FIDUCIARIES",
            "",
            "Section 6.01. Personal Representative. I nominate and appoint my",
            "husband, Robert James Whitfield, as Personal Representative of",
            "this Will. If he is unable or unwilling to serve, I nominate",
            "and appoint my daughter, Katherine Anne Whitfield, as successor",
            "Personal Representative.",
            "",
            "Section 6.02. Trustee. I nominate and appoint First National",
            "Bank of Fairfax, Virginia, as Trustee of any trust created",
            "under this Will. If First National Bank is unable or unwilling",
            "to serve, I nominate and appoint Meridian Trust Company of",
            "Alexandria, Virginia, as successor Trustee.",
            "",
            "Section 6.03. Guardian. If my husband does not survive me, I",
            "nominate and appoint my sister, Dorothy Louise Patterson, as",
            "guardian of the person and property of any minor children.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.38)

    elif page_num == 5:
        # PAGE 6: Article VII - Powers + Article VIII
        heading = "ARTICLE VII - FIDUCIARY POWERS"
        draw.text((mx, y), heading, fill=(10, 10, 10), font=font_heading)
        y += 50

        body_lines = [
            "Section 7.01. In addition to all powers conferred by applicable",
            "law, I grant to my Personal Representative and Trustee the",
            "following powers, to be exercised in their sole discretion:",
            "",
            "   (a) To sell, lease, mortgage, pledge, exchange, or otherwise",
            "       dispose of any property at public or private sale;",
            "",
            "   (b) To invest and reinvest estate or trust assets in any",
            "       form of property, including mutual funds, securities,",
            "       real estate, and other investments;",
            "",
            "   (c) To borrow money for estate or trust purposes and to",
            "       encumber estate or trust property as security;",
            "",
            "   (d) To compromise, settle, or abandon claims for or against",
            "       the estate or any trust;",
            "",
            "   (e) To distribute property in kind or in cash, and to make",
            "       non-pro-rata distributions as deemed appropriate.",
            "",
            "",
            "ARTICLE VIII - NO-CONTEST CLAUSE",
            "",
            "Section 8.01. If any beneficiary under this Will contests or",
            "challenges the validity of this Will or any provision herein,",
            "or institutes or joins in any proceeding to contest or challenge",
            "this Will, then such beneficiary shall forfeit all benefits",
            "under this Will and shall be treated as having predeceased me.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.38)

    elif page_num == 6:
        # PAGE 7: Article IX - General Provisions + signature page start
        heading = "ARTICLE IX - GENERAL PROVISIONS"
        draw.text((mx, y), heading, fill=(10, 10, 10), font=font_heading)
        y += 50

        body_lines = [
            "Section 9.01. Survivorship. For purposes of this Will, any",
            "beneficiary who does not survive me by thirty (30) days shall",
            "be deemed to have predeceased me.",
            "",
            "Section 9.02. Governing Law. This Will shall be governed by",
            "and construed in accordance with the laws of the Commonwealth",
            "of Virginia.",
            "",
            "Section 9.03. Severability. If any provision of this Will is",
            "held invalid or unenforceable, the remaining provisions shall",
            "continue in full force and effect.",
            "",
            "Section 9.04. Definitions. As used in this Will:",
            "   (a) \"descendants\" means children, grandchildren, and more",
            "       remote descendants by blood or legal adoption;",
            "   (b) \"per stirpes\" means by right of representation under",
            "       Virginia law;",
            "   (c) \"property\" includes real and personal property of every",
            "       kind and description.",
            "",
            "",
            "IN WITNESS WHEREOF, I have hereunto set my hand to this, my",
            "Last Will and Testament, consisting of eight (8) pages, each",
            "of which I have initialed for identification, on this 15th day",
            "of March, 2024, at Fairfax, Virginia.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.40)

        y += 40
        # Signature line
        draw.line([(mx + 50, y + 30), (mx + 450, y + 30)], fill=(60, 60, 60), width=1)
        # Handwritten signature
        draw_handwritten_text(draw, "Margaret E. Whitfield", mx + 80, y, size=26, color=(10, 10, 80))
        y += 50
        draw.text((mx + 50, y), "MARGARET ELEANOR WHITFIELD, Testatrix", fill=(10, 10, 10), font=font_body)

    elif page_num == 7:
        # PAGE 8: Witness attestation clause + notary (mixed typed + handwritten)
        heading = "ATTESTATION CLAUSE"
        draw.text((mx, y), heading, fill=(10, 10, 10), font=font_heading)
        y += 50

        body_lines = [
            "We, the undersigned witnesses, declare that the foregoing instrument",
            "was signed, published, and declared by Margaret Eleanor Whitfield,",
            "the Testatrix, as her Last Will and Testament, in our presence, and",
            "that we, at her request and in her presence and in the presence of",
            "each other, have subscribed our names as attesting witnesses thereto.",
            "",
            "We further declare that the Testatrix appeared to be of sound mind",
            "and under no constraint or undue influence at the time of the",
            "execution of this Will.",
            "",
            "Executed on this 15th day of March, 2024.",
        ]
        y = draw_text_block(draw, body_lines, mx, y, font_body, line_spacing=1.40)

        y += 30
        # Witness 1 - handwritten signature + typed info
        draw.line([(mx + 50, y + 30), (mx + 400, y + 30)], fill=(60, 60, 60), width=1)
        draw_handwritten_text(draw, "James R. Morrison", mx + 80, y, size=24, color=(10, 10, 80))
        y += 50
        draw.text((mx + 50, y), "James R. Morrison", fill=(10, 10, 10), font=font_body)
        y += 28
        draw.text((mx + 50, y), "Address: 1150 Oak Valley Court, Fairfax, VA 22031", fill=(10, 10, 10), font=font_small)
        y += 40

        # Witness 2
        draw.line([(mx + 50, y + 30), (mx + 400, y + 30)], fill=(60, 60, 60), width=1)
        draw_handwritten_text(draw, "Sandra L. Hoffman", mx + 80, y, size=24, color=(10, 10, 80))
        y += 50
        draw.text((mx + 50, y), "Sandra L. Hoffman", fill=(10, 10, 10), font=font_body)
        y += 28
        draw.text((mx + 50, y), "Address: 738 Braddock Road, Alexandria, VA 22314", fill=(10, 10, 10), font=font_small)
        y += 60

        # Notary section
        draw.line([(mx, y), (max_x, y)], fill=(60, 60, 60), width=1)
        y += 20
        draw.text((mx, y), "NOTARIZATION", fill=(10, 10, 10), font=font_heading)
        y += 40
        notary_lines = [
            "Commonwealth of Virginia, County of Fairfax, ss.",
            "",
            "Subscribed, sworn to, and acknowledged before me by Margaret Eleanor",
            "Whitfield, the Testatrix, and by James R. Morrison and Sandra L.",
            "Hoffman, the witnesses, on this 15th day of March, 2024.",
        ]
        y = draw_text_block(draw, notary_lines, mx, y, font_body, line_spacing=1.40)

        y += 30
        draw.line([(mx + 50, y + 30), (mx + 400, y + 30)], fill=(60, 60, 60), width=1)
        draw_handwritten_text(draw, "Patricia Nguyen", mx + 100, y, size=24, color=(10, 10, 80))
        y += 50
        draw.text((mx + 50, y), "Patricia Nguyen, Notary Public", fill=(10, 10, 10), font=font_body)
        y += 28
        draw.text((mx + 50, y), "My commission expires: December 31, 2026", fill=(10, 10, 10), font=font_small)

    # Page number at bottom
    page_label = f"Page {page_num + 1} of 8"
    bbox = font_page.getbbox(page_label)
    pw = bbox[2] - bbox[0]
    draw.text(((IMG_W - pw) // 2, IMG_H - 80), page_label, fill=(80, 80, 80), font=font_page)

    # Add scan artifacts
    img = add_scan_noise(img)

    return img


def create_initial():
    os.makedirs(ESTATE_DIR, exist_ok=True)

    # Create each page as an image, then build an image-only PDF
    doc = pymupdf.open()

    for page_num in range(8):
        img = create_page_image(page_num)

        # Convert PIL Image to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Create a PDF page and insert the image (image-only = no text layer)
        page = doc.new_page(width=PAGE_W_PT, height=PAGE_H_PT)
        page.insert_image(
            pymupdf.Rect(0, 0, PAGE_W_PT, PAGE_H_PT),
            stream=img_bytes.read()
        )

    doc.save(OUTPUT)
    doc.close()

    # Verify no text layer
    verify_doc = pymupdf.open(OUTPUT)
    print(f"Created scanned will: {OUTPUT}")
    print(f"Page count: {verify_doc.page_count}")
    for i in range(verify_doc.page_count):
        text = verify_doc[i].get_text("text").strip()
        print(f"  Page {i+1} text length: {len(text)} chars (should be 0 for image-only)")
    verify_doc.close()

    # Open in Evince for GUI
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
