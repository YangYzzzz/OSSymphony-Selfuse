"""
Initial Setup: Add a new subdocument 'Appendix_B_Glossary.odt' at the end of the master document
Task ID: writer_rm_061
Domain: libreoffice_writer

Creates:
  - Textbook_Master.odm (master document with 12 subdocuments)
  - Preface.odt, Ch1.odt..Ch10.odt, Appendix_A_References.odt (subdocuments)
  - Appendix_B_Glossary.odt (standalone, NOT yet in master)
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
from odf.opendocument import OpenDocumentText
from odf.text import P, H, Section
from odf import text as odftext

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_061'


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


def create_odt(filepath, title, paragraphs):
    """Create a simple .odt file with a title and paragraphs."""
    doc = OpenDocumentText()
    h = H(outlinelevel=1)
    h.addText(title)
    doc.text.addElement(h)
    for para_text in paragraphs:
        p = P()
        p.addText(para_text)
        doc.text.addElement(p)
    doc.save(filepath)


def create_master_odm(filepath, subdoc_paths):
    """
    Create a .odm master document that references subdocuments.
    ODM is essentially an ODF text doc with section links.
    We build it using odfpy with text:section elements containing text:section-source.
    """
    doc = OpenDocumentText()

    # Add a title
    h = H(outlinelevel=1)
    h.addText("Introduction to Computer Science: A Comprehensive Textbook")
    doc.text.addElement(h)

    p = P()
    p.addText("This master document compiles all chapters and appendices of the textbook.")
    doc.text.addElement(p)

    # Add section links to each subdocument
    for i, subdoc_path in enumerate(subdoc_paths):
        basename = os.path.basename(subdoc_path)
        section_name = basename.replace('.odt', '')

        # Create a text:section with text:section-source pointing to the subdocument
        section = Section(name=section_name)
        from odf.text import SectionSource
        source = SectionSource()
        source.setAttribute('href', basename)
        source.setAttrNS('http://www.w3.org/1999/xlink', 'xlink:href', basename)
        source.setAttrNS('http://www.w3.org/1999/xlink', 'xlink:type', 'simple')
        section.addElement(source)

        # Add placeholder paragraph inside section
        sp = P()
        sp.addText(f"[Content from {basename}]")
        section.addElement(sp)

        doc.text.addElement(section)

    # Save as .odt first, then rename to .odm
    temp_path = filepath + '.tmp.odt'
    doc.save(temp_path)

    # Convert .odt to .odm by changing the mimetype inside the zip
    shutil.copy(temp_path, filepath)
    # Patch the mimetype entry in the zip to be the master doc type
    _patch_odm_mimetype(filepath)
    os.remove(temp_path)


def _patch_odm_mimetype(filepath):
    """
    Rewrite the ODF file changing the mimetype to master document type.
    ODM mimetype: application/vnd.oasis.opendocument.text-master
    """
    import io
    temp_path = filepath + '.rewrite'

    with zipfile.ZipFile(filepath, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'mimetype':
                    data = b'application/vnd.oasis.opendocument.text-master'
                    # mimetype must be stored uncompressed
                    zout.writestr(item, data, compress_type=zipfile.ZIP_STORED)
                elif item.filename == 'content.xml':
                    # Also update the office:document-content mimetype attribute
                    content = data.decode('utf-8')
                    content = content.replace(
                        'application/vnd.oasis.opendocument.text',
                        'application/vnd.oasis.opendocument.text-master'
                    )
                    zout.writestr(item, content.encode('utf-8'))
                elif item.filename == 'meta.xml':
                    meta = data.decode('utf-8')
                    meta = meta.replace(
                        'application/vnd.oasis.opendocument.text',
                        'application/vnd.oasis.opendocument.text-master'
                    )
                    zout.writestr(item, meta.encode('utf-8'))
                elif item.filename == 'manifest.xml' or item.filename == 'META-INF/manifest.xml':
                    manifest = data.decode('utf-8')
                    manifest = manifest.replace(
                        'application/vnd.oasis.opendocument.text',
                        'application/vnd.oasis.opendocument.text-master'
                    )
                    zout.writestr(item, manifest.encode('utf-8'))
                else:
                    zout.writestr(item, data)

    os.replace(temp_path, filepath)


def create_initial():
    # Define subdocument content
    subdocs = {
        'Preface.odt': {
            'title': 'Preface',
            'paragraphs': [
                'Welcome to "Introduction to Computer Science," a comprehensive textbook designed for first-year undergraduate students.',
                'This textbook covers fundamental concepts from algorithms and data structures to operating systems and networking.',
                'Each chapter builds upon the previous one, creating a cohesive learning journey through the core principles of computing.',
                'We extend our gratitude to the many reviewers and contributors who helped shape this edition.',
                'Special thanks to Dr. Elena Vasquez for her invaluable feedback on the algorithms chapters.',
            ]
        },
        'Ch1.odt': {
            'title': 'Chapter 1: Introduction to Computing',
            'paragraphs': [
                'Computing has fundamentally transformed every aspect of modern society, from healthcare to entertainment.',
                'The field traces its roots to the pioneering work of Alan Turing, who formalized the concept of computation in 1936.',
                'A computer system consists of hardware components and software that work together to process information.',
                'The von Neumann architecture, proposed in 1945, remains the foundation of most modern computers.',
                'Binary representation allows computers to encode all forms of data using just two symbols: 0 and 1.',
                'Understanding numbering systems, including binary, octal, and hexadecimal, is essential for any computer scientist.',
            ]
        },
        'Ch2.odt': {
            'title': 'Chapter 2: Programming Fundamentals',
            'paragraphs': [
                'Programming is the process of creating instructions that a computer can execute to solve specific problems.',
                'Variables store data values that can be referenced and manipulated throughout a program.',
                'Control structures such as if-else statements and loops direct the flow of program execution.',
                'Functions allow programmers to organize code into reusable, modular components.',
                'Debugging is the systematic process of identifying and fixing errors in computer programs.',
            ]
        },
        'Ch3.odt': {
            'title': 'Chapter 3: Data Structures',
            'paragraphs': [
                'Data structures are specialized formats for organizing and storing data efficiently.',
                'Arrays provide contiguous memory allocation for elements of the same type, enabling O(1) random access.',
                'Linked lists offer dynamic memory allocation but sacrifice random access for efficient insertion and deletion.',
                'Stacks follow the Last-In-First-Out (LIFO) principle, commonly used in function call management.',
                'Queues implement First-In-First-Out (FIFO) ordering, essential for task scheduling and buffering.',
                'Trees are hierarchical structures where binary search trees enable O(log n) search operations.',
            ]
        },
        'Ch4.odt': {
            'title': 'Chapter 4: Algorithms and Complexity',
            'paragraphs': [
                'An algorithm is a finite sequence of well-defined steps that produces a correct output for any valid input.',
                'Big-O notation describes the upper bound of an algorithm\'s time or space complexity as input size grows.',
                'Sorting algorithms like merge sort achieve O(n log n) time complexity, which is optimal for comparison-based sorting.',
                'Divide and conquer strategies break problems into smaller subproblems that are solved recursively.',
                'Dynamic programming optimizes solutions by storing intermediate results to avoid redundant calculations.',
            ]
        },
        'Ch5.odt': {
            'title': 'Chapter 5: Object-Oriented Programming',
            'paragraphs': [
                'Object-oriented programming organizes software design around data objects rather than functions and logic.',
                'Encapsulation bundles data and methods that operate on that data within a single unit called a class.',
                'Inheritance allows new classes to derive properties and behaviors from existing parent classes.',
                'Polymorphism enables objects of different types to respond to the same method call in type-specific ways.',
                'The SOLID principles guide developers in creating maintainable and extensible object-oriented systems.',
            ]
        },
        'Ch6.odt': {
            'title': 'Chapter 6: Operating Systems',
            'paragraphs': [
                'An operating system manages computer hardware and provides services for application programs.',
                'Process management involves creating, scheduling, and terminating processes and threads.',
                'Memory management techniques include paging, segmentation, and virtual memory systems.',
                'File systems organize data on storage devices using hierarchical directory structures.',
                'The kernel is the core component that provides the most fundamental services of an operating system.',
            ]
        },
        'Ch7.odt': {
            'title': 'Chapter 7: Computer Networks',
            'paragraphs': [
                'Computer networking enables communication and resource sharing between interconnected computing devices.',
                'The OSI model defines seven layers of network communication, from physical transmission to application protocols.',
                'TCP/IP is the foundational protocol suite of the Internet, providing reliable end-to-end data transmission.',
                'Network security encompasses firewalls, encryption, and authentication mechanisms to protect data in transit.',
                'The Domain Name System (DNS) translates human-readable domain names into numerical IP addresses.',
            ]
        },
        'Ch8.odt': {
            'title': 'Chapter 8: Databases',
            'paragraphs': [
                'Database management systems provide structured approaches to storing, retrieving, and managing large datasets.',
                'The relational model organizes data into tables with rows and columns, enforcing data integrity through constraints.',
                'SQL (Structured Query Language) is the standard language for interacting with relational databases.',
                'Normalization reduces data redundancy by organizing tables according to formal rules called normal forms.',
                'NoSQL databases offer flexible schemas and horizontal scaling for applications with rapidly changing data requirements.',
            ]
        },
        'Ch9.odt': {
            'title': 'Chapter 9: Software Engineering',
            'paragraphs': [
                'Software engineering applies systematic, disciplined approaches to the development and maintenance of software systems.',
                'The software development lifecycle includes requirements gathering, design, implementation, testing, and deployment.',
                'Agile methodologies emphasize iterative development, continuous feedback, and adaptive planning.',
                'Version control systems like Git track changes to source code and facilitate collaboration among developers.',
                'Software testing ensures that programs function correctly through unit tests, integration tests, and system tests.',
            ]
        },
        'Ch10.odt': {
            'title': 'Chapter 10: Artificial Intelligence',
            'paragraphs': [
                'Artificial intelligence encompasses systems that can perform tasks typically requiring human intelligence.',
                'Machine learning algorithms improve their performance on tasks through experience and exposure to data.',
                'Neural networks, inspired by biological brain structures, form the basis of modern deep learning systems.',
                'Natural language processing enables computers to understand, interpret, and generate human language.',
                'Computer vision systems can analyze and interpret visual information from images and video streams.',
                'Reinforcement learning trains agents to make sequential decisions by maximizing cumulative rewards.',
            ]
        },
        'Appendix_A_References.odt': {
            'title': 'Appendix A: References',
            'paragraphs': [
                'Abelson, H., & Sussman, G. J. (1996). Structure and Interpretation of Computer Programs. MIT Press.',
                'Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms (3rd ed.). MIT Press.',
                'Knuth, D. E. (1997). The Art of Computer Programming, Volume 1: Fundamental Algorithms (3rd ed.). Addison-Wesley.',
                'Patterson, D. A., & Hennessy, J. L. (2014). Computer Organization and Design (5th ed.). Morgan Kaufmann.',
                'Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). Operating System Concepts (10th ed.). Wiley.',
                'Tanenbaum, A. S., & Wetherall, D. J. (2011). Computer Networks (5th ed.). Pearson.',
                'Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.',
                'Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns. Addison-Wesley.',
            ]
        },
    }

    # Appendix B exists as standalone file but NOT in master doc
    appendix_b = {
        'title': 'Appendix B: Glossary of Terms',
        'paragraphs': [
            'Algorithm: A step-by-step procedure for solving a problem or accomplishing a task in a finite number of steps.',
            'API (Application Programming Interface): A set of protocols and tools for building software applications that specify how components should interact.',
            'Binary: A base-2 numeral system that uses only two digits, 0 and 1, to represent all values.',
            'Cache: A hardware or software component that stores data so future requests for that data can be served faster.',
            'Compiler: A program that translates source code written in a high-level programming language into machine code.',
            'Database: An organized collection of structured information stored electronically in a computer system.',
            'Encryption: The process of encoding information so that only authorized parties can access and read it.',
            'Firewall: A network security system that monitors and controls incoming and outgoing network traffic.',
            'GUI (Graphical User Interface): A visual interface that allows users to interact with electronic devices through icons and visual indicators.',
            'Hash Function: A function that maps data of arbitrary size to fixed-size values, commonly used in data structures and cryptography.',
            'IDE (Integrated Development Environment): A software suite that provides comprehensive facilities for software development.',
            'JSON (JavaScript Object Notation): A lightweight data interchange format that is easy for humans to read and write.',
            'Kernel: The core component of an operating system that manages system resources and hardware communication.',
            'Latency: The time delay between a cause and its effect, commonly measured in networking as round-trip time.',
            'Middleware: Software that acts as a bridge between an operating system or database and applications.',
            'Namespace: A container that holds a set of identifiers and allows disambiguation of homonymous identifiers.',
            'Object: An instance of a class that encapsulates data and behavior in object-oriented programming.',
            'Protocol: A set of rules governing the format and transmission of data between computing devices.',
            'Query: A request for data or information from a database, typically written in SQL or similar languages.',
            'Recursion: A method of solving a problem where the solution depends on solutions to smaller instances of the same problem.',
            'Stack: A linear data structure that follows the Last-In-First-Out (LIFO) principle for element access.',
            'Thread: The smallest sequence of programmed instructions that can be managed independently by a scheduler.',
            'URL (Uniform Resource Locator): A reference to a web resource that specifies its location on a computer network.',
            'Variable: A named storage location in memory that holds a value which can be modified during program execution.',
            'XML (Extensible Markup Language): A markup language that defines rules for encoding documents in a human-readable and machine-readable format.',
        ]
    }

    # Create all subdocument .odt files
    for filename, content in subdocs.items():
        filepath = os.path.join(WORKDIR, filename)
        create_odt(filepath, content['title'], content['paragraphs'])
        print(f'Created subdocument: {filepath}')

    # Create Appendix_B_Glossary.odt (standalone, NOT in master)
    appendix_b_path = os.path.join(WORKDIR, 'Appendix_B_Glossary.odt')
    create_odt(appendix_b_path, appendix_b['title'], appendix_b['paragraphs'])
    print(f'Created standalone file: {appendix_b_path}')

    # Create master document with only the original 12 subdocuments
    subdoc_paths = [os.path.join(WORKDIR, f) for f in subdocs.keys()]
    master_path = os.path.join(WORKDIR, 'Textbook_Master.odm')
    create_master_odm(master_path, subdoc_paths)
    print(f'Master document created: {master_path}')

    # GUI-ready: open master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{master_path}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with Textbook_Master.odm')


create_initial()
