from fastapi import APIRouter, HTTPException
from typing import List

from fastapi.param_functions import Depends
from app.services.auth import get_current_active_user, RoleChecker

from app.api import crud
from app.models.pydantic import User_Pydantic

router = APIRouter()

@router.get('/', response_model=List[User_Pydantic], dependencies=[Depends(RoleChecker(['admin']))])
async def get_all_users():
    users = await crud.get_all_users()
    for user in users:
        await user.fetch_related("roles")
    return users

@router.get('/me', response_model=User_Pydantic)
async def get_me(current_active_user = Depends(get_current_active_user)) -> User_Pydantic:
    return current_active_user

