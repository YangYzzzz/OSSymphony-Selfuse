"""
Initial Setup: Fix broken subdocument link in master document
Task ID: writer_rm_075
Domain: libreoffice_writer

Creates:
  - /home/user/writer_rm_075.odm  (master document with 6 subdocument links; Chapter4 is broken)
  - /docs/chapters/Chapter1.odt through Chapter6.odt (actual chapter files)
  - /docs/current/Chapter4.odt (the moved file the user needs to relink to)
  - /docs/old/ directory exists but Chapter4.odt is NOT there (broken link)
"""

import os
import shlex
import subprocess
import time
import zipfile
from io import BytesIO


WORKDIR = '/home/user'
TASK_ID = 'writer_rm_075'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odm'

DOCS_DIR = f'{WORKDIR}/docs'
CHAPTERS_DIR = f'{DOCS_DIR}/chapters'
CURRENT_DIR = f'{DOCS_DIR}/current'
OLD_DIR = f'{DOCS_DIR}/old'


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


def create_odt_file(filepath, title, body_text):
    """Create a minimal ODT file with given content."""
    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="TitleStyle" style:family="paragraph">
      <style:paragraph-properties fo:text-align="start"/>
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="BodyStyle" style:family="paragraph">
      <style:paragraph-properties fo:text-align="start"/>
      <style:text-properties fo:font-size="12pt"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:p text:style-name="TitleStyle">{title}</text:p>
      <text:p text:style-name="BodyStyle">{body_text}</text:p>
    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  office:version="1.2">
</office:document-styles>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  office:version="1.2">
  <office:meta>
    <meta:generator>CUA-Gym Setup</meta:generator>
  </office:meta>
</office:document-meta>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''

    mimetype = 'application/vnd.oasis.opendocument.text'

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and uncompressed
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)


def create_odm_file(filepath, subdoc_links):
    """
    Create a LibreOffice Master Document (.odm) with subdocument section links.

    subdoc_links: list of (section_name, href_path) tuples
    """
    # Build text:section elements for each subdocument
    sections = ''
    for sec_name, href in subdoc_links:
        sections += f'''      <text:section text:style-name="SectStyle" text:name="{sec_name}" text:protected="false">
        <text:section-source xlink:href="{href}" text:filter-name="writer8" xmlns:xlink="http://www.w3.org/1999/xlink"/>
        <text:p text:style-name="Standard"/>
      </text:section>
'''

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="TitleStyle" style:family="paragraph">
      <style:paragraph-properties fo:text-align="center"/>
      <style:text-properties fo:font-size="24pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Standard" style:family="paragraph"/>
    <style:style style:name="SectStyle" style:family="section"/>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:p text:style-name="TitleStyle">Quantum Computing Research Project - Master Document</text:p>
      <text:p text:style-name="Standard"/>
{sections}    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  office:version="1.2">
  <office:styles>
    <style:style style:name="Standard" style:family="paragraph">
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:style>
  </office:styles>
</office:document-styles>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  office:version="1.2">
  <office:meta>
    <meta:generator>CUA-Gym Setup</meta:generator>
    <dc:title>Quantum Computing Research Project</dc:title>
  </office:meta>
</office:document-meta>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.text-master"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''

    mimetype = 'application/vnd.oasis.opendocument.text-master'

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)


