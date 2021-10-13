from typing import Any, Dict, List, Optional

from app.models.tortoise import AllowedUsers, Roles, Users, Birth, Cow

import pydantic
import datetime
from .enums import GenderEnum, BirthProcessEnum, BreedEnum, FirstMilkEnum, DischargeReasonEnum
from pydantic import EmailStr
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

# Early initialisation of Tortoise ORM Models.
# Initialise the relationships between Models. This does not initialise any database connection.
Tortoise.init_models(["app.models.tortoise"], "models")



# Users
class CreateUser(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: pydantic.SecretStr


User_Pydantic = pydantic_model_creator(
    Users,
    name="User",
    exclude=("hashed_password", "confirmation"),
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

AllowedUsersResponseSchema = pydantic_model_creator(
    AllowedUsers
    )

# Births
class BirthCreateSchema(pydantic.BaseModel):
    date_of_birth : datetime.date
    weight : float
    first_milk : FirstMilkEnum
    ear_number : int
    necklace_number_mother : int
    gender : GenderEnum
    breed : Optional[BreedEnum]
    birth_process : BirthProcessEnum
    
    # Bijzonderheden
    twins : Optional[bool] = False
    reverse : Optional[bool] = False
    cesarean_section : Optional[bool] = False
    embryo : Optional[bool] = False

    remarks : Optional[str] 

BirthReturnSchema = pydantic_model_creator(
    Birth
)

CowReturnSchema = pydantic_model_creator(
    Cow
)

class DischargeSchema(pydantic.BaseModel):
    id:int
    reason:DischargeReasonEnum
