import jwt
from datetime import datetime, timedelta
from pathlib import Path
from fastapi.security import HTTPBearer,  HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, Depends


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

