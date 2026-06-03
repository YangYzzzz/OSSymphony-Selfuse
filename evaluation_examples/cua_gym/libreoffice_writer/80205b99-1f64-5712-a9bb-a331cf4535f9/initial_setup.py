"""
Initial Setup: Multi-app reminder doc update - journal style guide + manuscript draft
Task ID: osworld_multi_apps_reminder_doc_update_writer_007
Domain: libreoffice_writer

Creates two ODF documents in /home/user/Documents/:
  1. journal_style_guide.odt - lists 6 requirements for manuscript submission
  2. manuscript_draft.odt   - a non-compliant draft (Letter size, Calibri 11pt,
                               1.5 spacing, 3cm margins, non-italic captions, no footer)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'

# ── helpers ──────────────────────────────────────────────────────────────────

def launch_gui(command: str, delay_sec: float = 1.5):
    """Launch a GUI app on the VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_style_guide():
    """Create journal_style_guide.odt with 6 numbered requirements."""
    from odf.opendocument import OpenDocumentText
    from odf.style import (Style, TextProperties, ParagraphProperties,
                           PageLayout, PageLayoutProperties, MasterPage)
    from odf.text import P, List, ListItem, H

    doc = OpenDocumentText()

    # --- Page layout (A4, standard margins) ---
    pl = PageLayout(name="Standard")
    plp = PageLayoutProperties(
        pagewidth="21cm", pageheight="29.7cm",
        marginleft="2.54cm", marginright="2.54cm",
        margintop="2.54cm", marginbottom="2.54cm",
        printorientation="portrait"
    )
    pl.addElement(plp)
    doc.automaticstyles.addElement(pl)

    mp = MasterPage(name="Standard", pagelayoutname="Standard")
    doc.masterstyles.addElement(mp)

    # --- Title style ---
    title_style = Style(name="TitleStyle", family="paragraph")
    title_style.addElement(TextProperties(
        fontname="Times New Roman", fontsize="16pt", fontweight="bold"
    ))
    title_style.addElement(ParagraphProperties(
        textalign="center",
        marginbottom="0.4cm"
    ))
    doc.automaticstyles.addElement(title_style)

    # --- Body style ---
    body_style = Style(name="BodyStyle", family="paragraph")
    body_style.addElement(TextProperties(
        fontname="Times New Roman", fontsize="12pt"
    ))
    body_style.addElement(ParagraphProperties(
        textalign="left",
        marginbottom="0.2cm"
    ))
    doc.automaticstyles.addElement(body_style)

    # --- Section heading style ---
    heading_style = Style(name="HeadingStyle", family="paragraph")
    heading_style.addElement(TextProperties(
        fontname="Times New Roman", fontsize="13pt", fontweight="bold"
    ))
    heading_style.addElement(ParagraphProperties(
        margintop="0.4cm", marginbottom="0.2cm"
    ))
    doc.automaticstyles.addElement(heading_style)

    # === Content ===

    # Title
    title = H(outlinelevel=1, stylename="TitleStyle")
    title.addText("Journal of Applied Sciences — Manuscript Submission Style Guide")
    doc.text.addElement(title)

    # Intro paragraph
    intro = P(stylename="BodyStyle")
    intro.addText(
        "Authors submitting manuscripts to the Journal of Applied Sciences must comply "
        "with the following formatting requirements. Non-compliant submissions will be "
        "returned for revision before peer review."
    )
    doc.text.addElement(intro)

    # Section: Formatting Requirements
    sec = H(outlinelevel=2, stylename="HeadingStyle")
    sec.addText("Section 1: Mandatory Formatting Requirements")
    doc.text.addElement(sec)

    requirements = [
        ("Requirement 1 — Page Size",
         "All manuscripts must be formatted on A4 paper (210 mm × 297 mm). "
         "Letter-size or other page dimensions will not be accepted."),
        ("Requirement 2 — Body Font",
         "The entire body text of the manuscript must be set in 12-point Times New Roman. "
         "Use of other typefaces (e.g., Calibri, Arial, Cambria) is not permitted."),
        ("Requirement 3 — Line Spacing",
         "Double line spacing (2.0) is required throughout the main body of the manuscript, "
         "including the abstract, main text, and references."),
        ("Requirement 4 — Page Margins",
         "All four margins (top, bottom, left, right) must be set to exactly 2.54 cm (1 inch). "
         "Wider or narrower margins will result in automatic rejection during initial screening."),
        ("Requirement 5 — Figure Captions",
         "All figure captions must be formatted in 10-point italic text. "
         "Bold or standard-weight captions are not compliant with journal style."),
        ("Requirement 6 — Footer / Word Count",
         "A word count field showing the total number of words in the document must appear "
         "in the document footer. This facilitates rapid editorial screening for length compliance."),
    ]

    for req_title, req_body in requirements:
        req_heading = H(outlinelevel=3, stylename="HeadingStyle")
        req_heading.addText(req_title)
        doc.text.addElement(req_heading)

        req_para = P(stylename="BodyStyle")
        req_para.addText(req_body)
        doc.text.addElement(req_para)

    # Contact section
    contact_heading = H(outlinelevel=2, stylename="HeadingStyle")
    contact_heading.addText("Section 2: Submission Instructions")
    doc.text.addElement(contact_heading)

    sub_para = P(stylename="BodyStyle")
    sub_para.addText(
        "Completed manuscripts should be submitted via the journal's online portal at "
        "submissions.jas-journal.org. Before uploading, authors must verify that all six "
        "formatting requirements in Section 1 have been applied. Submissions are accepted "
        "year-round; however, papers received after the 15th of each month will be held "
        "for the following review cycle."
    )
    doc.text.addElement(sub_para)

    contact_para = P(stylename="BodyStyle")
    contact_para.addText(
        "For technical questions regarding formatting, contact the editorial office at "
        "style@jas-journal.org."
    )
    doc.text.addElement(contact_para)

    style_guide_path = f"{WORKDIR}/journal_style_guide.odt"
    doc.save(style_guide_path)
    print(f"Created: {style_guide_path}")
    return style_guide_path


