"""
Sends out an email

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
        self.last_month = (dt.date.today().replace(day=1) - dt.timedelta(days=1)).strftime('%b-%Y')
        self.input_file = os.path.join(os.path.dirname(__file__), '../output/file_cleaned.csv')
        self.filename = 'name.csv'

    def create_message(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'Monthly ... for {}'.format(self.last_month)
        msg['From'] = self.env['Email']['JESSE']
        msg['To'] = self.env['Email']['TSQBX']

        body = """
        [body]
        
        - Jesse
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
        smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
        smtp.quit()

        print('EMAIL SENT')
