"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m tweaking a 1200×1200 px promo graphic and my “SALE 50% OFF” text layer (currently active) is buried under the product photo. How do I pop this active layer all the way to the top of the stack so it’s visible above everything else?
Generated: 2025-09-01 13:39:30
Status: success
Model: o3
Total Steps: 4
"""

#!/usr/bin/env python3
"""
Reward Script – GIMP Layer Order Verification
============================================
Task: Ensure the text layer named "SALE 50% OFF" has been moved to the very top of the
layer stack so it is visible above the product photo.

Verification Method:
  • Load the supplied XCF with gimpformats (NO filesystem searching).
  • Inspect the layer stack (top-to-bottom order as stored in the file).
  • Award progressive points only for actual task achievements:
      0.2 – Target text layer exists
      0.1 – Reference "Product Photo" layer exists (needed for relative check)
      0.4 – Target layer is above the product layer
      0.3 – Target layer is the very topmost layer
  • Total score is capped at 1.0.

Output:
  • Detailed print statements show each verification step.
  • Final line prints exactly:  REWARD: <score>

IMPORTANT:
  – STRICTLY uses the provided path: /tmp/sale_layer_order_task.xcf
  – No directory searches, globbing, or placeholder checks.
  – No hard-coded True values or hacking patterns.
"""

from gimpformats.gimpXcfDocument import GimpDocument

# 🚨 CRITICAL – use EXACT path from task context
XCF_FILE_PATH = "/tmp/sale_layer_order_task.xcf"

def verify_layer_order(path: str = XCF_FILE_PATH) -> float:
    print(f"\uD83C\uDFAB Verifying layer order for file: {path}")
    total_score = 0.0
    MAX_SCORE = 1.0

    # --- Load XCF -----------------------------------------------------------
    try:
        doc = GimpDocument(path)
        print("✓ XCF file loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load XCF file: {e}")
        print("REWARD: 0.0")
        return 0.0  # Cannot proceed if file doesn't load

    # --- Gather layer names (top to bottom) ---------------------------------
    layer_names = [layer.name for layer in doc._layers]
    print(f"Layer stack (top → bottom): {layer_names}")

    sale_layer_name = "SALE 50% OFF"
    product_layer_name = "Product Photo"

    sale_index = None
    product_index = None

    # --- Requirement 1: Target text layer exists ---------------------------
    if sale_layer_name in layer_names:
        sale_index = layer_names.index(sale_layer_name)
        print(f"✓ Found '{sale_layer_name}' at index {sale_index} (0.2 points)")
        total_score += 0.2
    else:
        print(f"✗ Required layer '{sale_layer_name}' not found")

    # --- Requirement 2: Reference product layer exists ---------------------
    if product_layer_name in layer_names:
        product_index = layer_names.index(product_layer_name)
        print(f"✓ Found '{product_layer_name}' at index {product_index} (0.1 points)")
        total_score += 0.1
    else:
        print(f"✗ Reference layer '{product_layer_name}' not found")

    # --- Requirement 3: SALE layer above product layer ---------------------
    if sale_index is not None and product_index is not None:
        if sale_index < product_index:
            print(f"✓ '{sale_layer_name}' is above '{product_layer_name}' (0.4 points)")
            total_score += 0.4
        else:
            print(f"✗ '{sale_layer_name}' is below '{product_layer_name}'")

    # --- Requirement 4: SALE layer is very topmost -------------------------
    if sale_index is not None:
        if sale_index == 0:
            print(f"✓ '{sale_layer_name}' is the TOP layer (0.3 points)")
            total_score += 0.3
        else:
            print(f"✗ '{sale_layer_name}' is not the topmost layer")

    # --- Final score -------------------------------------------------------
    total_score = min(total_score, MAX_SCORE)
    print(f"Total Score: {total_score}")
    print(f"REWARD: {total_score}")
    return total_score

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_layer_order()

