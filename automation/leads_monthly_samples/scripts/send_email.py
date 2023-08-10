"""
Sends out an email ... from Bx Team

Author: Jesse Liu
"""

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime as dt
import smtplib
import os


class Email:

    def __init__(self, env):
        self.env = env
        self.month = dt.date.today().strftime('%b%Y')
        self.first_dom = dt.date.today().replace(day=1).strftime('%d%b%Y')
        self.input_file = os.path.join(os.path.dirname(__file__), '../output/file.csv')
        self.filename = 'name_from_{}.csv'.format(self.first_dom)

    def create_message(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'subject_name {}'.format(self.month)
        msg['From'] = self.env['Email']['JESSE']
        msg['To'] = self.env['Email']['LEADS']
        msg['Cc'] = self.env['Email']['TSQBX']

        body = """
        Hi Leads,

        [Body]

        Best,
        TSQ Bx
        """
        msg.attach(MIMEText(body))

        with open(self.input_file, 'r') as file:
            attachment = MIMEApplication(file.read())
            attachment['Content-Disposition'] = 'attachment; filename={}'.format(self.filename)
        msg.attach(attachment)

        return msg

    def send_email(self):
        msg = self.create_message()
        host = self.env['Server']['HOST']
        port = self.env['Server']['PORT']

        smtp = smtplib.SMTP(host, port)
        smtp.sendmail(msg['From'], msg['To'].split(',') + msg['Cc'].split(','), msg.as_string())
        smtp.quit()

        print('EMAIL SENT')
