import json
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.anyio


def test_registration(test_client: TestClient):
    payload = json.dumps(
        {
            "first_name": "test",
            "last_name": "gebruiker",
            "email": "test_gebruiker@test.com",
            "password": "testgebruiker",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = test_client.post("api/auth/register", headers=headers, data=payload)
    # check response code is 201
    pytest.assume(response.status_code == 201)
    pytest.assume(type(response.json()["id"] == int))
    pytest.assume(
        (
            datetime.strptime(
                response.json()["created_at"],
                "%Y-%m-%dT%H:%M:%S.%f+00:00",
            )
            < datetime.now()
        )
        and (
            datetime.strptime(
                response.json()["created_at"],
                "%Y-%m-%dT%H:%M:%S.%f+00:00",
            )
            > datetime.now() - timedelta(seconds=5)
        )
    )
    # pytest.assume(response.json()["lat_modified_at"] == "test@test.com")

    # pytest.assume(response.json()["email"] == "test@test.com")
    # pytest.assume(response.json()["is_active"] == False)
    # pytest.assume(len(response.json()["roles"]) == 1)
    # pytest.assume(response.json()["roles"][0]["name"] == "werknemer")


def test_registration_user_allready_registered(test_client: TestClient):
    payload = json.dumps(
        {
            "first_name": "test",
            "last_name": "gebruiker",
            "email": "test_gebruiker@test.com",
            "password": "testgebruiker",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = test_client.post("api/auth/register", headers=headers, data=payload)
    # check response code is 400 and response text as expected
    pytest.assume(response.status_code == 400)
    pytest.assume(response.json()["detail"] == "Deze gebruiker bestaat al")


def test_registration_invalid_user_information_missing_first_name(
    test_client: TestClient,
):
    payload = json.dumps(
        {
            "last_name": "gebruiker",
            "email": "test_gebruiker@test.com",
            "password": "testgebruiker",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = test_client.post("api/auth/register", headers=headers, data=payload)
    # check response code is 400 and response text as expected
    print(response.status_code)
    print(response.json())
