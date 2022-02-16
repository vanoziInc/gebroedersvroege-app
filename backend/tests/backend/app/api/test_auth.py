import json
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from app.services.mail import fm

pytestmark = pytest.mark.anyio


async def test_registration_success(
    test_client: TestClient, invite_new_user_fixture: int
):
    # Invite user for registration
    await invite_new_user_fixture("test_gebruiker@test.com")
    # Set user details for registration
    payload = json.dumps(
        {
            "first_name": "test",
            "last_name": "gebruiker",
            "email": "test_gebruiker@test.com",
            "password": "testgebruiker",
        }
    )
    headers = {"Content-Type": "application/json"}
    fm.config.SUPPRESS_SEND = 1
    with fm.record_messages() as outbox:
        response = await test_client.post(
            "/auth/register", headers=headers, data=payload
        )
        assert response.status_code == 201
        assert type(response.json()["id"] == int)
        # Check the created by timestamp is from the last 5 seconds
        assert (
                datetime.strptime(
                    response.json()["created_at"],
                    "%Y-%m-%dT%H:%M:%S.%f+00:00",
                )
                < datetime.now()
            ) and (
                datetime.strptime(
                    response.json()["created_at"],
                    "%Y-%m-%dT%H:%M:%S.%f+00:00",
                )
                > datetime.now() - timedelta(seconds=5)
            )
        
        assert (
                datetime.strptime(
                    response.json()["last_modified_at"],
                    "%Y-%m-%dT%H:%M:%S.%f+00:00",
                )
                < datetime.now()
            ) and (
                datetime.strptime(
                    response.json()["last_modified_at"],
                    "%Y-%m-%dT%H:%M:%S.%f+00:00",
                )
                > datetime.now() - timedelta(seconds=5)
            )
        
        assert response.json()["email"] == "test_gebruiker@test.com"
        assert response.json()["is_active"] == False
        assert len(response.json()["roles"]) == 1
        assert response.json()["roles"][0]["name"] == "werknemer"
        # Email checks
        assert len(outbox) == 1
        assert outbox[0]["from"] == "Superleuk app Gebr. Vroege <supermooiapp@gmail.com>"
        assert outbox[0]["To"] == "test_gebruiker@test.com"
        assert outbox[0]["Subject"] == "Welkom!!"


async def test_registration_user_allready_registered(test_client: TestClient):
    payload = json.dumps(
        {
            "first_name": "test",
            "last_name": "gebruiker",
            "email": "test_gebruiker@test.com",
            "password": "testgebruiker",
        }
    )
    headers = {"Content-Type": "application/json"}
    response = await test_client.post("/auth/register", headers=headers, data=payload)
    # check response code is 400 and response text as expected
    assert response.status_code == 400
    assert response.json()["detail"] == "Deze gebruiker bestaat al"


async def test_registration_user_not_invited(
    test_client: TestClient,
):
    payload = json.dumps(
        {
            "first_name": "test",
            "last_name": "gebruiker",
            "email": "test2_gebruiker@test.com",
            "password": "testgebruiker",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = await test_client.post("/auth/register", headers=headers, data=payload)
    # check response code is 400 and response text as expected
    assert response.status_code == 400
    assert response.json()["detail"] == "Dit email adres is niet bevoegd om zich te registeren"
