"""
Pulls the DB tables and populates the web app with the data

Author: Jesse Liu
"""

import pandas as pd
from contents.connections.connect_db import Connect


class Query:

    def __init__(self):
        self.query = self.create_query()

    # Grabs the initial base query that can be filtered
    @staticmethod
    def create_query():
        query = """
            SELECT *
            FROM db
            """
        return query

    def get_thyroseq_db(self, columns, limit, style, columns
                        ):

        conn = Connect().open_connection()

        # get the base query for all rows
        self.query = self.create_query()

        # customize the query by selection of columns
        self.query = self.select_columns(columns)

        self.query = self.filter_

        self.query = self.filter_

        self.query = self.filter_

        # more filters ...

        # sort by selection
        self.query = self.filter_sort(sort, descending)

        # after filtering for every category: add limit if True
        if limit[0]:
            self.query += """ LIMIT {} """.format(min(20, max(1, limit[1])))

        print(self.query)

        rows = conn.execute(self.query)
        col_names = [description[0] for description in conn.description]
        query_df = pd.DataFrame(rows, columns=col_names)
        Connect().close_connection()
	
	# puts a hyperlink into the database being display so it is clickable
        if style:
            styler = query_df.style.format({'col1': self.make_col1_clickable,
                                            'col2': self.make_col2_clickable}).\
                set_table_attributes('class="table-striped table"').\
                set_table_styles([dict(selector="th", props='text-align: center'),
                                  dict(selector="td", props='text-align: center')]).\
                hide(axis="index")
            return styler
        else:
            return query_df

    @staticmethod
    def query_by_id(db_id):
        conn = Connect().open_connection()
        query = """select * from db where id is {}""".format(db_id)
        rows = conn.execute(query)
        col_names = [description[0] for description in conn.description]
        query_df = pd.DataFrame(rows, columns=col_names)
        Connect().close_connection()
        return query_df


    def select_columns(self, columns):
        columns = ', '.join('"' + column + '"' for column in columns)
        new_query = """ SELECT {} FROM ({}) WHERE 1=1 """.format(columns, self.query)
        return new_query

    def filter_col(self, col):
        if col == '':
            pass
        else:
            self.query += """ AND Col = '{}' \n""".format(col)
        return self.query

    # other filter functions

    def filter_sort(self, sort, descending):
        if sort == '':
            pass
        else:
            self.query += """ ORDER BY "{}" """.format(sort)

            if descending:
                self.query += """ DESC, id \n"""
            else:
                self.query += """ ASC, id \n"""
        return self.query

    @staticmethod
    def make_col1_clickable(column):
        if column is None:
            pass
        else:
            transcript = column.split(',')
            term = ''
            for i, x in enumerate(col1):
                term += x + '[] OR'
            site = 'https://www.google.com/?term={}'.format(term)
            return '<a target="_blank" href="{}">{}</a>'.format(site, column)
