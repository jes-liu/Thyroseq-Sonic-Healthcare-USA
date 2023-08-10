"""
Runs the monthly QC plots from R and .sh and sends the pdf plot to email

Author: Jesse Liu
"""

from send_email import Email
import subprocess
import time
import yaml
import os


with open(os.path.join(os.path.dirname(__file__), '../.info/env.yaml'), 'r') as yml:
    env = yaml.safe_load(yml)

if __name__ == '__main__':
    print('QC GENERATING...')
    subprocess.call(['sh', os.path.join(os.path.dirname(__file__), 'QMR-generator.sh')])
    time.sleep(1800)
    print('QC DONE')
    Email(env).send_email()
