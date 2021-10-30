import os
from typing import List

from app.config import get_fastapi_mail_config
from app.models.pydantic import (
    AllowedUsersCreateSchema,
    AllowedUsersUpdateschema,
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

# CRUD Implementation for allowed users

# Create allowed user (only the admin can do this)
@router.post("/", response_model=AllowedUsersResponseSchema, status_code=201, dependencies=[Depends(RoleChecker(['admin']))])
async def post_allowed_users(
    added_user: AllowedUsersCreateSchema,
    config: ConnectionConfig = Depends(get_fastapi_mail_config),
) -> AllowedUsersResponseSchema:
    if await AllowedUsers.get_or_none(email=added_user.email) is not None:
        raise HTTPException(status_code=400, detail="Er is al een uitnodiging gestuurd naar dit email adres")
    else:
        # Add allowed user to database
        try:
            allowed_user = await AllowedUsers.create(email=added_user.email)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Er is een overwachte fout opgetreden bij het opslaan in de database",
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
                detail=f"Er is een overwachte fout opgetreden bij het versturen van de email",
            )
        return allowed_user

# Read all allowed users (Only the admin can do this)
@router.get(
    "/",
    response_model=List[AllowedUsersResponseSchema],
    dependencies=[Depends(RoleChecker(["admin"]))],
)
async def get_allowed_users():
    return await AllowedUsers.all()

@router.get('/{id}', response_model=AllowedUsersResponseSchema)
async def get_allowed_user(id: int):
    allowd_user = await AllowedUsers.get_or_none(id=id)
    if allowd_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Dit email adres komt niet voor in de lijst met toegestane email adressen"
        )

@router.put('/{id}', response_model=AllowedUsersResponseSchema)
async def update_allowed_user(id :int, 
    updated_birth: BirthCreateSchema
):
    allowd_user = await AllowedUsers.get_or_none(id=id)
