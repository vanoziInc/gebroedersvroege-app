import os

from app.config import Settings, get_fastapi_mail_config, get_settings
from app.models.pydantic import (
    CreateUser,
    EmailSchema,
    ResetPassword,
    User_Pydantic,
    TokenSchema,
)
from app.models.tortoise import AllowedUsers, Roles, Users
from app.services.auth import Auth
from app.services.mail import Mailer
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import ConnectionConfig
from jose import jwt
from starlette import status
from starlette.responses import JSONResponse


router = APIRouter()


@router.post("/register", response_model=User_Pydantic, status_code=201)
async def register(
    register_info: CreateUser,
    config: ConnectionConfig = Depends(get_fastapi_mail_config),
) -> User_Pydantic:
    # Check if user allready exists
    if await Users.get_or_none(email=register_info.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    # Check if user is in allowed users table
    if await AllowedUsers.get_or_none(email=register_info.email) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not allowed to register",
        )
    # Create user
    try:
        user = await Users.create(
            email=register_info.email,
            hashed_password=Auth.get_password_hash(
                register_info.password.get_secret_value()
            ),
        )
        # create confirmation token and add the jti to the database user
        confirmation_token = Auth.get_confirmation_token(user.email)
        user.confirmation = confirmation_token["jti"]
        await user.save()
        # add user roles
        role, _ = await Roles.get_or_create(name="henk", description="test_role")
        await user.roles.add(role)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while creating user in the database",
        )
    try:
        await Mailer.send_welcome_message(
            config=config,
            email=EmailSchema(
                recipient_addresses=[user.email],
                body={
                    "username": user.email,
                    "base_url": os.getenv("BASE_URL"),
                    "confirmation_token": confirmation_token["token"],
                },
            ),
        )
    except:
        await user.delete()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while sending user email",
        )
    await user.fetch_related("roles")
    return user


@router.post("/activate_account", status_code=200)
async def activate_account(
    token: TokenSchema, settings: Settings = Depends(get_settings)
):
    token = token.token
    invalid_token_error = HTTPException(status_code=400, detail="Invalid token")
    # Check if token expiration date is reached
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=settings.token_algorithm
        )
    except jwt.JWTError as e:
        print(e)
        raise HTTPException(status_code=403, detail="Token has expired")
    # Check if scope of the token is valid
    if payload["scope"] != "registration":
        raise invalid_token_error
    user = await Users.get_or_none(email=payload["sub"])
    # Check if token belongs to user and not already been used
    if not user or user.confirmation.hex != payload["jti"]:
        raise invalid_token_error
    if user.is_active:
        raise HTTPException(status_code=403, detail="User already activated")
    # Set confirmation UID to None and user to active
    try:
        user.confirmation = None
        user.is_active = True
        await user.save()
        return JSONResponse({"message": "Account activated"})
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while modifying user in the database",
        )


@router.get("/resent_activation_token/{email}", status_code=200)
async def resent_activation_code(
    email: str, config: ConnectionConfig = Depends(get_fastapi_mail_config)
):
    # Check if user allready exists
    if await Users.get_or_none(email=email) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email address does not exist",
        )
    user = await Users.get(email=email)
    # Check that account is not yet activated
    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is allready activated",
        )

    # create confirmation token and add the jti to the database user
    confirmation_token = Auth.get_confirmation_token(user.email)
    user.confirmation = confirmation_token["jti"]
    await user.save()
    try:
        await Mailer.send_welcome_message(
            config=config,
            email=EmailSchema(
                recipient_addresses=[user.email],
                body={
                    "username": user.email,
                    "confirmation_token": confirmation_token["token"],
                },
            ),
        )
    except:
        await user.delete()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while sending user email",
        )


@router.post("/login")
async def get_login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await Auth.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Auth.get_access_token(email=user.email)
    refresh_token = Auth.get_refresh_token(email=user.email)
    return JSONResponse(
        {
            "access_token": access_token["token"], 
            "refresh_token" : refresh_token["token"],
            "token_type": "bearer"
        }, status_code=200
    )

@router.post("/refresh")
async def refresh(token:TokenSchema, settings: Settings = Depends(get_settings)):
    invalid_token_error = HTTPException(status_code=400, detail="Invalid token")
    # Check if token expiration date is reached
    try:
        payload = jwt.decode(
            token.refresh_token, settings.secret_key, algorithms=settings.token_algorithm
        )
    except jwt.JWTError as e:
        raise HTTPException(status_code=403, detail="Token has expired")
    # Check if scope of the token is valid
    if payload["scope"] != "refresh":
        raise invalid_token_error
    user = await Users.get_or_none(email=payload["sub"])
    # Check if token belongs to user and not already been used
    if not user:
        raise invalid_token_error
    access_token = Auth.get_access_token(email=user.email)
    refresh_token = Auth.get_refresh_token(email=user.email)
    return JSONResponse(
        {
            "access_token": access_token["token"], 
            "refresh_token" : refresh_token["token"],
            "token_type": "bearer"
        }, status_code=200
    )

@router.get("/forgot_password/{email}")
async def forgot_password(
    email: str,
    config: ConnectionConfig = Depends(get_fastapi_mail_config),
):
    # check if email address exists
    user = await Users.get_or_none(email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
        )
    reset_password_token = Auth.get_reset_password_token(email=user.email)
    try:
        await Mailer.send_reset_password_message(
            config=config,
            email=EmailSchema(
                recipient_addresses=[user.email],
                body={
                    "username": user.email,
                    "base_url": os.getenv("BASE_URL"),
                    "reset_password_token": reset_password_token["token"],
                    "sender" : "Gebroeders Vroege"
                },
            ),
        )
        return JSONResponse({"message": "Reset token has been sent"}, status_code=200)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while sending user email",
        )


@router.post("/reset_password")
async def reset_password(
    reset_info: ResetPassword, settings: Settings = Depends(get_settings)
):
    invalid_token_error = HTTPException(status_code=400, detail="Invalid token")
    # Check if token expiration date is reached
    try:
        payload = jwt.decode(
            reset_info.token, settings.secret_key, algorithms=settings.token_algorithm
        )
    except jwt.JWTError as e:
        raise HTTPException(status_code=403, detail="Token has expired")
    # Check if scope of the token is valid
    if payload["scope"] != "reset-password":
        raise invalid_token_error
    user = await Users.get_or_none(email=payload["sub"])
    # Check if token belongs to user and not already been used
    if not user:
        raise invalid_token_error

    # Update password
    ## Create password hash for new password and save in the database
    new_password_hashed = Auth.get_password_hash(reset_info.password.get_secret_value())
    user.hashed_password = new_password_hashed
    await user.save()
    # Create a success respons
    return JSONResponse({"message": "Password successfully reset"}, status_code=200)
