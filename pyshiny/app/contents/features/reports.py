"""
Takes in a id and generates a PNG file used to visualize how the report would look like
and also generates a PDF file to be downloaded when needed

Author: Jesse Liu
"""

import os
import img2pdf
from PIL import Image
from contents.features.query import Query
from html2image import Html2Image  # requires "requests" module
from jinja2 import FileSystemLoader, Environment


class Report:

    def __init__(self, db_id):
        self.req_path = os.path.join(os.path.dirname(__file__), '../utils/req/')
        self.tmp_path = os.path.join(os.path.dirname(__file__), '../utils/tmp/')
        self.template_file = 'report_template.html'
        self.report_edit = 'report_edit.html'
        self.image_file = 'report_image.png'
        self.image_crop = 'image_crop.png'
        self.report_file = 'temp_report.pdf'
        self.db = Query().query_by_id(db_id)

    # Creates a PDF report file from the PNG file that is used as the output for the download
    def generate_full_report(self):
        pdf_file = self.convert_to_pdf()
        return pdf_file

    # Creates a PNG report file from the HTML file that is used as the output for the report pill card
    def generate_temp_report(self):
        html_file = self.edit_template()
        image_file = self.convert_to_png(html_file)
        return image_file

    # Grabs the location of the HTML report template file and edits the variables within it using inputs from a db row
    def edit_template(self):
        loader = FileSystemLoader(searchpath=self.tmp_path)
        env = Environment(loader=loader)
        copied_file = self.copy_file()
        template = env.get_template(copied_file)
        text = template.render(
            columns = column
        )
        html_file = open(self.tmp_path + copied_file, 'w')
        html_file.write(text)
        html_file.close()
        return html_file.name

    # Copies and preserves the template file onto a new HTML file to be edited
    def copy_file(self):
        template_path = os.path.join(self.req_path, self.template_file)
        edit_path = os.path.join(self.tmp_path, self.report_edit)
        with open(template_path, 'r') as template, open(edit_path, 'w') as edit:
            for line in template:
                edit.write(line)
        return self.report_edit

    # Converts the HTML file to PNG file for visualization
    def convert_to_png(self, html_file):
        with open(html_file) as f:
            Html2Image(output_path=self.tmp_path).screenshot(f.read(), save_as=self.image_file, size=(1920, 1700))
        return self.image_file

    # Converts the PNG file to PDF file for downloading
    def convert_to_pdf(self):
        img_path = os.path.join(self.tmp_path, self.image_file)
        image = Image.open(img_path)
        image = image.crop((0, 100, 1228, 3370))
        image.save(img_path)
        image = Image.open(img_path)
        pdf_bytes = img2pdf.convert(image.filename)
        pdf_path = os.path.join(self.tmp_path, self.report_file)
        file = open(pdf_path, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
        return self.report_file
