import json
import uuid

import pytest
from app.models.tortoise import Roles
from fastapi.testclient import TestClient
import asyncio

def test_registration(test_client: TestClient):
    return True


def test_registration(test_client: TestClient):
    payload = 'email=elma%40test.com&password=elma123%24%25'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = test_client.post(
        "api/auth/register", headers=headers, data=payload)

    assert response.status_code == 201
    assert response.json()["email"] == "elma@test.com"
    assert response.json()["is_active"] == False
    assert len(response.json()["roles"]) == 1
    assert response.json()["roles"][0]["name"] == "henk"