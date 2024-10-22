from celery import Celery
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM
import smtplib
from email.mime.text import MIMEText

celery = Celery('tasks', broker='redis://redis:6379')

@celery.task
def send_notification_add(email_to: str):
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(MAIL_USERNAME, MAIL_PASSWORD)
    email = MIMEText(f'''
        <div style="background-color: #2B2D31; border-radius:10px;">
        </div>
        ''', "html")
    smtp_server.sendmail("", email_to, email.as_string())


@celery.task
def send_notification_delete(email_to: str):
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(MAIL_USERNAME, MAIL_PASSWORD)
    email = MIMEText(f'''
        <div style="background-color: #2B2D31; border-radius:10px;">
        </div>
        ''', "html")
    smtp_server.sendmail(MAIL_USERNAME, email_to, email.as_string())
