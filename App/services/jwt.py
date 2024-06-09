import jwt
from datetime import datetime, timedelta, timezone
from fastapi import status, Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from .constant import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from app.exception import ReverseBitException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# generate hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# validate password
def verify_password(plain_password, hashed_password):
    is_valid_password = pwd_context.verify(plain_password, hashed_password)
    if not is_valid_password:
        raise ReverseBitException(
            message="Invalid Password.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return True


# Generate Refresh Token
def generate_refresh_token(email):
    expires_delta = timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
    payload = {
        "username": email,
        "exp": datetime.utcnow() + expires_delta,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def create_access_token(email):
    expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "username": email,
        "exp": datetime.utcnow() + expires_delta,  # Access token expires in 15 minutes
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_access_refresh_token(email):
    access_token = create_access_token(email=email)
    refresh_token = generate_refresh_token(email=email)

    response = {
        "access_token": access_token,
        "access_token_expiry_in_minutes": int(ACCESS_TOKEN_EXPIRE_MINUTES),
        "refresh_token": refresh_token,
        "refresh_token_expiry_in_minutes": int(REFRESH_TOKEN_EXPIRE_MINUTES),
    }
    return response


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise Exception("Invalid user")
        return username
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authenticated.",
        )
