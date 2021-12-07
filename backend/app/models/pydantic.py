from typing import Any, Dict, List, Optional

from app.models.tortoise import AllowedUsers, GeneralMaintenance, Roles, Users, WorkingHours

import pydantic
import datetime
from pydantic import EmailStr
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

# Early initialisation of Tortoise ORM Models.
# Initialise the relationships between Models. This does not initialise any database connection.
Tortoise.init_models(["app.models.tortoise"], "models")



# Users
class CreateUser(pydantic.BaseModel):
    first_name :str
    last_name :str
    email: pydantic.EmailStr
    password: pydantic.SecretStr


User_Pydantic = pydantic_model_creator(
    Users,
    name="User",
    exclude=("hashed_password", "confirmation", "working_hours"),
)

# Roles

RolesSchema = pydantic_model_creator(
    Roles,
    name="Role",
    exclude=['id','users']
)


#  Email
class EmailSchema(pydantic.BaseModel):
    recipient_addresses: List[EmailStr]
    body: Dict[str, Any]

# Activate Account
class TokenSchema(pydantic.BaseModel):
    token: Optional[str]
    refresh_token: Optional[str]


# Reset password
class ResetPassword(pydantic.BaseModel):
    token: str
    password: pydantic.SecretStr


# Allowed Users
class AllowedUsersCreateSchema(pydantic.BaseModel):
    email: EmailStr

class AllowedUsersUpdateschema(pydantic.BaseModel):
    email: EmailStr

AllowedUsersResponseSchema = pydantic_model_creator(
    AllowedUsers
    )

# General maintenance
# GET
GeneralMaintenanceResponseSchema = pydantic_model_creator(GeneralMaintenance)
# CREATE
class GeneralMaintenanceCreateSchema(pydantic.BaseModel):
    description : str

# UPDATE
class GeneralMaintenanceUpdateSchema(pydantic.BaseModel):
    description : str

# Working Hours
# GET
WorkingHoursResponseSchema = pydantic_model_creator(WorkingHours, exclude=['user'])
    
# CREATE
class WorkingHoursCreateSchema(pydantic.BaseModel):
    user_id : int
    date: datetime.date
    hours: int
    description : str

# UPDATE
class WorkingHoursUpdateSchema(pydantic.BaseModel):
    id : Optional[int]
    user_id : Optional[int]
    date: Optional[datetime.date]
    hours: Optional[float]
    description : Optional[str]
    submitted: Optional[bool] = False

# UPDATE
class WorkingHoursSubmitSchema(pydantic.BaseModel):
    ids : List[int]



# ADMIN WORKING HOURS
class WeekResult(pydantic.BaseModel):
    user_id : int
    name : str
    sum_hours : float
    submitted : bool

class WeeksNotSubmittedAllUsersResponseSchema(pydantic.BaseModel):
    year :int
    week : int
    week_start : datetime.date
    week_end : datetime.date
    employee_info : List[WeekResult]