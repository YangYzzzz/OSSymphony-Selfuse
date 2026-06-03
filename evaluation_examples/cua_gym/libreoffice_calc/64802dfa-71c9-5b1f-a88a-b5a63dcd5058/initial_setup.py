"""
Initial Setup: Save all open Chrome tabs as PDFs to /home/user/Documents/Papers
Task ID: osworld_multi_apps_bulk_pdf_save_007
Domain: multi_apps (Chrome + OS)

This script:
1. Kills any existing Chrome processes
2. Creates local HTML files simulating arXiv paper abstract pages
3. Ensures /home/user/Documents/Papers does NOT exist (clean initial state)
4. Launches Chrome with 3 tabs showing the paper abstract pages
5. Starts socat bridge for CDP remote debugging access
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_007'

# Paper data - 3 realistic arXiv paper abstracts
PAPERS = [
    {
        "title": "Attention Is All You Need",
        "arxiv_id": "1706.03762",
        "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin",
        "abstract": (
            "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks "
            "that include an encoder and a decoder. The best performing models also connect the encoder and decoder "
            "through an attention mechanism. We propose a new simple network architecture, the Transformer, based "
            "solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two "
            "machine translation tasks show these models to be superior in quality while being more parallelizable and "
            "requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German "
            "translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the "
            "WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art "
            "BLEU score of 41.0 after training for 3.5 days on eight GPUs, a small fraction of the training costs "
            "of the best models from the literature."
        ),
        "submitted": "Submitted on 12 Jun 2017",
        "subjects": "Computation and Language (cs.CL); Machine Learning (cs.LG)",
    },
    {
        "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "arxiv_id": "1810.04805",
        "authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        "abstract": (
            "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder "
            "Representations from Transformers. Unlike recent language representation models, BERT is designed to "
            "pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left "
            "and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just "
            "one additional output layer to create state-of-the-art models for a wide range of tasks, such as "
            "question answering and language inference, without substantial task-specific architecture modifications. "
            "BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven "
            "natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute "
            "improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering "
            "Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point "
            "absolute improvement)."
        ),
        "submitted": "Submitted on 11 Oct 2018",
        "subjects": "Computation and Language (cs.CL)",
    },
    {
        "title": "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
        "arxiv_id": "2010.11929",
        "authors": "Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, Neil Houlsby",
        "abstract": (
            "While the Transformer architecture has become the de-facto standard for natural language processing tasks, "
            "its applications to computer vision remain limited. In vision, attention is either applied in conjunction "
            "with convolutional networks, or used to replace certain components of convolutional networks while keeping "
            "their overall structure in place. We show that this reliance on CNNs is not necessary and a pure "
            "transformer applied directly to sequences of image patches can perform very well on image classification "
            "tasks. When pre-trained on large amounts of data and transferred to multiple mid-sized or small image "
            "recognition benchmarks (ImageNet, CIFAR-100, VTAB, etc.), Vision Transformer (ViT) attains excellent "
            "results compared to state-of-the-art convolutional networks while requiring substantially fewer "
            "computational resources to train."
        ),
        "submitted": "Submitted on 22 Oct 2020",
        "subjects": "Computer Vision and Pattern Recognition (cs.CV); Artificial Intelligence (cs.AI); Machine Learning (cs.LG)",
    },
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[{arxiv_id}] {title}</title>
    <style>
        body {{ font-family: 'Computer Modern', serif; margin: 0; padding: 0; background: #fff; color: #333; }}
        #header {{ background: #b31b1b; color: white; padding: 10px 20px; display: flex; align-items: center; }}
        #header h1 {{ font-size: 24px; margin: 0; font-weight: bold; letter-spacing: 1px; }}
        #header a {{ color: white; text-decoration: none; }}
        .container {{ max-width: 900px; margin: 30px auto; padding: 0 20px; }}
        h1.title {{ font-size: 22px; font-weight: bold; margin-bottom: 8px; color: #222; }}
        .authors {{ font-size: 14px; color: #555; margin-bottom: 6px; }}
        .submitted {{ font-size: 13px; color: #666; margin-bottom: 4px; }}
        .subjects {{ font-size: 13px; color: #666; margin-bottom: 20px; }}
        .abstract-title {{ font-size: 16px; font-weight: bold; margin-top: 20px; margin-bottom: 8px; }}
        .abstract {{ font-size: 14px; line-height: 1.7; text-align: justify; }}
        .arxiv-id {{ font-size: 13px; color: #b31b1b; font-weight: bold; margin-bottom: 6px; }}
        hr {{ border: none; border-top: 1px solid #ccc; margin: 20px 0; }}
    </style>
</head>
<body>
    <div id="header">
        <h1><a href="https://arxiv.org">arXiv.org</a> &gt; cs &gt; arXiv:{arxiv_id}</h1>
    </div>
    <div class="container">
        <div class="arxiv-id">arXiv:{arxiv_id}</div>
        <h1 class="title">{title}</h1>
        <div class="authors">{authors}</div>
        <div class="submitted">{submitted}</div>
        <div class="subjects">Subjects: {subjects}</div>
        <hr>
        <div class="abstract-title">Abstract</div>
        <div class="abstract">{abstract}</div>
    </div>
</body>
</html>
"""


