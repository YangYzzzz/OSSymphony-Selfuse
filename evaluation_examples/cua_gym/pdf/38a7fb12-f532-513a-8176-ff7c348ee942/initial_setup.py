"""
Initial Setup: Create illustrated_guide.pdf with 40 pages and chapter bookmarks (no figure bookmarks)
Task ID: pdf_mbc_054
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_054'
OUTPUT = f'{WORKDIR}/Documents/illustrated_guide.pdf'


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


def create_initial():
    import pymupdf

    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # Chapter structure for a 40-page illustrated guide
    chapters = [
        {"title": "Chapter 1: Introduction to Visual Design", "start": 0, "end": 4},
        {"title": "Chapter 2: Color Theory and Application", "start": 4, "end": 9},
        {"title": "Chapter 3: Typography and Layout", "start": 9, "end": 16},
        {"title": "Chapter 4: Illustration Techniques", "start": 16, "end": 23},
        {"title": "Chapter 5: Digital Media Production", "start": 23, "end": 30},
        {"title": "Chapter 6: Print and Publication", "start": 30, "end": 35},
        {"title": "Chapter 7: Portfolio and Presentation", "start": 35, "end": 40},
    ]

    # Page content descriptions for realistic text
    page_contents = [
        # Chapter 1: Introduction to Visual Design (pages 1-4)
        ("Introduction to Visual Design",
         "Visual design is the strategic use of imagery, color, fonts, and space to engage users and enhance usability. "
         "This guide explores fundamental principles that every designer should master. From ancient cave paintings to "
         "modern digital interfaces, visual communication has been at the heart of human expression."),
        ("The History of Visual Communication",
         "The earliest known examples of visual communication date back over 40,000 years. Cave paintings in Lascaux, "
         "France and Altamira, Spain demonstrate humanity's innate desire to communicate through images. The invention "
         "of the printing press by Johannes Gutenberg in 1440 revolutionized how visual information was disseminated."),
        ("Principles of Design",
         "The fundamental principles of design include balance, contrast, emphasis, movement, pattern, rhythm, and unity. "
         "These principles guide designers in creating compositions that are both aesthetically pleasing and functionally "
         "effective. Understanding these principles is essential for creating cohesive visual experiences."),
        ("Design Thinking Process",
         "Design thinking is a human-centered approach to innovation that draws from the designer's toolkit to integrate "
         "the needs of people, the possibilities of technology, and the requirements for business success. The five stages "
         "are: Empathize, Define, Ideate, Prototype, and Test."),
        # Chapter 2: Color Theory (pages 5-9)
        ("Understanding Color",
         "Color theory is a body of practical guidance for color mixing and the visual effects of specific color combinations. "
         "Sir Isaac Newton's color wheel, developed in 1666, remains the foundation of modern color theory. The primary "
         "colors—red, blue, and yellow—form the basis from which all other colors are derived."),
        ("The Color Wheel and Harmonies",
         "Color harmonies are specific combinations of colors on the color wheel that create pleasing visual effects. "
         "Complementary colors sit opposite each other on the wheel, creating high contrast. Analogous colors are "
         "adjacent on the wheel, creating serene and comfortable designs."),
        ("Color Psychology in Design",
         "Colors evoke psychological responses that can be leveraged in design. Red signals energy and urgency, commonly "
         "used in clearance sales. Blue conveys trust and dependability, favored by financial institutions. Green represents "
         "nature and health, popular in organic and wellness branding."),
        ("Digital Color Systems: RGB and CMYK",
         "RGB (Red, Green, Blue) is the additive color model used for screens and digital displays. CMYK (Cyan, Magenta, "
         "Yellow, Key/Black) is the subtractive color model used for print production. Understanding when to use each "
         "system is critical for ensuring color accuracy across media."),
        ("Advanced Color Techniques",
         "Advanced color techniques include gradient mapping, duotone effects, and color grading. These methods allow "
         "designers to create sophisticated visual atmospheres. Gradient mapping replaces luminosity values with colors "
         "from a gradient, creating dramatic tonal effects."),
        # Chapter 3: Typography and Layout (pages 10-16)
        ("Foundations of Typography",
         "Typography is the art and technique of arranging type to make written language legible, readable, and appealing. "
         "The anatomy of type includes terms like baseline, x-height, ascender, descender, and cap height. Understanding "
         "these elements is crucial for selecting and pairing typefaces effectively."),
        ("Typeface Classification",
         "Typefaces are classified into several categories: Serif (Times New Roman, Georgia), Sans-serif (Helvetica, Arial), "
         "Monospace (Courier, Consolas), Script (Brush Script, Pacifico), and Display (Impact, Lobster). Each category "
         "carries distinct connotations and is suited to different design contexts."),
        ("Font Pairing and Hierarchy",
         "Effective font pairing creates visual interest while maintaining readability. A common approach pairs a serif "
         "heading font with a sans-serif body font. Typographic hierarchy uses size, weight, color, and spacing to guide "
         "the reader's eye through content in order of importance."),
        ("Grid Systems and Layout",
         "Grid systems provide a structural framework for organizing content on a page. The Swiss/International Style grid, "
         "developed in the 1950s, remains influential today. Modern responsive grids adapt fluidly across screen sizes, "
         "ensuring consistent layouts from mobile devices to large desktop monitors."),
        ("White Space and Composition",
         "White space, or negative space, is the empty area between design elements. Far from being wasted space, it improves "
         "readability, creates visual hierarchy, and gives designs a clean, sophisticated appearance. Apple's design "
         "philosophy famously leverages generous white space for a premium aesthetic."),
        ("Figure 3.1: The Anatomy of a Typeface",
         "This page presents a detailed diagram of typeface anatomy. The illustration shows the key measurements and "
         "structural elements that define a typeface: baseline, mean line, cap line, ascender line, and descender line. "
         "Each element is labeled with precise terminology used by typographers and font designers worldwide."),
        ("Responsive Typography",
         "Responsive typography adapts text size, line height, and column width based on the viewing device. Fluid "
         "typography uses CSS clamp() or viewport units to scale smoothly between breakpoints. This ensures optimal "
         "readability whether content is viewed on a phone, tablet, or desktop display."),
        # Chapter 4: Illustration Techniques (pages 17-23)
        ("Introduction to Illustration",
         "Illustration serves as a powerful communication tool that can simplify complex ideas, evoke emotions, and "
         "create memorable visual narratives. From editorial illustrations to technical diagrams, the applications are "
         "diverse. Modern illustrators work across both traditional and digital media."),
        ("Vector Illustration",
         "Vector graphics use mathematical equations to define shapes, allowing infinite scalability without quality loss. "
         "Adobe Illustrator and Affinity Designer are industry-standard vector tools. Vector illustrations are ideal for "
         "logos, icons, infographics, and any graphics requiring crisp reproduction at various sizes."),
        ("Raster Illustration and Digital Painting",
         "Raster (bitmap) illustrations are composed of pixels, offering rich textures and photorealistic effects. "
         "Photoshop, Procreate, and Krita are popular raster illustration tools. Digital painting techniques mirror "
         "traditional methods like oil painting, watercolor, and charcoal drawing."),
        ("Isometric and Technical Illustration",
         "Isometric illustration presents 3D objects without perspective distortion, using parallel projection at 30-degree "
         "angles. Technical illustration combines artistic skill with scientific accuracy to communicate complex information "
         "clearly. Exploded views, cutaway diagrams, and cross-sections are common techniques."),
        ("Character Design and Storytelling",
         "Character design involves creating visual personas with distinct personalities, proportions, and style. Successful "
         "characters are recognizable even in silhouette. The design process includes research, sketching, refinement, and "
         "creating model sheets that show the character from multiple angles and in various expressions."),
        ("Infographic Design",
         "Infographics transform data and information into visual stories. Effective infographics combine clear data "
         "visualization with engaging illustration. Common types include statistical, informational, timeline, process, "
         "geographic, comparison, and hierarchical infographics."),
        ("Motion and Animation Basics",
         "Animation brings illustrations to life through movement. The 12 principles of animation, established by Disney "
         "animators Frank Thomas and Ollie Johnston, remain the foundation of compelling motion design. Modern tools like "
         "After Effects, Lottie, and CSS animations make motion accessible to all designers."),
        # Chapter 5: Digital Media Production (pages 24-30)
        ("Digital Asset Management",
         "Effective digital asset management (DAM) ensures that design files, images, fonts, and brand resources are "
         "organized, accessible, and version-controlled. Cloud-based DAM platforms like Brandfolder and Bynder streamline "
         "collaboration across distributed teams."),
        ("Image Optimization for Web",
         "Web images must balance visual quality with file size for fast page loads. Modern formats like WebP and AVIF "
         "offer superior compression compared to JPEG and PNG. Responsive images using srcset and the picture element "
         "serve appropriate sizes based on device capabilities."),
        ("Video Production Fundamentals",
         "Video content dominates digital media, with over 80% of internet traffic attributed to video streaming. "
         "Fundamental concepts include frame rate (24fps for cinematic, 30/60fps for web), resolution (1080p, 4K), "
         "codec selection (H.264, H.265, VP9), and bitrate optimization."),
        ("Audio Design and Integration",
         "Audio design enhances multimedia experiences through sound effects, background music, voiceover, and spatial "
         "audio. The psychoacoustic principles of masking, localization, and loudness perception inform effective audio "
         "mixing. Formats range from lossless (WAV, FLAC) to compressed (MP3, AAC, Opus)."),
        ("Interactive Media and UX",
         "Interactive media design combines visual design with user experience principles. Microinteractions—small, "
         "task-based animations—provide feedback and delight. Prototyping tools like Figma, Sketch, and InVision allow "
         "designers to test interactions before development begins."),
        ("Accessibility in Digital Design",
         "Accessible design ensures content is usable by people with disabilities. WCAG 2.1 guidelines establish standards "
         "for perceivable, operable, understandable, and robust digital content. Key considerations include color contrast "
         "ratios (4.5:1 minimum for normal text), keyboard navigation, and screen reader compatibility."),
        ("Cross-Platform Design Strategy",
         "Designing across platforms requires understanding the conventions and constraints of each. iOS Human Interface "
         "Guidelines, Material Design for Android, and Fluent Design for Windows each prescribe distinct interaction "
         "patterns. A successful cross-platform strategy respects platform conventions while maintaining brand consistency."),
        # Chapter 6: Print and Publication (pages 31-35)
        ("Print Production Essentials",
         "Print production transforms digital designs into physical products. Key concepts include bleed (extending artwork "
         "3mm beyond the trim line), safe zones (keeping critical content 5mm inside the trim), spot colors (Pantone "
         "matching), and paper stock selection (coated vs. uncoated, weight in GSM)."),
        ("Prepress and File Preparation",
         "Prepress involves preparing design files for commercial printing. Essential steps include converting RGB to CMYK, "
         "embedding or outlining fonts, flattening transparency, setting appropriate resolution (300 DPI minimum), and "
         "creating printer-ready PDF/X files with proper trim marks and color bars."),
        ("Binding and Finishing Techniques",
         "Binding methods include saddle stitch (stapled), perfect binding (glued spine), spiral/coil binding, and "
         "case binding (hardcover). Finishing techniques such as embossing, debossing, foil stamping, spot UV coating, "
         "and die cutting add tactile dimension and premium quality to printed pieces."),
        ("Publication Layout and Design",
         "Publication design for books, magazines, and catalogs requires mastery of multi-page layout. Consistent use of "
         "master pages, baseline grids, paragraph styles, and image placement creates a cohesive reading experience. "
         "Pagination, running headers, and folios maintain navigation throughout long documents."),
        ("Sustainable Print Practices",
         "Environmentally responsible printing uses FSC-certified papers, soy-based inks, and waterless printing processes. "
         "Design choices like minimizing ink coverage, selecting recycled stocks, and right-sizing print runs reduce "
         "environmental impact while maintaining quality."),
        # Chapter 7: Portfolio and Presentation (pages 36-40)
        ("Building a Design Portfolio",
         "A strong portfolio showcases your best work with clear project narratives. Each case study should include the "
         "challenge, process, solution, and results. Curate 8-12 projects that demonstrate range while highlighting your "
         "specialty. Quality always trumps quantity in portfolio presentation."),
        ("Presentation Design Principles",
         "Effective presentations tell stories through sequential visual frames. The 10-20-30 rule suggests no more than "
         "10 slides, 20 minutes, and 30-point minimum font size. Use high-quality imagery, minimal text, and consistent "
         "visual language to maintain audience engagement."),
        ("Client Communication and Feedback",
         "Presenting design work to clients requires clear articulation of design decisions. Use design rationale to "
         "connect visual choices to business objectives. Structured feedback processes—using tools like InVision, Figma "
         "comments, or annotated PDFs—keep review cycles efficient and productive."),
        ("Career Development in Design",
         "The design industry offers diverse career paths: UI/UX design, brand identity, motion graphics, illustration, "
         "art direction, and design leadership. Continuous learning through conferences (AIGA, Config), online platforms "
         "(Skillshare, Coursera), and community engagement keeps skills current."),
        ("Conclusion: The Future of Visual Design",
         "Visual design continues to evolve with emerging technologies. AI-assisted design tools, augmented reality "
         "interfaces, variable fonts, and generative art are reshaping the profession. The fundamentals covered in this "
         "guide—color, typography, layout, and composition—remain the bedrock upon which innovation builds."),
    ]

    # Create 40 pages with content
    for i in range(40):
        page = doc.new_page(width=595, height=842)  # A4
        title, body = page_contents[i]

        # Page header
        page.insert_text(
            pymupdf.Point(72, 50),
            "The Illustrated Guide to Visual Design",
            fontsize=8,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )

        # Horizontal rule under header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 58), pymupdf.Point(523, 58))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

        # Chapter indicator at top right
        for ch in chapters:
            if ch["start"] <= i < ch["end"]:
                page.insert_text(
                    pymupdf.Point(350, 50),
                    ch["title"].split(":")[0],
                    fontsize=8,
                    fontname="helv",
                    color=(0.5, 0.5, 0.5),
                )
                break

        # Section title
        page.insert_text(
            pymupdf.Point(72, 100),
            title,
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )

        # Body text
        body_rect = pymupdf.Rect(72, 130, 523, 750)
        page.insert_textbox(
            body_rect,
            body,
            fontsize=11,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Add some visual elements to certain pages (boxes, shapes)
        if i % 5 == 2:
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(100, 400, 495, 600))
            shape.finish(color=(0.6, 0.6, 0.8), fill=(0.93, 0.93, 0.97), width=1)
            shape.commit()
            page.insert_text(
                pymupdf.Point(120, 430),
                "[Illustration placeholder]",
                fontsize=10,
                fontname="heit",
                color=(0.5, 0.5, 0.7),
            )

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(280, 810),
            str(i + 1),
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # Set chapter bookmarks (TOC) - NO figure bookmarks
    toc = [
        [1, "Chapter 1: Introduction to Visual Design", 1],
        [2, "The History of Visual Communication", 2],
        [2, "Principles of Design", 3],
        [2, "Design Thinking Process", 4],
        [1, "Chapter 2: Color Theory and Application", 5],
        [2, "Understanding Color", 5],
        [2, "The Color Wheel and Harmonies", 6],
        [2, "Color Psychology in Design", 7],
        [2, "Digital Color Systems", 8],
        [2, "Advanced Color Techniques", 9],
        [1, "Chapter 3: Typography and Layout", 10],
        [2, "Foundations of Typography", 10],
        [2, "Typeface Classification", 11],
        [2, "Font Pairing and Hierarchy", 12],
        [2, "Grid Systems and Layout", 13],
        [2, "White Space and Composition", 14],
        [2, "Responsive Typography", 16],
        [1, "Chapter 4: Illustration Techniques", 17],
        [2, "Introduction to Illustration", 17],
        [2, "Vector Illustration", 18],
        [2, "Raster Illustration", 19],
        [2, "Isometric and Technical Illustration", 20],
        [2, "Character Design", 21],
        [2, "Infographic Design", 22],
        [2, "Motion and Animation Basics", 23],
        [1, "Chapter 5: Digital Media Production", 24],
        [2, "Digital Asset Management", 24],
        [2, "Image Optimization", 25],
        [2, "Video Production", 26],
        [2, "Audio Design", 27],
        [2, "Interactive Media and UX", 28],
        [2, "Accessibility in Digital Design", 29],
        [2, "Cross-Platform Design", 30],
        [1, "Chapter 6: Print and Publication", 31],
        [2, "Print Production Essentials", 31],
        [2, "Prepress and File Preparation", 32],
        [2, "Binding and Finishing", 33],
        [2, "Publication Layout", 34],
        [2, "Sustainable Print Practices", 35],
        [1, "Chapter 7: Portfolio and Presentation", 36],
        [2, "Building a Design Portfolio", 36],
        [2, "Presentation Design Principles", 37],
        [2, "Client Communication", 38],
        [2, "Career Development", 39],
        [2, "Conclusion: The Future of Visual Design", 40],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify
    doc2 = pymupdf.open(OUTPUT)
    print(f'Pages: {doc2.page_count}')
    existing_toc = doc2.get_toc()
    print(f'Bookmark entries: {len(existing_toc)}')
    for entry in existing_toc[:5]:
        print(f'  {entry}')
    doc2.close()

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
