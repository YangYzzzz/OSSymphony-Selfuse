"""
Reward Script: Add alt text descriptions to all images in a PDF
Task ID: pdf_res_020
Domain: pdf
Scoring:
  - Component 1 (0.10): Output tagged file exists
  - Component 2 (0.15): PDF has MarkInfo with Marked=True
  - Component 3 (0.15): PDF has StructTreeRoot with Document element
  - Component 4 (0.30): 4 Figure struct elements present
  - Component 5 (0.30): Correct alt text format for all 4 figures
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_020'
OUTPUT_FILE = os.path.join(WORKDIR, 'papers', 'accessibility_paper_tagged.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid PDF (0.10 points)
    # This is NOT a precondition -- the task asks the agent to CREATE this file.
    # The initial_env does NOT have this file.
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 -- Output file does not exist: {file_path}")
            print("REWARD: 0.0")
            return 0.0

        import pikepdf
        pdf = pikepdf.open(file_path)
        page_count = len(pdf.pages)
        if page_count > 0:
            print(f"PASS: Component 1 -- Output file exists and is valid PDF with {page_count} pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- PDF has 0 pages")
        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 1 -- Cannot open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Reopen for structure checks
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
        catalog = pdf.Root
    except Exception as e:
        print(f"ERROR: Cannot reopen PDF for structure checks: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: MarkInfo with Marked=True (0.15 points)
    try:
        if "/MarkInfo" in catalog:
            mark_info = catalog["/MarkInfo"]
            if "/Marked" in mark_info and bool(mark_info["/Marked"]):
                print(f"PASS: Component 2 -- MarkInfo/Marked is True (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- MarkInfo exists but Marked is not True")
        else:
            print(f"FAIL: Component 2 -- No /MarkInfo in catalog")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: StructTreeRoot exists with Document element (0.15 points)
    try:
        if "/StructTreeRoot" not in catalog:
            print(f"FAIL: Component 3 -- No /StructTreeRoot in catalog")
        else:
            struct_root = catalog["/StructTreeRoot"]
            if "/K" not in struct_root:
                print(f"FAIL: Component 3 -- StructTreeRoot has no /K children")
            else:
                top_elem = struct_root["/K"]
                # Check if top element is a Document
                if hasattr(top_elem, "keys") and "/S" in top_elem and str(top_elem["/S"]) == "/Document":
                    print(f"PASS: Component 3 -- StructTreeRoot has /Document element (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 -- StructTreeRoot top element is not /Document")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 4 Figure struct elements present (0.30 points)
    figure_elements = []
    try:
        if "/StructTreeRoot" in catalog:
            struct_root = catalog["/StructTreeRoot"]
            if "/K" in struct_root:
                top_elem = struct_root["/K"]

                def find_figures(elem, results):
                    """Recursively find all /Figure struct elements."""
                    if isinstance(elem, pikepdf.Array):
                        for child in elem:
                            find_figures(child, results)
                    elif hasattr(elem, "keys"):
                        s_val = str(elem.get("/S", ""))
                        if s_val == "/Figure":
                            alt_text = ""
                            if "/Alt" in elem:
                                alt_text = str(elem["/Alt"])
                            results.append(alt_text)
                        if "/K" in elem:
                            find_figures(elem["/K"], results)

                find_figures(top_elem, figure_elements)

        num_figures = len(figure_elements)
        if num_figures == 4:
            print(f"PASS: Component 4 -- Found exactly 4 Figure elements (0.30 pts)")
            total_score += 0.30
        elif num_figures > 0:
            partial = 0.30 * (min(num_figures, 4) / 4)
            print(f"PARTIAL: Component 4 -- Found {num_figures}/4 Figure elements ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No Figure elements found in structure tree")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Correct alt text format for all figures (0.30 points)
    # Expected: "Figure N: [See paper for description]" for N = 1..4
    try:
        if len(figure_elements) == 0:
            print(f"FAIL: Component 5 -- No figure elements to check alt text")
        else:
            correct_count = 0
            expected_alts = [
                "Figure 1: [See paper for description]",
                "Figure 2: [See paper for description]",
                "Figure 3: [See paper for description]",
                "Figure 4: [See paper for description]",
            ]
            for i, alt in enumerate(figure_elements):
                if i < len(expected_alts):
                    if alt == expected_alts[i]:
                        correct_count += 1
                        print(f"  Figure {i+1} alt text: CORRECT")
                    else:
                        print(f"  Figure {i+1} alt text: WRONG (got: '{alt}', expected: '{expected_alts[i]}')")

            if correct_count == 4:
                print(f"PASS: Component 5 -- All 4 figures have correct alt text (0.30 pts)")
                total_score += 0.30
            elif correct_count > 0:
                partial = 0.30 * (correct_count / 4)
                print(f"PARTIAL: Component 5 -- {correct_count}/4 figures have correct alt text ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- No figures have correct alt text")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    pdf.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
