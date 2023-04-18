from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, validator, AnyUrl, HttpUrl ,BaseSettings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()
class Email(BaseModel):
    sender: EmailStr
    receiver: EmailStr
    subject: str
    body: str

class EmailList(BaseModel):
    email_list: List[EmailStr]

class Settings(BaseSettings):
    email_user: str
    email_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

app = FastAPI()
settings = Settings()

@app.post("/send_email/")
def send_email(email: Email):
    message = MIMEMultipart()
    message['From'] = email.sender
    message['To'] = email.receiver
    message['Subject'] = email.subject
    message.attach(MIMEText(email.body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(settings.email_user, settings.email_password)
        smtp.sendmail(email.sender, email.receiver, message.as_string())

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

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(settings.email_user, settings.email_password)
            smtp.sendmail(email.sender, email.receiver, message.as_string())

    return {"message": "Emails sent successfully."}
