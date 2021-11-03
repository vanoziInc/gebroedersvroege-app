from typing import Any, Dict, List, Optional

from app.models.tortoise import AllowedUsers, GeneralMaintenance, Roles, Users

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