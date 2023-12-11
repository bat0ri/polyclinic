import jwt
from datetime import datetime, timedelta
from pathlib import Path
from fastapi.security import HTTPBearer,  HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, Depends, status
from auth.repository import UserRepo
from config import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


def encode_jwt(payload: dict, expire_minutes: int = 10):
    private_key_path = Path("auth/certs/jwt-private.pem")
    

    if not private_key_path.is_file():
        raise FileNotFoundError("Private key file not found")
    
    private_key = private_key_path.read_text()

    to_encode = payload.copy()
    now = datetime.utcnow()
    expiration_time = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expiration_time,
        iat=now
    )
    encoded = jwt.encode(to_encode, private_key, algorithm="RS256")
    return encoded


def decode_jwt(token):
    public_key_path = Path("auth/certs/jwt-public.pem")

    if not public_key_path.is_file():
        raise FileNotFoundError("Public key file not found")

    public_key = public_key_path.read_text()

    decoded = jwt.decode(token, public_key, algorithms=["RS256"])
    return decoded


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str):
        is_token_valid = False

        try:
            payload = decode_jwt(jwt_token)
            is_token_valid = True
        except jwt.ExpiredSignatureError:
            is_token_valid = False
        except jwt.InvalidTokenError:
            is_token_valid = False
        return is_token_valid


class RoleBasedJWTBearer(JWTBearer):
    async def __call__(self, request: Request):
        jwt_token = await super().__call__(request)
        if jwt_token:
            payload = decode_jwt(jwt_token)
            user_roles = payload.get("roles", [])

            if "ROLE_DOCTOR" in user_roles:
                return jwt_token
            elif "ROLE_PATIENT" in user_roles:
                raise HTTPException(status_code=403, detail="Вы не доктор")
            else:
                raise HTTPException(status_code=403, detail="ошибка роли")
        else:
            raise HTTPException(status_code=403, detail="ошибка токена")


async def get_current_user(token: str = Depends(JWTBearer()), 
                            session: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception

    payload = decode_jwt(token)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    async with UserRepo(session) as repository:
        user = await repository.get_user_by_username(username)

    return user