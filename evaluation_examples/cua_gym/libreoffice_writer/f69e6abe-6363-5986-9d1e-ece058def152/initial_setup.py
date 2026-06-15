"""
Initial Setup: Open a saved version of a document for side-by-side reference
Task ID: writer_lec_092
Domain: libreoffice_writer

Creates an ODT document with 5 saved versions, version 3 labeled 'Approved draft'.
Opens the document in LibreOffice Writer.

Strategy:
1. Create ODT from text via soffice --convert-to (native ODF)
2. Open in LO with UNO socket listener
3. For each version: dispatch .uno:VersionDialog, click Save New Version
   via xdotool mouse click, type comment, Alt+O to confirm, Escape to close
4. Restart LO without listener for GUI-ready state
"""

import os
import subprocess
import shlex
import time
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_092'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def kill_lo():
    subprocess.run(['killall', '-9', 'soffice.bin', 'oosplash'], capture_output=True)
    time.sleep(3)


def shell(cmd, timeout=120):
    """Run shell command on the VM with DISPLAY=:0."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        timeout=timeout, env=env
    )
    return result.stdout.strip()


def clean_recovery():
    reg_file = os.path.expanduser(
        '~/.config/libreoffice/4/user/registrymodifications.xcu'
    )
    if os.path.exists(reg_file):
        with open(reg_file, 'r') as fh:
            content = fh.read()
        content = re.sub(
            r'<item[^>]*Recovery[^>]*>.*?</item>', '', content, flags=re.DOTALL
        )
        with open(reg_file, 'w') as fh:
            fh.write(content)


def create_base_document():
    """Create base ODT document from plain text via LO headless conversion."""
    txt_file = f'{WORKDIR}/_temp_content.txt'
    content = """Quarterly Performance Review - Q4 2025

Prepared by: Regional Operations Division
Date: December 15, 2025

1. Executive Summary

The fourth quarter of 2025 demonstrated strong growth across all key performance indicators. Revenue increased by 18.3% compared to Q3, driven primarily by expansion in the Southeast Asian market and the successful launch of our premium service tier.

2. Financial Performance

Total revenue for Q4 reached $4.72 million, exceeding our projected target of $4.15 million by 13.7%. Operating expenses remained within budget at $2.89 million, resulting in an operating margin of 38.8%.

Key financial highlights:
- Gross profit margin: 62.4% (up from 58.1% in Q3)
- Customer acquisition cost: $127 (down from $143)
- Average revenue per user: $89.50 (up from $76.20)

3. Market Analysis

Our market share in the enterprise segment grew from 12.4% to 15.7%, positioning us as the third-largest provider in the industry. The competitive landscape shifted significantly with the merger of TechCore Solutions and DataBridge Inc., creating a formidable competitor with combined annual revenue exceeding $12 billion.

4. Operational Highlights

The engineering team completed the migration to the new cloud infrastructure ahead of schedule. System uptime improved to 99.97%, and average response time decreased by 34%. The customer support team reduced average resolution time from 4.2 hours to 2.8 hours.

5. Recommendations

Based on the Q4 results, we recommend the following strategic initiatives for Q1 2026:
1. Accelerate expansion into the Latin American market
2. Increase R&D investment by 25% to maintain competitive edge
3. Launch customer loyalty program targeting high-value accounts
4. Hire 15 additional engineers for the platform team"""

    with open(txt_file, 'w') as f:
        f.write(content)

    shell(f'soffice --headless --norestore --convert-to odt --outdir {WORKDIR} {txt_file}', timeout=60)
    time.sleep(2)

    converted = txt_file.replace('.txt', '.odt')
    if os.path.exists(converted):
        if os.path.exists(OUTPUT):
            os.remove(OUTPUT)
        os.rename(converted, OUTPUT)
        print(f"Base ODT created: {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")
    else:
        print("ERROR: Conversion failed")
        return False

    os.remove(txt_file)
    kill_lo()
    return True


def add_version_via_shell(comment):
    """
    Add a single version by dispatching VersionDialog via UNO and
    interacting with the dialog via xdotool shell commands.
    """
    # UNO Python snippet to dispatch VersionDialog (runs in background)
    uno_snippet = """
