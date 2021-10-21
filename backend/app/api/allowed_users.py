import os
from typing import List

from app.config import get_fastapi_mail_config
from app.models.pydantic import (
    AllowedUsersCreateSchema,
    AllowedUsersResponseSchema,
    EmailSchema,
)
from app.models.tortoise import AllowedUsers
from app.services.auth import RoleChecker
from app.services.mail import Mailer
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from fastapi_mail import ConnectionConfig
from starlette import status

router = APIRouter()


@router.post("/", response_model=AllowedUsersResponseSchema, status_code=201, dependencies=[Depends(RoleChecker(['admin']))])
async def post_allowed_users(
    added_user: AllowedUsersCreateSchema,
    config: ConnectionConfig = Depends(get_fastapi_mail_config),
) -> AllowedUsersResponseSchema:
    if await AllowedUsers.get_or_none(email=added_user.email) is not None:
        raise HTTPException(status_code=400, detail="User allready invited")
    else:
        # Add allowed user to database
        try:
            allowed_user = await AllowedUsers.create(email=added_user.email)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while creating user in the database",
            )
        # Send email
        try:
            await Mailer.send_invitation_message(
                config=config,
                email=EmailSchema(
                    recipient_addresses=[allowed_user.email],
                    body={
                        "username": allowed_user.email,
                        "base_url": os.getenv("BASE_URL"),
                        "sender": "Gebroeders Vroege",
                    },
                ),
            )
        except:
            await allowed_user.delete()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error while sending user email",
            )
        return allowed_user


@router.get(
    "/",
    response_model=List[AllowedUsersResponseSchema],
    dependencies=[Depends(RoleChecker(["admin"]))],
)
async def get_allowed_users():
    return await AllowedUsers.all()


