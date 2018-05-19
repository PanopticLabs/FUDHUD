import json
import sys
import os
import re

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

with open('cred.json') as json_cred:
    cred = json.load(json_cred)

smtp_server = str(cred['smtp_server'])
sender = str(cred['sender_mail'])
password = str(cred['sender_pass'])
destination = [str(cred['receiver_mail'])]

def sendMail(subject, content):
    try:
        msg = MIMEText(content)
        msg['Subject']= subject
        msg['From'] = sender

        conn = SMTP(smtp_server)
        conn.set_debuglevel(False)
        conn.login(sender, password)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except Exception as e:
        sys.exit( "mail failed; %s" % str(e) )
