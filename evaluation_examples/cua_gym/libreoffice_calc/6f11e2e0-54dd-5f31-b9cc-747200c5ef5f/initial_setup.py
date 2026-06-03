"""
Initial Setup: Create loan_agreement.pdf for amortization schedule task
Task ID: pdf_cross_042
Domain: libreoffice_calc
"""

import os
import shlex
import subprocess
import time

# VM paths
WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_042'
PDF_OUTPUT = f'{WORKDIR}/loan_agreement.pdf'


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


def create_loan_agreement_pdf():
    """Create a realistic 3-page loan agreement PDF using reportlab."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import black, grey, lightgrey, HexColor
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    except ImportError:
        import subprocess as sp
        sp.run(['pip3', 'install', 'reportlab'], check=True)
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import black, grey, lightgrey, HexColor
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

    # Ensure Documents directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=HexColor("#1a1a6b"),
        spaceAfter=16,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor("#003366"),
        spaceBefore=14,
        spaceAfter=6
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=16
    )
    bold_style = ParagraphStyle(
        'CustomBold',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceAfter=6
    )
    small_style = ParagraphStyle(
        'SmallText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor("#555555"),
        spaceAfter=6
    )

    # ─── PAGE 1: Cover / Summary of Loan Terms ───────────────────────────────

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("RESIDENTIAL MORTGAGE LOAN AGREEMENT", title_style))
    story.append(Paragraph("Loan Agreement No.: RML-2025-04721", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Parties
    story.append(Paragraph("PARTIES TO THE AGREEMENT", heading_style))
    parties_data = [
        ["Lender:", "Pinnacle Federal Savings Bank"],
        ["", "789 Commerce Boulevard, Suite 400"],
        ["", "Austin, TX 78701"],
        ["Borrower:", "James R. Whitfield"],
        ["", "4312 Maple Grove Lane"],
        ["", "Austin, TX 78745"],
        ["Co-Borrower:", "Catherine M. Whitfield"],
        ["", "4312 Maple Grove Lane"],
        ["", "Austin, TX 78745"],
    ]
    for row in parties_data:
        label = row[0]
        value = row[1]
        if label:
            story.append(Paragraph(f"<b>{label}</b> {value}", normal_style))
        else:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{value}", normal_style))

    story.append(Spacer(1, 0.2 * inch))

    # Key loan terms table
    story.append(Paragraph("LOAN TERMS SUMMARY", heading_style))

    terms_data = [
        ["Term", "Detail"],
        ["Principal:", "$250,000"],
        ["Annual Interest Rate:", "5.25%"],
        ["Loan Term:", "30 years"],
        ["Payment Frequency:", "Monthly"],
        ["First Payment Due:", "June 1, 2025"],
        ["Maturity Date:", "May 1, 2055"],
        ["Loan Type:", "Fixed-Rate Conventional Mortgage"],
        ["Property Address:", "4312 Maple Grove Lane, Austin, TX 78745"],
        ["Property Type:", "Single Family Residential"],
    ]

    terms_table = Table(terms_data, colWidths=[2.2 * inch, 3.8 * inch])
    terms_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#1a1a6b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), HexColor("#EEF2FF")]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(terms_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(
        "By signing below, the Borrower(s) acknowledge receipt of this Loan Agreement and agree to the terms "
        "and conditions stated herein. This document has been prepared pursuant to applicable federal and state "
        "lending regulations including TILA, RESPA, and the Texas Finance Code.",
        small_style
    ))

    story.append(PageBreak())

    # ─── PAGE 2: Terms and Conditions ────────────────────────────────────────

    story.append(Paragraph("TERMS AND CONDITIONS", title_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("1. PROMISE TO PAY", heading_style))
    story.append(Paragraph(
        "Borrower promises to pay to the order of Lender the principal sum of Two Hundred Fifty Thousand "
        "Dollars ($250,000.00), together with interest on the outstanding principal balance, at the annual "
        "rate of five and one-quarter percent (5.25%), calculated on a monthly basis. The Borrower shall "
        "make equal monthly installment payments consisting of principal and interest until the loan is "
        "paid in full. Each monthly payment shall be applied first to accrued interest, then to the "
        "reduction of principal.",
        normal_style
    ))

    story.append(Paragraph("2. PAYMENT SCHEDULE", heading_style))
    story.append(Paragraph(
        "Payments shall be made on the first (1st) day of each calendar month beginning June 1, 2025. "
        "The regular monthly payment amount has been calculated using the standard amortization formula. "
        "All 360 monthly payments shall be equal in amount except for the final payment, which shall be "
        "adjusted to retire the remaining principal balance and accrued interest. Payments shall be made "
        "to Pinnacle Federal Savings Bank, Payment Processing Center, P.O. Box 8842, Austin, TX 78714, "
        "or as otherwise directed by Lender.",
        normal_style
    ))

    story.append(Paragraph("3. INTEREST CALCULATION", heading_style))
    story.append(Paragraph(
        "Interest shall accrue on the outstanding principal balance at the rate of 5.25% per annum. "
        "For the purpose of monthly payment calculation, the monthly periodic rate shall be the annual "
        "rate divided by twelve (5.25% / 12 = 0.4375% per month). Interest is calculated on the "
        "outstanding principal balance at the beginning of each payment period. The monthly payment "
        "amount is calculated to fully amortize the loan over the 30-year term.",
        normal_style
    ))

    story.append(Paragraph("4. PREPAYMENT", heading_style))
    story.append(Paragraph(
        "Borrower may prepay the principal balance in whole or in part at any time without penalty. "
        "Any prepayment shall be applied to the outstanding principal balance and shall not relieve "
        "Borrower of the obligation to make regular monthly payments as they become due. Partial "
        "prepayments will reduce the outstanding principal but will not alter the required monthly "
        "payment amount unless specifically requested by Borrower and approved by Lender.",
        normal_style
    ))

    story.append(Paragraph("5. LATE CHARGES", heading_style))
    story.append(Paragraph(
        "If Borrower fails to pay any monthly installment within fifteen (15) calendar days after the "
        "date it is due, Borrower shall pay to Lender a late charge equal to five percent (5%) of the "
        "overdue installment. Late charges shall be assessed for each month or portion thereof in which "
        "a payment remains overdue. Lender reserves the right to report delinquent payments to credit "
        "reporting agencies after sixty (60) days.",
        normal_style
    ))

    story.append(Paragraph("6. ESCROW ACCOUNT", heading_style))
    story.append(Paragraph(
        "Borrower agrees to establish and maintain an escrow account with Lender for the payment of "
        "property taxes and homeowner's insurance premiums. The monthly escrow payment, as determined "
        "by annual analysis, shall be collected in addition to the principal and interest payment. "
        "The escrow account is separate from the principal and interest payment amounts stated in "
        "this agreement.",
        normal_style
    ))

    story.append(PageBreak())

    # ─── PAGE 3: Additional Provisions and Signatures ────────────────────────

    story.append(Paragraph("ADDITIONAL PROVISIONS AND SIGNATURES", title_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("7. DEFAULT", heading_style))
    story.append(Paragraph(
        "The Borrower shall be in default if: (a) Borrower fails to pay any monthly installment when "
        "due and such failure continues for thirty (30) days; (b) Borrower fails to maintain the "
        "property in good repair; (c) Borrower abandons the property; (d) Borrower sells or transfers "
        "the property without Lender's prior written consent; or (e) Borrower files for bankruptcy or "
        "becomes insolvent. Upon default, Lender may declare the entire outstanding balance immediately "
        "due and payable.",
        normal_style
    ))

    story.append(Paragraph("8. INSURANCE REQUIREMENTS", heading_style))
    story.append(Paragraph(
        "Borrower agrees to maintain standard homeowner's insurance in an amount not less than the "
        "replacement cost of the improvements on the property, with Lender named as mortgagee. "
        "Flood insurance shall be required if the property is located in a designated flood hazard "
        "area. Evidence of insurance shall be provided to Lender annually.",
        normal_style
    ))

    story.append(Paragraph("9. GOVERNING LAW", heading_style))
    story.append(Paragraph(
        "This Loan Agreement shall be governed by and construed in accordance with the laws of the "
        "State of Texas, without regard to conflicts of law principles. Any disputes arising under "
        "this agreement shall be resolved in the courts of Travis County, Texas. Each party consents "
        "to the personal jurisdiction of such courts.",
        normal_style
    ))

    story.append(Paragraph("10. ACKNOWLEDGMENT", heading_style))
    story.append(Paragraph(
        "Borrower acknowledges having read and understood all provisions of this Loan Agreement. "
        "Borrower certifies that all information provided in the loan application is true and correct. "
        "This agreement constitutes the entire agreement between the parties with respect to the loan "
        "and supersedes all prior negotiations, representations, warranties, and understandings.",
        normal_style
    ))

    story.append(Spacer(1, 0.3 * inch))

    # Signature block
    sig_data = [
        ["BORROWER SIGNATURES", "", "DATE"],
        ["", "", ""],
        ["_________________________________", "    ", "________________"],
        ["James R. Whitfield (Borrower)", "", ""],
        ["", "", ""],
        ["_________________________________", "    ", "________________"],
        ["Catherine M. Whitfield (Co-Borrower)", "", ""],
        ["", "", ""],
        ["_________________________________", "    ", "________________"],
        ["Authorized Representative, Pinnacle Federal Savings Bank", "", ""],
    ]
    sig_table = Table(sig_data, colWidths=[3.5 * inch, 0.5 * inch, 2 * inch])
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, black),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sig_table)

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "Loan Agreement No.: RML-2025-04721 | Date Prepared: April 15, 2025 | "
        "NMLS ID: 478263 | This is a legally binding document.",
        small_style
    ))

    doc.build(story)
    print(f'Initial PDF created: {PDF_OUTPUT}')


def main():
    create_loan_agreement_pdf()

    # Verify file exists
    if not os.path.exists(PDF_OUTPUT):
        raise RuntimeError(f'ERROR: PDF not created at {PDF_OUTPUT}')
    file_size = os.path.getsize(PDF_OUTPUT)
    print(f'File size: {file_size} bytes')

    # GUI-ready startup: open the PDF in evince
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with loan_agreement.pdf using DISPLAY=:0')


main()
