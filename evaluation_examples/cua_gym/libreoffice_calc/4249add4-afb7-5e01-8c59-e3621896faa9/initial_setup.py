"""
Initial Setup: Audit bibliography of a research paper draft.
Task ID: osworld_multi_apps_web_references_012
Domain: multi_apps (LibreOffice Writer + Calc)

Creates:
  - /home/user/Documents/paper_draft.odt  (research paper with 15 IEEE references)
  - /home/user/Desktop/ref_audit.ods      (empty audit spreadsheet with headers)
"""

import os
import shlex
import subprocess
import time

WORKDIR_DOCS = '/home/user/Documents'
WORKDIR_DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_references_012'
ODT_PATH = f'{WORKDIR_DOCS}/paper_draft.odt'
ODS_PATH = f'{WORKDIR_DESKTOP}/ref_audit.ods'


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


def create_paper_draft():
    """Create a research paper ODT with 15 IEEE-format references in bibliography."""
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import H, P, Span
    from odf import dc

    doc = OpenDocumentText()

    # Define heading style
    h1_style = Style(name="Heading 1", family="paragraph")
    h1_style.addElement(TextProperties(fontsize="16pt", fontweight="bold"))
    h1_style.addElement(ParagraphProperties(marginbottom="0.2cm", margintop="0.5cm"))
    doc.styles.addElement(h1_style)

    h2_style = Style(name="Heading 2", family="paragraph")
    h2_style.addElement(TextProperties(fontsize="13pt", fontweight="bold"))
    h2_style.addElement(ParagraphProperties(marginbottom="0.1cm", margintop="0.3cm"))
    doc.styles.addElement(h2_style)

    body_style = Style(name="Body Text", family="paragraph")
    body_style.addElement(TextProperties(fontsize="11pt"))
    doc.styles.addElement(body_style)

    ref_style = Style(name="Reference", family="paragraph")
    ref_style.addElement(TextProperties(fontsize="10pt"))
    ref_style.addElement(ParagraphProperties(margintop="0.1cm", marginbottom="0.1cm",
                                              textindent="-0.6cm", marginleft="0.6cm"))
    doc.styles.addElement(ref_style)

    # Title
    title_h = H(outlinelevel=1, stylename="Heading 1")
    title_h.addText("Deep Learning for Biomedical Image Segmentation: A Comprehensive Survey")
    doc.text.addElement(title_h)

    # Abstract
    abstract_h = H(outlinelevel=2, stylename="Heading 2")
    abstract_h.addText("Abstract")
    doc.text.addElement(abstract_h)

    abstract_p = P(stylename="Body Text")
    abstract_p.addText(
        "Biomedical image segmentation has witnessed remarkable advances with the advent of deep learning. "
        "This survey reviews state-of-the-art architectures including convolutional neural networks, "
        "transformer-based models, and hybrid approaches applied to medical imaging modalities such as "
        "MRI, CT, and histopathology. We analyze performance benchmarks, discuss remaining challenges "
        "in data scarcity and domain adaptation, and identify future research directions. Our analysis "
        "covers over 200 papers published between 2015 and 2024, highlighting key milestones and "
        "emerging trends in the field."
    )
    doc.text.addElement(abstract_p)

    # Introduction
    intro_h = H(outlinelevel=2, stylename="Heading 2")
    intro_h.addText("1. Introduction")
    doc.text.addElement(intro_h)

    intro_p1 = P(stylename="Body Text")
    intro_p1.addText(
        "Medical image segmentation is a fundamental task in computer-aided diagnosis, surgical planning, "
        "and treatment monitoring. Accurate delineation of anatomical structures and pathological regions "
        "enables clinicians to make more informed decisions and improves patient outcomes. Traditional "
        "segmentation methods relied on handcrafted features and domain-specific heuristics, which limited "
        "their generalizability across different imaging protocols and patient populations [1], [2]."
    )
    doc.text.addElement(intro_p1)

    intro_p2 = P(stylename="Body Text")
    intro_p2.addText(
        "The emergence of deep learning has fundamentally transformed the landscape of biomedical image "
        "analysis. Convolutional neural networks (CNNs), particularly the U-Net architecture [3], have "
        "become the de facto standard for medical image segmentation tasks. More recently, vision "
        "transformers [4] and hybrid CNN-transformer models [5] have demonstrated competitive performance, "
        "especially on large-scale datasets. Despite these advances, challenges remain in handling class "
        "imbalance [6], limited labeled data [7], and cross-domain generalization [8]."
    )
    doc.text.addElement(intro_p2)

    # Related Work
    related_h = H(outlinelevel=2, stylename="Heading 2")
    related_h.addText("2. Related Work")
    doc.text.addElement(related_h)

    related_p1 = P(stylename="Body Text")
    related_p1.addText(
        "Early work on automated medical image segmentation focused on atlas-based methods and statistical "
        "shape models [9]. Graph-cut methods provided globally optimal solutions for binary segmentation "
        "problems [10], while active contours offered a flexible framework for boundary detection [11]. "
        "Random forests and support vector machines were later applied to pixel-level classification, "
        "achieving strong performance on specific modalities [12]."
    )
    doc.text.addElement(related_p1)

    related_p2 = P(stylename="Body Text")
    related_p2.addText(
        "The introduction of fully convolutional networks (FCNs) [13] marked a paradigm shift, enabling "
        "end-to-end learning for dense prediction tasks. Subsequent encoder-decoder architectures with "
        "skip connections [3] addressed the loss of spatial information during downsampling. Attention "
        "mechanisms [14] further improved performance by focusing the model on relevant regions, while "
        "multi-scale feature fusion [15] captured contextual information at different resolutions."
    )
    doc.text.addElement(related_p2)

    # Methodology
    method_h = H(outlinelevel=2, stylename="Heading 2")
    method_h.addText("3. Methodology")
    doc.text.addElement(method_h)

    method_p = P(stylename="Body Text")
    method_p.addText(
        "We conducted a systematic literature review following PRISMA guidelines. Databases including "
        "PubMed, IEEE Xplore, and arXiv were queried for papers on deep learning-based medical image "
        "segmentation published between January 2015 and December 2024. Inclusion criteria required "
        "papers to report quantitative segmentation metrics on standard benchmarks. A total of 247 papers "
        "met our inclusion criteria after duplicate removal and quality assessment."
    )
    doc.text.addElement(method_p)

    # Results
    results_h = H(outlinelevel=2, stylename="Heading 2")
    results_h.addText("4. Results and Discussion")
    doc.text.addElement(results_h)

    results_p = P(stylename="Body Text")
    results_p.addText(
        "Our analysis reveals consistent performance improvements across all imaging modalities over "
        "the review period. Cardiac MRI segmentation achieved Dice scores exceeding 0.92 on benchmark "
        "datasets, compared to 0.78 for atlas-based methods. Brain tumor segmentation on BraTS showed "
        "improvements from 0.71 to 0.88 Dice for whole tumor class. However, performance on rare "
        "pathologies and out-of-distribution datasets remains a significant challenge."
    )
    doc.text.addElement(results_p)

    # Conclusion
    conclusion_h = H(outlinelevel=2, stylename="Heading 2")
    conclusion_h.addText("5. Conclusion")
    doc.text.addElement(conclusion_h)

    conclusion_p = P(stylename="Body Text")
    conclusion_p.addText(
        "This survey has provided a comprehensive overview of deep learning methods for biomedical "
        "image segmentation. Key findings include the dominance of encoder-decoder architectures, "
        "the growing importance of attention mechanisms, and the emerging role of self-supervised "
        "pre-training. Future directions include foundation models, federated learning for privacy-"
        "preserving training, and uncertainty quantification for clinical deployment."
    )
    doc.text.addElement(conclusion_p)

    # Bibliography header
    bib_h = H(outlinelevel=2, stylename="Heading 2")
    bib_h.addText("References")
    doc.text.addElement(bib_h)

    # 15 IEEE-format references
    # Format: [N] Author(s), "Title," Journal/Conf, vol., no., pp., year. doi: XX
    references = [
        # [1] Old paper (>10 years) - published 2008
        '[1] D. L. Pham, C. Xu, and J. L. Prince, "Current methods in medical image segmentation," '
        'Annu. Rev. Biomed. Eng., vol. 2, no. 1, pp. 315-337, 2000. doi: 10.1146/annurev.bioeng.2.1.315',

        # [2] Old paper - published 2006
        '[2] N. Paragios, Y. Chen, and O. Faugeras, Handbook of Mathematical Models in Computer Vision. '
        'New York, NY, USA: Springer, 2006. doi: 10.1007/0-387-28831-7',

        # [3] U-Net - highly cited peer-reviewed, 2015 (>10 years old by 2025)
        '[4] O. Ronneberger, P. Fischer, and T. Brox, "U-Net: Convolutional networks for biomedical '
        'image segmentation," in Proc. MICCAI, Munich, Germany, 2015, pp. 234-241. '
        'doi: 10.1007/978-3-319-24574-4_28',

        # [4] ViT - 2020, valid DOI, peer-reviewed
        '[4] A. Dosovitskiy et al., "An image is worth 16x16 words: Transformers for image recognition '
        'at scale," in Proc. ICLR, 2021. doi: 10.48550/arXiv.2010.11929',

        # [5] TransUNet - 2021, valid DOI
        '[5] J. Chen et al., "TransUNet: Transformers make strong encoders for medical image segmentation," '
        'arXiv preprint arXiv:2102.04306, 2021. doi: 10.48550/arXiv.2102.04306',

        # [6] Class imbalance - 2017, valid DOI, peer-reviewed
        '[6] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollar, "Focal loss for dense object '
        'detection," in Proc. ICCV, Venice, Italy, 2017, pp. 2980-2988. doi: 10.1109/ICCV.2017.324',

        # [7] Semi-supervised learning - 2020
        '[7] X. Luo et al., "Semi-supervised medical image segmentation through dual-task consistency," '
        'in Proc. AAAI, 2021, pp. 8801-8809. doi: 10.1609/aaai.v35i10.17066',

        # [8] Domain adaptation - broken DOI
        '[8] K. Kamnitsas et al., "Unsupervised domain adaptation in brain lesion segmentation with '
        'adversarial networks," in Proc. IPMI, 2017, pp. 597-609. doi: 10.1007/978-3-319-99999-9_00',

        # [9] Atlas-based - 2010, old
        '[9] T. F. Cootes, C. J. Taylor, D. H. Cooper, and J. Graham, "Active shape models-their '
        'training and application," Comput. Vis. Image Underst., vol. 61, no. 1, pp. 38-59, 1995. '
        'doi: 10.1006/cviu.1995.1004',

        # [10] Graph cuts - 2001, old
        '[10] Y. Boykov and M.-P. Jolly, "Interactive graph cuts for optimal boundary and region '
        'segmentation of objects in N-D images," in Proc. ICCV, 2001, pp. 105-112. '
        'doi: 10.1109/ICCV.2001.937505',

        # [11] Active contours - 1988, very old, valid
        '[11] M. Kass, A. Witkin, and D. Terzopoulos, "Snakes: Active contour models," '
        'Int. J. Comput. Vis., vol. 1, no. 4, pp. 321-331, 1988. doi: 10.1007/BF00133570',

        # [12] Random forest - 2012, >10 years
        '[12] A. Criminisi, J. Shotton, and E. Konukoglu, "Decision forests: A unified framework '
        'for classification, regression, density estimation, manifold learning and semi-supervised '
        'learning," Found. Trends Comput. Graph. Vis., vol. 7, pp. 81-227, 2012. '
        'doi: 10.1561/0600000035',

        # [13] FCN - 2015, valid, >10 years
        '[13] J. Long, E. Shelhamer, and T. Darrell, "Fully convolutional networks for semantic '
        'segmentation," in Proc. CVPR, Boston, MA, USA, 2015, pp. 3431-3440. '
        'doi: 10.1109/CVPR.2015.7298965',

        # [14] Attention U-Net - 2018, valid, peer-reviewed
        '[14] O. Oktay et al., "Attention U-Net: Learning where to look for the pancreas," '
        'in Proc. MIDL, Amsterdam, Netherlands, 2018. doi: 10.48550/arXiv.1804.03999',

        # [15] Multi-scale - blog post / not peer-reviewed
        '[15] Y. Liu, "Multi-scale feature fusion for medical image segmentation," '
        'Medium Blog Post, https://medium.com/@yliu/multiscale-seg-2022, 2022. '
        'doi: 10.99999/not-a-real-doi-99999',
    ]

    for ref_text in references:
        ref_p = P(stylename="Reference")
        ref_p.addText(ref_text)
        doc.text.addElement(ref_p)

    # Ensure Documents directory exists
    os.makedirs(WORKDIR_DOCS, exist_ok=True)
    doc.save(ODT_PATH)
    print(f'paper_draft.odt created: {ODT_PATH}')


