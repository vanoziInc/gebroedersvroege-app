import asyncio
import os
from typing import Generator

import pytest
import requests
from app.config import Settings, get_settings
from app.main import create_application
from app.models.tortoise import Roles, Users
from starlette.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_BACKEND_URL"))


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": ["app.models.tortoise"]}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url}")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success created database schema")


async def init(db_url: str = os.environ.get("DATABASE_TEST_BACKEND_URL")):
    await init_db(db_url, True, True)
    # Insert testdata into the database
    # Roles
    admin_role = await Roles.create(name="admin", description="User met admin rechten")
    werknemer_role = await Roles.create(
        name="werknemer", description="User met algemene werknemers rechten"
    )
    # Users
    admin_user = await Users.create(
        email="admin@admin.com",
        hashed_password="$2b$12$UKv6whbIteBbIsION9igLef5qOS6yzLn1MczUCST7X6RDn18afzZ2",
        is_active=True,
        confirmation=None,
    )
    werknemer_user = await Users.create(
        email="werknemer@werknemer.com",
        hashed_password="$2b$12$X6OGY1eXztIH2rYDwyVFO.nmrPYq98kla4JmweOu4N/oMgoe3yaKK",
        is_active=True,
        confirmation=None,
    )
    # Userroles
    await admin_user.roles.add(admin_role)
    await werknemer_user.roles.add(werknemer_role)


# Redefine the event_loop fixture with the session scope
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_client():
    app = create_application()
    await init()
    yield TestClient(app)
    await Tortoise._drop_databases()
    print("Database dropped")
