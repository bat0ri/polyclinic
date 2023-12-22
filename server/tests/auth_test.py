import pytest
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from auth.hashing import BcryptHasher
from auth.models import User, Roles
from conftest import client, async_session_maker
from unittest.mock import MagicMock, patch
from fastapi import HTTPException



async def test_add_user():
    async with async_session_maker() as session:
        password = "password"
        hashed_password = BcryptHasher.get_password_hash(password)

        new_user_data = {
            "username": "test_user",
            "hash_password": hashed_password,
            "email": "test@example.com",
            "is_active": True,
            "roles": [Roles.ROLE_PACIENT.value],
            "create_date": datetime.now(),
            "update_date": None
        }

        new_user = User(**new_user_data)
        session.add(new_user)
        await session.commit()

        query = select(User)
        result = await session.execute(query)
        fetched_user = result.scalars().first()

        assert fetched_user.username == new_user_data["username"]
        assert BcryptHasher.verify_password(password, fetched_user.hash_password)
        assert fetched_user.email == new_user_data["email"]
        assert fetched_user.is_active == new_user_data["is_active"]
        assert fetched_user.roles == new_user_data["roles"]
        assert fetched_user.create_date == new_user_data["create_date"]
        assert fetched_user.update_date == new_user_data["update_date"]



def test_user_properties():
    new_user_data = {
        "username": "test_user",
        "hash_password": "password",
        "email": "test@example.com",
        "is_active": True,
        "roles": [Roles.ROLE_DOCTOR.value],
        "create_date": datetime.now(),
        "update_date": None
    }

    new_user = User(**new_user_data)
    assert new_user.is_superadmin is False
    assert new_user.is_doctor is True



