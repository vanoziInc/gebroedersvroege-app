import json
from unicodedata import category

import pytest
from app.models.pydantic import MachineCreateSchema
from fastapi.testclient import TestClient

pytestmark = pytest.mark.anyio


@pytest.mark.apitest
@pytest.mark.dev
async def test_add_machine(test_client: TestClient, admin_token: str):
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }
    payload = MachineCreateSchema(
        work_number="M24",
        work_name="Test Machine",
        category="Trekker",
        brand_name="John Deere",
        type_name="7810",
        licence_number="MM-11-XX",
    ).json()
    response = await test_client.put("/machines/", headers=headers, content=payload)
    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["created_at"]
    assert response.json()["last_modified_at"]
    # Check if email has been send out correctly
    assert response.json()["work_number"] == "M24"
    assert response.json()["work_name"] == "Test Machine"
    assert response.json()["category"] == "Trekker"
    assert response.json()["brand_name"] == "John Deere"
    assert response.json()["type_name"] == "7810"
    assert response.json()["licence_number"] == "MM-11-XX"

@pytest.mark.apitest
@pytest.mark.dev
async def test_update_machine(test_client: TestClient, admin_token: str):
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }
    payload = MachineCreateSchema(
        work_number="M24",
        work_name="Test Machine",
        category="Trekker",
        brand_name="Fendt",
        type_name="7810",
        licence_number="MM-11-XX",
    ).json()
    response = await test_client.put("/machines/", headers=headers, content=payload)
    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["created_at"]
    assert response.json()["last_modified_at"]
    # Check if email has been send out correctly
    assert response.json()["work_number"] == "M24"
    assert response.json()["work_name"] == "Test Machine"
    assert response.json()["category"] == "Trekker"
    assert response.json()["brand_name"] == "Fendt"
    assert response.json()["type_name"] == "7810"
    assert response.json()["licence_number"] == "MM-11-XX"

@pytest.mark.apitest
@pytest.mark.dev
async def test_get_single_machine(test_client: TestClient, werknemer_token: str):
    headers = {
        "Authorization": f"Bearer {werknemer_token}",
        "Content-Type": "application/json",
    }
    response = await test_client.get("/machines/1", headers=headers)
    assert response.status_code == 200

@pytest.mark.apitest
@pytest.mark.dev
async def test_get_all_machines(test_client: TestClient, werknemer_token: str):
    headers = {
        "Authorization": f"Bearer {werknemer_token}",
        "Content-Type": "application/json",
    }
    response = await test_client.get("/machines/", headers=headers)
    assert response.status_code == 200

