"""
Initial Setup: Thesis formatting task — create thesis_formatting_rules.odt and thesis_chapter2.odt
Task ID: osworld_multi_apps_reminder_doc_update_writer_006
Domain: libreoffice_writer

Creates:
  /home/user/Documents/thesis_formatting_rules.odt  — 6-rule formatting reference
  /home/user/Documents/thesis_chapter2.odt           — chapter file to be edited by agent
"""

import os
import shlex
import subprocess
import time

# odfpy imports
from odf.opendocument import OpenDocumentText
from odf.style import (
    Style, TextProperties, ParagraphProperties,
)
from odf.text import P, H
from odf.namespaces import FONS

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_reminder_doc_update_writer_006'
RULES_FILE = f'{WORKDIR}/thesis_formatting_rules.odt'
CHAPTER_FILE = f'{WORKDIR}/thesis_chapter2.odt'

# 1.5 line spacing in ODF = fo:line-height: 150% is NOT a length, use a pt value.
# 1.5 * 12pt = 18pt. Use "18pt" for 1.5 line spacing with 12pt font.
LINE_HEIGHT_1_5 = "150%"  # actually set via percentage — use setAttrNS with FONS


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


def make_body_style(doc, name, fontname, fontsize="12pt", line_height="150%",
                    textindent="0cm", marginleft="0cm",
                    marginbottom="0.2cm", margintop="0cm",
                    fontweight=None, fontstyle=None, bold_size=None):
    """Helper: create a paragraph style with given properties."""
    style = Style(name=name, family="paragraph")
    tp_kwargs = dict(fontname=fontname, fontsize=bold_size or fontsize)
    if fontweight:
        tp_kwargs["fontweight"] = fontweight
    if fontstyle:
        tp_kwargs["fontstyle"] = fontstyle
    style.addElement(TextProperties(**tp_kwargs))
    pp = ParagraphProperties(
        marginbottom=marginbottom,
        margintop=margintop,
        textindent=textindent,
        marginleft=marginleft,
    )
    # Set line-height via fo namespace (accepts % or pt)
    pp.setAttrNS(FONS, "line-height", line_height)
    style.addElement(pp)
    doc.automaticstyles.addElement(style)
    return style


def create_formatting_rules():
    """Create thesis_formatting_rules.odt listing the 6 formatting requirements."""
    doc = OpenDocumentText()

    # Heading style for the document title
    h_style = Style(name="RulesHeading", family="paragraph")
    h_style.addElement(TextProperties(fontname="Times New Roman", fontsize="14pt", fontweight="bold"))
    h_style.addElement(ParagraphProperties(marginbottom="0.3cm"))
    doc.automaticstyles.addElement(h_style)

    # Body text style
    b_style = Style(name="RulesBody", family="paragraph")
    b_style.addElement(TextProperties(fontname="Times New Roman", fontsize="12pt"))
    pp = ParagraphProperties(marginbottom="0.2cm")
    pp.setAttrNS(FONS, "line-height", "150%")
    b_style.addElement(pp)
    doc.automaticstyles.addElement(b_style)

    # Title
    title = P(stylename="RulesHeading")
    title.addText("Thesis Formatting Requirements")
    doc.text.addElement(title)

    doc.text.addElement(P(stylename="RulesBody"))

    intro = P(stylename="RulesBody")
    intro.addText("All thesis chapters must comply with the following six formatting requirements:")
    doc.text.addElement(intro)

    doc.text.addElement(P(stylename="RulesBody"))

    rules = [
        "1. Font: All body text must use 12pt Garamond.",
        "2. Line Spacing: Use exactly 24pt line spacing throughout the document.",
        "3. Page Numbers: Insert page numbers starting from page 2 (first page has no number).",
        "4. Chapter Title Style: Apply the 'Heading 1' paragraph style to the chapter title heading.",
        "5. Paragraph Indentation: Set a first-line indent of 1.27 cm for all body paragraphs.",
        "6. Bibliography Format: All bibliography entries must use a hanging indent of 1.27 cm.",
    ]

    for rule in rules:
        rp = P(stylename="RulesBody")
        rp.addText(rule)
        doc.text.addElement(rp)

    doc.text.addElement(P(stylename="RulesBody"))
    note = P(stylename="RulesBody")
    note.addText("These requirements must be applied to thesis_chapter2.odt before submission.")
    doc.text.addElement(note)

    os.makedirs(WORKDIR, exist_ok=True)
    doc.save(RULES_FILE)
    print(f'Formatting rules file created: {RULES_FILE}')


