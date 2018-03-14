#! /usr/local/bin/python

import sys, os, re, io, csv, time
from smtplib import SMTP_SSL as SMTP
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
def sendMail(to, name, passw):
    ### Settings ###

    SMTPserver = 'open.netservis.cz'
    sender =     "admin@gpjp.cz"
    USERNAME = "admin@gpjp.cz"
    PASSWORD = "omega258N"

    destination = [to]
    plain = ["centrum.cz"]

    subject = "Přihlášení do sítě"
    if any(True if a in b else False for a in plain for b in destination):
        with open('email_plain.html', 'r', encoding='utf8') as myfile:
            content=myfile.read().replace('{{-uname-}}', name).replace('{{-passw-}}', passw)
    else:
        with open('email.html', 'r', encoding='utf8') as myfile:
            content=myfile.read().replace('{{-uname-}}', name).replace('{{-passw-}}', passw)
    
    #content=io.open("email.html", mode="r", encoding="utf-8")
    attachment="podminky_site_gpjp_0118.pdf"

    ### APP ###

    msg = MIMEMultipart('html')
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(destination)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(content, 'html'))

    with open(attachment, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(attachment)
        )
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
    msg.attach(part)

    smtp = SMTP(SMTPserver, 465)
    smtp.set_debuglevel(False)
    smtp.login(USERNAME, PASSWORD)

    try:
        smtp.sendmail(sender, destination, msg.as_string())
    except Exception as exc:
        sys.exit( "mail failed; %s" % str(exc) ) # give a error message
    finally:
        smtp.quit()


with open('studenti_test.csv', 'r') as f:
    reader = csv.reader(f)
    people = list(reader)

for line in people:
    print("Sending to", line[1])
    sendMail(line[1], line[0], line[2])
    time.sleep(1)
