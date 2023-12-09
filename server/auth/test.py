from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Примеры пользователей (в реальности используй базу данных или ORM)
users = {
    "user1": {
        "username": "user1",
        "password": "password1",
    }
}

# Функция для создания JWT токена
def create_jwt_token(data, secret_key, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

# Функция для проверки пароля
def verify_password(username: str, password: str):
    if username not in users or users[username]["password"] != password:
        return False
    return True

# Функция для получения пользователя по имени
def get_user(username: str):
    if username in users:
        return users[username]
    return None

# Регистрация пользователя
@app.post("/register")
async def register(username: str, password: str):
    # В реальности добавь сохранение пользователя в базу данных или ORM
    users[username] = {"username": username, "password": password}
    return {"message": "User registered successfully"}


@app.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if not verify_password(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создание JWT токена и установка его в куки
    access_token_expires = timedelta(minutes=30)
    access_token = create_jwt_token(
        data={"sub": username}, secret_key="secret_key", expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token)

    return {"access_token": access_token, "token_type": "bearer"}

# Защищенный эндпоинт, требующий JWT токен
@app.get("/protected")
async def protected_route(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, "secret_key", algorithms=["HS256"])
        username = decoded_token.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = get_user(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"message": "Access granted", "user": user}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Выход - удаление токена из куков
@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
