"""
General utils code

Author: Jesse Liu
"""

from io import BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from shiny.types import FileInfo
from contents.features.query import Query
import os
import pandas as pd


# Stores the choices for the filters and also used as categorical results
def choices():
    choice_file = pd.read_csv(os.path.join(os.path.dirname(__file__), 'req/choices.csv'))

    # choices

    categories = {'': [],
                  'Columns': column_choices
                  }

    return categories


# Creates a table from the MGP file inputted and outputs a df table
def create_mgp_table(file):
    # task
        return file_html


# Convert from MGP to WF
def convert_mgp_to(file):
    # task
        return mgp_df


# Takes a PDF and converts it to HTML
def convert_pdf_to_html(filename):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    fp = open(filename, 'rb')
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    text = retstr.getvalue().decode()
    fp.close()
    device.close()
    retstr.close()

    with open('report_{}.html'.format(codec), 'w') as out:
        out.write(text)


if __name__ == '__main__':
    convert_pdf_to_html(os.path.join(os.path.dirname(__file__), 'filename.pdf'))
