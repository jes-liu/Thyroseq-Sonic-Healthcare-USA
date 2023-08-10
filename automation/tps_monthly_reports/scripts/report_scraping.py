"""
Read PDF files and grab info

Author: Jesse Liu
"""

import os
import pandas as pd
from pathlib import Path
import PyPDF2
pd.options.mode.chained_assignment = None

class Report:

    def __init__(self):
        self.input_file = pd.read_csv(os.path.join(os.path.dirname(__file__), '../output/file_output.csv'))
        self.output_file = os.path.join(os.path.dirname(__file__), '../output/file_scraped.csv')

    def get_info(self, text):

        # break up the text using headers
	pre_info = {}        

        # fixing some items in the dicts
	post_info = {}
        if text.find('word') != -1:
            post_info['key'] = 'value'
            try:
                for key, value in pre_info.items():
                    # task
            except IndexError or ValueError or TypeError or KeyError as s:
                post_info['key'] = s
        else:
            # something

        # deletion of unwanted keys
        tbl_del = ['key names']
	

        for var in tbl_del:
            try:
                del pre_info[var]
            except:
                pass

        info = {**post_info, **pre_info}  # prioritizes pre_info

        return info

    def get_second_info(self, text, row):
        # more text info
        return info

    def scrape(self):
        tbl = self.input_file
        print('SCRAPING STARTED')

        tbl = tbl.drop_duplicates(subset='column', keep="last")
        num_ = len(tbl)
        print('Number of ... this Month: {}'.format(num_))

        # read pdf into text
        for i, row in tbl.iterrows():
            if pd.isnull(row['filePath']):
                continue
            elif Path(row['col']).is_file():
                reader = PyPDF2.PdfReader(row['col'])
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                text = ''.join(text)
                info = self.get_info(text)
		
		# more tasks here

                
        output_tbl = tbl[['column_name']]

        output_tbl.to_csv(self.output_file, index=False)

        return print('... SCRAPED')
