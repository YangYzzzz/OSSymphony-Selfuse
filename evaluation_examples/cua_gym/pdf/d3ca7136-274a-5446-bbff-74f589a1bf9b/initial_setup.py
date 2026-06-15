"""
Initial Setup: Create a 7-page essay PDF with specific phrases containing grammar errors on page 3.
Task ID: pdf_fm_044
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_044'
OUTPUT = f'{WORKDIR}/Documents/essay_draft.pdf'


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
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions
    W, H = 595, 842  # A4
    margin_left = 72
    margin_right = 523
    top_start = 72
    line_height = 22
    fontsize = 12
    title_fontsize = 18

    # ---- Page 1: Title & Introduction ----
    page = doc.new_page(width=W, height=H)
    y = 80
    page.insert_text(pymupdf.Point(margin_left, y), "The Evolution of Scientific Reasoning",
                     fontsize=title_fontsize, fontname="hebo", color=(0, 0, 0))
    y += 40
    page.insert_text(pymupdf.Point(margin_left, y), "A Critical Analysis of Methodological Approaches",
                     fontsize=14, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 50

    intro_lines = [
        "The history of scientific inquiry stretches back thousands of years, from the early",
        "observations of Aristotle to the rigorous experimental methods of modern laboratories.",
        "Throughout this long trajectory, the fundamental principles of reasoning have undergone",
        "significant transformations that reflect broader cultural and intellectual shifts.",
        "",
        "This essay examines the key turning points in the development of scientific methodology,",
        "with particular attention to the epistemological debates that shaped how researchers",
        "approach the generation and validation of knowledge. We will explore how paradigm shifts,",
        "as described by Thomas Kuhn, have repeatedly redefined the boundaries of acceptable",
        "scientific practice and discourse.",
        "",
        "The central thesis of this paper is that scientific reasoning has never been a purely",
        "logical endeavor. Instead, it has always been influenced by social, economic, and",
        "political factors that determine which questions are deemed worthy of investigation",
        "and which methods are considered legitimate. By examining specific historical case",
        "studies, we can better understand the complex interplay between objective inquiry",
        "and subjective human experience.",
        "",
        "In the following chapters, we will trace the evolution of scientific thought from",
        "ancient Greece through the Scientific Revolution, the Enlightenment, and into the",
        "contemporary era of big data and computational science.",
    ]
    for line in intro_lines:
        page.insert_text(pymupdf.Point(margin_left, y), line,
                         fontsize=fontsize, fontname="tiro", color=(0, 0, 0))
        y += line_height

    # ---- Page 2: Historical Background ----
    page = doc.new_page(width=W, height=H)
    y = 80
    page.insert_text(pymupdf.Point(margin_left, y), "Chapter 1: Historical Foundations",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 40

    ch1_lines = [
        "The roots of systematic scientific inquiry can be traced to ancient Mesopotamia,",
        "where early astronomers meticulously recorded celestial movements over centuries.",
        "These observations, while lacking a formal theoretical framework, represented the",
        "first sustained effort to understand natural phenomena through careful documentation.",
        "",
        "In ancient Greece, philosophers like Thales and Anaximander proposed naturalistic",
        "explanations for events that had previously been attributed to divine intervention.",
        "This marked a crucial philosophical shift: the idea that the natural world operated",
        "according to discoverable laws rather than the whims of capricious deities.",
        "",
        "Aristotle's contributions to scientific methodology were perhaps the most enduring",
        "of the ancient world. His emphasis on empirical observation and systematic classification",
        "provided a framework that would dominate Western thought for nearly two millennia.",
        "However, his reliance on deductive reasoning from first principles sometimes led",
        "to conclusions that contradicted observable evidence.",
        "",
        "The Islamic Golden Age preserved and expanded upon Greek scientific knowledge during",
        "a period when much of Europe had lost access to these texts. Scholars like Ibn al-Haytham",
        "made groundbreaking contributions to optics and the experimental method, laying",
        "important groundwork for the later Scientific Revolution in Europe.",
        "",
        "The transmission of this knowledge back to Europe through translations in Spain",
        "and Sicily catalyzed a renewed interest in natural philosophy that would eventually",
        "transform into modern science as we understand it today.",
    ]
    for line in ch1_lines:
        page.insert_text(pymupdf.Point(margin_left, y), line,
                         fontsize=fontsize, fontname="tiro", color=(0, 0, 0))
        y += line_height

    # ---- Page 3 (0-indexed page 2): The Critical Page ----
    # This page must contain the 3 target phrases at specific line positions
    page = doc.new_page(width=W, height=H)
    y = 80
    page.insert_text(pymupdf.Point(margin_left, y), "Chapter 2: Methodological Debates",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 40

    # Lines of page 3 content (line numbering starts at 1 from first paragraph line)
    # Line 5 must contain "irregardless of the outcome"
    # Line 12 must contain "could of been"
    # Line 18 must contain "alot of evidence"
    page3_lines = [
        "The debate over proper scientific methodology has been one of the most contentious",     # line 1
        "issues in the philosophy of science. Researchers have long disagreed about whether",      # line 2
        "inductive or deductive approaches yield more reliable results. Some have argued that",    # line 3
        "empirical observation should always take precedence over theoretical speculation,",       # line 4
        "irregardless of the outcome that emerges from controlled experimentation in the",         # line 5
        "laboratory setting. This position, while popular among practicing scientists, has",       # line 6
        "been challenged by philosophers who point out the theory-laden nature of observation.",   # line 7
        "",                                                                                        # line 8
        "Karl Popper's falsificationism represented a major advancement in understanding the",    # line 9
        "demarcation problem. By proposing that scientific theories must be falsifiable, Popper", # line 10
        "provided a criterion that distinguished genuine science from pseudoscience. The impact", # line 11
        "could of been even more transformative had the scientific community fully embraced",      # line 12
        "his framework from the outset. Instead, many researchers continued to rely on",          # line 13
        "verification-based approaches that Popper had convincingly criticized.",                  # line 14
        "",                                                                                        # line 15
        "Thomas Kuhn's paradigm theory offered a different perspective on scientific change.",     # line 16
        "Rather than viewing science as a cumulative enterprise, Kuhn argued that revolutionary", # line 17
        "shifts occur when alot of evidence accumulates against the prevailing paradigm.",         # line 18
        "These paradigm shifts, according to Kuhn, are not purely rational events but involve",   # line 19
        "sociological and psychological factors that influence how scientists interpret data.",    # line 20
        "",                                                                                        # line 21
        "The Kuhn-Popper debate illuminated fundamental tensions in the philosophy of science",   # line 22
        "that remain unresolved to this day. While Popper emphasized the logical structure of",   # line 23
        "scientific reasoning, Kuhn drew attention to the historical and social context in",      # line 24
        "which scientific knowledge is produced and evaluated by the broader community.",         # line 25
    ]
    for line in page3_lines:
        page.insert_text(pymupdf.Point(margin_left, y), line,
                         fontsize=fontsize, fontname="tiro", color=(0, 0, 0))
        y += line_height

    # ---- Page 4: Experimental Methods ----
    page = doc.new_page(width=W, height=H)
    y = 80
    page.insert_text(pymupdf.Point(margin_left, y), "Chapter 3: The Experimental Revolution",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 40
    ch3_lines = [
        "The development of controlled experimentation marked a watershed moment in the",
        "history of science. Francis Bacon's advocacy for systematic empirical investigation",
        "in the early seventeenth century provided a philosophical foundation for what would",
        "become the dominant mode of scientific inquiry in the modern era.",
        "",
        "Galileo Galilei's experiments with inclined planes and pendulums demonstrated the",
        "power of combining mathematical analysis with careful observation. His work showed",
        "that natural phenomena could be described with precision using the language of",
        "mathematics, an insight that would prove foundational for subsequent developments.",
        "",
        "Robert Boyle's contributions to experimental methodology included the development",
        "of rigorous protocols for reproducibility. His insistence that experiments should be",
        "described in sufficient detail for others to replicate represented a crucial step",
        "toward the establishment of modern scientific norms.",
        "",
        "The statistical revolution of the nineteenth and twentieth centuries introduced",
        "new tools for analyzing experimental results. The work of Ronald Fisher, Jerzy",
        "Neyman, and Egon Pearson established the framework of hypothesis testing that",
        "remains central to experimental science across virtually all disciplines.",
        "",
        "Contemporary debates about reproducibility and replication have highlighted the",
        "ongoing challenges of maintaining rigorous experimental standards in an era of",
        "increasing publication pressure and methodological complexity.",
    ]
    for line in ch3_lines:
        page.insert_text(pymupdf.Point(margin_left, y), line,
                         fontsize=fontsize, fontname="tiro", color=(0, 0, 0))
        y += line_height

    # ---- Page 5: Modern Developments ----
    page = doc.new_page(width=W, height=H)
    y = 80
    page.insert_text(pymupdf.Point(margin_left, y), "Chapter 4: Modern Scientific Practice",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 40
    ch4_lines = [
        "The twentieth century brought unprecedented changes to the practice of science.",
        "The emergence of big science, characterized by large collaborative projects and",
        "enormous funding requirements, transformed the social organization of research.",
        "Projects like the Manhattan Project and later the Human Genome Project demonstrated",
        "that some scientific questions require coordinated effort on a massive scale.",
        "",
        "The digital revolution has further transformed scientific methodology. Computational",
        "modeling now allows researchers to simulate complex systems that would be impossible",
        "to study through direct experimentation. Machine learning algorithms can identify",
        "patterns in vast datasets that human analysts might overlook entirely.",
        "",
        "However, these advances have also introduced new methodological challenges. The",
        "reproducibility crisis, first identified in psychology but now recognized across",
        "many disciplines, has raised serious questions about the reliability of published",
        "scientific findings. Studies have suggested that a significant proportion of published",
        "results cannot be reproduced when independent researchers attempt replication.",
        "",
        "Open science initiatives represent one response to these challenges. By making data,",
        "code, and methodological details freely available, researchers aim to increase",
        "transparency and facilitate independent verification of scientific claims.",
    ]
    for line in ch4_lines:
        page.insert_text(pymupdf.Point(margin_left, y), line,
                         fontsize=fontsize, fontname="tiro", color=(0, 0, 0))
        y += line_height

    # ---- Page 6: Ethics and Society ----
    page = doc.new_page(width=W, height=H)
    y = 80
    page.insert_text(pymupdf.Point(margin_left, y), "Chapter 5: Ethics and Social Responsibility",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 40
    ch5_lines = [
        "The relationship between science and society raises important ethical questions that",
        "extend beyond the laboratory. The development of nuclear weapons, genetic engineering,",
        "and artificial intelligence has forced researchers to confront the potential consequences",
        "of their work in ways that previous generations of scientists rarely considered.",
        "",
        "Research ethics has evolved from a relatively informal set of professional norms to",
        "a formalized system of institutional review boards, informed consent requirements,",
        "and regulatory oversight. The Nuremberg Code and the Declaration of Helsinki",
        "established fundamental principles for the ethical conduct of research involving",
        "human subjects that continue to guide contemporary practice.",
        "",
        "Environmental ethics presents additional challenges for scientific methodology. The",
        "precautionary principle suggests that in the absence of complete scientific certainty,",
        "actions should be taken to prevent potential environmental harm. This principle",
        "sometimes conflicts with traditional scientific skepticism, which demands strong",
        "evidence before accepting claims about causal relationships.",
        "",
        "The democratization of scientific knowledge through public engagement and citizen",
        "science initiatives has created new opportunities for broader participation in the",
        "research enterprise, while also raising questions about expertise and authority.",
    ]
    for line in ch5_lines:
        page.insert_text(pymupdf.Point(margin_left, y), line,
                         fontsize=fontsize, fontname="tiro", color=(0, 0, 0))
        y += line_height

    # ---- Page 7: Conclusion ----
    page = doc.new_page(width=W, height=H)
    y = 80
    page.insert_text(pymupdf.Point(margin_left, y), "Conclusion",
                     fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 40
    conclusion_lines = [
        "The evolution of scientific reasoning reflects humanity's enduring quest to understand",
        "the natural world through systematic inquiry. From the earliest astronomical observations",
        "to the sophisticated computational methods of the twenty-first century, the methods",
        "and standards of science have continuously adapted to new challenges and opportunities.",
        "",
        "This essay has traced the major developments in scientific methodology, highlighting",
        "the philosophical debates that have shaped how researchers approach their work. The",
        "tension between empiricism and rationalism, between individual genius and collective",
        "enterprise, and between pure inquiry and social responsibility continues to define",
        "the landscape of contemporary science.",
        "",
        "Looking forward, the integration of artificial intelligence, open data practices, and",
        "interdisciplinary collaboration promises to reshape scientific methodology in ways",
        "that we can only begin to imagine. The challenge for the scientific community will be",
        "to embrace these innovations while maintaining the core commitment to rigorous,",
        "transparent, and ethical inquiry that has driven progress for centuries.",
        "",
        "Ultimately, the story of scientific reasoning is not merely a history of ideas but a",
        "testament to the human capacity for critical thinking, creative problem-solving, and",
        "collaborative knowledge-building across cultures and generations.",
    ]
    for line in conclusion_lines:
        page.insert_text(pymupdf.Point(margin_left, y), line,
                         fontsize=fontsize, fontname="tiro", color=(0, 0, 0))
        y += line_height

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify the target phrases exist on page 3 (0-indexed page 2)
    doc = pymupdf.open(OUTPUT)
    page = doc[2]
    text = page.get_text("text")
    for phrase in ["irregardless of the outcome", "could of been", "alot of evidence"]:
        if phrase in text:
            print(f'  VERIFIED: "{phrase}" found on page 3')
        else:
            print(f'  WARNING: "{phrase}" NOT found on page 3')
    doc.close()

    # GUI-ready startup
    launch_gui(f'evince --page-index=2 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
