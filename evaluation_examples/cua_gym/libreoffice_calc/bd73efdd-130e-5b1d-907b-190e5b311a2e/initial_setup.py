"""
Initial Setup: RLHF paper on Desktop, Chrome open with PDF
Task ID: osworld_multi_apps_bookmark_authors_002
Domain: chrome / multi-app
Initial state: PDF of Ouyang et al. 2022 on Desktop, Chrome open showing the PDF,
               no 'RLHF Researchers' bookmark folder in Bookmarks bar.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bookmark_authors_002'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/rlhf_paper.pdf'

# Chrome config paths (x86 Linux VM)
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
    """Kill any running Chrome instances before modifying Chrome files."""
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    time.sleep(2)


def create_pdf():
    """Create a realistic PDF of the RLHF paper on the Desktop."""
    os.makedirs(DESKTOP, exist_ok=True)

    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 12, 'Training language models to follow instructions', ln=True, align='C')
        pdf.cell(0, 12, 'with human feedback', ln=True, align='C')
        pdf.ln(4)

        pdf.set_font('Helvetica', '', 10)
        authors = ('Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, '
                   'Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, '
                   'John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, '
                   'Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, Ryan Lowe')
        pdf.multi_cell(0, 6, authors, align='C')
        pdf.ln(4)

        pdf.set_font('Helvetica', 'I', 10)
        pdf.cell(0, 8, 'OpenAI  —  2022', ln=True, align='C')
        pdf.ln(6)

        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, 'Abstract', ln=True)
        pdf.set_font('Helvetica', '', 10)
        abstract = (
            'Making language models bigger does not inherently make them better at following '
            'a user\'s intent. For example, large language models can generate outputs that are '
            'untruthful, toxic, or simply not helpful to the user. In other words, these models '
            'are not aligned with their users. In this paper, we show an avenue for aligning '
            'language models with user intent on a wide range of tasks by fine-tuning with human '
            'feedback. Starting with a set of labeler-written prompts and prompts submitted through '
            'the OpenAI API, we collect a dataset of labeler demonstrations of the desired model '
            'behavior, which we use to fine-tune GPT-3 using supervised learning. We then collect '
            'a dataset of rankings of model outputs, which we use to further fine-tune this '
            'supervised model using reinforcement learning from human feedback (RLHF). We call '
            'the resulting models InstructGPT. In human evaluations on our prompt distribution, '
            'outputs from the 1.3B parameter InstructGPT model are preferred to outputs from the '
            '175B GPT-3, despite having 100x fewer parameters. Moreover, InstructGPT models show '
            'improvements in truthfulness and reductions in toxic output generation while having '
            'minimal performance regressions on public NLP datasets. These results suggest that '
            'fine-tuning with human feedback is a promising direction for aligning language models '
            'with human intent.'
        )
        pdf.multi_cell(0, 5, abstract)
        pdf.ln(6)

        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, '1  Introduction', ln=True)
        pdf.set_font('Helvetica', '', 10)
        intro = (
            'Large language models (LLMs) can be "prompted" to perform a range of natural language '
            'processing (NLP) tasks. However, these models are often not aligned with what users '
            'actually want. This paper presents InstructGPT, a method using reinforcement learning '
            'from human feedback (RLHF) to align GPT-3 with human intent. Human labelers rated '
            'outputs from InstructGPT as significantly better than those from the much larger '
            'GPT-3 model, demonstrating the power of alignment techniques.'
        )
        pdf.multi_cell(0, 5, intro)

        pdf.output(PDF_PATH)
        print(f'PDF created: {PDF_PATH}')
    except ImportError:
        # Fallback: create a minimal valid PDF manually
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
<< /Length 420 >>
stream
BT
/F1 16 Tf
50 750 Td
(Training language models to follow instructions with human feedback) Tj
0 -25 Td
/F1 10 Tf
(Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright,) Tj
0 -15 Td
(Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray,) Tj
0 -15 Td
(John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens,) Tj
0 -15 Td
(Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, Ryan Lowe) Tj
0 -20 Td
(OpenAI - 2022) Tj
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
0000000274 00000 n
0000000746 00000 n

trailer
<< /Size 6 /Root 1 0 R >>
startxref
825
%%EOF"""
        with open(PDF_PATH, 'wb') as f:
            f.write(pdf_content)
        print(f'PDF created (fallback): {PDF_PATH}')


def setup_bookmarks():
    """Set up Chrome bookmarks WITHOUT the RLHF Researchers folder (initial state)."""
    os.makedirs(CHROME_DEFAULT, exist_ok=True)

    ts = str(int(time.time() * 1e6))
    bookmarks = {
        'checksum': '',
        'roots': {
            'bookmark_bar': {
                'children': [],
                'date_added': ts,
                'date_modified': ts,
                'guid': 'bookmark_bar',
                'id': '1',
                'name': 'Bookmarks bar',
                'type': 'folder'
            },
            'other': {
                'children': [],
                'date_added': ts,
                'date_modified': ts,
                'guid': 'other_bookmarks',
                'id': '2',
                'name': 'Other bookmarks',
                'type': 'folder'
            },
            'synced': {
                'children': [],
                'date_added': ts,
                'date_modified': ts,
                'guid': 'synced_bookmarks',
                'id': '3',
                'name': 'Mobile bookmarks',
                'type': 'folder'
            }
        },
        'version': 1
    }

    with open(BOOKMARKS_FILE, 'w') as f:
        json.dump(bookmarks, f, indent=2)
    print(f'Bookmarks set up (no RLHF Researchers folder): {BOOKMARKS_FILE}')


def main():
    # 1. Kill Chrome so we can safely modify its files
    kill_chrome()

    # 2. Create the PDF on the Desktop
    create_pdf()

    # 3. Set up bookmarks with NO RLHF Researchers folder
    setup_bookmarks()

    # 4. Launch Chrome with the PDF open (using file:// URL)
    #    Chrome opens the PDF in-browser which lets the agent read it
    pdf_url = f'file://{PDF_PATH}'
    launch_gui(f'google-chrome --remote-debugging-port=1337 "{pdf_url}"', delay_sec=3.0)
    print(f'GUI_READY: Chrome opened with PDF at {pdf_url}')


main()
