"""
Initial Setup: Export bookmarks from legal_code.pdf using pdftk
Task ID: pdf_mbc_043
Domain: pdf
Creates a multi-page legal PDF with hierarchical bookmarks (TOC).
The agent must use pdftk to export the bookmarks to a text file.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_043'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/legal_code.pdf'

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


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Make sure legal_bookmarks.txt does NOT exist (agent must create it)
    txt_path = f'{DOCS_DIR}/legal_bookmarks.txt'
    if os.path.exists(txt_path):
        os.remove(txt_path)

    doc = pymupdf.open()

    # Define the bookmark/TOC structure
    # Title I: pages 1-29, Title II: pages 30-54, Title III: pages 55-65
    toc = [
        [1, "Title I - General Provisions", 1],
        [2, "Chapter 1 - Definitions", 1],
        [2, "Chapter 2 - Scope of Application", 8],
        [2, "Chapter 3 - Enforcement Authority", 15],
        [2, "Chapter 4 - Penalties and Remedies", 22],
        [1, "Title II - Regulatory Framework", 30],
        [2, "Chapter 5 - Licensing Requirements", 30],
        [2, "Chapter 6 - Compliance Standards", 37],
        [2, "Chapter 7 - Reporting Obligations", 44],
        [1, "Title III - Judicial Proceedings", 55],
        [2, "Chapter 8 - Jurisdiction and Venue", 55],
        [2, "Chapter 9 - Evidentiary Standards", 60],
        [2, "Chapter 10 - Appellate Review", 63],
    ]

    total_pages = 65

    # Legal content sections for realism
    legal_sections = {
        1: (
            "TITLE I - GENERAL PROVISIONS\n\n"
            "Chapter 1 - Definitions\n\n"
            "Section 101. Short Title.\n"
            "This Act may be cited as the 'Consolidated Regulatory Code of 2025'.\n\n"
            "Section 102. Definitions.\n"
            "As used in this Act, unless the context otherwise requires:\n\n"
            "(a) 'Agency' means any department, board, commission, or other entity of the "
            "Federal Government established under this Act or any predecessor statute.\n\n"
            "(b) 'Administrator' means the chief executive officer of the Agency, appointed "
            "by the President with the advice and consent of the Senate.\n\n"
            "(c) 'Covered entity' means any person, partnership, corporation, association, "
            "or other legal entity subject to the jurisdiction of the Agency.\n\n"
            "(d) 'Compliance order' means a written directive issued by the Agency requiring "
            "a covered entity to take specific action to conform with applicable regulations.\n\n"
            "(e) 'Material violation' means any failure to comply with the provisions of this "
            "Act that results in, or has the potential to result in, significant harm to the "
            "public interest, the environment, or the financial integrity of regulated markets."
        ),
        8: (
            "Chapter 2 - Scope of Application\n\n"
            "Section 201. Applicability.\n"
            "The provisions of this Title shall apply to all covered entities operating within "
            "the jurisdiction of the United States, its territories, and possessions.\n\n"
            "Section 202. Exemptions.\n"
            "(a) The following entities shall be exempt from the provisions of this Title:\n"
            "  (1) State and local governmental agencies acting in their sovereign capacity;\n"
            "  (2) Nonprofit organizations with annual revenues below $500,000;\n"
            "  (3) Educational institutions accredited by recognized accrediting bodies.\n\n"
            "Section 203. Preemption.\n"
            "Nothing in this Act shall be construed to preempt any State law that provides "
            "greater protection to consumers or the public interest."
        ),
        15: (
            "Chapter 3 - Enforcement Authority\n\n"
            "Section 301. Powers of the Agency.\n"
            "The Agency shall have the authority to:\n"
            "(a) Conduct investigations and inspections of covered entities;\n"
            "(b) Issue subpoenas for the production of documents and testimony;\n"
            "(c) Impose civil monetary penalties for violations of this Act;\n"
            "(d) Seek injunctive relief in Federal district court;\n"
            "(e) Promulgate rules and regulations necessary to carry out the purposes of this Act."
        ),
        22: (
            "Chapter 4 - Penalties and Remedies\n\n"
            "Section 401. Civil Penalties.\n"
            "(a) Any covered entity that violates any provision of this Act shall be subject to "
            "a civil penalty not to exceed $100,000 per violation per day.\n\n"
            "(b) In determining the amount of any civil penalty, the Agency shall consider:\n"
            "  (1) The severity and duration of the violation;\n"
            "  (2) The economic benefit obtained by the violator;\n"
            "  (3) The violator's history of prior violations;\n"
            "  (4) Any good faith efforts to comply.\n\n"
            "Section 402. Criminal Penalties.\n"
            "Any person who knowingly and willfully violates any provision of this Act shall "
            "be guilty of a felony and, upon conviction, shall be fined not more than $1,000,000 "
            "or imprisoned for not more than 10 years, or both."
        ),
        30: (
            "TITLE II - REGULATORY FRAMEWORK\n\n"
            "Chapter 5 - Licensing Requirements\n\n"
            "Section 501. License Required.\n"
            "No covered entity shall engage in regulated activity without first obtaining a "
            "license from the Agency in accordance with this Chapter.\n\n"
            "Section 502. Application Process.\n"
            "(a) Each application for a license shall be submitted on forms prescribed by the "
            "Agency and shall include:\n"
            "  (1) The full legal name and address of the applicant;\n"
            "  (2) A description of the proposed regulated activity;\n"
            "  (3) Evidence of financial responsibility;\n"
            "  (4) Background check authorization for all principal officers."
        ),
        37: (
            "Chapter 6 - Compliance Standards\n\n"
            "Section 601. General Standards.\n"
            "Each licensed entity shall maintain compliance with the following standards:\n"
            "(a) Recordkeeping: Maintain accurate and complete records of all regulated "
            "transactions for a period of not less than seven years.\n\n"
            "(b) Internal Controls: Establish and maintain a system of internal controls "
            "reasonably designed to ensure compliance with applicable laws and regulations.\n\n"
            "(c) Training: Provide annual compliance training to all employees engaged in "
            "regulated activities."
        ),
        44: (
            "Chapter 7 - Reporting Obligations\n\n"
            "Section 701. Periodic Reports.\n"
            "(a) Each licensed entity shall file with the Agency:\n"
            "  (1) Quarterly financial statements within 45 days of each quarter end;\n"
            "  (2) Annual compliance reports within 90 days of each fiscal year end;\n"
            "  (3) Suspicious activity reports within 15 days of detection.\n\n"
            "Section 702. Material Event Notification.\n"
            "A licensed entity shall notify the Agency within 24 hours of any event that "
            "materially affects its ability to conduct regulated activities."
        ),
        55: (
            "TITLE III - JUDICIAL PROCEEDINGS\n\n"
            "Chapter 8 - Jurisdiction and Venue\n\n"
            "Section 801. Federal Court Jurisdiction.\n"
            "The United States district courts shall have exclusive jurisdiction over all "
            "civil actions arising under this Act.\n\n"
            "Section 802. Venue.\n"
            "(a) Any civil action under this Act may be brought in:\n"
            "  (1) The judicial district where the defendant resides;\n"
            "  (2) The judicial district where the violation occurred;\n"
            "  (3) The District of Columbia."
        ),
        60: (
            "Chapter 9 - Evidentiary Standards\n\n"
            "Section 901. Burden of Proof.\n"
            "In any civil enforcement action brought under this Act, the Agency shall bear "
            "the burden of proving a violation by a preponderance of the evidence.\n\n"
            "Section 902. Admissibility of Agency Records.\n"
            "Records maintained by the Agency in the regular course of business shall be "
            "admissible as evidence in any proceeding under this Act."
        ),
        63: (
            "Chapter 10 - Appellate Review\n\n"
            "Section 1001. Right of Appeal.\n"
            "Any party aggrieved by a final order of the Agency may obtain review in the "
            "United States Court of Appeals for the circuit in which the party resides or "
            "has its principal place of business.\n\n"
            "Section 1002. Standard of Review.\n"
            "The findings of the Agency shall be upheld if supported by substantial evidence "
            "on the record as a whole.\n\n"
            "Section 1003. Stay of Agency Action.\n"
            "The filing of a petition for review shall not operate as a stay of the Agency's "
            "order unless specifically ordered by the court."
        ),
    }

    # Filler paragraph for pages without specific content
    filler = (
        "The provisions of this section shall be interpreted in accordance with the "
        "general principles of statutory construction and the legislative intent expressed "
        "in the preamble to this Act. Where any ambiguity exists, the interpretation that "
        "best advances the protective purposes of this legislation shall be preferred. "
        "Nothing in this section shall be construed to limit or restrict any other rights "
        "or remedies available under Federal or State law."
    )

    for page_num in range(total_pages):
        page = doc.new_page(width=612, height=792)  # Letter size

        # Header
        page.insert_text(
            pymupdf.Point(72, 50),
            "CONSOLIDATED REGULATORY CODE OF 2025",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Page number
        page.insert_text(
            pymupdf.Point(550, 770),
            str(page_num + 1),
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Content
        content_y = 72
        pg = page_num + 1  # 1-indexed

        if pg in legal_sections:
            text = legal_sections[pg]
        else:
            # Generate section-appropriate filler
            if pg <= 29:
                title_ref = "Title I"
            elif pg <= 54:
                title_ref = "Title II"
            else:
                title_ref = "Title III"
            text = (
                f"Section {pg * 10 + 1}. [{title_ref} Continued]\n\n"
                f"{filler}\n\n"
                f"(a) For the purposes of this section, the term 'regulated activity' shall "
                f"have the meaning ascribed to it in Section 102(f) of this Act.\n\n"
                f"(b) The Administrator may, by rule, modify the requirements of this section "
                f"upon a finding that such modification is consistent with the purposes of "
                f"this Act and would not adversely affect the public interest.\n\n"
                f"{filler}"
            )

        rect = pymupdf.Rect(72, content_y, 540, 750)
        page.insert_textbox(
            rect,
            text,
            fontsize=11,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # Set the TOC (bookmarks)
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()

    print(f'Initial file created: {OUTPUT}')

    # Verify bookmarks were set
    verify_doc = pymupdf.open(OUTPUT)
    verify_toc = verify_doc.get_toc()
    print(f'Bookmarks set: {len(verify_toc)} entries')
    for entry in verify_toc:
        print(f'  Level {entry[0]}: "{entry[1]}" -> Page {entry[2]}')
    verify_doc.close()

    # Install pdftk: download and extract JRE + pdftk-java + dependency jars
    # into user-local dirs so pdftk is available without root
    print('Installing pdftk (Java + pdftk-java) into user space...')

    def install_pdftk():
        """Download and extract pdftk + Java into user-local dirs."""
        # Download non-JRE packages (these are small and version-stable)
        subprocess.run(
            "cd /tmp && apt-get download pdftk-java libbcprov-java libcommons-lang3-java 2>/dev/null",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

        # Download JRE: try default version first, fall back to base version
        result = subprocess.run(
            "cd /tmp && apt-get download openjdk-11-jre-headless 2>&1",
            shell=True, capture_output=True, text=True,
        )
        if result.returncode != 0:
            # Fallback: try base Ubuntu 22.04 version
            subprocess.run(
                "cd /tmp && apt-get download openjdk-11-jre-headless=11.0.14.1+1-0ubuntu1 2>&1",
                shell=True, capture_output=True, text=True,
            )

        # Extract all packages
        subprocess.run(
            "cd /tmp && dpkg -x openjdk-11-jre-headless_*.deb /tmp/jre-extract 2>/dev/null",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            "cd /tmp && dpkg -x pdftk-java_*.deb /tmp/pdftk-extract 2>/dev/null",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            "cd /tmp && for f in libbcprov-java*.deb libcommons-lang3-java*.deb; do dpkg -x $f /tmp/jars-extract 2>/dev/null; done",
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

    install_pdftk()

    # Create a pdftk wrapper script on PATH
    pdftk_wrapper = os.path.expanduser('~/.local/bin/pdftk')
    os.makedirs(os.path.dirname(pdftk_wrapper), exist_ok=True)
    with open(pdftk_wrapper, 'w') as f:
        f.write('''#!/bin/sh
export JAVA_HOME=/tmp/jre-extract/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
BCPROV=/tmp/jars-extract/usr/share/java/bcprov.jar
COMMONS=/tmp/jars-extract/usr/share/java/commons-lang3.jar
PDFTK=/tmp/pdftk-extract/usr/share/pdftk/pdftk.jar
java -cp $BCPROV:$COMMONS:$PDFTK com.gitlab.pdftk_java.pdftk "$@"
''')
    os.chmod(pdftk_wrapper, 0o755)

    # Also create symlink at /tmp/pdftk for easier access
    pdftk_tmp = '/tmp/pdftk'
    if os.path.exists(pdftk_tmp):
        os.remove(pdftk_tmp)
    os.symlink(pdftk_wrapper, pdftk_tmp)

    # Add ~/.local/bin to PATH in .bashrc if not already there
    bashrc = os.path.expanduser('~/.bashrc')
    path_line = 'export PATH="$HOME/.local/bin:$PATH"'
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            content = f.read()
        if '.local/bin' not in content:
            with open(bashrc, 'a') as f:
                f.write(f'\n{path_line}\n')
    else:
        with open(bashrc, 'w') as f:
            f.write(f'{path_line}\n')

    # Verify pdftk works
    result = subprocess.run(
        [pdftk_wrapper, OUTPUT, 'dump_data_utf8'],
        capture_output=True, text=True
    )
    if 'BookmarkBegin' in result.stdout:
        print('pdftk installed and working correctly')
    else:
        print(f'WARNING: pdftk may not be working. stdout: {result.stdout[:200]}')
        print(f'stderr: {result.stderr[:200]}')

    # Open the PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
