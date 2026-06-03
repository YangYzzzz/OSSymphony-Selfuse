"""
Initial Setup: Multi-Agent Paper Bookmark Task
Task ID: osworld_multi_apps_bookmark_authors_012
Domain: chrome (multi-app: PDF + Chrome bookmarks)

Sets up:
1. PDF of 'Emergent Tool Use From Multi-Agent Autocurricula' (Baker et al., 2020) on Desktop
2. Chrome open with the PDF loaded
3. Clean Chrome bookmarks (NO 'Multi-Agent Team' folder — that's the task)
4. No bookmarks_screenshot.png on Desktop
"""

import os
import json
import shlex
import subprocess
import time
import shutil

# ---------- paths ----------
HOME = '/home/user'
DESKTOP = os.path.join(HOME, 'Desktop')
TASK_ID = 'osworld_multi_apps_bookmark_authors_012'
PDF_PATH = os.path.join(DESKTOP, 'emergent_tool_use_multi_agent.pdf')

CHROME_USER_DATA = os.path.join(HOME, '.config/google-chrome')
CHROME_DEFAULT = os.path.join(CHROME_USER_DATA, 'Default')
BOOKMARKS_FILE = os.path.join(CHROME_DEFAULT, 'Bookmarks')

# ---------- helper ----------
def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking."""
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
    """Kill any running Chrome/Chromium instances."""
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chromium'], capture_output=True)
    time.sleep(2)


def create_pdf():
    """Create a realistic-looking PDF of the Baker et al. 2020 paper."""
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove stale screenshot if present (should not exist in initial state)
    screenshot_path = os.path.join(DESKTOP, 'bookmarks_screenshot.png')
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)

    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # --- Page 1: Title page ---
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_xy(20, 30)
        pdf.multi_cell(170, 8, 'Emergent Tool Use From Multi-Agent Autocurricula', align='C')

        pdf.set_font('Helvetica', '', 12)
        pdf.set_xy(20, 55)
        pdf.multi_cell(170, 7,
            'Bowen Baker*, Ingmar Kanitscheider*, Todor Markov, Yi Wu,\n'
            'Glenn Powell, Bob McGrew, Igor Mordatch',
            align='C')

        pdf.set_font('Helvetica', 'I', 11)
        pdf.set_xy(20, 80)
        pdf.multi_cell(170, 7, 'OpenAI\nPublished at ICLR 2020', align='C')

        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_xy(20, 100)
        pdf.cell(170, 7, 'Abstract', align='L')

        pdf.set_font('Helvetica', '', 10)
        pdf.set_xy(20, 110)
        pdf.multi_cell(170, 6,
            'We study the emergence of complex skills in a multi-agent hide-and-seek '
            'environment. We find that through multi-agent competition, agents develop '
            'increasingly sophisticated strategies including tool use and collaborative '
            'coordination. Starting from simple locomotion, agents learn to use movable '
            'boxes and ramps as tools to gain positional advantages over opponents. '
            'These emergent behaviors arise without any explicit reward for tool use; '
            'the only reward signal comes from the competitive hide-and-seek game itself. '
            'Our results demonstrate that autocurricula induced by multi-agent competition '
            'can lead to the emergence of complex, human-relevant behaviors and skills.',
            align='J')

        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_xy(20, 185)
        pdf.cell(170, 7, '1  Introduction', align='L')

        pdf.set_font('Helvetica', '', 10)
        pdf.set_xy(20, 195)
        pdf.multi_cell(170, 6,
            'One of the long-standing goals of artificial intelligence is to develop '
            'agents that can learn to use tools and develop complex strategies without '
            'explicit programming. In this paper, we demonstrate that such capabilities '
            'can emerge naturally from multi-agent competition in physically simulated '
            'environments. We introduce a hide-and-seek environment where hiders must '
            'evade seekers in a 3D physics simulation, and show that over the course '
            'of training, both teams develop increasingly sophisticated strategies.',
            align='J')

        # --- Page 2: Method ---
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_xy(20, 20)
        pdf.cell(170, 7, '2  Environment and Methods', align='L')

        pdf.set_font('Helvetica', '', 10)
        pdf.set_xy(20, 30)
        pdf.multi_cell(170, 6,
            'The environment consists of a bounded arena with movable boxes and ramps. '
            'Hiders are rewarded for not being seen by seekers, while seekers are rewarded '
            'for observing at least one hider. Both teams are trained using Proximal Policy '
            'Optimization (PPO) with centralized value functions and decentralized policies. '
            'Agents observe their local surroundings through a combination of proprioceptive '
            'information and a limited field of view.',
            align='J')

        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_xy(20, 90)
        pdf.cell(170, 7, '3  Results', align='L')

        pdf.set_font('Helvetica', '', 10)
        pdf.set_xy(20, 100)
        pdf.multi_cell(170, 6,
            'Training proceeds through several distinct phases of emergent behavior:\n'
            '  Phase 1 (0-25M steps): Agents develop basic locomotion and collision avoidance.\n'
            '  Phase 2 (25-75M steps): Hiders learn to use boxes to block doorways.\n'
            '  Phase 3 (75-150M steps): Seekers learn to use ramps to overcome barriers.\n'
            '  Phase 4 (150-200M steps): Hiders learn to move ramps away from seekers.\n'
            '  Phase 5 (200M+ steps): Seekers learn to "surf" on boxes to bypass defenses.\n\n'
            'These results demonstrate six distinct emergent behaviors arising purely '
            'from competitive pressure, without any explicit reward shaping.',
            align='J')

        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_xy(20, 185)
        pdf.cell(170, 7, 'References', align='L')

        pdf.set_font('Helvetica', '', 9)
        pdf.set_xy(20, 195)
        pdf.multi_cell(170, 5,
            '[1] Baker, B., Kanitscheider, I., Markov, T., Wu, Y., Powell, G., McGrew, B., '
            '& Mordatch, I. (2020). Emergent tool use from multi-agent autocurricula. '
            'International Conference on Learning Representations (ICLR 2020).\n\n'
            '[2] Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. (2017). '
            'Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347.\n\n'
            '[3] Mordatch, I., & Abbeel, P. (2018). Emergence of grounded compositional '
            'language in multi-agent populations. AAAI Conference on Artificial Intelligence.',
            align='L')

        pdf.output(PDF_PATH)
        print(f'PDF created: {PDF_PATH}')

    except ImportError:
        # Fallback: create a minimal valid PDF manually
        print('fpdf2 not available, creating minimal PDF...')
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
<< /Length 400 >>
stream
BT
/F1 16 Tf
50 720 Td
(Emergent Tool Use From Multi-Agent Autocurricula) Tj
0 -30 Td
/F1 12 Tf
(Bowen Baker, Ingmar Kanitscheider, Todor Markov, Yi Wu,) Tj
0 -18 Td
(Glenn Powell, Bob McGrew, Igor Mordatch) Tj
0 -18 Td
(OpenAI  -  ICLR 2020) Tj
0 -40 Td
/F1 11 Tf
(Abstract) Tj
0 -18 Td
/F1 10 Tf
(We study the emergence of complex skills in a multi-agent environment.) Tj
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
0000000718 00000 n

trailer
<< /Size 6 /Root 1 0 R >>
startxref
800
%%EOF"""
        with open(PDF_PATH, 'wb') as f:
            f.write(pdf_content)
        print(f'Minimal PDF created: {PDF_PATH}')


