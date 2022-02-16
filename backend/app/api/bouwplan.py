from datetime import date
from typing import List

from app.helpers.excel_functions import excel_to_list_of_dicts
from app.models.pydantic import BouwPlanDataModel
from app.models.tortoise import BouwPlan
from app.services.auth import RoleChecker
from fastapi import APIRouter, File, UploadFile
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError, parse_obj_as

from app.services.auth import get_current_active_user

router = APIRouter()

# TODO: Create test
@router.get(
    "/",
    dependencies=[Depends(RoleChecker(["admin", "werknemer"]))],
    response_model=List[BouwPlanDataModel],
)
async def get_bouwplan(year: int):
    bouwplannen = await BouwPlan.filter(year=year)
    return bouwplannen


# TODO: Create test
@router.post(
    "/upload",
    dependencies=[Depends(RoleChecker(["admin", "werknemer"]))],
    response_model=List[BouwPlanDataModel],
)
async def upload_bouwplan(
    year: int,
    current_user=Depends(get_current_active_user),
    in_file: UploadFile = File(...),
):
    # Check the document type
    if in_file.content_type not in [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ]:
        return JSONResponse(
            status_code=400, content={"detail": "Ongeldig document type"}
        )
    # Parse the excel
    data = excel_to_list_of_dicts(excel_file=in_file.file.read())
    # validate against pydantic model
    try:
        parse_obj_as(List[BouwPlanDataModel], data)
    except ValidationError as e:
        return JSONResponse(
            status_code=422, content={"detail": "Fout bij valideren van de data"}
        )
    finally:
        # Delete all bouwplan entries for that year
        await BouwPlan.filter(year=year).delete()
        # Save data in the database
        for bouwplan in data:
            bouwplan["year"] = year
            bouwplan["created_by"] = current_user.email
            bouwplan["last_modified_by"] = current_user.email
            await BouwPlan.create(**bouwplan)
        bouwplannen = await BouwPlan.filter(year=year)
        return bouwplannen
