"""
Initial Setup: Bookmark personal webpages of transformer paper authors
Task ID: osworld_multi_apps_bookmark_authors_001
Domain: chrome (multi-app with PDF on Desktop)

Creates:
1. A PDF of the 'Attention Is All You Need' paper on the Desktop
2. Clean Chrome bookmarks (no 'Transformer Authors' folder)
3. Opens Chrome and the PDF file so the agent can see the paper
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bookmark_authors_001'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/attention_is_all_you_need.pdf'

CHROME_DEFAULT = os.path.join(WORKDIR, '.config', 'google-chrome', 'Default')
BOOKMARKS_FILE = os.path.join(CHROME_DEFAULT, 'Bookmarks')


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


def create_pdf():
    """Create a realistic PDF of 'Attention Is All You Need' paper on the Desktop."""
    os.makedirs(DESKTOP, exist_ok=True)

    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, 'Attention Is All You Need', ln=True, align='C')
        pdf.ln(4)

        # Authors
        pdf.set_font('Helvetica', '', 11)
        authors = (
            'Ashish Vaswani*   Noam Shazeer*   Niki Parmar*   Jakob Uszkoreit*'
        )
        pdf.cell(0, 8, authors, ln=True, align='C')
        authors2 = (
            'Llion Jones*   Aidan N. Gomez*   Lukasz Kaiser*   Illia Polosukhin*'
        )
        pdf.cell(0, 8, authors2, ln=True, align='C')
        pdf.ln(4)

        # Affiliation note
        pdf.set_font('Helvetica', 'I', 9)
        pdf.cell(0, 6, '* Equal contribution', ln=True, align='C')
        pdf.cell(0, 6, 'Google Brain / Google Research / University of Toronto', ln=True, align='C')
        pdf.ln(6)

        # Abstract header
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, 'Abstract', ln=True, align='C')

        # Abstract text
        pdf.set_font('Helvetica', '', 10)
        abstract = (
            'The dominant sequence transduction models are based on complex recurrent or convolutional '
            'neural networks that include an encoder and a decoder. The best performing models also connect '
            'the encoder and decoder through an attention mechanism. We propose a new simple network '
            'architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence '
            'and convolutions entirely. Experiments on two machine translation tasks show these models to be '
            'superior in quality while being more parallelizable and requiring significantly less time to train. '
            'Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over '
            'the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 '
            'English-to-French translation task, our model establishes a new single-model state-of-the-art '
            'BLEU score of 41.0 after training for 3.5 days on eight GPUs, a small fraction of the training '
            'costs of the best models from the literature.'
        )
        pdf.multi_cell(0, 6, abstract)
        pdf.ln(6)

        # Introduction header
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, '1  Introduction', ln=True)

        # Introduction text
        pdf.set_font('Helvetica', '', 10)
        intro = (
            'Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks '
            'in particular, have been firmly established as state of the art approaches in sequence modeling '
            'and transduction problems such as language modeling and machine translation [35, 2, 5]. Numerous '
            'efforts have since continued to push the boundaries of recurrent language models and '
            'encoder-decoder architectures [38, 24, 15].\n\n'
            'Recurrent models typically factor computation along the symbol positions of the input and output '
            'sequences. Aligning the positions to steps in computation time, they generate a sequence of '
            'hidden states h_t, as a function of the previous hidden state h_{t-1} and the input for '
            'position t. This inherently sequential nature precludes parallelization within training examples, '
            'which becomes critical at longer sequence lengths, as memory constraints limit batching across '
            'examples. Recent work has achieved significant improvements in computational efficiency through '
            'factorization tricks [21] and conditional computation [32], while also improving model '
            'performance in case of the latter. The fundamental constraint of sequential computation, however, '
            'remains.\n\n'
            'Attention mechanisms have become an integral part of compelling sequence modeling and '
            'transduction models in various tasks, allowing modeling of dependencies without regard to their '
            'distance in the input or output sequences [2, 19]. In all but a few cases [27], however, such '
            'attention mechanisms are used in conjunction with a recurrent network.\n\n'
            'In this work we propose the Transformer, a model architecture eschewing recurrence and instead '
            'relying entirely on an attention mechanism to draw global dependencies between input and output. '
            'The Transformer allows for significantly more parallelization and can reach a new state of the '
            'art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.'
        )
        pdf.multi_cell(0, 6, intro)
        pdf.ln(6)

        # Model Architecture section
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, '2  Model Architecture', ln=True)

        pdf.set_font('Helvetica', '', 10)
        arch = (
            'Most competitive neural sequence transduction models have an encoder-decoder structure [5, 2, 35]. '
            'Here, the encoder maps an input sequence of symbol representations (x_1, ..., x_n) to a '
            'sequence of continuous representations z = (z_1, ..., z_n). Given z, the decoder then generates '
            'an output sequence (y_1, ..., y_m) of symbols one element at a time. At each step the model is '
            'auto-regressive [10], consuming the previously generated symbols as additional input when '
            'generating the next.\n\n'
            'The Transformer follows this overall architecture using stacked self-attention and '
            'point-wise, fully connected layers for both the encoder and decoder, shown in the left and '
            'right halves of Figure 1, respectively.'
        )
        pdf.multi_cell(0, 6, arch)

        pdf.output(PDF_PATH)
        print(f'PDF created: {PDF_PATH}')

    except ImportError:
        # Fallback: create a minimal PDF manually
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj

2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj

3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj

4 0 obj
<< /Length 800 >>
stream
BT
/F1 16 Tf
150 740 Td
(Attention Is All You Need) Tj
/F1 11 Tf
60 700 Td
(Ashish Vaswani   Noam Shazeer   Niki Parmar   Jakob Uszkoreit) Tj
60 680 Td
(Llion Jones   Aidan N. Gomez   Lukasz Kaiser   Illia Polosukhin) Tj
/F1 10 Tf
60 640 Td
(Abstract) Tj
60 620 Td
(The dominant sequence transduction models are based on complex recurrent or) Tj
60 605 Td
(convolutional neural networks that include an encoder and a decoder. We propose) Tj
60 590 Td
(the Transformer, a model architecture based solely on attention mechanisms.) Tj
60 575 Td
(Our model achieves 28.4 BLEU on WMT 2014 English-to-German translation.) Tj
ET
endstream
endobj

5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj

xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000266 00000 n
0000001118 00000 n

trailer
<< /Size 6 /Root 1 0 R >>
startxref
1200
%%EOF"""
        with open(PDF_PATH, 'wb') as f:
            f.write(pdf_content)
        print(f'PDF created (fallback): {PDF_PATH}')


