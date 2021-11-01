from smtplib import SMTP
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import get_fastapi_mail_config
from fastapi import Depends
from app.models.pydantic import EmailSchema

class Mailer:
    async def send_invitation_message(email: EmailSchema, config: ConnectionConfig = Depends(get_fastapi_mail_config)):
        message = MessageSchema(
            subject="Uitnoding voor Gebr. Vroege app",
            # List of recipients, as many as you can pass
            recipients=email.dict().get("recipient_addresses"),
            template_body=email.dict().get("body"),
        )
        fm = FastMail(config)
        await fm.send_message(message, template_name="invite_email.html")

    async def send_welcome_message(email: EmailSchema, config: ConnectionConfig = Depends(get_fastapi_mail_config)):
        message = MessageSchema(
            subject="Welkom!!",
            # List of recipients, as many as you can pass
            recipients=email.dict().get("recipient_addresses"),
            template_body=email.dict().get("body"),
        )
        fm = FastMail(config)
        await fm.send_message(message, template_name="account_activation_email.html")

    async def send_reset_password_message(email: EmailSchema, config: ConnectionConfig):
        message = MessageSchema(
            subject="Password reset",
            # List of recipients, as many as you can pass
            recipients=email.dict().get("recipient_addresses"),
            template_body=email.dict().get("body"),
        )
        fm = FastMail(config)
        await fm.send_message(message, template_name="reset_password_email.html")
