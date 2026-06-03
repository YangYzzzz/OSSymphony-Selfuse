"""
Initial Setup: Journal editor reference quality check task
Task ID: osworld_multi_apps_web_references_014
Domain: libreoffice_calc (multi-app: calc + writer + odt files)

Creates:
  - ~/Desktop/submissions/ folder with 3 .odt paper draft files
  - ~/Desktop/editorial_db.ods with header row only (empty database)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_references_014'

SUBMISSIONS_DIR = f'{WORKDIR}/Desktop/submissions'
EDITORIAL_DB = f'{WORKDIR}/Desktop/editorial_db.ods'


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


def create_odt_submission(filepath, paper_title, author_name, coauthor_name, references):
    """Create an .odt submission file using python-odf."""
    try:
        from odf.opendocument import OpenDocumentText
        from odf.text import P, H, Span
        from odf.style import Style, TextProperties, ParagraphProperties
        from odf import style as odf_style

        doc = OpenDocumentText()

        # Define heading style
        h1_style = Style(name="Heading1Custom", family="paragraph")
        h1_style.addElement(TextProperties(fontsize="16pt", fontweight="bold"))
        doc.automaticstyles.addElement(h1_style)

        normal_style = Style(name="NormalText", family="paragraph")
        normal_style.addElement(TextProperties(fontsize="12pt"))
        doc.automaticstyles.addElement(normal_style)

        # Title
        title_p = H(outlinelevel=1)
        title_p.addText(paper_title)
        doc.text.addElement(title_p)

        # Authors
        author_p = P()
        author_p.addText(f"Authors: {author_name}, {coauthor_name}")
        doc.text.addElement(author_p)

        # Abstract
        abstract_h = H(outlinelevel=2)
        abstract_h.addText("Abstract")
        doc.text.addElement(abstract_h)

        abstract_p = P()
        abstract_p.addText(
            "This paper presents a comprehensive study examining key factors in the field. "
            "We employ a mixed-methods approach combining quantitative analysis with qualitative review. "
            "Our findings contribute to the existing literature and provide new insights for practitioners."
        )
        doc.text.addElement(abstract_p)

        # Introduction
        intro_h = H(outlinelevel=2)
        intro_h.addText("1. Introduction")
        doc.text.addElement(intro_h)

        intro_p = P()
        intro_p.addText(
            "The study of information systems has grown considerably in recent years. "
            "Multiple researchers have explored the theoretical underpinnings and practical applications. "
            "This paper builds on the foundational work established in the literature."
        )
        doc.text.addElement(intro_p)

        # Methodology
        method_h = H(outlinelevel=2)
        method_h.addText("2. Methodology")
        doc.text.addElement(method_h)

        method_p = P()
        method_p.addText(
            "We conducted a systematic review following established protocols. "
            "Data collection involved structured interviews and survey instruments. "
            "Statistical analysis was performed using standard software packages."
        )
        doc.text.addElement(method_p)

        # Results
        results_h = H(outlinelevel=2)
        results_h.addText("3. Results and Discussion")
        doc.text.addElement(results_h)

        results_p = P()
        results_p.addText(
            "The results indicate significant relationships between the studied variables. "
            "These findings are consistent with prior research in related domains. "
            "Implications for theory and practice are discussed in the following sections."
        )
        doc.text.addElement(results_p)

        # Bibliography section
        bib_h = H(outlinelevel=2)
        bib_h.addText("References")
        doc.text.addElement(bib_h)

        for ref in references:
            ref_p = P()
            ref_p.addText(ref)
            doc.text.addElement(ref_p)

        doc.save(filepath)
        print(f'Created: {filepath}')
    except ImportError:
        # Fallback: create a simple text-based ODF
        _create_odt_fallback(filepath, paper_title, author_name, coauthor_name, references)


def _create_odt_fallback(filepath, paper_title, author_name, coauthor_name, references):
    """Fallback: create ODF file using raw XML zip."""
    import zipfile
    import textwrap

    ref_paragraphs = ""
    for ref in references:
        escaped = ref.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        ref_paragraphs += f'<text:p text:style-name="Text_20_Body">{escaped}</text:p>\n'

    content_xml = textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-content
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
        xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
        xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
        office:version="1.3">
      <office:automatic-styles/>
      <office:body>
        <office:text>
          <text:h text:style-name="Heading_20_1" text:outline-level="1">{paper_title}</text:h>
          <text:p text:style-name="Text_20_Body">Authors: {author_name}, {coauthor_name}</text:p>
          <text:h text:style-name="Heading_20_2" text:outline-level="2">Abstract</text:h>
          <text:p text:style-name="Text_20_Body">This paper presents a comprehensive study examining key factors in the field. We employ a mixed-methods approach combining quantitative analysis with qualitative review. Our findings contribute to the existing literature and provide new insights for practitioners.</text:p>
          <text:h text:style-name="Heading_20_2" text:outline-level="2">1. Introduction</text:h>
          <text:p text:style-name="Text_20_Body">The study of information systems has grown considerably in recent years. Multiple researchers have explored the theoretical underpinnings and practical applications. This paper builds on the foundational work established in the literature.</text:p>
          <text:h text:style-name="Heading_20_2" text:outline-level="2">2. Methodology</text:h>
          <text:p text:style-name="Text_20_Body">We conducted a systematic review following established protocols. Data collection involved structured interviews and survey instruments. Statistical analysis was performed using standard software packages.</text:p>
          <text:h text:style-name="Heading_20_2" text:outline-level="2">3. Results and Discussion</text:h>
          <text:p text:style-name="Text_20_Body">The results indicate significant relationships between the studied variables. These findings are consistent with prior research in related domains. Implications for theory and practice are discussed in the following sections.</text:p>
          <text:h text:style-name="Heading_20_2" text:outline-level="2">References</text:h>
          {ref_paragraphs}
        </office:text>
      </office:body>
    </office:document-content>
    """)

    manifest_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <manifest:manifest
        xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
        manifest:version="1.3">
      <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.text"/>
      <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
      <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
      <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
    </manifest:manifest>
    """)

    styles_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-styles
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
        xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
        xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
        office:version="1.3">
      <office:styles>
        <style:style style:name="Heading_20_1" style:family="paragraph" style:display-name="Heading 1">
          <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
        </style:style>
        <style:style style:name="Heading_20_2" style:family="paragraph" style:display-name="Heading 2">
          <style:text-properties fo:font-size="14pt" fo:font-weight="bold"/>
        </style:style>
        <style:style style:name="Text_20_Body" style:family="paragraph" style:display-name="Text Body">
          <style:text-properties fo:font-size="12pt"/>
        </style:style>
      </office:styles>
    </office:document-styles>
    """)

    meta_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-meta
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
        xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
        office:version="1.3">
      <office:meta>
        <meta:generator>CUA-Gym Setup</meta:generator>
      </office:meta>
    </office:document-meta>
    """)

    mimetype = "application/vnd.oasis.opendocument.text"

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
    print(f'Created (fallback): {filepath}')


def create_editorial_db_ods(filepath):
    """Create the empty editorial_db.ods with header row only."""
    import zipfile
    import textwrap

    # Headers only — no data rows
    headers = ["Paper_ID", "Ref_Number", "Title", "DOI", "Citation_Count", "Self_Citation", "DOI_Valid"]

    header_cells = ""
    for col_idx, h in enumerate(headers):
        # ODS uses 0-based columns in table:table-cell sequences
        header_cells += (
            f'<table:table-cell office:value-type="string">'
            f'<text:p>{h}</text:p>'
            f'</table:table-cell>'
        )

    content_xml = textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-content
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
        xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
        xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
        xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
        office:version="1.3">
      <office:automatic-styles/>
      <office:body>
        <office:spreadsheet>
          <table:table table:name="Sheet1">
            <table:table-row>
              {header_cells}
            </table:table-row>
          </table:table>
        </office:spreadsheet>
      </office:body>
    </office:document-content>
    """)

    manifest_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <manifest:manifest
        xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
        manifest:version="1.3">
      <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.spreadsheet"/>
      <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
      <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
      <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
    </manifest:manifest>
    """)

    styles_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-styles
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
        office:version="1.3">
      <office:styles/>
    </office:document-styles>
    """)

    meta_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-meta
        xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
        xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
        office:version="1.3">
      <office:meta>
        <meta:generator>CUA-Gym Setup</meta:generator>
      </office:meta>
    </office:document-meta>
    """)

    mimetype = "application/vnd.oasis.opendocument.spreadsheet"

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
    print(f'Created: {filepath}')


def create_initial():
    # Create submissions directory
    os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
    print(f'Created directory: {SUBMISSIONS_DIR}')

    # =========================================================================
    # submission1.odt
    # Author: Dr. Elena Martinez (with some self-citations)
    # 12 references — 3 are self-citations (25% > 20% threshold → flag)
    # Some DOIs are broken
    # =========================================================================
    submission1_refs = [
        "[1] Martinez, E., & Thompson, R. (2021). Adaptive learning frameworks in digital environments. Journal of Educational Technology, 45(3), 112-129. DOI: 10.1016/j.jet.2021.03.112",
        "[2] Johnson, A., Lee, K., & Park, S. (2020). Deep learning for natural language processing: A survey. ACM Computing Surveys, 53(2), 1-34. DOI: 10.1145/3378673",
        "[3] Martinez, E. (2019). Cognitive load and interface design principles. Human-Computer Interaction, 34(1), 45-78. DOI: 10.1080/hci.2019.1589234",
        "[4] Williams, B., Chen, Y., & Davis, M. (2022). Reinforcement learning in autonomous systems. IEEE Transactions on Neural Networks, 33(4), 1567-1589. DOI: 10.1109/tnn.2022.3156789",
        "[5] Kumar, P., Sharma, N., & Gupta, R. (2021). Blockchain applications in healthcare data management. Journal of Medical Informatics, 87, 103-118. DOI: 10.1016/j.jmi.2021.87.103",
        "[6] Martinez, E., Nguyen, T., & Roberts, J. (2022). Personalized recommendation systems: Challenges and opportunities. ACM Transactions on Information Systems, 40(1), 1-28. DOI: 10.1145/3478674",
        "[7] Brown, L., White, A., & Green, C. (2020). Cloud computing security: Threats and countermeasures. Computers & Security, 92, 101737. DOI: 10.1016/j.cose.2020.101737",
        "[8] Zhang, W., Liu, H., & Wang, Q. (2021). Graph neural networks for social network analysis. Social Networks, 67, 45-62. DOI: 10.1016/j.socnet.2021.0045INVALID",
        "[9] Anderson, K., Taylor, S., & Moore, R. (2019). Privacy-preserving data mining techniques. Data Mining and Knowledge Discovery, 33(5), 1289-1318. DOI: 10.1007/dmkd.2019.5512",
        "[10] Martinez, E. (2018). User engagement metrics in web applications: A longitudinal study. Behaviour & Information Technology, 37(8), 789-804. DOI: 10.1080/bit.2018.3312BROKEN",
        "[11] Li, X., Zhao, Y., & Chen, J. (2022). Federated learning for privacy protection in IoT networks. IEEE Internet of Things Journal, 9(3), 2156-2170. DOI: 10.1109/jiot.2021.3110234",
        "[12] Hernandez, G., Costa, M., & Silva, P. (2021). Natural language generation for automated reporting. Computational Linguistics, 47(2), 389-425. DOI: 10.1162/coli_a_00421",
    ]

    # =========================================================================
    # submission2.odt
    # Author: Dr. James Chen (with no self-citations — all good)
    # 13 references — 0 self-citations, a few broken DOIs
    # =========================================================================
    submission2_refs = [
        "[1] Chen, J., Wang, L., & Zhang, H. (2022). Transfer learning approaches in biomedical image segmentation. Medical Image Analysis, 78, 102418. DOI: 10.1016/j.media.2022.102418",
        "[2] Thompson, R., Baker, D., & Harris, E. (2021). Explainable artificial intelligence: Methods and applications. Artificial Intelligence Review, 54(2), 181-233. DOI: 10.1007/s10462-020-09825-4",
        "[3] Patel, S., Mehta, A., & Shah, V. (2020). Smart grid optimization using multi-agent systems. Energy Conversion and Management, 215, 112856. DOI: 10.1016/j.enconman.2020.112856INVALID",
        "[4] Kim, S., Park, J., & Lee, H. (2022). Attention mechanisms in transformer architectures for document classification. Pattern Recognition Letters, 153, 82-89. DOI: 10.1016/j.patrec.2021.11.024",
        "[5] Roberts, M., Wilson, E., & Clarke, F. (2021). Quantum computing algorithms for optimization problems. Journal of Quantum Computing, 3(1), 1-25. DOI: 10.26421/jqc3.1-1",
        "[6] Nakamura, T., Tanaka, R., & Sato, K. (2020). Autonomous vehicle perception systems: LiDAR and camera fusion. IEEE Transactions on Intelligent Transportation Systems, 21(5), 2200-2215. DOI: 10.1109/tits.2019.2948340",
        "[7] Garcia, A., Lopez, B., & Torres, C. (2022). Social media misinformation detection using graph convolutional networks. Information Processing & Management, 59(3), 102917. DOI: 10.1016/j.ipm.2022.102917",
        "[8] Williams, N., Adams, P., & Evans, R. (2021). Edge computing for real-time data analytics in industrial IoT. Journal of Industrial Information Integration, 24, 100258. DOI: 10.1016/j.jii.2021.100258",
        "[9] Okonkwo, C., Adeyemi, B., & Nwosu, L. (2022). Machine learning for malware detection in mobile applications. Computers & Security, 115, 102622. DOI: 10.1016/j.cose.2022.102622BROKEN",
        "[10] Perez, J., Rodriguez, A., & Morales, E. (2020). Sentiment analysis for customer feedback in e-commerce. Expert Systems with Applications, 161, 113721. DOI: 10.1016/j.eswa.2020.113721",
        "[11] Sullivan, K., Murphy, D., & O'Brien, T. (2021). Compiler optimization techniques for energy-efficient computing. ACM Transactions on Architecture and Code Optimization, 18(4), 1-26. DOI: 10.1145/3472292",
        "[12] Zhao, X., Liu, Y., & Sun, W. (2022). Contrastive learning for unsupervised visual representation learning. Computer Vision and Image Understanding, 222, 103488. DOI: 10.1016/j.cviu.2022.103488",
        "[13] Fernandez, R., Castillo, L., & Vargas, M. (2021). Zero-shot learning for cross-lingual information retrieval. Information Retrieval Journal, 24(3), 189-224. DOI: 10.1007/s10791-021-09390-w",
    ]

    # =========================================================================
    # submission3.odt
    # Author: Dr. Sarah Kim (heavy self-citations — 4 out of 11 = 36.4%)
    # 11 references — 4 self-citations (36% > 20% threshold → flag)
    # No broken DOIs
    # =========================================================================
    submission3_refs = [
        "[1] Kim, S. (2020). Deep neural architectures for medical diagnosis support systems. Nature Machine Intelligence, 2(7), 392-405. DOI: 10.1038/s42256-020-0187-7",
        "[2] Yamamoto, H., Tanaka, K., & Ito, M. (2022). Sparse representation learning for high-dimensional data compression. IEEE Transactions on Signal Processing, 70, 1234-1248. DOI: 10.1109/tsp.2022.3152847",
        "[3] Kim, S., & Park, J. (2019). Active learning strategies for medical image annotation. Journal of Biomedical Informatics, 97, 103251. DOI: 10.1016/j.jbi.2019.103251",
        "[4] Lindstrom, A., Nielsen, B., & Hansen, C. (2021). Causal inference methods in observational health studies. Statistics in Medicine, 40(14), 3289-3307. DOI: 10.1002/sim.9003",
        "[5] Kim, S., Lee, H., & Choi, Y. (2021). Multi-task learning for clinical note classification. Artificial Intelligence in Medicine, 114, 102044. DOI: 10.1016/j.artmed.2021.102044",
        "[6] Bauer, F., Wagner, T., & Schulz, M. (2020). Interpretable machine learning for financial risk assessment. Journal of Risk and Financial Management, 13(12), 300. DOI: 10.3390/jrfm13120300",
        "[7] Hassan, A., Ali, M., & Ibrahim, R. (2022). Cybersecurity threat intelligence sharing using distributed ledger technology. Future Generation Computer Systems, 129, 133-148. DOI: 10.1016/j.future.2021.11.028",
        "[8] Kim, S., & Yoon, J. (2022). Self-supervised pre-training for radiology report generation. Medical Image Analysis, 82, 102592. DOI: 10.1016/j.media.2022.102592",
        "[9] Martins, R., Carvalho, A., & Santos, B. (2021). Neural architecture search for resource-constrained edge devices. Neural Networks, 144, 193-207. DOI: 10.1016/j.neunet.2021.08.025",
        "[10] Olsson, P., Eriksson, J., & Lindgren, M. (2020). Human factors in cyber-physical system design. Applied Ergonomics, 86, 103096. DOI: 10.1016/j.apergo.2020.103096",
        "[11] Kim, S., Oh, H., & Kwon, B. (2018). Weakly supervised lesion detection in chest X-rays using graph attention networks. Computers in Biology and Medicine, 99, 179-190. DOI: 10.1016/j.compbiomed.2018.06.017",
    ]

    # Create the three submission files
    create_odt_submission(
        f'{SUBMISSIONS_DIR}/submission1.odt',
        "Adaptive Personalization in Digital Learning Systems",
        "Dr. Elena Martinez",
        "Dr. Richard Thompson",
        submission1_refs
    )

    create_odt_submission(
        f'{SUBMISSIONS_DIR}/submission2.odt',
        "Recent Advances in Transfer Learning for Biomedical Applications",
        "Dr. James Chen",
        "Dr. Wei Wang",
        submission2_refs
    )

    create_odt_submission(
        f'{SUBMISSIONS_DIR}/submission3.odt',
        "Self-Supervised Learning in Medical Imaging: A Comprehensive Review",
        "Dr. Sarah Kim",
        "Dr. Hana Lee",
        submission3_refs
    )

    # Create the empty editorial_db.ods
    create_editorial_db_ods(EDITORIAL_DB)

    # Ensure Desktop dir exists (should already exist on typical VM)
    desktop_path = f'{WORKDIR}/Desktop'

    print(f'All initial files created under {desktop_path}')

    # GUI-ready startup: open the submissions folder in file manager and the editorial DB
    launch_gui(f'nautilus "{SUBMISSIONS_DIR}"', delay_sec=1.5)
    launch_gui(f'libreoffice --calc "{EDITORIAL_DB}"', delay_sec=2.0)
    print('GUI_READY: launched file manager and LibreOffice Calc with DISPLAY=:0')


create_initial()
