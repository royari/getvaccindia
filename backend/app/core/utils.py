# %%
import os
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Body
from fastapi_mail.config import ConnectionConfig
from jinja2 import Environment, FileSystemLoader

from jinja2.nodes import Output
from pydantic import BaseModel
from fastapi import Depends
from fastapi.responses import JSONResponse
from typing import Dict, List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic.networks import EmailStr, HttpUrl
from core.config import settings
import ssl


def create_aliased_response(model: BaseModel, status_code) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=jsonable_encoder(model, by_alias=True))


mail_conf = ConnectionConfig(
    MAIL_USERNAME="getvaccindia",
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM="getvaccindia@gmail.com",
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)

file_loader = FileSystemLoader("email-template/")


async def send_email(email: List[EmailStr], body, subject):
    message = MessageSchema(subject=subject, recipients=email, body=body, subtype="html")
    fm = FastMail(mail_conf)
    await fm.send_message(message)


async def send_confirmation_email(email: List[EmailStr], template_data: Dict, user_id: str):
    env = Environment(loader=file_loader)
    unsub_slug = settings.UNSUBSCRIBE_BASE + user_id
    template = env.get_template("confirmation.html")
    output = template.render(data=template_data, unsub=unsub_slug)
    await send_email(email=email, body=output, subject="getvaccindia email subscription")
