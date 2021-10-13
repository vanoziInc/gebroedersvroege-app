from app.models.tortoise import Birth
from typing import List

from app.models.pydantic import (
    BirthCreateSchema, BirthReturnSchema, CowReturnSchema
)
from app.models.tortoise import Birth, Cow, Calve
from app.services.auth import RoleChecker
from app.services.mail import Mailer
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from starlette import status

router = APIRouter()

# CRUD
# CREATE

@router.post('/', response_model=CowReturnSchema, status_code=201)
async def create_birth (
    added_birth: BirthCreateSchema
):
    # Check if cow allready exists
    cow = await Cow.get_or_none(ear_number=added_birth.ear_number)
    if cow is not None:
        raise HTTPException(status_code=400, detail="Cow allready exists")
    # Create a birth, cow and calve object
    birth = await Birth.create(**added_birth.dict())
    cow = await Cow.create(**added_birth.dict(), birth=birth)
    calve = await Calve.create(cow=cow)
    # Find mother if available and add calve to it
    mother = await Cow.get_or_none(necklace_number=added_birth.necklace_number_mother)
    if mother is not None:
        calve.mother = mother
        await calve.save()
    await cow.fetch_related('calves')
    return cow

# READ ALL
@router.get('/', response_model=List[BirthReturnSchema], status_code=200)
async def get_births():
    births = await Birth.all().prefetch_related('cow')
    return births

# UPDATE
@router.put('/{id}', response_model=BirthReturnSchema)
async def update_birth(id :int, 
    updated_birth: BirthCreateSchema
):
    birth = await Birth.get(id=id)
    await birth.fetch_related('cow')
    # cow = await Cow.get(id=birth_dict.cow[0].id)
    await birth.update_from_dict(updated_birth.dict())
    cow = await Cow.get(id = birth.cow[0].id)
    await cow.update_from_dict(updated_birth.dict())
    await birth.save()
    await cow.save()
    await birth.fetch_related('cow')
    return birth