def kill_chrome():
    """Kill any existing Chrome/Chromium processes."""
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(2)


def create_paper_html_files():
    """Create local HTML files simulating arXiv paper abstract pages."""
    html_dir = os.path.join(WORKDIR, f'.{TASK_ID}_papers')
    os.makedirs(html_dir, exist_ok=True)

    html_paths = []
    for i, paper in enumerate(PAPERS):
        html_content = HTML_TEMPLATE.format(**paper)
        fname = f'paper_{i+1}.html'
        fpath = os.path.join(html_dir, fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        html_paths.append(fpath)
        print(f'Created HTML for: {paper["title"]}')

    return html_paths


def ensure_papers_dir_absent():
    """Ensure /home/user/Documents/Papers does NOT exist for the initial state."""
    papers_dir = os.path.join(WORKDIR, 'Documents', 'Papers')
    if os.path.exists(papers_dir):
        shutil.rmtree(papers_dir)
        print(f'Removed pre-existing directory: {papers_dir}')
    else:
        print(f'Confirmed absent: {papers_dir}')

    # Ensure Documents dir exists (common in Linux desktops)
    docs_dir = os.path.join(WORKDIR, 'Documents')
    os.makedirs(docs_dir, exist_ok=True)


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


def start_socat_bridge():
    """Start socat bridge to expose Chrome CDP port 1337 on port 9222."""
    # Kill existing socat first
    subprocess.run(['pkill', '-f', 'socat.*9222'], capture_output=True)
    time.sleep(0.5)
    env = os.environ.copy()
    subprocess.Popen(
        ['socat', 'tcp-listen:9222,fork', 'tcp:localhost:1337'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(1)


def launch_chrome_with_tabs(html_paths):
    """Launch Chrome with debugging enabled and open 3 paper tabs."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"

    # Build file:// URLs for local HTML files
    file_urls = [f'file://{p}' for p in html_paths]

    # Chrome launch command with remote debugging
    chrome_cmd = [
        'google-chrome',
        '--remote-debugging-port=1337',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-sync',
        '--disable-default-apps',
    ] + file_urls

    subprocess.Popen(
        chrome_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(4)  # Wait for Chrome to fully load all tabs


def create_initial():
    print(f'=== Initial Setup: {TASK_ID} ===')

    # Step 1: Kill any existing Chrome processes
    kill_chrome()

    # Step 2: Create HTML files for the 3 arXiv papers
    html_paths = create_paper_html_files()

    # Step 3: Ensure Documents/Papers does NOT exist
    ensure_papers_dir_absent()

    # Step 4: Start socat bridge for CDP access
    start_socat_bridge()

    # Step 5: Launch Chrome with 3 paper tabs
    launch_chrome_with_tabs(html_paths)

    print('=== Initial setup complete ===')
    print('Chrome is open with 3 arXiv paper abstract tabs:')
    for paper in PAPERS:
        print(f'  - {paper["title"]}')
    print('Documents/Papers directory does NOT exist (needs to be created by agent).')
    print('GUI_READY: Chrome launched with DISPLAY=:0')


create_initial()