def create_initial():
    # Create directory structure
    for d in [CHAPTERS_DIR, CURRENT_DIR, OLD_DIR]:
        os.makedirs(d, exist_ok=True)

    # Chapter content - realistic research document content
    chapters = {
        'Chapter1': (
            'Chapter 1: Introduction to Quantum Computing',
            'Quantum computing represents a fundamental paradigm shift in computational science. '
            'Unlike classical computers that process information in binary bits, quantum computers '
            'leverage quantum mechanical phenomena such as superposition and entanglement to perform '
            'calculations on quantum bits (qubits). This chapter provides an overview of the historical '
            'development of quantum computing, from Richard Feynman\'s 1982 proposal to the current '
            'state of the field. We examine the theoretical foundations that make quantum computation '
            'possible and discuss the potential impact on cryptography, drug discovery, materials '
            'science, and optimization problems.'
        ),
        'Chapter2': (
            'Chapter 2: Quantum Gates and Circuits',
            'Quantum gates are the building blocks of quantum circuits, analogous to classical logic '
            'gates. This chapter covers single-qubit gates (Hadamard, Pauli-X, Pauli-Y, Pauli-Z, '
            'Phase, and T gates), multi-qubit gates (CNOT, Toffoli, SWAP), and universal gate sets. '
            'We demonstrate how these gates manipulate qubit states through unitary transformations '
            'and present several important quantum circuit designs including the quantum Fourier '
            'transform, Grover\'s diffusion operator, and error correction circuits. Each gate is '
            'described mathematically with its corresponding matrix representation.'
        ),
        'Chapter3': (
            'Chapter 3: Quantum Algorithms',
            'This chapter explores the major quantum algorithms that demonstrate computational '
            'advantage over classical methods. We begin with Deutsch-Jozsa algorithm as an '
            'introductory example, then proceed to Shor\'s algorithm for integer factorization '
            'and its implications for RSA cryptography. Grover\'s search algorithm is presented '
            'with its quadratic speedup for unstructured search. We also cover the Quantum '
            'Approximate Optimization Algorithm (QAOA), Variational Quantum Eigensolver (VQE), '
            'and quantum machine learning algorithms including quantum support vector machines.'
        ),
        'Chapter4': (
            'Chapter 4: Quantum Error Correction',
            'Quantum error correction is essential for building reliable quantum computers. '
            'This chapter covers the three main types of quantum errors: bit-flip, phase-flip, '
            'and combined errors. We present the Shor 9-qubit code, Steane 7-qubit code, and '
            'the surface code architecture. The stabilizer formalism is introduced as a framework '
            'for understanding and designing quantum error correcting codes. We discuss fault-tolerant '
            'quantum computation, the threshold theorem, and practical considerations for implementing '
            'error correction in current noisy intermediate-scale quantum (NISQ) devices. Recent '
            'experimental demonstrations from IBM, Google, and academic labs are reviewed.'
        ),
        'Chapter5': (
            'Chapter 5: Quantum Hardware Platforms',
            'Multiple physical platforms are being developed for quantum computing, each with '
            'distinct advantages and challenges. This chapter surveys superconducting qubits '
            '(IBM, Google), trapped ions (IonQ, Honeywell), photonic systems (Xanadu, PsiQuantum), '
            'topological qubits (Microsoft), and neutral atom arrays (QuEra, Atom Computing). '
            'For each platform, we discuss qubit coherence times, gate fidelities, connectivity, '
            'scalability prospects, and current qubit counts. A comparative analysis highlights '
            'the trade-offs between different approaches and their suitability for various '
            'application domains.'
        ),
        'Chapter6': (
            'Chapter 6: Applications and Future Outlook',
            'Quantum computing promises transformative applications across multiple industries. '
            'This chapter examines near-term applications in quantum chemistry (molecular simulation), '
            'optimization (logistics, portfolio optimization), machine learning (quantum kernels, '
            'quantum neural networks), and cryptography (quantum key distribution). We discuss the '
            'concept of quantum advantage and review claims of quantum supremacy. The chapter '
            'concludes with a roadmap for quantum computing development, addressing key milestones '
            'such as achieving 1000+ logical qubits, developing practical quantum error correction, '
            'and building commercially viable quantum applications.'
        ),
    }

    # Create chapter ODT files in /docs/chapters/
    for chap_name, (title, body) in chapters.items():
        create_odt_file(f'{CHAPTERS_DIR}/{chap_name}.odt', title, body)

    # Chapter4.odt was moved to /docs/current/ (the correct new location)
    import shutil
    shutil.copy(f'{CHAPTERS_DIR}/Chapter4.odt', f'{CURRENT_DIR}/Chapter4.odt')

    # /docs/old/ exists but Chapter4.odt is NOT there (it was moved away)
    # This makes the old link broken

    # Create the master document with subdocument links
    # Chapter4 points to the OLD (broken) path
    subdoc_links = [
        ('Chapter1_Section', f'{CHAPTERS_DIR}/Chapter1.odt'),
        ('Chapter2_Section', f'{CHAPTERS_DIR}/Chapter2.odt'),
        ('Chapter3_Section', f'{CHAPTERS_DIR}/Chapter3.odt'),
        ('Chapter4_Section', f'{OLD_DIR}/Chapter4.odt'),       # BROKEN LINK - file not here
        ('Chapter5_Section', f'{CHAPTERS_DIR}/Chapter5.odt'),
        ('Chapter6_Section', f'{CHAPTERS_DIR}/Chapter6.odt'),
    ]

    create_odm_file(OUTPUT, subdoc_links)
    print(f'Initial master document created: {OUTPUT}')
    print(f'Chapter files created in {CHAPTERS_DIR}/')
    print(f'Chapter4.odt also at {CURRENT_DIR}/Chapter4.odt (correct new location)')
    print(f'Broken link: {OLD_DIR}/Chapter4.odt (does not exist)')

    # Open master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
