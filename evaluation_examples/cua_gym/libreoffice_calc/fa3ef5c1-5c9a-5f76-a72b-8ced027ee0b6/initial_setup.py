"""
Initial Setup: Web download task - download API spec PDFs from documentation page
Task ID: osworld_multi_apps_web_download_005
Domain: multi_apps (Chrome + OS)

Sets up:
  - ~/api_docs/ directory (empty - target download folder)
  - ~/api_pdfs/ directory with real PDF spec files to be served
  - A local HTTP server (port 8765) serving the docs HTML + PDF files
  - Chrome open on the documentation page listing the PDF download links
"""

import os
import shlex
import subprocess
import time
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_download_005'
API_DOCS_DIR = f'{WORKDIR}/api_docs'
API_PDFS_DIR = f'{WORKDIR}/api_pdfs'
HTML_DIR = f'{WORKDIR}/api_site'
SERVER_PORT = 8765
SERVER_URL = f'http://localhost:{SERVER_PORT}/index.html'


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


def create_pdf_with_python(output_path: str, title: str, version: str, content_lines: list):
    """Create a realistic-looking API spec PDF using fpdf2."""
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_margins(25, 25, 25)
        pdf.add_page()
        # Use explicit width to avoid fpdf2 width-calculation bug after draw operations
        W = 160  # 210 - 25 - 25 mm

        # Title
        pdf.set_font('Helvetica', 'B', 18)
        pdf.set_text_color(30, 80, 160)
        pdf.multi_cell(W, 12, title, align='L')
        pdf.ln(2)

        # Version line
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(W, 8, f'Version: {version}   |   Confidential & Internal Use Only', align='L')
        pdf.ln(4)

        # Separator line
        pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(0.5)
        pdf.line(25, pdf.get_y(), 185, pdf.get_y())
        pdf.ln(5)

        # Section: Overview
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(30, 80, 160)
        pdf.multi_cell(W, 9, '1. Overview')
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(W, 6,
            f'This document describes the specification for the {title}. '
            f'It provides a comprehensive reference for developers integrating with this API, '
            f'including endpoint definitions, authentication schemes, request/response formats, '
            f'and error handling guidelines.')
        pdf.ln(3)

        # Section: Endpoints
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(30, 80, 160)
        pdf.multi_cell(W, 9, '2. API Endpoints')
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(50, 50, 50)
        for line in content_lines:
            pdf.multi_cell(W, 6, line)
        pdf.ln(3)

        # Section: Authentication
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(30, 80, 160)
        pdf.multi_cell(W, 9, '3. Authentication')
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(W, 6,
            'All requests must include a Bearer token in the Authorization header. '
            'Tokens are issued via the /auth/token endpoint with a valid API key. '
            'Tokens expire after 3600 seconds and must be refreshed using the refresh endpoint.')
        pdf.ln(3)

        # Section: Error Codes
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(30, 80, 160)
        pdf.multi_cell(W, 9, '4. Error Codes')
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(40, 40, 40)
        errors = [
            '400 Bad Request    - Invalid request parameters or missing required fields.',
            '401 Unauthorized   - Missing or invalid authentication token.',
            '403 Forbidden      - Authenticated but insufficient permissions.',
            '404 Not Found      - The requested resource does not exist.',
            '429 Too Many Req.  - Rate limit exceeded. Retry after the indicated delay.',
            '500 Server Error   - Unexpected server-side error.',
        ]
        for error_line in errors:
            pdf.multi_cell(W, 6, error_line)

        # Footer
        pdf.set_y(-20)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.multi_cell(W, 5,
            f'Acme Software Inc. - {title} - {version} - Generated 2025-03-01',
            align='L')

        pdf.output(output_path)
        return True
    except Exception as e:
        print(f'fpdf2 PDF creation failed: {e}', file=sys.stderr)
        return False


def create_minimal_pdf(output_path: str, title: str):
    """Fallback: create a minimal but valid PDF using raw bytes."""
    content = f'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'
    content += f'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n'
    content += f'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n'
    content += f'   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n'
    stream_text = f'BT /F1 16 Tf 72 720 Td ({title}) Tj ET'
    content += f'4 0 obj\n<< /Length {len(stream_text)} >>\nstream\n{stream_text}\nendstream\nendobj\n'
    content += f'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n'
    content += f'xref\n0 6\n0000000000 65535 f \n'
    offsets = []
    pos = 0
    for obj_content in content.split('\n'):
        pos += len(obj_content) + 1
    content += f'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{len(content)}\n%%EOF\n'
    with open(output_path, 'w') as f:
        f.write(content)