def create_manuscript_draft():
    """Create manuscript_draft.odt — non-compliant (Letter size, Calibri 11pt,
    1.5 spacing, 3cm margins, non-italic captions, no footer)."""
    from odf.opendocument import OpenDocumentText
    from odf.style import (Style, TextProperties, ParagraphProperties,
                           PageLayout, PageLayoutProperties, MasterPage)
    from odf.text import P, H

    doc = OpenDocumentText()

    # --- Page layout: Letter size (21.59cm x 27.94cm), 3cm margins, NOT A4 ---
    pl = PageLayout(name="PageLayout1")
    plp = PageLayoutProperties(
        pagewidth="21.59cm", pageheight="27.94cm",
        marginleft="3cm", marginright="3cm",
        margintop="3cm", marginbottom="3cm",
        printorientation="portrait"
    )
    pl.addElement(plp)
    doc.automaticstyles.addElement(pl)

    mp = MasterPage(name="Standard", pagelayoutname="PageLayout1")
    doc.masterstyles.addElement(mp)

    # --- Body text style: Calibri 11pt, NOT Times New Roman 12pt ---
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(TextProperties(
        fontname="Calibri", fontsize="11pt"
    ))
    body_style.addElement(ParagraphProperties(
        textalign="left",
        lineheight="150%",
        marginbottom="0.3cm"
    ))
    doc.automaticstyles.addElement(body_style)

    # --- Heading style ---
    heading_style = Style(name="HeadStyle", family="paragraph")
    heading_style.addElement(TextProperties(
        fontname="Calibri", fontsize="13pt", fontweight="bold"
    ))
    heading_style.addElement(ParagraphProperties(
        margintop="0.5cm", marginbottom="0.2cm"
    ))
    doc.automaticstyles.addElement(heading_style)

    # --- Figure caption style: NOT italic, Calibri 11pt ---
    caption_style = Style(name="CaptionStyle", family="paragraph")
    caption_style.addElement(TextProperties(
        fontname="Calibri", fontsize="11pt"
    ))
    caption_style.addElement(ParagraphProperties(
        textalign="center",
        marginbottom="0.3cm"
    ))
    doc.automaticstyles.addElement(caption_style)

    # === Content ===

    title = H(outlinelevel=1, stylename="HeadStyle")
    title.addText(
        "Characterization of Microplastic Distribution in Coastal Sediments: "
        "A Longitudinal Study of Three Estuarine Systems"
    )
    doc.text.addElement(title)

    authors = P(stylename="BodyText")
    authors.addText(
        "Dr. Elara Voss\u00b9, Prof. Nikhil Batra\u00b2, Dr. Camille Fontaine\u00b3"
    )
    doc.text.addElement(authors)

    affiliations = P(stylename="BodyText")
    affiliations.addText(
        "\u00b9 Institute of Marine Ecology, University of Northshore, UK\n"
        "\u00b2 Department of Environmental Chemistry, IIT Delhi, India\n"
        "\u00b3 Laboratoire d\u2019Oc\u00e9anographie, Universit\u00e9 de Bretagne, France"
    )
    doc.text.addElement(affiliations)

    abs_heading = H(outlinelevel=2, stylename="HeadStyle")
    abs_heading.addText("Abstract")
    doc.text.addElement(abs_heading)

    abstract = P(stylename="BodyText")
    abstract.addText(
        "Microplastic pollution has emerged as one of the most pervasive environmental "
        "challenges of the 21st century. This study examines the spatial and temporal "
        "distribution of microplastic particles (\u2264 5 mm) in the surface sediments of "
        "three contrasting estuarine systems: the Tamar Estuary (UK), the Hooghly Estuary "
        "(India), and the Loire Estuary (France). Over a 36-month monitoring period "
        "(January 2022 to December 2024), sediment cores were collected at 12 standardized "
        "sites per estuary, yielding 1,296 individual samples. Particle counts, morphologies, "
        "polymer types (identified via Fourier-transform infrared spectroscopy), and size "
        "distributions were recorded. Polymer abundance ranged from 142 to 8,740 particles "
        "kg\u207b\u00b9 dry weight across all sites."
    )
    doc.text.addElement(abstract)

    intro_heading = H(outlinelevel=2, stylename="HeadStyle")
    intro_heading.addText("1. Introduction")
    doc.text.addElement(intro_heading)

    intro1 = P(stylename="BodyText")
    intro1.addText(
        "The ubiquity of plastic materials in modern industrial and consumer supply chains "
        "has resulted in their progressive fragmentation and deposition across terrestrial, "
        "freshwater, and marine environments. Microplastics — defined as particles smaller "
        "than 5 mm in their longest dimension — originate from the breakdown of larger plastic "
        "items (secondary microplastics) or are manufactured directly at micro-scale for use "
        "in personal care products, industrial abrasives, and medical applications (primary "
        "microplastics). Since Moore et al. (2001) first quantified microplastic accumulation "
        "in the North Pacific Gyre, the field has expanded rapidly."
    )
    doc.text.addElement(intro1)

    intro2 = P(stylename="BodyText")
    intro2.addText(
        "Estuaries represent particularly sensitive environments for microplastic accumulation. "
        "As transition zones between riverine and marine systems, they receive plastic inputs "
        "from both land-based sources (stormwater runoff, wastewater effluents, litter) and "
        "marine transport. Hydrodynamic processes — including tidal forcing, salinity gradients, "
        "and flocculation — modulate particle residence times and deposition patterns in ways "
        "that differ substantially from open ocean environments (Browne et al., 2011). "
        "Despite growing awareness, comparative longitudinal studies spanning multiple estuarine "
        "systems across different industrialization contexts remain scarce."
    )
    doc.text.addElement(intro2)

    methods_heading = H(outlinelevel=2, stylename="HeadStyle")
    methods_heading.addText("2. Materials and Methods")
    doc.text.addElement(methods_heading)

    methods1 = P(stylename="BodyText")
    methods1.addText(
        "2.1 Study Sites. Three estuarine systems were selected to represent contrasting "
        "socio-economic and hydrological contexts. The Tamar Estuary (50.38\u00b0N, 4.17\u00b0W) "
        "drains a predominantly agricultural catchment in southwest England, with moderate "
        "urbanization and historically significant industrial contamination from Cornish tin mining. "
        "Annual freshwater discharge averages 21 m\u00b3 s\u207b\u00b9. The Hooghly Estuary "
        "(22.55\u00b0N, 88.35\u00b0E) forms the western distributary of the Ganges-Brahmaputra "
        "delta and serves as the primary drainage channel for Kolkata metropolitan area "
        "(population ~14.8 million). Annual freshwater discharge ranges from 180 to 640 m\u00b3 "
        "s\u207b\u00b9 depending on monsoon intensity."
    )
    doc.text.addElement(methods1)

    methods2 = P(stylename="BodyText")
    methods2.addText(
        "2.2 Sediment Sampling Protocol. At each site, replicate sediment cores (n = 3) were "
        "extracted using stainless steel push-corers (inner diameter 7.5 cm, depth 15 cm) "
        "during spring low tide conditions. The upper 3 cm of each core was sectioned "
        "immediately in the field using pre-cleaned ceramic blades. All sample containers "
        "were pre-washed with 70% ethanol and sealed with parafilm to prevent atmospheric "
        "contamination by airborne fibres, consistent with GESAMP (2019) guidelines."
    )
    doc.text.addElement(methods2)

    results_heading = H(outlinelevel=2, stylename="HeadStyle")
    results_heading.addText("3. Results")
    doc.text.addElement(results_heading)

    results1 = P(stylename="BodyText")
    results1.addText(
        "3.1 Overall Microplastic Abundance. Total microplastic counts varied substantially "
        "across the three estuaries (Table 1). Mean abundance at Hooghly sites was "
        "5,842 \u00b1 1,230 particles kg\u207b\u00b9 dw, approximately 4.1-fold higher than "
        "Tamar sites (1,423 \u00b1 389 particles kg\u207b\u00b9 dw). Loire Estuary sites "
        "exhibited intermediate concentrations of 2,917 \u00b1 654 particles kg\u207b\u00b9 dw. "
        "A Kruskal-Wallis test confirmed significant inter-estuary differences "
        "(H = 67.4, df = 2, p < 0.001)."
    )
    doc.text.addElement(results1)

    # Figure 1 caption - NOT italic (will need to be made italic in golden)
    fig1_cap = P(stylename="CaptionStyle")
    fig1_cap.addText(
        "Figure 1. Mean microplastic abundance (particles kg\u207b\u00b9 dry weight) "
        "across 12 sampling stations in three estuaries from 2022 to 2024. "
        "Error bars indicate \u00b1 1 standard deviation. Hooghly sites consistently "
        "showed the highest concentrations."
    )
    doc.text.addElement(fig1_cap)

    results2 = P(stylename="BodyText")
    results2.addText(
        "3.2 Polymer Composition. FTIR spectroscopy identified seven dominant polymer types "
        "across all sites: polyethylene (PE, 34%), polypropylene (PP, 22%), polystyrene (PS, 14%), "
        "polyethylene terephthalate (PET, 11%), polyvinyl chloride (PVC, 8%), nylon (PA, 6%), "
        "and polycarbonate (PC, 5%). Polymer composition profiles were broadly similar across "
        "all three estuaries, though Hooghly samples showed a significantly higher proportion "
        "of PET particles, consistent with the concentration of textile industries in the "
        "Kolkata industrial belt."
    )
    doc.text.addElement(results2)

    # Figure 2 caption - NOT italic
    fig2_cap = P(stylename="CaptionStyle")
    fig2_cap.addText(
        "Figure 2. Polymer composition of microplastic particles identified by FTIR "
        "spectroscopy across all three estuarine systems (n = 1,296 samples). "
        "Pie charts display mean proportions for each estuary; total proportions may "
        "not sum to 100% due to rounding."
    )
    doc.text.addElement(fig2_cap)

    discussion_heading = H(outlinelevel=2, stylename="HeadStyle")
    discussion_heading.addText("4. Discussion")
    doc.text.addElement(discussion_heading)

    disc1 = P(stylename="BodyText")
    disc1.addText(
        "The substantially elevated microplastic concentrations observed in the Hooghly Estuary "
        "corroborate earlier point-source studies (Chatterjee & Sharma, 2020; Batra et al., 2022) "
        "and highlight the disproportionate contribution of rapidly urbanizing regions with "
        "limited waste management infrastructure. The dominance of PE and PP fragments is "
        "consistent with global sediment studies and reflects the prevalence of single-use "
        "packaging materials in the waste stream. Temporal trends over the 36-month study "
        "period indicated no significant decline in abundance at any site, suggesting that "
        "current mitigation measures are insufficient to reduce estuarine plastic loading "
        "within observable timescales."
    )
    doc.text.addElement(disc1)

    disc2 = P(stylename="BodyText")
    disc2.addText(
        "The intermediate concentrations observed in the Loire Estuary, despite its position "
        "in a high-income nation with established waste management systems, indicate that "
        "legacy contamination and diffuse agricultural inputs remain significant contributors "
        "even in regulated contexts. The Tamar's lower counts may partly reflect its smaller "
        "catchment population (~500,000) and the absence of major urban agglomerations within "
        "the drainage basin. However, seasonal flood events were associated with transient "
        "concentration spikes at all sites, underscoring the role of episodic hydrological "
        "forcing in resuspension and redistribution of sediment-bound microplastics."
    )
    doc.text.addElement(disc2)

    conclusion_heading = H(outlinelevel=2, stylename="HeadStyle")
    conclusion_heading.addText("5. Conclusion")
    doc.text.addElement(conclusion_heading)

    concl = P(stylename="BodyText")
    concl.addText(
        "This study provides the first directly comparable longitudinal dataset of microplastic "
        "sediment concentrations across three estuaries spanning contrasting industrialization "
        "levels and geographical contexts. Our findings confirm that urbanization intensity and "
        "waste infrastructure quality are the primary drivers of microplastic loading, while "
        "polymer composition remains broadly consistent regardless of source region. Long-term "
        "monitoring programs and basin-level intervention strategies targeting primary packaging "
        "materials are urgently required to arrest the continuing accumulation of microplastics "
        "in estuarine sediments."
    )
    doc.text.addElement(concl)

    refs_heading = H(outlinelevel=2, stylename="HeadStyle")
    refs_heading.addText("References")
    doc.text.addElement(refs_heading)

    refs = [
        "Batra, N., Rao, P., & Singh, A. (2022). Microplastic abundance in Hooghly Estuary "
        "sediments: seasonal and spatial variation. Marine Pollution Bulletin, 175, 113312.",
        "Browne, M.A., Crump, P., Niven, S.J., Teuten, E., Tonkin, A., Galloway, T., & "
        "Thompson, R. (2011). Accumulation of microplastic on shorelines worldwide: sources "
        "and sinks. Environmental Science & Technology, 45(21), 9175\u20139179.",
        "Chatterjee, S., & Sharma, S. (2020). Microplastics in our oceans and marine health. "
        "Field Actions Science Reports, 19, 54\u201361.",
        "GESAMP (2019). Guidelines for the Monitoring and Assessment of Plastic Litter and "
        "Microplastics in the Ocean. IMO/FAO/UNESCO-IOC/UNIDO/WMO/IAEA/UN/UNEP/UNDP Joint "
        "Group of Experts on the Scientific Aspects of Marine Environmental Protection, "
        "Report No. 99.",
        "Moore, C.J., Moore, S.L., Leecaster, M.K., & Weisberg, S.B. (2001). A comparison "
        "of plastic and plankton in the North Pacific Central Gyre. Marine Pollution "
        "Bulletin, 42(12), 1297\u20131300.",
        "Voss, E., Fontaine, C., & Lambert, J. (2023). Tidal dynamics and microplastic "
        "transport in European macrotidal estuaries. Estuarine, Coastal and Shelf Science, "
        "287, 108312.",
    ]
    for ref_text in refs:
        ref_para = P(stylename="BodyText")
        ref_para.addText(ref_text)
        doc.text.addElement(ref_para)

    manuscript_path = f"{WORKDIR}/manuscript_draft.odt"
    doc.save(manuscript_path)
    print(f"Created: {manuscript_path}")
    return manuscript_path


def main():
    os.makedirs(WORKDIR, exist_ok=True)

    style_guide_path = create_style_guide()
    manuscript_path = create_manuscript_draft()

    # GUI: open both files — style guide first (reference), then manuscript (to edit)
    launch_gui(f'libreoffice --writer "{style_guide_path}"', delay_sec=2.5)
    launch_gui(f'libreoffice --writer "{manuscript_path}"', delay_sec=2.5)
    print("GUI_READY: launched LibreOffice Writer for both documents with DISPLAY=:0")


main()
