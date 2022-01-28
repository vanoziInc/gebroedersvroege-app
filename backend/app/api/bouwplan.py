from app.helpers.bouwplan import bouwplan_2022

import os, json
from typing import List

from fastapi.responses import JSONResponse
from fastapi.param_functions import Depends
from fastapi import APIRouter

from app.services.auth import RoleChecker

router = APIRouter()

@router.get(
    "/",
    dependencies=[Depends(RoleChecker(["admin", "werknemer"]))],
)
async def get_bouwplan_2022():
    return JSONResponse(status_code=200, content=bouwplan_2022())
