"""
Initial Setup: Create a master document (.odm) with 4 subdocuments for a whitepaper.
Task ID: writer_rm_079
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_079'

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


# --- Subdocument content definitions ---
# Each subdoc is an ODT file with realistic whitepaper content

SUBDOCS = {
    "Chapter1_Introduction.odt": {
        "title": "Chapter 1: Introduction to Quantum-Resistant Cryptography",
        "paragraphs": [
            "The rapid advancement of quantum computing poses an unprecedented threat to modern cryptographic infrastructure. As organizations worldwide increasingly depend on digital security for sensitive communications, financial transactions, and national defense, the need for quantum-resistant cryptographic solutions has become critically urgent.",
            "This whitepaper examines the current landscape of post-quantum cryptography (PQC), evaluating the most promising algorithmic approaches that have emerged from decades of research. Our analysis draws on extensive testing conducted at the Meridian Research Institute between January 2024 and December 2024, involving over 2,400 benchmark trials across 8 hardware configurations.",
            "The National Institute of Standards and Technology (NIST) finalized its first set of post-quantum cryptographic standards in August 2024, selecting CRYSTALS-Kyber for key encapsulation and CRYSTALS-Dilithium for digital signatures. These selections mark a pivotal moment in the transition toward quantum-safe security infrastructure.",
            "Section 1.1: Scope and Objectives",
            "This document provides a comprehensive technical assessment covering four primary areas: lattice-based cryptosystems, hash-based signature schemes, code-based encryption methods, and multivariate polynomial systems. For each approach, we present theoretical foundations, implementation benchmarks, and practical deployment considerations.",
            "Section 1.2: Methodology Overview",
            "Our evaluation methodology follows the NIST Post-Quantum Cryptography Standardization Process framework. All algorithms were tested on standardized hardware platforms including Intel Xeon Platinum 8380 processors and ARM Cortex-A78 chips. Performance metrics include key generation time, encryption/decryption throughput, signature generation/verification speed, and memory consumption.",
            "Section 1.3: Document Structure",
            "The remainder of this whitepaper is organized as follows: Chapter 2 provides detailed analysis of lattice-based approaches, Chapter 3 covers hash-based and code-based alternatives, and Chapter 4 presents our deployment recommendations and migration roadmap for enterprise environments.",
        ]
    },
    "Chapter2_LatticeBased.odt": {
        "title": "Chapter 2: Lattice-Based Cryptographic Systems",
        "paragraphs": [
            "Lattice-based cryptography has emerged as the most versatile and well-studied family of post-quantum cryptographic primitives. The mathematical hardness of lattice problems, particularly the Learning With Errors (LWE) problem and its ring variant (Ring-LWE), provides a robust foundation for constructing encryption, key exchange, and digital signature schemes.",
            "Section 2.1: CRYSTALS-Kyber Key Encapsulation Mechanism",
            "CRYSTALS-Kyber, standardized as ML-KEM (Module-Lattice Key Encapsulation Mechanism), operates on module lattices and offers three security levels: Kyber-512 (NIST Level 1), Kyber-768 (NIST Level 3), and Kyber-1024 (NIST Level 5). Our benchmarks revealed the following performance characteristics on Intel Xeon Platinum 8380:",
            "Kyber-512: Key generation 42.3 microseconds, encapsulation 51.7 microseconds, decapsulation 56.2 microseconds. Public key size: 800 bytes, ciphertext size: 768 bytes.",
            "Kyber-768: Key generation 68.9 microseconds, encapsulation 79.4 microseconds, decapsulation 85.1 microseconds. Public key size: 1,184 bytes, ciphertext size: 1,088 bytes.",
            "Kyber-1024: Key generation 103.2 microseconds, encapsulation 118.6 microseconds, decapsulation 127.3 microseconds. Public key size: 1,568 bytes, ciphertext size: 1,568 bytes.",
            "Section 2.2: CRYSTALS-Dilithium Digital Signatures",
            "CRYSTALS-Dilithium, standardized as ML-DSA (Module-Lattice Digital Signature Algorithm), provides a complementary signature scheme based on the same lattice foundations. Three parameter sets target different security levels:",
            "Dilithium2 (NIST Level 2): Signature generation 287.4 microseconds, verification 112.8 microseconds. Signature size: 2,420 bytes, public key size: 1,312 bytes.",
            "Dilithium3 (NIST Level 3): Signature generation 478.6 microseconds, verification 189.3 microseconds. Signature size: 3,293 bytes, public key size: 1,952 bytes.",
            "Dilithium5 (NIST Level 5): Signature generation 712.1 microseconds, verification 284.7 microseconds. Signature size: 4,595 bytes, public key size: 2,592 bytes.",
            "Section 2.3: NTRU and NTRU Prime",
            "While not selected as primary NIST standards, NTRU-based schemes remain important alternatives. NTRU offers competitive performance with different security assumptions, providing defense-in-depth options for organizations requiring algorithm diversity. Our testing of ntruhrss701 showed key generation at 89.7 microseconds and decapsulation at 43.2 microseconds, with a ciphertext overhead of 1,138 bytes.",
            "Section 2.4: Implementation Considerations",
            "Constant-time implementation is critical for lattice-based schemes to prevent side-channel attacks. Our analysis identified timing vulnerabilities in three open-source Kyber implementations that could leak secret key material through cache-timing channels. We recommend using only audited, constant-time reference implementations such as those provided by the PQ-CRYSTALS project.",
        ]
    },
    "Chapter3_AlternativeApproaches.odt": {
        "title": "Chapter 3: Hash-Based and Code-Based Approaches",
        "paragraphs": [
            "Beyond lattice-based methods, two additional families of quantum-resistant primitives deserve careful consideration: hash-based signatures and code-based encryption. Each offers unique security properties rooted in well-understood mathematical problems.",
            "Section 3.1: SPHINCS+ Stateless Hash-Based Signatures",
            "SPHINCS+, standardized as SLH-DSA (Stateless Hash-Based Digital Signature Algorithm), relies solely on the security of hash functions. This conservative approach provides confidence against unexpected breakthroughs in lattice mathematics. However, SPHINCS+ signatures are significantly larger than Dilithium signatures.",
            "SPHINCS+-128s (NIST Level 1, small): Signature generation 54.3 milliseconds, verification 2.8 milliseconds. Signature size: 7,856 bytes.",
            "SPHINCS+-192f (NIST Level 3, fast): Signature generation 12.7 milliseconds, verification 1.4 milliseconds. Signature size: 35,664 bytes.",
            "SPHINCS+-256s (NIST Level 5, small): Signature generation 198.4 milliseconds, verification 8.6 milliseconds. Signature size: 29,792 bytes.",
            "The trade-off between signature size and computational cost makes SPHINCS+ most suitable for high-security applications where bandwidth is not the primary constraint, such as firmware signing, certificate issuance, and long-term archival authentication.",
            "Section 3.2: Classic McEliece Code-Based Encryption",
            "Classic McEliece, based on Goppa codes, has withstood over 40 years of cryptanalysis. It offers extremely fast encapsulation and decapsulation but requires very large public keys:",
            "McEliece-348864 (NIST Level 1): Public key size 261,120 bytes, ciphertext 128 bytes. Encapsulation: 18.2 microseconds.",
            "McEliece-6960119 (NIST Level 5): Public key size 1,047,319 bytes, ciphertext 226 bytes. Encapsulation: 67.8 microseconds.",
            "The enormous public key sizes make Classic McEliece impractical for many interactive protocols but well-suited for long-term key establishment scenarios where the public key can be pre-distributed.",
            "Section 3.3: Multivariate Polynomial Schemes",
            "Multivariate cryptography remains an active research area, though no multivariate scheme was selected in the NIST standardization. The GeMSS signature scheme and Rainbow (subsequently broken) illustrate both the potential and risks of this approach. Our recommendation is to monitor ongoing research but not deploy multivariate schemes in production at this time.",
            "Section 3.4: Comparative Analysis Summary",
            "Table 3.1 presents a comprehensive comparison of all evaluated algorithms across seven metrics: key size, ciphertext/signature size, computational speed, implementation maturity, security confidence, side-channel resistance, and standardization status. Lattice-based schemes offer the best overall balance, while hash-based and code-based alternatives provide valuable diversity for hybrid deployment strategies.",
        ]
    },
    "Chapter4_Recommendations.odt": {
        "title": "Chapter 4: Deployment Recommendations and Migration Roadmap",
        "paragraphs": [
            "Transitioning to quantum-resistant cryptography requires careful planning, phased implementation, and ongoing evaluation. This chapter presents our recommended migration roadmap based on organizational risk profiles and infrastructure complexity.",
            "Section 4.1: Immediate Actions (2025 Q1-Q2)",
            "All organizations should begin cryptographic inventory assessment immediately. Document every system using RSA, ECC, or Diffie-Hellman key exchange. Classify systems by data sensitivity and required protection lifetime. Deploy hybrid TLS configurations combining classical and post-quantum key exchange on internet-facing services.",
            "Priority 1: Email encryption systems protecting data with 10+ year confidentiality requirements. Priority 2: VPN and remote access infrastructure. Priority 3: Code signing and software update mechanisms.",
            "Section 4.2: Short-Term Migration (2025 Q3 - 2026 Q2)",
            "Implement ML-KEM (Kyber) hybrid key exchange across all TLS 1.3 deployments. Upgrade certificate authorities to issue dual-algorithm certificates combining ECDSA with ML-DSA (Dilithium). Begin testing SPHINCS+ for firmware signing and long-term document authentication.",
            "Estimated resource requirements: 2-4 FTE cryptographic engineers for a mid-size enterprise, $150,000-$400,000 for testing infrastructure, 6-9 months for pilot deployment across critical systems.",
            "Section 4.3: Medium-Term Transition (2026 Q3 - 2028 Q4)",
            "Complete migration of all internal PKI to post-quantum algorithms. Replace legacy VPN protocols with quantum-resistant alternatives. Implement post-quantum secure messaging for executive communications. Conduct red team exercises specifically targeting quantum attack vectors.",
            "Section 4.4: Long-Term Vision (2029 and Beyond)",
            "Establish continuous monitoring for advances in quantum computing capability. Maintain algorithm agility to enable rapid transitions if selected algorithms are found vulnerable. Participate in industry working groups to shape evolving standards. Invest in quantum key distribution (QKD) research for highest-security applications.",
            "Section 4.5: Risk Assessment Framework",
            "Organizations should evaluate their quantum risk using the following formula: Quantum Risk Score = (Data Sensitivity x Protection Lifetime) / Migration Readiness. A score above 7.0 indicates critical urgency for immediate migration initiation.",
            "Section 4.6: Conclusions",
            "The quantum threat to classical cryptography is not hypothetical but inevitable. The timeline remains uncertain, with expert estimates ranging from 5 to 20 years for cryptographically relevant quantum computers. However, the harvest-now-decrypt-later threat makes immediate action necessary for any data requiring long-term confidentiality. Organizations that begin migration now will be well-positioned regardless of when large-scale quantum computers become available.",
            "References",
            "1. NIST Post-Quantum Cryptography Standardization, FIPS 203-205, August 2024.",
            "2. Alagic, G. et al., Status Report on the Third Round of the NIST PQC Process, NISTIR 8413, 2022.",
            "3. Bernstein, D.J. and Lange, T., Post-Quantum Cryptography, Nature 549, 188-194, 2017.",
            "4. Mosca, M., Cybersecurity in an Era with Quantum Computers, IEEE Security & Privacy 16(5), 2018.",
            "5. Chen, L. et al., Report on Post-Quantum Cryptography, NISTIR 8105, 2016.",
        ]
    }
}


def create_odt_subdocument(filepath, title, paragraphs):
    """Create a proper ODT file using odfpy."""
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H
    from odf import style as odf_style
    from odf.style import Style, TextProperties, ParagraphProperties

    doc = OpenDocumentText()

    # Create heading style
    h_style = Style(name="ChapterHeading", family="paragraph")
    h_style.addElement(TextProperties(attributes={
        'fontsize': '18pt',
        'fontweight': 'bold',
        'color': '#1a3c6e',
    }))
    h_style.addElement(ParagraphProperties(attributes={
        'marginbottom': '0.3in',
    }))
    doc.automaticstyles.addElement(h_style)

    # Create body style
    b_style = Style(name="BodyText", family="paragraph")
    b_style.addElement(TextProperties(attributes={
        'fontsize': '11pt',
        'fontfamily': 'Liberation Serif',
    }))
    b_style.addElement(ParagraphProperties(attributes={
        'marginbottom': '0.15in',
        'textalign': 'justify',
    }))
    doc.automaticstyles.addElement(b_style)

    # Section heading style
    s_style = Style(name="SectionHeading", family="paragraph")
    s_style.addElement(TextProperties(attributes={
        'fontsize': '14pt',
        'fontweight': 'bold',
        'color': '#2d5aa0',
    }))
    s_style.addElement(ParagraphProperties(attributes={
        'margintop': '0.2in',
        'marginbottom': '0.1in',
    }))
    doc.automaticstyles.addElement(s_style)

    # Add title as heading
    heading = H(outlinelevel=1, stylename=h_style, text=title)
    doc.text.addElement(heading)

    # Add paragraphs
    for para_text in paragraphs:
        if para_text.startswith("Section ") or para_text.startswith("References"):
            p = P(stylename=s_style, text=para_text)
        else:
            p = P(stylename=b_style, text=para_text)
        doc.text.addElement(p)

    doc.save(filepath)
    print(f'  Created subdocument: {filepath}')


def create_master_document(master_path, subdoc_filenames):
    """
    Create an ODM (Master Document) file.
    We first create a normal ODT with odfpy containing section links,
    then convert it to ODM by changing the MIME type in the zip.
    """
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H, Section, SectionSource
    from odf.style import Style, TextProperties, ParagraphProperties

    # First create as ODT
    temp_odt = master_path.replace('.odm', '_temp.odt')
    doc = OpenDocumentText()

    # Title style
    t_style = Style(name="MasterTitle", family="paragraph")
    t_style.addElement(TextProperties(attributes={
        'fontsize': '24pt',
        'fontweight': 'bold',
        'color': '#0d2137',
    }))
    t_style.addElement(ParagraphProperties(attributes={
        'textalign': 'center',
        'marginbottom': '0.3in',
    }))
    doc.automaticstyles.addElement(t_style)

    # Subtitle style
    s_style = Style(name="SubTitle", family="paragraph")
    s_style.addElement(TextProperties(attributes={
        'fontsize': '14pt',
        'fontstyle': 'italic',
        'color': '#4a6fa5',
    }))
    s_style.addElement(ParagraphProperties(attributes={
        'textalign': 'center',
        'marginbottom': '0.15in',
    }))
    doc.automaticstyles.addElement(s_style)

    # Normal text style
    n_style = Style(name="NormalText", family="paragraph")
    n_style.addElement(TextProperties(attributes={
        'fontsize': '11pt',
    }))
    doc.automaticstyles.addElement(n_style)

    # Add master doc title page
    title = H(outlinelevel=1, stylename=t_style, text="Quantum-Resistant Cryptography: A Comprehensive Technical Assessment")
    doc.text.addElement(title)

    subtitle = P(stylename=s_style, text="Meridian Research Institute - Whitepaper Series 2025")
    doc.text.addElement(subtitle)

    authors = P(stylename=s_style, text="Dr. Elena Vasquez, Dr. James Thornton, Dr. Aisha Patel")
    doc.text.addElement(authors)

    date_p = P(stylename=s_style, text="Published: March 2025 | Version 2.1")
    doc.text.addElement(date_p)

    abstract = P(stylename=n_style, text="Abstract: This whitepaper provides a comprehensive evaluation of post-quantum cryptographic algorithms following the NIST standardization process. Based on extensive benchmarking of lattice-based, hash-based, and code-based cryptosystems, we present deployment recommendations and a phased migration roadmap for enterprise environments.")
    doc.text.addElement(abstract)

    # Add sections linking to subdocuments
    for i, subdoc_name in enumerate(subdoc_filenames, 1):
        section = Section(name=f"LinkedSection{i}")
        section_source = SectionSource(
            sectionname="",
        )
        section_source.setAttrNS(
            'urn:oasis:names:tc:opendocument:xmlns:xlink:1.0',
            'href',
            subdoc_name
        )
        section_source.setAttrNS(
            'urn:oasis:names:tc:opendocument:xmlns:xlink:1.0',
            'type',
            'simple'
        )
        section.addElement(section_source)
        # Add placeholder text for the section
        placeholder = P(stylename=n_style, text=f"[Content from {subdoc_name}]")
        section.addElement(placeholder)
        doc.text.addElement(section)

    doc.save(temp_odt)
    print(f'Temp ODT created: {temp_odt}')

    # Convert ODT to ODM by changing the mimetype in the zip archive
    import zipfile
    import io

    with zipfile.ZipFile(temp_odt, 'r') as zin:
        with zipfile.ZipFile(master_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'mimetype':
                    # Change mimetype from text to master document
                    zout.writestr(item, 'application/vnd.oasis.opendocument.text-master')
                else:
                    zout.writestr(item, data)

    os.remove(temp_odt)
    print(f'Master document created: {master_path}')


def create_initial():
    subdoc_dir = WORKDIR
    master_path = f'{WORKDIR}/Whitepaper_Master.odm'

    subdoc_filenames = list(SUBDOCS.keys())

    # Create subdocuments
    for filename, content in SUBDOCS.items():
        filepath = os.path.join(subdoc_dir, filename)
        create_odt_subdocument(filepath, content['title'], content['paragraphs'])

    # Create master document
    create_master_document(master_path, subdoc_filenames)

    # Also create the task_id file as .docx placeholder (empty) so the agent knows the target
    # Actually, the task says to convert the master doc - the agent will create the output
    # The initial state is just the master doc + subdocs

    print(f'All files created in {WORKDIR}')
    print(f'Master document: {master_path}')
    print(f'Subdocuments: {", ".join(subdoc_filenames)}')

    # GUI-ready: open the master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{master_path}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with master document on DISPLAY=:0')


create_initial()
