"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m organizing the styling for my new website—could you create a stylesheet named “styles.css” inside /home/user/web/css so I can start adding my CSS rules?
Generated: 2025-09-11 11:40:47
Status: success
Model: azure-o3
Total Steps: 7
"""

from pathlib import Path


def verify_task():
    """Reward script to verify that the user created a stylesheet named
    "styles.css" inside /home/user/web/css.

    Scoring rules (progressive):
    1. CSS directory (/home/user/web/css) exists and is a directory  -> 0.3 pts
    2. styles.css exists inside that directory and is a regular file -> +0.7 pts

    Returns a float score between 0.0 and 1.0 and prints detailed
    diagnostics followed by a mandatory line in the form:
        REWARD: X.X
    """
    css_dir = Path("/home/user/web/css")
    css_file = css_dir / "styles.css"

    total_score = 0.0
    max_score = 1.0

    print("--- Verification: Website Stylesheet Creation ---")
    print(f"Expected CSS directory : {css_dir}")
    print(f"Expected stylesheet file: {css_file}\n")

    # Requirement 1: CSS directory exists
    if css_dir.exists() and css_dir.is_dir():
        print("✓ CSS directory exists and is a directory (0.3 points)")
        total_score += 0.3
    else:
        print("✗ CSS directory is missing or not a directory (0 points)")

    # Requirement 2: styles.css exists
    if css_file.exists() and css_file.is_file():
        size_bytes = css_file.stat().st_size
        print(f"✓ Stylesheet file exists (0.7 points) - size: {size_bytes} bytes")
        total_score += 0.7
    else:
        print("✗ Stylesheet file is missing (0 points)")

    final_score = min(total_score, max_score)
    print(f"\nTotal Score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
