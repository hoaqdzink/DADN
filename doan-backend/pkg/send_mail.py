import smtplib
import os
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_mail(subject_mail, body_content, recipient):
    sender = os.getenv("MAIL_SENDER")
    sender_name = os.getenv("MAIL_SENDER_NAME")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_port = int(os.getenv("SMTP_PORT"))

    message = MIMEMultipart("alternative")

    message["Subject"] = subject_mail
    message["From"] = email.utils.formataddr((sender_name, sender))
    message["To"] = recipient

    body_part = MIMEText(body_content, "html")
    message.attach(body_part)
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_user, smtp_password)
    server.sendmail(sender, recipient, message.as_string())
    server.close()
