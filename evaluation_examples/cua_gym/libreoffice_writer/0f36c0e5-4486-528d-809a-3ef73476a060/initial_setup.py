"""
Initial Setup: Create Writer document with envelope and set default feed direction
Task ID: writer_lec_051
Domain: libreoffice_writer

Creates a Writer document with:
1. An envelope section (first page with Envelope page style)
2. A business letter body
3. Sets the LO envelope printer feed direction to face-down, flap-right (non-target)
4. Opens the document in LibreOffice Writer
"""

import os
import subprocess
import time
import shlex
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_051'
OUTPUT_ODT = f'{WORKDIR}/{TASK_ID}.odt'

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


def set_envelope_printer_config(from_above, alignment, shift_right=0, shift_down=0):
    """
    Set LO envelope printer feed direction in registrymodifications.xcu.

    Args:
        from_above: True = face up, False = face down
        alignment: 0-7, feed orientation
            Face-up row:  0=flap-left, 1=flap-right, 2=flap-bottom, 3=flap-top
            Face-down row: 4=flap-left, 5=flap-right, 6=flap-bottom, 7=flap-top
        shift_right: shift right value in 1/100 mm
        shift_down: shift down value in 1/100 mm
    """
    reg_path = os.path.expanduser('~/.config/libreoffice/4/user/registrymodifications.xcu')

    if not os.path.exists(reg_path):
        # Create a minimal registrymodifications.xcu
        content = '''<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</oor:items>
'''
        os.makedirs(os.path.dirname(reg_path), exist_ok=True)
        with open(reg_path, 'w') as f:
            f.write(content)

    with open(reg_path, 'r') as f:
        content = f.read()

    # Build the config items to inject
    items = [
        (f'/org.openoffice.Office.Writer/Envelope/Print', 'FromAbove',
         'boolean', str(from_above).lower()),
        (f'/org.openoffice.Office.Writer/Envelope/Print', 'Alignment',
         'int', str(alignment)),
        (f'/org.openoffice.Office.Writer/Envelope/Print', 'Right',
         'int', str(shift_right)),
        (f'/org.openoffice.Office.Writer/Envelope/Print', 'Down',
         'int', str(shift_down)),
    ]

    for path, name, typ, value in items:
        item_str = f'<item oor:path="{path}"><prop oor:name="{name}" oor:op="fuse"><value>{value}</value></prop></item>'

        # Check if item already exists and replace it
        import re
        pattern = rf'<item oor:path="{re.escape(path)}"><prop oor:name="{name}"[^>]*>.*?</prop></item>'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, item_str, content, flags=re.DOTALL)
        else:
            # Insert before closing </oor:items>
            content = content.replace('</oor:items>', item_str + '\n</oor:items>')

    with open(reg_path, 'w') as f:
        f.write(content)

    print(f'Set envelope printer config: FromAbove={from_above}, Alignment={alignment}')


