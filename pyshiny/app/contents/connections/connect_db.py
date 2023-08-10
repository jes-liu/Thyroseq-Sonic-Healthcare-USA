"""
Creates a connection to the local DB in SQLite
In the future, changes will be made to connect to a new DB server

Author: Jesse Liu
"""

import os
import sqlite3


class Connect:

    def __init__(self):
        self.db_name = os.path.join(os.path.dirname(__file__), '../utils/req/file')
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.MESSAGE_SUCCESS = 'Connection Successful'
        self.MESSAGE_FAIL = 'Connection Failed'

    # Check if the connection is successful or fail; returns a message based on result
    def check_connection(self):
        """
        :param
        :return: success or fail connection message
        """

        if self.cursor:
            message = self.MESSAGE_SUCCESS
        else:
            message = self.MESSAGE_FAIL

        return print(message)

    # Opens the connection to the database
    def open_connection(self):
        """
        :param
        :return: the connection of said database as a cursor
        """
        if os.path.exists(self.db_name):
            print('Database Exists... Connecting....')
            self.check_connection()
            return self.cursor
        else:
            return print('ERROR: Database Does Not Exist')

    # Closes the connection to the database
    def close_connection(self):
        """
        :param
        :return: verification message that the connection is closed
        """

        self.conn.close()
        return print('Connection Closed')
