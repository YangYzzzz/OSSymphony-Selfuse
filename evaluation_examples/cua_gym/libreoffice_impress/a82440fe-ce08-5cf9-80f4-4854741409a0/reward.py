"""
FINAL REWARD SCRIPT - SUCCESS
Task: On slide 37 I’ve got an image labeled “Picture 1.” When someone clicks that graphic, I want LibreOffice Impress to jump straight to slide 10—basically an internal hyperlink. How do I set that up?
Generated: 2025-09-10 13:29:08
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
from zipfile import ZipFile
from lxml import etree


def verify_internal_hyperlink(file_path: str) -> float:
    """
    Verify that, in the given PPTX file, the picture named "Picture 1" on
    slide 37 has an internal hyperlink that jumps to slide 10.

    Scoring (progressive):
        0.2 – slide 37 exists in the file
        0.3 – a picture shape named "Picture 1" exists on slide 37
        0.5 – that picture contains a hyperlink pointing to slide10.xml

    Returns
    -------
    float
        A score between 0.0 and 1.0 reflecting completion of the task.
    """

    print(f"Verifying internal hyperlink in {file_path}")

    score = 0.0
    max_score = 1.0

    # Open XML namespace map for convenience
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }

    # -------- Basic file checks (no points for existence) --------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    try:
        with ZipFile(file_path, "r") as z:
            # -----------------------------------------------------------------
            # 1. Slide 37 must exist (0.2 points)
            # -----------------------------------------------------------------
            slide_path = "ppt/slides/slide37.xml"
            if slide_path not in z.namelist():
                print("✗ slide 37 not found")
                return 0.0  # cannot continue without the slide

            print("✓ slide 37 found (0.2 points)")
            score += 0.2

            slide_xml = z.read(slide_path)
            slide_root = etree.fromstring(slide_xml)

            # -----------------------------------------------------------------
            # 2. Picture named "Picture 1" must exist on slide 37 (0.3 points)
            #    We perform a case-insensitive match on the @name attribute.
            # -----------------------------------------------------------------
            pic_xpath = (
                "//p:pic[p:nvPicPr/p:cNvPr["  # find picture elements
                "translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
                "='picture 1']]"
            )
            pic_nodes = slide_root.xpath(pic_xpath, namespaces=ns)

            if not pic_nodes:
                print("✗ Picture 1 not found on slide 37")
            else:
                print(f"✓ Picture 1 found ({len(pic_nodes)}) (0.3 points)")
                score += 0.3

                # -----------------------------------------------------------------
                # 3. Check that this picture has a hyperlink pointing to slide 10
                #    (0.5 points)
                # -----------------------------------------------------------------
                picture = pic_nodes[0]
                hlink_nodes = picture.xpath(".//a:hlinkClick", namespaces=ns)

                if not hlink_nodes:
                    print("✗ No hyperlink associated with Picture 1")
                else:
                    # Retrieve relationship ID
                    rid = hlink_nodes[0].get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
                    print(f"✓ Hyperlink element found with r:id={rid}")

                    # Load the relationships file for slide 37
                    rels_path = "ppt/slides/_rels/slide37.xml.rels"
                    if rels_path not in z.namelist():
                        print("✗ Relationships file for slide 37 is missing")
                    else:
                        rels_root = etree.fromstring(z.read(rels_path))
                        target_slide = None
                        for rel in rels_root:
                            if rel.get("Id") == rid:
                                target_slide = rel.get("Target")
                                break

                        if target_slide is None:
                            print("✗ Relationship entry for the hyperlink not found")
                        else:
                            print(f"Hyperlink target: {target_slide}")
                            # The target may be a relative path like "slide10.xml"
                            if "slide10.xml" in target_slide:
                                print("✓ Hyperlink correctly points to slide 10 (0.5 points)")
                                score += 0.5
                            else:
                                print("✗ Hyperlink does not point to slide 10")

        final_score = min(score, max_score)
        print(f"Final score: {final_score}")
        return final_score

    except Exception as e:
        print("✗ Error during verification:", e)
        return 0.0


if __name__ == "__main__":
    # Path to the presentation file in the VM environment
    FILE_PATH = (
        "/home/user/on_slide_37_ive_got_an_image_labeled_picture_1_"
        "when_someone_clicks_that_graphic_i_want_libreoffice_i_golden.pptx"
    )

    reward = verify_internal_hyperlink(FILE_PATH)
    print(f"REWARD: {reward}")

