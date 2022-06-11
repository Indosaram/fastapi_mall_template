import os
import datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError, jwt

from auth.schemas import TokenData

load_dotenv()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict, expires_delta: Optional[datetime.timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        return TokenData(name=name)
    except JWTError:
        raise credentials_exception
