from icalendar import Calendar
from datetime import datetime, date
from urllib import request
import os, re
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ICS_URL = os.getenv("ICS_URL")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
NOTIFY_DAYS = os.getenv("NOTIFY_DAYS")

# From https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression
MAIL_REGEX = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
NOTIFY_DAYS = NOTIFY_DAYS.split(",")

def template(file, vevent):
    f = open(file, "r")
    template = f.read()
    f.close()
    template = template.replace("%title%", vevent.get("summary"))
    days = (vevent.decoded("dtstart") - datetime.now().date()).days
    template = template.replace("%time%", "heute" if days == 0 else ("morgen" if days == 1 else "in " + str(days) + " Tagen"))
    return template

def send_mail(from_addr, to_addr, subject, message_plain, message_html):
    msg = MIMEMultipart("alternative")
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg.attach(MIMEText(message_html, "html"))
    msg.attach(MIMEText(message_plain, "plain"))
    smtp.sendmail(from_addr, to_addr, msg.as_string())

MAIL_REGEX = re.compile(MAIL_REGEX)
smtp = SMTP_SSL(SMTP_HOST, SMTP_PORT)
smtp.set_debuglevel(2)
smtp.login(SMTP_USER, SMTP_PASSWORD)
ics_file = request.urlopen(ICS_URL)
cal = Calendar.from_ical(ics_file.read())

for component in cal.walk():
    if(component.name == "VEVENT") and isinstance(component.decoded("dtstart"), date):
        days = (component.decoded("dtstart") - datetime.now().date()).days
        if str(days) in NOTIFY_DAYS:
            from_addr = component.get("summary") + " <" + component.get("summary").lower().replace(" ", "_") + "@fickt-di.ch>"
            subject = template("template_subject.txt", component)
            message_plain = template("template_message.txt", component)
            message_html = template("template_message.html", component)
            for to_addr in component.get("description").split("\n"):
                if(MAIL_REGEX.match(to_addr)):
                    send_mail(from_addr, to_addr, subject, message_plain, message_html)

smtp.quit()
ics_file.close()