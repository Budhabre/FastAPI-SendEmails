from pydantic import BaseSettings


class Settings(BaseSettings):
    email_user: str
    email_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
