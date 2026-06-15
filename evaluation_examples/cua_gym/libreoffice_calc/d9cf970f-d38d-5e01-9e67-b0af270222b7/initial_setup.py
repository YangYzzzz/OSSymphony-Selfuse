"""
Initial Setup: Librarian reading list ISBN lookup task
Task ID: osworld_multi_apps_web_references_007
Domain: multi_apps (libreoffice_writer + libreoffice_calc)

Creates:
  - /home/user/Documents/course_readings.odt  — Writer doc with 10 CS books (no ISBNs)
  - /home/user/Desktop/isbn_tracker.ods       — Calc sheet with Title/Author/ISBN_13/OpenLibrary_URL headers (ISBN_13 and URL columns empty)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_references_007'
WRITER_PATH = f'{WORKDIR}/Documents/course_readings.odt'
CALC_PATH = f'{WORKDIR}/Desktop/isbn_tracker.ods'


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


def create_writer_doc():
    """Create course_readings.odt with 10 CS books (no ISBNs)."""
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import P, Span

    doc = OpenDocumentText()

    # Define bold text style (using keyword arguments for odfpy)
    label_style = Style(name="LabelStyle", family="text")
    label_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(label_style)

    text = doc.text

    # Title paragraph
    title_para = P()
    title_span = Span(stylename="LabelStyle")
    title_span.addText("Course Reading List — Computer Science Fundamentals")
    title_para.addElement(title_span)
    text.addElement(title_para)

    # Empty line
    text.addElement(P())

    intro_para = P()
    intro_para.addText(
        "The following is a required reading list for advanced computer science studies. "
        "Each entry includes the book title, author(s), and publisher. "
        "Please verify ISBN-13 numbers via OpenLibrary (https://openlibrary.org/) for library catalog entry."
    )
    text.addElement(intro_para)

    # Empty separator
    text.addElement(P())

    # Book data: (title, authors, publisher, year)
    books = [
        (
            "The Art of Computer Programming, Vol. 1",
            "Donald E. Knuth",
            "Addison-Wesley Professional",
            "2011"
        ),
        (
            "Introduction to Algorithms",
            "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
            "MIT Press",
            "2009"
        ),
        (
            "Design Patterns: Elements of Reusable Object-Oriented Software",
            "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (Gang of Four)",
            "Addison-Wesley Professional",
            "1994"
        ),
        (
            "Structure and Interpretation of Computer Programs",
            "Harold Abelson, Gerald Jay Sussman",
            "MIT Press",
            "1996"
        ),
        (
            "Clean Code: A Handbook of Agile Software Craftsmanship",
            "Robert C. Martin",
            "Prentice Hall",
            "2008"
        ),
        (
            "The Pragmatic Programmer: Your Journey to Mastery",
            "David Thomas, Andrew Hunt",
            "Addison-Wesley Professional",
            "2019"
        ),
        (
            "Code Complete: A Practical Handbook of Software Construction",
            "Steve McConnell",
            "Microsoft Press",
            "2004"
        ),
        (
            "Algorithms",
            "Robert Sedgewick, Kevin Wayne",
            "Addison-Wesley Professional",
            "2011"
        ),
        (
            "Computer Networks",
            "Andrew S. Tanenbaum, David J. Wetherall",
            "Pearson",
            "2010"
        ),
        (
            "Operating System Concepts",
            "Abraham Silberschatz, Peter Baer Galvin, Greg Gagne",
            "Wiley",
            "2018"
        ),
    ]

    for i, (title, authors, publisher, year) in enumerate(books, 1):
        # Book number line
        book_num_para = P()
        book_num_span = Span(stylename="LabelStyle")
        book_num_span.addText(f"Book {i}:")
        book_num_para.addElement(book_num_span)
        text.addElement(book_num_para)

        # Title line
        title_para = P()
        title_label = Span(stylename="LabelStyle")
        title_label.addText("Title: ")
        title_para.addElement(title_label)
        title_para.addText(title)
        text.addElement(title_para)

        # Author line
        author_para = P()
        author_label = Span(stylename="LabelStyle")
        author_label.addText("Author(s): ")
        author_para.addElement(author_label)
        author_para.addText(authors)
        text.addElement(author_para)

        # Publisher line
        pub_para = P()
        pub_label = Span(stylename="LabelStyle")
        pub_label.addText("Publisher: ")
        pub_para.addElement(pub_label)
        pub_para.addText(publisher)
        text.addElement(pub_para)

        # Year line
        year_para = P()
        year_label = Span(stylename="LabelStyle")
        year_label.addText("Year: ")
        year_para.addElement(year_label)
        year_para.addText(year)
        text.addElement(year_para)

        # ISBN note (explicitly empty / to be looked up)
        isbn_para = P()
        isbn_label = Span(stylename="LabelStyle")
        isbn_label.addText("ISBN-13: ")
        isbn_para.addElement(isbn_label)
        isbn_para.addText("[To be verified via OpenLibrary]")
        text.addElement(isbn_para)

        # Separator blank line
        text.addElement(P())

    # Ensure Documents directory exists
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)
    doc.save(WRITER_PATH)
    print(f'Writer document created: {WRITER_PATH}')


def create_calc_sheet():
    """Create isbn_tracker.ods with headers and 10 book rows (ISBN_13 and URL empty)."""
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell, TableColumn
    from odf.text import P
    from odf.style import Style, TextProperties, TableCellProperties, TableColumnProperties

    doc = OpenDocumentSpreadsheet()

    # Header style (bold text, blue background, white font)
    header_style = Style(name="HeaderStyle", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(header_style)

    # Column width styles
    col_style_a = Style(name="ColA", family="table-column")
    col_style_a.addElement(TableColumnProperties(columnwidth="3.5in"))
    doc.automaticstyles.addElement(col_style_a)

    col_style_b = Style(name="ColB", family="table-column")
    col_style_b.addElement(TableColumnProperties(columnwidth="2.5in"))
    doc.automaticstyles.addElement(col_style_b)

    col_style_c = Style(name="ColC", family="table-column")
    col_style_c.addElement(TableColumnProperties(columnwidth="1.8in"))
    doc.automaticstyles.addElement(col_style_c)

    col_style_d = Style(name="ColD", family="table-column")
    col_style_d.addElement(TableColumnProperties(columnwidth="3.0in"))
    doc.automaticstyles.addElement(col_style_d)

    table = Table(name="ISBN Tracker")

    table.addElement(TableColumn(stylename="ColA"))
    table.addElement(TableColumn(stylename="ColB"))
    table.addElement(TableColumn(stylename="ColC"))
    table.addElement(TableColumn(stylename="ColD"))

    def make_cell(text_val, style=None):
        if style:
            cell = TableCell(stylename=style, valuetype="string")
        else:
            cell = TableCell(valuetype="string")
        p = P()
        p.addText(str(text_val) if text_val is not None else "")
        cell.addElement(p)
        return cell

    def make_empty_cell():
        cell = TableCell(valuetype="string")
        p = P()
        p.addText("")
        cell.addElement(p)
        return cell

    # Header row
    header_row = TableRow()
    header_row.addElement(make_cell("Title", style="HeaderStyle"))
    header_row.addElement(make_cell("Author", style="HeaderStyle"))
    header_row.addElement(make_cell("ISBN_13", style="HeaderStyle"))
    header_row.addElement(make_cell("OpenLibrary_URL", style="HeaderStyle"))
    table.addElement(header_row)

    # Book data rows (ISBN_13 and URL empty — to be filled by agent)
    books = [
        ("The Art of Computer Programming, Vol. 1", "Donald E. Knuth"),
        ("Introduction to Algorithms", "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein"),
        ("Design Patterns: Elements of Reusable Object-Oriented Software", "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides"),
        ("Structure and Interpretation of Computer Programs", "Harold Abelson, Gerald Jay Sussman"),
        ("Clean Code: A Handbook of Agile Software Craftsmanship", "Robert C. Martin"),
        ("The Pragmatic Programmer: Your Journey to Mastery", "David Thomas, Andrew Hunt"),
        ("Code Complete: A Practical Handbook of Software Construction", "Steve McConnell"),
        ("Algorithms", "Robert Sedgewick, Kevin Wayne"),
        ("Computer Networks", "Andrew S. Tanenbaum, David J. Wetherall"),
        ("Operating System Concepts", "Abraham Silberschatz, Peter Baer Galvin, Greg Gagne"),
    ]

    for title, author in books:
        row = TableRow()
        row.addElement(make_cell(title))
        row.addElement(make_cell(author))
        row.addElement(make_empty_cell())   # ISBN_13 — empty
        row.addElement(make_empty_cell())   # OpenLibrary_URL — empty
        table.addElement(row)

    doc.spreadsheet.addElement(table)

    # Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)
    doc.save(CALC_PATH)
    print(f'Calc spreadsheet created: {CALC_PATH}')


def main():
    create_writer_doc()
    create_calc_sheet()

    # GUI-ready startup: open both documents
    # Open Writer document first
    launch_gui(f'libreoffice --writer "{WRITER_PATH}"', delay_sec=3.0)
    # Open Calc spreadsheet
    launch_gui(f'libreoffice --calc "{CALC_PATH}"', delay_sec=2.0)

    print('GUI_READY: launched LibreOffice Writer and Calc with DISPLAY=:0')


main()
