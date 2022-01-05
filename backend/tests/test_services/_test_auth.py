import re

import pytest
from app.config import Settings
from app.models.tortoise import Users
from app.services.auth import Auth, get_current_user
from fastapi import Depends
from jose import jwt
from tests.conftest import get_settings_override


def test_password_hash_generation_with_valid_password():
    """Tests Auth.get_password_hash with a password length greater than 0"""
    hashed_password = Auth.get_password_hash(password="secretstring")
    assert hashed_password != "secretstring"


def test_password_hash_generation_with_empty_password():
    """Tests Auth.get_password_hash with a password length of 0"""
    hashed_password = Auth.get_password_hash(password="")
    assert hashed_password != ""


def test_password_verification_plain_password_is_equal_to_hashed_password():
    """Tests Auth.verify_password whereby plain password corresponds with hashed password"""
    hashed_password = Auth.get_password_hash(password="secretstring")
    assert Auth.verify_password(
        plain_password="secretstring", hashed_password=hashed_password
    )


def test_password_verification_plain_password_is_not_equal_to_hashed_password():
    """Tests Auth.verify_password whereby plain password does not correspond with hashed password"""
    hashed_password = Auth.get_password_hash(password="secretstring")
    assert (
        Auth.verify_password(
            plain_password="secretstring_mismatch", hashed_password=hashed_password
        )
        is False
    )


def test_password_verification_with_plain_password_equal_to_None():
    """Tests Auth.verify_password whereby plain password is None raises an Exception"""
    hashed_password = Auth.get_password_hash(password="secretstring")
    with pytest.raises(Exception) as e_info:
        Auth.verify_password(plain_password=None, hashed_password=hashed_password)


def test_generation_of_token():
    """Tests Auth.get_token Token generation with email address"""
    token: str = Auth.get_token(data={"email": "test@test.com"}, expires_delta=10)
    assert token.startswith("ey")


def test_get_confirmation_token(settings: Settings = get_settings_override()):
    # set regex pattern for uuid4
    re_pattern_uuid4 = "[0-9a-f]{32}\Z"
    confirmation_token = Auth.get_confirmation_token(email="test@test.com")
    assert len(confirmation_token["jti"]) == 32
    assert re.search(re_pattern_uuid4, confirmation_token["jti"])
    decrypted_token = jwt.decode(
        confirmation_token["token"],
        settings.secret_key,
        algorithms=settings.token_algorithm,
    )
    assert decrypted_token.get("sub") == "test@test.com"
    assert decrypted_token.get("scope") == "registration"
    assert len(decrypted_token.get("jti")) == 32
    assert re.search(re_pattern_uuid4, decrypted_token.get("jti"))


# def test_get_access_token(settings: Settings = get_settings_override()):
#     # set regex pattern for uuid4
#     re_pattern_uuid4 = "[0-9a-f]{32}\Z"
#     access_token = Auth.get_access_token(email="test@test.com")
#     assert len(access_token["jti"]) == 32
#     assert re.search(re_pattern_uuid4, access_token["jti"])
#     decrypted_token = jwt.decode(
#         access_token["token"], settings.secret_key, algorithms=settings.token_algorithm
#     )
#     assert decrypted_token.get("sub") == "test@test.com"
#     assert decrypted_token.get("scope") == "login"
#     assert len(decrypted_token.get("jti")) == 32
#     assert re.search(re_pattern_uuid4, decrypted_token.get("jti"))
