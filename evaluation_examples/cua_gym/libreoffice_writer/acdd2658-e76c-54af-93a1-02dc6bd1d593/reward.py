"""
Reward Script: Verify InsertClosingParagraph macro in engagement letter
Task ID: writer_legal_063
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): ODT file with macro storage exists
  Component 2 (0.3): Macro named 'InsertClosingParagraph' exists in Basic library
  Component 3 (0.2): Macro is a proper Sub with correct structure
  Component 4 (0.3): Macro body contains the exact required closing text
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import glob

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_063'

# The expected closing text that the macro should insert
EXPECTED_TEXT = (
    "We appreciate the opportunity to represent you in this matter. "
    "Please sign and return this letter to confirm your engagement of our firm. "
    "This engagement letter shall be governed by the laws of the State of New York."
)


def find_odt_file():
    """Find any ODT file that could contain macros for this task."""
    # Check canonical path first
    canonical = os.path.join(WORKDIR, f'{TASK_ID}.odt')
    if os.path.exists(canonical):
        return canonical
    # Search for any ODT file in WORKDIR
    odt_files = glob.glob(os.path.join(WORKDIR, '*.odt'))
    if odt_files:
        return odt_files[0]
    return None


def extract_macro_source(odt_path):
    """
    Extract Basic macro source code from an ODT file.
    Returns a dict: {module_name: source_code}
    """
    macros = {}
    try:
        with zipfile.ZipFile(odt_path, 'r') as z:
            names = z.namelist()
            # Look for Basic module XML files
            for name in names:
                if name.startswith('Basic/') and name.endswith('.xml') and 'Module' in name:
                    content = z.read(name).decode('utf-8')
                    # Parse XML to extract script content
                    try:
                        root = ET.fromstring(content)
                        # The module name is in script:name attribute
                        mod_name = root.attrib.get(
                            '{http://openoffice.org/2000/script}name', ''
                        )
                        # The macro source is the text content of the element
                        source = root.text or ''
                        if source.strip():
                            macros[mod_name] = source
                    except ET.ParseError:
                        # Try plain text extraction as fallback
                        pass

            # Also check script-lb.xml for library element names
            for name in names:
                if name.endswith('script-lb.xml'):
                    content = z.read(name).decode('utf-8')
                    try:
                        root = ET.fromstring(content)
                        ns = {'library': 'http://openoffice.org/2000/library'}
                        for elem in root.findall('.//library:element', ns):
                            elem_name = elem.attrib.get(
                                '{http://openoffice.org/2000/library}name', ''
                            )
                            if elem_name and elem_name not in macros:
                                # Module is declared but we didn't find source
                                pass
                    except ET.ParseError:
                        pass
    except Exception as e:
        print(f"ERROR: Failed to read ODT file: {e}")
    return macros


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ODT file exists (0.2 points)
    # Macros in LibreOffice are stored in ODT format, not DOCX.
    # This component FAILS on initial_env (no ODT) and PASSES on golden_env.
    try:
        odt_path = find_odt_file()
        if odt_path and os.path.exists(odt_path):
            # Verify it's a valid ZIP/ODT file with Basic directory
            with zipfile.ZipFile(odt_path, 'r') as z:
                names = z.namelist()
                has_basic = any(n.startswith('Basic/') for n in names)
                if has_basic:
                    print(f"PASS: Component 1 -- ODT file with Basic macro storage found: {odt_path} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 1 -- ODT file exists but no Basic/ directory (no macros)")
        else:
            print("FAIL: Component 1 -- No ODT file found in /home/user/")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if odt_path is None or not os.path.exists(odt_path):
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Extract macros for remaining components
    macros = extract_macro_source(odt_path)
    print(f"DEBUG: Found {len(macros)} macro module(s): {list(macros.keys())}")

    # Component 2: Macro named 'InsertClosingParagraph' exists (0.3 points)
    # Check that a Sub named InsertClosingParagraph is defined in any module
    try:
        macro_source = ""
        for mod_name, source in macros.items():
            if 'InsertClosingParagraph' in source:
                macro_source = source
                break

        if len(macro_source) > 0:
            print(f"PASS: Component 2 -- Macro 'InsertClosingParagraph' found in Basic library (0.3 pts)")
            total_score += 0.3
        else:
            # Also search all module sources for any sub with that name
            print(f"FAIL: Component 2 -- No macro named 'InsertClosingParagraph' found. Modules: {list(macros.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Macro is a proper Sub with correct structure (0.2 points)
    # Must have Sub InsertClosingParagraph() ... End Sub
    try:
        if macro_source:
            lines = macro_source.strip().split('\n')
            has_sub_decl = any(
                line.strip().lower().startswith('sub insertclosingparagraph')
                for line in lines
            )
            has_end_sub = any(
                line.strip().lower() == 'end sub'
                for line in lines
            )
            if has_sub_decl and has_end_sub:
                print(f"PASS: Component 3 -- Proper Sub/End Sub structure found (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 -- Missing Sub declaration ({has_sub_decl}) or End Sub ({has_end_sub})")
        else:
            print("FAIL: Component 3 -- No macro source to check")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Macro contains the exact required closing text (0.3 points)
    # The macro must insert the specific engagement letter closing paragraph
    try:
        if macro_source:
            # Normalize whitespace for comparison
            normalized_source = ' '.join(macro_source.split())
            normalized_expected = ' '.join(EXPECTED_TEXT.split())

            if normalized_expected in normalized_source:
                print(f"PASS: Component 4 -- Macro contains exact closing text (0.3 pts)")
                total_score += 0.3
            else:
                # Check key phrases for partial match info
                key_phrases = [
                    "We appreciate the opportunity to represent you",
                    "Please sign and return this letter",
                    "governed by the laws of the State of New York"
                ]
                matches = sum(1 for phrase in key_phrases if phrase in macro_source)
                print(f"FAIL: Component 4 -- Closing text not found verbatim. Key phrase matches: {matches}/3")
        else:
            print("FAIL: Component 4 -- No macro source to check")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
