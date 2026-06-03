"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm organizing my project documentation and realized I still need a README—could you help me add a new README.md file to /home/user/docs?
Generated: 2025-09-11 13:50:34
Status: success
Model: azure-o3
Total Steps: 1
"""

from pathlib import Path


def verify_readme(filepath: str = "/home/user/docs/README.md") -> float:
    """Reward script to verify the README.md creation task.

    Scoring rubric (adds up to 1.0):
    1. File exists                        : 0.4
    2. Substantial content (>=20 chars)   : 0.4
    3. Contains at least one MD heading   : 0.2
    """

    total_score = 0.0
    max_score = 1.0

    readme_path = Path(filepath)

    # 1. Verify the file exists and is a regular file (0.4 pts)
    if readme_path.exists() and readme_path.is_file():
        print("✓ README.md file exists (0.4 points)")
        total_score += 0.4

        try:
            # Read file content
            content = readme_path.read_text(encoding="utf-8", errors="ignore")

            # 2. Verify substantial content (>= 20 non-whitespace characters) (0.4 pts)
            if content and len(content.strip()) >= 20:
                print("✓ README.md has substantial content (>=20 chars) (0.4 points)")
                total_score += 0.4
            else:
                print("✗ README.md content is too short (<20 chars)")

            # 3. Check for at least one Markdown heading starting with '#' (0.2 pts)
            has_heading = any(line.strip().startswith("#") for line in content.splitlines())
            if has_heading:
                print("✓ README.md contains a markdown heading (0.2 points)")
                total_score += 0.2
            else:
                print("✗ README.md does not contain any markdown headings")
        except Exception as e:
            print(f"✗ Error reading README.md: {e}")
    else:
        print("✗ README.md file not found at the expected location")

    # Cap the score at 1.0
    final_score = min(total_score, max_score)

    # Output the result in the required format
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_readme()
