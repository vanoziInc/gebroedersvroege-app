from app.models.tortoise import Users
from typing import List
from app.models.pydantic import User_Pydantic

#  Users

async def get_all_users() -> List:
    users = await Users.all()
    return users

async def get_user_by_email(email:str) -> User_Pydantic:
    user = await Users.get_or_none(email=email)
    return user

