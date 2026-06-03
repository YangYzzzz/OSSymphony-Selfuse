"""
Initial Setup: Multi-app doc follow instructions - style checklist ODT task
Task ID: osworld_multi_apps_doc_follow_instructions_003
Domain: libreoffice_writer (ODT)

Creates:
  - /home/user/Desktop/style_checklist.odt  -- checklist with 3 checked items
  - /home/user/Documents/presentation_draft.odt -- 3-page doc, default margins, no footer
"""

import os
import shlex
import subprocess
import time


WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_follow_instructions_003'
CHECKLIST_PATH = f'{WORKDIR}/Desktop/style_checklist.odt'
DRAFT_PATH = f'{WORKDIR}/Documents/presentation_draft.odt'


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


def create_checklist_odt():
    """Create style_checklist.odt on the Desktop with 3 checked items."""
    from odf.opendocument import OpenDocumentText
    from odf.style import (Style, TextProperties, ParagraphProperties,
                           PageLayout, PageLayoutProperties, MasterPage,
                           Header, Footer)
    from odf.text import P, Span, List, ListItem
    from odf import teletype

    doc = OpenDocumentText()

    # Create a basic text style
    heading_style = Style(name="Heading1Custom", family="paragraph")
    heading_style.addElement(TextProperties(fontsize="14pt", fontweight="bold"))
    doc.automaticstyles.addElement(heading_style)

    normal_style = Style(name="NormalCustom", family="paragraph")
    normal_style.addElement(TextProperties(fontsize="12pt"))
    doc.automaticstyles.addElement(normal_style)

    # Title paragraph
    title_para = P(stylename="NormalCustom")
    title_para.addText("Style Checklist for presentation_draft.odt:")
    doc.text.addElement(title_para)

    # Empty line
    doc.text.addElement(P())

    # Checked items using Unicode checkbox character (☑ = U+2611)
    checked_items = [
        "\u2611 Set page margins to 2cm all sides",
        "\u2611 Set document language to English (US)",
        "\u2611 Add page numbers in footer (centered)",
    ]

    for item_text in checked_items:
        item_para = P(stylename="NormalCustom")
        item_para.addText(item_text)
        doc.text.addElement(item_para)

    # Ensure the Desktop directory exists
    os.makedirs(os.path.dirname(CHECKLIST_PATH), exist_ok=True)
    doc.save(CHECKLIST_PATH)
    print(f"Checklist created: {CHECKLIST_PATH}")


