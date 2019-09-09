import json
import sys
import os
import re

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

#################################################################################
#Get relative path###############################################################
#################################################################################
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]

#################################################################################
#Retrieve authentication variables###############################################
#################################################################################
with open(os.path.join(script_dir, 'cred.json')) as json_cred:
    cred = json.load(json_cred)

smtp_server = str(cred['smtp_server'])
sender = str(cred['sender_mail'])
password = str(cred['sender_pass'])
destination = [str(cred['receiver_mail'])]

def sendMail(subject, content):
    try:
        msg = MIMEText(str(content))
        msg['Subject']= str(subject)
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
