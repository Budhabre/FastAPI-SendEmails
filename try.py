from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
from decouple import config

class Email(BaseModel):
    sender: str
    receiver: str
    subject: str
    body: str

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=config('POSTGRES_DB'),
            user=config('POSTGRES_USER'),
            password=config('POSTGRES_PASSWORD'),
            host=config('POSTGRES_HOST'),
            port=config('POSTGRES_PORT')
        )

    def create_email(self, email: Email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO emails (sender, receiver, subject, body) VALUES (%s, %s, %s, %s)",
                    (email.sender, email.receiver, email.subject, email.body))
        self.conn.commit()
        cur.close()

    def get_all_emails(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM emails")
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_email_by_id(self, email_id: int):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM emails WHERE id = %s", (email_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            raise HTTPException(status_code=404, detail="Email not found")
        return {"sender": row[0], "receiver": row[1], "subject": row[2], "body": row[3]}

    def delete_email_by_id(self, email_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM emails WHERE id = %s", (email_id,))
        self.conn.commit()
        cur.close()

app = FastAPI()
db = DB()

@app.post("/send_email/")
def send_email(email: Email):
    message = MIMEMultipart()
    message['From'] = email.sender
    message['To'] = email.receiver
    message['Subject'] = email.subject
    message.attach(MIMEText(email.body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(config('EMAIL_USER'), config('EMAIL_PASSWORD'))
        smtp.sendmail(email.sender, email.receiver, message.as_string())

    db.create_email(email)
    return {"message": "Email sent successfully."}

@app.get("/emails/")
def read_emails():
    rows = db.get_all_emails()
    if not rows:
        raise HTTPException(status_code=404, detail="Emails not found")
    return [{"id": row[4], "sender": row[0], "receiver": row[1], "subject": row[2], "body": row[3]} for row in rows]

@app.get("/emails/{email_id}")
def read_email(email_id: int):
    return db.get_email_by_id(email_id)

@app.delete("/emails/{email_id}")
def delete_email(email_id: int):
    db.delete_email_by_id(email_id)
    return {"message": "Email deleted successfully."}
