"""
Initial Setup: ML Tutorial Website with PDF Downloads
Task ID: osworld_multi_apps_web_download_002
Domain: multi_apps (Chrome + OS)

Creates:
  - ~/ml_course/ directory with only chapter1.pdf
  - A local HTTP server at port 8765 serving an ML tutorial page
    with download links for chapter1.pdf through chapter8.pdf
  - Launches Chrome pointing at that local server
"""

import os
import shlex
import subprocess
import time
import textwrap
from pathlib import Path

WORKDIR = '/home/user'
ML_COURSE_DIR = f'{WORKDIR}/ml_course'
SERVER_DIR = f'{WORKDIR}/ml_tutorial_site'
SERVER_PORT = 8765
TASK_ID = 'osworld_multi_apps_web_download_002'


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


def build_pdf_bytes(chapter_num: int, title: str, summary: str) -> bytes:
    """Build a valid PDF using raw PDF syntax (no external library needed)."""
    # Truncate/sanitize text for PDF stream (only ASCII for safety)
    def safe(s):
        return s.encode('ascii', 'replace').decode('ascii')

    ch = chapter_num
    t = safe(title)
    s1 = safe(summary[:120])
    s2 = safe(summary[120:240]) if len(summary) > 120 else ""
    s3 = safe(summary[240:360]) if len(summary) > 240 else ""

    lines = [
        f"BT",
        f"/F1 20 Tf",
        f"72 720 Td",
        f"(Chapter {ch}: {t}) Tj",
        f"0 -30 Td",
        f"/F1 12 Tf",
        f"(Machine Learning Fundamentals - Study Materials) Tj",
        f"0 -40 Td",
        f"/F1 14 Tf",
        f"(Overview) Tj",
        f"0 -20 Td",
        f"/F1 10 Tf",
        f"({s1}) Tj",
    ]
    if s2:
        lines += [f"0 -15 Td", f"({s2}) Tj"]
    if s3:
        lines += [f"0 -15 Td", f"({s3}) Tj"]
    lines += [
        f"0 -40 Td",
        f"/F1 14 Tf",
        f"(Learning Objectives) Tj",
        f"0 -20 Td",
        f"/F1 10 Tf",
        f"(- Understand core concepts from Chapter {ch}.) Tj",
        f"0 -15 Td",
        f"(- Apply theory to practical ML problems.) Tj",
        f"0 -15 Td",
        f"(- Implement algorithms with Python.) Tj",
        f"0 -15 Td",
        f"(- Evaluate models with appropriate metrics.) Tj",
        f"ET",
    ]
    stream = "\n".join(lines)
    stream_bytes = stream.encode('latin-1')
    stream_len = len(stream_bytes)

    objects = []
    # obj 1: catalog
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # obj 2: pages
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    # obj 3: page
    objects.append(
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
        b"   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    )
    # obj 4: content stream
    objects.append(
        f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode('latin-1') +
        stream_bytes + b"\nendstream\nendobj\n"
    )
    # obj 5: font
    objects.append(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

    # Build xref
    header = b"%PDF-1.4\n"
    body = b""
    offsets = []
    pos = len(header)
    for obj in objects:
        offsets.append(pos)
        body += obj
        pos += len(obj)

    xref_offset = len(header) + len(body)
    xref = b"xref\n"
    xref += f"0 {len(objects)+1}\n".encode()
    xref += b"0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n".encode()

    trailer = (
        f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode()

    return header + body + xref + trailer


def create_tutorial_website():
    """Create a local web directory with an HTML tutorial page and PDF files."""
    os.makedirs(SERVER_DIR, exist_ok=True)

    chapter_data = [
        (1, "Introduction to Machine Learning",
         "This chapter provides a comprehensive introduction to machine learning, covering "
         "supervised, unsupervised, and reinforcement learning paradigms. We explore the "
         "historical context and modern applications."),
        (2, "Linear Regression and Gradient Descent",
         "Explores the foundational linear regression model and the gradient descent "
         "optimization algorithm. Covers cost functions, learning rates, and convergence."),
        (3, "Classification and Logistic Regression",
         "Introduces classification problems and the logistic regression model. Topics include "
         "decision boundaries, sigmoid function, and binary cross-entropy loss."),
        (4, "Neural Networks and Deep Learning",
         "Covers multi-layer perceptrons, backpropagation, activation functions, and the "
         "basics of deep neural network architectures."),
        (5, "Convolutional Neural Networks",
         "Focuses on CNNs for image recognition tasks. Covers convolution layers, pooling, "
         "feature maps, and popular architectures like VGG and ResNet."),
        (6, "Recurrent Neural Networks and LSTM",
         "Explores sequence modeling with RNNs and Long Short-Term Memory networks. "
         "Applications in NLP and time series forecasting."),
        (7, "Unsupervised Learning and Clustering",
         "Covers k-means clustering, hierarchical clustering, dimensionality reduction "
         "with PCA, and autoencoders."),
        (8, "Model Evaluation and Deployment",
         "Best practices for model evaluation, cross-validation, hyperparameter tuning, "
         "and deploying ML models to production environments."),
    ]

    # Create PDFs in the server directory (for download links)
    for ch_num, title, summary in chapter_data:
        pdf_path = os.path.join(SERVER_DIR, f'chapter{ch_num}.pdf')
        with open(pdf_path, 'wb') as f:
            f.write(build_pdf_bytes(ch_num, title, summary))
        print(f'  Created: {pdf_path}')

    # Build the HTML page
    chapter_rows = ""
    for ch_num, title, _ in chapter_data:
        status = "Already Downloaded" if ch_num == 1 else "Available"
        row_style = 'style="background:#f0fdf4"' if ch_num == 1 else ''
        status_style = 'style="color:#166534;background:#dcfce7;padding:3px 10px;border-radius:20px;font-size:0.82rem;font-weight:600"' if ch_num == 1 else 'style="color:#1e40af;background:#dbeafe;padding:3px 10px;border-radius:20px;font-size:0.82rem;font-weight:600"'
        chapter_rows += f"""
        <tr {row_style}>
          <td style="font-weight:600;color:#475569;padding:14px 16px">Chapter {ch_num}</td>
          <td style="padding:14px 16px;font-size:0.95rem">{title}</td>
          <td style="padding:14px 16px"><a href="/chapter{ch_num}.pdf" download="chapter{ch_num}.pdf" style="display:inline-flex;align-items:center;gap:6px;background:#2563eb;color:white;text-decoration:none;padding:7px 14px;border-radius:6px;font-size:0.87rem;font-weight:500">&#8595; Download PDF</a></td>
          <td style="padding:14px 16px"><span {status_style}>{status}</span></td>
        </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ML Fundamentals - Course Materials</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#f8fafc; color:#1e293b; line-height:1.6; margin:0; padding:0; }}
    header {{ background:linear-gradient(135deg,#1e40af 0%,#3b82f6 100%); color:white; padding:40px 0; text-align:center; }}
    header h1 {{ font-size:2.2rem; margin:0 0 8px; }}
    header p {{ font-size:1.05rem; opacity:0.85; margin:0; }}
    .container {{ max-width:900px; margin:40px auto; padding:0 20px; }}
    .notice {{ background:#fffbeb; border:1px solid #f59e0b; border-radius:8px; padding:14px 20px; margin-bottom:28px; color:#92400e; font-size:0.95rem; }}
    table {{ width:100%; border-collapse:collapse; background:white; border-radius:12px; overflow:hidden; box-shadow:0 1px 8px rgba(0,0,0,0.08); }}
    thead {{ background:#1e40af; color:white; }}
    thead th {{ padding:14px 16px; text-align:left; font-weight:600; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.04em; }}
    tbody tr {{ border-bottom:1px solid #e2e8f0; }}
    tbody tr:last-child {{ border-bottom:none; }}
    footer {{ text-align:center; color:#94a3b8; font-size:0.85rem; margin:40px 0 20px; }}
  </style>
</head>
<body>
  <header>
    <h1>Machine Learning Fundamentals</h1>
    <p>Comprehensive course materials for self-paced study</p>
  </header>
  <div class="container">
    <div class="notice">
      <strong>Note:</strong> Chapter 1 has already been downloaded to your
      <code>~/ml_course</code> folder. Please download the remaining chapters.
    </div>
    <table>
      <thead>
        <tr>
          <th>Chapter</th>
          <th>Title</th>
          <th>Download</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {chapter_rows}
      </tbody>
    </table>
  </div>
  <footer>
    <p>ML Fundamentals Course &copy; 2025 - All materials for educational use</p>
  </footer>
</body>
</html>"""

    html_path = os.path.join(SERVER_DIR, 'index.html')
    with open(html_path, 'w') as f:
        f.write(html_content)
    print(f'  Created: {html_path}')


def start_http_server():
    """Start a background HTTP server serving SERVER_DIR on SERVER_PORT."""
    # Kill any existing server on the port
    subprocess.run(
        ['pkill', '-f', f'python3.*http.server.*{SERVER_PORT}'],
        capture_output=True
    )
    time.sleep(0.5)

    subprocess.Popen(
        ['python3', '-m', 'http.server', str(SERVER_PORT), '--directory', SERVER_DIR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=SERVER_DIR,
    )
    time.sleep(1.5)
    print(f'  HTTP server started at http://localhost:{SERVER_PORT}/')


def create_initial():
    # 1. Create ml_course directory with only chapter1.pdf
    os.makedirs(ML_COURSE_DIR, exist_ok=True)
    chapter1_path = os.path.join(ML_COURSE_DIR, 'chapter1.pdf')
    with open(chapter1_path, 'wb') as f:
        f.write(build_pdf_bytes(
            1,
            "Introduction to Machine Learning",
            "This chapter provides a comprehensive introduction to machine learning, covering "
            "supervised, unsupervised, and reinforcement learning paradigms. We explore the "
            "historical context and modern applications."
        ))
    print(f'Initial file created: {chapter1_path}')

    # 2. Create the tutorial website with all 8 chapter PDFs
    print('Creating tutorial website...')
    create_tutorial_website()

    # 3. Start local HTTP server
    print('Starting HTTP server...')
    start_http_server()

    # 4. Kill any existing Chrome instances for a clean start
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    time.sleep(2.0)

    # 5. Launch Chrome pointing at the tutorial page
    tutorial_url = f'http://localhost:{SERVER_PORT}/'
    launch_gui(
        f'google-chrome --no-first-run --no-default-browser-check '
        f'"{tutorial_url}"',
        delay_sec=3.0
    )
    print(f'GUI_READY: Chrome launched with DISPLAY=:0 at {tutorial_url}')
    print(f'Initial setup complete. ml_course contains: chapter1.pdf only')


create_initial()
