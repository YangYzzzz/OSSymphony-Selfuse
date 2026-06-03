"""
Initial Setup: Deep Speech 2 paper PDF on Desktop, Chrome open, no bookmarks yet.
Task ID: osworld_multi_apps_bookmark_authors_015
Domain: chrome / multi-app
"""

import os
import json
import shlex
import subprocess
import time
import urllib.request

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bookmark_authors_015'
DESKTOP_DIR = '/home/user/Desktop'
PDF_PATH = f'{DESKTOP_DIR}/deep_speech2.pdf'

CHROME_USER_DATA = os.path.expanduser('~/.config/google-chrome')
CHROME_DEFAULT = os.path.join(CHROME_USER_DATA, 'Default')
BOOKMARKS_FILE = os.path.join(CHROME_DEFAULT, 'Bookmarks')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def kill_chrome():
    """Kill any running Chrome instances so we can modify config files."""
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(2)


def create_deep_speech2_pdf():
    """Create a realistic Deep Speech 2 PDF on the Desktop using fpdf2."""
    os.makedirs(DESKTOP_DIR, exist_ok=True)

    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font('Helvetica', 'B', 16)
        pdf.multi_cell(0, 10, 'Deep Speech 2: End-to-End Speech Recognition in English and Mandarin', align='C')
        pdf.ln(5)

        # Authors
        pdf.set_font('Helvetica', '', 11)
        authors = (
            'Dario Amodei, Rishita Anubhai, Eric Battenberg, Carl Case, Jared Casper, '
            'Bryan Catanzaro, Jingdong Chen, Mike Chrzanowski, Adam Coates, Greg Diamos, '
            'Erich Elsen, Jesse Engel, Linxi Fan, Christopher Fougner, Tony Han, Awni Hannun, '
            'Billy Jun, Patrick LeGresley, Libby Lin, Jitong Chen, Xu Liu, KiJung Park, '
            'Patrick Nguyen, Mary Power, Sameep Raju, Sherjil Ozair, Andrew Ng, Sharan Narang, '
            'Ziang Xie, Peng Qi'
        )
        pdf.multi_cell(0, 7, authors, align='C')
        pdf.ln(3)

        # Affiliation
        pdf.set_font('Helvetica', 'I', 10)
        pdf.multi_cell(0, 7, 'Baidu Silicon Valley Artificial Intelligence Lab', align='C')
        pdf.ln(5)

        # Abstract header
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, 'Abstract', ln=True)
        pdf.ln(2)

        # Abstract text
        pdf.set_font('Helvetica', '', 10)
        abstract = (
            'We show that an end-to-end deep learning approach can be used to recognize '
            'either English or Mandarin Chinese speech-two vastly different languages. '
            'Because it replaces entire pipelines of hand-engineered components with neural '
            'networks, end-to-end learning allows us to handle a diverse variety of speech '
            'including noisy environments, accents and different languages. '
            'Key to our approach is our application of HPC techniques, making it possible '
            'to train a network end-to-end from tens of thousands of hours of data. '
            'Our system achieves a word error rate better than published systems on several '
            'benchmark datasets including LibriSpeech, WSJ, and TIMIT.'
        )
        pdf.multi_cell(0, 6, abstract)
        pdf.ln(5)

        # Introduction section
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, '1. Introduction', ln=True)
        pdf.ln(2)

        pdf.set_font('Helvetica', '', 10)
        intro = (
            'We present Deep Speech 2, an updated end-to-end speech system. This work builds '
            'on Deep Speech 1, extending the model to work on both English and Mandarin speech. '
            'Our architecture uses recurrent neural networks (RNNs) trained with CTC loss to '
            'map sequences of audio spectrograms to sequences of characters. We demonstrate '
            'that deep learning can achieve high accuracy on diverse speech data without '
            'hand-engineering linguistic features.'
        )
        pdf.multi_cell(0, 6, intro)
        pdf.ln(5)

        # Architecture section
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, '2. Model Architecture', ln=True)
        pdf.ln(2)

        pdf.set_font('Helvetica', '', 10)
        arch = (
            'The Deep Speech 2 model consists of several convolutional layers followed by '
            'recurrent layers. We use Batch Normalization throughout the network which '
            'significantly speeds up training and improves final performance. The model '
            'is trained end-to-end with CTC, eliminating the need for a separate alignment '
            'step. We train our models on GPUs using data parallelism across multiple machines.'
        )
        pdf.multi_cell(0, 6, arch)
        pdf.ln(5)

        # Reference
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, 'ArXiv', ln=True)
        pdf.ln(2)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, 'https://arxiv.org/abs/1512.02595', ln=True)

        pdf.output(PDF_PATH)
        print(f'PDF created at: {PDF_PATH}')

    except ImportError:
        # Fallback: create a minimal PDF manually
        _create_minimal_pdf()