def create_chapter2():
    """
    Create thesis_chapter2.odt with:
      - Times New Roman 12pt (NOT Garamond)
      - 1.5 line spacing (150% fo:line-height, NOT 24pt)
      - No page numbers
      - Chapter title as plain P paragraph (NOT Heading 1 / H element)
      - No first-line indent (textindent=0cm)
      - Flat bibliography (no hanging indent: marginleft=0cm, textindent=0cm)
    """
    doc = OpenDocumentText()

    # Chapter title style — plain paragraph, bold, NOT Heading 1
    ct_style = Style(name="ChapterTitle", family="paragraph")
    ct_style.addElement(TextProperties(fontname="Times New Roman", fontsize="14pt", fontweight="bold"))
    ct_pp = ParagraphProperties(marginbottom="0.4cm", margintop="0.2cm", textindent="0cm")
    ct_style.addElement(ct_pp)
    doc.automaticstyles.addElement(ct_style)

    # Body paragraph style — TNR 12pt, 150% line spacing, no indent
    bp_style = Style(name="BodyPara", family="paragraph")
    bp_style.addElement(TextProperties(fontname="Times New Roman", fontsize="12pt"))
    bp_pp = ParagraphProperties(marginbottom="0.2cm", textindent="0cm")
    bp_pp.setAttrNS(FONS, "line-height", "150%")
    bp_style.addElement(bp_pp)
    doc.automaticstyles.addElement(bp_style)

    # Subsection heading style — TNR 12pt bold italic, 150% line spacing
    sh_style = Style(name="SubHeading", family="paragraph")
    sh_style.addElement(TextProperties(fontname="Times New Roman", fontsize="12pt",
                                        fontweight="bold", fontstyle="italic"))
    sh_pp = ParagraphProperties(margintop="0.3cm", marginbottom="0.2cm", textindent="0cm")
    sh_pp.setAttrNS(FONS, "line-height", "150%")
    sh_style.addElement(sh_pp)
    doc.automaticstyles.addElement(sh_style)

    # Bibliography entry style — flat, no hanging indent
    bib_style = Style(name="BibEntry", family="paragraph")
    bib_style.addElement(TextProperties(fontname="Times New Roman", fontsize="12pt"))
    bib_pp = ParagraphProperties(marginbottom="0.2cm", textindent="0cm", marginleft="0cm")
    bib_pp.setAttrNS(FONS, "line-height", "150%")
    bib_style.addElement(bib_pp)
    doc.automaticstyles.addElement(bib_style)

    # Blank line style
    bl_style = Style(name="BlankLine", family="paragraph")
    bl_style.addElement(TextProperties(fontname="Times New Roman", fontsize="12pt"))
    doc.automaticstyles.addElement(bl_style)

    # ---- Document content ----

    # Chapter title — plain P (not H/Heading 1)
    chapter_title = P(stylename="ChapterTitle")
    chapter_title.addText("Chapter 2: Literature Review")
    doc.text.addElement(chapter_title)

    doc.text.addElement(P(stylename="BlankLine"))

    p1 = P(stylename="BodyPara")
    p1.addText(
        "The study of cognitive load theory has attracted considerable scholarly attention "
        "since Sweller (1988) first introduced the concept in the context of problem-solving "
        "research. This chapter surveys the principal theoretical frameworks that have informed "
        "contemporary instructional design, with particular reference to multimedia learning "
        "environments and their impact on student performance in higher education settings."
    )
    doc.text.addElement(p1)

    p2 = P(stylename="BodyPara")
    p2.addText(
        "Early theoretical contributions positioned working memory capacity as the primary "
        "bottleneck in learning complex material. Baddeley and Hitch (1974) proposed the "
        "multi-component model of working memory, distinguishing between the phonological loop, "
        "the visuospatial sketchpad, and the central executive. These distinctions became "
        "foundational for subsequent researchers investigating how instructional materials "
        "should be structured to minimise extraneous cognitive load."
    )
    doc.text.addElement(p2)

    doc.text.addElement(P(stylename="BlankLine"))

    sub1 = P(stylename="SubHeading")
    sub1.addText("2.1 Cognitive Load and Instructional Design")
    doc.text.addElement(sub1)

    p3 = P(stylename="BodyPara")
    p3.addText(
        "Paas and van Merrienboer (1994) operationalised cognitive load as a construct "
        "measurable through subjective rating scales and secondary task performance. Their "
        "empirical work demonstrated that problem variability training significantly reduced "
        "cognitive load during later transfer tasks. This finding has since been replicated "
        "across domains ranging from mathematics education to medical diagnosis training."
    )
    doc.text.addElement(p3)

    p4 = P(stylename="BodyPara")
    p4.addText(
        "Mayer's (2001) cognitive theory of multimedia learning extended these insights by "
        "specifying how textual and pictorial information should be integrated to support "
        "learning. The coherence principle, contiguity principle, and segmenting principle "
        "each reflect empirically derived recommendations for reducing extraneous load while "
        "maximising germane processing. Critically, Mayer's framework presupposes that "
        "learners actively select, organise, and integrate incoming information streams."
    )
    doc.text.addElement(p4)

    p5 = P(stylename="BodyPara")
    p5.addText(
        "More recent contributions by Sweller, Ayres, and Kalyuga (2011) have refined "
        "the triarchic model, distinguishing intrinsic, extraneous, and germane load as "
        "theoretically distinct but interacting components. Kalyuga (2009) further introduced "
        "the expertise reversal effect, noting that instructional techniques beneficial for "
        "novices may impose unnecessary cognitive burden on expert learners. This finding "
        "underscores the importance of adaptive instructional systems that adjust difficulty "
        "and support in response to learner knowledge state."
    )
    doc.text.addElement(p5)

    doc.text.addElement(P(stylename="BlankLine"))

    sub2 = P(stylename="SubHeading")
    sub2.addText("2.2 Technology-Enhanced Learning Environments")
    doc.text.addElement(sub2)

    p6 = P(stylename="BodyPara")
    p6.addText(
        "The proliferation of digital learning platforms has created new opportunities and "
        "challenges for applying cognitive load theory at scale. Learning management systems "
        "such as Moodle and Canvas allow instructors to embed multimedia resources, discussion "
        "forums, and adaptive quizzing within a single interface. However, the cognitive "
        "demands of navigating these platforms can themselves constitute a source of "
        "extraneous load for inexperienced users (Cierniak, Scheiter, & Gerjets, 2009)."
    )
    doc.text.addElement(p6)

    p7 = P(stylename="BodyPara")
    p7.addText(
        "Intelligent tutoring systems represent a more theoretically motivated approach to "
        "technology-enhanced learning. Systems such as Carnegie Learning's MATHia platform "
        "employ Bayesian knowledge tracing to infer student proficiency and adjust problem "
        "difficulty accordingly. Empirical evaluations of these systems have reported "
        "moderate to large effect sizes relative to traditional classroom instruction, "
        "particularly for students from disadvantaged socioeconomic backgrounds who may "
        "have fewer opportunities for personalised support outside school."
    )
    doc.text.addElement(p7)

    p8 = P(stylename="BodyPara")
    p8.addText(
        "Recent research has also explored the potential of eye-tracking and physiological "
        "measures to provide real-time indices of cognitive load during digital learning. "
        "Pupil dilation, fixation duration, and galvanic skin response have each been "
        "proposed as objective proxies for mental effort (Paas, Tuovinen, Tabbers, & "
        "Van Gerven, 2003). While promising, these measures remain technically demanding "
        "and have not yet been integrated into mainstream educational technology products."
    )
    doc.text.addElement(p8)

    doc.text.addElement(P(stylename="BlankLine"))

    sub3 = P(stylename="SubHeading")
    sub3.addText("2.3 Summary")
    doc.text.addElement(sub3)

    p9 = P(stylename="BodyPara")
    p9.addText(
        "The literature reviewed in this chapter reveals a well-developed theoretical "
        "consensus around cognitive load as a key determinant of learning effectiveness. "
        "Empirical research consistently supports the value of reducing extraneous load, "
        "managing intrinsic load through sequencing and scaffolding, and fostering germane "
        "load through elaborative practice. Emerging technologies offer new tools for "
        "implementing these principles at scale, though further research is needed to "
        "establish their ecological validity in diverse educational contexts."
    )
    doc.text.addElement(p9)

    doc.text.addElement(P(stylename="BlankLine"))

    # Bibliography — flat entries (no hanging indent)
    bib_title = P(stylename="SubHeading")
    bib_title.addText("References")
    doc.text.addElement(bib_title)

    bib_entries = [
        "Baddeley, A. D., & Hitch, G. J. (1974). Working memory. In G. Bower (Ed.), The psychology of learning and motivation (Vol. 8, pp. 47-90). Academic Press.",
        "Cierniak, G., Scheiter, K., & Gerjets, P. (2009). Explaining the split-attention effect: Is the reduction of extraneous cognitive load accompanied by an increase in germane cognitive load? Computers in Human Behavior, 25(2), 315-324.",
        "Kalyuga, S. (2009). Managing cognitive load in adaptive multimedia learning. Information Science Reference.",
        "Mayer, R. E. (2001). Multimedia learning. Cambridge University Press.",
        "Paas, F., & van Merrienboer, J. J. G. (1994). Variability of worked examples and transfer of geometrical problem-solving skills. Journal of Educational Psychology, 86(1), 122-133.",
        "Paas, F., Tuovinen, J. E., Tabbers, H., & Van Gerven, P. W. M. (2003). Cognitive load measurement as a means to advance cognitive load theory. Educational Psychologist, 38(1), 63-71.",
        "Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. Cognitive Science, 12(2), 257-285.",
        "Sweller, J., Ayres, P., & Kalyuga, S. (2011). Cognitive load theory. Springer.",
    ]

    for entry in bib_entries:
        bib_para = P(stylename="BibEntry")
        bib_para.addText(entry)
        doc.text.addElement(bib_para)

    os.makedirs(WORKDIR, exist_ok=True)
    doc.save(CHAPTER_FILE)
    print(f'Chapter 2 file created: {CHAPTER_FILE}')


def main():
    create_formatting_rules()
    create_chapter2()

    # Open both files in LibreOffice Writer; chapter file opened last (active window)
    launch_gui(f'libreoffice --writer "{RULES_FILE}"', delay_sec=2.0)
    launch_gui(f'libreoffice --writer "{CHAPTER_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


main()
