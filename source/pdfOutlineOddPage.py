# cpps2md - pdfOutlineOddPage
# jamhus_tao @ 2023
import os
import sys
import pypdf
import tkinter
from tkinter import filedialog


PATH_INPUT = ""
PATH_OUTPUT = ""


def ask():
    global PATH_INPUT, PATH_OUTPUT
    if len(sys.argv) == 2:
        PATH_INPUT = sys.argv[1]
    else:
        _app = tkinter.Tk()
        _app.withdraw()
        PATH_INPUT = filedialog.askopenfilename(filetypes=[("PDF", ("*.PDF", ))], initialdir="../.out")
    PATH_OUTPUT = os.path.splitext(PATH_INPUT)
    PATH_OUTPUT = PATH_OUTPUT[0] + "OutlineOddPage" + PATH_OUTPUT[1]
    if os.path.isfile(PATH_INPUT) and os.path.splitext(PATH_INPUT)[1].lower() == ".pdf":
        print("Output Path is {}.".format(PATH_OUTPUT))
    else:
        print("Uncorrected File Format {}.".format(PATH_INPUT))
        exit()


def done():
    reader = pypdf.PdfReader(PATH_INPUT)
    outlines = reader.outline
    page_numbers = []
    for outline in outlines:
        if not isinstance(outline, list):
            page_numbers.append(reader.get_page_number(outline.page))

    writer = pypdf.PdfWriter()
    writer.clone_document_from_reader(reader)
    cnt = 0
    for page_number in page_numbers:
        if (cnt + page_number) % 2:
            writer.insert_blank_page(595, 842, index=cnt + page_number)
            cnt += 1
    writer.write(PATH_OUTPUT)
    writer.close()


if __name__ == "__main__":
    ask()
    done()
