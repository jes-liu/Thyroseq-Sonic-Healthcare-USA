"""
Creates a connection to TPS, runs a query, and saves info in csv

Author: Jesse Liu
"""

import jaydebeapi
import pandas as pd
import os


class SQL:

    def __init__(self, env):
        self.env = env
        self.output_file = os.path.join(os.path.dirname(__file__), '../output/file.csv')
        self.query_file = os.path.join(os.path.dirname(__file__), 'query.sql')

    # Opens the connection to the database
    def open_connection(self):
        driver_name = self.env['Environment']['DRIVER_NAME']
        connection_url = self.env['Environment']['CONNECTION_URL']
        connection_properties = self.env['Environment']['CONNECTION_PROPERTIES']
        jar_path = os.path.join(os.path.join(os.path.dirname(__file__), '../../.info'), self.env['Environment']['JAR'])

        conn = jaydebeapi.connect(driver_name, connection_url, connection_properties, jar_path)
        print('DATABASE EXISTS... CONNECTING....')

        if conn:
            print('CONNECTED')
        else:
            print('FAILED CONNECTION')

        return conn

    # Closes the connection to the database
    @staticmethod
    def close_connection(conn):
        conn.close()
        return print('CONNECTION CLOSED')

    # Grab the query and run it
    def run_query(self):
        conn = self.open_connection()
        cursor = conn.cursor()

        cursor.execute(self.query())
        col_names = [description[0] for description in cursor.description]
        query_df = pd.DataFrame(cursor.fetchall(), columns=col_names)

        query_df.to_csv(self.output_file, index=False)
        self.close_connection(conn)

        return query_df

    # Create query
    def query(self):
        with open(self.query_file, 'r') as sql:
            query = sql.read()
        return query
