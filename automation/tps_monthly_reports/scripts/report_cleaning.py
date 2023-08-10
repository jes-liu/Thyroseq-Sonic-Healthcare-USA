"""
This file takes in the reports and cleans the data

Author: Jesse Liu
"""

import pandas as pd
import datetime
import re
import os


class Cleaning:

    def __init__(self):
        self.tbl = pd.read_csv(os.path.join(os.path.dirname(__file__), '../output/file_data.csv'))
        self.output_file = os.path.join(os.path.dirname(__file__), '../output/file_cleaned.csv')
    
    def clean_name(self):
        nrow = len(self.tbl)
        column = self.tbl["column"]
    
        exceptions = ['word']
        # check to see if value is IN one of these, not if they are equal to
        exceptions = '\t'.join(exceptions)
    
        for i in range(nrow):
            if str(column[i]).strip() in exceptions:
                pass
            else:
                column[i] = str(column[i]).strip() + ', ' + str(column[i]).strip()
    
        return self.tbl

    def clean_name(self):
        nrow = len(self.tbl)
        # task
    
        return self.tbl

    def change_date_format(self):
        # change the date format from 'mm/dd/yyyy' to 'yyyy-mm-dd'
        dates = ['date']
    
        for i in range(len(dates)):
            if dates[i] == 'date':
                for x, date in enumerate(self.tbl[dates[i]]):
                    try:
                        self.tbl.loc[x, dates[i]] = datetime.datetime.strptime(str(date), "%d-%b-%y").strftime("%Y-%m-%d").strip()
                    except ValueError:  # remove non-date values in the csv file
                        continue
            else:
                for x, date in enumerate(self.tbl[dates[i]]):
                    try:
                        self.tbl.loc[x, dates[i]] = datetime.datetime.strptime(str(date), "%m/%d/%y").strftime("%Y-%m-%d").strip()
                    except ValueError:  # remove non-date values in the csv file
                        continue
        return self.tbl

    def change_text_to_int(self):
        # task
    
        return self.tbl

    def strip_whitetext(self):
        # strips the leading and trailing white spaces for the following columns
        for i in range(len(self.tbl)):
            # task
    
        return self.tbl

    def fix_name(self):
        # task
        return self.tbl

    def fix_name(self):
        # task
        return self.tbl

    def clean_name(self):
        # task
        return self.tbl

    def reclean_name(self):
        # task
    
        return self.tbl

    def replace_nan(self):
        for i in range(len(self.tbl)):
            for j in range(len(self.tbl.columns)):
                if self.tbl.loc[i, self.tbl.columns[j]] == 'nan':
                    self.tbl.loc[i, self.tbl.columns[j]] = ''
        return self.tbl

    def clean(self):
        print('CLEANING...')
        self.tbl.dropna(how='all', inplace=True)  # drop the empty rows
        self.tbl = self.tbl.drop_duplicates()
        self.tbl.reset_index(drop=True, inplace=True)  # reset the index after dropping rows
        self.tbl = self.clean_name()
        self.tbl = self.clean_name()
        self.tbl = self.change_text_to_int()
        self.tbl = self.clean_name()
        self.tbl = self.clean_name()
        self.tbl = self.clean_name()
        self.tbl = self.clean_name()
        self.tbl = self.change_date_format()
        self.tbl = self.strip_whitetext()
        self.tbl = self.replace_nan()
    
        output_tbl = self.tbl[['column_names']]
    
        output_tbl.to_csv(self.output_file, index=False)
    
        return print('REPORT CLEANED')
