from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from auth.token import verify_token

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(OAUTH2_SCHEME)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
