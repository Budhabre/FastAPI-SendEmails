from fastapi import FastAPI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from schema import Email, EmailList
from settings import Settings


app = FastAPI()
settings = Settings()


def _send_email(message, sender, receiver):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(settings.email_user, settings.email_password)
        smtp.sendmail(sender, receiver, message.as_string())


@app.post("/send_email/")
def send_email(email: Email):
    message = MIMEMultipart()
    message['From'] = email.sender
    message['To'] = email.receiver
    message['Subject'] = email.subject
    message.attach(MIMEText(email.body, 'plain'))

    _send_email(message, email.sender, email.receiver)

    return {"message": "Email sent successfully."}


@app.post("/send_emails/")
def send_emails(email_list: EmailList):
    for receiver in email_list.email_list:
        email = Email(sender=settings.email_user, receiver=receiver, subject='Hello', body='Hello, this is a test email.')
        message = MIMEMultipart()
        message['From'] = email.sender
        message['To'] = email.receiver
        message['Subject'] = email.subject
        message.attach(MIMEText(email.body, 'plain'))

        _send_email(message, email.sender, email.receiver)

    return {"message": "Emails sent successfully."}