def create_ref_audit_ods():
    """Create an empty ref_audit.ods with headers only."""
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TableCellProperties, TextProperties
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    ods = OpenDocumentSpreadsheet()

    # Header style
    header_style = Style(name="HeaderStyle", family="table-cell")
    header_style.addElement(TableCellProperties(backgroundcolor="#4472C4", border="0.05cm solid #000000"))
    header_style.addElement(TextProperties(fontweight="bold", color="#FFFFFF", fontsize="11pt"))
    ods.styles.addElement(header_style)

    # Normal cell style
    cell_style = Style(name="CellStyle", family="table-cell")
    cell_style.addElement(TableCellProperties(border="0.02cm solid #CCCCCC"))
    cell_style.addElement(TextProperties(fontsize="10pt"))
    ods.styles.addElement(cell_style)

    table = Table(name="Audit")
    ods.spreadsheet.addElement(table)

    # Headers row
    headers = ["Ref_Number", "Title", "DOI_Valid", "Citation_Count", "Age_Years", "Peer_Reviewed", "Flag"]
    header_row = TableRow()
    for h in headers:
        cell = TableCell(stylename="HeaderStyle", valuetype="string")
        cell.addElement(P(text=h))
        header_row.addElement(cell)
    table.addElement(header_row)

    # Ensure Desktop directory exists
    os.makedirs(WORKDIR_DESKTOP, exist_ok=True)
    ods.save(ODS_PATH)
    print(f'ref_audit.ods created: {ODS_PATH}')


def main():
    create_paper_draft()
    create_ref_audit_ods()

    # GUI-ready startup: open the Writer doc and Calc file
    # Open paper_draft.odt in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{ODT_PATH}"', delay_sec=3.0)
    # Open ref_audit.ods in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{ODS_PATH}"', delay_sec=2.0)
    # Open Chrome for DOI verification
    launch_gui('google-chrome --new-window "https://doi.org"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer, LibreOffice Calc, and Chrome with DISPLAY=:0')


main()
