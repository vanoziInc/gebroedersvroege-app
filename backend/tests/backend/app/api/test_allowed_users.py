import pytest, json

from fastapi.testclient import TestClient
from app.models.pydantic import AllowedUsersCreateSchema

pytestmark = pytest.mark.anyio


@pytest.mark.apitest
async def test_add_allowed_users(test_client: TestClient, request_headers_admin: dict):
    payload = AllowedUsersCreateSchema(email="test_gebruiker@test.com").json()
    response = await test_client.post(
        "/allowed_users/", headers=request_headers_admin, data=payload
    )
    pytest.assume(response.status_code == 201)
    pytest.assume(response.json()["id"])
    pytest.assume(response.json()["created_at"])
    pytest.assume(response.json()["last_modified_at"])
    pytest.assume(response.json()["email"] == "test_gebruiker@test.com")


@pytest.mark.apitest
async def test_add_allowed_users_invalid_email_address(
    test_client: TestClient, request_headers_admin: dict
):
    payload = json.dumps(
        {
            "email": "test_gebruiker@testcom",
        }
    )
    response = await test_client.post(
        "/allowed_users/", headers=request_headers_admin, data=payload
    )
    pytest.assume(response.status_code == 422)
    pytest.assume(
        response.json()["detail"][0]["msg"] == "value is not a valid email address"
    )
    pytest.assume(response.json()["detail"][0]["type"] == "value_error.email")


@pytest.mark.apitest
async def test_allowed_user_allready_invited(
    test_client: TestClient, request_headers_admin: dict
):
    payload = AllowedUsersCreateSchema(email="test_gebruiker@test.com").json()
    response = await test_client.post(
        "/allowed_users/", headers=request_headers_admin, data=payload
    )
    pytest.assume(response.status_code == 400)
    pytest.assume(
        response.json()["detail"]
        == "Er is al een uitnodiging gestuurd naar dit email adres"
    )

@pytest.mark.apitest
async def test_allowed_user_allready_registered(
    test_client: TestClient, request_headers_admin: dict
):
    payload = AllowedUsersCreateSchema(email="werknemer@werknemer.com").json()
    response = await test_client.post(
        "/allowed_users/", headers=request_headers_admin, data=payload
    )
    pytest.assume(response.status_code == 400)
    pytest.assume(
        response.json()["detail"]
        == "Dit email adres is al geregistreerd"
    )



@pytest.mark.apitest
async def test_add_allowed_users_insufficient_privilege(test_client: TestClient, request_headers_werknemer: dict):
    payload = AllowedUsersCreateSchema(email="werknemer@werknemer.com").json()
    response = await test_client.post(
        "/allowed_users/", headers=request_headers_werknemer, data=payload
    )
    pytest.assume(response.status_code == 403)
    pytest.assume(
        response.json()["detail"]
        == "Operation not permitted"
    )
