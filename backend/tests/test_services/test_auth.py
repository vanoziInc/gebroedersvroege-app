import re

import pytest
from app.config import Settings
from app.models.tortoise import Users
from app.services.auth import Auth, get_current_user
from fastapi import Depends
from jose import jwt
from tests.conftest import get_settings_override


def test_password_hash_generation():
    hashed_password = Auth.get_password_hash(password="secretstring")
    assert hashed_password != "secretstring"


def test_password_verification():
    hashed_password = Auth.get_password_hash(password="secretstring")
    assert Auth.verify_password(
        plain_password="secretstring", hashed_password=hashed_password)


def test_get_token():
    token: str = Auth.get_token(
        data={"email": "test@test.com"}, expires_delta=10)
    assert token.startswith("ey")


def test_get_confirmation_token(settings: Settings = get_settings_override()):
    # set regex pattern for uuid4
    re_pattern_uuid4 = '[0-9a-f]{32}\Z'
    confirmation_token = Auth.get_confirmation_token(email="test@test.com")
    assert len(confirmation_token["jti"]) == 32
    assert re.search(re_pattern_uuid4, confirmation_token["jti"])
    decrypted_token = jwt.decode(
        confirmation_token["token"], settings.secret_key, algorithms=settings.token_algorithm
    )
    assert decrypted_token.get("sub") == "test@test.com"
    assert decrypted_token.get("scope") == "registration"
    assert len(decrypted_token.get("jti")) == 32
    assert re.search(re_pattern_uuid4, decrypted_token.get("jti"))


def test_get_access_token(settings: Settings = get_settings_override()):
    # set regex pattern for uuid4
    re_pattern_uuid4 = '[0-9a-f]{32}\Z'
    access_token = Auth.get_access_token(email="test@test.com")
    assert len(access_token["jti"]) == 32
    assert re.search(re_pattern_uuid4, access_token["jti"])
    decrypted_token = jwt.decode(
        access_token["token"], settings.secret_key, algorithms=settings.token_algorithm
    )
    assert decrypted_token.get("sub") == "test@test.com"
    assert decrypted_token.get("scope") == "login"
    assert len(decrypted_token.get("jti")) == 32
    assert re.search(re_pattern_uuid4, decrypted_token.get("jti"))

