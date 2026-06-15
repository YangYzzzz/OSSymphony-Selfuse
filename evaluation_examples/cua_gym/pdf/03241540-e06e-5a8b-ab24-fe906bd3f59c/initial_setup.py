"""
Initial Setup: Create a bilingual PDF with text in multiple languages/scripts.
Task ID: pdf_cr_075
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'pdf_cr_075'
OUTPUT = f'{DESKTOP}/bilingual.pdf'


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
    import pymupdf

    os.makedirs(DESKTOP, exist_ok=True)

    doc = pymupdf.open()

    # ====== Page 1: Title page + English introduction with some CJK ======
    page1 = doc.new_page(width=595, height=842)

    # Title
    page1.insert_text(
        pymupdf.Point(72, 60),
        "Global Market Expansion Report",
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Subtitle
    page1.insert_text(
        pymupdf.Point(72, 90),
        "Prepared by: International Strategy Division",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 105), pymupdf.Point(523, 105))
    shape.finish(color=(0.6, 0.6, 0.6), width=1)
    shape.commit()

    # English paragraph
    rect1 = pymupdf.Rect(72, 120, 523, 300)
    page1.insert_textbox(
        rect1,
        "This report presents an analysis of market expansion opportunities across "
        "the Asia-Pacific region. Our research team conducted extensive surveys in "
        "Tokyo, Shanghai, Seoul, and Singapore during Q1 2025. The findings reveal "
        "significant growth potential in cloud computing services, with projected "
        "annual revenue increases of 23% to 35% across all four markets. Key "
        "stakeholders from Mitsubishi Electric, Tencent Holdings, Samsung Electronics, "
        "and DBS Group provided strategic insights during the consultation phase.",
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # CJK content section - use a CJK-capable font
    # Try to use a system CJK font
    cjk_font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc",
    ]

    cjk_font = None
    cjk_font_path = None
    for fp in cjk_font_paths:
        if os.path.exists(fp):
            try:
                cjk_font = pymupdf.Font(fontfile=fp)
                cjk_font_path = fp
                break
            except Exception:
                continue

    # Section header
    page1.insert_text(
        pymupdf.Point(72, 330),
        "Executive Summary / \u6267\u884c\u6458\u8981",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    if cjk_font:
        tw = pymupdf.TextWriter(page1.rect)
        # CJK paragraph
        cjk_text = (
            "\u672c\u62a5\u544a\u6db5\u76d6\u4e86\u4e9a\u592a\u5730\u533a\u7684"
            "\u5e02\u573a\u6269\u5f20\u673a\u4f1a\u5206\u6790\u3002\u6211\u4eec"
            "\u7684\u7814\u7a76\u56e2\u961f\u57282025\u5e74\u7b2c\u4e00\u5b63"
            "\u5ea6\u5728\u4e1c\u4eac\u3001\u4e0a\u6d77\u3001\u9996\u5c14\u548c"
            "\u65b0\u52a0\u5761\u8fdb\u884c\u4e86\u5e7f\u6cdb\u7684\u8c03\u67e5"
            "\u3002\u7814\u7a76\u7ed3\u679c\u663e\u793a\uff0c\u4e91\u8ba1\u7b97"
            "\u670d\u52a1\u5728\u8fd9\u56db\u4e2a\u5e02\u573a\u5747\u5177\u6709"
            "\u663e\u8457\u7684\u589e\u957f\u6f5c\u529b\uff0c\u9884\u8ba1\u5e74"
            "\u6536\u5165\u589e\u957f\u7387\u4e3a23%\u81f335%\u3002"
        )
        tw.append(pymupdf.Point(72, 370), cjk_text, font=cjk_font, fontsize=10)
        tw.write_text(page1, color=(0, 0, 0))
    else:
        # Fallback: insert CJK as unicode text (may render as boxes but still extractable)
        page1.insert_text(
            pymupdf.Point(72, 370),
            "\u672c\u62a5\u544a\u6db5\u76d6\u4e86\u4e9a\u592a\u5730\u533a\u7684"
            "\u5e02\u573a\u6269\u5f20\u673a\u4f1a\u5206\u6790\u3002",
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
        )

    # More English text at bottom of page 1
    rect2 = pymupdf.Rect(72, 440, 523, 600)
    page1.insert_textbox(
        rect2,
        "The following sections detail market-specific findings, competitive landscape "
        "analysis, and recommended entry strategies. Financial projections are based on "
        "data collected from 247 enterprise clients and validated against publicly "
        "available market research from Gartner, IDC, and McKinsey Global Institute.",
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ====== Page 2: Mixed Latin and CJK data table content ======
    page2 = doc.new_page(width=595, height=842)

    page2.insert_text(
        pymupdf.Point(72, 60),
        "Market Analysis: Regional Performance",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Table header
    table_y = 100
    headers = ["Region", "Revenue (USD)", "Growth %", "Employees"]
    col_x = [72, 200, 330, 440]
    for i, h in enumerate(headers):
        page2.insert_text(pymupdf.Point(col_x[i], table_y), h, fontsize=10, fontname="hebo", color=(0, 0, 0))

    # Draw header underline
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, table_y + 5), pymupdf.Point(523, table_y + 5))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()

    # Table data
    table_data = [
        ["North America", "$12,450,000", "18.2%", "3,240"],
        ["Western Europe", "$8,930,000", "14.7%", "2,180"],
        ["Japan / \u65e5\u672c", "$6,720,000", "22.5%", "1,450"],
        ["China / \u4e2d\u56fd", "$9,180,000", "31.4%", "2,890"],
        ["South Korea / \u97e9\u56fd", "$4,560,000", "26.8%", "980"],
        ["Southeast Asia", "$3,890,000", "35.1%", "1,120"],
        ["Australia / NZ", "$2,340,000", "12.3%", "620"],
    ]

    for row_idx, row in enumerate(table_data):
        y = table_y + 25 + row_idx * 22
        for col_idx, val in enumerate(row):
            if cjk_font and any(ord(c) > 0x2FFF for c in val):
                tw2 = pymupdf.TextWriter(page2.rect)
                tw2.append(pymupdf.Point(col_x[col_idx], y), val, font=cjk_font, fontsize=10)
                tw2.write_text(page2, color=(0, 0, 0))
            else:
                page2.insert_text(pymupdf.Point(col_x[col_idx], y), val, fontsize=10, fontname="helv", color=(0, 0, 0))

    # Additional analysis in English
    rect3 = pymupdf.Rect(72, 320, 523, 500)
    page2.insert_textbox(
        rect3,
        "The Asia-Pacific markets demonstrate particularly strong growth trajectories. "
        "China leads with a 31.4% year-over-year increase, driven by enterprise digital "
        "transformation initiatives. Southeast Asian markets show the highest growth rate "
        "at 35.1%, albeit from a smaller base. Japan maintains steady growth at 22.5%, "
        "supported by government incentives for cloud adoption in traditional industries. "
        "South Korea benefits from strong 5G infrastructure enabling edge computing adoption.",
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # CJK analysis paragraph
    if cjk_font:
        tw3 = pymupdf.TextWriter(page2.rect)
        cjk_analysis = (
            "\u4e9a\u592a\u5730\u533a\u7684\u5e02\u573a\u589e\u957f\u52a8\u529b"
            "\u4e3b\u8981\u6765\u6e90\u4e8e\u4f01\u4e1a\u6570\u5b57\u5316\u8f6c"
            "\u578b\u548c\u4e91\u8ba1\u7b97\u670d\u52a1\u7684\u666e\u53ca\u3002"
            "\u7279\u522b\u662f\u4e2d\u56fd\u5e02\u573a\uff0c\u53d7\u76ca\u4e8e"
            "\u653f\u5e9c\u653f\u7b56\u652f\u6301\u548c\u5927\u578b\u4f01\u4e1a"
            "\u7684\u79ef\u6781\u6295\u5165\uff0c\u589e\u957f\u52bf\u5934\u5f3a"
            "\u52b2\u3002"
        )
        tw3.append(pymupdf.Point(72, 530), cjk_analysis, font=cjk_font, fontsize=10)
        tw3.write_text(page2, color=(0, 0, 0))

    # ====== Page 3: Mostly English with strategic recommendations ======
    page3 = doc.new_page(width=595, height=842)

    page3.insert_text(
        pymupdf.Point(72, 60),
        "Strategic Recommendations",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    recommendations = (
        "Based on our comprehensive analysis, we recommend the following strategic "
        "initiatives for the next fiscal year:\n\n"
        "1. Establish dedicated cloud service centers in Shanghai and Tokyo within "
        "Q2 2025, leveraging existing partnerships with Alibaba Cloud and AWS Japan.\n\n"
        "2. Expand the Southeast Asian sales team by 40%, focusing on enterprise "
        "clients in Singapore, Jakarta, and Bangkok.\n\n"
        "3. Launch localized product offerings with full CJK language support, "
        "including documentation in Simplified Chinese, Traditional Chinese, Japanese, "
        "and Korean.\n\n"
        "4. Invest $2.5M in regional marketing campaigns targeting mid-market "
        "enterprises (500-5000 employees) across all four priority markets.\n\n"
        "5. Develop strategic partnerships with local system integrators including "
        "Fujitsu (Japan), Inspur (China), LG CNS (South Korea), and NCS Group (Singapore)."
    )

    rect4 = pymupdf.Rect(72, 85, 523, 450)
    page3.insert_textbox(
        rect4,
        recommendations,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer with mixed text
    page3.insert_text(
        pymupdf.Point(72, 750),
        "Confidential - Internal Use Only",
        fontsize=9,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    if cjk_font:
        tw4 = pymupdf.TextWriter(page3.rect)
        tw4.append(pymupdf.Point(72, 770), "\u673a\u5bc6 - \u4ec5\u4f9b\u5185\u90e8\u4f7f\u7528", font=cjk_font, fontsize=9)
        tw4.write_text(page3, color=(0.5, 0.5, 0.5))

    # ====== Page 4: Appendix with CJK-heavy content ======
    page4 = doc.new_page(width=595, height=842)

    page4.insert_text(
        pymupdf.Point(72, 60),
        "Appendix A: Partner Directory / \u9644\u5f55A\uff1a\u5408\u4f5c\u4f19\u4f34\u76ee\u5f55",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    if cjk_font:
        tw5 = pymupdf.TextWriter(page4.rect)

        partners_cjk = [
            ("\u4e09\u83f1\u7535\u673a\u682a\u5f0f\u4f1a\u793e (Mitsubishi Electric)", 100),
            ("\u6771\u4eac\u672c\u793e: \u6771\u4eac\u90fd\u5343\u4ee3\u7530\u533a\u4e38\u306e\u5185\u4e8c\u4e01\u76ee7\u756a3\u53f7", 120),
            ("", 145),
            ("\u817e\u8baf\u63a7\u80a1\u6709\u9650\u516c\u53f8 (Tencent Holdings)", 170),
            ("\u6df1\u5733\u603b\u90e8: \u5e7f\u4e1c\u7701\u6df1\u5733\u5e02\u5357\u5c71\u533a\u79d1\u6280\u4e2d\u4e00\u8def", 190),
            ("", 215),
            ("\uc0bc\uc131\uc804\uc790 (Samsung Electronics)", 240),
            ("\uc11c\uc6b8\ubcf8\uc0ac: \uc11c\uc6b8\ud2b9\ubcc4\uc2dc \uc11c\ucd08\uad6c \uc11c\ucd08\ub300\ub85c74\uae38 11", 260),
        ]

        for text, y in partners_cjk:
            if text:
                tw5.append(pymupdf.Point(72, y), text, font=cjk_font, fontsize=10)

        tw5.write_text(page4, color=(0, 0, 0))

    # English partner entries
    en_partners = [
        ("DBS Group Holdings Ltd", 310),
        ("Singapore HQ: 12 Marina Boulevard, DBS Asia Central, Singapore 018982", 330),
        ("", 355),
        ("NCS Group Pte Ltd", 380),
        ("Block 71, Ayer Rajah Crescent, #01-01, Singapore 139951", 400),
    ]
    for text, y in en_partners:
        if text:
            page4.insert_text(pymupdf.Point(72, y), text, fontsize=10, fontname="helv", color=(0, 0, 0))

    # Contact info
    page4.insert_text(
        pymupdf.Point(72, 460),
        "For inquiries, contact: strategy@globalcorp.com",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
    )

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Make sure language_report.txt does NOT exist
    report_path = f'{DESKTOP}/language_report.txt'
    if os.path.exists(report_path):
        os.remove(report_path)

    # Open PDF in evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
