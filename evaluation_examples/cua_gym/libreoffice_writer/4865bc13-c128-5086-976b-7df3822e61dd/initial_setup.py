"""
Initial Setup: Replace subdocument in master document
Task ID: writer_rm_071
Domain: libreoffice_writer

Creates a LibreOffice Writer master document (Guide_Master.odm) with 5 subdocuments
(Ch1.odt through Ch5.odt plus Ch4_OldVersion.odt), and a Ch4_Revised.odt file
with updated content. Opens the master document in LibreOffice Writer.
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_071'

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


def create_odt_file(filepath, title, paragraphs):
    """Create an ODF text document (.odt) with given title and paragraphs."""
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H
    from odf import style as odf_style

    doc = OpenDocumentText()

    # Add heading style
    h_style = odf_style.Style(name="HeadingStyle", family="paragraph")
    h_props = odf_style.TextProperties(fontsize="18pt", fontweight="bold")
    h_style.addElement(h_props)
    doc.automaticstyles.addElement(h_style)

    # Add title heading
    heading = H(outlinelevel=1, stylename=h_style, text=title)
    doc.text.addElement(heading)

    # Add paragraphs
    for para_text in paragraphs:
        p = P(text=para_text)
        doc.text.addElement(p)

    doc.save(filepath)


def create_master_document(filepath, subdoc_paths):
    """
    Create an ODM (master document) that references the given subdocument paths.
    ODM is essentially an ODF text document with section-source links.
    """
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H, Section, SectionSource
    from odf import style as odf_style

    doc = OpenDocumentText()

    # Title
    title_style = odf_style.Style(name="MasterTitle", family="paragraph")
    title_props = odf_style.TextProperties(fontsize="24pt", fontweight="bold")
    title_style.addElement(title_props)
    doc.automaticstyles.addElement(title_style)

    heading = H(outlinelevel=1, stylename=title_style,
                text="Technical Writing Style Guide - Master Document")
    doc.text.addElement(heading)

    intro = P(text="This master document compiles all chapters of the Technical Writing Style Guide.")
    doc.text.addElement(intro)

    # Add sections referencing subdocuments
    for i, subdoc_path in enumerate(subdoc_paths):
        basename = os.path.basename(subdoc_path)
        section_name = f"Section_{i+1}_{basename.replace('.odt', '')}"

        section = Section(name=section_name)
        # The section-source links to the subdocument
        source = SectionSource()
        source.setAttribute('href', subdoc_path)
        source.setAttribute('filtername', 'writer8')
        section.addElement(source)

        # Add a placeholder paragraph inside the section
        p = P(text=f"[Content from {basename}]")
        section.addElement(p)

        doc.text.addElement(section)

    # Save as .odm by first saving as .odt then renaming
    # Actually, ODM uses the same format but with different mimetype
    tmp_path = filepath + '.tmp.odt'
    doc.save(tmp_path)

    # Convert to ODM: change mimetype inside the zip
    with zipfile.ZipFile(tmp_path, 'r') as zin:
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'mimetype':
                    # ODM mimetype
                    zout.writestr(item, 'application/vnd.oasis.opendocument.text-master')
                else:
                    zout.writestr(item, data)

    os.remove(tmp_path)


def create_initial():
    # --- Create subdocument content ---

    # Chapter 1: Introduction to Technical Writing
    create_odt_file(
        os.path.join(WORKDIR, 'Ch1.odt'),
        'Chapter 1: Introduction to Technical Writing',
        [
            'Technical writing is a specialized form of communication that conveys complex information '
            'in a clear, concise, and accessible manner. It bridges the gap between subject matter '
            'experts and the audiences who need to understand their work.',
            'The primary goal of technical writing is to make information easy to understand and use. '
            'Whether documenting software APIs, writing user manuals, or creating scientific reports, '
            'the principles remain consistent: clarity, accuracy, and audience awareness.',
            'This guide provides a comprehensive framework for producing high-quality technical '
            'documents across various domains and formats. Each chapter addresses a specific aspect '
            'of the writing process, from initial planning to final review.',
            'Key principles covered in this guide include: document structure and organization, '
            'audience analysis and adaptation, visual communication and layout, revision strategies '
            'and peer review processes, and publishing workflow management.',
        ]
    )

    # Chapter 2: Document Structure and Organization
    create_odt_file(
        os.path.join(WORKDIR, 'Ch2.odt'),
        'Chapter 2: Document Structure and Organization',
        [
            'Effective document structure is the foundation of readable technical writing. '
            'A well-organized document guides the reader through complex information with '
            'minimal cognitive effort.',
            'Begin every document with a clear statement of purpose and scope. The introduction '
            'should answer three questions: What is this document about? Who is it for? '
            'What will the reader be able to do after reading it?',
            'Use hierarchical headings (H1 through H4) to create a logical outline. Each heading '
            'level should represent a consistent level of detail. Avoid skipping heading levels, '
            'as this disrupts the document\'s visual hierarchy.',
            'Paragraphs should focus on a single idea or concept. The first sentence of each '
            'paragraph should introduce its topic, and subsequent sentences should support or '
            'elaborate on that topic. Keep paragraphs between 3 and 8 sentences.',
            'Transition sentences between sections help maintain narrative flow. Use phrases like '
            '"Building on the principles described above..." or "The next section addresses..." '
            'to connect related topics.',
        ]
    )

    # Chapter 3: Audience Analysis
    create_odt_file(
        os.path.join(WORKDIR, 'Ch3.odt'),
        'Chapter 3: Audience Analysis and Adaptation',
        [
            'Understanding your audience is perhaps the most critical step in the technical '
            'writing process. The same information may need to be presented very differently '
            'depending on who will read it.',
            'Identify your primary and secondary audiences before writing. Primary audiences '
            'are the intended readers who will act on the information. Secondary audiences may '
            'include reviewers, managers, or archival readers.',
            'Assess your audience\'s technical proficiency using a three-tier model: novice '
            '(needs extensive explanation and context), intermediate (familiar with basic concepts '
            'but needs guidance on specifics), and expert (requires only reference-level detail).',
            'Adjust vocabulary, sentence complexity, and assumed knowledge based on your audience '
            'profile. For mixed audiences, use layered information design: provide an overview '
            'accessible to all readers, with detailed sections for advanced users.',
            'Cultural and linguistic considerations also matter. Avoid idioms, colloquialisms, '
            'and culture-specific references when writing for international audiences. Use simple, '
            'direct sentence structures that translate well across languages.',
        ]
    )

    # Chapter 4: Old Version (Visual Communication) - the one to be replaced
    create_odt_file(
        os.path.join(WORKDIR, 'Ch4_OldVersion.odt'),
        'Chapter 4: Visual Communication (Draft v1.2)',
        [
            'NOTE: This is an older draft version dated 2024-09-15. This chapter is pending revision.',
            'Visual elements play a supporting role in technical documents. Charts, diagrams, '
            'and screenshots can illustrate concepts that are difficult to convey through text alone.',
            'When including images, ensure they are of sufficient resolution for the target medium. '
            'Screen captures should be at least 150 DPI for print output.',
            'Tables should be used for structured data comparison. Keep tables simple with clear '
            'column headers and consistent formatting.',
            'This draft lacks coverage of accessibility requirements for visual content, infographic '
            'design principles, and interactive media guidelines. These topics will be addressed '
            'in the revised version.',
        ]
    )

    # Chapter 4: Revised Version (to be used as replacement)
    create_odt_file(
        os.path.join(WORKDIR, 'Ch4_Revised.odt'),
        'Chapter 4: Visual Communication and Information Design',
        [
            'Visual communication is integral to effective technical documentation. Research shows '
            'that readers retain 65% of information when it is paired with relevant imagery, '
            'compared to only 10% for text-only presentation.',
            'Effective use of diagrams, charts, tables, and illustrations transforms complex data '
            'into accessible visual narratives. Every visual element should serve a clear purpose '
            'and be directly referenced in the surrounding text.',
            'Accessibility is a fundamental requirement for all visual content. Provide descriptive '
            'alt text for images, use colorblind-friendly palettes (avoid red-green distinctions), '
            'and ensure sufficient contrast ratios (minimum 4.5:1 for text, 3:1 for large text).',
            'Infographic design follows the principle of progressive disclosure: lead with the key '
            'takeaway, then provide supporting data in layers of increasing detail. Use consistent '
            'visual language throughout a document series.',
            'Interactive media elements such as embedded videos, animated diagrams, and expandable '
            'sections enhance digital documents. Ensure all interactive content degrades gracefully '
            'to static alternatives for print and PDF output.',
            'Data visualization best practices: choose chart types appropriate to the data '
            '(bar charts for comparison, line charts for trends, scatter plots for correlation). '
            'Label all axes, include units, and provide source citations for external data.',
            'Screenshot guidelines: capture at native resolution, annotate with numbered callouts '
            'rather than arrows, maintain a consistent border and shadow style, and update captures '
            'promptly when the interface changes.',
        ]
    )

    # Chapter 5: Review and Publishing
    create_odt_file(
        os.path.join(WORKDIR, 'Ch5.odt'),
        'Chapter 5: Review, Revision, and Publishing',
        [
            'The review process is essential for producing accurate, polished technical documents. '
            'Plan for at least two rounds of review: technical accuracy review by subject matter '
            'experts, and editorial review for clarity and consistency.',
            'Establish a style guide or adopt an existing one (such as the Microsoft Manual of Style '
            'or the Google Developer Documentation Style Guide) to ensure consistency across all '
            'documents in your organization.',
            'Version control is critical for collaborative writing projects. Use meaningful version '
            'numbers (major.minor format) and maintain a changelog that records the date, author, '
            'and nature of each revision.',
            'Before publishing, conduct a final checklist review: verify all cross-references, '
            'test all hyperlinks, confirm image resolution and placement, validate code samples, '
            'and check for consistent terminology throughout the document.',
            'Publishing workflows should include format conversion testing. Verify that the document '
            'renders correctly in all target formats (HTML, PDF, EPUB) and on all target devices '
            'before releasing to the audience.',
        ]
    )

    # --- Create the master document (ODM) ---
    subdoc_refs = [
        'Ch1.odt',
        'Ch2.odt',
        'Ch3.odt',
        'Ch4_OldVersion.odt',
        'Ch5.odt',
    ]
    master_path = os.path.join(WORKDIR, 'Guide_Master.odm')
    create_master_document(master_path, subdoc_refs)
    print(f'Master document created: {master_path}')

    # Verify all files exist
    for f in subdoc_refs + ['Ch4_Revised.odt', 'Guide_Master.odm']:
        fp = os.path.join(WORKDIR, f)
        assert os.path.exists(fp), f"Missing file: {fp}"
        print(f'  Verified: {fp} ({os.path.getsize(fp)} bytes)')

    # --- GUI-ready startup ---
    launch_gui(f'libreoffice --writer "{master_path}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with Guide_Master.odm on DISPLAY=:0')


create_initial()
