"""
Runs ...

Author: Jesse Liu
"""

from connection import SQL
from send_email import Email
import yaml
import os


with open(os.path.join(os.path.dirname(__file__), '../../.info/env.yaml'), 'r') as yml:
    env = yaml.safe_load(yml)

if __name__ == '__main__':
    SQL(env).run_query()
    Email(env).send_email()