def create_api_pdfs():
    """Create realistic API spec PDF files in api_pdfs directory."""
    os.makedirs(API_PDFS_DIR, exist_ok=True)

    specs = [
        {
            'filename': 'api_v1_spec.pdf',
            'title': 'Acme API v1 Specification',
            'version': '1.0.3',
            'endpoints': [
                'GET    /v1/users            - List all users',
                'POST   /v1/users            - Create a new user',
                'GET    /v1/users/{id}       - Get user by ID',
                'PUT    /v1/users/{id}       - Update user by ID',
                'DELETE /v1/users/{id}       - Delete user by ID',
                'GET    /v1/products         - List all products',
                'POST   /v1/products         - Create a new product',
                'GET    /v1/products/{id}    - Get product by ID',
                'GET    /v1/orders           - List all orders',
                'POST   /v1/orders           - Create a new order',
            ],
        },
        {
            'filename': 'api_v2_spec.pdf',
            'title': 'Acme API v2 Specification',
            'version': '2.1.0',
            'endpoints': [
                'GET    /v2/users            - List users with pagination',
                'POST   /v2/users            - Create user with validation',
                'GET    /v2/users/{uuid}     - Get user by UUID',
                'PATCH  /v2/users/{uuid}     - Partial update user',
                'DELETE /v2/users/{uuid}     - Soft-delete user',
                'GET    /v2/products         - List products with filters',
                'POST   /v2/products         - Create product with inventory',
                'GET    /v2/products/{sku}   - Get product by SKU',
                'GET    /v2/orders           - List orders with status filter',
                'POST   /v2/orders           - Create order with line items',
                'GET    /v2/analytics        - Get usage analytics summary',
            ],
        },
        {
            'filename': 'api_v3_spec.pdf',
            'title': 'Acme API v3 Specification',
            'version': '3.0.0-beta',
            'endpoints': [
                'GET    /v3/users            - List users (GraphQL-compatible)',
                'POST   /v3/users            - Create user with profile',
                'GET    /v3/users/{id}       - Get user with relations',
                'PATCH  /v3/users/{id}       - Update user fields',
                'DELETE /v3/users/{id}       - Archive user record',
                'GET    /v3/products         - List products with variants',
                'POST   /v3/products         - Create product bundle',
                'GET    /v3/products/{id}    - Get product with metadata',
                'GET    /v3/orders           - List orders with events',
                'POST   /v3/orders           - Place order with webhook',
                'GET    /v3/analytics/live   - Real-time analytics stream',
                'POST   /v3/webhooks         - Register event webhooks',
            ],
        },
    ]

    for spec in specs:
        out_path = os.path.join(API_PDFS_DIR, spec['filename'])
        success = create_pdf_with_python(out_path, spec['title'], spec['version'], spec['endpoints'])
        if not success:
            create_minimal_pdf(out_path, spec['title'])
        if os.path.exists(out_path):
            print(f'  Created PDF: {out_path} ({os.path.getsize(out_path)} bytes)')
        else:
            print(f'  ERROR: Failed to create {out_path}', file=sys.stderr)


