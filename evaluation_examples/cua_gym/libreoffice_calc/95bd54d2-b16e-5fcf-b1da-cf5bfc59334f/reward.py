"""
Reward Script: Install Writer's Tools extension for LibreOffice Writer
Task ID: osworld_multi_apps_ext_install_006
Domain: libreoffice_writer (extension installation)
Scoring:
  Component 1 (0.5 pts): WritersTools extension installed in uno_packages cache
                          (pmap file exists and contains com.waanders.WritersTools entry)
  Component 2 (0.3 pts): Installed extension has correct identifier and version (1.9.0)
  Component 3 (0.2 pts): WritersTools.oxt file downloaded to /home/user/Downloads/
  Total: 1.0
"""

import os
import glob
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_ext_install_006'

# Path constants
UNO_PACKAGES_BASE = '/home/user/.config/libreoffice/4/user/uno_packages/cache'
UNO_PACKAGES_PMAP = os.path.join(UNO_PACKAGES_BASE, 'uno_packages.pmap')
UNO_PACKAGES_DIR = os.path.join(UNO_PACKAGES_BASE, 'uno_packages')
DOWNLOADS_DIR = '/home/user/Downloads'

EXPECTED_IDENTIFIER = 'com.waanders.WritersTools'
EXPECTED_VERSION = '1.9.0'
EXPECTED_DISPLAY_NAME = "Writer's Tools"


def verify_task():
    """
    Verify that the Writer's Tools extension has been installed in LibreOffice Writer.
    Checks:
    1. uno_packages.pmap exists and registers the WritersTools extension
    2. Installed extension has the correct identifier and version in description.xml
    3. WritersTools.oxt was downloaded to ~/Downloads/
    Returns a float score between 0.0 and 1.0.
    """
    total_score = 0.0

    # Component 1: uno_packages.pmap exists and contains com.waanders.WritersTools (0.5 points)
    # This is the definitive indicator that the extension was installed via unopkg
    try:
        if os.path.exists(UNO_PACKAGES_PMAP):
            with open(UNO_PACKAGES_PMAP, 'rb') as f:
                pmap_content = f.read()
            pmap_str = pmap_content.decode('utf-8', errors='replace')

            if EXPECTED_IDENTIFIER in pmap_str:
                print(f"PASS: Component 1 — uno_packages.pmap found and contains {EXPECTED_IDENTIFIER} (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — uno_packages.pmap exists but does NOT contain {EXPECTED_IDENTIFIER}")
                print(f"  pmap content preview: {repr(pmap_str[:200])}")
        else:
            print(f"FAIL: Component 1 — uno_packages.pmap not found at {UNO_PACKAGES_PMAP}")
            print("  Extension has not been installed via unopkg")
    except Exception as e:
        print(f"ERROR: Component 1 — Failed to read pmap: {e}")

    # Component 2: Installed extension's description.xml has correct identifier and version (0.3 points)
    # Walk the uno_packages directory and look for WritersTools.oxt/description.xml
    try:
        installed_desc_files = glob.glob(
            os.path.join(UNO_PACKAGES_DIR, '**', 'WritersTools.oxt', 'description.xml'),
            recursive=True
        )
        if installed_desc_files:
            desc_path = installed_desc_files[0]
            with open(desc_path, 'r', encoding='utf-8') as f:
                desc_content = f.read()

            has_identifier = EXPECTED_IDENTIFIER in desc_content
            has_version = EXPECTED_VERSION in desc_content
            has_display_name = EXPECTED_DISPLAY_NAME in desc_content

            if has_identifier and has_version:
                print(f"PASS: Component 2 — Installed description.xml has correct identifier ({EXPECTED_IDENTIFIER}) and version ({EXPECTED_VERSION}) (0.3 pts)")
                total_score += 0.3
            else:
                missing = []
                if not has_identifier:
                    missing.append(f"identifier '{EXPECTED_IDENTIFIER}'")
                if not has_version:
                    missing.append(f"version '{EXPECTED_VERSION}'")
                print(f"FAIL: Component 2 — Installed extension description.xml missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 2 — No WritersTools.oxt/description.xml found in uno_packages directory")
            print(f"  Searched: {UNO_PACKAGES_DIR}")
    except Exception as e:
        print(f"ERROR: Component 2 — Failed to verify installed extension: {e}")

    # Component 3: WritersTools.oxt file downloaded to ~/Downloads/ (0.2 points)
    # The task involves downloading from extensions website, so the .oxt file should be present
    try:
        oxt_files = glob.glob(os.path.join(DOWNLOADS_DIR, '*.oxt'))
        writers_tools_oxt = [f for f in oxt_files if 'WritersTools' in os.path.basename(f) or 'writers' in os.path.basename(f).lower()]

        if writers_tools_oxt:
            oxt_path = writers_tools_oxt[0]
            oxt_size = os.path.getsize(oxt_path)
            # Verify it's a valid zip/oxt file
            try:
                with zipfile.ZipFile(oxt_path) as z:
                    filenames = z.namelist()
                    has_description = any('description.xml' in name for name in filenames)
                    has_manifest = any('manifest.xml' in name for name in filenames)
                if has_description and has_manifest:
                    print(f"PASS: Component 3 — Valid WritersTools.oxt found in Downloads ({oxt_size} bytes, {len(filenames)} files) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — WritersTools.oxt found but missing expected internals (description.xml: {has_description}, manifest.xml: {has_manifest})")
            except zipfile.BadZipFile:
                print(f"FAIL: Component 3 — {oxt_path} exists but is not a valid zip/oxt file")
        else:
            # Also check for any .oxt file in Downloads
            all_oxt = glob.glob(os.path.join(DOWNLOADS_DIR, '**/*.oxt'), recursive=True)
            if all_oxt:
                print(f"FAIL: Component 3 — Found .oxt files in Downloads but none named WritersTools: {all_oxt}")
            else:
                print(f"FAIL: Component 3 — No WritersTools.oxt found in {DOWNLOADS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 3 — Failed to check Downloads directory: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