def _create_minimal_pdf():
    """Create a minimal PDF without fpdf2 (plain text encoded as PDF)."""
    content = b"""%PDF-1.4
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
/F1 14 Tf
50 750 Td
(Deep Speech 2: End-to-End Speech Recognition) Tj
0 -25 Td
/F1 10 Tf
(in English and Mandarin) Tj
0 -20 Td
(Dario Amodei, Rishita Anubhai, Eric Battenberg, Carl Case,) Tj
0 -15 Td
(Jared Casper, Bryan Catanzaro, Jingdong Chen, Mike Chrzanowski,) Tj
0 -15 Td
(Adam Coates, Greg Diamos, Erich Elsen, Jesse Engel, Linxi Fan,) Tj
0 -15 Td
(Christopher Fougner, Tony Han, Awni Hannun, Billy Jun,) Tj
0 -15 Td
(Patrick LeGresley, Libby Lin, Jitong Chen, Xu Liu, KiJung Park,) Tj
0 -15 Td
(Patrick Nguyen, Mary Power, Sameep Raju, Sherjil Ozair, Andrew Ng,) Tj
0 -15 Td
(Sharan Narang, Ziang Xie, Peng Qi) Tj
0 -25 Td
/F1 12 Tf
(Baidu Silicon Valley Artificial Intelligence Lab) Tj
0 -30 Td
/F1 10 Tf
(ArXiv: https://arxiv.org/abs/1512.02595) Tj
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
        f.write(content)
    print(f'Minimal PDF created at: {PDF_PATH}')


def setup_bookmarks_without_speech_authors():
    """Set up Chrome bookmarks WITHOUT the 'Speech Authors' folder (pre-task state)."""
    os.makedirs(CHROME_DEFAULT, exist_ok=True)

    ts = str(int(time.time() * 1_000_000))
    ts2 = str(int(time.time() * 1_000_000) + 1000)

    bookmarks = {
        'checksum': '',
        'roots': {
            'bookmark_bar': {
                'children': [],
                'date_added': ts,
                'date_modified': ts,
                'guid': 'da1acf9f-d3d8-43d7-bb73-b2e0f2c4a8b1',
                'id': '1',
                'name': 'Bookmarks bar',
                'type': 'folder'
            },
            'other': {
                'children': [],
                'date_added': ts,
                'date_modified': ts,
                'guid': 'da1acf9f-d3d8-43d7-bb73-b2e0f2c4a8b2',
                'id': '2',
                'name': 'Other bookmarks',
                'type': 'folder'
            },
            'synced': {
                'children': [],
                'date_added': ts,
                'date_modified': ts,
                'guid': 'da1acf9f-d3d8-43d7-bb73-b2e0f2c4a8b3',
                'id': '3',
                'name': 'Mobile bookmarks',
                'type': 'folder'
            }
        },
        'version': 1
    }

    with open(BOOKMARKS_FILE, 'w') as f:
        json.dump(bookmarks, f, indent=2)
    print(f'Bookmarks set up (no Speech Authors folder): {BOOKMARKS_FILE}')


def main():
    # Step 1: Kill Chrome so we can safely write config files
    kill_chrome()

    # Step 2: Create the Deep Speech 2 PDF on Desktop
    create_deep_speech2_pdf()

    # Step 3: Set up Chrome bookmarks without 'Speech Authors' folder
    setup_bookmarks_without_speech_authors()

    # Step 4: Launch Chrome with the PDF open (for the agent to see)
    # Using file:// URL to show PDF in Chrome
    launch_gui(f'google-chrome --remote-debugging-port=1337 "file://{PDF_PATH}"', delay_sec=3.0)
    print(f'GUI_READY: Chrome launched with Deep Speech 2 PDF at DISPLAY=:0')
    print('Initial state: PDF open in Chrome, no Speech Authors bookmarks folder')


main()
