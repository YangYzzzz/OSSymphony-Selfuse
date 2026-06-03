"""
Initial Setup: Create a scanned legal contract PDF (image-only, no text layer)
Task ID: pdf_gf1_027
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'scanned_contract'
OUTPUT = f'{DOCUMENTS}/{TASK_ID}.pdf'


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


# --- Contract text content for 3 pages ---

PAGE1_LINES = [
    ("PROFESSIONAL SERVICES AGREEMENT", 18, True),
    ("", 12, False),
    ("This Professional Services Agreement (the \"Agreement\") is entered into", 11, False),
    ("as of March 15, 2025, by and between:", 11, False),
    ("", 11, False),
    ("Meridian Technology Solutions Inc., a Delaware corporation with its", 11, False),
    ("principal office at 4500 Innovation Drive, Suite 200, San Jose, CA 95134", 11, False),
    ("(hereinafter referred to as the \"Service Provider\" or \"First Party\"),", 11, False),
    ("", 11, False),
    ("AND", 12, True),
    ("", 11, False),
    ("Cascade Financial Group LLC, a New York limited liability company with", 11, False),
    ("its principal office at 280 Park Avenue, 38th Floor, New York, NY 10017", 11, False),
    ("(hereinafter referred to as the \"Client\" or \"Second Party\").", 11, False),
    ("", 11, False),
    ("Each individually referred to as a \"Party\" and collectively as the \"Parties.\"", 11, False),
    ("", 11, False),
    ("RECITALS", 14, True),
    ("", 11, False),
    ("WHEREAS, the Service Provider is engaged in the business of providing", 11, False),
    ("enterprise software development, cloud infrastructure management, and", 11, False),
    ("cybersecurity consulting services; and", 11, False),
    ("", 11, False),
    ("WHEREAS, the Client desires to engage the Service Provider to perform", 11, False),
    ("certain professional services as more particularly described herein; and", 11, False),
    ("", 11, False),
    ("WHEREAS, the Service Provider hereby agrees to provide such services", 11, False),
    ("subject to the terms and conditions set forth in this Agreement;", 11, False),
    ("", 11, False),
    ("NOW, THEREFORE, in consideration of the mutual covenants and agreements", 11, False),
    ("contained herein, and for other good and valuable consideration, the", 11, False),
    ("receipt and sufficiency of which are hereby acknowledged, the Parties", 11, False),
    ("agree as follows:", 11, False),
    ("", 11, False),
    ("ARTICLE 1 - SCOPE OF SERVICES", 13, True),
    ("", 11, False),
    ("1.1  The Service Provider shall provide the following services to the", 11, False),
    ("Client (collectively, the \"Services\"):", 11, False),
    ("", 11, False),
    ("     (a)  Design, develop, and deploy a custom enterprise resource", 11, False),
    ("          planning (ERP) system tailored to the Client's operational", 11, False),
    ("          requirements, including but not limited to financial reporting,", 11, False),
    ("          inventory management, and human resources modules;", 11, False),
    ("", 11, False),
    ("     (b)  Provide ongoing cloud infrastructure management services", 11, False),
    ("          including server provisioning, load balancing, and disaster", 11, False),
    ("          recovery planning for a period of twenty-four (24) months;", 11, False),
    ("", 11, False),
    ("     (c)  Conduct comprehensive cybersecurity assessments and implement", 11, False),
    ("          appropriate security measures in accordance with industry best", 11, False),
    ("          practices and applicable regulatory requirements.", 11, False),
]

PAGE2_LINES = [
    ("ARTICLE 2 - COMPENSATION AND PAYMENT TERMS", 13, True),
    ("", 11, False),
    ("2.1  In consideration for the Services, the Client shall pay the Service", 11, False),
    ("Provider a total fee of Two Million Four Hundred Thousand Dollars", 11, False),
    ("($2,400,000.00), payable according to the following schedule:", 11, False),
    ("", 11, False),
    ("     (a)  An initial deposit of $480,000.00 (twenty percent) due upon", 11, False),
    ("          execution of this Agreement;", 11, False),
    ("", 11, False),
    ("     (b)  Monthly installments of $80,000.00 for the duration of the", 11, False),
    ("          service period, due on the first business day of each month;", 11, False),
    ("", 11, False),
    ("     (c)  A final payment upon satisfactory completion of all Services", 11, False),
    ("          as determined by mutual written agreement of the Parties.", 11, False),
    ("", 11, False),
    ("2.2  All payments shall be made in United States Dollars by wire transfer", 11, False),
    ("to the account designated by the Service Provider.", 11, False),
    ("", 11, False),
    ("ARTICLE 3 - TERM AND TERMINATION", 13, True),
    ("", 11, False),
    ("3.1  This Agreement shall commence on the Effective Date and continue", 11, False),
    ("for a period of twenty-four (24) months, unless earlier terminated in", 11, False),
    ("accordance with the provisions of this Article.", 11, False),
    ("", 11, False),
    ("3.2  Either Party may terminate this Agreement for cause upon thirty (30)", 11, False),
    ("days' written notice if the other Party materially breaches any term of", 11, False),
    ("this Agreement and fails to cure such breach within the notice period.", 11, False),
    ("", 11, False),
    ("ARTICLE 4 - CONFIDENTIALITY", 13, True),
    ("", 11, False),
    ("4.1  Each Party acknowledges that in the course of performing its", 11, False),
    ("obligations under this Agreement, it may receive or have access to", 11, False),
    ("Confidential Information of the other Party. Each Party hereby agrees", 11, False),
    ("to hold all such Confidential Information in strict confidence and", 11, False),
    ("shall not disclose, publish, or otherwise disseminate such information", 11, False),
    ("to any third party without the prior written consent of the disclosing", 11, False),
    ("Party, except as required by applicable law or regulation.", 11, False),
    ("", 11, False),
    ("ARTICLE 5 - INTELLECTUAL PROPERTY", 13, True),
    ("", 11, False),
    ("5.1  All intellectual property, including but not limited to software", 11, False),
    ("code, documentation, designs, and related materials developed by the", 11, False),
    ("Service Provider specifically for the Client under this Agreement", 11, False),
    ("(\"Work Product\") shall be the exclusive property of the Client upon", 11, False),
    ("full payment of all fees due hereunder.", 11, False),
    ("", 11, False),
    ("5.2  The Service Provider retains all rights to its pre-existing", 11, False),
    ("intellectual property, tools, frameworks, and methodologies, and grants", 11, False),
    ("the Client a non-exclusive, perpetual license to use such materials", 11, False),
    ("solely as incorporated into the Work Product.", 11, False),
]

PAGE3_LINES = [
    ("ARTICLE 6 - LIMITATION OF LIABILITY", 13, True),
    ("", 11, False),
    ("6.1  IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER PARTY FOR", 11, False),
    ("ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES,", 11, False),
    ("REGARDLESS OF THE CAUSE OF ACTION OR THE THEORY OF LIABILITY, EVEN IF", 11, False),
    ("SUCH PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.", 11, False),
    ("", 11, False),
    ("6.2  The Service Provider's total aggregate liability under this", 11, False),
    ("Agreement shall not exceed the total fees paid by the Client under", 11, False),
    ("this Agreement during the twelve (12) months preceding the event", 11, False),
    ("giving rise to the claim.", 11, False),
    ("", 11, False),
    ("ARTICLE 7 - GOVERNING LAW AND DISPUTE RESOLUTION", 13, True),
    ("", 11, False),
    ("7.1  This Agreement shall be governed by and construed in accordance", 11, False),
    ("with the laws of the State of New York, without regard to its conflict", 11, False),
    ("of laws principles.", 11, False),
    ("", 11, False),
    ("7.2  Any dispute arising out of or in connection with this Agreement", 11, False),
    ("shall first be submitted to mediation. If the dispute is not resolved", 11, False),
    ("through mediation within sixty (60) days, either Party may pursue", 11, False),
    ("binding arbitration in New York, New York.", 11, False),
    ("", 11, False),
    ("ARTICLE 8 - GENERAL PROVISIONS", 13, True),
    ("", 11, False),
    ("8.1  This Agreement constitutes the entire agreement between the Parties", 11, False),
    ("with respect to the subject matter hereof and supersedes all prior", 11, False),
    ("negotiations, representations, warranties, commitments, and agreements.", 11, False),
    ("", 11, False),
    ("8.2  No amendment or modification of this Agreement shall be valid or", 11, False),
    ("binding unless made in writing and signed by both Parties.", 11, False),
    ("", 11, False),
    ("IN WITNESS WHEREOF, the Parties have executed this Agreement as of the", 11, False),
    ("date first written above.", 11, False),
    ("", 11, False),
    ("", 11, False),
    ("_______________________________          _______________________________", 11, False),
    ("Elena Vasquez                            Robert J. Thornton III", 11, False),
    ("Chief Executive Officer                  Managing Director", 11, False),
    ("Meridian Technology Solutions Inc.        Cascade Financial Group LLC", 11, False),
    ("", 11, False),
    ("Date: March 15, 2025                     Date: March 15, 2025", 11, False),
]

ALL_PAGES = [PAGE1_LINES, PAGE2_LINES, PAGE3_LINES]


def create_text_pdf(output_path):
    """Create a PDF with real text content (intermediate step)."""
    import pymupdf

    doc = pymupdf.open()

    for page_lines in ALL_PAGES:
        page = doc.new_page(width=612, height=792)  # Letter size
        y = 72  # top margin

        for text, fontsize, bold in page_lines:
            if text == "":
                y += fontsize * 0.6
                continue
            fontname = "hebo" if bold else "helv"
            page.insert_text(
                pymupdf.Point(72, y),
                text,
                fontsize=fontsize,
                fontname=fontname,
                color=(0, 0, 0),
            )
            y += fontsize * 1.4

    doc.save(output_path)
    doc.close()


def create_scanned_pdf(text_pdf_path, output_path):
    """Render each page of text PDF to image, then create image-only PDF (no text layer)."""
    import pymupdf
    from PIL import Image, ImageFilter
    import random

    text_doc = pymupdf.open(text_pdf_path)
    scan_doc = pymupdf.open()

    for page_idx in range(text_doc.page_count):
        page = text_doc[page_idx]
        # Render at 200 DPI for realistic scan quality
        mat = pymupdf.Matrix(200 / 72, 200 / 72)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Apply scan effects: slight noise, very slight blur
        # Add slight yellowish tint to simulate aged paper
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.95)

        # Add very slight Gaussian noise for scan realism
        import numpy as np
        arr = np.array(img, dtype=np.float32)
        noise = np.random.normal(0, 2, arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)

        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Create new page with same dimensions as original and insert image
        new_page = scan_doc.new_page(width=612, height=792)
        img_rect = pymupdf.Rect(0, 0, 612, 792)
        new_page.insert_image(img_rect, stream=img_bytes.read())

    scan_doc.save(output_path)
    scan_doc.close()
    text_doc.close()


def create_initial():
    os.makedirs(DOCUMENTS, exist_ok=True)

    # Step 1: Create intermediate text PDF
    text_pdf = f'/tmp/contract_text.pdf'
    create_text_pdf(text_pdf)

    # Step 2: Convert to scanned (image-only) PDF
    create_scanned_pdf(text_pdf, OUTPUT)

    # Clean up intermediate
    os.remove(text_pdf)

    # Verify: text extraction should return empty/minimal text
    import pymupdf
    doc = pymupdf.open(OUTPUT)
    for i in range(doc.page_count):
        text = doc[i].get_text("text").strip()
        print(f"  Page {i+1} text length: {len(text)} chars (should be ~0)")
    print(f"  Page count: {doc.page_count}")
    doc.close()

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
