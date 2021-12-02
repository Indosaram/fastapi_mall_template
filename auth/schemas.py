from typing import Optional

from pydantic import BaseModel


class Login(BaseModel):
    name: str
    password: str

    class Config:
        schema_extra = {"example": {"name": "indo", "password": "projex"}}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Optional[str] = None
