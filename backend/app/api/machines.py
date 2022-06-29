import os
from platform import machine
from typing import List

from app.models.pydantic import MachineCreateSchema, MachineResponseSchema
from app.models.tortoise import Machines
from app.services.auth import RoleChecker, get_current_active_user
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from starlette import status
from starlette.responses import JSONResponse


router = APIRouter()


@router.put(
    "/",
    dependencies=[Depends(RoleChecker(["admin"]))],
    status_code=201,
    response_model=MachineResponseSchema,
)
async def post_machine(
    incoming_machine: MachineCreateSchema,
    current_active_user=Depends(get_current_active_user),
):
    # Check if work number already exists
    machine = await Machines.get_or_none(work_number=incoming_machine.work_number)
    if machine is None:
        # create new machine
        try:
            machine = await Machines.create(
                **incoming_machine.dict(),
                created_by=current_active_user.email,
                last_modified_by=current_active_user.email,
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Er is een overwachte fout opgetreden, neem contact op met de beheerder",
            )
        await machine.fetch_related('maintenance_issues')
        return machine
    else:
        # Update existing machine
        await machine.update_from_dict(incoming_machine.dict()).save()
        machine = await Machines.get(work_number=incoming_machine.work_number)
        await machine.fetch_related('maintenance_issues')
        return machine


@router.get("/", status_code=200, response_model=List[MachineResponseSchema])
async def get_machines(
    current_active_user=Depends(get_current_active_user),
) -> List[MachineResponseSchema]:
    return await Machines.all().prefetch_related('maintenance_issues')


@router.get("/{id}", status_code=200, response_model=MachineResponseSchema)
async def get_single_machines(
    id: int, current_active_user=Depends(get_current_active_user)
) -> MachineResponseSchema:
    return await Machines.get_or_none(id=id).prefetch_related('maintenance_issues')


@router.delete("/{id}", status_code=200, dependencies=[Depends(RoleChecker(["admin"]))])
async def delete_single_machine(id: int):
    machine = await Machines.get_or_none(id=id)
    if machine is not None:
        await machine.delete()
        return JSONResponse({"detail": "Machine succesvol verwijderd"}, status_code=200)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine niet gevonden",
        )