def setup_bookmarks():
    """Set up clean Chrome bookmarks without Multi-Agent Team folder."""
    os.makedirs(CHROME_DEFAULT, exist_ok=True)

    ts = str(int(time.time() * 1_000_000))

    bookmarks = {
        "checksum": "",
        "roots": {
            "bookmark_bar": {
                "children": [
                    {
                        "date_added": ts,
                        "date_last_used": "0",
                        "guid": "00000000-0000-4000-a000-000000000001",
                        "id": "6",
                        "name": "Gmail",
                        "type": "url",
                        "url": "https://mail.google.com/mail/u/0/"
                    },
                    {
                        "date_added": ts,
                        "date_last_used": "0",
                        "guid": "00000000-0000-4000-a000-000000000002",
                        "id": "7",
                        "name": "Google Drive",
                        "type": "url",
                        "url": "https://drive.google.com/drive/"
                    },
                    {
                        "date_added": ts,
                        "date_last_used": "0",
                        "guid": "00000000-0000-4000-a000-000000000003",
                        "id": "8",
                        "name": "YouTube",
                        "type": "url",
                        "url": "https://www.youtube.com/"
                    }
                ],
                "date_added": ts,
                "date_modified": ts,
                "guid": "00000000-0000-4000-a000-000000000010",
                "id": "1",
                "name": "Bookmarks bar",
                "type": "folder"
            },
            "other": {
                "children": [],
                "date_added": ts,
                "date_modified": "0",
                "guid": "00000000-0000-4000-a000-000000000020",
                "id": "2",
                "name": "Other bookmarks",
                "type": "folder"
            },
            "synced": {
                "children": [],
                "date_added": ts,
                "date_modified": "0",
                "guid": "00000000-0000-4000-a000-000000000030",
                "id": "3",
                "name": "Mobile bookmarks",
                "type": "folder"
            }
        },
        "version": 1
    }

    with open(BOOKMARKS_FILE, 'w') as f:
        json.dump(bookmarks, f, indent=2)
    print(f'Bookmarks configured (no Multi-Agent Team folder): {BOOKMARKS_FILE}')


def main():
    # 1. Kill Chrome so we can safely modify its files
    kill_chrome()

    # 2. Create the PDF on Desktop
    create_pdf()

    # 3. Set up clean bookmarks (no Multi-Agent Team folder)
    setup_bookmarks()

    # 4. Launch Chrome with the PDF open so agent can see it
    #    Use google-chrome with remote debugging enabled
    chrome_cmd = f'google-chrome --no-first-run --no-default-browser-check "{PDF_PATH}"'
    launch_gui(chrome_cmd, delay_sec=3.0)
    print('GUI_READY: Chrome launched with PDF open on DISPLAY=:0')

    print(f'\nInitial state ready:')
    print(f'  PDF: {PDF_PATH}')
    print(f'  Bookmarks: clean (no Multi-Agent Team folder)')
    print(f'  Chrome: open with PDF')


main()
