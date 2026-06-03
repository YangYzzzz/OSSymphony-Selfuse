"""
Initial Setup: Create resource_list.pdf with hyperlinks across multiple domains
Task ID: pdf_cross_102
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'pdf_cross_102'
PDF_OUTPUT = f'{WORKDIR}/Documents/resource_list.pdf'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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

    # Create directories
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    print(f'Created scripts directory: {SCRIPTS_DIR}')

    # Ensure extract_urls.py does NOT exist
    extract_script = f'{SCRIPTS_DIR}/extract_urls.py'
    if os.path.exists(extract_script):
        os.remove(extract_script)
    url_report = f'{WORKDIR}/Documents/url_report.json'
    if os.path.exists(url_report):
        os.remove(url_report)

    # Define all URLs with their domains - ~45 links across 6 domains + a few others
    github_urls = [
        "https://github.com/python/cpython",
        "https://github.com/pallets/flask",
        "https://github.com/django/django",
        "https://github.com/numpy/numpy",
        "https://github.com/pandas-dev/pandas",
        "https://github.com/scikit-learn/scikit-learn",
        "https://github.com/pytorch/pytorch",
        "https://github.com/tensorflow/tensorflow",
    ]
    python_docs_urls = [
        "https://docs.python.org/3/library/os.html",
        "https://docs.python.org/3/library/json.html",
        "https://docs.python.org/3/library/re.html",
        "https://docs.python.org/3/library/pathlib.html",
        "https://docs.python.org/3/tutorial/index.html",
        "https://docs.python.org/3/library/urllib.parse.html",
        "https://docs.python.org/3/library/collections.html",
    ]
    stackoverflow_urls = [
        "https://stackoverflow.com/questions/1732348/regex-match-open-tags",
        "https://stackoverflow.com/questions/2081586/web-scraping-with-python",
        "https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory",
        "https://stackoverflow.com/questions/6357361/alternative-to-os-path-join-for-urls",
        "https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file",
        "https://stackoverflow.com/questions/2504411/proper-indentation-for-python-multiline-strings",
        "https://stackoverflow.com/questions/9029294/python-dictionary-update",
    ]
    medium_urls = [
        "https://medium.com/@pythondeveloper/getting-started-with-pymupdf",
        "https://medium.com/towards-data-science/python-pdf-processing-guide",
        "https://medium.com/better-programming/top-python-libraries-2024",
        "https://medium.com/@developer/understanding-python-decorators",
        "https://medium.com/analytics-vidhya/data-wrangling-with-pandas",
        "https://medium.com/geekculture/docker-best-practices-2024",
    ]
    arxiv_urls = [
        "https://arxiv.org/abs/1706.03762",
        "https://arxiv.org/abs/1810.04805",
        "https://arxiv.org/abs/2005.14165",
        "https://arxiv.org/abs/1512.03385",
        "https://arxiv.org/abs/2010.11929",
        "https://arxiv.org/abs/2103.00020",
    ]
    other_urls = [
        "https://pypi.org/project/pymupdf/",
        "https://pypi.org/project/requests/",
        "https://readthedocs.org/projects/pymupdf/",
        "https://realpython.com/python-pdf-processing/",
        "https://realpython.com/python-requests/",
        "https://wikipedia.org/wiki/PDF",
        "https://en.wikipedia.org/wiki/Hyperlink",
        "https://www.w3.org/TR/pdf-structure/",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview",
        "https://developer.mozilla.org/en-US/docs/Web/API/URL",
        "https://docs.github.com/en/rest",
    ]

    doc = pymupdf.open()

    # ─── PAGE 1: Introduction & Overview ───────────────────────────────────────
    page1 = doc.new_page(width=612, height=792)

    # Title
    page1.insert_text(pymupdf.Point(72, 60), "Resource List: Python & Machine Learning",
                      fontsize=18, fontname="hebo", color=(0, 0, 0.6))
    page1.insert_text(pymupdf.Point(72, 85), "A curated collection of useful links across major domains",
                      fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape1.finish(color=(0.5, 0.5, 0.5), width=1)
    shape1.commit()

    # Introduction paragraph
    intro_rect = pymupdf.Rect(72, 105, 540, 180)
    page1.insert_textbox(
        intro_rect,
        "This document provides a comprehensive list of online resources for Python developers "
        "and machine learning practitioners. Resources are organized by domain and include "
        "official documentation, community Q&A, research papers, tutorials, and open-source "
        "project repositories.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=0
    )

    # Section header
    page1.insert_text(pymupdf.Point(72, 200), "1. GitHub Repositories",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))

    # GitHub links - annotation-based (embedded hyperlinks with visible text)
    github_y = 225
    for i, url in enumerate(github_urls[:4]):
        repo_name = url.replace("https://github.com/", "")
        page1.insert_text(pymupdf.Point(90, github_y), f"• {repo_name}",
                          fontsize=11, fontname="helv", color=(0, 0, 0.7))
        link_rect = pymupdf.Rect(90, github_y - 12, 400, github_y + 2)
        page1.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        github_y += 22

    # Section: Python Docs with text-based URLs visible
    page1.insert_text(pymupdf.Point(72, 330), "2. Official Python Documentation",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))
    page1.insert_text(pymupdf.Point(90, 355),
                      "Visit the official docs at: https://docs.python.org/3/tutorial/index.html",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(90, 372),
                      "JSON library: https://docs.python.org/3/library/json.html",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(90, 389),
                      "OS module: https://docs.python.org/3/library/os.html",
                      fontsize=10, fontname="helv", color=(0, 0, 0))

    # ─── PAGE 2: More GitHub + Stack Overflow ──────────────────────────────────
    page2 = doc.new_page(width=612, height=792)

    page2.insert_text(pymupdf.Point(72, 60), "Page 2: Repositories & Community Resources",
                      fontsize=16, fontname="hebo", color=(0, 0, 0.6))
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape2.finish(color=(0.5, 0.5, 0.5), width=1)
    shape2.commit()

    # Remaining GitHub links (annotation-based)
    page2.insert_text(pymupdf.Point(72, 95), "More GitHub Repositories:",
                      fontsize=13, fontname="hebo", color=(0, 0.3, 0.6))
    g_y = 118
    for url in github_urls[4:]:
        repo_name = url.replace("https://github.com/", "")
        page2.insert_text(pymupdf.Point(90, g_y), f"• {repo_name}",
                          fontsize=11, fontname="helv", color=(0, 0, 0.7))
        link_rect = pymupdf.Rect(90, g_y - 12, 420, g_y + 2)
        page2.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        g_y += 22

    # Stack Overflow section
    page2.insert_text(pymupdf.Point(72, 220), "3. Stack Overflow Q&A",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))
    so_y = 245
    for url in stackoverflow_urls[:4]:
        # Mix: some annotation-based, some text-based
        qid = url.split("/questions/")[1].split("/")[0]
        page2.insert_text(pymupdf.Point(90, so_y), f"• Question #{qid}: {url}",
                          fontsize=9, fontname="helv", color=(0, 0, 0))
        link_rect = pymupdf.Rect(90, so_y - 10, 540, so_y + 2)
        page2.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        so_y += 22

    # Text-based SO URLs
    page2.insert_text(pymupdf.Point(72, 350), "Additional Stack Overflow references (text URLs):",
                      fontsize=12, fontname="hebo", color=(0, 0.3, 0.6))
    so_text_y = 372
    for url in stackoverflow_urls[4:]:
        page2.insert_text(pymupdf.Point(90, so_text_y), url,
                          fontsize=9, fontname="helv", color=(0, 0, 0.8))
        so_text_y += 18

    # Python docs annotation links
    page2.insert_text(pymupdf.Point(72, 435), "Python Docs (linked):",
                      fontsize=12, fontname="hebo", color=(0, 0.3, 0.6))
    pd_y = 458
    for url in python_docs_urls[3:]:
        label = url.split("/")[-1].replace(".html", "")
        page2.insert_text(pymupdf.Point(90, pd_y), f"• {label}",
                          fontsize=11, fontname="helv", color=(0, 0, 0.7))
        link_rect = pymupdf.Rect(90, pd_y - 12, 350, pd_y + 2)
        page2.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        pd_y += 22

    # ─── PAGE 3: arXiv Papers ──────────────────────────────────────────────────
    page3 = doc.new_page(width=612, height=792)

    page3.insert_text(pymupdf.Point(72, 60), "Page 3: Research Papers (arXiv)",
                      fontsize=16, fontname="hebo", color=(0, 0, 0.6))
    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape3.finish(color=(0.5, 0.5, 0.5), width=1)
    shape3.commit()

    paper_titles = [
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "Language Models are Few-Shot Learners (GPT-3)",
        "Deep Residual Learning for Image Recognition",
        "An Image is Worth 16x16 Words (ViT)",
        "Learning Transferable Visual Models From Natural Language (CLIP)",
    ]
    ax_y = 100
    page3.insert_text(pymupdf.Point(72, 88), "4. Research Papers",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))
    for i, (url, title) in enumerate(zip(arxiv_urls, paper_titles)):
        arxiv_id = url.split("/abs/")[1]
        page3.insert_text(pymupdf.Point(90, ax_y), f"[{i+1}] {title}",
                          fontsize=11, fontname="hebo", color=(0, 0, 0))
        ax_y += 16
        page3.insert_text(pymupdf.Point(105, ax_y), f"arXiv: {arxiv_id}  -  {url}",
                          fontsize=9, fontname="helv", color=(0.2, 0.2, 0.6))
        link_rect = pymupdf.Rect(105, ax_y - 10, 540, ax_y + 2)
        page3.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        ax_y += 26

    # ─── PAGE 4: Medium Articles ───────────────────────────────────────────────
    page4 = doc.new_page(width=612, height=792)

    page4.insert_text(pymupdf.Point(72, 60), "Page 4: Blog Posts & Articles (Medium)",
                      fontsize=16, fontname="hebo", color=(0, 0, 0.6))
    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape4.finish(color=(0.5, 0.5, 0.5), width=1)
    shape4.commit()

    page4.insert_text(pymupdf.Point(72, 90), "5. Medium Articles & Blog Posts",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))

    medium_titles = [
        "Getting Started with PyMuPDF",
        "Python PDF Processing Guide",
        "Top Python Libraries 2024",
        "Understanding Python Decorators",
        "Data Wrangling with Pandas",
        "Docker Best Practices 2024",
    ]
    med_y = 115
    for url, title in zip(medium_urls, medium_titles):
        # Annotation-based links with title text
        page4.insert_text(pymupdf.Point(90, med_y), f"• {title}",
                          fontsize=11, fontname="helv", color=(0, 0, 0.7))
        link_rect = pymupdf.Rect(90, med_y - 12, 430, med_y + 2)
        page4.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        med_y += 22

    # Add some visible text URLs for medium as well
    page4.insert_text(pymupdf.Point(72, 260), "Direct article links:",
                      fontsize=12, fontname="hebo", color=(0, 0.3, 0.6))
    med_text_y = 280
    for url in medium_urls[:3]:
        page4.insert_text(pymupdf.Point(90, med_text_y), url,
                          fontsize=9, fontname="helv", color=(0, 0, 0.8))
        med_text_y += 18

    # ─── PAGE 5: Other Resources ──────────────────────────────────────────────
    page5 = doc.new_page(width=612, height=792)

    page5.insert_text(pymupdf.Point(72, 60), "Page 5: Additional Resources",
                      fontsize=16, fontname="hebo", color=(0, 0, 0.6))
    shape5 = page5.new_shape()
    shape5.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape5.finish(color=(0.5, 0.5, 0.5), width=1)
    shape5.commit()

    page5.insert_text(pymupdf.Point(72, 90), "6. PyPI Packages",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))
    pypi_y = 115
    for url in other_urls[:2]:
        pkg = url.replace("https://pypi.org/project/", "").rstrip("/")
        page5.insert_text(pymupdf.Point(90, pypi_y), f"• {pkg}",
                          fontsize=11, fontname="helv", color=(0, 0, 0.7))
        link_rect = pymupdf.Rect(90, pypi_y - 12, 350, pypi_y + 2)
        page5.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        pypi_y += 22

    page5.insert_text(pymupdf.Point(72, 175), "7. Tutorials & Guides",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))
    tut_y = 200
    for url in other_urls[3:6]:
        page5.insert_text(pymupdf.Point(90, tut_y), url,
                          fontsize=9, fontname="helv", color=(0, 0, 0.8))
        link_rect = pymupdf.Rect(90, tut_y - 10, 540, tut_y + 2)
        page5.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        tut_y += 22

    page5.insert_text(pymupdf.Point(72, 270), "8. Reference Documentation",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))
    ref_y = 295
    for url in other_urls[6:]:
        page5.insert_text(pymupdf.Point(90, ref_y), url,
                          fontsize=9, fontname="helv", color=(0, 0, 0))
        ref_y += 18

    # ─── PAGE 6: Summary & Misc ────────────────────────────────────────────────
    page6 = doc.new_page(width=612, height=792)

    page6.insert_text(pymupdf.Point(72, 60), "Page 6: Summary & Quick Reference",
                      fontsize=16, fontname="hebo", color=(0, 0, 0.6))
    shape6 = page6.new_shape()
    shape6.draw_line(pymupdf.Point(72, 72), pymupdf.Point(540, 72))
    shape6.finish(color=(0.5, 0.5, 0.5), width=1)
    shape6.commit()

    summary_rect = pymupdf.Rect(72, 85, 540, 155)
    page6.insert_textbox(
        summary_rect,
        "This document contains links to key Python and ML resources across major platforms: "
        "GitHub repositories for popular frameworks, official Python documentation pages, "
        "Stack Overflow answers, arXiv research papers, Medium blog posts, and PyPI packages.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=0
    )

    # Quick reference table-like layout
    page6.insert_text(pymupdf.Point(72, 170), "Domain Summary:",
                      fontsize=13, fontname="hebo", color=(0, 0.3, 0.6))
    domains_summary = [
        ("github.com", "8 repositories"),
        ("docs.python.org", "7 documentation pages"),
        ("stackoverflow.com", "7 Q&A threads"),
        ("medium.com", "6 articles"),
        ("arxiv.org", "6 research papers"),
        ("other domains", "11 additional links"),
    ]
    sum_y = 195
    for domain, count in domains_summary:
        page6.insert_text(pymupdf.Point(90, sum_y), f"• {domain}: {count}",
                          fontsize=11, fontname="helv", color=(0, 0, 0))
        sum_y += 20

    # Add annotation links for pypi and readthedocs (remaining other_urls)
    page6.insert_text(pymupdf.Point(72, 340), "9. ReadTheDocs & Specifications",
                      fontsize=14, fontname="hebo", color=(0, 0.3, 0.6))
    rd_y = 365
    for url in [other_urls[2]]:  # readthedocs
        page6.insert_text(pymupdf.Point(90, rd_y), f"• PyMuPDF Documentation",
                          fontsize=11, fontname="helv", color=(0, 0, 0.7))
        link_rect = pymupdf.Rect(90, rd_y - 12, 350, rd_y + 2)
        page6.insert_link({"kind": pymupdf.LINK_URI, "from": link_rect, "uri": url})
        rd_y += 22

    # Also add some text-based remaining python docs on this page
    page6.insert_text(pymupdf.Point(72, 410), "Python Docs Quick Links:",
                      fontsize=13, fontname="hebo", color=(0, 0.3, 0.6))
    pd_text_y = 432
    for url in python_docs_urls[:2]:
        page6.insert_text(pymupdf.Point(90, pd_text_y), url,
                          fontsize=9, fontname="helv", color=(0, 0, 0.8))
        pd_text_y += 18

    # Footer note
    page6.insert_text(pymupdf.Point(72, 720),
                      "Generated for CUA-Gym task pdf_cross_102. Use extract_urls.py to process.",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Save the PDF
    doc.save(PDF_OUTPUT)
    doc.close()
    print(f'Initial PDF created: {PDF_OUTPUT}')

    # Verify scripts dir exists and extract_urls.py does NOT exist
    assert os.path.isdir(SCRIPTS_DIR), f"Scripts dir not found: {SCRIPTS_DIR}"
    assert not os.path.exists(f'{SCRIPTS_DIR}/extract_urls.py'), "extract_urls.py should NOT exist in initial env"
    assert not os.path.exists(f'{WORKDIR}/Documents/url_report.json'), "url_report.json should NOT exist in initial env"
    print(f'Scripts directory ready: {SCRIPTS_DIR}')
    print(f'Verified: extract_urls.py does NOT exist (agent must create it)')
    print(f'Verified: url_report.json does NOT exist (agent must create it)')

    # GUI-ready startup
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince to display resource_list.pdf with DISPLAY=:0')


create_initial()