def create_draft_odt():
    """
    Create presentation_draft.odt in Documents.
    3-page document with:
      - Default (wide) margins (NOT 2cm - that is what the agent must set)
      - NO footer
      - Language NOT explicitly set to English (US)
    """
    from odf.opendocument import OpenDocumentText
    from odf.style import (Style, TextProperties, ParagraphProperties,
                           PageLayout, PageLayoutProperties, MasterPage,
                           Header, Footer, DefaultStyle)
    from odf.text import P
    from odf.namespaces import OFFICENS, FONS, STYLENS, TEXTNS
    from odf import teletype
    import lxml.etree as ET

    doc = OpenDocumentText()

    # Page layout with default margins (2.54cm / 1 inch - NOT the 2cm task requires)
    page_layout = PageLayout(name="PageLayout1")
    page_layout.addElement(PageLayoutProperties(
        margintop="2.54cm",
        marginbottom="2.54cm",
        marginleft="2.54cm",
        marginright="2.54cm",
        pagewidth="21.001cm",
        pageheight="29.7cm",
    ))
    doc.automaticstyles.addElement(page_layout)

    # Master page (no header, no footer)
    master_page = MasterPage(name="Standard", pagelayoutname="PageLayout1")
    doc.masterstyles.addElement(master_page)

    # Heading style
    h1_style = Style(name="H1Style", family="paragraph")
    h1_style.addElement(TextProperties(fontsize="18pt", fontweight="bold"))
    doc.automaticstyles.addElement(h1_style)

    # Normal paragraph style
    body_style = Style(name="BodyStyle", family="paragraph")
    body_style.addElement(TextProperties(fontsize="12pt"))
    doc.automaticstyles.addElement(body_style)

    # Page break style
    page_break_style = Style(name="PageBreakStyle", family="paragraph")
    page_break_style.addElement(ParagraphProperties(breakbefore="page"))
    page_break_style.addElement(TextProperties(fontsize="12pt"))
    doc.automaticstyles.addElement(page_break_style)

    # ---- Page 1 ----
    p = P(stylename="H1Style")
    p.addText("Introduction to Q3 Marketing Strategy")
    doc.text.addElement(p)

    para1 = P(stylename="BodyStyle")
    para1.addText("The Q3 marketing campaign focuses on expanding our digital presence across key "
                  "social media platforms. Our primary objectives include increasing brand awareness "
                  "by 25% and generating qualified leads through targeted content marketing initiatives.")
    doc.text.addElement(para1)

    para2 = P(stylename="BodyStyle")
    para2.addText("The strategic approach combines data-driven insights with creative storytelling "
                  "to engage our target demographic of professionals aged 28-45. Key channels include "
                  "LinkedIn, industry newsletters, and webinar series.")
    doc.text.addElement(para2)

    para3 = P(stylename="BodyStyle")
    para3.addText("Budget allocation has been reviewed and approved by the finance committee. "
                  "A total of $180,000 has been reserved for Q3 campaigns, representing a 15% increase "
                  "from Q2 spending.")
    doc.text.addElement(para3)

    # ---- Page 2 (page break) ----
    pb2 = P(stylename="PageBreakStyle")
    pb2.addText("Campaign Timeline and Milestones")
    doc.text.addElement(pb2)

    para4 = P(stylename="BodyStyle")
    para4.addText("Phase 1 (July): Launch brand refresh campaign featuring updated visual identity. "
                  "Deliverables include new logo variants, color palette update, and revised brand "
                  "guidelines distributed to all departments.")
    doc.text.addElement(para4)

    para5 = P(stylename="BodyStyle")
    para5.addText("Phase 2 (August): Content marketing push with weekly blog posts, monthly "
                  "whitepapers, and bi-weekly video content. Target: 50 pieces of long-form content "
                  "across the quarter.")
    doc.text.addElement(para5)

    para6 = P(stylename="BodyStyle")
    para6.addText("Phase 3 (September): Performance review and optimization. A/B testing results "
                  "will be analyzed and top-performing content amplified through paid promotion. "
                  "Expected conversion rate improvement: 12-18%.")
    doc.text.addElement(para6)

    # ---- Page 3 (page break) ----
    pb3 = P(stylename="PageBreakStyle")
    pb3.addText("Performance Metrics and Success Criteria")
    doc.text.addElement(pb3)

    para7 = P(stylename="BodyStyle")
    para7.addText("Key Performance Indicators (KPIs) will be tracked on a weekly basis using our "
                  "integrated analytics dashboard. Primary metrics include website traffic, lead "
                  "conversion rates, email open rates, and social media engagement scores.")
    doc.text.addElement(para7)

    para8 = P(stylename="BodyStyle")
    para8.addText("Secondary metrics capture brand sentiment through monthly surveys and Net Promoter "
                  "Score (NPS) tracking. Customer feedback from regional sales teams will supplement "
                  "quantitative data with qualitative insights.")
    doc.text.addElement(para8)

    para9 = P(stylename="BodyStyle")
    para9.addText("Quarterly review meetings with department heads will evaluate progress against "
                  "targets. Final Q3 report due October 15th will include recommendations for Q4 "
                  "strategy adjustments.")
    doc.text.addElement(para9)

    # Ensure the Documents directory exists
    os.makedirs(os.path.dirname(DRAFT_PATH), exist_ok=True)
    doc.save(DRAFT_PATH)
    print(f"Draft created: {DRAFT_PATH}")


def create_initial():
    create_checklist_odt()
    create_draft_odt()

    # Open checklist first so agent can read it, then open the draft
    launch_gui(f'libreoffice --writer "{CHECKLIST_PATH}"', delay_sec=2.0)
    launch_gui(f'libreoffice --writer "{DRAFT_PATH}"', delay_sec=2.0)
    print("GUI_READY: launched LibreOffice Writer windows with DISPLAY=:0")


create_initial()