def setup_chrome_bookmarks():
    """Ensure Chrome bookmarks have NO 'Transformer Authors' folder - clean state."""
    os.makedirs(CHROME_DEFAULT, exist_ok=True)

    if os.path.exists(BOOKMARKS_FILE):
        with open(BOOKMARKS_FILE, 'r') as f:
            bookmarks = json.load(f)

        # Remove any existing 'Transformer Authors' folder if present
        bar_children = bookmarks['roots']['bookmark_bar']['children']
        bar_children = [
            child for child in bar_children
            if not (child.get('type') == 'folder' and child.get('name') == 'Transformer Authors')
        ]
        bookmarks['roots']['bookmark_bar']['children'] = bar_children

        with open(BOOKMARKS_FILE, 'w') as f:
            json.dump(bookmarks, f, indent=3)
        print('Chrome bookmarks cleaned: no Transformer Authors folder present')
    else:
        print(f'Bookmarks file not found at {BOOKMARKS_FILE}')


def main():
    # Step 1: Create the PDF on the Desktop
    create_pdf()

    # Step 2: Ensure Chrome bookmarks are clean (no task-completed state)
    setup_chrome_bookmarks()

    # Step 3: Kill any running Chrome instances before relaunching
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    time.sleep(2)

    # Step 4: Launch Chrome with the PDF open so the agent sees the paper
    # Chrome opens a PDF file by navigating to it with file:// URL
    launch_gui(f'google-chrome --no-first-run "file://{PDF_PATH}"', delay_sec=3.0)

    print('GUI_READY: Chrome launched with PDF paper open on DISPLAY=:0')
    print(f'Initial state ready: PDF at {PDF_PATH}')
    print(f'Chrome open with NO Transformer Authors bookmarks')


main()