import uno, threading, time
lc = uno.getComponentContext()
r = lc.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', lc)
ctx = r.resolve('uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
sm = ctx.ServiceManager
dt = sm.createInstanceWithContext('com.sun.star.frame.Desktop', ctx)
doc = dt.getCurrentComponent()
fr = doc.getCurrentController().getFrame()
dp = sm.createInstanceWithContext('com.sun.star.frame.DispatchHelper', ctx)
def d():
    try: dp.executeDispatch(fr, '.uno:VersionDialog', '', 0, ())
    except: pass
t = threading.Thread(target=d, daemon=True)
t.start()
time.sleep(120)
"""
    # Write UNO snippet to a temp file
    uno_file = f'{WORKDIR}/_dispatch_ver.py'
    with open(uno_file, 'w') as f:
        f.write(uno_snippet)

    # Run the UNO script in background, then interact with dialog via xdotool
    # Escape the comment for safe shell usage
    safe_comment = comment.replace("'", "'\\''")

    shell_script = f"""
python3 {uno_file} &
UPID=$!
sleep 5

# Get dialog geometry for button click position
GEOM=$(xdotool getactivewindow getwindowgeometry 2>/dev/null)
DX=$(echo "$GEOM" | grep Position | sed 's/.*Position: //' | sed 's/,.*//')
DY=$(echo "$GEOM" | grep Position | sed 's/.*,//' | sed 's/ .*//')

# Click "Save New Version" button (approx 90px right, 20px down from dialog origin)
BX=$((DX + 90))
BY=$((DY + 20))
xdotool mousemove $BX $BY click 1
sleep 3

# Type the comment
xdotool type --clearmodifiers --delay 30 '{safe_comment}'
sleep 0.5

# Click OK via Alt+O
xdotool key alt+o
sleep 5

# Close Versions dialog
xdotool key Escape
sleep 2

# Kill UNO background process
kill $UPID 2>/dev/null
wait $UPID 2>/dev/null
echo VERSION_SAVED
"""
    result = shell(shell_script, timeout=90)
    success = 'VERSION_SAVED' in result
    print(f"  Version '{comment}': {'OK' if success else 'FAIL'}")
    return success


def add_all_versions():
    """Open LO with UNO listener and add 5 versions."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"

    # Start LO with UNO listener
    subprocess.Popen(
        ['soffice', '--norestore',
         '--accept=socket,host=localhost,port=2002;urp;StarOffice.ComponentContext',
         OUTPUT],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env
    )
    time.sleep(12)
    print("LO started with UNO listener")

    version_comments = [
        "Initial outline",
        "Added financial section",
        "Approved draft",
        "Added appendices",
        "Final review notes",
    ]

    for i, comment in enumerate(version_comments):
        print(f"Adding version {i+1}/5: {comment}")
        add_version_via_shell(comment)
        time.sleep(1)

    # Verify
    import zipfile
    if os.path.exists(OUTPUT):
        with zipfile.ZipFile(OUTPUT, 'r') as zf:
            names = zf.namelist()
            version_files = [n for n in names if 'ersion' in n.lower()]
            print(f"Version entries: {version_files}")
            print(f"File size: {os.path.getsize(OUTPUT)} bytes")
            return len(version_files) >= 6  # VersionList.xml + 5 versions

    return False


def main():
    kill_lo()
    clean_recovery()

    for f in [OUTPUT]:
        try:
            os.remove(f)
        except:
            pass

    # Step 1: Create base document
    if not create_base_document():
        print("FAILED: Could not create base document")
        return

    # Step 2: Add 5 versions
    success = add_all_versions()

    if success:
        print("SUCCESS: Document with 5 versions created")
    else:
        print("WARNING: Some versions may be missing")

    # Step 3: Restart LO without UNO listener for clean GUI-ready state
    kill_lo()
    time.sleep(2)
    clean_recovery()

    # Clean up temp files
    for f in [f'{WORKDIR}/_dispatch_ver.py']:
        try:
            os.remove(f)
        except:
            pass

    # Step 4: Open the document in Writer
    launch_gui(f'libreoffice --norestore --writer "{OUTPUT}"', delay_sec=3.0)
    print(f'Initial file: {OUTPUT}')
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


main()
