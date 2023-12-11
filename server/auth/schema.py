from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from auth.models import Roles
from pathlib import Path
from fastapi import Form
from auth.models import Roles


class CreateUser(BaseModel):
    username: str
    hash_password: str
    email: str
    
class GetUserByEmail(BaseModel):
    email: EmailStr

class GetUserByUsername(BaseModel):
    username: str

class RegistrationUser(BaseModel):
    email: EmailStr = Field("user@email.com", description="Email")
    password: str = Field("pass", description="пароль")
    username: str = Field("username", description="Имя пользователя")
    
    phone_number: Optional[str] = Field(None, description="Номер телефона")
    first_name: Optional[str] = Field(None, description="Имя")
    last_name: Optional[str] = Field(None, description="Фамилия")
    roles: Roles = Roles.ROLE_PACIENT

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Имя пользователя должно содержать только буквы и цифры')
        return v

    #@validator('phone_number')
    #def validate_phone_number(cls, v):
    #    if v and not v.startswith('+7') or not v[1:].isdigit() or len(v) != 12:
    #        raise ValueError('Номер телефона должен быть в формате +7XXXXXXXXXX')
    #    return v

    class Config:
        from_attributes = True


class LoginForm(BaseModel):
    username: str
    password: str

class TokenInfo(BaseModel):
    access_token: str
    token_type: str