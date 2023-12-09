from pydantic import BaseModel
from typing import List
from auth.models import Roles
from pathlib import Path


class CreateUser(BaseModel):
    username: str
    hash_password: str
    email: str
    
class GetUserByEmail(BaseModel):
    email: str

class GetUserByUsername(BaseModel):
    username: str


class LoginForm(BaseModel):
    login: str
    password: str

class TokenInfo(BaseModel):
    access_token: str
    token_type: str