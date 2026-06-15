"""
Initial Setup: Expand selection in nested HTML using VSCode
Task ID: vscode_edit_035
Domain: vs_code

Creates ~/Desktop/template.html (60-line HTML file) with:
  - Line 20: <div class="content">  (opening tag)
  - Line 25: <span class="highlight"> inside <p> inside <div class="content">  (cursor target)
  - Line 35: </div>                 (closing tag)
Opens VSCode with cursor on line 25 col 20 (inside the span text).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_035'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/template.html'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # 60-line HTML file:
    #   Lines  1-19: DOCTYPE, head, body open, header section
    #   Line  20: <div class="content">         (opening tag)
    #   Line  21: <h2 class="section-title">
    #   Line  22: <p class="intro-text">
    #   Line  23: <p class="description"> opening
    #   Line  24:   "Our curated collection features"
    #   Line  25:   <span class="highlight">latest arrivals</span>  ← cursor here
    #   Line  26:   "from leading manufacturers."
    #   Line  27: </p>
    #   Line  28: <ul class="product-list">
    #   Line  29-33: five <li> items
    #   Line  34: </ul>
    #   Line  35: </div>                        (closing tag)
    #   Lines 36-60: promotions, sidebar, main, footer
    html_content = (
        '<!DOCTYPE html>\n'                                                   # 1
        '<html lang="en">\n'                                                  # 2
        '<head>\n'                                                            # 3
        '    <meta charset="UTF-8">\n'                                        # 4
        '    <meta name="viewport" content="width=device-width">\n'           # 5
        '    <title>Product Catalog - TechShop</title>\n'                     # 6
        '    <link rel="stylesheet" href="styles.css">\n'                     # 7
        '    <script src="app.js" defer></script>\n'                          # 8
        '</head>\n'                                                           # 9
        '<body>\n'                                                            # 10
        '    <header class="site-header">\n'                                  # 11
        '        <nav><a href="/" class="logo">TechShop</a>\n'                # 12
        '            <ul>\n'                                                  # 13
        '                <li><a href="/products">Products</a></li>\n'         # 14
        '                <li><a href="/about">About</a></li>\n'               # 15
        '                <li><a href="/contact">Contact</a></li>\n'           # 16
        '            </ul>\n'                                                 # 17
        '        </nav>\n'                                                    # 18
        '    </header>\n'                                                     # 19
        '    <div class="content">\n'                                         # 20
        '        <h2 class="section-title">Featured Products</h2>\n'          # 21
        '        <p class="intro-text">Browse our top-rated items.</p>\n'     # 22
        '        <p class="description">Our curated collection\n'             # 23
        '            features the best products including\n'                  # 24
        '            <span class="highlight">latest arrivals</span>\n'        # 25
        '            from leading tech manufacturers.\n'                      # 26
        '        </p>\n'                                                      # 27
        '        <ul class="product-list">\n'                                 # 28
        '            <li>Wireless Headphones - $89.99</li>\n'                 # 29
        '            <li>Mechanical Keyboard - $129.99</li>\n'                # 30
        '            <li>USB-C Hub - $45.00</li>\n'                           # 31
        '            <li>Webcam HD Pro - $65.00</li>\n'                       # 32
        '            <li>Smart Mouse - $39.99</li>\n'                         # 33
        '        </ul>\n'                                                     # 34
        '    </div>\n'                                                        # 35
        '    <section class="promotions">\n'                                  # 36
        '        <h3>Current Promotions</h3>\n'                               # 37
        '        <p>Save up to 30% on selected items this week.</p>\n'        # 38
        '        <ul>\n'                                                      # 39
        '            <li>Buy 2 accessories, get 1 free</li>\n'                # 40
        '            <li>Members get early access to new arrivals</li>\n'     # 41
        '        </ul>\n'                                                     # 42
        '    </section>\n'                                                    # 43
        '    <aside class="sidebar">\n'                                       # 44
        '        <h4>Categories</h4>\n'                                       # 45
        '        <ul class="category-list">\n'                                # 46
        '            <li><a href="/audio">Audio</a></li>\n'                   # 47
        '            <li><a href="/peripherals">Peripherals</a></li>\n'       # 48
        '            <li><a href="/accessories">Accessories</a></li>\n'       # 49
        '        </ul>\n'                                                     # 50
        '    </aside>\n'                                                      # 51
        '    <main class="extra-content">\n'                                  # 52
        '        <article>\n'                                                 # 53
        '            <h5>Editor\'s Pick This Month</h5>\n'                    # 54
        '            <p>Top pick: Wireless Headphones Pro.</p>\n'             # 55
        '        </article>\n'                                                # 56
        '    </main>\n'                                                       # 57
        '    <footer class="site-footer">\n'                                  # 58
        '        <p>&copy; 2025 TechShop.</p></footer>\n'                     # 59
        '</body></html>\n'                                                    # 60
    )

    with open(OUTPUT, 'w') as f:
        f.write(html_content)
    print(f'Initial file created: {OUTPUT}')

    # Verify structure
    with open(OUTPUT, 'r') as f:
        file_lines = f.readlines()
    total_lines = len(file_lines)
    print(f'Total lines: {total_lines}')
    print(f'Line 20: {file_lines[19].rstrip()}')
    print(f'Line 25: {file_lines[24].rstrip()}')
    print(f'Line 35: {file_lines[34].rstrip()}')

    # Open VSCode with the file, cursor on line 25 col 20
    # (inside <span class="highlight">latest arrivals</span> text)
    launch_gui(f'code --goto "{OUTPUT}:25:20"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0, cursor at line 25:20')


create_initial()