def create_document_with_envelope():
    """Create a Writer document with envelope using UNO API."""
    import uno
    from com.sun.star.beans import PropertyValue

    # Kill any existing LO
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(3)

    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    proc = subprocess.Popen([
        'soffice', '--norestore',
        '--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
    time.sleep(6)

    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
        'com.sun.star.bridge.UnoUrlResolver', localContext)
    ctx = resolver.resolve(
        'uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext('com.sun.star.frame.Desktop', ctx)

    doc = desktop.loadComponentFromURL('private:factory/swriter', '_blank', 0, ())
    time.sleep(2)

    # Configure Envelope page style
    page_styles = doc.getStyleFamilies().getByName('PageStyles')
    env_style = page_styles.getByName('Envelope')

    from com.sun.star.awt import Size
    env_size = Size()
    env_size.Width = 24130   # #10 envelope width (9.5 inches)
    env_size.Height = 10478  # #10 envelope height (4.125 inches)
    env_style.setPropertyValue('Size', env_size)
    env_style.setPropertyValue('IsLandscape', True)
    env_style.setPropertyValue('TopMargin', 1000)
    env_style.setPropertyValue('BottomMargin', 1000)
    env_style.setPropertyValue('LeftMargin', 2000)
    env_style.setPropertyValue('RightMargin', 2000)

    text = doc.getText()
    cursor = text.createTextCursor()

    # --- Envelope page (first section) ---
    cursor.gotoStart(False)
    cursor.setPropertyValue('PageDescName', 'Envelope')
    cursor.setPropertyValue('PageNumberOffset', 1)

    from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK

    # Return address (top-left)
    cursor.setPropertyValue('CharHeight', 10)
    text.insertString(cursor, 'Sarah Chen', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, 'Meridian Consulting Group', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, '2890 Market Street, Floor 12', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, 'San Francisco, CA 94114', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    # Space for delivery address
    for _ in range(4):
        text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    # Delivery address (indented to center-right area)
    cursor.setPropertyValue('ParaLeftMargin', 5000)
    cursor.setPropertyValue('CharHeight', 12)
    text.insertString(cursor, 'Mr. James Rodriguez', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue('ParaLeftMargin', 5000)
    text.insertString(cursor, 'Pinnacle Technologies Inc.', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue('ParaLeftMargin', 5000)
    text.insertString(cursor, '4521 Innovation Drive, Suite 300', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue('ParaLeftMargin', 5000)
    text.insertString(cursor, 'San Francisco, CA 94107', False)

    # --- Page break to Standard for letter body ---
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    cursor.setPropertyValue('BreakType', 4)  # PAGE_BEFORE
    cursor.setPropertyValue('PageDescName', 'Standard')
    cursor.setPropertyValue('ParaLeftMargin', 0)
    cursor.setPropertyValue('CharHeight', 12)

    # Date
    text.insertString(cursor, 'March 28, 2026', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    # Letter body
    text.insertString(cursor, 'Dear Mr. Rodriguez,', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    text.insertString(cursor,
        'I am writing to provide an update on the Meridian Q2 project milestones. '
        'As discussed during our last meeting, the development team has successfully '
        'completed the initial prototype phase ahead of schedule.', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    text.insertString(cursor,
        'The key deliverables for this quarter include the redesigned user interface, '
        'improved database performance metrics, and the new reporting dashboard. Our '
        'QA team has begun regression testing and we expect to have the preliminary '
        'results by the end of next week.', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    text.insertString(cursor,
        'I have attached the updated project timeline and budget allocation report '
        'for your review. Please note the revised completion dates for Phase 3, '
        'which have been moved forward by two weeks based on our current progress.', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    text.insertString(cursor,
        'Please let me know if you would like to schedule a follow-up meeting to '
        'review the progress in detail. I am available Tuesday through Thursday '
        'next week.', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)

    text.insertString(cursor, 'Best regards,', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, 'Sarah Chen', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, 'Senior Project Manager', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, 'Meridian Consulting Group', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, 'schen@meridianconsulting.com', False)
    text.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)
    text.insertString(cursor, '(415) 555-0147', False)

    # Save as ODF
    url_odt = 'file://' + OUTPUT_ODT
    props_odt = (PropertyValue('FilterName', 0, 'writer8', 0),)
    doc.storeToURL(url_odt, props_odt)

    doc.close(True)
    time.sleep(1)
    proc.terminate()
    time.sleep(2)

    print(f'Document created: {OUTPUT_ODT}')
    print(f'File size: {os.path.getsize(OUTPUT_ODT)} bytes')


def main():
    # Step 1: Create the document with envelope
    create_document_with_envelope()

    # Step 2: Set the envelope printer feed to non-default (face-down, flap-right)
    # This is the "before" state that the agent needs to change
    # Alignment=5 means face-down row, flap-right
    # FromAbove=false means face down
    set_envelope_printer_config(from_above=False, alignment=5, shift_right=0, shift_down=0)

    # Step 3: Launch document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT_ODT}"', delay_sec=3.0)

    print(f'Initial file created: {OUTPUT_ODT}')
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')
    print('Envelope feed direction set to: face-down, flap-right (non-target)')


main()
