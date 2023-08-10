"""
Runs ... and send the file to email

Author: Jesse Liu
"""

from report_scraping import Report
from report_cleaning import Cleaning
from send_email import Email
from connection import SQL
import yaml
import os


with open(os.path.join(os.path.dirname(__file__), '../../.info/env.yaml'), 'r') as yml:
    env = yaml.safe_load(yml)

if __name__ == '__main__':
    SQL(env).run_query()
    Report().scrape()
    Cleaning().clean()
    Email(env).send_email()
