import logging
import os
from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings, AnyUrl, SecretStr
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    app_name :str = os.getenv("APP_NAME", "TEST APP")
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.environ.get("DATABASE_URL")
    token_algorithm: str = os.getenv("TOKEN_ALGORITHM", "HS256")
    secret_key = SecretStr = os.getenv("SECRET_KEY", "erruggeheim")
    registration_token_lifetime :int = os.getenv("REGISTRATION_TOKEN_LIFETIME", 10080)
    login_token_lifetime :int = os.getenv("LOGIN_TOKEN_LIFETIME", 43800)
    refresh_token_lifetime : int= os.getenv("LOGIN_TOKEN_LIFETIME", 43800)
    reset_password_token_lifetime :int = os.getenv("RESET_PASSWORD_TOKEN_LIFETIME", 10080)


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()

@lru_cache
def get_fastapi_mail_config() -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=os.getenv("MAIL_PORT"),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
        MAIL_TLS = os.getenv("MAIL_TLS"),
        MAIL_SSL = os.getenv("MAIL_SSL"),
        TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
    )

