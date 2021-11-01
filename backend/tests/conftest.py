
import os
from typing import Generator

import pytest
from app.config import Settings, get_settings
from app.main import create_application
from starlette.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from app.models.tortoise import AllowedUsers, Users, Roles


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_BACKEND_URL"))


# @pytest.fixture(scope="module")
# def client() -> Generator:
#     app = create_application()
#     app.dependency_overrides[get_settings] = get_settings_override
#     register_tortoise(
#         app,
#         db_url=os.environ.get("DATABASE_TEST_URL"),
#         modules={"models": ["app.models.tortoise"]},
#         generate_schemas=True,
#         add_exception_handlers=True,
#     )
#     with TestClient(app) as c:
#         yield c


# @pytest.fixture(scope="module")
# def event_loop(client: TestClient) -> Generator:
#     yield client.task.get_loop()

import os, asyncio

import pytest
from tortoise import Tortoise

DB_URL = "sqlite://:memory:"


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": ["app.models.tortoise"]}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = os.environ.get("DATABASE_TEST_BACKEND_URL")):
    await init_db(db_url, True, True)

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def test_client():
    app = create_application()
    await init()
    yield TestClient(app, base_url=os.environ.get("BASE_URL"))
    await Tortoise._drop_databases()

