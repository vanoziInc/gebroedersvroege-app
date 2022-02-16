from pathlib import Path
import PIL, pytest
from fastapi.testclient import TestClient

# Post
# Tests
# 1 incorrect document type
# 2 fout bij valideren data
@pytest.mark.dev
async def test_add_bouwplan_with_invalid_document_type(
    test_client: TestClient, admin_token: str, tmp_path
):
    files=[
    ('in_file',('python_logo.jpeg',open('./tests/backend/app/api/data/python_logo.jpeg','rb'),'image/jpeg'))
    ]
    # files=[
    # ('in_file',('bouwplan_2022.xlsx',open('./bouwplan_2022.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    # ]
    headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {admin_token}'
    }
    params = {"year":"2022"}
    response = await test_client.post("/bouwplan/upload",params=params, headers=headers, files=files)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Ongeldig document type'}
