from pydantic import BaseModel, EmailStr
from typing import List


class Email(BaseModel):
    sender: EmailStr
    receiver: EmailStr
    subject: str
    body: str


class EmailList(BaseModel):
    email_list: List[EmailStr]
