import json
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


@pytest.mark.asyncio
def test_add_email_to_allowed_users(test_client: TestClient):
    # Get admin access token
    response = test_client.post(
        "api/auth/login",
        headers={},
        data={"username": "admin@admin.com", "password": "admin"},
        files=[],
    )
    admin_access_token = response.json()["access_token"]
    # Create payload, headers and make the response
    payload = json.dumps(
        {
            "email": "test_gebruiker@test.com",
        }
    )
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {admin_access_token}",
        "Content-Type": "application/json",
    }
    response = test_client.post("api/allowed_users/", headers=headers, data=payload)
    pytest.assume(response.status_code == 201)
    pytest.assume(response.json()["id"])
    pytest.assume(response.json()["created_at"])
    pytest.assume(response.json()["last_modified_at"])
    pytest.assume(response.json()["email"] == "test_gebruiker@test.com")


@pytest.mark.asyncio
def test_add_email_to_allowed_users_email_allready_exists(test_client: TestClient):
    # Get admin access token
    response = test_client.post(
        "api/auth/login",
        headers={},
        data={"username": "admin@admin.com", "password": "admin"},
        files=[],
    )
    admin_access_token = response.json()["access_token"]
    # Create payload, headers and make the response
    payload = json.dumps(
        {
            "email": "test_gebruiker@test.com",
        }
    )
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {admin_access_token}",
        "Content-Type": "application/json",
    }
    response = test_client.post("api/allowed_users/", headers=headers, data=payload)
    pytest.assume(response.status_code == 400)
    pytest.assume(
        response.json()["detail"]
        == "Er is al een uitnodiging gestuurd naar dit email adres"
    )


@pytest.mark.asyncio
def test_add_email_to_allowed_users_with_invalid_email(test_client: TestClient):
    # Get admin access token
    response = test_client.post(
        "api/auth/login",
        headers={},
        data={"username": "admin@admin.com", "password": "admin"},
        files=[],
    )
    admin_access_token = response.json()["access_token"]
    # Create payload, headers and make the response
    payload = json.dumps(
        {
            "email": "test_gebruiker@testcom",
        }
    )
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {admin_access_token}",
        "Content-Type": "application/json",
    }
    response = test_client.post("api/allowed_users/", headers=headers, data=payload)
    pytest.assume(response.status_code == 422)
    pytest.assume(
        response.json()["detail"][0]["msg"] == "value is not a valid email address"
    )
    pytest.assume(response.json()["detail"][0]["type"] == "value_error.email")


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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
