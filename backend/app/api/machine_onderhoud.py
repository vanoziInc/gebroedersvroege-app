import os
from platform import machine
from typing import List

from app.models.pydantic import (
    MachineMaintenanceCreate,
    MachineMaintenanceResponseSchema,
    MachineMaintenanceUpdate,
)
from app.services.auth import RoleChecker, get_current_active_user
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from starlette import status
from starlette.responses import JSONResponse

from app.models.tortoise import MaintenanceMachines, Machines


router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=MachineMaintenanceResponseSchema,
)
async def post_machine_maintenance_issue(
    incoming_issue: MachineMaintenanceCreate,
    current_active_user=Depends(get_current_active_user),
):
    # Check if work number already exists
    machine = await Machines.get_or_none(id=incoming_issue.machine_id)
    if machine is not None:
        # create new machine
        try:
            maintenace_issue = await MaintenanceMachines.create(
                **incoming_issue.dict(),
                created_by=current_active_user.email,
                last_modified_by=current_active_user.email,
                machine=machine
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Er is een overwachte fout opgetreden, neem contact op met de beheerder",
            )
        return maintenace_issue
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Machine niet bekend",
        )


@router.put(
    "/",
    status_code=200,
    response_model=MachineMaintenanceResponseSchema,
)
async def update_machine_maintenance_issue(
    updated_maintenance_issue: MachineMaintenanceUpdate,
    current_active_user=Depends(get_current_active_user),
):
    # Check if work number already exists
    maintenance_issue = await MaintenanceMachines.get_or_none(
        id=updated_maintenance_issue.id
    )
    if maintenance_issue is not None:
        try:
            # Update machine maintenance issue
            maintenance_issue.update_from_dict(updated_maintenance_issue.dict())
            maintenance_issue.last_modified_by = current_active_user.email
            await maintenance_issue.save()
            await maintenance_issue.fetch_related('machine')
            return maintenance_issue
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Er is een overwachte fout opgetreden, neem contact op met de beheerder",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onderhouds issue niet bekend",
        )


@router.get("/", status_code=200, response_model=List[MachineMaintenanceResponseSchema])
async def get_maintenance_issues(
    current_active_user=Depends(get_current_active_user),
) -> List[MachineMaintenanceResponseSchema]:
    return await MaintenanceMachines.all().prefetch_related('machine')


@router.get("/{id}", status_code=200, response_model=MachineMaintenanceResponseSchema)
async def get_single_maintenance_issues(
    id: int, current_active_user=Depends(get_current_active_user)
) -> MachineMaintenanceResponseSchema:
    return await MaintenanceMachines.get_or_none(id=id)


@router.delete("/{id}", status_code=200)
async def delete_single_maintenance_issue(id: int):
    maintenance_issue = await MaintenanceMachines.get_or_none(id=id)
    if maintenance_issue is not None:
        await maintenance_issue.delete()
        return JSONResponse(
            {"detail": "Onderhouds issue succesvol verwijderd"}, status_code=200
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onderhouds issue is niet gevonden",
        )
