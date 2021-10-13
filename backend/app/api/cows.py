from app.models.tortoise import Cow
from app.models.pydantic import CowReturnSchema, DischargeSchema
from typing import List
from datetime import datetime

from app.services.auth import RoleChecker
from app.services.mail import Mailer
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from starlette import status
from starlette.responses import JSONResponse


router = APIRouter()

# CRUD
# CREATE

@router.get("/", status_code=200, response_model=List[CowReturnSchema])
async def read_all_cows():
    cows = await Cow.all().prefetch_related('birth', 'calves')
    return cows



@router.put("/discharge_cow", status_code=200 ,response_model=CowReturnSchema)
async def dispatch_cow(discharge_info:DischargeSchema):
    cow = await Cow.get_or_none(id=discharge_info.id)
    if cow is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Koe met dit oornummer is niet bekend"
        )
    if cow.date_discharched is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Koe met dit oornummer is al afgevoerd"
        )
    try:
        cow.reason_discharched = discharge_info.reason
        cow.date_discharched = datetime.now()
        await cow.save()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    else:
        return cow
