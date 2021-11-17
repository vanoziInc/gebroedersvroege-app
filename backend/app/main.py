import logging, os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api import auth, users, allowed_users, roles, user_roles, general_maintenance, working_hours
from app.db import init_db


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    # load router into application
    application.include_router(auth.router, prefix="/api/auth", tags=["auth"]) 
    application.include_router(users.router, prefix="/api/users", tags=["users"]) 
    application.include_router(allowed_users.router, prefix="/api/allowed_users", tags=["allowed_users"])
    application.include_router(roles.router, prefix="/api/roles", tags=["roles"])
    application.include_router(user_roles.router, prefix="/api/user_roles", tags=["user_roles"])
    application.include_router(general_maintenance.router, prefix="/api/general_maintenance", tags=["general_maintenance"])
    application.include_router(working_hours.router, prefix="/api/working_hours", tags=["working_hours"])

    # set environment variables based on the environemnt set in the docker-compose file
    # if os.getenv("ENVIRONMENT") =='dev':
    #     load_dotenv('.env.dev')
    #     dotenv_values(".env.dev")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create admin role and user
    # log.info("Create admin role and admin user ...")
    # from app.models.tortoise import Users, Roles
    # from app.services.auth import Auth
    # role, _= await Roles.get_or_create(name="admin", description="User has administrative rights")
    # user = await Users.get_or_create(email="admin@admin.com", hashed_password=Auth.get_password_hash("admin123$%"))
    # await user.roles.add(role)
    # log.info("Admin role and user created")

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)
    
 

@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")