def create_html_page():
    """Create the API documentation HTML page with download links."""
    os.makedirs(HTML_DIR, exist_ok=True)

    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Acme Software — API Documentation</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f4f6f9;
      color: #333;
    }
    header {
      background: linear-gradient(135deg, #1e4fa0, #2d6cc0);
      color: white;
      padding: 28px 40px;
    }
    header h1 { font-size: 26px; font-weight: 700; margin-bottom: 6px; }
    header p  { font-size: 14px; opacity: 0.85; }
    .container { max-width: 900px; margin: 36px auto; padding: 0 24px; }
    .intro {
      background: white;
      border-radius: 8px;
      padding: 24px 28px;
      margin-bottom: 28px;
      border: 1px solid #dde3ec;
      font-size: 14px;
      line-height: 1.7;
      color: #555;
    }
    .intro strong { color: #222; }
    h2 {
      font-size: 18px;
      font-weight: 700;
      color: #1e4fa0;
      margin-bottom: 16px;
    }
    .spec-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 18px;
      margin-bottom: 36px;
    }
    .spec-card {
      background: white;
      border-radius: 8px;
      border: 1px solid #dde3ec;
      padding: 20px 22px;
      transition: box-shadow 0.15s;
    }
    .spec-card:hover { box-shadow: 0 4px 16px rgba(30,79,160,0.12); }
    .spec-card .badge {
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.04em;
      padding: 3px 9px;
      border-radius: 12px;
      margin-bottom: 10px;
    }
    .badge-v1 { background: #e8f0fe; color: #1e4fa0; }
    .badge-v2 { background: #e6f4ea; color: #1a7340; }
    .badge-v3 { background: #fef3c7; color: #92400e; }
    .spec-card h3 { font-size: 15px; font-weight: 700; color: #222; margin-bottom: 6px; }
    .spec-card p  { font-size: 12px; color: #777; margin-bottom: 14px; line-height: 1.5; }
    .download-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #1e4fa0;
      color: white;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 6px;
      transition: background 0.15s;
    }
    .download-btn:hover { background: #163c80; }
    .download-btn svg { width: 14px; height: 14px; fill: white; }
    footer {
      text-align: center;
      padding: 24px;
      font-size: 12px;
      color: #999;
      border-top: 1px solid #e5e7eb;
      margin-top: 16px;
    }
  </style>
</head>
<body>
  <header>
    <h1>Acme Software — Developer Portal</h1>
    <p>API Documentation &amp; Specification Downloads</p>
  </header>

  <div class="container">
    <div class="intro">
      <strong>Welcome to the Acme API Documentation Hub.</strong>
      This page provides downloadable PDF specification sheets for each version of the Acme REST API.
      Each spec sheet includes full endpoint listings, authentication requirements, request/response
      schemas, and error code references. Download the spec(s) relevant to your integration target.
    </div>

    <h2>Available API Spec Sheets</h2>

    <div class="spec-grid">

      <div class="spec-card">
        <span class="badge badge-v1">Version 1</span>
        <h3>Acme API v1 Specification</h3>
        <p>The original REST API (v1.0.3). Covers core user, product, and order
           endpoints. Suitable for legacy integrations.</p>
        <a class="download-btn" href="api_v1_spec.pdf" download="api_v1_spec.pdf">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 9h-4V3H9v6H5l7 7 7-7zm-7 10H5v2h14v-2h-7z"/>
          </svg>
          Download PDF
        </a>
      </div>

      <div class="spec-card">
        <span class="badge badge-v2">Version 2</span>
        <h3>Acme API v2 Specification</h3>
        <p>Major revision (v2.1.0) with UUID-based identifiers, pagination,
           partial updates (PATCH), and analytics endpoints.</p>
        <a class="download-btn" href="api_v2_spec.pdf" download="api_v2_spec.pdf">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 9h-4V3H9v6H5l7 7 7-7zm-7 10H5v2h14v-2h-7z"/>
          </svg>
          Download PDF
        </a>
      </div>

      <div class="spec-card">
        <span class="badge badge-v3">Version 3 (Beta)</span>
        <h3>Acme API v3 Specification</h3>
        <p>Next-generation API (v3.0.0-beta) with GraphQL compatibility,
           webhook support, and real-time analytics streaming.</p>
        <a class="download-btn" href="api_v3_spec.pdf" download="api_v3_spec.pdf">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 9h-4V3H9v6H5l7 7 7-7zm-7 10H5v2h14v-2h-7z"/>
          </svg>
          Download PDF
        </a>
      </div>

    </div>
  </div>

  <footer>
    &copy; 2025 Acme Software Inc. &mdash; All rights reserved.
    For support, contact <strong>developer-support@acmesoftware.example.com</strong>
  </footer>
</body>
</html>
'''
    html_path = os.path.join(HTML_DIR, 'index.html')
    with open(html_path, 'w') as f:
        f.write(html_content)
    print(f'HTML page created: {html_path}')


def symlink_pdfs_into_site():
    """Symlink/copy PDFs into the HTML serving directory so relative links work."""
    for fname in ['api_v1_spec.pdf', 'api_v2_spec.pdf', 'api_v3_spec.pdf']:
        src = os.path.join(API_PDFS_DIR, fname)
        dst = os.path.join(HTML_DIR, fname)
        if os.path.exists(dst):
            os.remove(dst)
        import shutil
        shutil.copy2(src, dst)
        print(f'  Copied {fname} into site dir')


def kill_existing_server():
    """Kill any existing HTTP server on our port."""
    subprocess.run(
        f'fuser -k {SERVER_PORT}/tcp 2>/dev/null || true',
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(0.5)


def start_http_server():
    """Start a background HTTP server to serve the API docs site."""
    kill_existing_server()

    server_script = f'''
import http.server, os, sys
os.chdir("{HTML_DIR}")
handler = http.server.SimpleHTTPRequestHandler
handler.log_message = lambda *a: None  # suppress access logs
server = http.server.HTTPServer(("0.0.0.0", {SERVER_PORT}), handler)
server.serve_forever()
'''
    server_script_path = f'{WORKDIR}/.api_site_server.py'
    with open(server_script_path, 'w') as f:
        f.write(server_script)

    env = os.environ.copy()
    subprocess.Popen(
        [sys.executable, server_script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(1.5)
    print(f'HTTP server started on port {SERVER_PORT}')


def setup_chrome_download_dir():
    """Configure Chrome to download files to ~/api_docs by default."""
    chrome_prefs_path = os.path.expanduser('~/.config/google-chrome/Default/Preferences')
    if not os.path.exists(chrome_prefs_path):
        print('Chrome Preferences not found, skipping download dir config')
        return

    import json
    try:
        with open(chrome_prefs_path, 'r') as f:
            prefs = json.load(f)
        # Set default download directory and disable prompt
        prefs.setdefault('download', {})
        prefs['download']['default_directory'] = API_DOCS_DIR
        prefs['download']['prompt_for_download'] = False
        prefs['download']['directory_upgrade'] = True
        prefs.setdefault('savefile', {})
        prefs['savefile']['default_directory'] = API_DOCS_DIR
        with open(chrome_prefs_path, 'w') as f:
            json.dump(prefs, f, indent=2)
        print(f'Chrome download directory set to: {API_DOCS_DIR}')
    except Exception as e:
        print(f'Warning: Could not configure Chrome download dir: {e}', file=sys.stderr)


def kill_chrome():
    """Kill any running Chrome instance before modifying prefs."""
    subprocess.run('pkill -f google-chrome 2>/dev/null || true',
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('pkill -f chromium 2>/dev/null || true',
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2.0)


def create_initial():
    print('=== Creating initial state for osworld_multi_apps_web_download_005 ===')

    # 1. Create ~/api_docs/ directory (empty - target for downloads)
    os.makedirs(API_DOCS_DIR, exist_ok=True)
    print(f'Created empty download target: {API_DOCS_DIR}')

    # 2. Create PDF spec files
    print('Creating API spec PDF files...')
    create_api_pdfs()

    # 3. Create HTML documentation page
    print('Creating HTML documentation page...')
    create_html_page()

    # 4. Copy PDFs alongside HTML so relative links work
    print('Setting up site files...')
    symlink_pdfs_into_site()

    # 5. Kill Chrome before modifying prefs
    print('Stopping any running Chrome...')
    kill_chrome()

    # 6. Configure Chrome download directory
    print('Configuring Chrome download directory...')
    setup_chrome_download_dir()

    # 7. Start local HTTP server
    print('Starting local HTTP server...')
    start_http_server()

    # 8. Launch Chrome with the documentation page open
    print(f'Launching Chrome on {SERVER_URL} ...')
    launch_gui(
        f'google-chrome --no-first-run --no-default-browser-check '
        f'--disable-extensions-except --start-maximized '
        f'"{SERVER_URL}"',
        delay_sec=3.0
    )

    # Verify key artifacts
    print('\n=== Verification ===')
    print(f'api_docs dir exists: {os.path.isdir(API_DOCS_DIR)}')
    print(f'api_docs contents: {os.listdir(API_DOCS_DIR)}')
    pdf_files = ['api_v1_spec.pdf', 'api_v2_spec.pdf', 'api_v3_spec.pdf']
    for fname in pdf_files:
        path = os.path.join(HTML_DIR, fname)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        print(f'  {fname}: {"OK" if size > 0 else "MISSING"} ({size} bytes)')

    print(f'\nGUI_READY: Chrome launched with DISPLAY=:0 pointing to {SERVER_URL}')
    print('Initial state: ~/api_docs/ is empty; PDFs are served at localhost:8765')


create_initial()
