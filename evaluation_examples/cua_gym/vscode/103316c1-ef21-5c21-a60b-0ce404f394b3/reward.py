"""
Reward Script: Polyglot Notebook Environment in VSCode
Task ID: vscode_gf5_024
Domain: vscode
Scoring:
  - Component 1 (0.20): Polyglot Notebooks extension installed
  - Component 2 (0.15): exploration.ipynb exists and is valid notebook with >= 2 cells
  - Component 3 (0.25): Cell 1 uses #!csharp kernel with C# data processing code
  - Component 4 (0.25): Cell 2 uses #!javascript kernel with Vega-Lite content
  - Component 5 (0.15): Both cells have execution outputs (ran successfully)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_024'
NOTEBOOK_PATH = os.path.join(WORKDIR, 'projects', 'data-viz', 'exploration.ipynb')


def check_extension_installed(ext_id_fragment):
    """Check if a VSCode extension is installed by scanning the extensions directory on disk."""
    ext_id_lower = ext_id_fragment.lower()
    search_dirs = [
        os.path.join(WORKDIR, '.vscode', 'extensions'),
        os.path.join(WORKDIR, '.vscode-server', 'extensions'),
    ]
    for search_dir in search_dirs:
        if os.path.isdir(search_dir):
            for dirname in os.listdir(search_dir):
                if ext_id_lower in dirname.lower():
                    return True
    return False


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: Polyglot Notebooks extension is installed (0.20 points)
    try:
        # The extension ID for Polyglot Notebooks is ms-dotnettools.dotnet-interactive-vscode
        if check_extension_installed('dotnet-interactive-vscode'):
            print(f"PASS: Component 1 — Polyglot Notebooks extension installed (0.20 pts)")
            total_score += 0.20
        else:
            ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
            contents = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
            print(f"FAIL: Component 1 — Polyglot Notebooks extension not found. Extensions dir: {contents}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Precondition: load notebook
    notebook = None
    try:
        if not os.path.exists(NOTEBOOK_PATH):
            print(f"FAIL: exploration.ipynb not found at {NOTEBOOK_PATH}")
            print(f"REWARD: {total_score}")
            return total_score
        with open(NOTEBOOK_PATH, 'r') as f:
            notebook = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load notebook: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    cells = notebook.get('cells', [])

    # Component 2: Notebook exists with at least 2 cells (0.15 points)
    try:
        if len(cells) >= 2:
            print(f"PASS: Component 2 — exploration.ipynb has {len(cells)} cells (>= 2) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Notebook has {len(cells)} cells, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cell 1 uses #!csharp kernel with C# data processing (0.25 points)
    try:
        csharp_found = False
        for cell in cells:
            source = cell.get('source', [])
            if isinstance(source, list):
                source_text = '\n'.join(source)
            else:
                source_text = str(source)

            # Check for #!csharp magic command
            has_csharp_magic = '#!csharp' in source_text

            # Check metadata for csharp kernel
            metadata = cell.get('metadata', {})
            polyglot_meta = metadata.get('polyglot_notebook', {})
            dotnet_meta = metadata.get('dotnet_interactive', {})
            kernel_name = polyglot_meta.get('kernelName', '') or dotnet_meta.get('language', '')
            has_csharp_kernel = kernel_name.lower() == 'csharp'

            # Check for C# data processing content (LINQ, Console.WriteLine, var, etc.)
            has_csharp_code = any(kw in source_text for kw in [
                'Console.', 'var ', '.GroupBy', '.Select', 'new {', 'new[', 'foreach'
            ])

            if (has_csharp_magic or has_csharp_kernel) and has_csharp_code:
                csharp_found = True
                break

        if csharp_found:
            print(f"PASS: Component 3 — Found C# cell with #!csharp kernel and data processing code (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — No cell with #!csharp kernel and C# data processing code found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Cell 2 uses #!javascript kernel with Vega-Lite content (0.25 points)
    try:
        js_found = False
        for cell in cells:
            source = cell.get('source', [])
            if isinstance(source, list):
                source_text = '\n'.join(source)
            else:
                source_text = str(source)

            # Check for #!javascript magic command
            has_js_magic = '#!javascript' in source_text

            # Check metadata for javascript kernel
            metadata = cell.get('metadata', {})
            polyglot_meta = metadata.get('polyglot_notebook', {})
            dotnet_meta = metadata.get('dotnet_interactive', {})
            kernel_name = polyglot_meta.get('kernelName', '') or dotnet_meta.get('language', '')
            has_js_kernel = kernel_name.lower() == 'javascript'

            # Check for Vega-Lite or visualization content
            has_vega = any(kw in source_text.lower() for kw in [
                'vega-lite', 'vega', 'vegaspec', 'vegalite',
                'console.log', '"mark"', "'mark'"
            ])

            if (has_js_magic or has_js_kernel) and has_vega:
                js_found = True
                break

        if js_found:
            print(f"PASS: Component 4 — Found JavaScript cell with #!javascript kernel and Vega-Lite content (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — No cell with #!javascript kernel and Vega-Lite/visualization content found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Both cells have execution outputs (ran successfully) (0.15 points)
    try:
        csharp_has_output = False
        js_has_output = False

        for cell in cells:
            source = cell.get('source', [])
            if isinstance(source, list):
                source_text = '\n'.join(source)
            else:
                source_text = str(source)

            outputs = cell.get('outputs', [])
            has_output = len(outputs) > 0

            # Check no error outputs
            has_error = any(o.get('output_type') == 'error' for o in outputs)

            metadata = cell.get('metadata', {})
            polyglot_meta = metadata.get('polyglot_notebook', {})
            dotnet_meta = metadata.get('dotnet_interactive', {})
            kernel_name = polyglot_meta.get('kernelName', '') or dotnet_meta.get('language', '')

            if '#!csharp' in source_text or kernel_name.lower() == 'csharp':
                if has_output and not has_error:
                    csharp_has_output = True
            if '#!javascript' in source_text or kernel_name.lower() == 'javascript':
                if has_output and not has_error:
                    js_has_output = True

        if csharp_has_output and js_has_output:
            print(f"PASS: Component 5 — Both C# and JavaScript cells have successful outputs (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — C# output: {csharp_has_output}, JS output: {js_has_output}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
