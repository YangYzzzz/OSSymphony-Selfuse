"""
Reward Script: Add a secondary Y-axis for the 'Growth Rate' series
Task ID: calc_chart_secondary_axis_052
Domain: libreoffice_calc
Scoring:
  Component 1 (0.40): Growth Rate series is assigned to a separate secondary axis group
                       (verified by finding two separate barChart plot areas or two valAx elements)
  Component 2 (0.30): Secondary Y-axis is positioned on the right side
                       (crosses val="max" OR axPos val="r" in the secondary valAx)
  Component 3 (0.30): Secondary Y-axis has a title containing "Growth" or "%" or "Rate"
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_chart_secondary_axis_052'

NS = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def get_chart_xml(file_path):
    """Extract chart XML content from an xlsx file. Returns list of chart XML strings."""
    charts = []
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            chart_files = [n for n in z.namelist() if 'xl/charts/chart' in n and n.endswith('.xml')]
            for cf in sorted(chart_files):
                content = z.read(cf).decode('utf-8')
                charts.append(content)
    except Exception as e:
        print(f"ERROR: Could not read chart XML from {file_path}: {e}")
    return charts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist and be a valid xlsx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    chart_xmls = get_chart_xml(file_path)
    if not chart_xmls:
        print("CRITICAL: No chart XML found in file")
        print("REWARD: 0.0")
        return 0.0

    chart_xml = chart_xmls[0]

    # Parse the chart XML
    try:
        root = ET.fromstring(chart_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse chart XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Growth Rate series is assigned to a separate/secondary axis group (0.40 points)
    # In the golden file, two separate barChart elements exist in the plotArea,
    # each referencing a different axId. Alternatively, two distinct valAx elements exist.
    # We check for two valAx elements with different axIds, OR two barChart groups.
    try:
        # Find all barChart elements
        plot_area = root.find('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}plotArea')
        bar_charts = []
        if plot_area is not None:
            bar_charts = plot_area.findall(
                '{http://schemas.openxmlformats.org/drawingml/2006/chart}barChart'
            )

        # Find all valAx elements
        val_axes = root.findall(
            './/{http://schemas.openxmlformats.org/drawingml/2006/chart}valAx'
        )

        # Check: either 2+ separate barChart groups or 2+ valAx elements with different axIds
        has_two_bar_charts = len(bar_charts) >= 2
        has_two_val_axes = len(val_axes) >= 2

        # Verify that Growth Rate series (C column data) actually references a different axId
        # Look for series referencing 'C' column data in the Growth Rate barChart
        growth_rate_separate = False
        if has_two_bar_charts:
            for bc in bar_charts:
                # Check if this barChart references the C column (Growth Rate data)
                for ser in bc.findall('{http://schemas.openxmlformats.org/drawingml/2006/chart}ser'):
                    val_elem = ser.find(
                        './/{http://schemas.openxmlformats.org/drawingml/2006/chart}f'
                    )
                    if val_elem is not None and '$C$' in (val_elem.text or ''):
                        # Found the Growth Rate series — check its axId references
                        ax_ids_in_bc = [
                            ax.get('val') for ax in bc.findall(
                                '{http://schemas.openxmlformats.org/drawingml/2006/chart}axId'
                            )
                        ]
                        # Primary barChart should reference axId 100/10
                        # Secondary should reference different axIds
                        # Check that this chart's axIds differ from the first barChart's axIds
                        first_bc_ax_ids = [
                            ax.get('val') for ax in bar_charts[0].findall(
                                '{http://schemas.openxmlformats.org/drawingml/2006/chart}axId'
                            )
                        ]
                        # If not all axIds match the first barChart, it's a separate axis group
                        if set(ax_ids_in_bc) != set(first_bc_ax_ids):
                            growth_rate_separate = True

        if has_two_val_axes and has_two_bar_charts and growth_rate_separate:
            print(f"PASS: Component 1 — Growth Rate series is in a separate barChart group with "
                  f"its own axis (found {len(bar_charts)} barChart groups, {len(val_axes)} valAx) (0.40 pts)")
            total_score += 0.40
        elif has_two_val_axes and has_two_bar_charts:
            # Two bar charts and two axes exist, even if we couldn't confirm the separate axIds
            print(f"PASS: Component 1 — Two barChart groups and two valAx found "
                  f"(secondary axis structure present) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — Expected 2 barChart groups and 2 valAx, "
                  f"found {len(bar_charts)} barChart(s), {len(val_axes)} valAx. "
                  f"Growth Rate series is not on a secondary axis.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Secondary Y-axis is positioned on the right side (0.30 points)
    # In the golden file, the secondary valAx has <crosses val="max"/> which places it on the right.
    # Alternatively axPos val="r" would also indicate right side.
    try:
        secondary_axis_right = False
        if len(val_axes) >= 2:
            # Check each valAx beyond the first (or any non-primary axis)
            # Primary axis has axId=100 in initial; secondary has axId=200 in golden
            # We identify the secondary by checking which one has crosses="max" or axPos="r"
            for vax in val_axes:
                ax_id_elem = vax.find(
                    '{http://schemas.openxmlformats.org/drawingml/2006/chart}axId'
                )
                ax_id = ax_id_elem.get('val') if ax_id_elem is not None else None

                # Check for crosses="max" (right-side secondary)
                crosses_elem = vax.find(
                    '{http://schemas.openxmlformats.org/drawingml/2006/chart}crosses'
                )
                crosses_val = crosses_elem.get('val') if crosses_elem is not None else None

                # Check for axPos="r"
                ax_pos_elem = vax.find(
                    '{http://schemas.openxmlformats.org/drawingml/2006/chart}axPos'
                )
                ax_pos_val = ax_pos_elem.get('val') if ax_pos_elem is not None else None

                if crosses_val == 'max' or ax_pos_val == 'r':
                    secondary_axis_right = True
                    print(f"PASS: Component 2 — Secondary Y-axis is on the right side "
                          f"(axId={ax_id}, crosses={crosses_val}, axPos={ax_pos_val}) (0.30 pts)")
                    total_score += 0.30
                    break

        if not secondary_axis_right:
            ax_positions = []
            for vax in val_axes:
                ax_id_e = vax.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}axId')
                ax_pos_e = vax.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}axPos')
                crosses_e = vax.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}crosses')
                ax_positions.append(
                    f"axId={ax_id_e.get('val') if ax_id_e is not None else None}, "
                    f"axPos={ax_pos_e.get('val') if ax_pos_e is not None else None}, "
                    f"crosses={crosses_e.get('val') if crosses_e is not None else None}"
                )
            print(f"FAIL: Component 2 — No secondary Y-axis found on the right side. "
                  f"Axes found: {ax_positions}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Secondary Y-axis has a title related to "Growth Rate %" (0.30 points)
    # In the golden file, the secondary valAx has a title: "Growth Rate %"
    try:
        secondary_axis_has_title = False
        if len(val_axes) >= 2:
            for vax in val_axes:
                # Skip the primary axis (axId=100, which is Revenue)
                ax_id_elem = vax.find(
                    '{http://schemas.openxmlformats.org/drawingml/2006/chart}axId'
                )
                ax_id = ax_id_elem.get('val') if ax_id_elem is not None else None

                # Find title text in this axis
                title_elem = vax.find(
                    './/{http://schemas.openxmlformats.org/drawingml/2006/chart}title'
                )
                if title_elem is not None:
                    # Extract text from the rich text within the title
                    text_nodes = title_elem.findall(
                        './/{http://schemas.openxmlformats.org/drawingml/2006/main}t'
                    )
                    title_text = ''.join(t.text or '' for t in text_nodes).strip()

                    # Check if it relates to Growth Rate / percentage
                    title_lower = title_text.lower()
                    if ('growth' in title_lower or '%' in title_text or
                            'rate' in title_lower or 'percent' in title_lower):
                        # Make sure this isn't the primary Revenue axis
                        if 'revenue' not in title_lower:
                            secondary_axis_has_title = True
                            print(f"PASS: Component 3 — Secondary Y-axis has title '{title_text}' "
                                  f"(axId={ax_id}) (0.30 pts)")
                            total_score += 0.30
                            break

        if not secondary_axis_has_title:
            # Collect all axis titles for debugging
            axis_titles = []
            for vax in val_axes:
                ax_id_e = vax.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}axId')
                title_e = vax.find('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}title')
                title_text = 'no title'
                if title_e is not None:
                    text_nodes = title_e.findall(
                        './/{http://schemas.openxmlformats.org/drawingml/2006/main}t'
                    )
                    title_text = ''.join(t.text or '' for t in text_nodes).strip()
                axis_titles.append(
                    f"axId={ax_id_e.get('val') if ax_id_e is not None else None}: '{title_text}'"
                )
            print(f"FAIL: Component 3 — No secondary Y-axis with Growth Rate title found. "
                  f"Axis titles: {axis_titles}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
